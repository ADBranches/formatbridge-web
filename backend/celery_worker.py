from app import create_app

flask_app = create_app()
celery = flask_app.extensions["celery"]

from app.tasks.cleanup_tasks import cleanup_temp_storage_task  # noqa: F401
from app.tasks.conversion_tasks import process_conversion_job_task  # noqa: F401


@celery.task(name="tasks.ping")
def ping():
    return {"message": "pong"}