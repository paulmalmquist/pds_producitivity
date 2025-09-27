from fastapi import APIRouter

from models.jira import JiraCreateRequest, JiraCreateResponse

router = APIRouter()


@router.get('/standup-digest')
def standup_digest() -> dict:
    return {
        'blocked': ['Awaiting permit approval'],
        'in_progress': ['Site mobilization', 'Vendor onboarding'],
        'upcoming': ['Executive update draft'],
    }


@router.post('/create', response_model=JiraCreateResponse)
def create_issue(request: JiraCreateRequest) -> JiraCreateResponse:
    key = 'JLL-1234'
    url = f'https://jira.example.com/browse/{key}'
    return JiraCreateResponse(key=key, url=url)
