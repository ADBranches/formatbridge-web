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

    from app.services.image_conversion_service import convert_image_file

    source_path = tmp_path / f"sample.{source_extension}"
    create_sample_image(source_path, source_format)

    result = convert_image_file(
        source_path=source_path,
        output_format=target_format,
        original_filename=source_path.name,
    )

    output_path = Path(result["output_path"])

    assert output_path.exists()
    assert output_path.suffix.lower() == f".{target_format}"
    assert result["output_format"] == target_format
    assert result["size_bytes"] > 0

    with Image.open(output_path) as converted_image:
        converted_image.load()
        assert converted_image.width == 64
        assert converted_image.height == 64


def build_test_app(monkeypatch, tmp_path):
    database_path = tmp_path / "phase9_test.db"

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


def test_create_editable_docx_from_images(monkeypatch, tmp_path):
    monkeypatch.setenv("DOCX_OUTPUT_DIR", str(tmp_path / "converted"))

    from app.models.file_asset import FileAsset
    from app.services import ocr_service

    source_path = tmp_path / "scan.png"
    create_sample_image(source_path, "PNG")

    source_file = FileAsset(
        public_id="ocr_file_1",
        original_filename="scan.png",
        stored_filename="scan.png",
        mime_type="image/png",
        extension="png",
        size_bytes=source_path.stat().st_size,
        storage_path=str(source_path),
    )

    monkeypatch.setattr(
        ocr_service,
        "extract_text_from_image",
        lambda *args, **kwargs: "Invoice Number 12345\nCustomer Name Example",
    )

    result = ocr_service.create_editable_docx_from_images([source_file])
    output_path = Path(result["output_path"])

    assert output_path.exists()
    assert output_path.suffix.lower() == ".docx"
    assert result["output_format"] == "docx"
    assert result["size_bytes"] > 0
    assert result["extracted_section_count"] == 1

    with ZipFile(output_path, "r") as archive:
        names = archive.namelist()
        assert "word/document.xml" in names
        document_xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
        assert "Invoice Number 12345" in document_xml
        assert "Customer Name Example" in document_xml


def test_conversion_router_writes_ocr_docx_result_rows(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)

    from app.extensions import db
    from app.models.file_asset import FileAsset
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult
    from app.services import ocr_service
    from app.services.conversion_router_service import run_phase3_conversion_job

    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    first_path = upload_dir / "scan-one.png"
    second_path = upload_dir / "scan-two.png"
    create_sample_image(first_path, "PNG")
    create_sample_image(second_path, "PNG")

    monkeypatch.setattr(
        ocr_service,
        "extract_text_from_image",
        lambda *args, **kwargs: "Detected OCR text for editable DOCX",
    )

    with app.app_context():
        file_one = FileAsset(
            public_id="ocr_public_1",
            original_filename="scan-one.png",
            stored_filename="scan-one.png",
            mime_type="image/png",
            extension="png",
            size_bytes=first_path.stat().st_size,
            storage_path=str(first_path),
        )
        file_two = FileAsset(
            public_id="ocr_public_2",
            original_filename="scan-two.png",
            stored_filename="scan-two.png",
            mime_type="image/png",
            extension="png",
            size_bytes=second_path.stat().st_size,
            storage_path=str(second_path),
        )
        db.session.add(file_one)
        db.session.add(file_two)
        db.session.commit()

        job = ConversionJob(
            public_id="job_ocr_docx_1",
            requested_output_format="docx",
            source_count=2,
            source_public_ids=["ocr_public_1", "ocr_public_2"],
            status="processing",
            ocr_enabled=True,
        )
        db.session.add(job)
        db.session.commit()

        summary = run_phase3_conversion_job("job_ocr_docx_1")

        result_rows = ConversionResult.query.filter_by(job_id=job.id).all()

        assert summary["converted_count"] == 1
        assert len(result_rows) == 1
        assert result_rows[0].status == "success"
        assert result_rows[0].output_format == "docx"
        assert result_rows[0].output_filename.endswith(".docx")
        assert Path(result_rows[0].output_path).exists()

        with ZipFile(result_rows[0].output_path, "r") as archive:
            document_xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
            assert "Detected OCR text for editable DOCX" in document_xml