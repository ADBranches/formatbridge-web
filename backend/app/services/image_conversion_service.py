from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener

from app.utils.naming import ensure_directory, normalize_target_format

register_heif_opener()

SUPPORTED_INPUT_EXTENSIONS = {"heic", "heif", "jpg", "jpeg", "png", "webp"}
SUPPORTED_TARGET_FORMATS = {"jpg", "png", "webp"}

PIL_SAVE_FORMATS = {
    "jpg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
}


def convert_image_file(
    source_path: str | Path,
    output_path: str | Path,
    target_format: str,
) -> Path:
    source = Path(source_path)
    destination = Path(output_path)
    normalized_target = normalize_target_format(target_format)

    if normalized_target not in SUPPORTED_TARGET_FORMATS:
        raise ValueError(
            f"Unsupported output format '{target_format}'. "
            f"Expected one of: {sorted(SUPPORTED_TARGET_FORMATS)}"
        )

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    source_extension = source.suffix.lower().lstrip(".")
    if source_extension not in SUPPORTED_INPUT_EXTENSIONS:
        raise ValueError(
            f"Unsupported input extension '{source_extension}'. "
            f"Expected one of: {sorted(SUPPORTED_INPUT_EXTENSIONS)}"
        )

    ensure_directory(destination.parent)

    try:
        with Image.open(source) as opened_image:
            working_image = ImageOps.exif_transpose(opened_image)
            prepared_image = _prepare_image_for_target(
                image=working_image,
                target_format=normalized_target,
            )

            save_kwargs = _build_save_kwargs(normalized_target)
            prepared_image.save(
                destination,
                format=PIL_SAVE_FORMATS[normalized_target],
                **save_kwargs,
            )
    except UnidentifiedImageError as exc:
        raise ValueError(f"Unsupported or corrupted image file: {source}") from exc

    return destination


def _prepare_image_for_target(image: Image.Image, target_format: str) -> Image.Image:
    if target_format == "jpg":
        return _flatten_to_rgb(image)

    if target_format in {"png", "webp"}:
        if _has_alpha_channel(image):
            return image.convert("RGBA")
        return image.convert("RGB")

    raise ValueError(f"Unsupported target format '{target_format}'.")


def _flatten_to_rgb(image: Image.Image) -> Image.Image:
    if _has_alpha_channel(image):
        rgba_image = image.convert("RGBA")
        background = Image.new("RGBA", rgba_image.size, (255, 255, 255, 255))
        composed = Image.alpha_composite(background, rgba_image)
        return composed.convert("RGB")

    if image.mode not in {"RGB", "L"}:
        return image.convert("RGB")

    if image.mode == "L":
        return image.convert("RGB")

    return image.copy()


def _has_alpha_channel(image: Image.Image) -> bool:
    if image.mode in {"RGBA", "LA"}:
        return True

    if image.mode == "P" and "transparency" in image.info:
        return True

    return "A" in image.getbands()


def _build_save_kwargs(target_format: str) -> dict:
    if target_format == "jpg":
        return {
            "quality": 95,
            "optimize": True,
        }

    if target_format == "png":
        return {
            "optimize": True,
        }

    if target_format == "webp":
        return {
            "quality": 90,
            "method": 6,
        }

    return {}