"""
This module defines API endpoints for handling chat records. The endpoints allow
for creating, updating, retrieving, and deleting chat records using the FastAPI framework.

Endpoints:
- POST /chat: Create a new chat record.
- PUT /chat: Update an existing chat record.
- GET /chat/{chat_id}: Retrieve a chat record by its chat ID.
- DELETE /chat/{chat_id}: Delete a chat record by its chat ID.
"""

# Import necessary modules and components
from backend.dependencies.core import DBSessionDep as db_session
from backend.crud.chat import (
    create_chat,
    get_chat_by_chatid,
    update_chat_by_chatid,
    delete_chat_by_chatid,
)
from fastapi import APIRouter, status, Request, HTTPException, Depends
from backend.schemas.input import UserInputCreate, UserInputShow, PredictionInputShow
import uuid
from src.dummy_code import dummy_prediction
import logging
from src.settings import LoggerSettings
from backend.dependencies.auth import security, verification
from typing import Annotated

# Setup logger
logger = logging.getLogger(LoggerSettings().logger_name)

# Initialize router
router = APIRouter(tags=["chat_records"])


# @router.post("/chat", response_model=UserInputShow, status_code=status.HTTP_201_CREATED)
# async def create_chat_api(request: Request, user_chat: UserInputCreate, db: db_session):
#     """
#     Create a new chat record.

#     Args:
#     - request (Request): The incoming request object.
#     - user_chat (UserInputCreate): The user input data for creating a chat.
#     - db (db_session): The database session.

#     Returns:
#     - UserInputShow: The created chat record.
#     """
#     if not user_chat.session_id:
#         user_chat.session_id = uuid.uuid4()

#     updated_record = user_chat.dict()
#     updated_record["chat_id"] = uuid.uuid4()

#     logger.info(f"Record with chat id: {updated_record}")

#     return await create_chat(db, updated_record)


# @router.put("/chat", response_model=PredictionInputShow, status_code=status.HTTP_200_OK)
# async def update_chat_api(request: Request, user_chat: UserInputShow, db: db_session):
#     """
#     Update an existing chat record.

#     Args:
#     - request (Request): The incoming request object.
#     - user_chat (UserInputShow): The user input data for updating a chat.
#     - db (db_session): The database session.

#     Returns:
#     - PredictionInputShow: The updated chat record with prediction results.
#     """
#     chat_record = user_chat.dict()
#     prediction = dummy_prediction(user_chat.user_query)
#     chat_record["prediction_label"] = prediction["prediction_label"]
#     chat_record["prediction_probability"] = prediction["prediction_probability"]
#     chat_record["status"] = "completed"

#     logger.info(f"Updated record: {chat_record}")

#     return await update_chat_by_chatid(db, chat_record)


@router.get(
    "/chat/{chat_id}",
    response_model=PredictionInputShow,
    status_code=status.HTTP_200_OK,
)
async def get_chat_by_chatid_api(
    request: Request,
    chat_id: uuid.UUID,
    db: db_session,
    Verification: Annotated[bool, Depends(verification)],
):
    """
    Retrieve a chat record by its chat ID.

    Args:
    - request (Request): The incoming request object.
    - chat_id (uuid.UUID): The unique identifier of the chat record.
    - db (db_session): The database session.

    Returns:
    - PredictionInputShow: The retrieved chat record.
    """
    if not Verification:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return await get_chat_by_chatid(db, chat_id)


@router.delete(
    "/chat/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chat_by_chatid_api(
    request: Request,
    chat_id: uuid.UUID,
    db: db_session,
    Verification: Annotated[bool, Depends(verification)],
):
    """
    Delete a chat record by its chat ID.

    Args:
    - request (Request): The incoming request object.
    - chat_id (uuid.UUID): The unique identifier of the chat record.
    - db (db_session): The database session.

    Returns:
    - HTTP_204_NO_CONTENT: No content status indicating successful deletion.
    """
    if not Verification:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return await delete_chat_by_chatid(db, chat_id)
