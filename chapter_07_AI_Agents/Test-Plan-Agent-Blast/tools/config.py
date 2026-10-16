"""Configuration loader for the Test Plan Agent.

Reads credentials from the project `.env` file only. Secrets are never
printed, logged, or included in prompts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

from tools.errors import ConfigError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENV_PATH = PROJECT_ROOT / ".env"

REQUIRED_KEYS = ("JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "GROQ_API_KEY", "GROQ_MODEL")
SECRET_KEYS = ("JIRA_API_TOKEN", "GROQ_API_KEY")

DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"
DEFAULT_TIMEOUT = 15


@dataclass(frozen=True)
class Config:
    """Validated application configuration."""

    jira_url: str
    jira_email: str
    jira_api_token: str
    groq_api_key: str
    groq_model: str
    jira_ac_field: str = ""
    timeout: int = DEFAULT_TIMEOUT
    env_path: Path = DEFAULT_ENV_PATH

    def masked(self) -> dict[str, str]:
        """Safe-to-display view: every secret replaced with a placeholder."""
        data = {
            "JIRA_URL": self.jira_url,
            "JIRA_EMAIL": self.jira_email,
            "JIRA_API_TOKEN": self.jira_api_token,
            "GROQ_API_KEY": self.groq_api_key,
            "GROQ_MODEL": self.groq_model,
            "JIRA_AC_FIELD": self.jira_ac_field,
        }
        return {
            key: ("***set***" if key in SECRET_KEYS and value else value)
            for key, value in data.items()
        }


def _read_env(env_path: Path) -> dict[str, str]:
    if not env_path.exists():
        raise ConfigError(
            f"Configuration file not found at {env_path}. "
            "Copy .env.example to .env and fill in your credentials."
        )
    raw = dotenv_values(env_path)
    return {key: (value or "").strip() for key, value in raw.items()}


def load_config(env_path: Path | None = None) -> Config:
    """Load and validate configuration from `.env`."""
    path = env_path or DEFAULT_ENV_PATH
    values = _read_env(path)

    missing = [key for key in REQUIRED_KEYS if not values.get(key)]
    if missing:
        labels = ", ".join(missing)
        raise ConfigError(
            f"Configuration is incomplete. Missing: {labels}. "
            "Fill these in your .env file."
        )

    return Config(
        jira_url=values["JIRA_URL"].rstrip("/"),
        jira_email=values["JIRA_EMAIL"],
        jira_api_token=values["JIRA_API_TOKEN"],
        groq_api_key=values["GROQ_API_KEY"],
        groq_model=values.get("GROQ_MODEL") or DEFAULT_GROQ_MODEL,
        jira_ac_field=values.get("JIRA_AC_FIELD", ""),
        env_path=path,
    )
