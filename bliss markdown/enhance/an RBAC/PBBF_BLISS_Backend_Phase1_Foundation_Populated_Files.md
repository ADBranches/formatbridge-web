# PBBF BLISS — RBAC Actionability & Production Readiness Implementation Roadmap

**Purpose:** Convert the current RBAC-aware UI from mostly display/navigation surfaces into fully action-capable workflows for all Release 1 roles: patient, provider/counselor/lactation consultant, care coordinator, and admin.

**Release principle:** No feature should be considered production-ready because a page merely displays data. A feature is production-ready only when the correct role can perform the intended action, the action persists in the backend, the UI reflects the state change, unauthorized users are blocked, required notifications/audit events are created, and functional tests prove the workflow.

**Implementation rule:** Inspect before patching. No file changes should be made until the current file structure, API contracts, schemas, services, tests, and frontend patterns are inspected.

---

## 0. Release Actionability Definition of Done

Every role-action feature must satisfy:

- Role can perform the expected action from the UI.
- API validates input and persists state.
- UI updates after success without requiring manual database edits.
- Unauthorized roles are blocked at frontend and backend.
- Audit event is created where governance applies.
- Notification is created/sent where workflow requires communication.
- Tests exist for success, validation failure, and access denial.
- Manual QA confirms the browser flow works after refresh/logout/login.

---

## 1. Timeline Overview

### Recommended duration

**4 to 6 focused implementation weeks**, depending on whether external email/video providers are integrated now or mocked locally for Release 1.

### Sprint breakdown

- **Sprint A — Foundation action infrastructure:** 3–5 days
- **Sprint B — Admin + RBAC user actions:** 4–6 days
- **Sprint C — Patient action workflows:** 5–7 days
- **Sprint D — Provider/care-team action workflows:** 5–8 days
- **Sprint E — Telehealth/video session management:** 5–8 days
- **Sprint F — Notifications, email, and in-app toast center:** 4–7 days
- **Sprint G — Cross-role sync, audit, release QA:** 5–7 days

---

## 2. Phase A — Inspect and Lock Action Contracts

### Objective

Create a role-action matrix and confirm which backend endpoints and frontend UI components already exist, which are display-only, and which need implementation.

### Roles covered

- Patient
- Provider
- Counselor
- Lactation consultant
- Care coordinator
- Admin
- Superuser if retained

### Backend files to inspect

- `pbbf-api/app/modules/auth/router.py`
- `pbbf-api/app/modules/auth/service.py`
- `pbbf-api/app/modules/users/router.py`
- `pbbf-api/app/modules/users/service.py`
- `pbbf-api/app/modules/users/repository.py`
- `pbbf-api/app/modules/appointments/router.py`
- `pbbf-api/app/modules/appointments/service.py`
- `pbbf-api/app/modules/telehealth/router.py`
- `pbbf-api/app/modules/telehealth/service.py`
- `pbbf-api/app/modules/encounters/router.py`
- `pbbf-api/app/modules/referrals/router.py`
- `pbbf-api/app/modules/screenings/router.py`
- `pbbf-api/app/modules/notifications/router.py`
- `pbbf-api/app/modules/admin/router.py`
- `pbbf-api/app/modules/audit/router.py`
- `pbbf-api/app/common/permissions/object_access.py`

### Frontend files to inspect

- `pbbf-telehealth/src/shared/constants/navigation.js`
- `pbbf-telehealth/src/routes/ProtectedRoute.jsx`
- `pbbf-telehealth/src/shared/guards/AuthGuard.jsx`
- `pbbf-telehealth/src/shared/guards/RoleGuard.jsx`
- `pbbf-telehealth/src/components/layout/Topbar.jsx`
- `pbbf-telehealth/src/components/layout/Sidebar.jsx`
- all role pages under:
  - `src/pages/patient/*`
  - `src/pages/provider/*`
  - `src/pages/admin/*`
  - `src/modules/*`

### Deliverables

- `docs/release/RBAC_ACTION_MATRIX.md`
- exact endpoint inventory
- missing action list
- role-to-feature authorization matrix

### Acceptance criteria

- Every sidebar item maps to a real page and real action if applicable.
- Every page has explicit owner role(s).
- Deferred features are excluded or hidden.

