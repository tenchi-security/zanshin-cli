from typing import List, Optional
from uuid import UUID

import typer
from zanshinsdk import AlertSeverity, Client, ScanTargetKind

import src.config.sdk as sdk_config
from src.lib.utils import dump_json

app = typer.Typer()


@app.command(name="scan_targets_following")
def summary_scan_targets_following(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_ids: Optional[List[UUID]] = typer.Option(
        None, help="Only summarize scan targets from the specified following ids"
    ),
    following_tags: Optional[List[str]] = typer.Option(
        None, help="Only summarize scan targets from the specified following tags"
    ),
    scan_target_kinds: Optional[List[ScanTargetKind]] = typer.Option(
        None, help="Only summarize scan targets from the specified kinds"
    ),
    alert_severities: Optional[List[AlertSeverity]] = typer.Option(
        None, help="Only summarize alerts with the specified severities"
    ),
    include_empty_following_tags: Optional[bool] = typer.Option(
        None, help="Include alerts from scan targets without tags"
    ),
):
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.get_scan_targets_following_summary(
            organization_id=organization_id,
            following_ids=following_ids,
            following_tags=following_tags,
            scan_target_kinds=scan_target_kinds,
            alert_severities=alert_severities,
            include_empty_following_tags=include_empty_following_tags,
        )
    )


@app.command(name="scan_targets_detail")
def summary_scan_targets_detail(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_ids: Optional[List[UUID]] = typer.Option(
        None, help="Only summarize scan targets from the specified scan target ids"
    ),
    scan_target_tags: Optional[List[str]] = typer.Option(
        None, help="Only summarize scan targets from the specified scan target tags"
    ),
    scan_target_kinds: Optional[List[ScanTargetKind]] = typer.Option(
        None, help="Only summarize scan targets from the specified kinds"
    ),
    alert_severities: Optional[List[AlertSeverity]] = typer.Option(
        None, help="Only summarize alerts with the specified severities"
    ),
):
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.get_scan_target_detail_summary(
            organization_id=organization_id,
            scan_target_ids=scan_target_ids,
            scan_target_tags=scan_target_tags,
            scan_target_kinds=scan_target_kinds,
            alert_severities=alert_severities,
        )
    )
