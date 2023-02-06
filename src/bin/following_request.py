import typer
import config.sdk as sdk_config
from zanshinsdk import Client
from lib.utils import dump_json, output_iterable
from uuid import UUID

app = typer.Typer()

@app.command(name='list')
def organization_following_request_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the following requests of organization this user has direct access to.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_following_requests(organization_id))


@app.command(name='get')
def organization_following_request_get(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        following_id: UUID = typer.Argument(..., help="UUID of the following request")
):
    """
    Returns a request received by an organization to follow another.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_organization_following_request(organization_id, following_id))


@app.command(name='accept')
def organization_following_request_accept(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        following_id: UUID = typer.Argument(..., help="UUID of the following request")
):
    """
    Accepts a request to follow another organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.accept_organization_following_request(organization_id, following_id))


@app.command(name='decline')
def organization_following_request_decline(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        following_id: UUID = typer.Argument(..., help="UUID of the following request")
):
    """
    Declines a request to follow another organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.decline_organization_following_request(organization_id, following_id))
