from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename


FORMAT_ALIASES = {
    "jpg": "jpg",
    "jpeg": "jpg",
    "png": "png",
    "webp": "webp",
}


def normalize_target_format(target_format: str) -> str:
    normalized = (target_format or "").strip().lower().lstrip(".")

    if normalized not in FORMAT_ALIASES:
        raise ValueError(
            f"Unsupported target format '{target_format}'. "
            f"Expected one of: {sorted(FORMAT_ALIASES)}"
        )

    return FORMAT_ALIASES[normalized]


def get_output_extension(output_format: str) -> str:
    return normalize_target_format(output_format)


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_converted_filename(original_filename: str, output_format: str) -> str:
    safe_name = secure_filename(original_filename) or "converted_file"
    base_stem = Path(safe_name).stem.strip() or "converted_file"
    normalized_stem = (
        "".join(
            char if char.isalnum() or char in {"-", "_"} else "_"
            for char in base_stem
        ).strip("_")
        or "converted_file"
    )
    extension = get_output_extension(output_format)
    unique_suffix = uuid4().hex[:10]

    return f"{normalized_stem}_{unique_suffix}.{extension}"


def build_output_path(
    directory: str | Path,
    original_filename: str,
    target_format: str,
) -> Path:
    normalized_target = normalize_target_format(target_format)
    output_dir = ensure_directory(directory)

    stem = Path(original_filename).stem.strip() or "converted_file"
    safe_stem = "".join(
        char if char.isalnum() or char in {"-", "_"} else "_"
        for char in stem
    ).strip("_") or "converted_file"

    unique_suffix = uuid4().hex[:10]
    return output_dir / f"{safe_stem}_{unique_suffix}.{normalized_target}"