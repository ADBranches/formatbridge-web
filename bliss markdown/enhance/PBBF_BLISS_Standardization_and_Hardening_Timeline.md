# PBBF BLISS Telehealth Platform — Standardization and Hardening Execution Timeline

**Repository:** `bliss-telehealth/`  
**Backend:** `pbbf-api/`  
**Frontend:** `pbbf-telehealth/`  
**Shared docs:** `docs/`  
**Shared infrastructure:** `infra/`  
**Shared scripts:** `scripts/`

---

## Purpose of This Timeline

This timeline is written for the **actual existing PBBF BLISS repository** after inspection of the backend, frontend, tests, scripts, and documentation structure.

This is **not a discovery checklist** and not a generic project plan. The project already contains the main MVP modules. The work now is to:

- standardize EPDS correctly,
- align frontend/backend API contracts,
- fix object-level authorization,
- harden audit/session/security behavior,
- repair ambiguous user workflows,
- complete pilot-readiness testing,
- and prepare the system for controlled staging/UAT.

---

## Project Position

The current project already includes strong structural coverage for:

```text
- Authentication and users
- Patient intake and consent
- Appointments
- EPDS screening
- Telehealth session access
- Encounter documentation
- Referrals
- Notifications
- Audit
- Admin dashboard/reporting shell
- Backend tests
- Frontend tests/E2E shell
- Operational docs
- Deployment docs
```

The immediate risk is **not lack of modules**. The immediate risk is:

```text
- frontend/backend contract mismatch,
- non-standard EPDS wording/scoring in frontend,
- object-level authorization gaps,
- incomplete audit coverage,
- weak logout/session governance,
- and production-safety gaps.
```

---

# Stage 0 — EPDS International Standard Lock

## Objective

Replace the current custom/paraphrased EPDS implementation with a standard Edinburgh Postnatal Depression Scale workflow.

The EPDS must be implemented as the recognized 10-item Edinburgh Postnatal Depression Scale, not as a custom wellness questionnaire and not as a locally invented “best version.”

## Standard EPDS rules to enforce

The platform must enforce:

```text
- 10 questions/items.
- Recall period: “in the past 7 days.”
- Questions 1, 2, and 4 are scored normally: top answer = 0, bottom answer = 3.
- Questions 3 and 5–10 are reverse scored: top answer = 3, bottom answer = 0.
- Maximum score = 30.
- Possible depression threshold commonly begins at 10 or greater.
- Scores above 13 indicate higher likelihood of depressive illness and require careful clinical review.
- Item 10 must always be reviewed independently.
- EPDS score must not override clinical judgment.
```

## Files to update

### Backend

```text
pbbf-api/app/modules/screenings/constants.py
pbbf-api/app/modules/screenings/scoring.py
pbbf-api/app/modules/screenings/schemas.py
pbbf-api/app/modules/screenings/service.py
pbbf-api/app/modules/screenings/router.py
pbbf-api/tests/modules/screenings/test_epds_submission.py
pbbf-api/tests/modules/screenings/test_epds_scoring.py
pbbf-api/tests/modules/screenings/test_epds_risk_flags.py
pbbf-api/tests/modules/screenings/test_safety_flag_rules.py
```

### Frontend

```text
pbbf-telehealth/src/modules/screenings/utils/epdsQuestions.js
pbbf-telehealth/src/modules/screenings/hooks/useEpdsForm.js
pbbf-telehealth/src/modules/screenings/components/EpdsQuestionnaire.jsx
pbbf-telehealth/src/modules/screenings/components/ScoreSummaryCard.jsx
pbbf-telehealth/src/pages/patient/Screening.jsx
pbbf-telehealth/src/modules/screenings/__tests__/EpdsQuestionnaire.test.jsx
pbbf-telehealth/src/modules/screenings/__tests__/ScreeningPage.test.jsx
pbbf-telehealth/src/modules/screenings/__tests__/useEpdsForm.test.jsx
```

## Files to create

