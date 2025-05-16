from enum import Enum
from pathlib import Path
from typing import TextIO

from pydantic import BaseModel, Field


class FormItemType(Enum):
    GROUP = 1
    FIELD = 2
    TEXT = 3
    ROSTER = 5
    LEVEL = 6
    BLOCK = 7


class FormBase(BaseModel):
    name: str
    label: str
    form_file_number: int | None = None


class FormItemBase(FormBase):
    item_type: FormItemType


class FormGroup(FormItemBase):
    required: bool
    max: int
    items: list[FormItemBase] = []


class FormText(FormItemBase):
    text: str
    position: tuple[int, int, int, int] | None = None
    horizontal_alignment: str | None = None
    vertical_alignment: str | None = None


class FormItemCaptureType(Enum):
    TEXT_BOX = "TextBox"
    RADIO_BUTTON = "RadioButton"
    CHECK_BOX = "CheckBox"
    DROP_DOWN = "DropDown"
    COMBO_BOX = "ComboBox"
    DATE = "Date"
    NUMBER_PAD = "NumberPad"
    BARCODE = "Barcode"
    SLIDER = "Slider"
    TOGGLE_BUTTON = "ToggleButton"
    PHOTO = "Photo"
    SIGNATURE = "Signature"
    AUDIO = "Audio"


class FormField(FormItemBase):
    dictionary_item: str
    data_capture_type: FormItemCaptureType
    text: FormText | None = None
    position: tuple[int, int, int, int] | None = None
    use_unicode_text_box: bool = False


class RosterColumn(BaseModel):
    width: int | None = None
    header_text: FormText | None = None
    fields: list[FormField] = []


class Roster(FormGroup):
    type: str
    type_name: str
    display_size: tuple[int, int, int, int]
    orientation: str
    field_row_height: int
    heading_row_height: int
    use_occurrence_labels: bool | None = None
    free_movement: bool = False
    columns: list[RosterColumn] = []
    stub_text: list[FormText] = []


class FormLevel(FormBase):
    groups: list[FormGroup]


class Form(FormBase):
    level: int
    size: tuple[int, int]
    items: list[FormItemBase] = []


