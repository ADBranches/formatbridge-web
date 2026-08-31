# Sprint 8 Frontend Development Timeline

## Purpose

This timeline governs implementation of the assigned Sprint 8 frontend work:

1. A comprehensive multi-step car-listing wizard for dealership administrators.
2. A test-drive dispatch management grid for operational booking updates.

The implementation uses dependency-graph engineering to determine task readiness, ownership, blockers, safe parallel execution, and integration order. Validation-loop engineering governs repeated inspection, targeted modification, testing, evidence collection, recovery, and completion.

No existing source file may be modified before its complete relevant structure, associated contract, and test coverage have been inspected. Missing external integrations must remain isolated behind typed adapters and deterministic mocks until confirmed upstream implementations are available.

## Delivery principles

- Sprint 8 must use a separate branch.
- The branch must start from the approved current integration base, not from the Sprint 7 feature branch.
- Existing components, services, types, routes, and tests must be reused where appropriate.
- Duplicate forms, upload adapters, booking services, routes, dashboards, and state providers are prohibited.
- Independent tasks may run in parallel only when files, state, and outputs do not conflict.
- Targeted validation must pass before broader regression testing.
- External contracts must be confirmed before mocks are replaced.
- Every completed implementation phase must end with a verified Git commit before the next implementation phase begins.
- Staging, committing, pushing, pull-request activity, merging, rebasing, and conflict resolution require explicit authorization.

## Current verified baseline

- The current working branch is the completed Sprint 7 feature branch.
- The Sprint 7 branch is synchronized with its remote and has a clean working tree.
- The Sprint 7 branch is five commits ahead and three commits behind the inspected `upstream/main`.
- The approved Sprint 8 branch base must therefore be established from the current integration branch rather than inherited from the Sprint 7 branch.
- Existing administrator inventory, image-upload, booking, authentication, route, validation, and test structures are present and must be reused after targeted inspection.
- No dedicated Sprint 8 documentation currently exists.

## Dependency graph

### Local frontend dependencies

```text
Approved Sprint 8 branch base
├── Existing administrator routing and authorization
├── Existing vehicle types and inventory utilities
├── Existing car-creation form
├── Existing image selection and preview behavior
├── Existing booking-history and availability services
└── Existing test conventions

Car-listing wizard
├── Wizard state and validation model
├── Core details step
├── Specifications step
├── Asset-upload step
│   └── Confirmed batch-upload contract or isolated adapter
├── Review and publish step
│   └── Confirmed car-creation contract
└── Responsive, accessibility, failure, and security validation

Dispatch management grid
├── Booking normalization and status model
├── Approved transition graph
├── Administrator booking-list contract
├── Booking-status mutation contract
├── Synchronization strategy
└── Responsive, accessibility, failure, and security validation
```

### External dependencies

```text
Ronald-owned inventory work
├── Batch multi-image upload
├── Image validation
├── Image ordering
├── Partial-failure behavior
└── Dynamic pricing and deal-badge output

Max-owned booking work
├── Administrator booking list
├── Booking-status update endpoint
├── Approved status transitions
├── Idempotency and conflict behavior
└── Audit and error response contract

Devine-owned security work
├── Multi-session behavior
├── Remote-session revocation
├── Administrator MFA
└── Pricing-operation challenge behavior

Edward-owned marketplace work
├── Shared vehicle fields
├── Comparison data requirements
└── Filter parameter requirements
```

---

# Phase 1: Sprint 8 Branch Foundation and Baseline Lock

## Specific objective

Create a clean Sprint 8 branch from the approved integration base and prove that Sprint 7 commits, uncommitted files, generated assets, and unrelated changes are not inherited accidentally.

## Dependency status

- Requires confirmation of the approved integration base.
- Must precede all Sprint 8 source modifications.

## Existing files to inspect

- `.gitignore`
- `package.json`
- `package-lock.json`
- `README.md`
- `.env.example`
- `vite.config.ts`

## Existing directories to inspect

- `src/`
- `backend/`
- `docs/`
- `src/tests/`
- `backend/tests/`

## New files

- None

## Files to modify

- None

## Implementation responsibilities

- Fetch all remotes.
- verify the approved base branch and commit.
- Confirm the Sprint 7 branch is clean and synchronized.
- Create `feature/edwin-sprint8-admin-workflows` from the approved base.
- Record the merge base.
- Run the existing baseline build and relevant tests.

## Validation loop

