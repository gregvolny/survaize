import React, { useState, useEffect } from "react";
import CodeMirror, {
  drawSelection,
  gutter,
  highlightActiveLineGutter,
  lineNumbers,
} from "@uiw/react-codemirror";
import { json as jsonMode } from "@codemirror/lang-json";
import { jsonSchema } from "codemirror-json-schema";
import questionnaireCompletionSchema from "../models/questionnaire.schema.json";

import { oneDark } from "@codemirror/theme-one-dark";
import { useQuestionnaire } from "./QuestionnaireComponents";
import RobotReadingAnimation from "./RobotReadingAnimation";
import QuestionItem from "./QuestionItem";
import {
  bracketMatching,
  foldGutter,
  indentOnInput,
} from "@codemirror/language";
import { lintGutter } from "@codemirror/lint";
import {
  autocompletion,
  closeBrackets,
  completionKeymap,
  startCompletion,
} from "@codemirror/autocomplete";
import { EditorView, keymap } from "@codemirror/view";

interface QuestionnaireDisplayProps {
  showRaw: boolean;
}

export const QuestionnaireDisplay: React.FC<QuestionnaireDisplayProps> = ({
  showRaw,
}) => {
  const [editorValue, setEditorValue] = useState<string>("");
  const [parseError, setParseError] = useState<string | null>(null);

  const {
    questionnaire,
    isLoading,
    loadProgress,
    loadMessage,
    setQuestionnaire,
  } = useQuestionnaire();

  useEffect(() => {
    if (questionnaire) {
      setEditorValue(JSON.stringify(questionnaire, null, 2));
      setParseError(null);
    }
  }, [questionnaire]);

  // Custom completion trigger for keyboard shortcuts
  const triggerCompletionSync = (target: EditorView) => {
    return startCompletion(target);
  };

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
  const handleChange = (value: string): void => {
    try {
      const parsed = JSON.parse(value);
      setQuestionnaire(parsed);
      setParseError(null);
    } catch {
      setParseError("Invalid JSON");
    }
  };

  return (
    <div className="questionnaire-display">
      {!showRaw && (
        <div className="questionnaire-header">
          <div>
            <h2>{questionnaire.title}</h2>
            {questionnaire.description && <p>{questionnaire.description}</p>}
          </div>
        </div>
      )}

      {showRaw ? (
        <div className="json-display">
          <CodeMirror
            value={editorValue}
            height="500px"
            extensions={[
              gutter({ class: "CodeMirror-lint-markers" }),
              bracketMatching(),
              highlightActiveLineGutter(),
              closeBrackets(),
              lineNumbers(),
              lintGutter(),
              indentOnInput(),
              drawSelection(),
              foldGutter(),
              jsonMode(),
              autocompletion({
                activateOnTyping: true,
                maxRenderedOptions: 20,
                defaultKeymap: true,
              }),
              jsonSchema(questionnaireCompletionSchema),
              keymap.of([
                ...completionKeymap,
                { key: "Ctrl-Space", run: triggerCompletionSync },
                { key: "Alt-Space", run: triggerCompletionSync },
                {
                  key: "Cmd-Space",
                  preventDefault: true,
                  run: triggerCompletionSync,
                }, // Try Cmd+Space too
              ]),
            ]}
            theme={oneDark}
            onChange={handleChange}
          />
          {parseError && <div className="error-message">{parseError}</div>}
        </div>
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
