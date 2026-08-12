# YouTube Web Downloader Development Timeline

## Project Overview

**Project root:**

```text
/home/trovas/Downloads/projects/byupw/block4_2026/youtube-web-downloader
```

**Development environment:**

- Kali GNU/Linux, Debian-based
- Python 3.13
- FastAPI backend
- React 19 with TypeScript and Vite frontend
- Tailwind CSS 4
- yt-dlp media engine
- FFmpeg and FFprobe media processing
- SQLite local persistence
- Server-Sent Events for download progress
- Localhost-only initial deployment

## Development Strategy

The project will use a **backend-foundation-first, synchronized vertical-slice strategy**.

1. Establish the backend foundation and API conventions first.
2. Correct and complete the frontend toolchain.
3. Develop each user-facing feature across backend and frontend in sync.
4. Run targeted tests after each feature.
5. Run full regression tests only at phase gates and release milestones.

The frontend must not depend on invented media data. Backend response schemas will be established before the corresponding frontend feature is implemented.

## Safety and Product Boundaries

The application is intended for media that the user owns, media in the public domain, appropriately licensed media, or content whose creator has authorized downloading.

The application will not implement:

- DRM circumvention
- Paywall bypass
- CAPTCHA bypass
- Private-video access workarounds
- Age-restriction bypass
- Arbitrary cookie extraction
- Arbitrary shell command execution
- User-controlled raw yt-dlp arguments
- Downloading from local files or private network addresses

---

# Confirmed Baseline Before Phase 1

## Existing Directories

```text
youtube-web-downloader/
├── backend/
├── frontend/
│   ├── dist/
│   ├── public/
│   └── src/
├── storage/
│   ├── downloads/
│   ├── thumbnails/
│   └── tmp/
└── .git/
```

## Existing Files

```text
backend/requirements-lock.txt
frontend/.gitignore
frontend/.oxlintrc.json
frontend/README.md
frontend/index.html
frontend/package.json
frontend/package-lock.json
frontend/public/favicon.svg
frontend/public/icons.svg
frontend/src/App.css
frontend/src/App.tsx
frontend/src/index.css
frontend/src/main.tsx
frontend/tsconfig.app.json
frontend/tsconfig.json
frontend/tsconfig.node.json
frontend/vite.config.ts
```

## Confirmed Environment State

- Backend runtime dependencies are installed.
- Backend development dependencies still need verification or installation.
- Frontend production build succeeds.
- Node.js 20 is installed, but selected frontend test dependencies require Node.js 22 or newer.
- Tailwind packages are installed but not yet connected to Vite or the stylesheet.
- Port `8000` is occupied by another Python process.
- Port `8001` is available for this project.
- Backend application source files do not yet exist.
- The Git branch is initially named `master` and should be renamed to `main`.
- A repository-level `.gitignore` does not yet exist.

---

# Phase 1: Backend Foundation

## Primary Objective

Create a minimal, testable, localhost-only FastAPI application that defines backend structure, settings, routing conventions, health reporting, and code-quality checks.

## Directories Exclusive to Phase 1

```text
backend/app/
backend/app/api/
backend/app/api/routes/
backend/app/core/
backend/app/schemas/
backend/tests/
```

## Files Exclusive to Phase 1

```text
backend/app/__init__.py
backend/app/main.py
backend/app/api/__init__.py
backend/app/api/router.py
backend/app/api/routes/__init__.py
backend/app/api/routes/health.py
backend/app/core/__init__.py
backend/app/core/config.py
backend/app/schemas/__init__.py
backend/app/schemas/health.py
backend/tests/__init__.py
backend/tests/test_health.py
backend/pytest.ini
backend/ruff.toml
.gitignore
storage/downloads/.gitkeep
storage/thumbnails/.gitkeep
storage/tmp/.gitkeep
```

## Specific Objectives

1. Install and verify `pytest`, `pytest-asyncio`, `httpx`, and `ruff`.
2. Create the FastAPI application factory.
3. Define centralized settings using `pydantic-settings`.
4. Define the `/api/v1` API prefix.
5. Implement `GET /api/v1/health`.
6. Define a typed health-response schema.
7. Configure targeted backend tests.
8. Configure Ruff linting and import ordering.
9. Add repository-wide ignore rules.
10. Preserve empty storage directories with `.gitkeep` files.
11. Rename the Git branch from `master` to `main`.
12. Run the backend on `127.0.0.1:8001` while port `8000` remains occupied.

## Targeted Tests

```text
backend/tests/test_health.py
```

Test cases:

- Health endpoint returns HTTP 200.
- Health response reports `healthy`.
- Health response contains service name, application version, and environment.
- OpenAPI includes `/api/v1/health`.

## Completion Criteria

