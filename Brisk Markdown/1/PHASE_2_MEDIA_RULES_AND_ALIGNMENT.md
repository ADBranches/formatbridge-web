# Phase 2 — Define Editable Media Rules (Terminal‑First Guide)

**Phase Status:** READY FOR IMPLEMENTATION  
**Prerequisite:** ✅ Phase 1 audit completed and locked  
**Environment:** Kali Linux · zsh · terminal‑only workflow

---

## Phase 2 Objective

Formally **define, freeze, and align** the rules for editable media across:
- Backend schemas & API expectations
- Admin UI editing behavior
- Future Phase 3–7 implementations

⚠️ **Important**: This phase introduces **NO functional changes**. It is a *pre‑implementation alignment phase* that ensures all later edits are intentional, minimal, and safe.

---

## ✅ Confirmed Design Decisions (Locked)

Based strictly on Phase 1 findings.

### 1️⃣ Single Unified Media Model

✔ One `media` table supports **both images and videos**
✔ No table split or polymorphism needed

```text
IMAGE | VIDEO
```

---

### 2️⃣ Editable Fields (Admin‑Only)

Admins are allowed to edit **existing uploaded media at any time**:

| Field | Editable | Notes |
|---|---|---|
| title | ✅ | Display title |
| description | ✅ | Caption/description |
| media_type | ⚠️ restricted | IMAGE ↔ VIDEO only when replacing file |
| is_featured | ✅ | Gallery prominence |
| sort_order | ✅ | Display ordering |
| project_id | ✅ | Re‑association allowed |
| service_id | ✅ | Gallery category |
| url | ✅ (replace only) | Old file cleaned later |

🚫 File replacement **never creates a new DB row**

---

### 3️⃣ Media Replacement Rules

When an admin replaces a file:

1. Upload new file
2. Detect media type from file extension
3. Update `media.url`
4. Update `media.media_type`
5. (Later phase) delete old physical file

✅ ID remains constant

---

### 4️⃣ Upload Responsibilities Split

| Responsibility | Owner |
|---|---|
| Validate extension | Backend |
| Validate MIME | Backend |
| Store under /static/uploads | Backend |
| Metadata editing | Admin UI |
| Preview rendering | Frontend |

---

## 🔴 Identified Gaps to Fix (Next Phases)

| Location | Problem | Phase |
|---|---|---|
| ImageUploadField.jsx | image‑only restriction | Phase 3 |
| AdminGallery.jsx | no edit modal | Phase 4 |
| Backend uploads | no cleanup on replace | Phase 6 |

---

## 🔒 Files Reviewed & Locked (NO changes now)

### Backend
- `~/Downloads/projects/byupw/6_block/wdd330/construction_co/backend/app/models/media.py`
- `~/Downloads/projects/byupw/6_block/wdd330/construction_co/backend/app/schemas/media.py`
- `~/Downloads/projects/byupw/6_block/wdd330/construction_co/backend/app/api_flask/media.py`

### Frontend
- `~/Downloads/projects/byupw/6_block/wdd330/construction_co/front_v02/src/components/GallerySection.jsx`
- `~/Downloads/projects/byupw/6_block/wdd330/construction_co/front_v02/src/lib/mediaResolver.js`

✅ These already meet Phase‑2 requirements

---

## ✅ Phase 2 Completion Criteria

Phase 2 is complete when:

- Editable rules are formally accepted
- No schema or API disagreement exists
- All future phases agree to this contract

✅ Phase 2 produces **clarity, not code**

---

## ⏭️ What Comes Next — Phase 3

**Phase 3 Objective**
> Enable mixed image + video uploads in the Admin UI

**First file to modify**
```text
front_v02/src/components/ui/ImageUploadField.jsx
```

📄 I will next provide:
- **Phase 3 terminal implementation markdown (.md)**
- Safe section‑level commands (`sed`, `apply_patch`)
- Zero rewrites, zero guessing

🚫 Implementation will not begin until Phase 3 markdown is delivered.
