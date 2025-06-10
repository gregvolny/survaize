import { render, screen, fireEvent } from "@testing-library/react";
import { vi } from "vitest";
import { QuestionnaireDisplay } from "../components/QuestionnaireDisplay";
import { QuestionnaireContext } from "../components/QuestionnaireComponents";
import { Questionnaire } from "../models/questionnaire";

const sample: Questionnaire = {
  title: "Test",
  description: null,
  id_fields: [],
  sections: [],
};

const contextValue: React.ContextType<typeof QuestionnaireContext> = {
  questionnaire: sample,
  setQuestionnaire: vi.fn(),
  isLoading: false,
  setIsLoading: vi.fn(),
  loadProgress: 0,
  setLoadProgress: vi.fn(),
  loadMessage: "",
  setLoadMessage: vi.fn(),
};

test("shows editor when toggled", () => {
  render(
    <QuestionnaireContext.Provider value={contextValue}>
      <QuestionnaireDisplay />
    </QuestionnaireContext.Provider>,
  );
  const toggle = screen.getByTitle(/Show raw JSON/i);
  fireEvent.click(toggle);
  expect(document.querySelector(".cm-editor")).toBeInTheDocument();
});
