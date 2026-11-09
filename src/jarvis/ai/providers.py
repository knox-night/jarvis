from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from google import genai


class AIProvider(ABC):
    @abstractmethod
    def generate_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Return a response for the given user message and optional context."""


class MockAIProvider(AIProvider):
    def generate_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        context_summary = ""
        if context:
            memories = context.get("memory", [])
            if memories:
                context_summary = " I also remember: " + "; ".join(memories[-3:])

        return (
            f"JARVIS mock response: I heard: '{message}'. "
            f"This is a placeholder for the real cloud AI provider.{context_summary}"
        )


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str):
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not configured. Set it in your environment or switch providers.")
        self.client = genai.Client(api_key=api_key)

    def generate_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        prompt = ""
        if context:
            memories = context.get("memory", [])
            if memories:
                prompt = "Relevant memories:\n" + "\n".join(f"- {item}" for item in memories[-3:]) + "\n\n"

        prompt += f"User message:\n{message}"
        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text


def create_provider(provider_name: str, api_key: str = "") -> AIProvider:
    provider_name = (provider_name or "mock").lower()
    if provider_name == "gemini":
        return GeminiProvider(api_key)
    if provider_name == "mock":
        return MockAIProvider()

    raise ValueError(f"Unsupported AI provider: {provider_name}")
