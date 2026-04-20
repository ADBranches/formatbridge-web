from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.file_asset import FileAsset
from app.schemas.conversion_schema import (
    serialize_conversion_job_created,
    validate_conversion_request,
)
from app.tasks.conversion_tasks import process_conversion_job_task

conversions_bp = Blueprint("conversions", __name__, url_prefix="/conversions")


@conversions_bp.post("")
def create_conversion_job():
    payload = request.get_json(silent=True) or {}
    data = validate_conversion_request(payload)

    source_public_ids = data["file_public_ids"]
    requested_output_format = data["output_format"]

    files = (
        FileAsset.query.filter(FileAsset.public_id.in_(source_public_ids))
        .order_by(FileAsset.id.asc())
        .all()
    )

    if len(files) != len(source_public_ids):
        found_ids = {file.public_id for file in files}
        missing_ids = [public_id for public_id in source_public_ids if public_id not in found_ids]
        raise NotFound(f"Some uploaded files were not found: {', '.join(missing_ids)}")

    job = ConversionJob(
        public_id=__import__("uuid").uuid4().hex,
        requested_output_format=requested_output_format,
        source_count=len(source_public_ids),
        source_public_ids=source_public_ids,
        status="queued",
    )

    db.session.add(job)
    db.session.commit()

    process_conversion_job_task.delay(job.public_id)

    return jsonify(
        serialize_conversion_job_created(
            message="Conversion job created successfully.",
            job=job,
        )
    ), 202