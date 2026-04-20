# FormatBridge — Phase 7: Batch Results and ZIP Packaging

## Objective
Allow multiple outputs to be downloaded in a bundled archive.

This phase gives you:

- ZIP packaging for all successful outputs of a job
- single result download links
- a dedicated results summary screen
- preserved result order inside the ZIP archive

---

# Important note before you start

Phase 7 does **not** need:

- a new database name
- a new PostgreSQL user
- new DB grants
- a new Redis service
- a new migration

Keep using the exact identifiers already established in Phase 1–6:

```env
POSTGRES_DB=formatbridge_db
POSTGRES_USER=formatbridge_user
POSTGRES_PASSWORD=formatbridge_pass
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
DATABASE_URL=postgresql://formatbridge_user:formatbridge_pass@127.0.0.1:5433/formatbridge_db

REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

No new DB permission grant is needed if you are still using the PostgreSQL service already created in Phase 1.

---

# Phase 7 exact additions to `.env`

Add these to your existing `.env` and `.env.example`:

```env
# =========================
# ZIP ARCHIVES
# =========================
ZIP_OUTPUT_DIR=app/temp_storage/archives
```

## Meaning
- `ZIP_OUTPUT_DIR=app/temp_storage/archives` -> packaged job archives will be written here

---

# Create required archive directory

Run this once:

```bash
mkdir -p backend/app/temp_storage/archives
```

---

# Files to Populate

## 1) `backend/app/services/zip_service.py`

```python
from __future__ import annotations

import os
import time
import uuid
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult


def ensure_zip_output_directory(path: str | Path | None = None) -> Path:
    directory = Path(path or os.getenv("ZIP_OUTPUT_DIR", "app/temp_storage/archives"))
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_zip_filename(job_public_id: str) -> str:
    timestamp = int(time.time())
    token = uuid.uuid4().hex[:8]
    return f"{job_public_id}-results-{timestamp}-{token}.zip"


def get_successful_results_for_job(job: ConversionJob) -> list[ConversionResult]:
    results = (
        ConversionResult.query.filter_by(job_id=job.id, status="success")
        .order_by(ConversionResult.id.asc())
        .all()
    )

    filtered_results = [result for result in results if result.output_path]
    if not filtered_results:
        raise ValueError("No successful conversion results are available for ZIP packaging.")

    return filtered_results


def build_unique_archive_name(original_name: str, seen_names: set[str], result_id: int) -> str:
    candidate = original_name
    if candidate not in seen_names:
        seen_names.add(candidate)
        return candidate

    path = Path(original_name)
    candidate = f"{path.stem}-{result_id}{path.suffix}"
    seen_names.add(candidate)
    return candidate


def create_zip_for_job(
    job: ConversionJob,
    output_dir: str | Path | None = None,
) -> dict:
    results = get_successful_results_for_job(job)

    output_directory = ensure_zip_output_directory(output_dir)
    output_filename = build_zip_filename(job.public_id)
    output_path = output_directory / output_filename

    added_files: list[str] = []
    seen_names: set[str] = set()

    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as archive:
        for result in results:
            file_path = Path(result.output_path)
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Generated output file is missing on disk: {result.output_filename or file_path.name}"
                )

            archive_name = build_unique_archive_name(
                result.output_filename or file_path.name,
                seen_names,
                result.id,
            )

            archive.write(file_path, arcname=archive_name)
            added_files.append(archive_name)

    return {
        "output_filename": output_filename,
        "output_path": str(output_path),
        "size_bytes": output_path.stat().st_size,
        "file_count": len(added_files),
        "files": added_files,
    }
```

---

## 2) `backend/app/api/v1/downloads.py`

Replace your current file with this Phase 7 version:

```python
from pathlib import Path

from flask import Blueprint, send_file
from werkzeug.exceptions import NotFound

from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.conversion_result import ConversionResult
from app.services.zip_service import create_zip_for_job

