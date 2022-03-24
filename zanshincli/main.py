import sys
from collections.abc import Sequence, Mapping
from configparser import RawConfigParser
from datetime import timedelta
from enum import Enum
from json import dumps
from stat import S_IRUSR, S_IWUSR
from typing import Iterable, Iterator, Dict, Any, Optional, List
from uuid import UUID
import boto3
from boto3_type_annotations.organizations import Client as Boto3OrganizationsClient
from boto3_type_annotations.sts import Client as Boto3STSClient
from .awsorgrun import AWSOrgRunTarget, awsorgrun

import typer
import click
from click import Context
from prettytable import PrettyTable
from sys import version as python_version
from time import perf_counter
from typer import Typer
from zanshinsdk import Client, AlertState, AlertSeverity, __version__ as sdk_version
from zanshinsdk.client import ScanTargetKind, ScanTargetAWS, Roles, CONFIG_DIR, CONFIG_FILE
from zanshinsdk.alerts_history import FilePersistentAlertsIterator
from zanshinsdk.following_alerts_history import FilePersistentFollowingAlertsIterator

from zanshincli import __version__ as cli_version


class OrderedCommands(click.Group):
    def list_commands(self, ctx: Context) -> Iterable[str]:
        return self.commands.keys()


class OutputFormat(str, Enum):
    """
    Used to specify command-line parameters indicating output format.
    """
    JSON = "json"
    TABLE = "table"
    CSV = "csv"
    HTML = "html"


class AWSAccount(dict):
    """
    Class representing a AWS Account as returned by boto3
    """

    def __init__(self, Id: str, Name: str, Arn: str, Email: str, Onboard: bool = False):
        dict.__init__(self, Id=Id, Name=Name, Arn=Arn,
                      Email=Email, Onboard=Onboard)


###################################################
# Exchanger
###################################################

def zanshin_exchanger(_, value, __):
    print(value)


sys.excepthook = zanshin_exchanger


###################################################
# Utils
###################################################

def format_field(value: Any) -> str:
    """
    Function that formats a single field for output on a table or CSV output, in order to deal with nested arrays or
    objects in the JSON outputs of the API
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


def output_iterable(iterator: Iterator[Dict], empty: Any = None, _each_iteration_function: Any = None) -> None:
    """
    Function that iterates over a series of dicts representing JSON objects returned by API list operations, and which
    outputs them using typer.echo in the specified format. Will use streaming processing for JSON, all others need to
    load all responses in memory in a PrettyTable prior to output, which could be problematic for large number of
    entries
    :param _each_iteration_function:
    :param empty:
    :param iterator: the iterator containing the JSON objects
    :return: None
    """
    global global_options

    global_options['entries'] = 0
    if global_options['format'] is OutputFormat.JSON:
        for entry in iterator:
            typer.echo(dumps(entry, indent=4))
            global_options['entries'] += 1
            if _each_iteration_function:
                _each_iteration_function()
    else:
        table = PrettyTable()
        for entry in iterator:
            if not table.field_names:
                table.field_names = sorted(entry.keys())
            else:
                for k in entry.keys():
                    if k not in table.field_names:
                        table.add_column(k, [empty] * global_options['entries'])
            table.add_row([format_field(entry.get(fn, empty)) for fn in table.field_names])
            global_options['entries'] += 1
            if _each_iteration_function:
                _each_iteration_function()
        if global_options['format'] is OutputFormat.TABLE:
            typer.echo(table.get_string())
        elif global_options['format'] is OutputFormat.CSV:
            typer.echo(table.get_csv_string())
        elif global_options['format'] is OutputFormat.HTML:
            typer.echo(table.get_html_string())
        else:
            raise NotImplementedError(f"unexpected format type {global_options['format']}")


def dump_json(out: [Dict, any]) -> None:
    typer.echo(dumps(out, indent=4))


###################################################
# Main App
###################################################

global_options: dict = {'entries': 1}
main_app: Typer = typer.Typer(cls=OrderedCommands)


@main_app.callback()
def global_options_callback(ctx: typer.Context,
                            profile: str = typer.Option("default",
                                                        help="Configuration file section to read API key"
                                                             "and configuration from"),
                            output_format: OutputFormat = typer.Option(OutputFormat.JSON, '--format',
                                                                       help="Output format to use for list operations",
                                                                       case_sensitive=False),
                            verbose: bool = typer.Option(True, help="Print more information to stderr")):
    """
    Command-line utility to interact with the Zanshin SaaS service offered by Tenchi Security
    (https://tenchisecurity.com), go to https://github.com/tenchi-security/zanshin-cli for license, source code and
    documentation
    """
    if verbose:
        # print summary of data processed and elapsed time at the end of the execution
        start_time = perf_counter()

        def print_elapsed_time():
            typer.echo(
                f"zanshin: {global_options['entries']} object(s) processed in"
                f"{timedelta(seconds=perf_counter() - start_time)}",
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
    cfg.read(CONFIG_FILE)
    typer.echo("This command will allow you to set up profiles in the configuration file.")
    profile = typer.prompt("Please enter the profile name to use", default=global_options['profile'])
    if cfg.has_section(profile):
        typer.confirm("Profile already exists. Overwrite?", abort=True)
    else:
        cfg.add_section(profile)
    cfg.set(profile, "api_key", typer.prompt("Please enter the API key", hide_input=True))
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open('w') as f:
        cfg.write(f)
    CONFIG_FILE.chmod(S_IRUSR | S_IWUSR)


@main_app.command()
def version():
    """
    Display the program and Python versions in use.
    """
    typer.echo(f'Zanshin CLI v{cli_version}')
    typer.echo(f'Zanshin Python SDK v{sdk_version}')
    typer.echo(f'Python {python_version}')


###################################################
# Account App
###################################################

account_app = typer.Typer(cls=OrderedCommands)
main_app.add_typer(account_app, name="account",
                   help="Operations on user the API key owner has direct access to")


@account_app.command(name='me')
def account_me():
    """
    Returns the details of the user account that owns the API key used by this Connection instance as per
    """
    client = Client(profile=global_options['profile'])
    try:
        dump_json(client.get_me())
    except Exception as e:
        print(e)


###################################################
# Account Invites App
###################################################

invites_app = typer.Typer(cls=OrderedCommands)
account_app.add_typer(invites_app, name="invites",
                      help="Operations on invites from account the API key owner has direct access to")


@invites_app.command(name='list')
def account_invite_list():
    """
    Iterates over the invites of current logged user.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_invites())