class FormFile(BaseModel):
    """Represents a CSPro form file."""

    name: str = Field(..., description="Name of the form file")
    dictionary_name: str = Field(..., description="Associated dictionary name")
    dictionary_file_name: str = Field(..., description="Name of dictionary file on disk")
    forms: list[Form] = Field(default_factory=list, description="Forms in the form file")
    levels: list[FormLevel] = Field(default_factory=list, description="Levels in the form file")

    def save(self, output_path: Path) -> None:
        """Save the CSPro form file to disk in INI-like format.

        This method writes the FormFile object to disk in the INI-like format expected
        by CSPro. It includes all form components: forms, groups, fields, texts, and rosters.
        """
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\ufeff")  # UTF-8 BOM
            self._write_formfile_section(f)
            self._write_dictionaries_section(f)
            self._write_forms_section(f)
            self._write_levels_section(
                f,
            )

    def _write_formfile_section(self, f: TextIO):
        f.write("[FormFile]\r\n")
        f.write("Version=CSPro 8.0\r\n")
        f.write(f"Name={self.name}\r\n")
        f.write(f"Label={self.name.replace('_FF', '')}\r\n")
        f.write("DefaultTextFont=-013 0000 0000 0000 0700 0000 0000 0000 0000 0000 0000 0000 0000 Arial\r\n")
        f.write("FieldEntryFont=0018 0000 0000 0000 0600 0000 0000 0000 0000 0000 0000 0000 0000 Courier New\r\n")
        f.write("Type=SystemControlled\r\n  \r\n")

    def _write_dictionaries_section(self, f: TextIO):
        f.write("[Dictionaries]\r\n")
        f.write(f"File=.\\{self.dictionary_file_name}\r\n  \r\n")

    def _write_forms_section(self, f: TextIO):
        for form in self.forms:
            f.write("[Form]\r\n")
            f.write(f"Name={form.name}\r\n")
            f.write(f"Label={form.label}\r\n")
            f.write(f"Level={form.level}\r\n")
            f.write(f"Size={form.size[0]},{form.size[1]}\r\n  \r\n")
            for item in form.items:
                f.write(f"Item={item.name}\r\n")
            f.write("  \r\n")
            f.write("[EndForm]\r\n  \r\n")

    def _write_levels_section(self, f: TextIO):
        if self.levels:
            for level in self.levels:
                f.write("[Level]\r\n")
                f.write(f"Name={level.name}\r\n")
                f.write(f"Label={level.label}\r\n")
                for group in level.groups:
                    f.write("  \r\n")
                    self._write_group_section(f, group)
        f.write("  \r\n")

    def _write_group_section(self, f: TextIO, group: FormGroup):
        f.write("[Group]\r\n")
        f.write(f"Required={'Yes' if group.required else 'No'}\r\n")
        f.write(f"Name={group.name}\r\n")
        f.write(f"Label={group.label}\r\n")
        f.write(f"Form={group.form_file_number}\r\n")
        f.write(f"Max={group.max}\r\n")
        for item in group.items:
            f.write("  \r\n")
            if isinstance(item, FormField):
                self._write_field_section(f, item)
            elif isinstance(item, FormText):
                self._write_text_section(f, item)
            elif isinstance(item, Roster):
                self._write_roster_section(f, item, group)
        f.write("[EndGroup]\r\n")

    def _write_field_section(self, f: TextIO, item: FormField):
        f.write("[Field]\r\n")
        f.write(f"Name={item.name}\r\n")
        p = item.position
        if p:
            f.write(f"Position={p[0]},{p[1]},{p[2]},{p[3]}\r\n")
        f.write(f"Item={item.dictionary_item},{self.dictionary_name}\r\n")
        f.write("FieldLabelType=DictionaryLabel\r\n")
        if item.use_unicode_text_box:
            f.write("UseUnicodeTextBox=Yes\r\n")
        f.write(f"DataCaptureType={item.data_capture_type.value}\r\n")
        if item.form_file_number:
            f.write(f"Form={item.form_file_number}\r\n")
        if item.text:
            f.write("  \r\n")
            self._write_text_section(f, item.text)

    def _write_text_section(self, f: TextIO, item: FormText):
        f.write("[Text]\r\n")
        p = item.position
        if p:
            f.write(f"Position={p[0]},{p[1]},{p[2]},{p[3]}\r\n")
        f.write(f"Text={item.text}\r\n")
        f.write("  \r\n")

    def _write_roster_section(self, f: TextIO, roster: Roster, group: FormGroup):
        f.write("[Grid]\r\n")
        f.write(f"Name={roster.name}\r\n")
        f.write(f"Label={roster.label}\r\n")
        f.write(f"Form={group.form_file_number}\r\n")
        f.write(f"Required={'Yes' if roster.required else 'No'}\r\n")
        f.write(f"Type={roster.type}\r\n")
        f.write(f"TypeName={roster.type_name}\r\n")
        f.write(f"Max={roster.max}\r\n")
        f.write(
            f"DisplaySize={roster.display_size[0]},{roster.display_size[1]},{roster.display_size[2]},{roster.display_size[3]}\r\n"
        )
        f.write(f"Orientation={roster.orientation}\r\n")
        f.write(f"FieldRowHeight={roster.field_row_height}\r\n")
        f.write(f"HeadingRowHeight={roster.heading_row_height}\r\n")
        if roster.use_occurrence_labels:
            f.write("UseOccurrenceLabels=Yes\r\n")
        f.write(f"FreeMovement={'Yes' if roster.free_movement else 'No'}\r\n \r\n")
        for stub in roster.stub_text:
            self._write_text_section(f, stub)
            f.write("  \r\n")
        for column in roster.columns:
            self._write_column_section(f, column)
        f.write("[EndGrid]\r\n \r\n")

    def _write_column_section(self, f: TextIO, column: RosterColumn):
        f.write("[Column]\r\n")
        if column.width:
            f.write(f"Width={column.width}\r\n")
        if column.header_text:
            f.write("  \r\n")
            f.write("[HeaderText]\r\n")
            f.write(f"Text={column.header_text.text}\r\n")
        for field in column.fields:
            f.write("  \r\n")
            self._write_field_section(f, field)
        f.write("[EndColumn]\r\n  \r\n")
