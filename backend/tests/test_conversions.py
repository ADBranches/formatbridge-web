from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


def create_sample_image(path: Path, image_format: str) -> Path:
    image = Image.new("RGB", (64, 64), (20, 140, 220))

    if image_format.upper() == "JPEG":
        image.save(path, format="JPEG")
    elif image_format.upper() == "PNG":
        image.save(path, format="PNG")
    elif image_format.upper() == "WEBP":
        image.save(path, format="WEBP")
    elif image_format.upper() == "HEIF":
        image.save(path, format="HEIF")
    else:
        raise ValueError(f"Unsupported test image format: {image_format}")

    return path


@pytest.mark.parametrize(
    "source_extension,source_format,target_format",
    [
        ("heic", "HEIF", "jpg"),
        ("heic", "HEIF", "png"),
        ("jpg", "JPEG", "jpg"),
        ("jpg", "JPEG", "png"),
        ("jpg", "JPEG", "webp"),
        ("jpeg", "JPEG", "jpg"),
        ("jpeg", "JPEG", "png"),
        ("jpeg", "JPEG", "webp"),
        ("png", "PNG", "jpg"),
        ("png", "PNG", "png"),
        ("png", "PNG", "webp"),
        ("webp", "WEBP", "jpg"),
        ("webp", "WEBP", "png"),
        ("webp", "WEBP", "webp"),
    ],
)

def test_supported_image_conversions(monkeypatch, tmp_path, source_extension, source_format, target_format):
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("CONVERTED_FILES_DIR", str(tmp_path / "converted"))

    from app.services.image_conversion_service import convert_image_file
    from app.utils.naming import build_output_path, normalize_target_format

    source_path = tmp_path / f"sample.{source_extension}"
    create_sample_image(source_path, source_format)

    normalized_target = normalize_target_format(target_format)

    output_path = build_output_path(
        directory=tmp_path / "converted",
        original_filename=source_path.name,
        target_format=normalized_target,
    )

    converted_path = convert_image_file(
        source_path=source_path,
        output_path=output_path,
        target_format=normalized_target,
    )

    assert converted_path.exists()
    assert converted_path.suffix.lower() == f".{normalized_target}"
    assert converted_path.stat().st_size > 0

    with Image.open(converted_path) as converted_image:
        converted_image.load()
        assert converted_image.width == 64
        assert converted_image.height == 64


def build_test_app(monkeypatch, tmp_path):
    database_path = tmp_path / "phase6_test.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("PDF_OUTPUT_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("DOCX_OUTPUT_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    monkeypatch.setenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")
    monkeypatch.setenv("CONVERTED_FILES_DIR", str(tmp_path / "converted"))

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


def test_conversion_router_writes_image_result_rows(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)

    from app.extensions import db
    from app.models.file_asset import FileAsset
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult
    from app.services.conversion_router_service import run_phase3_conversion_job

    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    source_path = upload_dir / "sample.png"
    create_sample_image(source_path, "PNG")

    with app.app_context():
        source_file = FileAsset(
            public_id="file_public_1",
            original_filename="sample.png",
            stored_filename="sample.png",
            mime_type="image/png",
            extension="png",
            size_bytes=source_path.stat().st_size,
            storage_path=str(source_path),
        )
        db.session.add(source_file)
        db.session.commit()

        job = ConversionJob(
            public_id="job_public_1",
            requested_output_format="jpg",
            source_count=1,
            source_public_ids=["file_public_1"],
            status="processing",
        )
        db.session.add(job)
        db.session.commit()

        summary = run_phase3_conversion_job("job_public_1")

        result_rows = ConversionResult.query.filter_by(job_id=job.id).all()

        assert summary["converted_count"] == 1
        assert len(result_rows) == 1
        assert result_rows[0].status == "success"
        assert result_rows[0].output_filename is not None
        assert result_rows[0].output_path is not None
        assert Path(result_rows[0].output_path).exists()


def test_create_docx_from_single_image(monkeypatch, tmp_path):
    monkeypatch.setenv("DOCX_OUTPUT_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("DOCX_INCLUDE_TITLE", "true")
    monkeypatch.setenv("DOCX_DEFAULT_TITLE", "Phase 6 DOCX")

    from app.models.file_asset import FileAsset
    from app.services.docx_service import create_docx_from_images

    source_path = tmp_path / "single.png"
    create_sample_image(source_path, "PNG")

    source_file = FileAsset(
        public_id="docx_file_1",
        original_filename="single.png",
        stored_filename="single.png",
        mime_type="image/png",
        extension="png",
        size_bytes=source_path.stat().st_size,
        storage_path=str(source_path),
    )

    result = create_docx_from_images([source_file])
    output_path = Path(result["output_path"])

    assert output_path.exists()
    assert output_path.suffix.lower() == ".docx"
    assert result["output_format"] == "docx"
    assert result["size_bytes"] > 0
    assert result["embedded_image_count"] == 1

    with ZipFile(output_path, "r") as archive:
        names = archive.namelist()
        assert "word/document.xml" in names
        assert any(name.startswith("word/media/") for name in names)


def test_conversion_router_writes_docx_result_rows(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)

    from app.extensions import db
    from app.models.file_asset import FileAsset
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult
    from app.services.conversion_router_service import run_phase3_conversion_job

    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    first_path = upload_dir / "first.png"
    second_path = upload_dir / "second.png"
    create_sample_image(first_path, "PNG")
    create_sample_image(second_path, "PNG")

    with app.app_context():
        file_one = FileAsset(
            public_id="docx_public_1",
            original_filename="first.png",
            stored_filename="first.png",
            mime_type="image/png",
            extension="png",
            size_bytes=first_path.stat().st_size,
            storage_path=str(first_path),
        )
        file_two = FileAsset(
            public_id="docx_public_2",
            original_filename="second.png",
            stored_filename="second.png",
            mime_type="image/png",
            extension="png",
            size_bytes=second_path.stat().st_size,
            storage_path=str(second_path),
        )
        db.session.add(file_one)
        db.session.add(file_two)
        db.session.commit()

        job = ConversionJob(
            public_id="job_docx_1",
            requested_output_format="docx",
            source_count=2,
            source_public_ids=["docx_public_1", "docx_public_2"],
            status="processing",
        )
        db.session.add(job)
        db.session.commit()

        summary = run_phase3_conversion_job("job_docx_1")

        result_rows = ConversionResult.query.filter_by(job_id=job.id).all()

        assert summary["converted_count"] == 1
        assert len(result_rows) == 1
        assert result_rows[0].status == "success"
        assert result_rows[0].output_format == "docx"
        assert result_rows[0].output_filename.endswith(".docx")
        assert Path(result_rows[0].output_path).exists()

        with ZipFile(result_rows[0].output_path, "r") as archive:
            names = archive.namelist()
            assert "word/document.xml" in names
            assert any(name.startswith("word/media/") for name in names)