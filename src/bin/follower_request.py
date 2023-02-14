from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

app = typer.Typer()


@app.command(name="list")
def organization_follower_request_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization")
):
    """
    Lists the follower requests of organization this user has direct access to.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_followers(organization_id))


@app.command(name="create")
def organization_follower_request_create(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    token: UUID = typer.Argument(..., help="Token of the follower request"),
):
    """
    Create organization follower request.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.create_organization_follower_request(organization_id, token))


@app.command(name="get")
def organization_follower_request_get(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    token: UUID = typer.Argument(..., help="Token of the follower request"),
):
    """
    Get organization follower request.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_organization_follower_request(organization_id, token))


@app.command(name="delete")
def organization_follower_request_delete(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    token: UUID = typer.Argument(..., help="Token of the follower request"),
):
    """
    Delete organization follower request.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.delete_organization_follower_request(organization_id, token))