@invites_app.command(name='get')
def account_invite_get(invite_id: UUID = typer.Argument(..., help="UUID of the invite")):
    """
    Gets a specific invitation details, it only works if the invitation was made for the current logged user.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.get_invite(invite_id))


@invites_app.command(name='accept')
def account_invite_accept(invite_id: UUID = typer.Argument(..., help="UUID of the invite")):
    """
    Accepts an invitation with the informed ID, it only works if the user accepting the invitation is the user that
    received the invitation.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.get_invite(invite_id))


###################################################
# Account API key App
###################################################

api_key_app = typer.Typer(cls=OrderedCommands)
account_app.add_typer(api_key_app, name="api_key",
                      help="Operations on API keys from account the API key owner has direct access to")


@api_key_app.command(name='list')
def account_api_key_list():
    """
    Iterates over the API keys of current logged user.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_api_keys())


@api_key_app.command(name='create')
def account_api_key_create(name: str = typer.Argument(..., help="Name of the new API key")):
    """
    Creates a new API key for the current logged user, API Keys can be used to interact with the zanshin api directly
    a behalf of that user.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.create_api_key(name))


@api_key_app.command(name='delete')
def account_api_key_delete(api_key_id: UUID = typer.Argument(..., help="UUID of the invite to delete")):
    """
    Deletes a given API key by its id, it will only work if the informed ID belongs to the current logged user.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.delete_api_key(api_key_id))


###################################################
# Organization App
###################################################

organization_app = typer.Typer(cls=OrderedCommands)
main_app.add_typer(organization_app, name="organization",
                   help="Operations on organizations the API key owner has direct access to")


@organization_app.command(name='list')
def organization_list():
    """
    Lists the organizations this user has direct access to as a member.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organizations())


@organization_app.command(name='get')
def organization_get(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Gets an organization given its ID.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.get_organization(organization_id))


