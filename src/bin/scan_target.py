from typing import Dict, Iterator, List, Optional
from uuid import UUID

import boto3
import typer
from boto3_type_annotations.organizations import Client as Boto3OrganizationsClient
from zanshinsdk import Client
from zanshinsdk.client import DAILY as DAILY_SCHEDULE
from zanshinsdk.client import (
    OAuthTargetKind,
    ScanTargetAWS,
    ScanTargetAZURE,
    ScanTargetBITBUCKET,
    ScanTargetDOMAIN,
    ScanTargetGCP,
    ScanTargetGITHUB,
    ScanTargetGITLAB,
    ScanTargetGWORKSPACE,
    ScanTargetHUAWEI,
    ScanTargetJIRA,
    ScanTargetKind,
    ScanTargetMS365,
    ScanTargetORACLE,
    ScanTargetSALESFORCE,
    ScanTargetSchedule,
    ScanTargetSLACK,
    ScanTargetZENDESK,
)

import src.config.sdk as sdk_config
from src.lib.awsorgrun import AWSOrgRunTarget, awsorgrun
from src.lib.models import AWSAccount
from src.lib.utils import dump_json, output_iterable

app = typer.Typer()


@app.command(name="list")
def organization_scan_target_list(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization")
):
    """
    Lists the scan targets of organization this user has direct access to.
    """
    client = Client(profile=sdk_config.profile)
    output_iterable(client.iter_organization_scan_targets(organization_id))


@app.command(name="create")
def organization_scan_target_create(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    kind: ScanTargetKind = typer.Argument(..., help="kind of the scan target"),
    name: str = typer.Argument(..., help="name of the scan target"),
    credential: str = typer.Argument(..., help="credential of the scan target"),
    schedule: str = typer.Argument(
        DAILY_SCHEDULE.json(), help="schedule of the scan target"
    ),
):
    """
    Create a new scan target in organization.
    """
    client = Client(profile=sdk_config.profile)

    credential_map = {
        ScanTargetKind.AWS: ScanTargetAWS,
        ScanTargetKind.AZURE: ScanTargetAZURE,
        ScanTargetKind.GCP: ScanTargetGCP,
        ScanTargetKind.HUAWEI: ScanTargetHUAWEI,
        ScanTargetKind.DOMAIN: ScanTargetDOMAIN,
        ScanTargetKind.ORACLE: ScanTargetORACLE,
        ScanTargetKind.ZENDESK: ScanTargetZENDESK,
        ScanTargetKind.GWORKSPACE: ScanTargetGWORKSPACE,
        ScanTargetKind.SLACK: ScanTargetSLACK,
        ScanTargetKind.BITBUCKET: ScanTargetBITBUCKET,
        ScanTargetKind.JIRA: ScanTargetJIRA,
        ScanTargetKind.GITLAB: ScanTargetGITLAB,
        ScanTargetKind.SALESFORCE: ScanTargetSALESFORCE,
        ScanTargetKind.MS365: ScanTargetMS365,
        ScanTargetKind.GITHUB: ScanTargetGITHUB,
    }

    if kind not in credential_map:
        raise ValueError(f"Unsupported kind: {kind}")

    credential = credential_map[kind](credential)

    scan_target = client.create_organization_scan_target(
        organization_id,
        kind,
        name,
        credential,
        ScanTargetSchedule.model_validate_json(schedule),
    )

    if kind not in [member.value for member in OAuthTargetKind]:
        return dump_json(scan_target)

    should_return_oauth_link = typer.prompt(
        "Do you want to receive the oauth link from this scan target? (y/n)",
        default="n",
        type=str,
    )

    if should_return_oauth_link.lower() != "y":
        return dump_json(scan_target)

    dump_json(client.get_kind_oauth_link(organization_id, scan_target["id"], kind))


@app.command(name="get")
def organization_scan_target_get(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
):
    """
    Get scan target of organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_organization_scan_target(organization_id, scan_target_id))


@app.command(name="update")
def organization_scan_target_update(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
    name: Optional[str] = typer.Argument(None, help="name of the scan target"),
    schedule: Optional[str] = typer.Argument(None, help="schedule of the scan target"),
):
    """
    Update scan target of organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(
        client.update_organization_scan_target(
            organization_id,
            scan_target_id,
            name,
            ScanTargetSchedule.model_validate_json(schedule),
        )
    )


@app.command(name="delete")
def organization_scan_target_delete(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
):
    """
    Delete scan target of organization.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.delete_organization_scan_target(organization_id, scan_target_id))


@app.command(name="check")
def organization_scan_target_check(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
):
    """
    Check scan target.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.check_organization_scan_target(organization_id, scan_target_id))


