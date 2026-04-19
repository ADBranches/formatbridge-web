# FormatBridge — Phase 2: Upload Pipeline and File Validation

## Objective
Build secure file upload and server-side validation for the FormatBridge MVP.

This phase gives you:

- drag-and-drop upload UI
- multiple file upload
- file size validation
- MIME/type validation
- temporary file persistence
- uploaded file records written to PostgreSQL

---

# Important note before you start

Phase 2 does **not** need a new database name, a new database user, or a new Redis service.

Keep using the exact Phase 1 identifiers:

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

For this phase, you only add upload-related settings.

---

# Phase 2 exact additions to `.env`

Add these to your existing `.env` and `.env.example`:

```env
# =========================
# UPLOADS
# =========================
MAX_CONTENT_LENGTH=16777216
MAX_FILES_PER_UPLOAD=10
MAX_FILE_SIZE_MB=8
UPLOAD_DIR=app/temp_storage/uploads
ALLOWED_UPLOAD_EXTENSIONS=heic,heif,jpg,jpeg,png,webp,gif
ALLOWED_UPLOAD_MIME_TYPES=image/heic,image/heif,image/jpeg,image/png,image/webp,image/gif
```

## Meaning
- `MAX_CONTENT_LENGTH=16777216` → total request cap = 16 MB
- `MAX_FILES_PER_UPLOAD=10` → user can upload at most 10 files per request
- `MAX_FILE_SIZE_MB=8` → single file cap = 8 MB
- `UPLOAD_DIR=app/temp_storage/uploads` → persisted temporary upload folder inside backend app
- `ALLOWED_UPLOAD_EXTENSIONS` → accepted extensions
- `ALLOWED_UPLOAD_MIME_TYPES` → accepted MIME types

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

No new DB permission grant is needed if you are still using the PostgreSQL service created in Phase 1.

---

# Required package install for frontend

Phase 2 uses drag-and-drop upload with `react-dropzone`.

Run this in `frontend/`:

```bash
npm install react-dropzone
```

---

# Files to Populate

## 1) `frontend/src/components/upload/UploadDropzone.jsx`

