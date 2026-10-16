"""Tests for ConfigManager."""

from config_manager import ConfigManager
from errors import ConfigError


def test_loads_values_from_env(minimal_env):
    cm = ConfigManager(env_path=minimal_env)
    assert cm.get("JIRA_BASE_URL") == "https://example.atlassian.net"
    assert cm.get("JIRA_EMAIL") == "test@example.com"
    assert cm.get("JIRA_API_TOKEN") == "test-token"
    assert cm.get("LLM_PROVIDER") == "ollama"


def test_defaults_applied_when_missing(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text("JIRA_EMAIL=x@y.z\n", encoding="utf-8")
    cm = ConfigManager(env_path=env_path)
    assert cm.get("OLLAMA_MODEL") == "gemma3:1b"
    assert cm.get("LLM_PROVIDER") == "ollama"


def test_legacy_alias_mapping(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text(
        "\n".join(
            [
                "Tesr_Case_Generator_Token=alias-token",
                "Local_TC_Generator_key=alias-groq",
            ]
        ),
        encoding="utf-8",
    )
    cm = ConfigManager(env_path=env_path)
    assert cm.get("JIRA_API_TOKEN") == "alias-token"
    assert cm.get("GROQ_API_KEY") == "alias-groq"


def test_validate_raises_when_incomplete(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text("JIRA_BASE_URL=https://x.atlassian.net\n", encoding="utf-8")
    cm = ConfigManager(env_path=env_path)
    try:
        cm.validate()
        assert False, "expected ConfigError"
    except ConfigError as exc:
        assert "Jira Email" in exc.message


def test_validate_passes_when_complete(minimal_env):
    cm = ConfigManager(env_path=minimal_env)
    cm.validate()  # should not raise


def test_save_writes_updates(minimal_env):
    cm = ConfigManager(env_path=minimal_env)
    cm.save({"JIRA_EMAIL": "new@example.com"})
    assert cm.get("JIRA_EMAIL") == "new@example.com"


def test_save_syncs_legacy_alias_for_token(minimal_env):
    cm = ConfigManager(env_path=minimal_env)
    cm.save({"JIRA_API_TOKEN": "brand-new-token"})
    assert cm.get("JIRA_API_TOKEN") == "brand-new-token"
    # Legacy alias stays in sync so older tooling still works.
    content = minimal_env.read_text(encoding="utf-8")
    assert "Tesr_Case_Generator_Token=brand-new-token" in content


def test_is_configured_for_groq_requires_key(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text("GROQ_MODEL=llama\n", encoding="utf-8")
    cm = ConfigManager(env_path=env_path)
    assert not cm.is_configured("groq")
