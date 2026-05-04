# Terminal Patch Commands — CMS Editable Media + Video Gallery Support

**Branch:** `cms-media-video-edit-phase1`  
**Patch method:** one terminal-created Python patch script with backups  
**Backend target:** Flask WSGI files under `backend/app/api_flask/`  
**Frontend target:** React/Vite files under `front_v02/src/`

---

## What This Patch Implements

This patch implements the foundation for the CMS media work:

- gallery uploads accept images and videos
- upload responses include `url` and `media_type`
- backend adds `PATCH /api/v1/admin/media/<media_id>`
- frontend media API adds `updateMedia()`
- public gallery keeps media type
- public gallery renders videos with `<video controls>`

> Note: The uploaded `AdminGallery.jsx` content was still cut before the full file end. So this patch prepares backend + public display + API helpers. The final admin edit modal UI will be patched after we get the complete `AdminGallery.jsx` file.

---

# 1. Go To Project Root

```bash
cd ~/byupw/6_block/wdd330/construction_co 2>/dev/null || cd ~/Desktop/byupw/6_block/wdd330/construction_co 2>/dev/null || pwd
ls
```

You should see:

```text
backend
front_v02
README.md
```

---

# 2. Confirm Branch

```bash
git branch --show-current
git status
```

If not on the patch branch:

```bash
git checkout cms-media-video-edit-phase1
```

---

# 3. Create The Patch Script

Run this full command:

