from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
import uuid


class UserInput(BaseModel):
    user_query: Union[str, None]
    session_id: Union[uuid.UUID, None]


class UserInputShow(UserInput):
    chat_id: Union[uuid.UUID, None]
    status: Union[str, None]
    prediction_label: Union[str, None]
    prediction_probability: Union[float, None]


class InferenceResult(BaseModel):
    prediction_label: Union[str, None]
    prediction_prob: Union[float, None]
    user_query: Union[str, None]
    prediction_class: Union[int, None]


class InferenceResponse(BaseModel):
    """
    Output response for model inference
    """

    error: Optional[bool]
    results: InferenceResult


class ErrorResponse(BaseModel):
    """
    Error response for the API
    """

    error: bool | None
    message: str | None
    traceback: str | None
