
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_healthy_scenario():
    response = client.get("/status/healthy")

    assert response.status_code == 200
    assert response.json()["healthy"] is True


def test_database_failure():
    response = client.get("/status/database_down")

    assert response.status_code == 200
    assert response.json()["healthy"] is False
    assert "Database" in response.json()["message"]


def test_high_latency():
    response = client.get("/status/high_latency")

    assert response.status_code == 200
    assert response.json()["response_time_ms"] == 2500


def test_invalid_scenario():
    response = client.get("/status/unknown")

    assert response.status_code == 422
