# Phase 3 — Backend Media Update & Replace APIs (Terminal‑First Guide)

**Environment:** Kali Linux · zsh · terminal‑only workflow  
**Project Root:** `~/Downloads/projects/byupw/6_block/wdd330/construction_co`

**Phase Status:** READY FOR IMPLEMENTATION

---

## Phase 3 Objective

Enable **admins only** to:
- Update media metadata (title, description, sort_order, is_featured, relations)
- Replace the physical media file **without creating a new DB row**
- Delete media safely
- List media consistently for admin workflows

✅ Phase 1 & 2 confirmed that most of this already exists — this phase **closes the remaining backend gaps and formalizes replacement support**.

---

## Background Reality (From Phase 1)

✅ Already present:
- `PATCH /admin/media/<id>` (metadata update)
- `DELETE /admin/media/<id>`
- Upload routes returning `{ url, media_type }`

🔴 Missing / incomplete:
- Unified **file replacement** flow
- Optional cleanup hook for old files (not deletion yet)

---

## Phase 3 Strategy (Minimal & Safe)

We will:
1. Extend `PATCH /admin/media/<id>` to optionally accept:
   - `file` (multipart)
2. Reuse existing upload logic for storage
3. Update `url` + `media_type` atomically
4. Leave old file cleanup to Phase 6

🚫 No schema changes
🚫 No new tables

---

## 🔍 Files to Modify (Backend Only)

### Primary Targets
- `~/Downloads/projects/byupw/6_block/wdd330/construction_co/backend/app/api_flask/media.py`
- `~/Downloads/projects/byupw/6_block/wdd330/construction_co/backend/app/api_flask/uploads.py`

### Optional Helper Location
- `~/Downloads/projects/byupw/6_block/wdd330/construction_co/backend/app/services/`

---

## Step A — Inspect Existing PATCH Handler (Mandatory)

Before modifying, re‑inspect the end of `media.py` to confirm exact structure.

```zsh
sed -n '200,350p' ~/Downloads/projects/byupw/6_block/wdd330/construction_co/backend/app/api_flask/media.py
```

✅ Do **not** proceed until reviewed.

---

## Step B — Design Decision (Locked)

### PATCH `/admin/media/<media_id>` will support:

**Content‑Type: `multipart/form-data`**

| Field | Optional | Purpose |
|---|---|---|
| title | ✅ | Metadata edit |
| description | ✅ | Metadata edit |
| sort_order | ✅ | Reorder |
| is_featured | ✅ | Toggle featured |
| project_id | ✅ | Re‑associate |
| service_id | ✅ | Re‑associate |
| file | ✅ | Replace physical file |

---

## Step C — Implementation Plan (No Code Yet)

We will:
1. Detect `request.files.get("file")`
2. If file exists:
   - Store via `_save_upload()` (existing)
   - Update `media.url`
   - Update `media.media_type`
3. Apply `MediaUpdate` for remaining fields

All inside **existing PATCH route**.

---

## Step D — Guardrails

- Only `@admin_required("gallery")`
- Reject mismatched media_type vs file
- Return updated `MediaOut`

---

## ✅ Phase 3 Completion Criteria

| Requirement | Status |
|---|---|
| Admin can update metadata | ✅ existing |
| Admin can delete media | ✅ existing |
| Admin can replace file | ✅ after this phase |
| Public endpoints untouched | ✅ |

---

## 🚫 What Phase 3 Does NOT Do

- ❌ Delete old physical files
- ❌ Change frontend UI
- ❌ Update DB schema

(These are later phases.)

---

## ⏭️ Next Phase — Phase 4

**Objective:** Admin UI edit modal + file replacement UI

---

## ✅ Required Confirmation Before Coding

Reply with **one of the following**:

1️⃣ `Proceed with Phase 3 backend patch guide`
2️⃣ `Show me the rest of PATCH handler before changes`

No backend modification will occur without your explicit go‑ahead.
