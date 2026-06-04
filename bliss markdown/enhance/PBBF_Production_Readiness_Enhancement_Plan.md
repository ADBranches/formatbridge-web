# PBBF BLISS — Production Readiness Enhancement Plan

## Purpose
This plan turns the current BLISS Telehealth MVP into a **production-ready Release 1 surface** by removing deferred/placeholder features from the shipped UI, completing missing in-scope behaviors, normalizing role actions, wiring notifications across the operational workflows, and hardening audit/product readiness coverage. The scope is aligned to the inspected codebase and the attached MVP backlog. citeturn74search1turn76search7turn77search7

---

## Phase 0 — Guardrails and working baseline

### Objective
Freeze the current state, confirm that role-aware UI work and layout changes still build, and establish a clean implementation boundary before functional cleanup begins. citeturn76search7turn77search7

### Files to inspect/validate
- `pbbf-telehealth/src/shared/constants/navigation.js`
- `pbbf-telehealth/src/app/AppRoutes.jsx`
- `pbbf-telehealth/src/components/layout/Sidebar.jsx`
- `pbbf-telehealth/src/components/layout/Topbar.jsx`
- `pbbf-telehealth/src/components/layout/AppShell.jsx`
- `pbbf-telehealth/src/components/layout/AuthShell.jsx`
- `pbbf-api/app/modules/auth/schemas.py`
- `pbbf-api/app/modules/auth/service.py`
- `pbbf-api/app/modules/users/schemas.py`
- `pbbf-api/app/modules/users/service.py` citeturn76search7turn77search7

### Expected outcome
A stable baseline from which placeholder removal and end-to-end workflow completion can proceed without re-breaking navigation, auth payloads, or layout behavior. citeturn76search7turn77search7

---

## Phase 1 — Remove deferred and placeholder features from the shipped MVP surface

### Objective
Hide or remove UI features that the backlog explicitly defers beyond MVP or that are still obvious placeholders, so the released product only exposes features that are truly supported. The current inspection clearly identifies **Messages**, **Resources**, and **Admin Settings** as non-production-ready in their present form. citeturn74search1turn76search7turn77search7

### Files to update
#### Navigation and routing
- `pbbf-telehealth/src/shared/constants/routes.js`
- `pbbf-telehealth/src/shared/constants/navigation.js`
- `pbbf-telehealth/src/app/AppRoutes.jsx` citeturn76search7turn77search7

#### Remove/hide these pages from MVP navigation/routes
- `pbbf-telehealth/src/pages/patient/Messages.jsx`
- `pbbf-telehealth/src/pages/patient/Resources.jsx`
- `pbbf-telehealth/src/pages/admin/Settings.jsx` citeturn76search7turn77search7

#### Tests to update
- `pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx`
- any route/navigation tests that assert those pages remain visible (inspect under `pbbf-telehealth/src/app/__tests__`, `pbbf-telehealth/src/modules/admin/__tests__`, and patient page tests). citeturn76search7turn77search7

### Decision note
The static **Care Plan** page is also not yet truly production-ready, but it should be handled in its own phase because it represents an in-scope care-output concept rather than a clearly deferred backlog theme. citeturn74search1turn76search7turn77search7

---

## Phase 2 — Complete the missing in-scope auth behavior (Forgot Password)

### Objective
Close the MVP auth gap by implementing **forgot password / password recovery** properly end-to-end, or otherwise temporarily remove it from the UI until the backend exists. The inspected frontend currently calls `/auth/forgot-password`, but the inspected backend auth surface does not yet expose that endpoint, and the UI still tells users password recovery is “not available yet.” citeturn74search1turn76search7turn77search7

### Backend files to create/update
- `pbbf-api/app/modules/auth/router.py`
- `pbbf-api/app/modules/auth/schemas.py`
- `pbbf-api/app/modules/auth/service.py`
- `pbbf-api/app/modules/auth/repository.py`
- `pbbf-api/app/modules/audit/service.py` (log password-recovery events)
- `pbbf-api/app/modules/notifications/service.py` (if email/SMS recovery flow is implemented through notifications)
- optionally create a dedicated token/reset helper module if the recovery flow is not folded into existing auth helpers. citeturn74search1turn76search7turn77search7

### Frontend files to update
- `pbbf-telehealth/src/modules/auth/services/authApi.js`
- `pbbf-telehealth/src/services/auth.service.js`
- `pbbf-telehealth/src/modules/auth/pages/ForgotPassword.jsx`
- any auth tests covering recovery/error states under `pbbf-telehealth/src/modules/auth/__tests__`. citeturn76search7turn77search7

### Expected outcome
Password recovery becomes a real Release 1 capability, aligned with the backlog’s auth stories and without placeholder messaging in the shipped UI. citeturn74search1turn76search7turn77search7

---

## Phase 3 — Normalize role actions end-to-end across patient, provider-family, care coordinator, and admin

