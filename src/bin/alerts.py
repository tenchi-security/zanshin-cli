from collections import defaultdict
from json import dumps
from typing import Dict, Iterator, List, Optional
from uuid import UUID

import typer
from zanshinsdk import (
    AlertSeverity,
    AlertsOrderOpts,
    AlertState,
    Client,
    GroupedAlertOrderOpts,
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
        None, help="Include alerts from scan targets without tags"
    ),
    states: Optional[List[AlertState]] = typer.Option(
        [
            x.value
            for x in AlertState
            if x != AlertState.CLOSED and x != AlertState.ACTIVE
        ],
        help="Only list alerts in the specified states",
        case_sensitive=False,
    ),
    severities: Optional[List[AlertSeverity]] = typer.Option(
        [x.value for x in AlertSeverity],
        help="Only list alerts with the specified severities",
        case_sensitive=False,
    ),
    lang: Optional[Languages] = typer.Option(
        Languages.EN_US.value,
        help="Show alert titles in the specified language",
        case_sensitive=False,
    ),
    created_at_start: Optional[str] = typer.Option(
        None, help="Date created starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    created_at_end: Optional[str] = typer.Option(
        None, help="Date created ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    updated_at_start: Optional[str] = typer.Option(
        None, help="Date updated starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    updated_at_end: Optional[str] = typer.Option(
        None, help="Date updated ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    search: Optional[str] = typer.Option("", help="Text to search for in the alerts"),
    sort: Optional[SortOpts] = typer.Option(None, help="Sort order"),
    rules: Optional[List[str]] = typer.Option(
        None, help="Only list alerts in the specified rules"
    ),
    opened_at_start: Optional[str] = typer.Option(
        None, help="Date opened starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    opened_at_end: Optional[str] = typer.Option(
        None, help="Date opened ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    resolved_at_start: Optional[str] = typer.Option(
        None, help="Date resolved starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    resolved_at_end: Optional[str] = typer.Option(
        None, help="Date resolved ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    cursor: Optional[str] = typer.Option(None, help="Cursor for pagination"),
    order: Optional[AlertsOrderOpts] = typer.Option(
        AlertsOrderOpts.SEVERITY, help="Field to sort results on"
    ),
    comments: bool = typer.Option(
        False, "--comments", help="Retrieve alerts with their comments"
    ),
):
    """
    List alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=sdk_config.profile)

    alerts = client.iter_alerts(
        organization_id=organization_id,
        scan_target_ids=scan_target_ids,
        scan_target_tags=scan_target_tags,
        include_empty_scan_target_tags=include_empty_scan_target_tags,
        cursor=cursor,
        order=order,
        rules=rules,
        states=states,
        severities=severities,
        lang=lang,
        opened_at_start=opened_at_start,
        opened_at_end=opened_at_end,
        resolved_at_start=resolved_at_start,
        resolved_at_end=resolved_at_end,
        created_at_start=created_at_start,
        created_at_end=created_at_end,
        updated_at_start=updated_at_start,
        updated_at_end=updated_at_end,
        search=search,
        sort=sort,
    )

    def alerts_with_comments():
        for alert in alerts:
            alert["comments"] = [
                comment["comment"]
                for comment in client.iter_alert_comments(alert["id"])
            ]
            yield alert

    output_iterable(alerts_with_comments() if comments else alerts)


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
        None, help="Include alerts from scan targets without tags"
    ),
    states: Optional[List[AlertState]] = typer.Option(
        [
            x.value
            for x in AlertState
            if x != AlertState.CLOSED and x != AlertState.ACTIVE
        ],
        help="Only list alerts in the specified states",
        case_sensitive=False,
    ),
    severities: Optional[List[AlertSeverity]] = typer.Option(
        [x.value for x in AlertSeverity],
        help="Only list alerts with the specified severities",
        case_sensitive=False,
    ),
    lang: Optional[Languages] = typer.Option(
        Languages.EN_US.value,
        help="Show alert titles in the specified language",
        case_sensitive=False,
    ),
    created_at_start: Optional[str] = typer.Option(
        None, help="Date created starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    created_at_end: Optional[str] = typer.Option(
        None, help="Date created ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    updated_at_start: Optional[str] = typer.Option(
        None, help="Date updated starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    updated_at_end: Optional[str] = typer.Option(
        None, help="Date updated ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    search: Optional[str] = typer.Option("", help="Text to search for in the alerts"),
    sort: Optional[SortOpts] = typer.Option(None, help="Sort order"),
    rules: Optional[List[str]] = typer.Option(
        None, help="Only list alerts in the specified rules"
    ),
    opened_at_start: Optional[str] = typer.Option(
        None, help="Date opened starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    opened_at_end: Optional[str] = typer.Option(
        None, help="Date opened ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    resolved_at_start: Optional[str] = typer.Option(
        None, help="Date resolved starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    resolved_at_end: Optional[str] = typer.Option(
        None, help="Date resolved ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    cursor: Optional[str] = typer.Option(None, help="Cursor for pagination"),
    order: Optional[AlertsOrderOpts] = typer.Option(
        AlertsOrderOpts.SEVERITY, help="Field to sort results on"
    ),
    comments: bool = typer.Option(
        False, "--comments", help="Retrieve alerts with their comments"
    ),
):
    """
    List following alerts from a given organization, with optional filters by following ids, state or severity.
    """
    client = Client(profile=sdk_config.profile)
    alerts = client.iter_following_alerts(
        organization_id=organization_id,
        following_ids=following_ids,
        following_tags=following_tags,
        include_empty_following_tags=include_empty_following_tags,
        cursor=cursor,
        order=order,
        rules=rules,
        states=states,
        severities=severities,
        lang=lang,
        opened_at_start=opened_at_start,
        opened_at_end=opened_at_end,
        resolved_at_start=resolved_at_start,
        resolved_at_end=resolved_at_end,
        created_at_start=created_at_start,
        created_at_end=created_at_end,
        updated_at_start=updated_at_start,
        updated_at_end=updated_at_end,
        search=search,
        sort=sort,
    )

    def alerts_with_comments():
        for alert in alerts:
            alert["comments"] = [
                comment["comment"]
                for comment in client.iter_alert_comments(alert["id"])
            ]
            yield alert

    output_iterable(alerts_with_comments() if comments else alerts)


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
    scan_target_ids: Optional[List[UUID]] = typer.Option(
        None, help="Only list alerts from the specified scan targets"
    ),
    scan_target_tags: Optional[List[str]] = typer.Option(
        None, help="Only lists alerts from the specified tags"
    ),
    include_empty_scan_target_tags: Optional[bool] = typer.Option(
        None, help="Include alerts from scan targets without tags"
    ),
    states: Optional[List[AlertState]] = typer.Option(
        [
            x.value
            for x in AlertState
            if x != AlertState.CLOSED and x != AlertState.ACTIVE
        ],
        help="Only list alerts in the specified states",
        case_sensitive=False,
    ),
    severities: Optional[List[AlertSeverity]] = typer.Option(
        [x.value for x in AlertSeverity],
        help="Only list alerts with the specified severities",
        case_sensitive=False,
    ),
    lang: Optional[Languages] = typer.Option(
        Languages.EN_US.value,
        help="Show alert titles in the specified language",
        case_sensitive=False,
    ),
    created_at_start: Optional[str] = typer.Option(
        None, help="Date created starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    created_at_end: Optional[str] = typer.Option(
        None, help="Date created ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    updated_at_start: Optional[str] = typer.Option(
        None, help="Date updated starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    updated_at_end: Optional[str] = typer.Option(
        None, help="Date updated ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    search: Optional[str] = typer.Option("", help="Text to search for in the alerts"),
    sort: Optional[SortOpts] = typer.Option(None, help="Sort order"),
    rules: Optional[List[str]] = typer.Option(
        None, help="Only list alerts in the specified rules"
    ),
    opened_at_start: Optional[str] = typer.Option(
        None, help="Date opened starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    opened_at_end: Optional[str] = typer.Option(
        None, help="Date opened ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    resolved_at_start: Optional[str] = typer.Option(
        None, help="Date resolved starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    resolved_at_end: Optional[str] = typer.Option(
        None, help="Date resolved ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    cursor: Optional[str] = typer.Option(None, help="Cursor for pagination"),
    order: Optional[GroupedAlertOrderOpts] = typer.Option(
        GroupedAlertOrderOpts.SEVERITY, help="Field to sort results on"
    ),
):
    """
    List grouped alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(
        client.iter_grouped_alerts(
            organization_id=organization_id,
            scan_target_ids=scan_target_ids,
            scan_tagert_tags=scan_target_tags,
            include_empty_scan_target_tags=include_empty_scan_target_tags,
            cursor=cursor,
            order=order,
            rules=rules,
            states=states,
            severities=severities,
            lang=lang,
            opened_at_start=opened_at_start,
            opened_at_end=opened_at_end,
            resolved_at_start=resolved_at_start,
            resolved_at_end=resolved_at_end,
            created_at_start=created_at_start,
            created_at_end=created_at_end,
            updated_at_start=updated_at_start,
            updated_at_end=updated_at_end,
            search=search,
            sort=sort,
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
        None, help="Include alerts from scan targets without tags"
    ),
    states: Optional[List[AlertState]] = typer.Option(
        [
            x.value
            for x in AlertState
            if x != AlertState.CLOSED and x != AlertState.ACTIVE
        ],
        help="Only list alerts in the specified states",
        case_sensitive=False,
    ),
    severities: Optional[List[AlertSeverity]] = typer.Option(
        [x.value for x in AlertSeverity],
        help="Only list alerts with the specified severities",
        case_sensitive=False,
    ),
    lang: Optional[Languages] = typer.Option(
        Languages.EN_US.value,
        help="Show alert titles in the specified language",
        case_sensitive=False,
    ),
    created_at_start: Optional[str] = typer.Option(
        None, help="Date created starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    created_at_end: Optional[str] = typer.Option(
        None, help="Date created ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    updated_at_start: Optional[str] = typer.Option(
        None, help="Date updated starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    updated_at_end: Optional[str] = typer.Option(
        None, help="Date updated ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    search: Optional[str] = typer.Option("", help="Text to search for in the alerts"),
    sort: Optional[SortOpts] = typer.Option(None, help="Sort order"),
    rules: Optional[List[str]] = typer.Option(
        None, help="Only list alerts in the specified rules"
    ),
    opened_at_start: Optional[str] = typer.Option(
        None, help="Date opened starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    opened_at_end: Optional[str] = typer.Option(
        None, help="Date opened ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    resolved_at_start: Optional[str] = typer.Option(
        None, help="Date resolved starts at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    resolved_at_end: Optional[str] = typer.Option(
        None, help="Date resolved ends at (format YYYY-MM-DDTHH:MM:SS)"
    ),
    cursor: Optional[str] = typer.Option(None, help="Cursor for pagination"),
    order: Optional[GroupedAlertOrderOpts] = typer.Option(
        GroupedAlertOrderOpts.SEVERITY, help="Field to sort results on"
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
            rules=rules,
            states=states,
            severities=severities,
            lang=lang,
            opened_at_start=opened_at_start,
            opened_at_end=opened_at_end,
            resolved_at_start=resolved_at_start,
            resolved_at_end=resolved_at_end,
            created_at_start=created_at_start,
            created_at_end=created_at_end,
            updated_at_start=updated_at_start,
            updated_at_end=updated_at_end,
            search=search,
            sort=sort,
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


@app.command(name="batch_update_state")
def batch_update_state(
    organization_id: UUID = typer.Argument(
        ..., help="UUID of the organization that owns the alerts"
    ),
    state: AlertState = typer.Argument(..., help="New state to set for the alerts"),
    comment: str = typer.Argument(..., help="Comment explaining this batch update"),
    dry_run: bool = typer.Argument(
        ..., help="If true, performs a simulation without making actual changes"
    ),
    scan_target_ids: Optional[List[UUID]] = typer.Option(
        None,
        "--scan-target-ids",
        help="List of UUIDs representing the scan targets to filter by",
    ),
    alert_ids: Optional[List[str]] = typer.Option(
        None, "--alert-ids", help="List of alert IDs to update"
    ),
    states: Optional[List[AlertState]] = typer.Option(
        None, "--states", help="List of existing alert states to filter alerts by"
    ),
    rules: Optional[List[str]] = typer.Option(
        None, "--rules", help="List of rules to filter alerts by"
    ),
    severities: Optional[List[str]] = typer.Option(
        None,
        "--severities",
        help="List of severities to filter alerts by (e.g., 'low', 'medium', 'high')",
    ),
    include_empty_scan_target_tags: Optional[bool] = typer.Option(
        None,
        "--include-empty-scan-target-tags",
        help="Whether to include alerts with scan targets that have no associated tags",
    ),
):
    client = Client(profile=sdk_config.profile)
    typer.echo(
        client.batch_update_alerts_state(
            organization_id=organization_id,
            state=state,
            dry_run=dry_run,
            comment=comment,
            scan_target_ids=scan_target_ids,
            alert_ids=alert_ids,
            states=states,
            rules=rules,
            severities=severities,
            include_empty_scan_target_tags=include_empty_scan_target_tags,
        )
    )


def get_rule_badge(rule):
    rule_title = {
        # ! itentionally Empty
    }
    title_badges = {
        # ! Itentionally Empty
    }
    title = rule_title.get(rule, None)
    if title is None:
        return None
    badge = title_badges.get(title, None)
    if badge is None:
        return None
    return badge


def get_following_badges(
    open_rules: Iterator[Dict], resolved_rules: Iterator[Dict]
) -> Dict:
    badges = defaultdict(lambda: {"open": 0, "resolved": 0})
    for open_rule in open_rules:
        badge = get_rule_badge(open_rule["rule"])
        if not badge:
            continue
        badges[badge]["open"] = open_rule["total"]
    for resolved_rule in resolved_rules:
        badge = get_rule_badge(resolved_rule["rule"])
        if not badge:
            continue
        badges[badge]["resolved"] = resolved_rule["total"]
    for badge, stats in badges.items():
        if stats["resolved"] == 0 and stats["open"] == 0:
            badges[badge]["percentage"] = 100
        else:
            badges[badge]["percentage"] = round(
                (stats["resolved"] / (stats["resolved"] + stats["open"])) * 100, 2
            )
    return badges


def calculate_global_badges(following_badges: Iterator[Dict]) -> Dict:
    global_scores = {
        "UNCATEGORIZED": 0,
        # ! Will add others scores later
    }
    num_items = len(following_badges)
    for item in following_badges:
        for key in global_scores.keys():
            global_scores[key] += item[key]
    for key in global_scores.keys():
        global_scores[key] = round(global_scores[key] / num_items, 1)
    global_entry = {"ID": "GLOBAL", "NAME": "Global Avarage"}
    global_entry.update(global_scores)

    return global_entry


@app.command(name="generate_following_badges")
def generate_following_badges(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_ids: Optional[List[UUID]] = typer.Option(
        None, help="Only list alerts from the specified scan targets"
    ),
    severities: Optional[List[AlertSeverity]] = typer.Option(
        [AlertSeverity.CRITICAL, AlertSeverity.HIGH],
        help="Only list alerts with the specified severities",
        case_sensitive=False,
    ),
):
    client = Client(profile=sdk_config.profile)
    followings = [
        following
        for following in client.iter_organization_following(organization_id)
        if not following_ids or following["id"] in following_ids
    ]
    following_badges = []
    for following in followings:
        open_rules = [
            rules
            for rules in client.iter_grouped_following_alerts(
                organization_id=organization_id,
                following_ids=[following["id"]],
                severities=severities,
                states=[AlertState.OPEN, AlertState.IN_PROGRESS],
                page_size=1000,
            )
        ]
        resolved_rules = [
            rules
            for rules in client.iter_grouped_following_alerts(
                organization_id=organization_id,
                following_ids=[following["id"]],
                severities=severities,
                states=[
                    AlertState.RISK_ACCEPTED,
                    AlertState.MITIGATING_CONTROL,
                    AlertState.FALSE_POSITIVE,
                    AlertState.CLOSED,
                ],
                page_size=1000,
            )
        ]
        badges = get_following_badges(open_rules, resolved_rules)
        following_badges.append(
            {
                "ID": following["id"],
                "NAME": following["name"],
                "UNCATEGORIZED": badges.get("UNCATEGORIZED", {}).get("percentage", 100),
                # ! Will add others scores later
            }
        )
    if following_badges:
        following_badges.insert(0, calculate_global_badges(following_badges))
    output_iterable(following_badges)