1. Verify branch and working tree.
2. Verify base and merge-base commit.
3. Verify no Sprint 7-only diff appears unexpectedly.
4. Run baseline tests and build.
5. Confirm generated assets are restored.

## Exit criteria

- Separate Sprint 8 branch exists locally.
- Branch starts from the approved base.
- Working tree is clean.
- Baseline validation passes.
- No Sprint 8 feature file has been modified.

## Approval gate

Stop before pushing the new branch. Request explicit authorization.

## Commit requirement

No implementation commit is required because no source modification occurs.

---

# Phase 2: Consolidated Contract and Ownership Review

## Specific objective

Inspect all local and upstream implementations that the wizard and dispatch grid depend on, then classify each dependency as ready, partial, blocked, or validation-only.

## Existing files to inspect

### Administrator inventory

- `src/app/components/admin/AddNewCarForm.tsx`
- `src/app/components/admin/CarImageUploader.tsx`
- `src/app/components/admin/EditVehicleModal.tsx`
- `src/app/components/admin/AdminListingsTable.tsx`
- `src/app/components/admin/AdminDashboard.tsx`
- `src/app/lib/adminInventory.ts`

### Vehicle backend

- `backend/controllers/carsController.js`
- `backend/models/carsModel.js`
- `backend/routes/carsRoutes.js`
- `backend/middleware/validateCarPayload.js`

### Image upload

- `backend/controllers/uploadController.js`
- `backend/controllers/carImageController.js`
- `backend/middleware/uploadMiddleware.js`
- `backend/models/uploadModel.js`
- `backend/services/carImageService.js`
- `backend/services/cloudinaryService.js`
- `backend/utils/optimizeCarImage.js`
- `backend/utils/imageOptimization.js`
- `backend/utils/carImageCleanupContract.js`

### Booking and dispatch

- `backend/controllers/adminController.js`
- `backend/controllers/bookingController.js`
- `backend/models/Booking.js`
- `backend/routes/adminRoutes.js`
- `backend/routes/bookingRoutes.js`
- `src/features/profile/services/bookingHistoryApi.ts`
- `src/features/profile/hooks/useBookingHistory.ts`
- `src/features/test-drive/services/availabilityApi.ts`
- `src/features/test-drive/services/testDriveService.ts`

### Existing tests

- `backend/tests/carPayloadValidation.manual.js`
- `backend/tests/carImageCleanup.manual.js`
- `backend/tests/imageOptimization.manual.js`
- `src/tests/bookingHistory.manual.ts`
- `src/tests/bookingAvailability.manual.ts`
- `src/tests/availabilitySelection.manual.ts`
- `src/tests/authPersistence.manual.ts`
- `src/tests/protectedRoute.manual.ts`

## Existing directories to inspect

- `src/app/components/admin/`
- `src/features/cars/`
- `src/features/test-drive/`
- `src/features/profile/`
- `backend/controllers/`
- `backend/routes/`
- `backend/models/`
- `backend/middleware/`
- `backend/services/`

## New files

- `docs/sprint8/sprint8-contract-register.md`
- `docs/sprint8/sprint8-dependency-register.md`

## Files to modify

- None unless inspection reveals an incorrect existing contract statement.

## Upstream branches to inspect

- `upstream/main`
- `upstream/edward`
- `upstream/Devine-codes`
- `upstream/Search-Engine-Feeds-&-Chat-Archiving`
- Confirmed Max-owned remote branch

## Implementation responsibilities

- Record branch heads and changed files.
- Extract confirmed routes, request shapes, response shapes, allowed status values, image limits, authorization rules, error behavior, and test evidence.
- Identify duplicates and contradictions.
- Determine whether `cancelled` or `canceled` is authoritative.
- Determine whether `completed` is currently supported by the backend.
- Determine whether car creation is atomic or split into vehicle creation, upload, and publication.
- Determine whether administrator pricing operations require MFA.

## Collaborator communication

After the consolidated inspection, draft reminders only for missing or incomplete work. Do not repeat previously sent requirements. Request only the latest commit, completed items, missing contract details, blockers, expected delivery date, and shared-environment availability.

## Validation loop

1. Fetch remotes.
2. Compare branch heads.
3. Inspect relevant files.
4. Record confirmed contracts.
5. Record missing contracts and owners.
6. Verify documentation contains no secrets or unsupported claims.

## Exit criteria

