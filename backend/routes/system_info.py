"""
This module defines an endpoint to provide deployment information for debugging purposes.
The endpoint returns various system and library versions, as well as GPU-related information.

Components:
- APIRouter: Router for defining API endpoints.
- LoggerSettings: Settings for configuring the logger.
"""

# Import necessary standard library modules
import os
import sys

# Import necessary third-party libraries
import torch
import transformers
from fastapi import APIRouter
import logging

# Import local settings for logging
from src.settings import LoggerSettings

# Setup logger
logger = logging.getLogger(LoggerSettings().logger_name)

# Initialize router
router = APIRouter(tags=["system_info"])


@router.get("/api/about")
async def show_about():
    """
    Get deployment information, for debugging.
    This endpoint returns various system and library versions, as well as GPU-related information.
    """
    logger.info("About API called")

    def bash(command):
        """
        Execute a bash command and return its output.
        """
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
