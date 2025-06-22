import json
from collections.abc import Callable
from typing import IO

import logfire

from survaize.model.questionnaire import Questionnaire


class JSONReader:
    """Read questionnaire from JSON file (Survaize JSON schema)."""

    @logfire.instrument(extract_args=False)
    def read(
        self,
        file: IO[bytes],
        progress_callback: Callable[[int, str], None] | None = None,
    ) -> Questionnaire:
        """Read a document and extract its content.

        Args:
            file: File-like object containing the JSON questionnaire

        Returns:
            A Questionnaire containing the extracted content
        """
        file.seek(0)
        if progress_callback:
            progress_callback(0, "Reading JSON file")
        questionnaire = Questionnaire.model_validate(json.load(file))
        if progress_callback:
            progress_callback(100, "Completed")
        return questionnaire
