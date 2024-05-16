import uuid
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db_models.models import ChatRecord
from pydantic import BaseModel

import logging
from src.settings import LoggerSettings

logger = logging.getLogger(LoggerSettings().logger_name)


async def create_chat(db_session: AsyncSession, chat_dict: dict):
    chat_record = ChatRecord(**chat_dict)
    db_session.add(chat_record)
    await db_session.commit()
    await db_session.refresh(chat_record)
    return chat_record


async def update_chat_by_chatid(db_session: AsyncSession, chat_dict: dict):

    logger.info(f"Input Chat Record: {chat_dict}")

    result = await db_session.execute(
        select(ChatRecord).filter(ChatRecord.chat_id == chat_dict["chat_id"])
    )
    chat = result.scalars().first()

    logger.info(f"DB Extracted Chat Record: {chat}")

    if not chat:
        raise HTTPException(status_code=404, detail="Chat record not found")

    for key, value in chat_dict.items():
        setattr(chat, key, value)

    await db_session.commit()
    await db_session.refresh(chat)
    return chat


async def get_chat_by_chatid(db_session: AsyncSession, chat_id: uuid.UUID):
    record = (
        (
            await db_session.execute(
                select(ChatRecord).filter(ChatRecord.chat_id == chat_id)
            )
        )
        .scalars()
        .first()
    )

    logger.info(f"Record Found: {record}")

    if not record:
        raise HTTPException(status_code=404, detail="Chat record not found")

    return record
