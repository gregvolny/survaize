import logging
from pathlib import Path

from survaize.model.questionnaire import Questionnaire

logger = logging.getLogger(__name__)


class JSONWriter:
    """Generates JSON format output from questionnaires."""

    def write(self, questionnaire: Questionnaire, output_path: Path):
        """Generate a JSON representation of a questionnaire.

        Args:
            questionnaire: The structured questionnaire data
            output_path: Path where the JSON file should be saved

        """
        logger.info(f"Writing output to: {output_path}")

        with open(output_path, "w") as f:
            f.write(questionnaire.model_dump_json(indent=2, exclude_none=True))
