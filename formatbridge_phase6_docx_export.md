# FormatBridge — Phase 6: DOCX Export

## Objective
Support image-to-DOCX export for the MVP.

This phase gives you:

- image embedded in DOCX
- optional title and spacing rules
- downloadable DOCX output
- worker routing for DOCX jobs

---

# Important note before you start

Phase 6 does **not** need:

- a new database name
- a new PostgreSQL user
- new DB grants
- a new Redis service
- a new migration

Keep using the exact identifiers already established in Phase 1–5:

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

No new DB permission grant is needed if you are still using the PostgreSQL service already created in Phase 1.

---

# Phase 6 exact additions to `.env`

Add these to your existing `.env` and `.env.example`:

```env
# =========================
# DOCX
# =========================
DOCX_OUTPUT_DIR=app/temp_storage/converted
DOCX_IMAGE_MAX_WIDTH_INCHES=6.5
DOCX_INCLUDE_TITLE=true
DOCX_DEFAULT_TITLE=Converted Images
DOCX_IMAGE_SPACING_AFTER_PT=12
```

## Meaning
- `DOCX_OUTPUT_DIR=app/temp_storage/converted` -> DOCX files are saved alongside other converted outputs
- `DOCX_IMAGE_MAX_WIDTH_INCHES=6.5` -> max image width inside the Word document
- `DOCX_INCLUDE_TITLE=true` -> include a heading near the top of the document
- `DOCX_DEFAULT_TITLE=Converted Images` -> default heading text
- `DOCX_IMAGE_SPACING_AFTER_PT=12` -> spacing after each inserted image paragraph

---

# Required package additions

Add this to `backend/requirements.txt` if it is not already present:

```txt
python-docx
pytest
```

Then install:

```bash
cd backend
source env/bin/activate
pip install -r requirements.txt
```

Keep the existing Phase 4 and Phase 5 packages too.

---

# Files to Populate

## 1) `backend/app/services/docx_service.py`

```python
from __future__ import annotations

import os
import time
import uuid
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt
from PIL import Image
from pillow_heif import register_heif_opener
from werkzeug.utils import secure_filename

from app.models.file_asset import FileAsset

register_heif_opener()


def ensure_docx_output_directory(path: str | Path | None = None) -> Path:
    directory = Path(path or os.getenv("DOCX_OUTPUT_DIR", "app/temp_storage/converted"))
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_docx_filename(source_files: list[FileAsset]) -> str:
    timestamp = int(time.time())
    token = uuid.uuid4().hex[:8]

    if len(source_files) == 1:
        base_name = secure_filename(source_files[0].original_filename) or "file"
        stem = Path(base_name).stem or "file"
        return f"{stem}-{timestamp}-{token}.docx"

    return f"merged-{timestamp}-{token}.docx"


def get_image_width_inches(image_path: str | Path, max_width_inches: float) -> float:
    with Image.open(image_path) as image:
        width_px, height_px = image.size
        if width_px <= 0 or height_px <= 0:
            return max_width_inches

        dpi = image.info.get("dpi", (96, 96))[0] or 96
        width_inches = width_px / dpi if dpi else width_px / 96

        if width_inches <= 0:
            return max_width_inches

        return min(width_inches, max_width_inches)


def create_docx_from_images(
    source_files: list[FileAsset],
    title: str | None = None,
    output_dir: str | Path | None = None,
) -> dict:
    if not source_files:
        raise ValueError("At least one source file is required to create a DOCX.")

    output_directory = ensure_docx_output_directory(output_dir)
    output_filename = build_docx_filename(source_files)
    output_path = output_directory / output_filename

    document = Document()

    include_title = os.getenv("DOCX_INCLUDE_TITLE", "true").lower() == "true"
    effective_title = title or os.getenv("DOCX_DEFAULT_TITLE", "Converted Images")

    if include_title:
        document.add_heading(effective_title, level=1)

    max_width_inches = float(os.getenv("DOCX_IMAGE_MAX_WIDTH_INCHES", "6.5"))
    spacing_after_pt = int(os.getenv("DOCX_IMAGE_SPACING_AFTER_PT", "12"))

    inserted_count = 0

    for source_file in source_files:
        file_path = Path(source_file.storage_path)
        if not file_path.exists():
            raise FileNotFoundError(
                f"Uploaded source file is missing on disk: {source_file.original_filename}"
            )

        document.add_paragraph(source_file.original_filename)

        width_inches = get_image_width_inches(file_path, max_width_inches)

        image_paragraph = document.add_paragraph()
        run = image_paragraph.add_run()
        run.add_picture(str(file_path), width=Inches(width_inches))
        image_paragraph.paragraph_format.space_after = Pt(spacing_after_pt)

        inserted_count += 1

    document.save(output_path)

    return {
        "output_filename": output_filename,
        "output_path": str(output_path),
        "output_format": "docx",
        "size_bytes": output_path.stat().st_size,
        "embedded_image_count": inserted_count,
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

> Yes, this file is mostly the same as Phase 5. That is okay.  
> Phase 6 mainly extends the routing and generation services, not the Celery task contract.

---

## 3) `backend/tests/test_conversions.py`

Replace your current file with this Phase 6 version:

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
    database_path = tmp_path / "phase6_test.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("PDF_OUTPUT_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("DOCX_OUTPUT_DIR", str(tmp_path / "converted"))
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
```

