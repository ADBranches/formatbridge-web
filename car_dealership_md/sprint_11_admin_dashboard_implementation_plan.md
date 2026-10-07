# Car Dealership Sprint 11 Implementation Plan

## Admin Dashboard and Operational Management Workflow

**Repository:** `/home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership`  
**Planning baseline:** `feature/edwin-sprint10-quality-assurance` at `f8b545646dc2a68127121790c25c4be2af10bb1d`  
**Target development branch:** `feature/edwin-sprint11-admin-operations`  
**Status:** Planning complete. Implementation not started.

---

## 1. Sprint Goal

Build a protected, live-data admin dashboard that enables dealership administrators to:

1. View total cars, bookings, users, and pending-work statistics.
2. Review all bookings in an operational table.
3. Apply controlled booking-status transitions.
4. Review pending vehicle listings.
5. Approve or reject pending listings with a recorded rejection reason.
6. Perform all operations through authenticated backend endpoints.
7. Receive explicit loading, empty, success, validation, authorization, and failure feedback.

## 2. Acceptance Criteria

- The admin dashboard displays live business data rather than fixture or UI-only data.
- Booking records load from the backend and authorized administrators can update statuses.
- Pending listings can be opened and reviewed from a dedicated queue.
- Listing approval and rejection operations persist through protected backend endpoints.
- Unauthenticated users are redirected to login.
- Authenticated non-admin users cannot access admin operations.
- All mutations provide pending, success, recoverable error, and retry states.
- Frontend and backend validation pass without weakening existing authentication or authorization controls.

---

## 3. Verified Repository Findings

### Existing foundations to retain

- Canonical frontend API helpers already exist in `src/api/client.ts`.
- Canonical authentication state exists in `src/app/context/auth.tsx` and `src/features/auth/hooks/useAuth.ts`.
- `ProtectedRoute` handles authentication readiness and login redirection.
- Backend JWT and role middleware exist in `backend/middleware/authMiddleware.js`.
- Protected read endpoints already exist for:
  - `GET /api/admin/stats`
  - `GET /api/admin/users`
  - `GET /api/admin/bookings`
  - `GET /api/admin/cars`
- PostgreSQL controller functions already describe booking status changes and listing review actions, but are not yet exposed through the active admin router.
- Existing admin UI components include inventory tables, edit and delete modals, add-car UI, and image upload UI.

### Critical gaps and conflicts

1. The current branch is 21 commits behind `upstream/main`; upstream changes must be reviewed and integrated before implementation.
2. `src/pages/Admin.tsx` expects `totalCars`, while the active `/api/admin/stats` response exposes `inventoryCount`. A single normalized contract is required.
3. `backend/routes/adminRoutes.js` uses the in-memory database adapter, while `backend/controllers/adminController.js` uses PostgreSQL. Sprint 11 must select one authoritative persistence path. Use PostgreSQL unless current runtime evidence proves otherwise.
4. `backend/routes/adminMetricsRoutes.js` is not protected and uses an incompatible collection-style adapter. It must not become the Sprint 11 authority without refactoring and protection.
5. Booking statuses conflict across implementations. Existing values include `pending`, `confirmed`, `cancelled`, and `completed`.
6. Listing statuses conflict between backend lowercase workflow values and frontend labels such as `Available`, `Pending Test Drive`, and `Sold`.
7. The active admin router lacks mutation endpoints for booking status changes and listing approval/rejection.
8. `ProtectedRoute` only checks authentication. Admin role authorization currently occurs inside application/page logic and should be centralized.
9. Several admin components still use fixture data or UI-only mutations.
10. No dedicated Sprint 11 automated/manual contract tests exist for admin operations.

---

## 4. Mandatory Development Rules

- Inspect each target file immediately before modification.
- Work only on `feature/edwin-sprint11-admin-operations`.
- Do not develop or merge directly on `main`.
- Fetch and review `origin` and `upstream` before integrating collaborator work.
- Preserve JWT verification and server-side role enforcement.
- Never treat frontend role checks as the security boundary.
- Do not expose raw database errors or sensitive token values to the UI.
- Do not introduce mock business data into the production admin path.
- Create a verified Git commit at the end of every completed phase.
- Save every terminal command batch and complete output as a descriptively named `.txt` file directly in:
  `/home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/`
