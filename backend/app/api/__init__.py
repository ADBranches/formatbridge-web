from flask import Blueprint

from app.api.v1 import api_v1_bp

api_bp = Blueprint("api", __name__)
api_bp.register_blueprint(api_v1_bp)