---

## 3. Phase B — Global Auth Actions and Session UX

### Objective

Make authentication action-complete, especially global logout, session expiry, refresh, and account recovery.

### Required user actions

#### All authenticated users

- Sign out globally from any workspace.
- Session expires and protected pages redirect to login.
- Refresh token flow renews session where valid.
- Invalid/expired session clears UI state.

#### Unauthenticated users

- Login.
- Register as patient.
- Request password reset.
- Reset password.

### Backend files to update/inspect

- `pbbf-api/app/modules/auth/router.py`
- `pbbf-api/app/modules/auth/service.py`
- `pbbf-api/app/modules/auth/repository.py`
- `pbbf-api/app/modules/auth/schemas.py`
- `pbbf-api/app/modules/auth/tokens.py`
- `pbbf-api/app/db/models/user.py`
- any session model/migration files if present

### Frontend files to update/inspect

- `pbbf-telehealth/src/components/layout/Topbar.jsx`
- `pbbf-telehealth/src/services/auth.service.js`
- `pbbf-telehealth/src/store/authStore.js`
- `pbbf-telehealth/src/modules/auth/components/LoginForm.jsx`
- `pbbf-telehealth/src/modules/auth/pages/ForgotPassword.jsx`
- `pbbf-telehealth/src/modules/auth/pages/ResetPassword.jsx`

### Tests

- `pbbf-api/tests/modules/auth/*`
- `pbbf-telehealth/src/modules/auth/__tests__/*`
- add logout UI test if not already committed

### Acceptance criteria

- Sign out button is visible globally for authenticated users.
- Logout clears session and redirects to login.
- Protected URL access after logout is blocked.
- Password reset flow is real or clearly disabled until configured.

---

## 4. Phase C — Admin RBAC Management Actions

### Objective

Turn Admin Users from a read-only table into real operational user management.

### Required admin actions

- Create/provision internal user.
- Activate/deactivate user.
- Change role.
- View user status and role.
- Audit every admin user-management action.
- Prevent non-admin access.

### Backend files to update/inspect

- `pbbf-api/app/modules/users/router.py`
- `pbbf-api/app/modules/users/service.py`
- `pbbf-api/app/modules/users/repository.py`
- `pbbf-api/app/modules/users/schemas.py`
- `pbbf-api/app/modules/admin/router.py`
- `pbbf-api/app/modules/audit/service.py`
- `pbbf-api/app/db/models/user.py`
- `pbbf-api/app/db/models/role.py`

### Proposed endpoints

- `POST /api/v1/users/internal`
- `PATCH /api/v1/users/{user_id}/status`
- `PATCH /api/v1/users/{user_id}/role`

### Frontend files to update/inspect

- `pbbf-telehealth/src/pages/admin/Users.jsx`
- `pbbf-telehealth/src/modules/admin/services/adminApi.js`
- `pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js`
- create if needed:
  - `src/modules/admin/components/UserActionMenu.jsx`
  - `src/modules/admin/components/UserProvisioningModal.jsx`

### Tests

- Backend:
  - `pbbf-api/tests/modules/users/test_admin_user_actions.py`
  - `pbbf-api/tests/security/test_admin_user_boundaries.py`
- Frontend:
  - `src/modules/admin/__tests__/UsersActions.test.jsx`

### Acceptance criteria

- Admin can create internal user.
- Admin can deactivate/reactivate user.
- Admin can change role.
- Deactivated user cannot login.
- Audit log records the action.
- Non-admin roles cannot perform these actions.

---

## 5. Phase D — Patient Action Workflows

### Objective

Ensure the patient role can complete all Release 1 actions, and each action updates backend state plus dependent workflows.

### Required patient actions

- Complete consent.
- Save intake draft.
- Submit intake.
- Book appointment.
- Reschedule appointment.
- Cancel appointment.
- Submit EPDS screening.
- View own screening history.
- Access telehealth session.
- View real care plan outputs.
- View in-app notifications.

### Backend files to update/inspect