- Stop at the end of each phase if validation fails, a dependency is unresolved, or unexpected repository changes appear.

---

# Phased Implementation

## Phase 0: Establish the Sprint 11 Branch and Integrate the Current Baseline

### Objectives

- Preserve the verified Sprint 10 state.
- Inspect upstream changes before integration.
- Integrate the latest approved upstream baseline without silently overwriting Sprint 10 work.
- Create the dedicated Sprint 11 branch.

### Files to modify

- None expected unless merge-conflict resolution is required.

### Files to create

- No source files.
- Evidence output: `sprint11_phase0_branch_baseline_and_upstream_review.txt`

### Required work

1. Confirm the working tree is clean.
2. Fetch `origin` and `upstream` with pruning.
3. Inspect commits and changed files between `HEAD` and `upstream/main`.
4. Pay particular attention to:
   - `backend/routes/adminRoutes.js`
   - `backend/middleware/authMiddleware.js`
   - `backend/controllers/authController.js`
   - `backend/server.js`
   - `src/app/components/admin/AdminDashboard.tsx`
   - `src/features/auth/components/LoginForm.tsx`
5. Integrate the approved upstream baseline.
6. Run frontend build and backend syntax validation.
7. Create `feature/edwin-sprint11-admin-operations` from the validated integrated state.

### Validation gate

- Working tree clean before integration.
- Fetch status is zero.
- No unresolved conflict markers.
- Frontend build passes.
- Backend syntax check passes.
- New branch name is exact.
- `PATH` remains intact.

### Commit checkpoint

`chore: establish Sprint 11 admin operations baseline`

### Stop conditions

- Upstream contains unexplained scope that changes auth, booking persistence, or admin routing.
- Any merge conflict cannot be resolved from inspected evidence.
- Build or syntax validation fails.

---

## Phase 1: Normalize Admin Domain Contracts

### Objectives

- Define one frontend contract for dashboard statistics, bookings, listing reviews, and operation results.
- Define canonical status values and allowed booking transitions.
- Isolate backend naming differences in normalization functions rather than spreading conditionals through components.

### Files to create

- `src/features/admin-operations/types/adminOperations.types.ts`
- `src/features/admin-operations/types/index.ts`
- `src/features/admin-operations/validation/bookingStatusTransitions.ts`
- `src/features/admin-operations/validation/listingReviewValidation.ts`
- `src/features/admin-operations/services/adminNormalization.ts`
- `src/features/admin-operations/services/index.ts`
- `src/tests/adminOperationsContracts.manual.ts`

### Files to modify

- `src/app/lib/adminInventory.ts`
- `src/types/vehicle.ts`
- `package.json`

### Canonical frontend contracts

#### Dashboard statistics

```ts
type AdminDashboardStats = {
  totalCars: number;
  totalBookings: number;
  totalUsers: number;
  pendingBookings: number;
  pendingListings: number;
  generatedAt: string | null;
};
```

#### Booking status

```ts
type BookingStatus =
  | "pending"
  | "confirmed"
  | "completed"
  | "cancelled"
  | "rejected";
```

Recommended transitions:

- `pending` to `confirmed`, `rejected`, or `cancelled`
- `confirmed` to `completed` or `cancelled`
- `completed`, `cancelled`, and `rejected` are terminal

#### Listing review status

```ts
type ListingReviewStatus = "pending" | "approved" | "rejected";
```

#### Rejection validation

- Require a trimmed reason.
- Minimum: 5 characters.
- Maximum: 500 characters.
- Never render rejection text as HTML.

### Validation gate

- Status transition tests cover valid and invalid paths.
- Normalizers handle PostgreSQL snake_case and collection-style camelCase inputs.
- TypeScript build passes.
- Existing inventory types continue compiling.

### Commit checkpoint

`feat: define Sprint 11 admin operation contracts`

### Stop conditions

- Backend owners require a different canonical status model.
- Existing data contains unclassified statuses that cannot be safely normalized.

---

## Phase 2: Secure and Complete Backend Admin Endpoints

### Objectives

- Make the PostgreSQL admin controller the authoritative operational path.
- Expose protected mutation endpoints.
- Validate IDs, request bodies, status transitions, and rejection reasons.
- Return stable response envelopes.

### Files to create

- `backend/middleware/validateAdminOperation.js`
- `backend/utils/adminStatusTransitions.js`
- `backend/tests/adminOperationsContract.manual.js`

