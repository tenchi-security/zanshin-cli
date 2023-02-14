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
    Iterates over the invites of current logged user.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_invites())


@app.command(name="get")
def account_invite_get(
    invite_id: UUID = typer.Argument(..., help="UUID of the invite")
):
    """
    Gets a specific invitation details, it only works if the invitation was made for the current logged user.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_invite(invite_id))


@app.command(name="accept")
def account_invite_accept(
    invite_id: UUID = typer.Argument(..., help="UUID of the invite")
):
    """
    Accepts an invitation with the informed ID, it only works if the user accepting the invitation is the user that
    received the invitation.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_invite(invite_id))