- `pbbf-api/app/modules/intake/router.py`
- `pbbf-api/app/modules/intake/service.py`
- `pbbf-api/app/modules/appointments/router.py`
- `pbbf-api/app/modules/appointments/service.py`
- `pbbf-api/app/modules/screenings/router.py`
- `pbbf-api/app/modules/screenings/service.py`
- `pbbf-api/app/modules/telehealth/router.py`
- `pbbf-api/app/modules/notifications/service.py`
- `pbbf-api/app/modules/encounters/service.py`

### Frontend files to update/inspect

- `pbbf-telehealth/src/pages/patient/Dashboard.jsx`
- `pbbf-telehealth/src/pages/patient/CarePlan.jsx`
- `pbbf-telehealth/src/modules/intake/*`
- `pbbf-telehealth/src/modules/appointments/*`
- `pbbf-telehealth/src/modules/screenings/*`
- `pbbf-telehealth/src/modules/telehealth/*`
- `pbbf-telehealth/src/modules/notifications/*`

### Tests

- `pbbf-api/tests/integration/test_patient_journey.py`
- `pbbf-api/tests/security/test_cross_patient_access_denied.py`
- frontend patient action tests under relevant modules

### Acceptance criteria

- Patient actions persist after refresh/logout/login.
- Notifications are generated for scheduling actions.
- EPDS score/severity is visible after submission.
- Care plan reflects encounter/referral/screening/appointment data.
- Patient cannot access another patient’s records.

---

## 6. Phase E — Provider, Counselor, Lactation Consultant Actions

### Objective

Make the provider-family roles action-complete for assigned patients/appointments, while keeping object-level access tight.

### Required provider-family actions

- View assigned appointments.
- Open patient context for assigned appointment.
- Create encounter note for assigned appointment.
- Save draft encounter.
- Validate incomplete finalization is blocked.
- Finalize complete encounter.
- Review EPDS history/result.
- Create referral.
- Link referral to encounter where applicable.
- Update referral status where allowed.

### Role nuance

- `provider`, `counselor`, `lactation_consultant` should share provider-family workflow where clinically appropriate.
- Role-specific specialization can be added later, but access checks must be deliberate.

### Backend files to update/inspect

- `pbbf-api/app/modules/encounters/router.py`
- `pbbf-api/app/modules/encounters/service.py`
- `pbbf-api/app/modules/screenings/service.py`
- `pbbf-api/app/modules/referrals/service.py`
- `pbbf-api/app/modules/appointments/service.py`
- `pbbf-api/app/common/permissions/object_access.py`

### Frontend files to update/inspect

- `pbbf-telehealth/src/pages/provider/Dashboard.jsx`
- `pbbf-telehealth/src/pages/provider/Notes.jsx`
- `pbbf-telehealth/src/pages/provider/Referrals.jsx`
- `pbbf-telehealth/src/modules/encounters/*`
- `pbbf-telehealth/src/modules/referrals/*`
- `pbbf-telehealth/src/modules/screenings/*`

### Tests

- `pbbf-api/tests/modules/encounters/*`
- `pbbf-api/tests/modules/referrals/*`
- `pbbf-api/tests/security/test_cross_provider_access_denied.py`
- frontend provider dashboard/encounter/referral tests

### Acceptance criteria

- Assigned provider can document assigned appointment.
- Unassigned provider is blocked.
- Finalized encounter cannot be modified.
- Patient care plan updates after finalized encounter.
- Referral creation triggers audit/notification where applicable.

---

## 7. Phase F — Care Coordinator Actions

### Objective

Make care coordination a real workflow, not just a role label.

### Required care coordinator actions

- View referral queue.
- Create referral if allowed by workflow.
- Update referral status.
- Record follow-up outcome.
- See referral follow-up date.
- Trigger/update referral follow-up notification.
- View relevant patient context only as permitted.
- Be blocked from provider-only encounter finalization.
- Be blocked from admin-only user management.

### Backend files to update/inspect

- `pbbf-api/app/modules/referrals/router.py`
- `pbbf-api/app/modules/referrals/service.py`
- `pbbf-api/app/modules/referrals/repository.py`
- `pbbf-api/app/modules/notifications/service.py`
- `pbbf-api/app/common/permissions/object_access.py`

### Frontend files to update/inspect

