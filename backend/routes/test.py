from fastapi import APIRouter
import logging
from src.settings import LoggerSettings

logger = logging.getLogger(LoggerSettings().logger_name)

router = APIRouter()


@router.get("/api/test")
async def test():
    """Test API"""
    logger.info("Test API")
    return {"message": "Hello World!"}