@app.command(name="oauth_link")
def organization_scan_target_oauth_link(
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    scan_target_id: UUID = typer.Argument(..., help="UUID of the scan target"),
):
    """
    Retrieve a link to allow the user to authorize zanshin to read info from their scan target environment.
    """
    client = Client(profile=sdk_config.profile)
    dump_json(client.get_scan_target_oauth_link(organization_id, scan_target_id))


@app.command(name="onboard_aws")
def onboard_organization_aws_scan_target(
    boto3_profile: str = typer.Option(
        None, help="Boto3 profile name to use for Onboard AWS Account"
    ),
    region: str = typer.Argument(..., help="AWS Region to deploy CloudFormation"),
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    name: str = typer.Argument(..., help="name of the scan target"),
    credential: str = typer.Argument(..., help="credential of the scan target"),
    schedule: str = typer.Argument(
        DAILY_SCHEDULE.json(), help="schedule of the scan target"
    ),
):
    """
    Create a new scan target in organization and perform onboard. Requires boto3 and correct AWS IAM Privileges.
    Checkout the required AWS IAM privileges here https://github.com/tenchi-security/zanshin-sdk-python/blob/main/zanshinsdk/docs/README.md
    """
    client = Client(profile=sdk_config.profile)
    credential = ScanTargetAWS(credential)
    kind = ScanTargetKind.AWS

    if len(name) < 3:
        raise ValueError("Scan Target name must be at least 3 characters long")

    if boto3_profile:
        boto3_session = boto3.Session(profile_name=boto3_profile)
    else:
        boto3_session = boto3.Session()

    dump_json(
        client.onboard_scan_target(
            boto3_session=boto3_session,
            region=region,
            organization_id=organization_id,
            kind=kind,
            name=name,
            credential=credential,
            schedule=ScanTargetSchedule.model_validate_json(schedule),
        )
    )


@app.command(name="onboard_aws_organization")
def onboard_organization_aws_organization_scan_target(
    target_accounts: AWSOrgRunTarget = typer.Option(
        None, help="choose which accounts to onboard"
    ),
    exclude_account: Optional[List[str]] = typer.Option(
        None, help="ID, Name, E-mail or ARN of AWS Account not to be onboarded"
    ),
    boto3_profile: str = typer.Option(
        None, help="Boto3 profile name to use for Onboard AWS Account"
    ),
    aws_role_name: str = typer.Option(
        "OrganizationAccountAccessRole",
        help="Name of AWS role that allow access from Management Account to Member accounts",
    ),
    region: str = typer.Argument(..., help="AWS Region to deploy CloudFormation"),
    organization_id: UUID = typer.Argument(..., help="UUID of the organization"),
    schedule: str = typer.Argument(
        DAILY_SCHEDULE.json(), help="schedule of the scan target"
    ),
):
    """
    For each of selected accounts in AWS Organization, creates a new Scan Target in informed zanshin organization
    and performs onboarding. Requires boto3 and correct AWS IAM Privileges.
    Checkout the required AWS IAM privileges at
    https://github.com/tenchi-security/zanshin-cli/blob/main/src/lib/docs/README.md
    """
    client = Client(profile=sdk_config.profile)
    if boto3_profile:
        boto3_session = boto3.Session(profile_name=boto3_profile)
    else:
        boto3_session = boto3.Session()

    # Validate user provided IAM Role Name not ARN
    _validate_role_name(aws_role_name)

    if not target_accounts and exclude_account:
        raise ValueError(
            "exclude_account can only be informed using target-accounts ALL, MEMBERS or MASTER"
        )

    # Fetching organization's existing Scan Targets of kind AWS
    # in order to see if AWS Accounts are already in Zanshin
    typer.echo("Looking for Zanshin AWS Scan Targets")
    organization_current_scan_targets: Iterator[Dict] = (
        client.iter_organization_scan_targets(organization_id=organization_id)
    )
    organization_aws_scan_targets: List[ScanTargetAWS] = [
        sc
        for sc in organization_current_scan_targets
        if sc["kind"] == ScanTargetKind.AWS
    ]

    # Add all accounts found in zanshin organization to be excluded
    if not exclude_account:
        exclude_account = []
    exclude_account_list = list(exclude_account)
    for scan_target in organization_aws_scan_targets:
        exclude_account_list.append(scan_target["credential"]["account"])
    exclude_account = tuple(exclude_account_list)

    if target_accounts:
        awsorgrun(
            session=boto3_session,
            role=aws_role_name,
            target=target_accounts,
            accounts=None,
            exclude=exclude_account,
            func=_sdk_onboard_scan_target,
            region=region,
            organization_id=organization_id,
            schedule=ScanTargetSchedule.model_validate_json(schedule),
        )
    else:
        aws_organizations_client: Boto3OrganizationsClient = boto3_session.client(
            "organizations"
        )
        customer_aws_accounts: List[AWSAccount] = _get_aws_accounts_from_organization(
            aws_organizations_client
        )

        # Check if there're new AWS Accounts in Customer Organization that aren't in Zanshin yet
        typer.echo("Detecting AWS Accounts already in Zanshin Organization")
        onboard_accounts: List[AWSAccount] = []

        for customer_acc in customer_aws_accounts:
            current_acc_id = customer_acc["Id"]
            is_aws_account_already_in_zanshin = [
                acc
                for acc in organization_aws_scan_targets
                if acc["credential"]["account"] == current_acc_id
            ]
            if not is_aws_account_already_in_zanshin:
                onboard_accounts.append(customer_acc)

        # If flag all_accounts is present, it means all AWS Accounts that aren't already in Zanshin organization will be
        # onboarded. Otherwise, we'll prompt the user to select the accounts they want to Onboard manually.
        for acc in onboard_accounts:
            onboard_acc = typer.confirm(
                f"Onboard AWS account {acc['Name']} ({acc['Id']})?", default=True
            )
            acc["Onboard"] = onboard_acc
            if onboard_acc:
                onboard_acc_name: str = typer.prompt(
                    "Scan Target Name", default=acc["Name"], type=str
                )
                while len(onboard_acc_name.strip()) < 3:
                    onboard_acc_name = typer.prompt(
                        "Name must be minimum 3 characters. Scan Target Name",
                        default=acc["Name"],
                        type=str,
                    )
                acc["Name"] = onboard_acc_name

        aws_accounts_selected_to_onboard = [
            acc for acc in onboard_accounts if acc["Onboard"]
        ]
        typer.echo(
            f"{len(aws_accounts_selected_to_onboard)} Account(s) marked to Onboard"
        )
        if not aws_accounts_selected_to_onboard:
            raise typer.Exit()
        awsorgrun(
            target=AWSOrgRunTarget.NONE,
            exclude=exclude_account_list,
            session=boto3_session,
            role=aws_role_name,
            accounts=aws_accounts_selected_to_onboard,
            func=_sdk_onboard_scan_target,
            region=region,
            organization_id=organization_id,
            schedule=ScanTargetSchedule.model_validate_json(schedule),
        )


