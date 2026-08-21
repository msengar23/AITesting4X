"""Test case generator: end-to-end orchestration.

Pipeline: validate config -> extract issue key -> fetch Jira issue ->
verify LLM provider -> build grounded prompt -> generate -> parse result.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

from config_manager import ConfigManager
from errors import ConfigError, GenerationError
from jira_client import JiraClient
from llm_client import LLMClient, GenerationResult
from prompt_builder import build_prompt
from utils import parse_markdown_table

logger = logging.getLogger("tc_generator.generator")

ISSUE_KEY_IN_TEXT_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,9}-\d{1,6})\b")


@dataclass
class GenerationOutput:
    result: GenerationResult
    issue: dict
    table_rows: list[dict[str, str]] = field(default_factory=list)
    raw_markdown: str = ""


def extract_issue_key(user_message: str) -> str | None:
    """Return the first Jira issue key found in a natural-language message."""
    match = ISSUE_KEY_IN_TEXT_RE.search(user_message)
    return match.group(1) if match else None


def extract_instructions(user_message: str, issue_key: str | None) -> str:
    """Strip the issue key token from the message, leaving the instruction."""
    if not issue_key:
        return user_message.strip()
    return user_message.replace(issue_key, "").strip()


def generate(user_message: str, config: ConfigManager | None = None) -> GenerationOutput:
    """Generate test cases / test plan for the Jira issue in `user_message`."""
    config = config or ConfigManager()
    config.validate()

    issue_key = extract_issue_key(user_message)
    if not issue_key:
        raise GenerationError(
            "No Jira issue key found in your request. "
            "Include a key like PROJ-123, e.g. 'Create test cases for PROJ-123'."
        )

    instructions = extract_instructions(user_message, issue_key)
    if not instructions:
        instructions = "Create functional positive and negative test cases, boundary value analysis, "
        "equivalence partitioning, and security test cases relevant to the Jira issue."

    all_config = config.get_all()
    provider = config.provider()

    logger.info("Fetching Jira issue %s", issue_key)
    jira = JiraClient(
        base_url=all_config["JIRA_BASE_URL"],
        email=all_config["JIRA_EMAIL"],
        api_token=all_config["JIRA_API_TOKEN"],
    )
    issue = jira.get_issue(issue_key)

    logger.info("Verifying %s availability", provider)
    llm = LLMClient(provider=provider, config=all_config)
    llm.verify_available()

    system_prompt, user_prompt = build_prompt(issue_data=issue, user_request=instructions)
    logger.info("Generating with %s", provider)
    result = llm.generate(system_prompt=system_prompt, user_prompt=user_prompt)

    rows = parse_markdown_table(result.text)
    return GenerationOutput(
        result=result,
        issue=issue,
        table_rows=rows,
        raw_markdown=result.text,
    )
