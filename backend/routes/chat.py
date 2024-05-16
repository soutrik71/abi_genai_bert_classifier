from backend.dependencies.core import DBSessionDep
from backend.crud.chat import create_chat, get_chat_by_chat_id
from backend.models.db_model import ChatRecord
from fastapi import APIRouter, status, Request
from backend.schemas.input import UserInput, UserInputShow
import uuid

router = APIRouter()

UserInputShow


@router.post("/chat", response_model=UserInputShow, status_code=status.HTTP_201_CREATED)
async def create_chat(request: Request, chat: UserInput, db: DBSessionDep):
    if not chat.session_id:
        chat.session_id = uuid.uuid4()
    # prepare the orm table record
    new_chat = ChatRecord(**chat.dict())
    return await create_chat(db, new_chat)


@router.get(
    "/chat/{chat_id}", response_model=UserInputShow, status_code=status.HTTP_200_OK
)
async def get_chat(chat_id: uuid.UUID, db: DBSessionDep):
    return await get_chat_by_chat_id(db, chat_id)
