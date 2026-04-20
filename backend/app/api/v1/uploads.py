from flask import Blueprint, jsonify, request

from app.schemas.upload_schema import serialize_upload_response
from app.services.file_service import save_uploaded_files

uploads_bp = Blueprint("uploads", __name__, url_prefix="/uploads")


@uploads_bp.post("")
def upload_files():
    files = request.files.getlist("files")

    saved_assets = save_uploaded_files(files)

    return jsonify(
        serialize_upload_response(
            message="Files uploaded successfully.",
            assets=saved_assets,
        )
    ), 201