from typing import List, Optional
from uuid import UUID

import typer
from zanshinsdk import Client
from zanshinsdk.client import Roles

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

###################################################
# Organization Member Invite App
###################################################

app = typer.Typer()


@app.command(name="list")
def organization_member_invite_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization")
):
    """
    Lists the member invites of organization this user has direct access to.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_members_invites(organization_id))


@app.command(name="create")
def organization_member_invite_create(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    organization_member_invite_email: str = typer.Argument(
        ..., help="E-mail of the organization member"
    ),
    organization_member_invite_role: Optional[List[Roles]] = typer.Option(
        [x.value for x in Roles],
        help="Role of the organization member",
        case_sensitive=False,
    ),
):
    """
    Create organization member invite.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.create_organization_members_invite(
            organization_id,
            organization_member_invite_email,
            organization_member_invite_role,
        )
    )


@app.command(name="get")
def organization_member_invite_get(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    organization_member_invite_email: str = typer.Argument(
        ..., help="E-mail of the organization member invite"
    ),
):
    """
    Get organization member invite.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.get_organization_member(
            organization_id, organization_member_invite_email
        )
    )


@app.command(name="delete")
def organization_member_invite_delete(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    organization_member_invite_email: str = typer.Argument(
        ..., help="E-mail of the organization member"
    ),
):
    """
    Delete organization member invite.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.delete_organization_member_invite(
            organization_id, organization_member_invite_email
        )
    )


@app.command(name="resend")
def organization_member_invite_resend(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    organization_member_invite_email: str = typer.Argument(
        ..., help="E-mail of the organization member"
    ),
):
    """
    Resend organization member invitation.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.resend_organization_member_invite(
            organization_id, organization_member_invite_email
        )
    )
