from pathlib import Path
from typing import Protocol

from survaize.model.questionnaire import Questionnaire


class Writer(Protocol):
    """Protocol defining the interface for writing questionnaires to disk in various formats."""

    def write(self, questionnaire: Questionnaire, output_path: Path):
        """Write a questionnaire to a file.

        Args:
            questionnaire: The structured questionnaire data
            output_path: Path where the questionnaire should be saved
        """
        ...
