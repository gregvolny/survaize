# Project coding standards

1. Follow Python best practices with clear typing - all function parameter and return types must be explicit
2. Use descriptive function and variable names
3. Each function should have a clear single responsibility
4. Include docstrings for all public functions and classes
5. Prefer immutable data structures where possible
6. Use functional programming principles (pure functions, minimal side effects)
7. Use the Python logging library for logging e.g. `logger = logging.getLogger(__name__)`
8. Only add comments to complex hard to understand code, don't comment every line
9. Prefix private methods in classes with _

# Architecture

### Core Components

1. **Models**
   - `Questionnaire` intermediate format for survey questionnaire (structured JSON)

2. **Document Readers**
   - `Reader` protocol, reads file and produces a `Questionnaire` 
   - `PDFReader` reads a PDF and generates a `Questionnaire`  (uses `AIQuestionnaireInterpreter` to find questionnaire structure)
   - `JSONReader` reads a `Questionnaire` from a JSON file

3. **Questionnaire Interpretation**
   - `AIQuestionnaireInterpreter` that uses LLMs to convert a `ScannedQuestionnaire` into a structured `Questionnaire` object

4. **Document Writers**
   - `Writer` protocol, takes a `Questionnaire` and writes it to disk
   - Writers for each output format (`CSProWriter`, `JSONWriter`)

5. **Converter**
   - Orchestrates conversion: input file → reader → writer

6. **CSPro**
   - Models & serializers for CSPro files (dictionary, forms, question text)
