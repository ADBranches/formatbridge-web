# Admin CMS Customization Timeline

**Project:** Construction Company CMS customization  
**Target area:** Existing Flask WSGI backend + React/Vite frontend  
**Main objective:** Allow admins to edit previously uploaded content at any time, and extend gallery/media uploads to support videos in multiple formats alongside current image formats.

> **Note:** This plan is based on the current folder structure shared in chat. FastAPI traces are intentionally ignored. Some exact file edits must be confirmed after reviewing the actual contents of the media/gallery/admin upload files.

---

## Timeline Chart

| Phase | Unit Objective | Main Work | Likely Files / Areas | Output | Estimated Time |
|---|---|---|---|---|---|
| 1 | Audit current CMS upload/edit flow | Inspect how media, gallery, services, projects, hero, and admin uploads currently work | `app/api_flask/media.py`, `app/api_flask/uploads.py`, `app/models/media.py`, `front_v02/src/components/admin/*`, `front_v02/src/lib/mediaApi.js`, `front_v02/src/lib/mediaResolver.js` | Clear map of current upload/edit/delete flow | 0.5 day |
| 2 | Define editable uploaded content model | Confirm whether uploaded content is stored as independent media records or attached directly to projects/services/hero/gallery | `app/models/media.py`, possibly `project.py`, `service.py`, `hero_slide.py`; schemas in `app/schemas/media.py` | Final editing rules: title, alt text, caption, file replacement, ordering, visibility | 0.5 day |
| 3 | Backend: support update/replace media | Add/confirm endpoints for updating metadata, replacing files, deleting files, and listing media by type | `app/api_flask/media.py`, `app/api_flask/uploads.py`, `app/services/*media*`, `app/schemas/media.py` | Admin can update existing uploaded content through API | 1 day |
| 4 | Backend: add video upload support | Extend allowed file validation to include video MIME types and extensions, store media type as image/video | `app/api_flask/uploads.py`, `app/api_flask/media.py`, `app/models/media.py`, `app/schemas/media.py`, `app/config.py` | Gallery accepts image + video uploads safely | 1 day |
| 5 | Database migration / model adjustment | Add/confirm fields like `media_type`, `mime_type`, `size`, `duration`, `caption`, `alt_text`, `sort_order`, `is_active` | `app/models/media.py`, `migrations/`, `alembic.ini` | DB supports richer editable media | 0.5–1 day |
| 6 | Frontend: admin gallery upload UI | Update admin gallery/media UI to accept videos and preview both images and videos | `front_v02/src/pages/admin/AdminGallery.jsx`, `front_v02/src/components/ui/ImageUploadField.jsx`, `front_v02/src/lib/mediaApi.js`, `front_v02/src/lib/mediaResolver.js` | Admin can upload and preview images/videos | 1 day |
| 7 | Frontend: admin edit existing media UI | Add edit modal/form for changing metadata or replacing uploaded file | `front_v02/src/pages/admin/AdminGallery.jsx`, possible new component `MediaEditModal.jsx`, `front_v02/src/components/admin/*` | Admin can edit uploaded content any time | 1 day |
| 8 | Public gallery rendering | Render videos correctly in public gallery without breaking images | `front_v02/src/components/GallerySection.jsx`, `front_v02/src/lib/galleryStore.js`, `front_v02/src/lib/mediaResolver.js`, possibly service/project detail pages | Public gallery displays mixed media | 0.5 day |
| 9 | Validation, limits, and security | Enforce safe file types, size limits, authenticated admin-only changes, cleanup old replaced files | `app/api_flask/uploads.py`, `app/middlewares/auth_middleware.py`, `app/config.py`, `app/utils/logger.py` | Secure upload/edit behavior | 0.5 day |
| 10 | Testing and regression check | Test upload, edit, replace, delete, image preview, video preview, public display, admin auth | `tests/`, `front_v02/src/__tests__/`, manual browser tests | Stable feature ready for deployment | 1 day |
| 11 | Deployment cleanup | Apply migrations, update requirements if needed, verify WSGI paths and static upload serving | `passenger_wsgi.py`, `requirements.txt`, `app/static/uploads/`, server config | Feature deployed safely | 0.5 day |

