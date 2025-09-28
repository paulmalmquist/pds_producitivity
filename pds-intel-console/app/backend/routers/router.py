from fastapi import APIRouter

from models.router import ClassifyRequest, ClassifyResponse
from utils.intent_classifier import classify_intent

router = APIRouter()


@router.post('/classify', response_model=ClassifyResponse)
def classify(request: ClassifyRequest) -> ClassifyResponse:
    intent, reasons = classify_intent(request.prompt)
    return ClassifyResponse(intent=intent, reasons=reasons)
