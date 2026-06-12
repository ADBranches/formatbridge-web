# Car Dealership User Stories Implementation Guide — Edwin Section

> Owner: Edwin Kambale  
> Branch: `feature/test-drive-scheduler`  
> Project stack: React + TypeScript + Vite + Tailwind CSS v4, with Node.js/Express support where full-stack functionality is required  
> Package manager for this repo stage: `npm`, because the README instructs `npm i` and `npm run dev`, and local `pnpm` is currently blocked by Corepack issues.  
> Upstream repo: `stevenssebuma/cardealership`  
> Fork repo: `ADBranches/cardealership`

---

## 0. Purpose Of This Guide

This guide describes the development instructions for Edwin's allocated user stories in phase/stage format.

The guide is intentionally aligned to the current repository foundation instead of creating a parallel architecture. The current app entry point is `src/main.tsx`, which renders `src/app/App.tsx`. Existing UI components are under `src/app/components/ui/`. Backend-related files currently exist in both `backend/` and `src/backend/`, so backend additions must be made carefully after confirming the active backend structure.

---

## 1. Assigned User Stories

### User Story A — Interactive Test Drive Scheduler

As a serious car buyer, the user should be able to pick an open calendar date and time through a form on the car details/test-drive area so that the user can reserve a real-world test drive slot.

Acceptance objectives:

- Block historical dates.
- Block invalid test-drive times.
- Show clear visual confirmation after submission.
- Prevent unauthenticated users from submitting.
- Redirect unauthenticated users politely to login.

### User Story B — Admin Dashboard & Operations Control Panel

As a dealership manager, the user should see a private dashboard table showing current listings with Edit and Delete actions so that pricing can be updated or sold cars can be removed.

Acceptance objectives:

- Hide the admin view behind an admin route guard.
- Check admin permissions before showing the dashboard.
- Display current listings in a dashboard table.
- Provide Edit and Delete actions.
- Show a delete confirmation modal before deleting a listing.

---

# Phase 1 — Repository Stabilization And Baseline Verification

## Objective

Confirm the current repository is clean, uses the existing foundation, and runs locally before feature work begins.

## Files/Directories In This Phase

```text
README.md
package.json
package-lock.json
vite.config.ts
postcss.config.mjs
src/main.tsx
src/app/App.tsx
src/styles/index.css
src/styles/tailwind.css
src/app/components/ui/
backend/
src/backend/
```

## Instructions

1. Confirm the feature branch is active.

```bash
git branch
```

Expected active branch:

```text
feature/test-drive-scheduler
```

2. Confirm the accidental `checkout` branch is removed.

```bash
git branch --list
```

Expected branches:

```text
feature/test-drive-scheduler
main
```

3. Confirm working tree is clean.

```bash
git status
```

4. Install dependencies using npm.

```bash
npm i
```

5. Run the frontend.

```bash
npm run dev
```

6. Open the local app.

```text
http://localhost:5173
```

## Done Criteria

- The app loads locally.
- `git status` is clean before feature changes.
- The active branch is `feature/test-drive-scheduler`.
- No new project structure is created outside the current foundation.

---

# Phase 2 — Locate Test Drive Integration Points

## Objective

