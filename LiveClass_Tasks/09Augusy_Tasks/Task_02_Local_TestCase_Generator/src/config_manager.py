"""Configuration manager: loads and saves .env credentials.

Primary source of truth is the `.env` file next to the app. The manager
supports both canonical keys (JIRA_API_TOKEN, GROQ_API_KEY) and the
legacy alias keys that appeared in earlier versions of the user's .env
(Tesr_Case_Generator_Token, Local_TC_Generator_key).
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import dotenv_values, set_key

from errors import ConfigError

# Legacy alias keys -> canonical keys.
_ALIASES = {
    "TESR_CASE_GENERATOR_TOKEN": "JIRA_API_TOKEN",
    "LOCAL_TC_GENERATOR_KEY": "GROQ_API_KEY",
}

# Canonical keys that must never be printed.
SECRET_KEYS = ("JIRA_API_TOKEN", "GROQ_API_KEY")

DEFAULTS = {
    "LLM_PROVIDER": "ollama",
    "OLLAMA_BASE_URL": "http://localhost:11434",
    "OLLAMA_MODEL": "gemma3:1b",
    "GROQ_MODEL": "llama-3.3-70b-versatile",
}

_ALLOWED_PROVIDERS = ("ollama", "groq")


def default_env_path() -> Path:
    """Path to the .env file next to this module (src/.env)."""
    return Path(__file__).resolve().parent / ".env"


def _canonicalize(raw: dict[str, str]) -> dict[str, str]:
    """Map legacy alias keys to canonical keys and strip whitespace."""
    result: dict[str, str] = {}
    for key, value in raw.items():
        if value is None:
            continue
        stripped = str(value).strip()
        upper = key.upper()
        canonical = _ALIASES.get(upper, key)
        result[canonical] = stripped
    return result


class ConfigManager:
    """Reads and writes application configuration from a .env file."""

    def __init__(self, env_path: Path | None = None) -> None:
        self.env_path = env_path or default_env_path()
        self._data: dict[str, str] = {}
        self.reload()

    def reload(self) -> None:
        if self.env_path.exists():
            raw = dotenv_values(self.env_path)
        else:
            raw = {}
        self._data = _canonicalize(raw)

    def get(self, key: str) -> str:
        """Return a config value or an empty string if unset."""
        value = self._data.get(key, "")
        return value or DEFAULTS.get(key, "")

    def get_all(self) -> dict[str, str]:
        return {key: self.get(key) for key in DEFAULTS} | {
            key: self.get(key) for key in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "GROQ_API_KEY")
        }

    def is_configured(self, provider: str) -> bool:
        if provider == "groq":
            return bool(self.get("GROQ_API_KEY") and self.get("GROQ_MODEL"))
        return bool(self.get("OLLAMA_BASE_URL") and self.get("OLLAMA_MODEL"))

    def validate(self) -> None:
        """Raise ConfigError if required configuration is missing/invalid."""
        missing = []
        if not self.get("JIRA_BASE_URL"):
            missing.append("Jira Base URL")
        if not self.get("JIRA_EMAIL"):
            missing.append("Jira Email")
        if not self.get("JIRA_API_TOKEN"):
            missing.append("Jira API Token")

        provider = self.get("LLM_PROVIDER").lower()
        if provider not in _ALLOWED_PROVIDERS:
            raise ConfigError(
                f"Invalid LLM_PROVIDER '{provider}'. Choose 'ollama' or 'groq'."
            )
        if not self.is_configured(provider):
            if provider == "groq":
                missing.append("Groq API Key (and model)")
            else:
                missing.append("Ollama URL / model")

        if missing:
            raise ConfigError(
                "Configuration is incomplete. Missing: " + ", ".join(missing) + "."
            )

    def provider(self) -> str:
        return self.get("LLM_PROVIDER").lower()

    def save(self, updates: dict[str, str]) -> None:
        """Write updates into the .env file atomically (via dotenv set_key)."""
        self.env_path.parent.mkdir(parents=True, exist_ok=True)
        for key, value in updates.items():
            if value is None:
                continue
            set_key(str(self.env_path), key, str(value).strip(), quote_mode="never")

        # Also keep legacy aliases in sync so older tooling still works.
        synced: dict[str, str] = {}
        if "JIRA_API_TOKEN" in updates:
            synced["Tesr_Case_Generator_Token"] = str(updates["JIRA_API_TOKEN"]).strip()
        if "GROQ_API_KEY" in updates:
            synced["Local_TC_Generator_key"] = str(updates["GROQ_API_KEY"]).strip()
        for key, value in synced.items():
            set_key(str(self.env_path), key, value, quote_mode="never")

        self.reload()


# Module-level convenience instance pointing at src/.env.
manager = ConfigManager()

# Load values into the process environment so other libraries (e.g. the
# OpenAI SDK) can pick them up from os.environ if needed.
for _key, _value in manager.get_all().items():
    if _value and _key in SECRET_KEYS and not os.environ.get(_key):
        os.environ[_key] = _value
