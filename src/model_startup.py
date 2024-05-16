from src.settings import (
    env_settings,
    AzureblobSettings,
    LoggerSettings,
)
import logging
from src.utils.azure_connector import AzureBlobConnection
import os
from src.inference import ModelInference

logger = logging.getLogger(LoggerSettings().logger_name)


def model_startup(
    env_settings=env_settings,
    AzureblobSettings=AzureblobSettings,
    ModelInference=ModelInference,
):
    logger.info("Downloading model from Azure Blob Storage")
    az_connection = AzureBlobConnection(
        storage_account=env_settings.STORAGE_ACCOUNT,
        client_id=env_settings.CLIENT_ID,
        tenant_id=env_settings.TENANT_ID,
        client_secret=env_settings.SECRET_ID,
    )

    az_connection.azblob_download(
        container_name=env_settings.CONTAINER_NAME,
        root_path=os.getcwd(),
        local_output_path=AzureblobSettings().input_path,
        blob_path=AzureblobSettings().blob_path,
        file_names=[],
    )
    logger.info("Initializing model inference")
    infer_model = ModelInference()

    return infer_model
