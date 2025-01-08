from json import dumps
from typing import List, Optional
from uuid import UUID

import typer
from zanshinsdk import (
    AlertSeverity,
    AlertsOrderOpts,
    AlertState,
    Client,
    Languages,
    SortOpts,
)
from zanshinsdk.alerts_history import FilePersistentAlertsIterator
from zanshinsdk.following_alerts_history import FilePersistentFollowingAlertsIterator

import src.config.sdk as sdk_config
from src.lib.models import AlertStateSetable
from src.lib.utils import output_iterable

app = typer.Typer()


@app.command(name="list")
def alert_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_ids: Optional[List[UUID]] = typer.Option(
        None, help="Only list alerts from the specified scan targets"
    ),
    scan_target_tags: Optional[List[str]] = typer.Option(
        None, help="Only lists alerts from the specified tags"
    ),
    include_empty_scan_target_tags: Optional[bool] = typer.Option(
        None, help="Include alerts without tags on the list"
    ),
    cursor: Optional[str] = typer.Option(None, help="Cursor for pagination"),
    order: Optional[AlertsOrderOpts] = typer.Option(
        AlertsOrderOpts.SEVERITY, help="Field to sort results on"
    ),
):
    """
    List alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(
        client.iter_alerts(
            organization_id=organization_id,
            scan_target_ids=scan_target_ids,
            scan_target_tags=scan_target_tags,
            include_empty_scan_target_tags=include_empty_scan_target_tags,
            cursor=cursor,
            order=order,
        )
    )


@app.command(name="list_following")
def alert_following_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_ids: Optional[List[UUID]] = typer.Option(
        None, help="Only list alerts from the specified scan targets"
    ),
    following_tags: Optional[List[UUID]] = typer.Option(
        None, help="Only lists alerts from the specified tags"
    ),
    include_empty_following_tags: Optional[bool] = typer.Option(
        None, help="Include alerts without tags on the list"
    ),
    cursor: Optional[str] = typer.Option(None, help="Cursor for pagination"),
    order: Optional[AlertsOrderOpts] = typer.Option(
        AlertsOrderOpts.SEVERITY, help="Field to sort results on"
    ),
):
    """
    List following alerts from a given organization, with optional filters by following ids, state or severity.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(
        client.iter_following_alerts(
            organization_id=organization_id,
            following_ids=following_ids,
            following_tags=following_tags,
            include_empty_following_tags=include_empty_following_tags,
            cursor=cursor,
            order=order,
        )
    )


@app.command(name="list_history")
def alert_history_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: Optional[List[UUID]] = typer.Option(
        None, help="Only list alerts from the specified scan targets"
    ),
    cursor: Optional[str] = typer.Option(None, help="Cursor for pagination"),
    persist: Optional[bool] = typer.Option(False, help="Persist"),
):
    """
    List alerts from a given organization, with optional filters by scan target, state or severity
    """
    client = Client(profile=sdk_config.profile)

    if persist:
        iter_alerts = FilePersistentAlertsIterator(
            filename="zanshin",
            client=client,
            organization_id=organization_id,
            scan_target_ids=scan_target_id,
            cursor=cursor,
        )
        output_iterable(iter_alerts, None, iter_alerts.save)
    else:
        output_iterable(
            client.iter_alerts_history(
                organization_id=organization_id,
                scan_target_ids=scan_target_id,
                cursor=cursor,
            )
        )


@app.command(name="list_history_following")
def alert_history_following_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_ids: Optional[List[UUID]] = typer.Option(
        None, help="Only list alerts from the specified scan targets"
    ),
    cursor: Optional[str] = typer.Option(None, help="Cursor for pagination"),
    persist: Optional[bool] = typer.Option(False, help="Persist"),
):
    """
    List alerts from a given organization, with optional filters by scan target, state or severity
    """
    client = Client(profile=sdk_config.profile)

    if persist:
        iter_alerts = FilePersistentFollowingAlertsIterator(
            filename="zanshin",
            client=client,
            organization_id=organization_id,
            following_ids=following_ids,
            cursor=cursor,
        )
        output_iterable(iter_alerts, None, iter_alerts.save)
    else:
        output_iterable(
            client.iter_alerts_following_history(
                organization_id=organization_id,
                following_ids=following_ids,
                cursor=cursor,
            )
        )


