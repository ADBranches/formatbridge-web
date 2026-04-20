from app.models.file_asset import FileAsset


def serialize_file_asset(asset: FileAsset) -> dict:
    return {
        "id": asset.id,
        "public_id": asset.public_id,
        "original_filename": asset.original_filename,
        "stored_filename": asset.stored_filename,
        "mime_type": asset.mime_type,
        "extension": asset.extension,
        "size_bytes": asset.size_bytes,
        "storage_path": asset.storage_path,
        "created_at": asset.created_at.isoformat(),
    }


def serialize_upload_response(message: str, assets: list[FileAsset]) -> dict:
    return {
        "message": message,
        "data": {
            "count": len(assets),
            "files": [serialize_file_asset(asset) for asset in assets],
        },
    }