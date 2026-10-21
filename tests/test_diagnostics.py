
from app.diagnostics import (
    check_service_health,
    get_recent_logs,
    check_response_time,
)


def test_healthy_service():
    result = check_service_health("healthy")
    assert result["healthy"] is True


def test_database_failure():
    result = check_service_health("database_down")
    assert result["healthy"] is False


def test_error_log():
    result = get_recent_logs("database_down")
    assert result["logs"][0]["level"] == "ERROR"


def test_high_latency():
    result = check_response_time("high_latency")
    assert result["within_threshold"] is False


def test_unknown_scenario():
    result = check_service_health("unknown")
    assert result["error"] == "Unknown scenario"
