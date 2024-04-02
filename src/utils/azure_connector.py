import logging
import os
import time
import warnings
from typing import Any, List

from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

warnings.filterwarnings("ignore")

# Contextlogger----
logger = logging.getLogger("torch_classifier")

SLEEP_TIME = 2


class AzureBlobConnection:
    """
    This class is used to connect to Azure Blob Storage and perform operations like download and upload

    Attributes:
        storage_account (str): The name of the Azure Blob Storage account.
        client_id (str): The client ID of the Azure Blob Storage account.
        tenant_id (str): The tenant ID of the Azure Blob Storage account.
        client_secret (str): The client secret of the Azure Blob Storage account.
        connect_str (str): The connection string of the Azure Blob Storage account.
        blob_service_client (BlobServiceClient): The client object for the Azure Blob Storage account.
    """

    def __init__(
        self,
        storage_account: str = None,
        client_id: str = None,
        tenant_id: str = None,
        client_secret: str = None,
        connect_str: str = None,
    ):
        self.storage_account = storage_account
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        self.connect_str = connect_str
        self.blob_service_client = self._create_blob_service_client()

    def _create_blob_service_client(self):
        if self.connect_str is not None:
            logger.info(
                "Establishing Connection  with Azure Blob Storage using connection string"
            )
            return BlobServiceClient.from_connection_string(self.connect_str)
        else:
            logger.info(
                "Establishing Connection  with Azure Blob Storage using credentials"
            )
            token_credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
            return BlobServiceClient(
                account_url=f"https://{self.storage_account}.blob.core.windows.net",
                credential=token_credential,
            )

    def _download_blob(self, blob_client, download_path):
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

    def _blob_temp_downloads(
        self,
        root_path: str,
        output_path: str,
        container_client: Any,
        file_name: str,
    ):
        os.makedirs(os.path.join(root_path, output_path), exist_ok=True)
        blob_client = container_client.get_blob_client(file_name)
        if blob_client.exists():
            logger.info("downloading the blob to local file")
            download_file_path = os.path.join(
                root_path, output_path, os.path.basename(file_name)
            )
            logger.info("Downloaded file at:{}".format(download_file_path))
            self._download_blob(blob_client, download_file_path)
            time.sleep(SLEEP_TIME)
            return True
        else:
            logger.error(
                f"{file_name} could not be downloaded as it does not exist in the blob."
            )
            return False

    def azblob_download(
        self,
        container_name: str,
        root_path: str,
        output_path: str,
        blob_prefix: str = None,
        file_names: List[str] = None,
    ):
        logger.info("Mode of Source selected is Azure Blob")
        try:
            container_client = self.blob_service_client.get_container_client(
                container_name
            )
            if not container_client.exists():
                raise ValueError("Source Container not found.")

            blob_list = container_client.list_blobs()
            file_list = [blob.name for blob in blob_list if blob_prefix in blob.name]
            if file_names:
                file_list = [
                    file for file in file_list if os.path.basename(file) in file_names
                ]

            for file_name in file_list:
                self._blob_temp_downloads(
                    root_path, output_path, container_client, file_name
                )

            logger.info(
                f"All Blobs download process successful, Total count :::{len(file_list)}"
            )
        except Exception as ex:
            logger.exception(f"Process Stopped due to an exception {ex}")

    def _temp_blob_upload(
        self,
        root_path: str,
        input_path: str,
        blob_prefix: str,
        local_file_name: str,
        container_name: str,
    ):
        upload_file_path = os.path.join(root_path, input_path, local_file_name)
        blob_name = (
            os.path.join(blob_prefix, local_file_name)
            if blob_prefix
            else local_file_name
        )
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, blob_type="BlockBlob")

    def azblob_upload(
        self,
        container_name: str,
        root_path: str,
        input_path: str,
        file_names: List[str],
        blob_prefix: str = None,
    ):
        logger.info("Mode of Source selected is Azure Blob for files upload")
        try:
            container_client = self.blob_service_client.get_container_client(
                container_name
            )
            if not container_client.exists():
                raise ValueError("Source Container not found.")

            if len(file_names) == 0:
                logger.info("No files specified explicitely, so taking all files ")
                file_names = os.listdir(os.path.join(root_path, input_path))

            for local_file_name in file_names:
                self._temp_blob_upload(
                    root_path, input_path, blob_prefix, local_file_name, container_name
                )
                time.sleep(SLEEP_TIME)
                logger.info(
                    f"Have successfully pushed file {local_file_name} in blob {blob_prefix} "
                    f"in container {container_name}"
                )
        except Exception as ex:
            logger.exception(f"Process Stopped due to an exception {ex}")
            raise ValueError(f"Process Stopped due to an exception {ex}")
