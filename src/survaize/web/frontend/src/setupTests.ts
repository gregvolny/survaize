import "@testing-library/jest-dom";
import { vi } from "vitest";

vi.mock("codemirror-json-schema", () => ({
  jsonSchemaLinter: () => () => null,
  jsonSchemaHover: () => () => null,
  jsonCompletion: () => null,
  jsonSchema: () => [], // Return empty array which is a valid extension
}));
