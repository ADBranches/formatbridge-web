# PBBF BLISS — MVP Coverage Assessment and Phase 2 Production Hardening Timeline

## Repository root
`bliss-telehealth/`

Primary application roots:
- `bliss-telehealth/pbbf-api`
- `bliss-telehealth/pbbf-telehealth`

---

# 1. Resolution on the current build timeline

## Verdict
Yes — the recent timeline you have already built **does achieve Phase 1 to the core** for an MVP aligned to the approved user stories.

## Why that conclusion is true
The recent build timeline already covers the main MVP user-story domains through the backend and frontend implementation tracks:

### Backend MVP coverage already achieved by the earlier timeline
- Auth and identity
- Intake and consent
- Appointment scheduling
- Screenings / EPDS logic
- Telehealth session access
- Encounter documentation
- Referrals
- Notifications
- Audit
- Admin reporting

That means the backend timeline already implemented the **functional backbone** of the approved MVP.

### Frontend MVP coverage already achieved by the earlier timeline
- Authentication UX and route protection
- Patient onboarding and intake
- Patient appointments
- Screening and self-assessment flow
- Telehealth readiness and session access
- Provider workspace
- Admin workspace
- Shared UX hardening

That means the frontend timeline already implemented the **role-facing MVP workflows** required by the backlog.

## Important qualification
The later stages of the recent timeline already started to move beyond Phase 1:
- backend Phase 9 and Phase 10
- frontend Phase 9 and Phase 10

Those phases already introduced:
- integration readiness
- deployment support
- hardening concerns
- documentation
- packaging for QA/staging

So the correct conclusion is:

> **The recent timeline already completes Phase 1 (build the MVP against the approved user stories) to the core.**  
> It also already begins Phase 2, but **not yet deeply enough** for broad production-grade service operations.

---

# 2. What Phase 2 means in your case

## Phase 1
Build the MVP against the approved user stories.

## Phase 2
Harden that MVP into a product that can support:
- controlled pilot rollout
- real operational support
- better security and recovery posture
- stronger compliance and governance readiness
- reliable QA/UAT
- monitored staging and controlled production release

This phase is **not about inventing lots of new product features**.  
It is mainly about:
- reliability
- governance
- security
- observability
- backup and recovery
- operational workflows
- release discipline
- safe rollout

---

# 3. Recommended Phase 2 timeline structure

## Suggested execution model
Run Phase 2 as **10 sequential hardening stages**.

### Suggested duration envelope
This is a realistic range, not a rigid calendar:
- Stage 1 to Stage 3: 2 to 4 weeks
- Stage 4 to Stage 7: 4 to 8 weeks
- Stage 8 to Stage 10: 3 to 6 weeks

Total realistic Phase 2 window:
- **9 to 18 weeks**, depending on team size, integration friction, and governance review cycles.

---

# 4. Phase 2 — Production-Grade Service Operations Timeline

---

## Stage 1 — Release Readiness Audit and MVP Freeze
### Objective
Freeze the MVP scope, confirm what is already complete, identify true production gaps, and stop accidental scope drift before hardening begins.

### Backend stage objective
Audit every implemented backend workflow against the MVP user stories and label each item as:
- complete
- partially complete
- implemented but not hardened
- missing for pilot readiness

### Frontend stage objective
Audit every patient, provider, and admin route for:
- connected state
- loading/error/empty behavior
- real backend integration state
- role protection behavior
- QA completeness

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/release-readiness/`
- `bliss-telehealth/docs/release-readiness/mvp-coverage-matrix.md`
- `bliss-telehealth/docs/release-readiness/phase2-gap-analysis.md`
- `bliss-telehealth/docs/release-readiness/pilot-scope-freeze.md`

#### Backend
- `bliss-telehealth/pbbf-api/docs/release-audit/`
- `bliss-telehealth/pbbf-api/docs/release-audit/backend-story-traceability.md`
- `bliss-telehealth/pbbf-api/tests/`
- `bliss-telehealth/pbbf-api/tests/integration/`
- `bliss-telehealth/pbbf-api/tests/smoke/`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/docs/release-audit/`
- `bliss-telehealth/pbbf-telehealth/docs/release-audit/frontend-story-traceability.md`
- `bliss-telehealth/pbbf-telehealth/src/test/`
- `bliss-telehealth/pbbf-telehealth/src/test/e2e/`