```text
pbbf-api/docs/clinical-operations/epds-standard-implementation.md
pbbf-api/tests/modules/screenings/test_epds_standard_question_order.py
pbbf-api/tests/modules/screenings/test_epds_item10_review_required.py
pbbf-api/tests/modules/screenings/test_epds_threshold_config.py
pbbf-telehealth/src/modules/screenings/utils/epdsStandard.js
pbbf-telehealth/src/modules/screenings/__tests__/EpdsStandard.test.js
```

## Required implementation decisions

```text
- Backend must be the scoring authority.
- Frontend local scoring must be removed or labelled as non-authoritative preview only.
- Frontend must submit answer values in a backend-approved q1–q10 object format.
- Frontend must display backend score, severity_band, interpretation, and critical_flag.
- Item 10 must create a separate safety-review flag even if total score is low.
```

## Completion checkpoint

EPDS submission, scoring, severity banding, interpretation, and item-10 flagging pass backend tests and match the standard EPDS scoring model.

---

# Stage 1 — Frontend/Backend Contract Alignment Foundation

## Objective

Make frontend and backend agree on API routes, request payloads, response shapes, and status names before adding or polishing more features.

## Files to update

### Backend

```text
pbbf-api/app/modules/intake/schemas.py
pbbf-api/app/modules/intake/service.py
pbbf-api/app/modules/appointments/schemas.py
pbbf-api/app/modules/appointments/service.py
pbbf-api/app/modules/appointments/router.py
pbbf-api/app/modules/encounters/router.py
pbbf-api/app/modules/encounters/schemas.py
pbbf-api/app/modules/referrals/schemas.py
pbbf-api/app/modules/referrals/service.py
pbbf-api/app/modules/telehealth/schemas.py
pbbf-api/app/modules/telehealth/service.py
```

### Frontend

```text
pbbf-telehealth/src/services/api.js
pbbf-telehealth/src/shared/services/api.js
pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
pbbf-telehealth/src/modules/intake/services/intakeApi.js
pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js
pbbf-telehealth/src/modules/appointments/services/appointmentsApi.js
pbbf-telehealth/src/modules/encounters/services/encountersApi.js
pbbf-telehealth/src/modules/encounters/hooks/useEncounterEditor.js
pbbf-telehealth/src/modules/referrals/services/referralsApi.js
pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js
pbbf-telehealth/src/modules/screenings/hooks/useEpdsForm.js
pbbf-telehealth/src/modules/screenings/services/screeningsApi.js
```

## Files to create

```text
docs/api-contracts/frontend-backend-contract-map.md
docs/api-contracts/mvp-payload-decisions.md
pbbf-api/tests/integration/test_contract_patient_flow.py
pbbf-api/tests/integration/test_contract_provider_flow.py
pbbf-telehealth/src/test/msw/contractHandlers.js
```

## Contract mismatches to resolve

```text
intake: service_needs vs service_need
intake: consent_accepted vs consent_acknowledged
intake: privacy_accepted vs privacy_policy_version
appointments: preferred time request vs confirmed booking
appointments: hardcoded provider_id vs selected/assigned provider
encounters: frontend routes vs backend routes
referrals: destination vs destination_name
referrals: follow_up_date vs follow_up_at
screenings: EPDS array answers vs q1–q10 object
admin: metricDetails referenced in frontend but not returned by hook
```

## Completion checkpoint

Every MVP frontend service calls a backend route that exists and sends payload fields accepted by backend schemas.

---

# Stage 2 — Critical Object-Level Authorization Hardening

## Objective

Fix object-level authorization so patients, providers, care coordinators, and admins access only records they are allowed to access.

## Files to update

```text
pbbf-api/app/common/permissions/dependencies.py
pbbf-api/app/modules/telehealth/service.py
pbbf-api/app/modules/telehealth/repository.py
pbbf-api/app/modules/encounters/service.py
pbbf-api/app/modules/encounters/repository.py
pbbf-api/app/modules/appointments/service.py
pbbf-api/app/modules/appointments/repository.py
pbbf-api/app/modules/screenings/service.py
pbbf-api/app/modules/referrals/service.py
pbbf-api/tests/modules/telehealth/test_session_access.py
pbbf-api/tests/modules/encounters/test_create_note.py
pbbf-api/tests/modules/referrals/test_create_referral.py
```

## Files to create

