from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

app = typer.Typer()


@app.command(name="list")
def organization_following_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization")
):
    """
    Lists the following of organization this user has direct access to.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_following(organization_id))


@app.command(name="stop")
def organization_following_stop(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    organization_following_id: UUID = typer.Argument(
        ..., help="UUID of the organization following"
    ),
):
    """
    Stops one organization following of another.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.stop_organization_following(organization_id, organization_following_id)
    )
