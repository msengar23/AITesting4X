"""Call Groq to draft the test plan, returning raw JSON text.

Implements architecture/SOP_generate_plan.md section 4. Uses `requests`
directly (the project does not depend on the openai SDK).
"""

from __future__ import annotations

import requests

from tools.config import Config
from tools.errors import (
    LLMAuthError,
    LLMModelNotFoundError,
    LLMRateLimitError,
    LLMResponseError,
    LLMUnavailableError,
)

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
TEMPERATURE = 0.2


def generate(
    config: Config,
    system_prompt: str,
    user_prompt: str,
    session: requests.Session | None = None,
) -> str:
    """Return the model's raw response text (expected to be a JSON object)."""
    http = session or requests.Session()
    payload = {
        "model": config.groq_model,
        "temperature": TEMPERATURE,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    try:
        response = http.post(
            GROQ_ENDPOINT,
            headers={
                "Authorization": f"Bearer {config.groq_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=max(config.timeout, 60),
        )
    except requests.exceptions.Timeout as exc:
        raise LLMUnavailableError(
            "Groq did not respond in time. Please try again."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise LLMUnavailableError(
            "Groq is not reachable. Check your network connection."
        ) from exc

    if response.status_code == 401:
        raise LLMAuthError("Groq authentication failed. Check your Groq API key.")
    if response.status_code == 429:
        raise LLMRateLimitError("Groq rate limit exceeded. Please try again shortly.")
    if response.status_code >= 400:
        body = response.text[:400].lower()
        if "model" in body and ("not found" in body or "does not exist" in body):
            raise LLMModelNotFoundError(
                f"Model '{config.groq_model}' is not available on Groq. Pick an available model."
            )
        raise LLMUnavailableError(
            f"Groq returned an unexpected error (HTTP {response.status_code})."
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise LLMUnavailableError("Groq returned an unexpected response format.") from exc

    text = ""
    choices = data.get("choices") or []
    if choices:
        text = (choices[0].get("message") or {}).get("content") or ""
    if not text.strip():
        raise LLMResponseError("The model returned an empty response. Please try again.")

    return text.strip()
