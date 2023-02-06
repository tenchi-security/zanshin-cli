import typer
import config.sdk as sdk_config
from zanshinsdk import Client
from lib.utils import dump_json, output_iterable
from uuid import UUID
from typing import Optional, List
from zanshinsdk.client import Roles

###################################################
# Organization Member App
###################################################

app = typer.Typer()

@app.command(name='list')
def organization_member_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the members of organization this user has direct access to.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_members(organization_id))


@app.command(name='get')
def organization_member_get(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_id: UUID = typer.Argument(..., help="UUID of the organization member")
):
    """
    Get organization member.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_organization_member(organization_id, organization_member_id))


@app.command(name='update')
def organization_member_update(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_id: UUID = typer.Argument(..., help="UUID of the organization member"),
        role: Optional[List[Roles]] = typer.Option([x.value for x in Roles],
                                                   help="Role of the organization member",
                                                   case_sensitive=False)
):
    """
    Update organization member.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.update_organization_member(organization_id, organization_member_id, role))


@app.command(name='delete')
def organization_member_delete(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_id: UUID = typer.Argument(..., help="UUID of the organization member")
):
    """
    Delete organization member.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.delete_organization_member(organization_id, organization_member_id))