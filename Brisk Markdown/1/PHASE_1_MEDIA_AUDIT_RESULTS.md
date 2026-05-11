# Phase 1 — System Audit & Flow Mapping ✅ (Completed)

**Environment:** Kali Linux · zsh · terminal‑first workflow  
**Project:** Construction CMS (Flask WSGI + FastAPI + React/Vite)

This document records the **confirmed findings** after inspecting the actual source files. It serves as the authoritative reference for all subsequent implementation phases.

---

## 1️⃣ Backend — Confirmed Media Flow

### ✅ Upload Handling (`app/api_flask/uploads.py`)

**Storage location**
- All uploaded files are saved under:
  ```text
  ~/Downloads/projects/byupw/6_block/wdd330/construction_co/backend/app/static/uploads/
  ```

**Upload routes**
| Route | Purpose | Subdir | Supports Video |
|---|---|---|---|
| `/admin/uploads/service-hero` | Service hero image | `uploads/services/` | ❌ image‑only |
| `/admin/uploads/project-media` | Project gallery | `uploads/projects/` | ✅ image + video |
| `/admin/uploads/service-gallery` | Service gallery | `uploads/services/` | ✅ image + video |
| `/admin/uploads/partner-logo` | Partner logos | `uploads/partners/` | ❌ image‑only |

**Key findings**
- Extension‑based media detection via `_detect_media_type()`
- Videos already **accepted and stored** for project + service galleries
- URLs returned are **absolute** via `url_for('static', ...)`

---

### ✅ Media API (`app/api_flask/media.py`)

**Public endpoints**
- `GET /api/v1/media`
- `GET /api/v1/gallery/about`

**Admin endpoints**
- `POST /api/v1/admin/projects/<project_id>/media`
- `PATCH /api/v1/admin/media/<media_id>` ✅ metadata update
- `DELETE /api/v1/admin/media/<media_id>` ✅ hard delete

**Media serialization includes**
```json
{
  id,
  service_name,
  service_slug,
  title,
  description,
  url,
  media_type,   // IMAGE | VIDEO
  sort_order,
  is_featured
}
```

✅ Backend already fully **media‑type aware**

---

### ✅ Data Model (`app/models/media.py`)

- Single unified `media` table
- Supports:
  - `IMAGE` and `VIDEO`
  - project‑linked media
  - service‑linked media (gallery categories)

✅ No schema redesign required for video

---

## 2️⃣ Frontend — Confirmed Media Flow

### ✅ Admin Gallery (`AdminGallery.jsx`)

- Categories = `Service` records
- Media loaded from:
  ```http
  GET /api/v1/admin/services/<service_id>/media
  ```
- Upload preview uses `URL.createObjectURL`

⚠️ **Observation**
- Upload UI does not yet differentiate image vs video visually

---

### ✅ Image Upload Field (`ImageUploadField.jsx`)

**Client validation**
- ❌ image‑only (`png, jpg, jpeg, webp, svg, gif`)
- Explicit MIME + extension checking

🔴 **This is the PRIMARY frontend blocker for video**

---

### ✅ Public Gallery (`GallerySection.jsx`)

✅ Already video‑aware:
```jsx
const isVideo = mediaType === "VIDEO";
```

Renders:
- `<img />` for images
- `<video controls />` for videos

✅ Public rendering is READY

---

### ✅ Media Resolution (`mediaResolver.js`)

- Resolves:
  - `/uploads/...`
  - `/static/...`
  - absolute URLs

✅ Works for both images & videos

---

## 3️⃣ STATIC Serving (Critical Confirmation)

### FastAPI (`app/main.py`)
```py
app.mount("/static", StaticFiles(directory=backend/static))
```

### Flask WSGI (`passenger_wsgi.py`)
- Production Flask app uses same static directory

✅ Uploaded videos are served correctly in both dev & prod

---

## ✅ Phase 1 Conclusion

| Area | Status |
|---|---|
| Backend supports video | ✅ |
| Media DB supports edits | ✅ |
| Public gallery renders video | ✅ |
| Admin edit APIs exist | ✅ |
| Frontend upload blocks video | 🔴 |

**Main gap identified:**
> `ImageUploadField.jsx` enforces image‑only validation

---

## ⏭️ Next Phase (Phase 2)

**Objective**
- Define editable rules formally
- Prepare frontend + admin UI for mixed media

**Next action (no code yet):**
I will return **Phase 2 – Implementation Markdown** with:
- Targeted file sections
- Exact terminal commands (`sed`, `apply_patch`, `python - <<'PY'`)
- Zero guesswork

✅ Phase 1 is **complete and locked**.