def _sdk_onboard_scan_target(
    target,
    aws_account_id,
    aws_account_name,
    boto3_session,
    region,
    organization_id,
    schedule,
):
    client = Client(profile=sdk_config.profile)
    account_credential = ScanTargetAWS(aws_account_id)
    client.onboard_scan_target(
        boto3_session=boto3_session,
        region=region,
        kind=ScanTargetKind.AWS,
        name=aws_account_name,
        schedule=schedule,
        organization_id=organization_id,
        credential=account_credential,
    )


def _validate_role_name(aws_cross_account_role_name: str):
    """
    Make sure provided role name is valid as in it's not an ARN, and not bigger than AWS constraints.
    :param: aws_cross_account_role_name - Role name received from user input
    """
    if ":" in aws_cross_account_role_name:
        raise ValueError(
            f"IAM Role Name required. Value {aws_cross_account_role_name} is not a role name."
        )
    if len(aws_cross_account_role_name) <= 1 or len(aws_cross_account_role_name) >= 65:
        raise ValueError("IAM Role Name is invalid.")


def _get_aws_accounts_from_organization(
    boto3_organizations_client: Boto3OrganizationsClient,
) -> List[AWSAccount]:
    """
    With boto3 Organizations Client, list AWS Accounts from Organization.
    If [NextToken] is present, keeps fetching Accounts until complete.
    Creates AWSAccount class with response data.

    :param: boto3_organizations_client - boto3 Client for Organizations
    :return: aws_accounts_response: List[AWSAccount]
    """

    aws_accounts_response: List[AWSAccount] = []
    req_aws_accounts = boto3_organizations_client.list_accounts(MaxResults=5)

    for acc in req_aws_accounts["Accounts"]:
        aws_accounts_response.append(
            AWSAccount(
                Id=acc["Id"], Name=acc["Name"], Arn=acc["Arn"], Email=acc["Email"]
            )
        )

    if "NextToken" not in req_aws_accounts:
        return aws_accounts_response

    while req_aws_accounts["NextToken"]:
        req_aws_accounts = boto3_organizations_client.list_accounts(
            MaxResults=5, NextToken=req_aws_accounts["NextToken"]
        )
        for acc in req_aws_accounts["Accounts"]:
            aws_accounts_response.append(
                AWSAccount(
                    Id=acc["Id"], Name=acc["Name"], Arn=acc["Arn"], Email=acc["Email"]
                )
            )
        if "NextToken" not in req_aws_accounts:
            break
    return aws_accounts_response
