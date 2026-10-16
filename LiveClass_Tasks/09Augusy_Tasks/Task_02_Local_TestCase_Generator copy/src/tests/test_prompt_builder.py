"""Tests for prompt building, issue key extraction, and markdown parsing."""

from prompt_builder import SYSTEM_PROMPT, build_prompt
from test_case_generator import extract_instructions, extract_issue_key
from utils import parse_markdown_table


def test_extract_issue_key():
    assert extract_issue_key("Create test cases for PROJ-123 please") == "PROJ-123"
    assert extract_issue_key("no key here") is None
    assert extract_issue_key("VWO-49 in lower case mention") == "VWO-49"


def test_extract_instructions_removes_key():
    assert extract_instructions("Create test cases for PROJ-123", "PROJ-123") == "Create test cases for"


def test_build_prompt_includes_jira_data(sample_issue):
    system, user = build_prompt(issue_data=sample_issue, user_request="Create functional test cases")
    assert "STRICT ANTI-HALLUCINATION POLICY" in system
    assert "Password must contain at least 8 characters." in user
    assert sample_issue["key"] in user
    # Credentials must never appear.
    assert "token" not in user.lower() or "jira_api_token" not in user.lower()


def test_build_prompt_mentions_missing_wording(sample_issue):
    _, user = build_prompt(issue_data=sample_issue, user_request="Anything")
    assert "Not specified in the Jira issue" in SYSTEM_PROMPT or "Not specified" in SYSTEM_PROMPT


def test_parse_markdown_table():
    md = (
        "| TC ID | Scenario |\n"
        "|---|---|\n"
        "| TC-001 | Login works |\n"
        "| TC-002 | Login fails |\n"
    )
    rows = parse_markdown_table(md)
    assert len(rows) == 2
    assert rows[0]["TC ID"] == "TC-001"
    assert rows[1]["Scenario"] == "Login fails"


def test_parse_markdown_table_empty_on_no_table():
    assert parse_markdown_table("no table here") == []
