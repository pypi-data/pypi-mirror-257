import asyncio
from typing import Optional

import beaupy
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow.clients import launchflow_client
from launchflow.clients.response_schemas import EnvironmentResponse
from launchflow.exceptions import LaunchFlowRequestFailure


def get_environment(
    project_name: str, environment_name: Optional[str], prompt_for_creation: bool = True
) -> str:
    if environment_name is None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Fetching environments...", total=None)
            environments = launchflow_client.environments.list(project_name)
            progress.remove_task(task)
        environment_names = [f"{e.name}" for e in environments]
        if prompt_for_creation:
            environment_names.append("[i yellow]Create new environment[/i yellow]")
        print("Select the environment to use:")
        selected_environment = beaupy.select(environment_names, return_index=True)
        if prompt_for_creation and selected_environment == len(environment_names) - 1:
            environment = create_environment(
                environment_name=None, project_name=project_name
            )
            environment_name = environment.name.split("/")[-1]
        else:
            environment_name = environment_names[selected_environment]
            rich.print(f"[pink1]>[/pink1] {environment_name}")
        return environment_name
    try:
        # Fetch the project to ensure it exists
        _ = launchflow_client.environments.get(environment_name)
    except LaunchFlowRequestFailure as e:
        if e.status_code == 404 and prompt_for_creation:
            answer = beaupy.confirm(
                f"Environment `{environment_name}` does not yet exist. Would you like to create it?"
            )
            if answer:
                # TODO: this will just use their default account. Should maybe ask them.
                # But maybe that should be in the create project flow?
                environment = create_environment(environment_name, project_name)
                environment_name = environment.name.split("/")[-1]
            else:
                raise e
        else:
            raise e
    return environment_name


async def _monitor_env_creation(project_name: str, environment_name: str):
    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        # TODO: ideally the server would return the status updates but for now this is fine.
        gcp_proj_task = progress.add_task(
            "Creating GCP project for environment...", total=None
        )
        sa_task = progress.add_task(
            "Creating service account for environment...", total=None
        )
        apis_task = progress.add_task(
            "Enabling required APIs in GCP (this may take several minutes)...",
            total=None,
        )
        iam_task = progress.add_task(
            "Setting project IAM permissions for service account...", total=None
        )
        finished_tasks = set()

        def create_env():
            return launchflow_client.environments.create(project_name, environment_name)

        loop = asyncio.get_event_loop()
        coro = loop.run_in_executor(None, create_env)

        def mark_done(task: int, msg: str):
            progress.remove_task(task)
            progress.console.print(f"[green]✓[/green] {msg}")
            finished_tasks.add(task)

        while True:
            try:
                environment = await asyncio.wait_for(asyncio.shield(coro), timeout=3)
                break
            except asyncio.TimeoutError:
                if gcp_proj_task not in finished_tasks:
                    mark_done(gcp_proj_task, "GCP project successfully created.")
                    continue
                if sa_task not in finished_tasks:
                    mark_done(sa_task, "Service account successfully created.")
                    continue
                if iam_task not in finished_tasks:
                    mark_done(iam_task, "Project IAM permissions updated.")
                    continue
            except Exception as e:
                # Remove all tasks and print error message
                [progress.remove_task(t.id) for t in progress.tasks]
                progress.console.print("[red]✗[/red] Failed to create environment.")
                raise e
        mark_done(apis_task, "Required APIs successfully enabled.")
        progress.console.print("\n[green]✓[/green] Environment created successfully.")
        return environment


def create_environment(
    environment_name: Optional[str], project_name: str
) -> EnvironmentResponse:
    """Create a new environment in a project."""
    if environment_name is None:
        environment_name = beaupy.prompt("Enter the environment name:")
        rich.print(f"[pink1]>[/pink1] {environment_name}")

    return asyncio.run(_monitor_env_creation(project_name, environment_name))
