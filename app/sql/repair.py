"""SQL repair loop that retries on errors."""
from __future__ import annotations

import json
from typing import List, Tuple

from app.sql.dbsql import dbsql

from app.config import get_settings
from app.llm.prompts import repair_prompt
from app.llm.provider import LLMProvider
from app.llm.planner import PlanResult
from app.sql.executor import DatabricksExecutor
from app.sql.validate import ensure_select_only, dry_run


class SQLRepairExecutor:
    def __init__(self, llm: LLMProvider, executor: DatabricksExecutor) -> None:
        self.llm = llm
        self.executor = executor
        self.settings = get_settings()
        self.max_retries = 2

    def run(self, question: str, plan: PlanResult) -> Tuple[str, List[str], List[dict]]:
        sql_text = plan.sql
        fields = plan.fields_used
        for attempt in range(self.max_retries + 1):
            ensure_select_only(sql_text)
            try:
                dry_run(sql_text)
                rows = self.executor.execute(sql_text)
                return sql_text, fields, rows
            except (dbsql.DatabaseError, dbsql.Error, ValueError) as exc:  # type: ignore[attr-defined]
                if attempt == self.max_retries:
                    raise RuntimeError(f"SQL failed after retries: {exc}")
                prompt = repair_prompt(
                    question=question,
                    schema_context=plan.schema_context,
                    error_message=str(exc),
                    previous_sql=sql_text,
                    max_rows=self.settings.max_rows,
                )
                try:
                    response = self.llm.complete(prompt)
                except json.JSONDecodeError:
                    response = self.llm.complete(prompt + "\nReturn JSON only.")
                sql_text = response.get("sql", sql_text)
                fields = response.get("fields_used", fields)
        raise RuntimeError("Repair loop exhausted")


__all__ = ["SQLRepairExecutor"]
