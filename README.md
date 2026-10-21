
# AI IT Incident Assistant

A small portfolio project exploring AI agent workflows,
diagnostic tools, and IT incident investigation.

## Current features

- FastAPI application
- Health endpoint
- Simulated IT incident scenarios
- Automated tests

## Planned features

- Read-only diagnostic tools
- Ollama AI agent with tool calling
- Evidence-based incident reports
- Evaluation tests
- Docker and CI/CD

## Run locally

Install dependencies:

    pip install -r requirements.txt

Start the API:

    python -m uvicorn app.main:app --reload

Open:

    http://127.0.0.1:8000/docs

## Tests

    python -m pytest -q

## Note

All incident scenarios are simulated.
This project does not monitor or modify real infrastructure.