@organization_app.command(name='update')
def organization_update(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        name: Optional[str] = typer.Argument(None, help="Name of the organization"),
        picture: Optional[str] = typer.Argument(None, help="Picture of the organization"),
        email: Optional[str] = typer.Argument(None, help="Contact e-mail of the organization")
):
    """
    Gets an organization given its ID.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.update_organization(organization_id, name, picture, email))


###################################################
# Organization Member App
###################################################

organization_member_app = typer.Typer(cls=OrderedCommands)
organization_app.add_typer(organization_member_app, name="member",
                           help="Operations on members of organization the API key owner has direct access to")


@organization_member_app.command(name='list')
def organization_member_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the members of organization this user has direct access to.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organization_members(organization_id))


@organization_member_app.command(name='get')
def organization_member_get(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_id: UUID = typer.Argument(..., help="UUID of the organization member")
):
    """
    Get organization member.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.get_organization_member(organization_id, organization_member_id))


@organization_member_app.command(name='update')
def organization_member_update(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_id: UUID = typer.Argument(..., help="UUID of the organization member"),
        role: Optional[List[Roles]] = typer.Option([x.value for x in Roles],
                                                   help="Role of the organization member",
                                                   case_sensitive=False)
):
    """
    Update organization member.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.update_organization_member(organization_id, organization_member_id, role))


@organization_member_app.command(name='delete')
def organization_member_delete(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_id: UUID = typer.Argument(..., help="UUID of the organization member")
):
    """
    Delete organization member.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.delete_organization_member(organization_id, organization_member_id))


###################################################
# Organization Member Invite App
###################################################

organization_member_invite_app = typer.Typer(cls=OrderedCommands)
organization_member_app.add_typer(organization_member_invite_app, name="invite",
                                  help="Operations on member invites of organization the API key owner has direct"
                                       "access to")


@organization_member_invite_app.command(name='list')
def organization_member_invite_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the member invites of organization this user has direct access to.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organization_members_invites(organization_id))


@organization_member_invite_app.command(name='create')
def organization_member_invite_create(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_invite_email: str = typer.Argument(..., help="E-mail of the organization member"),
        organization_member_invite_role: Optional[List[Roles]] = typer.Option([x.value for x in Roles],
                                                                              help="Role of the organization member",
                                                                              case_sensitive=False)
):
    """
    Create organization member invite.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.create_organization_members_invite(organization_id, organization_member_invite_email,
                                                        organization_member_invite_role))


@organization_member_invite_app.command(name='get')
def organization_member_invite_get(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_invite_email: str = typer.Argument(..., help="E-mail of the organization member invite")
):
    """
    Get organization member invite.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.get_organization_member(organization_id, organization_member_invite_email))


@organization_member_invite_app.command(name='delete')
def organization_member_invite_delete(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_invite_email: str = typer.Argument(..., help="E-mail of the organization member")
):
    """
    Delete organization member invite.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.delete_organization_member_invite(organization_id, organization_member_invite_email))


@organization_member_invite_app.command(name='resend')
def organization_member_invite_resend(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_member_invite_email: str = typer.Argument(..., help="E-mail of the organization member")
):
    """
    Resend organization member invitation.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.resend_organization_member_invite(organization_id, organization_member_invite_email))


###################################################
# Organization Follower App
###################################################

organization_follower_app = typer.Typer(cls=OrderedCommands)
organization_app.add_typer(organization_follower_app, name="follower",
                           help="Operations on followers of organization the API key owner has direct access to")


@organization_follower_app.command(name='list')
def organization_follower_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the followers of organization this user has direct access to.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organization_followers(organization_id))


@organization_follower_app.command(name='stop')
def organization_follower_stop(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_follower_id: UUID = typer.Argument(..., help="UUID of the organization follower")
):
    """
    Stops one organization follower of another.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.stop_organization_follower(organization_id, organization_follower_id))


###################################################
# Organization Follower Request App
###################################################

organization_follower_request_app = typer.Typer(cls=OrderedCommands)
organization_follower_app.add_typer(organization_follower_request_app, name="request",
                                    help="Operations on follower requests of organization the API key owner has direct"
                                         "access to")


@organization_follower_request_app.command(name='list')
def organization_follower_request_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the follower requests of organization this user has direct access to.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organization_followers(organization_id))


@organization_follower_request_app.command(name='create')
def organization_follower_request_create(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        token: UUID = typer.Argument(..., help="Token of the follower request")
):
    """
    Create organization follower request.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.create_organization_follower_request(organization_id, token))


@organization_follower_request_app.command(name='get')
def organization_follower_request_get(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        token: UUID = typer.Argument(..., help="Token of the follower request")
):
    """
    Get organization follower request.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.get_organization_follower_request(organization_id, token))


@organization_follower_request_app.command(name='delete')
def organization_follower_request_delete(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        token: UUID = typer.Argument(..., help="Token of the follower request")
):
    """
    Delete organization follower request.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.delete_organization_follower_request(organization_id, token))