### Completion gate
You can point to one written source of truth showing:
- what the MVP already covers
- what is missing for controlled real-world use
- what Phase 2 will and will not change

---

## Stage 2 — Environment Separation, Secrets, and Configuration Governance
### Objective
Make local, test, staging, and production environments behave predictably and safely.

### Backend stage objective
Separate all environment configuration cleanly and eliminate any remaining ambiguous defaults for database, secrets, docs exposure, CORS, hosts, and logging.

### Frontend stage objective
Lock the frontend to explicit environment variables for API base URLs, feature flags, and deployment-mode behavior.

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/environment/`
- `bliss-telehealth/docs/environment/environment-matrix.md`
- `bliss-telehealth/docs/environment/secrets-governance.md`

#### Backend
- `bliss-telehealth/pbbf-api/app/common/config/settings.py`
- `bliss-telehealth/pbbf-api/.env.example`
- `bliss-telehealth/pbbf-api/docs/backend-env.md`
- `bliss-telehealth/pbbf-api/infra/`
- `bliss-telehealth/pbbf-api/infra/docker-compose.backend.yml`
- `bliss-telehealth/pbbf-api/infra/Dockerfile.backend`
- `bliss-telehealth/pbbf-api/scripts/validate_env.py`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/.env.example`
- `bliss-telehealth/pbbf-telehealth/docs/frontend-deployment.md`
- `bliss-telehealth/pbbf-telehealth/src/services/api.js`
- `bliss-telehealth/pbbf-telehealth/vite.config.js`

### Completion gate
No developer, tester, or deployment target should need hidden manual tweaks to make the app boot correctly in each environment.

---

## Stage 3 — Security Controls, IAM, and Access Hardening
### Objective
Raise the security posture from “working auth” to “defensible access control.”

### Backend stage objective
Strengthen token handling, role boundaries, admin access rules, session handling, secret rotation posture, rate limiting, and security headers.

### Frontend stage objective
Confirm the UI never leaks privileged routes, actions, or cross-role controls; improve logout/session-expiry behavior.

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/security/`
- `bliss-telehealth/docs/security/access-control-matrix.md`
- `bliss-telehealth/docs/security/admin-operations-policy.md`

#### Backend
- `bliss-telehealth/pbbf-api/app/common/permissions/`
- `bliss-telehealth/pbbf-api/app/common/permissions/dependencies.py`
- `bliss-telehealth/pbbf-api/app/common/utils/security.py`
- `bliss-telehealth/pbbf-api/app/main.py`
- `bliss-telehealth/pbbf-api/tests/test_security_headers.py`
- `bliss-telehealth/pbbf-api/tests/test_rate_limit_smoke.py`
- `bliss-telehealth/pbbf-api/tests/modules/auth/`
- `bliss-telehealth/pbbf-api/tests/modules/users/`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/src/routes/ProtectedRoute.jsx`
- `bliss-telehealth/pbbf-telehealth/src/shared/guards/AuthGuard.jsx`
- `bliss-telehealth/pbbf-telehealth/src/shared/guards/RoleGuard.jsx`
- `bliss-telehealth/pbbf-telehealth/src/store/authStore.js`
- `bliss-telehealth/pbbf-telehealth/src/modules/auth/__tests__/`
- `bliss-telehealth/pbbf-telehealth/src/pages/admin/__tests__/AdminRouteProtection.test.jsx`

### Completion gate
Every role is restricted correctly, admin-only actions are not reachable by other roles, and security behaviors are test-backed.

---

## Stage 4 — Observability, Audit Enrichment, and Incident Readiness
### Objective
Make the system understandable when something goes wrong.

### Backend stage objective
Strengthen structured logging, request tracing, audit completeness, health checks, readiness signals, and failure observability.

