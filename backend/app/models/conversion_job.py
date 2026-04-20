from __future__ import annotations

from datetime import datetime

from app.extensions import db


class ConversionJob(db.Model):
    __tablename__ = "conversion_jobs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(64), nullable=False, unique=True, index=True)

    requested_output_format = db.Column(db.String(20), nullable=False, index=True)
    source_count = db.Column(db.Integer, nullable=False)
    source_public_ids = db.Column(db.JSON, nullable=False)

    ocr_enabled = db.Column(db.Boolean, nullable=False, default=False)

    status = db.Column(db.String(30), nullable=False, default="queued", index=True)
    error_message = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    results = db.relationship(
        "ConversionResult",
        backref="job",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<ConversionJob id={self.id} public_id={self.public_id!r} "
            f"status={self.status!r} output={self.requested_output_format!r} "
            f"ocr_enabled={self.ocr_enabled}>"
        )