from typer import Typer, Argument
from zanshinsdk import Client
from utils import dump_json, output_iterable
from  options import GlobalOptions
from uuid import UUID

class Invites:
    app: Typer = Typer()

    def load_commands(self):
        global_options = GlobalOptions().global_options

        @self.app.command(name='list')
        def account_invite_list():
            """
            Iterates over the invites of current logged user.
            """
            client = Client(profile=global_options['profile'])
            
            output_iterable(client.iter_invites())

        @self.app.command(name='get')
        def account_invite_get(invite_id: UUID = Argument(..., help="UUID of the invite")):
            """
            Gets a specific invitation details, it only works if the invitation was made for the current logged user.
            """
            client = Client(profile=global_options['profile'])
            dump_json(client.get_invite(invite_id))


        @self.app.command(name='accept')
        def account_invite_accept(invite_id: UUID = Argument(..., help="UUID of the invite")):
            """
            Accepts an invitation with the informed ID, it only works if the user accepting the invitation is the user that
            received the invitation.
            """
            client = Client(profile=global_options['profile'])
            dump_json(client.get_invite(invite_id))

        return self.app

