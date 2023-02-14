from typing import List, Optional
from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json

app = typer.Typer()


@app.command(name="alert")
def summary_alert(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: Optional[List[UUID]] = typer.Option(
        None,
        help="Only summarize alerts from the specified"
        "scan targets, defaults to all.",
    ),
):
    """
    Gets a summary of the current state of alerts for an organization, both in total and broken down by scan target.
    """
    client = Client(profile=sdk_config.profile)

    dump_json(client.get_alert_summaries(organization_id, scan_target_id))


@app.command(name="alert_following")
def summary_alert_following(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_ids: Optional[List[UUID]] = typer.Option(
        None,
        help="Only summarize alerts from the" "specified following, defaults to" "all.",
    ),
):
    """
    Gets a summary of the current state of alerts for followed organizations.
    """
    client = Client(profile=sdk_config.profile)

    dump_json(client.get_following_alert_summaries(organization_id, following_ids))


@app.command(name="scan")
def summary_scan(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_ids: Optional[List[UUID]] = typer.Option(
        None,
        help="Only summarize alerts from the specified"
        "scan targets, defaults to all.",
    ),
    days: Optional[int] = typer.Option(
        7, help="Number of days to go back in time in historical search"
    ),
):
    """
    Returns summaries of scan results over a period of time, summarizing number of alerts that changed states.
    """
    client = Client(profile=sdk_config.profile)

    dump_json(client.get_scan_summaries(organization_id, scan_target_ids, days))


@app.command(name="scan_following")
def summary_scan_following(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_ids: Optional[List[UUID]] = typer.Option(
        None,
        help="Only summarize alerts from the" "specified following, defaults to" "all.",
    ),
    days: Optional[int] = typer.Option(
        7, help="Number of days to go back in time in historical" "search"
    ),
):
    """
    Returns summaries of scan results over a period of time, summarizing number of alerts that changed states.
    """
    client = Client(profile=sdk_config.profile)

    dump_json(client.get_scan_summaries(organization_id, following_ids, days))