---

# Required supporting edits

These files were not in your Phase 6 list, but they are required for the phase to actually run cleanly.

---

## A) Create `backend/app/services/conversion_router_service.py` update

Replace your current file with this Phase 6 version so DOCX jobs are routed correctly.

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
    In Phase 6, this function routes image, PDF, and DOCX jobs to the correct service.
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
        "source_count": job.source_count,
        "converted_count": converted_count,
    }
```

---

## B) Update `backend/app/api/v1/downloads.py`

Replace your current file with this version so DOCX downloads get the correct MIME type:

```python
from pathlib import Path

from flask import Blueprint, send_file
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_result import ConversionResult

downloads_bp = Blueprint("downloads", __name__, url_prefix="/downloads")

DOCX_MIMETYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


@downloads_bp.get("/results/<int:result_id>")
def download_result(result_id: int):
    result = db.session.get(ConversionResult, result_id)

    if not result:
        raise NotFound("Conversion result was not found.")

    if result.status != "success":
        raise NotFound("Conversion result is not ready for download.")

    if not result.output_path:
        raise NotFound("No output path is recorded for this conversion result.")

    file_path = Path(result.output_path)
    if not file_path.exists():
        raise NotFound("Generated output file is missing on disk.")

    mimetype = None
    if result.output_format == "pdf":
        mimetype = "application/pdf"
    elif result.output_format == "docx":
        mimetype = DOCX_MIMETYPE

    return send_file(
        file_path,
        as_attachment=True,
        download_name=result.output_filename or file_path.name,
        mimetype=mimetype,
    )
```

---

## C) Frontend note

Your Phase 5 `FormatSelector.jsx` and `ConvertPage.jsx` already include `DOCX` in the output options.

So no frontend file change is required in this phase unless you want to add DOCX-specific helper text.

---

# Exact migration command status

No new DB migration is required for Phase 6.

Reason:
- you are reusing the existing `conversion_results` table
- `output_filename` and `output_path` already exist
- DOCX export is a service-routing phase, not a schema-change phase

---

# Exact startup order after Phase 6 files are in place

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

# Exact test commands for Phase 6

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

## Check 1 — DOCX opens in Word / LibreOffice

Open:

```text
http://127.0.0.1:5173/convert
```

Then:
1. upload one or more valid images
2. choose `DOCX`
3. create the conversion job
4. wait for `success`
5. click the download button

Expected:
- a `.docx` file downloads
- the file opens in Microsoft Word or LibreOffice Writer

---

## Check 2 — embedded images render correctly

Expected inside the downloaded `.docx`:
- image filenames appear as paragraphs
- images are embedded beneath those lines
- spacing between images is visible
- optional title appears if `DOCX_INCLUDE_TITLE=true`

---

# Optional direct API flow test

## A) Upload source files

```bash
curl -X POST http://127.0.0.1:5000/api/v1/uploads \
  -F "files=@/absolute/path/to/first.png" \
  -F "files=@/absolute/path/to/second.png"
```

Copy the returned file `public_id` values.

## B) Create a DOCX conversion job

```bash
curl -X POST http://127.0.0.1:5000/api/v1/conversions \
  -H "Content-Type: application/json" \
  -d '{
    "file_public_ids": ["PUT_FIRST_FILE_ID", "PUT_SECOND_FILE_ID"],
    "output_format": "docx"
  }'
```

Copy the returned job `public_id`.

## C) Poll job status

```bash
curl http://127.0.0.1:5000/api/v1/jobs/PUT_REAL_JOB_PUBLIC_ID_HERE
```

When the job is successful, copy the first result `id`.

## D) Download the generated DOCX

```bash
curl -L http://127.0.0.1:5000/api/v1/downloads/results/PUT_RESULT_ID_HERE -o converted.docx
```

Expected:
- `converted.docx` is downloaded locally
- it opens correctly in Word / LibreOffice

---

# Exact SQL checks

Check the newest results:

```bash
docker exec -it formatbridge_postgres psql -U formatbridge_user -d formatbridge_db -c "SELECT id, job_id, source_file_id, output_format, status, output_filename, output_path, created_at FROM conversion_results ORDER BY id DESC;"
```

For a DOCX job, expect:
- one result row
- `source_file_id` may be `NULL`
- `output_format = 'docx'`
- `status = 'success'`

---

# What Phase 6 completes

Once this works, your project will have:

- image -> DOCX export
- optional title and spacing rules
- embedded images inside `.docx`
- downloadable DOCX results through the same download endpoint
- backend routing for DOCX jobs

That is a proper Phase 6 foundation.

---

# Best next step after Phase 6

The next clean move is **Phase 7 — Batch Results and ZIP Packaging**, where you add:

- ZIP packaging of multiple outputs
- job-level bulk download
- results summary screen improvements

That is the correct next stage after DOCX export is stable.
