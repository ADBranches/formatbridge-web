from pathlib import Path

from flask import Blueprint, current_app, send_file
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult
from app.services.zip_service import create_zip_for_job

downloads_bp = Blueprint("downloads", __name__, url_prefix="/downloads")

DOCX_MIMETYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


def resolve_output_path(stored_path: str) -> Path:
    path = Path(stored_path)

    if path.is_absolute():
        return path

    backend_root = Path(current_app.root_path).parent
    return (backend_root / path).resolve()


@downloads_bp.get("/results/<int:result_id>")
def download_result(result_id: int):
    result = db.session.get(ConversionResult, result_id)

    if not result:
        raise NotFound("Conversion result was not found.")

    if result.status != "success":
        raise NotFound("Conversion result is not ready for download.")

    if not result.output_path:
        raise NotFound("No output path is recorded for this conversion result.")

    file_path = resolve_output_path(result.output_path)

    if not file_path.exists():
        raise NotFound("Generated output file is missing on disk.")

    mimetype = None
    if result.output_format == "pdf":
        mimetype = "application/pdf"
    elif result.output_format == "docx":
        mimetype = DOCX_MIMETYPE

    return send_file(
        file_path,
        as_attachment=True,
        download_name=result.output_filename or file_path.name,
        mimetype=mimetype,
    )


@downloads_bp.get("/jobs/<string:job_public_id>/zip")
def download_job_zip(job_public_id: str):
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()

    if not job:
        raise NotFound("Conversion job was not found.")

    zip_bundle = create_zip_for_job(job)
    zip_path = resolve_output_path(zip_bundle["output_path"])

    if not zip_path.exists():
        raise NotFound("Generated ZIP archive is missing on disk.")

    return send_file(
        zip_path,
        as_attachment=True,
        download_name=zip_bundle["output_filename"],
        mimetype="application/zip",
    )