# PBBF BLISS Telehealth — Project Hardening README

**Purpose:** This README is the implementation guide to tighten the current PBBF BLISS telehealth project from a strong MVP shell into a safer, better-aligned, controlled pilot-ready product.

**Repository roots:**

```text
bliss-telehealth/
├── pbbf-api/           # FastAPI backend
├── pbbf-telehealth/    # React/Vite frontend
├── docs/               # Shared governance, rollout, QA, security docs
├── infra/              # Shared infrastructure assets
└── scripts/            # Shared scripts
```

---

## 1. Executive Verdict

The project has strong MVP coverage and a substantial Phase 2 hardening structure, but it is **not yet fully production-ready**.

### Current state

```text
Backend MVP coverage:              Strong
Backend Phase 2 hardening:         Partial
Frontend MVP UI shell:             Strong
Frontend/backend integration:      Partial with several contract mismatches
Production readiness:              Not yet
Controlled pilot readiness:        Likely after P0/P1 fixes and passing tests
```

### Main reason production readiness is not confirmed

The project does not mainly suffer from missing modules. The modules exist. The main issues are:

1. Frontend/backend API contracts do not fully agree.
2. Object-level authorization is inconsistent in some backend workflows.
3. Audit coverage exists but is not consistently wired across sensitive workflows.
4. Token/session/logout governance is incomplete.
5. Some operational scripts and health endpoints need safer production guardrails.
6. Some frontend features are route shells or placeholders but look production-facing.

---

## 2. MVP vs Phase 2 Boundary

### Keep in MVP / controlled pilot scope

```text
- Patient registration and login
- Patient intake and consent
- Appointment booking or request workflow
- Telehealth session access
- Provider encounter notes
- EPDS screening
- Referrals
- Notifications for operational events
- Admin dashboard
- Audit visibility
```

### Keep deferred unless explicitly approved

```text
- Full secure clinical messaging
- Full education resource library
- Broad multilingual product coverage
- Mobile app rollout
- AI-assisted triage/documentation
- Advanced analytics/data warehouse
```

### Required rule

If a deferred feature has a route/page already, label it as:

```text
MVP shell only — full workflow deferred
```

This applies especially to:

```text
/patient/messages
/patient/resources
/admin/settings
```

---

## 3. P0 Fixes — Must Complete Before Pilot/UAT

P0 items affect security, basic workflow integrity, or core frontend/backend integration.

### P0-01 Fix patient/provider profile ID vs user ID authorization

Backend appointment, encounter, and telehealth records appear to store `patient_id` and `provider_id` as profile IDs. Some services compare them against `current_user.id`, which is likely a user account ID.

Affected areas:

```text
pbbf-api/app/modules/telehealth/service.py
pbbf-api/app/modules/telehealth/repository.py
pbbf-api/app/modules/encounters/service.py
pbbf-api/app/modules/encounters/repository.py
```

Required behavior:

```text
Patient authorization must compare appointment.patient_id to current_user.patient_profile.id.
Provider authorization must compare appointment.provider_id to current_user.provider_profile.id.
Admin/care coordinator access must be explicitly allowed and audited.
```

Definition of done:

```text
- Patients cannot access another patient’s telehealth session or encounter.
- Providers cannot access unassigned patient sessions/encounters.
- Existing tests cover matching and non-matching patient/provider profiles.
```

---

### P0-02 Add authorization to telehealth get_session

Current issue:

```text
GET /telehealth/sessions/{session_id}
```

The service fetches a session by ID but does not visibly verify whether the current user is allowed to view it.

Required behavior:

```text
- Patient can view only their own session.
- Provider can view only assigned session.
- Admin/care coordinator can view sessions by policy.
```

Definition of done:

```text
- get_session requires current_user.
- get_session reuses the same object-level authorization logic as join_session.
- Unauthorized access returns 403.
```

---

### P0-03 Remove database URL from health responses

Current risk:

```text
/api/v1/health returns settings.effective_database_url
```

Required behavior:

```text
Return only database.connected and optionally database.engine.
Do not expose database URL, hostname, username, path, or credentials.
```

Definition of done:

```text
- /health and /api/v1/health no longer expose full DB URL.
- Tests confirm sensitive DB URL is not present in response body.
```

