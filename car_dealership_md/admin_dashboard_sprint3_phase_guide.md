# Admin Dashboard Sprint Implementation Guide

**Project:** Car Dealership Admin Dashboard & Operations Control Panel  
**Branch:** `feature/admin-dashboard`  
**Working repo path:** `/home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership`  
**Guide purpose:** This guide breaks the sprint into clean implementation phases. Each phase lists the files to create/edit, the objective, expected implementation notes, validation commands, and done criteria.

---

## Current Verified Project Status

From the latest inspection:

- Current working directory is the correct project path: `/home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership`.
- Active branch is `feature/admin-dashboard`.
- Branch is up to date with `origin/feature/admin-dashboard`.
- Working tree was clean before the latest repair work.
- Frontend admin files already exist:
  - `src/app/components/admin/AdminDashboard.tsx`
  - `src/app/components/admin/AdminListingsTable.tsx`
  - `src/app/components/admin/DeleteConfirmModal.tsx`
  - `src/app/components/admin/AddNewCarForm.tsx`
  - `src/app/components/admin/EditVehicleModal.tsx`
  - `src/app/components/admin/README.md`
- Frontend helper files already exist:
  - `src/app/lib/api.ts`
  - `src/app/lib/auth.ts`
  - `src/app/lib/adminInventory.ts`
- Backend already exists in this same repo:
  - `backend/server.js`
  - `backend/routes/carsRoutes.js`
  - `backend/controllers/carsController.js`
  - `backend/models/carsModel.js`
  - `backend/middleware/authMiddleware.js`

---

## Global Rules For This Sprint

1. **Use terminal commands only.**
2. **Always `cd` into the project path before commands:**

   ```bash
   cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
   ```

3. **Inspect files before editing if the file already exists.**
4. **Avoid heredoc commands** like `cat <<EOF`; use safer file writing methods.
5. **Do not expose admin dashboard publicly by default.**
6. **Backend destructive actions must stay protected by admin JWT middleware.**
7. **Frontend delete should update UI state first until backend endpoint behavior is confirmed.**
8. **After each phase, run a targeted build/test before moving forward.**
9. **Restore generated `dist` files after build unless we intentionally commit production assets:**

   ```bash
   git restore dist
   ```

---

# Phase 9 — Admin Dashboard Planning Stub

## Objective
Create the initial admin dashboard folder and planning stub files without affecting the customer marketplace or test-drive scheduler work.

## Files/Directories In This Phase

### Create/Edit

- `src/app/components/admin/README.md`
- `src/app/components/admin/AdminDashboard.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `src/app/components/admin/DeleteConfirmModal.tsx`
- `src/app/lib/auth.ts`

## Implementation Notes

- Create the `admin` component directory.
- Add a README describing admin dashboard planning.
- Add placeholder components:
  - `AdminDashboard`
  - `AdminListingsTable`
  - `DeleteConfirmModal`
- Add temporary `auth.ts` helper file for upcoming guard logic.
- Do not connect the admin dashboard to the main app yet unless intentionally testing.

## Validation Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
ls src/app/components/admin
ls src/app/lib
npm run build
git restore dist
```

## Done Criteria

- Admin directory exists.
- Planning README exists.
- Placeholder admin components exist.
- Temporary auth helper exists.
- Build passes.
- Customer marketplace is unchanged.

---

# Phase 10 — Build Admin Route Guard Or Section Guard

## Objective
Hide admin UI unless the user has admin permissions.

## Files/Directories In This Phase

### Edit

- `src/app/lib/auth.ts`
- `src/app/components/admin/AdminDashboard.tsx`
- `src/app/App.tsx`

## Expected Helper Functions

`src/app/lib/auth.ts` should expose:

```ts
getAuthToken()
isAuthenticated()
isAdminUser()
```

## Temporary Auth Detection Rules

Until backend JWT role payload is finalized, temporary admin detection may check `localStorage` keys:

- `user`
- `role`
- `isAdmin`

Valid temporary admin checks:

- `localStorage.setItem("role", "admin")`
- `localStorage.setItem("isAdmin", "true")`
- `localStorage.setItem("user", JSON.stringify({ role: "admin" }))`
- `localStorage.setItem("user", JSON.stringify({ isAdmin: true }))`

## Implementation Notes

- `AdminDashboard.tsx` should show:
  - `LOGIN REQUIRED` if unauthenticated.
  - `UNAUTHORIZED` if authenticated but not admin.
  - `INVENTORY CONTROL PANEL` only if admin.
- `App.tsx` should mount admin only on a temporary admin-only route, for example `/admin`.
- Do not add a public navigation link to `/admin` yet.

## Browser Test

Open:

```text
http://localhost:5173/admin
```

Unauthenticated:

