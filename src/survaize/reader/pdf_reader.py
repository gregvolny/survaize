"""Module defining the document reading layer of the pipeline."""

import logging
from pathlib import Path

import cv2
import numpy as np
import pdf2image
import pytesseract
from PIL import Image

from survaize.interpreter.ai_interpreter import AIQuestionnaireInterpreter
from survaize.interpreter.scanned_questionnaire import ScannedQuestionnaire
from survaize.model.questionnaire import Questionnaire

# Configure logger
logger = logging.getLogger(__name__)


class PDFReader:
    """Reads PDF documents and extracts text and images."""

    def __init__(self, interpreter: AIQuestionnaireInterpreter):
        """Initialize the PDFReader with an interpreter.

        Args:
            interpreter: An instance of AIQuestionnaireInterpreter
        """
        self.interpreter: AIQuestionnaireInterpreter = interpreter

    def read(self, file_path: Path) -> Questionnaire:
        """Read a PDF document and extract its content.

        Args:
            file_path: Path to the PDF file

        Returns:
            A Questionnaire containing the extracted content
        """

        pages = self._extract_pages(file_path)

        texts = [self._process_page(page) for page in pages]

        scanned_questionnaire = ScannedQuestionnaire(pages=pages, extracted_text=texts, source_path=file_path)

        return self.interpreter.interpret(scanned_questionnaire)

    def _extract_pages(self, pdf_path: Path) -> list[Image.Image]:
        """Convert PDF pages to images.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            list of PIL Image objects, one per page
        """
        logger.info(f"Converting PDF to images: {pdf_path}")
        return pdf2image.convert_from_path(pdf_path)  # type: ignore

    def _process_page(self, image: Image.Image) -> str:
        """Process a single page image with OCR.

        Args:
            image: PIL Image object of the page

        Returns:
            Extracted text from the page
        """
        # Convert PIL image to OpenCV format for preprocessing
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Basic image preprocessing
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray)

        # Perform OCR
        return pytesseract.image_to_string(denoised)  # type: ignore
