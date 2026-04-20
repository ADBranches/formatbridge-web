# FormatBridge — Phase 8: Cleanup, Error Handling, and Hardening

## Objective
Make the system safer and production-ready for MVP release.

This phase gives you:

- expired temp file cleanup
- better error responses
- basic structured logging
- a practical rate-limiting plan for MVP hardening
- cleaner environment configuration

---

# Important note before you start

Phase 8 does **not** need:

- a new database name
- a new PostgreSQL user
- new DB grants
- a new Redis service
- a new database migration

Keep using the exact identifiers already established in Phase 1–7:

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

# Phase 8 exact additions to `.env`

Add these to your existing `.env` and `.env.example`:

```env
# =========================
# CLEANUP
# =========================
TEMP_FILE_RETENTION_HOURS=24
ARCHIVE_RETENTION_HOURS=24
CLEANUP_BATCH_SIZE=500

# =========================
# LOGGING
# =========================
APP_LOG_LEVEL=INFO

# =========================
# RATE LIMITING PLAN
# =========================
RATE_LIMIT_UPLOADS_PER_MINUTE=20
RATE_LIMIT_CONVERSIONS_PER_MINUTE=20
RATE_LIMIT_DOWNLOADS_PER_MINUTE=60
```

## Meaning
- `TEMP_FILE_RETENTION_HOURS=24` -> uploaded and converted temp files older than 24 hours can be deleted
- `ARCHIVE_RETENTION_HOURS=24` -> ZIP archives older than 24 hours can be deleted
- `CLEANUP_BATCH_SIZE=500` -> max files to remove in one cleanup run
- `APP_LOG_LEVEL=INFO` -> Flask and worker log verbosity
- the `RATE_LIMIT_*` values are part of the hardening plan and documentation for the MVP release

---

# Files to Populate

## 1) `backend/app/services/cleanup_service.py`

```python
from __future__ import annotations

import logging
import os
import time
from pathlib import Path

logger = logging.getLogger(__name__)


def get_retention_seconds(env_name: str, default_hours: int) -> int:
    hours = int(os.getenv(env_name, str(default_hours)))
    return max(hours, 0) * 3600


def should_delete_file(path: Path, older_than_seconds: int, now_ts: float | None = None) -> bool:
    if not path.is_file():
        return False

    now_ts = now_ts or time.time()
    file_age = now_ts - path.stat().st_mtime
    return file_age >= older_than_seconds


def cleanup_directory(
    directory: str | Path,
    older_than_seconds: int,
    batch_size: int | None = None,
) -> dict:
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)

    deleted_files: list[str] = []
    kept_files: list[str] = []
    scanned = 0
    limit = batch_size or int(os.getenv("CLEANUP_BATCH_SIZE", "500"))

    for file_path in sorted(path.iterdir(), key=lambda item: item.stat().st_mtime if item.exists() else 0):
        if scanned >= limit:
            break

        scanned += 1

        if should_delete_file(file_path, older_than_seconds):
            try:
                file_path.unlink(missing_ok=True)
                deleted_files.append(str(file_path))
                logger.info("Deleted stale file: %s", file_path)
            except Exception as exc:
                logger.exception("Failed to delete stale file %s: %s", file_path, exc)
        else:
            kept_files.append(str(file_path))

    return {
        "directory": str(path),
        "scanned": scanned,
        "deleted_count": len(deleted_files),
        "kept_count": len(kept_files),
        "deleted_files": deleted_files,
    }


def cleanup_uploads() -> dict:
    upload_dir = os.getenv("UPLOAD_DIR", "app/temp_storage/uploads")
    retention_seconds = get_retention_seconds("TEMP_FILE_RETENTION_HOURS", 24)
    return cleanup_directory(upload_dir, retention_seconds)


def cleanup_converted_outputs() -> dict:
    converted_dir = os.getenv("CONVERTED_DIR", "app/temp_storage/converted")
    retention_seconds = get_retention_seconds("TEMP_FILE_RETENTION_HOURS", 24)
    return cleanup_directory(converted_dir, retention_seconds)


def cleanup_archives() -> dict:
    archives_dir = os.getenv("ZIP_OUTPUT_DIR", "app/temp_storage/archives")
    retention_seconds = get_retention_seconds("ARCHIVE_RETENTION_HOURS", 24)
    return cleanup_directory(archives_dir, retention_seconds)


def cleanup_all_temp_storage() -> dict:
    uploads_summary = cleanup_uploads()
    converted_summary = cleanup_converted_outputs()
    archives_summary = cleanup_archives()

    total_deleted = (
        uploads_summary["deleted_count"]
        + converted_summary["deleted_count"]
        + archives_summary["deleted_count"]
    )

    return {
        "uploads": uploads_summary,
        "converted": converted_summary,
        "archives": archives_summary,
        "total_deleted_count": total_deleted,
    }
```

