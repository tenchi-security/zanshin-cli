from collections.abc import Sequence, Mapping
from configparser import RawConfigParser
from datetime import timedelta
from enum import Enum
from json import dumps
from stat import S_IRUSR, S_IWUSR
from sys import version as python_version
from time import perf_counter
from typing import Iterator, Dict, Any, Optional, List
from uuid import UUID

import typer
from prettytable import PrettyTable
from typer import Typer
from zanshinsdk import Client, AlertState, AlertSeverity, __version__ as sdk_version
from zanshinsdk.client import _CONFIG_DIR, _CONFIG_FILE

from zanshincli import __version__ as cli_version


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
    Function that formats a single field for output on a table or CSV output, in order to deal with nested arrays or
    objects in the JSON outputs of the API.
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


def output_iterable(iterator: Iterator[Dict]) -> None:
    """
    Function that iterates over a series of dicts representing JSON objects returned by API list operations, and which
    outputs them using typer.echo in the specified format. Will use streaming processing for JSON, all others need to
    load all responses in memory in a PrettyTable prior to output, which could be problematic for large number of
    entries.
    :param iterator: the iterator containing the JSON objects
    :return: None
    """
    rows = 0
    if global_options['format'] is OutputFormat.JSON:
        for entry in iterator:
            typer.echo(dumps(entry, indent=4))
            rows += 1
    else:
        table = PrettyTable()
        for entry in iterator:
            if not table.field_names:
                table.field_names = sorted(entry.keys())
            else:
                for k in entry.keys():
                    if k not in table.field_names:
                        table.add_column(k, [None] * rows)
            table.add_row([format_field(entry.get(fn, None)) for fn in table.field_names])
            rows += 1
        if global_options['format'] is OutputFormat.TABLE:
            typer.echo(table.get_string())
        elif global_options['format'] is OutputFormat.CSV:
            typer.echo(table.get_csv_string())
        elif global_options['format'] is OutputFormat.HTML:
            typer.echo(table.get_html_string())
        else:
            raise NotImplementedError(f"unexpected format type {global_options['format']}")
    global_options['entries'] = rows


###################################################
# Main App
###################################################

global_options: dict = {'entries': 1}
main_app: Typer = typer.Typer()


@main_app.callback()
def global_options_callback(ctx: typer.Context,
                            profile: str = typer.Option("default",
                                                        help="Configuration file section to read API key and configutation from"),
                            output_format: OutputFormat = typer.Option(OutputFormat.JSON, '--format',
                                                                       help="Output format to use for list operations",
                                                                       case_sensitive=False),
                            verbose: bool = typer.Option(True, help="Print timiing and other information to stderr")):
    """
    Command-line utility to interact with the Zanshin SaaS service offered by Tenchi Security, go to
    https://github.com/tenchi-security/zanshin-cli for license, source code and documentation
    """
    if verbose:
        # print summary of data processed and elapsed time at the end of the execution
        start_time = perf_counter()
        def print_elapsed_time():
            typer.echo(
                f"zanshin: {global_options['entries']} object(s) processed in {timedelta(seconds=perf_counter() - start_time)}",
                err=True)
        ctx.call_on_close(print_elapsed_time)

    global_options['verbose'] = verbose
    global_options['profile'] = profile
    global_options['format'] = output_format


@main_app.command()
def init():
    """
    Update settings on configuration file.
    """
    cfg = RawConfigParser()
    cfg.read(_CONFIG_FILE)
    typer.echo("This command will allow you to set up profiles in the configuration file.")
    profile = typer.prompt("Please enter the profile name to use", default=global_options['profile'])
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
def me():
    """
    Show details about the owner of the API key being used.
    """
    client = Client(profile=global_options['profile'])
    typer.echo(dumps(client.me(), indent=4))


@main_app.command()
def alert(alert_id: UUID = typer.Argument(..., help="UUID of the alert to look up")):
    """
    Returns details about a specified alert
    """
    client = Client(profile=global_options['profile'])
    typer.echo(dumps(client.get_alert(alert_id), indent=4))


@main_app.command()
def version():
    """
    Display the program and Python versions in use.
    """
    typer.echo(f'Zanshin CLI v{cli_version}')
    typer.echo(f'Zanshin Python SDK v{sdk_version}')
    typer.echo(f'Python {python_version}')


###################################################
# Organization App
###################################################

organization_app = typer.Typer()
main_app.add_typer(organization_app, name="organization",
                   help="Operations on organizations the API key owner has direct access to")