Identify exactly where the scheduler should be inserted into the current one-page app flow.

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/ui/button.tsx
src/app/components/ui/card.tsx
src/app/components/ui/input.tsx
src/app/components/ui/label.tsx
```

## Instructions

1. Locate vehicle and action button references.

```bash
grep -n "BOOK TEST DRIVE\|VIEW DETAILS\|Calendar\|vehicles\|VehicleCard" src/app/App.tsx
```

2. Use the existing `vehicles` array as the initial data source for the scheduler.

3. Use the existing header button labelled `BOOK TEST DRIVE` as the scroll trigger to the scheduler section.

4. Do not introduce React Router yet unless a real details page or login page exists in the repo.

## Done Criteria

- The `vehicles` array location is known.
- The `BOOK TEST DRIVE` button location is known.
- The scheduler insertion point is chosen inside `src/app/App.tsx`.

---

# Phase 3 — Build Test Drive Scheduler Component

## Objective

Create a focused scheduler component that can be placed into the existing `App.tsx` page without rewriting the whole app.

## Files/Directories In This Phase

```text
src/app/components/test-drive/
src/app/components/test-drive/TestDriveScheduler.tsx
src/app/App.tsx
src/app/components/ui/button.tsx
src/app/components/ui/input.tsx
src/app/components/ui/card.tsx
src/app/components/ui/label.tsx
```

## Instructions

1. Create the feature directory.

```bash
mkdir -p src/app/components/test-drive
```

2. Create the scheduler component.

```text
src/app/components/test-drive/TestDriveScheduler.tsx
```

3. The component should receive vehicle options as props from `App.tsx`.

Expected prop shape:

```ts
type VehicleOption = {
  id: number;
  name: string;
  brand: string;
  year: number;
};
```

4. The component should include these fields:

```text
Vehicle selector
Phone number
Date
Time
Optional notes
Submit button
```

5. The component should define allowed time slots.

```text
09:00
10:00
11:00
12:00
14:00
15:00
16:00
```

6. The component should block historical dates using the date input `min` value.

7. The component should validate empty vehicle, date, time, and phone fields.

8. The component should show success confirmation after valid submission.

## Done Criteria

- `TestDriveScheduler.tsx` exists.
- The scheduler renders vehicle, phone, date, time, notes, and submit fields.
- Past dates are blocked.
- Invalid times are blocked.
- Success confirmation appears after valid submission.

---

# Phase 4 — Integrate Scheduler Into Existing App

## Objective

Mount the scheduler inside the existing page and connect the existing header CTA to the scheduler.

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/test-drive/TestDriveScheduler.tsx
```

## Instructions

1. Import the scheduler in `src/app/App.tsx`.

```ts
import { TestDriveScheduler } from "./components/test-drive/TestDriveScheduler";
```

2. Render the scheduler after the inventory section or before the contact section.

```tsx
<TestDriveScheduler vehicles={vehicles} />
```

3. Ensure the scheduler section has this ID:

```text
test-drive
```

4. Update the existing `BOOK TEST DRIVE` button to scroll smoothly to the scheduler.

```tsx
onClick={() =>
  document.getElementById("test-drive")?.scrollIntoView({ behavior: "smooth" })
}
```

5. Keep the existing visual style and Tailwind classes consistent with the Panda Motors UI.

## Done Criteria

- Clicking `BOOK TEST DRIVE` scrolls to the scheduler.
- Scheduler appears in the existing one-page layout.
- No duplicate app shell is created.
- No unrelated files are modified.

---

# Phase 5 — Add Authentication Gate For Scheduler Submission

## Objective

Prevent unauthenticated users from submitting the scheduler form and redirect users politely to login.

## Files/Directories In This Phase

```text
src/app/components/test-drive/TestDriveScheduler.tsx
src/app/App.tsx
```

## Instructions

1. Add a temporary frontend auth check based on local storage until the team confirms the final auth context.

Accepted temporary token keys:

```text
token
authToken
jwt
```

2. If no token exists, block submission.

3. Show a friendly message:

```text
Please sign in first so we can reserve your test drive securely.
```

4. Redirect unauthenticated users to:

```text
/login?redirect=/test-drive
```

5. Do not call backend booking logic when the user is unauthenticated.

6. Add a `TODO` comment to replace the localStorage check with the team auth provider once available.

## Done Criteria

- Unauthenticated submission is blocked.
- User sees a polite message.
- User is redirected to login.
- No booking payload is submitted without auth.

---

# Phase 6 — Prepare Scheduler API Contract

## Objective

Define the frontend-to-backend contract for test-drive booking without forcing backend implementation before the active backend structure is confirmed.

## Files/Directories In This Phase

```text
src/app/components/test-drive/TestDriveScheduler.tsx
src/app/lib/
src/app/lib/api.ts
backend/
src/backend/
```

