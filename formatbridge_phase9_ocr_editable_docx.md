# FormatBridge — Phase 9: OCR and Editable DOCX Enhancement

## Objective
Add OCR workflows for scanned image text extraction.

This phase gives you:

- OCR preprocessing
- text extraction
- editable DOCX generation path
- an optional OCR toggle in the frontend when DOCX is selected

---

# Important note before you start

Phase 9 adds **one backend model change** so the queued job can remember whether OCR was requested.

That means this phase **does require a migration** for `conversion_jobs.ocr_enabled`.

It does **not** need:
- a new database name
- a new PostgreSQL user
- new DB grants
- a new Redis service

Keep using the exact identifiers already established in Phase 1–8:

```env
POSTGRES_DB=formatbridge_db
POSTGRES_USER=formatbridge_user
POSTGRES_PASSWORD=formatbridge_pass
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
DATABASE_URL=postgresql://formatbridge_user:formatbridge_pass@127.0.0.1:5433/formatbridge_db

REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

---

# Phase 9 exact additions to `.env`

Add these to your existing `.env` and `.env.example`:

```env
# =========================
# OCR
# =========================
OCR_LANGUAGES=eng
OCR_ENABLED_DEFAULT=false
OCR_MIN_TEXT_LENGTH=3
OCR_DOCX_INCLUDE_SOURCE_NAMES=true
OCR_DOCX_EMPTY_TEXT_PLACEHOLDER=[No readable text detected]
```

## Meaning
- `OCR_LANGUAGES=eng` -> Tesseract language pack to use
- `OCR_ENABLED_DEFAULT=false` -> OCR remains opt-in for DOCX jobs
- `OCR_MIN_TEXT_LENGTH=3` -> very short OCR output can be treated as empty
- `OCR_DOCX_INCLUDE_SOURCE_NAMES=true` -> include each source filename as a heading/paragraph
- `OCR_DOCX_EMPTY_TEXT_PLACEHOLDER=[No readable text detected]` -> fallback text when OCR finds nothing useful

---

# Required package additions

Add this to `backend/requirements.txt` if it is not already present:

```txt
pytesseract
pytest
```

Then install:

```bash
cd backend
source env/bin/activate
pip install -r requirements.txt
```

---

# Required system package on Debian / Kali / Ubuntu

`pytesseract` needs the Tesseract binary installed on the OS.

Run this:

```bash
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-eng
```

You can verify it with:

```bash
tesseract --version
```

---

# Files to Populate

## 1) `backend/app/services/ocr_service.py`

```python
from __future__ import annotations

import os
import time
import uuid
from pathlib import Path

import pytesseract
from docx import Document
from docx.shared import Pt
from PIL import Image, ImageFilter, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener
from werkzeug.utils import secure_filename

from app.models.file_asset import FileAsset

register_heif_opener()


def ensure_ocr_docx_output_directory(path: str | Path | None = None) -> Path:
    directory = Path(path or os.getenv("DOCX_OUTPUT_DIR", "app/temp_storage/converted"))
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_ocr_docx_filename(source_files: list[FileAsset]) -> str:
    timestamp = int(time.time())
    token = uuid.uuid4().hex[:8]

    if len(source_files) == 1:
        base_name = secure_filename(source_files[0].original_filename) or "file"
        stem = Path(base_name).stem or "file"
        return f"{stem}-ocr-{timestamp}-{token}.docx"

    return f"merged-ocr-{timestamp}-{token}.docx"


def preprocess_image_for_ocr(source_path: str | Path) -> Image.Image:
    try:
        with Image.open(source_path) as image:
            grayscale = ImageOps.grayscale(image)
            contrasted = ImageOps.autocontrast(grayscale)
            sharpened = contrasted.filter(ImageFilter.SHARPEN)
            return sharpened
    except UnidentifiedImageError as exc:
        raise ValueError(f"Unsupported or unreadable image file for OCR: {source_path}") from exc


