from __future__ import annotations

import os

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge

from app.utils.file_types import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, get_extension


EXTENSION_MIME_FALLBACKS = {
    "heic": {"application/octet-stream"},
    "heif": {"application/octet-stream"},
}


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


def validate_file_mime_type(mime_type: str, filename: str = "") -> None:
    extension = get_extension(filename)

    if mime_type in ALLOWED_MIME_TYPES:
        return

    if extension in EXTENSION_MIME_FALLBACKS and mime_type in EXTENSION_MIME_FALLBACKS[extension]:
        return

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
