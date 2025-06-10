import React, { useState } from "react";
import { useQuestionnaire } from "./QuestionnaireComponents";
import RobotReadingAnimation from "./RobotReadingAnimation";
import QuestionItem from "./QuestionItem";

export const QuestionnaireDisplay: React.FC = () => {
  const [showRaw, setShowRaw] = useState<boolean>(false);

  const toggleView = (): void => {
    setShowRaw((prev) => !prev);
  };
  const { questionnaire, isLoading, loadProgress, loadMessage } =
    useQuestionnaire();

  if (isLoading) {
    return (
      <div className="questionnaire-loading">
        <RobotReadingAnimation />
        <p>
          {loadMessage} ({Math.round(loadProgress)}%)
        </p>
        <div className="progress-bar-container">
          <div
            className="progress-bar"
            style={{ width: `${loadProgress}%` }}
          ></div>
        </div>
      </div>
    );
  }

  if (!questionnaire) {
    return (
      <div className="questionnaire-placeholder">
        <p>No questionnaire loaded. Please open a questionnaire file.</p>
      </div>
    );
  }

  return (
    <div className="questionnaire-display">
      <div className="questionnaire-header">
        <div>
          <h2>{questionnaire.title}</h2>
          {questionnaire.description && <p>{questionnaire.description}</p>}
        </div>
        <button
          className="icon-button"
          onClick={toggleView}
          title={showRaw ? "Show formatted view" : "Show raw JSON"}
        >
          {"{}"}
        </button>
      </div>

      {showRaw ? (
        <pre className="json-display">
          {JSON.stringify(questionnaire, null, 2)}
        </pre>
      ) : (
        <div className="sections-container">
          {questionnaire.sections.map((section) => (
            <div key={section.id} className="section">
              <div className="section-header">
                <h3>
                  {section.number}: {section.title}
                </h3>
                {section.description && <p>{section.description}</p>}
                {section.universe && (
                  <div className="section-universe">
                    <strong>Universe:</strong> {section.universe}
                  </div>
                )}
                {section.occurrences > 1 && (
                  <div className="section-occurrences">
                    <strong>Repeats:</strong> up to {section.occurrences} times
                  </div>
                )}
              </div>

              <div className="questions-list">
                {section.questions.map((question) => (
                  <QuestionItem 
                    key={question.id} 
                    question={question} 
                    isIdField={questionnaire.id_fields.includes(question.id)}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
