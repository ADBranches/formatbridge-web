# Edwin Sprint 6 Development Timeline

## Sprint 6 Scope

**Role:** Frontend Developer, Profile Management and Interactive UI Validation

### Task 1: Customer Profile and Password Reset Dashboard

**Goal:** Allow authenticated customers to manage contact information, update account passwords, and review their complete test-drive booking history.

### Task 2: Instant Booking Availability Interceptor

**Goal:** Prevent customers from completing a booking for a time slot that has already been reserved.

---

## Sprint 6 Branch Strategy

### Branch Name

```text
feature/edwin-sprint6-profile-booking
```

### Branch Source

Create the Sprint 6 branch from the latest reviewed `upstream/main`, not from the completed Sprint 5 feature branch.

### Branch Creation Sequence

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
git fetch origin
git fetch upstream
git switch main
git pull --ff-only upstream main
git switch -c feature/edwin-sprint6-profile-booking
git push -u origin feature/edwin-sprint6-profile-booking
```

### Branch Rules

- Keep Sprint 6 work isolated on `feature/edwin-sprint6-profile-booking`.
- Do not continue development on the Sprint 5 branch.
- Use one focused commit for each completed implementation phase.
- Run a targeted test before each phase commit.
- Synchronize with the latest `upstream/main` before opening the Sprint 6 pull request.
- Resolve integration conflicts before requesting administrator review.
- Do not force-push after the pull request is opened unless explicitly requested.

---

## Fast-Track Schedule

```text
Day 1: Branch baseline, API contracts, and profile feature foundation
Day 2: Profile update and password-change workflows
Day 3: Customer booking-history dashboard
Day 4: Availability service and instant booking interceptor
Day 5: Integration drill, regression validation, documentation, upstream sync, and PR
```

### Delivery Target

```text
Duration: 5 working days
Implementation phases: 8
Implementation commits: 6 to 8 focused commits
Final result: clean, tested, documented, conflict-free PR
```

---

# Phase 0: Sprint 6 Baseline and Contract Lock

## Objective

- Create the Sprint 6 branch from the latest `upstream/main`.
- Confirm the active router and Sprint 5 authentication provider.
- Inspect the existing profile, booking calendar, API client, and test structure.
- Confirm the exact profile, password, booking-history, and availability API contracts.
- Identify cross-team blockers before frontend implementation.
- Prevent duplicate routers and authentication stores from returning.

## Files and Directories to Review

```text
package.json
package-lock.json
vite.config.ts
.env.example
README.md

src/app/App.tsx
src/app/context/auth.tsx
src/app/components/auth/

src/api/
src/features/auth/
src/features/cars/
src/features/test-drives/

src/components/ProfileSettings.tsx
src/components/Profile.css
src/components/BookingCalendar.jsx
src/components/BookingCalendar.css

src/pages/profile.tsx
src/pages/profile.css

src/tests/

backend/routes/authRoutes.js
backend/routes/bookingRoutes.js
backend/routes/testDriveRoutes.js
backend/controllers/authController.js
backend/middleware/authMiddleware.js
```

## Phase Output

```text
Confirmed active router
Confirmed authoritative AuthProvider
Confirmed profile component ownership
Confirmed booking calendar ownership
Recorded profile endpoint contract
Recorded password endpoint contract
Recorded booking-history endpoint contract
Recorded availability endpoint contract
Clean Sprint 6 branch pushed to origin
```

## Exit Gate

- Correct Sprint 6 branch is active.
- Working tree is clean.
- Branch is synchronized with origin.
- No duplicate router or authentication store is active.
- Required backend contracts are recorded.
- Missing cross-team contracts are assigned to their owners.

## Commit

No commit unless baseline documentation requires correction.

---

# Phase 1: Profile Feature Consolidation

## Objective

- Create one authoritative profile feature boundary.
- Reuse the Sprint 5 `AuthProvider` and protected-route behavior.
- Consolidate existing profile components without maintaining duplicate dashboards.
- Add typed profile and booking-history models.
- Add the protected `/settings` route.
- Establish loading, empty, success, and sanitized error states.

## Directories to Create

```text
src/features/profile/
src/features/profile/components/
src/features/profile/hooks/
src/features/profile/services/
src/features/profile/types/
src/features/profile/utils/

