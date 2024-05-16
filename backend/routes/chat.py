from backend.dependencies.core import DBSessionDep as db_session
from backend.crud.chat import create_chat, get_chat_by_chatid, update_chat_by_chatid
from fastapi import APIRouter, status, Request
from backend.schemas.input import UserInputCreate, UserInputShow, PredictionInputShow
import uuid
from src.dummy_code import dummy_prediction
import logging
from src.settings import LoggerSettings

logger = logging.getLogger(LoggerSettings().logger_name)

router = APIRouter()


@router.post("/chat", response_model=UserInputShow, status_code=status.HTTP_201_CREATED)
async def create_chat_api(request: Request, user_chat: UserInputCreate, db: db_session):
    if not user_chat.session_id:
        user_chat.session_id = uuid.uuid4()

    updated_record = user_chat.dict()
    updated_record["chat_id"] = uuid.uuid4()

    logger.info(f"Record with chat id : {updated_record}")

    return await create_chat(db, updated_record)


@router.put("/chat", response_model=PredictionInputShow, status_code=status.HTTP_200_OK)
async def update_chat_api(request: Request, user_chat: UserInputShow, db: db_session):

    chat_record = user_chat.dict()
    prediction = dummy_prediction(user_chat.user_query)
    chat_record["prediction_label"] = prediction["prediction_label"]
    chat_record["prediction_probability"] = prediction["prediction_probability"]
    chat_record["status"] = "completed"

    logger.info(f"Updated record: {chat_record}")

    return await update_chat_by_chatid(db, chat_record)


@router.get(
    "/chat/{chat_id}",
    response_model=PredictionInputShow,
    status_code=status.HTTP_200_OK,
)
async def get_chat_by_chatid_api(chat_id: uuid.UUID, db: db_session):
    return await get_chat_by_chatid(db, chat_id)
