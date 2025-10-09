"""Planner that converts natural language questions into SQL."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List

from app.config import get_settings
from app.llm.prompts import planner_prompt
from app.llm.provider import LLMProvider
from app.schema.resolver import resolve_synonyms, surface_relevant_columns
from app.schema.unity import UnityCatalogClient, build_condensed_context


@dataclass
class PlanResult:
    sql: str
    fields_used: List[str]
    assumptions: str
    tables_considered: List[str]
    schema_context: str


class NL2SQLPlanner:
    def __init__(self, llm: LLMProvider, unity_client: UnityCatalogClient) -> None:
        self.llm = llm
        self.unity_client = unity_client
        self.settings = get_settings()

    def _rules_text(self) -> str:
        return "\n".join(
            [
                "- Single SELECT statement only.",
                "- No CREATE/ALTER/DROP/DELETE/UPDATE/INSERT statements.",
                "- Use fully qualified table names when ambiguity exists.",
                "- Infer reasonable date filters when the question implies a period.",
                f"- Apply LIMIT {self.settings.max_rows} for row-level outputs.",
            ]
        )

    def build_plan(self, question: str, top_k: int) -> PlanResult:
        tables = self.unity_client.get_tables()
        condensed = build_condensed_context(tables, question, top_k_tables=top_k, max_columns=50)
        synonyms = resolve_synonyms(question)
        relevant_columns = surface_relevant_columns(question, tables)
        if relevant_columns:
            column_lines = "\n".join(f"Hint: {table}.{column}" for table, column in relevant_columns)
            condensed_text = f"{condensed['text']}\n{column_lines}"
        else:
            condensed_text = condensed["text"]
        prompt = planner_prompt(
            question=question,
            schema_context=condensed_text,
            synonyms=synonyms,
            rules=self._rules_text(),
            max_rows=self.settings.max_rows,
        )
        try:
            response = self.llm.complete(prompt)
        except json.JSONDecodeError:
            response = self.llm.complete(prompt + "\nRespond ONLY with JSON.")
        if not isinstance(response, dict) or "sql" not in response:
            raise ValueError("LLM response missing SQL")
        sql = response.get("sql", "").strip()
        fields = response.get("fields_used", [])
        if not isinstance(fields, list):
            fields = []
        assumptions = response.get("assumptions", "")
        return PlanResult(
            sql=sql,
            fields_used=fields,
            assumptions=assumptions,
            tables_considered=condensed["tables"],
            schema_context=condensed_text,
        )


__all__ = ["NL2SQLPlanner", "PlanResult"]
