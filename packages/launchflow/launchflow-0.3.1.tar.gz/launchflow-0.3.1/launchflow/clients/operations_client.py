import time

import requests

from launchflow.clients.response_schemas import OperationResponse, OperationStatus
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class OperationsClient:
    def base_url(self) -> str:
        return f"{config.settings.launch_service_address}/operations"

    def stream_operation_status(self, operation_id: str):
        operation_status = OperationStatus.UNKNOWN

        while True:
            operation = self.get(operation_id)
            operation_status = operation.status

            if operation.status.is_final():
                break

            yield operation_status

            time.sleep(1)

        yield operation_status

    def get_operation_status(self, operation_id: str):
        operation = self.get(operation_id)
        return operation.status

    def get(self, operation_id: str):
        response = requests.get(
            f"{self.base_url()}/{operation_id}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return OperationResponse.model_validate(response.json())
