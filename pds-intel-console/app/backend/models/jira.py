from pydantic import BaseModel


class JiraCreateRequest(BaseModel):
    summary: str
    description: str | None = None


class JiraCreateResponse(BaseModel):
    key: str
    url: str
