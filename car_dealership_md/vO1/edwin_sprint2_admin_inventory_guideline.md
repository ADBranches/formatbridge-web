# Edwin Sprint 2 Implementation Guideline — Admin Inventory Management Forms

> Project: Car Dealership  
> Assigned Developer: Edwin  
> Role: Frontend Dev #2 — Admin Inventory Management Forms  
> Source assignment: Sprint 2 brief from `Car_dealership_2.pdf`  
> Working rule: Inspect existing files before modifying them. Create new files only when the implementation phase explicitly requires them.

---

## 1. Edwin's Assigned Sprint 2 Modules

Edwin's Sprint 2 frontend responsibilities are focused on private admin inventory management.

### Module A — Multistep "Add New Car" Form Layout

**Goal:** Create the interface admins use to list new vehicles.

Required fields:

- Make
- Model
- Price
- Year
- Mileage
- Pictures/file input

Required behavior:

- Prevent submission when required fields are blank.
- Show strict, user-friendly frontend error messages.
- Prepare the form for future backend integration with image upload and inventory creation endpoints.

### Module B — Interactive Admin Listings Table

**Goal:** Allow admins to manage active vehicle cards/listings.

Required behavior:

- Build a dashboard table/grid for active listings.
- Use Ronald's paginated API when available.
- Each row/listing should show a visible status badge, such as:
  - Available
  - Pending Test Drive
  - Sold
- Each row should include action triggers for:
  - Edit tools
  - Delete confirmation modal

---

## 2. Implementation Principles

Before implementing each phase:

1. Confirm the active branch.
2. Confirm the working tree is clean.
3. Inspect the current file structure.
4. Inspect existing component patterns before creating new ones.
5. Reuse existing UI components where possible.
6. Avoid backend duplication until backend ownership and endpoints are confirmed.
7. Keep admin work separated from public marketplace/test-drive work.

Recommended branch for Sprint 2 Edwin work:

```bash
feature/admin-inventory-management
```

If continuing from the existing admin branch:

```bash
feature/admin-dashboard
```

---

# Phase 0 — Pre-Implementation Inspection

## Objective

Inspect the current frontend/admin structure before changing files.

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/admin/
src/app/components/ui/
src/app/lib/
src/styles/
package.json
README.md
```

## Terminal Inspection Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
git status
git branch
find src/app -maxdepth 4 -type f | sort
find src/app/components/admin -maxdepth 3 -type f | sort
find src/app/components/ui -maxdepth 2 -type f | sort
ls src/app/lib
```

## Done Criteria

- Active branch is confirmed.
- Working tree is clean.
- Existing admin and UI component files are known.
- No files have been modified yet.

---

# Phase 1 — Admin Inventory Data Contract Planning

## Objective

Define the frontend shape for vehicle/admin listing data before building forms and tables.

## Files/Directories In This Phase

```text
src/app/components/admin/
src/app/lib/
src/app/lib/adminInventory.ts
```

## Planned File

```text
src/app/lib/adminInventory.ts
```

## Responsibilities

Define shared frontend types for:

- Vehicle listing
- Vehicle status
- Add-new-car form payload
- Edit vehicle payload

## Suggested Type Shape

```ts
export type VehicleStatus = "Available" | "Pending Test Drive" | "Sold";

export type AdminVehicle = {
  id: number | string;
  make?: string;
  model?: string;
  name?: string;
  brand?: string;
  year: number;
  price: number;
  mileage?: number;
  status: VehicleStatus;
  condition?: string;
  image?: string;
  specs?: {
    power?: string;
    engine?: string;
    drive?: string;
  };
};

export type AddCarFormValues = {
  make: string;
  model: string;
  price: string;
  year: string;
  mileage: string;
  imageFile: File | null;
};
```

## Done Criteria

- Shared inventory types are planned or created.
- Add-car form and admin table can rely on consistent data shape.
- Future backend API integration is easier.

---

# Phase 2 — Multistep Add New Car Form Structure

## Objective

Create the admin form shell for adding vehicles without connecting backend submission yet.

