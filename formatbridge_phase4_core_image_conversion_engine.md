# Phase 4 — Core Image Conversion Engine

## Objective
Implement the actual image-to-image conversion workflows for the FormatBridge backend.

## Files to Populate
- `backend/app/services/image_conversion_service.py`
- `backend/app/services/conversion_router_service.py`
- `backend/app/utils/naming.py`
- `backend/tests/test_conversions.py`

## MVP Conversions to Support
- HEIC -> JPG
- HEIC -> PNG
- JPG/JPEG/PNG/WEBP -> JPG
- JPG/JPEG/PNG/WEBP -> PNG
- JPG/JPEG/PNG/WEBP -> WEBP

## Before You Paste These Files
This phase assumes the following already exist from earlier phases:
- `app.extensions.db`
- `app.models.file_asset.FileAsset`
- `app.models.conversion_result.ConversionResult`

This phase also needs these Python packages installed:

```bash
cd ~/Downloads/projects/formatbridge-web/backend
source env/bin/activate
python -m pip install Pillow pillow-heif pytest
python -m pip freeze > requirements.txt
```

---

# 1) `backend/app/utils/naming.py`

```python
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
```

---

# 2) `backend/app/services/image_conversion_service.py`

```python
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
```

---

# 3) `backend/app/services/conversion_router_service.py`

```python
from __future__ import annotations

from pathlib import Path

from flask import current_app

from app.extensions import db
from app.models.conversion_result import ConversionResult
from app.models.file_asset import FileAsset
from app.services.image_conversion_service import convert_image_file
from app.utils.naming import build_output_path, normalize_target_format


def convert_asset_to_image_format(
    source_asset: FileAsset,
    target_format: str,
    job_id: int | None = None,
) -> ConversionResult:
    normalized_target = normalize_target_format(target_format)

    conversions_dir = Path(
        current_app.config.get(
            "CONVERTED_FILES_DIR",
            Path(current_app.instance_path) / "converted",
        )
    )

    output_path = build_output_path(
        directory=conversions_dir,
        original_filename=source_asset.original_filename,
        target_format=normalized_target,
    )

    converted_path = convert_image_file(
        source_path=source_asset.storage_path,
        output_path=output_path,
        target_format=normalized_target,
    )

    result = ConversionResult(
        job_id=job_id,
        source_file_id=source_asset.id,
        output_format=normalized_target,
        output_filename=converted_path.name,
        output_path=str(converted_path),
        size_bytes=converted_path.stat().st_size,
        is_zip_bundle=False,
    )

    db.session.add(result)
    db.session.commit()

    return result
```

> **Note:**  
> This script assumes your Phase 3 `ConversionResult` model already has these fields:
> - `job_id`
> - `source_file_id`
> - `output_format`
> - `output_filename`
> - `output_path`
> - `size_bytes`
> - `is_zip_bundle`

If your field names differ, align the constructor in this file to your existing Phase 3 model.

---

# 4) `backend/tests/test_conversions.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest
from flask import Flask
from PIL import Image
from pillow_heif import register_heif_opener

import app.services.conversion_router_service as router_service
from app.services.image_conversion_service import convert_image_file
from app.utils.naming import build_converted_filename


register_heif_opener()


@dataclass
class DummyAsset:
    id: int
    original_filename: str
    storage_path: str


class DummySession:
    def __init__(self) -> None:
        self.added = []
        self.committed = False

    def add(self, obj) -> None:
        self.added.append(obj)

    def commit(self) -> None:
        self.committed = True


class DummyDB:
    def __init__(self) -> None:
        self.session = DummySession()


class DummyConversionResult:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture
def sample_png(tmp_path: Path) -> Path:
    image_path = tmp_path / "sample.png"
    image = Image.new("RGBA", (64, 64), (0, 128, 255, 180))
    image.save(image_path, format="PNG")
    return image_path


@pytest.fixture
def sample_jpg(tmp_path: Path) -> Path:
    image_path = tmp_path / "sample.jpg"
    image = Image.new("RGB", (64, 64), (200, 100, 50))
    image.save(image_path, format="JPEG")
    return image_path


def _create_heic_image(target_path: Path) -> Path:
    image = Image.new("RGB", (64, 64), (10, 200, 90))
    try:
        image.save(target_path, format="HEIF")
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"HEIF encoder unavailable in local environment: {exc}")
    return target_path


