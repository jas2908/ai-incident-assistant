from app.diagnostics import (
    check_service_health,
    get_recent_logs,
    check_response_time,
)


def build_incident_report(scenario: str) -> dict:
    """Build a structured report from simulated diagnostic evidence."""

    health = check_service_health(scenario)
    logs = get_recent_logs(scenario)
    latency = check_response_time(scenario)

    if "error" in health:
        raise ValueError("Unknown incident scenario")

    if scenario == "database_down":
        likely_cause = (
            "Database connectivity failure. The simulated logs "
            "report that the database connection was refused."
        )
        actions = [
            "Check whether the database service is running.",
            "Verify database connection settings.",
            "Investigate network connectivity and database logs.",
        ]
    elif scenario == "high_latency":
        likely_cause = (
            "The service is responding more slowly than the configured threshold. "
            "The underlying reason is not yet confirmed."
        )
        actions = [
            "Check CPU and memory usage.",
            "Investigate slow database queries.",
            "Review application performance metrics.",
        ]
    else:
        likely_cause = "No incident detected."
        actions = ["Continue monitoring the service."]

    return {
        "scenario": scenario,
        "incident_summary": health["message"],
        "evidence": {
            "health": health,
            "logs": logs["logs"],
            "response_time": latency,
        },
        "likely_cause": likely_cause,
        "recommended_actions": actions,
        "incident_start_time": None,
    }