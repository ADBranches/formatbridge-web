from __future__ import annotations

import os
import time
import uuid
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult


def ensure_zip_output_directory(path: str | Path | None = None) -> Path:
    directory = Path(path or os.getenv("ZIP_OUTPUT_DIR", "app/temp_storage/archives"))
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_zip_filename(job_public_id: str) -> str:
    timestamp = int(time.time())
    token = uuid.uuid4().hex[:8]
    return f"{job_public_id}-results-{timestamp}-{token}.zip"


def get_successful_results_for_job(job: ConversionJob) -> list[ConversionResult]:
    results = (
        ConversionResult.query.filter_by(job_id=job.id, status="success")
        .order_by(ConversionResult.id.asc())
        .all()
    )

    filtered_results = [result for result in results if result.output_path]
    if not filtered_results:
        raise ValueError("No successful conversion results are available for ZIP packaging.")

    return filtered_results


def build_unique_archive_name(original_name: str, seen_names: set[str], result_id: int) -> str:
    candidate = original_name
    if candidate not in seen_names:
        seen_names.add(candidate)
        return candidate

    path = Path(original_name)
    candidate = f"{path.stem}-{result_id}{path.suffix}"
    seen_names.add(candidate)
    return candidate


def create_zip_for_job(
    job: ConversionJob,
    output_dir: str | Path | None = None,
) -> dict:
    results = get_successful_results_for_job(job)

    output_directory = ensure_zip_output_directory(output_dir)
    output_filename = build_zip_filename(job.public_id)
    output_path = output_directory / output_filename

    added_files: list[str] = []
    seen_names: set[str] = set()

    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as archive:
        for result in results:
            file_path = Path(result.output_path)
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Generated output file is missing on disk: {result.output_filename or file_path.name}"
                )

            archive_name = build_unique_archive_name(
                result.output_filename or file_path.name,
                seen_names,
                result.id,
            )

            archive.write(file_path, arcname=archive_name)
            added_files.append(archive_name)

    return {
        "output_filename": output_filename,
        "output_path": str(output_path),
        "size_bytes": output_path.stat().st_size,
        "file_count": len(added_files),
        "files": added_files,
    }