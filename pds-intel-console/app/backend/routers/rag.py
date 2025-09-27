from fastapi import APIRouter

from models.rag import RagRequest, RagResponse, RagSource

router = APIRouter()


@router.post('/ask', response_model=RagResponse)
def ask_rag(request: RagRequest) -> RagResponse:
    answer = (
        "Here is what I found about your request. The Northwind project is tracking on schedule "
        "with a minor variance in vendor onboarding."
    )
    sources = [
        RagSource(title="Project Charter", url="https://example.com/charter"),
        RagSource(title="Vendor Playbook", url="https://example.com/playbook"),
    ]
    entities = ["Northwind HQ Refresh", "Acme Contractors", "Variance"]
    return RagResponse(answer=answer, sources=sources, entities=entities)