@organization_app.command(name='list')
def organization_list():
    """
    Lists the organizations this user has direct access to as a member.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organizations())


@organization_app.command(name='alerts')
def organization_alerts(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                        state: Optional[List[AlertState]] = typer.Option(
                            [x.value for x in AlertState if x != AlertState.CLOSED],
                            help="Only list alerts in the specified states.", case_sensitive=False),
                        severity: Optional[List[AlertSeverity]] = typer.Option([x.value for x in AlertSeverity],
                                                                               help="Only list alerts with the specified severities",
                                                                               case_sensitive=False)):
    """
    List alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(
        client.iter_organization_alerts(organization_id=organization_id, states=state, severities=severity))


###################################################
# Organization / Scan Target App
###################################################

scan_target_app = typer.Typer()
organization_app.add_typer(scan_target_app, name="scan_target",
                           help="Operations on scan targets from organizations the API key owner has direct access to")


@scan_target_app.command(name='list')
def scan_target_list(organization_id: UUID = typer.Argument(...,
                                                            help="UUID of the organizations whose scan targets should be listed")):
    """
    Lists the scan targets (i.e. linked cloud accounts) from an organization that user has access to as a member.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_scan_targets(organization_id=organization_id))


@scan_target_app.command(name='scan')
def scan_target_scan(organization_id: UUID = typer.Argument(..., help="UUID of the organization to list alerts from"),
                     scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target to start scan")):
    """
    Starts an ad-hoc scan of a specified scan target
    """
    client = Client(profile=global_options['profile'])
    typer.echo(
        dumps(client.start_scan_target(organization_id=organization_id, scan_target_id=scan_target_id), indent=4))


@scan_target_app.command(name='check')
def scan_target_check(organization_id: UUID = typer.Argument(..., help="UUID of the organization to list alerts from"),
                      scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target to start scan")):
    """
    Checks if a scan target is correctly configured
    """
    client = Client(profile=global_options['profile'])
    typer.echo(
        dumps(client.check_scan_target(organization_id=organization_id, scan_target_id=scan_target_id), indent=4))


###################################################
# Following App
###################################################

following_app = typer.Typer()
main_app.add_typer(following_app, name="following",
                   help="Operations on organizations that are being followed by one of the organizations the API key owner is a member of")


@following_app.command(name='list')
def following_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists other organizations that a specified organization is following
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_following(organization_id))


@following_app.command(name='stop')
def following_stop(organization_id: UUID = typer.Argument(...,
                                                          help="UUID of the follower organization (which the API key owner must be a member of)"),
                   following_id: UUID = typer.Argument(..., help="UUID of the followed organization")):
    """
    Stops one organization from following another
    """
    client = Client(profile=global_options['profile'])
    typer.echo(client.stop_following(organization_id, following_id))


@following_app.command(name='alerts')
def following_alerts(following_id: Optional[List[UUID]] = typer.Option(None,
                                                                       help="Only list alerts from the specified followed organizations"),
                     state: Optional[List[AlertState]] = typer.Option(
                         [x.value for x in AlertState if x != AlertState.CLOSED],
                         help="Only list alerts in the specified states.", case_sensitive=False),
                     severity: Optional[List[AlertSeverity]] = typer.Option([x.value for x in AlertSeverity],
                                                                            help="Only list alerts with the specified severities",
                                                                            case_sensitive=False)):
    """
    Lists alerts of organizations that the API key owner is following
    """
    client = Client(profile=global_options['profile'])
    if not following_id:
        following_id = []
        for org in client.iter_organizations():
            following_id.extend([x['id'] for x in client.iter_following(org['id'])])
    output_iterable(client.iter_following_alerts(following_ids=following_id, states=state, severities=severity))


###################################################
# Following / Requests App
###################################################

following_requests_app = typer.Typer()
following_app.add_typer(following_requests_app, name="requests",
                        help="Operations on requests submitted by third parties to be followed by one of the organizations the API key owner is a member of")


@following_requests_app.command(name='list')
def following_requests_list(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization that received the request")):
    """
    Lists all of the requests from organizations that want to be followed by a specified organization that the API key
    owner is a member of
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_following_requests(organization_id))


@following_requests_app.command(name='accept')
def following_requests_accept(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization that received the request"),
        following_id: UUID = typer.Argument(..., help="UUID of the organization that requested to be followed")):
    """
    Accepts a request to follow another organization
    """
    client = Client(profile=global_options['profile'])
    typer.echo(dumps(client.accept_following_request(organization_id, following_id), indent=4))


@following_requests_app.command(name='decline')
def following_requests_decline(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization that received the request"),
        following_id: UUID = typer.Argument(..., help="UUID of the organization that requested to be followed")):
    """
    Declines a request to follow another organization
    """
    client = Client(profile=global_options['profile'])
    typer.echo(dumps(client.decline_following_request(organization_id, following_id), indent=4))


if __name__ == "__main__":
    main_app()
