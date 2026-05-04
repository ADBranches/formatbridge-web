# Phase 1 Implementation Guide — Admin CMS Media Editing + Video Gallery Support

**Project:** Construction Company CMS  
**Backend:** Flask WSGI active structure  
**Frontend:** React/Vite  
**Patch tactic:** Targeted section patches first, full-file replacement only where needed

> **Important:** FastAPI traces are ignored as agreed. The active implementation path is `backend/app/api_flask/*` plus the React app in `front_v02/src/*`.

---

## What Happened

You were right to call this out. We agreed the guide should be delivered as **Markdown**, especially because we are using a patch-based implementation workflow. This file is the corrected Markdown guide for the first implementation phase.

---

## Phase 1 Objective

Enable the project foundation for:

1. Gallery uploads to accept **images and videos**.
2. Backend upload endpoints to return both:
   - `url`
   - `media_type`
3. Admin CMS to support editing existing media records through a backend update endpoint.
4. Public gallery to render images using `<img>` and videos using `<video controls>`.
5. Frontend store/API helpers to preserve media type.

This phase does **not yet fully patch `AdminGallery.jsx`**, because the uploaded audit cut off that file before the full JSX return section.

---

## Files Touched In Phase 1

### Backend

```text
backend/app/api_flask/uploads.py
backend/app/api_flask/media.py
```

### Frontend

```text
front_v02/src/lib/mediaApi.js
front_v02/src/lib/galleryStore.js
front_v02/src/components/GallerySection.jsx
```

### File Needed Before Phase 2

```text
front_v02/src/pages/admin/AdminGallery.jsx
```

Run:

```bash
sed -n '1,460p' front_v02/src/pages/admin/AdminGallery.jsx
```

Paste the full output before we patch the admin editing interface.

---

## Step 0 — Create A Safe Patch Branch

Run from your project root:

```bash
cd ~/byupw/6_block/wdd330/construction_co

git status

git checkout -b cms-media-video-edit-phase1
```

If you are not using git, make manual backups:

```bash
cp backend/app/api_flask/uploads.py backend/app/api_flask/uploads.py.bak-phase1
cp backend/app/api_flask/media.py backend/app/api_flask/media.py.bak-phase1
cp front_v02/src/lib/mediaApi.js front_v02/src/lib/mediaApi.js.bak-phase1
cp front_v02/src/lib/galleryStore.js front_v02/src/lib/galleryStore.js.bak-phase1
cp front_v02/src/components/GallerySection.jsx front_v02/src/components/GallerySection.jsx.bak-phase1
```

---

# Patch 1 — Backend Uploads

## Target File

```text
backend/app/api_flask/uploads.py
```

## Objective

Allow project and service gallery uploads to accept both images and videos.

Your file already has:

```python
IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif", "svg"}
VIDEO_EXTENSIONS = {"mp4", "webm", "ogg", "mov"}
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS
```

But the service/project gallery endpoints still force image-only validation. We will patch that.

---

## Patch 1.1 — Add Helper Functions

Find this function:

```python
def _allowed(filename: str, media_type: str | None = None) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    if media_type == "image":
        return ext in IMAGE_EXTENSIONS
    if media_type == "video":
        return ext in VIDEO_EXTENSIONS
    return ext in ALLOWED_EXTENSIONS
```

Immediately after it, add:

```python
def _detect_media_type(filename: str) -> str | None:
    """
    Detect media type from file extension.
    Returns: "image", "video", or None.
    """
    if "." not in filename:
        return None

    ext = filename.rsplit(".", 1)[1].lower()

    if ext in IMAGE_EXTENSIONS:
        return "image"

    if ext in VIDEO_EXTENSIONS:
        return "video"

    return None


def _save_upload(file, subdir: str) -> tuple[str, str]:
    """
    Save an uploaded file under app/static/uploads/<subdir>.
    Returns: (public_url, detected_media_type)
    """
    detected_media_type = _detect_media_type(file.filename)

    if detected_media_type is None:
        raise ValueError("Unsupported file type")

    upload_root = os.path.join(current_app.static_folder, "uploads", subdir)
    os.makedirs(upload_root, exist_ok=True)

    name_part = secure_filename(file.filename.rsplit(".", 1)[0])
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{name_part}-{int(time.time())}-{uuid.uuid4().hex[:6]}.{ext}"

    path = os.path.join(upload_root, filename)
    file.save(path)

    url = url_for("static", filename=f"uploads/{subdir}/{filename}", _external=True)
    return url, detected_media_type
```

---

## Patch 1.2 — Replace `upload_project_media()`

Replace the whole existing `upload_project_media()` function with:

