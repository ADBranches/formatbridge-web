from flask import Blueprint

from app.api.v1.conversions import conversions_bp
from app.api.v1.downloads import downloads_bp
from app.api.v1.jobs import jobs_bp
from app.api.v1.uploads import uploads_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/v1")
api_v1_bp.register_blueprint(uploads_bp)
api_v1_bp.register_blueprint(conversions_bp)
api_v1_bp.register_blueprint(jobs_bp)
api_v1_bp.register_blueprint(downloads_bp)