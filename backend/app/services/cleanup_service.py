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