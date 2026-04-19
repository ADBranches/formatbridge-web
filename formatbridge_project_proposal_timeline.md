# FormatBridge Project Proposal, Repository Structure, and Phased Build Timeline

## Project Title
**FormatBridge: A Web-Based Multi-Format File Conversion Platform**

## Proposed Repository Name
`formatbridge-web`

## Preferred Core Stack
### Frontend
- React
- Vite
- Tailwind CSS
- React Router
- React Dropzone
- TanStack Query

### Backend
- Flask
- Celery
- Redis

### File Processing
- Pillow
- pillow-heif
- img2pdf
- PyMuPDF
- python-docx
- Tesseract OCR

### Data and Storage
- PostgreSQL
- Local temporary file storage for MVP
- ZIP packaging for batch downloads

### Deployment
- Nginx
- Gunicorn
- Docker
- Linux VPS / cloud VM

---

# 1. Executive Summary
FormatBridge is a browser-based file conversion platform that allows users to upload images and supported documents, convert them into other output formats, and download the results individually or in batch. The system will prioritize common real-world needs such as:

- HEIC to JPG or PNG
- JPG/PNG/WEBP to PDF
- image files to DOCX
- multiple files to ZIP download
- optional OCR workflows for scanned content

The platform will target users who want fast, simple, and reliable conversion without installing desktop software.

---

# 2. Problem Statement
Users frequently face compatibility issues when sharing or printing files created on phones, browsers, office software, or design tools. Common issues include:

- HEIC images not opening well on some systems
- WEBP images needing JPG or PNG versions
- multiple images needing to become one PDF
- scanned images needing Word export
- lack of one tool that supports both conversion and batch downloading

Many available tools are limited, confusing, watermark outputs, or fail on modern formats.

---

# 3. Proposed Solution
Develop a full-stack web application with a React + Tailwind CSS frontend and a Flask + Celery + Redis backend that supports:

- multi-file upload
- format detection
- conversion job queueing
- output download
- batch ZIP packaging
- optional OCR for scanned documents
- job history for users or active sessions

---

# 4. General Objective
To build a secure and user-friendly web application for converting multiple image and document-related file formats into other useful output formats.

---

# 5. Specific Objectives
- support modern image inputs such as HEIC and WEBP
- support standard outputs such as JPG, PNG, PDF, and DOCX
- support single and multiple file uploads
- preserve quality where possible
- support batch conversion and ZIP download
- allow future OCR-based editable document export
- provide a responsive mobile-friendly interface

---

# 6. Scope

## 6.1 MVP Scope
The first usable release should support:

- HEIC -> JPG
- HEIC -> PNG
- JPG/JPEG/PNG/WEBP -> PDF
- JPG/JPEG/PNG/WEBP -> DOCX (image embedded in document)
- multiple file upload
- batch download as ZIP
- conversion status display
- temporary file cleanup

## 6.2 Phase 2 Scope
After MVP, add:

- OCR image -> editable DOCX
- GIF frame handling rules
- PDF preview thumbnails
- user accounts
- saved conversion history
- conversion quotas
- admin dashboard

## 6.3 Non-Goals for MVP
Do not start with these:

- full video conversion
- advanced collaborative workspaces
- permanent unlimited file storage
- complex billing system
- AI document enhancement

---

# 7. Key Functional Requirements
- user uploads one or multiple files
- system validates file type and size
- user selects target format
- system creates conversion job
- job is processed asynchronously
- user sees job progress
- user downloads result
- multiple outputs can be packaged into ZIP
- temporary files are removed after expiry

---

# 8. Non-Functional Requirements
- secure file validation
- responsive UI
- reliable queue processing
- reasonable performance for medium-sized files
- clean API structure
- modular conversion service design
- easy future extension for new formats

---

# 9. Proposed Architecture

## 9.1 Frontend Responsibilities
- drag-and-drop upload UI
- file preview cards
- format selector
- conversion job submission
- status polling
- download pages
- error reporting
- responsive experience

## 9.2 Backend Responsibilities
- file upload endpoints
- file validation
- job creation
- dispatching tasks to Celery
- conversion orchestration
- result storage metadata
- download endpoints
- ZIP packaging
- cleanup jobs

## 9.3 Worker Responsibilities
- perform file conversion
- call correct conversion library by input/output format
- generate output files
- update job state
- handle failed jobs safely

## 9.4 Database Responsibilities
- store job metadata
- store user references later
- store file records
- store conversion request and result status
- store timestamps and cleanup state

---

# 10. Recommended Repository Structure