---

### P0-04 Align public registration with backend policy

Current issue:

Frontend public register form allows role selection:

```text
patient
provider
care_coordinator
admin
```

Backend registration creates patient accounts only.

Required decision:

```text
Public self-registration = patient only.
Internal staff/admin accounts = admin-created only.
```

Frontend changes:

```text
- Remove role selector from public registration.
- Send only full_name, email, password, phone_number if used.
- Redirect to /patient/dashboard or onboarding after successful registration.
```

Backend changes:

```text
- Keep public register patient-only.
- Add/confirm admin-only staff provisioning endpoint separately.
```

Definition of done:

```text
- No public UI allows self-selecting admin/provider roles.
- Tests verify public registration always creates patient role.
```

---

### P0-05 Align intake frontend payload with backend schema

Current frontend sends:

```text
full_name
phone_number
service_needs
postpartum_summary
consent_accepted
privacy_accepted
```

Backend expects:

```text
date_of_birth
address
preferred_language
preferred_contact_method
emergency_contact_name
emergency_contact_phone
emergency_contact_relationship
service_need
consent_acknowledged
consent_version
privacy_policy_version
postpartum_questionnaire
attachments
notes
```

Required decision:

Choose one.

#### Option A — Backend remains single service need

Frontend must:

```text
- Change serviceNeeds array to serviceNeed string.
- Send service_need.
- Send consent_acknowledged.
- Send consent_version.
- Send privacy_policy_version.
- Map postpartumSummary to notes or postpartum_questionnaire.
- Move fullName/phoneNumber to /users/me update or remove from intake payload.
```

#### Option B — Backend supports multiple service needs

Backend must:

```text
- Add service_needs JSON/list support.
- Update schema, validator, model/migration, tests.
- Decide how triage handles multiple needs.
```

Recommended for speed:

```text
Use Option A for pilot.
```

Definition of done:

```text
- Save draft succeeds.
- Submit intake succeeds.
- Consent version and privacy policy version are stored.
- Frontend tests verify exact payload keys.
```

---

### P0-06 Persist consent before or during intake submission reliably

Current issue:

ConsentPage validates consent locally and navigates to intake, but it does not persist consent before route change.

Required behavior:

```text
- Either save a draft with consent fields before navigating, or
- Keep consent and intake in one page/state flow, or
- Store consent state safely and submit it with intake.
```

Definition of done:

```text
- Consent cannot be lost when navigating from consent page to intake page.
- Backend receives consent_acknowledged, consent_version, privacy_policy_version.
```

---

### P0-07 Decide and align appointment workflow

Current ambiguity:

Frontend says:

```text
Patient chooses a preferred date/time.
```

Backend expects:

```text
Patient books provider-specific appointment with provider_id, start_at, end_at.
```

Choose one.

#### Option A — True booking

Required:

```text
- Backend exposes provider availability.
- Frontend shows available provider/slot selection.
- Patient selects actual slot.
- Backend creates confirmed booking.
```

#### Option B — Appointment request

Required:

```text
- Backend allows provider_id nullable.
- Frontend submits preferred start/end time.
- Appointment status begins as requested/unassigned.
- Admin/care coordinator assigns provider later.
```

Recommended for current code:

```text
Option B may fit the current “preferred date/time” UI better.
Option A fits the original MVP backlog better but needs availability work.
```

Definition of done:

```text
- No hardcoded DEV_DEFAULT_PROVIDER_ID in production code.
- Patient can see created appointments/requests.
- Backend and frontend use the same status vocabulary.
```

---

### P0-08 Add patient appointment listing

Current issue:

`useAppointments()` explicitly clears appointments for patient role.

Required behavior:

```text
- Backend provides patient appointment list.
- Frontend loads patient appointments from backend.
- After booking, patient sees the booking/request.
```

Definition of done:

```text
- Patient appointments page displays real backend records.
- Cancel/reschedule still enforce patient ownership.
```

---

### P0-09 Align EPDS submission payload

Current frontend sends:

```json
{
  "answers": [
    { "question_id": "q1", "score": 0 }
  ]
}
```

Backend scoring engine expects q1-q10 answer keys or a schema that can become:

