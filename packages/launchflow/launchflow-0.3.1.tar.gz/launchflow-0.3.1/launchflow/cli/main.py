import asyncio
import os
import sys
import time
from typing import Optional

import beaupy
import requests
import rich
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

import launchflow
from launchflow.cli import project_gen
from launchflow.cli.accounts import account_commands
from launchflow.cli.cloud import cloud_commands
from launchflow.cli.config import config_commands
from launchflow.cli.contants import ENVIRONMENT_HELP, PROJECT_HELP
from launchflow.cli.environments import environment_commands
from launchflow.cli.project import project_commands
from launchflow.cli.resources import resource_commands
from launchflow.cli.resources_ast import find_launchflow_resources
from launchflow.cli.templates import infra_dot_py_template, main_template
from launchflow.cli.utils import import_from_string, tar_deployment_source_in_memory
from launchflow.config import config
from launchflow.deployment import Deployment
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.flows.auth import login_flow, logout_flow
from launchflow.flows.environments_flows import get_environment
from launchflow.flows.project_flows import get_project
from launchflow.flows.resource_flows import clean as clean_resources
from launchflow.flows.resource_flows import connect as connect_resources
from launchflow.flows.resource_flows import create as create_resources
from launchflow.flows.resource_flows import import_resources

app = typer.Typer(help="LaunchFlow CLI.")
app.add_typer(account_commands.app, name="accounts")
app.add_typer(project_commands.app, name="projects")
app.add_typer(environment_commands.app, name="environments")
app.add_typer(cloud_commands.app, name="cloud")
app.add_typer(resource_commands.app, name="resources")
app.add_typer(config_commands.app, name="config")


_SCAN_DIRECTORY_HELP = (
    "Directory to scan for resources. Defaults to the current working directory."
)


@app.command()
def init(
    directory: str = typer.Argument(".", help="Directory to initialize launchflow."),
    account_id: str = typer.Option(
        None,
        help="Account ID to use for this project. Defaults to the account ID set in the config.",
    ),
):
    """Initialize a new launchflow project."""
    try:
        project = project_gen.project(account_id)
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(1)

    full_directory_path = os.path.join(os.path.abspath(directory), project)
    while os.path.exists(full_directory_path):
        typer.echo(f"Directory `{full_directory_path}` already exists.")
        directory_name = beaupy.prompt("Enter a directory name for your project:")
        full_directory_path = os.path.join(os.path.abspath(directory), directory_name)

    framework = project_gen.framework()
    resources = project_gen.resources()
    infra = infra_dot_py_template.template(project, framework, resources)
    requirements = project_gen.requirements(framework, resources)
    main = main_template.template(framework, resources)

    os.makedirs(full_directory_path)
    infra_py = os.path.join(full_directory_path, "infra.py")
    main_py = os.path.join(full_directory_path, "main.py")
    requirements_txt = os.path.join(full_directory_path, "requirements.txt")

    with open(infra_py, "w") as f:
        f.write(infra)

    with open(main_py, "w") as f:
        f.write(main)

    with open(requirements_txt, "w") as f:
        f.write(requirements + "\n")

    print()
    print("Done!")
    print()
    print("To create your resources run:")
    rich.print("  $ [green]launchflow create")


@app.command()
def create(
    resource: str = typer.Argument(
        None,
        help="Resource to create. If none we will scan the directory for resources.",
    ),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
    scan_directory: str = typer.Option(".", help=_SCAN_DIRECTORY_HELP),
):
    """Create any resources that are not already created."""
    try:
        project = get_project(project, prompt_for_creation=True)
        environment = get_environment(
            project_name=project, environment_name=environment
        )
        if resource is None:
            resources = find_launchflow_resources(scan_directory)
        else:
            resources = [resource]
        with launchflow.allow(connection_failures=True):
            asyncio.run(
                create_resources(project, environment, *import_resources(resources))
            )
    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command()
def clean(
    scan_directory: str = typer.Option(".", help=_SCAN_DIRECTORY_HELP),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
):
    """Clean up any resources that are not in the current directory but are part of the project / environment."""
    try:
        project = get_project(project, prompt_for_creation=False)
        environment = get_environment(
            project_name=project,
            environment_name=environment,
            prompt_for_creation=False,
        )
        resources = find_launchflow_resources(scan_directory)
        with launchflow.allow(connection_failures=True):
            asyncio.run(
                clean_resources(project, environment, *import_resources(resources))
            )
    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command()
def connect(
    resource: str = typer.Argument(
        None,
        help="Resource to connect. If none we will scan the directory for all resources.",
    ),
    project: str = typer.Option(None, help="Project to connect to."),
    environment: str = typer.Option(None, help="Environment to connect to."),
    scan_directory: str = typer.Option(".", help=_SCAN_DIRECTORY_HELP),
):
    """Initialize connection information for resources."""
    try:
        project = get_project(project, prompt_for_creation=False)
        environment = get_environment(
            project_name=project,
            environment_name=environment,
            prompt_for_creation=False,
        )
        if resource is None:
            resources = find_launchflow_resources(scan_directory)
        else:
            resources = [resource]
        with launchflow.allow(connection_failures=True):
            connect_resources(project, environment, *import_resources(resources))
    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command(hidden=True)
def deploy(
    deployment: str = typer.Argument(..., help="Deployment to deploy."),
):
    """Deploy a deployment to your cloud."""
    sys.path.insert(0, "")
    deployment = import_from_string(deployment)
    if not isinstance(deployment, Deployment):
        typer.echo(f"{deployment} is not a launchflow.Deployment object")
        raise typer.Exit(1)

    tar_bytes = tar_deployment_source_in_memory(deployment)
    files = {"source": ("source.tar.gz", tar_bytes, "application/zip")}

    form_data = {"deployment": deployment.name}

    # TODO: Add a deployments client
    response = requests.put(
        f"{config.settings.launch_service_address}/projects/{launchflow._project}/environments/{launchflow._environment}/deploy",
        files=files,
        data=form_data,
    )
    if response.status_code == 200:
        typer.echo("Deployment successful!")
        operation_id = response.json()["id"]
        operation_status = response.json()["status"]
    else:
        raise RuntimeError(f"Failed to deploy: {response.reason}")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(f"Operation Status: {operation_status}\n", total=None)

        done = False
        while not done:
            response = requests.get(
                f"{config.settings.launch_service_address}/operations/{operation_id}",
            )
            if response.status_code == 200:
                operation = response.json()
                operation_status = operation["status"]
                if operation["status"] == "SUCCESS":
                    done = True
                elif operation["status"] == "FAILURE":
                    done = True
                else:
                    progress.update(
                        task, description=f"Operation Status: {operation_status}"
                    )
            else:
                raise RuntimeError(f"Failed to get operation: {response.reason}")
            time.sleep(1)

        progress.remove_task(task)
        if operation_status == "SUCCESS":
            progress.console.print("[green]✓[/green] Operation successful")
        if operation_status == "FAILURE":
            progress.console.print("[red]✗[/red] Operation failed")


@app.command()
def login():
    """Login to LaunchFlow. If you haven't signup this will create a free account for you."""
    try:
        login_flow()
    except Exception as e:
        typer.echo(f"Failed to login. {e}")
        typer.Exit(1)


@app.command()
def logout():
    """Logout of LaunchFlow."""
    try:
        logout_flow()
    except Exception as e:
        typer.echo(f"Failed to logout. {e}")
        typer.Exit(1)


if __name__ == "__main__":
    app()
