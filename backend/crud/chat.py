"""
This module provides CRUD operations for the ChatRecord model using SQLAlchemy with asynchronous support.
Functions included:
- create_chat: Create a new chat record.
- update_chat_by_chatid: Update an existing chat record by its chat_id.
- get_chat_by_chatid: Retrieve a chat record by its chat_id.
- delete_chat_by_chatid: Delete a chat record by its chat_id.
"""

# Import necessary modules and components
import uuid
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db_models.models import ChatRecord
import logging
from src.settings import LoggerSettings

# Setup logger
logger = logging.getLogger(LoggerSettings().logger_name)


async def create_chat(db_session: AsyncSession, chat_dict: dict):
    """
    Create a new chat record in the database and meant to be used with the prediction route.

    Args:
    - db_session (AsyncSession): The database session.
    - chat_dict (dict): A dictionary containing the chat record details.

    Returns:
    - ChatRecord: The newly created chat record.
    """
    chat_record = ChatRecord(**chat_dict)
    db_session.add(chat_record)
    await db_session.commit()
    await db_session.refresh(chat_record)
    return chat_record


async def update_chat_by_chatid(db_session: AsyncSession, chat_dict: dict):
    """
    Update an existing chat record in the database by its chat_id and meant to be used with the prediction route.

    Args:
    - db_session (AsyncSession): The database session.
    - chat_dict (dict): A dictionary containing the updated chat record details.

    Returns:
    - ChatRecord: The updated chat record.

    Raises:
    - HTTPException: If the chat record is not found.
    """
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
    """
    Retrieve a chat record from the database by its chat_id.

    Args:
    - db_session (AsyncSession): The database session.
    - chat_id (uuid.UUID): The unique identifier of the chat record.

    Returns:
    - ChatRecord: The retrieved chat record.

    Raises:
    - HTTPException: If the chat record is not found.
    """
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


async def delete_chat_by_chatid(db_session: AsyncSession, chat_id: uuid.UUID):
    """
    Delete a chat record from the database by its chat_id.

    Args:
    - db_session (AsyncSession): The database session.
    - chat_id (uuid.UUID): The unique identifier of the chat record.

    Returns:
    - ChatRecord: The deleted chat record.

    Raises:
    - HTTPException: If the chat record is not found.
    """
    record = (
        (
            await db_session.execute(
                select(ChatRecord).filter(ChatRecord.chat_id == chat_id)
            )
        )
        .scalars()
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="Chat record not found")

    db_session.delete(record)
    logger.info(f"Record Deleted: {record}")
    await db_session.commit()
    await db_session.refresh(record)
    return
