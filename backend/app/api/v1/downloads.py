from pathlib import Path

from flask import Blueprint, send_file
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_result import ConversionResult

downloads_bp = Blueprint("downloads", __name__, url_prefix="/downloads")

DOCX_MIMETYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


@downloads_bp.get("/results/<int:result_id>")
def download_result(result_id: int):
    result = db.session.get(ConversionResult, result_id)

    if not result:
        raise NotFound("Conversion result was not found.")

    if result.status != "success":
        raise NotFound("Conversion result is not ready for download.")

    if not result.output_path:
        raise NotFound("No output path is recorded for this conversion result.")

    file_path = Path(result.output_path)
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