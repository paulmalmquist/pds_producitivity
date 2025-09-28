from pydantic import BaseModel


class Playbook(BaseModel):
    name: str
    steps: list[str]