```python
@uploads_bp.post("/admin/uploads/project-media")
@admin_required("gallery")
def upload_project_media():
    """
    Admin: upload a gallery image or video for a project.
    Accepts multipart/form-data with:
    - file
    - media_type optional: image/video

    Returns:
    {
      "url": "...",
      "media_type": "IMAGE" | "VIDEO"
    }
    """
    file = request.files.get("file")
    requested_media_type = (request.form.get("media_type") or "").lower().strip()

    if not file or file.filename == "":
        return jsonify({"detail": "No file uploaded"}), 400

    detected_media_type = _detect_media_type(file.filename)

    if detected_media_type is None:
        return jsonify({"detail": "Unsupported file type"}), 400

    if requested_media_type and requested_media_type not in {"image", "video"}:
        return jsonify({"detail": "Invalid media type"}), 400

    if requested_media_type and requested_media_type != detected_media_type:
        return jsonify({
            "detail": f"File extension does not match requested media type: {requested_media_type}"
        }), 400

    try:
        url, media_type = _save_upload(file, "projects")
    except ValueError as exc:
        return jsonify({"detail": str(exc)}), 400

    return jsonify({
        "url": url,
        "media_type": media_type.upper(),
    }), 201
```

---

## Patch 1.3 — Replace `upload_service_gallery()`

Replace the whole existing `upload_service_gallery()` function with:

```python
@uploads_bp.post("/admin/uploads/service-gallery")
@admin_required("gallery")
def upload_service_gallery():
    """
    Admin: upload a gallery image or video for a service/category.
    Accepts multipart/form-data with:
    - file
    - media_type optional: image/video

    Returns:
    {
      "url": "...",
      "media_type": "IMAGE" | "VIDEO"
    }
    """
    file = request.files.get("file")
    requested_media_type = (request.form.get("media_type") or "").lower().strip()

    if not file or file.filename == "":
        return jsonify({"detail": "No file uploaded"}), 400

    detected_media_type = _detect_media_type(file.filename)

    if detected_media_type is None:
        return jsonify({"detail": "Unsupported file type"}), 400

    if requested_media_type and requested_media_type not in {"image", "video"}:
        return jsonify({"detail": "Invalid media type"}), 400

    if requested_media_type and requested_media_type != detected_media_type:
        return jsonify({
            "detail": f"File extension does not match requested media type: {requested_media_type}"
        }), 400

    try:
        url, media_type = _save_upload(file, "services")
    except ValueError as exc:
        return jsonify({"detail": str(exc)}), 400

    return jsonify({
        "url": url,
        "media_type": media_type.upper(),
    }), 201
```

---

# Patch 2 — Backend Media Update Endpoint

## Target File

```text
backend/app/api_flask/media.py
```

## Objective

Allow admin CMS to edit existing uploaded media records.

---

## Patch 2.1 — Update Import

Find:

```python
from app.schemas.media import MediaCreate, MediaOut
```

Replace with:

```python
from app.schemas.media import MediaCreate, MediaOut, MediaUpdate
```

---

## Patch 2.2 — Add Update Route

Add this after `admin_delete_media()`:

```python
@media_bp.patch("/admin/media/<media_id>")
@admin_required("gallery")
def admin_update_media(media_id: str):
    """
    Admin: update an existing media item.

    Supports editing:
    - title
    - description
    - url
    - media_type
    - is_featured
    - sort_order
    - project_id
    - service_id

    This enables CMS editing without deleting/recreating media rows.
    """
    mid = _parse_uuid(media_id)
    if mid is None:
        return jsonify({"detail": "Invalid media id"}), 400

    payload = request.get_json(silent=True) or {}

    if "media_type" in payload and isinstance(payload["media_type"], str):
        payload["media_type"] = payload["media_type"].upper()

    try:
        media_in = MediaUpdate.model_validate(payload)
    except Exception as exc:
        return jsonify({"detail": str(exc)}), 400

    update_data = media_in.model_dump(exclude_unset=True)

    with get_session() as db:
        media = db.query(Media).filter(Media.id == mid).first()

        if not media:
            return jsonify({"detail": "Media not found"}), 404

        for key, value in update_data.items():
            setattr(media, key, value)

        db.commit()
        db.refresh(media)

        data = _serialize_media(media)

    return jsonify(data), 200
```

Optional: if you want `PUT` too, add:

```python
@media_bp.put("/admin/media/<media_id>")
@admin_required("gallery")
def admin_replace_media(media_id: str):
    return admin_update_media(media_id)
```

---

# Patch 3 — Frontend Media API

## Target File

```text
front_v02/src/lib/mediaApi.js
```

---

## Patch 3.1 — Replace `uploadProjectMedia`

Replace the existing function with:

```javascript
export async function uploadProjectMedia(file, mediaType = "") {
  const formData = new FormData();
  formData.append("file", file);

  if (mediaType) {
    formData.append("media_type", mediaType);
  }

  const data = await api.post(
    "/api/v1/admin/uploads/project-media",
    formData,
    {
      headers: {
        ...adminHeaders(),
      },
    }
  );

  if (!data?.url) {
    throw new Error("Upload succeeded but no URL returned.");
  }

  return data;
}
```

