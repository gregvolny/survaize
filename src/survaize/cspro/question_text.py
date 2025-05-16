from pathlib import Path

import yaml
from pydantic import BaseModel


class QsfLanguage(BaseModel):
    """Represents a language in the QSF file."""

    name: str
    label: str


class QsfStyle(BaseModel):
    """Represents a style in the QSF file."""

    name: str
    className: str
    css: str


class QsfText(BaseModel):
    """Represents localized text in the QSF file."""

    EN: str


class QsfCondition(BaseModel):
    """Represents a condition for a question in the QSF file."""

    questionText: QsfText
    helpText: QsfText


class QsfQuestion(BaseModel):
    """Represents a question in the QSF file."""

    name: str
    conditions: list[QsfCondition]


class QsfFile(BaseModel):
    """Represents the root of a QSF file."""

    fileType: str = "Question Text"
    version: str = "CSPro 8.0"
    languages: list[QsfLanguage]
    styles: list[QsfStyle]
    questions: list[QsfQuestion]

    def save(self, path: Path):
        """Convert the QSF file to YAML format."""
        # Write the YAML file
        with open(path, "w", encoding="utf-8") as f:
            f.write("---\n")  # Add document start marker
            yaml.dump(
                self.model_dump(mode="json"),
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )
            f.write("...")  # Add document end marker