- Backend imports without errors.
- Ruff reports no violations.
- Targeted health tests pass.
- `GET http://127.0.0.1:8001/api/v1/health` returns valid JSON.
- API documentation opens at `http://127.0.0.1:8001/docs`.
- Git branch is `main`.
- Root `.gitignore` excludes virtual environments, build output, local configuration, and generated downloads.

---

# Phase 2: Frontend Toolchain and API Connectivity

## Primary Objective

Correct the frontend runtime and testing environment, activate Tailwind CSS, establish the backend proxy, and prove frontend-to-backend connectivity.

## Directories Exclusive to Phase 2

```text
frontend/src/components/
frontend/src/lib/
frontend/src/types/
frontend/src/test/
```

## Files Exclusive to Phase 2

```text
frontend/.nvmrc
frontend/src/components/ApiStatus.tsx
frontend/src/components/ApiStatus.test.tsx
frontend/src/lib/api.ts
frontend/src/types/api.ts
frontend/src/test/setup.ts
frontend/vitest.config.ts
```

## Existing Files Modified in Phase 2

```text
frontend/package.json
frontend/package-lock.json
frontend/vite.config.ts
frontend/src/App.tsx
frontend/src/App.css
frontend/src/index.css
frontend/README.md
```

## Specific Objectives

1. Upgrade or select a compatible Node.js 22 LTS environment.
2. Record the selected Node version in `.nvmrc`.
3. Reinstall frontend dependencies under the compatible Node version.
4. Add the Tailwind Vite plugin.
5. Import Tailwind in the main stylesheet.
6. Add a Vite proxy from `/api` to `http://127.0.0.1:8001`.
7. Add Vitest scripts and browser simulation configuration.
8. Create a typed API client wrapper.
9. Create a simple API status component.
10. Verify that the browser can reach the backend health endpoint through the Vite proxy.

## Targeted Tests

```text
frontend/src/components/ApiStatus.test.tsx
```

Test cases:

- Loading state is displayed while the health request is pending.
- Healthy state is displayed after a successful response.
- Unavailable state is displayed after a failed response.

## Completion Criteria

- Node engine warnings are eliminated.
- Tailwind utility classes compile.
- Vitest executes successfully.
- Frontend build succeeds.
- Frontend lint succeeds.
- `/api/v1/health` is accessed through the Vite proxy.
- The interface displays backend availability accurately.

---

# Phase 3: URL Validation and Media Metadata Inspection

## Primary Objective

Allow a user to submit a permitted media URL and receive normalized metadata and available media formats without downloading the media.

## Directories Exclusive to Phase 3

```text
backend/app/services/
backend/app/exceptions/
frontend/src/features/media-inspection/
```

## Files Exclusive to Phase 3

```text
backend/app/services/__init__.py
backend/app/services/url_validator.py
backend/app/services/media_inspector.py
backend/app/exceptions/__init__.py
backend/app/exceptions/media.py
backend/app/api/routes/media.py
backend/app/schemas/media.py
backend/tests/test_url_validator.py
backend/tests/test_media_inspector.py
backend/tests/test_media_route.py
frontend/src/features/media-inspection/UrlForm.tsx
frontend/src/features/media-inspection/MediaPreview.tsx
frontend/src/features/media-inspection/FormatList.tsx
frontend/src/features/media-inspection/mediaApi.ts
frontend/src/features/media-inspection/mediaTypes.ts
frontend/src/features/media-inspection/UrlForm.test.tsx
frontend/src/features/media-inspection/MediaPreview.test.tsx
```

## Existing Files Modified in Phase 3

```text
backend/app/api/router.py
backend/app/main.py
frontend/src/App.tsx
frontend/src/lib/api.ts
```

## Specific Objectives

1. Accept only `http` and `https` URLs.
2. Reject local files, localhost addresses, loopback addresses, and private network targets.
3. Normalize supported YouTube URL variants.
4. Inspect metadata with yt-dlp without downloading media.
5. Return title, uploader, duration, thumbnail, webpage URL, and normalized format options.
6. Prevent raw yt-dlp output from leaking directly into the frontend API contract.
7. Present URL validation errors clearly.
8. Display metadata and available formats in the frontend.
9. Add request timeout handling.
10. Avoid credential, cookie, private-video, and bypass functionality.

## Targeted Tests

Backend:

```text
backend/tests/test_url_validator.py
backend/tests/test_media_inspector.py
backend/tests/test_media_route.py
```

Frontend:

```text
frontend/src/features/media-inspection/UrlForm.test.tsx
frontend/src/features/media-inspection/MediaPreview.test.tsx
```

Test cases include:

- Valid public URL is accepted.
- Malformed URL is rejected.
- Localhost and private-address URLs are rejected.
- Metadata is normalized correctly.
- Empty and unavailable format lists are handled.
- Frontend loading, success, and failure states render correctly.