def normalize_extracted_text(text: str) -> str:
    normalized = "\n".join(line.strip() for line in text.splitlines())
    normalized = "\n".join(line for line in normalized.splitlines() if line)
    min_length = int(os.getenv("OCR_MIN_TEXT_LENGTH", "3"))

    if len(normalized.strip()) < min_length:
        return os.getenv("OCR_DOCX_EMPTY_TEXT_PLACEHOLDER", "[No readable text detected]")

    return normalized.strip()


def extract_text_from_image(source_path: str | Path, languages: str | None = None) -> str:
    languages = languages or os.getenv("OCR_LANGUAGES", "eng")

    try:
        processed_image = preprocess_image_for_ocr(source_path)
        text = pytesseract.image_to_string(processed_image, lang=languages)
        return normalize_extracted_text(text)
    except pytesseract.pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR is not installed on this system. Install 'tesseract-ocr' first."
        ) from exc


def create_editable_docx_from_images(
    source_files: list[FileAsset],
    title: str | None = None,
    output_dir: str | Path | None = None,
) -> dict:
    if not source_files:
        raise ValueError("At least one source file is required to create an OCR DOCX.")

    output_directory = ensure_ocr_docx_output_directory(output_dir)
    output_filename = build_ocr_docx_filename(source_files)
    output_path = output_directory / output_filename

    document = Document()
    document_title = title or "OCR Extracted Text"
    document.add_heading(document_title, level=1)

    include_source_names = os.getenv("OCR_DOCX_INCLUDE_SOURCE_NAMES", "true").lower() == "true"
    extracted_sections = 0

    for source_file in source_files:
        file_path = Path(source_file.storage_path)
        if not file_path.exists():
            raise FileNotFoundError(
                f"Uploaded source file is missing on disk: {source_file.original_filename}"
            )

        extracted_text = extract_text_from_image(file_path)

        if include_source_names:
            document.add_paragraph(source_file.original_filename)

        for paragraph_text in extracted_text.split("\n"):
            paragraph = document.add_paragraph(paragraph_text)
            paragraph.paragraph_format.space_after = Pt(6)

        extracted_sections += 1

    document.save(output_path)

    return {
        "output_filename": output_filename,
        "output_path": str(output_path),
        "output_format": "docx",
        "size_bytes": output_path.stat().st_size,
        "extracted_section_count": extracted_sections,
    }
```

---

## 2) `backend/app/tasks/conversion_tasks.py`

Replace your current file with this version:

```python
from __future__ import annotations

from datetime import datetime

from celery.exceptions import Ignore

from app.extensions import celery_app, db
from app.models.conversion_job import ConversionJob
from app.services.conversion_router_service import run_phase3_conversion_job


def get_job_or_raise(job_public_id: str) -> ConversionJob:
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()
    if not job:
        raise ValueError(f"Conversion job '{job_public_id}' was not found.")
    return job


@celery_app.task(name="tasks.process_conversion_job")
def process_conversion_job_task(job_public_id: str):
    job = get_job_or_raise(job_public_id)

    try:
        job.status = "processing"
        job.started_at = datetime.utcnow()
        job.updated_at = datetime.utcnow()
        db.session.commit()

        summary = run_phase3_conversion_job(job_public_id)

        job = get_job_or_raise(job_public_id)
        job.status = "success"
        job.completed_at = datetime.utcnow()
        job.updated_at = datetime.utcnow()
        db.session.commit()

        return {
            "job_public_id": job_public_id,
            "status": "success",
            "summary": summary,
        }

    except Exception as exc:
        db.session.rollback()

        job = ConversionJob.query.filter_by(public_id=job_public_id).first()
        if job:
            job.status = "failed"
            job.error_message = str(exc)
            job.completed_at = datetime.utcnow()
            job.updated_at = datetime.utcnow()
            db.session.commit()

        raise Ignore() from exc
