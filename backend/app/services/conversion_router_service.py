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