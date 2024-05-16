from fastapi import APIRouter, status, Request

from backend.schemas.input import UserInput, InferenceResponse, ErrorResponse
import logging
from src.settings import LoggerSettings

logger = logging.getLogger(LoggerSettings().logger_name)


router = APIRouter()


@router.post(
    "/api/predict",
    response_model=InferenceResponse,
    status_code=status.HTTP_200_OK,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def do_predict(request: Request, user_query: UserInput):
    """
    Perform prediction on input data using the model loaded in the app state
    """
    logger.info(f"Received user query: {user_query.user_query}")
    # extract model from app state
    model = request.app.state.model
    # Perform prediction on input data
    logger.info("Performing prediction on user query")
    results = model.predict(user_query.user_query)
    logger.info("Publishing results")
    results = {"error": False, "results": results}
    return InferenceResponse(**results)
