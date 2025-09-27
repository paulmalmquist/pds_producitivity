from pydantic import BaseModel


class TableauSnapshotRequest(BaseModel):
    viewId: str


class TableauSnapshotResponse(BaseModel):
    image_base64: str
    view_url: str