## Completion Criteria

- A permitted URL can be inspected from the browser.
- No media file is downloaded during inspection.
- Backend returns normalized typed data.
- Invalid and unsafe URLs are rejected.
- Targeted backend and frontend tests pass.

---

# Phase 4: Download Job Creation and Format Selection

## Primary Objective

Create a controlled download job from a previously inspected media item and selected output format.

## Directories Exclusive to Phase 4

```text
backend/app/jobs/
frontend/src/features/download-jobs/
```

## Files Exclusive to Phase 4

```text
backend/app/jobs/__init__.py
backend/app/jobs/models.py
backend/app/jobs/manager.py
backend/app/services/download_service.py
backend/app/services/filename_service.py
backend/app/api/routes/downloads.py
backend/app/schemas/download.py
backend/tests/test_filename_service.py
backend/tests/test_job_manager.py
backend/tests/test_download_route.py
frontend/src/features/download-jobs/FormatSelector.tsx
frontend/src/features/download-jobs/DownloadButton.tsx
frontend/src/features/download-jobs/DownloadJobCard.tsx
frontend/src/features/download-jobs/downloadApi.ts
frontend/src/features/download-jobs/downloadTypes.ts
frontend/src/features/download-jobs/FormatSelector.test.tsx
frontend/src/features/download-jobs/DownloadButton.test.tsx
```

## Existing Files Modified in Phase 4

```text
backend/app/api/router.py
backend/app/core/config.py
frontend/src/App.tsx
frontend/src/features/media-inspection/MediaPreview.tsx
```

## Specific Objectives

1. Define controlled job states: queued, running, processing, completed, failed, and cancelled.
2. Create unique server-generated job identifiers.
3. Allow selection of normalized format identifiers only.
4. Reject raw command-line arguments from clients.
5. Generate safe filenames.
6. Confine output paths to `storage/downloads/`.
7. Place incomplete files in `storage/tmp/`.
8. Apply maximum job-count and concurrency controls.
9. Return the job immediately after creation.
10. Display job status in the frontend.

## Targeted Tests

Backend:

```text
backend/tests/test_filename_service.py
backend/tests/test_job_manager.py
backend/tests/test_download_route.py
```

Frontend:

```text
frontend/src/features/download-jobs/FormatSelector.test.tsx
frontend/src/features/download-jobs/DownloadButton.test.tsx
```

## Completion Criteria

- A valid format can create a queued job.
- Invalid format identifiers are rejected.
- Generated file paths cannot escape the storage directory.
- The frontend displays the created job and initial state.
- Targeted tests pass.

---

# Phase 5: Real-Time Progress and Cancellation

## Primary Objective

Provide live progress updates from the backend and allow active jobs to be cancelled safely.

## Directories Exclusive to Phase 5

```text
backend/app/events/
frontend/src/features/download-progress/
```

## Files Exclusive to Phase 5

```text
backend/app/events/__init__.py
backend/app/events/broker.py
backend/app/schemas/progress.py
backend/tests/test_progress_broker.py
backend/tests/test_progress_stream.py
backend/tests/test_job_cancellation.py
frontend/src/features/download-progress/ProgressBar.tsx
frontend/src/features/download-progress/ProgressDetails.tsx
frontend/src/features/download-progress/CancelDownloadButton.tsx
frontend/src/features/download-progress/useDownloadProgress.ts
frontend/src/features/download-progress/ProgressBar.test.tsx
frontend/src/features/download-progress/useDownloadProgress.test.tsx
```

## Existing Files Modified in Phase 5

```text
backend/app/api/routes/downloads.py
backend/app/jobs/manager.py
backend/app/services/download_service.py
backend/app/schemas/download.py
frontend/src/features/download-jobs/DownloadJobCard.tsx
```

## Specific Objectives

1. Connect yt-dlp progress hooks to normalized application events.
2. Stream job events with Server-Sent Events.
3. Report downloaded bytes, total bytes, percentage, speed, and estimated remaining time when available.
4. Handle indeterminate totals without inventing percentages.
5. Allow queued and active jobs to be cancelled.
6. Clean up partial files after cancellation.
7. Reconnect the frontend event stream safely.
8. Stop listening after completion, failure, or cancellation.

## Targeted Tests

```text
backend/tests/test_progress_broker.py
backend/tests/test_progress_stream.py
backend/tests/test_job_cancellation.py
frontend/src/features/download-progress/ProgressBar.test.tsx
frontend/src/features/download-progress/useDownloadProgress.test.tsx
```

## Completion Criteria

- Browser progress updates without polling.
- Cancellation transitions the job to `cancelled`.
- Temporary files are cleaned safely.
- Stream resources close after terminal job states.
- Targeted tests pass.

