"""Helper module to access the Databricks SQL connector with a graceful fallback."""
from __future__ import annotations

import importlib.util
from typing import Any


_spec = importlib.util.find_spec("databricks.sql")
if _spec is not None:
    from databricks import sql as dbsql  # type: ignore
else:
    class _MissingDatabricksModule:
        class DatabaseError(Exception):
            pass

        class Error(Exception):
            pass

        @staticmethod
        def connect(*_: Any, **__: Any) -> Any:
            raise RuntimeError(
                "databricks-sql-connector is not installed. Install it via requirements.txt before running the service."
            )

    dbsql = _MissingDatabricksModule()  # type: ignore


__all__ = ["dbsql"]
