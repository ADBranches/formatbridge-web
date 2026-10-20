# Sprint 13 End-to-End Implementation Timeline

## Task

**TSK-010: Modularize hard-coded backend endpoints**

Move hard-coded mock admin, cars, and booking endpoints out of `backend/server.js` into their appropriate route and controller modules, mount the routers from the server, preserve health checks and centralized error handling, and remove duplicate mock authentication endpoints only after the canonical authentication router has been verified as ready.

## Repository and Evidence Baseline

- Repository root: `/home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership`
- Backend entry point: `backend/server.js`
- Runtime: Node.js `v22.22.2`, npm `10.9.7`
- Backend style: ECMAScript modules
- Existing route modules: authentication, cars, bookings, admin, admin metrics, test drives, exchange rates, and optimized assets
- Existing controller modules: authentication, cars, bookings, admin, admin metrics, and car images
- Existing authorization middleware: `authenticateToken`, `protect`, and `adminOnly`
- Existing logging/error infrastructure: Winston request/error logging and structured API error responses
- Existing end-to-end surface: React frontend, Express backend, PostgreSQL persistence, authentication, admin workflows, cars, bookings, dispatch, and automated tests

## Mandatory Engineering Rules

1. Build and validate the sprint end to end, not as an isolated backend edit.
2. Work only on a dedicated Sprint 13 development branch.
3. Fetch and inspect the parent integration repository before implementation and again before final handoff.
4. Do not merge directly into `main`.
5. Preserve authentication, authorization, database, observability, health-check, error-handling, and frontend contracts.
6. Do not remove mock authentication routes until the canonical authentication router passes contract and runtime validation.
7. Do not invent replacement endpoints. Preserve the current HTTP methods, paths, status codes, response envelopes, and authorization rules unless a verified defect requires correction.
8. Use loop-based and graph-engineering checks: trace each endpoint through route, middleware, controller, persistence/service, frontend consumer, and test coverage.
9. Save every terminal command batch and complete output as a descriptive `.txt` file in the project parent directory.
10. Commit and push every fully verified phase. Create the pull request only after all required validations pass.

---

## Phase 0: Correct Repository Baseline and Integration Preflight

### Objectives

- Enter the actual Git repository rather than its parent evidence directory.
- Record branch, status, remotes, tracking branch, recent commits, and divergence.
- Fetch all remotes without merging.
- Identify the parent integration branch and review incoming changes affecting Sprint 13 files.
- Create and push a dedicated Sprint 13 branch from the verified baseline.

### Files created

- `SPRINT_13_END_TO_END_IMPLEMENTATION_TIMELINE.md`

### Files modified

- None in application source.

### Evidence output

- Parent directory: `sprint13_phase0_repository_baseline_and_branch.txt`

### Completion gate

- Correct Git root confirmed.
- Worktree clean or all pre-existing changes explicitly classified.
- Parent integration branch fetched and reviewed.
- Dedicated Sprint 13 branch exists locally and remotely.
- Timeline committed and pushed.

---

## Phase 1: Endpoint Graph and Contract Audit

### Objectives

- Inventory every inline endpoint in `backend/server.js`.
- Classify each endpoint as health, authentication, admin, cars, bookings, infrastructure, or unrelated domain functionality.
- Trace frontend consumers and automated tests for every endpoint in Sprint 13 scope.
- Detect duplicate route registrations and route-order conflicts.
- Determine whether canonical authentication routes are fully mounted and equivalent to any inline mock routes.
- Capture existing methods, paths, middleware, request schemas, response envelopes, status codes, and side effects before moving code.

### Files inspected

- `backend/server.js`
- `backend/routes/authRoutes.js`
- `backend/routes/carsRoutes.js`
- `backend/routes/bookingRoutes.js`
- `backend/routes/adminRoutes.js`
- `backend/controllers/authController.js`
- `backend/controllers/carsController.js`
- `backend/controllers/bookingController.js`
- `backend/controllers/adminController.js`
- `backend/middleware/authMiddleware.js`
- Existing backend tests discovered under the repository test locations
- Frontend API adapters and consumers under `src/`

### Files created

- `docs/sprint-13-endpoint-contract-audit.md`

### Files modified

- None in runtime source.

### Evidence output

- Parent directory: `sprint13_phase1_endpoint_graph_and_contract_audit.txt`

### Completion gate

- Every targeted inline endpoint has one verified destination router and controller.
- Every affected frontend consumer is mapped.
- Authentication duplication status is explicitly recorded as removable or deferred.
- Health and error infrastructure boundaries are documented.

---

## Phase 2: Admin Endpoint Modularization

### Objectives

- Move only verified inline admin handlers from `backend/server.js` into the admin controller.
- Declare corresponding routes in the admin router.
- Preserve `protect` and `adminOnly` enforcement.
- Preserve request validation, response shape, status codes, database behavior, and logging.
- Ensure the server mounts the admin router once at the canonical prefix.

