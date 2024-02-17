import requests

from launchflow.clients.response_schemas import ProjectResponse
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class ProjectsClient:
    def __init__(self):
        self.url = f"{config.settings.launch_service_address}/projects"

    def create(self, project_name: str, cloud_provider: str, account_id: str):
        body = {
            "name": project_name,
            "cloud_provider": cloud_provider,
        }
        response = requests.post(
            f"{self.url}?account_id={account_id}",
            json=body,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ProjectResponse.model_validate(response.json())

    def get(self, project_name: str):
        response = requests.get(
            f"{self.url}/{project_name}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ProjectResponse.model_validate(response.json())

    def list(self, account_id: str):
        response = requests.get(
            f"{self.url}?account_id={account_id}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return [
            ProjectResponse.model_validate(project)
            for project in response.json()["projects"]
        ]
