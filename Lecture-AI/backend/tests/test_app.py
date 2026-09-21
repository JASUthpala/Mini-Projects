import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, detect_media_type, ensure_upload_folder


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_detect_media_type_supports_audio_and_pdf():
    assert detect_media_type("lecture.pdf") == "pdf"
    assert detect_media_type("lecture.mp3") == "audio"
    assert detect_media_type("lecture.wav") == "audio"
    assert detect_media_type("notes.txt") is None


def test_ensure_upload_folder_creates_directory(tmp_path):
    folder = tmp_path / "uploads"
    assert ensure_upload_folder(str(folder)) is True
    assert folder.exists()
    assert folder.is_dir()


def test_process_route_requires_file(client):
    response = client.post("/process")
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["error"] == "No file uploaded"


def test_process_route_handles_valid_pdf_file(client, monkeypatch, tmp_path):
    captured = {}

    def fake_extract_text(path):
        captured["pdf_path"] = path
        return "This is lecture content about machine learning."

    def fake_summary(text):
        return "Machine learning summary."

    def fake_questions(text):
        return "1. What is machine learning?"

    monkeypatch.setattr("app.extract_text_from_pdf", fake_extract_text)
    monkeypatch.setattr("app.summarize", fake_summary)
    monkeypatch.setattr("app.generate_questions", fake_questions)

    pdf_path = tmp_path / "lecture.pdf"
    pdf_path.write_bytes(b"fake pdf")

    with open(pdf_path, "rb") as pdf_file:
        response = client.post("/process", data={"file": (pdf_file, "lecture.pdf")}, content_type="multipart/form-data")

    assert response.status_code == 200
    assert response.get_json()["summary"] == "Machine learning summary."
    assert response.get_json()["questions"] == "1. What is machine learning?"
    assert "lecture.pdf" in captured["pdf_path"]
