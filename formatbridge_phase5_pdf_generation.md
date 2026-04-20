# FormatBridge — Phase 5: PDF Generation and Multi-Image PDF Merge

## Objective
Support image-to-PDF and multi-image PDF export.

This phase gives you:

- single image -> PDF
- multiple images -> one merged PDF
- preserved source-file order in merged PDF output
- downloadable PDF results through a backend download endpoint

---

# Important note before you start

Phase 5 does **not** need:

- a new database name
- a new PostgreSQL user
- new DB grants
- a new Redis service
- a new Flask secret key

Keep using the exact identifiers already established in Phase 1–4:

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

# Phase 5 exact additions to `.env`

Add these to your existing `.env` and `.env.example`:

```env
# =========================
# PDF
# =========================
PDF_OUTPUT_DIR=app/temp_storage/converted
PDF_IMAGE_RESOLUTION=100.0
```

## Meaning
- `PDF_OUTPUT_DIR=app/temp_storage/converted` -> PDF outputs will be saved in the same converted output directory
- `PDF_IMAGE_RESOLUTION=100.0` -> export resolution used when Pillow writes PDFs

---

# Required package additions

Add these to `backend/requirements.txt` if they are not already present:

```txt
pypdf
pytest
```

Then install:

```bash
cd backend
source env/bin/activate
pip install -r requirements.txt
```

`Pillow` and `pillow-heif` should already exist from Phase 4. Keep them.

---

# Create required frontend directory

Run this once if it does not exist:

```bash
mkdir -p frontend/src/components/conversion
```

---

# Files to Populate

## 1) `backend/app/services/pdf_service.py`

```python
from __future__ import annotations

import os
import time
import uuid
from pathlib import Path

from PIL import Image, ImageSequence, UnidentifiedImageError
from pillow_heif import register_heif_opener
from werkzeug.utils import secure_filename

from app.models.file_asset import FileAsset

register_heif_opener()


def ensure_pdf_output_directory(path: str | Path | None = None) -> Path:
    directory = Path(path or os.getenv("PDF_OUTPUT_DIR", "app/temp_storage/converted"))
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_pdf_filename(source_files: list[FileAsset]) -> str:
    timestamp = int(time.time())
    token = uuid.uuid4().hex[:8]

    if len(source_files) == 1:
        base_name = secure_filename(source_files[0].original_filename) or "file"
        stem = Path(base_name).stem or "file"
        return f"{stem}-{timestamp}-{token}.pdf"

    return f"merged-{timestamp}-{token}.pdf"


def flatten_image_for_pdf(image: Image.Image) -> Image.Image:
    if image.mode == "RGB":
        return image.copy()

    if image.mode in ("RGBA", "LA"):
        rgba_image = image.convert("RGBA")
        background = Image.new("RGB", rgba_image.size, (255, 255, 255))
        background.paste(rgba_image, mask=rgba_image.getchannel("A"))
        return background

    if image.mode == "P":
        rgba_image = image.convert("RGBA")
        background = Image.new("RGB", rgba_image.size, (255, 255, 255))
        background.paste(rgba_image, mask=rgba_image.getchannel("A"))
        return background

    return image.convert("RGB")


def open_pdf_ready_image(source_path: str | Path) -> Image.Image:
    try:
        with Image.open(source_path) as image:
            first_frame = next(ImageSequence.Iterator(image), image)
            return flatten_image_for_pdf(first_frame)
    except UnidentifiedImageError as exc:
        raise ValueError(f"Unsupported or unreadable image file: {source_path}") from exc


def create_pdf_from_images(
    source_files: list[FileAsset],
    output_dir: str | Path | None = None,
) -> dict:
    if not source_files:
        raise ValueError("At least one source file is required to create a PDF.")

    output_directory = ensure_pdf_output_directory(output_dir)
    output_filename = build_pdf_filename(source_files)
    output_path = output_directory / output_filename

    prepared_images: list[Image.Image] = []

    try:
        for source_file in source_files:
            file_path = Path(source_file.storage_path)
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Uploaded source file is missing on disk: {source_file.original_filename}"
                )

            prepared_images.append(open_pdf_ready_image(file_path))

        first_image, *remaining_images = prepared_images

        first_image.save(
            output_path,
            format="PDF",
            save_all=True,
            append_images=remaining_images,
            resolution=float(os.getenv("PDF_IMAGE_RESOLUTION", "100.0")),
        )

        return {
            "output_filename": output_filename,
            "output_path": str(output_path),
            "output_format": "pdf",
            "size_bytes": output_path.stat().st_size,
            "page_count": len(prepared_images),
        }

    finally:
        for image in prepared_images:
            image.close()
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

---

## 3) `frontend/src/components/conversion/FormatSelector.jsx`

```jsx
const DEFAULT_OPTIONS = ["jpg", "png", "webp", "pdf", "docx"];