## Files/Directories In This Phase

```text
src/app/components/admin/AddNewCarForm.tsx
src/app/components/admin/
src/app/components/ui/button.tsx
src/app/components/ui/input.tsx
src/app/components/ui/label.tsx
src/app/components/ui/card.tsx
src/app/components/ui/tabs.tsx
```

## Planned File

```text
src/app/components/admin/AddNewCarForm.tsx
```

## Form Steps

### Step 1 — Basic Vehicle Identity

Fields:

- Make
- Model
- Year

### Step 2 — Pricing And Usage

Fields:

- Price
- Mileage

### Step 3 — Image Upload

Fields:

- File input for pictures

### Step 4 — Review And Submit

Displays entered values before submit.

## Validation Rules

- Make is required.
- Model is required.
- Price is required and must be greater than zero.
- Year is required and must be a valid year.
- Mileage is required and cannot be negative.
- Image file is required if the team requires pictures before listing.
- Image file validation should later align with Ronald's upload requirements.

## Done Criteria

- `AddNewCarForm.tsx` exists.
- Form has clear steps.
- Required fields are visible.
- Form prevents blank submissions.
- User-friendly error messages display per field.
- No backend submission is required yet.

---

# Phase 3 — Add New Car Form Validation Logic

## Objective

Implement strict frontend validation for the Add New Car form.

## Files/Directories In This Phase

```text
src/app/components/admin/AddNewCarForm.tsx
src/app/lib/adminInventory.ts
```

## Validation Behaviors

- Validate current step before moving forward.
- Validate all fields before final submission.
- Show clear error messages.
- Keep user input in state between steps.
- Prevent submit if any required field is invalid.

## Example Error Messages

```text
Make is required.
Model is required.
Price must be greater than zero.
Year must be valid.
Mileage cannot be negative.
Please select at least one vehicle image.
```

## Done Criteria

- Invalid form cannot proceed silently.
- Blank required fields show errors.
- Final submit is blocked if invalid.
- Validation is clear and user-friendly.

---

# Phase 4 — Add New Car Form Image Input Preparation

## Objective

Prepare the file input for future cloud image upload integration.

## Files/Directories In This Phase

```text
src/app/components/admin/AddNewCarForm.tsx
src/app/lib/adminInventory.ts
```

## Expected Future Backend Endpoint

```text
POST /api/cars/upload
```

## Future Backend Requirements From Ronald's Assignment

- Accept multipart form data.
- Validate image file type.
- Validate image size under 5MB.
- Return secure public image URL.

## Frontend Preparation

- Use file input.
- Accept image types only.
- Show selected file name.
- Optionally preview selected image.
- Validate size under 5MB on frontend as a user-friendly early check.

## Done Criteria

- File input exists.
- Image-only selection is encouraged via `accept="image/*"`.
- File name or preview displays after selection.
- Oversized files can show frontend validation warning.
- Upload is not connected until backend endpoint is confirmed.

---

# Phase 5 — Integrate Add New Car Form Into Admin Dashboard

## Objective

Place the Add New Car form inside the admin dashboard without disrupting the existing listings table.

## Files/Directories In This Phase

```text
src/app/components/admin/AdminDashboard.tsx
src/app/components/admin/AddNewCarForm.tsx
src/app/components/admin/AdminListingsTable.tsx
```

## UI Placement Options

Recommended layout:

```text
Admin Dashboard Header
Add New Car Form Section
Inventory Listings Table Section
```

Alternative layout:

```text
Tabs:
- Add Vehicle
- Manage Inventory
```

## Done Criteria

- Admin users can access the Add New Car form.
- Non-admin users cannot access it.
- Existing table remains functional.
- No public/customer page is affected.

---

# Phase 6 — Interactive Admin Listings Table Status Badges

## Objective

Enhance the admin listings table with visible status badges.

## Files/Directories In This Phase

```text
src/app/components/admin/AdminListingsTable.tsx
src/app/components/ui/badge.tsx
src/app/lib/adminInventory.ts
```

## Status Badge Values

