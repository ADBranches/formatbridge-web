# Admin CMS Media Edit & Video Support – Execution Timeline

This document defines the **clear execution phases**, objectives, and **exact backend & frontend files/directories** to be modified for implementing an **editable admin media CMS with video support**, based strictly on the current project structure.

---

## Phase 1 — System Audit & Flow Mapping

### Objective
Understand the **current media upload, storage, and rendering flow** across Flask backend and React frontend. Identify how images are stored, linked, and displayed.

### Backend Targets
- `app/api_flask/media.py`
- `app/api_flask/uploads.py`
- `app/models/media.py`
- `app/schemas/media.py`
- `app/config.py`
- `app/main.py`
- `passenger_wsgi.py`

### Frontend Targets
- `src/pages/admin/AdminGallery.jsx`
- `src/components/GallerySection.jsx`
- `src/components/ui/ImageUploadField.jsx`
- `src/lib/mediaApi.js`
- `src/lib/mediaResolver.js`
- `src/lib/galleryStore.js`

### Output
✅ Confirmed current upload paths, APIs, and gallery rendering flow

---

## Phase 2 — Define Editable Media Rules

### Objective
Formally define **what admins can edit** on uploaded media and confirm a **single unified media model** for images and videos.

### Key Decisions
- Single `media` table for images + videos
- Editable fields:
  - title
  - caption
  - alt_text
  - visibility (`is_active`)
  - sort_order
  - file replacement

### Backend Targets
- `app/models/media.py`
- `app/schemas/media.py`

### Output
✅ Final media edit rules & schema agreement

---

## Phase 3 — Backend Media Update & Replace APIs

### Objective
Enable admins to **update metadata, replace files, delete media, and list media** via secured APIs.

### Backend Targets
- `app/api_flask/media.py`
- `app/api_flask/uploads.py`
- `app/services/` (media-related helpers if added)
- `app/middlewares/auth_middleware.py`

### Output
✅ Admin-only media edit / replace / delete endpoints

---

## Phase 4 — Video Upload Support (Backend)

### Objective
Extend upload handling to support **video formats** alongside images.

### Add Support For
- `.mp4`
- `.webm`
- `.mov`

### Backend Targets
- `app/api_flask/uploads.py`
- `app/api_flask/media.py`
- `app/config.py`
- `app/utils/logger.py`

### Output
✅ Secure mixed-media uploader (image + video)

---

## Phase 5 — Database Model Adjustments & Migration

### Objective
Extend the `media` model to support **richer metadata** required for editing and videos.

### Fields Added / Confirmed
- `media_type` (image | video)
- `mime_type`
- `file_size`
- `caption`
- `alt_text`
- `sort_order`
- `is_active`

### Backend Targets
- `app/models/media.py`
- `migrations/`
- `alembic.ini`

### Output
✅ Database supports editable mixed media

---

## Phase 6 — Admin Upload UI (Images + Videos)

### Objective
Allow admins to **upload and preview images and videos** when adding gallery items.

### Frontend Targets
- `src/pages/admin/AdminGallery.jsx`
- `src/components/ui/ImageUploadField.jsx`
- `src/lib/mediaApi.js`

### UI Behavior
- `<img>` previews for images
- `<video controls>` previews for videos

### Output
✅ Mixed-media upload UI

---

## Phase 7 — Admin Edit Existing Media UI

### Objective
Enable admins to **edit existing uploaded media at any time**.

### Features
- Edit metadata
- Replace file without deleting record
- Toggle visibility

### Frontend Targets
- `src/pages/admin/AdminGallery.jsx`
- `src/components/ui/Modal.jsx`
- *(optional new)* `src/components/admin/MediaEditModal.jsx`

### Output
✅ Full admin media editing capability

---

## Phase 8 — Public Gallery Rendering (Mixed Media)

### Objective
Render images and videos correctly on public pages without breaking existing layouts.

### Frontend Targets
- `src/components/GallerySection.jsx`
- `src/lib/mediaResolver.js`
- `src/lib/galleryStore.js`

### Output
✅ Public gallery supports image + video

---

## Phase 9 — Validation, Security & File Cleanup

### Objective
Ensure upload and edit operations are **secure, safe, and clean**.

### Controls
- MIME + extension validation
- File size limits
- Admin-only authorization
- Delete old files on replacement

### Backend Targets
- `app/api_flask/uploads.py`
- `app/middlewares/auth_middleware.py`
- `app/config.py`
- `app/utils/logger.py`

### Output
✅ Secure and reliable media handling

---

## Phase 10 — Testing & Regression

### Objective
Verify all new functionality works and existing features are not broken.

### Backend Tests
- `tests/api/test_admin_cms_api.py`
- *(new)* `tests/api/test_media_upload_edit.py`

### Frontend Tests
- `src/__tests__/ServicesAdmin.test.jsx`
- `src/__tests__/ProjectsAdmin.test.jsx`
- *(new)* `AdminGallery.test.jsx`

### Output
✅ Tested, stable implementation

---

## Phase 11 — Deployment & Verification

### Objective
Safely deploy changes and confirm media serving works in production.

### Tasks
- Run Alembic migrations
- Verify WSGI static serving
- Confirm video streaming

### Deployment Targets
- `passenger_wsgi.py`
- `app/static/uploads/`
- `app/main.py`

### Output
✅ Feature live and production-ready

---

## Final Outcome

✅ Admins can edit uploaded content anytime
✅ Gallery supports images + videos
✅ Secure, tested, maintainable CMS media system
