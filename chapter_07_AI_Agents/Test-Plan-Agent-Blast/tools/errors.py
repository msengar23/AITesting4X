"""Domain exception taxonomy for the Test Plan Agent.

Every exception carries a `message` that is safe to display to the user:
no secrets, no tokens, no raw response bodies, no stack traces. Internal
detail may be attached via `detail` and is never shown.
"""

from __future__ import annotations


class AppError(Exception):
    """Base class for all application domain errors."""

    def __init__(self, message: str, *, detail: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail


class ConfigError(AppError):
    """Configuration is missing or invalid."""


class JiraError(AppError):
    """Base class for Jira-related errors."""


class JiraInvalidKeyError(JiraError):
    """The issue key format is invalid."""


class JiraAuthError(JiraError):
    """Jira authentication failed (HTTP 401)."""


class JiraPermissionError(JiraError):
    """Jira authorization failed (HTTP 403)."""


class JiraNotFoundError(JiraError):
    """Jira issue not found (HTTP 404)."""


class JiraTimeoutError(JiraError):
    """Jira request timed out."""


class JiraNetworkError(JiraError):
    """Jira network or connection failure."""


class LLMError(AppError):
    """Base class for LLM-related errors."""


class LLMAuthError(LLMError):
    """LLM provider authentication failed."""


class LLMRateLimitError(LLMError):
    """LLM provider rate limit exceeded."""


class LLMModelNotFoundError(LLMError):
    """The configured model is not available on the provider."""


class LLMUnavailableError(LLMError):
    """The LLM service is not reachable."""


class LLMResponseError(LLMError):
    """The LLM returned an empty or unusable response."""


class PlanValidationError(AppError):
    """The model returned a test plan that failed schema or coverage validation."""