```text
pbbf-api/app/common/permissions/object_access.py
pbbf-api/tests/modules/permissions/test_object_access.py
pbbf-api/tests/security/test_cross_patient_access_denied.py
pbbf-api/tests/security/test_cross_provider_access_denied.py
```

## Required fixes

```text
- Do not compare appointment.patient_id to current_user.id when patient_id is a patient profile ID.
- Use current_user.patient_profile.id for patient ownership checks.
- Use current_user.provider_profile.id for provider assignment checks.
- Add authorization to telehealth get_session.
- Restrict provider access to assigned/related patients.
```

## Completion checkpoint

Cross-patient and cross-provider access tests fail before the fix and pass after the fix.

---

# Stage 3 — Auth, Registration, and Session Governance

## Objective

Make authentication behavior consistent, secure, and aligned with the MVP role model.

## Files to update

### Backend

```text
pbbf-api/app/modules/auth/router.py
pbbf-api/app/modules/auth/schemas.py
pbbf-api/app/modules/auth/service.py
pbbf-api/app/modules/auth/tokens.py
pbbf-api/app/modules/users/router.py
pbbf-api/app/modules/users/service.py
pbbf-api/app/common/utils/security.py
pbbf-api/tests/modules/auth/test_register.py
pbbf-api/tests/modules/auth/test_login.py
pbbf-api/tests/modules/auth/test_refresh_token.py
pbbf-api/tests/modules/users/test_user_profile.py
```

### Frontend

```text
pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx
pbbf-telehealth/src/modules/auth/components/LoginForm.jsx
pbbf-telehealth/src/modules/auth/utils/validators.js
pbbf-telehealth/src/modules/auth/hooks/useAuth.js
pbbf-telehealth/src/services/auth.service.js
pbbf-telehealth/src/store/authStore.js
```

## Files to create

```text
pbbf-api/app/db/models/auth_session.py
pbbf-api/app/modules/auth/session_repository.py
pbbf-api/tests/modules/auth/test_logout_revokes_session.py
pbbf-telehealth/src/modules/auth/__tests__/SessionRefresh.test.jsx
```

## Required fixes

```text
- Public registration must be patient-only.
- Remove privileged role selector from public register form.
- Internal provider/admin/care coordinator creation must be admin-only.
- Add lactation_consultant to frontend redirect mapping.
- Frontend password validation must match backend password rules.
- Logout must invalidate server-side refresh/session state.
- Refresh token workflow must either be implemented or removed from frontend until supported.
```

## Completion checkpoint

No public user can self-register as provider, care coordinator, lactation consultant, counselor, or admin.

---

# Stage 4 — Intake and Consent Governance

## Objective

Make intake and consent reliable, auditable, and aligned between frontend and backend.

## Files to update

```text
pbbf-api/app/modules/intake/router.py
pbbf-api/app/modules/intake/schemas.py
pbbf-api/app/modules/intake/service.py
pbbf-api/app/modules/intake/repository.py
pbbf-api/app/modules/intake/validators.py
pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
pbbf-telehealth/src/modules/intake/utils/intakeSchema.js
pbbf-telehealth/src/modules/intake/pages/ConsentPage.jsx
pbbf-telehealth/src/modules/intake/pages/IntakeFormPage.jsx
pbbf-telehealth/src/modules/intake/components/IntakeForm.jsx
```

## Files to create

```text
pbbf-api/app/db/models/consent_event.py
pbbf-api/alembic/versions/<new>_add_consent_events.py
pbbf-api/tests/modules/intake/test_consent_versioning.py
pbbf-api/tests/modules/intake/test_consent_event_history.py
pbbf-telehealth/src/modules/intake/__tests__/ConsentPersistence.test.jsx
```

## Required fixes

```text
- Persist consent version.
- Persist privacy policy version.
- Do not lose consent state between consent page and intake page.
- Decide single service_need or multiple service_needs.
- Map postpartum summary to backend notes or questionnaire structure.
```

## Completion checkpoint

Consent capture is not just a checkbox in the UI; it is stored as a durable event.

---

# Stage 5 — Appointment Workflow Alignment

## Objective

