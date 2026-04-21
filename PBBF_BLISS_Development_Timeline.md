# PBBF BLISS Telehealth Platform Development Timeline

## Project Context

This timeline is designed for the current repository structure already in place under:

- `bliss-telehealth/pbbf-api`
- `bliss-telehealth/pbbf-telehealth`
- `bliss-telehealth/docs`
- `bliss-telehealth/infra`
- `bliss-telehealth/scripts`

It assumes the project will continue with the locked implementation direction already established in the project documents:

- **Backend:** FastAPI modular monolith
- **Frontend:** React + Vite + Tailwind CSS
- **Database:** PostgreSQL
- **Cache / async support:** Redis where needed
- **Identity / enterprise integrations:** Microsoft-oriented path for later production alignment
- **MVP scope first:** patient portal, provider portal, scheduling, telehealth access, encounter documentation, EPDS screening, referrals, notifications, and admin reporting

---

## Working Rule for This Timeline

This document is intentionally written to support **actual development execution**.

That means each phase includes:

- a clear objective
- the directories and files to **modify** from what already exists
- the directories and files to **create** where gaps still exist
- the unit/integration tests expected in that phase
- a completion checkpoint

Where a path already exists in your repository, the instruction is to **modify or complete it**, not recreate it.

---

# Master Delivery Order

## Delivery Sequence

1. Backend foundation hardening
2. Frontend foundation hardening
3. Backend auth and role enforcement
4. Frontend auth and protected routing
5. Backend intake, scheduling, screenings, telehealth, encounters, referrals, notifications, and admin reporting
6. Frontend patient, provider, and admin flows
7. End-to-end integration and test coverage
8. Deployment hardening, documentation, and release readiness

## MVP Release Goal

The MVP is complete when:

- patients can register, sign in, complete intake, book an appointment, complete screening, and join a session
- providers can view appointments, review patient information, document encounters, and create referrals
- admins can monitor users, appointments, audit events, and basic utilization metrics
- core backend modules are covered by unit tests and key workflows are covered by integration tests
- frontend critical flows are covered by component and page-level tests

---

# Backend Development Timeline

Repository root: `bliss-telehealth/pbbf-api`

---

## Backend Phase 1 — Foundation Audit and Structural Cleanup

### Objective

Stabilize the current FastAPI codebase, remove structural ambiguity, and make the backend safe to build on without rework later.

### Existing directories to keep and complete

- `app/common/config`
- `app/common/errors`
- `app/common/events`
- `app/common/middleware`
- `app/common/permissions`
- `app/common/utils`
- `app/common/validators`
- `app/db`
- `app/db/models`
- `app/db/repositories`
- `app/modules/*`
- `scripts`
- `alembic`
- `docs`
- `infra`

### Modify these files

- `app/main.py`
- `app/__init__.py`
- `app/common/config/settings.py`
- `app/db/session.py`
- `app/db/base.py`
- `app/db/__init__.py`
- `requirements.txt`
- `scripts/seed_users.py`

### Create these files if missing

