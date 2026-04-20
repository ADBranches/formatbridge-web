# FormatBridge — Phase 4: Core Image Conversion Engine

## Objective
Implement actual image-to-image conversion workflows.

This phase gives you:

- real conversion logic via **Pillow** and **pillow-heif**
- output file generation on disk
- `conversion_results` rows written to the database
- worker-driven jobs that now do actual image conversion instead of only queue simulation

---

# Important note before you start

Phase 4 does **not** need a new database name, a new database user, or new PostgreSQL grants.

Keep using the exact identifiers already established in Phase 1–3:

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

# Phase 4 exact additions to `.env`

Add these to your existing `.env` and `.env.example`:

```env
# =========================
# IMAGE CONVERSION
# =========================
CONVERTED_DIR=app/temp_storage/converted
JPG_QUALITY=95
WEBP_QUALITY=95
```

## Meaning
- `CONVERTED_DIR=app/temp_storage/converted` → folder for generated image outputs
- `JPG_QUALITY=95` → JPEG save quality
- `WEBP_QUALITY=95` → WEBP save quality

---

# Required package additions

Add these to `backend/requirements.txt` if they are not already present:

```txt
Pillow
pillow-heif
pytest
```

Then install:

```bash
cd backend
source env/bin/activate
pip install -r requirements.txt
```

---

# Create required folder for outputs

Run this once:

```bash
mkdir -p backend/app/temp_storage/converted
```

---

# Files to Populate

## 1) `backend/app/services/image_conversion_service.py`

```python
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageSequence, UnidentifiedImageError
from pillow_heif import register_heif_opener

from app.utils.naming import build_converted_filename, ensure_directory

register_heif_opener()

SUPPORTED_IMAGE_CONVERSION_RULES: dict[str, set[str]] = {
    "heic": {"jpg", "png"},
    "heif": {"jpg", "png"},
    "jpg": {"jpg", "png", "webp"},
    "jpeg": {"jpg", "png", "webp"},
    "png": {"jpg", "png", "webp"},
    "webp": {"jpg", "png", "webp"},
}


def get_source_extension(source_path: str | Path) -> str:
    return Path(source_path).suffix.lower().replace(".", "")


def is_supported_conversion(input_extension: str, output_format: str) -> bool:
    return output_format.lower() in SUPPORTED_IMAGE_CONVERSION_RULES.get(
        input_extension.lower(), set()
    )


def open_image_copy(source_path: str | Path) -> Image.Image:
    try:
        with Image.open(source_path) as image:
            first_frame = next(ImageSequence.Iterator(image), image)
            return first_frame.copy()
    except UnidentifiedImageError as exc:
        raise ValueError(f"Unsupported or unreadable image file: {source_path}") from exc


def prepare_image_for_output(image: Image.Image, output_format: str) -> Image.Image:
    output_format = output_format.lower()

    if output_format == "jpg":
        if image.mode in ("RGBA", "LA"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            alpha_channel = image.getchannel("A")
            background.paste(image.convert("RGBA"), mask=alpha_channel)
            return background

        if image.mode == "P":
            converted = image.convert("RGBA")
            background = Image.new("RGB", converted.size, (255, 255, 255))
            alpha_channel = converted.getchannel("A")
            background.paste(converted, mask=alpha_channel)
            return background

        if image.mode != "RGB":
            return image.convert("RGB")

        return image

    if output_format == "png":
        if image.mode not in ("RGB", "RGBA"):
            return image.convert("RGBA" if "A" in image.getbands() else "RGB")
        return image

    if output_format == "webp":
        if image.mode not in ("RGB", "RGBA"):
            return image.convert("RGBA" if "A" in image.getbands() else "RGB")
        return image

    raise ValueError(f"Unsupported output format: {output_format}")


def get_save_kwargs(output_format: str) -> dict:
    output_format = output_format.lower()

    if output_format == "jpg":
        return {
            "format": "JPEG",
            "quality": int(os.getenv("JPG_QUALITY", "95")),
            "optimize": True,
        }

    if output_format == "png":
        return {
            "format": "PNG",
            "optimize": True,
        }

    if output_format == "webp":
        return {
            "format": "WEBP",
            "quality": int(os.getenv("WEBP_QUALITY", "95")),
            "method": 6,
        }

    raise ValueError(f"Unsupported output format: {output_format}")


def convert_image_file(
    source_path: str | Path,
    output_format: str,
    original_filename: str | None = None,
    output_dir: str | Path | None = None,
) -> dict:
    source_path = Path(source_path)
    if not source_path.exists():
        raise FileNotFoundError(f"Source file does not exist: {source_path}")

    input_extension = get_source_extension(source_path)
    output_format = output_format.lower()

    if not is_supported_conversion(input_extension, output_format):
        raise ValueError(
            f"Unsupported conversion: {input_extension.upper()} -> {output_format.upper()}"
        )

    output_directory = ensure_directory(
        output_dir or os.getenv("CONVERTED_DIR", "app/temp_storage/converted")
    )

    base_filename = original_filename or source_path.name
    output_filename = build_converted_filename(base_filename, output_format)
    output_path = output_directory / output_filename

    image = open_image_copy(source_path)
    prepared_image = prepare_image_for_output(image, output_format)
    prepared_image.save(output_path, **get_save_kwargs(output_format))

    return {
        "output_filename": output_filename,
        "output_path": str(output_path),
        "output_format": output_format,
        "size_bytes": output_path.stat().st_size,
    }
```

---

## 2) `backend/app/services/conversion_router_service.py`

Replace your Phase 3 stub with this Phase 4 version.