---

## Specific Objectives Per Phase

### Phase 1 — Audit Current CMS Flow
- Identify current upload endpoints.
- Identify how gallery items are fetched and rendered.
- Confirm whether admin currently edits only text records or also uploaded files.

### Phase 2 — Define Editable Media Rules
- Decide what admin can edit:
  - file replacement
  - title
  - caption
  - alt text
  - category/type
  - visibility
  - display order
- Decide whether videos are stored in the same table as images or separate records.

### Phase 3 — Backend Editing API
- Add/update API routes for:
  - media update
  - media replacement
  - media delete
  - media listing
- Ensure only authenticated admins can use them.

### Phase 4 — Video Upload Support
- Add allowed video extensions such as:
  - `.mp4`
  - `.webm`
  - `.mov`
  - `.avi` if desired
- Add MIME checking where possible.
- Store uploaded videos under a sensible path such as `uploads/gallery/videos/`.

### Phase 5 — Database / Migration
- Add fields if missing:
  - `media_type`
  - `mime_type`
  - `file_size`
  - `caption`
  - `alt_text`
  - `sort_order`
  - `is_active`
- Generate migration and apply it.

### Phase 6 — Admin Upload UI
- Change file input accept rules from image-only to image/video.
- Show image previews with `<img>`.
- Show video previews with `<video controls>`.

### Phase 7 — Admin Edit UI
- Add edit button per uploaded media item.
- Open edit modal/form.
- Allow replacing the file without deleting the database record.
- Refresh admin list after save.

### Phase 8 — Public Gallery Rendering
- Detect `media_type`.
- Render images and videos differently.
- Prevent videos from autoplaying unless intentionally desired.

### Phase 9 — Security and Cleanup
- Validate extensions and MIME types.
- Enforce file size limits.
- Require admin authentication.
- Delete old physical file after successful replacement where safe.

### Phase 10 — Tests
- Backend tests for upload/update/delete.
- Frontend tests for admin gallery and public gallery rendering.
- Manual tests for video formats.

### Phase 11 — Deployment
- Run migrations.
- Confirm static upload paths.
- Confirm WSGI deployment serves uploaded video files correctly.

---

## Files I Need You To Show Next Before Exact Implementation

Please paste or show the contents/structure for these files first so the implementation guide can be exact instead of guessed:

### Backend
- `app/api_flask/media.py`
- `app/api_flask/uploads.py`
- `app/models/media.py`
- `app/schemas/media.py`
- `app/config.py`
- `app/api_flask/__init__.py`
- `app/main.py` or the active Flask app factory file
- `passenger_wsgi.py`

### Frontend
- `front_v02/src/pages/admin/AdminGallery.jsx`
- `front_v02/src/components/ui/ImageUploadField.jsx`
- `front_v02/src/lib/mediaApi.js`
- `front_v02/src/lib/mediaResolver.js`
- `front_v02/src/lib/galleryStore.js`
- `front_v02/src/components/GallerySection.jsx`

### Optional but useful
- Any admin table/component currently showing uploaded gallery items.
- Any migration related to `media`.
- Any current upload tests.

---

## Recommended Implementation Order

1. Confirm current media model and upload endpoints.
2. Extend backend validation and database fields.
3. Add backend edit/replace/delete routes.
4. Update admin gallery UI.
5. Update public gallery renderer.
6. Add tests.
7. Deploy and verify uploaded video serving.

---

## Important Assumptions

- Backend is Flask WSGI now. FastAPI files are ignored.
- Admin CMS already has authentication.
- Gallery currently supports multiple image formats.
- Uploaded files are served from a static uploads folder.
- Video uploads should be admin-only.
