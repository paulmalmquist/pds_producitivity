from pydantic import BaseModel


class EmailSearchResponse(BaseModel):
    thread_id: str
    subject: str
    sender: str
    snippet: str
