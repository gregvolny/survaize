from pathlib import Path
from typing import Protocol

from survaize.model.questionnaire import Questionnaire


class Reader(Protocol):
    """Protocol defining the interface for questionnaire readers."""

    def read(self, file_path: Path) -> Questionnaire:
        """Read a document and extract its content.

        Args:
            file_path: Path to the document file

        Returns:
            A Questionnaire containing the extracted content
        """
        ...