###################################################
# Organization Following App
###################################################

organization_following_app = typer.Typer(cls=OrderedCommands)
organization_app.add_typer(organization_following_app, name="following",
                           help="Operations on following of organization the API key owner has direct access to")


@organization_following_app.command(name='list')
def organization_following_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the following of organization this user has direct access to.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organization_following(organization_id))


@organization_following_app.command(name='stop')
def organization_following_stop(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        organization_following_id: UUID = typer.Argument(..., help="UUID of the organization following")
):
    """
    Stops one organization following of another.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.stop_organization_following(organization_id, organization_following_id))


###################################################
# Organization Following Request App
###################################################

organization_following_request_app = typer.Typer(cls=OrderedCommands)
organization_following_app.add_typer(organization_following_request_app, name="request",
                                     help="Operations on following requests of organization the API key owner has"
                                          "direct access to")


@organization_following_request_app.command(name='list')
def organization_following_request_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the following requests of organization this user has direct access to.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organization_following_requests(organization_id))


@organization_following_request_app.command(name='get')
def organization_following_request_get(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        following_id: UUID = typer.Argument(..., help="UUID of the following request")
):
    """
    Returns a request received by an organization to follow another.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.get_organization_following_request(organization_id, following_id))


@organization_following_request_app.command(name='accept')
def organization_following_request_accept(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        following_id: UUID = typer.Argument(..., help="UUID of the following request")
):
    """
    Accepts a request to follow another organization.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.accept_organization_following_request(organization_id, following_id))


@organization_following_request_app.command(name='decline')
def organization_following_request_decline(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        following_id: UUID = typer.Argument(..., help="UUID of the following request")
):
    """
    Declines a request to follow another organization.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.decline_organization_following_request(organization_id, following_id))


###################################################
# Organization Scan Target App
###################################################

organization_scan_target_app = typer.Typer(cls=OrderedCommands)
organization_app.add_typer(organization_scan_target_app, name="scan_target",
                           help="Operations on scan targets from organizations the API key owner has direct access to")


@organization_scan_target_app.command(name='list')
def organization_scan_target_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization")):
    """
    Lists the scan targets of organization this user has direct access to.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organization_scan_targets(organization_id))


@organization_scan_target_app.command(name='create')
def organization_scan_target_create(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        kind: ScanTargetKind = typer.Argument(..., help="kind of the scan target"),
        name: str = typer.Argument(..., help="name of the scan target"),
        credential: str = typer.Argument(..., help="credential of the scan target"),
        schedule: str = typer.Argument("0 0 * * *", help="schedule of the scan target")
):
    """
    Create a new scan target in organization.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.create_organization_scan_target(organization_id, kind, name, credential, schedule))


@organization_scan_target_app.command(name='get')
def organization_scan_target_get(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target")
):
    """
    Get scan target of organization.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.get_organization_scan_target(organization_id, scan_target_id))


@organization_scan_target_app.command(name='update')
def organization_scan_target_update(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
        name: Optional[str] = typer.Argument(None, help="name of the scan target"),
        schedule: Optional[str] = typer.Argument(None, help="schedule of the scan target")
):
    """
    Update scan target of organization.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.update_organization_scan_target(organization_id, scan_target_id, name, schedule))


@organization_scan_target_app.command(name='delete')
def organization_scan_target_delete(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target")
):
    """
    Delete scan target of organization.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.delete_organization_scan_target(organization_id, scan_target_id))


@organization_scan_target_app.command(name='check')
def organization_scan_target_check(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target")
):
    """
    Check scan target.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.check_organization_scan_target(organization_id, scan_target_id))


