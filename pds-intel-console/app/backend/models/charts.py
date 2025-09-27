from pydantic import BaseModel


class ChartRenderRequest(BaseModel):
    columns: list[str]
    rows: list[list[object]]
    viz_hints: dict | None = None


class ChartRenderResponse(BaseModel):
    chartSpec: dict
