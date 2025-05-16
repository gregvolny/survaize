"""Command-line interface for Survaize."""

import logging
import os
from pathlib import Path
from typing import Literal

import click
from dotenv import load_dotenv
from rich.console import Console

from survaize.config.llm_config import LLMConfig
from survaize.convert.converter import QuestionnaireConverter

# Load environment variables from .env file if present
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# For console UI
console = Console()
OutputFormat = Literal["json"]  # Will be extended to include "cspro" and "odk" later


@click.group()
def cli() -> None:
    """Survaize - generate mobile survey apps from questionnaires ."""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("output_file", type=click.Path(dir_okay=False, path_type=Path))
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["cspro", "json"]),
    default="json",
    help="Output format for the questionnaire",
)
@click.option(
    "--api-key",
    envvar="OPENAI_API_KEY",
    help="OpenAI API key (can also be set via OPENAI_API_KEY env var)",
)
@click.option(
    "--api-version",
    envvar="OPENAI_API_VERSION",
    help="OpenAI API version (can also be set via OPENAI_API_VERSION env var)",
)
@click.option(
    "--api-url",
    envvar="OPENAI_API_URL",
    help="OpenAI API URL (can also be set via OPENAI_API_URL env var)",
)
@click.option(
    "--api-deployment",
    envvar="OPENAI_API_DEPLOYMENT",
    help="OpenAI API deployment name (can also be set via OPENAI_API_DEPLOYMENT env var)",
)
def convert(
    input_file: Path,
    output_file: Path,
    output_format: OutputFormat,
    api_key: str | None,
    api_version: str | None,
    api_url: str | None,
    api_deployment: str | None,
) -> None:
    """Convert a questionnaire to the specified format.

    Args:
        input_file: Path to the input file (PDF format or JSON)
        output_file: Path to file to write the output to
        output_format: Format to convert to ('cspro' or 'json')
        api_key: OpenAI API key
        api_version: OpenAI API version
        api_url: OpenAI API URL
        api_deployment: OpenAI API deployment name
    """
    # Get credentials from environment if not provided via CLI
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    api_version = api_version or os.getenv("OPENAI_API_VERSION")
    api_url = api_url or os.getenv("OPENAI_API_URL")
    api_deployment = os.getenv("OPENAI_API_DEPLOYMENT")

    # Validate all required credentials are available
    missing: list[str] = []
    if not api_key:
        missing.append("OPENAI_API_KEY")
    if not api_version:
        missing.append("OPENAI_API_VERSION")
    if not api_url:
        missing.append("OPENAI_API_URL")
    if not api_deployment:
        missing.append("OPENAI_API_DEPLOYMENT")

    if missing:
        raise click.UsageError(
            f"Missing required API credentials: {', '.join(missing)}. "
            + "Please provide them as command line options or set them in environment variables."
        )

    try:
        # Initialize converter (we can safely assert types since we validated above)
        assert api_key is not None
        assert api_version is not None
        assert api_url is not None
        assert api_deployment is not None
        llm_config = LLMConfig(
            api_key=api_key,
            api_version=api_version,
            api_url=api_url,
            api_deployment=api_deployment,
        )

        converter = QuestionnaireConverter(llm_config=llm_config)

        # Convert using the pipeline architecture
        output_path = converter.convert(input_file=input_file, output_file=output_file, output_format=output_format)

        console.log(f"[green]Successfully converted {input_file} to {output_path}")

    except Exception as e:
        console.log(f"[red]Error during conversion: {e}")
        logger.exception("Conversion failed")
        raise


if __name__ == "__main__":
    cli()
