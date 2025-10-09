from app.llm.prompts import planner_prompt


def test_planner_prompt_contains_rules_and_tables():
    question = "Show revenue by region"
    schema_context = "Table finance.analytics.revenue\n- region (STRING)"
    prompt = planner_prompt(question, schema_context, {"arr": "finance.analytics.revenue.arr"}, "- rule", 100)
    assert "finance.analytics.revenue" in prompt
    assert "SELECT" in prompt.upper()
    assert "arr ->" in prompt
