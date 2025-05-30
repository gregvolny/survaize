import os
from dataclasses import dataclass
from enum import Enum


class OpenAIProviderType(Enum):
    OPENAI = "openai"
    AZURE = "azure"


@dataclass(frozen=True)
class LLMConfig:
    """Configuration for the OpenAI API."""

    api_key: str
    api_version: str | None
    api_url: str | None
    model: str
    provider: OpenAIProviderType = OpenAIProviderType.OPENAI


def create_llm_config_from_env() -> LLMConfig:
    """Create LLM config from environment variables.

    Returns:
        LLMConfig instance

    Raises:
        ValueError: If required environment variables are missing
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    api_provider = os.environ.get("OPENAI_PROVIDER", "openai")
    api_version = os.environ.get("OPENAI_API_VERSION")
    api_url = os.environ.get("OPENAI_API_URL")
    api_model = os.environ.get("OPENAI_API_MODEL", "gpt-4o")

    provider = OpenAIProviderType.AZURE if api_provider == "azure" else OpenAIProviderType.OPENAI

    if provider == OpenAIProviderType.AZURE:
        if not api_url:
            raise ValueError("OPENAI_API_URL environment variable is required for Azure provider")
        if not api_version:
            api_version = "2024-05-01-preview"

    return LLMConfig(
        api_key=api_key,
        api_version=api_version,
        api_url=api_url,
        model=api_model,
        provider=provider,
    )
