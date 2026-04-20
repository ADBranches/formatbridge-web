from datetime import datetime

from app.extensions import db


class ConversionResult(db.Model):
    __tablename__ = "conversion_results"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(
        db.Integer,
        db.ForeignKey("conversion_jobs.id"),
        nullable=False,
        index=True,
    )
    source_file_id = db.Column(
        db.Integer,
        db.ForeignKey("file_assets.id"),
        nullable=True,
        index=True,
    )
    output_format = db.Column(db.String(20), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="processing")
    output_filename = db.Column(db.String(255), nullable=True)
    output_path = db.Column(db.String(500), nullable=True, unique=True)
    size_bytes = db.Column(db.Integer, nullable=False, default=0)
    is_zip_bundle = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<ConversionResult id={self.id} output_filename={self.output_filename!r} "
            f"output_format={self.output_format!r}>"
        )