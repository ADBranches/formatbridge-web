# CMS Gallery Media & Video Support – Implementation Timeline

> **Project:** construction_co
> **Branch:** `cms-media-video-edit-phase1`
> **Goal:** Enable full admin CMS control over gallery media (edit/update anytime) and support multi-format video uploads and rendering alongside images.

This guide is a **phase-by-phase, actionable timeline** designed specifically for your current project structure. Each phase lists:
- Objectives
- Exact files to modify
- What success looks like before moving on

---

## Phase 0 – Baseline & Contract Alignment (Foundation)

### Objectives
- Establish a **single, explicit media contract** shared by backend and frontend.
- Confirm supported media types and storage strategy.

### Decisions (to lock in)
- **Storage:** All media (images + videos) live under `backend/app/static/uploads/services/`
- **Media types:** `IMAGE`, `VIDEO` (uppercase, stored in DB)
- **Supported formats:**
  - Images: `jpg`, `jpeg`, `png`, `webp`
  - Videos: `mp4`, `webm`, `mov`

### Files to review / confirm
- `backend/app/models/media.py`
- `backend/app/api_flask/uploads.py`
- `front_v02/src/lib/mediaApi.js`

### Exit criteria
- Backend consistently stores `media_type`.
- Frontend receives `media_type` for every gallery item.

---

## Phase 1 – Backend: Media Model & Upload Support ✅ (mostly done)

### Objectives
- Ensure backend can **detect, store, and expose** media type.
- Allow future edits via API (PATCH).

### Files
- ✅ `backend/app/models/media.py`
- ✅ `backend/app/schemas/media.py`
- ✅ `backend/app/api_flask/uploads.py`
- ✅ `backend/app/api_flask/media.py`

### Key changes
- Media type detection from file extension
- Unified upload helper for images & videos
- New admin update endpoint:
  ```http
  PATCH /api/v1/admin/media/{media_id}
  ```

### Exit criteria
- Uploading a video returns `{ url, media_type: "VIDEO" }`.
- Admin can PATCH media metadata without reuploading.

---

## Phase 2 – Frontend Data Layer: Media Awareness ✅ (mostly done)

### Objectives
- Frontend stores and propagates `mediaType` everywhere.

### Files
- ✅ `front_v02/src/lib/mediaApi.js`
- ✅ `front_v02/src/lib/galleryStore.js`
- ✅ `front_v02/src/lib/mediaResolver.js`

### Key changes
- Upload functions accept optional `mediaType`.
- Gallery items include:
  ```js
  {
    url,
    image,
    mediaType, // IMAGE | VIDEO
  }
  ```

### Exit criteria
- AdminGallery and public GallerySection receive `mediaType` reliably.

---

## Phase 3 – Frontend Public Gallery: Image + Video Rendering

### Objectives
- Render **videos and images** correctly in the public gallery.
- Zero regressions for existing image content.

### File (primary)
- `front_v02/src/components/GallerySection.jsx`

### Required changes
1. Normalize media attributes:
   ```js
   const src = resolveImage(item.image || item.url);
   const mediaType = (item.mediaType || item.media_type || "IMAGE")
     .toString()
     .toUpperCase();
   const isVideo = mediaType === "VIDEO";
   ```

2. Replace image-only rendering with conditional media rendering:
   ```jsx
   {isVideo ? (
     <video
       src={src}
       className="h-full w-full object-cover"
       controls
       preload="metadata"
     />
   ) : (
     <motion.img ... />
   )}
   ```

### Exit criteria
- Images still render normally.
- Videos load, show controls, and do not break layout.

---

## Phase 4 – Admin CMS: Media Editing (Core CMS Upgrade)

### Objectives
- Admins can **edit uploaded media at any time**.
- No reupload required for title/description/category changes.

### Backend files
- `backend/app/api_flask/media.py`

### Frontend files
- `front_v02/src/pages/admin/AdminGallery.jsx`
- (optional) `front_v02/src/components/ui/Modal.jsx`

### Admin features to add
- Edit title
- Edit description
- Change category (service)
- Toggle featured status
- Update sort order

### UX recommendation
- **Modal-based edit form** per media card
- Uses existing:
  ```http
  PATCH /api/v1/admin/media/{media_id}
  ```

### Exit criteria
- Admin edits persist after refresh.
- No new uploads required for metadata changes.

---

## Phase 5 – Admin CMS: Video-Aware Upload UI

### Objectives
- Admin can upload **images OR videos** intentionally.
- Correct previews shown before upload.

### Frontend file
- `front_v02/src/pages/admin/AdminGallery.jsx`

### Required UI upgrades
- File input accepts:
  ```html
  accept="image/*,video/*"
  ```
- Detect file type on selection:
  ```js
  const isVideo = file.type.startsWith("video/");
  ```
- Send `media_type` on upload
- Video preview uses `<video>` instead of `<img>`

### Exit criteria
- Admin can upload mp4/webm successfully.
- Preview matches file type.

---

## Phase 6 – Public & Admin Parity Polish

### Objectives
- Consistent media handling everywhere.

### Optional enhancements
- Poster thumbnails for videos
- Aspect-ratio wrapper for mixed media
- Lazy loading

### Files
- `front_v02/src/components/GallerySection.jsx`
- `front_v02/src/pages/admin/AdminGallery.jsx`

---

## Phase 7 – QA, Migration & Cleanup

### Objectives
- Harden system before merging.

### Checklist
- ✅ Existing images unaffected
- ✅ Videos stream correctly in production
- ✅ No broken media URLs
- ✅ DB rows valid for old records (default `IMAGE`)

### Suggested tests
- Upload image
- Upload video
- Edit media metadata
- Delete media

---

## Final Notes

- **Avoid script-based JSX patching** going forward
- Prefer direct component edits for UI logic
- Backend is now flexible enough for future media types
