import os
from typing import Any, Callable, Dict, Generic, Optional, TypeVar

import yaml

import launchflow
from launchflow import exceptions

T = TypeVar("T")


def write_resource_info_to_file(
    resource_name: str,
    connection_info: Dict[str, Any],
):
    resource_path = os.path.join(".launchflow", resource_name + ".yaml")
    os.makedirs(os.path.dirname(resource_path), exist_ok=True)
    with open(resource_path, "w") as f:
        yaml.dump(connection_info, f)


def read_resource_info_from_file(resource_name: str) -> Dict[str, Any]:
    resource_path = os.path.join(".launchflow", resource_name + ".yaml")
    if not os.path.exists(resource_path):
        raise exceptions.ConnectionInfoNotFound(resource_name=resource_name)
    with open(resource_path) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


class Resource(Generic[T]):

    # TODO: Consider adding project & environment overrides on the resource level
    def __init__(
        self,
        name: str,
        provider_product_type: str,
        create_args: dict,
    ) -> None:
        self.name = name
        self._provider_product_type = provider_product_type
        self._create_args = create_args
        launchflow._resources.append(self)

    def _save_connection(self, connection_info: Dict[str, Any]) -> None:
        # Save the connection info to a local file
        write_resource_info_to_file(self.name, connection_info)

    def _load_connection(self, parse_fn: Callable[[Dict[str, Any]], T]) -> Optional[T]:
        try:
            resource_info = read_resource_info_from_file(self.name)
        except exceptions.ConnectionInfoNotFound as e:
            if launchflow._allow_connection_failures:
                return None
            else:
                raise e
        return parse_fn(resource_info)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