```text
Available
Pending Test Drive
Sold
```

## Badge Behavior

- Available: positive/active visual style.
- Pending Test Drive: warning/in-progress visual style.
- Sold: muted/closed visual style.

## Done Criteria

- Each row has a visible Status column or badge.
- Badge value is easy to scan.
- Status display is consistent across rows.

---

# Phase 7 — Admin Listings Table Pagination Contract

## Objective

Prepare the admin table to consume Ronald's paginated API once available.

## Files/Directories In This Phase

```text
src/app/components/admin/AdminListingsTable.tsx
src/app/lib/adminInventory.ts
src/app/lib/api.ts
```

## Expected Future API

```text
GET /api/cars?page=1&limit=12
```

## Frontend Preparation

- Track current page.
- Track page size/limit.
- Prepare loading state.
- Prepare empty state.
- Prepare error state.
- Keep current local data fallback until API is ready.

## Done Criteria

- Table can later switch from local vehicles to paginated API data.
- Pagination UI is planned or scaffolded.
- No hard dependency on unavailable backend endpoint.

---

# Phase 8 — Edit Vehicle Flow Refinement

## Objective

Ensure edit tools allow admins to update active listing fields at UI level.

## Files/Directories In This Phase

```text
src/app/components/admin/EditVehicleModal.tsx
src/app/components/admin/AdminListingsTable.tsx
src/app/components/ui/dialog.tsx
src/app/components/ui/input.tsx
src/app/components/ui/button.tsx
src/app/components/ui/label.tsx
```

## Current Edit Scope

Editable fields:

- Price
- Condition/status where applicable

## Future Backend Endpoint

```text
PUT /api/cars/:id
Authorization: Bearer <ADMIN_JWT_TOKEN>
```

## Done Criteria

- Edit button opens modal.
- Selected vehicle details are shown.
- Admin can update price.
- Admin can update condition/status.
- Invalid input is blocked.
- Save updates UI state.
- Backend persistence is clearly marked as future work.

---

# Phase 9 — Delete Confirmation Modal Refinement

## Objective

Ensure delete action is safe and cannot happen accidentally.

## Files/Directories In This Phase

```text
src/app/components/admin/DeleteConfirmModal.tsx
src/app/components/admin/AdminListingsTable.tsx
src/app/components/ui/dialog.tsx
src/app/components/ui/button.tsx
```

## Required Modal Actions

```text
Cancel
Confirm Delete
```

## Future Backend Endpoint

```text
DELETE /api/cars/:id
Authorization: Bearer <ADMIN_JWT_TOKEN>
```

## Done Criteria

- Delete button opens modal.
- Modal shows selected vehicle details.
- Cancel closes modal without deleting.
- Confirm Delete removes vehicle from UI state.
- Backend persistence is clearly marked as future work.

---

# Phase 10 — Admin Access Guard Validation

## Objective

Confirm admin inventory management tools are protected from unauthorized users.

## Files/Directories In This Phase

```text
src/app/lib/auth.ts
src/app/components/admin/AdminDashboard.tsx
src/app/App.tsx
```

## Temporary Auth Keys

```text
token
authToken
jwt
role
isAdmin
user
```

## Expected Behaviors

### Unauthenticated

- Admin dashboard is hidden.
- User sees sign-in guidance.

### Authenticated Non-Admin

- Admin tools are hidden.
- User sees admin permission needed message.

### Authenticated Admin

- Admin dashboard is visible.
- Add New Car form is visible.
- Inventory table is visible.

## Done Criteria

- Admin UI is hidden from unauthenticated users.
- Admin UI is hidden from regular users.
- Admin UI is visible only to admin users.
- Auth helpers remain isolated in `src/app/lib/auth.ts`.

---

# Phase 11 — Backend Integration Readiness Check

## Objective

Identify needed backend integration points without implementing duplicate backend work.

## Files/Directories In This Phase

```text
backend/
src/backend/
src/tests/cars.http
src/docs/swagger.js
src/app/lib/api.ts
```

## Required Backend Endpoints

