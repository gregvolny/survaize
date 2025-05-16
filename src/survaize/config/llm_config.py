from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    """Configuration for the OpenAI API."""

    api_key: str
    api_version: str
    api_url: str
    api_deployment: str
