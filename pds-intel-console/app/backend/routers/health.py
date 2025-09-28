from fastapi import APIRouter

from models.health import HealthStatus

router = APIRouter()


@router.get('/', response_model=HealthStatus)
def get_health() -> HealthStatus:
    return HealthStatus(
        databricks='ok',
        jira='ok',
        tableau='ok',
        email='degraded',
        jll_gpt='ok',
    )