### Objective
Ensure every role can perform **exactly** the actions the MVP expects — no missing provider-family access, no accidental overexposure, and no UI route that lands on an unimplemented backend capability. The inspection already shows a mismatch where counselor/lactation-consultant support exists in some modules (e.g., encounters) but not consistently in appointment listing and other provider-family workflows. citeturn74search1turn76search7turn77search7

### Backend files to update
#### Appointments
- `pbbf-api/app/modules/appointments/service.py`
- `pbbf-api/app/modules/appointments/router.py`
- `pbbf-api/app/modules/appointments/repository.py`
- `pbbf-api/app/modules/appointments/schemas.py` citeturn76search7turn77search7

#### Telehealth
- `pbbf-api/app/modules/telehealth/service.py`
- `pbbf-api/app/modules/telehealth/router.py`
- `pbbf-api/app/modules/telehealth/repository.py` citeturn76search7turn77search7

#### Encounters
- `pbbf-api/app/modules/encounters/service.py`
- `pbbf-api/app/modules/encounters/router.py` citeturn76search7turn77search7

#### Screenings
- `pbbf-api/app/modules/screenings/service.py`
- `pbbf-api/app/modules/screenings/router.py` citeturn76search7turn77search7

#### Referrals
- `pbbf-api/app/modules/referrals/service.py`
- `pbbf-api/app/modules/referrals/router.py` citeturn76search7turn77search7

#### Common authorization layer
- `pbbf-api/app/common/permissions/object_access.py`
- any role dependency helpers already used by auth/users/intake modules. citeturn76search7turn77search7

### Frontend files to update
#### Navigation and route exposure
- `pbbf-telehealth/src/shared/constants/navigation.js`
- `pbbf-telehealth/src/app/AppRoutes.jsx`
- `pbbf-telehealth/src/shared/guards/RoleGuard.jsx` citeturn76search7turn77search7

#### Provider-family / coordinator action surfaces
- `pbbf-telehealth/src/pages/provider/Dashboard.jsx`
- `pbbf-telehealth/src/pages/provider/Notes.jsx`
- `pbbf-telehealth/src/pages/provider/Referrals.jsx`
- `pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js`
- `pbbf-telehealth/src/modules/appointments/services/appointmentsApi.js` citeturn76search7turn77search7

### Expected outcome
- `provider`, `counselor`, and `lactation_consultant` all have coherent provider-family workflows where intended.
- `care_coordinator` gets a deliberate provider-lite/admin-lite action map instead of accidental behavior.
- the UI only exposes actions that the backend truly supports. citeturn74search1turn76search7turn77search7

---

## Phase 4 — Complete notifications across the MVP workflows

### Objective
Upgrade notifications from a partial foundation into a full MVP operational notification flow. The inspected code shows notifications are real at the service/repository layer and referral follow-up hooks exist, but appointment confirmations, reminders, reschedules, cancellations, and no-show follow-up are not yet wired through the core appointment workflow. citeturn74search1turn76search7turn77search7

### Backend files to update
#### Notifications core
- `pbbf-api/app/modules/notifications/service.py`
- `pbbf-api/app/modules/notifications/repository.py`
- `pbbf-api/app/modules/notifications/schemas.py`
- `pbbf-api/app/modules/notifications/router.py`
- `pbbf-api/app/modules/notifications/tasks.py`
- `pbbf-api/app/modules/notifications/channels.py` citeturn76search7turn77search7

#### Appointment workflow trigger points
- `pbbf-api/app/modules/appointments/service.py`
- potentially `pbbf-api/app/modules/telehealth/service.py` for visit reminders or missed-visit follow-up transitions. citeturn74search1turn76search7turn77search7

#### Referral hook already present — should be retained and extended if needed
- `pbbf-api/app/modules/referrals/service.py` citeturn76search7turn77search7

### Frontend files to update/create
- inspect/extend notification UI under `pbbf-telehealth/src/modules/notifications/`
- `pbbf-telehealth/src/modules/notifications/components/ReminderBanner.jsx`
- create notification hooks/services/pages if the MVP requires a visible operational/user notification surface beyond the reminder banner. citeturn74search1turn76search7turn77search7

### Expected outcome
- appointment confirmation notification created on booking
- appointment reminder notification created/scheduled before visit
- reschedule/cancellation notifications created on status changes
- referral follow-up notification remains working
- queue/send/fail status remains visible for operations/admin workflows. citeturn74search1turn76search7turn77search7

---

## Phase 5 — Convert Care Plan from demo/static to real care output

### Objective
Replace the hardcoded `CarePlan.jsx` demo-like experience with a real patient-facing care outputs view derived from encounter follow-up plans, referrals, screening summaries, and possibly selected appointment/follow-up data. The backlog expects encounter documentation and follow-up outputs to reach the patient where the design requires it. citeturn74search1turn76search7turn77search7

