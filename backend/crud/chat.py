import uuid
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.db_model import ChatRecord


async def create_chat(db_session: AsyncSession, chat_record: ChatRecord):
    db_session.add(chat_record)
    await db_session.commit()
    await db_session.refresh(chat_record)
    return chat_record


async def get_chat_by_chat_id(db_session: AsyncSession, chat_id: uuid.UUID):
    record = (
        await db_session.execute(
            select(ChatRecord).filter(ChatRecord.chat_id == chat_id)
        )
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Chat record not found")

    return record
