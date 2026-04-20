from __future__ import annotations

import os
import time
import uuid
from pathlib import Path

from PIL import Image, ImageSequence, UnidentifiedImageError
from pillow_heif import register_heif_opener
from werkzeug.utils import secure_filename

from app.models.file_asset import FileAsset

register_heif_opener()


def ensure_pdf_output_directory(path: str | Path | None = None) -> Path:
    directory = Path(path or os.getenv("PDF_OUTPUT_DIR", "app/temp_storage/converted"))
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_pdf_filename(source_files: list[FileAsset]) -> str:
    timestamp = int(time.time())
    token = uuid.uuid4().hex[:8]

    if len(source_files) == 1:
        base_name = secure_filename(source_files[0].original_filename) or "file"
        stem = Path(base_name).stem or "file"
        return f"{stem}-{timestamp}-{token}.pdf"

    return f"merged-{timestamp}-{token}.pdf"


def flatten_image_for_pdf(image: Image.Image) -> Image.Image:
    if image.mode == "RGB":
        return image.copy()

    if image.mode in ("RGBA", "LA"):
        rgba_image = image.convert("RGBA")
        background = Image.new("RGB", rgba_image.size, (255, 255, 255))
        background.paste(rgba_image, mask=rgba_image.getchannel("A"))
        return background

    if image.mode == "P":
        rgba_image = image.convert("RGBA")
        background = Image.new("RGB", rgba_image.size, (255, 255, 255))
        background.paste(rgba_image, mask=rgba_image.getchannel("A"))
        return background

    return image.convert("RGB")


def open_pdf_ready_image(source_path: str | Path) -> Image.Image:
    try:
        with Image.open(source_path) as image:
            first_frame = next(ImageSequence.Iterator(image), image)
            return flatten_image_for_pdf(first_frame)
    except UnidentifiedImageError as exc:
        raise ValueError(f"Unsupported or unreadable image file: {source_path}") from exc


def create_pdf_from_images(
    source_files: list[FileAsset],
    output_dir: str | Path | None = None,
) -> dict:
    if not source_files:
        raise ValueError("At least one source file is required to create a PDF.")

    output_directory = ensure_pdf_output_directory(output_dir)
    output_filename = build_pdf_filename(source_files)
    output_path = output_directory / output_filename

    prepared_images: list[Image.Image] = []

    try:
        for source_file in source_files:
            file_path = Path(source_file.storage_path)
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Uploaded source file is missing on disk: {source_file.original_filename}"
                )

            prepared_images.append(open_pdf_ready_image(file_path))

        first_image, *remaining_images = prepared_images

        first_image.save(
            output_path,
            format="PDF",
            save_all=True,
            append_images=remaining_images,
            resolution=float(os.getenv("PDF_IMAGE_RESOLUTION", "100.0")),
        )

        return {
            "output_filename": output_filename,
            "output_path": str(output_path),
            "output_format": "pdf",
            "size_bytes": output_path.stat().st_size,
            "page_count": len(prepared_images),
        }

    finally:
        for image in prepared_images:
            image.close()