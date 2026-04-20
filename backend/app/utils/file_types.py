from pathlib import Path

ALLOWED_EXTENSIONS = {
    "heic",
    "heif",
    "jpg",
    "jpeg",
    "png",
    "webp",
    "gif",
}

ALLOWED_MIME_TYPES = {
    "image/heic",
    "image/heif",
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower().replace(".", "")