---

## Patch 3.2 — Replace `uploadServiceGalleryMedia`

Replace the existing function with:

```javascript
export async function uploadServiceGalleryMedia(file, mediaType = "") {
  const formData = new FormData();
  formData.append("file", file);

  if (mediaType) {
    formData.append("media_type", mediaType);
  }

  const data = await api.post(
    "/api/v1/admin/uploads/service-gallery",
    formData,
    {
      headers: {
        ...adminHeaders(),
      },
    }
  );

  if (!data?.url) {
    throw new Error("Upload succeeded but no URL returned.");
  }

  return data;
}
```

---

## Patch 3.3 — Add `updateMedia`

Add this near `deleteMedia`:

```javascript
/**
 * Update existing media metadata or file URL.
 * Backend: PATCH /api/v1/admin/media/:mediaId
 */
export async function updateMedia(mediaId, body) {
  const media = await api.patch(
    `/api/v1/admin/media/${mediaId}`,
    body,
    {
      headers: adminHeaders(),
    }
  );

  return media;
}
```

---

# Patch 4 — Preserve Media Type In Gallery Store

## Target File

```text
front_v02/src/lib/galleryStore.js
```

Find:

```javascript
image: m.url,
```

Change that section to:

```javascript
image: m.url,
mediaType: (m.media_type || "IMAGE").toString().toUpperCase(),
url: m.url,
```

---

# Patch 5 — Public Gallery Video Rendering

## Target File

```text
front_v02/src/components/GallerySection.jsx
```

Find:

```javascript
const src = resolveImage(item.image);
```

Replace with:

```javascript
const src = resolveImage(item.image || item.url);
const mediaType = (item.mediaType || item.media_type || "IMAGE")
  .toString()
  .toUpperCase();
const isVideo = mediaType === "VIDEO";
```

Then replace this image-only block:

```jsx
<motion.img
  src={src}
  alt={item.title || ""}
  className="h-full w-full object-cover"
  whileHover={{ scale: 1.05 }}
  transition={{ duration: 0.4 }}
/>
```

With this mixed media block:

```jsx
{isVideo ? (
  <video
    src={src}
    className="h-full w-full object-cover"
    controls
    preload="metadata"
  >
    Your browser does not support the video tag.
  </video>
) : (
  <motion.img
    src={src}
    alt={item.title || ""}
    className="h-full w-full object-cover"
    whileHover={{ scale: 1.05 }}
    transition={{ duration: 0.4 }}
  />
)}
```

Also change:

```jsx
No gallery images added yet. Check back soon.
```

To:

```jsx
No gallery media added yet. Check back soon.
```

---

# Step 6 — Backend Syntax Checks

From project root:

```bash
cd backend

python -m py_compile app/api_flask/uploads.py
python -m py_compile app/api_flask/media.py
```

If no output appears, syntax is okay.

Then run:

```bash
pytest
```

---

# Step 7 — Frontend Checks

From project root:

```bash
cd front_v02

npm run lint
```

If tests are configured:

```bash
npm test -- --run
```

Or:

```bash
npm test
```

---

# Step 8 — Manual Smoke Test

## Upload Video To Service Gallery

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/uploads/service-gallery" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -F "file=@/path/to/test-video.mp4" \
  -F "media_type=video"
```

Expected response:

```json
{
  "url": "http://127.0.0.1:8000/static/uploads/services/test-video-...mp4",
  "media_type": "VIDEO"
}
```

## Create Media Row For Uploaded Video

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/services/YOUR_SERVICE_ID/media" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test video",
    "description": "Gallery video test",
    "url": "PASTE_RETURNED_URL_HERE",
    "media_type": "VIDEO",
    "is_featured": false,
    "sort_order": 0
  }'
```

## Test Media Edit Endpoint

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/admin/media/YOUR_MEDIA_ID" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated media title",
    "description": "Updated media description",
    "media_type": "VIDEO"
  }'
```

---

# Phase 1 Acceptance Criteria

Phase 1 is complete when:

- Project gallery upload accepts image files.
- Project gallery upload accepts video files.
- Service gallery upload accepts image files.
- Service gallery upload accepts video files.
- Upload response includes `media_type`.
- Backend has `PATCH /api/v1/admin/media/<media_id>`.
- Public gallery renders videos with `<video controls>`.
- Public gallery still renders images normally.

---

# Next Phase

Before Phase 2, provide the full admin gallery file:

```bash
sed -n '1,460p' front_v02/src/pages/admin/AdminGallery.jsx
```

Phase 2 will patch:

```text
front_v02/src/pages/admin/AdminGallery.jsx
```

Expected Phase 2 features:

- admin edit button per gallery item
- edit modal/form
- title/description update
- media replacement
- media type auto-detection
- video preview in admin CMS
- refresh gallery after edit
