from launchflow.clients.accounts_client import AccountsClient
from launchflow.clients.connect_client import CloudConectClient
from launchflow.clients.environments_client import EnvironmentsClient
from launchflow.clients.operations_client import OperationsClient
from launchflow.clients.projects_client import ProjectsClient
from launchflow.clients.resources_client import ResourcesClient


class LaunchFlowClient:
    # TODO: add caching so we don't look up the same entities during a session.
    def __init__(self) -> None:
        self.accounts = AccountsClient()
        self.environments = EnvironmentsClient()
        self.projects = ProjectsClient()
        self.connect = CloudConectClient()
        self.resources = ResourcesClient()
        self.operations = OperationsClient()


launchflow_client = LaunchFlowClient()
