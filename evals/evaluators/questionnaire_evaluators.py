"""Questionnaire-specific evaluators for Survaize."""

import logging
from pathlib import Path

from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from typing_extensions import override

from evals.datasets.case_metadata import CaseMetadata
from survaize.model.questionnaire import MultipleChoiceQuestion, Option, Questionnaire, Section, SingleChoiceQuestion

logger = logging.getLogger(__name__)

class SectionPresenceEvaluator(Evaluator[Path, Questionnaire, CaseMetadata]):
    """Evaluator for checking that all expected sections are present."""

    @override
    def evaluate(self, ctx: EvaluatorContext[Path, Questionnaire, CaseMetadata]) -> dict[str, float]:
        """Compute precision, recall, and F1 for section presence."""
        expected = ctx.expected_output
        assert expected is not None, "Expected output must not be None"
        actual: Questionnaire = ctx.output

        expected_sections = {(section.number, section.title) for section in expected.sections}
        actual_sections = {(section.number, section.title) for section in actual.sections}
        true_positives = expected_sections & actual_sections

        precision = len(true_positives) / len(actual_sections) if actual_sections  else 0.0
        recall = len(true_positives) / len(expected_sections) if expected_sections else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0

        # log mismatches
        missing = expected_sections - actual_sections
        extra = actual_sections - expected_sections
        if missing:
            logger.warning(f"Missing sections: {missing}")
        if extra:
            logger.warning(f"Unexpected sections: {extra}")
        return {
            "section_presence_precision": precision,
            "section_presence_recall": recall,
            "section_presence_f1": f1,
        }

class QuestionPresenceEvaluator(Evaluator[Path, Questionnaire, CaseMetadata]):
    """Evaluator for checking that all expected questions are present."""

    @override
    def evaluate(self, ctx: EvaluatorContext[Path, Questionnaire, CaseMetadata]) -> dict[str, float]:
        """Compute precision, recall, and F1 for question presence."""
        expected = ctx.expected_output
        assert expected is not None, "Expected output must not be None"
        actual: Questionnaire = ctx.output

        expected_questions = {
            (section.number, question.number, question.text)
            for section in expected.sections
            for question in section.questions
        }
        actual_questions = {
            (section.number, question.number, question.text)
            for section in actual.sections
            for question in section.questions
        }
        true_positives = expected_questions & actual_questions

        precision = len(true_positives) / len(actual_questions) if actual_questions else 0.0
        recall = len(true_positives) / len(expected_questions) if expected_questions else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0

        # log mismatches
        missing_q = expected_questions - actual_questions
        extra_q = actual_questions - expected_questions
        if missing_q:
            logger.warning(f"Missing questions: {missing_q}")
        if extra_q:
            logger.warning(f"Unexpected questions: {extra_q}")
        return {
            "question_presence_precision": precision,
            "question_presence_recall": recall,
            "question_presence_f1": f1,
        }

class QuestionTypeEvaluator(Evaluator[Path, Questionnaire, CaseMetadata]):
    """Evaluator for checking that question types match the expected types."""

    @override
    def evaluate(
        self,
        ctx: EvaluatorContext[Path, Questionnaire, CaseMetadata]
    ) -> dict[str, float]:
        expected = ctx.expected_output
        assert expected is not None, "Expected output must not be None"
        actual: Questionnaire = ctx.output

        # build maps keyed by (section_id, question_number) → QuestionType
        expected_map = {
            (sec.number, q.number): q.type
            for sec in expected.sections
            for q in sec.questions
        }
        actual_map = {
            (sec.number, q.number): q.type
            for sec in actual.sections
            for q in sec.questions
        }

        # count how many actual types match expected types
        matches = {
            key for key, typ in actual_map.items()
            if key in expected_map and expected_map[key] == typ
        }

        precision = len(matches) / len(actual_map) if actual_map else 0.0
        recall = len(matches) / len(expected_map) if expected_map else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0

        # log type mismatches
        mismatches = [key for key in expected_map if key in actual_map and expected_map[key] != actual_map[key]]
        for sec_q in mismatches:
            exp, act = expected_map[sec_q], actual_map[sec_q]
            logger.warning(f"Type mismatch at {sec_q}: expected {exp}, got {act}")
        return {
            "question_type_precision": precision,
            "question_type_recall": recall,
            "question_type_f1": f1,
        }


class OptionExtractionEvaluator(Evaluator[Path, Questionnaire, CaseMetadata]):
    """Evaluator for checking that select‐question options are correctly extracted."""

    @override
    def evaluate(
        self,
        ctx: EvaluatorContext[Path, Questionnaire, CaseMetadata]
    ) -> dict[str, float]:
        expected = ctx.expected_output
        assert expected is not None, "Expected output must not be None"
        actual: Questionnaire = ctx.output

        def collect_options(qs: list[Section]) -> dict[tuple[str, str], list[Option]]:
            # returns mapping (section_number, question_number) → set of option labels
            return {
                (sec.number, q.number): q.options
                for sec in qs
                for q in sec.questions
                if isinstance(q, SingleChoiceQuestion | MultipleChoiceQuestion)
            }

        expected_opts = collect_options(expected.sections)
        actual_opts = collect_options(actual.sections)

        # count how many actual option‐sets exactly match expected
        matches = {
            key for key, opts in actual_opts.items()
            if key in expected_opts and expected_opts[key] == opts
        }

        precision = len(matches) / len(actual_opts) if actual_opts else 0.0
        recall = len(matches) / len(expected_opts) if expected_opts else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0

        # log option mismatches
        for key, opts in actual_opts.items():
            if key in expected_opts and expected_opts[key] != opts:
                logger.warning(f"Option mismatch at {key}: expected {expected_opts[key]}, got {opts}")
        return {
            "option_extraction_precision": precision,
            "option_extraction_recall": recall,
            "option_extraction_f1": f1,
        }