Make scheduling coherent by choosing either true booking or appointment request flow.

## Files to update

### Backend

```text
pbbf-api/app/modules/appointments/router.py
pbbf-api/app/modules/appointments/schemas.py
pbbf-api/app/modules/appointments/service.py
pbbf-api/app/modules/appointments/repository.py
pbbf-api/app/db/models/appointment.py
```

### Frontend

```text
pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js
pbbf-telehealth/src/modules/appointments/services/appointmentsApi.js
pbbf-telehealth/src/modules/appointments/components/AppointmentForm.jsx
pbbf-telehealth/src/modules/appointments/components/AppointmentCard.jsx
pbbf-telehealth/src/pages/patient/Appointments.jsx
pbbf-telehealth/src/modules/appointments/pages/BookAppointmentPage.jsx
```

## Files to create

```text
pbbf-api/app/modules/appointments/availability.py
pbbf-api/tests/modules/appointments/test_patient_listing.py
pbbf-api/tests/modules/appointments/test_admin_listing.py
pbbf-api/tests/modules/appointments/test_status_lifecycle.py
pbbf-telehealth/src/modules/appointments/utils/appointmentStatus.js
```

## Required decision

Choose one:

```text
Option A: confirmed booking with provider availability
Option B: appointment request with later provider assignment
```

## Required fixes

```text
- Remove DEV_DEFAULT_PROVIDER_ID.
- Add patient appointment listing.
- Add provider appointment listing with patient context.
- Add admin/care coordinator scheduling oversight.
- Standardize appointment statuses.
- Wire appointment lifecycle to notifications.
```

## Completion checkpoint

A patient can create an appointment/request and see it immediately in their appointment list.

---

# Stage 6 — Standard EPDS Screening Workflow Completion

## Objective

Complete the standard EPDS screening flow after Stage 0 locks the standard.

## Files to update

```text
pbbf-api/app/modules/screenings/constants.py
pbbf-api/app/modules/screenings/scoring.py
pbbf-api/app/modules/screenings/schemas.py
pbbf-api/app/modules/screenings/service.py
pbbf-api/app/modules/screenings/repository.py
pbbf-api/tests/modules/screenings/test_epds_scoring.py
pbbf-api/tests/modules/screenings/test_epds_risk_flags.py
pbbf-telehealth/src/modules/screenings/utils/epdsQuestions.js
pbbf-telehealth/src/modules/screenings/hooks/useEpdsForm.js
pbbf-telehealth/src/modules/screenings/components/EpdsQuestionnaire.jsx
pbbf-telehealth/src/modules/screenings/components/ScoreSummaryCard.jsx
```

## Files to create

```text
pbbf-api/tests/modules/screenings/test_epds_item10_review_required.py
pbbf-api/tests/modules/screenings/test_epds_threshold_config.py
pbbf-telehealth/src/modules/screenings/utils/epdsStandard.js
pbbf-telehealth/src/modules/screenings/__tests__/EpdsStandard.test.js
```

## Required fixes

```text
- Use official 10-item EPDS structure.
- Use past-7-days instruction.
- Use correct normal and reverse scoring.
- Backend must be scoring authority.
- Item 10 must always be separately flagged for review.
- Frontend must display backend score, severity_band, interpretation, and critical_flag.
```

## Completion checkpoint

EPDS scoring tests prove the implementation follows the standard scoring method.

---

# Stage 7 — Telehealth and Encounter Workflow Repair

## Objective

Make telehealth joining and provider documentation reliable, authorized, and route-aligned.

## Files to update

### Backend

```text
pbbf-api/app/modules/telehealth/router.py
pbbf-api/app/modules/telehealth/schemas.py
pbbf-api/app/modules/telehealth/service.py
pbbf-api/app/modules/telehealth/repository.py
pbbf-api/app/modules/encounters/router.py
pbbf-api/app/modules/encounters/schemas.py
pbbf-api/app/modules/encounters/service.py
pbbf-api/app/modules/encounters/repository.py
```

### Frontend