---

# Phase 6: FFmpeg Post-Processing and Output Delivery

## Primary Objective

Merge compatible media streams, support controlled output modes, verify completed files, and make completed local files available through safe API endpoints.

## Directories Exclusive to Phase 6

```text
frontend/src/features/completed-downloads/
```

## Files Exclusive to Phase 6

```text
backend/app/services/ffmpeg_service.py
backend/app/services/file_service.py
backend/app/schemas/file.py
backend/api-notes.md
backend/tests/test_ffmpeg_service.py
backend/tests/test_file_service.py
backend/tests/test_file_route.py
frontend/src/features/completed-downloads/CompletedDownload.tsx
frontend/src/features/completed-downloads/FileActions.tsx
frontend/src/features/completed-downloads/fileApi.ts
frontend/src/features/completed-downloads/CompletedDownload.test.tsx
```

## Existing Files Modified in Phase 6

```text
backend/app/api/routes/downloads.py
backend/app/services/download_service.py
backend/app/jobs/manager.py
backend/app/core/config.py
frontend/src/features/download-jobs/DownloadJobCard.tsx
```

## Specific Objectives

1. Merge selected video and audio streams with FFmpeg.
2. Support controlled output containers such as MP4, WebM, and M4A.
3. Add an optional audio-only mode using approved backend presets.
4. Verify output files with FFprobe.
5. Store completed files only in `storage/downloads/`.
6. Serve completed files by job identifier, never by arbitrary client-provided paths.
7. Use safe response filenames.
8. Report post-processing as a distinct job state.
9. Remove invalid output after a failed verification.

## Targeted Tests

```text
backend/tests/test_ffmpeg_service.py
backend/tests/test_file_service.py
backend/tests/test_file_route.py
frontend/src/features/completed-downloads/CompletedDownload.test.tsx
```

## Completion Criteria

- Separate streams are merged successfully when required.
- Completed files pass FFprobe verification.
- Files are delivered only through safe job-based endpoints.
- Failed processing returns a clear error and cleans invalid files.
- Targeted tests pass.

---

# Phase 7: SQLite Persistence and Download History

## Primary Objective

Persist job records and present a durable local download history across application restarts.

## Directories Exclusive to Phase 7

```text
backend/app/db/
backend/app/repositories/
frontend/src/features/history/
```

## Files Exclusive to Phase 7

```text
backend/app/db/__init__.py
backend/app/db/database.py
backend/app/db/models.py
backend/app/db/migrations.py
backend/app/repositories/__init__.py
backend/app/repositories/download_repository.py
backend/app/api/routes/history.py
backend/app/schemas/history.py
backend/tests/test_database.py
backend/tests/test_download_repository.py
backend/tests/test_history_route.py
frontend/src/features/history/DownloadHistory.tsx
frontend/src/features/history/HistoryItem.tsx
frontend/src/features/history/historyApi.ts
frontend/src/features/history/historyTypes.ts
frontend/src/features/history/DownloadHistory.test.tsx
```

## Existing Files Modified in Phase 7

```text
backend/app/api/router.py
backend/app/main.py
backend/app/core/config.py
backend/app/jobs/manager.py
frontend/src/App.tsx
```

## Generated Runtime Files

```text
storage/app.db
```

The database file is generated locally and must remain ignored by Git.

## Specific Objectives

1. Persist job metadata and terminal states in SQLite.
2. Restore historical jobs after backend restart.
3. Keep active in-memory execution state separate from persistent history.
4. Provide a paginated history endpoint.
5. Record created, started, completed, failed, and cancelled timestamps.
6. Display completed, failed, and cancelled jobs in the frontend.
7. Allow the user to remove a history record without unsafe arbitrary file deletion.
8. Reconcile missing files with historical records.

## Targeted Tests

```text
backend/tests/test_database.py
backend/tests/test_download_repository.py
backend/tests/test_history_route.py
frontend/src/features/history/DownloadHistory.test.tsx
```

## Completion Criteria

- Completed jobs remain visible after restart.
- History pagination works.
- Missing local files are represented correctly.
- Database failures produce controlled API errors.
- Targeted tests pass.

---

# Phase 8: Subtitles, Thumbnails, and Metadata Options

## Primary Objective

Add controlled optional media enhancements without exposing unrestricted yt-dlp or FFmpeg arguments.

## Directories Exclusive to Phase 8

```text
frontend/src/features/media-options/
```

## Files Exclusive to Phase 8

```text
backend/app/services/subtitle_service.py
backend/app/services/thumbnail_service.py
backend/app/schemas/options.py
backend/tests/test_subtitle_service.py
backend/tests/test_thumbnail_service.py
backend/tests/test_download_options.py
frontend/src/features/media-options/DownloadOptions.tsx
frontend/src/features/media-options/SubtitleSelector.tsx
frontend/src/features/media-options/MetadataOptions.tsx
frontend/src/features/media-options/DownloadOptions.test.tsx
```