```js
localStorage.clear()
location.reload()
```

Expected:

```text
LOGIN REQUIRED
```

Authenticated but not admin:

```js
localStorage.clear()
localStorage.setItem("role", "user")
location.reload()
```

Expected:

```text
UNAUTHORIZED
```

Admin:

```js
localStorage.clear()
localStorage.setItem("role", "admin")
location.reload()
```

Expected:

```text
INVENTORY CONTROL PANEL
```

## Validation Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
grep -n "AdminDashboard\|/admin" src/app/App.tsx
grep -R "&lt;\|&gt;\|&amp;" src/app/components/admin src/app/lib || true
npm run build
git restore dist
```

## Done Criteria

- Admin dashboard is not visible to regular users.
- Admin dashboard is visible only when admin permission is detected.
- Guard logic is isolated in `src/app/lib/auth.ts` where possible.
- Temporary `/admin` route works.
- Build passes.

---

# Phase 11 — Build Admin Listings Table

## Objective
Display current vehicle listings with Edit and Delete controls.

## Files/Directories In This Phase

### Edit/Create

- `src/app/components/admin/AdminDashboard.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `src/app/components/ui/table.tsx`
- `src/app/components/ui/button.tsx`
- `src/app/App.tsx`
- `src/app/lib/api.ts`
- `src/app/lib/adminInventory.ts`

## Expected Table Columns

- Vehicle
- Brand
- Year
- Price
- Condition
- Drive
- Actions

Optional useful column:

- Status

## Implementation Notes

- Use existing local vehicle array as temporary inventory data if backend car endpoint is not ready.
- Keep source data isolated in a helper file such as:
  - `src/app/lib/api.ts`, or
  - `src/app/lib/adminInventory.ts`
- Add an **Edit** button for every row.
- Add a **Delete** button for every row.
- Do not permanently delete from backend yet.
- Keep the table responsive using horizontal overflow on small screens.

## Validation Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
sed -n '1,220p' src/app/components/admin/AdminListingsTable.tsx
sed -n '1,220p' src/app/components/admin/AdminDashboard.tsx
npm run build
git restore dist
```

## Browser Test

```js
localStorage.clear()
localStorage.setItem("role", "admin")
location.reload()
```

Expected on `/admin`:

- Admin inventory heading appears.
- Vehicle rows appear.
- Each row has **Edit** and **Delete** actions.

## Done Criteria

- Admin dashboard lists current inventory.
- Every row has Edit and Delete actions.
- Data source can later be swapped from local array to API response.
- Build passes.

---

# Phase 12 — Add Delete Confirmation Modal

## Objective
Prevent accidental inventory deletion by requiring confirmation before delete.

## Files/Directories In This Phase

### Edit/Create

- `src/app/components/admin/DeleteConfirmModal.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `src/app/components/ui/dialog.tsx`
- `src/app/components/ui/button.tsx`

## Implementation Notes

- Use existing dialog UI component if available.
- Modal should show selected vehicle details:
  - Vehicle name/model
  - Brand
  - Year
  - Price
  - Condition
  - Drive
- Modal actions:
  - Cancel
  - Confirm Delete
- Clicking Delete should only open the modal.
- Cancel should close the modal without changing table data.
- Confirm Delete should remove the item from frontend UI state for now.
- Add a TODO comment for later backend integration:

```text
DELETE /api/cars/:id
```

## Important Backend Rule

Do not wire permanent backend delete until the active backend API and admin JWT role checking are confirmed.

Later backend endpoint should be:

```http
DELETE /api/cars/:id
```

The endpoint must require admin JWT.

## Validation Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
sed -n '1,220p' src/app/components/admin/DeleteConfirmModal.tsx
sed -n '1,260p' src/app/components/admin/AdminListingsTable.tsx
sed -n '1,220p' src/app/components/ui/dialog.tsx
grep -R "&lt;\|&gt;\|&amp;" src/app/components/admin src/app/components/ui/dialog.tsx src/app/lib || true
npm run build
git restore dist
```

## Browser Test

On `/admin` with admin mode active:

```js
localStorage.clear()
localStorage.setItem("role", "admin")
location.reload()
```

Manual checks:

1. Click **Delete** on a row.
2. Confirmation modal opens.
3. Modal displays the selected vehicle details.
4. Click **Cancel**.
5. Row remains in the table.
6. Click **Delete** again.
7. Click **Confirm Delete**.
8. Row disappears from UI state.
9. Refresh browser.
10. Row returns because backend delete is not connected yet.

## Done Criteria

- Delete button opens confirmation modal.
- Delete does not happen immediately.
- Cancel closes modal without changes.
- Confirm Delete removes item from UI state or calls backend only when backend is ready.
- Build passes.

---

# Phase 13 — Add Edit Vehicle Modal

## Objective
Allow admin users to edit selected vehicle details in UI state first, without backend update until endpoint behavior is confirmed.

## Files/Directories In This Phase

### Edit/Create

- `src/app/components/admin/EditVehicleModal.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `src/app/components/ui/dialog.tsx`
- `src/app/components/ui/button.tsx`
- `src/app/components/ui/input.tsx`
- `src/app/components/ui/select.tsx`
- `src/app/lib/adminInventory.ts`

