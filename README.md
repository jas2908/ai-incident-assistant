# AI Incident Assistant

A small backend project that uses a local language model to investigate simulated IT incidents.

I built this project to explore how AI agents can use tools to gather information instead of relying only on what a model already knows. The idea is simple: when something goes wrong with a service, the assistant checks the available diagnostic information and uses it to help explain what might be happening.

The project is built with Python, FastAPI, Ollama, and Llama 3.1.

## How it works

The application currently supports three simulated scenarios:

- `healthy` – the service is running normally
- `database_down` – the application cannot connect to its database
- `high_latency` – the service is responding more slowly than expected

When an investigation starts, the AI agent can call three diagnostic functions:

- `check_service_health` – checks the simulated service status
- `get_recent_logs` – retrieves simulated application logs
- `check_response_time` – checks response time against a threshold

The agent receives the results of these checks and uses them to generate an investigation summary.

I also added a separate report builder that produces a consistent JSON report with the available evidence, a likely cause, and suggested next steps. This makes the output easier to use from other applications, even when the AI-generated explanation varies.

## Tech stack

- **Python** – application logic and diagnostic functions
- **FastAPI** – REST API and interactive documentation
- **Ollama + Llama 3.1 (8B)** – local AI model with tool calling
- **Pydantic** – API data validation
- **pytest** – automated tests
- **Git** – version control

## Getting started

I developed and tested the project using Ubuntu on WSL, but it should also work in other environments where Python and Ollama are available.

You'll need Python 3.11 or newer and a working Ollama installation.

### 1. Clone the project

```bash
git clone https://github.com/jas2908/ai-incident-assistant.git
cd ai-incident-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the AI model

Download Llama 3.1 through Ollama:

```bash
ollama pull llama3.1:8b
```

Make sure Ollama is running. If it isn't already running as a service, start it with:

```bash
ollama serve
```

### 5. Start the API

```bash
python -m uvicorn app.main:app --reload
```

The API documentation is available at:

http://localhost:8000/docs

You can try the endpoints directly from Swagger UI.

## API endpoints

| Endpoint | What it does |
|---|---|
| `GET /health` | Checks whether the API is running |
| `GET /status/{scenario}` | Returns the simulated service status |
| `GET /investigate/{scenario}` | Runs an AI investigation using diagnostic tools |
| `GET /report/{scenario}` | Generates a structured incident report |
| `GET /analyze/{scenario}` | Runs the AI investigation and returns a structured report |

For example, to investigate a slow service:

```bash
curl http://localhost:8000/analyze/high_latency
```

Or to get just the structured report:

```bash
curl http://localhost:8000/report/high_latency
```

In the high-latency scenario, the simulated response time is 2,500 ms, compared with a threshold of 1,000 ms. The report includes that measurement and suggests areas to investigate further.

## Testing

The project includes tests for the API, diagnostic functions, report generation, and agent behavior.

Run them with:

```bash
python -m pytest -q
```

For the agent tests, I use mocked Ollama responses. This lets me test how the application handles tool calls without needing to run the language model for every test.


