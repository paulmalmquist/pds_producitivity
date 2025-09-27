from models.router import ClassifyRequest
from routers.router import classify


def test_router_classification():
    request = ClassifyRequest(prompt='Create a Jira task and share the latest chart')
    response = classify(request)
    assert response.intent == 'mixed'
    assert any('jira' in reason for reason in response.reasons)