## Expected Editable Fields

Minimum:

- Price
- Condition
- Status

Optional later:

- Vehicle name
- Brand
- Year
- Image URL
- Specs

## Implementation Notes

- Clicking Edit opens modal.
- Modal shows selected vehicle details.
- Save updates UI state only.
- Add TODO comment for later backend endpoint:

```http
PUT /api/cars/:id
```

- Do not call backend until backend contract is finalized.

## Validation Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
sed -n '1,260p' src/app/components/admin/EditVehicleModal.tsx
sed -n '1,320p' src/app/components/admin/AdminListingsTable.tsx
npm run build
git restore dist
```

## Done Criteria

- Edit opens modal.
- Cancel closes without changes.
- Save updates UI state.
- Backend update is not called yet unless confirmed.
- Build passes.

---

# Phase 14 — Add New Car Form

## Objective
Allow admin users to add a new vehicle listing to temporary UI state.

## Files/Directories In This Phase

### Edit/Create

- `src/app/components/admin/AddNewCarForm.tsx`
- `src/app/components/admin/AdminDashboard.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `src/app/components/ui/dialog.tsx`
- `src/app/components/ui/button.tsx`
- `src/app/components/ui/input.tsx`
- `src/app/components/ui/select.tsx`
- `src/app/lib/adminInventory.ts`

## Expected Fields

Minimum:

- Vehicle name
- Brand
- Type/category
- Year
- Price
- Condition
- Drive

Optional:

- Image URL
- Engine
- Power
- Status

## Implementation Notes

- Add **Add New Vehicle** button in admin dashboard.
- Opening the form should not affect current table until Save is clicked.
- Save adds new vehicle to UI state.
- Add TODO comment for later backend endpoint:

```http
POST /api/cars
```

- Backend creation must eventually require admin JWT.

## Validation Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
sed -n '1,280p' src/app/components/admin/AddNewCarForm.tsx
sed -n '1,280p' src/app/components/admin/AdminDashboard.tsx
npm run build
git restore dist
```

## Done Criteria

- Add New Vehicle button exists.
- Form opens.
- Cancel closes without adding data.
- Save adds a new row to UI state.
- Build passes.

---

# Phase 15 — Backend Cars API Inspection And Contract Alignment

## Objective
Confirm existing backend API route names, controller behavior, model shape, and auth middleware before wiring frontend actions to backend.

## Files/Directories In This Phase

### Inspect/Edit If Needed

- `backend/server.js`
- `backend/routes/carsRoutes.js`
- `backend/controllers/carsController.js`
- `backend/models/carsModel.js`
- `backend/middleware/authMiddleware.js`
- `backend/utils/jwt.js`
- `backend/package.json`
- `src/tests/cars.http`
- `src/docs/swagger.js`

## Inspection Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
sed -n '1,260p' backend/server.js
sed -n '1,260p' backend/routes/carsRoutes.js
sed -n '1,320p' backend/controllers/carsController.js
sed -n '1,260p' backend/models/carsModel.js
sed -n '1,260p' backend/middleware/authMiddleware.js
cat backend/package.json
```

## Expected Backend Endpoints

Target final contract:

```http
GET /api/cars
GET /api/cars/:id
POST /api/cars
PUT /api/cars/:id
DELETE /api/cars/:id
```

Admin-only endpoints:

```http
POST /api/cars
PUT /api/cars/:id
DELETE /api/cars/:id
```

## Done Criteria

- Existing backend route paths are confirmed.
- Existing controller names are confirmed.
- Existing model fields are confirmed.
- Auth middleware behavior is confirmed.
- Admin-only route strategy is confirmed before frontend integration.

---

# Phase 16 — Wire Frontend Inventory Read To Backend

## Objective
Load admin inventory table from backend `GET /api/cars` if available, with local fallback if backend is unavailable.

## Files/Directories In This Phase

### Edit

