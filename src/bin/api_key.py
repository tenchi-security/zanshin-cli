from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

app = typer.Typer()


@app.command(name="list")
def account_api_key_list():
    """
    Iterates over the API keys of current logged user.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_api_keys())


@app.command(name="create")
def account_api_key_create(
    name: str = typer.Argument(..., help="Name of the new API key")
):
    """
    Creates a new API key for the current logged user, API Keys can be used to interact with the zanshin api directly
    a behalf of that user.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.create_api_key(name))


@app.command(name="delete")
def account_api_key_delete(
    api_key_id: UUID = typer.Argument(..., help="UUID of the invite to delete")
):
    """
    Deletes a given API key by its id, it will only work if the informed ID belongs to the current logged user.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.delete_api_key(api_key_id))