@organization_scan_target_app.command(name='onboard_aws')
def onboard_organization_aws_scan_target(
        boto3_profile: str = typer.Option("default", help="Boto3 profile name to use for Onboard AWS Account"),
        region: str = typer.Argument(..., help="AWS Region to deploy CloudFormation"),
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        name: str = typer.Argument(..., help="name of the scan target"),
        credential: str = typer.Argument(..., help="credential of the scan target"),
        schedule: str = typer.Argument("0 0 * * *", help="schedule of the scan target")
):
    """
    Create a new scan target in organization and perform onboard. Requires boto3 and correct AWS IAM Privileges.
    Checkout the required AWS IAM privileges here https://github.com/tenchi-security/zanshin-sdk-python/blob/main/zanshinsdk/docs/README.md
    """
    client = Client(profile=global_options['profile'])
    credential = ScanTargetAWS(credential)
    kind = ScanTargetKind.AWS

    if len(name) < 3:
        raise ValueError("Scan Target name must be at least 3 characters long")

    dump_json(client.onboard_scan_target(boto3_profile=boto3_profile, region=region,
              organization_id=organization_id, kind=kind, name=name, credential=credential, schedule=schedule))


@organization_scan_target_app.command(name='onboard_aws_organization')
def onboard_organization_aws_organization_scan_target(
        target_accounts: AWSOrgRunTarget = typer.Option(
            None, help="choose which accounts to onboard"),
        exclude_account: Optional[List[str]] = typer.Option(
            [], help="ID, Name, E-mail or ARN of AWS Account not to be onboarded. "),
        boto3_profile: str = typer.Option(
            "default", help="Boto3 profile name to use for Onboard AWS Account. If not informed will use \'default\' profile"),
        aws_role_name: str = typer.Option("OrganizationAccountAccessRole",
            help="Name of AWS role that allow access from Management Account to Member accounts.\
                   If not informed will use OrganizationAccountAccessRole."),
        region: str = typer.Argument(...,
                                     help="AWS Region to deploy CloudFormation"),
        organization_id: UUID = typer.Argument(...,
                                               help="UUID of the organization"),
        schedule: str = typer.Argument(
            "0 0 * * *", help="schedule of the scan target")
):
    """
    For each of selected accounts in AWS Organization, creates a new Scan Target in informed zanshin organization
    and performs onboarding. Requires boto3 and correct AWS IAM Privileges.
    Checkout the required AWS IAM privileges at
    https://github.com/tenchi-security/zanshin-cli/blob/main/zanshincli/docs/README.md
    """
    client = Client(profile=global_options['profile'])
    boto3_session = boto3.Session(profile_name=boto3_profile)

    # Validate user provided IAM Role Name not ARN
    _validate_role_name(aws_role_name)

    if not target_accounts and exclude_account:
        raise ValueError(
            "exclude_account can only be informed using target-accounts ALL, MEMBERS or MASTER")

    # Fetching organization's existing Scan Targets of kind AWS
    # in order to see if AWS Accounts are already in Zanshin
    typer.echo("Looking for Zanshin AWS Scan Targets")
    organization_current_scan_targets: Iterator[Dict] = client.iter_organization_scan_targets(
        organization_id=organization_id)
    organization_aws_scan_targets: List[ScanTargetAWS] = [sc for sc in organization_current_scan_targets if
                                                          sc['kind'] == ScanTargetKind.AWS]

    # Add all accounts found in zanshin organization to be excluded
    exclude_account_list = list(exclude_account)
    for scan_target in organization_aws_scan_targets:
        exclude_account_list.append(scan_target['credential']['account'])
    exclude_account = tuple(exclude_account_list)

    if target_accounts:
        awsorgrun(session=boto3_session, role=aws_role_name, target=target_accounts, accounts=None,
                  exclude=exclude_account, func=_sdk_onboard_scan_target, region=region,
                  organization_id=organization_id, schedule=schedule)
    else:
        aws_organizations_client: Boto3OrganizationsClient = boto3_session.client(
            'organizations')
        customer_aws_accounts: List[AWSAccount] = _get_aws_accounts_from_organization(
            aws_organizations_client)

        # Check if there're new AWS Accounts in Customer Organization that aren't in Zanshin yet
        typer.echo("Detecting AWS Accounts already in Zanshin Organization")
        onboard_accounts: List[AWSAccount] = []

        for customer_acc in customer_aws_accounts:
            current_acc_id = customer_acc['Id']
            is_aws_account_already_in_zanshin = [
                acc for acc in organization_aws_scan_targets if acc['credential']['account'] == current_acc_id]
            if not is_aws_account_already_in_zanshin:
                onboard_accounts.append(customer_acc)

        # If flag all_accounts is present, it means all AWS Accounts that aren't already in Zanshin organization will be
        # onboarded. Otherwise, we'll prompt the user to select the accounts they want to Onboard manually.
        for acc in onboard_accounts:
            onboard_acc = typer.confirm(
                f"Onboard AWS account {acc['Name']} ({acc['Id']})?", default=True)
            acc["Onboard"] = onboard_acc
            if onboard_acc:
                onboard_acc_name: str = typer.prompt(
                    "Scan Target Name", default=acc['Name'], type=str)
                while (len(onboard_acc_name.strip()) < 3):
                    onboard_acc_name = typer.prompt(
                        "Name must be minimum 3 characters. Scan Target Name", default=acc['Name'], type=str)
                acc["Name"] = onboard_acc_name

        aws_accounts_selected_to_onboard = [
            acc for acc in onboard_accounts if acc["Onboard"]]
        typer.echo(
            f"{len(aws_accounts_selected_to_onboard)} Account(s) marked to Onboard")
        if not aws_accounts_selected_to_onboard:
            raise typer.Exit()
        awsorgrun(target=AWSOrgRunTarget.NONE, exclude=exclude_account_list, session=boto3_session, role=aws_role_name,
                  accounts=aws_accounts_selected_to_onboard, func=_sdk_onboard_scan_target, region=region,
                  organization_id=organization_id, schedule=schedule)