- `src/app/lib/api.ts`
- `src/app/lib/adminInventory.ts`
- `src/app/components/admin/AdminDashboard.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `backend/routes/carsRoutes.js`
- `backend/controllers/carsController.js`

## Implementation Notes

- Create `getCars()` helper in frontend API layer.
- Use backend response first.
- Keep local array fallback for development resilience.
- Show loading state.
- Show error state if backend fails and fallback is unavailable.

## Done Criteria

- Admin table can render backend vehicles.
- Loading state works.
- Error state works.
- Local fallback remains available until backend is stable.
- Build passes.

---

# Phase 17 — Wire Create And Edit To Backend

## Objective
Connect Add and Edit actions to protected backend endpoints after backend auth contract is confirmed.

## Files/Directories In This Phase

### Edit

- `src/app/lib/api.ts`
- `src/app/lib/auth.ts`
- `src/app/components/admin/AddNewCarForm.tsx`
- `src/app/components/admin/EditVehicleModal.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `backend/routes/carsRoutes.js`
- `backend/controllers/carsController.js`
- `backend/middleware/authMiddleware.js`

## Target Endpoints

```http
POST /api/cars
PUT /api/cars/:id
```

## Implementation Notes

- Send admin JWT in request headers.
- Keep optimistic UI update only if request succeeds or is intentionally optimistic with rollback.
- Show user-friendly error if backend rejects request.
- Do not hide backend failures silently.

## Done Criteria

- Add New Vehicle calls backend when admin JWT exists.
- Edit Vehicle calls backend when admin JWT exists.
- Unauthorized users cannot create/edit cars.
- UI handles success and failure.
- Build passes.

---

# Phase 18 — Wire Delete To Backend

## Objective
Connect confirmed delete action to protected backend delete endpoint.

## Files/Directories In This Phase

### Edit

- `src/app/lib/api.ts`
- `src/app/lib/auth.ts`
- `src/app/components/admin/DeleteConfirmModal.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `backend/routes/carsRoutes.js`
- `backend/controllers/carsController.js`
- `backend/middleware/authMiddleware.js`

## Target Endpoint

```http
DELETE /api/cars/:id
```

## Implementation Notes

- Delete must remain confirmation-based.
- Send admin JWT.
- Remove row from UI only after backend success, or use optimistic update with rollback.
- Show error message if delete fails.

## Done Criteria

- Delete requires modal confirmation.
- Delete calls backend endpoint.
- Non-admin user cannot delete.
- UI updates correctly after backend success.
- Build passes.

---

# Phase 19 — Final QA, Cleanup, And Sprint Documentation

## Objective
Clean final implementation, verify no broken files, run targeted tests, and prepare final sprint summary.

## Files/Directories In This Phase

### Inspect/Edit

- `src/app/components/admin/*`
- `src/app/lib/*`
- `src/app/App.tsx`
- `backend/routes/*`
- `backend/controllers/*`
- `backend/middleware/*`
- `src/tests/cars.http`
- `src/docs/swagger.js`
- `README.md`
- `src/app/components/admin/README.md`

## Final Validation Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
git status
grep -R "&lt;\|&gt;\|&amp;" src/app/components/admin src/app/lib src/app/components/ui/dialog.tsx || true
npm run build
git restore dist
```

Backend validation if backend scripts are configured:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership/backend
npm test
```

If no backend test script exists:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership/backend
npm run dev
```

Then manually test API routes using `src/tests/cars.http` or curl.

## Git Review Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
git status
git diff -- src/app/components/admin src/app/lib src/app/App.tsx backend src/tests src/docs README.md
```

## Done Criteria

- Full frontend build passes.
- Admin UI works in browser.
- Admin guard works.
- Inventory table works.
- Edit, Add, and Delete flows work according to current backend readiness.
- Backend route contract is documented.
- No accidental scheduler changes are included unless intended.
- Final sprint summary is ready.

---

# Recommended Phase Order From Here

Based on current progress, continue in this order:

1. **Repair malformed frontend admin files** if build fails.
2. **Complete Phase 12** delete confirmation modal.
3. **Complete Phase 13** edit modal.
4. **Complete Phase 14** add new car form.
5. **Inspect backend contract in Phase 15.**
6. **Wire backend read in Phase 16.**
7. **Wire backend create/edit in Phase 17.**
8. **Wire backend delete in Phase 18.**
9. **Complete final QA in Phase 19.**

---

# Quick Phase Completion Template

Use this after every phase:

```md
## Phase X Completion Notes

### Files Created
- 

### Files Edited
- 

### Commands Run
```bash

```

### Result
- Build: Passed / Failed
- Browser test: Passed / Failed
- Backend test: Passed / Failed / Not applicable

### Notes
- 

### Next Phase
- Phase X+1 — 
```

---

# Immediate Next Step

Continue with **Phase 12 — Add Delete Confirmation Modal**.

Before editing, inspect the target files:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
sed -n '1,260p' src/app/components/admin/AdminListingsTable.tsx
sed -n '1,220p' src/app/components/admin/DeleteConfirmModal.tsx
sed -n '1,220p' src/app/components/ui/dialog.tsx
```

Then patch only those files needed for Phase 12.
