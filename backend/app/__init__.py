from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest, NotFound, RequestEntityTooLarge

from app.api import api_bp
from app.config import get_config
from app.database import ping_database
from app.extensions import cors, db, init_celery, migrate


def create_app(config_name: str | None = None):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )
    init_celery(app)

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/api/v1/health")
    def health_check():
        database_status = "connected"
        status = "healthy"
        error_message = None

        try:
            ping_database()
        except Exception as exc:
            database_status = "disconnected"
            status = "degraded"
            error_message = str(exc)

        payload = {
            "success": database_status == "connected",
            "message": "Health check completed.",
            "error": error_message,
            "data": {
                "status": status,
                "service": "formatbridge-api",
                "database": database_status,
                "queue": "configured",
            },
        }

        return jsonify(payload), 200 if database_status == "connected" else 503

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return jsonify({
            "success": False,
            "message": str(error),
            "data": None,
        }), 400


    @app.errorhandler(NotFound)
    def handle_not_found(error):
        return jsonify({
            "success": False,
            "message": str(error),
            "data": None,
        }), 404


    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(error):
        return jsonify({
            "success": False,
            "message": str(error),
            "data": None,
        }), 413

    return app