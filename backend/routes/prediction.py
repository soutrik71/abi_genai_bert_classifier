from fastapi import APIRouter, Body, status

from backend.schema import InferenceInput, InferenceResponse
from src.test_code import dummy_prediction

router = APIRouter()


@router.post(
    "/api/predict", response_model=InferenceResponse, status_code=status.HTTP_200_OK
)
def do_predict(user_query: InferenceInput):
    """
    Perform prediction on input data
    """
    # Perform prediction on input data
    results = dummy_prediction(user_query)
    return InferenceResponse(**results)
