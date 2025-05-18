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