```json
{
  "answers": {
    "q1": 0,
    "q2": 1,
    "q3": 2,
    "q4": 0,
    "q5": 1,
    "q6": 0,
    "q7": 2,
    "q8": 1,
    "q9": 0,
    "q10": 0
  }
}
```

Required behavior:

```text
- Pick one format.
- Prefer q1-q10 object for backend engine simplicity.
- Frontend must display backend score/severity/critical_flag as authoritative.
```

Definition of done:

```text
- EPDS submit succeeds.
- Frontend displays score, severity_band, interpretation, critical_flag from backend.
- Local score is removed or clearly treated as non-authoritative preview.
```

---

### P0-10 Align encounter frontend routes and payloads

Frontend expects:

```text
GET   /encounters/by-appointment/{appointmentId}
POST  /encounters
PATCH /encounters/{id}/save
PATCH /encounters/{id}/finalize
```

Backend exposes:

```text
POST /encounters/appointments/{appointment_id}
GET  /encounters/{encounter_id}
PUT  /encounters/{encounter_id}/draft
POST /encounters/{encounter_id}/finalize
```

Required behavior:

Choose one route contract and update the other side.

Recommended backend additions for frontend UX:

```text
GET /encounters/by-appointment/{appointment_id}
```

Frontend should map fields to backend:

```text
note -> note_text or objective
assessment -> assessment
followUpPlan -> follow_up_plan
plan -> care plan if required
```

Definition of done:

```text
- Provider can select appointment.
- Existing encounter loads if present.
- Draft save works.
- Finalize works.
- Finalized note cannot be edited.
```

---

### P0-11 Align referral creation payload

Frontend sends:

```text
destination
follow_up_date
appointment_id
category as free text
```

Backend expects:

```text
destination_name
follow_up_at
category enum
encounter_id optional
```

Required frontend changes:

```text
- destination -> destination_name
- followUpDate -> follow_up_at
- Remove appointment_id unless backend accepts it.
- Use select/dropdown for backend enum categories.
- Parse list response from items[].
```

Definition of done:

```text
- Provider/care coordinator can create referral.
- Referral list loads from backend items[].
- Status update works.
```

---

### P0-12 Consolidate API clients

Current project has two API clients:

```text
src/services/api.js            # fetch-based, mostly correct
src/shared/services/api.js     # axios-based, likely stale/broken
```

Required behavior:

```text
- Keep one canonical API client.
- Use one env variable name, preferably VITE_API_BASE_URL.
- Ensure token field is accessToken.
- Remove or rewrite stale axios client.
```

Definition of done:

```text
- No module imports stale shared API client unless fixed.
- Tests verify Authorization header uses accessToken.
```

---

## 4. P1 Fixes — Complete Before Production-Like Staging

### P1-01 Wire audit events into all sensitive workflows

Audit exists and is used in referrals/notifications, but not consistently elsewhere.

Add audit events for:

```text
auth.login_success
auth.login_failed
auth.logout
auth.refresh
user.role_updated
user.status_updated
intake.draft_created
intake.draft_updated
intake.submitted
consent.acknowledged
screening.epds_submitted
screening.critical_flag_created
screening.reviewed
appointment.created
appointment.cancelled
appointment.rescheduled
appointment.provider_assigned
telehealth.session_created
telehealth.joined
telehealth.status_changed
encounter.created
encounter.draft_saved
encounter.finalized
referral.created
referral.status_updated
notification.created
notification.dispatched
```

Definition of done:

```text
- Critical events are visible in /audit.
- Admin audit page displays them.
- Tests verify audit record creation.
```

---

### P1-02 Persist request_id in audit_logs table

Current model uses an in-memory request_id property, not a DB column.

Required:

```text
- Add request_id column to AuditLog model.
- Add Alembic migration.
- Store request_id from request context.
- Add index if used for investigation.
```

---

### P1-03 Strengthen environment validation

Update `scripts/validate_env.py` to reject:

```text
- SQLite in staging/production
- weak secret key length
- placeholder secret key
- wildcard CORS in production
- wildcard allowed hosts in production
- production docs enabled
- non-HTTPS external base URL in production
```

---

### P1-04 Improve logout/session governance

Current logout is mostly frontend state clearing.

