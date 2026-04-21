import os
import uuid

from flask import Blueprint, request
from werkzeug.exceptions import NotFound, Unauthorized

from app.api.v1.auth import get_current_user_from_request
from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.file_asset import FileAsset
from app.schemas.conversion_schema import (
    serialize_conversion_job_created,
    validate_conversion_request,
)
from app.tasks.conversion_tasks import process_conversion_job_task
from app.utils.response import success_response

conversions_bp = Blueprint("conversions", __name__, url_prefix="/conversions")


@conversions_bp.post("")
def create_conversion_job():
    payload = request.get_json(silent=True) or {}
    data = validate_conversion_request(payload)

    source_public_ids = data["file_public_ids"]
    requested_output_format = data["output_format"]
    ocr_enabled = data["ocr_enabled"]

    allow_anonymous = os.getenv("ALLOW_ANONYMOUS_CONVERSIONS", "true").lower() == "true"
    current_user = get_current_user_from_request(required=False)

    if not current_user and not allow_anonymous:
        raise Unauthorized("Authentication is required to create conversion jobs.")

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
        public_id=uuid.uuid4().hex,
        user_id=current_user.id if current_user else None,
        requested_output_format=requested_output_format,
        source_count=len(source_public_ids),
        source_public_ids=source_public_ids,
        ocr_enabled=ocr_enabled,
        status="queued",
    )

    db.session.add(job)
    db.session.commit()

    process_conversion_job_task.delay(job.public_id)

    payload = serialize_conversion_job_created(
        message="Conversion job created successfully.",
        job=job,
    )

    return success_response(
        message=payload["message"],
        data=payload["data"],
        status_code=202,
    )