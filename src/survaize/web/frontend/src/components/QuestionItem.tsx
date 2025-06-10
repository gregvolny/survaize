import React from "react";
import { Question, QuestionType } from "../models/questionnaire";

interface QuestionItemProps {
  question: Question;
  isIdField?: boolean;
}

const QuestionItem: React.FC<QuestionItemProps> = ({
  question,
  isIdField = false,
}) => {
  let details: React.ReactNode = null;

  switch (question.type) {
    case QuestionType.SINGLE_SELECT:
    case QuestionType.MULTI_SELECT: {
      const hasManyOptions = question.options.length > 8;
      details = (
        <div
          className={`question-options${hasManyOptions ? " many-options" : ""}`}
        >
          <span className="option-label">Options:</span>
          <ul>
            {question.options.map((option) => (
              <li key={option.code}>
                <code>{option.code}</code>: {option.label}
              </li>
            ))}
          </ul>
        </div>
      );
      break;
    }
    case QuestionType.NUMERIC: {
      const showRange =
        question.min_value !== null || question.max_value !== null;
      const minDisplay =
        question.min_value !== null ? question.min_value : "-∞";
      const maxDisplay = question.max_value !== null ? question.max_value : "∞";
      details = (
        <div className="question-constraints">
          {showRange && (
            <div>
              Range: {minDisplay}-{maxDisplay}
            </div>
          )}
          {question.decimal_places !== null && (
            <div>Decimal places: {question.decimal_places}</div>
          )}
        </div>
      );
      break;
    }
    case QuestionType.TEXT:
      details =
        question.max_length !== null ? (
          <div className="question-constraints">
            Max length: {question.max_length}
          </div>
        ) : null;
      break;
    case QuestionType.DATE:
      details = (
        <div className="question-constraints">
          {question.min_date && <div>Min date: {question.min_date}</div>}
          {question.max_date && <div>Max date: {question.max_date}</div>}
        </div>
      );
      break;
    case QuestionType.LOCATION:
      details = (
        <div className="question-constraints">
          <div>Geographic coordinates (latitude, longitude)</div>
        </div>
      );
      break;
    default:
      details = null;
  }

  return (
    <div className="question-item" key={question.id}>
      <div className="question-header">
        <span className="question-number">{question.number}</span>
        <span className="question-id">[{question.id}]</span>
        {isIdField && <span className="id-marker">id</span>}
        <span className="question-type">{question.type}</span>
      </div>
      <div className="question-text">{question.text}</div>
      {question.instructions && (
        <div className="question-instructions">
          <em>Instructions: {question.instructions}</em>
        </div>
      )}
      {question.universe && (
        <div className="question-universe">
          <strong>Universe:</strong> {question.universe}
        </div>
      )}
      {details}
    </div>
  );
};

export default QuestionItem;
