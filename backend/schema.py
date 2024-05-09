from typing import Any, Dict, List, Optional

from pydantic.v1 import BaseModel, Field


class InferenceInput(BaseModel):
    """
    Input values for model inference
    """

    user_query: str = Field(..., title="User query")


class InferenceResult(BaseModel):
    """
    Inference result from the model
    """

    model_output: Dict[str, Any] = Field(..., title="Model output")


class InferenceResponse(BaseModel):
    """
    Output response for model inference
    """

    error: bool = Field(..., example=False, title="Whether there is error")
    results: InferenceResult