- `pbbf-telehealth/src/shared/constants/navigation.js`
- `pbbf-telehealth/src/pages/provider/Dashboard.jsx`
- `pbbf-telehealth/src/pages/provider/Referrals.jsx`
- `pbbf-telehealth/src/modules/referrals/*`

### Tests

- `pbbf-api/tests/modules/referrals/*`
- new `pbbf-api/tests/security/test_care_coordinator_boundaries.py`
- frontend referral workflow tests

### Acceptance criteria

- Coordinator can execute referral follow-up workflow.
- Coordinator cannot finalize provider encounter notes unless explicitly allowed.
- Coordinator cannot access admin user management.
- Referral actions generate audit and notification events.

---

## 8. Phase G — Telehealth Video Conferencing and Session Management

### Objective

Move telehealth from status-only/session-link display into real session-management behavior with video-conferencing integration boundaries.

### Important decision

For Release 1, the practical production-ready path should be:

- Store and manage generated meeting/session links.
- Support patient/provider join actions.
- Track join timestamps.
- Track session lifecycle.
- Use an external video provider link for actual video room, such as Teams/Bookings or an approved meeting URL.
- Do not build raw custom video infrastructure unless explicitly funded and approved.

### Required actions

#### Patient

- View upcoming telehealth session.
- Run device/browser guidance or readiness check.
- Join session.
- Patient join timestamp persists.

#### Provider

- Launch/join assigned session.
- Provider join timestamp persists.
- Move session status waiting → in_progress → ended.
- Mark no-show where appropriate.

#### Admin/care coordinator

- View session status operationally where allowed.
- Investigate no-show/completion counts.

### Backend files to update/inspect

- `pbbf-api/app/modules/telehealth/router.py`
- `pbbf-api/app/modules/telehealth/service.py`
- `pbbf-api/app/modules/telehealth/repository.py`
- `pbbf-api/app/modules/telehealth/schemas.py`
- `pbbf-api/app/db/models/telehealth_session.py`
- `pbbf-api/app/modules/notifications/service.py`
- `pbbf-api/app/modules/audit/service.py`

### Frontend files to update/inspect

- `pbbf-telehealth/src/modules/telehealth/components/JoinSessionCard.jsx`
- `pbbf-telehealth/src/modules/telehealth/components/DeviceCheckPanel.jsx`
- `pbbf-telehealth/src/modules/telehealth/hooks/useSessionAccess.js`
- `pbbf-telehealth/src/modules/telehealth/services/telehealthApi.js`
- `pbbf-telehealth/src/pages/patient/Session.jsx`
- provider session launch UI if present

### Proposed endpoints

- `POST /api/v1/telehealth/sessions/{session_id}/join`
- `POST /api/v1/telehealth/sessions/{session_id}/start`
- `POST /api/v1/telehealth/sessions/{session_id}/end`
- `POST /api/v1/telehealth/sessions/{session_id}/no-show`
- `POST /api/v1/telehealth/sessions/{session_id}/meeting-link`

### Tests

- `pbbf-api/tests/modules/telehealth/*`
- frontend `SessionPage`, `JoinSessionCard`, `SessionResilience` tests

### Acceptance criteria

- Join action opens/redirects to valid meeting link.
- Patient/provider timestamps persist.
- Unauthorized users cannot join unrelated sessions.
- Status transitions are enforced.
- No-show creates notification/follow-up event.

---

## 9. Phase H — Notification Engine, Toasts, and Email

### Objective

Implement notifications as real workflow outputs, visible in-app and deliverable by email.

### Required notification triggers

- Appointment booked confirmation.
- Appointment reminder.
- Rescheduled appointment notice.
- Cancelled appointment notice.
- Missed visit/no-show follow-up.
- Referral follow-up reminder.
- Encounter/care-plan available notification if enabled.
- Admin/user-management notification where appropriate.

### Required surfaces

#### In-app

- Global notification/toast provider.
- Toast on successful action.
- Notification center or dropdown for pending/user notifications.
- Read/mark as read action.

#### Email

- Email dispatch abstraction.
- Local/dev console or file provider.
- Production SMTP/provider integration flag.
- Delivery status update: pending/sent/failed.
- Retry-safe jobs.

### Backend files to update/inspect

