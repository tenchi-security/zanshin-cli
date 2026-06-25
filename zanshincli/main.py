import logging
import sys
from configparser import RawConfigParser
from datetime import timedelta
from stat import S_IRUSR, S_IWUSR
from sys import stderr
from sys import version as python_version
from time import perf_counter

import typer
from typer import Typer
from zanshinsdk import __version__ as sdk_version
from zanshinsdk.client import CONFIG_DIR, CONFIG_FILE

import src.bin.account as account
import src.bin.alerts as alerts
import src.bin.api_key as api_key
import src.bin.follower as follower
import src.bin.follower_request as follower_request
import src.bin.following as following
import src.bin.following_request as following_request
import src.bin.invites as invites
import src.bin.member as organization_member
import src.bin.member_invite as member_invite
import src.bin.organization as organization
import src.bin.scan as scan
import src.bin.scan_target as scan_target
import src.bin.scan_target_groups as scan_target_groups
import src.bin.summary as summary
import src.config.sdk as sdk_config
from src.lib.models import OutputFormat
from src.lib.version import __version__ as cli_version

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
def global_options_callback(
    ctx: typer.Context,
    profile: str = typer.Option(
        "default",
        help="Configuration file section to read API key" "and configuration from",
    ),
    output_format: OutputFormat = typer.Option(
        OutputFormat.JSON,
        "--format",
        help="Output format to use for list operations",
        case_sensitive=False,
    ),
    verbose: bool = typer.Option(True, help="Print more information to stderr"),
    debug: bool = typer.Option(False, help="Enable debug logging in the SDK"),
):
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
                err=True,
            )

        ctx.call_on_close(print_elapsed_time)

    if debug:
        logger = logging.getLogger("zanshinsdk")
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(stderr)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(name)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    sdk_config.debug = debug
    sdk_config.verbose = verbose
    sdk_config.profile = profile
    sdk_config.format = output_format


@main_app.command()
def init():
    """
    Initialize or update the Zanshin CLI configuration file with an API profile.
    """
    cfg = RawConfigParser()
    cfg.read(CONFIG_FILE)
    typer.echo(
        "This command will allow you to set up profiles in the configuration file."
    )
    profile = typer.prompt(
        "Please enter the profile name to use", default=sdk_config.profile
    )
    if cfg.has_section(profile):
        typer.confirm("Profile already exists. Overwrite?", abort=True)
    else:
        cfg.add_section(profile)
    cfg.set(
        profile, "api_key", typer.prompt("Please enter the API key", hide_input=True)
    )
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("w") as f:
        cfg.write(f)
    CONFIG_FILE.chmod(S_IRUSR | S_IWUSR)


@main_app.command()
def version():
    """
    Display the current versions of the Zanshin CLI, SDK, and Python.
    """
    typer.echo(f"Zanshin CLI v{cli_version}")
    typer.echo(f"Zanshin Python SDK v{sdk_version}")
    typer.echo(f"Python {python_version}")


###################################################
# Account App
###################################################

main_app.add_typer(
    account.app,
    name="account",
    help="Manage the user account associated with the current API key.",
)


###################################################
# Account Invites App
###################################################

account.app.add_typer(
    invites.app,
    name="invites",
    help="Manage pending invitations for the logged-in user.",
)


###################################################
# Account API key App
###################################################

account.app.add_typer(
    api_key.app,
    name="api_key",
    help="Manage API keys associated with the logged-in user account.",
)


###################################################
# Organization App
###################################################

main_app.add_typer(
    organization.app,
    name="organization",
    help="Manage organizations the logged-in user has access to.",
)


###################################################
# Organization Member App
###################################################

organization.app.add_typer(
    organization_member.app,
    name="member",
    help="Manage members within an organization.",
)


###################################################
# Organization Member Invite App
###################################################

organization_member.app.add_typer(
    member_invite.app,
    name="invite",
    help="Manage member invitations for an organization.",
)


###################################################
# Organization Follower App
###################################################

organization.app.add_typer(
    follower.app,
    name="follower",
    help="Manage followers of an organization.",
)


###################################################
# Organization Follower Request App
###################################################

follower.app.add_typer(
    follower_request.app,
    name="request",
    help="Manage incoming requests to follow an organization."
    "access to",
)


###################################################
# Organization Following App
###################################################

organization.app.add_typer(
    following.app,
    name="following",
    help="Manage relationships with following organizations.",
)


###################################################
# Organization Following Request App
###################################################

following.app.add_typer(
    following_request.app,
    name="request",
    help="Manage outgoing requests to follow other organizations.",
)


###################################################
# Organization Scan Target App
###################################################

organization.app.add_typer(
    scan_target.app,
    name="scan_target",
    help="Manage scan targets within an organization.",
)


###################################################
# Organization Scan Target Scan App
###################################################

scan_target.app.add_typer(
    scan.app,
    name="scan",
    help="Manage and trigger scans for specific scan targets.",
)


###################################################
# Scan Target Groups App
###################################################

organization.app.add_typer(
    scan_target_groups.app,
    name="scan-target-groups",
    help="Manage scan target groups within an organization.",
)


###################################################
# Alert
###################################################

main_app.add_typer(
    alerts.app,
    name="alert",
    help="Manage and view security alerts across organizations.",
)


###################################################
# Summary
###################################################

main_app.add_typer(
    summary.app,
    name="summary",
    help="Generate aggregated data summaries and reports.",
)


if __name__ == "__main__":
    main_app()