## Instructions

1. Create a frontend API helper directory only if one does not already exist.

```bash
mkdir -p src/app/lib
```

2. Create or reserve this helper file:

```text
src/app/lib/api.ts
```

3. Prepare the expected booking payload shape.

```ts
type TestDriveBookingPayload = {
  vehicleId: string;
  vehicleName?: string;
  date: string;
  time: string;
  phone: string;
  notes?: string;
};
```

4. Expected backend endpoint when backend integration begins:

```text
POST /api/test-drives
```

5. Expected headers:

```text
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

6. Keep the first implementation clean by logging or stubbing the payload only if the backend endpoint is not ready.

## Done Criteria

- API payload contract is clear.
- Frontend does not depend on an unconfirmed backend route.
- Scheduler can later be connected to `POST /api/test-drives` with minimal changes.

---

# Phase 7 — Test Scheduler Feature

## Objective

Validate all acceptance criteria for the Interactive Test Drive Scheduler.

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/test-drive/TestDriveScheduler.tsx
src/styles/index.css
src/styles/tailwind.css
```

## Instructions

1. Run the development server.

```bash
npm run dev
```

2. Test the button scroll.

```text
BOOK TEST DRIVE -> Scheduler section
```

3. Test unauthenticated submission.

Expected result:

```text
Submission blocked
Message displayed
Redirect attempted
```

4. Test authenticated submission by temporarily setting a token in browser console.

```js
localStorage.setItem("token", "demo-token");
```

5. Test valid submission.

6. Test invalid submission:

```text
No phone
No time
Past date
```

7. Run production build.

```bash
npm run build
```

## Done Criteria

- Scheduler passes manual tests.
- `npm run build` succeeds.
- No unrelated code changes exist.

---

# Phase 8 — Commit And Push Scheduler PR

## Objective

Submit the first user story as a clean pull request.

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/test-drive/TestDriveScheduler.tsx
package.json
package-lock.json
```

## Instructions

1. Check changed files.

```bash
git status
```

2. Add only relevant files.

```bash
git add src/app/App.tsx src/app/components/test-drive/TestDriveScheduler.tsx
```

3. Commit.

```bash
git commit -m "Add test drive scheduler form"
```

4. Push.

```bash
git push
```

5. Open PR.

```text
base repository: stevenssebuma/cardealership
base branch: main
head repository: ADBranches/cardealership
compare branch: feature/test-drive-scheduler
```

## PR Title

```text
Add Test Drive Scheduler Form
```

## PR Description

```markdown
## What this PR does
- Adds a test drive scheduler section
- Connects the BOOK TEST DRIVE CTA to the scheduler
- Blocks historical dates and invalid times
- Prevents unauthenticated users from submitting
- Shows success confirmation after valid submission

## Assigned user story
Edwin - Interactive Test Drive Scheduler

## Test notes
- npm run dev
- npm run build
```

## Done Criteria

- PR is opened against upstream `main`.
- PR description clearly links to Edwin's assigned user story.
- Scheduler implementation is reviewable as one focused change.

---

# Phase 9 — Admin Dashboard Planning

## Objective

Prepare the second user story without mixing it into the scheduler PR.

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/admin/
src/app/components/admin/AdminDashboard.tsx
src/app/components/admin/AdminListingsTable.tsx
src/app/components/admin/DeleteConfirmModal.tsx
src/app/components/ui/table.tsx
src/app/components/ui/dialog.tsx
src/app/components/ui/button.tsx
src/app/lib/auth.ts
src/app/lib/api.ts
```

## Instructions

1. Start the admin dashboard work only after the scheduler PR is pushed or ready for review.

