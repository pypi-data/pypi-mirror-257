import requests

from launchflow.clients.response_schemas import AccountResponse
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class AccountsClient:
    # TODO: add caching so we don't look up the same account during a session.
    def __init__(self):
        self.url = f"{config.settings.account_service_address}/accounts"

    def list(self):
        response = requests.get(
            self.url,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return [
            AccountResponse.model_validate(account)
            for account in response.json()["accounts"]
        ]

    def get(self, account_id: str):
        response = requests.get(
            f"{self.url}/{account_id}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return AccountResponse.model_validate(response.json())