```text
formatbridge-web/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── assets/
│       ├── components/
│       │   ├── common/
│       │   ├── upload/
│       │   ├── conversion/
│       │   ├── jobs/
│       │   └── layout/
│       ├── pages/
│       │   ├── HomePage.jsx
│       │   ├── ConvertPage.jsx
│       │   ├── ResultsPage.jsx
│       │   ├── NotFoundPage.jsx
│       │   └── HistoryPage.jsx
│       ├── routes/
│       │   └── index.jsx
│       ├── hooks/
│       ├── lib/
│       ├── services/
│       │   ├── apiClient.js
│       │   ├── uploadService.js
│       │   └── jobService.js
│       ├── store/
│       ├── utils/
│       └── styles/
├── backend/
│   ├── requirements.txt
│   ├── run.py
│   ├── wsgi.py
│   ├── celery_worker.py
│   ├── migrations/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── conversion_job.py
│   │   │   ├── file_asset.py
│   │   │   ├── conversion_result.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── upload_schema.py
│   │   │   ├── conversion_schema.py
│   │   │   └── result_schema.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── uploads.py
│   │   │       ├── conversions.py
│   │   │       ├── jobs.py
│   │   │       ├── downloads.py
│   │   │       └── health.py
│   │   ├── services/
│   │   │   ├── file_service.py
│   │   │   ├── conversion_router_service.py
│   │   │   ├── image_conversion_service.py
│   │   │   ├── pdf_service.py
│   │   │   ├── docx_service.py
│   │   │   ├── ocr_service.py
│   │   │   ├── zip_service.py
│   │   │   └── cleanup_service.py
│   │   ├── tasks/
│   │   │   ├── conversion_tasks.py
│   │   │   └── cleanup_tasks.py
│   │   ├── utils/
│   │   │   ├── file_types.py
│   │   │   ├── validators.py
│   │   │   ├── naming.py
│   │   │   └── response.py
│   │   └── temp_storage/
│   └── tests/
│       ├── test_health.py
│       ├── test_uploads.py
│       ├── test_conversions.py
│       ├── test_jobs.py
│       └── test_downloads.py
└── docs/
    ├── proposal.md
    ├── architecture.md
    ├── api_contract.md
    ├── database_schema.md
    ├── deployment_guide.md
    └── testing_checklist.md
```

---

# 11. Suggested Database Design

## 11.1 conversion_jobs
- id
- public_id
- user_id nullable
- requested_output_format
- source_count
- status
- error_message nullable
- created_at
- updated_at
- completed_at nullable

## 11.2 file_assets
- id
- job_id
- original_filename
- stored_filename
- mime_type
- input_format
- size_bytes
- storage_path
- created_at

## 11.3 conversion_results
- id
- job_id
- source_file_id
- output_format
- output_filename
- output_path
- size_bytes
- is_zip_bundle
- created_at

## 11.4 users later
- id
- full_name
- email
- password_hash
- is_active
- created_at

---

# 12. API Design Overview

## Public API Endpoints
### Health
- `GET /api/v1/health`

### Uploads
- `POST /api/v1/uploads`

### Conversion
- `POST /api/v1/conversions`

### Jobs
- `GET /api/v1/jobs/<job_id>`
- `GET /api/v1/jobs/<job_id>/results`

### Downloads
- `GET /api/v1/downloads/<result_id>`
- `GET /api/v1/downloads/jobs/<job_id>/zip`

---

# 13. Conversion Rules for MVP

## Supported Input -> Output
### HEIC
- HEIC -> JPG
- HEIC -> PNG
- HEIC -> PDF
- HEIC -> DOCX

### JPG/JPEG/PNG/WEBP
- image -> JPG
- image -> PNG
- image -> WEBP
- image -> PDF
- image -> DOCX

## DOCX Rule
For MVP:
- image -> DOCX means image embedded in a Word document

For later:
- scanned image -> OCR text -> editable DOCX

## GIF Rule
For MVP:
- accept static GIF carefully
- postpone animated GIF conversion rules until Phase 2

---

# 14. Phased Build Timeline

## Phase 1 — Product Foundation and Environment Setup
### Objective
Establish the repository, local environments, tooling, and basic frontend/backend scaffolding.

