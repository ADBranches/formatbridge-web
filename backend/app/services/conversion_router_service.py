from __future__ import annotations

from datetime import datetime
from pathlib import Path

from flask import current_app
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult
from app.models.file_asset import FileAsset
from app.services.image_conversion_service import convert_image_file
from app.utils.naming import build_output_path, normalize_target_format


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
            raise ValueError(
                f"Uploaded source file is missing from the database: {public_id}"
            )
        ordered_files.append(source_file)

    return ordered_files


def create_processing_result(
    job: ConversionJob,
    source_file: FileAsset,
) -> ConversionResult:
    result = ConversionResult(
        job_id=job.id,
        source_file_id=source_file.id,
        output_format=job.requested_output_format,
        status="processing",
        output_filename=None,
        output_path=None,
        size_bytes=0,
        is_zip_bundle=False,
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
    
    job.status = "processing"
    job.started_at = datetime.utcnow()
    job.error_message = None
    db.session.commit()

    converted_count = 0
    normalized_target = normalize_target_format(job.requested_output_format)

    conversions_dir = Path(
        current_app.config.get(
            "CONVERTED_FILES_DIR",
            Path(current_app.instance_path) / "converted",
        )
    )

    for source_file in source_files:
        if not Path(source_file.storage_path).exists():
            raise FileNotFoundError(
                f"Uploaded source file is missing on disk: {source_file.original_filename}"
            )

        result = create_processing_result(job, source_file)

        try:
            output_path = build_output_path(
                directory=conversions_dir,
                original_filename=source_file.original_filename,
                target_format=normalized_target,
            )

            converted_path = convert_image_file(
                source_path=source_file.storage_path,
                output_path=output_path,
                target_format=normalized_target,
            )

            result = db.session.get(ConversionResult, result.id)
            if result is None:
                raise ValueError("Conversion result record could not be reloaded.")

            result.status = "success"
            result.output_filename = converted_path.name
            result.output_path = str(converted_path)
            result.size_bytes = converted_path.stat().st_size
            db.session.commit()

            converted_count += 1

        except Exception as exc:
            db.session.rollback()
            mark_result_failed(result.id)

            job = db.session.get(ConversionJob, job.id)
            if job is not None:
                job.status = "failed"
                job.completed_at = datetime.utcnow()
                job.error_message = str(exc)
                db.session.commit()

            raise
    
    job = db.session.get(ConversionJob, job.id)
    job.status = "completed"
    job.completed_at = datetime.utcnow()
    db.session.commit()
    
    return {
        "job_public_id": job.public_id,
        "requested_output_format": job.requested_output_format,
        "source_count": job.source_count,
        "converted_count": converted_count,
    }