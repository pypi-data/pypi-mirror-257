import unittest
from unittest.mock import patch

from vecflowapi.Client import Client
from tests.Helpers import mock_response


class TestAPIKeyOperations(unittest.TestCase):
    @patch("requests.get")
    def test_generate_api_key_success(self, mock_get):
        mock_get.return_value = mock_response(json_data={"api_key": "new_api_key"})
        client = Client()
        api_key = client.generate_api_key("user", "pass")
        self.assertEqual(api_key, "new_api_key")

    @patch("requests.get")
    def test_list_api_keys_success(self, mock_get):
        mock_get.return_value = mock_response(
            json_data={"api_keys": ["api_key_1", "api_key_2"]}
        )
        client = Client()
        api_keys = client.list_api_keys("user", "pass")
        self.assertEqual(api_keys, ["api_key_1", "api_key_2"])

if __name__ == '__main__':
    unittest.main()

