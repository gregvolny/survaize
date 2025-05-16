from survaize.model.questionnaire import (
    DateQuestion,
    NumericQuestion,
    PartialQuestionnaire,
    Questionnaire,
    QuestionType,
    Section,
    TextQuestion,
    merge_questionnaires,
)


def test_merge_new_sections():
    """Tests merging a PartialQuestionnaire with sections not present in the base Questionnaire."""
    base_q = Questionnaire(
        title="Base Survey",
        description="Base Description",
        id_fields=[],
        sections=[
            Section(
                id="section_a",
                number="A",
                title="Section A",
                description=None,
                universe=None,
                questions=[
                    TextQuestion(
                        number="A1",
                        id="q_a1",
                        text="Question A1",
                        type=QuestionType.TEXT,
                        instructions=None,
                        universe=None,
                        max_length=None,
                    )
                ],
                occurrences=1,
            )
        ],
    )
    partial_q = PartialQuestionnaire(
        sections=[
            Section(
                id="section_b",
                number="B",
                title="Section B",
                description=None,
                universe=None,
                questions=[
                    NumericQuestion(
                        number="B1",
                        id="q_b1",
                        text="Question B1",
                        type=QuestionType.NUMERIC,
                        instructions=None,
                        universe=None,
                        min_value=None,
                        max_value=None,
                        decimal_places=None,
                    )
                ],
                occurrences=1,
            ),
            Section(
                id="section_c",
                number="C",
                title="Section C",
                description=None,
                universe=None,
                questions=[
                    DateQuestion(
                        number="C1",
                        id="q_c1",
                        text="Question C1",
                        type=QuestionType.DATE,
                        instructions=None,
                        universe=None,
                        min_date=None,
                        max_date=None,
                    )
                ],
                occurrences=1,
            ),
        ]
    )

    merged = merge_questionnaires(base_q, partial_q)

    assert len(merged.sections) == 3
    assert merged.sections[0].id == "section_a"
    assert merged.sections[1].id == "section_b"
    assert merged.sections[2].id == "section_c"
    assert len(merged.sections[0].questions) == 1
    assert len(merged.sections[1].questions) == 1
    assert len(merged.sections[2].questions) == 1
    assert merged.sections[1].questions[0].text == "Question B1"


def test_merge_existing_sections_new_questions():
    """Tests merging a PartialQuestionnaire where sections exist in the base
    but the partial contains new questions for those sections.
    """
    base_q = Questionnaire(
        title="Base Survey",
        description="Base Description",
        id_fields=[],
        sections=[
            Section(
                id="section_a",
                number="A",
                title="Section A",
                description=None,
                universe=None,
                questions=[
                    TextQuestion(
                        number="A1",
                        id="q_a1",
                        text="Question A1",
                        type=QuestionType.TEXT,
                        instructions=None,
                        universe=None,
                        max_length=None,
                    )
                ],
                occurrences=1,
            ),
            Section(
                id="section_b",
                number="B",
                title="Section B",
                description=None,
                universe=None,
                questions=[
                    NumericQuestion(
                        number="B1",
                        id="q_b1",
                        text="Question B1",
                        type=QuestionType.NUMERIC,
                        instructions=None,
                        universe=None,
                        min_value=None,
                        max_value=None,
                        decimal_places=None,
                    )
                ],
                occurrences=1,
            ),
        ],
    )
    partial_q = PartialQuestionnaire(
        sections=[
            Section(
                id="section_a",  # Existing section
                number="A",
                title="Section A",  # Title can be different, id is key
                description=None,
                universe=None,
                questions=[
                    DateQuestion(
                        number="A2",
                        id="q_a2",
                        text="Question A2",
                        type=QuestionType.DATE,
                        instructions=None,
                        universe=None,
                        min_date=None,
                        max_date=None,
                    )  # New question
                ],
                occurrences=1,
            ),
            Section(
                id="section_c",  # New section
                number="C",
                title="Section C",
                description=None,
                universe=None,
                questions=[
                    TextQuestion(
                        number="C1",
                        id="q_c1",
                        text="Question C1",
                        type=QuestionType.TEXT,
                        instructions=None,
                        universe=None,
                        max_length=None,
                    )
                ],
                occurrences=1,
            ),
        ]
    )

    merged = merge_questionnaires(base_q, partial_q)

    assert len(merged.sections) == 3
    assert merged.sections[0].id == "section_a"
    assert len(merged.sections[0].questions) == 2  # A1 and A2
    assert merged.sections[0].questions[0].number == "A1"
    assert merged.sections[0].questions[1].number == "A2"

    assert merged.sections[1].id == "section_b"
    assert len(merged.sections[1].questions) == 1

    assert merged.sections[2].id == "section_c"
    assert len(merged.sections[2].questions) == 1


