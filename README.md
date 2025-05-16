# Survaize

Survaize is a tool that automatically converts "paper" questionnaires into interactive survey apps. It uses a combination of OCR and generative AI vision models to understand the structure of survey questionnaires in order to generate survey apps compatible with data collection platforms like [CSPro](https://www.census.gov/data/software/cspro.html).

## Features

- Read PDF questionnaires 
- Intelligent survey structure recognition using Generative AI
- Conversion to intermediate JSON format
- Export to popular survey platforms (CSPro, others in the future)

## Installation

Eventually this will be published to PyPy but for now follow the instructions in [installation.md](installation.md).

## Setup
Survaize requires an AzureOpenAI API deployment. There are two ways to specify the settings. The easiest way is to create a .env with the following variables:

```
OPENAI_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXX"
OPENAI_API_VERSION="2024-12-01-preview"
OPENAI_API_URL="https://myazuredeploy-openai.openai.azure.com/"
OPENAI_API_DEPLOYMENT="gpt-4.1"
```

Alternatively, you can pass those variables as command line arguments to survaize (run `survaize --help` for details).

## Running
To convert a PDF questionnaire to CSPro run:

```shell
survaize convert input_file output_file --format cspro
```

For example:

```shell
survaize convert examples/PopstanHouseholdQuestionnaire.pdf output/PopstanHouseholdSurvey --format cspro
```
will generate a complete CSPro application (dictionary, forms...) in the directory `output/PopstanHouseholdSurvey`.

Survaize uses JSON as an intermediate format so JSON files can be used as input or output files. The above command could be split into two using an intermediate JSON file:

```shell
survaize convert examples/PopstanHouseholdQuestionnaire.pdf output/PopstanHouseholdSurvey.json --format json
survaize convert output/PopstanHouseholdSurvey.json output/PopstanHouseholdSurvey --format cspro
```

You can even hand edit the intermediate JSON file before generating the CSPro application.

## Development

This project uses Python and UV as the package manager. To install see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

For instructions on publishing to PyPI, see [publishing.md](publishing.md).

## License

MIT 

## TODO
- Support other LLM APIs besides Azure OpenAI
- Add a fix loop to handle case when LLM produces invalid JSON
- Use question type from Questionnaire to set capture type in CSPro to handle dates correctly
- Correctly handle location question type (produce two fields in CSPro)
- Fills in CAPI question text
- Evals