```text
pbbf-telehealth/src/modules/telehealth/hooks/useSessionAccess.js
pbbf-telehealth/src/modules/telehealth/services/telehealthApi.js
pbbf-telehealth/src/modules/telehealth/components/JoinSessionCard.jsx
pbbf-telehealth/src/pages/patient/Session.jsx
pbbf-telehealth/src/modules/encounters/services/encountersApi.js
pbbf-telehealth/src/modules/encounters/hooks/useEncounterEditor.js
pbbf-telehealth/src/modules/encounters/components/EncounterEditor.jsx
pbbf-telehealth/src/pages/provider/Notes.jsx
```

## Files to create

```text
pbbf-api/tests/modules/telehealth/test_get_session_authorization.py
pbbf-api/tests/modules/encounters/test_get_by_appointment.py
pbbf-telehealth/src/modules/telehealth/utils/sessionStatus.js
pbbf-telehealth/src/modules/encounters/utils/encounterPayload.js
```

## Required fixes

```text
- Telehealth get_session must enforce authorization.
- Session list response must include fields frontend needs.
- Frontend must handle waiting and no_show states.
- Encounter frontend routes must match backend.
- Encounter payload fields must match backend schema.
```

## Completion checkpoint

Patient can join an authorized session and provider can create, save, and finalize an encounter note.

---

# Stage 8 — Referrals, Notifications, and Audit Completion

## Objective

Make follow-up workflows trackable, auditable, and operationally useful.

## Files to update

### Backend

```text
pbbf-api/app/modules/referrals/router.py
pbbf-api/app/modules/referrals/schemas.py
pbbf-api/app/modules/referrals/service.py
pbbf-api/app/modules/referrals/repository.py
pbbf-api/app/modules/notifications/service.py
pbbf-api/app/modules/notifications/repository.py
pbbf-api/app/modules/notifications/channels.py
pbbf-api/app/modules/audit/service.py
pbbf-api/app/modules/audit/repository.py
pbbf-api/app/db/models/audit_log.py
```

### Frontend

```text
pbbf-telehealth/src/modules/referrals/services/referralsApi.js
pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js
pbbf-telehealth/src/modules/referrals/components/ReferralForm.jsx
pbbf-telehealth/src/modules/referrals/components/ReferralTimeline.jsx
pbbf-telehealth/src/pages/provider/Referrals.jsx
pbbf-telehealth/src/pages/admin/AuditLogs.jsx
```

## Files to create

```text
pbbf-api/alembic/versions/<new>_add_audit_request_id.py
pbbf-api/tests/modules/audit/test_request_id_persistence.py
pbbf-api/tests/modules/referrals/test_encounter_patient_match.py
pbbf-api/tests/modules/notifications/test_appointment_notification_hooks.py
pbbf-telehealth/src/modules/referrals/utils/referralCategories.js
```

## Required fixes

```text
- Referral create payload must use destination_name and follow_up_at.
- Referral category must be enum-driven.
- Referral list frontend must read items[].
- AuditLog must persist request_id as a DB column.
- Appointment lifecycle should create notification records.
- Notification dispatch must be environment-aware.
```

## Completion checkpoint

Referral creation, referral status update, notification hook, and audit trail all work together.

---

# Stage 9 — Admin Workspace and Reporting Hardening

## Objective

Turn the admin area from read-only visibility into a reliable operational oversight workspace.

## Files to update

### Backend

```text
pbbf-api/app/modules/admin/router.py
pbbf-api/app/modules/admin/schemas.py
pbbf-api/app/modules/admin/service.py
pbbf-api/app/modules/admin/repository.py
pbbf-api/app/modules/admin/metrics.py
pbbf-api/app/modules/users/router.py
pbbf-api/app/modules/users/service.py
```

### Frontend

```text
pbbf-telehealth/src/modules/admin/services/adminApi.js
pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js
pbbf-telehealth/src/pages/admin/Dashboard.jsx
pbbf-telehealth/src/pages/admin/Users.jsx
pbbf-telehealth/src/pages/admin/Reports.jsx
pbbf-telehealth/src/pages/admin/AuditLogs.jsx
pbbf-telehealth/src/pages/admin/Settings.jsx
pbbf-telehealth/src/components/layout/Sidebar.jsx
```

## Files to create