def test_merge_existing_sections_duplicate_questions():
    """Tests that duplicate questions (same question number within the same section)
    are not added when merging.
    """
    base_q = Questionnaire(
        title="Base Survey",
        description="Base Description",
        id_fields=[],
        sections=[
            Section(
                id="section_a",
                number="A",
                title="Section A",
                description=None,
                universe=None,
                questions=[
                    TextQuestion(
                        number="A1",
                        id="q_a1",
                        text="Question A1 Original",
                        type=QuestionType.TEXT,
                        instructions=None,
                        universe=None,
                        max_length=None,
                    ),
                    TextQuestion(
                        number="A2",
                        id="q_a2",
                        text="Question A2",
                        type=QuestionType.TEXT,
                        instructions=None,
                        universe=None,
                        max_length=None,
                    ),
                ],
                occurrences=1,
            )
        ],
    )
    partial_q = PartialQuestionnaire(
        sections=[
            Section(
                id="section_a",
                number="A",
                title="Section A",
                description=None,
                universe=None,
                questions=[
                    NumericQuestion(
                        number="A1",
                        id="q_a1_dup",
                        text="Question A1 Duplicate",
                        type=QuestionType.NUMERIC,
                        instructions=None,
                        universe=None,
                        min_value=None,
                        max_value=None,
                        decimal_places=None,
                    ),  # Duplicate number
                    DateQuestion(
                        number="A3",
                        id="q_a3",
                        text="Question A3",
                        type=QuestionType.DATE,
                        instructions=None,
                        universe=None,
                        min_date=None,
                        max_date=None,
                    ),  # New question
                ],
                occurrences=1,
            )
        ]
    )

    merged = merge_questionnaires(base_q, partial_q)

    assert len(merged.sections) == 1
    assert merged.sections[0].id == "section_a"
    assert len(merged.sections[0].questions) == 3  # A1, A2, A3

    q_a1_merged = next(q for q in merged.sections[0].questions if q.number == "A1")
    assert q_a1_merged.text == "Question A1 Original"  # Original should be kept
    assert q_a1_merged.type == QuestionType.TEXT

    assert any(q.number == "A2" for q in merged.sections[0].questions)
    assert any(q.number == "A3" for q in merged.sections[0].questions)


def test_merge_empty_partial_questionnaire():
    """Tests merging an empty PartialQuestionnaire (no sections)."""
    base_q = Questionnaire(
        title="Base Survey",
        description="Base Description",
        id_fields=[],
        sections=[
            Section(
                id="section_a",
                number="A",
                title="Section A",
                description=None,
                universe=None,
                questions=[
                    TextQuestion(
                        number="A1",
                        id="q_a1",
                        text="Question A1",
                        type=QuestionType.TEXT,
                        instructions=None,
                        universe=None,
                        max_length=None,
                    )
                ],
                occurrences=1,
            )
        ],
    )
    partial_q = PartialQuestionnaire(sections=[])

    merged = merge_questionnaires(base_q, partial_q)

    assert len(merged.sections) == 1
    assert merged.sections[0].id == "section_a"
    assert len(merged.sections[0].questions) == 1
    assert merged == base_q  # Should be identical


def test_merge_into_empty_base_questionnaire():
    """Tests merging a PartialQuestionnaire into an empty base Questionnaire."""
    base_q = Questionnaire(title="", description="", id_fields=[], sections=[])
    partial_q = PartialQuestionnaire(
        sections=[
            Section(
                id="section_b",
                number="B",
                title="Section B",
                description=None,
                universe=None,
                questions=[
                    NumericQuestion(
                        number="B1",
                        id="q_b1",
                        text="Question B1",
                        type=QuestionType.NUMERIC,
                        instructions=None,
                        universe=None,
                        min_value=None,
                        max_value=None,
                        decimal_places=None,
                    )
                ],
                occurrences=1,
            )
        ]
    )

    merged = merge_questionnaires(base_q, partial_q)

    assert len(merged.sections) == 1
    assert merged.sections[0].id == "section_b"
    assert len(merged.sections[0].questions) == 1
    assert merged.sections[0].questions[0].text == "Question B1"
    assert merged.sections[0].questions[0].type == QuestionType.NUMERIC
    # Title and description should remain from the base (empty in this case)
    assert merged.title == ""
    assert merged.description == ""
    # id_fields should also remain from the base
    assert merged.id_fields == []

    # Test with a base that has some metadata
    base_q_with_meta = Questionnaire(
        title="Initial Title", description="Initial Desc", id_fields=["field1"], sections=[]
    )
    merged_with_meta = merge_questionnaires(base_q_with_meta, partial_q)
    assert merged_with_meta.title == "Initial Title"
    assert merged_with_meta.description == "Initial Desc"
    assert merged_with_meta.id_fields == ["field1"]
    assert len(merged_with_meta.sections) == 1
    assert merged_with_meta.sections[0].id == "section_b"
    assert merged_with_meta.sections[0].questions[0].type == QuestionType.NUMERIC