```python
from __future__ import annotations

from pathlib import Path

from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult
from app.models.file_asset import FileAsset
from app.services.image_conversion_service import convert_image_file


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


def create_processing_result(job: ConversionJob, source_file: FileAsset) -> ConversionResult:
    result = ConversionResult(
        job_id=job.id,
        source_file_id=source_file.id,
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


def run_phase3_conversion_job(job_public_id: str) -> dict:
    """
    Kept with the same function name for compatibility with the Phase 3 Celery task.
    In Phase 4, this function now performs real image conversion.
    """
    job = get_job_or_raise(job_public_id)
    source_files = get_ordered_source_files(job)

    converted_count = 0

    for source_file in source_files:
        if not Path(source_file.storage_path).exists():
            raise FileNotFoundError(
                f"Uploaded source file is missing on disk: {source_file.original_filename}"
            )

        result = create_processing_result(job, source_file)

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

    return {
        "job_public_id": job.public_id,
        "requested_output_format": job.requested_output_format,
        "source_count": job.source_count,
        "converted_count": converted_count,
    }
```

---

## 3) `backend/app/utils/naming.py`

```python
from __future__ import annotations

import time
import uuid
from pathlib import Path

from werkzeug.utils import secure_filename

OUTPUT_EXTENSION_MAP = {
    "jpg": "jpg",
    "png": "png",
    "webp": "webp",
}


def get_output_extension(output_format: str) -> str:
    normalized = output_format.lower()
    if normalized not in OUTPUT_EXTENSION_MAP:
        raise ValueError(f"Unsupported output format: {output_format}")
    return OUTPUT_EXTENSION_MAP[normalized]


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_converted_filename(original_filename: str, output_format: str) -> str:
    safe_name = secure_filename(original_filename) or "file"
    base_stem = Path(safe_name).stem or "file"
    timestamp = int(time.time())
    token = uuid.uuid4().hex[:8]
    extension = get_output_extension(output_format)

    return f"{base_stem}-{timestamp}-{token}.{extension}"
```

---

## 4) `backend/tests/test_conversions.py`

```python
from __future__ import annotations

from pathlib import Path

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
    database_path = tmp_path / "phase4_test.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
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


def test_conversion_router_writes_result_rows(monkeypatch, tmp_path):
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
```

---

# Required supporting edits

These files were not in your Phase 4 list, but they are required for the phase to actually run cleanly.

---

## A) Update `backend/requirements.txt`

Append these if missing:

```txt
Pillow
pillow-heif
pytest
```

---

## B) No change is required in `backend/app/tasks/conversion_tasks.py`

Your Phase 3 task can stay as it is **because the router function name is intentionally preserved**:

```python
run_phase3_conversion_job(job_public_id)
```

In Phase 4, that same function now performs real image conversion.

---

## C) No new database migration is required for Phase 4

Phase 4 uses the Phase 3 tables you already created:

- `file_assets`
- `conversion_jobs`
- `conversion_results`

You are **not** adding new DB columns in this phase.

---

# Exact startup order after Phase 4 files are in place

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

# Exact test commands for Phase 4

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

## Check 1 — each supported conversion returns valid output

Open:

```text
http://127.0.0.1:5173/convert
```

Then:
1. upload a valid source image
2. choose one of the supported output formats
3. create the conversion job

Use these valid combinations:

- HEIC → JPG
- HEIC → PNG
- JPG / JPEG → JPG
- JPG / JPEG → PNG
- JPG / JPEG → WEBP
- PNG → JPG
- PNG → PNG
- PNG → WEBP
- WEBP → JPG
- WEBP → PNG
- WEBP → WEBP

Expected:
- worker finishes with `success`
- `conversion_results` row is written
- output file exists on disk in `backend/app/temp_storage/converted`

---

## Check 2 — converted files open correctly

Run this exact SQL check:

```bash
docker exec -it formatbridge_postgres psql -U formatbridge_user -d formatbridge_db -c "SELECT id, job_id, output_format, status, output_filename, output_path, created_at FROM conversion_results ORDER BY id DESC;"
```

Then inspect one generated file directly, for example:

```bash
file backend/app/temp_storage/converted/PUT_REAL_OUTPUT_FILENAME_HERE
```

Expected:
- JPG outputs are detected as JPEG image data
- PNG outputs are detected as PNG image data
- WEBP outputs are detected as WebP image data

---

# Optional direct API flow test

## A) Upload a source file

```bash
curl -X POST http://127.0.0.1:5000/api/v1/uploads \
  -F "files=@/absolute/path/to/sample.png"
```

Copy the returned `public_id`.

## B) Create a conversion job

```bash
curl -X POST http://127.0.0.1:5000/api/v1/conversions \
  -H "Content-Type: application/json" \
  -d '{
    "file_public_ids": ["PUT_REAL_FILE_PUBLIC_ID_HERE"],
    "output_format": "webp"
  }'
```

Copy the returned job `public_id`.

## C) Poll job status

```bash
curl http://127.0.0.1:5000/api/v1/jobs/PUT_REAL_JOB_PUBLIC_ID_HERE
```

Expected:
- initial `queued`
- then `processing`
- then `success`

---

# What Phase 4 completes

Once this works, your project will have:

- real HEIC / HEIF input support
- real JPG / JPEG / PNG / WEBP image conversion
- generated output files written to disk
- `conversion_results` database rows written per source file
- Celery workers performing actual image processing

That is a proper Phase 4 foundation.

---

# Best next step after Phase 4

The next clean move is **Phase 5 — PDF Generation and Multi-Image PDF Merge**, where you add:

- image → PDF
- multiple images merged into one PDF
- downloadable PDF output flow

That is the correct next stage after image-to-image conversion is stable.