## Existing Files Modified in Phase 8

```text
backend/app/schemas/media.py
backend/app/schemas/download.py
backend/app/services/download_service.py
backend/app/services/ffmpeg_service.py
frontend/src/features/media-inspection/MediaPreview.tsx
frontend/src/features/download-jobs/DownloadButton.tsx
```

## Specific Objectives

1. Display available subtitle languages from inspected metadata.
2. Allow approved subtitle selection.
3. Support subtitle download or embedding where technically compatible.
4. Support thumbnail download and optional embedding.
5. Support controlled title, artist, and source metadata embedding.
6. Store thumbnail artifacts in `storage/thumbnails/`.
7. Validate every option against server-supported presets.

## Targeted Tests

```text
backend/tests/test_subtitle_service.py
backend/tests/test_thumbnail_service.py
backend/tests/test_download_options.py
frontend/src/features/media-options/DownloadOptions.test.tsx
```

## Completion Criteria

- Available subtitle languages display correctly.
- Unsupported combinations are rejected before job execution.
- Thumbnail and metadata behavior is predictable per output container.
- Targeted tests pass.

---

# Phase 9: Security, Limits, and Operational Hardening

## Primary Objective

Harden the local application against unsafe input, uncontrolled resource use, path manipulation, network abuse, and stale generated files.

## Directories Exclusive to Phase 9

```text
backend/app/security/
backend/app/maintenance/
```

## Files Exclusive to Phase 9

```text
backend/app/security/__init__.py
backend/app/security/network_policy.py
backend/app/security/path_policy.py
backend/app/security/rate_limit.py
backend/app/maintenance/__init__.py
backend/app/maintenance/cleanup.py
backend/app/core/logging.py
backend/app/api/routes/system.py
backend/app/schemas/system.py
backend/tests/test_network_policy.py
backend/tests/test_path_policy.py
backend/tests/test_rate_limit.py
backend/tests/test_cleanup.py
backend/tests/test_disk_space.py
```

## Existing Files Modified in Phase 9

```text
backend/app/main.py
backend/app/core/config.py
backend/app/services/url_validator.py
backend/app/services/download_service.py
backend/app/services/file_service.py
backend/app/jobs/manager.py
backend/app/api/router.py
```

## Specific Objectives

1. Re-resolve hostnames immediately before outbound access to reduce DNS rebinding risk.
2. Reject loopback, link-local, multicast, reserved, and private network addresses.
3. Enforce maximum duration and estimated file-size limits.
4. Limit simultaneous inspection and download jobs.
5. Check disk space before and during download processing.
6. Apply safe timeouts.
7. Clean abandoned temporary files.
8. Expire old download files according to local policy.
9. Add structured application logging without exposing sensitive data.
10. Keep the application bound to `127.0.0.1` by default.
11. Add a system status endpoint for disk and queue visibility.

## Targeted Tests

```text
backend/tests/test_network_policy.py
backend/tests/test_path_policy.py
backend/tests/test_rate_limit.py
backend/tests/test_cleanup.py
backend/tests/test_disk_space.py
```

## Completion Criteria

- Unsafe network targets are rejected consistently.
- Output paths cannot escape approved storage directories.
- Resource limits are configurable and enforced.
- Cleanup removes only eligible generated files.
- Logs contain useful context without raw secrets or cookies.
- Targeted tests pass.

---

# Phase 10: User Experience, Accessibility, and Responsive Design

## Primary Objective

Turn the functional interface into a polished, understandable, keyboard-accessible, and responsive localhost application.

## Directories Exclusive to Phase 10

```text
frontend/src/components/layout/
frontend/src/components/feedback/
frontend/src/components/ui/
frontend/src/styles/
```

## Files Exclusive to Phase 10

```text
frontend/src/components/layout/AppHeader.tsx
frontend/src/components/layout/AppFooter.tsx
frontend/src/components/layout/AppShell.tsx
frontend/src/components/feedback/Alert.tsx
frontend/src/components/feedback/EmptyState.tsx
frontend/src/components/feedback/LoadingState.tsx
frontend/src/components/ui/Button.tsx
frontend/src/components/ui/Card.tsx
frontend/src/components/ui/Field.tsx
frontend/src/components/ui/Select.tsx
frontend/src/styles/theme.css
frontend/src/styles/utilities.css
frontend/src/components/ui/Button.test.tsx
frontend/src/components/feedback/Alert.test.tsx
```

