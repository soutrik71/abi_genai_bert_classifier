from fastapi import APIRouter, Request, status
from backend.schema import InferenceInput, InferenceResponse

from src.test_code import dummy_prediction

router = APIRouter()


@router.post(
    "/api/v1/predict", response_model=InferenceResponse, status_code=status.HTTP_200_OK
)
def do_predict(request: Request, body: InferenceInput):
    """
    Perform prediction on input data
    """
    # Perform prediction on input data
    results = dummy_prediction(body.user_query)

    return {"error": False, "results": results}
