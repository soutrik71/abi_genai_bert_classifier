"""
This module defines Pydantic models for handling user input and output for the API.
The models include structures for creating and showing user inputs, prediction results, and error responses.

Models:
- UserInputCreate: Model for creating user input with user query and session ID.
- UserInputShow: Model for showing user input with additional chat ID and status.
- PredictionInputShow: Model for showing prediction results with label and probability.
- ErrorResponse: Model for error responses in the API.
"""

# Import necessary modules and components
from typing import Optional, Union
from pydantic import BaseModel
import uuid


class UserInputCreate(BaseModel):
    """
    Model for creating user input.

    Attributes:
    - user_query (Union[str, None]): The user's query string.
    - session_id (Union[uuid.UUID, None]): The unique session identifier.
    """

    user_query: Union[str, None]
    session_id: Union[uuid.UUID, None]


class UserInputShow(UserInputCreate):
    """
    Model for showing user input with additional information.

    Attributes:
    - chat_id (Union[uuid.UUID, None]): The unique chat identifier.
    - status (Union[str, None]): The status of the chat.
    """

    chat_id: Union[uuid.UUID, None]
    status: Union[str, None]


class PredictionInputShow(UserInputShow):
    """
    Model for showing prediction results.

    Attributes:
    - prediction_label (Union[str, None]): The label predicted by the model.
    - prediction_probability (Union[float, None]): The probability of the predicted label.
    """

    prediction_label: Union[str, None]
    prediction_probability: Union[float, None]


# Uncomment the InferenceResponse class if it is needed in the future
# class InferenceResponse(BaseModel):
#     """
#     Output response for model inference.
#
#     Attributes:
#     - error (Optional[bool]): Indicates if there was an error.
#     - results (PredictionInputShow): The prediction results.
#     """
#     error: Optional[bool]
#     results: PredictionInputShow


class ErrorResponse(BaseModel):
    """
    Model for error responses in the API.

    Attributes:
    - error (Optional[bool]): Indicates if there was an error.
    - message (Optional[str]): The error message.
    - traceback (Optional[str]): The traceback of the error.
    """

    error: Optional[bool]
    message: Optional[str]
    traceback: Optional[str]
