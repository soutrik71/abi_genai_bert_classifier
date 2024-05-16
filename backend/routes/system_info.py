import os
import sys

import torch
import transformers
from fastapi import APIRouter
import logging
from src.settings import LoggerSettings

logger = logging.getLogger(LoggerSettings().logger_name)


router = APIRouter()


@router.get("/api/about")
async def show_about():
    """
    Get deployment information, for debugging
    """
    logger.info("About API")

    def bash(command):
        output = os.popen(command).read()
        return str(output)

    return {
        "sys.version": sys.version,
        "torch.__version__": torch.__version__,
        "transformers.__version__": transformers.__version__,
        "torch.cuda.is_available()": torch.cuda.is_available(),
        "torch.version.cuda": torch.version.cuda,
        "torch.backends.cudnn.version()": torch.backends.cudnn.version(),
        "torch.backends.cudnn.enabled": torch.backends.cudnn.enabled,
        "nvidia-smi": bash("nvidia-smi"),
    }
