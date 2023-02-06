from typing import Union
import typer
from json import dumps

def dump_json(out: Union[dict, any]) -> None:
    typer.echo(dumps(out, indent=4))
