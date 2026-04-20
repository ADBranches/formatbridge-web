from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from PIL import Image


def create_sample_output_image(path: Path, image_format: str, color: tuple[int, int, int]) -> Path:
    image = Image.new("RGB", (64, 64), color)

    if image_format.upper() == "JPEG":
        image.save(path, format="JPEG")
    elif image_format.upper() == "PNG":
        image.save(path, format="PNG")
    elif image_format.upper() == "WEBP":
        image.save(path, format="WEBP")
    else:
        raise ValueError(f"Unsupported test output format: {image_format}")

    return path


def build_test_app(monkeypatch, tmp_path):
    database_path = tmp_path / "phase7_test.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("PDF_OUTPUT_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("DOCX_OUTPUT_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("ZIP_OUTPUT_DIR", str(tmp_path / "archives"))
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


def test_zip_service_packages_all_successful_results(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)

    from app.extensions import db
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult
    from app.services.zip_service import create_zip_for_job

    converted_dir = tmp_path / "converted"
    converted_dir.mkdir(parents=True, exist_ok=True)

    first_output = create_sample_output_image(converted_dir / "first.jpg", "JPEG", (255, 0, 0))
    second_output = create_sample_output_image(converted_dir / "second.png", "PNG", (0, 255, 0))

    with app.app_context():
        job = ConversionJob(
            public_id="job_zip_1",
            requested_output_format="jpg",
            source_count=2,
            source_public_ids=["a", "b"],
            status="success",
        )
        db.session.add(job)
        db.session.commit()

        result_one = ConversionResult(
            job_id=job.id,
            source_file_id=None,
            output_format="jpg",
            status="success",
            output_filename="first.jpg",
            output_path=str(first_output),
        )
        result_two = ConversionResult(
            job_id=job.id,
            source_file_id=None,
            output_format="png",
            status="success",
            output_filename="second.png",
            output_path=str(second_output),
        )
        db.session.add(result_one)
        db.session.add(result_two)
        db.session.commit()

        zip_bundle = create_zip_for_job(job)

    zip_path = Path(zip_bundle["output_path"])
    assert zip_path.exists()
    assert zip_path.suffix.lower() == ".zip"
    assert zip_bundle["file_count"] == 2
    assert zip_bundle["size_bytes"] > 0

    with ZipFile(zip_path, "r") as archive:
        names = archive.namelist()
        assert names == ["first.jpg", "second.png"]
        archive.extractall(tmp_path / "extracted")

    assert (tmp_path / "extracted" / "first.jpg").exists()
    assert (tmp_path / "extracted" / "second.png").exists()


def test_job_zip_download_endpoint_returns_archive(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)

    from app.extensions import db
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult

    converted_dir = tmp_path / "converted"
    converted_dir.mkdir(parents=True, exist_ok=True)

    first_output = create_sample_output_image(converted_dir / "first.jpg", "JPEG", (255, 0, 0))
    second_output = create_sample_output_image(converted_dir / "second.png", "PNG", (0, 255, 0))

    with app.app_context():
        job = ConversionJob(
            public_id="job_zip_download_1",
            requested_output_format="jpg",
            source_count=2,
            source_public_ids=["a", "b"],
            status="success",
        )
        db.session.add(job)
        db.session.commit()

        result_one = ConversionResult(
            job_id=job.id,
            source_file_id=None,
            output_format="jpg",
            status="success",
            output_filename="first.jpg",
            output_path=str(first_output),
        )
        result_two = ConversionResult(
            job_id=job.id,
            source_file_id=None,
            output_format="png",
            status="success",
            output_filename="second.png",
            output_path=str(second_output),
        )
        db.session.add(result_one)
        db.session.add(result_two)
        db.session.commit()

    client = app.test_client()
    response = client.get("/api/v1/downloads/jobs/job_zip_download_1/zip")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/zip")
    assert "attachment" in response.headers.get("Content-Disposition", "")

    zip_path = tmp_path / "downloaded.zip"
    zip_path.write_bytes(response.data)

    with ZipFile(zip_path, "r") as archive:
        names = archive.namelist()
        assert names == ["first.jpg", "second.png"]