- Contract register is complete.
- Dependency owners and blockers are explicit.
- No endpoint or event name is guessed.
- Required collaborator reminders are ready or sent.
- Safe mock boundaries are identified.

## Approval gate

Stop before introducing mocks or modifying feature source files.

## Commit requirement

Create and verify a documentation-only commit after approval.

---

# Phase 3: Shared Sprint 8 Domain Types and Adapter Boundaries

## Specific objective

Establish one typed frontend domain for vehicle drafts, wizard validation, selected images, booking records, booking statuses, status transitions, API results, and provisional adapter boundaries.

## Existing files to inspect

- `src/app/lib/adminInventory.ts`
- Existing vehicle type files discovered during inspection
- Existing booking type files discovered during inspection
- `src/config/env.ts`
- `.env.example`
- `src/vite-env.d.ts`

## Existing directories to inspect

- `src/features/cars/`
- `src/features/test-drive/`
- `src/features/profile/`
- `src/app/lib/`

## New directories

- `src/features/admin-listing/`
- `src/features/admin-listing/types/`
- `src/features/admin-listing/services/`
- `src/features/admin-dispatch/`
- `src/features/admin-dispatch/types/`
- `src/features/admin-dispatch/services/`

Create these directories only if no suitable existing feature directories can be extended safely.

## New files

- `src/features/admin-listing/types/listingWizard.types.ts`
- `src/features/admin-listing/types/index.ts`
- `src/features/admin-listing/services/listingApi.ts`
- `src/features/admin-listing/services/listingUploadApi.ts`
- `src/features/admin-dispatch/types/dispatch.types.ts`
- `src/features/admin-dispatch/types/index.ts`
- `src/features/admin-dispatch/services/dispatchApi.ts`

## Files to modify

- Existing shared vehicle type file, if one authoritative type already exists
- Existing booking type file, if one authoritative type already exists
- `src/config/env.ts`, only if isolated mock flags are required
- `.env.example`, only after confirming naming and default policy
- `src/vite-env.d.ts`, only for verified new environment variables

## Implementation responsibilities

- Reuse shared vehicle and booking fields.
- Avoid duplicate domain models.
- Define normalized frontend values separately from backend payload shapes.
- Represent provisional operations through interfaces, not hardcoded component calls.
- Keep mocks disabled by default and blocked in production.
- Define server error normalization without exposing private payloads.

## Validation loop

- Type-check all new types and adapters.
- Verify environment parsing.
- Verify mock rejection in production.
- Verify no live endpoint is invented.
- Verify no duplicate type or service exists.

## Exit criteria

- Typed boundaries exist.
- Existing domain types remain authoritative where possible.
- Mock and live adapters are replaceable without view rewrites.
- Production mock selection is blocked.

## Approval gate

Stop before implementing wizard state or dispatch state.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 4: Listing Wizard State, Validation, and Draft Preservation

## Specific objective

Implement deterministic wizard state, step eligibility, validation, navigation, draft preservation, attachment metadata, and safe reset behavior independently of final backend submission.

## Existing files to inspect

- `src/app/components/admin/AddNewCarForm.tsx`
- `src/app/components/admin/CarImageUploader.tsx`
- Existing validation utilities
- Existing button, input, select, textarea, and error components

## New directories

- `src/features/admin-listing/state/`
- `src/features/admin-listing/validation/`
- `src/features/admin-listing/hooks/`

## New files

- `src/features/admin-listing/state/listingWizardReducer.ts`
- `src/features/admin-listing/state/listingWizardInitialState.ts`
- `src/features/admin-listing/state/index.ts`
- `src/features/admin-listing/validation/listingWizardValidation.ts`
- `src/features/admin-listing/hooks/useListingWizard.ts`
- `src/tests/listingWizardState.manual.ts`
- `src/tests/listingWizardValidation.manual.ts`

## Files to modify

- `src/app/components/admin/AddNewCarForm.tsx`, only after complete inspection

## Implementation responsibilities

- Track current step and completed steps.
- Preserve values during backward and forward navigation.
- Prevent invalid advancement.
- Normalize numeric fields safely.
- Distinguish client validation from server validation.
- Track files without attempting to persist raw `File` objects across page reloads.
- Define safe draft-reset behavior.
- Prevent duplicate submission.

## Validation scenarios

- Initial state
- Valid and invalid step transitions
- Backward navigation
- Data preservation
- Field normalization
- Attachment metadata preservation
- Reset behavior
- Duplicate submission protection
- Unknown action handling