```text
pbbf-api/tests/modules/admin/test_report_export.py
pbbf-api/tests/modules/users/test_admin_user_provisioning.py
pbbf-telehealth/src/modules/admin/components/UserRoleActions.jsx
pbbf-telehealth/src/modules/admin/components/ReportExportPanel.jsx
pbbf-telehealth/src/modules/admin/components/AuditFilterPanel.jsx
```

## Required fixes

```text
- Admin reports page must not reference undefined metricDetails.
- Add report export only if backend supports it.
- Add user role/status controls only after audit and guardrails exist.
- Sidebar should filter navigation by current user role.
```

## Completion checkpoint

Admin users can monitor the system safely and perform only approved operational actions.

---

# Stage 10 — Environment, Deployment, and Operational Safety

## Objective

Make the system safe to run in staging and controlled pilot environments.

## Files to update

```text
pbbf-api/app/common/config/settings.py
pbbf-api/app/__init__.py
pbbf-api/scripts/validate_env.py
pbbf-api/scripts/backup_db.sh
pbbf-api/scripts/restore_db.sh
pbbf-api/scripts/run_migration_validation.sh
pbbf-api/scripts/post_deploy_smoke.sh
pbbf-api/infra/docker-compose.backend.yml
pbbf-api/infra/Dockerfile.backend
pbbf-telehealth/.env.example
pbbf-telehealth/vite.config.js
pbbf-telehealth/docs/frontend-deployment.md
docs/environment/environment-matrix.md
docs/deployment/staging-release-checklist.md
docs/deployment/pilot-readiness-checklist.md
docs/rollout/rollback-plan.md
```

## Files to create

```text
docs/operations/production-safety-checklist.md
docs/operations/staging-smoke-test-log.md
docs/security/frontend-token-storage-decision.md
pbbf-api/tests/test_health_no_sensitive_leak.py
pbbf-api/tests/test_validate_env_production_safety.py
```

## Required fixes

```text
- validate_env.py must block unsafe production config.
- restore script must have production guardrails.
- migration validation must refuse non-validation DBs by default.
- health endpoints must not leak DB URL.
- frontend must use one API base URL env variable.
```

## Completion checkpoint

Staging can be deployed, smoke-tested, and rolled back using documented commands.

---

# Stage 11 — Full Test, UAT, and Pilot Readiness

## Objective

Prove the product works through full patient, provider, and admin journeys.

## Files to update

```text
pbbf-api/tests/integration/test_patient_journey.py
pbbf-api/tests/integration/test_provider_journey.py
pbbf-api/tests/integration/test_admin_journey.py
pbbf-telehealth/src/test/e2e/patient-flow.spec.js
pbbf-telehealth/src/test/e2e/provider-flow.spec.js
pbbf-telehealth/src/test/e2e/admin-flow.spec.js
docs/qa/role-based-test-matrix.md
docs/qa/uat-plan.md
docs/qa/defect-triage-log.md
```

## Files to create

```text
docs/qa/pilot-exit-criteria.md
docs/qa/epds-standard-verification-checklist.md
docs/qa/security-regression-checklist.md
```

## Required verification commands

### Backend

```bash
cd pbbf-api
pytest -q
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

## Completion checkpoint

The system is ready for controlled pilot only when patient, provider, and admin journeys pass in a staging-like environment.

---

# Final Execution Order

```text
Stage 0: EPDS international standard lock
Stage 1: API contract alignment
Stage 2: object-level authorization hardening
Stage 3: auth and session governance
Stage 4: intake and consent governance
Stage 5: appointment workflow decision and repair
Stage 6: standard EPDS workflow completion
Stage 7: telehealth and encounter repair
Stage 8: referrals, notifications, and audit completion
Stage 9: admin workspace hardening
Stage 10: environment and deployment safety
Stage 11: full test, UAT, and pilot readiness
```

---

# Final Execution Rule

```text
Modify existing files first.
Create only the targeted missing files listed in each stage.
Do not add major new features until P0 contract, authorization, and EPDS standardization work is complete.
Do not treat custom EPDS wording or simple summed frontend score as final clinical screening logic.
Backend remains the authority for EPDS scoring and item-10 safety flagging.
```
