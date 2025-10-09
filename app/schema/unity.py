"""Unity Catalog metadata utilities."""
from __future__ import annotations

import re
from contextlib import closing
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from app.sql.dbsql import dbsql

from app.config import get_settings
from app.utils import TTLCache


@dataclass
class Column:
    name: str
    type: str
    comment: Optional[str]


@dataclass
class Table:
    catalog: str
    schema: str
    name: str
    columns: List[Column]
    comment: Optional[str]

    @property
    def full_name(self) -> str:
        return f"{self.catalog}.{self.schema}.{self.name}"


class UnityCatalogClient:
    """Fetches and caches Unity Catalog metadata."""

    def __init__(self) -> None:
        settings = get_settings()
        self.host = settings.databricks_host
        self.http_path = settings.databricks_http_path
        self.token = settings.databricks_pat
        self.catalogs = settings.default_catalogs
        self.schemas = settings.default_schemas
        self.cache = TTLCache(settings.cache_ttl_seconds)

    def _connect(self):
        return dbsql.connect(
            server_hostname=self.host,
            http_path=self.http_path,
            access_token=self.token,
        )

    def _load_metadata(self) -> List[Table]:
        conditions: List[str] = ["table_schema NOT IN ('information_schema')"]
        if self.catalogs:
            formatted = ",".join(f"'{c}'" for c in self.catalogs)
            conditions.append(f"table_catalog IN ({formatted})")
        if self.schemas:
            formatted = ",".join(f"'{s}'" for s in self.schemas)
            conditions.append(f"table_schema IN ({formatted})")
        where_clause = " AND ".join(conditions)
        query = f"""
            SELECT
                c.table_catalog,
                c.table_schema,
                c.table_name,
                c.column_name,
                c.data_type,
                c.comment AS column_comment,
                t.comment AS table_comment
            FROM system.information_schema.columns c
            LEFT JOIN system.information_schema.tables t
                ON c.table_catalog = t.table_catalog
                AND c.table_schema = t.table_schema
                AND c.table_name = t.table_name
            WHERE {where_clause}
            ORDER BY c.table_catalog, c.table_schema, c.table_name, c.ordinal_position
        """
        with self._connect() as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        tables: Dict[str, Table] = {}
        for catalog, schema, name, column, dtype, column_comment, table_comment in rows:
            key = f"{catalog}.{schema}.{name}"
            if key not in tables:
                derived_comment = table_comment or name.replace("_", " ")
                tables[key] = Table(
                    catalog=catalog,
                    schema=schema,
                    name=name,
                    columns=[],
                    comment=derived_comment,
                )
            tables[key].columns.append(Column(name=column, type=dtype, comment=column_comment))
        return list(tables.values())

    def get_tables(self) -> List[Table]:
        cached = self.cache.get("metadata")
        if cached is not None:
            return cached
        tables = self._load_metadata()
        self.cache.set("metadata", tables)
        return tables


def derive_pk_fk(table: Table) -> Dict[str, List[str]]:
    pk_candidates = [col.name for col in table.columns if col.name.endswith("_id") or col.name == "id"]
    fk_candidates = []
    for col in table.columns:
        match = re.match(r"(.*)_id", col.name)
        if match:
            ref = match.group(1)
            fk_target = f"{table.catalog}.{table.schema}.{ref}(id)"
            fk_candidates.append(f"{col.name}->{fk_target}")
    return {"pk": pk_candidates, "fk": fk_candidates}


def build_condensed_context(
    tables: Iterable[Table],
    question: str,
    top_k_tables: int = 12,
    max_columns: int = 50,
) -> Dict[str, List[str] | str]:
    question_lower = question.lower()
    scored: List[tuple[int, Table]] = []
    for table in tables:
        score = 0
        if table.name.lower() in question_lower:
            score += 3
        if table.schema.lower() in question_lower:
            score += 1
        for column in table.columns:
            if column.name.lower() in question_lower:
                score += 1
        scored.append((score, table))
    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [table for _, table in scored[:top_k_tables]]

    context_lines: List[str] = []
    included_columns = 0
    for table in selected:
        derived = derive_pk_fk(table)
        pk_line = f"PK: {', '.join(derived['pk'])}" if derived["pk"] else ""
        fk_line = "" if not derived["fk"] else "FK hints: " + ", ".join(derived["fk"])
        header = " ".join(part for part in [f"Table {table.full_name}", pk_line, fk_line] if part)
        context_lines.append(header)
        for column in table.columns:
            if included_columns >= max_columns:
                break
            desc = column.comment or column.name.replace("_", " ")
            context_lines.append(f"- {column.name} ({column.type}): {desc}")
            included_columns += 1
    return {
        "text": "\n".join(context_lines),
        "tables": [table.full_name for table in selected],
    }


DEFAULT_SYNONYMS: Dict[str, str] = {
    "arr": "finance.revenue.annual_recurring_revenue",
    "revpor": "finance.revenue.revenue_per_room",
}


def get_synonyms() -> Dict[str, str]:
    return DEFAULT_SYNONYMS


__all__ = [
    "UnityCatalogClient",
    "Table",
    "Column",
    "build_condensed_context",
    "get_synonyms",
    "derive_pk_fk",
]
