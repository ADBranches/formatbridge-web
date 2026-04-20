from __future__ import annotations

from app.extensions import celery_app
from app.services.cleanup_service import cleanup_all_temp_storage


@celery_app.task(name="tasks.cleanup_temp_storage")
def cleanup_temp_storage_task():
    return cleanup_all_temp_storage()