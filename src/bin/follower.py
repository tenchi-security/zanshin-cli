from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

app = typer.Typer()


@app.command(name="list")
def organization_follower_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization")
):
    """
    List the followers of an organization the user has direct access to.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_followers(organization_id))


@app.command(name="stop")
def organization_follower_stop(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    organization_follower_id: UUID = typer.Argument(
        ..., help="UUID of the organization follower"
    ),
):
    """
    Stop a specific follower from following the given organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.stop_organization_follower(organization_id, organization_follower_id)
    )
