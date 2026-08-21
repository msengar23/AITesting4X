"""LLM client supporting Ollama (primary) and Groq (fallback).

Uses the OpenAI-compatible SDK for both providers so there is a single
client code path. Provider/model availability is verified before any
generation attempt, and provider errors are mapped to friendly messages.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import requests
from openai import OpenAI

from errors import (
    LLMAuthError,
    LLMModelNotFoundError,
    LLMRateLimitError,
    LLMResponseError,
    LLMUnavailableError,
)

logger = logging.getLogger("tc_generator.llm")

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OLLAMA_DUMMY_KEY = "ollama"


@dataclass
class GenerationResult:
    text: str
    provider: str
    model: str


class LLMClient:
    """Generates chat completions via an OpenAI-compatible endpoint."""

    def __init__(self, provider: str, config: dict[str, str]) -> None:
        self.provider = provider.lower()
        if self.provider not in ("ollama", "groq"):
            raise ValueError(f"Unsupported provider: {provider}")

        self.model = config.get("OLLAMA_MODEL" if self.provider == "ollama" else "GROQ_MODEL", "")
        if self.provider == "ollama":
            base = (config.get("OLLAMA_BASE_URL") or "http://localhost:11434").rstrip("/")
            self.ollama_base = base
            self.client = OpenAI(base_url=f"{base}/v1", api_key=OLLAMA_DUMMY_KEY)
        else:
            api_key = config.get("GROQ_API_KEY", "")
            self.ollama_base = ""
            self.client = OpenAI(base_url=GROQ_BASE_URL, api_key=api_key)

    def verify_available(self) -> None:
        """Raise a friendly error if the provider/model is not usable."""
        if self.provider == "ollama":
            self._verify_ollama()
        else:
            self._verify_groq()

    def _verify_ollama(self) -> None:
        try:
            response = requests.get(f"{self.ollama_base}/api/tags", timeout=5)
        except requests.exceptions.RequestException as exc:
            raise LLMUnavailableError(
                "Ollama is not reachable. Make sure the Ollama service is running "
                f"at {self.ollama_base}."
            ) from exc

        if response.status_code >= 400:
            raise LLMUnavailableError(
                f"Ollama responded with HTTP {response.status_code}. Check the Ollama service."
            )

        try:
            models = response.json().get("models", [])
        except ValueError as exc:
            raise LLMUnavailableError("Ollama returned an unexpected response format.") from exc

        names = {m.get("name", "").split(":")[0] for m in models if isinstance(m, dict)}
        configured = self.model.split(":")[0]
        if self.model not in {m.get("name", "") for m in models if isinstance(m, dict)} and configured not in names:
            raise LLMModelNotFoundError(
                f"Model '{self.model}' is not installed in Ollama. "
                "Run `ollama pull gemma3:1b` or pick an installed model."
            )

    def _verify_groq(self) -> None:
        try:
            models = self.client.models.list()
        except Exception as exc:  # noqa: BLE001 - map any SDK error to friendly message
            message = str(exc)
            lowered = message.lower()
            if "authentication" in lowered or "401" in message or "invalid api key" in lowered:
                raise LLMAuthError("Groq authentication failed. Check your Groq API key.") from exc
            if "rate" in lowered or "429" in message:
                raise LLMRateLimitError("Groq rate limit exceeded. Please try again shortly.") from exc
            raise LLMUnavailableError("Groq is not reachable. Check your network connection.") from exc

        available = {m.id for m in getattr(models, "data", [])}
        if self.model not in available:
            raise LLMModelNotFoundError(
                f"Model '{self.model}' is not available on Groq. Pick an available model."
            )

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> GenerationResult:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
        except Exception as exc:  # noqa: BLE001
            message = str(exc)
            lowered = message.lower()
            if "model_not_found" in lowered or "model not found" in lowered:
                raise LLMModelNotFoundError(
                    f"Model '{self.model}' was not found on {self.provider}."
                ) from exc
            if "authentication" in lowered or "invalid api key" in lowered or "401" in message:
                raise LLMAuthError(f"{self.provider.capitalize()} authentication failed. Check the API key.") from exc
            if "rate" in lowered or "429" in message:
                raise LLMRateLimitError(
                    f"{self.provider.capitalize()} rate limit exceeded. Please try again shortly."
                ) from exc
            if self.provider == "ollama":
                raise LLMUnavailableError(
                    "Ollama failed during generation. Check that the service is running."
                ) from exc
            raise LLMUnavailableError("Groq failed during generation. Please try again.") from exc

        text = ""
        if completion and completion.choices:
            text = completion.choices[0].message.content or ""
        if not text.strip():
            raise LLMResponseError("The model returned an empty response. Please try again.")

        return GenerationResult(text=text.strip(), provider=self.provider, model=self.model)
