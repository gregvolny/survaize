import json
import os
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path

from openai import AzureOpenAI, OpenAI
from openai.types.chat import ChatCompletion

from survaize.config.llm_config import LLMConfig, OpenAIProviderType


class RecordingMode(Enum):
    """Mode for the :class:`RecordingClient`."""

    OFF = "off"
    RECORD = "record"
    REPLAY = "replay"


class _RecordingCompletions:
    _client: AzureOpenAI | OpenAI
    _mode: RecordingMode
    _directory: Path
    _counter: list[int]

    def __init__(self, client: AzureOpenAI | OpenAI, mode: RecordingMode, directory: Path, counter: list[int]) -> None:
        self._client = client
        self._mode = mode
        self._directory = directory
        self._counter = counter

    def create(self, *args: object, **kwargs: object) -> ChatCompletion:
        self._counter[0] += 1
        file_path = self._directory / f"{self._counter[0]:03d}.json"
        if self._mode is RecordingMode.REPLAY:
            with open(file_path) as f:
                data = json.load(f)
            return ChatCompletion.model_validate(data["response"])
        response = self._client.chat.completions.create(*args, **kwargs)
        if self._mode is RecordingMode.RECORD:
            self._directory.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w") as f:
                json.dump(
                    {"request": {"args": args, "kwargs": kwargs}, "response": response.model_dump()},
                    f,
                    indent=2,
                )
        return response


class _RecordingChat:
    completions: _RecordingCompletions

    def __init__(self, client: AzureOpenAI | OpenAI, mode: RecordingMode, directory: Path, counter: list[int]) -> None:
        self.completions = _RecordingCompletions(client, mode, directory, counter)


class RecordingClient:
    """OpenAI client wrapper that records or replays chat completions."""

    _client: AzureOpenAI | OpenAI
    _mode: RecordingMode
    _base_directory: Path
    _directory: Path
    _counter: list[int]
    chat: _RecordingChat

    def __init__(self, client: AzureOpenAI | OpenAI, mode: RecordingMode, directory: Path) -> None:
        self._client = client
        self._mode = mode
        self._base_directory = directory
        if mode is RecordingMode.RECORD:
            self._directory = directory / datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
        else:
            self._directory = directory
        self._counter = [0]
        self.chat = _RecordingChat(client, mode, self._directory, self._counter)

    def __getattr__(self, item: str) -> object:  # pragma: no cover - passthrough
        return getattr(self._client, item)


def create_openai_client(llm_config: LLMConfig) -> AzureOpenAI | OpenAI | RecordingClient:
    """Create an OpenAI client optionally wrapped for recording or replay."""
    if llm_config.provider == OpenAIProviderType.AZURE:
        assert llm_config.api_url is not None
        client: AzureOpenAI | OpenAI = AzureOpenAI(
            api_key=llm_config.api_key,
            api_version=llm_config.api_version,
            azure_endpoint=llm_config.api_url,
        )
    else:
        client = OpenAI(api_key=llm_config.api_key, base_url=llm_config.api_url)

    mode_str = os.environ.get("OPENAI_RECORDING_MODE", "off").lower()
    try:
        mode = RecordingMode(mode_str)
    except ValueError:  # pragma: no cover - invalid mode falls back to off
        mode = RecordingMode.OFF
    directory = Path(os.environ.get("OPENAI_RECORDING_DIR", "openai_records"))
    if mode is not RecordingMode.OFF:
        return RecordingClient(client, mode, directory)
    return client
