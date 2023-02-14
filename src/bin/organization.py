from typing import Optional
from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

###################################################
# Organization App
###################################################

app = typer.Typer()


@app.command(name="list")
def organization_list():
    """
    Lists the organizations this user has direct access to as a member.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organizations())


@app.command(name="get")
def organization_get(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization")
):
    """
    Gets an organization given its ID.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_organization(organization_id))


@app.command(name="update")
def organization_update(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    name: Optional[str] = typer.Argument(None, help="Name of the organization"),
    picture: Optional[str] = typer.Argument(None, help="Picture of the organization"),
    email: Optional[str] = typer.Argument(
        None, help="Contact e-mail of the organization"
    ),
):
    """
    Gets an organization given its ID.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.update_organization(organization_id, name, picture, email))


@app.command(name="create")
def organization_create(
    name: str = typer.Argument(..., help="Name of the organization")
):
    """
    Creates an organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.create_organization(name))


@app.command(name="delete")
def organization_delete(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization")
):
    """
    Deletes an organization given its ID.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.delete_organization(organization_id))
