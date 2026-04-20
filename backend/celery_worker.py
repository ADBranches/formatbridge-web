from app import create_app

flask_app = create_app()
celery = flask_app.extensions["celery"]

# import task modules so the worker registers them
from app.tasks.conversion_tasks import process_conversion_job_task  # noqa: F401


@celery.task(name="tasks.ping")
def ping():
    return {"message": "pong"}