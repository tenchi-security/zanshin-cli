import unittest, json
from io import StringIO
from unittest.mock import patch

from zanshincli.main import global_options, zanshin_exchanger, format_field, output_iterable, dump_json, global_options_callback


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
