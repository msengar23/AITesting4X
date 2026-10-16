"""Utility helpers: secret-redacting logging and markdown table parsing."""

from __future__ import annotations

import logging
import re
from pathlib import Path

# Keys whose values must never appear in logs.
_SECRET_KEYS = (
    "JIRA_API_TOKEN",
    "TESR_CASE_GENERATOR_TOKEN",
    "LOCAL_TC_GENERATOR_KEY",
    "GROQ_API_KEY",
    "AUTHORIZATION",
)


class SecretRedactionFilter(logging.Filter):
    """Redacts known secret values and Authorization headers from log records."""

    def __init__(self, secrets: dict[str, str] | None = None) -> None:
        super().__init__()
        self._patterns: list[re.Pattern[str]] = []
        for key, value in (secrets or {}).items():
            if not value:
                continue
            upper = key.upper()
            if any(s in upper for s in ("TOKEN", "KEY", "SECRET", "AUTH")):
                self._patterns.append(re.compile(re.escape(value), re.IGNORECASE))

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for pattern in self._patterns:
            msg = pattern.sub("[REDACTED]", msg)
        # Redact Authorization headers generically.
        msg = re.sub(r"(Authorization:\s*)(\S+)", r"\1[REDACTED]", msg)
        record.msg = msg
        record.args = ()
        return True


def setup_logging(env_path: Path | None = None, secrets: dict[str, str] | None = None) -> logging.Logger:
    """Configure application logging with secret redaction.

    Returns the root application logger. Logs go to stdout and to a
    `logs/app.log` file next to the caller-provided env_path (or cwd).
    """
    logger = logging.getLogger("tc_generator")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if env_path is not None:
        log_dir = env_path.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    redaction = SecretRedactionFilter(secrets)
    for handler in logger.handlers:
        handler.addFilter(redaction)
    logger.propagate = False
    return logger


def mask_secret(value: str | None) -> str:
    """Return a masked display form of a secret, e.g. 'abc***xyz'."""
    if not value:
        return ""
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


def parse_markdown_table(markdown: str) -> list[dict[str, str]]:
    """Parse the first markdown table in `markdown` into a list of dicts.

    Returns a list of row dicts keyed by header. Returns an empty list if
    no table with a separator row is found.
    """
    lines = [ln.strip() for ln in markdown.splitlines() if ln.strip()]
    header_index = -1
    for i, line in enumerate(lines[:-1]):
        if "|" not in line:
            continue
        if re.match(r"^[\s|:\-]+$", lines[i + 1]) and "|" in lines[i + 1]:
            header_index = i
            break
    if header_index == -1:
        return []

    headers = [cell.strip() for cell in lines[header_index].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[header_index + 2 :]:
        if "|" not in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 1 and not cells[0]:
            continue
        row = {}
        for idx, header in enumerate(headers):
            row[header] = cells[idx].strip() if idx < len(cells) else ""
        rows.append(row)
    return rows