downloads_bp = Blueprint("downloads", __name__, url_prefix="/downloads")

DOCX_MIMETYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


@downloads_bp.get("/results/<int:result_id>")
def download_result(result_id: int):
    result = db.session.get(ConversionResult, result_id)

    if not result:
        raise NotFound("Conversion result was not found.")

    if result.status != "success":
        raise NotFound("Conversion result is not ready for download.")

    if not result.output_path:
        raise NotFound("No output path is recorded for this conversion result.")

    file_path = Path(result.output_path)
    if not file_path.exists():
        raise NotFound("Generated output file is missing on disk.")

    mimetype = None
    if result.output_format == "pdf":
        mimetype = "application/pdf"
    elif result.output_format == "docx":
        mimetype = DOCX_MIMETYPE

    return send_file(
        file_path,
        as_attachment=True,
        download_name=result.output_filename or file_path.name,
        mimetype=mimetype,
    )


@downloads_bp.get("/jobs/<string:job_public_id>/zip")
def download_job_zip(job_public_id: str):
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()

    if not job:
        raise NotFound("Conversion job was not found.")

    zip_bundle = create_zip_for_job(job)
    zip_path = Path(zip_bundle["output_path"])

    if not zip_path.exists():
        raise NotFound("Generated ZIP archive is missing on disk.")

    return send_file(
        zip_path,
        as_attachment=True,
        download_name=zip_bundle["output_filename"],
        mimetype="application/zip",
    )
```

---

## 3) `frontend/src/pages/ResultsPage.jsx`

```jsx
import { Link, useParams } from "react-router-dom";
import JobStatusCard from "../components/jobs/JobStatusCard";
import ResultList from "../components/jobs/ResultList";
import useJobPolling from "../hooks/useJobPolling";

export default function ResultsPage() {
  const { jobId } = useParams();
  const { jobPayload, pollingError, isPolling } = useJobPolling(jobId || null);

  const job = jobPayload?.job;
  const results = jobPayload?.results || [];

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-12">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900">
              Conversion Results
            </h1>
            <p className="mt-2 text-slate-600">
              Review single downloads or package all successful outputs into one ZIP archive.
            </p>
          </div>

          <div className="flex gap-3">
            <Link
              to="/convert"
              className="inline-flex rounded-xl border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Back to convert
            </Link>
          </div>
        </div>

        {jobId && (
          <div className="mt-6 rounded-3xl border border-brand-200 bg-brand-50 p-4 text-sm text-brand-700">
            Tracking job: <span className="font-semibold break-all">{jobId}</span>
            {isPolling && <span className="ml-2">• polling...</span>}
          </div>
        )}

        <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_1fr]">
          <JobStatusCard
            job={job}
            results={results}
            pollingError={pollingError}
          />

          <ResultList
            jobPublicId={job?.public_id || jobId || ""}
            results={results}
          />
        </div>
      </section>
    </main>
  );
}
```

---

## 4) `frontend/src/components/jobs/ResultList.jsx`

```jsx
const API_BASE_URL = "http://127.0.0.1:5000/api/v1";

function buildSingleDownloadUrl(resultId) {
  return `${API_BASE_URL}/downloads/results/${resultId}`;
}

function buildZipDownloadUrl(jobPublicId) {
  return `${API_BASE_URL}/downloads/jobs/${jobPublicId}/zip`;
}