### Frontend stage objective
Surface clearer operational errors, integration failures, and retry-friendly UI states without exposing unsafe details.

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/operations/`
- `bliss-telehealth/docs/operations/incident-response-runbook.md`
- `bliss-telehealth/docs/operations/logging-and-monitoring-plan.md`

#### Backend
- `bliss-telehealth/pbbf-api/app/common/middleware/logging.py`
- `bliss-telehealth/pbbf-api/app/common/middleware/request_context.py`
- `bliss-telehealth/pbbf-api/app/modules/audit/`
- `bliss-telehealth/pbbf-api/app/modules/notifications/tasks.py`
- `bliss-telehealth/pbbf-api/tests/modules/audit/`
- `bliss-telehealth/pbbf-api/tests/test_health.py`
- `bliss-telehealth/pbbf-api/tests/test_app_boot.py`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/src/shared/components/ErrorState.jsx`
- `bliss-telehealth/pbbf-telehealth/src/shared/hooks/useToast.js`
- `bliss-telehealth/pbbf-telehealth/src/shared/components/FormErrorSummary.jsx`
- `bliss-telehealth/pbbf-telehealth/src/modules/*/__tests__/`

### Completion gate
You can observe system health, trace major failures, and explain what happened during an incident or failed workflow.

---

## Stage 5 — Clinical Safety, Consent Governance, and Operational Playbooks
### Objective
Move from functional workflow to controlled care workflow.

### Backend stage objective
Confirm consent versioning behavior, screening safety flags, role review rules, no-show handling, referral follow-up expectations, and audit capture for sensitive workflow transitions.

### Frontend stage objective
Improve clarity around screening completion, consent acknowledgement, provider note finalization, and telehealth readiness messaging.

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/clinical-operations/`
- `bliss-telehealth/docs/clinical-operations/consent-version-governance.md`
- `bliss-telehealth/docs/clinical-operations/screening-escalation-playbook.md`
- `bliss-telehealth/docs/clinical-operations/no-show-and-follow-up-playbook.md`
- `bliss-telehealth/docs/clinical-operations/referral-operating-guidelines.md`

#### Backend
- `bliss-telehealth/pbbf-api/app/modules/intake/`
- `bliss-telehealth/pbbf-api/app/modules/screenings/`
- `bliss-telehealth/pbbf-api/app/modules/encounters/`
- `bliss-telehealth/pbbf-api/app/modules/referrals/`
- `bliss-telehealth/pbbf-api/tests/modules/intake/`
- `bliss-telehealth/pbbf-api/tests/modules/screenings/`
- `bliss-telehealth/pbbf-api/tests/modules/encounters/`
- `bliss-telehealth/pbbf-api/tests/modules/referrals/`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/src/modules/intake/`
- `bliss-telehealth/pbbf-telehealth/src/modules/screenings/`
- `bliss-telehealth/pbbf-telehealth/src/modules/telehealth/`
- `bliss-telehealth/pbbf-telehealth/src/modules/encounters/`
- `bliss-telehealth/pbbf-telehealth/src/modules/referrals/`
- `bliss-telehealth/pbbf-telehealth/src/pages/patient/`
- `bliss-telehealth/pbbf-telehealth/src/pages/provider/`

### Completion gate
Sensitive care workflows are no longer just technically functional; they are operationally understandable and governance-aware.

---

## Stage 6 — Data Protection, Backup, Recovery, and Retention Controls
### Objective
Protect the system against data loss, unsafe retention, and weak recovery posture.

### Backend stage objective
Add backup strategy, restore verification, data retention rules, export handling controls, and recovery documentation.

### Frontend stage objective
Prevent stale or misleading UI behavior around deleted, archived, or expired records; ensure exports/reports/downloads match retention expectations.

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/data-governance/`
- `bliss-telehealth/docs/data-governance/backup-and-restore-plan.md`
- `bliss-telehealth/docs/data-governance/data-retention-policy.md`
- `bliss-telehealth/docs/data-governance/export-handling-policy.md`

#### Backend
- `bliss-telehealth/pbbf-api/scripts/backup_db.sh`
- `bliss-telehealth/pbbf-api/scripts/restore_db.sh`
- `bliss-telehealth/pbbf-api/docs/backend-restore-validation.md`
- `bliss-telehealth/pbbf-api/app/modules/admin/`
- `bliss-telehealth/pbbf-api/app/modules/audit/`
- `bliss-telehealth/pbbf-api/tests/integration/test_admin_journey.py`
- `bliss-telehealth/pbbf-api/tests/test_recovery_smoke.py`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/src/pages/admin/Reports.jsx`
- `bliss-telehealth/pbbf-telehealth/src/pages/admin/AuditLogs.jsx`
- `bliss-telehealth/pbbf-telehealth/src/modules/admin/`
- `bliss-telehealth/pbbf-telehealth/docs/frontend-deployment.md`
- `bliss-telehealth/pbbf-telehealth/docs/frontend-testing.md`