- `pbbf-api/app/modules/notifications/router.py`
- `pbbf-api/app/modules/notifications/service.py`
- `pbbf-api/app/modules/notifications/repository.py`
- `pbbf-api/app/modules/notifications/channels.py`
- `pbbf-api/app/jobs/notification_jobs.py`
- `pbbf-api/app/jobs/reminder_jobs.py`
- `pbbf-api/app/db/models/notification.py`

### Frontend files to update/inspect

- `pbbf-telehealth/src/modules/notifications/components/ReminderBanner.jsx`
- create if needed:
  - `src/modules/notifications/components/NotificationCenter.jsx`
  - `src/modules/notifications/components/ToastProvider.jsx`
  - `src/modules/notifications/hooks/useNotifications.js`
  - `src/modules/notifications/services/notificationsApi.js`
- `src/components/layout/Topbar.jsx`

### Tests

- `pbbf-api/tests/modules/notifications/*`
- frontend notification tests
- integration tests over appointment/referral/no-show flows

### Acceptance criteria

- Workflow actions create notifications.
- Notifications are visible to the correct user.
- Toast appears after action success/failure.
- Email provider dispatch updates delivery status.
- Failed email delivery records reason and can be retried.
- Notifications are not confused with future secure clinical messaging.

---

## 10. Phase I — Admin Reports and Audit Actionability

### Objective

Make admin reporting and audit review action-capable, not just display-only.

### Required admin actions

- Export operational report CSV.
- Filter audit logs server-side.
- Page through audit logs.
- Inspect audit event details.
- Confirm dashboard metrics change after workflow actions.

### Backend files to update/inspect

- `pbbf-api/app/modules/admin/router.py`
- `pbbf-api/app/modules/admin/service.py`
- `pbbf-api/app/modules/admin/repository.py`
- `pbbf-api/app/modules/audit/router.py`
- `pbbf-api/app/modules/audit/service.py`
- `pbbf-api/app/modules/audit/repository.py`

### Frontend files to update/inspect

- `pbbf-telehealth/src/pages/admin/Reports.jsx`
- `pbbf-telehealth/src/pages/admin/AuditLogs.jsx`
- `pbbf-telehealth/src/modules/admin/components/AuditLogTable.jsx`
- `pbbf-telehealth/src/modules/admin/services/adminApi.js`

### Proposed endpoints

- `GET /api/v1/admin/reports/operational.csv`
- existing `GET /api/v1/audit/?action=&entity_type=&actor_user_id=&date_from=&date_to=&limit=&offset=`

### Acceptance criteria

- Admin can download CSV report.
- CSV data matches dashboard definitions.
- Audit filtering uses backend query params.
- Audit pagination works from UI.
- Non-admin access is blocked.

---

## 11. Phase J — Cross-Role Workflow Sync

### Objective

Validate that user actions create the expected downstream effects for other roles.

### Required event loops

#### Patient → Provider

- Patient submits intake.
- Provider/care team can see readiness/context where allowed.

#### Patient → Provider/Admin

- Patient books appointment.
- Provider sees assigned appointment.
- Admin appointment metrics update.
- Patient receives confirmation/reminder notification.

#### Patient → Provider

- Patient submits EPDS.
- Provider can review result.
- Critical flag appears where applicable.
- Admin critical screening metric updates.

#### Provider → Patient

- Provider finalizes encounter.
- Patient care plan updates.
- Patient receives care plan/follow-up notification if enabled.

#### Provider/Care Coordinator → Patient/Admin

- Staff creates referral.
- Patient care plan shows referral.
- Admin referral metrics update.
- Referral follow-up notification is created.
- Audit event is created.

### Tests

- `pbbf-api/tests/integration/test_patient_journey.py`
- new `pbbf-api/tests/integration/test_cross_role_release_journey.py`
- frontend journey smoke tests where feasible

### Acceptance criteria

- State changes flow across roles.
- Role boundaries remain intact.
- Audit/notification side effects are verifiable.

---

## 12. Phase K — Manual Production Readiness QA

### Objective

Perform browser-based release acceptance after action implementation is complete.

### QA path