### Files modified

- `backend/server.js`
- `backend/routes/adminRoutes.js`
- `backend/controllers/adminController.js`

### Files created or modified for tests

- Existing admin route/contract test file identified in Phase 1, or if no suitable file exists: `backend/tests/sprint13-admin-route-modularization.test.js`

### Evidence output

- Parent directory: `sprint13_phase2_admin_route_modularization.txt`

### Completion gate

- No targeted inline admin handler remains in `backend/server.js`.
- Admin route prefix is mounted once.
- Unauthenticated and non-admin requests remain blocked.
- Authorized admin requests preserve their previous contracts.
- Targeted tests pass with no shell or runtime errors.

---

## Phase 3: Cars Endpoint Modularization

### Objectives

- Move verified inline car handlers into the cars controller and router.
- Preserve public versus protected route boundaries.
- Preserve pagination, filtering, availability, image, and persistence behavior where applicable.
- Keep infrastructure endpoints such as sitemap/RSS generation in the server unless Phase 1 proves they belong to a dedicated infrastructure router.
- Confirm frontend inventory and car-detail consumers continue using unchanged API contracts.

### Files modified

- `backend/server.js`
- `backend/routes/carsRoutes.js`
- `backend/controllers/carsController.js`
- Frontend API adapter file identified in Phase 1 only if a verified contract defect requires a correction

### Files created or modified for tests

- Existing cars API test file identified in Phase 1, or if absent: `backend/tests/sprint13-cars-route-modularization.test.js`

### Evidence output

- Parent directory: `sprint13_phase3_cars_route_modularization.txt`

### Completion gate

- No targeted inline cars handler remains in `backend/server.js`.
- Cars router is mounted once at its canonical prefix.
- Public and protected behavior remains unchanged.
- Frontend inventory and detail requests succeed against the live local backend.
- Targeted tests pass.

---

## Phase 4: Booking Endpoint Modularization

### Objectives

- Move verified inline booking handlers into the booking controller and router.
- Preserve booking creation, availability, history, status transitions, admin management, and dispatch-related contracts.
- Preserve authorization and transition guards.
- Verify the complete browser-to-database path for booking operations.

### Files modified

- `backend/server.js`
- `backend/routes/bookingRoutes.js`
- `backend/controllers/bookingController.js`
- Frontend booking API adapter or consumer files identified in Phase 1 only when required by verified evidence

### Files created or modified for tests

- Existing booking and dispatch contract tests identified in Phase 1, or if absent: `backend/tests/sprint13-booking-route-modularization.test.js`

### Evidence output

- Parent directory: `sprint13_phase4_booking_route_modularization.txt`

### Completion gate

- No targeted inline booking handler remains in `backend/server.js`.
- Booking router is mounted once.
- Approved transitions still succeed and unsupported transitions remain blocked.
- Customer and admin booking workflows succeed end to end.
- Targeted booking and dispatch tests pass.

---

## Phase 5: Canonical Authentication Cutover Gate

### Objectives

- Compare inline mock authentication behavior with `authRoutes` and `authController`.
- Verify registration, login, session, logout/cleanup, role enforcement, email verification, password recovery, and protected-route behavior relevant to the duplicated routes.
- Remove duplicate mock authentication endpoints only if the canonical router is demonstrably complete and mounted.
- If canonical readiness is incomplete, retain the mock endpoints temporarily, document the exact dependency, and prevent accidental duplicate matching through route order or feature isolation.

### Files modified only when canonical readiness passes

- `backend/server.js`
- `backend/routes/authRoutes.js` only if a verified mounting/contract defect exists
- `backend/controllers/authController.js` only if a verified canonical behavior gap is within Sprint 13 scope

### Files created or modified for tests

- Existing authentication contract tests identified in Phase 1, or if absent: `backend/tests/sprint13-auth-router-cutover.test.js`

### Documentation modified

- `docs/sprint-13-endpoint-contract-audit.md`

### Evidence output

- Parent directory: `sprint13_phase5_canonical_auth_cutover_gate.txt`

### Completion gate

- Exactly one authoritative implementation serves each authentication endpoint.
- No authentication/security control is disabled.
- Registration, login, session protection, and admin enforcement pass.
- If removal is deferred, the blocker and safe interim state are documented clearly.

---

## Phase 6: Health Checks, Error Handling, and Server Composition

### Objectives

- Reduce `backend/server.js` to application composition and infrastructure responsibilities.
- Preserve the health-check endpoint and its exact contract.
- Preserve middleware order, CORS, parsing, performance monitoring, logging, not-found handling, and centralized error handling.
- Confirm all domain routers are mounted before not-found and error middleware.
- Detect duplicate route mounts and unreachable handlers.

### Files modified

- `backend/server.js`

### Files modified only if existing architecture already uses dedicated middleware modules

- Existing not-found/error middleware file identified in Phase 1

### Files created or modified for tests

