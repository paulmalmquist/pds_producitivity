from pydantic import BaseModel, Field


class ClassifyRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


class ClassifyResponse(BaseModel):
    intent: str
    reasons: list[str]
