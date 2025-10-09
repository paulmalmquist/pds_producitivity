import sys
from pathlib import Path

import pytest

pytest.importorskip("pydantic")
pytest.importorskip("fastapi")


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

@pytest.fixture(autouse=True)
def env_settings(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "test.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_HTTP_PATH", "/sql/warehouses/test")
    monkeypatch.setenv("DATABRICKS_PERSONAL_ACCESS_TOKEN", "dapi-test")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_MODEL", "gpt-test")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("CHART_ENGINE", "matplotlib")
    yield