```bash
cat > apply_cms_media_phase1_patch.py <<'PY'
from pathlib import Path
import re
import shutil
import sys
from datetime import datetime

ROOT = Path.cwd()
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP_DIR = ROOT / f"patch_backups_cms_media_phase1_{STAMP}"

FILES = {
    "uploads": ROOT / "backend/app/api_flask/uploads.py",
    "media": ROOT / "backend/app/api_flask/media.py",
    "media_api": ROOT / "front_v02/src/lib/mediaApi.js",
    "gallery_store": ROOT / "front_v02/src/lib/galleryStore.js",
    "gallery_section": ROOT / "front_v02/src/components/GallerySection.jsx",
}


def fail(msg):
    print(f"\n❌ {msg}")
    sys.exit(1)


def read(path):
    if not path.exists():
        fail(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def write(path, text):
    path.write_text(text, encoding="utf-8")
    print(f"✅ patched: {path}")


def backup(path):
    BACKUP_DIR.mkdir(exist_ok=True)
    dest = BACKUP_DIR / path.relative_to(ROOT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)


for p in FILES.values():
    backup(p)

print(f"✅ backups saved in: {BACKUP_DIR}")

# ------------------------------------------------------------
# Patch backend/app/api_flask/uploads.py
# ------------------------------------------------------------
uploads_path = FILES["uploads"]
uploads = read(uploads_path)

helper_block = """

def _detect_media_type(filename: str) -> str | None:
    # Detect media type from file extension.
    if "." not in filename:
        return None

    ext = filename.rsplit(".", 1)[1].lower()

    if ext in IMAGE_EXTENSIONS:
        return "image"

    if ext in VIDEO_EXTENSIONS:
        return "video"

    return None


def _save_upload(file, subdir: str) -> tuple[str, str]:
    # Save an uploaded file under app/static/uploads/<subdir>.
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
"""

if "def _detect_media_type(" not in uploads:
    marker = "    return ext in ALLOWED_EXTENSIONS\n"
    if marker not in uploads:
        fail("Could not find _allowed() ending marker in uploads.py")
    uploads = uploads.replace(marker, marker + helper_block, 1)

project_func = """@uploads_bp.post(\"/admin/uploads/project-media\")
@admin_required(\"gallery\")
def upload_project_media():
    file = request.files.get(\"file\")
    requested_media_type = (request.form.get(\"media_type\") or \"\").lower().strip()

    if not file or file.filename == \"\":
        return jsonify({\"detail\": \"No file uploaded\"}), 400

    detected_media_type = _detect_media_type(file.filename)

    if detected_media_type is None:
        return jsonify({\"detail\": \"Unsupported file type\"}), 400

    if requested_media_type and requested_media_type not in {\"image\", \"video\"}:
        return jsonify({\"detail\": \"Invalid media type\"}), 400

    if requested_media_type and requested_media_type != detected_media_type:
        return jsonify({
            \"detail\": f\"File extension does not match requested media type: {requested_media_type}\"
        }), 400

    try:
        url, media_type = _save_upload(file, \"projects\")
    except ValueError as exc:
        return jsonify({\"detail\": str(exc)}), 400

    return jsonify({
        \"url\": url,
        \"media_type\": media_type.upper(),
    }), 201
"""

service_func = """@uploads_bp.post(\"/admin/uploads/service-gallery\")
@admin_required(\"gallery\")
def upload_service_gallery():
    file = request.files.get(\"file\")
    requested_media_type = (request.form.get(\"media_type\") or \"\").lower().strip()

    if not file or file.filename == \"\":
        return jsonify({\"detail\": \"No file uploaded\"}), 400

    detected_media_type = _detect_media_type(file.filename)

    if detected_media_type is None:
        return jsonify({\"detail\": \"Unsupported file type\"}), 400

    if requested_media_type and requested_media_type not in {\"image\", \"video\"}:
        return jsonify({\"detail\": \"Invalid media type\"}), 400

    if requested_media_type and requested_media_type != detected_media_type:
        return jsonify({
            \"detail\": f\"File extension does not match requested media type: {requested_media_type}\"
        }), 400

    try:
        url, media_type = _save_upload(file, \"services\")
    except ValueError as exc:
        return jsonify({\"detail\": str(exc)}), 400

    return jsonify({
        \"url\": url,
        \"media_type\": media_type.upper(),
    }), 201
"""

uploads = re.sub(
    r'@uploads_bp\.post\("/admin/uploads/project-media"\)\n@admin_required\("gallery"\)\ndef upload_project_media\(\):\n.*?(?=\n\s*"""Upload a gallery image for a service\.|\n@uploads_bp\.post\("/admin/uploads/service-gallery"\))',
    project_func + "\n\n",
    uploads,
    flags=re.S,
)

uploads = re.sub(
    r'@uploads_bp\.post\("/admin/uploads/service-gallery"\)\n@admin_required\("gallery"\)\ndef upload_service_gallery\(\):\n.*?(?=\n@uploads_bp\.post\("/admin/uploads/partner-logo"\))',
    service_func + "\n\n",
    uploads,
    flags=re.S,
)

if "requested_media_type" not in uploads:
    fail("Upload function replacement failed in uploads.py")

write(uploads_path, uploads)

# ------------------------------------------------------------
# Patch backend/app/api_flask/media.py
# ------------------------------------------------------------
media_path = FILES["media"]
media = read(media_path)

media = media.replace(
    "from app.schemas.media import MediaCreate, MediaOut",
    "from app.schemas.media import MediaCreate, MediaOut, MediaUpdate",
)

update_route = """

@media_bp.patch(\"/admin/media/<media_id>\")
@admin_required(\"gallery\")
def admin_update_media(media_id: str):
    mid = _parse_uuid(media_id)
    if mid is None:
        return jsonify({\"detail\": \"Invalid media id\"}), 400

    payload = request.get_json(silent=True) or {}

    if \"media_type\" in payload and isinstance(payload[\"media_type\"], str):
        payload[\"media_type\"] = payload[\"media_type\"].upper()

    try:
        media_in = MediaUpdate.model_validate(payload)
    except Exception as exc:
        return jsonify({\"detail\": str(exc)}), 400

    update_data = media_in.model_dump(exclude_unset=True)

    with get_session() as db:
        media = db.query(Media).filter(Media.id == mid).first()

        if not media:
            return jsonify({\"detail\": \"Media not found\"}), 404

        for key, value in update_data.items():
            setattr(media, key, value)

        db.commit()
        db.refresh(media)

        data = _serialize_media(media)

    return jsonify(data), 200


@media_bp.put(\"/admin/media/<media_id>\")
@admin_required(\"gallery\")
def admin_replace_media(media_id: str):
    return admin_update_media(media_id)
"""

if "def admin_update_media(" not in media:
    marker = 'return ("", 204)\n'
    if marker not in media:
        fail("Could not find admin_delete_media return marker in media.py")
    media = media.replace(marker, marker + update_route, 1)

write(media_path, media)

# ------------------------------------------------------------
# Patch front_v02/src/lib/mediaApi.js
# ------------------------------------------------------------
media_api_path = FILES["media_api"]
media_api = read(media_api_path)

new_upload_project = """export async function uploadProjectMedia(file, mediaType = \"\") {
  const formData = new FormData();
  formData.append(\"file\", file);

  if (mediaType) {
    formData.append(\"media_type\", mediaType);
  }

  const data = await api.post(
    \"/api/v1/admin/uploads/project-media\",
    formData,
    {
      headers: {
        ...adminHeaders(),
      },
    }
  );

  if (!data?.url) {
    throw new Error(\"Upload succeeded but no URL returned.\");
  }

  return data;
}
"""

new_upload_service = """export async function uploadServiceGalleryMedia(file, mediaType = \"\") {
  const formData = new FormData();
  formData.append(\"file\", file);

  if (mediaType) {
    formData.append(\"media_type\", mediaType);
  }

  const data = await api.post(
    \"/api/v1/admin/uploads/service-gallery\",
    formData,
    {
      headers: {
        ...adminHeaders(),
      },
    }
  );

  if (!data?.url) {
    throw new Error(\"Upload succeeded but no URL returned.\");
  }

  return data;
}
"""

media_api = re.sub(
    r'export async function uploadProjectMedia\(file\) \{.*?\n\}',
    new_upload_project.rstrip(),
    media_api,
    flags=re.S,
)

media_api = re.sub(
    r'export async function uploadServiceGalleryMedia\(file\) \{.*?\n\}',
    new_upload_service.rstrip(),
    media_api,
    flags=re.S,
)

update_media_func = """

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
"""

if "export async function updateMedia(" not in media_api:
    marker = "export async function deleteMedia(mediaId) {"
    idx = media_api.find(marker)
    if idx == -1:
        fail("Could not find deleteMedia() marker in mediaApi.js")
    media_api = media_api[:idx] + update_media_func + "\n" + media_api[idx:]

write(media_api_path, media_api)

# ------------------------------------------------------------
# Patch front_v02/src/lib/galleryStore.js
# ------------------------------------------------------------
gallery_store_path = FILES["gallery_store"]
gallery_store = read(gallery_store_path)

if "mediaType:" not in gallery_store:
    gallery_store = gallery_store.replace(
        "image: m.url,",
        "image: m.url,\n    mediaType: (m.media_type || \"IMAGE\").toString().toUpperCase(),\n    url: m.url,",
        1,
    )

write(gallery_store_path, gallery_store)

# ------------------------------------------------------------
# Patch front_v02/src/components/GallerySection.jsx
# ------------------------------------------------------------
gallery_section_path = FILES["gallery_section"]
gallery_section = read(gallery_section_path)

gallery_section = gallery_section.replace(
    "const src = resolveImage(item.image);",
    """const src = resolveImage(item.image || item.url);
          const mediaType = (item.mediaType || item.media_type || \"IMAGE\")
            .toString()
            .toUpperCase();
          const isVideo = mediaType === \"VIDEO\";""",
    1,
)

old_img_block = """<motion.img
                  src={src}
                  alt={item.title || \"\"}
                  className=\"h-full w-full object-cover\"
                  whileHover={{ scale: 1.05 }}
                  transition={{ duration: 0.4 }}
                />"""

new_media_block = """{isVideo ? (
                  <video
                    src={src}
                    className=\"h-full w-full object-cover\"
                    controls
                    preload=\"metadata\"
                  >
                    Your browser does not support the video tag.
                  </video>
                ) : (
                  <motion.img
                    src={src}
                    alt={item.title || \"\"}
                    className=\"h-full w-full object-cover\"
                    whileHover={{ scale: 1.05 }}
                    transition={{ duration: 0.4 }}
                  />
                )}"""

if old_img_block in gallery_section:
    gallery_section = gallery_section.replace(old_img_block, new_media_block, 1)
else:
    fail("Could not find GallerySection.jsx image block. Manual patch may be needed.")

gallery_section = gallery_section.replace(
    "No gallery images added yet. Check back soon.",
    "No gallery media added yet. Check back soon.",
)

write(gallery_section_path, gallery_section)

print("\n✅ Phase 1 CMS media/video patch completed.")
print("✅ Review git diff, then run checks.")
PY
```

