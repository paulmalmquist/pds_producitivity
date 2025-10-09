"""LLM provider abstraction."""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Dict

import httpx

from app.config import get_settings


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> Dict[str, Any]:
        """Return parsed JSON from the model."""


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.openai_api_key
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        self.model = settings.llm_model
        self.timeout = settings.llm_timeout

    def complete(self, prompt: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful data analytics assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
        }
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)


class AnthropicProvider(LLMProvider):
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.anthropic_api_key
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not configured")
        self.model = settings.llm_model
        self.timeout = settings.llm_timeout

    def complete(self, prompt: str) -> Dict[str, Any]:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
        payload = {
            "model": self.model,
            "max_tokens": 800,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
        }
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content = "".join(block.get("text", "") for block in data.get("content", []))
        return json.loads(content)


def get_provider() -> LLMProvider:
    settings = get_settings()
    provider = settings.llm_provider.lower()
    if provider == "openai":
        return OpenAIProvider()
    if provider == "anthropic":
        return AnthropicProvider()
    raise ValueError(f"Unsupported LLM provider: {provider}")


__all__ = ["LLMProvider", "OpenAIProvider", "AnthropicProvider", "get_provider"]
