"""
Unit tests for minio_handler module.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock
from minio.error import ResponseError, BucketAlreadyExists, BucketAlreadyOwnedByYou
from galaxiumtools.minio_handler import MinioHandler


class TestMinioHandler(unittest.TestCase):
    """
    Test cases for MinioHandler class.
    """

    def setUp(self):
        self.mock_client = MagicMock()
        self.minio_handler = MinioHandler(
            endpoint="minio.example.com:9000",
            access_key="your-access-key",
            secret_key="your-secret-key",
        )
        self.minio_handler.client = self.mock_client

    def test_create_bucket(self):
        self.mock_client.make_bucket.side_effect = [
            BucketAlreadyOwnedByYou(),
            BucketAlreadyExists(),
            ResponseError(),
        ]
        self.minio_handler.create_bucket("test-bucket")
        self.assertEqual(self.mock_client.make_bucket.call_count, 3)

    def test_remove_bucket(self):
        self.mock_client.remove_bucket.side_effect = ResponseError()
        with self.assertRaises(Exception):
            self.minio_handler.remove_bucket("test-bucket")

    def test_upload_folder(self):
        # Create a temporary directory with files for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some subdirectories and files inside the temporary directory
            os.makedirs(os.path.join(temp_dir, 'subdir1'))
            os.makedirs(os.path.join(temp_dir, 'subdir2'))
            open(os.path.join(temp_dir, 'file1.txt'), 'a').close()
            open(os.path.join(temp_dir, 'subdir1', 'file2.txt'), 'a').close()
            open(os.path.join(temp_dir, 'subdir2', 'file3.txt'), 'a').close()

            # Patch the upload_object method to track calls
            with patch.object(self.minio_handler, 'upload_object') as mock_upload_object:
                # Upload the temporary directory to Minio
                self.minio_handler.upload_folder('test-bucket', temp_dir, object_prefix='test_prefix')

                # Assert that the upload_object method was called for each file
                mock_upload_object.assert_any_call('test-bucket', 'test_prefix/file1.txt', os.path.join(temp_dir, 'file1.txt'))
                mock_upload_object.assert_any_call('test-bucket', 'test_prefix/subdir1/file2.txt', os.path.join(temp_dir, 'subdir1', 'file2.txt'))
                mock_upload_object.assert_any_call('test-bucket', 'test_prefix/subdir2/file3.txt', os.path.join(temp_dir, 'subdir2', 'file3.txt'))



if __name__ == "__main__":
    unittest.main()