@app.command(name="list_grouped")
def grouped_alert_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: Optional[List[UUID]] = typer.Option(
        None, help="Only list alerts from the specified scan targets"
    ),
    state: Optional[List[AlertState]] = typer.Option(
        [
            x.value
            for x in AlertState
            if x != AlertState.CLOSED and x != AlertState.ACTIVE
        ],
        help="Only list alerts in the specified states",
        case_sensitive=False,
    ),
    severity: Optional[List[AlertSeverity]] = typer.Option(
        [x.value for x in AlertSeverity],
        help="Only list alerts with the specified severities",
        case_sensitive=False,
    ),
):
    """
    List grouped alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(
        client.iter_grouped_alerts(
            organization_id=organization_id,
            scan_target_ids=scan_target_id,
            states=state,
            severities=severity,
        )
    )


@app.command(name="list_grouped_following")
def grouped_alert_following_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_ids: Optional[List[UUID]] = typer.Option(
        None, help="Only list alerts from the specified scan targets"
    ),
    following_tags: Optional[List[UUID]] = typer.Option(
        None, help="Only lists alerts from the specified tags"
    ),
    include_empty_following_tags: Optional[bool] = typer.Option(
        None, help="Include alerts without tags on the list"
    ),
    cursor: Optional[str] = typer.Option(None, help="Cursor for pagination"),
    order: Optional[AlertsOrderOpts] = typer.Option(
        AlertsOrderOpts.SEVERITY, help="Field to sort results on"
    ),
):
    """
    List grouped following alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(
        client.iter_grouped_following_alerts(
            organization_id=organization_id,
            following_ids=following_ids,
            following_tags=following_tags,
            include_empty_following_tags=include_empty_following_tags,
            cursor=cursor,
            order=order,
        )
    )


@app.command(name="get")
def alert_get(
    alert_id: UUID = typer.Argument(..., help="UUID of the alert to look up"),
    list_history: Optional[bool] = typer.Option(False, help="History of this alert"),
    list_comments: Optional[bool] = typer.Option(False, help="Comments of this alert"),
):
    """
    Returns details about a specified alert
    """
    if list_history:
        client = Client(profile=sdk_config.profile)
        output_iterable(client.iter_alert_history(alert_id))
    elif list_comments:
        client = Client(profile=sdk_config.profile)
        output_iterable(client.iter_alert_comments(alert_id))
    else:
        client = Client(profile=sdk_config.profile)
        typer.echo(dumps(client.get_alert(alert_id), indent=4))


@app.command(name="update")
def alert_update(
    organization_id: UUID = typer.Argument(
        ..., help="UUID of the organization that owns the alert"
    ),
    scan_target_id: UUID = typer.Argument(
        ..., help="UUID of the scan target associated with the alert"
    ),
    alert_id: UUID = typer.Argument(..., help="UUID of the alert"),
    state: Optional[AlertStateSetable] = typer.Option(None, help="New alert state"),
    labels: Optional[List[str]] = typer.Option(
        None, help="Custom label(s) for the alert"
    ),
    comment: Optional[str] = typer.Option(
        None,
        help="A comment when setting the alert state to RISK_ACCEPTED, FALSE_POSITIVE, MITIGATING_CONTROL",
    ),
):
    """
    Updates the alert.
    """

    client = Client(profile=sdk_config.profile)
    typer.echo(
        client.update_alert(
            organization_id, scan_target_id, alert_id, state, labels, comment
        )
    )