## Exit criteria

- State is deterministic.
- Validation is independent of presentation.
- Navigation does not lose entered data.
- No backend call is made yet.
- Targeted tests pass.

## Approval gate

Stop before building the full wizard interface.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 5: Core Details and Specifications Interface

## Specific objective

Build accessible wizard steps for vehicle identity and specifications using the verified vehicle contract.

## Existing files to inspect

- `src/app/components/admin/AddNewCarForm.tsx`
- Existing shared form controls
- Existing vehicle display and filtering components
- Existing vehicle validation middleware

## New directories

- `src/features/admin-listing/components/`

## New files

- `src/features/admin-listing/components/ListingWizard.tsx`
- `src/features/admin-listing/components/ListingWizardProgress.tsx`
- `src/features/admin-listing/components/CoreDetailsStep.tsx`
- `src/features/admin-listing/components/SpecificationsStep.tsx`
- `src/features/admin-listing/components/ListingWizardErrors.tsx`
- `src/features/admin-listing/components/index.ts`

## Files to modify

- `src/app/components/admin/AddNewCarForm.tsx`
- Existing admin stylesheet or a verified dedicated stylesheet

## Implementation responsibilities

- VIN, make, model, year, and required identity fields
- Mileage, engine, color, price, and confirmed specification fields
- Accessible labels, descriptions, and inline errors
- Error summary and first-invalid-field focus
- Keyboard-operable progress navigation
- Mobile-safe layout
- Preserve values across step changes

## Validation scenarios

- Required fields
- VIN rules
- Numeric boundaries
- Invalid year and mileage
- Long values
- Keyboard navigation
- Screen-reader current-step announcement
- Tablet and mobile layouts

## Exit criteria

- First two steps are complete and accessible.
- Fields match verified backend and shared frontend contracts.
- No duplicate vehicle model is introduced.
- Targeted tests and production build pass.

## Approval gate

Stop before asset-upload implementation.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 6: Batch Asset Selection and Upload Boundary

## Specific objective

Implement the wizard asset step with local selection, validation, preview, removal, ordering, failure handling, and a replaceable upload adapter.

## Existing files to inspect

- `src/app/components/admin/CarImageUploader.tsx`
- `backend/middleware/uploadMiddleware.js`
- `backend/controllers/uploadController.js`
- `backend/controllers/carImageController.js`
- `backend/services/carImageService.js`
- `backend/services/cloudinaryService.js`
- `backend/utils/optimizeCarImage.js`
- `backend/utils/imageOptimization.js`
- `backend/utils/carImageCleanupContract.js`

## New files

- `src/features/admin-listing/components/AssetUploadStep.tsx`
- `src/features/admin-listing/components/SelectedImageList.tsx`
- `src/features/admin-listing/components/ImageUploadStatus.tsx`
- `src/features/admin-listing/validation/imageSelectionValidation.ts`
- `src/tests/listingImageSelection.manual.ts`
- `src/tests/listingUploadAdapter.manual.ts`

## Files to modify

- `src/app/components/admin/CarImageUploader.tsx`, only if reuse requires targeted extraction
- `src/features/admin-listing/services/listingUploadApi.ts`
- Environment files only if a mock flag is justified and approved

## Implementation responsibilities

- Select up to the confirmed image limit.
- Validate accepted MIME types and sizes.
- Detect duplicates.
- Generate and revoke preview URLs.
- Remove and reorder selected images.
- Preserve ordering metadata.
- Support non-drag keyboard file selection.
- Handle partial upload failure safely.
- Prevent duplicate upload submission.
- Keep synthetic behavior isolated and disabled in production.

## External dependency condition

If Ronald’s confirmed batch-upload implementation is unavailable, implement only the typed adapter and deterministic mock after explicit approval. Do not guess route paths, form field names, limits, or response shapes.

## Exit criteria

- Asset selection and validation work independently.
- Preview resources are cleaned up.
- Ordering is deterministic.
- Partial failure is represented safely.
- Production mock selection is blocked.
- Targeted tests pass.

## Approval gate

Stop before connecting final publish behavior.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 7: Review, Publish, and Transaction Recovery

## Specific objective

Implement the final review and publication workflow, including server validation, submission locking, upload sequencing, partial-failure recovery, success confirmation, and administrator-safe retry behavior.

## Existing files to inspect