### Files to modify

- `backend/controllers/adminController.js`
- `backend/routes/adminRoutes.js`
- `backend/server.js`
- `backend/package.json`

### Endpoints to implement or normalize

```text
GET    /api/admin/stats
GET    /api/admin/bookings
PATCH  /api/admin/bookings/:id/status
GET    /api/admin/listings/pending
PATCH  /api/admin/listings/:id/approve
PATCH  /api/admin/listings/:id/reject
```

All routes must use:

```text
authenticateToken -> checkRole(["admin"]) -> validation -> controller
```

### Required response shapes

#### Statistics

```json
{
  "success": true,
  "data": {
    "totalCars": 0,
    "totalBookings": 0,
    "totalUsers": 0,
    "pendingBookings": 0,
    "pendingListings": 0
  },
  "timestamp": "ISO-8601"
}
```

#### Collection response

```json
{
  "success": true,
  "data": [],
  "total": 0
}
```

#### Mutation response

```json
{
  "success": true,
  "message": "Operation completed.",
  "data": {}
}
```

### Backend validation requirements

- Numeric positive resource IDs only.
- Reject unsupported booking statuses with HTTP 400.
- Reject forbidden transition paths with HTTP 409.
- Return HTTP 404 for missing booking or listing.
- Require rejection reason for listing rejection.
- Return HTTP 401 for missing or invalid token.
- Return HTTP 403 for authenticated non-admin users.
- Use parameterized SQL only.
- Do not return stack traces or SQL error text.
- Update `updated_at` for all mutations.
- Approval should clear stale rejection reason where schema permits.
- Rejection should not populate `approved_at`.

### Architecture correction

`backend/routes/adminMetricsRoutes.js` must either be protected and explicitly retained as a non-authoritative analytics route, or its mounting must be documented as out of this sprint. It must not supply operational truth while using an incompatible adapter.

### Validation gate

- Backend syntax check passes.
- Missing token returns 401.
- Non-admin token returns 403.
- Admin token returns stats and collections.
- Invalid status returns 400.
- Illegal transition returns 409.
- Unknown IDs return 404.
- Successful mutations persist and are visible on a subsequent GET.

### Commit checkpoint

`feat: secure admin booking and listing operations`

### Stop conditions

- Required PostgreSQL columns do not exist.
- The active runtime is proven to use a different persistence adapter.
- Authentication middleware does not attach a trusted role claim.

---

## Phase 3: Build the Frontend Admin API Adapter

### Objectives

- Connect frontend admin operations to protected endpoints through the canonical API client.
- Centralize normalization, authorization failure handling, and safe error messages.
- Support request cancellation for dashboard loads.

### Files to create

- `src/features/admin-operations/services/adminOperationsApi.ts`
- `src/features/admin-operations/hooks/useAdminDashboard.ts`
- `src/features/admin-operations/hooks/useAdminBookings.ts`
- `src/features/admin-operations/hooks/usePendingListings.ts`
- `src/features/admin-operations/hooks/index.ts`
- `src/tests/adminOperationsApi.manual.ts`

### Files to modify

- `src/api/client.ts`, only if a generic safe JSON/error helper is genuinely missing.
- `src/features/admin-operations/services/index.ts`
- `package.json`

### Required service functions

```ts
loadAdminStats(accessToken, options)
loadAdminBookings(accessToken, options)
updateAdminBookingStatus(id, status, accessToken, options)
loadPendingListings(accessToken, options)
approvePendingListing(id, accessToken, options)
rejectPendingListing(id, reason, accessToken, options)
```

### Required behavior

- Attach `Authorization: Bearer <token>` through existing authenticated request helpers.
- Do not log or return tokens.
- Normalize 401, 403, 404, 409, validation, server, and network failures.
- On 401, allow the consuming hook/page to clear the invalid session.
- Avoid optimistic mutation for approval/rejection unless rollback is fully implemented.
- Refresh affected statistics and queues after successful mutations.
- Ignore abort errors during unmount or request replacement.

### Validation gate

- API adapter contract tests pass.
- Bearer header is attached.
- Tokens do not appear in serialized error results.
- Response normalization works for empty and populated data.
- Build passes.

### Commit checkpoint

`feat: add authenticated admin operations client`

