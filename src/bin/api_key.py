from uuid import UUID

import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json, output_iterable

app = typer.Typer()


@app.command(name="list")
def account_api_key_list():
    """
    List all API keys belonging to the currently logged-in user.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_api_keys())


@app.command(name="create")
def account_api_key_create(
    name: str = typer.Argument(..., help="Name of the new API key")
):
    """
    Create a new API key for the logged-in user to interact with the Zanshin API.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.create_api_key(name))


@app.command(name="delete")
def account_api_key_delete(
    api_key_id: UUID = typer.Argument(..., help="UUID of the API key to delete")
):
    """
    Delete a specific API key by its UUID. The key must belong to the logged-in user.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.delete_api_key(api_key_id))
