# PDS Intel Console Monorepo

This monorepo provisions the AI workbench for JLL PDS, combining an Angular 20 console with a FastAPI backend.

## Structure

```
/app
  /frontend   Angular 20 standalone application
  /backend    FastAPI services for routing, analytics, and automations
  /infra      Tooling, compose stack, and environment templates
```

## Getting Started

1. Copy `.env.example` to `.env` and populate credentials.
2. Install dependencies:
   - Frontend: `cd app/frontend && npm install`
   - Backend: `cd app/backend && pip install -r requirements.txt`
3. Start dev services via Docker Compose or the Makefile:
   - `cd app/infra && docker-compose up`
   - or `make dev`

The Angular app runs on `http://localhost:4200` and proxies to the FastAPI backend on `http://localhost:8000`.
