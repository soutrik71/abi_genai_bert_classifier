from fastapi import APIRouter, status

from backend.schema import ErrorResponse

import logging
from src.settings import LoggerSettings

logger = logging.getLogger(LoggerSettings().logger_name)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def status():
    """Status check for the API"""
    logger.info("Status check")
    return {"status": "ok"}
