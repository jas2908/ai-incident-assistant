
from datetime import datetime, timezone

from app.main import SCENARIOS


def check_service_health(scenario: str) -> dict:
    """Check the simulated service health."""
    if scenario not in SCENARIOS:
        return {"error": "Unknown scenario"}

    healthy, latency, message = SCENARIOS[scenario]

    return {
        "scenario": scenario,
        "healthy": healthy,
        "message": message,
    }


def get_recent_logs(scenario: str) -> dict:
    """Return simulated application logs."""
    if scenario not in SCENARIOS:
        return {"error": "Unknown scenario"}

    messages = {
        "healthy": ("INFO", "Application running normally"),
        "database_down": ("ERROR", "Database connection refused"),
        "high_latency": ("WARNING", "Request exceeded latency threshold"),
    }

    level, message = messages[scenario]

    return {
        "scenario": scenario,
        "logs": [
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": level,
                "message": message,
            }
        ],
    }


def check_response_time(scenario: str) -> dict:
    if scenario not in SCENARIOS:
        return {"error": "Unknown scenario"}

    healthy, latency, _ = SCENARIOS[scenario]

    if scenario == "database_down":
        return {
            "scenario": scenario,
            "response_time_ms": None,
            "threshold_ms": 1000,
            "within_threshold": None,
            "message": "Response time unavailable because the database is down.",
        }

    return {
        "scenario": scenario,
        "response_time_ms": latency,
        "threshold_ms": 1000,
        "within_threshold": latency <= 1000,
    }