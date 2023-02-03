from typer import Typer
from zanshinsdk import Client
from utils import dump_json
import options

class Account:
    app: Typer = Typer()

    def load_commands(self):
        @self.app.command(name='me')
        def account_me():
            """
            Returns the details of the user account that owns the API key used by this Connection instance as per
            """
            client = Client(profile=options.global_options['profile'])
            try:
                dump_json(client.get_me())
            except Exception as e:
                print(e)
        return self.app


    
    
    