def _sdk_onboard_scan_target(target, aws_account_id, aws_account_name, boto3_session, region, organization_id, schedule):
    client = Client(profile=global_options['profile'])
    account_credential = ScanTargetAWS(aws_account_id)
    client.onboard_scan_target(boto3_session=boto3_session, region=region, kind=ScanTargetKind.AWS, name=aws_account_name,
                               schedule=schedule, organization_id=organization_id, credential=account_credential)


def _validate_role_name(aws_cross_account_role_name: str):
    """
    Make sure provided role name is valid as in it's not an ARN, and not bigger than AWS constraints.
    :param: aws_cross_account_role_name - Role name received from user input
    """
    if ':' in aws_cross_account_role_name:
        raise ValueError(
            f"IAM Role Name required. Value {aws_cross_account_role_name} is not a role name.")
    if len(aws_cross_account_role_name) <= 1 or len(aws_cross_account_role_name) >= 65:
        raise ValueError(f"IAM Role Name is invalid.")

def _get_aws_accounts_from_organization(boto3_organizations_client: Boto3OrganizationsClient) -> List[AWSAccount]:
    """
    With boto3 Organizations Client, list AWS Accounts from Organization.
    If [NextToken] is present, keeps fetching Accounts until complete.
    Creates AWSAccount class with response data.

    :param: boto3_organizations_client - boto3 Client for Organizations
    :return: aws_accounts_response: List[AWSAccount]
    """

    aws_accounts_response: List[AWSAccount] = []
    req_aws_accounts = boto3_organizations_client.list_accounts(MaxResults=5)

    for acc in req_aws_accounts['Accounts']:
        aws_accounts_response.append(AWSAccount(
            Id=acc['Id'], Name=acc['Name'], Arn=acc['Arn'], Email=acc['Email']))

    if not 'NextToken' in req_aws_accounts:
        return aws_accounts_response

    while req_aws_accounts['NextToken']:
        req_aws_accounts = boto3_organizations_client.list_accounts(
            MaxResults=5, NextToken=req_aws_accounts['NextToken'])
        for acc in req_aws_accounts['Accounts']:
            aws_accounts_response.append(AWSAccount(
                Id=acc['Id'], Name=acc['Name'], Arn=acc['Arn'], Email=acc['Email']))
        if not 'NextToken' in req_aws_accounts:
            break
    return aws_accounts_response


###################################################
# Organization Scan Target Scan App
###################################################

organization_scan_target_scan_app = typer.Typer(cls=OrderedCommands)
organization_scan_target_app.add_typer(organization_scan_target_scan_app, name="scan",
                                       help="Operations on scan targets from organizations the API key owner has direct"
                                            "access to")


@organization_scan_target_scan_app.command(name='start')
def organization_scan_target_scan_start(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target")
):
    """
    Starts a scan on the specified scan target.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.start_organization_scan_target_scan(organization_id, scan_target_id))


@organization_scan_target_scan_app.command(name='stop')
def organization_scan_target_scan_stop(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target")
):
    """
    Stop a scan on the specified scan target.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.stop_organization_scan_target_scan(organization_id, scan_target_id))


