from __future__ import annotations

from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener
from pypdf import PdfReader

register_heif_opener()


def create_sample_image(path: Path, image_format: str, color: tuple[int, int, int]) -> Path:
    image = Image.new("RGB", (64, 64), color)

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


def build_test_app(monkeypatch, tmp_path):
    database_path = tmp_path / "phase5_test.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("PDF_OUTPUT_DIR", str(tmp_path / "converted"))
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


def test_single_image_pdf_generation(monkeypatch, tmp_path):
    monkeypatch.setenv("PDF_OUTPUT_DIR", str(tmp_path / "converted"))

    from app.models.file_asset import FileAsset
    from app.services.pdf_service import create_pdf_from_images

    source_path = tmp_path / "single.png"
    create_sample_image(source_path, "PNG", (20, 140, 220))

    source_file = FileAsset(
        public_id="single_public_id",
        original_filename="single.png",
        stored_filename="single.png",
        mime_type="image/png",
        extension="png",
        size_bytes=source_path.stat().st_size,
        storage_path=str(source_path),
    )

    result = create_pdf_from_images([source_file])
    output_path = Path(result["output_path"])

    assert output_path.exists()
    assert output_path.suffix.lower() == ".pdf"
    assert result["output_format"] == "pdf"
    assert result["size_bytes"] > 0
    assert result["page_count"] == 1

    reader = PdfReader(str(output_path))
    assert len(reader.pages) == 1


def test_multi_image_pdf_merge_preserves_order_by_page_count(monkeypatch, tmp_path):
    monkeypatch.setenv("PDF_OUTPUT_DIR", str(tmp_path / "converted"))

    from app.models.file_asset import FileAsset
    from app.services.pdf_service import create_pdf_from_images

    first_path = tmp_path / "01-first.png"
    second_path = tmp_path / "02-second.png"
    third_path = tmp_path / "03-third.png"

    create_sample_image(first_path, "PNG", (255, 0, 0))
    create_sample_image(second_path, "PNG", (0, 255, 0))
    create_sample_image(third_path, "PNG", (0, 0, 255))

    source_files = [
        FileAsset(
            public_id="file_1",
            original_filename="01-first.png",
            stored_filename="01-first.png",
            mime_type="image/png",
            extension="png",
            size_bytes=first_path.stat().st_size,
            storage_path=str(first_path),
        ),
        FileAsset(
            public_id="file_2",
            original_filename="02-second.png",
            stored_filename="02-second.png",
            mime_type="image/png",
            extension="png",
            size_bytes=second_path.stat().st_size,
            storage_path=str(second_path),
        ),
        FileAsset(
            public_id="file_3",
            original_filename="03-third.png",
            stored_filename="03-third.png",
            mime_type="image/png",
            extension="png",
            size_bytes=third_path.stat().st_size,
            storage_path=str(third_path),
        ),
    ]

    result = create_pdf_from_images(source_files)
    output_path = Path(result["output_path"])

    assert output_path.exists()
    assert result["page_count"] == 3

    reader = PdfReader(str(output_path))
    assert len(reader.pages) == 3


def test_pdf_download_endpoint_returns_generated_file(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)

    from app.extensions import db
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult

    converted_dir = tmp_path / "converted"
    converted_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = converted_dir / "ready.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%Phase5 test PDF\n")

    with app.app_context():
        job = ConversionJob(
            public_id="job_pdf_1",
            requested_output_format="pdf",
            source_count=2,
            source_public_ids=["a", "b"],
            status="success",
        )
        db.session.add(job)
        db.session.commit()

        result = ConversionResult(
            job_id=job.id,
            source_file_id=None,
            output_format="pdf",
            status="success",
            output_filename="ready.pdf",
            output_path=str(pdf_path),
        )
        db.session.add(result)
        db.session.commit()

        result_id = result.id

    client = app.test_client()
    response = client.get(f"/api/v1/downloads/results/{result_id}")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/pdf")
    assert "attachment" in response.headers.get("Content-Disposition", "")