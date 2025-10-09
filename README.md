# Databricks NL→SQL Assistant

A FastAPI service that turns natural-language questions into safe Databricks SQL queries, executes them, and returns readable answers with auto-generated charts.

## Prerequisites

- Python 3.12
- Access to a Databricks SQL Warehouse with read permissions
- API access to either OpenAI or Anthropic (set via `LLM_PROVIDER`)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

| Variable | Description |
| --- | --- |
| `LLM_PROVIDER` | `openai` or `anthropic` |
| `LLM_MODEL` | Model name for the chosen provider |
| `OPENAI_API_KEY` | Required when `LLM_PROVIDER=openai` |
| `ANTHROPIC_API_KEY` | Required when `LLM_PROVIDER=anthropic` |
| `DATABRICKS_HOST` | Databricks workspace hostname |
| `DATABRICKS_HTTP_PATH` | SQL Warehouse HTTP path |
| `DATABRICKS_PERSONAL_ACCESS_TOKEN` | Personal access token with read access |
| `DEFAULT_CATALOGS` | Optional comma-separated catalogs to index |
| `DEFAULT_SCHEMAS` | Optional comma-separated schemas to index |
| `MAX_ROWS` | Maximum rows to return (default 500) |
| `CHART_ENGINE` | `matplotlib` (default) or `plotly` |
| `ALLOWED_STATEMENTS` | Currently fixed to `SELECT_ONLY` |

Example `.env`:

```
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
DATABRICKS_HOST=dbc-123.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/abc
DATABRICKS_PERSONAL_ACCESS_TOKEN=dapi...
DEFAULT_CATALOGS=main
DEFAULT_SCHEMAS=analytics
MAX_ROWS=500
CHART_ENGINE=matplotlib
```

## Running the service

```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000/static/index.html](http://localhost:8000/static/index.html) to try the browser demo.

## How it works

1. **Schema intelligence** – Unity Catalog metadata is cached for 10 minutes and condensed per question.
2. **Planning** – Few-shot prompt templates steer the LLM to produce SELECT-only SQL with field provenance.
3. **Validation & repair** – Static guards plus `EXPLAIN` dry-run catch errors, with up to two LLM-assisted retries.
4. **Execution** – The validated SQL runs on the configured Databricks warehouse with read-only credentials.
5. **Visualization** – Chart heuristics select a chart type and render a PNG (matplotlib by default).
6. **Feedback** – POST `/feedback` appends review events to `feedback/events.jsonl` for future tuning.

Identical questions served within two minutes return cached answers. Each `/ask` is logged (question, tables considered, SQL, row count) without persisting sensitive row data.

## Example flow

1. Ask: “What was ARR by region last quarter?”
2. Planner selects revenue tables, proposes SQL with date filters and LIMIT.
3. Validator runs EXPLAIN; on success the query executes and returns aggregated rows.
4. Response includes answer text, SQL, sampled rows, and an auto-generated bar chart.

## Extending

- Add new synonyms in `app/schema/unity.py` or extend resolution logic in `app/schema/resolver.py`.
- Add more few-shot examples in `app/llm/prompts.py` to tailor behavior.
- Swap chart engines by setting `CHART_ENGINE=plotly` (requires plotly + kaleido).

## Testing

```bash
pytest
```
