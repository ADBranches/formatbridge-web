from __future__ import annotations

import re
import secrets
from pathlib import Path


TARGET_FORMAT_ALIASES = {
    "jpeg": "jpg",
    "jpg": "jpg",
    "png": "png",
    "webp": "webp",
}

TARGET_FORMATS = set(TARGET_FORMAT_ALIASES.values())


def normalize_target_format(target_format: str) -> str:
    normalized = target_format.strip().lower().lstrip(".")
    normalized = TARGET_FORMAT_ALIASES.get(normalized, normalized)

    if normalized not in TARGET_FORMATS:
        raise ValueError(
            f"Unsupported target format '{target_format}'. "
            f"Expected one of: {sorted(TARGET_FORMATS)}"
        )

    return normalized


def sanitize_stem(filename: str) -> str:
    raw_stem = Path(filename).stem.strip().lower()
    raw_stem = re.sub(r"[^a-z0-9]+", "_", raw_stem)
    raw_stem = re.sub(r"_+", "_", raw_stem).strip("_")
    return raw_stem or "file"


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_converted_filename(
    original_filename: str,
    target_format: str,
    token: str | None = None,
) -> str:
    normalized_format = normalize_target_format(target_format)
    safe_stem = sanitize_stem(original_filename)
    suffix = token or secrets.token_hex(4)
    return f"{safe_stem}_{suffix}.{normalized_format}"


def build_output_path(
    directory: str | Path,
    original_filename: str,
    target_format: str,
    token: str | None = None,
) -> Path:
    ensured_directory = ensure_directory(directory)
    filename = build_converted_filename(
        original_filename=original_filename,
        target_format=target_format,
        token=token,
    )
    return ensured_directory / filename