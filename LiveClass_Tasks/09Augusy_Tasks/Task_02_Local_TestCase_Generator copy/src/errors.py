"""Domain exceptions for the application with user-friendly messages.

Every exception carries a `message` that is safe to show in the UI and
never contains secrets, tokens, or sensitive response details.
"""


class AppError(Exception):
    """Base class for all application domain errors."""

    def __init__(self, message: str, *, detail: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail  # internal detail, never shown to the user


class ConfigError(AppError):
    """Configuration is missing or invalid."""


class JiraError(AppError):
    """Base class for Jira-related errors."""


class JiraAuthError(JiraError):
    """Jira authentication failed (HTTP 401)."""


class JiraPermissionError(JiraError):
    """Jira authorization failed (HTTP 403)."""


class JiraNotFoundError(JiraError):
    """Jira issue not found (HTTP 404)."""


class JiraTimeoutError(JiraError):
    """Jira request timed out."""


class JiraNetworkError(JiraError):
    """Jira network/connection failure."""


class JiraInvalidKeyError(JiraError):
    """The issue key format is invalid."""


class LLMError(AppError):
    """Base class for LLM-related errors."""


class LLMUnavailableError(LLMError):
    """The LLM service is not reachable."""


class LLMModelNotFoundError(LLMError):
    """The configured model is not available on the provider."""


class LLMAuthError(LLMError):
    """LLM provider authentication failed."""


class LLMRateLimitError(LLMError):
    """LLM provider rate limit exceeded."""


class LLMResponseError(LLMError):
    """The LLM returned an unexpected or unusable response."""


class GenerationError(AppError):
    """The end-to-end generation workflow failed."""