```text
POST /api/cars/upload
GET /api/cars?page=1&limit=12
POST /api/cars
PUT /api/cars/:id
DELETE /api/cars/:id
```

## Required Middleware

```text
requireAuth
requireAdmin
```

## Done Criteria

- Active backend folder is confirmed by team.
- No duplicate backend server is added.
- Required endpoints are identified.
- Frontend remains ready for integration.

---

# Phase 12 — Final PR Readiness Checklist

## Objective

Confirm Edwin's Sprint 2 admin inventory management work is ready for review.

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/admin/AdminDashboard.tsx
src/app/components/admin/AdminListingsTable.tsx
src/app/components/admin/DeleteConfirmModal.tsx
src/app/components/admin/EditVehicleModal.tsx
src/app/components/admin/AddNewCarForm.tsx
src/app/lib/auth.ts
src/app/lib/adminInventory.ts
README.md
```

## Checklist

- [ ] App runs with `npm run dev`.
- [ ] App builds with `npm run build`.
- [ ] Admin dashboard is hidden from unauthenticated users.
- [ ] Admin dashboard is hidden from non-admin users.
- [ ] Admin dashboard is visible to admin users.
- [ ] Add New Car form exists.
- [ ] Add New Car form validates blank fields.
- [ ] Add New Car form includes Make, Model, Price, Year, Mileage, and picture input.
- [ ] Listings table displays active vehicles.
- [ ] Listings table includes status badges.
- [ ] Edit action opens edit tools/modal.
- [ ] Delete action opens confirmation modal.
- [ ] Cancel does not delete.
- [ ] Confirm Delete removes listing from UI state.
- [ ] Backend integration TODOs are clear.
- [ ] No duplicate backend implementation was added.
- [ ] Branch is clean before PR.

---

# Browser UI Testing Guide

## Admin Access Tests

Open:

```text
http://localhost:5173/admin
```

### Unauthenticated User

```js
localStorage.clear();
location.reload();
```

Expected:

```text
Admin dashboard tools are hidden.
Sign-in guidance appears.
```

### Authenticated Non-Admin User

```js
localStorage.setItem("token", "demo-token");
localStorage.setItem("role", "customer");
location.reload();
```

Expected:

```text
Admin permission message appears.
Admin tools remain hidden.
```

### Authenticated Admin User

```js
localStorage.setItem("token", "demo-token");
localStorage.setItem("role", "admin");
location.reload();
```

Expected:

```text
Admin dashboard appears.
Inventory management tools are visible.
```

## Add New Car Form Tests

Expected manual tests:

- Submit with blank Make.
- Submit with blank Model.
- Submit with invalid Price.
- Submit with invalid Year.
- Submit with negative Mileage.
- Submit without picture if picture is required.
- Confirm user-friendly error messages appear.

## Edit Tests

Expected manual tests:

- Click Edit.
- Confirm modal opens.
- Update price.
- Update status/condition.
- Save.
- Confirm table updates.
- Try invalid price.
- Confirm validation error appears.

## Delete Tests

Expected manual tests:

- Click Delete.
- Confirm modal opens.
- Click Cancel.
- Confirm item remains.
- Click Delete again.
- Click Confirm Delete.
- Confirm item is removed from UI state.

---

# Branching Summary

## Sprint 2 Edwin Admin Branch

```text
feature/admin-inventory-management
```

or, if continuing current work:

```text
feature/admin-dashboard
```

Used for:

```text
Multistep Add New Car Form Layout
Interactive Admin Listings Table
Admin Edit/Delete UI
Admin route guard behavior
```

---

# Notes For Coordination

- Edwin and Edward should share reusable styling components to keep public customer views and private admin views visually consistent.
- Edwin should wait for Ronald's paginated `GET /api/cars` endpoint before replacing local vehicle data.
- Edwin should wait for Ronald's cloud upload endpoint before fully wiring picture upload.
- Edwin should wait for backend auth/admin role confirmation before replacing localStorage-based admin checks.
- Edwin should avoid creating duplicate backend servers or routes until backend ownership is confirmed.