---

# 4. Run The Patch Script

```bash
python apply_cms_media_phase1_patch.py
```

Expected output:

```text
✅ backups saved in: patch_backups_cms_media_phase1_...
✅ patched: backend/app/api_flask/uploads.py
✅ patched: backend/app/api_flask/media.py
✅ patched: front_v02/src/lib/mediaApi.js
✅ patched: front_v02/src/lib/galleryStore.js
✅ patched: front_v02/src/components/GallerySection.jsx
✅ Phase 1 CMS media/video patch completed.
```

---

# 5. Review The Diff

```bash
git diff -- backend/app/api_flask/uploads.py
git diff -- backend/app/api_flask/media.py
git diff -- front_v02/src/lib/mediaApi.js
git diff -- front_v02/src/lib/galleryStore.js
git diff -- front_v02/src/components/GallerySection.jsx
```

Or full diff:

```bash
git diff
```

---

# 6. Backend Syntax Checks

```bash
cd backend
python -m py_compile app/api_flask/uploads.py
python -m py_compile app/api_flask/media.py
cd ..
```

No output means syntax is okay.

---

# 7. Frontend Build Checks

```bash
cd front_v02
npm run build
cd ..
```

Optional lint:

```bash
cd front_v02
npm run lint
cd ..
```

---

