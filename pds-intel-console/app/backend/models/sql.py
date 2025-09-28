from pydantic import BaseModel


class SqlRequest(BaseModel):
    sql: str


class SqlResponse(BaseModel):
    columns: list[str]
    rows: list[list[object]]
