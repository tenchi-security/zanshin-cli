#!/usr/bin/env python3

import logging
import os
import subprocess
from enum import Enum
from sys import stderr
from typing import Any, Callable, Dict, Iterable, List

import boto3
import botocore

__version__ = "1.0.0"

logger = logging.getLogger("awsorgrun")
handler = logging.StreamHandler(stderr)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s pid=%(process)d %(module)s %(levelname)s %(message)s",
        "%Y-%m-%dT%H:%M:%S%z",
    )
)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class AWSOrgRunTarget(str, Enum):
    ALL = "ALL"
    MASTER = "MASTER"
    MEMBERS = "MEMBERS"
    NONE = "NONE"


def awsorgrun(
    session: boto3.Session,
    role: str,
    target: AWSOrgRunTarget,
    exclude: List[str],
    accounts: List[any],
    func: Callable[..., None],
    *args: Any,
    **kwargs: Any
) -> None:
    """
    Method that runs a given funcion in all AWS accounts from organization.

    :param session: boto3 session used to assume role in other accounts
    :param role: role name to assume in other accounts
    :param target: specify the target accounts, that can be MASTER, MEMBERS or ALL
    :param exclude: accounts not to be onboarded from selection
    :param func: the function to run for all accounts in organization
    """

    org_client = session.client("organizations")
    org_master_id = org_client.describe_organization()["Organization"][
        "MasterAccountId"
    ]

    if not accounts:
        accounts = list_member_accounts(org_client)

    for account in accounts:
        if not account:
            logger.error("no Organizations accounts found!")
        elif exclude and (
            account["Name"] in exclude
            or account["Id"] in exclude
            or account["Arn"] in exclude
            or account["Email"] in exclude
        ):
            logger.info(
                "skipping account {0:s} ({1:s})...".format(
                    account["Id"], account["Name"]
                )
            )
        elif account["Status"] == "SUSPENDED" or account["Status"] == "PENDING_CLOSURE":
            logger.info(
                "skipping account {0:s} ({1:s}) because it is in {2:s} state".format(
                    account["Id"], account["Name"], account["Status"]
                )
            )
        elif account["Id"] == org_master_id:
            if target is AWSOrgRunTarget.ALL or target is AWSOrgRunTarget.MASTER:
                logger.info(
                    "found master account {0:s} ({1:s})".format(
                        account["Id"], account["Name"]
                    )
                )
                func(
                    AWSOrgRunTarget.MASTER,
                    org_master_id,
                    account["Name"],
                    session,
                    *args,
                    **kwargs
                )
        elif (
            target is AWSOrgRunTarget.ALL
            or target is AWSOrgRunTarget.MEMBERS
            or target is AWSOrgRunTarget.NONE
        ):
            logger.info(
                "found member account {0:s} ({1:s})".format(
                    account["Id"], account["Name"]
                )
            )
            func(
                AWSOrgRunTarget.MEMBERS,
                account["Id"],
                account["Name"],
                get_sts_session(session, account["Id"], role),
                *args,
                **kwargs
            )


def list_member_accounts(org_client: "botocore.client.Organizations") -> Iterable[Dict]:
    response = org_client.list_accounts()
    while True:
        yield from response.get("Accounts", [])
        if response.get("NextToken", None):
            response = org_client.list_accounts(NextToken=response["NextToken"])
        else:
            return


def get_sts_session(
    session: boto3.session.Session, account_id: str, role_name: str
) -> boto3.session.Session:
    sts_client = session.client("sts")
    partition = sts_client.get_caller_identity()["Arn"].split(":")[1]
    response = sts_client.assume_role(
        RoleArn="arn:{}:iam::{}:role/{}".format(partition, account_id, role_name),
        RoleSessionName="awsorgrun",
    )
    logger.info(
        "got STS credential {0:s} for account {1:s}".format(
            response["Credentials"]["AccessKeyId"], account_id
        )
    )
    return boto3.session.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
        region_name=session.region_name,
    )


def run_command(
    target: AWSOrgRunTarget,
    account_id: str,
    session: boto3.session.Session,
    command: str,
) -> None:
    session_creds = session.get_credentials()
    env = os.environ.copy()
    if session.region_name:
        env["AWS_DEFAULT_REGION"] = session.region_name
    env["AWS_ACCESS_KEY_ID"] = session_creds.access_key
    env["AWS_SECRET_ACCESS_KEY"] = session_creds.secret_key
    if session_creds.token:
        env["AWS_SESSION_TOKEN"] = session_creds.token
    elif "AWS_SESSION_TOKEN" in env:
        del env["AWS_SESSION_TOKEN"]
    proc = subprocess.run(command, shell=True, env=env)
    logger.info("command finished with exit status {0:d}".format(proc.returncode))
