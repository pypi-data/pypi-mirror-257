from launchflow.utils import get_failure_text


class LaunchFlowRequestFailure(Exception):
    def __init__(self, response) -> None:
        super().__init__(get_failure_text(response))
        self.status_code = response.status_code

    # TODO: use rich to make this pretty
    def pretty_print(self):
        print(self)


# TODO: Move "potential fix" messsages into the server.
# Server should return a json payload with a message per client type, i.e.
# {status: 409, message: "Conflict...", fix: {"cli": "Run this command..."}}
# Use details to return the fix payload:
# details = {message: "...", fix: {"cli": "Run this command..."}}
class ConnectionInfoNotFound(Exception):
    def __init__(self, resource_name: str) -> None:
        super().__init__(
            f"Connection info for resource '{resource_name}' not found. "
            f"\n\nPotential Fix:\nRun `launchflow create` to create the resource or "
            f"`launchflow connect` to connect to it.\n\n"
        )
