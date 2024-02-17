import datetime
import enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


# TODO: figure out how to better parse enums so we can make these lowercase
class OperationStatus(enum.Enum):
    UNKNOWN = "UNKNOWN"
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    WORKING = "WORKING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

    def is_final(self):
        return self in [
            OperationStatus.SUCCESS,
            OperationStatus.FAILURE,
            OperationStatus.CANCELLED,
            OperationStatus.EXPIRED,
            OperationStatus.TIMEOUT,
            OperationStatus.INTERNAL_ERROR,
        ]

    def is_error(self):
        return self in [
            OperationStatus.FAILURE,
            OperationStatus.INTERNAL_ERROR,
            OperationStatus.TIMEOUT,
        ]

    def is_success(self):
        return self == OperationStatus.SUCCESS

    def is_cancelled(self):
        return self == OperationStatus.CANCELLED


class OperationResponse(BaseModel):
    id: str
    status: OperationStatus


class ResourceResponse(BaseModel):
    name: str
    resource_provider: str
    resource_product: str
    resource_type: str
    status: str
    # TODO: make this non-optional once the db is updated
    create_args: Optional[Dict[str, Any]]

    def __str__(self) -> str:
        return f"Resource(name='{self.name}', resource_product='{self.resource_product}', resource_type='{self.resource_type}'"


class ResourceConnectionResponse(ResourceResponse):
    connection_info: Dict[str, Any]


class ProjectResponse(BaseModel):
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class GCPEnvironmentConfigResponse(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    gcp_project_id: str
    gcp_service_account_email: str
    default_gcp_region: str
    default_gcp_zone: str


class EnvironmentResponse(BaseModel):
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    gcp_config: GCPEnvironmentConfigResponse
    resources: Dict[str, ResourceResponse] = {}


class AccountResponse(BaseModel):
    id: str


class GCPConnectionInfoResponse(BaseModel):
    verified_at: Optional[datetime.datetime]
    admin_service_account_email: str


class AWSConnectionInfoResponse(BaseModel):
    verified_at: Optional[datetime.datetime]
    external_role_id: str
    cloud_foundation_template_url: Optional[str]


class ConnectionInfoResponse(BaseModel):
    gcp_connection_info: GCPConnectionInfoResponse
    aws_connection_info: AWSConnectionInfoResponse
