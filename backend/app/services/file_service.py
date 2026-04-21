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
        validate_file_mime_type(file_storage.mimetype or "", original_filename)

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