1. Admin action QA
2. Patient action QA
3. Provider action QA
4. Care coordinator action QA
5. Cross-role sync QA
6. Notification/toast/email QA
7. Telehealth/video session QA
8. Deferred feature boundary QA
9. DB migration/env closure
10. Release tag

### Acceptance criteria

- All role action flows pass.
- No broken sidebar links.
- No stale placeholder actions.
- No deferred features presented as shipped.
- No console errors during normal workflows.
- Seed scripts are idempotent and demo credentials are valid.
- Backend and frontend full suites pass.

---

## 13. Immediate Next Inspection Pack

Before any patching, inspect these first.

### Admin users/action inspection

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

sed -n '1,420p' pbbf-api/app/modules/users/router.py
sed -n '1,520p' pbbf-api/app/modules/users/service.py
sed -n '1,520p' pbbf-api/app/modules/users/repository.py
sed -n '1,420p' pbbf-api/app/modules/users/schemas.py
sed -n '1,420p' pbbf-telehealth/src/pages/admin/Users.jsx
sed -n '1,360p' pbbf-telehealth/src/modules/admin/services/adminApi.js
```

### Notification/toast inspection

```bash
sed -n '1,420p' pbbf-api/app/modules/notifications/service.py
sed -n '1,420p' pbbf-api/app/modules/notifications/router.py
sed -n '1,420p' pbbf-api/app/modules/notifications/channels.py
find pbbf-telehealth/src/modules/notifications -type f -maxdepth 4 -print -exec sed -n '1,240p' {} \;
find pbbf-telehealth/src -iname '*toast*' -o -iname '*notification*'
```

### Telehealth/video inspection

```bash
sed -n '1,520p' pbbf-api/app/modules/telehealth/router.py
sed -n '1,620p' pbbf-api/app/modules/telehealth/service.py
sed -n '1,520p' pbbf-api/app/modules/telehealth/repository.py
sed -n '1,420p' pbbf-api/app/db/models/telehealth_session.py
find pbbf-telehealth/src/modules/telehealth -type f -maxdepth 4 -print -exec sed -n '1,260p' {} \;
```

### Reports/audit action inspection

```bash
sed -n '1,420p' pbbf-api/app/modules/admin/router.py
sed -n '1,520p' pbbf-api/app/modules/admin/service.py
sed -n '1,520p' pbbf-api/app/modules/audit/router.py
sed -n '1,420p' pbbf-telehealth/src/pages/admin/Reports.jsx
sed -n '1,420p' pbbf-telehealth/src/pages/admin/AuditLogs.jsx
sed -n '1,420p' pbbf-telehealth/src/modules/admin/components/AuditLogTable.jsx
```

---

## 14. Priority Recommendation

Implement in this exact priority order:

1. **Phase B:** Global logout/session UX if not already committed.
2. **Phase C:** Admin user actions: activate/deactivate, role change, internal user provisioning.
3. **Phase H:** Notification center/toast/email dispatch foundation.
4. **Phase D:** Patient actions and visible notification feedback.
5. **Phase E/F:** Provider and care coordinator actions.
6. **Phase G:** Telehealth/video session lifecycle and meeting-link integration.
7. **Phase I:** Admin report export and audit UI server-side filters.
8. **Phase J/K:** Cross-role sync and final release QA.

---

## 15. Commit Strategy

Use one commit per functional action package:

- `feat: add global authenticated logout action`
- `feat: implement admin user management actions`
- `feat: add in-app notification center and toast feedback`
- `feat: complete patient action workflows`
- `feat: complete provider and coordinator action workflows`
- `feat: harden telehealth session lifecycle actions`
- `feat: add admin report export and audit filters`
- `test: add cross-role release workflow coverage`

Push to the same branch only after each package passes backend/frontend tests.

---

## 16. Notes and Risks

- Video conferencing should be treated as meeting-link/session lifecycle integration unless the project formally approves building direct WebRTC or custom embedded video.
- Email should use a provider abstraction so local development can use console/file mode while production uses SMTP/API provider.
- Secure chat, broad education library, multilingual expansion, mobile app, and AI-assisted triage remain post-MVP unless scope is formally changed.
- Seed scripts must be hardened because existing demo users may have stale hashes and reference data seeding currently fails when duplicate baseline rows exist.
