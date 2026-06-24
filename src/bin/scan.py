from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

app = typer.Typer()


@app.command(name="start")
def organization_scan_target_scan_start(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
    force: bool = typer.Option(
        False,
        help="Whether to force running a scan target that has state INVALID_CREDENTIAL or NEW",
    ),
):
    """
    Start a new scan on the specified scan target.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.start_organization_scan_target_scan(
            organization_id, scan_target_id, force
        )
    )


@app.command(name="stop")
def organization_scan_target_scan_stop(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
):
    """
    Stop a currently running scan on the specified scan target.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.stop_organization_scan_target_scan(organization_id, scan_target_id)
    )


@app.command(name="list")
def organization_scan_target_scan_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
):
    """
    List all scans performed on a specific scan target within an organization.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(
        client.iter_organization_scan_target_scans(organization_id, scan_target_id)
    )


@app.command(name="get")
def organization_scan_target_scan_get(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
    scan_id: UUID = typer.Argument(..., help="UUID of the scan"),
):
    """
    Get details of a specific scan performed on a scan target.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.get_organization_scan_target_scan(
            organization_id, scan_target_id, scan_id
        )
    )
