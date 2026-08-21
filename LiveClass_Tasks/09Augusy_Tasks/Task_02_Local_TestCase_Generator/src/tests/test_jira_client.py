"""Tests for JiraClient (HTTP mocked)."""

import pytest
import requests

from errors import JiraAuthError, JiraInvalidKeyError, JiraNotFoundError
from jira_client import JiraClient


def _client():
    return JiraClient("https://example.atlassian.net", "u@example.com", "tok")


def _issue_payload():
    return {
        "key": "PROJ-123",
        "fields": {
            "summary": "Login page",
            "description": {
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": "Password must be 8 chars."}],
                    }
                ],
            },
            "status": {"name": "In Progress"},
            "priority": {"name": "High"},
            "issuetype": {"name": "Story"},
            "project": {"name": "PROJ"},
            "labels": ["auth"],
            "components": [{"name": "Login"}],
            "reporter": {"displayName": "Jane"},
        },
    }


def test_get_issue_normalizes_fields(monkeypatch):
    client = _client()
    monkeypatch.setattr(client.session, "get", lambda url, timeout: _fake_response(200, _issue_payload()))
    issue = client.get_issue("PROJ-123")
    assert issue["key"] == "PROJ-123"
    assert issue["summary"] == "Login page"
    assert issue["description"] == "Password must be 8 chars."
    assert issue["status"] == "In Progress"
    assert issue["labels"] == ["auth"]


def test_get_issue_invalid_key():
    with pytest.raises(JiraInvalidKeyError):
        _client().get_issue("123-ABC")


def test_get_issue_401_maps_to_auth_error(monkeypatch):
    client = _client()
    monkeypatch.setattr(client.session, "get", lambda url, timeout: _fake_response(401, {}))
    with pytest.raises(JiraAuthError):
        client.get_issue("PROJ-123")


def test_get_issue_404_maps_to_not_found(monkeypatch):
    client = _client()
    monkeypatch.setattr(client.session, "get", lambda url, timeout: _fake_response(404, {}))
    with pytest.raises(JiraNotFoundError):
        client.get_issue("PROJ-123")


def test_get_issue_network_error(monkeypatch):
    client = _client()
    def boom(url, timeout):
        raise requests.exceptions.ConnectionError("refused")
    monkeypatch.setattr(client.session, "get", boom)
    from errors import JiraNetworkError
    with pytest.raises(JiraNetworkError):
        client.get_issue("PROJ-123")


def test_flatten_adf_handles_nested_lists():
    payload = {
        "key": "P-1",
        "fields": {
            "description": {
                "type": "doc",
                "content": [
                    {
                        "type": "bulletList",
                        "content": [
                            {
                                "type": "listItem",
                                "content": [
                                    {"type": "paragraph", "content": [{"type": "text", "text": "One"}]}
                                ],
                            }
                        ],
                    }
                ],
            }
        },
    }
    client = _client()
    issue = client._normalize_issue(payload)
    assert "One" in issue["description"]


def _fake_response(status_code, json_data):
    sc = status_code

    class FakeResponse:
        status_code = sc

        def json(self):
            return json_data

        @property
        def text(self):
            return str(json_data)

        def __repr__(self):
            return f"FakeResponse(status_code={sc})"

    return FakeResponse()
