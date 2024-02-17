# ruff: noqa
from contextlib import asynccontextmanager, contextmanager

from launchflow.resource import Resource

from . import fastapi, gcp
from .flows.resource_flows import clean as _clean
from .flows.resource_flows import connect as _connect
from .flows.resource_flows import create as _create

# TODO: Add generic resource imports, like Postgres, StorageBucket, etc.
# This should probably live directly under launchflow, i.e. launchflow/postgres.py

_allow_connection_failures = False
_resources = []


@asynccontextmanager
async def create(project: str, env: str, prompt: bool = True):
    """Create resources in a project and environment.

    NOTE: this does not prompt for confirmation before creating resources / replacing.

    Args:
    - project (str): The name of the project.
    - env (str): The name of the environment.
    - prompt (bool): Whether to prompt for confirmation before creating / replacing resources. Defaults to True.

    Example:
    ```python
    import launchflow as lf

    async with lf.create("project", "env"):
        bucket = lf.gcp.GCSBucket("bucket-for-lf")
    ```
    """
    with allow(connection_failures=True):
        global _resources
        _resources = []
        yield
        if _resources:
            await _create(project, env, *_resources, prompt=prompt)


def connect(project: str, env: str, *resources: Resource):
    """Connect resources in a project and environment. This will store connection info for the resources in the environment.

    Args:
    - project (str): The name of the project.
    - env (str): The name of the environment.
    - resources (Resource): The resources to connect.

    Example:
    ```python
    import launchflow as lf

    with lf.create("project", "env):
        bucket = lf.gcp.GCSBucket("bucket-for-lf")

    lf.connect("project", "env", bucket)
    ```
    """
    _connect(project, env, *resources)


async def clean(project: str, env: str, *resources: Resource):
    """Clean resources in a project and environment. This will remove any resources that are part of the environment but not part of the resources list. This is the inverse of `create`.

    Args:
    - project (str): The name of the project.
    - env (str): The name of the environment.
    - resources (Resource): The resources to clean.

    Example:
    ```python
    import launchflow as lf

    with lf.create("project", "env):
        bucket = lf.gcp.GCSBucket("bucket-for-lf")

    lf.clean("project", "env", bucket)
    ```
    """
    await _clean(project, env, *resources)


@contextmanager
def allow(*, connection_failures=False):
    global _allow_connection_failures
    original_state = {"allow_connection_failures": _allow_connection_failures}
    try:
        _allow_connection_failures = connection_failures
        yield
    finally:
        _allow_connection_failures = original_state["allow_connection_failures"]
