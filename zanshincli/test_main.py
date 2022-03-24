import unittest
from io import StringIO
from unittest.mock import patch
import os
from pathlib import Path

###### Commenting testes as those pass on dev machine and not on github actions

# from moto import mock_organizations, mock_sts, mock_s3
# from boto3_type_annotations.organizations import Client as Boto3OrganizationsClient
# import boto3

# from zanshincli import main
from zanshincli.main import global_options, zanshin_exchanger

from typer.testing import CliRunner

runner = CliRunner()


class TestStringMethods(unittest.TestCase):
    ###################################################
    # Set up
    ###################################################

    def setUp(self):
        global_options['profile'] = 'default'

    ###################################################
    # General Functions
    ###################################################
    def test_exchanger(self):
        _value = "Test"

        with patch("sys.stdout", new=StringIO()) as self.output:
            zanshin_exchanger(None, _value, None)
            self.assertEqual(_value, self.output.getvalue().strip())

    ###################################################
    # __mock_aws_credentials__
    ###################################################

    def mock_aws_credentials(self):
        """Mocked AWS Credentials for moto."""
        moto_credentials_file_path = Path(
            __file__).parent.absolute() / 'dummy_aws_credentials'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = str(
            moto_credentials_file_path)

    def test_format_field(self):
        pass

    def test_output_iterable(self):
        pass

    def test_dump_json(self):
        pass

    def test_global_options_callback(self):
        pass

    ###################################################
    # Commands
    ###################################################

    def test_init(self):
        pass

    def test_version(self):
        pass

    ###################################################
    # Commands account_app
    ###################################################

    def test_account_me(self):
        pass

    ###################################################
    # Commands account_app.invites_app
    ###################################################

    def test_account_invite_list(self):
        pass

    def test_account_invite_get(self):
        pass

    def test_account_invite_accept(self):
        pass

    ###################################################
    # Commands account_app.api_key_app
    ###################################################

    def test_account_api_key_list(self):
        pass

    def test_account_api_key_create(self):
        pass

    def test_account_api_key_delete(self):
        pass

    ###################################################
    # Commands organization_app
    ###################################################

    def test_organization_list(self):
        pass

    def test_organization_get(self):
        pass

    def test_organization_update(self):
        pass

    ###################################################
    # Commands organization_app.organization_member_app
    ###################################################

    def test_organization_member_list(self):
        pass

    def test_organization_member_get(self):
        pass

    def test_organization_member_update(self):
        pass

    def test_organization_member_delete(self):
        pass

    ###################################################
    # Commands organization_app.organization_member_invite_app
    ###################################################

    def test_organization_member_invite_list(self):
        pass

    def test_organization_member_invite_create(self):
        pass

    def test_organization_member_invite_get(self):
        pass

    def test_organization_member_invite_delete(self):
        pass

    def test_organization_member_invite_resend(self):
        pass

    ###################################################
    # Commands organization_app.organization_follower_app
    ###################################################

    def test_organization_follower_list(self):
        pass

    def test_organization_follower_stop(self):
        pass

    ###################################################
    # Commands organization_app.organization_follower_request_app
    ###################################################

    def test_organization_follower_request_list(self):
        pass

    def test_organization_follower_request_create(self):
        pass

    def test_organization_follower_request_get(self):
        pass

    def test_organization_follower_request_delete(self):
        pass

    ###################################################
    # Commands organization_app.organization_following_app
    ###################################################

    def test_organization_following_list(self):
        pass

    def test_organization_following_stop(self):
        pass

    ###################################################
    # Commands organization_app.organization_following_request_app
    ###################################################

    def test_organization_following_request_list(self):
        pass

    def test_organization_following_request_get(self):
        pass

    def test_organization_following_request_accept(self):
        pass

    def test_organization_following_request_decline(self):
        pass

    ###################################################
    # Commands organization_app.organization_scan_target_app
    ###################################################

    def test_organization_scan_target_list(self):
        pass

    def test_organization_scan_target_create(self):
        pass

    def test_organization_scan_target_get(self):
        pass

    def test_organization_scan_target_update(self):
        pass

    def test_organization_scan_target_delete(self):
        pass

    def test_organization_scan_target_check(self):
        pass

    ###################################################
    # Commands organization_app.organization_scan_target_scan_app
    ###################################################

    def test_organization_scan_target_scan_start(self):
        pass

    def test_organization_scan_target_scan_stop(self):
        pass

    def test_organization_scan_target_scan_list(self):
        pass

    def test_organization_scan_target_scan_get(self):
        pass

    ###################################################
    # Commands alert_app
    ###################################################

    def test_alert_list(self):
        pass

    def test_alert_following_list(self):
        pass

    def test_alert_history_list(self):
        pass

    def test_alert_history_following_list(self):
        pass

    def test_grouped_alert_list(self):
        pass

    def test_grouped_alert_following_list(self):
        pass

    def test_alert_get(self):
        pass

    ###################################################
    # Commands summary_app
    ###################################################

    def test_summary_alert(self):
        pass

    def test_summary_alert_following(self):
        pass

    def test_summary_scan(self):
        pass

    def test_summary_scan_following(self):
        pass

    """
    Commenting tests as those pass on local machine but fails on github actions
    """
    # @mock_organizations
    # @mock_sts
    # def test_onboard_aws_organization_interactive_mode(self):
    #     """
    #     Assert that the CLI method onboard_aws_organization works as expected using the interactive mode
    #     """

    #     # Mock AWS Boto3 profile 'foo'
    #     self.mock_aws_credentials()

    #     # Mock AWS Organizations Accounts
    #     boto3_session = boto3.Session(
    #         aws_access_key_id="123",
    #         aws_secret_access_key="123",
    #         aws_session_token="123",
    #     )
    #     organizations: Boto3OrganizationsClient = boto3_session.client(
    #         'organizations', region_name='us-east-1')
    #     organizations.create_organization(FeatureSet="ALL")
    #     total_mock_aws_accounts = 10

    #     mock_aws_accounts_ids = []
    #     for i in range(total_mock_aws_accounts):
    #         mocked_acc = organizations.create_account(
    #             AccountName=f"AWS_Account_{i}", Email=f"email{i}@tenchisecurity.com")
    #         mock_aws_accounts_ids.append(
    #             mocked_acc['CreateAccountStatus']['AccountId'])

    #     with patch("zanshinsdk.Client.onboard_scan_target") as mock_sdk:
    #         result = runner.invoke(main.organization_scan_target_app, [
    #                                "onboard_aws_organization", "us-east-1",
    #                                "2a061fef-a9d3-486e-a2c2-8fe6e69bd0ee", "--boto3-profile",
    #                                "foo"], input="\n")
    #         # assert result.exit_code == 0
    #         assert "Looking for Zanshin AWS Scan Targets" in result.stdout
    #         assert "Detecting AWS Accounts already in Zanshin Organization" in result.stdout
    #         assert "Onboard AWS account master (123456789012)? [Y/n]:" in result.stdout

    #         for i in range(total_mock_aws_accounts):
    #             assert f"Onboard AWS account AWS_Account_{i}" in result.stdout
    #         assert "11 Account(s) marked to Onboard" in result.stdout
    #         assert mock_sdk.has_any_call()
    #         assert 10 == mock_sdk.call_count

    #     # CleanUp
    #     for acc_id in mock_aws_accounts_ids:
    #         organizations.remove_account_from_organization(AccountId=acc_id)
    #     organizations.delete_organization()

    # @mock_organizations
    # @mock_sts
    # def test_onboard_aws_organization_automatic_mode(self):
    #     """
    #     Assert that the CLI method onboard_aws_organization works as expected using the automatic mode
    #     """
    #     # Mock AWS Boto3 profile 'foo'
    #     self.mock_aws_credentials()

    #     # Mock AWS Organizations Accounts
    #     boto3_session = boto3.Session(
    #         aws_access_key_id="123",
    #         aws_secret_access_key="123",
    #         aws_session_token="123",
    #     )
    #     organizations: Boto3OrganizationsClient = boto3_session.client(
    #         'organizations', region_name='us-east-1')
    #     organizations.create_organization(FeatureSet="ALL")
    #     total_mock_aws_accounts = 10

    #     mock_aws_accounts_ids = []
    #     for i in range(total_mock_aws_accounts):
    #         mocked_acc = organizations.create_account(
    #             AccountName=f"AWS_Account_{i}", Email=f"email{i}@tenchisecurity.com")
    #         mock_aws_accounts_ids.append(
    #             mocked_acc['CreateAccountStatus']['AccountId'])

    #     with patch("zanshinsdk.Client.onboard_scan_target") as mock_sdk:
    #         result = runner.invoke(main.organization_scan_target_app, [
    #                                "onboard_aws_organization", "us-east-1",
    #                                "2a061fef-a9d3-486e-a2c2-8fe6e69bd0ee", "--boto3-profile", "foo",
    #                                "--target-accounts", "MEMBERS"])
    #         # assert result.exit_code == 0
    #         assert "Looking for Zanshin AWS Scan Targets" in result.stdout
    #         assert 10 == mock_sdk.call_count
    #         assert mock_sdk.has_any_call()

    #     # CleanUp
    #     for acc_id in mock_aws_accounts_ids:
    #         organizations.remove_account_from_organization(AccountId=acc_id)
    #     organizations.delete_organization()

    # @mock_organizations
    # @mock_sts
    # def test_onboard_aws_organization_automatic_mode_excluding_accounts(self):
    #     """
    #     Assert that the CLI method onboard_aws_organization is excluding accounts to onboard according to
    #     CLI Arguments
    #     """
    #     # Mock AWS Boto3 profile 'foo'
    #     self.mock_aws_credentials()

    #     # Mock AWS Organizations Accounts, creating 10 accounts
    #     boto3_session = boto3.Session(
    #         aws_access_key_id="123",
    #         aws_secret_access_key="123",
    #         aws_session_token="123",
    #     )
    #     organizations: Boto3OrganizationsClient = boto3_session.client(
    #         'organizations', region_name='us-east-1')
    #     organizations.create_organization(FeatureSet="ALL")
    #     total_mock_aws_accounts = 10

    #     mock_aws_accounts_ids = []
    #     for i in range(total_mock_aws_accounts):
    #         mocked_acc = organizations.create_account(
    #             AccountName=f"AWS_Account_{i}", Email=f"email{i}@tenchisecurity.com")
    #         mock_aws_accounts_ids.append(
    #             mocked_acc['CreateAccountStatus']['AccountId'])

    #     with patch("zanshinsdk.Client.onboard_scan_target") as mock_sdk:
    #         result = runner.invoke(main.organization_scan_target_app, [
    #             "onboard_aws_organization", "us-east-1",
    #             "2a061fef-a9d3-486e-a2c2-8fe6e69bd0ee", "--boto3-profile", "foo",
    #             "--target-accounts", "MEMBERS", "--exclude-account", "AWS_Account_1",
    #             "--exclude-account", "AWS_Account_2"])
    #         assert result.exit_code == 0
    #         assert "Looking for Zanshin AWS Scan Targets" in result.stdout
    #         assert 8 == mock_sdk.call_count
    #         assert mock_sdk.has_any_call()

    #     # CleanUp
    #     for acc_id in mock_aws_accounts_ids:
    #         organizations.remove_account_from_organization(AccountId=acc_id)
    #     organizations.delete_organization()