### Stop conditions

- Backend response shape is unstable.
- Any service bypasses `src/api/client.ts` without documented necessity.

---

## Phase 4: Centralize Admin Route Authorization and Dashboard Shell

### Objectives

- Replace duplicate localStorage authorization logic with canonical auth context.
- Add an admin-specific route boundary.
- Establish the dashboard layout, navigation, summary cards, and consistent operational states.

### Files to create

- `src/app/components/auth/AdminRoute.tsx`
- `src/features/admin-operations/components/AdminDashboardShell.tsx`
- `src/features/admin-operations/components/AdminStatsCards.tsx`
- `src/features/admin-operations/components/AdminOperationError.tsx`
- `src/features/admin-operations/components/AdminDashboardSkeleton.tsx`
- `src/features/admin-operations/components/index.ts`
- `src/tests/adminRoute.manual.ts`

### Files to modify

- `src/app/App.tsx`
- `src/app/routes.tsx`, only if it remains part of the active route configuration.
- `src/app/layouts/DashboardLayout.tsx`
- `src/pages/Admin.tsx`
- `src/app/components/admin/AdminDashboard.tsx`
- `src/app/lib/auth.ts`
- `package.json`

### Required behavior

- Unauthenticated: redirect to `/login?redirect=/Admin`.
- Authenticated non-admin: render a 403-safe access-denied screen.
- Admin: render dashboard.
- Never grant admin access from standalone `role` or `isAdmin` localStorage flags.
- Load stats from the admin API.
- Show cards for total cars, bookings, users, pending bookings, and pending listings.
- Provide keyboard-accessible navigation among Overview, Bookings, and Pending Reviews.
- Use accessible status and alert live regions.

### Validation gate

- Admin route decision tests pass.
- Legacy localStorage admin escalation paths are removed from the active admin entry path.
- Direct navigation and refresh work for a valid admin session.
- Non-admin access is denied in UI and remains denied by backend.
- Loading, error, and empty states are visible and accessible.
- Build passes.

### Commit checkpoint

`feat: add protected live admin dashboard shell`

### Stop conditions

- More than one active admin page remains mounted for the same route.
- Role checks rely on mutable legacy flags.

---

## Phase 5: Implement Booking Management Workflow

### Objectives

- Display real bookings in an operational table.
- Support filtering and controlled status changes.
- Prevent duplicate or invalid mutations.

### Files to create

- `src/features/admin-operations/components/BookingManagementTable.tsx`
- `src/features/admin-operations/components/BookingStatusBadge.tsx`
- `src/features/admin-operations/components/BookingStatusDialog.tsx`
- `src/features/admin-operations/components/BookingFilters.tsx`
- `src/tests/adminBookingWorkflow.manual.ts`

### Files to modify

- `src/features/admin-operations/components/AdminDashboardShell.tsx`
- `src/features/admin-operations/components/index.ts`
- `src/pages/Admin.tsx`
- `package.json`

### Table fields

- Booking/reference ID
- Customer name and contact where available
- Vehicle make/model/year
- Booking date
- Time slot
- Current status
- Created date
- Available action

### Required behavior

- Filter by status.
- Optional text search by customer, vehicle, or booking ID.
- Only show valid next statuses.
- Require confirmation before terminal status transitions.
- Disable row actions while the selected mutation is pending.
- Announce successful changes through an accessible live region.
- Retain the previous status and show retry on mutation failure.
- Refresh bookings and statistics after success.
- Provide responsive mobile rendering without hiding critical data.

### Validation gate

- Pending to confirmed works.
- Confirmed to completed works.
- Cancellation path works.
- Invalid and terminal transitions are blocked client-side and server-side.
- Empty, loading, 401, 403, 404, 409, 500, and network states are covered.
- Rapid repeated clicks do not create duplicate requests.
- Build passes.

### Commit checkpoint

`feat: implement admin booking management workflow`

### Stop conditions

- Booking IDs are inconsistent across persistence layers.
- Backend mutation cannot be verified by a subsequent GET.

---

## Phase 6: Implement Pending Listing Review and Decision Workflow

### Objectives

- Display only pending listings in a dedicated review queue.
- Allow complete review before approval or rejection.
- Capture and persist rejection reasons.

### Files to create

