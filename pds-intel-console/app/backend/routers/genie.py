from fastapi import APIRouter

from models.genie import GenieRequest, GenieResponse, VizHints

router = APIRouter()


def call_genie(prompt: str, context: dict | None = None) -> GenieResponse:
    rows = [
        ["2025-01", 120000.0],
        ["2025-02", 125500.0],
        ["2025-03", 132250.0],
    ]
    viz_hints = VizHints(chartType="line", x="month", y="total_cost", isTimeSeries=True)
    return GenieResponse(
        narrative=(
            "Capital spend is trending upward month over month with a 10% increase in March "
            "driven by vendor mobilization."
        ),
        sql="SELECT month, total_cost FROM finance.monthly_costs WHERE project = 'Northwind'",
        columns=["month", "total_cost"],
        rows=rows,
        viz_hints=viz_hints,
    )


@router.post('/ask', response_model=GenieResponse)
def ask_genie(request: GenieRequest) -> GenieResponse:
    return call_genie(request.prompt, request.context)
