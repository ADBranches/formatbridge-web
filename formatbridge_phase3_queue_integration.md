# FormatBridge — Phase 3: Conversion Job Model and Queue Integration

## Objective
Add asynchronous job creation and progress tracking.

This phase gives you:

- conversion request endpoint
- Celery task creation
- job status updates
- polling UI
- worker-driven queued → processing → success / failed lifecycle

---

# Important note before you start

Phase 3 does **not** need a new database name, a new database user, or a new Redis service.

Keep using the exact Phase 1 and Phase 2 identifiers:

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

No new DB grant is needed if you are still using the PostgreSQL service already created in Phase 1.

---

# Phase 3 exact additions to `.env`

Add these to your existing `.env` and `.env.example`:

```env
# =========================
# CONVERSIONS
# =========================
JOB_POLL_INTERVAL_MS=2000
PHASE3_SIMULATED_PROCESSING_SECONDS=2
ALLOWED_OUTPUT_FORMATS=jpg,png,webp,pdf,docx
```

## Meaning
- `JOB_POLL_INTERVAL_MS=2000` → frontend polling interval = 2 seconds
- `PHASE3_SIMULATED_PROCESSING_SECONDS=2` → small delay so queued / processing / success are visible
- `ALLOWED_OUTPUT_FORMATS` → requestable target formats for Phase 3 job creation

---

# Secret key generation command

If you still need a stronger Flask secret key, use this exact command:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Then paste the output into:

```env
SECRET_KEY=your_generated_value_here
```

---

# Files to Populate

## 1) `backend/app/models/conversion_job.py`

```python
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ConversionJob(Base):
    __tablename__ = "conversion_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    public_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    requested_output_format: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    source_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_public_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)

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
            f"status={self.status!r} output={self.requested_output_format!r}>"
        )
```

---

## 2) `backend/app/models/conversion_result.py`

```python
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ConversionResult(Base):
    __tablename__ = "conversion_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    job_id: Mapped[int] = mapped_column(
        ForeignKey("conversion_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_file_id: Mapped[int | None] = mapped_column(
        ForeignKey("file_assets.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    output_format: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending", index=True)

    output_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    output_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    job = relationship("ConversionJob", back_populates="results")
    source_file = relationship("FileAsset")

    def __repr__(self) -> str:
        return (
            f"<ConversionResult id={self.id} job_id={self.job_id} "
            f"output_format={self.output_format!r} status={self.status!r}>"
        )
```

---

## 3) `backend/app/api/v1/conversions.py`

```python
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.file_asset import FileAsset
from app.schemas.conversion_schema import (
    serialize_conversion_job_created,
    validate_conversion_request,
)
from app.tasks.conversion_tasks import process_conversion_job_task

conversions_bp = Blueprint("conversions", __name__, url_prefix="/conversions")


@conversions_bp.post("")
def create_conversion_job():
    payload = request.get_json(silent=True) or {}
    data = validate_conversion_request(payload)

    source_public_ids = data["file_public_ids"]
    requested_output_format = data["output_format"]

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
        public_id=__import__("uuid").uuid4().hex,
        requested_output_format=requested_output_format,
        source_count=len(source_public_ids),
        source_public_ids=source_public_ids,
        status="queued",
    )

    db.session.add(job)
    db.session.commit()

    process_conversion_job_task.delay(job.public_id)

    return jsonify(
        serialize_conversion_job_created(
            message="Conversion job created successfully.",
            job=job,
        )
    ), 202
```

---

## 4) `backend/app/api/v1/jobs.py`

```python
from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound

from app.models.conversion_job import ConversionJob
from app.schemas.result_schema import serialize_job_status_response

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs_bp.get("/<string:job_public_id>")
def get_job_status(job_public_id: str):
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()

    if not job:
        raise NotFound("Conversion job was not found.")

    return jsonify(
        serialize_job_status_response(
            message="Job status fetched successfully.",
            job=job,
        )
    ), 200
```

