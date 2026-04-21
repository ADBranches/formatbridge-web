from flask import Blueprint

from app.api.v1.auth import get_current_user_from_request
from app.models.conversion_job import ConversionJob
from app.schemas.result_schema import serialize_job_status_response
from app.utils.response import success_response
from werkzeug.exceptions import NotFound

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs_bp.get("/<string:job_public_id>")
def get_job_status(job_public_id: str):
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()

    if not job:
        raise NotFound("Conversion job was not found.")

    payload = serialize_job_status_response(
        message="Job status fetched successfully.",
        job=job,
    )
    return success_response(
        message=payload["message"],
        data=payload["data"],
        status_code=200,
    )


@jobs_bp.get("/history")
def get_job_history():
    current_user = get_current_user_from_request(required=True)

    jobs = (
        ConversionJob.query.filter_by(user_id=current_user.id)
        .order_by(ConversionJob.created_at.desc())
        .all()
    )

    serialized_jobs = [
        {
            "public_id": job.public_id,
            "requested_output_format": job.requested_output_format,
            "source_count": job.source_count,
            "ocr_enabled": job.ocr_enabled,
            "status": job.status,
            "created_at": job.created_at.isoformat(),
        }
        for job in jobs
    ]

    return success_response(
        "Conversion history fetched successfully.",
        data={"jobs": serialized_jobs},
        status_code=200,
    )