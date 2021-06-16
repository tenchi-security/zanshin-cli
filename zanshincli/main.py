from collections.abc import Sequence, Mapping
from configparser import RawConfigParser
from enum import Enum
from json import dumps
from stat import S_IRUSR, S_IWUSR
from sys import version as python_version
from typing import Iterator, Dict, Any, Optional, List
from uuid import UUID

import typer
from prettytable import PrettyTable
from zanshinsdk import Client, AlertState, AlertSeverity, __version__ as sdk_version
from zanshinsdk.client import _CONFIG_DIR, _CONFIG_FILE

from zanshincli import __version__ as cli_version

main_app = typer.Typer()
organization_app = typer.Typer()
scan_target_app = typer.Typer()
main_app.add_typer(organization_app, name="organization",
                   help="Operations on organizations the API key owner has direct access to.")
organization_app.add_typer(scan_target_app, name="scan_target",
                           help="Operations on scan targets from organizations the API key owner has direct access to.")


class OutputFormat(str, Enum):
    """
    Used to specify command-line parameters indicating output format.
    """
    JSON = "json"
    TABLE = "table"
    CSV = "csv"
    HTML = "html"


def format_field(value: Any) -> str:
    """
    Function that formats a single field for output on a table or CSV output, in order to deal with nested arrays or objects in the JSON outputs of the API.
    :param value: the value to format
    :return: a string that is fit for console output
    """
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        if all(isinstance(x, (str, bytes, int, float)) for x in value):
            return ", ".join([str(x) for x in value])
        else:
            return dumps(value)
    elif isinstance(value, Mapping):
        return dumps(value)
    else:
        return value


def output_iterable(iterator: Iterator[Dict], format: OutputFormat) -> None:
    """
    Function that iterates over a series of dicts representing JSON objects returned by API list operations, and which
    outputs them using typer.echo in the specified format. Will use streaming processing for JSON, all others need to
    load all responses in memory in a PrettyTable prior to output, which could be problematic for large number of
    entries.
    :param iterator: the iterator containing the JSON objects
    :param format: the output format to use
    :return: None
    """
    if format is OutputFormat.JSON:
        for entry in iterator:
            typer.echo(dumps(entry, indent=4))
    else:
        table = PrettyTable()
        rows = 0
        for entry in iterator:
            if not table.field_names:
                table.field_names = sorted(entry.keys())
            else:
                for k in entry.keys():
                    if k not in table.field_names:
                        table.add_column(k, [None] * rows)
            table.add_row([format_field(entry.get(fn, None)) for fn in table.field_names])
            rows += 1
        if format is OutputFormat.TABLE:
            typer.echo(table.get_string())
        elif format is OutputFormat.CSV:
            typer.echo(table.get_csv_string())
        elif format is OutputFormat.HTML:
            typer.echo(table.get_html_string())
        else:
            raise NotImplementedError("unexpected format type")


@main_app.command()
def init():
    """
    Update settings on configuration file.
    """
    cfg = RawConfigParser()
    cfg.read(_CONFIG_FILE)
    typer.echo("This command will allow you to set up profiles in the configuration file.")
    profile = typer.prompt("Please enter the profile name to use", default="default")
    if cfg.has_section(profile):
        typer.confirm("Profile already exists. Overwrite?", abort=True)
    else:
        cfg.add_section(profile)
    cfg.set(profile, "api_key", typer.prompt("Please enter the API key", hide_input=True))
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with _CONFIG_FILE.open('w') as f:
        cfg.write(f)
    _CONFIG_FILE.chmod(S_IRUSR | S_IWUSR)


@main_app.command()
def me(profile: str = typer.Option("default",
                                   help="Configuration file section to use for credentials and other settings")):
    """
    Show details about the owner of the API key being used.
    """
    client = Client(profile=profile)
    typer.echo(dumps(client.me(), indent=4))


@main_app.command()
def version():
    """
    Display the program and Python versions in use.
    """
    typer.echo(f'Zanshin CLI v{cli_version}')
    typer.echo(f'Zanshin Python SDK v{sdk_version}')
    typer.echo(f'Python {python_version}')


@organization_app.command()
def list(profile: str = typer.Option("default",
                                     help="Configuration file section to use for credentials and other settings"),
         format: OutputFormat = typer.Option(OutputFormat.JSON, help="Format to use for the output.",
                                             case_sensitive=False)):
    """
    Lists the organizations this user has direct access to as a member.
    """
    client = Client(profile=profile)
    output_iterable(client.iter_organizations(), format)


@scan_target_app.command()
def list(profile: str = typer.Option("default",
                                     help="Configuration file section to use for credentials and other settings"),
         organization_id: UUID = typer.Argument(...,
                                                help="UUID of the organizations whose scan targets should be listed."),
         format: OutputFormat = typer.Option(OutputFormat.JSON.value, help="Format to use for the output.",
                                             case_sensitive=False)):
    """
    Lists the scan targets from an organization that user has access to as a member.
    """
    client = Client(profile=profile)
    output_iterable(client.iter_scan_targets(organization_id=organization_id), format)


@organization_app.command()
def alerts(organization_id: UUID = typer.Argument(..., help="UUID of the organization to list alerts from."),
           state: Optional[List[AlertState]] = typer.Option(
               [x.value for x in AlertState if x != AlertState.CLOSED],
               help="Only list alerts in the specified states.", case_sensitive=False),
           severity: Optional[List[AlertSeverity]] = typer.Option([x.value for x in AlertSeverity],
                                                                  help="Only list alerts with the specified severities.",
                                                                  case_sensitive=False),
           profile: str = typer.Option("default",
                                       help="Configuration file section to use for credentials and other settings"),
           format: OutputFormat = typer.Option(OutputFormat.JSON, help="Format to use for the output.",
                                               case_sensitive=False)):
    """
    List alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=profile)
    output_iterable(
        client.iter_organization_alerts(organization_id=organization_id, states=state, severities=severity), format)


@scan_target_app.command()
def scan(organization_id: UUID = typer.Argument(..., help="UUID of the organization to list alerts from."),
         scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target to start scan."),
         profile: str = typer.Option("default",
                                     help="Configuration file section to use for credentials and other settings")):
    """
    Start an Scan in a specific scan_target from an organization.
    """
    client = Client(profile=profile)
    typer.echo(
        dumps(client.start_scan_target(organization_id=organization_id, scan_target_id=scan_target_id), indent=4))


@scan_target_app.command()
def check(organization_id: UUID = typer.Argument(..., help="UUID of the organization to list alerts from."),
          scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target to start scan."),
          profile: str = typer.Option("default",
                                      help="Configuration file section to use for credentials and other settings")):
    """
    Check an scan_target status from an organization.
    """
    client = Client(profile=profile)
    typer.echo(
        dumps(client.check_scan_target(organization_id=organization_id, scan_target_id=scan_target_id), indent=4))


if __name__ == "__main__":
    main_app()