export default function ResultList({ jobPublicId, results = [] }) {
  const successfulResults = results.filter((result) => result.status === "success");
  const failedResults = results.filter((result) => result.status === "failed");

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Downloadable outputs
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Download single results or bundle all successful outputs into one ZIP file.
          </p>
        </div>

        {jobPublicId && successfulResults.length > 0 && (
          <a
            href={buildZipDownloadUrl(jobPublicId)}
            className="inline-flex rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"
          >
            Download ZIP
          </a>
        )}
      </div>

      <div className="mt-6 space-y-4">
        {successfulResults.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
            No successful results available yet.
          </div>
        ) : (
          successfulResults.map((result) => (
            <div
              key={result.id}
              className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4"
            >
              <p className="text-sm font-semibold text-slate-900">
                {result.output_filename || `Result ${result.id}`}
              </p>
              <p className="mt-1 text-xs text-slate-600">
                Format: {result.output_format?.toUpperCase()}
              </p>

              <div className="mt-4">
                <a
                  href={buildSingleDownloadUrl(result.id)}
                  className="inline-flex rounded-xl bg-white px-4 py-2 text-sm font-semibold text-slate-900 shadow-sm ring-1 ring-slate-200 transition hover:bg-slate-50"
                >
                  Download result
                </a>
              </div>
            </div>
          ))
        )}

        {failedResults.length > 0 && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-4">
            <h3 className="text-sm font-semibold text-red-700">
              Failed outputs
            </h3>
            <ul className="mt-2 space-y-2 text-sm text-red-700">
              {failedResults.map((result) => (
                <li key={result.id}>
                  {result.output_filename || `Result ${result.id}`} — {result.status}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
```

---

## 5) `backend/tests/test_jobs.py`

```python
from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from PIL import Image


def create_sample_output_image(path: Path, image_format: str, color: tuple[int, int, int]) -> Path:
    image = Image.new("RGB", (64, 64), color)

    if image_format.upper() == "JPEG":
        image.save(path, format="JPEG")
    elif image_format.upper() == "PNG":
        image.save(path, format="PNG")
    elif image_format.upper() == "WEBP":
        image.save(path, format="WEBP")
    else:
        raise ValueError(f"Unsupported test output format: {image_format}")

    return path


def build_test_app(monkeypatch, tmp_path):
    database_path = tmp_path / "phase7_test.db"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CONVERTED_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("PDF_OUTPUT_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("DOCX_OUTPUT_DIR", str(tmp_path / "converted"))
    monkeypatch.setenv("ZIP_OUTPUT_DIR", str(tmp_path / "archives"))
    monkeypatch.setenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    monkeypatch.setenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

    from app import create_app
    from app.extensions import db
    from app.models.file_asset import FileAsset
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult

    app = create_app("testing")

    with app.app_context():
        _ = FileAsset, ConversionJob, ConversionResult
        db.drop_all()
        db.create_all()

    return app


def test_zip_service_packages_all_successful_results(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)

    from app.extensions import db
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult
    from app.services.zip_service import create_zip_for_job

    converted_dir = tmp_path / "converted"
    converted_dir.mkdir(parents=True, exist_ok=True)

    first_output = create_sample_output_image(converted_dir / "first.jpg", "JPEG", (255, 0, 0))
    second_output = create_sample_output_image(converted_dir / "second.png", "PNG", (0, 255, 0))

    with app.app_context():
        job = ConversionJob(
            public_id="job_zip_1",
            requested_output_format="jpg",
            source_count=2,
            source_public_ids=["a", "b"],
            status="success",
        )
        db.session.add(job)
        db.session.commit()

        result_one = ConversionResult(
            job_id=job.id,
            source_file_id=None,
            output_format="jpg",
            status="success",
            output_filename="first.jpg",
            output_path=str(first_output),
        )
        result_two = ConversionResult(
            job_id=job.id,
            source_file_id=None,
            output_format="png",
            status="success",
            output_filename="second.png",
            output_path=str(second_output),
        )
        db.session.add(result_one)
        db.session.add(result_two)
        db.session.commit()

        zip_bundle = create_zip_for_job(job)

    zip_path = Path(zip_bundle["output_path"])
    assert zip_path.exists()
    assert zip_path.suffix.lower() == ".zip"
    assert zip_bundle["file_count"] == 2
    assert zip_bundle["size_bytes"] > 0

    with ZipFile(zip_path, "r") as archive:
        names = archive.namelist()
        assert names == ["first.jpg", "second.png"]
        archive.extractall(tmp_path / "extracted")

    assert (tmp_path / "extracted" / "first.jpg").exists()
    assert (tmp_path / "extracted" / "second.png").exists()


def test_job_zip_download_endpoint_returns_archive(monkeypatch, tmp_path):
    app = build_test_app(monkeypatch, tmp_path)

    from app.extensions import db
    from app.models.conversion_job import ConversionJob
    from app.models.conversion_result import ConversionResult

    converted_dir = tmp_path / "converted"
    converted_dir.mkdir(parents=True, exist_ok=True)

    first_output = create_sample_output_image(converted_dir / "first.jpg", "JPEG", (255, 0, 0))
    second_output = create_sample_output_image(converted_dir / "second.png", "PNG", (0, 255, 0))

    with app.app_context():
        job = ConversionJob(
            public_id="job_zip_download_1",
            requested_output_format="jpg",
            source_count=2,
            source_public_ids=["a", "b"],
            status="success",
        )
        db.session.add(job)
        db.session.commit()

        result_one = ConversionResult(
            job_id=job.id,
            source_file_id=None,
            output_format="jpg",
            status="success",
            output_filename="first.jpg",
            output_path=str(first_output),
        )
        result_two = ConversionResult(
            job_id=job.id,
            source_file_id=None,
            output_format="png",
            status="success",
            output_filename="second.png",
            output_path=str(second_output),
        )
        db.session.add(result_one)
        db.session.add(result_two)
        db.session.commit()

    client = app.test_client()
    response = client.get("/api/v1/downloads/jobs/job_zip_download_1/zip")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/zip")
    assert "attachment" in response.headers.get("Content-Disposition", "")

    zip_path = tmp_path / "downloaded.zip"
    zip_path.write_bytes(response.data)

    with ZipFile(zip_path, "r") as archive:
        names = archive.namelist()
        assert names == ["first.jpg", "second.png"]
```

---

# Required supporting edits

These files were not in your Phase 7 list, but they are required for the phase to actually run cleanly.

---

## A) Update `frontend/src/routes/index.jsx`

Replace your current file with this Phase 7 version so the new results screen is routable:

```jsx
import { createBrowserRouter, Link } from "react-router-dom";
import ConvertPage from "../pages/ConvertPage";
import ResultsPage from "../pages/ResultsPage";

function HomePage() {
  return (
    <main className="min-h-screen">
      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <span className="inline-flex rounded-full bg-brand-50 px-3 py-1 text-sm font-medium text-brand-700">
            Phase 7 ZIP packaging
          </span>

          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900">
            FormatBridge
          </h1>

          <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-600">
            Batch results, ZIP packaging, and a dedicated results screen.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/convert"
              className="inline-flex rounded-xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
            >
              Open convert page
            </Link>

            <a
              href="http://127.0.0.1:5000/api/v1/health"
              target="_blank"
              rel="noreferrer"
              className="inline-flex rounded-xl border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            >
              Check backend health
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}

function NotFoundPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">404</h1>
        <p className="mt-2 text-slate-600">Page not found.</p>
        <Link
          to="/"
          className="mt-4 inline-flex rounded-lg bg-slate-900 px-4 py-2 text-white"
        >
          Go home
        </Link>
      </div>
    </main>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/convert",
    element: <ConvertPage />,
  },
  {
    path: "/results/:jobId",
    element: <ResultsPage />,
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);

export default router;
```

---

## B) Update `frontend/src/pages/ConvertPage.jsx`

Use this exact targeted edit in the success area after a job is created, so the user can move to the results page:

Find this block:

```jsx
            {jobId && (
              <div className="rounded-3xl border border-brand-200 bg-brand-50 p-4 text-sm text-brand-700">
                Tracking job: <span className="font-semibold break-all">{jobId}</span>
                {isPolling && <span className="ml-2">• polling...</span>}
              </div>
            )}
```

Replace it with:

```jsx
            {jobId && (
              <div className="rounded-3xl border border-brand-200 bg-brand-50 p-4 text-sm text-brand-700">
                <p>
                  Tracking job: <span className="font-semibold break-all">{jobId}</span>
                  {isPolling && <span className="ml-2">• polling...</span>}
                </p>

                <div className="mt-3">
                  <a
                    href={`/results/${jobId}`}
                    className="inline-flex rounded-xl bg-white px-4 py-2 text-sm font-semibold text-slate-900 shadow-sm ring-1 ring-slate-200 transition hover:bg-slate-50"
                  >
                    Open results page
                  </a>
                </div>
              </div>
            )}
```

---

## C) No new package is required for ZIP handling

`zipfile` is part of the Python standard library.

---

# Exact migration command status

No new DB migration is required for Phase 7.

Reason:
- you are reusing the existing `conversion_results` table
- ZIP bundles are generated dynamically from existing successful result rows
- this phase is packaging and download orchestration, not a schema-change phase

---

# Exact startup order after Phase 7 files are in place

## 1. Start infrastructure
From repo root:

```bash
cp .env.example .env
docker compose up -d postgres redis
```

## 2. Start backend
From `backend/`:

```bash
source env/bin/activate
pip install -r requirements.txt
python run.py
```

## 3. Start Celery worker
From `backend/` in a second terminal:

```bash
source env/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```

## 4. Start frontend
From `frontend/`:

```bash
npm install
npm run dev
```

---

# Exact test commands for Phase 7

From `backend/`:

```bash
source env/bin/activate
pytest tests/test_jobs.py -q
```

If you want verbose output:

```bash
pytest tests/test_jobs.py -v
```

---

# Completion Check

## Check 1 — ZIP downloads successfully

Open:

```text
http://127.0.0.1:5173/convert
```

Then:
1. upload files
2. convert them into an output format that creates multiple successful results
3. wait for `success`
4. open the results page
5. click **Download ZIP**

Expected:
- a `.zip` archive downloads
- the archive opens successfully

---

## Check 2 — extracted files are valid

After downloading the ZIP:
1. extract it
2. open the extracted files

Expected:
- each file opens correctly
- the filenames inside the ZIP match the generated outputs

---

## Check 3 — result links match the correct files

On the results page:
- each successful result should have its own **Download result** link
- each link should download the correct individual output
- the ZIP should contain the same successful outputs shown in the list

---

# Optional direct API flow test

## A) Poll a finished job

```bash
curl http://127.0.0.1:5000/api/v1/jobs/PUT_REAL_JOB_PUBLIC_ID_HERE
```

Confirm that `results` contains successful rows.

## B) Download the ZIP bundle directly

```bash
curl -L http://127.0.0.1:5000/api/v1/downloads/jobs/PUT_REAL_JOB_PUBLIC_ID_HERE/zip -o results.zip
```

Expected:
- `results.zip` downloads locally
- it extracts successfully

---

# Exact SQL checks

Check the newest conversion results:

```bash
docker exec -it formatbridge_postgres psql -U formatbridge_user -d formatbridge_db -c "SELECT id, job_id, output_format, status, output_filename, output_path, created_at FROM conversion_results ORDER BY id DESC;"
```

For ZIP packaging, expect:
- existing successful result rows are reused
- no extra DB table is required for the ZIP archive itself

---

# What Phase 7 completes

Once this works, your project will have:

- ZIP packaging for all successful outputs of a job
- preserved result order inside the ZIP bundle
- single result download links
- a dedicated results summary screen
- job-level batch download via `/api/v1/downloads/jobs/<job_public_id>/zip`

That is a proper Phase 7 foundation.

---

# Best next step after Phase 7

The next clean move is **Phase 8 — Cleanup, Error Handling, and Hardening**, where you add:

- temporary file cleanup
- archive cleanup
- more consistent API error responses
- stronger validation and guard rails

That is the correct next stage after batch ZIP packaging is stable.
