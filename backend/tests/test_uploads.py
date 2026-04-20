from __future__ import annotations

import io

from PIL import Image


def build_test_app(monkeypatch, tmp_path):
    database_path = tmp_path / "phase8_uploads.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("ZIP_OUTPUT_DIR", str(tmp_path / "archives"))
    monkeypatch.setenv("MAX_CONTENT_LENGTH", str(1024 * 1024))
    monkeypatch.setenv("MAX_FILES_PER_UPLOAD", "2")
    monkeypatch.setenv("MAX_FILE_SIZE_MB", "1")
    monkeypatch.setenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    monkeypatch.setenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

    from app import create_app
    from app.extensions import db
    from app.models.file_asset import FileAsset
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult

    app = create_app("testing")

    with app.app_context():
        _ = FileAsset, ConversionJob, ConversionResult
        db.drop_all()
        db.create_all()

    return app


def make_test_image_file(filename: str = "sample.png", size=(64, 64)) -> tuple[io.BytesIO, str]:
    image = Image.new("RGB", size, (20, 140, 220))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer, filename


def test_upload_rejects_missing_files(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)
    client = app.test_client()

    response = client.post("/api/v1/uploads", data={}, content_type="multipart/form-data")

    assert response.status_code == 400
    body = response.get_json()
    assert body["success"] is False
    assert "No files were provided" in body["message"]


def test_upload_rejects_unsupported_extension(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)
    client = app.test_client()

    fake_file = (io.BytesIO(b"not-an-image"), "bad.exe")
    response = client.post(
        "/api/v1/uploads",
        data={"files": [fake_file]},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["success"] is False
    assert "Unsupported file extension" in body["message"]


def test_upload_rejects_too_many_files(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)
    client = app.test_client()

    file_one = make_test_image_file("one.png")
    file_two = make_test_image_file("two.png")
    file_three = make_test_image_file("three.png")

    response = client.post(
        "/api/v1/uploads",
        data={"files": [file_one, file_two, file_three]},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["success"] is False
    assert "at most 2 files" in body["message"]


def test_upload_rejects_large_invalid_job_safely(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)
    client = app.test_client()

    oversized_stream = io.BytesIO(b"x" * (2 * 1024 * 1024))
    response = client.post(
        "/api/v1/uploads",
        data={"files": [(oversized_stream, "large.png")]},
        content_type="multipart/form-data",
    )

    assert response.status_code in (400, 413)
    body = response.get_json()
    assert body["success"] is False
    assert body["message"]