import asyncio
import sys
from typing import List, Optional, Tuple

import beaupy
import deepdiff
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow.cli.utils import import_from_string
from launchflow.clients import launchflow_client
from launchflow.clients.response_schemas import (
    OperationStatus,
    ResourceConnectionResponse,
    ResourceResponse,
)
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.resource import Resource


def compare_dicts(d1, d2):
    return "\n        ".join(
        deepdiff.DeepDiff(d1, d2)
        .pretty()
        # NOTE: we replace these so rich doesn't get upset
        .replace("[", "{")
        .replace("]", "}")
        .replace("root", "")
        .split("\n")
    )


def _print_operation_status(
    progress: Progress,
    status: Optional[OperationStatus],
    resource: Resource,
    operation_type: str,
):
    if status is None:
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} status unknown for [blue]{resource}[/blue]"
        )
    elif status.is_success():
        progress.console.print(
            f"[green]✓[/green] {operation_type} successful for [blue]{resource}[/blue]"
        )
        return True
    elif status.is_error():
        progress.console.print(
            f"[red]✗[/red] {operation_type} failed for [blue]{resource}[/blue]"
        )
    elif status.is_cancelled():
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} cancelled for [blue]{resource}[/blue]"
        )
    else:
        progress.console.print(
            f"[yellow]?[/yellow] {operation_type} status unknown for [blue]{resource}[/blue]"
        )
    return False


async def _monitor_create_resource_operations(
    project: str, environment: str, resource_to_create: List[Tuple[Resource, bool]]
):
    # Add a new line here to make output a little cleaner
    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        operations = []
        task_to_resource = {}
        for resource, replace in resource_to_create:
            if replace:
                op_type = "Replacing"
                method = launchflow_client.resources.replace
            else:
                op_type = "Creating"
                method = launchflow_client.resources.create
            task = progress.add_task(f"{op_type} [blue]{resource}[/blue]...", total=1)
            task_to_resource[task] = (resource, replace)
            operations.append(
                (
                    method(
                        project_name=project,
                        environment_name=environment,
                        provider_product_type=resource._provider_product_type,
                        resource_name=resource.name,
                        create_args=resource._create_args,
                    ),
                    task,
                )
            )
        create_successes = 0
        create_failures = 0
        replace_successes = 0
        replace_failures = 0
        while operations:
            await asyncio.sleep(3)
            to_stream_operations = []
            for operation, task in operations:
                status = launchflow_client.operations.get_operation_status(
                    operation_id=operation.id
                )
                if status.is_final():
                    progress.remove_task(task)
                    resource, replace = task_to_resource[task]

                    success = _print_operation_status(
                        progress,
                        status,
                        resource,
                        "Creation" if not replace else "Replacement",
                    )
                    if success:
                        resource_info = launchflow_client.resources.connect(
                            project_name=project,
                            environment_name=environment,
                            provider_product_type=resource._provider_product_type,
                            resource_name=resource.name,
                        )
                        resource._save_connection(resource_info.connection_info)
                        if replace:
                            replace_successes += 1
                        else:
                            create_successes += 1
                    else:
                        if replace:
                            replace_failures += 1
                        else:
                            create_failures += 1
                else:
                    to_stream_operations.append((operation, task))
            operations = to_stream_operations
        if create_successes:
            progress.console.print(
                f"[green]✓[/green] Successfully created {create_successes} resources"
            )
        if replace_successes:
            progress.console.print(
                f"[green]✓[/green] Successfully replaced {replace_successes} resources"
            )
        if create_failures:
            progress.console.print(
                f"[red]✗[/red] Failed to create {create_failures} resources"
            )
        if replace_failures:
            progress.console.print(
                f"[red]✗[/red] Failed to replace {replace_failures} resources"
            )


async def _monitor_delete_resource_operations(
    project: str,
    environment: str,
    resource_to_delete: List[ResourceResponse],
):
    # Add a new line here to make output a little cleaner
    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        operations = []
        task_to_resource = {}
        for resource in resource_to_delete:
            task = progress.add_task(f"Deleting [blue]{resource}[/blue]...", total=1)
            task_to_resource[task] = resource
            name = resource.name.split("/")[-1]
            operations.append(
                (
                    launchflow_client.resources.delete(
                        project_name=project,
                        environment_name=environment,
                        resource_name=name,
                    ),
                    task,
                )
            )
        successes = 0
        failures = 0
        while operations:
            await asyncio.sleep(3)
            to_stream_operations = []
            for operation, task in operations:
                status = launchflow_client.operations.get_operation_status(
                    operation_id=operation.id
                )
                if status.is_final():
                    progress.remove_task(task)
                    resource = task_to_resource[task]
                    success = _print_operation_status(
                        progress, status, resource, "Deletion"
                    )
                    if success:
                        successes += 1
                    else:
                        failures += 1
                else:
                    to_stream_operations.append((operation, task))
            operations = to_stream_operations
        if successes:
            progress.console.print(
                f"[green]✓[/green] Successfully deleted {successes} resources"
            )
        if failures:
            progress.console.print(
                f"[red]✗[/red] Failed to delete {failures} resources"
            )


