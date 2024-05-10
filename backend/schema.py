from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class InferenceInput(BaseModel):
    user_query: Union[str, None]


class InferenceResult(BaseModel):
    label: Union[str, None]
    prob: Union[float, None]


class InferenceResponse(BaseModel):
    """
    Output response for model inference
    """

    error: Union[bool, None]
    results: InferenceResult