- `app/common/errors/http_exceptions.py`
- `app/common/errors/handlers.py`
- `app/common/middleware/request_context.py`
- `app/common/middleware/logging.py`
- `app/common/permissions/dependencies.py`
- `app/common/validators/pagination.py`
- `app/common/utils/datetime.py`
- `app/common/utils/pagination.py`
- `app/common/utils/response.py`
- `app/db/models/__init__.py`
- `app/db/repositories/base.py`
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_health.py`
- `tests/test_app_boot.py`

### Notes about existing structure

- The current modular layout is good. Keep it.
- The odd path `app/jobs/{__init__.py}` should be corrected into a normal Python package if it truly exists as shown.
- The repository should expose a clean app startup path and a clean test database initialization path before any feature expansion continues.

### Tests required in this phase

- app boot smoke test
- health endpoint test
- settings loading test
- DB session creation test

### Completion checkpoint

Backend starts cleanly, tests run, database session initialization is stable, and no core import-path or app boot issues remain.

---

## Backend Phase 2 — Data Models, Migrations, and Repository Base Layer

### Objective

Create or finalize the core database model layer and make migrations reliable enough for the rest of the system.

### Directories to modify

- `app/db/models`
- `app/db/repositories`
- `alembic`

### Create or complete these model files

- `app/db/models/user.py`
- `app/db/models/role.py`
- `app/db/models/patient.py`
- `app/db/models/provider.py`
- `app/db/models/appointment.py`
- `app/db/models/telehealth_session.py`
- `app/db/models/intake_submission.py`
- `app/db/models/screening.py`
- `app/db/models/encounter.py`
- `app/db/models/referral.py`
- `app/db/models/notification.py`
- `app/db/models/audit_log.py`

### Create or complete these shared repository files

- `app/db/repositories/base.py`
- `app/db/repositories/user_repository.py`
- `app/db/repositories/appointment_repository.py`
- `app/db/repositories/screening_repository.py`
- `app/db/repositories/encounter_repository.py`
- `app/db/repositories/referral_repository.py`

### Migration work

- create initial model migrations
- verify downgrade path
- seed minimal reference data such as roles

### Tests required in this phase

- model creation tests
- relationship integrity tests
- migration smoke test
- repository CRUD tests

### Completion checkpoint

All core MVP entities exist in the database, relationships are valid, and migrations can be applied on a clean database without manual intervention.

---

## Backend Phase 3 — Authentication, Authorization, and Identity Controls

### Objective

Finish secure authentication and role-based authorization for patients, providers, care coordinators, and admins.

### Existing module to complete

- `app/modules/auth`
- `app/modules/users`

### Modify these files

- `app/modules/auth/router.py`
- `app/modules/auth/schemas.py`
- `app/modules/auth/service.py`
- `app/modules/auth/repository.py`
- `app/modules/users/router.py`
- `app/modules/users/schemas.py`
- `app/modules/users/service.py`
- `app/modules/users/repository.py`
- `app/common/utils/security.py`
- `app/common/permissions/dependencies.py`

### Create these files if missing

- `app/modules/auth/dependencies.py`
- `app/modules/auth/tokens.py`
- `app/modules/users/dependencies.py`
- `tests/modules/auth/test_register.py`
- `tests/modules/auth/test_login.py`
- `tests/modules/auth/test_refresh_token.py`
- `tests/modules/auth/test_role_access.py`
- `tests/modules/users/test_user_profile.py`

### Functional outcomes expected

- patient registration
- login/logout flow
- password hashing and verification
- role-aware route protection
- current-user endpoint
- admin-only user management controls for MVP

### Tests required in this phase

- successful registration/login tests
- invalid credentials test
- unauthorized access test
- role restriction tests
- current-user endpoint test

### Completion checkpoint

Authentication and role protection are reliable enough for all later modules to use without rewriting auth logic.

---

## Backend Phase 4 — Patient Intake and Consent Workflow

### Objective

Build the intake and consent flow that establishes patient onboarding, basic profile capture, and triage readiness.

### Existing module to complete

- `app/modules/intake`

### Modify these files

- `app/modules/intake/router.py`
- `app/modules/intake/schemas.py`
- `app/modules/intake/service.py`
- `app/modules/intake/repository.py`

### Create these files if missing

- `app/modules/intake/constants.py`
- `app/modules/intake/validators.py`
- `tests/modules/intake/test_create_draft.py`
- `tests/modules/intake/test_submit_intake.py`
- `tests/modules/intake/test_consent_capture.py`

### Functional outcomes expected

- patient intake draft save
- intake submit
- consent acknowledgement capture
- emergency contact capture
- service need category capture
- intake status transitions

### Tests required in this phase

- draft save test
- final submit test
- validation error test
- consent required test
- role access test

### Completion checkpoint

Patients can complete onboarding and providers/admin workflows can consume structured intake data.

---

## Backend Phase 5 — Scheduling and Appointment Management

### Objective

Implement appointment booking, provider assignment, rescheduling, cancellation, and status control.

### Existing module to complete

- `app/modules/appointments`

### Modify these files

- `app/modules/appointments/router.py`
- `app/modules/appointments/schemas.py`
- `app/modules/appointments/service.py`
- `app/modules/appointments/repository.py`

### Create these files if missing

- `app/modules/appointments/constants.py`
- `app/modules/appointments/availability.py`
- `tests/modules/appointments/test_booking.py`
- `tests/modules/appointments/test_reschedule.py`
- `tests/modules/appointments/test_cancel.py`
- `tests/modules/appointments/test_provider_assignment.py`

### Functional outcomes expected

- create appointment
- list appointments by role
- reschedule appointment
- cancel appointment
- appointment status tracking
- timezone-safe serialized responses

### Tests required in this phase

- booking success test
- schedule conflict test
- cancel/reschedule tests
- provider-specific listing test
- patient-specific listing test

### Completion checkpoint

Appointments move through valid lifecycle states and are accessible according to user role.

---

## Backend Phase 6 — Screenings and EPDS Logic

### Objective

Implement the first screening workflow, with EPDS scoring, risk banding, and provider review visibility.

### Existing module to complete

- `app/modules/screenings`

### Modify these files

- `app/modules/screenings/router.py`
- `app/modules/screenings/schemas.py`
- `app/modules/screenings/service.py`
- `app/modules/screenings/repository.py`

### Create these files if missing

- `app/modules/screenings/scoring.py`
- `app/modules/screenings/constants.py`
- `tests/modules/screenings/test_epds_submission.py`
- `tests/modules/screenings/test_epds_scoring.py`
- `tests/modules/screenings/test_epds_risk_flags.py`

### Functional outcomes expected

- EPDS questionnaire submission
- score calculation
- severity band classification
- critical answer flagging
- patient history retrieval
- provider review access

### Tests required in this phase

- score calculation test
- banding logic test
- critical response flag test
- screening history test

### Completion checkpoint

The system stores valid EPDS results, classifies them consistently, and exposes them safely to the care team.

---

## Backend Phase 7 — Telehealth Session Access and Encounter Documentation

### Objective

Support virtual session access and provider documentation during or after visits.

### Existing modules to complete

- `app/modules/telehealth`
- `app/modules/encounters`

### Modify these files

- `app/modules/telehealth/router.py`
- `app/modules/telehealth/schemas.py`
- `app/modules/telehealth/service.py`
- `app/modules/telehealth/repository.py`
- `app/modules/encounters/router.py`
- `app/modules/encounters/schemas.py`
- `app/modules/encounters/service.py`
- `app/modules/encounters/repository.py`

### Create these files if missing

- `app/modules/telehealth/providers.py`
- `app/modules/encounters/templates.py`
- `tests/modules/telehealth/test_session_access.py`
- `tests/modules/telehealth/test_session_status.py`
- `tests/modules/encounters/test_create_note.py`
- `tests/modules/encounters/test_finalize_note.py`

### Functional outcomes expected

- telehealth session metadata creation
- role-aware join access
- join timestamps
- session status changes
- encounter creation by appointment
- note draft/save/finalize flow
- follow-up plan capture

### Tests required in this phase

- authorized join test
- unauthorized join test
- session state lifecycle test
- encounter note save/finalize tests

### Completion checkpoint

Patients can access a scheduled visit, and providers can document the visit in a structured manner.

---

## Backend Phase 8 — Referrals, Notifications, Audit, and Admin Reporting

### Objective

Complete the operational backbone required for follow-up, accountability, and basic reporting.

### Existing modules to complete

- `app/modules/referrals`
- `app/modules/notifications`
- `app/modules/audit`
- `app/modules/admin`

### Modify these files

- `app/modules/referrals/router.py`
- `app/modules/referrals/schemas.py`
- `app/modules/referrals/service.py`
- `app/modules/referrals/repository.py`
- `app/modules/notifications/router.py`
- `app/modules/notifications/schemas.py`
- `app/modules/notifications/service.py`
- `app/modules/notifications/repository.py`
- `app/modules/audit/router.py`
- `app/modules/audit/schemas.py`
- `app/modules/audit/service.py`
- `app/modules/audit/repository.py`
- `app/modules/admin/router.py`
- `app/modules/admin/schemas.py`
- `app/modules/admin/service.py`
- `app/modules/admin/repository.py`

### Create these files if missing

- `app/modules/notifications/channels.py`
- `app/modules/notifications/tasks.py`
- `app/modules/admin/metrics.py`
- `tests/modules/referrals/test_create_referral.py`
- `tests/modules/referrals/test_update_referral_status.py`
- `tests/modules/notifications/test_reminder_creation.py`
- `tests/modules/audit/test_audit_logging.py`
- `tests/modules/admin/test_dashboard_metrics.py`

### Functional outcomes expected

- referral creation and tracking
- reminder creation hooks
- notification delivery logging
- audit event persistence
- admin dashboard metrics endpoints

### Tests required in this phase

- referral status test
- notification creation test
- audit log write test
- admin summary metrics test

### Completion checkpoint

Admins and care teams can track operational activity and reporting basics without manual spreadsheet work.

---

## Backend Phase 9 — Background Jobs, Seed Data, and Integration Test Layer

### Objective

Prepare the backend for realistic QA and deployment by adding asynchronous job support, reliable seeds, and broader integration coverage.

### Directories to modify

- `app/jobs`
- `scripts`
- `tests`

### Modify these files

- `scripts/seed_users.py`

### Create these files if missing

- `app/jobs/__init__.py`
- `app/jobs/reminder_jobs.py`
- `app/jobs/notification_jobs.py`
- `scripts/seed_roles.py`
- `scripts/seed_reference_data.py`
- `tests/integration/test_patient_journey.py`
- `tests/integration/test_provider_journey.py`
- `tests/integration/test_admin_journey.py`

### Tests required in this phase

- end-to-end API workflow tests
- seeded data boot test
- background task smoke test

### Completion checkpoint

The backend can simulate realistic multi-step workflows, not just isolated unit-level behavior.

---

## Backend Phase 10 — Production Hardening and API Documentation

### Objective

Make the backend release-ready for staging or MVP deployment.

### Directories to modify

- `docs`
- `infra`
- `app/common`
- `tests`

### Modify these files

- `app/main.py`
- `app/common/config/settings.py`
- `requirements.txt`

### Create these files if missing

- `docs/backend-api.md`
- `docs/backend-env.md`
- `docs/backend-test-strategy.md`
- `infra/docker-compose.backend.yml`
- `infra/Dockerfile.backend`
- `infra/nginx.backend.conf`
- `tests/test_security_headers.py`
- `tests/test_rate_limit_smoke.py`

### Hardening outcomes expected

- environment separation
- production config sanity
- CORS policy review
- logging policy review
- error response consistency
- Swagger/OpenAPI cleanup

### Completion checkpoint

Backend is testable, documented, and deployable with far less risk of environment-specific failure.

---

# Frontend Development Timeline

Repository root: `bliss-telehealth/pbbf-telehealth`

---

## Frontend Phase 1 — Structural Audit and UI Foundation Cleanup

### Objective

Clean and standardize the current React structure so new features land into a coherent application shell instead of scattered files.

### Existing directories to keep and complete

- `src/app`
- `src/components/layout`
- `src/components/ui`
- `src/modules/*`
- `src/pages`
- `src/providers`
- `src/routes`
- `src/services`
- `src/shared`
- `src/store`
- `public`

### Modify these files

- `src/App.jsx`
- `src/main.jsx`
- `src/app/AppLayout.jsx`
- `src/app/AppRoutes.jsx`
- `src/index.css`
- `src/App.css`
- `src/components/layout/AppShell.jsx`
- `src/components/layout/Sidebar.jsx`
- `src/components/layout/Topbar.jsx`
- `src/shared/constants/routes.js`
- `src/shared/constants/roles.js`

### Create these files if missing

- `src/shared/constants/navigation.js`
- `src/shared/utils/storage.js`
- `src/shared/utils/formatters.js`
- `src/shared/components/Loader.jsx`
- `src/shared/components/EmptyState.jsx`
- `src/shared/components/ErrorState.jsx`
- `src/test/setup.jsx`
- `src/test/renderWithProviders.jsx`

### Notes about existing structure

- The current modular split is a good base.
- Keep `src/modules/*` for feature-specific logic.
- Keep `src/pages/*` only for route-level page composition.
- Reduce duplication between `src/services/api.js` and `src/shared/services/api.js` by choosing one canonical API client.

### Tests required in this phase

- app render smoke test
- route shell render test
- sidebar navigation render test
- topbar render test

### Completion checkpoint

The frontend has one clean shell, one route map, one API client strategy, and reusable UI primitives ready for feature work.

---

## Frontend Phase 2 — Authentication UX and Route Protection

### Objective

Build the visible authentication layer and lock private areas behind role-aware guards.

### Existing directories to complete

- `src/modules/auth`
- `src/routes`
- `src/shared/guards`
- `src/store`
- `src/services`

### Modify these files

- `src/pages/auth/Login.jsx`
- `src/routes/ProtectedRoute.jsx`
- `src/shared/guards/AuthGuard.jsx`
- `src/shared/guards/RoleGuard.jsx`
- `src/store/authStore.js`
- `src/services/auth.service.js`
- `src/services/api.js`

### Create these files if missing

- `src/modules/auth/pages/Register.jsx`
- `src/modules/auth/pages/ForgotPassword.jsx`
- `src/modules/auth/components/LoginForm.jsx`
- `src/modules/auth/components/RegisterForm.jsx`
- `src/modules/auth/hooks/useAuth.js`
- `src/modules/auth/services/authApi.js`
- `src/modules/auth/utils/validators.js`
- `src/modules/auth/__tests__/LoginForm.test.jsx`
- `src/modules/auth/__tests__/RegisterForm.test.jsx`
- `src/modules/auth/__tests__/AuthGuard.test.jsx`

### UX outcomes expected

- login screen
- registration screen
- auth store hydration
- token persistence
- logout flow
- protected routes by role

### Tests required in this phase

- login form validation test
- auth store state transition test
- protected route redirect test
- role guard restriction test

### Completion checkpoint

Users can sign in and are routed only to pages allowed for their role.

---

## Frontend Phase 3 — Patient Intake and Onboarding Experience

### Objective

Implement the patient onboarding experience for registration completion, consent, and intake capture.

### Existing directories to complete

- `src/modules/intake`
- `src/pages/patient`

### Modify these files

- `src/pages/patient/Dashboard.jsx`
- `src/modules/intake/pages/*`
- `src/modules/intake/components/*`
- `src/modules/intake/hooks/*`
- `src/modules/intake/services/*`

### Create these files if missing

- `src/modules/intake/pages/IntakeFormPage.jsx`
- `src/modules/intake/pages/ConsentPage.jsx`
- `src/modules/intake/components/IntakeForm.jsx`
- `src/modules/intake/components/ConsentCheckboxes.jsx`
- `src/modules/intake/components/EmergencyContactFields.jsx`
- `src/modules/intake/hooks/useIntakeForm.js`
- `src/modules/intake/services/intakeApi.js`
- `src/modules/intake/utils/intakeSchema.js`
- `src/modules/intake/__tests__/IntakeForm.test.jsx`
- `src/modules/intake/__tests__/ConsentPage.test.jsx`

### UX outcomes expected

- guided onboarding
- draft save support
- validation feedback
- consent acknowledgement
- service need selection

### Tests required in this phase

- field validation tests
- submit success test
- consent required test

### Completion checkpoint

A patient can complete onboarding from the UI without developer-side manual DB work.

---

## Frontend Phase 4 — Patient Scheduling and Appointment Flow

### Objective

Deliver the patient-facing scheduling experience and appointment lifecycle screens.

### Existing directories to complete

- `src/modules/appointments`
- `src/pages/patient`

### Modify these files

- `src/pages/patient/Appointments.jsx`
- `src/modules/appointments/pages/*`
- `src/modules/appointments/components/*`
- `src/modules/appointments/hooks/*`
- `src/modules/appointments/services/*`

### Create these files if missing

- `src/modules/appointments/pages/BookAppointmentPage.jsx`
- `src/modules/appointments/components/AppointmentCard.jsx`
- `src/modules/appointments/components/AppointmentForm.jsx`
- `src/modules/appointments/components/AppointmentStatusBadge.jsx`
- `src/modules/appointments/hooks/useAppointments.js`
- `src/modules/appointments/services/appointmentsApi.js`
- `src/modules/appointments/__tests__/AppointmentForm.test.jsx`
- `src/modules/appointments/__tests__/AppointmentsPage.test.jsx`

### UX outcomes expected

- list appointments
- book appointment
- reschedule/cancel controls
- status visibility
- next appointment emphasis on dashboard

### Tests required in this phase

- booking form validation test
- list rendering test
- reschedule action test

### Completion checkpoint

Patients can manage appointments from the UI and see backend-driven updates reflected correctly.

---

## Frontend Phase 5 — Screenings and Patient Self-Assessment Flow

### Objective

Build the EPDS experience in a patient-safe, readable, form-driven interface.

### Existing directories to complete

- `src/modules/screenings`
- `src/pages/patient`

### Modify these files

- `src/pages/patient/Screening.jsx`
- `src/modules/screenings/pages/*`
- `src/modules/screenings/components/*`
- `src/modules/screenings/hooks/*`
- `src/modules/screenings/services/*`

### Create these files if missing

- `src/modules/screenings/components/EpdsQuestionnaire.jsx`
- `src/modules/screenings/components/ScoreSummaryCard.jsx`
- `src/modules/screenings/hooks/useEpdsForm.js`
- `src/modules/screenings/services/screeningsApi.js`
- `src/modules/screenings/utils/epdsQuestions.js`
- `src/modules/screenings/__tests__/EpdsQuestionnaire.test.jsx`
- `src/modules/screenings/__tests__/ScreeningPage.test.jsx`

### UX outcomes expected

- questionnaire rendering
- submission flow
- completion confirmation
- prior screening visibility where allowed

### Tests required in this phase

- required-answer test
- scoring submit display test
- page render test

### Completion checkpoint

Patients can complete screening without broken form state or confusing question flow.

---

## Frontend Phase 6 — Telehealth Session Access and Patient Dashboard Completion

### Objective

Finish the patient dashboard around real visit readiness and telehealth access.

### Existing directories to complete

- `src/modules/telehealth`
- `src/pages/patient`
- `src/modules/notifications`

### Modify these files

- `src/pages/patient/Dashboard.jsx`
- `src/pages/patient/Session.jsx`
- `src/modules/telehealth/pages/*`
- `src/modules/telehealth/components/*`
- `src/modules/telehealth/hooks/*`
- `src/modules/notifications/components/*`

### Create these files if missing

- `src/modules/telehealth/components/JoinSessionCard.jsx`
- `src/modules/telehealth/components/DeviceCheckPanel.jsx`
- `src/modules/telehealth/hooks/useSessionAccess.js`
- `src/modules/telehealth/services/telehealthApi.js`
- `src/modules/notifications/components/ReminderBanner.jsx`
- `src/modules/telehealth/__tests__/JoinSessionCard.test.jsx`
- `src/modules/telehealth/__tests__/SessionPage.test.jsx`

### UX outcomes expected

- session join CTA
- appointment readiness messaging
- basic device guidance
- waiting or session state display
- reminder surfacing on dashboard

### Tests required in this phase

- join button state test
- no-session state test
- dashboard reminder display test

### Completion checkpoint

A patient can enter the portal and clearly understand how to join the next visit.

---

## Frontend Phase 7 — Provider Workspace: Dashboard, Notes, and Referrals

### Objective

Build the provider-facing workflow for appointments, chart context, notes, and referrals.

### Existing directories to complete

- `src/pages/provider`
- `src/modules/encounters`
- `src/modules/referrals`
- `src/modules/appointments`

### Modify these files

- `src/pages/provider/Dashboard.jsx`
- `src/pages/provider/Notes.jsx`
- `src/pages/provider/Referrals.jsx`
- `src/modules/encounters/pages/*`
- `src/modules/encounters/components/*`
- `src/modules/referrals/pages/*`
- `src/modules/referrals/components/*`

### Create these files if missing

- `src/modules/encounters/components/EncounterEditor.jsx`
- `src/modules/encounters/components/PatientSummaryCard.jsx`
- `src/modules/encounters/hooks/useEncounterEditor.js`
- `src/modules/encounters/services/encountersApi.js`
- `src/modules/referrals/components/ReferralForm.jsx`
- `src/modules/referrals/components/ReferralTimeline.jsx`
- `src/modules/referrals/hooks/useReferrals.js`
- `src/modules/referrals/services/referralsApi.js`
- `src/modules/encounters/__tests__/EncounterEditor.test.jsx`
- `src/modules/referrals/__tests__/ReferralForm.test.jsx`

### UX outcomes expected

- provider dashboard with appointments
- patient summary context
- encounter note drafting/finalization
- referral creation and tracking
- screening alert visibility

### Tests required in this phase

- encounter form save test
- referral submission test
- provider dashboard render test

### Completion checkpoint

Providers can complete their main clinical workflow from the frontend without fallback manual tools.

---

## Frontend Phase 8 — Admin Workspace and Reporting Basics

### Objective

Implement the admin-facing area for users, oversight, reporting, and audit visibility.

### Existing directories to complete

- `src/pages/admin`
- `src/modules/admin`

### Modify these files

- `src/pages/admin/Dashboard.jsx`
- `src/pages/admin/Users.jsx`
- `src/pages/admin/AuditLogs.jsx`
- `src/pages/admin/Reports.jsx`
- `src/pages/admin/Settings.jsx`
- `src/modules/admin/pages/*`
- `src/modules/admin/components/*`
- `src/modules/admin/services/*`

### Create these files if missing

- `src/modules/admin/components/KpiCard.jsx`
- `src/modules/admin/components/UtilizationChart.jsx`
- `src/modules/admin/components/AuditLogTable.jsx`
- `src/modules/admin/hooks/useAdminMetrics.js`
- `src/modules/admin/services/adminApi.js`
- `src/modules/admin/__tests__/AdminDashboard.test.jsx`
- `src/modules/admin/__tests__/AuditLogTable.test.jsx`

### UX outcomes expected

- KPI display
- user list management view
- audit log list/filter view
- report snapshot display

### Tests required in this phase

- dashboard metrics render test
- audit table render test
- admin route protection test

### Completion checkpoint

Admins can monitor the platform from a real interface, not just backend endpoints.

---

## Frontend Phase 9 — Shared UX Hardening, Error States, and Accessibility Pass

### Objective

Refine the product so it feels dependable, understandable, and consistent across roles.

### Directories to modify

- `src/shared/components`
- `src/components/ui`
- `src/modules/*`
- `src/pages/*`

### Create or complete these files

- `src/shared/components/FormErrorSummary.jsx`
- `src/shared/components/PageHeader.jsx`
- `src/shared/components/SectionCard.jsx`
- `src/shared/hooks/useToast.js`
- `src/shared/utils/a11y.js`
- `src/components/ui/Input.jsx`
- `src/components/ui/Select.jsx`
- `src/components/ui/Modal.jsx`
- `src/components/ui/Table.jsx`
- `src/components/ui/Textarea.jsx`
- `src/components/ui/Tabs.jsx`
- `src/components/ui/__tests__/Button.test.jsx`
- `src/components/ui/__tests__/Card.test.jsx`

### Hardening outcomes expected

- consistent empty/loading/error states
- keyboard navigation pass
- form feedback improvements
- reusable page header and section layout patterns

### Tests required in this phase

- component interaction tests
- accessibility smoke tests
- shared UI render tests

### Completion checkpoint

The product behaves consistently across patient, provider, and admin experiences.

---

## Frontend Phase 10 — Integration, E2E Readiness, and Deployment Support

### Objective

Prepare the frontend for staging and real integrated QA.

### Directories to modify

- `src`
- `public`
- project root config files

### Modify these files

- `package.json`
- `vite.config.js`
- `eslint.config.js`
- `README.md`

### Create these files if missing

- `src/test/msw/server.js`
- `src/test/msw/handlers.js`
- `src/test/e2e/patient-flow.spec.js`
- `src/test/e2e/provider-flow.spec.js`
- `src/test/e2e/admin-flow.spec.js`
- `.env.example`
- `docs/frontend-testing.md`
- `docs/frontend-deployment.md`

### Tests required in this phase

- mocked integration tests
- patient flow e2e test
- provider flow e2e test
- admin flow e2e test

### Completion checkpoint

Frontend is ready for connected QA against the backend and can be packaged for staging deployment with confidence.

---

# Suggested Cross-Project Test Layout

## Backend

```text
pbbf-api/
└── tests/
    ├── conftest.py
    ├── test_app_boot.py
    ├── test_health.py
    ├── integration/
    │   ├── test_patient_journey.py
    │   ├── test_provider_journey.py
    │   └── test_admin_journey.py
    └── modules/
        ├── auth/
        ├── intake/
        ├── appointments/
        ├── screenings/
        ├── telehealth/
        ├── encounters/
        ├── referrals/
        ├── notifications/
        ├── audit/
        └── admin/
```

## Frontend

```text
pbbf-telehealth/
└── src/
    ├── test/
    │   ├── setup.jsx
    │   ├── renderWithProviders.jsx
    │   ├── e2e/
    │   └── msw/
    ├── components/
    │   └── ui/__tests__/
    └── modules/
        ├── auth/__tests__/
        ├── intake/__tests__/
        ├── appointments/__tests__/
        ├── screenings/__tests__/
        ├── telehealth/__tests__/
        ├── encounters/__tests__/
        ├── referrals/__tests__/
        └── admin/__tests__/
```

---

# Recommended Build Discipline

## Backend discipline

- Do not add new modules outside `app/modules` unless they are truly cross-cutting.
- Keep schema validation in `schemas.py`, business logic in `service.py`, and persistence in `repository.py`.
- Every phase that adds persistence should add tests in the same phase.
- Migrations should be generated and applied immediately after model changes.

## Frontend discipline

- Route pages should stay thin.
- Reusable UI belongs in `src/components/ui` or `src/shared/components`.
- Feature logic belongs inside the corresponding `src/modules/<feature>` directory.
- Do not duplicate API clients or auth state utilities across directories.

---

# Final Execution Note

This timeline is built to help the team move phase by phase without losing track of what already exists.

The practical rule is simple:

- **Modify and complete existing paths first**
- **Create only the missing pieces needed for the current phase**
- **Add tests in the same phase, not later**
- **Do not jump to mobile or AI before the web MVP is stable**

