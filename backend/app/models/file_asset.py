from datetime import datetime

from app.extensions import db


class FileAsset(db.Model):
    __tablename__ = "file_assets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(64), nullable=False, unique=True, index=True)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False, unique=True)
    mime_type = db.Column(db.String(120), nullable=False, index=True)
    extension = db.Column(db.String(20), nullable=False, index=True)
    size_bytes = db.Column(db.Integer, nullable=False)
    storage_path = db.Column(db.String(500), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<FileAsset id={self.id} original_filename={self.original_filename!r} "
            f"mime_type={self.mime_type!r}>"
        )