import json
from pathlib import Path

from survaize.model.questionnaire import Questionnaire


class JSONReader:
    """Read questionnaire from JSON file (Survaize JSON schema)."""

    def read(self, file_path: Path) -> Questionnaire:
        """Read a document and extract its content.

        Args:
            file_path: Path to the document file

        Returns:
            A Questionnaire containing the extracted content
        """
        with open(file_path) as f:
            return Questionnaire.model_validate(json.load(f))