---

## 5) `backend/app/schemas/conversion_schema.py`

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

    return {
        "file_public_ids": cleaned_ids,
        "output_format": output_format,
    }


def serialize_conversion_job_summary(job: ConversionJob) -> dict:
    return {
        "public_id": job.public_id,
        "requested_output_format": job.requested_output_format,
        "source_count": job.source_count,
        "source_public_ids": job.source_public_ids,
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

## 6) `backend/app/schemas/result_schema.py`

```python
from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult
from app.schemas.conversion_schema import serialize_conversion_job_summary


def serialize_conversion_result(result: ConversionResult) -> dict:
    return {
        "id": result.id,
        "job_id": result.job_id,
        "source_file_id": result.source_file_id,
        "output_format": result.output_format,
        "status": result.status,
        "output_filename": result.output_filename,
        "output_path": result.output_path,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }


def serialize_job_status_response(message: str, job: ConversionJob) -> dict:
    return {
        "message": message,
        "data": {
            "job": serialize_conversion_job_summary(job),
            "results": [serialize_conversion_result(result) for result in job.results],
        },
    }
```

---

## 7) `backend/app/tasks/conversion_tasks.py`

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

        run_phase3_conversion_job(job_public_id)

        job = get_job_or_raise(job_public_id)
        job.status = "success"
        job.completed_at = datetime.utcnow()
        job.updated_at = datetime.utcnow()
        db.session.commit()

        return {
            "job_public_id": job_public_id,
            "status": "success",
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

## 8) `backend/app/services/conversion_router_service.py`

```python
from __future__ import annotations

import os
import time
from pathlib import Path

from werkzeug.exceptions import NotFound

from app.models.conversion_job import ConversionJob
from app.models.file_asset import FileAsset


def run_phase3_conversion_job(job_public_id: str) -> dict:
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()

    if not job:
        raise NotFound("Conversion job was not found.")

    source_files = (
        FileAsset.query.filter(FileAsset.public_id.in_(job.source_public_ids))
        .order_by(FileAsset.id.asc())
        .all()
    )

    if len(source_files) != len(job.source_public_ids):
        raise ValueError("Some uploaded source files are missing from the database.")

    for source_file in source_files:
        if not Path(source_file.storage_path).exists():
            raise FileNotFoundError(
                f"Uploaded source file is missing on disk: {source_file.original_filename}"
            )

    delay_seconds = int(os.getenv("PHASE3_SIMULATED_PROCESSING_SECONDS", "2"))
    if delay_seconds > 0:
        time.sleep(delay_seconds)

    return {
        "job_public_id": job.public_id,
        "requested_output_format": job.requested_output_format,
        "source_count": job.source_count,
        "phase": "phase-3-queue-integration",
        "note": "Actual format conversion will be implemented in Phase 4.",
    }
```

---

## 9) `frontend/src/components/jobs/JobStatusCard.jsx`

```jsx
function StatusBadge({ status }) {
  const normalized = (status || "").toLowerCase();

  const classes =
    normalized === "success"
      ? "bg-emerald-100 text-emerald-700 border-emerald-200"
      : normalized === "failed"
      ? "bg-red-100 text-red-700 border-red-200"
      : normalized === "processing"
      ? "bg-amber-100 text-amber-700 border-amber-200"
      : "bg-slate-100 text-slate-700 border-slate-200";

  return (
    <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold ${classes}`}>
      {status || "unknown"}
    </span>
  );
}

