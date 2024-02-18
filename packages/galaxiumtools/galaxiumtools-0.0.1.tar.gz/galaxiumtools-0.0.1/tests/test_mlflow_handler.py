"""
Unit tests for mlflow_handler module.
"""

import unittest
from unittest.mock import MagicMock
from minio_handler.mlflow_handler import MLFlowHandler


class TestMLFlowHandler(unittest.TestCase):
    """
    Test cases for MLFlowHandler class.
    """

    def setUp(self):
        self.mock_mlflow = MagicMock()
        self.mlflow_handler = MLFlowHandler(tracking_uri="http://mlflow.example.com")
        mlflow.set_tracking_uri = self.mock_mlflow

    def test_start_run(self):
        self.mlflow_handler.start_run(run_name="test-run")
        self.mock_mlflow.start_run.assert_called_once_with(run_name="test-run")

    # Add similar test cases for other methods


if __name__ == "__main__":
    unittest.main()