- `src/features/admin-operations/components/PendingListingsTable.tsx`
- `src/features/admin-operations/components/ListingReviewDialog.tsx`
- `src/features/admin-operations/components/ListingDecisionDialog.tsx`
- `src/features/admin-operations/components/ListingStatusBadge.tsx`
- `src/tests/adminListingReviewWorkflow.manual.ts`

### Files to modify

- `src/features/admin-operations/components/AdminDashboardShell.tsx`
- `src/features/admin-operations/components/index.ts`
- `src/pages/Admin.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`, only to reuse normalized types or remove conflicting pending-review responsibility.
- `package.json`

### Review details

- Listing ID
- Make and model
- Year
- Price
- Mileage
- Condition
- Submitted images or image availability
- Submission timestamp
- Current review status
- Existing rejection reason, if returned

### Approval behavior

- Require explicit confirmation.
- Disable both decision actions while pending.
- Remove the approved item from the pending queue after successful persistence.
- Refresh dashboard statistics.

### Rejection behavior

- Require a validated reason.
- Keep the dialog open when validation fails.
- Remove the item only after backend success.
- Preserve the reason server-side.

### Validation gate

- Pending list loads from the backend.
- Approval persists and item no longer appears in the pending queue.
- Rejection persists with reason and item no longer appears in the queue.
- Unknown listing returns a recoverable 404 state.
- Duplicate actions are prevented.
- Keyboard focus returns to the correct queue location after dialog closure.
- Build passes.

### Commit checkpoint

`feat: implement pending listing review decisions`

### Stop conditions

- Cars table lacks workflow columns and no approved schema migration exists.
- Listing images cannot be safely resolved from current records.

---

## Phase 7: Reconcile Existing Inventory Controls and Remove UI-Only Operations

### Objectives

- Prevent two competing admin implementations.
- Ensure existing inventory management components use live data or clearly remain outside Sprint 11.
- Remove fixture defaults and misleading UI-only success messages from active paths.

### Files to modify

- `src/app/components/admin/AdminDashboard.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `src/app/components/admin/EditVehicleModal.tsx`
- `src/app/components/admin/DeleteConfirmModal.tsx`
- `src/app/components/admin/AddNewCarForm.tsx`
- `src/app/components/admin/CarImageUploader.tsx`
- `src/pages/Admin.tsx`
- `src/pages/TestTasks/TestTasks.tsx`
- `src/app/lib/adminInventory.ts`

### Files to create

- `src/tests/adminInventoryReconciliation.manual.ts`

### Required decisions

- The Sprint 11 dashboard becomes the active `/Admin` implementation.
- `DEFAULT_VEHICLES` must not power the production admin listing table.
- UI-only edit/delete actions must not claim persistence.
- Existing listing creation and image upload functionality should remain available only where backend integration is already verified.
- Do not expand Sprint 11 into unrelated inventory CRUD if protected update/delete endpoints remain unavailable. Document that dependency instead.

### Validation gate

- One canonical admin route and dashboard remain active.
- No active production admin table silently falls back to fixtures.
- No UI-only operation presents a false success state.
- Existing car browsing and test-drive functionality still build and pass regression.

### Commit checkpoint

`refactor: reconcile admin inventory and operations UI`

### Stop conditions

- Removing duplicate code affects an unresolved collaborator branch.
- Inventory CRUD requirements expand beyond the approved Sprint 11 scope.

---

## Phase 8: Full Validation, Security Review, Documentation, and Handoff

### Objectives

- Prove every Sprint 11 acceptance criterion.
- Verify authorization, persistence, accessibility, responsiveness, and regression safety.
- Produce a reviewable commit and pull request handoff.

### Files to create

- `docs/sprint11/sprint11-admin-operations-contract.md`
- `docs/sprint11/sprint11-validation-report.md`
- `docs/sprint11/sprint11-security-review.md`
- `docs/sprint11/sprint11-dependency-register.md`
- `docs/sprint11/sprint11-rollback-plan.md`
- `docs/sprint11/sprint11-pr-summary.md`

### Files to modify

- `README.md`
- `package.json`
- `backend/package.json`
- `.env.example`, only if a new non-secret configuration key is required.

### Full validation matrix

#### Frontend

- Run all Sprint 11 contract tests.
- Run existing authentication, protected route, profile, booking, and regression tests.
- Run production build with an approved API base URL.
- Verify desktop, tablet, and mobile layouts.
- Verify keyboard-only operation and focus management.
- Verify accessible names, status announcements, error alerts, and dialog semantics.

#### Backend

- Run syntax checks.
- Run admin endpoint contract tests.
- Start the backend against the approved database configuration.
- Test 401, 403, 400, 404, 409, and success paths.
- Verify persisted status changes using a second read request.
- Confirm no secrets or tokens appear in logs or response bodies.

#### Integrated acceptance walkthrough

1. Sign in as admin.
2. Open `/Admin` directly and after refresh.
3. Confirm live total cars, bookings, and users.
4. Open booking management.
5. Change a pending booking to confirmed.
6. Verify persistence after reload.
7. Open pending listing reviews.
8. Approve one listing.
9. Reject another with a reason.
10. Verify both disappear from the pending queue.
11. Confirm statistics refresh.
12. Sign in as non-admin and confirm access denial.
13. Remove the token and confirm login redirection.

### Final Git requirements

- Working tree contains only approved Sprint 11 changes.
- No generated secrets, local `.env`, database dumps, or oversized evidence files are tracked.
- Final verified commit exists.
- Branch is pushed to `origin`.
- Pull request targets the repository administrator's approved integration branch.

### Final commit checkpoint

`docs: finalize Sprint 11 admin operations handoff`

### Proposed pull request title

`Sprint 11: Build live admin dashboard and operational workflows`

### Proposed pull request description

```markdown
## Summary

