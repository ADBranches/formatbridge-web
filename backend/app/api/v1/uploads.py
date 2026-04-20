from flask import Blueprint, request

from app.schemas.upload_schema import serialize_upload_response
from app.services.file_service import save_uploaded_files
from app.utils.response import success_response

uploads_bp = Blueprint("uploads", __name__, url_prefix="/uploads")


@uploads_bp.post("")
def upload_files():
    files = request.files.getlist("files")
    saved_assets = save_uploaded_files(files)

    payload = serialize_upload_response(
        message="Files uploaded successfully.",
        assets=saved_assets,
    )

    return success_response(
        message=payload["message"],
        data=payload["data"],
        status_code=201,
    )