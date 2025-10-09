"""Databricks SQL execution helpers."""
from __future__ import annotations

from contextlib import closing
from typing import Any, Dict, List

from app.sql.dbsql import dbsql

from app.config import get_settings
from app.utils import summarize_rows


class DatabricksExecutor:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _connect(self):
        return dbsql.connect(
            server_hostname=self.settings.databricks_host,
            http_path=self.settings.databricks_http_path,
            access_token=self.settings.databricks_pat,
        )

    def execute(self, sql_text: str) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(sql_text)
                rows = cursor.fetchmany(self.settings.max_rows)
                description = cursor.description or []
        columns = [col[0] for col in description]
        dict_rows = [dict(zip(columns, row)) for row in rows]
        return summarize_rows(dict_rows, self.settings.max_rows)


__all__ = ["DatabricksExecutor"]
