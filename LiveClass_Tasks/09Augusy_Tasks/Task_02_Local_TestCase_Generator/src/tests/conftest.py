"""Shared pytest fixtures and sys.path setup so tests can import src modules."""

import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC_DIR))


@pytest.fixture
def minimal_env(tmp_path):
    """Create a .env file with minimal valid config and return its path."""
    env_path = tmp_path / ".env"
    env_path.write_text(
        "\n".join(
            [
                "JIRA_BASE_URL=https://example.atlassian.net",
                "JIRA_EMAIL=test@example.com",
                "JIRA_API_TOKEN=test-token",
                "LLM_PROVIDER=ollama",
                "OLLAMA_BASE_URL=http://localhost:11434",
                "OLLAMA_MODEL=gemma3:1b",
                "GROQ_API_KEY=test-groq",
                "GROQ_MODEL=llama-3.3-70b-versatile",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return env_path


@pytest.fixture
def sample_issue():
    """A normalized Jira issue dict as produced by JiraClient._normalize_issue."""
    return {
        "key": "PROJ-123",
        "self": "https://example.atlassian.net/rest/api/3/issue/123",
        "summary": "User login with password validation",
        "description": "Password must contain at least 8 characters.",
        "status": "In Progress",
        "priority": "High",
        "issuetype": "Story",
        "project": "PROJ",
        "labels": ["auth"],
        "components": ["Login"],
    }
