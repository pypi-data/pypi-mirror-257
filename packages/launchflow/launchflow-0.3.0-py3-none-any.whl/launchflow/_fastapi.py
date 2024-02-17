import enum
import inspect
import os
from typing import Union

from fastapi import FastAPI

from launchflow.deployment import Deployment
from launchflow.docker import DockerfileBuilder


class ASGI(enum.Enum):
    Uvicorn = "uvicorn"
    Hypercorn = "hypercorn"
    Granian = "granian"


def _get_base_image() -> str:
    """Use the local Python version as the base image."""
    import sys

    version = sys.version_info
    return f"python:{version.major}.{version.minor}.{version.micro}-slim"


def _get_fastapi_entrypoint(app_instance: FastAPI) -> str:
    # Inspect where the FastAPI instance is defined
    for frame_info in inspect.stack():
        for var_name, var_val in frame_info.frame.f_globals.items():
            if var_val is app_instance:
                # Get the file path of the module where FastAPI instance is defined
                module_file_path = frame_info.filename

                # Convert file path to a module path
                root_path = (
                    os.getcwd()
                )  # Assuming the script is run from the project root
                relative_file_path = os.path.relpath(module_file_path, root_path)
                module_path = os.path.splitext(relative_file_path)[0].replace(
                    os.sep, "."
                )

                # Return the module path and the variable name
                return f"{module_path}:{var_name}"

    # If the instance is not found in the stack, raise an error or return a default value
    raise ValueError("FastAPI instance not found in the stack.")


def _get_command(asgi: ASGI, fastapi_app: FastAPI) -> str:
    """Return the command to run the FastAPI app."""
    entrypoint = _get_fastapi_entrypoint(fastapi_app)

    if asgi == ASGI.Uvicorn:
        return f"uvicorn {entrypoint} --port $PORT"
    elif asgi == ASGI.Hypercorn:
        return f"hypercorn {entrypoint} --bind 0.0.0.0:$PORT"
    elif asgi == ASGI.Granian:
        return f"granian --interface asgi {entrypoint} --port $PORT"


class FastAPIDeployment(Deployment):
    def __init__(
        self,
        fastapi_app: FastAPI,
        name: str,
        asgi: Union[str, ASGI] = "uvicorn",
        **kwargs,
    ) -> None:
        if isinstance(asgi, str):
            asgi = ASGI(asgi)

        dockerfile = kwargs.get("dockerfile", None)
        if dockerfile is None:
            dockerfile = DockerfileBuilder(
                base_image=_get_base_image(),
                # TODO: Add a requirements.txt file abstraction and use it here
                run_commands=["pip install fastapi"],
                command=_get_command(asgi, fastapi_app),
            ).build()
        kwargs["dockerfile"] = dockerfile

        super().__init__(name=name, **kwargs)
        self.fastapi_app = fastapi_app
        self.asgi = asgi
