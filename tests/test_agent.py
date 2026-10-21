from types import SimpleNamespace
from unittest.mock import patch

from app.agent import investigate_incident


def fake_response(content="", tool_calls=None):
    return SimpleNamespace(
        message=SimpleNamespace(
            content=content,
            tool_calls=tool_calls or [],
        )
    )


def fake_tool_call(name):
    return SimpleNamespace(
        function=SimpleNamespace(
            name=name,
            arguments={"scenario": "database_down"},
        )
    )


@patch("app.agent.Client")
def test_agent_executes_all_tools(mock_client):
    mock_client.return_value.chat.side_effect = [
        fake_response(tool_calls=[
            fake_tool_call("check_service_health"),
            fake_tool_call("get_recent_logs"),
            fake_tool_call("check_response_time"),
        ]),
        fake_response(content="Investigation complete."),
    ]

    result = investigate_incident("database_down")

    assert set(result["tools_used"]) == {
        "check_service_health",
        "get_recent_logs",
        "check_response_time",
    }
    assert result["report"] == "Investigation complete."


@patch("app.agent.Client")
def test_agent_requests_missing_tools(mock_client):
    mock_client.return_value.chat.side_effect = [
        fake_response(tool_calls=[
            fake_tool_call("get_recent_logs"),
        ]),
        fake_response(content="Premature report."),
        fake_response(tool_calls=[
            fake_tool_call("check_service_health"),
            fake_tool_call("check_response_time"),
        ]),
        fake_response(content="Final report."),
    ]

    result = investigate_incident("database_down")

    assert result["report"] == "Final report."
    assert len(result["tools_used"]) == 3


@patch("app.agent.Client")
def test_agent_rejects_unknown_tool(mock_client):
    mock_client.return_value.chat.side_effect = [
        fake_response(tool_calls=[
            fake_tool_call("delete_database"),
        ]),
        fake_response(tool_calls=[
            fake_tool_call("check_service_health"),
            fake_tool_call("get_recent_logs"),
            fake_tool_call("check_response_time"),
        ]),
        fake_response(content="Investigation complete."),
    ]

    result = investigate_incident("database_down")

    assert "delete_database" not in result["tools_used"]


@patch("app.agent.Client")
def test_agent_stops_after_max_rounds(mock_client):
    mock_client.return_value.chat.return_value = fake_response(
        content="I need more information."
    )

    result = investigate_incident("database_down")

    assert "maximum tool-calling rounds reached" in result["report"]
    assert mock_client.return_value.chat.call_count == 5