## Existing Files Modified in Phase 10

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/index.css
frontend/index.html
frontend/public/favicon.svg
```

## Specific Objectives

1. Establish a consistent visual system.
2. Provide responsive layouts for mobile, tablet, and desktop widths.
3. Provide visible keyboard focus states.
4. Associate labels, descriptions, and errors with form controls.
5. Announce progress and terminal job states to assistive technologies.
6. Improve loading, empty, success, warning, and failure states.
7. Avoid ambiguous icon-only controls.
8. Provide a clear authorized-use notice.
9. Preserve functionality with reduced-motion preferences.
10. Replace the default Vite demonstration interface and assets.

## Targeted Tests

```text
frontend/src/components/ui/Button.test.tsx
frontend/src/components/feedback/Alert.test.tsx
```

Additional validation:

- Keyboard-only navigation
- Responsive browser inspection
- Accessibility audit
- Contrast inspection
- Screen-reader announcement inspection

## Completion Criteria

- All major workflows are usable by keyboard.
- Form errors are programmatically associated with inputs.
- Progress updates have accessible announcements.
- Layout works across common viewport widths.
- Default Vite demonstration content has been removed.
- Frontend tests, lint, and build pass.

---

# Phase 11: Full-System Testing and Regression Gate

## Primary Objective

Validate the complete application through backend integration tests, frontend component tests, and end-to-end browser workflows.

## Directories Exclusive to Phase 11

```text
e2e/
scripts/
```

## Files Exclusive to Phase 11

```text
e2e/playwright.config.ts
e2e/package.json
e2e/package-lock.json
e2e/tests/health.spec.ts
e2e/tests/inspection.spec.ts
e2e/tests/download-job.spec.ts
e2e/tests/cancellation.spec.ts
e2e/tests/history.spec.ts
scripts/check-backend.sh
scripts/check-frontend.sh
scripts/check-all.sh
scripts/run-development.sh
```

## Existing Files Modified in Phase 11

```text
README.md
.gitignore
backend/pytest.ini
frontend/package.json
```

## Specific Objectives

1. Run the complete backend test suite.
2. Run the complete frontend test suite.
3. Run backend and frontend lint checks.
4. Build the production frontend.
5. Add browser-level end-to-end tests.
6. Mock or use controlled authorized test fixtures for media extraction.
7. Validate inspection, job creation, progress, cancellation, completion, and history workflows.
8. Add repeatable development and verification scripts.
9. Confirm that no generated media, secrets, virtual environments, or build artifacts are tracked.

## Test Commands Expected at the Phase Gate

```text
Backend targeted tests
Backend full test suite
Backend Ruff check
Frontend targeted tests
Frontend full test suite
Frontend Oxlint check
Frontend TypeScript build
End-to-end Playwright tests
Git ignored-file verification
```

## Completion Criteria

- All automated test suites pass.
- Frontend production build succeeds.
- No known high-severity dependency issue remains unresolved.
- Core browser workflows pass.
- Test failures are reproducible and documented.
- Git status contains only intended source and documentation files.

---

# Phase 12: Documentation, Local Packaging, and Release Candidate

## Primary Objective

Prepare a reproducible, documented localhost release candidate without prematurely introducing cloud deployment complexity.

## Directories Exclusive to Phase 12

```text
docs/
```

## Files Exclusive to Phase 12

```text
README.md
LICENSE
CHANGELOG.md
CONTRIBUTING.md
docs/architecture.md
docs/api.md
docs/development.md
docs/security.md
docs/troubleshooting.md
docs/authorized-use.md
backend/.env.example
frontend/.env.example
```

## Existing Files Modified in Phase 12

```text
backend/requirements-lock.txt
frontend/package-lock.json
.gitignore
scripts/run-development.sh
```

## Specific Objectives

1. Document installation on Kali Debian.
2. Document exact backend and frontend startup commands.
3. Document environment variables and safe defaults.
4. Document API endpoints and response schemas.
5. Explain project architecture and storage layout.
6. Document authorized-use boundaries.
7. Document common failures involving yt-dlp, FFmpeg, ports, Node.js, and disk space.
8. Add a changelog and release checklist.
9. Verify locked dependency snapshots.
10. Create the first release candidate tag only after all phase gates pass.

## Completion Criteria

- A new developer can set up the project from the README.
- Both services start on localhost using documented commands.
- Configuration examples contain no real secrets.
- Troubleshooting steps cover known setup issues.
- Full regression checks pass from a clean installation.
- Release candidate documentation is complete.

---

# Optional Phase 13: Single-Process Local Distribution

## Primary Objective

Optionally package the compiled frontend with the FastAPI backend for a simpler one-command local experience.

This phase is optional and must begin only after the development architecture is stable.

## Directories Exclusive to Phase 13

```text
backend/app/static/
packaging/
```

## Files Exclusive to Phase 13

```text
backend/app/static/.gitkeep
backend/app/core/static_files.py
packaging/build-local.sh
packaging/run-local.sh
packaging/README.md
```

## Existing Files Modified in Phase 13

```text
backend/app/main.py
frontend/vite.config.ts
.gitignore
README.md
```

## Specific Objectives

1. Build the React application into static assets.
2. Copy release assets into a backend-served static directory.
3. Serve the single-page application from FastAPI.
4. Preserve `/api/v1` routes and API documentation.
5. Keep development mode using separate hot-reload servers.
6. Provide a one-command localhost release startup script.

## Completion Criteria

- One local backend process serves both the UI and API.
- Browser refresh works on client routes.
- Development mode remains unchanged.
- Full regression tests pass against the packaged layout.

---

# Phase Dependency Sequence

```text
Phase 1: Backend Foundation
    ↓
