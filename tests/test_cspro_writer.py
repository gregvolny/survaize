from pathlib import Path

from survaize.reader.json_reader import JSONReader
from survaize.writer.cspro_writer import CSProWriter

test_data_dir = Path(__file__).parent / "fixtures" / "PopstanHouseholdSurvey"
cspro_fixture_dir = test_data_dir / "cspro"
json_fixture_file = test_data_dir / "PopstanHouseholdQuestionnaire.json"


def read_text(path: Path) -> str:
    """Read text from a file, normalizing line endings."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def test_cspro_writer_generates_expected_files(tmp_path: Path) -> None:
    """CSProWriter.write should generate files matching the cspro fixtures."""
    # Read questionnaire from JSON fixture
    reader = JSONReader()
    with open(json_fixture_file, "rb") as f:
        questionnaire = reader.read(f)

    # Prepare output path
    output_file = tmp_path / "PopstanHouseholdSurvey"

    # Run writer
    writer = CSProWriter()
    writer.write(questionnaire, output_file)

    assert output_file.is_dir(), f"Generated directory not found: {output_file}"

    # Compare each fixture file with generated file
    for fixture_path in sorted(cspro_fixture_dir.iterdir()):
        gen_path = output_file / fixture_path.name
        assert gen_path.exists(), f"Missing generated file: {gen_path.name}"
        # Compare contents
        expected = read_text(fixture_path)
        actual = read_text(gen_path)
        assert actual == expected, f"Contents differ for file {fixture_path.name}"

    # Ensure no extra files were generated
    generated_files = {p.name for p in output_file.iterdir()}
    fixture_files = {p.name for p in cspro_fixture_dir.iterdir()}
    assert generated_files == fixture_files, (
        f"Unexpected generated files: {sorted(generated_files - fixture_files)}; "
        f"missing files: {sorted(fixture_files - generated_files)}"
    )