### Completion gate
You can explain how data is backed up, how it is restored, and how long critical operational data is kept.

---

## Stage 7 — Performance, Reliability, and Resilience Validation
### Objective
Prove the MVP can stay stable under realistic workload and failure conditions.

### Backend stage objective
Run load tests, concurrency tests, job retry tests, DB stability checks, and migration stability checks.

### Frontend stage objective
Confirm the UI remains usable under slow API responses, partial failures, refreshes, and repeated navigation across roles.

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/performance/`
- `bliss-telehealth/docs/performance/performance-test-plan.md`
- `bliss-telehealth/docs/performance/reliability-gates.md`

#### Backend
- `bliss-telehealth/pbbf-api/tests/performance/`
- `bliss-telehealth/pbbf-api/tests/integration/`
- `bliss-telehealth/pbbf-api/app/jobs/`
- `bliss-telehealth/pbbf-api/alembic/`
- `bliss-telehealth/pbbf-api/scripts/run_load_tests.sh`
- `bliss-telehealth/pbbf-api/scripts/run_migration_validation.sh`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/src/test/e2e/`
- `bliss-telehealth/pbbf-telehealth/src/test/msw/`
- `bliss-telehealth/pbbf-telehealth/src/shared/components/`
- `bliss-telehealth/pbbf-telehealth/src/modules/*/__tests__/`
- `bliss-telehealth/pbbf-telehealth/docs/frontend-testing.md`

### Completion gate
The system can survive realistic usage, and you know where the stability limits are before public-facing rollout.

---

## Stage 8 — Integrated QA, UAT, Accessibility, and Staff Readiness
### Objective
Validate the whole product end to end with real workflows and real operational users.

### Backend stage objective
Support seeded environments, realistic test accounts, UAT defect triage, and stable connected QA endpoints.

### Frontend stage objective
Run E2E tests, accessibility smoke tests, user acceptance passes, and role-by-role workflow validation.

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/qa/`
- `bliss-telehealth/docs/qa/uat-plan.md`
- `bliss-telehealth/docs/qa/role-based-test-matrix.md`
- `bliss-telehealth/docs/qa/defect-triage-log.md`
- `bliss-telehealth/docs/training/`
- `bliss-telehealth/docs/training/patient-guides/`
- `bliss-telehealth/docs/training/provider-guides/`
- `bliss-telehealth/docs/training/admin-guides/`

#### Backend
- `bliss-telehealth/pbbf-api/scripts/seed_roles.py`
- `bliss-telehealth/pbbf-api/scripts/seed_users.py`
- `bliss-telehealth/pbbf-api/scripts/seed_reference_data.py`
- `bliss-telehealth/pbbf-api/tests/integration/test_patient_journey.py`
- `bliss-telehealth/pbbf-api/tests/integration/test_provider_journey.py`
- `bliss-telehealth/pbbf-api/tests/integration/test_admin_journey.py`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/src/test/e2e/patient-flow.spec.js`
- `bliss-telehealth/pbbf-telehealth/src/test/e2e/provider-flow.spec.js`
- `bliss-telehealth/pbbf-telehealth/src/test/e2e/admin-flow.spec.js`
- `bliss-telehealth/pbbf-telehealth/src/shared/utils/a11y.js`
- `bliss-telehealth/pbbf-telehealth/src/components/ui/`
- `bliss-telehealth/pbbf-telehealth/src/shared/components/`

### Completion gate
Real users can execute the main workflows in a controlled environment, and the team has documented training and QA evidence.

---

## Stage 9 — Staging Operations, Deployment Runbooks, and Pilot Readiness
### Objective
Make staging behave like a real operational environment and prepare for a controlled pilot.

### Backend stage objective
Finalize deployment automation, runbooks, service restart behavior, health validation, and operational handover documentation.