@organization_scan_target_scan_app.command(name='list')
def organization_scan_target_scan_list(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target")
):
    """
    Lists the scan target scans of organization this user has direct access to.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(client.iter_organization_scan_target_scans(organization_id, scan_target_id))


@organization_scan_target_scan_app.command(name='get')
def organization_scan_target_scan_get(
        organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
        scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
        scan_id: UUID = typer.Argument(..., help="UUID of the scan")
):
    """
    Get scan of scan target.
    """
    client = Client(profile=global_options['profile'])
    dump_json(client.get_organization_scan_target_scan(organization_id, scan_target_id, scan_id))


###################################################
# Alert
###################################################

alert_app = typer.Typer(cls=OrderedCommands)
main_app.add_typer(alert_app, name="alert",
                   help="Operations on alerts the API key owner has direct access to")


@alert_app.command(name='list')
def alert_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
               scan_target_id: Optional[List[UUID]] = typer.Option(None,
                                                                   help="Only list alerts from the specified"
                                                                        "scan targets."),
               states: Optional[List[AlertState]] = typer.Option(
                   [x.value for x in AlertState if x != AlertState.CLOSED],
                   help="Only list alerts in the specified states.", case_sensitive=False),
               severity: Optional[List[AlertSeverity]] = typer.Option([x.value for x in AlertSeverity],
                                                                      help="Only list alerts with the specified"
                                                                           "severities",
                                                                      case_sensitive=False),
               ):
    """
    List alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(
        client.iter_alerts(organization_id=organization_id, scan_target_ids=scan_target_id, states=states,
                           severities=severity)
    )


@alert_app.command(name='list_following')
def alert_following_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                         following_ids: Optional[List[UUID]] = typer.Option(None,
                                                                            help="Only list alerts from the specified"
                                                                                 "scan targets."),
                         states: Optional[List[AlertState]] = typer.Option(
                             [x.value for x in AlertState if x != AlertState.CLOSED],
                             help="Only list alerts in the specified states.", case_sensitive=False),
                         severity: Optional[List[AlertSeverity]] = typer.Option([x.value for x in AlertSeverity],
                                                                                help="Only list alerts with the"
                                                                                     "specified severities",
                                                                                case_sensitive=False)
                         ):
    """
    List following alerts from a given organization, with optional filters by following ids, state or severity.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(
        client.iter_following_alerts(organization_id=organization_id, following_ids=following_ids, states=states,
                                     severities=severity)
    )


@alert_app.command(name='list_history')
def alert_history_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                       scan_target_id: Optional[List[UUID]] = typer.Option(None,
                                                                           help="Only list alerts from the specified"
                                                                                "scan targets."),
                       cursor: Optional[str] = typer.Option(None, help="Cursor."),
                       persist: Optional[bool] = typer.Option(False, help="Persist.")
                       ):
    """
    List alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=global_options['profile'])

    if persist:
        iter_alerts = FilePersistentAlertsIterator(filename='zanshin', client=client, organization_id=organization_id,
                                                   scan_target_ids=scan_target_id, cursor=cursor)
        output_iterable(
            iter_alerts,
            None,
            iter_alerts.save
        )
    else:
        output_iterable(
            client.iter_alerts_history(organization_id=organization_id, scan_target_ids=scan_target_id, cursor=cursor)
        )


@alert_app.command(name='list_history_following')
def alert_history_following_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                                 following_ids: Optional[List[UUID]] = typer.Option(None,
                                                                                    help="Only list alerts from the specified"
                                                                                         "scan targets."),
                                 cursor: Optional[str] = typer.Option(None, help="Cursor."),
                                 persist: Optional[bool] = typer.Option(False, help="Persist.")
                                 ):
    """
    List alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=global_options['profile'])

    if persist:
        iter_alerts = FilePersistentFollowingAlertsIterator(filename='zanshin', client=client,
                                                            organization_id=organization_id,
                                                            following_ids=following_ids, cursor=cursor)
        output_iterable(
            iter_alerts,
            None,
            iter_alerts.save
        )
    else:
        output_iterable(
            client.iter_alerts_following_history(organization_id=organization_id, following_ids=following_ids,
                                                 cursor=cursor)
        )


@alert_app.command(name='list_grouped')
def grouped_alert_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                       scan_target_id: Optional[List[UUID]] = typer.Option(None,
                                                                           help="Only list alerts from the specified"
                                                                                "scan targets."),
                       state: Optional[List[AlertState]] = typer.Option(
                           [x.value for x in AlertState if x != AlertState.CLOSED],
                           help="Only list alerts in the specified states.", case_sensitive=False),
                       severity: Optional[List[AlertSeverity]] = typer.Option([x.value for x in AlertSeverity],
                                                                              help="Only list alerts with the specified"
                                                                                   "severities",
                                                                              case_sensitive=False)):
    """
    List grouped alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(
        client.iter_grouped_alerts(organization_id=organization_id, scan_target_ids=scan_target_id, states=state,
                                   severities=severity))