export default function FormatSelector({
  value,
  onChange,
  options = DEFAULT_OPTIONS,
  label = "Output format",
  disabled = false,
}) {
  return (
    <div>
      <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-600">
        {label}
      </label>

      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
        className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm text-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {options.map((format) => (
          <option key={format} value={format}>
            {format.toUpperCase()}
          </option>
        ))}
      </select>
    </div>
  );
}
```

---

## 4) `frontend/src/components/conversion/ConversionSummary.jsx`

```jsx
const API_BASE_URL = "http://127.0.0.1:5000/api/v1";

function buildDownloadUrl(resultId) {
  return `${API_BASE_URL}/downloads/results/${resultId}`;
}

export default function ConversionSummary({ job, results = [] }) {
  if (!job) return null;

  const successfulResults = results.filter((result) => result.status === "success");
  const failedResults = results.filter((result) => result.status === "failed");

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Conversion summary
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Review generated outputs and download completed results.
          </p>
        </div>

        <span className="inline-flex rounded-full border border-slate-200 bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
          {job.requested_output_format?.toUpperCase()}
        </span>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Job status</p>
          <p className="mt-1 text-sm font-medium text-slate-900">{job.status}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Successful outputs</p>
          <p className="mt-1 text-sm font-medium text-slate-900">
            {successfulResults.length}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Failed outputs</p>
          <p className="mt-1 text-sm font-medium text-slate-900">
            {failedResults.length}
          </p>
        </div>
      </div>

      <div className="mt-6 space-y-4">
        {successfulResults.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
            No downloadable outputs yet.
          </div>
        ) : (
          successfulResults.map((result) => (
            <div
              key={result.id}
              className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4"
            >
              <p className="text-sm font-semibold text-slate-900">
                {result.output_filename || "Generated output"}
              </p>
              <p className="mt-1 text-xs text-slate-600">
                Format: {result.output_format?.toUpperCase()}
              </p>

              <div className="mt-4">
                <a
                  href={buildDownloadUrl(result.id)}
                  className="inline-flex rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"
                >
                  Download result
                </a>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
```

---

## 5) `backend/tests/test_downloads.py`

```python
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
```

---

# Required supporting edits

These files were not in your Phase 5 list, but they are required for the phase to actually run cleanly.

---

## A) Create `backend/app/api/v1/downloads.py`

```python
from pathlib import Path

from flask import Blueprint, send_file
from werkzeug.exceptions import NotFound

from app.models.conversion_result import ConversionResult

downloads_bp = Blueprint("downloads", __name__, url_prefix="/downloads")


@downloads_bp.get("/results/<int:result_id>")
def download_result(result_id: int):
    result = ConversionResult.query.get(result_id)

    if not result:
        raise NotFound("Conversion result was not found.")

    if result.status != "success":
        raise NotFound("Conversion result is not ready for download.")

    if not result.output_path:
        raise NotFound("No output path is recorded for this conversion result.")

    file_path = Path(result.output_path)
    if not file_path.exists():
        raise NotFound("Generated output file is missing on disk.")

    return send_file(
        file_path,
        as_attachment=True,
        download_name=result.output_filename or file_path.name,
        mimetype="application/pdf" if result.output_format == "pdf" else None,
    )
```

---

## B) Update `backend/app/api/v1/__init__.py`

Replace your current file with this version:

```python
from flask import Blueprint

from app.api.v1.conversions import conversions_bp
from app.api.v1.downloads import downloads_bp
from app.api.v1.jobs import jobs_bp
from app.api.v1.uploads import uploads_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/v1")
api_v1_bp.register_blueprint(uploads_bp)
api_v1_bp.register_blueprint(conversions_bp)
api_v1_bp.register_blueprint(jobs_bp)
api_v1_bp.register_blueprint(downloads_bp)
```

---

## C) Update `backend/app/services/conversion_router_service.py`

Replace your current file with this Phase 5 version so PDF jobs create one merged result row while image jobs still use the Phase 4 flow.

```python
from __future__ import annotations

from pathlib import Path

from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult
from app.models.file_asset import FileAsset
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
    In Phase 5, this function routes image jobs and PDF jobs to the correct service.
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

## D) Update `frontend/src/pages/ConvertPage.jsx`

Replace your current file with this Phase 5 version so it uses the new `FormatSelector` and `ConversionSummary` components.

```jsx
import { useMemo, useState } from "react";
import ConversionSummary from "../components/conversion/ConversionSummary";
import FormatSelector from "../components/conversion/FormatSelector";
import JobStatusCard from "../components/jobs/JobStatusCard";
import UploadDropzone from "../components/upload/UploadDropzone";
import FileCard from "../components/upload/FileCard";
import useJobPolling from "../hooks/useJobPolling";
import { formatFileSize, validateFilesClientSide } from "../utils/fileHelpers";
import { createConversionJob } from "../services/jobService";
import { uploadFiles } from "../services/uploadService";

const MAX_FILES = 10;
const OUTPUT_OPTIONS = ["jpg", "png", "webp", "pdf", "docx"];

export default function ConvertPage() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [clientErrors, setClientErrors] = useState([]);
  const [serverError, setServerError] = useState("");
  const [uploadResult, setUploadResult] = useState(null);
  const [jobCreationError, setJobCreationError] = useState("");
  const [jobId, setJobId] = useState("");
  const [outputFormat, setOutputFormat] = useState("pdf");
  const [isUploading, setIsUploading] = useState(false);
  const [isCreatingJob, setIsCreatingJob] = useState(false);

  const { jobPayload, pollingError, isPolling } = useJobPolling(Boolean(jobId) ? jobId : null);

  const totalSize = useMemo(
    () => selectedFiles.reduce((sum, file) => sum + file.size, 0),
    [selectedFiles]
  );

  const handleFilesAdded = (incomingFiles) => {
    const mergedFiles = [...selectedFiles, ...incomingFiles].slice(0, MAX_FILES);
    const validation = validateFilesClientSide(mergedFiles);

    setSelectedFiles(validation.validFiles);
    setClientErrors(validation.errors);
    setServerError("");
    setUploadResult(null);
    setJobCreationError("");
    setJobId("");
  };

  const handleRemove = (targetIndex) => {
    const nextFiles = selectedFiles.filter((_, index) => index !== targetIndex);
    const validation = validateFilesClientSide(nextFiles);

    setSelectedFiles(validation.validFiles);
    setClientErrors(validation.errors);
  };

  const handleUpload = async () => {
    setServerError("");
    setUploadResult(null);
    setJobCreationError("");
    setJobId("");

    if (!selectedFiles.length) {
      setServerError("Please select at least one file before uploading.");
      return;
    }

    const validation = validateFilesClientSide(selectedFiles);
    if (validation.errors.length) {
      setClientErrors(validation.errors);
      return;
    }

    try {
      setIsUploading(true);
      const response = await uploadFiles(selectedFiles);
      setUploadResult(response);
    } catch (error) {
      setServerError(error.message || "Upload failed.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleCreateJob = async () => {
    setJobCreationError("");
    setJobId("");

    const uploadedFiles = uploadResult?.data?.files || [];
    if (!uploadedFiles.length) {
      setJobCreationError("Upload files first before creating a conversion job.");
      return;
    }

    try {
      setIsCreatingJob(true);
      const response = await createConversionJob(
        uploadedFiles.map((file) => file.public_id),
        outputFormat
      );

      const createdJobId = response?.data?.job?.public_id;
      setJobId(createdJobId || "");
    } catch (error) {
      setJobCreationError(error.message || "Failed to create conversion job.");
    } finally {
      setIsCreatingJob(false);
    }
  };

  const handleClear = () => {
    setSelectedFiles([]);
    setClientErrors([]);
    setServerError("");
    setUploadResult(null);
    setJobCreationError("");
    setJobId("");
  };

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Upload and Convert Files
          </h1>
          <p className="mt-2 text-slate-600">
            Phase 5 adds PDF generation, merged PDF export, and downloadable results.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.95fr]">
          <div className="space-y-6">
            <UploadDropzone
              onFilesAdded={handleFilesAdded}
              maxFiles={MAX_FILES}
              disabled={isUploading || isCreatingJob}
            />

            {clientErrors.length > 0 && (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                <h2 className="text-sm font-semibold text-amber-700">
                  Client-side validation issues
                </h2>
                <ul className="mt-2 ml-5 list-disc space-y-1 text-sm text-amber-700">
                  {clientErrors.map((error, index) => (
                    <li key={`${error}-${index}`}>{error}</li>
                  ))}
                </ul>
              </div>
            )}

            {serverError && (
              <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                {serverError}
              </div>
            )}

            {jobCreationError && (
              <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                {jobCreationError}
              </div>
            )}

            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900">
                    Selected files
                  </h2>
                  <p className="mt-1 text-sm text-slate-500">
                    {selectedFiles.length} file(s) · {formatFileSize(totalSize)}
                  </p>
                </div>

                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={handleClear}
                    disabled={isUploading || isCreatingJob}
                    className="rounded-xl border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    Clear
                  </button>

                  <button
                    type="button"
                    onClick={handleUpload}
                    disabled={isUploading || isCreatingJob || selectedFiles.length === 0}
                    className="rounded-xl bg-brand-600 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {isUploading ? "Uploading..." : "Upload files"}
                  </button>
                </div>
              </div>

              <div className="mt-6 grid gap-4">
                {selectedFiles.length === 0 ? (
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-sm text-slate-500">
                    No files selected yet.
                  </div>
                ) : (
                  selectedFiles.map((file, index) => (
                    <FileCard
                      key={`${file.name}-${index}`}
                      file={file}
                      onRemove={() => handleRemove(index)}
                    />
                  ))
                )}
              </div>
            </div>

            {uploadResult && (
              <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6 shadow-sm">
                <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
                  <div>
                    <h2 className="text-lg font-semibold text-emerald-800">
                      Upload successful
                    </h2>
                    <p className="mt-2 text-sm text-emerald-700">
                      {uploadResult.message}
                    </p>
                  </div>

                  <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
                    <FormatSelector
                      value={outputFormat}
                      onChange={setOutputFormat}
                      options={OUTPUT_OPTIONS}
                      disabled={isCreatingJob}
                    />

                    <button
                      type="button"
                      onClick={handleCreateJob}
                      disabled={isCreatingJob}
                      className="rounded-xl bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      {isCreatingJob ? "Creating job..." : "Create conversion job"}
                    </button>
                  </div>
                </div>

                <div className="mt-4 space-y-3">
                  {uploadResult.data.files.map((file) => (
                    <div
                      key={file.public_id}
                      className="rounded-2xl border border-emerald-200 bg-white p-4 text-sm"
                    >
                      <p className="font-medium text-slate-900">
                        {file.original_filename}
                      </p>
                      <p className="mt-1 text-slate-600">Stored as: {file.stored_filename}</p>
                      <p className="mt-1 text-slate-600">Public ID: {file.public_id}</p>
                      <p className="mt-1 text-slate-600">MIME: {file.mime_type}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <aside className="space-y-6">
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-semibold text-slate-900">
                Phase 5 rules
              </h2>

              <ul className="mt-4 space-y-3 text-sm text-slate-600">
                <li>Single image -> one PDF</li>
                <li>Multiple images -> one merged PDF</li>
                <li>Image order is preserved in the merged PDF</li>
                <li>Worker writes a downloadable PDF result row</li>
              </ul>
            </div>

            {jobId && (
              <div className="rounded-3xl border border-brand-200 bg-brand-50 p-4 text-sm text-brand-700">
                Tracking job: <span className="font-semibold break-all">{jobId}</span>
                {isPolling && <span className="ml-2">• polling...</span>}
              </div>
            )}

            <JobStatusCard
              job={jobPayload?.job}
              results={jobPayload?.results || []}
              pollingError={pollingError}
            />

            <ConversionSummary
              job={jobPayload?.job}
              results={jobPayload?.results || []}
            />
          </aside>
        </div>
      </section>
    </main>
  );
}
```

---

# Required supporting folder checks

Run these if needed:

```bash
mkdir -p backend/app/api/v1
mkdir -p backend/app/services
mkdir -p backend/tests
mkdir -p frontend/src/components/conversion
```

---

# Exact migration command status

No new DB migration is required for Phase 5.

Reason:
- you are reusing the existing `conversion_results` table
- `source_file_id` is already nullable
- `output_filename` and `output_path` already exist

So Phase 5 is a service-routing and download-endpoint phase, not a schema-change phase.

---

# Exact startup order after Phase 5 files are in place

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

# Exact test commands for Phase 5

From `backend/`:

```bash
source env/bin/activate
pytest tests/test_downloads.py -q
```

If you want verbose output:

```bash
pytest tests/test_downloads.py -v
```

---

# Completion Check

## Check 1 — generated PDFs open correctly

Open:

```text
http://127.0.0.1:5173/convert
```

Then:
1. upload one valid image
2. choose `PDF`
3. create the conversion job
4. wait for `success`
5. click the download button

Expected:
- a `.pdf` file downloads
- the file opens correctly in a PDF viewer

---

## Check 2 — multiple images preserve order

Use 3 images named in a clear sequence, for example:

- `01-first.png`
- `02-second.png`
- `03-third.png`

Upload them in that order, choose `PDF`, and create the job.

Expected:
- the merged PDF has 3 pages
- page 1 corresponds to the first uploaded image
- page 2 corresponds to the second uploaded image
- page 3 corresponds to the third uploaded image

---

## Check 3 — merged PDF is downloadable

After the job reaches `success`, the frontend summary should show a **Download result** button.

Expected:
- clicking it hits `GET /api/v1/downloads/results/<result_id>`
- the backend returns the generated PDF as an attachment
- the downloaded file opens

---

# Optional direct API flow test

## A) Upload source files

```bash
curl -X POST http://127.0.0.1:5000/api/v1/uploads \
  -F "files=@/absolute/path/to/01-first.png" \
  -F "files=@/absolute/path/to/02-second.png" \
  -F "files=@/absolute/path/to/03-third.png"
```

Copy the returned file `public_id` values in the same order.

## B) Create a PDF conversion job

```bash
curl -X POST http://127.0.0.1:5000/api/v1/conversions \
  -H "Content-Type: application/json" \
  -d '{
    "file_public_ids": ["PUT_FIRST_FILE_ID", "PUT_SECOND_FILE_ID", "PUT_THIRD_FILE_ID"],
    "output_format": "pdf"
  }'
```

Copy the returned job `public_id`.

## C) Poll job status

```bash
curl http://127.0.0.1:5000/api/v1/jobs/PUT_REAL_JOB_PUBLIC_ID_HERE
```

When the job is successful, copy the first result `id`.

## D) Download the generated PDF

```bash
curl -L http://127.0.0.1:5000/api/v1/downloads/results/PUT_RESULT_ID_HERE -o merged.pdf
```

Expected:
- `merged.pdf` is downloaded locally
- it opens correctly

---

# Exact SQL checks

Check the newest results:

```bash
docker exec -it formatbridge_postgres psql -U formatbridge_user -d formatbridge_db -c "SELECT id, job_id, source_file_id, output_format, status, output_filename, output_path, created_at FROM conversion_results ORDER BY id DESC;"
```

For a merged PDF job, expect:
- one result row
- `source_file_id` may be `NULL`
- `output_format = 'pdf'`
- `status = 'success'`

---

# What Phase 5 completes

Once this works, your project will have:

- single image -> PDF export
- multi-image merged PDF export
- preserved image order in merged PDFs
- downloadable PDF results through an API endpoint
- frontend summary with PDF download links

That is a proper Phase 5 foundation.

---

# Best next step after Phase 5

The next clean move is **Phase 6 — DOCX Export**, where you add:

- image -> DOCX
- downloadable DOCX results
- job routing for DOCX output

That is the correct next stage after PDF export is stable.
