"""Module defining the schema for the intermediate questionnaire format."""

from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    """Types of questions that can appear in a questionnaire."""

    SINGLE_SELECT = "single_select"
    MULTI_SELECT = "multi_select"
    NUMERIC = "numeric"
    TEXT = "text"
    DATE = "date"
    LOCATION = "location"


class Option(BaseModel):
    """Represents an option in a single or multiple select question."""

    code: str = Field(..., description="Unique code for the option")
    label: str = Field(..., description="Display label for the option")


class BaseQuestion(BaseModel):
    """Base class for all question types."""

    number: str = Field(..., description="The question number e.g. A1, A2, B1, B2, etc.")
    id: str = Field(..., description="Unique identifier for the question e.g. NAME, AGE, etc.")
    text: str = Field(..., description="The question text read to the respondent")
    instructions: str | None = Field(None, description="Additional instructions for the interviewer")
    universe: str | None = Field(
        None,
        description="Universe of respondents the question applies to e.g. residents over 10 years old",
    )


class NumericQuestion(BaseQuestion):
    """Numeric question type with its specific constraints."""

    type: Literal[QuestionType.NUMERIC]
    min_value: float | None = Field(None, description="Minimum allowed value")
    max_value: float | None = Field(None, description="Maximum allowed value")
    decimal_places: int | None = Field(None, description="Number of decimal places allowed")


class TextQuestion(BaseQuestion):
    """Text question type with its specific constraints."""

    type: Literal[QuestionType.TEXT]
    max_length: int | None = Field(None, description="Maximum length of text input")


class SingleChoiceQuestion(BaseQuestion):
    """Single select question type with its options."""

    type: Literal[QuestionType.SINGLE_SELECT]
    options: list[Option] = Field(..., description="List of available options")


class MultipleChoiceQuestion(BaseQuestion):
    """Multiple select question type with its options."""

    type: Literal[QuestionType.MULTI_SELECT]
    options: list[Option] = Field(..., description="List of available options")
    min_selections: int | None = Field(None, description="Minimum number of selections required")
    max_selections: int | None = Field(None, description="Maximum number of selections allowed")


class DateQuestion(BaseQuestion):
    """Date question type with its specific constraints."""

    type: Literal[QuestionType.DATE]
    min_date: str | None = Field(None, description="Minimum allowed date (YYYY-MM-DD)")
    max_date: str | None = Field(None, description="Maximum allowed date (YYYY-MM-DD)")


class LocationQuestion(BaseQuestion):
    """Location question type representing a geographical coordinate.

    Latitude ranges from -90 to 90 degrees.
    Longitude ranges from -180 to 180 degrees.
    """

    type: Literal[QuestionType.LOCATION]
    latitude: float | None = Field(None, description="The latitude coordinate (-90 to 90 degrees)")
    longitude: float | None = Field(None, description="The longitude coordinate (-180 to 180 degrees)")


# Question type is a discriminated union of all question types
Question = Annotated[
    NumericQuestion | TextQuestion | SingleChoiceQuestion | MultipleChoiceQuestion | DateQuestion | LocationQuestion,
    Field(discriminator="type"),
]


class Section(BaseModel):
    """Represents a section in the questionnaire containing related questions."""

    id: str = Field(..., description="Unique identifier for the section")
    number: str = Field(..., description="The section number e.g. A, B, I, II, etc.")
    title: str = Field(..., description="Title of the section")
    description: str | None = Field(None, description="Description of the section")
    universe: str | None = Field(
        None,
        description="Universe of respondents the section applies to e.g. residents over 10 years old",
    )
    questions: list[Question] = Field(..., description="Questions in this section")
    occurrences: int = Field(..., description="Maximum number of times the section is asked")


class TrailingSectionRef(BaseModel):
    """Reference to a section that continues on the next page."""

    id: str = Field(..., description="Unique identifier for the section")
    question_ids: list[str] = Field(..., description="IDs of the last question(s) on this page that may continue")


class SectionFragment(BaseModel):
    """Full trailing section used when providing context to the LLM."""

    id: str = Field(..., description="Unique identifier for the section")
    number: str = Field(..., description="The section number")
    title: str = Field(..., description="Title of the section")
    questions: list[Question] = Field(..., description="Last question(s) on the page that may continue")


class Questionnaire(BaseModel):
    """Top-level questionnaire structure."""

    title: str = Field(..., description="Title of the questionnaire")
    description: str | None = Field(None, description="Description of the questionnaire")
    id_fields: list[str] = Field(
        ...,
        description="List of field ids used to uniquely identify the unit of observation (household, individual, etc.)",
    )
    sections: list[Section] = Field(..., description="Sections in the questionnaire")
    trailing_sections: list[TrailingSectionRef] = Field(
        default_factory=list,
        description=(
            "Sections that may continue onto the next page. Only include the last questions from the current page."
        ),
    )


class PartialQuestionnaire(BaseModel):
    """Incomplete questionnaire, subset of a full questionnaire - used to represent a single page."""

    sections: list[Section] = Field(..., description="Sections in the questionnaire")
    trailing_sections: list[TrailingSectionRef] = Field(
        default_factory=list,
        description=(
            "Sections that may continue onto the next page. Only include the last questions from the current page."
        ),
    )


def merge_questionnaires(base: Questionnaire, partial: PartialQuestionnaire) -> Questionnaire:
    """Merge a partial questionnaire into an existing questionnaire.

    Handles cases where sections may span multiple pages by checking for existing sections
    and merging questions while avoiding duplicates.

    Args:
        base: The existing questionnaire to merge into
        partial: The partial questionnaire to merge from

    Returns:
        The merged questionnaire
    """
    # Create a copy of the base questionnaire to modify
    merged = base.model_copy(deep=True)

    # Keep track of section IDs and questions we've seen
    existing_section_ids = {section.id: idx for idx, section in enumerate(merged.sections)}

    # Process each section from the partial questionnaire
    for new_section in partial.sections:
        if new_section.id in existing_section_ids:
            # Section already exists, merge questions
            section_idx = existing_section_ids[new_section.id]
            existing_section = merged.sections[section_idx]

            # Track existing questions by number to avoid duplicates
            existing_question_numbers = {q.number: True for q in existing_section.questions}

            # Add new questions if they don't already exist
            for question in new_section.questions:
                if question.number not in existing_question_numbers:
                    existing_section.questions.append(question)
                    existing_question_numbers[question.number] = True
        else:
            # New section, add it directly
            merged.sections.append(new_section)
            existing_section_ids[new_section.id] = len(merged.sections) - 1

    return merged
