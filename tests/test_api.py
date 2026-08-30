from fastapi.testclient import TestClient

from querypilot.api import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_request_is_accepted() -> None:
    response = client.post("/api/analysis", json={"question": "Why did leads fall?"})
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
