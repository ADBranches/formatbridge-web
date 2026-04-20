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