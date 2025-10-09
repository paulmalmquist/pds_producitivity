"""SQL validation utilities."""
from __future__ import annotations

import re
from contextlib import closing

from app.sql.dbsql import dbsql

from app.config import get_settings

FORBIDDEN_KEYWORDS = ["UPDATE", "DELETE", "INSERT", "TRUNCATE", "CREATE", "ALTER", "DROP"]


def ensure_select_only(sql_text: str) -> None:
    normalized = sql_text.strip().upper()
    if not normalized.startswith("SELECT") and not normalized.startswith("WITH"):
        raise ValueError("Only SELECT statements are allowed")
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", normalized):
            raise ValueError(f"Forbidden keyword detected: {keyword}")


def dry_run(sql_text: str) -> None:
    settings = get_settings()
    explain_query = f"EXPLAIN \n{sql_text}"
    with dbsql.connect(
        server_hostname=settings.databricks_host,
        http_path=settings.databricks_http_path,
        access_token=settings.databricks_pat,
    ) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(explain_query)
            cursor.fetchall()


__all__ = ["ensure_select_only", "dry_run"]
