"""Module for orchestrating the questionnaire conversion process."""

import logging
from pathlib import Path

from survaize.config.llm_config import LLMConfig
from survaize.interpreter.ai_interpreter import AIQuestionnaireInterpreter
from survaize.reader.json_reader import JSONReader
from survaize.reader.pdf_reader import PDFReader
from survaize.reader.reader import Reader
from survaize.writer.cspro_writer import CSProWriter
from survaize.writer.json_writer import JSONWriter
from survaize.writer.writer import Writer

logger = logging.getLogger(__name__)


class QuestionnaireConverter:
    """Orchestrates the conversion of questionnaires."""

    def __init__(self, llm_config: LLMConfig):
        """Initialize the converter.
        Args:
            llm_config: Configuration for the LLM (API key, version, URL, deployment)
        """

        interpreter = AIQuestionnaireInterpreter(llm_config)
        self.readers: dict[str, Reader] = {
            "pdf": PDFReader(interpreter),
            "json": JSONReader(),
        }
        self.writers: dict[str, Writer] = {
            "json": JSONWriter(),
            "cspro": CSProWriter(),
        }

    def convert(self, input_file: Path, output_file: Path, output_format: str):
        """Convert a questionnaire to the specified format.

        Args:
            input_file: Path to the input file
            output_file: Path to file to write the output to
            output_format: Output format

        Returns:
            Path to the generated output file
        """
        output_file.parent.mkdir(parents=True, exist_ok=True)

        input_format = input_file.suffix.lower().replace(".", "")
        reader = self.readers.get(input_format)

        if not reader:
            raise ValueError(
                f"Unsupported input format: {input_format}. Supported formats are: {', '.join(self.readers.keys())}"
            )

        logger.info(f"Reading questionnaire: {input_file}")
        questionnaire = reader.read(input_file)

        writer = self.writers.get(output_format.lower())
        if not writer:
            raise ValueError(
                f"Unsupported output format: {output_format}. Supported formats are: {', '.join(self.writers.keys())}"
            )

        logger.info(f"Writing converted questionnaire: {output_file}")
        writer.write(questionnaire, output_file)
