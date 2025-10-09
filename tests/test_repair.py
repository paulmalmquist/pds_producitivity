from app.llm.planner import PlanResult
from app.llm.provider import LLMProvider
from app.sql.repair import SQLRepairExecutor


class FakeLLM(LLMProvider):
    def __init__(self) -> None:
        self.calls = 0

    def complete(self, prompt: str):
        self.calls += 1
        return {
            "sql": "SELECT fixed FROM table",
            "fields_used": ["table.fixed"],
            "assumptions": "",
        }


class FakeExecutor:
    def __init__(self) -> None:
        self.executed_sql = None

    def execute(self, sql_text: str):
        self.executed_sql = sql_text
        return [{"fixed": 1}]


def test_repair_attempt(monkeypatch):
    calls = {"count": 0}

    def failing_dry_run(sql_text: str):
        if calls["count"] == 0:
            calls["count"] += 1
            raise ValueError("missing column")
        calls["count"] += 1
        return None

    monkeypatch.setattr("app.sql.repair.dry_run", failing_dry_run)
    executor = SQLRepairExecutor(FakeLLM(), FakeExecutor())
    plan = PlanResult(
        sql="SELECT bad FROM table",
        fields_used=["table.bad"],
        assumptions="",
        tables_considered=["cat.schema.table"],
        schema_context="context",
    )
    sql, fields, rows = executor.run("question", plan)
    assert sql == "SELECT fixed FROM table"
    assert fields == ["table.fixed"]
    assert rows == [{"fixed": 1}]
