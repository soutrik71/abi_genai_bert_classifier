import uuid
from backend.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class ChatRecord(Base):
    __tablename__ = "chat_record"

    session_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4, unique=True
    )

    chat_id: Mapped[uuid.UUID] = mapped_column(
        index=True, default=uuid.uuid4, unique=True
    )

    user_query: Mapped[str] = mapped_column(index=True)
    status: Mapped[str] = mapped_column(index=True, default="pending")
    prediction_label: Mapped[Optional[str]] = mapped_column(nullable=True)
    prediction_probability: Mapped[Optional[float]] = mapped_column(nullable=True)
