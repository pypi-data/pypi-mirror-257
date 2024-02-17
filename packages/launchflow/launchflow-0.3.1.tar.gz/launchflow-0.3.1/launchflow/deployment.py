import enum
from typing import Union

from launchflow.docker import Dockerfile


class Provider(enum.Enum):
    GCP = "gcp"


class Deployment:
    def __init__(
        self,
        name: str,
        dockerfile: Union[str, Dockerfile] = "./Dockerfile",
        provider: Union[str, Provider] = "gcp",
    ) -> None:
        self.name = name

        if isinstance(dockerfile, str):
            dockerfile = Dockerfile.from_file(dockerfile)
        self.dockerfile = dockerfile

        if isinstance(provider, str):
            provider = Provider(provider)
        self.provider = provider
