
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Incident Assistant")

Scenario = Literal["healthy", "database_down", "high_latency"]


class IncidentStatus(BaseModel):
    scenario: Scenario
    healthy: bool
    response_time_ms: int
    message: str


# Simulated data — not real infrastructure monitoring.
SCENARIOS = {
    "healthy": (
        True,
        45,
        "Service is operating normally",
    ),
    "database_down": (
        False,
        0,
        "Database connection unavailable",
    ),
    "high_latency": (
        False,
        2500,
        "Response time exceeds threshold",
    ),
}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-incident-assistant",
    }


@app.get("/status/{scenario}", response_model=IncidentStatus)
def get_status(scenario: Scenario):
    healthy, latency, message = SCENARIOS[scenario]

    return IncidentStatus(
        scenario=scenario,
        healthy=healthy,
        response_time_ms=latency,
        message=message,
    )

@app.get("/investigate/{scenario}")
def investigate(scenario: Scenario):
    from app.agent import investigate_incident

    return investigate_incident(scenario)
