from collections.abc import Callable
from typing import IO, Protocol

from survaize.model.questionnaire import Questionnaire


class Reader(Protocol):
    """Protocol defining the interface for questionnaire readers."""

    def read(
        self,
        file: IO[bytes],
        progress_callback: Callable[[int, str], None] | None = None,
    ) -> Questionnaire:
        """Read a document and extract its content.

        Args:
            file: File-like object positioned at the beginning of the document
            progress_callback: Optional callback reporting progress percentage
                and a status message

        Returns:
            A Questionnaire containing the extracted content
        """
        ...
