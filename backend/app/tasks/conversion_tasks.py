from __future__ import annotations

from datetime import datetime

from celery.exceptions import Ignore

from app.extensions import celery_app, db
from app.models.conversion_job import ConversionJob
from app.services.conversion_router_service import run_phase3_conversion_job


def get_job_or_raise(job_public_id: str) -> ConversionJob:
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()
    if not job:
        raise ValueError(f"Conversion job '{job_public_id}' was not found.")
    return job


@celery_app.task(name="tasks.process_conversion_job")
def process_conversion_job_task(job_public_id: str):
    job = get_job_or_raise(job_public_id)

    try:
        job.status = "processing"
        job.started_at = datetime.utcnow()
        job.updated_at = datetime.utcnow()
        db.session.commit()

        summary = run_phase3_conversion_job(job_public_id)

        job = get_job_or_raise(job_public_id)
        job.status = "success"
        job.completed_at = datetime.utcnow()
        job.updated_at = datetime.utcnow()
        db.session.commit()

        return {
            "job_public_id": job_public_id,
            "status": "success",
            "summary": summary,
        }

    except Exception as exc:
        db.session.rollback()

        job = ConversionJob.query.filter_by(public_id=job_public_id).first()
        if job:
            job.status = "failed"
            job.error_message = str(exc)
            job.completed_at = datetime.utcnow()
            job.updated_at = datetime.utcnow()
            db.session.commit()

        raise Ignore() from exc