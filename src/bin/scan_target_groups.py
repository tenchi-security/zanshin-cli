from uuid import UUID

import typer
from zanshinsdk import Client
from zanshinsdk.client import (
    OAuthTargetKind,
    ScanTargetGroupCredentialListORACLE,
    ScanTargetKind,
)

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

app = typer.Typer()


@app.command(name="list")
def scan_target_groups_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization")
):
    """
    Lists the scan target groups of the user's organization.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_scan_target_groups(organization_id))


@app.command(name="get")
def scan_target_groups_get(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_group_id: UUID = typer.Argument(
        ..., help="UUID of the scan target group"
    ),
):
    """
    Gets details of the scan target group given its ID.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.get_organization_scan_target_group(organization_id, scan_target_group_id)
    )


@app.command(name="delete")
def scan_target_groups_delete(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_group_id: UUID = typer.Argument(
        ..., help="UUID of the scan target group"
    ),
):
    """
    Deletes the scan target group of the organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.delete_organization_scan_target_group(
            organization_id, scan_target_group_id
        )
    )


@app.command(name="update")
def scan_target_groups_update(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_group_id: UUID = typer.Argument(
        ..., help="UUID of the scan target group"
    ),
    name: str = typer.Argument(..., help="new name of the scan target group"),
):
    """
    Updates a scan target group.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.update_scan_target_group(organization_id, scan_target_group_id, name)
    )


@app.command(name="create")
def scan_target_groups_create(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    kind: ScanTargetKind = typer.Argument(
        ...,
        help="kind of the scan target group. Should be 'ORACLE', 'BITBUCKET' or 'GITLAB'",
    ),
    name: str = typer.Argument(..., help="name of the scan target group"),
):
    """
    Creates a scan target group for the organization.
    """
    client = Client(profile=sdk_config.profile)
    scan_target_group = client.create_scan_target_group(organization_id, kind, name)

    if kind not in [member.value for member in OAuthTargetKind]:
        return dump_json(scan_target_group)

    should_return_oauth_link = typer.prompt(
        "Do you want to receive the oauth link from this scan target group? (y/n)",
        default="n",
        type=str,
    )

    if should_return_oauth_link.lower() != "y":
        return dump_json(scan_target_group)

    dump_json(
        client.get_scan_target_group_oauth_link(
            organization_id, scan_target_group["id"]
        )
    )


@app.command(name="oauth_link")
def organization_scan_target_group_oauth_link(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_group_id: UUID = typer.Argument(
        ..., help="UUID of the scan target group"
    ),
):
    """
    Retrieve a link to allow the user to authorize zanshin to read info from their scan target group environment.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.get_scan_target_group_oauth_link(organization_id, scan_target_group_id)
    )


@app.command(name="script")
def scan_target_groups_script(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_group_id: UUID = typer.Argument(
        ..., help="UUID of the scan target group"
    ),
):
    """
    Gets download URL of the scan target group.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.get_scan_target_group_script(organization_id, scan_target_group_id)
    )


@app.command(name="compartments")
def scan_target_groups_compartments(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_group_id: UUID = typer.Argument(
        ..., help="UUID of the scan target group"
    ),
):
    """
    Iterates over the compartments of a scan target group.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(
        client.iter_scan_target_group_compartments(
            organization_id, scan_target_group_id
        )
    )


@app.command(name="insert")
def scan_target_groups_insert(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_group_id: UUID = typer.Argument(
        ..., help="UUID of the scan target group"
    ),
    region: str = typer.Argument(..., help="Oracle cloud region"),
    tenancy_id: str = typer.Argument(..., help="Oracle tenancyId"),
    user_id: str = typer.Argument(..., help="Oracle userId"),
    key_fingerprint: str = typer.Argument(
        ..., help="Oracle Fingerprint used for authentication"
    ),
):
    """
    Inserts an already created scan target group.
    """
    credential = ScanTargetGroupCredentialListORACLE(
        region, tenancy_id, user_id, key_fingerprint
    )
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.insert_scan_target_group_credential(
            organization_id, scan_target_group_id, credential
        )
    )


@app.command(name="create-by-compartments")
def scan_target_groups_create_by_compartments(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_group_id: UUID = typer.Argument(
        ..., help="UUID of the scan target group"
    ),
    name: str = typer.Argument(..., help="Compartment name"),
    ocid: str = typer.Argument(..., help="Oracle Compartment Id"),
):
    """
    Creates Scan Targets from previous listed compartments inside the scan target group.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.create_scan_target_by_compartments(
            organization_id, scan_target_group_id, name, ocid
        )
    )


@app.command(name="scan-targets")
def scan_target_groups_scan_targets(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_group_id: UUID = typer.Argument(
        ..., help="UUID of the scan target group"
    ),
):
    """
    Gets all scan targets from a specific scan target group.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(
        client.iter_scan_targets_from_group(organization_id, scan_target_group_id)
    )
