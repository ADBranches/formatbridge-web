# FormatBridge Testing Checklist

## Phase 1
- [ ] Frontend loads on `http://127.0.0.1:5173`
- [ ] Backend health endpoint responds
- [ ] PostgreSQL container is running
- [ ] Redis container is running
- [ ] Celery worker starts successfully

## Phase 2
- [ ] Valid uploads succeed
- [ ] Invalid file types are rejected
- [ ] Too many files are rejected
- [ ] Oversized uploads fail safely
- [ ] Uploaded file rows are written to `file_assets`

## Phase 3
- [ ] Conversion request creates a job
- [ ] Worker receives queued job
- [ ] Job transitions from queued to processing to success / failed
- [ ] UI polling reflects job state

## Phase 4
- [ ] HEIC -> JPG works
- [ ] HEIC -> PNG works
- [ ] JPG / JPEG / PNG / WEBP -> JPG works
- [ ] JPG / JPEG / PNG / WEBP -> PNG works
- [ ] JPG / JPEG / PNG / WEBP -> WEBP works
- [ ] Result rows are written to `conversion_results`

## Phase 5
- [ ] Single image -> PDF works
- [ ] Multi-image merged PDF works
- [ ] Page order is preserved
- [ ] PDF download endpoint works

## Phase 6
- [ ] Single image -> DOCX works
- [ ] Multi-image -> DOCX works
- [ ] Embedded images render in Word / LibreOffice
- [ ] DOCX download endpoint works

## Phase 7
- [ ] ZIP packaging works
- [ ] ZIP download endpoint works
- [ ] Extracted files are valid
- [ ] Result list shows correct individual links

## Phase 8
- [ ] Stale uploads are deleted
- [ ] Stale converted outputs are deleted
- [ ] Stale ZIP archives are deleted
- [ ] Oversized / invalid jobs fail safely
- [ ] Error responses are consistent and user-readable
- [ ] Health response is consistent