src/pages/Settings/
```

## Files to Create

```text
src/pages/Settings/SettingsPage.tsx

src/features/profile/components/ProfileSettingsPanel.tsx
src/features/profile/components/ProfileSettingsPanel.css
src/features/profile/components/ProfileSummaryCard.tsx
src/features/profile/components/ProfileForm.tsx

src/features/profile/hooks/useProfile.ts

src/features/profile/services/profileApi.ts

src/features/profile/types/index.ts
src/features/profile/utils/profileValidation.ts
```

## Existing Files to Review or Update

```text
src/app/App.tsx

src/components/ProfileSettings.tsx
src/components/Profile.css
src/pages/profile.tsx
src/pages/profile.css
```

## File Consolidation Rule

The existing profile files must be inspected and handled using one of these strategies:

```text
Migrate implementation into src/features/profile/
or
Retain the existing files only as thin compatibility exports
```

Do not maintain two independent profile dashboards.

## Exit Gate

- `/settings` is protected by the existing Sprint 5 route guard.
- Only one profile implementation is active.
- Profile types compile.
- Loading and sanitized error states render.
- No duplicate authentication state is introduced.
- Production build passes.

## Commit

```text
Create Sprint 6 profile feature foundation
```

---

# Phase 2: Contact Information Update

## Objective

- Load the authenticated customer’s current profile.
- Allow approved display-name and contact-field updates.
- Validate input before submission.
- Submit updates through the environment-driven API client.
- Update the authoritative authenticated user after a successful response.
- Prevent duplicate requests while submission is pending.
- Display sanitized API errors.

## Files to Create

```text
src/features/profile/components/ProfileForm.css

src/tests/profileValidation.manual.ts
src/tests/profileService.manual.ts
```

## Files to Update

```text
src/features/profile/components/ProfileForm.tsx
src/features/profile/hooks/useProfile.ts
src/features/profile/services/profileApi.ts
src/features/profile/types/index.ts
src/features/profile/utils/profileValidation.ts

src/app/context/auth.tsx
src/api/client.ts

package.json
```

## Required API Contract

```text
GET /api/auth/session
PATCH /api/users/me
```

If the approved backend route differs, update only the profile service after the contract is confirmed.

## Required UI States

```text
Initial loading
Profile loaded
Validation failure
Submitting
Update successful
Unauthorized session
Sanitized server failure
```

## Exit Gate

- Current profile loads for an authenticated user.
- Valid profile updates succeed.
- Invalid fields are blocked before submission.
- Submit controls are disabled during pending requests.
- Authenticated user state refreshes after success.
- Tokens and authorization headers are never logged.
- Profile validation and service tests pass.

## Commit

```text
Add authenticated profile update workflow
```

---

# Phase 3: Secure Password Update

## Objective

- Add a secure password-change form.
- Require the current password, new password, and confirmation.
- Validate minimum strength, confirmation, and password-reuse rules.
- Keep the backend authoritative for password verification.
- Clear password inputs immediately after success.
- Never persist or log password values.
- Reuse Sprint 5 invalid-session cleanup for unauthorized responses.

## Files to Create

```text
src/features/profile/components/PasswordChangeForm.tsx
src/features/profile/components/PasswordChangeForm.css

src/features/profile/hooks/usePasswordChange.ts

src/features/profile/utils/passwordValidation.ts

src/tests/passwordValidation.manual.ts
src/tests/passwordChange.manual.ts
```

## Files to Update

```text
src/features/profile/components/ProfileSettingsPanel.tsx
src/features/profile/services/profileApi.ts
src/features/profile/types/index.ts