- Existing health/error test file identified in Phase 1, or if absent: `backend/tests/sprint13-server-composition.test.js`

### Evidence output

- Parent directory: `sprint13_phase6_health_error_and_server_composition.txt`

### Completion gate

- Health endpoint returns the expected success contract.
- Unknown endpoints return the expected not-found response.
- Forced controller failures reach centralized error handling.
- No target domain handler remains inline in `backend/server.js`.
- Server starts cleanly on the configured port.

---

## Phase 7: Full End-to-End Runtime Validation

### Objectives

- Start PostgreSQL dependencies required by the verified local setup.
- Start the backend and frontend concurrently using existing project scripts.
- Validate browser-facing flows against the live local API.
- Exercise admin login/authorization, car inventory, car details, booking creation/history/status handling, and health checks.
- Verify frontend production build and all relevant backend suites.
- Confirm no frontend request falls back to stale mock data for the migrated endpoints.

### Files modified

- No source file unless validation reveals a reproducible Sprint 13 defect. Any repair must be minimal and added to the appropriate earlier phase file list.

### Evidence outputs

- Parent directory: `sprint13_phase7_backend_runtime.txt`
- Parent directory: `sprint13_phase7_frontend_runtime.txt`
- Parent directory: `sprint13_phase7_end_to_end_validation.txt`

### Completion gate

- Backend starts without syntax, import, route, database, or middleware errors.
- Frontend starts and builds successfully.
- Health, admin, cars, bookings, auth, and dispatch regression tests pass.
- Live browser-to-API-to-database workflows pass.
- No duplicate target endpoint is registered.

---

## Phase 8: Upstream Recheck, Final Regression, Commit, and Push

### Objectives

- Fetch the parent integration repository again.
- Review incoming changes touching Sprint 13 files before integrating anything.
- Integrate safely only after scope review.
- Re-run targeted and full regression validation after integration.
- Verify diff boundaries, conflict markers, secrets, generated artifacts, and worktree state.
- Create the final verified commit and push the development branch.

### Files modified

- Only files already approved in Phases 0 through 7, plus conflict resolutions that preserve both verified scopes.

### Evidence outputs

- Parent directory: `sprint13_phase8_upstream_recheck_and_integration.txt`
- Parent directory: `sprint13_phase8_final_regression_commit_push.txt`

### Completion gate

- Parent branch status and divergence are known.
- Incoming collaborator scope has been reviewed.
- All validation commands pass after integration.
- No unresolved conflict marker, secret, accidental artifact, or unrelated diff remains.
- Final commit exists locally and remotely.

---

## Phase 9: Pull Request and Integration Handoff

### Objectives

- Create a pull request from the Sprint 13 development branch to the verified integration branch.
- Provide exact scope, contracts preserved, files changed, tests executed, results, known deferred dependency, and rollback notes.
- Do not merge the pull request directly.

### Files created or modified

- `docs/sprint-13-endpoint-contract-audit.md`
- `SPRINT_13_END_TO_END_IMPLEMENTATION_TIMELINE.md` only if final status markers require updating

### Evidence output

- Parent directory: `sprint13_phase9_pr_and_handoff_verification.txt`

### Completion gate

- Pull request is open and mergeability is checked.
- Remote branch commit matches the verified local commit.
- Review instructions include live run commands and test evidence.
- Repository administrator/integration lead is left to review and merge.

---

## Required End-to-End Validation Matrix

### Static and structural

- JavaScript syntax/import validation
- Router import and mount validation
- Duplicate endpoint/mount search
- Conflict-marker search
- Tracked-secret and environment-file boundary inspection
- Git diff and changed-file boundary review

### Backend

- Server startup
- Health check
- Not-found behavior
- Centralized error behavior
- Authentication contract
- Admin authorization
- Cars API contracts
- Booking and dispatch contracts
- Database-backed persistence

### Frontend

- Development startup
- Production build
- Authentication/session flow
- Admin dashboard requests
- Inventory and car-detail requests
- Booking creation and management
- User-visible API error behavior

### Integration

- Parent-branch fetch before implementation
- Incoming scope review before integration
- Post-integration full regression
- Final commit and remote-branch verification
- Pull-request mergeability check

## Definition of Done

Sprint 13 is complete only when:

1. Targeted admin, cars, and booking handlers no longer live inline in `backend/server.js`.
2. Each migrated endpoint has one canonical route-to-controller execution path.
3. Health checks and centralized error handling remain operational.
4. Duplicate mock authentication endpoints are removed only after canonical authentication readiness passes, or their safe deferral is documented.
5. Existing API contracts and frontend workflows remain compatible.
6. Relevant targeted tests and the full regression suite pass.
7. Live frontend, backend, and database flows work locally end to end.
8. Parent integration changes are reviewed and safely reconciled.
9. The verified branch is committed and pushed.
10. A reviewable pull request is opened without directly merging into the integration branch.