2. Create a new feature branch from updated `main`.

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
git checkout -b feature/admin-dashboard
```

3. Create the admin components directory.

```bash
mkdir -p src/app/components/admin
```

4. Plan the admin dashboard components:

```text
AdminDashboard.tsx
AdminListingsTable.tsx
DeleteConfirmModal.tsx
```

5. Plan temporary frontend auth helpers:

```text
src/app/lib/auth.ts
```

6. Plan API helper reuse:

```text
src/app/lib/api.ts
```

## Done Criteria

- Admin work is on a separate branch.
- Admin dashboard files are planned separately from scheduler files.
- No scheduler PR scope creep.

---

# Phase 10 — Build Admin Route Guard Or Section Guard

## Objective

Hide admin UI unless the user has admin permissions.

## Files/Directories In This Phase

```text
src/app/lib/auth.ts
src/app/components/admin/AdminDashboard.tsx
src/app/App.tsx
```

## Instructions

1. Create a temporary auth helper if no team auth provider exists.

Expected helper functions:

```text
getAuthToken()
isAuthenticated()
isAdminUser()
```

2. Temporary admin detection can check localStorage until backend auth is finalized.

Accepted temporary keys:

```text
user
role
isAdmin
```

3. Do not expose the admin dashboard by default.

4. If the user is unauthenticated, show login-required messaging.

5. If the user is authenticated but not admin, show unauthorized messaging.

6. Replace temporary logic later when the backend JWT role payload is finalized.

## Done Criteria

- Admin dashboard is not visible to regular users.
- Admin dashboard is visible only when admin permission is detected.
- Guard logic is isolated in `src/app/lib/auth.ts` where possible.

---

# Phase 11 — Build Admin Listings Table

## Objective

Display current vehicle listings with Edit and Delete controls.

## Files/Directories In This Phase

```text
src/app/components/admin/AdminDashboard.tsx
src/app/components/admin/AdminListingsTable.tsx
src/app/components/ui/table.tsx
src/app/components/ui/button.tsx
src/app/App.tsx
src/app/lib/api.ts
```

## Instructions

1. Use the existing `vehicles` array as temporary inventory data if the backend car endpoint is not ready.

2. Expected table columns:

```text
Vehicle
Brand
Year
Price
Condition
Drive
Actions
```

3. Add an Edit button for each row.

4. Add a Delete button for each row.

5. Do not permanently delete from backend until the active backend API is confirmed.

6. Keep table responsive for desktop and usable on smaller screens.

## Done Criteria

- Admin dashboard lists current inventory.
- Every row has Edit and Delete actions.
- Data source can later be swapped from local array to API response.

---

# Phase 12 — Add Delete Confirmation Modal

## Objective

Prevent accidental inventory deletion by requiring confirmation before delete.

## Files/Directories In This Phase

```text
src/app/components/admin/DeleteConfirmModal.tsx
src/app/components/admin/AdminListingsTable.tsx
src/app/components/ui/dialog.tsx
src/app/components/ui/button.tsx
```

## Instructions

1. Create `DeleteConfirmModal.tsx`.

2. Use the existing dialog UI component if available.

3. Modal should show selected vehicle details.

4. Modal actions:

```text
Cancel
Confirm Delete
```

5. Confirm Delete should update UI state first if backend delete endpoint is not ready.

6. Later backend endpoint should be:

```text
DELETE /api/cars/:id
```

7. Delete endpoint should require admin JWT.

## Done Criteria

- Delete button opens confirmation modal.
- Delete does not happen immediately.
- Cancel closes modal without changes.
- Confirm Delete removes item from UI or calls backend when ready.

---

# Phase 13 — Prepare Backend Integration Points

## Objective

Identify backend routes needed by Edwin's frontend work without disrupting teammates' backend ownership.

## Files/Directories In This Phase

```text
backend/server.js
backend/routes/
backend/controllers/
backend/models/
src/backend/server.js
src/docs/swagger.js
src/tests/cars.http
```

## Instructions

1. Confirm with the team which backend folder is active:

```text
backend/
src/backend/
```

2. Do not add duplicate servers.

3. Required backend routes for scheduler/admin integration:

```text
POST /api/test-drives
GET /api/cars
GET /api/cars/:id
PUT /api/cars/:id
DELETE /api/cars/:id
```

4. Required middleware:

```text
requireAuth
requireAdmin
```

5. Required auth behavior:

```text
JWT required for scheduler booking
Admin JWT required for edit/delete inventory actions
```

6. If backend teammates own these endpoints, document the required payloads and wait for integration.

## Done Criteria

- Backend ownership is clear.
- No duplicate backend implementation is added.
- Frontend API contracts are ready.

---

# Phase 14 — Final Admin PR

## Objective

Submit the second user story as a separate focused pull request.

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/admin/AdminDashboard.tsx
src/app/components/admin/AdminListingsTable.tsx
src/app/components/admin/DeleteConfirmModal.tsx
src/app/lib/auth.ts
src/app/lib/api.ts
```

