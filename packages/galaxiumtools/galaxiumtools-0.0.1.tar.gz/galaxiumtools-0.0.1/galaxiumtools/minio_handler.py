"""
minio_handler module
A Python package to handle Minio interactions.
"""
import os
from tqdm import tqdm
from minio import Minio
from minio.error import ResponseError, BucketAlreadyExists, BucketAlreadyOwnedByYou


class MinioHandler:
    """
    MinioHandler class
    Provides methods to interact with Minio storage.
    """

    def __init__(self, endpoint, access_key, secret_key):
        """
        Initialize MinioHandler with endpoint, access_key, and secret_key.
        """
        self.client = Minio(
            endpoint, access_key=access_key, secret_key=secret_key, secure=False
        )

    def create_bucket(self, bucket_name):
        """
        Create a bucket in Minio storage.
        """
        try:
            self.client.make_bucket(bucket_name)
        except BucketAlreadyOwnedByYou:
            pass
        except BucketAlreadyExists:
            pass
        except ResponseError as err:
            raise Exception(f"Error creating bucket: {err}")

    def remove_bucket(self, bucket_name):
        """
        Remove a bucket from Minio storage.
        """
        try:
            self.client.remove_bucket(bucket_name)
        except ResponseError as err:
            raise Exception(f"Error removing bucket: {err}")

    def list_buckets(self):
        """
        List all buckets in Minio storage.
        """
        try:
            return self.client.list_buckets()
        except ResponseError as err:
            raise Exception(f"Error listing buckets: {err}")

    def upload_object(self, bucket_name, object_name, file_path):
        """
        Upload an object to a bucket in Minio storage.
        """
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
        except ResponseError as err:
            raise Exception(f"Error uploading object: {err}")

    def upload_folder(self, bucket_name, folder_path, object_prefix=""):
        """
        Upload a folder to a bucket in Minio storage.
        """
        for root, dirs, files in tqdm(os.walk(folder_path)):
            for file in files:
                file_path = os.path.join(root, file)
                object_name = os.path.join(
                    object_prefix, os.path.relpath(file_path, folder_path)
                )
                self.upload_object(bucket_name, object_name, file_path)

    def remove_object(self, bucket_name, object_name):
        """
        Remove an object from a bucket in Minio storage.
        """
        try:
            self.client.remove_object(bucket_name, object_name)
        except ResponseError as err:
            raise Exception(f"Error removing object: {err}")

    def list_objects(self, bucket_name):
        """
        List all objects in a bucket in Minio storage.
        """
        try:
            return self.client.list_objects(bucket_name)
        except ResponseError as err:
            raise Exception(f"Error listing objects: {err}")
