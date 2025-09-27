from fastapi import APIRouter

from models.tableau import TableauSnapshotRequest, TableauSnapshotResponse

router = APIRouter()


@router.get('/views')
def list_views() -> list[dict]:
    return [
        {'id': 'view-1', 'name': 'Executive Dashboard', 'project': 'PDS', 'url': 'https://tableau.example.com/views/view-1'},
        {'id': 'view-2', 'name': 'Vendor Health', 'project': 'PDS', 'url': 'https://tableau.example.com/views/view-2'},
    ]


@router.post('/snapshot', response_model=TableauSnapshotResponse)
def snapshot(request: TableauSnapshotRequest) -> TableauSnapshotResponse:
    image_base64 = 'iVBORw0KGgoAAAANSUhEUgAA'
    view_url = f'https://tableau.example.com/views/{request.viewId}'
    return TableauSnapshotResponse(image_base64=image_base64, view_url=view_url)
