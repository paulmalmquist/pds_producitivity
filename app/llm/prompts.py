"""Prompt templates for the NL->SQL workflow."""
from __future__ import annotations

from textwrap import dedent
from typing import Dict


FEW_SHOTS = [
    {
        "question": "How many new customers signed up last month?",
        "schema": "Table sales.customers PK: id\n- id (INT): customer id\n- signup_date (DATE): signup date\n- plan (STRING): product plan",
        "sql": "SELECT DATE_TRUNC('month', signup_date) AS month, COUNT(*) AS new_customers\nFROM sales.customers\nWHERE signup_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL 1 MONTH)\n  AND signup_date < DATE_TRUNC('month', CURRENT_DATE)\nGROUP BY 1",
    },
    {
        "question": "Show top 5 products by revenue last quarter",
        "schema": "Table sales.order_items\n- product_id (INT): product identifier\n- revenue (DECIMAL): revenue per line\nTable sales.products\n- id (INT): product id\n- name (STRING): product name",
        "sql": "SELECT p.name, SUM(oi.revenue) AS total_revenue\nFROM sales.order_items oi\nJOIN sales.products p ON oi.product_id = p.id\nWHERE oi.order_date >= DATE_TRUNC('quarter', CURRENT_DATE - INTERVAL 1 QUARTER)\n  AND oi.order_date < DATE_TRUNC('quarter', CURRENT_DATE)\nGROUP BY p.name\nORDER BY total_revenue DESC\nLIMIT 5",
    },
    {
        "question": "Compare ARR by region",
        "schema": "Table finance.revenue\n- region (STRING): customer region\n- arr (DOUBLE): annual recurring revenue",
        "sql": "SELECT region, SUM(arr) AS total_arr\nFROM finance.revenue\nGROUP BY region\nORDER BY total_arr DESC",
    },
]


def planner_prompt(question: str, schema_context: str, synonyms: Dict[str, str], rules: str, max_rows: int) -> str:
    examples = "\n\n".join(
        dedent(
            f"""Question: {item['question']}\nSchema:\n{item['schema']}\nSQL:\n{item['sql']}"""
        )
        for item in FEW_SHOTS
    )
    synonym_text = "\n".join(f"{k} -> {v}" for k, v in synonyms.items()) or "(none)"
    return dedent(
        f"""
        You are a senior analytics engineer. Convert the user's question into a single SELECT-only SQL query for Databricks.
        Follow these rules strictly:
        {rules}
        Always respond with valid JSON only: {{"sql": "...", "fields_used": ["table.column"...], "assumptions": "..."}}.
        Do not include markdown.

        Synonyms:\n{synonym_text}

        Condensed schema context:\n{schema_context}

        Examples:\n{examples}

        User question: {question}

        Remember to cap row-level outputs with LIMIT {max_rows} when the query would otherwise return many rows.
        """
    ).strip()


def repair_prompt(question: str, schema_context: str, error_message: str, previous_sql: str, max_rows: int) -> str:
    return dedent(
        f"""
        The previous SQL failed with the following Databricks error:
        {error_message}

        Please revise the SQL while respecting all original constraints:
        - Single SELECT statement only.
        - No DDL/DML or mutations.
        - Prefer aggregates, include LIMIT {max_rows} when many rows could return.
        - Maintain consistent field naming if possible.

        Schema context:\n{schema_context}

        Original question: {question}
        Previous SQL: {previous_sql}

        Respond with strict JSON: {{"sql": "...", "fields_used": ["table.column"...], "assumptions": "..."}}.
        """
    ).strip()


__all__ = ["planner_prompt", "repair_prompt", "FEW_SHOTS"]