---

## 2) `backend/app/tasks/cleanup_tasks.py`

```python
from __future__ import annotations

from app.extensions import celery_app
from app.services.cleanup_service import cleanup_all_temp_storage


@celery_app.task(name="tasks.cleanup_temp_storage")
def cleanup_temp_storage_task():
    return cleanup_all_temp_storage()
```

---

## 3) `backend/app/utils/response.py`

```python
from __future__ import annotations

from flask import jsonify


def success_response(message: str, data: dict | list | None = None, status_code: int = 200):
    payload = {
        "success": True,
        "message": message,
        "data": data if data is not None else {},
        "error": None,
    }
    return jsonify(payload), status_code


def error_response(
    message: str,
    status_code: int = 400,
    error_code: str | None = None,
    details: dict | list | None = None,
):
    payload = {
        "success": False,
        "message": message,
        "data": {},
        "error": {
            "code": error_code or "request_error",
            "details": details if details is not None else {},
        },
    }
    return jsonify(payload), status_code
```

---

## 4) `backend/tests/test_uploads.py`

Replace your current upload tests with this Phase 8 version:

```python
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
```

---

## 5) `backend/tests/test_health.py`

Replace your current health tests with this Phase 8 version:

```python
from __future__ import annotations


def build_test_app(monkeypatch, tmp_path):
    database_path = tmp_path / "phase8_health.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
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


def test_health_endpoint_returns_consistent_response(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)
    client = app.test_client()

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.get_json()

    assert body["success"] is True
    assert body["message"] == "Health check completed."
    assert body["data"]["service"] == "formatbridge-api"
    assert body["data"]["database"] == "connected"
    assert body["data"]["queue"] == "configured"
    assert body["error"] is None
```

---

## 6) `docs/testing_checklist.md`

```md
# FormatBridge Testing Checklist

## Phase 1
- [ ] Frontend loads on `http://127.0.0.1:5173`
- [ ] Backend health endpoint responds
- [ ] PostgreSQL container is running
- [ ] Redis container is running
- [ ] Celery worker starts successfully

## Phase 2
- [ ] Valid uploads succeed
- [ ] Invalid file types are rejected
- [ ] Too many files are rejected
- [ ] Oversized uploads fail safely
- [ ] Uploaded file rows are written to `file_assets`

## Phase 3
- [ ] Conversion request creates a job
- [ ] Worker receives queued job
- [ ] Job transitions from queued to processing to success / failed
- [ ] UI polling reflects job state

## Phase 4
- [ ] HEIC -> JPG works
- [ ] HEIC -> PNG works
- [ ] JPG / JPEG / PNG / WEBP -> JPG works
- [ ] JPG / JPEG / PNG / WEBP -> PNG works
- [ ] JPG / JPEG / PNG / WEBP -> WEBP works
- [ ] Result rows are written to `conversion_results`

## Phase 5
- [ ] Single image -> PDF works
- [ ] Multi-image merged PDF works
- [ ] Page order is preserved
- [ ] PDF download endpoint works

## Phase 6
- [ ] Single image -> DOCX works
- [ ] Multi-image -> DOCX works
- [ ] Embedded images render in Word / LibreOffice
- [ ] DOCX download endpoint works

## Phase 7
- [ ] ZIP packaging works
- [ ] ZIP download endpoint works
- [ ] Extracted files are valid
- [ ] Result list shows correct individual links

