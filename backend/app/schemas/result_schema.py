from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult
from app.schemas.conversion_schema import serialize_conversion_job_summary


def serialize_conversion_result(result: ConversionResult) -> dict:
    return {
        "id": result.id,
        "job_id": result.job_id,
        "source_file_id": result.source_file_id,
        "output_format": result.output_format,
        "status": result.status,
        "output_filename": result.output_filename,
        "output_path": result.output_path,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }


def serialize_job_status_response(message: str, job: ConversionJob) -> dict:
    return {
        "message": message,
        "data": {
            "job": serialize_conversion_job_summary(job),
            "results": [serialize_conversion_result(result) for result in job.results],
        },
    }