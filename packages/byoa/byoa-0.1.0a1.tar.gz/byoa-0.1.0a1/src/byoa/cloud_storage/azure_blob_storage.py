"""Azure blob storage helper functions"""

import os
from typing import Optional, Tuple

from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient


def _validate_access_info(
    account_name: Optional[str], blob_container_name: Optional[str], sas_credential: Optional[str]
) -> bool:
    """Validates the retrieved access info"""

    return all([account_name, blob_container_name, sas_credential])


def _get_access_info() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Retreives access information from the environment variables"""

    account_name = os.getenv("AZURE_ACCOUNT_NAME")
    blob_container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")
    sas_credential = os.getenv("AZURE_SAS_CREDENTIAL")

    return account_name, blob_container_name, sas_credential


def write_file_to_azure_blob_storage(
    local_file_path: str, blob_name: Optional[str] = None
) -> bool:
    """Upload file to Azure Blob Storage.

    Args:
      local_file_path(str): Path of the file to upload.
      blob_name(str, optional): Name of the blob to be uploaded, defaults to None

    Returns:
      bool: True or False depending on the success of the upload.
    """

    account_name, blob_container_name, sas_credential = _get_access_info()

    if _validate_access_info(account_name, blob_container_name, sas_credential):
        try:
            if blob_name is None:
                blob_name = os.path.basename(local_file_path)
            account_url = f"https://{account_name}.blob.core.windows.net"

            # Upload file
            blob_service_client = BlobServiceClient(
                account_url=account_url, credential=sas_credential
            )

            if blob_container_name is not None:
                blob_client = blob_service_client.get_blob_client(blob_container_name, blob_name)
                with open(local_file_path, "rb") as local_file:
                    blob_client.upload_blob(local_file)

                return True

            return False

        except AzureError as error:
            print(f"Error while uploading file to Azure: {error}")
            return False

    else:
        print("Please enter valid access information to Azure blob storage in .env file")
        return False


def upload_directory_to_azure_blob_storage(local_directory_path: str) -> bool:
    """Upload a directory and its contents to Azure Blob Storage.

    Args:
      local_directory_path(str): The local directory path to upload.

    Returns:
      bool: True or False depending on the success of the upload.
    """

    account_name, blob_container_name, sas_credential = _get_access_info()
    directory_name = os.path.basename(local_directory_path)
    if _validate_access_info(account_name, blob_container_name, sas_credential):
        try:
            for root, _, files in os.walk(local_directory_path):
                for file in files:
                    local_file_path = os.path.join(root, file)

                    relative_path = os.path.relpath(local_file_path, local_directory_path)
                    blob_name = os.path.join(directory_name, relative_path).replace(os.sep, "/")
                    write_file_to_azure_blob_storage(local_file_path, blob_name)

            return True

        except AzureError as error:
            print(f"Error while uploading directory to Azure Blob Storage: {error}")
            return False

    else:
        print("Please enter valid access information to Azure blob storage in .env file")
        return False


def get_azure_blob_url_path(local_path: str) -> str:
    """Get the azure blob path of the uploaded element (file or folder)

    Args:
      local_path(str): The local path of the uploaded folder/file

    Returns:
      str: The azure blob url of the uploaded folder/file
    """

    azure_blob_key = os.path.basename(local_path)
    account_name, blob_container_name, _ = _get_access_info()

    blob_url = (
        f"https://{account_name}.blob.core.windows.net/{blob_container_name}/{azure_blob_key}"
    )
    return blob_url
