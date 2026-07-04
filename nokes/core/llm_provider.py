"""LLM provider abstractions"""

import os
from abc import ABC, abstractmethod
from typing import Optional
import openai
from anthropic import Anthropic
from loguru import logger


class LLMProvider(ABC):
    """Abstract base for LLM providers"""

    @abstractmethod
    async def generate(
        self, messages: list, max_tokens: int = 2000, temperature: float = 0.7
    ) -> str:
        """Generate text response"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""

    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        logger.info(f"OpenAI provider initialized with model: {model}")

    async def generate(
        self, messages: list, max_tokens: int = 2000, temperature: float = 0.7
    ) -> str:
        """Generate using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""

    def __init__(self, model: str = "claude-3-opus-20240229"):
        self.model = model
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        logger.info(f"Anthropic provider initialized with model: {model}")

    async def generate(
        self, messages: list, max_tokens: int = 2000, temperature: float = 0.7
    ) -> str:
        """Generate using Anthropic API"""
        try:
            # Convert to Anthropic format
            system = messages[0]["content"] if messages[0]["role"] == "system" else ""
            api_messages = messages[1:] if messages[0]["role"] == "system" else messages

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=api_messages,
                temperature=temperature,
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic generation error: {e}")
            raise


def get_llm_provider(provider: str = "openai", model: Optional[str] = None) -> LLMProvider:
    """Factory function to get LLM provider

    Args:
        provider: Provider name (openai, anthropic)
        model: Optional model override

    Returns:
        Initialized LLM provider
    """
    if provider.lower() == "openai":
        return OpenAIProvider(model or "gpt-4-turbo-preview")
    elif provider.lower() == "anthropic":
        return AnthropicProvider(model or "claude-3-opus-20240229")
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