package.json
```

## Required API Contract

```text
PATCH /api/users/me/password
```

### Request Shape

```text
currentPassword
newPassword
```

### Expected Responses

```text
200 Password changed
400 Invalid input
401 Missing or expired session
403 Incorrect current password
429 Rate limited
```

## Exit Gate

- Current password is required.
- New password confirmation is validated.
- Weak passwords are rejected.
- Reused passwords are rejected when required by the approved policy.
- Password values are never stored in localStorage or logs.
- Successful requests clear all password fields.
- Unauthorized responses clear invalid authentication sessions.
- Password tests pass.

## Commit

```text
Add secure password change workflow
```

---

# Phase 4: Test-Drive Booking History

## Objective

- Display the authenticated customer’s full test-drive booking history.
- Separate upcoming, completed, and cancelled bookings.
- Sort bookings by appointment date.
- Add loading, empty, and failure states.
- Ensure the browser cannot request another customer’s history by changing a user ID.
- Keep booking-history data server-authoritative.

## Files to Create

```text
src/features/profile/components/BookingHistory.tsx
src/features/profile/components/BookingHistory.css
src/features/profile/components/BookingHistoryCard.tsx
src/features/profile/components/BookingStatusBadge.tsx

src/features/profile/hooks/useBookingHistory.ts

src/features/profile/utils/bookingHistory.ts

src/tests/bookingHistory.manual.ts
```

## Files to Update

```text
src/features/profile/components/ProfileSettingsPanel.tsx
src/features/profile/services/profileApi.ts
src/features/profile/types/index.ts

src/pages/Settings/SettingsPage.tsx

package.json
```

## Required API Contract

Preferred secure route:

```text
GET /api/bookings/me
```

Avoid relying on this browser-controlled route unless ownership is enforced by the backend:

```text
GET /api/bookings/user/:user_id
```

## Required Booking Groups

```text
Upcoming
Completed
Cancelled
```

## Exit Gate

- Authenticated booking history loads.
- Upcoming bookings render correctly.
- Completed bookings render correctly.
- Cancelled bookings render correctly.
- Empty state renders when no bookings exist.
- Booking dates are sorted correctly.
- The frontend does not accept an arbitrary user ID.
- Booking-history tests pass.

## Commit

```text
Add customer test drive booking history
```

---

# Phase 5: Booking Availability API Layer

## Objective

- Define one availability service and response contract.
- Fetch availability for a selected date.
- Abort stale requests when the date changes quickly.
- Normalize dates, time slots, and availability responses.
- Distinguish reserved slots from service failures.
- Avoid treating a failed request as proof that all slots are available.

## Directories to Create

```text
src/features/test-drives/components/
src/features/test-drives/hooks/
src/features/test-drives/services/
src/features/test-drives/types/
src/features/test-drives/utils/
```

## Files to Create

```text
src/features/test-drives/services/availabilityApi.ts
src/features/test-drives/hooks/useBookingAvailability.ts
src/features/test-drives/types/index.ts
src/features/test-drives/utils/bookingDate.ts
src/features/test-drives/utils/availability.ts

src/tests/bookingAvailability.manual.ts
```

## Files to Update

```text
src/api/client.ts
package.json
```

## Required API Contract

```text
GET /api/bookings/check-availability?date=YYYY-MM-DD
```

## Preferred Response Shape

```text
date
timezone
slots
slot.time
slot.available
slot.reason
```

## Request Lifecycle

```text
Date selected
Previous request aborted
Loading state starts
Availability request sent
Response normalized
Reserved slots marked unavailable
Available slots retained
Error handled safely
```

## Exit Gate

- Availability service accepts a valid date.
- Invalid dates are rejected before the request.
- Old requests are cancelled when the user changes dates.
- Unavailable slots normalize correctly.
- Network failure does not unlock every slot.
- Availability service tests pass.

## Commit

```text
Add booking availability service and hook
```

---

# Phase 6: Instant Booking Availability Interceptor UI

## Objective

- Connect the availability hook to the active booking calendar.
- Request availability immediately after date selection.
- Gray out and disable reserved hours.
- Clear a selected time if the slot becomes unavailable.
- Recheck the selected time immediately before final submission.
- Block submission if another customer reserved the slot.
- Refresh availability after a successful booking.
- Preserve keyboard and screen-reader usability.

## Files to Create

```text
src/features/test-drives/components/AvailabilityStatus.tsx
src/features/test-drives/components/TimeSlotPicker.tsx
src/features/test-drives/components/TimeSlotPicker.css