```

> Yes, this file is mostly unchanged. That is okay.  
> Phase 9 mainly extends the queued job data and routing logic, not the Celery task contract.

---

## 3) `frontend/src/components/conversion/OcrOptionToggle.jsx`

```jsx
export default function OcrOptionToggle({
  checked,
  onChange,
  disabled = false,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <label className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={checked}
          onChange={(event) => onChange(event.target.checked)}
          disabled={disabled}
          className="mt-1 h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
        />

        <div>
          <p className="text-sm font-semibold text-slate-900">
            Enable OCR for editable DOCX
          </p>
          <p className="mt-1 text-xs leading-5 text-slate-600">
            When enabled, the app extracts readable text from scanned images and
            writes that text into a DOCX file. When disabled, DOCX export keeps
            the original images embedded in the document.
          </p>
        </div>
      </label>
    </div>
  );
}
```

---

## 4) `backend/tests/test_conversions.py`

Replace your current file with this Phase 9 version:

```python
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
```

---

# Required supporting edits

These files were not in your Phase 9 list, but they are required for the phase to actually run cleanly.

---

## A) Update `backend/app/models/conversion_job.py`

Add a persisted OCR flag so the queue worker knows whether OCR was requested.

Replace your current file with this version:

```python
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ConversionJob(Base):
    __tablename__ = "conversion_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    public_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    requested_output_format: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    source_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_public_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)

    ocr_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="queued", index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    results = relationship(
        "ConversionResult",
        back_populates="job",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<ConversionJob id={self.id} public_id={self.public_id!r} "
            f"status={self.status!r} output={self.requested_output_format!r} "
            f"ocr_enabled={self.ocr_enabled}>"
        )
```

### Exact migration commands for this model change

From `backend/`:

```bash
source env/bin/activate
flask --app run.py db migrate -m "add ocr_enabled to conversion_jobs"
flask --app run.py db upgrade
```

---

## B) Update `backend/app/schemas/conversion_schema.py`

Replace your current file with this version:

```python
from __future__ import annotations

import os

from werkzeug.exceptions import BadRequest

from app.models.conversion_job import ConversionJob


def get_allowed_output_formats() -> set[str]:
    raw = os.getenv("ALLOWED_OUTPUT_FORMATS", "jpg,png,webp,pdf,docx")
    return {item.strip().lower() for item in raw.split(",") if item.strip()}


def validate_conversion_request(payload: dict) -> dict:
    file_public_ids = payload.get("file_public_ids")
    output_format = (payload.get("output_format") or "").strip().lower()
    ocr_enabled = bool(payload.get("ocr_enabled", False))

    if not isinstance(file_public_ids, list) or not file_public_ids:
        raise BadRequest("file_public_ids must be a non-empty list.")

    cleaned_ids: list[str] = []
    for item in file_public_ids:
        if not isinstance(item, str) or not item.strip():
            raise BadRequest("Each file_public_id must be a non-empty string.")
        cleaned_ids.append(item.strip())

    max_files = int(os.getenv("MAX_FILES_PER_UPLOAD", "10"))
    if len(cleaned_ids) > max_files:
        raise BadRequest(f"You can convert at most {max_files} files at once.")

    allowed_formats = get_allowed_output_formats()
    if output_format not in allowed_formats:
        allowed_display = ", ".join(sorted(allowed_formats))
        raise BadRequest(
            f"Unsupported output_format '{output_format}'. Allowed: {allowed_display}."
        )

    if ocr_enabled and output_format != "docx":
        raise BadRequest("OCR is only available when output_format is 'docx'.")

    return {
        "file_public_ids": cleaned_ids,
        "output_format": output_format,
        "ocr_enabled": ocr_enabled,
    }


def serialize_conversion_job_summary(job: ConversionJob) -> dict:
    return {
        "public_id": job.public_id,
        "requested_output_format": job.requested_output_format,
        "source_count": job.source_count,
        "source_public_ids": job.source_public_ids,
        "ocr_enabled": job.ocr_enabled,
        "status": job.status,
        "error_message": job.error_message,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
    }


