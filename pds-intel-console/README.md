# PDS Intel Console

Monorepo containing the Angular-based JLL PDS intelligence console and FastAPI orchestration services.

## Contents
- `app/frontend` — Angular 20 standalone application with AI chat, context deck, and workspace persistence.
- `app/backend` — FastAPI APIs for routing, Databricks Genie proxying, Jira/Tableau automation, and SSE streaming.
- `app/infra` — Compose stack, environment template, and helper Makefile.

Refer to `app/infra/README.md` for local development instructions.
