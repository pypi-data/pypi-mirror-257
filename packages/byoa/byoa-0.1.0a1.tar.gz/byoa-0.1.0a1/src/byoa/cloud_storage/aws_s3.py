"""AWS S3 helper functions"""

import os
from typing import Optional

import boto3
from boto3.exceptions import Boto3Error


def upload_file(local_file_path: str, bucket_name: Optional[str] = None) -> bool:
    """Upload a file to AWS S3 Bucket.

    Args:
      local_file_path(str): The local file path to upload.
      bucket_name(str, optional): The name of the AWS S3 bucket, defaults to None

    Returns:
      bool: True if upload was sucessful, False otherwise

    """

    # get bucket name
    if bucket_name is None:
        bucket_name = os.getenv("AWS_BUCKET_NAME")

    s3_client = boto3.client("s3")
    if s3_client and bucket_name is not None:
        try:
            file_name = os.path.basename(local_file_path)
            s3_client.upload_file(local_file_path, bucket_name, file_name)
            return True
        except Boto3Error as error:
            print(f"Error while uploading file to AWS S3: {error}")
            return False
    else:
        return False


def write_folder_to_aws_s3(local_folder_path: str, bucket_name: Optional[str] = None) -> bool:
    """Upload a folder to AWS S3 Bucket.

    Args:
      local_folder_path(str): The local folder path to upload
      bucket_name(str, optional): The name of the AWS S3 bucket, defaults to None

    Returns:
      bool: True if upload was sucessful, False otherwise
    """

    # get bucket name
    if bucket_name is None:
        bucket_name = os.getenv("AWS_BUCKET_NAME")  # careful, bucket name can still be None

    s3_client = boto3.client("s3")
    if s3_client:
        try:
            for root, _, files in os.walk(local_folder_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, local_folder_path)
                    s3_key = os.path.join(
                        os.path.basename(local_folder_path), relative_path
                    ).replace(os.sep, "/")

                    if bucket_name is not None:
                        s3_client.upload_file(local_file_path, bucket_name, s3_key)
            return True
        except Boto3Error as error:
            print(f"Error while uploading folder to AWS S3: {error}")
            return False
    else:
        return False


def get_s3_uri_path(local_path: str) -> str:
    """Get the s3 path of the uploaded element (file or folder)

    Args:
      local_path(str): The local path of the uploaded folder/file on s3

    Returns:
      str: the s3 uri of the uploaded folder/file
    """

    s3_key = os.path.basename(local_path)
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    s3_uri = f"s3://{bucket_name}/{s3_key}"

    return s3_uri
