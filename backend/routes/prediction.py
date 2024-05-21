"""
This module contains the FastAPI route for performing prediction on user input data.
The route receives a user query and performs prediction using the model loaded in the app state.
The prediction results are stored in the cache and the database.
The route returns the prediction results to the user.
"""

from fastapi import APIRouter, status, Request, HTTPException, Depends
from backend.dependencies.core import DBSessionDep as db_session
from backend.crud.chat import create_chat, update_chat_by_chatid
import uuid
from backend.schemas.input import UserInputCreate, PredictionInputShow, ErrorResponse
import logging
from src.settings import LoggerSettings
from backend.dependencies.auth import security, verification
from typing import Annotated

logger = logging.getLogger(LoggerSettings().logger_name)

router = APIRouter(tags=["prediction"])


@router.post(
    "/api/predict",
    response_model=PredictionInputShow,
    status_code=status.HTTP_200_OK,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def do_predict(
    request: Request,
    user_chat: UserInputCreate,
    db: db_session,
    Verification: Annotated[bool, Depends(verification)],
):
    """
    Perform prediction on the user input data and store the results in the cache and database.

    Args:
    - request (Request): The incoming request object.
    - user_chat (UserInputCreate): The user input data for prediction.
    - db (db_session): The database session.

    Returns:
    - PredictionInputShow: The prediction results.
    """
    if not Verification:
        raise HTTPException(status_code=401, detail="Unauthorized")

    logger.info(f"Received user query: {user_chat}")

    if not user_chat.session_id:
        user_chat.session_id = uuid.uuid4()

    cache = request.app.state.cache

    # Check if the result is already in the cache
    result = cache.get(user_chat.user_query)
    if result is not None:
        logger.info(f"Cache hit for query: {user_chat.user_query}")
        return PredictionInputShow(**result)

    logger.info(f"Cache miss for query: {user_chat.user_query}. Performing prediction.")

    updated_record = user_chat.dict()
    updated_record["chat_id"] = uuid.uuid4()

    # Create a new record in the database
    await create_chat(db, updated_record)

    # Extract model from app state and perform prediction
    model = request.app.state.model
    prediction_result = model.predict(user_chat.user_query)
    logger.info(f"Prediction result: {prediction_result}")

    # Update the record with prediction results
    updated_record.update(
        {
            "prediction_label": prediction_result["prediction_label"],
            "prediction_probability": prediction_result["prediction_probability"],
            "status": "completed",
        }
    )

    await update_chat_by_chatid(db, updated_record)

    # Store the result in the cache
    cache[user_chat.user_query] = updated_record

    return PredictionInputShow(**updated_record)