## Phase 8
- [ ] Stale uploads are deleted
- [ ] Stale converted outputs are deleted
- [ ] Stale ZIP archives are deleted
- [ ] Oversized / invalid jobs fail safely
- [ ] Error responses are consistent and user-readable
- [ ] Health response is consistent
```

---

## 7) `docs/deployment_guide.md`

```md
# FormatBridge Deployment Guide

## Overview
FormatBridge MVP deployment includes:
- React frontend
- Flask backend
- Celery worker
- Redis
- PostgreSQL
- Nginx reverse proxy

## Recommended Services
- `frontend`
- `backend`
- `celery_worker`
- `redis`
- `postgres`
- `nginx`

## Environment
Use a production `.env` with:
- strong `SECRET_KEY`
- production database credentials
- production Redis URL
- production CORS origins
- cleanup retention values
- logging level

## Gunicorn
Run Flask with Gunicorn in production, not the development server.

Example:
```bash
gunicorn -w 3 -b 0.0.0.0:5000 wsgi:app
```

## Celery Worker
Run a separate worker process:

```bash
celery -A celery_worker.celery worker --loglevel=info
```

## Cleanup Task Strategy
Recommended MVP strategy:
- run `cleanup_temp_storage_task` on a schedule
- use Celery Beat later if you want automated cleanup
- for a simple VPS, a cron job or scheduled management command is also acceptable

## Rate-Limiting Plan
For MVP hardening, apply rate limiting at the reverse proxy or app layer.

Suggested starting rules:
- uploads: 20 requests per minute per IP
- conversions: 20 requests per minute per IP
- downloads: 60 requests per minute per IP

You can enforce this with:
- Nginx rate limiting
- Flask-Limiter later if you decide to add it
- upstream API gateway controls

## Temp Storage
Use writable directories for:
- uploads
- converted outputs
- archives

These should be:
- excluded from Git
- cleaned regularly
- monitored for disk usage

## Logging
Recommended minimum logging:
- app startup
- upload validation failures
- conversion failures
- cleanup deletions
- worker task failures

## Reverse Proxy
Use Nginx to:
- serve the built frontend
- proxy API traffic to Flask
- optionally enforce upload limits
- optionally enforce rate limits

## Security Notes
- validate file types on both client and server
- enforce upload size limits
- rotate secrets
- keep temp files short-lived
- run behind HTTPS in production
```

---

# Required supporting edits

These files were not in your Phase 8 list, but they are required for the phase to actually run cleanly.

---

## A) Update `backend/app/__init__.py`

Replace your current file with this Phase 8 version:

```python
import logging
import os

from flask import Flask
from werkzeug.exceptions import BadRequest, NotFound, RequestEntityTooLarge

from app.api import api_bp
from app.api.v1 import api_v1_bp
from app.config import get_config
from app.database import ping_database
from app.extensions import cors, db, init_celery, migrate
from app.utils.response import error_response, success_response


