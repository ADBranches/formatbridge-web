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