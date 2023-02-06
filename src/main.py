import sys
from configparser import RawConfigParser
from datetime import timedelta
from stat import S_IRUSR, S_IWUSR
from sys import version as python_version, stderr
from time import perf_counter
from lib.models import OutputFormat
import config.sdk as sdk_config
import logging
import typer
from typer import Typer
from zanshinsdk import __version__ as sdk_version
from zanshinsdk.client import CONFIG_DIR, CONFIG_FILE
from lib.version import __version__ as cli_version

###################################################
# Exchanger
###################################################

def zanshin_exchanger(_, value, __):
    print(value)


sys.excepthook = zanshin_exchanger

###################################################
# Main App
###################################################

main_app: Typer = typer.Typer(name="zanshin", no_args_is_help=True)


@main_app.callback()
def global_options_callback(ctx: typer.Context,
                            profile: str = typer.Option("default",
                                                        help="Configuration file section to read API key"
                                                             "and configuration from"),
                            output_format: OutputFormat = typer.Option(OutputFormat.JSON, '--format',
                                                                       help="Output format to use for list operations",
                                                                       case_sensitive=False),
                            verbose: bool = typer.Option(True, help="Print more information to stderr"),
                            debug: bool = typer.Option(False, help="Enable debug logging in the SDK")):
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
                f"zanshin: {sdk_config.entries} object(s) processed in "
                f"{timedelta(seconds=perf_counter() - start_time)}",
                err=True)

        ctx.call_on_close(print_elapsed_time)

    if debug:
        logger = logging.getLogger("zanshinsdk")
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(stderr)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    sdk_config.debug = debug
    sdk_config.verbose = verbose
    sdk_config.profile = profile
    sdk_config.format = output_format
    
@main_app.command()
def init():
    """
    Update settings on configuration file.
    """
    cfg = RawConfigParser()
    cfg.read(CONFIG_FILE)
    typer.echo("This command will allow you to set up profiles in the configuration file.")
    profile = typer.prompt("Please enter the profile name to use", default=sdk_config.profile)
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

import bin.account as account
main_app.add_typer(account.app, name="account",
                   help="Operations on user the API key owner has direct access to")


###################################################
# Account Invites App
###################################################

import bin.invites as invites
account.app.add_typer(invites.app, name="invites",
                      help="Operations on invites from account the API key owner has direct access to")


###################################################
# Account API key App
###################################################

import bin.api_key as api_key
account.app.add_typer(api_key.app, name="api_key",
                      help="Operations on API keys from account the API key owner has direct access to")


###################################################
# Organization App
###################################################

import bin.organization as organization
main_app.add_typer(organization.app, name="organization",
                   help="Operations on organizations the API key owner has direct access to")


###################################################
# Organization Member App
###################################################

import bin.member as organization_member
organization.app.add_typer(organization_member.app, name="member",
                           help="Operations on members of organization the API key owner has direct access to")


###################################################
# Organization Member Invite App
###################################################

import bin.member_invite as member_invite
organization_member.app.add_typer(member_invite.app, name="invite",
                                  help="Operations on member invites of organization the API key owner has direct"
                                       "access to")


###################################################
# Organization Follower App
###################################################

import bin.follower as follower
organization.app.add_typer(follower.app, name="follower",
                           help="Operations on followers of organization the API key owner has direct access to")


###################################################
# Organization Follower Request App
###################################################

import bin.follower_request as follower_request
follower.app.add_typer(follower_request.app, name="request",
                                    help="Operations on follower requests of organization the API key owner has direct"
                                         "access to")


###################################################
# Organization Following App
###################################################

import bin.following as following
organization.app.add_typer(following.app, name="following",
                           help="Operations on following of organization the API key owner has direct access to")


###################################################
# Organization Following Request App
###################################################

import bin.following_request as following_request
following.app.add_typer(following_request.app, name="request",
                                     help="Operations on following requests of organization the API key owner has"
                                          "direct access to")


###################################################
# Organization Scan Target App
###################################################

import bin.scan_target as scan_target
organization.app.add_typer(scan_target.app, name="scan_target",
                           help="Operations on scan targets from organizations the API key owner has direct access to")


###################################################
# Organization Scan Target Scan App
###################################################

import bin.scan as scan
scan_target.app.add_typer(scan.app, name="scan",
                                       help="Operations on scan targets from organizations the API key owner has direct"
                                            " access to")


###################################################
# Scan Target Groups App
###################################################

import bin.scan_target_groups as scan_target_groups
organization.app.add_typer(scan_target_groups.app, name="scan-target-groups",
                   help="Operations on organizations scan target groups the API key owner has direct access to")


###################################################
# Alert
###################################################

import bin.alerts as alerts
main_app.add_typer(alerts.app, name="alert",
                   help="Operations on alerts the API key owner has direct access to")


###################################################
# Summary
###################################################

import bin.summary as summary
main_app.add_typer(summary.app, name="summary",
                   help="Operations on summaries the API key owner has direct access to")


if __name__ == "__main__":
    main_app()
