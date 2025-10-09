"""Pydantic data models for API requests and responses."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

ChartType = Literal["auto", "line", "bar", "pie", "scatter", "kpi"]
Verdict = Literal["good", "bad"]


class AskRequest(BaseModel):
    question: str
    chart_preference: ChartType = "auto"
    top_k: int = 12


class ChartPayload(BaseModel):
    type: Literal["line", "bar", "pie", "scatter", "kpi"]
    spec: Dict[str, Any]
    image_base64: str


class AskResponse(BaseModel):
    answer_text: str
    sql: str
    fields_used: List[str]
    sampled_rows: List[Dict[str, Any]]
    chart: Optional[ChartPayload]


class SchemaColumn(BaseModel):
    name: str
    type: str
    comment: Optional[str] = None


class ForeignKey(BaseModel):
    col: str
    ref: str


class SchemaTable(BaseModel):
    full_name: str
    columns: List[SchemaColumn]
    pk: List[str] = Field(default_factory=list)
    fk: List[ForeignKey] = Field(default_factory=list)
    comment: Optional[str] = None


class SchemaResponse(BaseModel):
    tables: List[SchemaTable]
    synonyms: Dict[str, str]


class FeedbackRequest(BaseModel):
    question: str
    sql: str
    verdict: Verdict
    note: Optional[str] = None


class LoggedAskEvent(BaseModel):
    timestamp: datetime
    user_agent: Optional[str]
    question: str
    tables_considered: List[str]
    final_sql: str
    row_count: int


__all__ = [
    "AskRequest",
    "AskResponse",
    "ChartPayload",
    "SchemaResponse",
    "FeedbackRequest",
    "LoggedAskEvent",
]
