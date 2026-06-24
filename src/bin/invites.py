from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

###################################################
# Account Invites App
###################################################

app = typer.Typer()


@app.command(name="list")
def account_invite_list():
    """
    List all pending invitations for the currently logged-in user.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_invites())


@app.command(name="get")
def account_invite_get(
    invite_id: UUID = typer.Argument(..., help="UUID of the invite")
):
    """
    Get details of a specific invitation belonging to the logged-in user.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_invite(invite_id))


@app.command(name="accept")
def account_invite_accept(
    invite_id: UUID = typer.Argument(..., help="UUID of the invite")
):
    """
    Accept a specific invitation. The invite must belong to the logged-in user.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.accept_invite(invite_id))
