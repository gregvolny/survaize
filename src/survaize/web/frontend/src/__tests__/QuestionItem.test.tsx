import { render, screen } from "@testing-library/react";
import { test, expect } from "vitest";
import QuestionItem from "../components/QuestionItem";
import {
  QuestionType,
  NumericQuestion,
  SingleChoiceQuestion,
  MultipleChoiceQuestion,
  TextQuestion,
  DateQuestion,
  LocationQuestion,
} from "../models/questionnaire";

test("renders range for numeric question", () => {
  const question: NumericQuestion = {
    number: "1",
    id: "age",
    text: "Age?",
    type: QuestionType.NUMERIC,
    min_value: 18,
    max_value: 65,
    decimal_places: null,
  };
  render(<QuestionItem question={question} />);
  expect(screen.getByText("Range: 18-65")).toBeInTheDocument();
});

test("renders negative infinity when min missing", () => {
  const question: NumericQuestion = {
    number: "2",
    id: "id2",
    text: "Weight?",
    type: QuestionType.NUMERIC,
    min_value: null,
    max_value: 20,
    decimal_places: null,
  };
  render(<QuestionItem question={question} />);
  expect(screen.getByText("Range: -∞-20")).toBeInTheDocument();
});

test("hides range line when both bounds missing", () => {
  const question: NumericQuestion = {
    number: "3",
    id: "id3",
    text: "Value?",
    type: QuestionType.NUMERIC,
    min_value: null,
    max_value: null,
    decimal_places: null,
  };
  render(<QuestionItem question={question} />);
  const range = screen.queryByText(/Range:/i);
  expect(range).toBeNull();
});

test("renders correct tooltip for numeric question", () => {
  const question: NumericQuestion = {
    number: "1",
    id: "age",
    text: "Age?",
    type: QuestionType.NUMERIC,
    min_value: 18,
    max_value: 65,
    decimal_places: null,
  };
  render(<QuestionItem question={question} />);
  const tooltipElement = screen.getByTitle("Numeric");
  expect(tooltipElement).toBeInTheDocument();
});

test("renders correct icon and tooltip for single select question", () => {
  const question: SingleChoiceQuestion = {
    number: "4",
    id: "gender",
    text: "What is your gender?",
    type: QuestionType.SINGLE_SELECT,
    options: [
      { code: "M", label: "Male" },
      { code: "F", label: "Female" },
    ],
  };
  render(<QuestionItem question={question} />);
  const iconElement = screen.getByRole("img", { hidden: true });
  expect(iconElement.parentElement).toHaveAttribute("title", "Single select");
});

test("renders correct icon and tooltip for multi select question", () => {
  const question: MultipleChoiceQuestion = {
    number: "5",
    id: "hobbies",
    text: "What are your hobbies?",
    type: QuestionType.MULTI_SELECT,
    options: [
      { code: "R", label: "Reading" },
      { code: "S", label: "Sports" },
    ],
  };
  render(<QuestionItem question={question} />);
  const iconElement = screen.getByRole("img", { hidden: true });
  expect(iconElement.parentElement).toHaveAttribute("title", "Multi select");
});

test("renders correct icon and tooltip for text question", () => {
  const question: TextQuestion = {
    number: "6",
    id: "name",
    text: "What is your name?",
    type: QuestionType.TEXT,
    max_length: 100,
  };
  render(<QuestionItem question={question} />);
  const iconElement = screen.getByRole("img", { hidden: true });
  expect(iconElement.parentElement).toHaveAttribute("title", "Text");
});

test("renders correct icon and tooltip for date question", () => {
  const question: DateQuestion = {
    number: "7",
    id: "birthdate",
    text: "What is your birth date?",
    type: QuestionType.DATE,
    min_date: "1900-01-01",
    max_date: "2023-12-31",
  };
  render(<QuestionItem question={question} />);
  const iconElement = screen.getByRole("img", { hidden: true });
  expect(iconElement.parentElement).toHaveAttribute("title", "Date");
});

test("renders correct icon and tooltip for location question", () => {
  const question: LocationQuestion = {
    number: "8",
    id: "location",
    text: "What is your current location?",
    type: QuestionType.LOCATION,
  };
  render(<QuestionItem question={question} />);
  const iconElement = screen.getByRole("img", { hidden: true });
  expect(iconElement.parentElement).toHaveAttribute("title", "Location");
});
