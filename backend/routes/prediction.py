from fastapi import APIRouter, status, Request
from backend.dependencies.core import DBSessionDep as db_session
from backend.crud.chat import (
    create_chat,
    update_chat_by_chatid,
)
import uuid
from backend.schemas.input import UserInputCreate, PredictionInputShow, ErrorResponse
import logging
from src.settings import LoggerSettings

logger = logging.getLogger(LoggerSettings().logger_name)


router = APIRouter(tags=["prediction"])


@router.post(
    "/api/predict",
    response_model=PredictionInputShow,
    status_code=status.HTTP_200_OK,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def do_predict(request: Request, user_chat: UserInputCreate, db: db_session):
    """
    Perform prediction on input data using the model loaded in the app state
    """
    logger.info(f"Received user query: {user_chat}")

    # adding chatid to the user query
    if not user_chat.session_id:
        user_chat.session_id = uuid.uuid4()

    updated_record = user_chat.dict()
    updated_record["chat_id"] = uuid.uuid4()

    # create a new record in the database
    logger.info(f"Creating new chat record: {updated_record}")
    await create_chat(db, updated_record)

    # extract model from app state
    model = request.app.state.model
    # Perform prediction on input data
    logger.info("Performing prediction on user query")
    results = model.predict(user_chat.user_query)
    logger.info(f"Publishing results: {results}")

    # update the record in the database
    updated_record["prediction_label"] = results["prediction_label"]
    updated_record["prediction_probability"] = results["prediction_probability"]
    updated_record["status"] = "completed"

    logger.info(f"Updated record in DB: {updated_record}")

    await update_chat_by_chatid(db, updated_record)

    return PredictionInputShow(**updated_record)
