import { render, screen } from "@testing-library/react";
import QuestionItem from "../components/QuestionItem";
import { QuestionType, NumericQuestion } from "../models/questionnaire";

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