- `src/app/components/admin/AddNewCarForm.tsx`
- `src/app/lib/adminInventory.ts`
- `backend/controllers/carsController.js`
- `backend/routes/carsRoutes.js`
- `backend/middleware/validateCarPayload.js`
- Confirmed car-creation and upload contracts

## New files

- `src/features/admin-listing/components/ReviewPublishStep.tsx`
- `src/features/admin-listing/components/ListingSubmissionStatus.tsx`
- `src/features/admin-listing/services/listingSubmissionCoordinator.ts`
- `src/tests/listingSubmission.manual.ts`

## Files to modify

- `src/features/admin-listing/components/ListingWizard.tsx`
- `src/features/admin-listing/services/listingApi.ts`
- `src/features/admin-listing/services/listingUploadApi.ts`
- `src/app/components/admin/AddNewCarForm.tsx`

## Implementation responsibilities

- Display a complete sanitized review summary.
- Map backend field errors to wizard steps.
- Lock duplicate submission.
- Follow the confirmed transaction order.
- Preserve a recoverable draft after failure.
- Avoid duplicate car creation during retry.
- Avoid orphaned images where the backend contract supports cleanup.
- Respect MFA challenge behavior if required for pricing.
- Return administrators to the verified inventory view after success.

## Validation scenarios

- Successful publish
- Server validation failure
- Unauthorized response
- Expired session
- MFA challenge
- Vehicle created but upload failed
- Upload succeeded but publication failed
- Duplicate retry
- Network interruption
- Safe reset after success

## Exit criteria

- Publish behavior follows confirmed contracts.
- Duplicate creation is prevented.
- Failure recovery is explicit.
- No private values are logged.
- Targeted tests and build pass.

## Approval gate

Stop before dispatch-grid implementation.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 8: Dispatch Domain State and Transition Rules

## Specific objective

Create deterministic booking normalization, status columns, allowed transitions, mutation state, optimistic-update rules, rollback behavior, and stale-response protection.

## Existing files to inspect

- `backend/controllers/adminController.js`
- `backend/controllers/bookingController.js`
- `backend/models/Booking.js`
- `backend/routes/adminRoutes.js`
- `backend/routes/bookingRoutes.js`
- `src/features/profile/services/bookingHistoryApi.ts`
- `src/features/profile/hooks/useBookingHistory.ts`
- `src/features/test-drive/services/testDriveService.ts`

## New directories

- `src/features/admin-dispatch/state/`
- `src/features/admin-dispatch/validation/`
- `src/features/admin-dispatch/hooks/`

## New files

- `src/features/admin-dispatch/state/dispatchReducer.ts`
- `src/features/admin-dispatch/state/dispatchInitialState.ts`
- `src/features/admin-dispatch/state/index.ts`
- `src/features/admin-dispatch/validation/bookingTransitions.ts`
- `src/features/admin-dispatch/hooks/useDispatchBoard.ts`
- `src/tests/dispatchState.manual.ts`
- `src/tests/bookingTransitions.manual.ts`

## Files to modify

- Existing shared booking type file if authoritative
- `src/features/admin-dispatch/services/dispatchApi.ts`

## Implementation responsibilities

- Normalize booking records.
- Define the approved statuses only.
- Define legal transitions.
- Prevent unsupported transitions.
- Track pending mutation per booking.
- Prevent duplicate clicks.
- Roll back optimistic movement after failure.
- Ignore stale mutation responses.
- Preserve server authority.

## External dependency condition

If Max’s status-update contract is missing, complete state and validation using an isolated adapter. Do not guess the live endpoint.

## Exit criteria

- State transitions are deterministic.
- Unsupported movement is blocked.
- Rollback and stale-response handling are validated.
- Targeted tests pass.

## Approval gate

Stop before rendering the dispatch board.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 9: Dispatch Management Grid Interface

## Specific objective

Build the administrator dispatch board with clear status groups, booking cards, actions, counts, loading states, empty states, and responsive behavior.

## Existing files to inspect

- `src/app/components/admin/AdminDashboard.tsx`
- Existing dashboard navigation
- Existing card, grid, table, badge, button, dialog, and empty-state components
- Existing booking-history components

## New directories

- `src/features/admin-dispatch/components/`

## New files