```jsx
import { useCallback } from "react";
import { useDropzone } from "react-dropzone";

const ACCEPTED_TYPES = {
  "image/heic": [".heic"],
  "image/heif": [".heif"],
  "image/jpeg": [".jpg", ".jpeg"],
  "image/png": [".png"],
  "image/webp": [".webp"],
  "image/gif": [".gif"],
};

export default function UploadDropzone({
  onFilesAdded,
  maxFiles = 10,
  disabled = false,
}) {
  const handleDrop = useCallback(
    (acceptedFiles) => {
      if (!acceptedFiles.length) return;
      onFilesAdded(acceptedFiles);
    },
    [onFilesAdded]
  );

  const { getRootProps, getInputProps, isDragActive, fileRejections } =
    useDropzone({
      onDrop: handleDrop,
      accept: ACCEPTED_TYPES,
      multiple: true,
      maxFiles,
      disabled,
    });

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`rounded-3xl border-2 border-dashed p-8 text-center transition ${
          isDragActive
            ? "border-brand-600 bg-brand-50"
            : "border-slate-300 bg-white hover:border-brand-500"
        } ${disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer"}`}
      >
        <input {...getInputProps()} />

        <div className="mx-auto max-w-2xl">
          <h2 className="text-xl font-semibold text-slate-900">
            Drag and drop files here
          </h2>

          <p className="mt-2 text-sm text-slate-600">
            Supported formats: HEIC, HEIF, JPG, JPEG, PNG, WEBP, GIF
          </p>

          <p className="mt-1 text-sm text-slate-500">
            You can upload up to {maxFiles} files at once.
          </p>

          <div className="mt-6">
            <span className="inline-flex rounded-xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-sm">
              Choose files
            </span>
          </div>
        </div>
      </div>

      {fileRejections.length > 0 && (
        <div className="rounded-2xl border border-red-200 bg-red-50 p-4">
          <h3 className="text-sm font-semibold text-red-700">
            Some files were rejected by the browser picker
          </h3>

          <ul className="mt-2 space-y-2 text-sm text-red-600">
            {fileRejections.map((entry, index) => (
              <li key={`${entry.file.name}-${index}`}>
                <span className="font-medium">{entry.file.name}</span>
                <ul className="ml-5 mt-1 list-disc">
                  {entry.errors.map((error) => (
                    <li key={error.code}>{error.message}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

---

## 2) `frontend/src/components/upload/FileCard.jsx`

```jsx
import { formatFileSize, getFileExtension } from "../../utils/fileHelpers";

export default function FileCard({ file, onRemove }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="truncate text-sm font-semibold text-slate-900">
            {file.name}
          </h3>
          <p className="mt-1 text-xs text-slate-500">
            Extension: {getFileExtension(file.name).toUpperCase() || "Unknown"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Type: {file.type || "Unknown"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Size: {formatFileSize(file.size)}
          </p>
        </div>

        <button
          type="button"
          onClick={onRemove}
          className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:bg-slate-50"
        >
          Remove
        </button>
      </div>
    </div>
  );
}
```

---

## 3) `frontend/src/pages/ConvertPage.jsx`

```jsx
import { useMemo, useState } from "react";
import UploadDropzone from "../components/upload/UploadDropzone";
import FileCard from "../components/upload/FileCard";
import { formatFileSize, validateFilesClientSide } from "../utils/fileHelpers";
import { uploadFiles } from "../services/uploadService";

const MAX_FILES = 10;

export default function ConvertPage() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [clientErrors, setClientErrors] = useState([]);
  const [serverError, setServerError] = useState("");
  const [uploadResult, setUploadResult] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

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

  const handleClear = () => {
    setSelectedFiles([]);
    setClientErrors([]);
    setServerError("");
    setUploadResult(null);
  };

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Upload Files
          </h1>
          <p className="mt-2 text-slate-600">
            Phase 2 focuses on secure upload, validation, and temporary file persistence.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[1.25fr_0.9fr]">
          <div className="space-y-6">
            <UploadDropzone
              onFilesAdded={handleFilesAdded}
              maxFiles={MAX_FILES}
              disabled={isUploading}
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
                    disabled={isUploading}
                    className="rounded-xl border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    Clear
                  </button>

                  <button
                    type="button"
                    onClick={handleUpload}
                    disabled={isUploading || selectedFiles.length === 0}
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
          </div>

          <aside className="space-y-6">
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-semibold text-slate-900">
                Upload rules
              </h2>

              <ul className="mt-4 space-y-3 text-sm text-slate-600">
                <li>Maximum files per request: 10</li>
                <li>Maximum single file size: 8 MB</li>
                <li>Maximum request size: 16 MB</li>
                <li>Allowed formats: HEIC, HEIF, JPG, JPEG, PNG, WEBP, GIF</li>
              </ul>
            </div>

            {uploadResult && (
              <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6 shadow-sm">
                <h2 className="text-lg font-semibold text-emerald-800">
                  Upload successful
                </h2>

                <p className="mt-2 text-sm text-emerald-700">
                  {uploadResult.message}
                </p>

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
                      <p className="mt-1 text-slate-600">MIME: {file.mime_type}</p>
                      <p className="mt-1 text-slate-600">Size: {formatFileSize(file.size_bytes)}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </aside>
        </div>
      </section>
    </main>
  );
}
```

---

## 4) `frontend/src/services/apiClient.js`

```js
const API_BASE_URL = "http://127.0.0.1:5000/api/v1";

async function parseJsonSafely(response) {
  const contentType = response.headers.get("content-type") || "";

  if (!contentType.includes("application/json")) {
    return null;
  }

  try {
    return await response.json();
  } catch {
    return null;
  }
}

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  const body = await parseJsonSafely(response);

  if (!response.ok) {
    const message =
      body?.message ||
      body?.error ||
      "Request failed. Please try again.";

    throw new Error(message);
  }

  return body;
}
```

---

## 5) `frontend/src/services/uploadService.js`

```js
import { apiRequest } from "./apiClient";

export async function uploadFiles(files) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  return apiRequest("/uploads", {
    method: "POST",
    body: formData,
  });
}
```

---

## 6) `frontend/src/utils/fileHelpers.js`

```js
const ALLOWED_EXTENSIONS = ["heic", "heif", "jpg", "jpeg", "png", "webp", "gif"];
const ALLOWED_MIME_TYPES = [
  "image/heic",
  "image/heif",
  "image/jpeg",
  "image/png",
  "image/webp",
  "image/gif",
];

const MAX_FILES = 10;
const MAX_FILE_SIZE_MB = 8;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

export function getFileExtension(filename = "") {
  return filename.includes(".") ? filename.split(".").pop().toLowerCase() : "";
}

export function formatFileSize(bytes = 0) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export function validateFilesClientSide(files) {
  const errors = [];
  const validFiles = [];

  if (files.length > MAX_FILES) {
    errors.push(`You can upload at most ${MAX_FILES} files at once.`);
  }

  files.slice(0, MAX_FILES).forEach((file) => {
    const extension = getFileExtension(file.name);

    if (!ALLOWED_EXTENSIONS.includes(extension)) {
      errors.push(`${file.name}: unsupported extension.`);
      return;
    }

    if (file.type && !ALLOWED_MIME_TYPES.includes(file.type)) {
      errors.push(`${file.name}: unsupported MIME type (${file.type}).`);
      return;
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      errors.push(`${file.name}: exceeds ${MAX_FILE_SIZE_MB} MB limit.`);
      return;
    }

    validFiles.push(file);
  });

  return { validFiles, errors };
}
```

---

## 7) `backend/app/api/v1/uploads.py`

```python
from flask import Blueprint, jsonify, request

from app.schemas.upload_schema import serialize_upload_response
from app.services.file_service import save_uploaded_files

uploads_bp = Blueprint("uploads", __name__, url_prefix="/uploads")


@uploads_bp.post("")
def upload_files():
    files = request.files.getlist("files")

    saved_assets = save_uploaded_files(files)

    return jsonify(
        serialize_upload_response(
            message="Files uploaded successfully.",
            assets=saved_assets,
        )
    ), 201
```

---

## 8) `backend/app/schemas/upload_schema.py`

```python
from app.models.file_asset import FileAsset


def serialize_file_asset(asset: FileAsset) -> dict:
    return {
        "id": asset.id,
        "public_id": asset.public_id,
        "original_filename": asset.original_filename,
        "stored_filename": asset.stored_filename,
        "mime_type": asset.mime_type,
        "extension": asset.extension,
        "size_bytes": asset.size_bytes,
        "storage_path": asset.storage_path,
        "created_at": asset.created_at.isoformat(),
    }


def serialize_upload_response(message: str, assets: list[FileAsset]) -> dict:
    return {
        "message": message,
        "data": {
            "count": len(assets),
            "files": [serialize_file_asset(asset) for asset in assets],
        },
    }
```

---

## 9) `backend/app/services/file_service.py`

```python
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Iterable

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.file_asset import FileAsset
from app.utils.file_types import get_extension
from app.utils.validators import (
    ensure_files_present,
    validate_file_count,
    validate_file_mime_type,
    validate_file_size,
    validate_file_extension,
)


def ensure_upload_directory(upload_dir: str) -> Path:
    path = Path(upload_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_stored_filename(original_filename: str) -> tuple[str, str]:
    safe_name = secure_filename(original_filename)
    extension = get_extension(safe_name)
    unique_token = uuid.uuid4().hex
    stored_filename = f"{Path(safe_name).stem}-{unique_token}.{extension}"
    return stored_filename, extension


def get_file_size(file_storage: FileStorage) -> int:
    current_position = file_storage.stream.tell()
    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(current_position)
    return size


def save_uploaded_files(files: Iterable[FileStorage]) -> list[FileAsset]:
    file_list = list(files)

    ensure_files_present(file_list)
    validate_file_count(file_list)

    upload_dir = ensure_upload_directory(
        os.getenv("UPLOAD_DIR", "app/temp_storage/uploads")
    )

    saved_assets: list[FileAsset] = []

    for file_storage in file_list:
        original_filename = file_storage.filename or ""

        validate_file_extension(original_filename)
        validate_file_mime_type(file_storage.mimetype or "")

        file_size = get_file_size(file_storage)
        validate_file_size(file_size, original_filename)

        stored_filename, extension = build_stored_filename(original_filename)
        stored_path = upload_dir / stored_filename

        file_storage.stream.seek(0)
        file_storage.save(stored_path)

        asset = FileAsset(
            public_id=uuid.uuid4().hex,
            original_filename=original_filename,
            stored_filename=stored_filename,
            mime_type=file_storage.mimetype or "application/octet-stream",
            extension=extension,
            size_bytes=file_size,
            storage_path=str(stored_path),
        )

        db.session.add(asset)
        saved_assets.append(asset)

    db.session.commit()
    return saved_assets
```

---

## 10) `backend/app/utils/file_types.py`

```python
from pathlib import Path

ALLOWED_EXTENSIONS = {
    "heic",
    "heif",
    "jpg",
    "jpeg",
    "png",
    "webp",
    "gif",
}

ALLOWED_MIME_TYPES = {
    "image/heic",
    "image/heif",
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower().replace(".", "")
```

---

## 11) `backend/app/utils/validators.py`

```python
from __future__ import annotations

import os

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge

from app.utils.file_types import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, get_extension


def ensure_files_present(files: list[FileStorage]) -> None:
    if not files:
        raise BadRequest("No files were provided. Use multipart/form-data with the 'files' field.")


def validate_file_count(files: list[FileStorage]) -> None:
    max_files = int(os.getenv("MAX_FILES_PER_UPLOAD", "10"))

    if len(files) > max_files:
        raise BadRequest(f"You can upload at most {max_files} files at once.")


def validate_file_extension(filename: str) -> None:
    extension = get_extension(filename)

    if not extension or extension not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise BadRequest(
            f"Unsupported file extension for '{filename}'. Allowed: {allowed}."
        )


def validate_file_mime_type(mime_type: str) -> None:
    if mime_type not in ALLOWED_MIME_TYPES:
        allowed = ", ".join(sorted(ALLOWED_MIME_TYPES))
        raise BadRequest(
            f"Unsupported MIME type '{mime_type}'. Allowed: {allowed}."
        )


def validate_file_size(file_size: int, filename: str) -> None:
    max_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "8"))
    max_size_bytes = max_size_mb * 1024 * 1024

    if file_size > max_size_bytes:
        raise RequestEntityTooLarge(
            f"'{filename}' exceeds the {max_size_mb} MB size limit."
        )
```

---

## 12) `backend/app/models/file_asset.py`

```python
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FileAsset(Base):
    __tablename__ = "file_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    public_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    mime_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    extension: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return (
            f"<FileAsset id={self.id} original_filename={self.original_filename!r} "
            f"mime_type={self.mime_type!r}>"
        )
```

---

# Required supporting edits

These files were not in your Phase 2 list, but they are required for the phase to actually run.

---

## A) Update `backend/app/config.py`

Replace your current file with this version:

```python
import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://formatbridge_user:formatbridge_pass@127.0.0.1:5433/formatbridge_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ]

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "16777216"))
    MAX_FILES_PER_UPLOAD = int(os.getenv("MAX_FILES_PER_UPLOAD", "10"))
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "8"))
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "app/temp_storage/uploads")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config(config_name: str | None = None):
    name = (config_name or os.getenv("FLASK_ENV", "development")).lower()

    mapping = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    return mapping.get(name, DevelopmentConfig)
```

---

## B) Create `backend/app/api/__init__.py`

```python
from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")
```

---

## C) Create `backend/app/api/v1/__init__.py`

```python
from flask import Blueprint

from app.api.v1.uploads import uploads_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/v1")
api_v1_bp.register_blueprint(uploads_bp)
```

---

## D) Update `backend/app/__init__.py`

Replace your current file with this version:

```python
from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge

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

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(error):
        return jsonify({"message": str(error)}), 413

    return app
```

---

## E) Update `backend/app/models/__init__.py`

Create or replace with:

```python
from .file_asset import FileAsset

__all__ = ["FileAsset"]
```

---

## F) Update `frontend/src/routes/index.jsx`

Replace the Phase 1 routes file with this version:

```jsx
import { createBrowserRouter, Link } from "react-router-dom";
import ConvertPage from "../pages/ConvertPage";

function HomePage() {
  return (
    <main className="min-h-screen">
      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <span className="inline-flex rounded-full bg-brand-50 px-3 py-1 text-sm font-medium text-brand-700">
            Phase 2 upload flow
          </span>

          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900">
            FormatBridge
          </h1>

          <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-600">
            Secure upload, validation, and temporary persistence for supported image formats.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/convert"
              className="inline-flex rounded-xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
            >
              Open upload page
            </Link>

            <a
              href="http://127.0.0.1:5000/api/v1/health"
              target="_blank"
              rel="noreferrer"
              className="inline-flex rounded-xl border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            >
              Check backend health
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}

function NotFoundPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">404</h1>
        <p className="mt-2 text-slate-600">Page not found.</p>
        <Link
          to="/"
          className="mt-4 inline-flex rounded-lg bg-slate-900 px-4 py-2 text-white"
        >
          Go home
        </Link>
      </div>
    </main>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/convert",
    element: <ConvertPage />,
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);

export default router;
```

---

## G) Create `frontend/src/pages/` directory

Run:

```bash
mkdir -p frontend/src/pages
```

---

## H) Create upload component directory

Run:

```bash
mkdir -p frontend/src/components/upload
```

---

## I) Create backend folders if missing

Run:

```bash
mkdir -p backend/app/api/v1
mkdir -p backend/app/schemas
mkdir -p backend/app/services
mkdir -p backend/app/utils
mkdir -p backend/app/models
mkdir -p backend/app/temp_storage/uploads
```

---

# Exact migration commands

From the project root:

```bash
cd backend
source env/bin/activate
flask --app run.py db migrate -m "add file_assets table"
flask --app run.py db upgrade
```

If this is the first migration for this repo, initialize first:

```bash
flask --app run.py db init
flask --app run.py db migrate -m "add file_assets table"
flask --app run.py db upgrade
```

---

# Exact startup order after Phase 2 files are in place

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

## 3. Start frontend
From `frontend/`:

```bash
npm install
npm run dev
```

---

# Completion Check

## Check 1 — valid files upload successfully

Open the frontend:
```text
http://127.0.0.1:5173
```

Go to:
```text
/convert
```

Upload valid files such as:
- `.jpg`
- `.jpeg`
- `.png`
- `.webp`
- `.gif`
- `.heic`

Expected:
- files appear in the selected list
- upload request returns success
- stored file info appears in the success panel

---

## Check 2 — invalid files are rejected cleanly

Try uploading:
- `.exe`
- `.pdf`
- overly large image above 8 MB
- more than 10 files

Expected:
- client-side validation errors appear in the UI
- server-side validation returns 400 or 413 with readable JSON messages

---

## Check 3 — uploaded records are written to DB

Run this exact SQL check:

```bash
docker exec -it formatbridge_postgres psql -U formatbridge_user -d formatbridge_db -c "SELECT id, original_filename, mime_type, size_bytes, created_at FROM file_assets ORDER BY id DESC;"
```

Expected:
- uploaded files appear as rows in `file_assets`

---

# Optional direct API test with curl

Use this command from your machine:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/uploads \
  -F "files=@/absolute/path/to/sample.jpg" \
  -F "files=@/absolute/path/to/sample.png"
```

Expected response shape:

```json
{
  "message": "Files uploaded successfully.",
  "data": {
    "count": 2,
    "files": [
      {
        "id": 1,
        "public_id": "....",
        "original_filename": "sample.jpg",
        "stored_filename": "sample-....jpg",
        "mime_type": "image/jpeg",
        "extension": "jpg",
        "size_bytes": 12345,
        "storage_path": "app/temp_storage/uploads/sample-....jpg",
        "created_at": "2026-04-19T..."
      }
    ]
  }
}
```

---

# What Phase 2 completes

Once this works, your project will have:

- frontend drag-and-drop selection
- multi-file upload UI
- backend upload API
- extension and MIME validation
- single-file size validation
- upload count validation
- temporary persisted files
- database upload records

That is a proper Phase 2 foundation.

---

# Best next step after Phase 2

The next clean move is **Phase 3 — Conversion Job Model and Queue Integration**, where you add:

- `conversion_job.py`
- `conversion_result.py`
- Celery task dispatch
- `/api/v1/conversions`
- `/api/v1/jobs/<job_id>`

That is the correct next stage after uploads are stable.