export default function JobStatusCard({ job, results = [], pollingError = "" }) {
  if (!job) return null;

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Conversion job
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Track asynchronous job state from the worker.
          </p>
        </div>

        <StatusBadge status={job.status} />
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Job ID</p>
          <p className="mt-1 break-all text-sm font-medium text-slate-900">
            {job.public_id}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Target format</p>
          <p className="mt-1 text-sm font-medium text-slate-900">
            {job.requested_output_format?.toUpperCase()}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Source count</p>
          <p className="mt-1 text-sm font-medium text-slate-900">{job.source_count}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Results tracked</p>
          <p className="mt-1 text-sm font-medium text-slate-900">{results.length}</p>
        </div>
      </div>

      {job.error_message && (
        <div className="mt-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {job.error_message}
        </div>
      )}

      {pollingError && (
        <div className="mt-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {pollingError}
        </div>
      )}

      <div className="mt-6 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
        <p><span className="font-medium text-slate-900">Created:</span> {job.created_at}</p>
        <p className="mt-1"><span className="font-medium text-slate-900">Started:</span> {job.started_at || "Not yet started"}</p>
        <p className="mt-1"><span className="font-medium text-slate-900">Completed:</span> {job.completed_at || "Not yet completed"}</p>
      </div>
    </div>
  );
}
```

---

## 10) `frontend/src/hooks/useJobPolling.js`

```jsx
import { useEffect, useState } from "react";
import { fetchJobStatus } from "../services/jobService";

const TERMINAL_STATUSES = new Set(["success", "failed"]);
const DEFAULT_INTERVAL_MS = 2000;

export default function useJobPolling(jobId, enabled = true, intervalMs = DEFAULT_INTERVAL_MS) {
  const [jobPayload, setJobPayload] = useState(null);
  const [pollingError, setPollingError] = useState("");
  const [isPolling, setIsPolling] = useState(false);

  useEffect(() => {
    if (!jobId || !enabled) return;

    let intervalId;
    let cancelled = false;

    const poll = async () => {
      try {
        setIsPolling(true);
        const payload = await fetchJobStatus(jobId);

        if (cancelled) return;

        setJobPayload(payload.data);
        setPollingError("");

        const status = payload?.data?.job?.status;
        if (TERMINAL_STATUSES.has(status)) {
          clearInterval(intervalId);
          setIsPolling(false);
        }
      } catch (error) {
        if (cancelled) return;
        setPollingError(error.message || "Failed to fetch job status.");
        clearInterval(intervalId);
        setIsPolling(false);
      }
    };

    poll();
    intervalId = window.setInterval(poll, intervalMs);

    return () => {
      cancelled = True  # intentional? 
      clearInterval(intervalId);
    };
  }, [jobId, enabled, intervalMs]);

  return {
    jobPayload,
    pollingError,
    isPolling,
  };
}
```

---

## 11) `frontend/src/services/jobService.js`

```js
import { apiRequest } from "./apiClient";

