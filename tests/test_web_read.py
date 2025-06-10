from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from survaize.model.questionnaire import Questionnaire
from survaize.reader.json_reader import JSONReader
from survaize.web.backend.api import routes
from survaize.web.backend.app import create_app

fixture_path = Path("tests/fixtures/PopstanHouseholdSurvey/PopstanHouseholdQuestionnaire.json")


def test_json_reader_progress() -> None:
    reader = JSONReader()
    progress: list[tuple[int, str]] = []
    with open(fixture_path, "rb") as f:
        questionnaire = reader.read(f, lambda p, m: progress.append((p, m)))
    assert progress[0][0] == 0
    assert progress[-1][0] == 100
    assert isinstance(questionnaire, Questionnaire)


@pytest.fixture()
def client() -> Iterator[TestClient]:
    app = create_app()

    def override_reader_factory():
        class DummyFactory:
            def get(self, _fmt: str) -> JSONReader:
                return JSONReader()

        return DummyFactory()  # type: ignore

    app.dependency_overrides[routes.get_reader_factory] = override_reader_factory
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_read_questionnaire_endpoint(client: TestClient) -> None:
    with open(fixture_path, "rb") as f:
        response = client.post(
            "/api/questionnaire/read",
            files={"file": ("q.json", f, "application/json")},
            data={"format": "json"},
        )
    assert response.status_code == 200
    job_id = response.json()["job_id"]

    messages: list[dict[str, object]] = []
    with client.websocket_connect(f"/api/questionnaire/read/{job_id}") as ws:
        while True:
            data = ws.receive_json()
            messages.append(data)
            if "questionnaire" in data or "error" in data:
                break

    assert any("questionnaire" in m for m in messages)
    assert messages[0]["progress"] == 0
    assert messages[-1]["progress"] == 100
