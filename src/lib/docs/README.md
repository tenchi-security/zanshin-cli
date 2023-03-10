# Zanshin Python CLI Documentation for AWS

This section contains information about how to use methods available in the Zanshin Python CLI to onboard AWS Accounts.

## What is Onboarding?

Onboarding is the process of adding new AWS Account (Scan Targets) to your Organization in Zanshin.

### zanshin organization scan_target onboard_aws_organization

Using this method you can onboard AWS Organizations, that are a group of AWS Accounts.
This method automatically creates a new Scan Targets to the Zanshin Organization informed in parameters and performs the onbard creating the roles required in each of your AWS Accounts.

Currently using the Zanshin CLI you're only able to onboard **AWS Scan Targets**.

> :warning: This method will deploy a CloudFormation stack in each of your AWS accounts.


**Currently supports only AWS Scan Targets.**

_For AWS Scan Target:_

- To be able to onboard AWS Organizations, you need to run this CLI with privileges on the AWS Organization **Management Account** otherwise it won't work. The reason for this is that only from the Management Account you can list Organizations Accounts and assume roles in Member accounts.

- **How it works**
  - This command can be executed in two different modes: **Interactive** or **Automatic**.
    - If your goal is to automatically onboard every new AWS Account created in your environment, you should go with the *Automatic* mode.
    - But if you're interested in manually selecting AWS Account to onboard, you should use the *Interactive* mode.
- **Automatic**
  - In automatic mode you should specify the parameter **target-accounts** with `ALL`, `MEMBERS` or `MASTER`. Given the choice, Zanshin CLI will list all AWS Accounts in your AWS Organization, and compare this with all AWS Scan Targets in your Zanshin Organization.
  - If Zanshin CLI identify an AWS Account that's already onboarded on Zanshin, this account will be ignored.
  - For the accounts selected to onboard, the Zanshin CLI will try to perform an `AssumeRole` using the role you informed via **aws-role-name** parameter on the target account.
  - Then Zanshin CLI will deploy a CloudFormation template that contains what's necessary for the Zanshin Engine perform Scans on your AWS Account.
  - Repeat until no more new AWS Accounts are found.
- **Interactive**
  - If you don't specify the parameter **target-accounts**, Zanshin CLI will ask you which of all AWS Accounts in your AWS Organization you want to onboard.
  - Zanshin CLI won't ask you about AWS Accounts that are already onboarded on your Zanshin Organization.



**Usage**

If you have [AWS Control Tower](https://aws.amazon.com/controltower) enabled in your AWS Organization, you can use the `AWSControlTowerExecution` role as follows:

```shell
$ zanshin organization scan_target onboard_aws_organization us-east-1 bd0e0c7c-example-uuid-b4ec-e9210fba4b37 --target-accounts MEMBERS --aws-role-name AWSControlTowerExecution
```

---

If you want to onboard all accounts except those named *main-account* and *dev-sandbox*, you can specify then using *--exclude-account* parameter:

```shell
$ zanshin organization scan_target onboard_aws_organization us-east-1 bd0e0c7c-example-uuid-b4ec-e9210fba4b37 --target-accounts ALL --aws-role-name AWSControlTowerExecution --exclude-account dev-sandbox --exclude-account main-account
```
> :information_source: You can exclude accounts by Arn, Id, E-mail and Name
---

If you want to interactively choose which AWS Account to onboard, just omit the *--target-accounts* parameter:

```shell
$ zanshin organization scan_target onboard_aws_organization us-east-1 bd0e0c7c-example-uuid-b4ec
```
> :warning: If you don't specify a role, Zanshin CLI will use OrganizationAccountAccessRole

---

#### Minimum required AWS IAM Privileges on AWS Management Account

The minimum required privileges that you need in your AWS Management Account to be able to orchestrate the deployment in your AWS Member accounts are this:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ListOrganizationAccounts",
            "Effect": "Allow",
            "Action": [
                "organizations:ListAccounts",
                "organizations:DescribeOrganization"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AssumeRoleAccounts",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": [
                "arn:aws:iam::*:role/(your role name)"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:PrincipalOrgID":[
                        "o-xxxxxxxxxx"
                    ]
                }
            }
        }
    ]
}
```

> **Attention**
> :warning: Make sure to substitute the following placeholders:
> - `your role name` to the correct name of the role you'll access in the member accounts.
> - `o-xxxxxxxxxx` to the ID of your AWS Organization.

If you're looking for the required privileges in the AWS Member accounts to actually deploy the CloudFormation, refer to [this documentation](https://github.com/tenchi-security/zanshin-sdk-python/blob/main/zanshinsdk/docs/README.md).