### Frontend stage objective
Finalize build packaging, environment validation, deployment docs, route refresh handling, and staging smoke checks.

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/deployment/`
- `bliss-telehealth/docs/deployment/staging-release-checklist.md`
- `bliss-telehealth/docs/deployment/pilot-readiness-checklist.md`
- `bliss-telehealth/docs/operations/runbooks/`
- `bliss-telehealth/docs/operations/runbooks/frontend-runbook.md`
- `bliss-telehealth/docs/operations/runbooks/backend-runbook.md`

#### Backend
- `bliss-telehealth/pbbf-api/infra/docker-compose.backend.yml`
- `bliss-telehealth/pbbf-api/infra/Dockerfile.backend`
- `bliss-telehealth/pbbf-api/infra/nginx.backend.conf`
- `bliss-telehealth/pbbf-api/docs/backend-api.md`
- `bliss-telehealth/pbbf-api/docs/backend-test-strategy.md`
- `bliss-telehealth/pbbf-api/tests/smoke/`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/README.md`
- `bliss-telehealth/pbbf-telehealth/docs/frontend-deployment.md`
- `bliss-telehealth/pbbf-telehealth/docs/frontend-testing.md`
- `bliss-telehealth/pbbf-telehealth/vite.config.js`
- `bliss-telehealth/pbbf-telehealth/package.json`
- `bliss-telehealth/pbbf-telehealth/public/`

### Completion gate
Staging can be deployed and operated repeatedly without undocumented manual rescue steps.

---

## Stage 10 — Controlled Production Rollout and Early-Life Support
### Objective
Move from staging confidence to controlled real-world rollout with early monitoring and rapid response discipline.

### Backend stage objective
Release gradually, monitor real usage, track failures, review audit/incident signals, and maintain rollback readiness.

### Frontend stage objective
Monitor real user flow breakage, route errors, cross-role regressions, and real browser/device issues during early-life support.

### Files and directories to create or complete

#### Shared project root
- `bliss-telehealth/docs/rollout/`
- `bliss-telehealth/docs/rollout/production-rollout-plan.md`
- `bliss-telehealth/docs/rollout/rollback-plan.md`
- `bliss-telehealth/docs/rollout/early-life-support-log.md`
- `bliss-telehealth/docs/rollout/community-pilot-observation-log.md`

#### Backend
- `bliss-telehealth/pbbf-api/docs/operations/`
- `bliss-telehealth/pbbf-api/docs/operations/post-launch-monitoring.md`
- `bliss-telehealth/pbbf-api/scripts/post_deploy_smoke.sh`
- `bliss-telehealth/pbbf-api/tests/smoke/`

#### Frontend
- `bliss-telehealth/pbbf-telehealth/docs/frontend-deployment.md`
- `bliss-telehealth/pbbf-telehealth/src/test/e2e/`
- `bliss-telehealth/pbbf-telehealth/src/shared/hooks/useToast.js`
- `bliss-telehealth/pbbf-telehealth/src/shared/components/ErrorState.jsx`

### Completion gate
The product is not just deployed — it is being actively operated, observed, and corrected under a controlled rollout plan.

---

# 5. Simple boundary between Phase 1 and Phase 2

## Phase 1 was complete when:
- the MVP user stories were implemented
- patient, provider, and admin workflows existed
- the backend supported the core business flows
- the frontend exposed the role-facing UX

## Phase 2 is complete when:
- the same MVP can be trusted operationally
- recovery is documented
- environments are predictable
- QA is role-realistic
- audit and observability are useful
- deployment is repeatable
- a pilot can be supported without guesswork

---

# 6. Strong recommendation on sequencing

Do **not** start adding major new features before finishing at least Stage 1 through Stage 6 of Phase 2.

That is the safest sequencing for this product because the current system is already functionally rich enough for an MVP, and the larger risk now is **operational weakness**, not lack of features.

---

# 7. Recommended next move

## Recommended truth-based next move
Because the recent build timeline already covers Phase 1 to the core, your next official timeline should be:

> **Phase 2 — Hardening it into production-grade service operations**

That is exactly what this document defines.

---

# 8. Completion summary

## What this file resolves
- confirms the earlier timeline already satisfied Phase 1 at MVP level
- separates Phase 1 from Phase 2 clearly
- provides a structured Phase 2 hardening timeline
- preserves the same staged style you have been using
- lists files and directories stage by stage
- keeps backend and frontend concerns visible inside every hardening stage

---

# 9. Suggested filename
`PBBF_BLISS_Phase2_Production_Hardening_Timeline.md`