export async function createConversionJob(filePublicIds, outputFormat) {
  return apiRequest("/conversions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      file_public_ids: filePublicIds,
      output_format: outputFormat,
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

# Required supporting edits

These files were not in your Phase 3 list, but they are required for the phase to actually run.

---

## A) Fix `frontend/src/hooks/useJobPolling.js`

Use this exact corrected version instead of the one above:

```jsx
import { useEffect, useState } from "react";
import { fetchJobStatus } from "../services/jobService";

const TERMINAL_STATUSES = new Set(["success", "failed"]);
const DEFAULT_INTERVAL_MS = 2000;

export default function useJobPolling(jobId, enabled = true, intervalMs = DEFAULT_INTERVAL_MS) {
  const [jobPayload, setJobPayload] = useState(null);
  const [pollingError, setPollingError] = useState("");
  const [isPolling, setIsPolling] = useState(false);

  useEffect(() => {
    if (!jobId || !enabled) return;

    let intervalId;
    let cancelled = false;

    const poll = async () => {
      try {
        setIsPolling(true);
        const payload = await fetchJobStatus(jobId);

        if (cancelled) return;

        setJobPayload(payload.data);
        setPollingError("");

        const status = payload?.data?.job?.status;
        if (TERMINAL_STATUSES.has(status)) {
          clearInterval(intervalId);
          setIsPolling(false);
        }
      } catch (error) {
        if (cancelled) return;
        setPollingError(error.message || "Failed to fetch job status.");
        clearInterval(intervalId);
        setIsPolling(false);
      }
    };

    poll();
    intervalId = window.setInterval(poll, intervalMs);

    return () => {
      cancelled = true;
      clearInterval(intervalId);
    };
  }, [jobId, enabled, intervalMs]);

  return {
    jobPayload,
    pollingError,
    isPolling,
  };
}
```

---

## B) Update `backend/app/api/v1/__init__.py`

Replace your current file with this version:

```python
from flask import Blueprint

from app.api.v1.conversions import conversions_bp
from app.api.v1.jobs import jobs_bp
from app.api.v1.uploads import uploads_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/v1")
api_v1_bp.register_blueprint(uploads_bp)
api_v1_bp.register_blueprint(conversions_bp)
api_v1_bp.register_blueprint(jobs_bp)
```

---

## C) Update `backend/app/models/__init__.py`

Replace with:

```python
from .file_asset import FileAsset
from .conversion_job import ConversionJob
from .conversion_result import ConversionResult

__all__ = ["FileAsset", "ConversionJob", "ConversionResult"]
```

---

## D) Update `backend/celery_worker.py`

Replace your current file with this version:

```python
from app import create_app

flask_app = create_app()
celery = flask_app.extensions["celery"]

# import task modules so the worker registers them
from app.tasks.conversion_tasks import process_conversion_job_task  # noqa: F401


@celery.task(name="tasks.ping")
def ping():
    return {"message": "pong"}
```

---

## E) Create `backend/app/tasks/__init__.py`

```python
# tasks package marker
```

---

## F) Update `backend/app/__init__.py`

Use this version so request errors and not-found errors are returned cleanly:

```python
from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest, NotFound, RequestEntityTooLarge

from app.api import api_bp
from app.api.v1 import api_v1_bp
from app.config import get_config
from app.database import ping_database
from app.extensions import cors, db, init_celery, migrate


def create_app(config_name: str | None = None):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )
    init_celery(app)

    api_bp.register_blueprint(api_v1_bp)
    app.register_blueprint(api_bp)

    @app.get("/api/v1/health")
    def health_check():
        database_status = "connected"
        status = "healthy"
        error_message = None

        try:
            ping_database()
        except Exception as exc:
            database_status = "disconnected"
            status = "degraded"
            error_message = str(exc)

        payload = {
            "status": status,
            "service": "formatbridge-api",
            "database": database_status,
            "queue": "configured",
            "error": error_message,
        }

        return jsonify(payload), 200 if database_status == "connected" else 503

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return jsonify({"message": str(error)}), 400

    @app.errorhandler(NotFound)
    def handle_not_found(error):
        return jsonify({"message": str(error)}), 404

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(error):
        return jsonify({"message": str(error)}), 413

    return app
```

---

## G) Update `frontend/src/pages/ConvertPage.jsx`

Replace your Phase 2 file with this Phase 3 version:

```jsx
import { useMemo, useState } from "react";
import UploadDropzone from "../components/upload/UploadDropzone";
import FileCard from "../components/upload/FileCard";
import JobStatusCard from "../components/jobs/JobStatusCard";
import useJobPolling from "../hooks/useJobPolling";
import { formatFileSize, validateFilesClientSide } from "../utils/fileHelpers";
import { uploadFiles } from "../services/uploadService";
import { createConversionJob } from "../services/jobService";

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
            Upload and Queue Conversion
          </h1>
          <p className="mt-2 text-slate-600">
            Phase 3 adds asynchronous conversion job creation and progress tracking.
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
                    <div>
                      <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-600">
                        Output format
                      </label>
                      <select
                        value={outputFormat}
                        onChange={(event) => setOutputFormat(event.target.value)}
                        className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm text-slate-800"
                      >
                        {OUTPUT_OPTIONS.map((format) => (
                          <option key={format} value={format}>
                            {format.toUpperCase()}
                          </option>
                        ))}
                      </select>
                    </div>

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
                Phase 3 rules
              </h2>

              <ul className="mt-4 space-y-3 text-sm text-slate-600">
                <li>Upload first</li>
                <li>Create a conversion job after upload succeeds</li>
                <li>Worker picks job from Redis broker queue</li>
                <li>UI polls until the job becomes success or failed</li>
                <li>Actual file conversion starts in Phase 4</li>
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
          </aside>
        </div>
      </section>
    </main>
  );
}
```

---

## H) Create frontend folders if missing

Run:

```bash
mkdir -p frontend/src/components/jobs
mkdir -p frontend/src/hooks
```

---

## I) Create backend folders if missing

Run:

```bash
mkdir -p backend/app/tasks
```

---

# Exact migration commands

From the project root:

```bash
cd backend
source env/bin/activate
flask --app run.py db migrate -m "add conversion_jobs and conversion_results tables"
flask --app run.py db upgrade
```

If migration history is not initialized yet, initialize first:

```bash
flask --app run.py db init
flask --app run.py db migrate -m "add conversion_jobs and conversion_results tables"
flask --app run.py db upgrade
```

---

# Exact startup order after Phase 3 files are in place

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

# Completion Check

## Check 1 — conversion request creates a job

Open:
```text
http://127.0.0.1:5173/convert
```

Then:
1. upload valid files
2. choose an output format
3. click **Create conversion job**

Expected:
- backend returns 202
- UI shows a job public ID
- initial status is usually `queued` or `processing`

---

## Check 2 — worker receives task

Watch the Celery worker terminal.

Expected:
- a task is received
- job transitions to `processing`
- after the configured delay, job transitions to `success`

---

## Check 3 — UI reflects queued, processing, success, failed

Expected on the page:
- `queued` when job is first created
- `processing` while the worker handles the job
- `success` when the phase 3 stub completes
- `failed` if source files are missing or the job lookup fails

---

# Optional direct API tests

## A) Create a conversion job directly

After Phase 2 upload gave you file public IDs, use:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/conversions \
  -H "Content-Type: application/json" \
  -d '{
    "file_public_ids": ["PUT_REAL_FILE_PUBLIC_ID_HERE"],
    "output_format": "pdf"
  }'
```

Expected:
- HTTP 202
- response includes `data.job.public_id`

## B) Fetch job status directly

```bash
curl http://127.0.0.1:5000/api/v1/jobs/PUT_REAL_JOB_PUBLIC_ID_HERE
```

Expected:
- HTTP 200
- job payload with status

---

# Exact SQL check for DB writes

Run this to confirm jobs are written:

```bash
docker exec -it formatbridge_postgres psql -U formatbridge_user -d formatbridge_db -c "SELECT id, public_id, requested_output_format, source_count, status, created_at FROM conversion_jobs ORDER BY id DESC;"
```

Run this to confirm results table exists:

```bash
docker exec -it formatbridge_postgres psql -U formatbridge_user -d formatbridge_db -c "SELECT id, job_id, output_format, status, created_at FROM conversion_results ORDER BY id DESC;"
```

In Phase 3, `conversion_results` may remain empty. That is okay.

---

# What Phase 3 completes

Once this works, your project will have:

- conversion job persistence
- queued async task dispatch via Celery
- status transitions stored in DB
- job polling from the frontend
- job inspection endpoint
- clean path into actual conversion logic

That is a proper Phase 3 foundation.

---

# Best next step after Phase 3

The next clean move is **Phase 4 — Core Image Conversion Engine**, where you replace the Phase 3 stub service with real:

- HEIC → JPG
- HEIC → PNG
- JPG / JPEG / PNG / WEBP → JPG
- JPG / JPEG / PNG / WEBP → PNG
- JPG / JPEG / PNG / WEBP → WEBP

That is the correct next stage after job queue integration is stable.
