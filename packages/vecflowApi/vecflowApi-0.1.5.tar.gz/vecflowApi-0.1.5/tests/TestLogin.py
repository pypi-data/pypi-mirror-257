import unittest
from unittest.mock import patch

from vecflowapi.Client import Client
from tests.Helpers import mock_response


class TestLogin(unittest.TestCase):
    TEST_USERNAME = "test_user"
    TEST_PASSWORD = "test_password"
    INCORRECT_PASSWORD = "incorrect_password"

    @patch("requests.post")
    def test_login_success(self, mock_post):
        mock_post.return_value = mock_response(json_data={"token": "dummy_token"})
        client = Client()
        token = client._login(self.TEST_USERNAME, self.TEST_PASSWORD)
        self.assertEqual(token, "dummy_token")

    @patch("requests.post")
    def test_login_failure(self, mock_post):
        mock_post.return_value = mock_response(status_code=401)
        client = Client()
        token = client._login(self.TEST_USERNAME, self.INCORRECT_PASSWORD)
        self.assertIsNone(token)

if __name__ == '__main__':
    unittest.main()
