from __future__ import annotations


def build_test_app(monkeypatch, tmp_path):
    database_path = tmp_path / "phase8_health.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("ZIP_OUTPUT_DIR", str(tmp_path / "archives"))
    monkeypatch.setenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    monkeypatch.setenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

    from app import create_app
    from app.extensions import db
    from app.models.file_asset import FileAsset
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult

    app = create_app("testing")

    with app.app_context():
        _ = FileAsset, ConversionJob, ConversionResult
        db.drop_all()
        db.create_all()

    return app


def test_health_endpoint_returns_consistent_response(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)
    client = app.test_client()

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.get_json()

    assert body["success"] is True
    assert body["message"] == "Health check completed."
    assert body["data"]["service"] == "formatbridge-api"
    assert body["data"]["database"] == "connected"
    assert body["data"]["queue"] == "configured"
    assert body["error"] is None