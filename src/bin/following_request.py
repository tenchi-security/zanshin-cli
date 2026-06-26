from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

app = typer.Typer()


@app.command(name="list")
def organization_following_request_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization")
):
    """
    List the following requests of an organization the user has direct access to.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_following_requests(organization_id))


@app.command(name="get")
def organization_following_request_get(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_id: UUID = typer.Argument(..., help="UUID of the following request"),
):
    """
    Get details of a specific request received by an organization to follow another.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_organization_following_request(organization_id, following_id))


@app.command(name="accept")
def organization_following_request_accept(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_id: UUID = typer.Argument(..., help="UUID of the following request"),
):
    """
    Accept a pending request to follow another organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.accept_organization_following_request(organization_id, following_id)
    )


@app.command(name="decline")
def organization_following_request_decline(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    following_id: UUID = typer.Argument(..., help="UUID of the following request"),
):
    """
    Decline a pending request to follow another organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.decline_organization_following_request(organization_id, following_id)
    )