src/tests/bookingInterceptor.manual.ts
```

## Files to Update

```text
src/components/BookingCalendar.jsx
src/components/BookingCalendar.css

src/features/test-drives/hooks/useBookingAvailability.ts
src/features/test-drives/services/availabilityApi.ts
src/features/test-drives/types/index.ts
src/features/test-drives/utils/availability.ts

src/tests/bookingAvailability.manual.ts

package.json
```

## Interaction Rules

```text
No date selected: no availability request
Date selected: request availability
Request pending: show slot-loading state
Reserved slot: disabled and visually muted
Available slot: selectable
Selected slot becomes reserved: clear selection
Submission begins: recheck selected slot
Recheck fails: block submission safely
Recheck unavailable: show conflict message
Successful booking: refresh availability
```

## Exit Gate

- Date selection triggers one active request.
- Reserved slots are disabled.
- Reserved slots cannot be submitted.
- A stale response cannot overwrite a newer date selection.
- Final submission performs an availability recheck.
- Successful booking refreshes availability.
- Keyboard navigation remains functional.
- Booking interceptor tests pass.

## Commit

```text
Add instant booking availability interceptor
```

---

# Phase 7: Cross-Functional Integration Drill

## Objective

- Validate profile and booking functionality against the real Sprint 6 backend.
- Verify Max’s booking availability engine receives frontend requests.
- Verify Devine’s confirmation-email workflow is triggered after a successful booking.
- Confirm profile update, password change, booking history, and availability contracts.
- Record owner-specific blockers without broadening Edwin’s frontend scope.

## Files and Directories to Review

```text
src/features/profile/
src/features/test-drives/

src/components/BookingCalendar.jsx
src/components/BookingCalendar.css

src/app/App.tsx
src/app/context/auth.tsx
src/api/client.ts

src/tests/profileService.manual.ts
src/tests/passwordChange.manual.ts
src/tests/bookingHistory.manual.ts
src/tests/bookingAvailability.manual.ts
src/tests/bookingInterceptor.manual.ts

backend/routes/authRoutes.js
backend/routes/bookingRoutes.js
backend/routes/testDriveRoutes.js

README.md
```

## Integration Scenarios

```text
Authenticated /settings visit
Profile update
Invalid profile update
Correct current-password change
Incorrect current-password rejection
Expired-session password request
Booking-history load
Empty booking history
Availability load after date selection
Rapid date switching
Reserved-slot rejection
Final pre-submit availability recheck
Successful test-drive booking
Availability refresh after booking
Confirmation-email trigger
Mobile viewport smoke test
Browser console inspection
Browser network inspection
```

## Exit Gate

- Profile update works against the secured API.
- Password change works against the secured API.
- Booking history is scoped to the authenticated customer.
- Reserved hours are disabled.
- Double booking is rejected.
- Successful booking triggers the downstream email workflow.
- No release-blocking console error remains.
- Cross-team dependencies and known limitations are recorded.

## Commit

No commit unless integration fixes are required.

---

# Phase 8: Sprint 6 Release and PR Readiness

## Objective

- Run Sprint 5 regression tests.
- Run all new Sprint 6 tests.
- Run upstream image-cleanup tests.
- Run frontend and backend security audits.
- Build and preview the production bundle.
- Inspect compiled output for local endpoints and private values.
- Document Sprint 6 behavior, deployment expectations, and limitations.
- Synchronize with the latest upstream before opening the PR.
- Resolve all conflicts before administrator review.

## Files and Directories to Review or Update

```text
README.md
package.json
package-lock.json
vite.config.ts
.env.example
.gitignore

src/app/
src/api/
src/features/auth/
src/features/profile/
src/features/test-drives/
src/components/
src/pages/
src/tests/