### Frontend files to update/create
- `pbbf-telehealth/src/pages/patient/CarePlan.jsx`
- create a dedicated hook if needed, e.g. `pbbf-telehealth/src/modules/encounters/hooks/useCarePlan.js`
- create a matching frontend service if needed, e.g. `pbbf-telehealth/src/modules/encounters/services/carePlanApi.js` citeturn74search1turn76search7turn77search7

### Backend files to update/create
- `pbbf-api/app/modules/encounters/router.py`
- `pbbf-api/app/modules/encounters/service.py`
- `pbbf-api/app/modules/encounters/repository.py`
- possibly add a patient-facing “care plan summary” endpoint if one does not already exist. citeturn74search1turn76search7turn77search7

### Expected outcome
The patient care-plan surface becomes a real clinical follow-up view rather than a static demo page. citeturn74search1turn76search7turn77search7

---

## Phase 6 — Admin and audit hardening

### Objective
Keep admin reporting and audit visibility in MVP scope, but harden them into a production-ready operational surface rather than a fragile demo/report snapshot experience. The inspected admin and audit modules already exist and are broadly aligned with the backlog. citeturn74search1turn76search7turn77search7

### Backend files to update
- `pbbf-api/app/modules/admin/router.py`
- `pbbf-api/app/modules/admin/service.py`
- `pbbf-api/app/modules/admin/repository.py`
- `pbbf-api/app/modules/admin/metrics.py`
- `pbbf-api/app/modules/audit/router.py`
- `pbbf-api/app/modules/audit/service.py`
- `pbbf-api/app/modules/audit/repository.py` citeturn74search1turn76search7turn77search7

### Frontend files to update
- `pbbf-telehealth/src/pages/admin/Dashboard.jsx`
- `pbbf-telehealth/src/pages/admin/Reports.jsx`
- `pbbf-telehealth/src/pages/admin/AuditLogs.jsx`
- `pbbf-telehealth/src/pages/admin/Users.jsx`
- `pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js`
- `pbbf-telehealth/src/modules/admin/components/AuditLogTable.jsx`
- `pbbf-telehealth/src/modules/admin/components/UtilizationChart.jsx` citeturn74search1turn76search7turn77search7

### Expected outcome
Admin users retain dashboards, reports, users, and audit visibility — but without placeholder settings and with audit/notification/reporting behavior better aligned to real operational review. citeturn74search1turn76search7turn77search7

---

## Phase 7 — Production readiness tests and release closure

### Objective
Bring the product to a release-quality definition of done by extending backend and frontend tests to cover the cleaned MVP surface, role-action boundaries, notification triggers, and admin/audit/reporting visibility. The backlog’s own definition of done explicitly requires user-facing flow, API behavior, validation, role access, audit handling where applicable, and functional tests. citeturn74search1turn76search7turn77search7

### Files to create/update
#### Backend tests
- `pbbf-api/tests/modules/appointments/*`
- `pbbf-api/tests/modules/telehealth/*`
- `pbbf-api/tests/modules/encounters/*`
- `pbbf-api/tests/modules/screenings/*`
- `pbbf-api/tests/modules/referrals/*`
- `pbbf-api/tests/modules/notifications/*`
- `pbbf-api/tests/modules/admin/*`
- `pbbf-api/tests/modules/audit/*`
- `pbbf-api/tests/security/*` for role/action boundary checks. citeturn76search7turn77search7

#### Frontend tests
- `pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx`
- `pbbf-telehealth/src/shared/guards/__tests__/*`
- `pbbf-telehealth/src/modules/auth/__tests__/*`
- `pbbf-telehealth/src/modules/appointments/__tests__/*`
- `pbbf-telehealth/src/modules/telehealth/__tests__/*`
- `pbbf-telehealth/src/modules/screenings/__tests__/*`
- `pbbf-telehealth/src/modules/referrals/__tests__/*`
- `pbbf-telehealth/src/modules/admin/__tests__/*`
- add/extend notification tests in `pbbf-telehealth/src/modules/notifications/` if those surfaces expand beyond the reminder banner. citeturn76search7turn77search7

### Expected outcome
A product-ready MVP that no longer exposes deferred placeholders and that has defensible functional coverage for the retained Release 1 feature set. citeturn74search1turn76search7turn77search7

---

## Recommended implementation order
1. **Phase 1** — remove/hide deferred placeholder UI features
2. **Phase 2** — implement forgot password properly
3. **Phase 3** — normalize role actions
4. **Phase 4** — wire notifications end-to-end
5. **Phase 5** — convert care plan into real care outputs
6. **Phase 6** — harden admin + audit surfaces
7. **Phase 7** — test, verify, and close release boundary. citeturn74search1turn76search7turn77search7

---

## Release boundary reminder
This plan is intentionally designed to deliver the product implied by the inspected codebase and the Release 1 backlog — **not** to expand scope into deferred secure messaging, broad resource-library delivery, multilingual expansion, or other later-phase items before the MVP is genuinely complete. citeturn74search1turn76search7turn77search7
