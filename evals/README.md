# Evals

This directory contains evaluation scripts and datasets. The evaluations assess the performance of the conversion process by checking how well the AI interprets and converts PDF questionnaires into structured formats. This is useful for validating changes to prompts or LLMs used in the conversion process.

Evals are implemented using the [Pydantic AI framework](https://ai.pydantic.dev/evals/#evaluators).

## Prerequisites

- Set required environment variables for your LLM provider. Follow directions in #setup in main README.md.

## Running the evaluations

From the project root, execute:

```bash
uv run python -m evals.run_evals
```

This command will:

1. Load the PDF-to-questionnaire dataset defined in `evals/datasets/pdf_to_questionnaire_dataset.py`.
2. Convert each PDF case into a `Questionnaire` using the `convert_questionnaire` task.
3. Compute performance metrics and print a summary report.

## Interpreting the output

The script prints a table with one row per case and an "Averages" row at the bottom. Columns:

- **Case ID**: Identifier for the test case.
- **Scores**: Precision, recall, and F1 metrics for:
  - `section_presence` (detecting survey sections)
  - `question_presence` (detecting question entries)
  - `question_type` (correct question types)
  - `option_extraction` (extracting choice options)
- **Duration**: Time taken to process each case.

**Metric definitions:**

***Precision***

Of all items your system extracted, the fraction that are correct. 

Precision = |Predicted ∩ Actual| / |Predicted|

Measures reliability—how many false positives you have.

***Recall***

Of all true items in the ground truth, the fraction your system actually extracted.

Recall = |Predicted ∩ Actual| / |Actual|

Measures completeness—how many false negatives you have.

***F₁-score***

The harmonic mean of precision and recall.

F₁ = 2 × (Precision × Recall) / (Precision + Recall)

Balanced trade-off—only high when both precision and recall are high.


### Sample output

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Case ID                  ┃ Scores                             ┃ Duration ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ popstan_household_survey │ section_presence_precision: 0.750  │     1.0s │
│                          │ section_presence_recall: 0.750     │          │
│                          │ section_presence_f1: 0.750         │          │
│                          │ question_presence_precision: 0.955 │          │
│                          │ question_presence_recall: 0.955    │          │
│                          │ question_presence_f1: 0.955        │          │
│                          │ question_type_precision: 1.00      │          │
│                          │ question_type_recall: 1.00         │          │
│                          │ question_type_f1: 1.00             │          │
│                          │ option_extraction_precision: 0.667 │          │
│                          │ option_extraction_recall: 0.667    │          │
│                          │ option_extraction_f1: 0.667        │          │
├──────────────────────────┼────────────────────────────────────┼──────────┤
│ Averages                 │ section_presence_precision: 0.750  │     1.0s │
│                          │ section_presence_recall: 0.750     │          │
│                          │ section_presence_f1: 0.750         │          │
│                          │ question_presence_precision: 0.955 │          │
│                          │ question_presence_recall: 0.955    │          │
│                          │ question_presence_f1: 0.955        │          │
│                          │ question_type_precision: 1.00      │          │
│                          │ question_type_recall: 1.00         │          │
│                          │ question_type_f1: 1.00             │          │
│                          │ option_extraction_precision: 0.667 │          │
│                          │ option_extraction_recall: 0.667    │          │
│                          │ option_extraction_f1: 0.667        │          │
└──────────────────────────┴────────────────────────────────────┴──────────┘
```


## What is evaluated

1. All sections and questions are present ✅
2. Question types match expected types ✅
3. Single/multi-select options are correctly extracted ✅
4. Numeric sizes are correctly extracted 🔲
5. Repeating sections are captured correctly 🔲
6. Question ids, instructions and section descriptions are reasonable (LLM judge) 🔲
7. Universe is reasonable (LLM judge) 🔲
8. ID fields are correct 🔲
9. Question ids are good (LLM judge) 🔲