# Phase 3 — Backend Media Update & Replace APIs ✅ (PATCH GUIDE)

**Environment:** Kali Linux · zsh  \ 
**Project Root:** `~/Downloads/projects/byupw/6_block/wdd330/construction_co`

This guide contains the **exact, safe, section‑level backend modifications** to enable **media file replacement via the existing PATCH route**, using only terminal commands.

---

## ✅ Confirmed Starting Point

You already have:
- `PATCH /admin/media/<media_id>` updating metadata ✅
- Upload helpers in `uploads.py` ✅
- Admin auth guard ✅

What we add now:
> **Optional file replacement** inside the PATCH route (multipart/form‑data)

---

## 🔒 Scope of Changes

We will **only modify**:

- `backend/app/api_flask/media.py`

🚫 No schema changes  
🚫 No frontend changes  
🚫 No file cleanup yet

---

## Step 1 — Add Required Imports

### Command (zsh)
```zsh
apply_patch <<'PATCH'
*** Begin Patch
*** Update File: backend/app/api_flask/media.py
@@
 from flask import Blueprint, jsonify, request
+from werkzeug.datastructures import ImmutableMultiDict
+
+# reuse upload helpers
+from app.api_flask.uploads import _save_upload, _detect_media_type
*** End Patch
PATCH
```

---

## Step 2 — Extend PATCH Handler to Support File Replacement

We replace **only the body** of `admin_update_media`.

### ✅ What this adds
- Accepts `multipart/form-data`
- Detects `file` if provided
- Replaces `url` + `media_type`
- Keeps existing metadata behavior intact

---

### Command (zsh)
```zsh
apply_patch <<'PATCH'
*** Begin Patch
*** Update File: backend/app/api_flask/media.py
@@
 def admin_update_media(media_id: str):
@@
-    payload = request.get_json(silent=True) or {}
+    # Support both JSON and multipart/form-data
+    payload = {}
+    if request.content_type and request.content_type.startswith("multipart/form-data"):
+        payload = dict(request.form)
+    else:
+        payload = request.get_json(silent=True) or {}
@@
-    try:
-        media_in = MediaUpdate.model_validate(payload)
+    try:
+        media_in = MediaUpdate.model_validate(payload)
     except Exception as exc:
         return jsonify({"detail": str(exc)}), 400
@@
     with get_session() as db:
         media = db.query(Media).filter(Media.id == mid).first()
@@
         if not media:
             return jsonify({"detail": "Media not found"}), 404

+        # --- Optional file replacement ---
+        file = request.files.get("file")
+        if file:
+            detected_type = _detect_media_type(file.filename)
+            if not detected_type:
+                return jsonify({"detail": "Unsupported file type"}), 400
+
+            # reuse existing storage logic
+            try:
+                url, new_type = _save_upload(file, "services" if media.service_id else "projects")
+            except Exception as exc:
+                return jsonify({"detail": str(exc)}), 400
+
+            media.url = url
+            media.media_type = new_type.upper()
+
+        # --- Apply metadata updates ---
         for key, value in update_data.items():
             setattr(media, key, value)
*** End Patch
PATCH
```

---

## Step 3 — Sanity Check (No Code Changes)

Run these commands to confirm patch integrity:

```zsh
python -m compileall backend/app/api_flask/media.py
```

```zsh
grep -R "Optional file replacement" -n backend/app/api_flask/media.py
```

---

## ✅ What You Can Do Now (Immediately)

Admins can now:
- PATCH metadata ✅
- PATCH with `file` to replace media ✅
- Keep the same media ID ✅

Example request:
```http
PATCH /api/v1/admin/media/<id>
Content-Type: multipart/form-data

file=@new_video.mp4
title=Updated title
```

---

## 🚫 Intentionally Deferred

These are **NOT** part of Phase 3:
- Deleting old physical files
- Frontend upload UI changes
- Edit modal UI

---

## ⏭️ Next Phase — Phase 4

**Objective:** Admin UI edit modal & file replacement interface

I will deliver a **Phase 4 terminal guide** when you say:

> **"Proceed to Phase 4 markdown"**

✅ Phase 3 backend implementation is now complete.
