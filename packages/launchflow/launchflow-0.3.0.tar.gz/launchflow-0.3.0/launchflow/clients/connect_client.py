import requests

from launchflow.clients.response_schemas import (
    AWSConnectionInfoResponse,
    ConnectionInfoResponse,
    GCPConnectionInfoResponse,
)
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class CloudConectClient:
    def __init__(self):
        self.url = f"{config.settings.launch_service_address}/cloud/connect"

    def status(self, account_id: str, include_aws_template_url: bool = False):
        response = requests.get(
            f"{self.url}?account_id={account_id}&include_aws_template_url={include_aws_template_url}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ConnectionInfoResponse.model_validate(response.json())

    def connect_gcp(self, account_id: str):
        response = requests.post(
            f"{self.url}/gcp?account_id={account_id}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return GCPConnectionInfoResponse.model_validate(response.json())

    def connect_aws(self, account_id: str, aws_account_id: str):
        response = requests.post(
            f"{self.url}/aws?account_id={account_id}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
            json={"aws_account_id": aws_account_id},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return AWSConnectionInfoResponse.model_validate(response.json())