backend/package.json
backend/package-lock.json
backend/routes/
backend/controllers/
backend/middleware/
backend/tests/
```

## Required Validation Scripts

```text
test:api-config
test:auth
test:auth-persistence
test:protected-route
test:vehicle-filters
test:profile
test:password-change
test:booking-history
test:booking-availability
test:booking-interceptor
```

## Final Validation Scope

```text
Sprint 5 authentication regressions
Sprint 6 profile validation
Sprint 6 password validation
Sprint 6 booking-history validation
Sprint 6 availability normalization
Sprint 6 booking interception
Image-cleanup regression
Frontend dependency audit
Backend runtime audit
Production build
Production preview
Protected settings route
Compiled API origin
Local endpoint scan
Private-value scan
Browser console and network drill
```

## Exit Gate

- All Sprint 5 tests pass.
- All Sprint 6 tests pass.
- Image-cleanup tests pass.
- Frontend audit reports zero vulnerabilities.
- Backend runtime audit reports zero vulnerabilities.
- Production build passes.
- Production preview passes.
- `/settings` works as a protected deep link.
- Reserved booking slots are disabled.
- No local production API endpoint is bundled.
- No private credential is bundled.
- README documents Sprint 6 behavior and limitations.
- Branch includes the latest upstream `main`.
- Branch is clean and pushed.
- PR has no merge conflicts.

## Commits

```text
Document Sprint 6 deployment and validation
Merge upstream main and resolve Sprint 6 conflicts
```

---

# Consolidated Sprint 6 File Map

## New Directories

```text
src/features/profile/
src/features/profile/components/
src/features/profile/hooks/
src/features/profile/services/
src/features/profile/types/
src/features/profile/utils/

src/features/test-drives/components/
src/features/test-drives/hooks/
src/features/test-drives/services/
src/features/test-drives/types/
src/features/test-drives/utils/

src/pages/Settings/
```

## New Files

```text
src/pages/Settings/SettingsPage.tsx

src/features/profile/components/ProfileSettingsPanel.tsx
src/features/profile/components/ProfileSettingsPanel.css
src/features/profile/components/ProfileSummaryCard.tsx
src/features/profile/components/ProfileForm.tsx
src/features/profile/components/ProfileForm.css
src/features/profile/components/PasswordChangeForm.tsx
src/features/profile/components/PasswordChangeForm.css
src/features/profile/components/BookingHistory.tsx
src/features/profile/components/BookingHistory.css
src/features/profile/components/BookingHistoryCard.tsx
src/features/profile/components/BookingStatusBadge.tsx

src/features/profile/hooks/useProfile.ts
src/features/profile/hooks/usePasswordChange.ts
src/features/profile/hooks/useBookingHistory.ts

src/features/profile/services/profileApi.ts

src/features/profile/types/index.ts

src/features/profile/utils/profileValidation.ts
src/features/profile/utils/passwordValidation.ts
src/features/profile/utils/bookingHistory.ts

src/features/test-drives/components/AvailabilityStatus.tsx
src/features/test-drives/components/TimeSlotPicker.tsx
src/features/test-drives/components/TimeSlotPicker.css

src/features/test-drives/hooks/useBookingAvailability.ts

src/features/test-drives/services/availabilityApi.ts

src/features/test-drives/types/index.ts

src/features/test-drives/utils/bookingDate.ts
src/features/test-drives/utils/availability.ts

src/tests/profileValidation.manual.ts
src/tests/profileService.manual.ts
src/tests/passwordValidation.manual.ts
src/tests/passwordChange.manual.ts
src/tests/bookingHistory.manual.ts
src/tests/bookingAvailability.manual.ts
src/tests/bookingInterceptor.manual.ts
```

## Existing Files Expected to Change

```text
src/app/App.tsx
src/app/context/auth.tsx
src/api/client.ts

src/components/BookingCalendar.jsx
src/components/BookingCalendar.css

src/components/ProfileSettings.tsx
src/components/Profile.css
src/pages/profile.tsx
src/pages/profile.css

