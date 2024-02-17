import requests

from launchflow.clients.response_schemas import EnvironmentResponse
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class EnvironmentsClient:
    def base_url(self, project_name: str) -> str:
        return f"{config.settings.launch_service_address}/projects/{project_name}/environments"

    def create(self, project_name: str, env_name: str):
        body = {
            "name": env_name,
        }
        response = requests.post(
            self.base_url(project_name),
            json=body,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return EnvironmentResponse.model_validate(response.json())

    def get(self, project_name: str, env_name: str):
        url = f"{self.base_url(project_name)}/{env_name}"
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return EnvironmentResponse.model_validate(response.json())

    def list(self, project_name):
        response = requests.get(
            self.base_url(project_name),
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return [
            EnvironmentResponse.model_validate(env)
            for env in response.json()["environments"]
        ]