- `src/features/admin-dispatch/components/DispatchBoard.tsx`
- `src/features/admin-dispatch/components/DispatchColumn.tsx`
- `src/features/admin-dispatch/components/DispatchBookingCard.tsx`
- `src/features/admin-dispatch/components/DispatchActionMenu.tsx`
- `src/features/admin-dispatch/components/DispatchEmptyState.tsx`
- `src/features/admin-dispatch/components/DispatchErrorState.tsx`
- `src/features/admin-dispatch/components/index.ts`
- `src/features/admin-dispatch/components/DispatchBoard.css`

## Files to modify

- `src/app/components/admin/AdminDashboard.tsx`
- `src/app/App.tsx`, only if a dedicated protected route is approved
- Existing admin navigation file identified during inspection

## Implementation responsibilities

- Render Pending Approval, Confirmed, Completed, and Canceled using verified backend values.
- Preserve accessible status names even if backend spelling differs.
- Show booking counts.
- Show customer, vehicle, date, time, and approved operational metadata.
- Provide legal actions only.
- Disable actions during mutation.
- Confirm irreversible cancellation where required.
- Support long names and narrow layouts.

## Responsive model

- Desktop: four-column grid if supported by width.
- Tablet: two-column grid or horizontally controlled layout.
- Mobile: status tabs or stacked sections, based on accessibility inspection.

## Exit criteria

- All verified statuses render correctly.
- Empty and loading states are usable.
- Legal actions are discoverable and accessible.
- Mobile users can reach every booking and action.
- Targeted tests and build pass.

## Approval gate

Stop before live mutation and synchronization integration.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 10: Status Mutation and Synchronization

## Specific objective

Connect dispatch actions to the confirmed backend contract and implement the approved synchronization mechanism without duplicate updates or stale state.

## Existing files to inspect

- Confirmed administrator booking-list route
- Confirmed booking-status mutation route
- Existing API helper
- Authentication context
- Existing refresh, polling, or transport utilities

## New files

- `src/features/admin-dispatch/services/dispatchSynchronization.ts`
- `src/tests/dispatchApi.manual.ts`
- `src/tests/dispatchSynchronization.manual.ts`

## Files to modify

- `src/features/admin-dispatch/services/dispatchApi.ts`
- `src/features/admin-dispatch/hooks/useDispatchBoard.ts`
- `src/features/admin-dispatch/components/DispatchBoard.tsx`
- `src/features/admin-dispatch/components/DispatchBookingCard.tsx`

## Implementation responsibilities

- Attach authentication through the approved helper.
- Use the confirmed status mutation contract.
- Apply optimistic movement only when safe.
- Reconcile server responses.
- Roll back failed transitions.
- Handle authorization, conflict, stale-state, validation, and server failures.
- Implement only the confirmed synchronization model: WebSocket, server-sent events, polling, or manual refresh.
- Clean up timers and listeners.

## Exit criteria

- Valid updates persist.
- Failed updates roll back.
- Duplicate actions are blocked.
- Stale responses do not overwrite newer state.
- Synchronization resources are cleaned up.
- Targeted tests pass.

## Approval gate

Stop before full accessibility, security, and regression review.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 11: Responsive, Accessibility, Security, and Failure-State Validation

## Specific objective

Validate both administrator workflows across desktop, tablet, and mobile layouts, with complete keyboard access, screen-reader semantics, secure failure handling, and resilient recovery behavior.

## Existing files to inspect

- All wizard components and styles
- All dispatch components and styles
- Existing admin layout styles
- `src/tests/protectedRoute.manual.ts`
- `src/tests/authPersistence.manual.ts`
- Existing accessibility test conventions

## New files

- `src/tests/listingWizardAccessibility.manual.ts`
- `src/tests/dispatchAccessibility.manual.ts`
- `src/tests/sprint8Security.manual.ts`
- `docs/sprint8/sprint8-ui-validation.md`
- `docs/sprint8/sprint8-security-review.md`

## Files to modify

- Wizard components and styles as proven necessary
- Dispatch components and styles as proven necessary
- `package.json`, only to add validated test scripts
- `package-lock.json` only if dependency metadata genuinely changes

## Validation scenarios

### Listing wizard

- Empty form
- Invalid field progression
- Long values
- Backward navigation
- Upload keyboard fallback
- Invalid images
- Partial upload failure
- Duplicate submission
- Session expiration
- MFA challenge
- Mobile navigation

### Dispatch board

