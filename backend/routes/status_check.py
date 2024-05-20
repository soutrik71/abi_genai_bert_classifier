"""
This module defines a status check endpoint for the API.
The endpoint provides a simple health check to verify that the API is running.

Components:
- APIRouter: Router for defining API endpoints.
- ErrorResponse: Schema for error responses.
- LoggerSettings: Settings for configuring the logger.
"""

# Import necessary modules and components
from fastapi import APIRouter, status
from backend.schemas.input import ErrorResponse
import logging
from src.settings import LoggerSettings

# Setup logger
logger = logging.getLogger(LoggerSettings().logger_name)

# Initialize router
router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def status():
    """
    Status check endpoint for the API.
    This endpoint returns a simple status message to indicate that the API is running.
    """
    logger.info("Status check")
    return {"status": "ok"}