Implements the protected Sprint 11 admin operations dashboard for live business statistics, booking management, and pending listing review.

## Completed work

- Added live statistics for cars, bookings, users, and pending work.
- Added authenticated booking management and validated status transitions.
- Added pending listing review with approval and reasoned rejection.
- Centralized admin route authorization through the canonical auth context.
- Added loading, empty, success, validation, authorization, and recoverable failure states.
- Added frontend and backend contract validation plus security and rollback documentation.

## Security controls

- JWT authentication retained.
- Server-side admin role enforcement applied to every admin endpoint.
- Parameterized persistence operations retained.
- Invalid transitions and malformed inputs rejected.
- Tokens and internal database errors excluded from client-facing output.

## Validation

- Frontend production build: PASS
- Backend syntax validation: PASS
- Admin endpoint contract tests: PASS
- Authorization tests: PASS
- Booking workflow tests: PASS
- Listing review workflow tests: PASS
- Existing regression suite: PASS
```

### Stop condition

After the final commit and push are verified, stop. Do not merge directly to `main`.

---

## 5. Collaborator Dependencies

### Inventory/backend dependency

The newly fetched `upstream/feature/inventory-management-46` contains inventory-management work and must be reviewed before editing overlapping car controller, route, database, or dashboard files.

### Authentication dependency

`upstream/main` includes authentication and RBAC changes. Sprint 11 must build on the current canonical JWT/auth context rather than the older localStorage-only admin checks.

### Persistence dependency

The repository currently contains both PostgreSQL-style and collection-style data access. Sprint 11 cannot safely ship until the active deployment persistence path is confirmed and used consistently for admin operations.

### Schema dependency

Required columns should include equivalent support for:

- `bookings.status`
- `bookings.updated_at`
- `cars.status`
- `cars.approved_at`
- `cars.rejection_reason`
- `cars.updated_at`

If any column is missing, create an approved migration rather than silently changing runtime assumptions.

---

## 6. Definition of Done

Sprint 11 is complete only when:

- All live statistics are returned by the backend and rendered by the dashboard.
- Booking statuses can be changed through protected, validated, persistent endpoints.
- Pending listings can be reviewed, approved, and rejected with a reason.
- Every admin endpoint rejects missing authentication and non-admin roles.
- The active dashboard contains no business-data fixtures or UI-only mutation claims.
- All new and existing required tests pass.
- Production frontend build and backend syntax validation pass.
- Accessibility and responsive checks pass.
- Every phase has a verified commit.
- Final branch push and pull-request handoff are complete.
- No direct merge to `main` has occurred.

---

## 7. Immediate Next Action

Begin **Phase 0 only**: inspect and integrate the latest upstream baseline, create `feature/edwin-sprint11-admin-operations`, validate the baseline, and create the phase commit. Do not begin contract or implementation changes until the Phase 0 gate is fully verified.