### Files and Directories to Populate
- `README.md`
- `.env.example`
- `docker-compose.yml`
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/tailwind.config.js`
- `frontend/src/main.jsx`
- `frontend/src/App.jsx`
- `frontend/src/routes/index.jsx`
- `backend/requirements.txt`
- `backend/run.py`
- `backend/wsgi.py`
- `backend/app/__init__.py`
- `backend/app/config.py`
- `backend/app/extensions.py`
- `backend/app/database.py`
- `backend/celery_worker.py`

### Deliverables
- React app boots successfully
- Flask app boots successfully
- Redis container or service runs
- Celery worker starts
- PostgreSQL connection works

### Completion Check
- frontend loads in browser
- backend health endpoint returns 200
- Celery worker connects to Redis
- database migrations can run

---

## Phase 2 — Upload Pipeline and File Validation
### Objective
Build secure file upload and server-side validation.

### Files and Directories to Populate
- `frontend/src/components/upload/UploadDropzone.jsx`
- `frontend/src/components/upload/FileCard.jsx`
- `frontend/src/pages/ConvertPage.jsx`
- `frontend/src/services/uploadService.js`
- `frontend/src/services/apiClient.js`
- `frontend/src/utils/fileHelpers.js`
- `backend/app/api/v1/uploads.py`
- `backend/app/schemas/upload_schema.py`
- `backend/app/services/file_service.py`
- `backend/app/utils/file_types.py`
- `backend/app/utils/validators.py`
- `backend/app/models/file_asset.py`

### Deliverables
- drag-and-drop upload UI
- multiple file upload
- file size validation
- MIME/type validation
- temporary file persistence

### Completion Check
- valid files upload successfully
- invalid files are rejected cleanly
- uploaded records are written to DB

---

## Phase 3 — Conversion Job Model and Queue Integration
### Objective
Add asynchronous job creation and progress tracking.

### Files and Directories to Populate
- `backend/app/models/conversion_job.py`
- `backend/app/models/conversion_result.py`
- `backend/app/api/v1/conversions.py`
- `backend/app/api/v1/jobs.py`
- `backend/app/schemas/conversion_schema.py`
- `backend/app/schemas/result_schema.py`
- `backend/app/tasks/conversion_tasks.py`
- `backend/app/services/conversion_router_service.py`
- `frontend/src/components/jobs/JobStatusCard.jsx`
- `frontend/src/hooks/useJobPolling.js`
- `frontend/src/services/jobService.js`

### Deliverables
- conversion request endpoint
- Celery task creation
- job status updates
- polling UI

### Completion Check
- conversion request creates a job
- worker receives task
- UI reflects queued, processing, success, failed

---

## Phase 4 — Core Image Conversion Engine
### Objective
Implement actual image-to-image conversion workflows.

### Files and Directories to Populate
- `backend/app/services/image_conversion_service.py`
- `backend/app/services/conversion_router_service.py`
- `backend/app/utils/naming.py`
- `backend/tests/test_conversions.py`

### MVP Conversions to Support
- HEIC -> JPG
- HEIC -> PNG
- JPG/JPEG/PNG/WEBP -> JPG
- JPG/JPEG/PNG/WEBP -> PNG
- JPG/JPEG/PNG/WEBP -> WEBP

### Deliverables
- conversion logic via Pillow and pillow-heif
- output file generation
- result records written

### Completion Check
- each supported conversion returns valid downloadable output
- converted files open correctly

---

## Phase 5 — PDF Generation and Multi-Image PDF Merge
### Objective
Support image-to-PDF and multi-image PDF export.

### Files and Directories to Populate
- `backend/app/services/pdf_service.py`
- `backend/app/tasks/conversion_tasks.py`
- `frontend/src/components/conversion/FormatSelector.jsx`
- `frontend/src/components/conversion/ConversionSummary.jsx`
- `backend/tests/test_downloads.py`

### Deliverables
- single image to PDF
- multiple images merged into one PDF
- download endpoint for PDF results

### Completion Check
- generated PDFs open correctly
- multiple images preserve order
- merged PDF is downloadable

---

## Phase 6 — DOCX Export
### Objective
Support image-to-DOCX export for MVP.

### Files and Directories to Populate
- `backend/app/services/docx_service.py`
- `backend/app/tasks/conversion_tasks.py`
- `backend/tests/test_conversions.py`

### Deliverables
- image embedded in DOCX
- optional title/spacing rules
- downloadable DOCX output

### Completion Check
- DOCX opens in Word/LibreOffice
- embedded images render correctly

---

## Phase 7 — Batch Results and ZIP Packaging
### Objective
Allow multiple outputs to be downloaded in a bundled archive.

### Files and Directories to Populate
- `backend/app/services/zip_service.py`
- `backend/app/api/v1/downloads.py`
- `frontend/src/pages/ResultsPage.jsx`
- `frontend/src/components/jobs/ResultList.jsx`
- `backend/tests/test_jobs.py`

### Deliverables
- ZIP packaging for all outputs of a job
- single result download links
- results summary screen

### Completion Check
- ZIP downloads successfully
- extracted files are valid
- result links match the correct files

---

## Phase 8 — Cleanup, Error Handling, and Hardening
### Objective
Make the system safer and production-ready for MVP release.

### Files and Directories to Populate
- `backend/app/services/cleanup_service.py`
- `backend/app/tasks/cleanup_tasks.py`
- `backend/app/utils/response.py`
- `backend/tests/test_uploads.py`
- `backend/tests/test_health.py`
- `docs/testing_checklist.md`
- `docs/deployment_guide.md`

### Deliverables
- expired temp file cleanup
- better error responses
- logging
- rate-limiting plan
- environment configuration cleanup

### Completion Check
- stale files are deleted
- large invalid jobs fail safely
- errors are consistent and user-readable

---

## Phase 9 — OCR and Editable DOCX Enhancement
### Objective
Add OCR workflows for scanned image text extraction.

### Files and Directories to Populate
- `backend/app/services/ocr_service.py`
- `backend/app/tasks/conversion_tasks.py`
- `frontend/src/components/conversion/OcrOptionToggle.jsx`
- `backend/tests/test_conversions.py`

### Deliverables
- OCR preprocessing
- text extraction
- editable DOCX generation path

### Completion Check
- scanned text is extracted into DOCX
- OCR option is optional and clearly labeled

---

## Phase 10 — User Accounts and Conversion History
### Objective
Add account-based history and future monetization readiness.

### Files and Directories to Populate
- `backend/app/models/user.py`
- `backend/app/api/v1/auth.py`
- `frontend/src/pages/HistoryPage.jsx`
- `frontend/src/store/authStore.js`
- `frontend/src/components/common/ProtectedRoute.jsx`

### Deliverables
- sign up / login
- job history view
- user-linked conversions

### Completion Check
- authenticated users see their past jobs
- anonymous workflows still work if allowed

---

# 15. Timeline Recommendation

## Short Build Plan
### Week 1
- Phase 1
- Phase 2

### Week 2
- Phase 3
- Phase 4

### Week 3
- Phase 5
- Phase 6

### Week 4
- Phase 7
- Phase 8

### Later Enhancements
- Phase 9
- Phase 10

---

# 16. Testing Strategy

## Frontend Testing
- upload UI rendering
- format selector behavior
- polling behavior
- results rendering
- error state rendering

## Backend Testing
- upload endpoint tests
- conversion job creation tests
- conversion service unit tests
- PDF generation tests
- DOCX generation tests
- ZIP packaging tests
- cleanup task tests

## Manual Validation Checklist
- upload HEIC and convert to JPG
- upload PNG and convert to PDF
- upload multiple files and download ZIP
- convert image to DOCX
- fail unsupported file safely
- confirm temp files clean up

---

# 17. Deployment Plan

## MVP Deployment Stack
- React frontend served by Nginx
- Flask API served by Gunicorn
- Celery worker process
- Redis instance
- PostgreSQL database
- Docker Compose for first deployment

## Basic Production Services
- `nginx`
- `frontend`
- `backend`
- `celery_worker`
- `redis`
- `postgres`

---

# 18. Risks and Mitigation

## Risk
HEIC libraries may behave differently across environments  
## Mitigation
Use Docker and pin package versions

## Risk
Large uploads may overload the server  
## Mitigation
Set upload limits and queue heavy jobs

## Risk
Animated GIF support may complicate MVP  
## Mitigation
Defer full animated GIF support to Phase 2

## Risk
OCR may be inaccurate on low-quality images  
## Mitigation
Keep OCR optional and label results clearly

## Risk
Temporary files may accumulate  
## Mitigation
Add scheduled cleanup tasks early

---

# 19. Success Metrics
The MVP can be considered successful if it can:

- convert HEIC to JPG and PNG reliably
- generate PDF from one or more images
- generate DOCX with embedded images
- process queued jobs through Celery
- return downloadable outputs and ZIP bundles
- handle failed jobs gracefully
- clean temporary files automatically

---

# 20. Final Recommended Build Order
Build in this order:

1. foundation and environment
2. uploads and validation
3. job queue and status flow
4. image conversion engine
5. PDF generation
6. DOCX generation
7. ZIP packaging
8. cleanup and hardening
9. OCR
10. user history

---

# 21. Conclusion
FormatBridge is a realistic and valuable web product idea with clear practical demand. Your preferred backend stack of **Flask + Celery + Redis** is a strong fit, especially when paired with **React + Tailwind CSS** on the frontend. This structure gives you a simple MVP path first, while still leaving room for future OCR, accounts, and scalable production deployment.

The best immediate target is to build a clean MVP focused on:
- HEIC conversion
- image to PDF
- image to DOCX
- multi-file ZIP download

That MVP alone would already be useful, demonstrable, and expandable.
