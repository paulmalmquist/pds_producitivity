"""Configuration management for the FastAPI Databricks NL->SQL service."""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings sourced from environment variables."""

    llm_provider: str = Field("openai", alias="LLM_PROVIDER")
    llm_model: str = Field("gpt-4o-mini", alias="LLM_MODEL")

    databricks_host: str = Field(..., alias="DATABRICKS_HOST")
    databricks_http_path: str = Field(..., alias="DATABRICKS_HTTP_PATH")
    databricks_pat: str = Field(..., alias="DATABRICKS_PERSONAL_ACCESS_TOKEN")

    default_catalogs: List[str] = Field(default_factory=list, alias="DEFAULT_CATALOGS")
    default_schemas: List[str] = Field(default_factory=list, alias="DEFAULT_SCHEMAS")

    max_rows: int = Field(500, alias="MAX_ROWS")
    chart_engine: str = Field("matplotlib", alias="CHART_ENGINE")
    allowed_statements: str = Field("SELECT_ONLY", alias="ALLOWED_STATEMENTS")
    openai_api_key: str | None = Field(None, alias="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(None, alias="ANTHROPIC_API_KEY")

    cache_ttl_seconds: int = 600
    question_cache_ttl_seconds: int = 120

    llm_timeout: int = 30
    sql_timeout: int = 90

    feedback_path: str = "feedback/events.jsonl"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __init__(self, **data: object) -> None:
        if "DEFAULT_CATALOGS" in data and isinstance(data["DEFAULT_CATALOGS"], str):
            data["DEFAULT_CATALOGS"] = [c.strip() for c in data["DEFAULT_CATALOGS"].split(",") if c.strip()]
        if "DEFAULT_SCHEMAS" in data and isinstance(data["DEFAULT_SCHEMAS"], str):
            data["DEFAULT_SCHEMAS"] = [s.strip() for s in data["DEFAULT_SCHEMAS"].split(",") if s.strip()]
        super().__init__(**data)


@lru_cache()
def get_settings() -> Settings:
    return Settings()


__all__ = ["Settings", "get_settings"]
