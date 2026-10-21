import pytest

from app.reports import build_incident_report


def test_high_latency_report():
    report = build_incident_report("high_latency")

    assert report["scenario"] == "high_latency"
    assert report["evidence"]["response_time"]["response_time_ms"] == 2500
    assert report["evidence"]["response_time"]["within_threshold"] is False
    assert report["incident_start_time"] is None
    assert len(report["recommended_actions"]) > 0


def test_database_down_report():
    report = build_incident_report("database_down")

    assert report["scenario"] == "database_down"
    assert report["evidence"]["health"]["healthy"] is False
    assert report["evidence"]["response_time"]["response_time_ms"] is None
    assert "Database" in report["likely_cause"]
    assert report["incident_start_time"] is None


def test_healthy_report():
    report = build_incident_report("healthy")

    assert report["evidence"]["health"]["healthy"] is True
    assert report["likely_cause"] == "No incident detected."


def test_invalid_scenario():
    with pytest.raises(ValueError):
        build_incident_report("unknown")