Required options:

```text
Option A: Store refresh token/session IDs server-side and revoke on logout.
Option B: Add token version per user and invalidate on logout/password reset.
Option C: Keep very short access tokens and httpOnly refresh cookie with rotation.
```

For controlled pilot, minimum acceptable:

```text
- Access tokens short-lived.
- Refresh tokens rotated or revocable.
- Logout calls backend and invalidates refresh token/session.
```

---

### P1-05 Wire appointment lifecycle to notifications

Add notification creation for:

```text
appointment.created
appointment.rescheduled
appointment.cancelled
appointment.reminder_due
```

Definition of done:

```text
- Notification records are created.
- Delivery status is trackable.
- Failed delivery can be investigated.
```

---

### P1-06 Restrict provider referral access

Current provider referral listing may be too broad.

Required behavior:

```text
- Provider sees referrals for assigned/related patients only.
- Care coordinator/admin may have broader operational access by policy.
```

---

### P1-07 Validate referral encounter-patient linkage

When creating referral with encounter_id:

```text
encounter.patient_id must equal payload.patient_id
```

---

### P1-08 Add production safeguards to restore/migration scripts

Restore script should:

```text
- Block production restore unless FORCE_RESTORE=true.
- Require explicit confirmation.
- Validate backup type matches database type.
- Optionally backup current DB before restore.
```

Migration validation script should:

```text
- Refuse production/staging DB unless explicitly allowed.
- Require PBBF_APP_ENV=test or validation.
```

---

### P1-09 Make notification delivery environment-aware

Current dispatch returns fake queued IDs.

Required:

```text
- Keep fake provider only for local/test.
- Use real provider adapter for staging/production if notifications are in pilot scope.
- Add delivery failure logging.
```

---

## 5. P2 Fixes — Improve Product Completeness

```text
- Add admin report export endpoint.
- Add provider utilization breakdown.
- Add data governance summary from real backup metadata if available.
- Add admin user creation/provisioning workflow.
- Add last-admin/self-deactivation guardrails.
- Add patient/provider names to appointment responses.
- Add encounter_id to appointment/provider workspace response if needed.
- Add frontend filters for audit logs.
- Add real device/browser permission checks for telehealth.
- Add explicit no_show/waiting UI states.
```

---

## 6. Frontend-Specific Hardening Checklist

### Auth

```text
- Remove role selector from public register.
- Add lactation_consultant to redirect mapping.
- Align password validation with backend.
- Implement refreshAccessToken or remove unused refresh token until backend supports it.
- Avoid long-lived tokens in localStorage for production.
```

### Intake

```text
- Align payload keys with backend.
- Persist consent reliably.
- Decide single vs multiple service needs.
- Navigate to /patient/dashboard after successful submit.
```

### Appointments

```text
- Remove hardcoded provider ID.
- Add provider/slot selection or switch to request workflow.
- Load patient appointments from backend.
- Standardize statuses.
```

### Screening

```text
- Submit q1-q10 object or update backend schema to accept array.
- Display backend score, severity_band, interpretation, and critical_flag.
- Treat local score as non-authoritative.
```

### Telehealth

```text
- Backend list response should include appointment time, service type, provider name if UI requires it.
- Handle waiting and no_show statuses.
- Do not block join solely because appointmentTime is missing if backend says session is ready.
```

### Encounters

```text
- Align routes/methods with backend.
- Add get-by-appointment endpoint or change frontend loading behavior.
- Align note fields with backend draft schema.
```

### Referrals

```text
- Use backend enum categories.
- Map destination_name and follow_up_at correctly.
- Parse items[] from backend list response.
```

### Admin

```text
- Add users role/status actions only after backend guardrails and audit exist.
- Add report export only after backend supports it.
- Fix metricDetails undefined usage or populate it.
- Ensure sidebar filters by allowedRoles.
```

---

## 7. Backend-Specific Hardening Checklist

### Authorization

```text
- Centralize patient/provider profile authorization helpers.
- Reuse helpers in appointments, telehealth, encounters, screenings, referrals.
- Add negative tests for cross-patient and cross-provider access.
```

### Audit

