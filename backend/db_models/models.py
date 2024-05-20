"""
This module defines the ORM model for chat records using SQLAlchemy.
The model represents chat interactions and their associated predictions.

Components:
- Base: Base class for the ORM models from SQLAlchemy.
- Mapped, mapped_column: Tools for defining ORM model columns and their properties.
- uuid: Module for generating unique identifiers.
- Optional: Type hint for optional fields.
"""

# Import necessary modules and components
import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base


class ChatRecord(Base):
    """
    ORM model for chat records.

    Attributes:
    - id: Primary key, auto-incremented, unique identifier for each chat record.
    - session_id: Unique identifier for a session, defaults to a new UUID.
    - chat_id: Unique identifier for a chat, defaults to a new UUID.
    - user_query: The user's query string.
    - status: The status of the chat, default is "pending".
    - prediction_label: The label predicted by the model, optional.
    - prediction_probability: The probability of the predicted label, optional.
    """

    __tablename__ = "chat_record"

    # Primary key for the chat record
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    # Unique session identifier, defaults to a new UUID
    session_id: Mapped[uuid.UUID] = mapped_column(index=True, default=uuid.uuid4)

    # Unique chat identifier, defaults to a new UUID
    chat_id: Mapped[uuid.UUID] = mapped_column(
        index=True, default=uuid.uuid4, unique=True
    )

    # User's query string
    user_query: Mapped[str] = mapped_column(index=True)

    # Status of the chat, default is "pending"
    status: Mapped[str] = mapped_column(index=True, default="pending")

    # Predicted label from the model, optional
    prediction_label: Mapped[Optional[str]] = mapped_column(nullable=True)

    # Probability of the predicted label, optional
    prediction_probability: Mapped[Optional[float]] = mapped_column(nullable=True)
