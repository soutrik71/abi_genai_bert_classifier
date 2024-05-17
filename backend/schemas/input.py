from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
import uuid


class UserInputCreate(BaseModel):
    user_query: Union[str, None]
    session_id: Union[uuid.UUID, None]


class UserInputShow(UserInputCreate):
    chat_id: Union[uuid.UUID, None]
    status: Union[str, None]


class PredictionInputShow(UserInputShow):
    prediction_label: Union[str, None]
    prediction_probability: Union[float, None]


# class InferenceResponse(BaseModel):
#     """
#     Output response for model inference
#     """

#     error: Optional[bool]
#     results: PredictionInputShow


class ErrorResponse(BaseModel):
    """
    Error response for the API
    """

    error: bool | None
    message: str | None
    traceback: str | None
