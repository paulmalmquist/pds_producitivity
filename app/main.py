"""FastAPI application entry point."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import Settings, get_settings
from app.llm.planner import NL2SQLPlanner
from app.llm.provider import get_provider
from app.models import AskRequest, AskResponse, FeedbackRequest, ForeignKey, LoggedAskEvent, SchemaColumn, SchemaResponse, SchemaTable
from app.schema.unity import UnityCatalogClient, derive_pk_fk, get_synonyms
from app.sql.executor import DatabricksExecutor
from app.sql.repair import SQLRepairExecutor
from app.utils import (
    extract_user_agent,
    format_answer_summary,
    log_ask_event,
    log_feedback_event,
    question_cache,
)
from app.viz.render import ChartRenderer
from app.viz.selector import select_chart


app = FastAPI(title="Databricks NL2SQL")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


def get_unity_client() -> UnityCatalogClient:
    return UnityCatalogClient()


def get_planner(unity_client: UnityCatalogClient = Depends(get_unity_client)) -> NL2SQLPlanner:
    provider = get_provider()
    return NL2SQLPlanner(provider, unity_client)


def get_repair_executor(
    planner: NL2SQLPlanner = Depends(get_planner),
) -> SQLRepairExecutor:
    provider = planner.llm
    executor = DatabricksExecutor()
    return SQLRepairExecutor(provider, executor)


def get_chart_renderer() -> ChartRenderer:
    return ChartRenderer()


@app.get("/schema", response_model=SchemaResponse)
def read_schema(unity_client: UnityCatalogClient = Depends(get_unity_client)) -> SchemaResponse:
    tables = unity_client.get_tables()
    response_tables = []
    for table in tables:
        derived = derive_pk_fk(table)
        response_tables.append(
            SchemaTable(
                full_name=table.full_name,
                columns=[SchemaColumn(name=col.name, type=col.type, comment=col.comment) for col in table.columns],
                pk=derived["pk"],
                fk=[
                    ForeignKey(col=mapping.split("->", 1)[0], ref=mapping.split("->", 1)[1])
                    for mapping in derived["fk"]
                ],
                comment=table.comment,
            )
        )
    return SchemaResponse(tables=response_tables, synonyms=get_synonyms())


@app.post("/ask", response_model=AskResponse)
def ask_question(
    request: AskRequest,
    http_request: Request,
    planner: NL2SQLPlanner = Depends(get_planner),
    repair_executor: SQLRepairExecutor = Depends(get_repair_executor),
    renderer: ChartRenderer = Depends(get_chart_renderer),
) -> AskResponse:
    cache_key = json.dumps(request.dict(), sort_keys=True)
    cached = question_cache.get(cache_key)
    if cached:
        return AskResponse(**cached)
    plan = planner.build_plan(request.question, request.top_k)
    try:
        final_sql, fields_used, rows = repair_executor.run(request.question, plan)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    chart_payload = None
    chart_choice = select_chart(rows, request.chart_preference)
    if chart_choice:
        chart_type, spec = chart_choice
        image = renderer.render(chart_type, spec, rows, title=request.question)
        chart_payload = {"type": chart_type, "spec": spec, "image_base64": image}
    answer_text = format_answer_summary(request.question, rows)
    response = AskResponse(
        answer_text=answer_text,
        sql=final_sql,
        fields_used=fields_used,
        sampled_rows=rows,
        chart=chart_payload,
    )
    event = LoggedAskEvent(
        timestamp=datetime.utcnow(),
        user_agent=extract_user_agent(http_request),
        question=request.question,
        tables_considered=plan.tables_considered,
        final_sql=final_sql,
        row_count=len(rows),
    )
    payload = event.dict()
    payload["timestamp"] = event.timestamp.isoformat()
    log_ask_event(payload)
    question_cache.set(cache_key, response.dict())
    return response


@app.post("/feedback")
def submit_feedback(request: FeedbackRequest, settings: Settings = Depends(get_settings)) -> Dict[str, str]:
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": request.question,
        "sql": request.sql,
        "verdict": request.verdict,
        "note": request.note,
    }
    log_feedback_event(settings.feedback_path, event)
    return {"status": "recorded"}


@app.exception_handler(Exception)
async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return JSONResponse(status_code=500, content={"detail": str(exc)})


__all__ = ["app"]
