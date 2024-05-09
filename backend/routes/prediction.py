from fastapi import APIRouter, status

from backend.schema import InferenceInput, InferenceResult
from src.test_code import dummy_prediction

router = APIRouter()


@router.post(
    "/api/predict", response_model=InferenceResult, status_code=status.HTTP_200_OK
)
def do_predict(user_query: InferenceInput):
    """
    Perform prediction on input data
    """
    # Perform prediction on input data
    print(user_query)
    results = dummy_prediction(user_query)

    return results