```text
- Persist request_id.
- Add workflow audit events.
- Include actor_user_id, entity_type, entity_id, action, details, ip_address, request_id.
```

### Environment

```text
- Strengthen validate_env.py.
- Remove DB URL from health.
- Ensure docs disabled in production.
```

### Reporting

```text
- Add exports only for approved reporting set.
- Track export audit events.
- Add export handling warnings in UI and API docs.
```

### Operations

```text
- Harden restore/migration scripts.
- Expand post-deploy smoke tests.
- Verify backup and restore on disposable environment.
```

---

## 8. Suggested Implementation Sequence

### Sprint A — Contract alignment and critical authorization

```text
1. Fix profile ID vs user ID checks.
2. Add telehealth get_session authorization.
3. Remove DB URL from health response.
4. Align intake payload.
5. Align EPDS payload.
6. Align encounter routes/payloads.
7. Align referral payload.
```

### Sprint B — Appointment workflow decision

```text
1. Decide true booking vs appointment request.
2. Remove hardcoded provider ID.
3. Add patient appointment listing.
4. Add provider/admin appointment list as needed.
5. Wire appointment notifications.
```

### Sprint C — Audit and governance

```text
1. Add request_id column/migration.
2. Wire audit events into sensitive workflows.
3. Add admin audit filters in UI.
4. Add role/status update audit.
```

### Sprint D — Auth/session hardening

```text
1. Remove public role selection.
2. Add frontend password validation parity.
3. Add refresh-token/session invalidation design.
4. Add password reset only if backend supports it.
```

### Sprint E — Operational readiness

```text
1. Strengthen validate_env.py.
2. Harden backup/restore/migration scripts.
3. Expand smoke checks.
4. Run full backend/frontend tests.
5. Execute UAT role matrix.
```

---

## 9. Verification Commands

### Backend

```bash
cd pbbf-api
python -m py_compile app/common/config/settings.py
python scripts/validate_env.py
pytest -q
pytest tests/modules/auth -q
pytest tests/modules/intake -q
pytest tests/modules/appointments -q
pytest tests/modules/screenings -q
pytest tests/modules/telehealth -q
pytest tests/modules/encounters -q
pytest tests/modules/referrals -q
pytest tests/modules/admin -q
pytest tests/modules/audit -q
pytest tests/integration -q
pytest tests/smoke -q
```

### Frontend

```bash
cd pbbf-telehealth
npm run lint
npm test -- --run
npm run build
npx playwright test
```

### Post-deploy smoke

```bash
cd pbbf-api
bash scripts/post_deploy_smoke.sh http://127.0.0.1:8000
```

---

## 10. Pilot Readiness Definition of Done

The project can be considered controlled-pilot ready when:

```text
- P0 items are complete.
- P1 security/audit/environment items are either complete or explicitly accepted as pilot risk.
- All backend tests pass.
- Frontend build passes.
- Main E2E flows pass for patient, provider, and admin.
- No public route allows privileged self-registration.
- No health endpoint leaks sensitive infrastructure info.
- Patients cannot access other patients’ data.
- Providers cannot access unassigned patient workflows.
- Audit events exist for critical workflow transitions.
- Backup/restore process has been tested in a disposable environment.
- UAT role-based checklist is completed.
```

---

## 11. Production Readiness Definition of Done

The project can be considered production-ready only when:

```text
- All P0 and P1 items are complete.
- Token/session governance supports server-side invalidation or secure refresh-token rotation.
- Notification delivery uses real configured provider adapters or is explicitly disabled.
- Restore/migration scripts cannot accidentally target production without explicit safeguards.
- Audit request_id is persisted.
- Report exports are permissioned and audited.
- Staging deployment is repeatable from documentation.
- Rollback plan has been tested.
- Early-life support log and incident runbook are active.
```

---

## 12. Final Recommendation

Do not add major new features until the P0 and P1 hardening work is complete. The project already has enough MVP surface area. The immediate risk is not lack of features; it is inconsistent contract alignment, object-level authorization, audit coverage, and operational hardening.

Recommended next official project phase:

```text
Phase 2A — Contract Alignment and Security Hardening
```

Then:

```text
Phase 2B — Pilot Readiness and UAT
```

Then:

```text
Phase 2C — Production Operations Readiness
```
