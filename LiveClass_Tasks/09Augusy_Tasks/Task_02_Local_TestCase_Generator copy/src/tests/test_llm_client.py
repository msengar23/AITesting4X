"""Tests for LLMClient (network mocked)."""

from unittest.mock import MagicMock

import pytest

from errors import LLMAuthError, LLMModelNotFoundError, LLMUnavailableError
from llm_client import LLMClient

OLLAMA_CONFIG = {
    "OLLAMA_BASE_URL": "http://localhost:11434",
    "OLLAMA_MODEL": "gemma3:1b",
    "GROQ_API_KEY": "gsk-test",
    "GROQ_MODEL": "llama-3.3-70b-versatile",
}


def test_ollama_client_builds_correct_base_url():
    client = LLMClient("ollama", OLLAMA_CONFIG)
    assert str(client.client.base_url).rstrip("/").endswith("/v1")


def test_groq_client_builds_correct_base_url():
    client = LLMClient("groq", OLLAMA_CONFIG)
    assert "groq.com" in str(client.client.base_url)


def test_verify_ollama_ok(monkeypatch):
    client = LLMClient("ollama", OLLAMA_CONFIG)

    class FakeResponse:
        status_code = 200

        def json(self):
            return {"models": [{"name": "gemma3:1b"}]}

    monkeypatch.setattr("llm_client.requests.get", lambda url, timeout: FakeResponse())
    client.verify_available()  # should not raise


def test_verify_ollama_missing_model(monkeypatch):
    client = LLMClient("ollama", OLLAMA_CONFIG)

    class FakeResponse:
        status_code = 200

        def json(self):
            return {"models": [{"name": "llama3.2:1b"}]}

    monkeypatch.setattr("llm_client.requests.get", lambda url, timeout: FakeResponse())
    with pytest.raises(LLMModelNotFoundError):
        client.verify_available()


def test_verify_ollama_unreachable(monkeypatch):
    import requests as real_requests

    client = LLMClient("ollama", OLLAMA_CONFIG)

    def boom(url, timeout):
        raise real_requests.exceptions.ConnectionError("refused")

    monkeypatch.setattr("llm_client.requests.get", boom)
    with pytest.raises(LLMUnavailableError):
        client.verify_available()


def test_verify_groq_auth_error():
    client = LLMClient("groq", OLLAMA_CONFIG)
    fake_models = MagicMock()
    fake_models.list.side_effect = Exception("AuthenticationError 401 invalid api key")
    client.client.models = fake_models
    with pytest.raises(LLMAuthError):
        client.verify_available()


def test_generate_returns_text():
    client = LLMClient("ollama", OLLAMA_CONFIG)
    fake_completion = MagicMock()
    fake_completion.choices = [MagicMock(message=MagicMock(content="| TC ID |\n|---|---|\n| TC-001 | x |"))]
    client.client.chat.completions.create = MagicMock(return_value=fake_completion)

    result = client.generate("system", "user")
    assert result.provider == "ollama"
    assert result.model == "gemma3:1b"
    assert "TC-001" in result.text


def test_generate_empty_response_raises():
    client = LLMClient("ollama", OLLAMA_CONFIG)
    fake_completion = MagicMock()
    fake_completion.choices = [MagicMock(message=MagicMock(content="   "))]
    client.client.chat.completions.create = MagicMock(return_value=fake_completion)
    from errors import LLMResponseError
    with pytest.raises(LLMResponseError):
        client.generate("system", "user")