Phase 2: Frontend Toolchain and API Connectivity
    ↓
Phase 3: URL Validation and Metadata Inspection
    ↓
Phase 4: Download Job Creation and Format Selection
    ↓
Phase 5: Real-Time Progress and Cancellation
    ↓
Phase 6: FFmpeg Post-Processing and Output Delivery
    ↓
Phase 7: SQLite Persistence and Download History
    ↓
Phase 8: Subtitles, Thumbnails, and Metadata Options
    ↓
Phase 9: Security, Limits, and Operational Hardening
    ↓
Phase 10: User Experience and Accessibility
    ↓
Phase 11: Full-System Testing and Regression Gate
    ↓
Phase 12: Documentation and Release Candidate
    ↓
Phase 13: Optional Single-Process Distribution
```

---

# Full Planned Project Structure

The following is the cumulative structure after all mandatory phases. Each file belongs to the phase where it was first introduced.

```text
youtube-web-downloader/
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── backend/
│   ├── .env.example
│   ├── api-notes.md
│   ├── pytest.ini
│   ├── requirements-lock.txt
│   ├── ruff.toml
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── downloads.py
│   │   │       ├── health.py
│   │   │       ├── history.py
│   │   │       ├── media.py
│   │   │       └── system.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── migrations.py
│   │   │   └── models.py
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   └── broker.py
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   └── media.py
│   │   ├── jobs/
│   │   │   ├── __init__.py
│   │   │   ├── manager.py
│   │   │   └── models.py
│   │   ├── maintenance/
│   │   │   ├── __init__.py
│   │   │   └── cleanup.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── download_repository.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── download.py
│   │   │   ├── file.py
│   │   │   ├── health.py
│   │   │   ├── history.py
│   │   │   ├── media.py
│   │   │   ├── options.py
│   │   │   ├── progress.py
│   │   │   └── system.py
│   │   ├── security/
│   │   │   ├── __init__.py
│   │   │   ├── network_policy.py
│   │   │   ├── path_policy.py
│   │   │   └── rate_limit.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── download_service.py
│   │       ├── ffmpeg_service.py
│   │       ├── file_service.py
│   │       ├── filename_service.py
│   │       ├── media_inspector.py
│   │       ├── subtitle_service.py
│   │       ├── thumbnail_service.py
│   │       └── url_validator.py
│   └── tests/
│       ├── __init__.py
│       ├── test_cleanup.py
│       ├── test_database.py
│       ├── test_disk_space.py
│       ├── test_download_options.py
│       ├── test_download_repository.py
│       ├── test_download_route.py
│       ├── test_ffmpeg_service.py
│       ├── test_file_route.py
│       ├── test_file_service.py
│       ├── test_filename_service.py
│       ├── test_health.py
│       ├── test_history_route.py
│       ├── test_job_cancellation.py
│       ├── test_job_manager.py
│       ├── test_media_inspector.py
│       ├── test_media_route.py
│       ├── test_network_policy.py
│       ├── test_path_policy.py
│       ├── test_progress_broker.py
│       ├── test_progress_stream.py
│       ├── test_rate_limit.py
│       ├── test_subtitle_service.py
│       ├── test_thumbnail_service.py
│       └── test_url_validator.py
├── docs/
│   ├── api.md
│   ├── architecture.md
│   ├── authorized-use.md
│   ├── development.md
│   ├── security.md
│   └── troubleshooting.md
├── e2e/
│   ├── package.json
│   ├── package-lock.json
│   ├── playwright.config.ts
│   └── tests/
│       ├── cancellation.spec.ts
│       ├── download-job.spec.ts
│       ├── health.spec.ts
│       ├── history.spec.ts
│       └── inspection.spec.ts
├── frontend/
│   ├── .env.example
│   ├── .gitignore
│   ├── .nvmrc
│   ├── .oxlintrc.json
│   ├── README.md
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── vitest.config.ts
│   ├── public/
│   │   ├── favicon.svg
│   │   └── icons.svg
│   └── src/
│       ├── App.css
│       ├── App.tsx
│       ├── index.css
│       ├── main.tsx
│       ├── components/
│       │   ├── ApiStatus.test.tsx
│       │   ├── ApiStatus.tsx
│       │   ├── feedback/
│       │   │   ├── Alert.test.tsx
│       │   │   ├── Alert.tsx
│       │   │   ├── EmptyState.tsx
│       │   │   └── LoadingState.tsx
│       │   ├── layout/
│       │   │   ├── AppFooter.tsx
│       │   │   ├── AppHeader.tsx
│       │   │   └── AppShell.tsx
│       │   └── ui/
│       │       ├── Button.test.tsx
│       │       ├── Button.tsx
│       │       ├── Card.tsx
│       │       ├── Field.tsx
│       │       └── Select.tsx
│       ├── features/
│       │   ├── completed-downloads/
│       │   │   ├── CompletedDownload.test.tsx
│       │   │   ├── CompletedDownload.tsx
│       │   │   ├── FileActions.tsx
│       │   │   └── fileApi.ts
│       │   ├── download-jobs/
│       │   │   ├── DownloadButton.test.tsx
│       │   │   ├── DownloadButton.tsx
│       │   │   ├── DownloadJobCard.tsx
│       │   │   ├── FormatSelector.test.tsx
│       │   │   ├── FormatSelector.tsx
│       │   │   ├── downloadApi.ts
│       │   │   └── downloadTypes.ts
│       │   ├── download-progress/
│       │   │   ├── CancelDownloadButton.tsx
│       │   │   ├── ProgressBar.test.tsx
│       │   │   ├── ProgressBar.tsx
│       │   │   ├── ProgressDetails.tsx
│       │   │   ├── useDownloadProgress.test.tsx
│       │   │   └── useDownloadProgress.ts
│       │   ├── history/
│       │   │   ├── DownloadHistory.test.tsx
│       │   │   ├── DownloadHistory.tsx
│       │   │   ├── HistoryItem.tsx
│       │   │   ├── historyApi.ts
│       │   │   └── historyTypes.ts
│       │   ├── media-inspection/
│       │   │   ├── FormatList.tsx
│       │   │   ├── MediaPreview.test.tsx
│       │   │   ├── MediaPreview.tsx
│       │   │   ├── UrlForm.test.tsx
│       │   │   ├── UrlForm.tsx
│       │   │   ├── mediaApi.ts
│       │   │   └── mediaTypes.ts
│       │   └── media-options/
│       │       ├── DownloadOptions.test.tsx
│       │       ├── DownloadOptions.tsx
│       │       ├── MetadataOptions.tsx
│       │       └── SubtitleSelector.tsx
│       ├── lib/
│       │   └── api.ts
│       ├── styles/
│       │   ├── theme.css
│       │   └── utilities.css
│       ├── test/
│       │   └── setup.ts
│       └── types/
│           └── api.ts
├── scripts/
│   ├── check-all.sh
│   ├── check-backend.sh
│   ├── check-frontend.sh
│   └── run-development.sh
└── storage/
    ├── downloads/
    │   └── .gitkeep
    ├── thumbnails/
    │   └── .gitkeep
    └── tmp/
        └── .gitkeep
