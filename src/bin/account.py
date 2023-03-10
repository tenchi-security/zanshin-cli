import typer
from zanshinsdk import Client

import src.config.sdk as sdk_config
from src.lib.utils import dump_json

###################################################
# Account App
###################################################

app = typer.Typer()


@app.command(name="me")
def account_me():
    """
    Returns the details of the user account that owns the API key used by this Connection instance
    """

    client = Client(profile=sdk_config.profile)
    try:
        dump_json(client.get_me())
    except Exception as e:
        print(e)
