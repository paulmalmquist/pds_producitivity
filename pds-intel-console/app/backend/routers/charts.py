from fastapi import APIRouter

from models.charts import ChartRenderRequest, ChartRenderResponse
from utils.chart_builder import suggest_chart

router = APIRouter()


@router.post('/render', response_model=ChartRenderResponse)
def render_chart(request: ChartRenderRequest) -> ChartRenderResponse:
    chart_type = suggest_chart(request.columns, request.rows, request.viz_hints)
    spec = {
        'type': chart_type,
        'data': {
            'labels': [row[0] for row in request.rows],
            'datasets': [
                {
                    'label': request.columns[1] if len(request.columns) > 1 else request.columns[0],
                    'data': [row[1] for row in request.rows],
                }
            ],
        },
    }
    return ChartRenderResponse(chartSpec=spec)