- Empty board
- Initial loading
- API failure
- Unauthorized response
- Long customer and vehicle names
- High booking volume
- Invalid transition
- Failed mutation rollback
- Duplicate clicks
- Stale response
- Synchronization interruption
- Keyboard navigation
- Screen-reader status announcements
- Mobile status navigation

## Security validation

- Administrator-only access
- No browser-supplied administrator identity
- Token required through approved request helper
- No sensitive logging
- File input treated as untrusted
- Production mocks blocked
- Private environment files ignored
- No sensitive compiled values

## Exit criteria

- Both workflows remain usable at agreed widths.
- No content becomes inaccessible.
- Keyboard and screen-reader behavior is present.
- Failure states provide recovery actions.
- Security tests pass.
- Build passes.

## Approval gate

Stop before full regression and production release validation.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 12: Full Regression and Production Build

## Specific objective

Run all targeted Sprint 8 tests and all affected existing regression suites, then inspect and restore generated production assets.

## Existing files to inspect

- `package.json`
- `package-lock.json`
- `vite.config.ts`
- `.env.example`
- `.gitignore`
- All Sprint 8 tests

## New files

- `docs/sprint8/sprint8-validation-report.md`

## Files to modify

- `package.json`
- `README.md`, only with concise project-facing validation guidance
- `package-lock.json` only when justified by actual dependency changes

## Required targeted suites

- Listing wizard state
- Listing validation
- Image selection
- Upload adapter
- Submission coordinator
- Dispatch state
- Booking transitions
- Dispatch API
- Synchronization
- Accessibility
- Security

## Required regression suites

- Authentication
- Protected routing
- Session persistence
- Profile
- Password
- Booking history
- Booking availability
- Availability selection
- Vehicle filters
- Car payload validation
- Image optimization and cleanup
- API configuration

## Production checks

- Production build succeeds.
- Source-map policy is honored.
- Mock modes are disabled.
- No local API or transport origin is compiled.
- No secret name or value is compiled.
- No synthetic fixture is enabled in production.
- Generated assets are restored.
- Only intended source changes remain.

## Exit criteria

- Targeted tests pass.
- Regression suites pass.
- Production build passes.
- Validation evidence is documented.
- Working tree contains only intended changes.

## Approval gate

Stop before cross-team integration walkthroughs.

## Commit requirement

Create and verify a Git commit before starting the next phase.

---

# Phase 13: Cross-Team Integration Walkthroughs

## Specific objective

Validate the wizard and dispatch board against deployed compatible upstream implementations in a shared environment.

## New files

- `docs/sprint8/listing-wizard-integration-walkthrough.md`
- `docs/sprint8/dispatch-integration-walkthrough.md`

## Files to modify

- Adapters only when confirmed contracts differ from provisional interfaces
- Existing Sprint 8 contract and dependency registers

## Listing walkthrough

1. Administrator authenticates.
2. Administrator enters core details and specifications.
3. Administrator selects and orders images.
4. Frontend validates all steps.
5. Backend creates or reserves the vehicle record according to the confirmed contract.
6. Batch images upload with confirmed ordering.
7. Partial failure behavior is tested.
8. Review and publish completes.
9. Inventory response displays the new listing.
10. Shared fields are verified against comparison and filter consumers.

## Dispatch walkthrough

1. Administrator loads the booking board.
2. Confirmed bookings are grouped correctly.
3. A pending booking moves through one approved transition.
4. Backend persistence is confirmed.
5. A prohibited transition is rejected.
6. Duplicate action is prevented.
7. A failed update rolls back.
8. Synchronization updates another active view.
9. Session revocation is tested if available.
10. Audit evidence is recorded without private customer data.

## Evidence to record

- Date and time
- Participants
- Frontend and backend commits
- Environment
- Synthetic record identifiers
- HTTP results
- Synchronization results
- Upload result
- Status-transition result
- Persistence result
- Errors and owners
- Final PASS or BLOCKED status

## Exit criteria

- Wizard submission passes end to end.
- Batch upload and ordering pass.
- Dispatch status mutation passes.
- Synchronization behavior passes.
- Security boundaries pass.
- Known defects have owners and dates.
- No secret or real customer data is committed.

## Approval gate

If external dependencies remain unavailable, record BLOCKED and stop. Do not report synthetic validation as live success.

## Commit requirement

Create and verify a Git commit for the evidence record before starting final handoff.

---

# Phase 14: Documentation, Cleanup, and Pull Request Preparation

## Specific objective

Finalize documentation, remove temporary artifacts, confirm repository readiness, and prepare a reviewer-focused pull request without merging.