def serialize_conversion_job_created(message: str, job: ConversionJob) -> dict:
    return {
        "message": message,
        "data": {
            "job": serialize_conversion_job_summary(job),
        },
    }
```

---

## C) Update `backend/app/api/v1/conversions.py`

Replace your current file with this version:

```python
import uuid

from flask import Blueprint, request
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.file_asset import FileAsset
from app.schemas.conversion_schema import (
    serialize_conversion_job_created,
    validate_conversion_request,
)
from app.tasks.conversion_tasks import process_conversion_job_task
from app.utils.response import success_response

conversions_bp = Blueprint("conversions", __name__, url_prefix="/conversions")


@conversions_bp.post("")
def create_conversion_job():
    payload = request.get_json(silent=True) or {}
    data = validate_conversion_request(payload)

    source_public_ids = data["file_public_ids"]
    requested_output_format = data["output_format"]
    ocr_enabled = data["ocr_enabled"]

    files = (
        FileAsset.query.filter(FileAsset.public_id.in_(source_public_ids))
        .order_by(FileAsset.id.asc())
        .all()
    )

    if len(files) != len(source_public_ids):
        found_ids = {file.public_id for file in files}
        missing_ids = [public_id for public_id in source_public_ids if public_id not in found_ids]
        raise NotFound(f"Some uploaded files were not found: {', '.join(missing_ids)}")

    job = ConversionJob(
        public_id=uuid.uuid4().hex,
        requested_output_format=requested_output_format,
        source_count=len(source_public_ids),
        source_public_ids=source_public_ids,
        ocr_enabled=ocr_enabled,
        status="queued",
    )

    db.session.add(job)
    db.session.commit()

    process_conversion_job_task.delay(job.public_id)

    payload = serialize_conversion_job_created(
        message="Conversion job created successfully.",
        job=job,
    )

    return success_response(
        message=payload["message"],
        data=payload["data"],
        status_code=202,
    )
```

---

## D) Update `backend/app/services/conversion_router_service.py`

Replace your current file with this Phase 9 version so OCR DOCX jobs route correctly.

```python
from __future__ import annotations

from pathlib import Path

from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult
from app.models.file_asset import FileAsset
from app.services.docx_service import create_docx_from_images
from app.services.image_conversion_service import convert_image_file
from app.services.ocr_service import create_editable_docx_from_images
from app.services.pdf_service import create_pdf_from_images


def get_job_or_raise(job_public_id: str) -> ConversionJob:
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()
    if not job:
        raise NotFound("Conversion job was not found.")
    return job


def get_ordered_source_files(job: ConversionJob) -> list[FileAsset]:
    source_files = (
        FileAsset.query.filter(FileAsset.public_id.in_(job.source_public_ids))
        .order_by(FileAsset.id.asc())
        .all()
    )

    source_map = {file.public_id: file for file in source_files}
    ordered_files: list[FileAsset] = []

    for public_id in job.source_public_ids:
        source_file = source_map.get(public_id)
        if not source_file:
            raise ValueError(f"Uploaded source file is missing from the database: {public_id}")
        ordered_files.append(source_file)

    return ordered_files


def create_processing_result(
    job: ConversionJob,
    source_file: FileAsset | None = None,
) -> ConversionResult:
    result = ConversionResult(
        job_id=job.id,
        source_file_id=source_file.id if source_file else None,
        output_format=job.requested_output_format,
        status="processing",
    )
    db.session.add(result)
    db.session.commit()
    return result


def mark_result_failed(result_id: int) -> None:
    result = db.session.get(ConversionResult, result_id)
    if not result:
        return

    result.status = "failed"
    db.session.commit()


def process_pdf_job(job: ConversionJob, source_files: list[FileAsset]) -> int:
    result = create_processing_result(job, source_file=None)

    try:
        converted = create_pdf_from_images(source_files)

        result = db.session.get(ConversionResult, result.id)
        result.status = "success"
        result.output_filename = converted["output_filename"]
        result.output_path = converted["output_path"]
        db.session.commit()

        return 1

    except Exception:
        db.session.rollback()
        mark_result_failed(result.id)
        raise