def test_build_converted_filename_changes_extension() -> None:
    filename = build_converted_filename("My Photo.HEIC", "png", token="abcd1234")
    assert filename == "my_photo_abcd1234.png"


def test_convert_png_to_jpg(sample_png: Path, tmp_path: Path) -> None:
    output_path = tmp_path / "converted.jpg"

    result = convert_image_file(
        source_path=sample_png,
        output_path=output_path,
        target_format="jpg",
    )

    assert result.exists()

    with Image.open(result) as converted:
        assert converted.format == "JPEG"
        assert converted.mode == "RGB"
        assert converted.size == (64, 64)


def test_convert_jpg_to_webp(sample_jpg: Path, tmp_path: Path) -> None:
    output_path = tmp_path / "converted.webp"

    result = convert_image_file(
        source_path=sample_jpg,
        output_path=output_path,
        target_format="webp",
    )

    assert result.exists()

    with Image.open(result) as converted:
        assert converted.format == "WEBP"
        assert converted.size == (64, 64)


def test_convert_heic_to_png(tmp_path: Path) -> None:
    source_path = _create_heic_image(tmp_path / "sample.heic")
    output_path = tmp_path / "converted.png"

    result = convert_image_file(
        source_path=source_path,
        output_path=output_path,
        target_format="png",
    )

    assert result.exists()

    with Image.open(result) as converted:
        assert converted.format == "PNG"
        assert converted.size == (64, 64)


def test_router_creates_result_record(sample_png: Path, tmp_path: Path, monkeypatch) -> None:
    test_app = Flask(__name__)
    test_app.config["CONVERTED_FILES_DIR"] = str(tmp_path / "converted")

    dummy_db = DummyDB()

    monkeypatch.setattr(router_service, "db", dummy_db)
    monkeypatch.setattr(router_service, "ConversionResult", DummyConversionResult)

    asset = DummyAsset(
        id=7,
        original_filename="sample.png",
        storage_path=str(sample_png),
    )

    with test_app.app_context():
        result = router_service.convert_asset_to_image_format(
            source_asset=asset,
            target_format="webp",
            job_id=99,
        )

    assert dummy_db.session.committed is True
    assert len(dummy_db.session.added) == 1
    assert result.job_id == 99
    assert result.source_file_id == 7
    assert result.output_format == "webp"
    assert result.is_zip_bundle is False
    assert Path(result.output_path).exists()

    with Image.open(result.output_path) as converted:
        assert converted.format == "WEBP"
        assert converted.size == (64, 64)
```

---

# Commands to Run After Populating These Files

## 1. Install the required libraries
```bash
cd ~/Downloads/projects/formatbridge-web/backend
source env/bin/activate
python -m pip install Pillow pillow-heif pytest
python -m pip freeze > requirements.txt
```

## 2. Run the conversion tests
```bash
pytest tests/test_conversions.py -q
```

## 3. Optional direct smoke test from Python shell
```bash
python - <<'PY'
from pathlib import Path
from PIL import Image
from app.services.image_conversion_service import convert_image_file

source = Path("tmp_sample.png")
target = Path("tmp_sample.webp")

Image.new("RGBA", (40, 40), (0, 150, 200, 180)).save(source, "PNG")
convert_image_file(source, target, "webp")

print("Created:", target.exists(), target)
PY
```

---

# Done When
This phase is complete when all of the following are true:

- HEIC -> JPG works
- HEIC -> PNG works
- JPG/JPEG/PNG/WEBP -> JPG works
- JPG/JPEG/PNG/WEBP -> PNG works
- JPG/JPEG/PNG/WEBP -> WEBP works
- converted output files are physically created on disk
- the router writes a `ConversionResult` record
- `pytest tests/test_conversions.py -q` passes
- converted files open correctly with Pillow

---

# Quick Notes
- `register_heif_opener()` is required so Pillow can open HEIC/HEIF files.
- JPG output cannot keep transparency, so this phase flattens alpha onto a white background before saving JPG.
- PNG and WEBP preserve alpha when the source image has transparency.

---

# Recommended Commit
```bash
git add backend/app/services/image_conversion_service.py \
        backend/app/services/conversion_router_service.py \
        backend/app/utils/naming.py \
        backend/tests/test_conversions.py \
        backend/requirements.txt

git commit -m "Implement Phase 4 core image conversion engine"
```