## New files

- `docs/sprint8/sprint8-deployment-handoff.md`
- `docs/sprint8/sprint8-rollback-plan.md`
- `docs/sprint8/sprint8-pr-summary.md`

## Files to modify

- `README.md`
- `.env.example`
- `package.json`
- `package-lock.json` only if justified
- Additional files only when final review proves cleanup is required

## Cleanup requirements

- Remove unused imports.
- Remove dead temporary fixtures.
- Confirm mocks are disabled by default.
- Confirm production mocks are blocked.
- Confirm no duplicate forms, routes, providers, services, or adapters exist.
- Confirm generated assets are not staged.
- Confirm private environment files remain ignored.
- Confirm endpoint and status names match approved contracts.
- Confirm the branch is synchronized with its remote.
- Run a read-only comparison with current upstream.
- Document conflicts without speculative resolution.

## Pull request contents

- Wizard and dispatch summary
- User-facing behavior
- Confirmed contracts
- Provisional boundaries
- Screenshots or approved demo links
- Targeted test results
- Regression results
- Production build result
- Cross-team walkthrough result
- Known dependencies
- Security considerations
- Files created and modified
- Integration notes
- Deployment handoff
- Rollback guidance

## Exit criteria

- Documentation is complete.
- Tests and build pass.
- Working tree is clean.
- Branch is pushed and synchronized.
- Pull-request description is accurate.
- Reviewer can distinguish completed work, provisional behavior, live validation, and blocked work.

## Final approval gate

Stop after repository readiness confirmation. Request explicit approval before opening the pull request, updating an existing pull request, merging, rebasing, or resolving conflicts.

## Commit requirement

Create and verify the final Sprint 8 handoff commit before any pull-request action.

---

# Parallel Workstream Rules

## Safe parallel work

The following may run concurrently after their dependencies are ready:

- Wizard validation logic and dispatch transition modeling
- Wizard accessibility inspection and dispatch accessibility inspection
- Collaborator branch inspections
- Contract documentation and test inventory
- Static security checks and duplicate-implementation checks
- Independent targeted test suites

## Required synchronization

The following must remain synchronized:

- Shared vehicle types used by the wizard and marketplace features
- Shared booking types used by dispatch and booking history
- Administrator routing and navigation
- Environment mock flags
- Package scripts
- Final documentation
- Git staging and commits

# Validation Loop Standard

Every implementation phase follows this loop:

```text
Inspect complete current structure
-> confirm local and external dependencies
-> apply targeted change
-> inspect exact diff
-> run targeted test
-> correct targeted failure
-> run broader regression
-> run security and build checks where applicable
-> restore generated assets
-> verify working tree
-> document evidence
-> request commit authorization
-> create verified commit
-> stop before the next phase
```

# Estimated Active Development Time

The estimate excludes waiting for collaborator commits, shared-environment access, and reviewer approvals.

- Branch foundation and baseline: 30 to 60 minutes
- Contract and dependency review: 2 to 4 hours
- Shared types and adapter boundaries: 2 to 4 hours
- Wizard state and validation: 3 to 5 hours
- Wizard interface: 4 to 7 hours
- Image selection and upload boundary: 4 to 8 hours
- Review and publication workflow: 3 to 6 hours
- Dispatch state and transitions: 3 to 5 hours
- Dispatch interface: 4 to 7 hours
- Mutation and synchronization: 3 to 6 hours
- Accessibility, security, and failure validation: 3 to 6 hours
- Regression and production validation: 2 to 4 hours
- Live walkthroughs: 2 to 4 hours after dependencies are available
- Final documentation and PR preparation: 2 to 4 hours

Estimated active implementation effort: **37 to 70 hours**, depending on the completeness and compatibility of upstream contracts.

# Definition of Done

Sprint 8 frontend work is complete only when:

- The wizard is implemented and validated.
- The dispatch grid is implemented and validated.
- Confirmed live contracts replace approved provisional adapters.
- Targeted and regression tests pass.
- Production build checks pass.
- Responsive, accessibility, security, and failure-state validation passes.
- Integration walkthroughs pass or are accurately recorded as blocked.
- Generated assets are restored.
- Documentation is complete.
- Every completed implementation phase has a verified Git commit.
- The branch is clean and synchronized.
- The pull request is accurate and ready for final review.
- No merge or conflict-resolution activity occurs without explicit approval.
