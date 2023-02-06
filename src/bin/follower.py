import typer
import config.sdk as sdk_config
from zanshinsdk import Client
from lib.utils import dump_json, output_iterable
from uuid import UUID

app = typer.Typer()

@app.command(name='list')
def organization_follower_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the followers of organization this user has direct access to.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_followers(organization_id))


@app.command(name='stop')
def organization_follower_stop(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_follower_id: UUID = typer.Argument(..., help="UUID of the organization follower")
):
    """
    Stops one organization follower of another.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.stop_organization_follower(organization_id, organization_follower_id))