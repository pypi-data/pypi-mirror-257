from typing import Any, Dict, List

import requests

from launchflow.clients.response_schemas import (
    OperationResponse,
    ResourceConnectionResponse,
    ResourceResponse,
)
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class ResourcesClient:

    def base_url(self, project_name: str, environment_name: str) -> str:
        return f"{config.settings.launch_service_address}/projects/{project_name}/environments/{environment_name}/resources"  # noqa: E501

    def create(
        self,
        project_name: str,
        environment_name: str,
        provider_product_type: str,
        resource_name: str,
        create_args: Dict[str, Any],
    ):
        response = requests.post(
            f"{self.base_url(project_name, environment_name)}/{provider_product_type}/{resource_name}",
            json=create_args,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 201:
            raise LaunchFlowRequestFailure(response)
        return OperationResponse.model_validate(response.json())

    def replace(
        self,
        project_name: str,
        environment_name: str,
        provider_product_type: str,
        resource_name: str,
        create_args: Dict[str, Any],
    ):
        response = requests.put(
            f"{self.base_url(project_name, environment_name)}/{provider_product_type}/{resource_name}",
            json=create_args,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 201:
            raise LaunchFlowRequestFailure(response)
        return OperationResponse.model_validate(response.json())

    def connect(
        self,
        project_name: str,
        environment_name: str,
        provider_product_type: str,
        resource_name: str,
    ):
        response = requests.get(
            f"{self.base_url(project_name, environment_name)}/{provider_product_type}/{resource_name}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ResourceConnectionResponse.model_validate(response.json())

    def get(self, project_name: str, environment_name: str, resource_name: str):
        url = f"{self.base_url(project_name, environment_name)}/{resource_name}"
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ResourceResponse.model_validate(response.json())

    def list(self, project_name: str, environment_name: str) -> List[ResourceResponse]:
        url = f"{self.base_url(project_name, environment_name)}"
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return [
            ResourceResponse.model_validate(resource)
            for resource in response.json()["resources"]
        ]

    def delete(self, project_name: str, environment_name: str, resource_name: str):
        url = f"{self.base_url(project_name, environment_name)}/{resource_name}"
        response = requests.delete(
            url,
            headers={"Authorization": f"Bearer {config.credentials.access_token}"},
        )
        if response.status_code != 202:
            raise LaunchFlowRequestFailure(response)
        return OperationResponse.model_validate(response.json())