## Instructions

1. Run development server.

```bash
npm run dev
```

2. Run production build.

```bash
npm run build
```

3. Check changed files.

```bash
git status
```

4. Add relevant files.

```bash
git add src/app/App.tsx src/app/components/admin src/app/lib
```

5. Commit.

```bash
git commit -m "Add admin dashboard inventory controls"
```

6. Push.

```bash
git push -u origin feature/admin-dashboard
```

7. Open PR into upstream `main`.

## PR Title

```text
Add Admin Dashboard Inventory Controls
```

## PR Description

```markdown
## What this PR does
- Adds protected admin dashboard area
- Displays vehicle listings in an admin table
- Adds Edit and Delete actions
- Adds delete confirmation modal

## Assigned user story
Edwin - Admin Dashboard & Operations Control Panel

## Test notes
- npm run dev
- npm run build
```

## Done Criteria

- Admin dashboard PR is opened separately from scheduler PR.
- PR targets `stevenssebuma/cardealership:main`.
- Admin story acceptance criteria are covered.

---

# Phase 15 — Final Quality Checklist

## Objective

Confirm both Edwin user stories are complete and cleanly integrated.

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/test-drive/TestDriveScheduler.tsx
src/app/components/admin/AdminDashboard.tsx
src/app/components/admin/AdminListingsTable.tsx
src/app/components/admin/DeleteConfirmModal.tsx
src/app/lib/auth.ts
src/app/lib/api.ts
README.md
```

## Checklist

- [ ] App runs with `npm run dev`.
- [ ] App builds with `npm run build`.
- [ ] Test-drive scheduler is visible in the page.
- [ ] Header `BOOK TEST DRIVE` scrolls to scheduler.
- [ ] Past dates are blocked.
- [ ] Invalid times are blocked.
- [ ] Unauthenticated users cannot submit scheduler.
- [ ] Success confirmation appears after valid scheduler submission.
- [ ] Admin dashboard is hidden from non-admin users.
- [ ] Admin dashboard lists vehicles.
- [ ] Edit and Delete actions are visible.
- [ ] Delete requires confirmation modal.
- [ ] Scheduler PR is separate from Admin PR.
- [ ] PRs target `stevenssebuma/cardealership:main`.

---

# Branching Summary

## Scheduler Branch

```text
feature/test-drive-scheduler
```

Used for:

```text
Interactive Test Drive Scheduler
```

## Admin Branch

```text
feature/admin-dashboard
```

Used for:

```text
Admin Dashboard & Operations Control Panel
```

---

# Recommended Development Order

```text
1. Stabilize repo and run app
2. Build scheduler component
3. Integrate scheduler into App.tsx
4. Add scheduler auth gate
5. Test and PR scheduler
6. Create admin branch
7. Build admin guard
8. Build admin listings table
9. Add delete confirmation modal
10. Test and PR admin dashboard
```

---

# Notes For Team Coordination

- Use npm for now because the current README documents npm usage and npm install works.
- Do not use pnpm until the Corepack/pnpm issue is fixed or the team confirms pnpm as required.
- Do not create Tailwind config files for Tailwind CSS v4 unless advanced customization is needed.
- Do not create a second frontend app structure.
- Do not create a duplicate backend server before confirming whether `backend/` or `src/backend/` is active.
- Keep each user story in its own PR for easier review.
