import unittest
from unittest.mock import patch

from vecflowapi.Client import Client
from vecflowapi.Pipeline import Pipeline
from tests.Helpers import mock_response


class TestClientOperations(unittest.TestCase):
    @patch("requests.post")
    def test_create_pipeline_success(self, mock_post):
        mock_post.return_value = mock_response()
        client = Client(api_key="dummy_api_key")
        pipeline = client.create_pipeline("test_pipeline")
        self.assertIsInstance(pipeline, Pipeline)
        self.assertEqual(pipeline.name, "test_pipeline")

    def test_get_pipeline_success(self):
        client = Client(api_key="dummy_api_key")
        pipeline = client.get_pipeline("existing_pipeline")
        self.assertIsInstance(pipeline, Pipeline)
        self.assertEqual(pipeline.name, "existing_pipeline")

    def test_get_pipeline_with_api_key(self):
        # Setup
        client = Client(api_key="dummy_api_key")
        pipeline_name = "test_pipeline"

        # Exercise
        pipeline = client.get_pipeline(pipeline_name)

        # Verify
        self.assertIsInstance(pipeline, Pipeline)
        self.assertEqual(pipeline.name, pipeline_name)

    # Common error scenario: API key not provided
    def test_create_pipeline_no_api_key_error(self):
        client = Client()  # No API key provided
        with self.assertRaises(PermissionError):
            client.create_pipeline("test_pipeline")

if __name__ == '__main__':
    unittest.main()

