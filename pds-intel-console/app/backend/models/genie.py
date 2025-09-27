from pydantic import BaseModel


class GenieRequest(BaseModel):
    prompt: str
    context: dict | None = None


class VizHints(BaseModel):
    chartType: str | None = None
    x: str | None = None
    y: str | None = None
    series: str | None = None
    isTimeSeries: bool | None = None
    percentLike: bool | None = None


class GenieResponse(BaseModel):
    narrative: str
    sql: str
    columns: list[str]
    rows: list[list[object]]
    viz_hints: VizHints | None = None
