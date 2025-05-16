from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass(frozen=True)
class ScannedQuestionnaire:
    """Images and OCR text from a paper questionnaire."""

    pages: list[Image.Image]
    extracted_text: list[str]
    source_path: Path
