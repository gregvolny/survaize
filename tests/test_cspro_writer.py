from pathlib import Path

from survaize.reader.json_reader import JSONReader
from survaize.writer.cspro_writer import CSProWriter
from survaize.model.questionnaire import (
    Questionnaire,
    Section,
    DateQuestion,
    QuestionType,
    QuestionnaireMetadata,
)
from survaize.cspro.form import FormItemCaptureType, Roster
from survaize.cspro.dictionary import DictionaryItem # Already implicitly used via writer

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
    questionnaire = reader.read(json_fixture_file)

    # Prepare output path
    output_file = tmp_path / f"{questionnaire.title}.cspro"

    # Run writer
    writer = CSProWriter()
    writer.write(questionnaire, output_file)

    # Determine generated directory using sanitized application name
    generated_dir = tmp_path / "PopstanHouseholdSurvey"
    assert generated_dir.is_dir(), f"Generated directory not found: {generated_dir}"

    # Compare each fixture file with generated file
    for fixture_path in sorted(cspro_fixture_dir.iterdir()):
        gen_path = generated_dir / fixture_path.name
        assert gen_path.exists(), f"Missing generated file: {gen_path.name}"
        # Compare contents
        expected = read_text(fixture_path)
        actual = read_text(gen_path)
        assert actual == expected, f"Contents differ for file {fixture_path.name}"


def test_date_question_in_regular_form(tmp_path: Path) -> None:
    """Verify DateQuestion in a regular section results in DATE capture type."""
    writer = CSProWriter()
    questionnaire = Questionnaire(
        id="test_date_survey",
        title="Test Date Survey",
        metadata=QuestionnaireMetadata(version="1.0", author="Test Author"),
        sections=[
            Section(
                id="SEC_A",
                number="A",
                title="Section A",
                occurrences=1,
                questions=[
                    DateQuestion(
                        id="BIRTH_DATE",
                        number="Q1",
                        text="Date of birth",
                        type=QuestionType.DATE,
                    )
                ],
            )
        ],
        id_fields=["BIRTH_DATE"],  # Making it an ID field for simplicity to ensure it's directly in a form group
    )

    # Note: _generate_form_file expects questionnaire as the first argument
    # This is a correction to the previous implementation plan.
    dictionary = writer._generate_data_dictionary(questionnaire)
    # Create a dummy dictionary file name
    dictionary_file_name = "test_date_survey.dcf"

    # Assuming _generate_form_file signature is:
    # def _generate_form_file(self, questionnaire: Questionnaire, dictionary: CSProDictionary, dictionary_file_name: str) -> FormFile:
    form_file = writer._generate_form_file(questionnaire, dictionary, dictionary_file_name)

    # ID items are usually in the first group of the first level's forms.
    # If BIRTH_DATE is an ID field, it will be in the ID_ITEMS_FORM group.
    # The ID_ITEMS_FORM is the first form, so forms[0]
    # The group for these items is groups[0] within that form's level representation.
    
    # Based on _generate_form_file structure:
    # forms[0] is ID_ITEMS_FORM, groups[0] is the corresponding FormGroup for ID items.
    # If there were non-ID questions in a section, they'd be in subsequent groups/forms.
    # Since BIRTH_DATE is an ID_FIELD, it should be in the first form group.

    assert len(form_file.levels) > 0, "No levels generated in form file"
    assert len(form_file.levels[0].groups) > 0, "No groups in the first level"
    
    id_group = form_file.levels[0].groups[0] # ID_ITEMS_FORM group
    assert id_group.name == "ID_ITEMS_FORM"

    found_field = None
    for item_field in id_group.items:
        if item_field.name == "BIRTH_DATE": # DictionaryItem name is directly used for FormField name
            found_field = item_field
            break
    
    assert found_field is not None, "BIRTH_DATE field not found in the ID_ITEMS_FORM group"
    assert hasattr(found_field, 'data_capture_type'), "Field does not have data_capture_type"
    assert found_field.data_capture_type == FormItemCaptureType.DATE, \
        f"BIRTH_DATE capture type is {found_field.data_capture_type}, expected DATE"


def test_date_question_in_roster_form(tmp_path: Path) -> None:
    """Verify DateQuestion in a roster section results in DATE capture type in roster columns."""
    writer = CSProWriter()
    questionnaire = Questionnaire(
        id="test_roster_date_survey",
        title="Test Roster Date Survey",
        metadata=QuestionnaireMetadata(version="1.0", author="Test Author"),
        sections=[
            Section(
                id="ROSTER_SEC",
                number="R",
                title="Roster Section",
                occurrences=3, # This makes it a roster
                questions=[
                    DateQuestion(
                        id="INTERVIEW_DATE",
                        number="Q1",
                        text="Date of interview",
                        type=QuestionType.DATE,
                    )
                ],
            )
        ],
        id_fields=[], # No ID fields for simplicity, focusing on roster
    )

    dictionary = writer._generate_data_dictionary(questionnaire)
    dictionary_file_name = "test_roster_date_survey.dcf"
    
    # Assuming _generate_form_file signature is:
    # def _generate_form_file(self, questionnaire: Questionnaire, dictionary: CSProDictionary, dictionary_file_name: str) -> FormFile:
    form_file = writer._generate_form_file(questionnaire, dictionary, dictionary_file_name)

    # The roster section will be the first non-ID form/group.
    # If no ID_FIELDS, then groups[0] should be for ROSTER_SEC_FORM
    # The _generate_form_file logic:
    # 1. Creates ID_ITEMS_FORM (if id_items exist). Let's assume no id_items for this test.
    #    To ensure this, questionnaire.id_fields = []
    # So, form_file.levels[0].groups[0] should be for ROSTER_SEC_FORM.
    # This group should contain one item: the Roster itself.

    assert len(form_file.levels) > 0, "No levels generated"
    assert len(form_file.levels[0].groups) > 0, "No groups in the first level"
    
    # The first group will be for the roster section
    roster_group = form_file.levels[0].groups[0] 
    assert "ROSTER_SEC_FORM" in roster_group.name

    assert len(roster_group.items) == 1, "Roster group should contain one item (the Roster)"
    roster_item = roster_group.items[0]
    assert isinstance(roster_item, Roster), "Item in roster group is not a Roster"

    # The Roster object has columns.
    # First column (index 0) in _create_roster_form is a stub RosterColumn(width=10)
    # Subsequent columns correspond to items in record.items
    # So, INTERVIEW_DATE field should be in roster_item.columns[1]
    
    assert len(roster_item.columns) > 1, "Roster has no columns for data fields"
    # Skipping column 0 as it's a stub.
    # The first data column is columns[1]
    data_column = None
    for col in roster_item.columns:
        if col.fields and col.fields[0].name == "INTERVIEW_DATE":
            data_column = col
            break
    
    assert data_column is not None, "INTERVIEW_DATE column not found in roster"
    assert len(data_column.fields) == 1, "Data column should have one field for INTERVIEW_DATE"
    
    interview_date_field = data_column.fields[0]
    assert hasattr(interview_date_field, 'data_capture_type'), "Field does not have data_capture_type"
    assert interview_date_field.data_capture_type == FormItemCaptureType.DATE, \
        f"INTERVIEW_DATE capture type is {interview_date_field.data_capture_type}, expected DATE"
