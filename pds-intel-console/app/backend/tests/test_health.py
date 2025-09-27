from fastapi.testclient import TestClient


def test_health_endpoint_reports_subsystems(client: TestClient):
    response = client.get('/health/')
    payload = response.json()
    assert payload['databricks'] == 'ok'
    assert payload['email'] == 'degraded'
    assert set(payload.keys()) == {'databricks', 'jira', 'tableau', 'email', 'jll_gpt'}