package.json
package-lock.json
README.md
```

## Files That Must Not Be Reintroduced

```text
src/routes/AppRoutes.jsx
src/components/ProtectedRoute.tsx
src/store/authSlice.js
src/store/store.js
```

The Sprint 5 `AuthProvider`, active `src/app/App.tsx` router, and authentication-ready route guards remain authoritative.

---

# Cross-Team Dependencies

## Devine

```text
Profile-read endpoint
Profile-update endpoint
Password-change endpoint
Authentication and authorization behavior
Password-change rate limiting
Confirmation-email pipeline
Reminder-email pipeline
```

## Max

```text
Authenticated booking-history endpoint
Date-based availability endpoint
Atomic double-booking prevention
Booking conflict response contract
Admin notification trigger
Representative booking data
```

## Ronald

```text
Shared API error response shape
Database query performance
Production error logging
Inventory filtering compatibility
```

## Edward

```text
Sorting query parameter agreement
Marketplace sorting UI
Print stylesheet
Shared responsive styling review
```

## Edwin

```text
Settings dashboard
Profile update form
Password-change form
Booking-history interface
Availability API service
Availability interceptor
Final pre-submit availability recheck
Frontend integration evidence
Browser console and network validation
```

---

# Sprint 6 Speed Rules

```text
One inspection pass per feature
One implementation phase at a time
One targeted test before wider tests
One focused commit per completed phase
No repeated full audit before Phase 8
No duplicate router
No duplicate authentication store
No speculative backend implementation
No placeholder production claims
No phase commit before its targeted test passes
No PR before latest upstream integration
No unresolved PR conflicts left for the administrator
```

## Daily Delivery Expectations

### Day 1

```text
Sprint 6 branch created
Contracts recorded
Profile feature foundation complete
/settings route protected
```

### Day 2

```text
Profile update complete
Password update complete
Profile and password tests passing
```

### Day 3

```text
Booking-history dashboard complete
Booking history tests passing
```

### Day 4

```text
Availability service complete
Instant availability interceptor complete
Availability and interceptor tests passing
```

### Day 5

```text
Cross-functional integration drill complete
Sprint 5 and Sprint 6 regressions passing
Production build and preview passing
Documentation complete
Latest upstream integrated
Conflicts resolved
PR opened for administrator review
```

---

# Sprint 6 Success Definition

```text
Authenticated user opens /settings
Authenticated user updates approved profile details
Authenticated user changes the account password securely
Authenticated user views complete test-drive booking history
User selects a booking date
Reserved hours are fetched immediately
Reserved hours are disabled
Stale availability requests are cancelled
Final booking submission rechecks availability
Double booking is prevented
Successful booking refreshes availability
Successful booking reaches the confirmation-email workflow
All Sprint 5 regressions pass
All Sprint 6 tests pass
Production build and preview pass
No private credential is bundled
Branch is current, clean, pushed, and conflict-free
PR is ready for administrator review
```

---

# Recommended Sprint 6 Commit Sequence

```text
1. Create Sprint 6 profile feature foundation
2. Add authenticated profile update workflow
3. Add secure password change workflow
4. Add customer test drive booking history
5. Add booking availability service and hook
6. Add instant booking availability interceptor
7. Document Sprint 6 deployment and validation
8. Merge upstream main and resolve Sprint 6 conflicts
```

---

# Final Sprint 6 Readiness Checklist

```text
[ ] Correct Sprint 6 branch active
[ ] Latest origin and upstream fetched
[ ] Profile API contracts confirmed
[ ] Availability API contract confirmed
[ ] /settings protected
[ ] Profile update implemented
[ ] Password change implemented
[ ] Password values never persisted or logged
[ ] Booking history implemented
[ ] Booking history scoped to authenticated user
[ ] Availability fetch triggered by date selection
[ ] Reserved slots disabled
[ ] Stale requests cancelled
[ ] Final availability recheck implemented
[ ] Double booking blocked
[ ] Confirmation-email workflow verified
[ ] Sprint 5 regression tests pass
[ ] Sprint 6 tests pass
[ ] Image-cleanup tests pass
[ ] Frontend audit clean
[ ] Backend runtime audit clean
[ ] Production build passes
[ ] Production preview passes
[ ] Browser console and network reviewed
[ ] README updated
[ ] Latest upstream main integrated
[ ] Merge conflicts resolved
[ ] Branch clean and pushed
[ ] PR ready for administrator review
```
