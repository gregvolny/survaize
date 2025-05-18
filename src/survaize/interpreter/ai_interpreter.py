"""Module for interpreting questionnaire documents using LLMs."""

import base64
import json
import logging
from io import BytesIO

from openai import AzureOpenAI, OpenAI
from openai.types.chat import (
    ChatCompletionContentPartImageParam,
    ChatCompletionContentPartTextParam,
)
from PIL import Image

from survaize.config.llm_config import LLMConfig, OpenAIProviderType
from survaize.interpreter.scanned_questionnaire import ScannedQuestionnaire
from survaize.model.questionnaire import PartialQuestionnaire, Questionnaire, merge_questionnaires

# Configure logger
logger = logging.getLogger(__name__)


class AIQuestionnaireInterpreter:
    """Interprets questionnaire documents using LLM vision models."""

    def __init__(self, llm_config: LLMConfig):
        """Initialize the interpreter.

        Args:
            llm_config: Configuration/keys for the OpenAI API
        """
        self.llm_config: LLMConfig = llm_config
        if llm_config.provider == OpenAIProviderType.AZURE:
            assert llm_config.api_url is not None
            self.client: OpenAI | AzureOpenAI = AzureOpenAI(
                api_key=llm_config.api_key,
                api_version=llm_config.api_version,
                azure_endpoint=llm_config.api_url,
            )
        else:  # default to openai client
            self.client = OpenAI(
                api_key=llm_config.api_key,
                base_url=llm_config.api_url,
            )

    def interpret(self, scanned_document: ScannedQuestionnaire) -> Questionnaire:
        """Interpret a questionnaire document into a structured format.

        Args:
            scanned_document: QuestionnaireDocument containing page images and OCR text

        Returns:
            Structured Questionnaire object
        """
        # Reset current state for a new interpretation
        current_state = None

        # Process each page
        total_pages = len(scanned_document.pages)

        for i, (page, text) in enumerate(zip(scanned_document.pages, scanned_document.extracted_text, strict=False), 1):
            logger.info(f"Examining page {i}/{total_pages}")
            if i == 1:
                # Process the first page
                current_state = self._process_first_page(page, text)
            else:
                assert current_state is not None
                # Process subsequent pages
                partial_questionnaire = self._process_subsequent_page(page, text, i, current_state)
                current_state = merge_questionnaires(current_state, partial_questionnaire)

        if current_state is None:
            raise ValueError("No valid questionnaire found in the document")
        return current_state

    def _process_first_page(self, image: Image.Image, ocr_text: str) -> Questionnaire:
        """Process the first page of the questionnaire.

        Args:
            image: PIL Image of the page
            ocr_text: OCR extracted text from the page
        """
        # Encode image for API
        base64_image = self._encode_image(image)

        prompt = self._create_vision_prompt(1)
        content = [
            ChatCompletionContentPartTextParam({"type": "text", "text": prompt}),
            ChatCompletionContentPartImageParam(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                }
            ),
            ChatCompletionContentPartTextParam({"type": "text", "text": f"OCR Text:\n{ocr_text}"}),
        ]

        response = self.client.chat.completions.create(
            model=self.llm_config.model,
            messages=[{"role": "user", "content": content}],
            response_format={"type": "json_object"},
        )

        try:
            response_str = response.choices[0].message.content
            if not response_str:
                raise ValueError(f"Refusal from OpenAI: {response.choices[0].message.refusal}")
            return Questionnaire.model_validate(json.loads(response_str))

        except Exception as e:
            logger.error(f"Error processing page {1}: {e}")
            logger.error(f"Raw response: {response}")
            raise

    def _process_subsequent_page(
        self,
        image: Image.Image,
        ocr_text: str,
        page_number: int,
        questionnaire_so_far: Questionnaire,
    ) -> PartialQuestionnaire:
        """Process a single page of the questionnaire.
        This method is called for all pages after the first one.

        Args:
            image: PIL Image of the page
            ocr_text: OCR extracted text from the page
            page_number: Current page number
        """
        # Encode image for API
        base64_image = self._encode_image(image)

        prompt = self._create_vision_prompt(page_number)
        content = [
            ChatCompletionContentPartTextParam({"type": "text", "text": prompt}),
            ChatCompletionContentPartImageParam(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                }
            ),
            ChatCompletionContentPartTextParam({"type": "text", "text": f"OCR Text:\n{ocr_text}"}),
            ChatCompletionContentPartTextParam(
                {
                    "type": "text",
                    "text": f"Questionnaire from previous pages:\n{questionnaire_so_far.model_dump_json(indent=2)}",
                }
            ),
        ]

        # Make the API call with structured output
        response = self.client.chat.completions.create(
            model=self.llm_config.model,
            messages=[{"role": "user", "content": content}],
            response_format={"type": "json_object"},
        )

        try:
            response_str = response.choices[0].message.content
            if not response_str:
                raise ValueError(f"Refusal from OpenAI: {response.choices[0].message.refusal}")
            return PartialQuestionnaire.model_validate(json.loads(response_str))

        except Exception as e:
            logger.error(f"Error processing page {page_number}: {e}")
            logger.error(f"Raw response: {response}")
            raise

    def _encode_image(self, image: Image.Image) -> str:
        """Encode a PIL image to base64.

        Args:
            image: PIL Image to encode

        Returns:
            Base64 encoded image string
        """
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def _create_vision_prompt(self, page_number: int) -> str:
        """Create the prompt for GPT-4 Vision.

        Args:
            page_number: Current page number

        Returns:
            Prompt string
        """
        schema_example = """
            {
                "title": "Survey Title",
                "description": "A national household survey",
                "id_fields": ["cluster", "household number"],
                "sections": [
                    {
                        "id": "section_a",
                        "number": "A",
                        "title": "Household Information",
                        "description": "Basic information about the household",
                        "universe": "Respondents over 18 years old",
                        "occurrences": 20,
                        "questions": [
                            {
                                "number": "A1",
                                "id": "cluster",
                                "text": "Enter cluster number for household from sample",
                                "type": "numeric",
                                "max_length": 99
                            },
                            {
                                "number": "A2",
                                "id": "household number",
                                "text": "Enter household number from sample",
                                "type": "numeric",
                                "max_length": 999
                            },
                            {
                                "number": "A3",
                                "id": "name",
                                "text": "What is your name?",
                                "type": "text",
                                "instructions": "Please enter the full name",
                                "max_length": 99
                            },
                            {
                                "number": "A4",
                                "id": "name",
                                "text": "What is your name?",
                                "type": "text",
                                "instructions": "Please enter the full name",
                                "max_length": 99
                            },
                            {
                                "number": "A5",
                                "id": "age",
                                "text": "What is your age?",
                                "type": "numeric",
                                "instructions": "Please enter the age in years",
                                "min_value": 0,
                                "max_value": 99
                            },
                            {
                                "number": "A6",
                                "id": "birth_date",
                                "text": "What is your date of birth?",
                                "type": "date"
                            },
                            {
                                "number": "A7",
                                "id": "gender",
                                "text": "What is your gender?",
                                "type": "single_select",
                                "options": [{"code": "1", "label": "Male"}, {"code": "2", "label": "Female"}]
                            }
                        ]
                    }
                ]
            }
        """

        partial_example = """
            {
                "sections": [
                    {
                        "id": "section_b",
                        "number": "B",
                        "title": "Education Information",
                        "description": "Information about educational background",
                        "universe": "Household members aged 5 and above",
                        "occurrences": 50,
                        "questions": [
                            {
                                "number": "B1",
                                "id": "edu_level",
                                "text": "What is the highest level of education completed?",
                                "type": "single_select",
                                "options": [
                                    {"code": "1", "label": "None"},
                                    {"code": "2", "label": "Primary"},
                                    {"code": "3", "label": "Secondary"},
                                    {"code": "4", "label": "Tertiary"}
                                ]
                            }
                        ]
                    }
                ]
            }
        """

        if page_number == 1:
            return f"""You are an expert in implementing CAPI survey instruments for surveys. Your job is to read a 
            paper questionnaire and convert it to a structured format that can be used for further processing.
                    
            Given the first page of a questionnaire as an image, along with the OCR text from the page, produce a JSON
            representation of the page of the questionnaire that follows the given schema.
            
            IMPORTANT: The JSON you produce must be a valid Questionnaire object containing all sections and questions
            found on the first page.

            Proceed as follows:

            1. Identify the title of the survey
            2. Identify any description of the survey
            3. Identify the sections of the survey and extract the following information:
                - Section ID (derived from the title, lowercase with underscores)
                - Section number
                - Section title
                - Section description (if present)
                - Universe (which respondent the section is intended for, if present)
                - Occurrences (how many times the section is repeated. Repeated sections are often represented as
                  tables with multiple rows in which case count the rows, otherwise estimate based on the 
                  topic/questions in the section e.g. if the section is about household members, it may be repeated 
                  for each member of the household)
            4. In each section identify the individual questions and extract the following information:
                - Question number
                - Question ID (derived from the question, lowercase with underscores)
                - Text of the question to be read to the respondent
                - Instructions to the interviewer (if present)
                - Question type (either single_select, multi_select, numeric, text, date, location)
                - single_select and multi_select questions will have a list of responses, for those questions extract 
                  the code and label for each response
                - numeric questions will have a minimum and maximum value which can be inferred based 
                  on the number of digits represented as boxes next to or under the question, if there is no information
                  to infer the minimum and maximum values, leave them blank
                - text questions will have a maximum length which can be inferred based on the number of boxes next to
                  or under the question, if there is no information to infer the maximum 
                length, leave it blank
            5. Identify the id-fields for the questionnaire. These must be a subset of the ids from questions in the
               questionnaire. They are usually at the start of the questionnaire and combined will uniquely identify
               the questionnaire. They are often geographic identifiers, household identifiers, or respondent
               identifiers or codes from the sample.

            Here is an example of the output you should produce:
            ```json
            {schema_example}
            ```
            """
        else:
            return f"""You are an expert in implementing CAPI survey instruments for surveys. Your job is to read a 
            paper questionnaire and convert it to a structured format that can be used for further processing.
                    
            Given page {page_number} of a questionnaire as an image, along with the OCR text from the page, produce a
            JSON representation of just the sections and questions found on this page.
            
            IMPORTANT: The JSON you produce must be a valid PartialQuestionnaire object containing only the sections 
            and questions found on this page. If a section continues from a previous page, include only the new
            questions found on this page.

            Proceed as follows:

            1. Identify any new sections that begin on this page and extract the following information:
                - Section ID (derived from the title, lowercase with underscores)
                - Section number
                - Section title
                - Section description (if present)
                - Universe (which respondent the section is intended for, if present)
                - Occurrences (how many times the section is repeated. Repeated sections are often represented as
                  tables with multiple rows in which case count the rows, otherwise estimate based on the
                  topic/questions in the section e.g. if the section is about household members, it may be repeated
                  for each member of the household)
            2. For questions that belong to a section from a previous page, include that section with its ID but only
               the new questions.
            3. Identify the individual questions and extract the following information:
                - Question number
                - Question ID (derived from the question, lowercase with underscores)
                - Text of the question to be read to the respondent
                - Instructions to the interviewer (if present)
                - Question type (either single_select, multi_select, numeric, text, date, location)
                - single_select and multi_select questions will have a list of responses, for those questions extract
                  the code and label for each response
                - numeric questions will have a minimum and maximum value which can be inferred based 
                  on the number of digits represented as boxes next to or under the question, if there is no 
                  information to infer the minimum and maximum values, leave them blank
                - text questions will have a maximum length which can be inferred based on the number of boxes next to
                  or under the question, if there is no information to infer the maximum length, leave it blank

            Here is an example of the output you should produce:
            ```json
            {partial_example}
            ```
            """