```

---

# Milestone Summary

## Milestone 1: Foundation Ready

Includes Phases 1 and 2.

Result:

- Backend health API works.
- Frontend toolchain is compatible.
- Frontend communicates with the backend.

## Milestone 2: Inspection Ready

Includes Phase 3.

Result:

- A permitted media URL can be inspected safely.
- Metadata and normalized formats appear in the browser.

## Milestone 3: Download Ready

Includes Phases 4, 5, and 6.

Result:

- A format can be selected.
- A controlled download job can run.
- Real-time progress appears.
- The completed file is verified and delivered safely.

## Milestone 4: Local Product Ready

Includes Phases 7 and 8.

Result:

- History persists across restarts.
- Optional subtitles, thumbnails, and metadata are supported.

## Milestone 5: Release Candidate Ready

Includes Phases 9, 10, 11, and 12.

Result:

- Security and resource limits are enforced.
- The interface is accessible and responsive.
- Full regression testing passes.
- Documentation supports a clean local installation.

---

# Phase Execution Rule

At the end of every phase:

1. Run the phase-specific targeted tests.
2. Run the relevant lint check.
3. Inspect the exact resulting directory structure.
4. Inspect `git status`.
5. Record completed objectives and unresolved issues.
6. Stop at the phase gate.
7. Begin the next phase only after reviewing the previous phase results.

No future-phase directory or file should be created early unless an earlier phase has a verified technical dependency on it.