def import_resources(resource_import_strs: List[str]) -> List[Resource]:
    sys.path.insert(0, "")
    resources: List[Resource] = []
    for resource_str in resource_import_strs:
        imported_resource = import_from_string(resource_str)
        if not isinstance(imported_resource, Resource):
            raise ValueError(f"Resource {resource_str} is not a valid Resource")
        resources.append(imported_resource)
    return resources


async def create(
    project: str, environment: str, *resources: List[Resource], prompt: bool = True
):
    # 1. Check which resources exist and whicn don't
    # TODO: do this async or maybe add a batch get endpoint
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            f"Loading application for: [bold yellow]`{project}/{environment}`[/bold yellow]",
        )
        new_resources = []
        replace_resources: List[Tuple[Resource, ResourceConnectionResponse]] = []
        for resource in resources:
            try:
                # Try to connect to all resources. If it fails for a 404, we know we need to create it.
                # Otherwise save the connection info.
                # TODO: check if we're replace if the create args don't match
                connection = launchflow_client.resources.connect(
                    project_name=project,
                    environment_name=environment,
                    resource_name=resource.name,
                    provider_product_type=resource._provider_product_type,
                )
                if connection.create_args != resource._create_args:
                    replace_resources.append((resource, connection))
                    continue
                resource._save_connection(connection.connection_info)
                progress.console.print(
                    f"[green]✓[/green] [blue]{resource}[/blue] already exists"
                )
            except LaunchFlowRequestFailure as e:
                if e.status_code == 404:
                    new_resources.append(resource)
                else:
                    raise e
        progress.remove_task(task)
    # 2. Prompt the user for what should be created
    to_run = []
    if not new_resources and not replace_resources:
        progress.console.print(
            "[green]✓[/green] All resources already exist. No action required."
        )
        return
    if prompt:
        options = []
        all_resources = []
        for resource in new_resources:
            options.append(f"[bold]Create[/bold]: [blue]{resource}[/blue]")
            all_resources.append((resource, False))
        for resource, connection in replace_resources:
            options.append(
                f"[bold]Replace[/bold]: [blue]{resource}[/blue]\n"
                f"    └── {compare_dicts(connection.create_args, resource._create_args)}"
            )
            all_resources.append((resource, True))
        rich.print(
            f"Select the resource operations you would like to perform in [bold yellow]`{project}/{environment}`[/bold yellow]:"
        )
        answers = beaupy.select_multiple(
            options, return_indices=True, ticked_indices=list(range(len(options)))
        )
        for answer in answers:
            resource, replace = all_resources[answer]
            rich.print(f"[pink1]>[/pink1] {options[answer]}")
            to_run.append((resource, replace))
        if not to_run:
            progress.console.print(
                "[green]✓[/green] No resources selected. No action required."
            )
            return
    else:
        for resource in new_resources:
            to_run.append((resource, False))
        for resource, connection in replace_resources:
            to_run.append((resource, True))

    # 3. Create the resources
    await _monitor_create_resource_operations(project, environment, to_run)


async def clean(
    project: str,
    environment: str,
    *local_resources: List[Resource],
    prompt: bool = True,
):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            f"Loading application for: [bold yellow]`{project}/{environment}`[/bold yellow]",
        )
        keyed_local_resources = {}
        for local_resource in local_resources:
            name = f"{project}/{environment}/{local_resource.name}"
            keyed_local_resources[name] = local_resource
        remote_resources = launchflow_client.resources.list(
            project_name=project,
            environment_name=environment,
        )

        to_delete_options = []
        for remote_resource in remote_resources:
            if (
                remote_resource.name not in keyed_local_resources
                and remote_resource.status == "ready"
            ):
                to_delete_options.append(remote_resource)
        progress.remove_task(task)
    to_delete = []
    if not to_delete_options:
        progress.console.print(
            "[green]✓[/green] No resources to delete. No action required."
        )
        return
    if prompt:
        rich.print(
            f"The following resources were unused in [bold yellow]`{project}/{environment}`[/bold yellow]. Select the resources you would like to [bold]delete[/bold]:"
        )
        options = [
            f"[bold]Delete[/bold]: [bold]{str(resource)}[/bold]"
            for resource in to_delete_options
        ]
        answers = beaupy.select_multiple(options, return_indices=True)
        for answer in answers:
            rich.print(
                f"[pink1]>[/pink1] Delete: [blue]{to_delete_options[answer]}[/blue]"
            )
            to_delete.append(to_delete_options[answer])
        if not to_delete:
            rich.print("[green]✓[/green] No resources selected. No action required.")
            return
    else:
        to_delete = to_delete_options
    await _monitor_delete_resource_operations(project, environment, to_delete)


def connect(project: str, environment: str, *resources: List[Resource]):
    if not resources:
        rich.print("[green]✓[/green] No resources to connect. No action required.")
        return
    for resource in resources:
        resource_info = launchflow_client.resources.connect(
            project,
            environment,
            resource._provider_product_type,
            resource.name,
        )
        resource._save_connection(resource_info.connection_info)
        rich.print(f"[green]✓[/green] Connected to {resource.name}")
    rich.print(f"[green]✓[/green] Successfully connected to {len(resources)} resources")
