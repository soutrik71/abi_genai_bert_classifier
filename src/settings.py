import logging
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
import warnings

warnings.filterwarnings("ignore")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("dev.env", "staging.env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )


env_settings = Settings(_env_file="dev.env", _env_file_encoding="utf-8", extra="allow")


class ModelSettings(BaseSettings):
    seed: int = 71
    model_path: str = "models"
    pretrained_model_name: str = "bert-base-uncased"
    learning_rate: float = 2e-05
    epochs: int = 20
    num_classes: int = 1
    drop_out: float = 0.3
    binary_thresh: float = 0.7


class DataSettings(BaseSettings):
    evaluation_size: float = 0.25
    class_names: list = ["SIMPLE", "COMPLEX"]
    data_path: str = "data/labeled_data"


class TokenizerSettings(BaseSettings):
    pretrained_model_name: str = "bert-base-uncased"
    max_length: int = 128
    batch_size: int = 16
    num_workers: int = 4


class AzureblobSettings(BaseSettings):
    blob_path: str = "classifier_model/"
    input_path: str = "models/"


class LoggerSettings(BaseSettings):
    logger_name: str = "custom_logger"
    log_level: int = logging.INFO