def configure_logging(app: Flask) -> None:
    log_level_name = os.getenv("APP_LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    app.logger.setLevel(log_level)
    app.logger.info("Logging configured at %s level.", log_level_name)


def create_app(config_name: str | None = None):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    configure_logging(app)

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

        return success_response(
            "Health check completed.",
            data={
                "status": status,
                "service": "formatbridge-api",
                "database": database_status,
                "queue": "configured",
                "error": error_message,
            },
            status_code=200 if database_status == "connected" else 503,
        )

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return error_response(
            message=str(error),
            status_code=400,
            error_code="bad_request",
        )

    @app.errorhandler(NotFound)
    def handle_not_found(error):
        return error_response(
            message=str(error),
            status_code=404,
            error_code="not_found",
        )

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(error):
        return error_response(
            message=str(error),
            status_code=413,
            error_code="payload_too_large",
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled application error: %s", error)
        return error_response(
            message="An unexpected server error occurred.",
            status_code=500,
            error_code="internal_server_error",
        )

    return app
```

---

## B) Update `backend/app/api/v1/uploads.py`

Replace your current file with this version so it returns standardized success responses:

```python
from flask import Blueprint, request

from app.schemas.upload_schema import serialize_upload_response
from app.services.file_service import save_uploaded_files
from app.utils.response import success_response

uploads_bp = Blueprint("uploads", __name__, url_prefix="/uploads")


@uploads_bp.post("")
def upload_files():
    files = request.files.getlist("files")
    saved_assets = save_uploaded_files(files)

    payload = serialize_upload_response(
        message="Files uploaded successfully.",
        assets=saved_assets,
    )

    return success_response(
        message=payload["message"],
        data=payload["data"],
        status_code=201,
    )
```

---

## C) Update `backend/celery_worker.py`

Replace your current file with this version so cleanup tasks are registered:

```python
from app import create_app

flask_app = create_app()
celery = flask_app.extensions["celery"]

from app.tasks.cleanup_tasks import cleanup_temp_storage_task  # noqa: F401
from app.tasks.conversion_tasks import process_conversion_job_task  # noqa: F401


@celery.task(name="tasks.ping")
def ping():
    return {"message": "pong"}
```

---

## D) Optional manual cleanup command

From `backend/` you can trigger cleanup manually:

```bash
source env/bin/activate
python - <<'PY'
from app import create_app
from app.services.cleanup_service import cleanup_all_temp_storage

app = create_app("development")
with app.app_context():
    print(cleanup_all_temp_storage())
PY
```

---

# Exact migration command status

No new DB migration is required for Phase 8.

Reason:
- this phase adds cleanup, logging, response consistency, and hardening
- no new DB schema is introduced

---

# Exact startup order after Phase 8 files are in place

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

# Exact test commands for Phase 8

From `backend/`:

```bash
source env/bin/activate
pytest tests/test_uploads.py tests/test_health.py -q
```

If you want verbose output:

```bash
pytest tests/test_uploads.py tests/test_health.py -v
```

---

# Completion Check

## Check 1 — stale files are deleted

Create old files inside:
- `backend/app/temp_storage/uploads`
- `backend/app/temp_storage/converted`
- `backend/app/temp_storage/archives`

Then run the manual cleanup command.

Expected:
- files older than the configured retention are deleted
- recent files remain

---

## Check 2 — large invalid jobs fail safely

Try:
- too many files
- unsupported extensions
- oversized uploads

Expected:
- failures return safe JSON responses
- no raw traceback is shown to the user
- messages are readable and consistent

---

## Check 3 — errors are consistent and user-readable

Expected response shape:

```json
{
  "success": false,
  "message": "Human-readable error message here",
  "data": {},
  "error": {
    "code": "bad_request",
    "details": {}
  }
}
```

Health success shape:

```json
{
  "success": true,
  "message": "Health check completed.",
  "data": {
    "status": "healthy",
    "service": "formatbridge-api",
    "database": "connected",
    "queue": "configured",
    "error": null
  },
  "error": null
}
```

---

# Rate-Limiting plan for MVP

Phase 8 includes the hardening **plan**, not full enforcement yet.

Recommended MVP enforcement order:
1. apply Nginx request-size limits
2. apply Nginx IP-based rate limits for uploads, conversions, and downloads
3. optionally add Flask-Limiter later if you want app-layer enforcement too

Recommended starting values:
- uploads: 20 requests / minute / IP
- conversions: 20 requests / minute / IP
- downloads: 60 requests / minute / IP

That is enough for the MVP hardening target without changing your current DB schema.

---

# What Phase 8 completes

Once this works, your project will have:

- stale temp file cleanup
- stale archive cleanup
- standardized JSON success and error responses
- safer behavior for invalid and oversized jobs
- basic logging
- a written deployment guide
- a written testing checklist
- a concrete rate-limiting plan

That is a proper Phase 8 foundation.

---

# Best next step after Phase 8

The next clean move is to polish the MVP release, verify all phase tests, and prepare deployment with:
- Nginx
- Gunicorn
- Celery worker
- Redis
- PostgreSQL
- periodic cleanup scheduling

That is the right move after hardening is in place.
