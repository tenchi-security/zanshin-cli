from typer import Typer
from zanshinsdk import Client
from utils import dump_json

class Account:
    app: Typer = Typer()
    options: dict
    def __init__(self, options: dict) -> None:
        self.options = options

    def load_commands(self):
        @self.app.command(name='me')
        def account_me():
            """
            Returns the details of the user account that owns the API key used by this Connection instance as per
            """
            client = Client(profile=self.options['profile'])
            try:
                dump_json(client.get_me())
            except Exception as e:
                print(e)
        return self.app


    
    
    