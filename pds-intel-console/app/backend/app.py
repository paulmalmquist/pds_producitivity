from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    charts,
    email,
    genie,
    health,
    jira,
    playbooks,
    rag,
    router,
    sql,
    stream,
    tableau,
)

app = FastAPI(title="PDS Intel Console API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router, prefix="/router", tags=["router"])
app.include_router(rag.router, prefix="/rag", tags=["rag"])
app.include_router(genie.router, prefix="/genie", tags=["genie"])
app.include_router(sql.router, prefix="/sql", tags=["sql"])
app.include_router(charts.router, prefix="/charts", tags=["charts"])
app.include_router(jira.router, prefix="/jira", tags=["jira"])
app.include_router(tableau.router, prefix="/tableau", tags=["tableau"])
app.include_router(email.router, prefix="/email", tags=["email"])
app.include_router(playbooks.router, prefix="/playbooks", tags=["playbooks"])
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(stream.router, prefix="/stream", tags=["stream"])