@alert_app.command(name='list_grouped_following')
def grouped_alert_following_list(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                                 following_ids: Optional[List[UUID]] = typer.Option(None,
                                                                                    help="Only list alerts from the"
                                                                                         "specified scan targets."),
                                 state: Optional[List[AlertState]] = typer.Option(
                                     [x.value for x in AlertState if x != AlertState.CLOSED],
                                     help="Only list alerts in the specified states.", case_sensitive=False),
                                 severity: Optional[List[AlertSeverity]] = typer.Option(
                                     [x.value for x in AlertSeverity],
                                     help="Only list alerts with the specified severities",
                                     case_sensitive=False)):
    """
    List grouped following alerts from a given organization, with optional filters by scan target, state or severity.
    """
    client = Client(profile=global_options['profile'])
    output_iterable(
        client.iter_grouped_following_alerts(organization_id=organization_id, following_ids=following_ids, states=state,
                                             severities=severity))


@alert_app.command(name='get')
def alert_get(alert_id: UUID = typer.Argument(..., help="UUID of the alert to look up"),
              list_history: Optional[bool] = typer.Option(False, help="History of this alert."),
              list_comments: Optional[bool] = typer.Option(False, help="Comments of this alert.")):
    """
    Returns details about a specified alert
    """
    if list_history:
        client = Client(profile=global_options['profile'])
        output_iterable(client.iter_alert_history(alert_id))
    elif list_comments:
        client = Client(profile=global_options['profile'])
        output_iterable(client.iter_alert_comments(alert_id))
    else:
        client = Client(profile=global_options['profile'])
        typer.echo(dumps(client.get_alert(alert_id), indent=4))


###################################################
# Summary
###################################################

summary_app = typer.Typer(cls=OrderedCommands)
main_app.add_typer(summary_app, name="summary",
                   help="Operations on summaries the API key owner has direct access to")


@summary_app.command(name='alert')
def summary_alert(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                  scan_target_id: Optional[List[UUID]] = typer.Option(None,
                                                                      help="Only summarize alerts from the specified"
                                                                           "scan targets, defaults to all.")):
    """
    Gets a summary of the current state of alerts for an organization, both in total and broken down by scan target.
    """
    client = Client(profile=global_options['profile'])

    dump_json(client.get_alert_summaries(organization_id, scan_target_id))


@summary_app.command(name='alert_following')
def summary_alert_following(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                            following_ids: Optional[List[UUID]] = typer.Option(None,
                                                                               help="Only summarize alerts from the"
                                                                                    "specified following, defaults to"
                                                                                    "all.")):
    """
    Gets a summary of the current state of alerts for followed organizations.
    """
    client = Client(profile=global_options['profile'])

    dump_json(client.get_following_alert_summaries(organization_id, following_ids))


@summary_app.command(name='scan')
def summary_scan(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                 scan_target_ids: Optional[List[UUID]] = typer.Option(None,
                                                                      help="Only summarize alerts from the specified"
                                                                           "scan targets, defaults to all."),
                 days: Optional[int] = typer.Option(7, help="Number of days to go back in time in historical search")
                 ):
    """
    Returns summaries of scan results over a period of time, summarizing number of alerts that changed states.
    """
    client = Client(profile=global_options['profile'])

    dump_json(client.get_scan_summaries(organization_id, scan_target_ids, days))


@summary_app.command(name='scan_following')
def summary_scan_following(organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
                           following_ids: Optional[List[UUID]] = typer.Option(None,
                                                                              help="Only summarize alerts from the"
                                                                                   "specified following, defaults to"
                                                                                   "all."),
                           days: Optional[int] = typer.Option(7,
                                                              help="Number of days to go back in time in historical"
                                                                   "search")
                           ):
    """
    Returns summaries of scan results over a period of time, summarizing number of alerts that changed states.
    """
    client = Client(profile=global_options['profile'])

    dump_json(client.get_scan_summaries(organization_id, following_ids, days))


if __name__ == "__main__":
    main_app()
