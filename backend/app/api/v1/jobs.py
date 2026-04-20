from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound

from app.models.conversion_job import ConversionJob
from app.schemas.result_schema import serialize_job_status_response

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs_bp.get("/<string:job_public_id>")
def get_job_status(job_public_id: str):
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()

    if not job:
        raise NotFound("Conversion job was not found.")

    return jsonify(
        serialize_job_status_response(
            message="Job status fetched successfully.",
            job=job,
        )
    ), 200