# Phase 1 — System Audit & Flow Mapping (Terminal‑First Guide)

**Scope:** Flask WSGI backend + React/Vite frontend  
**Environment:** Kali Linux, zsh shell  
**Method:** Read‑only inspection using terminal commands before any modification

---

## Phase Objective

Before touching any code, we must **fully understand**:
- How media is uploaded
- Where it is stored on disk
- How it is saved in the database
- How it is exposed via APIs
- How the admin UI uploads & lists media
- How the public gallery renders it

⚠️ **No implementation begins until every file listed below has been inspected.**

---

## Backend — Required File Inspections

### 1. `app/api_flask/media.py`

**Purpose to confirm**
- Existing media listing endpoints
- Admin vs public access
- Update/delete availability

**Run:**
```zsh
sed -n '1,200p' app/api_flask/media.py
```

---

### 2. `app/api_flask/uploads.py`

**Purpose to confirm**
- Upload route(s)
- Allowed file extensions
- Storage paths
- Image‑only assumptions

**Run:**
```zsh
sed -n '1,200p' app/api_flask/uploads.py
```

---

### 3. `app/models/media.py`

**Purpose to confirm**
- Media table fields
- Image vs generic media handling
- Relationships (projects/services)

**Run:**
```zsh
sed -n '1,200p' app/models/media.py
```

---

### 4. `app/schemas/media.py`

**Purpose to confirm**
- API response shape
- Fields exposed to frontend

**Run:**
```zsh
sed -n '1,200p' app/schemas/media.py
```

---

### 5. `app/config.py`

**Purpose to confirm**
- Upload directory
- Max file size
- Allowed extensions

**Run:**
```zsh
sed -n '1,200p' app/config.py
```

---

### 6. `app/main.py`

**Purpose to confirm**
- Flask app factory
- Blueprint registration
- Static/uploads serving

**Run:**
```zsh
sed -n '1,200p' app/main.py
```

---

### 7. `passenger_wsgi.py`

**Purpose to confirm**
- WSGI entry
- Static path exposure

**Run:**
```zsh
sed -n '1,200p' passenger_wsgi.py
```

---

## Frontend — Required File Inspections

### 8. `src/pages/admin/AdminGallery.jsx`

**Purpose to confirm**
- Upload UI logic
- Media listing UI
- Edit/delete availability

**Run:**
```zsh
sed -n '1,200p' front_v02/src/pages/admin/AdminGallery.jsx
```

---

### 9. `src/components/GallerySection.jsx`

**Purpose to confirm**
- Public rendering logic
- Assumption of `<img>` only

**Run:**
```zsh
sed -n '1,200p' front_v02/src/components/GallerySection.jsx
```

---

### 10. `src/components/ui/ImageUploadField.jsx`

**Purpose to confirm**
- File input accept rules
- Preview logic

**Run:**
```zsh
sed -n '1,200p' front_v02/src/components/ui/ImageUploadField.jsx
```

---

### 11. `src/lib/mediaApi.js`

**Purpose to confirm**
- Upload/list endpoints
- HTTP methods in use

**Run:**
```zsh
sed -n '1,200p' front_v02/src/lib/mediaApi.js
```

---

### 12. `src/lib/mediaResolver.js`

**Purpose to confirm**
- URL resolution
- Type assumptions (image only?)

**Run:**
```zsh
sed -n '1,200p' front_v02/src/lib/mediaResolver.js
```

---

### 13. `src/lib/galleryStore.js`

**Purpose to confirm**
- Data shape sent to GallerySection

**Run:**
```zsh
sed -n '1,200p' front_v02/src/lib/galleryStore.js
```

---

## Phase 1 Completion Criteria ✅

Phase 1 is considered **complete** ONLY when:
- All commands above have been run
- Output has been reviewed
- Media flow is understood end‑to‑end
- Image‑only assumptions are identified

---

## What Happens Next

After you paste the outputs (or confirm okay), I will:
1. Summarize the **actual current media flow**
2. Identify **exact breakpoints** for
   - video support
   - editable media
3. Return **Phase 2 implementation markdown**
4. Begin **safe, targeted terminal‑only modifications**

🚫 No file will be modified before this audit is complete.
