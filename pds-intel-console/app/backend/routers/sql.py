from fastapi import APIRouter

from models.sql import SqlRequest, SqlResponse

router = APIRouter()


@router.post('/run', response_model=SqlResponse)
def run_sql(request: SqlRequest) -> SqlResponse:
    columns = ["vendor", "spend"]
    rows = [["Acme Construction", 45000], ["BuildCo", 72000]]
    return SqlResponse(columns=columns, rows=rows)
