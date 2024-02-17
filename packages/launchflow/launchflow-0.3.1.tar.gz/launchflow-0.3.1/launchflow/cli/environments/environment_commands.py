import typer

from launchflow.cli.utils import print_response
from launchflow.clients import launchflow_client
from launchflow.flows.environments_flows import create_environment
from launchflow.flows.project_flows import get_project

app = typer.Typer(help="Interact with your LaunchFlow environments.")


@app.command()
def create(
    name: str = typer.Argument(None, help="The environment name."),
    project: str = typer.Option(
        None, help="The project to create the environments in."
    ),
):
    """Create a new environment in a LaunchFlow project."""
    try:
        project_name = get_project(project)
        environment = create_environment(name, project_name)
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(1)

    print_response("Environment", environment.model_dump())


@app.command()
def list(
    project: str = typer.Option(None, help="The project to list environments for.")
):
    """List all environments in a LaunchFlow project."""
    try:
        project_name = get_project(project)
        environments = launchflow_client.environments.list(project_name)
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(1)

    print_response(
        "Environments", {"environments": [env.model_dump() for env in environments]}
    )


@app.command()
def get(
    name: str = typer.Argument(..., help="The environment name."),
    project: str = typer.Option(None, help="The project the environment is in."),
):
    """Get information about a specific environment."""
    try:
        project = get_project(project)
        environment = launchflow_client.environments.get(project, name)
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(1)

    print_response("Environment", environment.model_dump())