# 8. Run Tests If Available

Backend:

```bash
cd backend
pytest
cd ..
```

Frontend:

```bash
cd front_v02
npm test -- --run
cd ..
```

If that does not work:

```bash
cd front_v02
npm test
cd ..
```

---

# 9. Manual Smoke Test Commands

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
  "url": "http://127.0.0.1:8000/static/uploads/services/your-file.mp4",
  "media_type": "VIDEO"
}
```

## Upload Image To Service Gallery

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/uploads/service-gallery" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -F "file=@/path/to/test-image.webp" \
  -F "media_type=image"
```

Expected response:

```json
{
  "url": "http://127.0.0.1:8000/static/uploads/services/your-file.webp",
  "media_type": "IMAGE"
}
```

## Create Media Row For Uploaded Video

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/services/YOUR_SERVICE_ID/media" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test gallery video",
    "description": "Video uploaded through CMS media patch",
    "url": "PASTE_RETURNED_URL_HERE",
    "media_type": "VIDEO",
    "is_featured": false,
    "sort_order": 0
  }'
```

## Edit Existing Media

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/admin/media/YOUR_MEDIA_ID" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated media title",
    "description": "Updated media description from edit endpoint",
    "media_type": "VIDEO"
  }'
```

---

# 10. Commit The Patch

```bash
git status

git add \
  backend/app/api_flask/uploads.py \
  backend/app/api_flask/media.py \
  front_v02/src/lib/mediaApi.js \
  front_v02/src/lib/galleryStore.js \
  front_v02/src/components/GallerySection.jsx \
  apply_cms_media_phase1_patch.py

git commit -m "Add editable media API and video gallery support foundation"

git push
```

If upstream error appears:

```bash
git push --set-upstream origin cms-media-video-edit-phase1
```

---

# 11. Rollback If Needed

```bash
git restore \
  backend/app/api_flask/uploads.py \
  backend/app/api_flask/media.py \
  front_v02/src/lib/mediaApi.js \
  front_v02/src/lib/galleryStore.js \
  front_v02/src/components/GallerySection.jsx
```

Backup folders are also created automatically:

```bash
ls -d patch_backups_cms_media_phase1_*
```

---

# 12. Required Next Output For Final Admin CMS UI Patch

After Phase 1 works, run:

```bash
sed -n '1,700p' front_v02/src/pages/admin/AdminGallery.jsx > admin_gallery_full_dump.txt
cat admin_gallery_full_dump.txt
```

Paste that full output here so the next patch can safely add:

- edit button per media item
- edit modal/form
- replace uploaded image/video
- admin image/video preview
- `PATCH /api/v1/admin/media/:id` integration
- refresh list after edit

---

# Phase 1 Is Done When

- backend compiles
- frontend builds
- service gallery accepts image files
- service gallery accepts video files
- project gallery accepts image files
- project gallery accepts video files
- public gallery displays videos with controls
- media edit endpoint works through curl
