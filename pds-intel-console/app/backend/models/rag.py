from pydantic import BaseModel


class RagRequest(BaseModel):
    prompt: str


class RagSource(BaseModel):
    title: str
    url: str


class RagResponse(BaseModel):
    answer: str
    sources: list[RagSource]
    entities: list[str]
