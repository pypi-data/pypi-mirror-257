import sys
from unittest import TestCase
from unittest.mock import patch

from dhapi.router.arg_parser import ArgParser


class TestArgParser(TestCase):
    @patch("dhapi.router.arg_parser.get_credentials", return_value={"username": "test_user", "password": "test_pw"})
    @patch.object(sys, 'argv', ["dhapi", "buy_lotto645", "-e", "receiver_email@email.com"])
    def test_given_email_flag_is_set_and_api_credentials_not_set_when_arg_parser_init_then_raise_runtime_error(self, get_credentials_mock):
        self.assertRaises(RuntimeError, ArgParser)

    @patch("dhapi.router.arg_parser.get_credentials", return_value={"username": "test_user", "password": "test_pw"})
    @patch.object(sys, 'argv', ["dhapi", "buy_lotto645"])
    def test_given_email_flag_not_set_when_arg_parser_email_method_used_then_no_error(self, get_credentials_mock):
        sut = ArgParser()

        self.assertDictEqual(sut.email_source(), {
            "recipient_email": None,
            "sender_email": None,
            "api_key": None,
            "api_secret": None,
        })

    @patch("dhapi.router.arg_parser.get_credentials", return_value={"mailjet_api_key": "test_key", "mailjet_api_secret": "test_secret", "mailjet_sender_email": "test_email@email.com"})
    @patch.object(sys, 'argv', ["dhapi", "buy_lotto645", "-e", "receiver_email@email.com"])
    def test_given_email_flag_is_set_and_api_credentials_set_when_arg_parser_init_then_raise_runtime_error(self, get_credentials_mock):
        ArgParser()
        # no error means success