def process_docx_job(job: ConversionJob, source_files: list[FileAsset]) -> int:
    result = create_processing_result(job, source_file=None)

    try:
        if job.ocr_enabled:
            converted = create_editable_docx_from_images(source_files)
        else:
            converted = create_docx_from_images(source_files)

        result = db.session.get(ConversionResult, result.id)
        result.status = "success"
        result.output_filename = converted["output_filename"]
        result.output_path = converted["output_path"]
        db.session.commit()

        return 1

    except Exception:
        db.session.rollback()
        mark_result_failed(result.id)
        raise


def process_image_job(job: ConversionJob, source_files: list[FileAsset]) -> int:
    converted_count = 0

    for source_file in source_files:
        if not Path(source_file.storage_path).exists():
            raise FileNotFoundError(
                f"Uploaded source file is missing on disk: {source_file.original_filename}"
            )

        result = create_processing_result(job, source_file=source_file)

        try:
            converted = convert_image_file(
                source_path=source_file.storage_path,
                output_format=job.requested_output_format,
                original_filename=source_file.original_filename,
            )

            result = db.session.get(ConversionResult, result.id)
            result.status = "success"
            result.output_filename = converted["output_filename"]
            result.output_path = converted["output_path"]
            db.session.commit()

            converted_count += 1

        except Exception:
            db.session.rollback()
            mark_result_failed(result.id)
            raise

    return converted_count


def run_phase3_conversion_job(job_public_id: str) -> dict:
    """
    Kept with the same function name for compatibility with the existing Celery task.
    In Phase 9, this function routes image, PDF, DOCX, and OCR-DOCX jobs.
    """
    job = get_job_or_raise(job_public_id)
    source_files = get_ordered_source_files(job)

    for source_file in source_files:
        if not Path(source_file.storage_path).exists():
            raise FileNotFoundError(
                f"Uploaded source file is missing on disk: {source_file.original_filename}"
            )

    if job.requested_output_format == "pdf":
        converted_count = process_pdf_job(job, source_files)
    elif job.requested_output_format == "docx":
        converted_count = process_docx_job(job, source_files)
    else:
        converted_count = process_image_job(job, source_files)

    return {
        "job_public_id": job.public_id,
        "requested_output_format": job.requested_output_format,
        "ocr_enabled": job.ocr_enabled,
        "source_count": job.source_count,
        "converted_count": converted_count,
    }
```

---

## E) Update `frontend/src/services/jobService.js`

Replace your current file with this version:

```js
import { apiRequest } from "./apiClient";

export async function createConversionJob(filePublicIds, outputFormat, ocrEnabled = false) {
  return apiRequest("/conversions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      file_public_ids: filePublicIds,
      output_format: outputFormat,
      ocr_enabled: ocrEnabled,
    }),
  });
}

