from pydantic import BaseModel


class HealthStatus(BaseModel):
    databricks: str
    jira: str
    tableau: str
    email: str
    jll_gpt: str