export async function fetchJobStatus(jobPublicId) {
  return apiRequest(`/jobs/${jobPublicId}`, {
    method: "GET",
  });
}
```

---

## F) Update `frontend/src/pages/ConvertPage.jsx`

Apply these targeted edits.

### 1. Add the new import

Add this near the other imports:

```jsx
import OcrOptionToggle from "../components/conversion/OcrOptionToggle";
```

### 2. Add OCR state

Add this near the other `useState` calls:

```jsx
const [ocrEnabled, setOcrEnabled] = useState(false);
```

### 3. Reset OCR when clearing

Inside `handleClear`, add:

```jsx
setOcrEnabled(false);
```

### 4. Reset OCR when output format is not DOCX

Add this import if it is not already present:

```jsx
import { useEffect, useMemo, useState } from "react";
```

Then add this hook inside the component:

```jsx
useEffect(() => {
  if (outputFormat !== "docx" && ocrEnabled) {
    setOcrEnabled(false);
  }
}, [outputFormat, ocrEnabled]);
```

### 5. Send the OCR flag when creating the job

Replace this block:

```jsx
const response = await createConversionJob(
  uploadedFiles.map((file) => file.public_id),
  outputFormat
);
```

with:

```jsx
const response = await createConversionJob(
  uploadedFiles.map((file) => file.public_id),
  outputFormat,
  ocrEnabled
);
```

### 6. Render the OCR toggle only when DOCX is selected

Place this directly below your `FormatSelector` in the upload-success section:

```jsx
{outputFormat === "docx" && (
  <OcrOptionToggle
    checked={ocrEnabled}
    onChange={setOcrEnabled}
    disabled={isCreatingJob}
  />
)}
```

---

# Exact migration commands

Because `conversion_job.py` is changed in this phase, run these exact commands:

```bash
cd backend
source env/bin/activate
flask --app run.py db migrate -m "add ocr_enabled to conversion_jobs"
flask --app run.py db upgrade
```

---

# Exact startup order after Phase 9 files are in place

## 1. Start infrastructure
From repo root:

```bash
cp .env.example .env
docker compose up -d postgres redis
```

## 2. Start backend
From `backend/`:

```bash
source env/bin/activate
pip install -r requirements.txt
python run.py
```

## 3. Start Celery worker
From `backend/` in a second terminal:

```bash
source env/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```

## 4. Start frontend
From `frontend/`:

```bash
npm install
npm run dev
```

---

# Exact test commands for Phase 9

From `backend/`:

```bash
source env/bin/activate
pytest tests/test_conversions.py -q
```

If you want verbose output:

```bash
pytest tests/test_conversions.py -v
```

---

# Completion Check

## Check 1 — scanned text is extracted into DOCX

Open:

```text
http://127.0.0.1:5173/convert
```

Then:
1. upload one or more scanned text images
2. choose `DOCX`
3. turn on the OCR option
4. create the conversion job
5. wait for `success`
6. download the DOCX result

Expected:
- the generated `.docx` opens in Word / LibreOffice
- extracted text appears as editable text inside the document
- the OCR path is text-first, not image-embedded

---

## Check 2 — OCR option is optional and clearly labeled

Expected in the frontend:
- the OCR checkbox only appears when `DOCX` is selected
- the label clearly explains what OCR does
- leaving OCR off keeps the previous image-embedded DOCX behavior
- turning OCR on uses the editable-text DOCX path

---

# Optional direct API flow test

## A) Upload source files

```bash
curl -X POST http://127.0.0.1:5000/api/v1/uploads \
  -F "files=@/absolute/path/to/scanned-page-1.png" \
  -F "files=@/absolute/path/to/scanned-page-2.png"
```

Copy the returned file `public_id` values.

## B) Create an OCR DOCX conversion job

```bash
curl -X POST http://127.0.0.1:5000/api/v1/conversions \
  -H "Content-Type: application/json" \
  -d '{
    "file_public_ids": ["PUT_FIRST_FILE_ID", "PUT_SECOND_FILE_ID"],
    "output_format": "docx",
    "ocr_enabled": true
  }'
```

Copy the returned job `public_id`.

## C) Poll job status

```bash
curl http://127.0.0.1:5000/api/v1/jobs/PUT_REAL_JOB_PUBLIC_ID_HERE
```

Expected:
- job summary includes `"ocr_enabled": true`
- status eventually becomes `success`

---

# What Phase 9 completes

Once this works, your project will have:

- OCR preprocessing for scanned images
- text extraction via Tesseract
- editable DOCX generation path
- optional OCR toggle in the frontend
- async queued OCR-DOCX processing

That is a proper Phase 9 foundation.

---

# Best next step after Phase 9

The next clean move is **Phase 10 — User Accounts and Conversion History**, where you add:

- sign up / login
- user-linked conversion history
- authenticated job ownership

That is the correct next stage after OCR enhancement is stable.
