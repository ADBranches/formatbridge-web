# LandaFlow End-to-End Corrective Development Timeline

## 1. Purpose

This corrective plan closes the delivery gaps identified after Sprint 04 while preserving the substantial engineering work already completed. LandaFlow remains an end-to-end product, which means every release-critical capability must be proven across the user interface, API, database, security controls, audit trail, external-provider integration, deployment, monitoring, backup, recovery, and operational-support paths.

The corrective programme does not discard the existing database, ledger, billing, mobile-money, reconciliation, infrastructure, CI, and testing foundations. It introduces stricter completion classifications and adds the work required to prove real provider integrations, professional user experience, production deployment, and operational readiness.

## 2. Corrected Definition of End-to-End Completion

A capability is end-to-end only when all applicable layers are implemented and verified:

1. A user can complete the intended journey through the web interface.
2. The API validates identity, organisation membership, permissions, input, and lifecycle rules.
3. The database preserves organisation isolation, referential integrity, idempotency, and history.
4. The relevant audit event records the actor or job identity, organisation, action, affected record, timestamp, and correlation identifier.
5. External-provider calls use the provider's official test or sandbox environment where available.
6. Callback, replay, duplicate, timeout, mismatch, and outage scenarios are tested.
7. Confirmed financial actions produce exactly one valid ledger outcome and, where applicable, one immutable receipt.
8. The capability works through the production-like HTTPS deployment.
9. Logs, health checks, metrics, backup, restoration, and incident procedures are available to authorised operators.
10. Validation evidence references the exact Git commit under review.

## 3. Completion Status Classification

The project will no longer use the word **complete** without an explicit qualification.

| Status | Meaning |
|---|---|
| Foundation complete | The schema, migration, shared contracts, or provider-neutral interfaces exist. |
| Implementation complete | Backend and frontend code exist, but external or deployed validation may remain. |
| Locally validated | Deterministic local tests and simulations pass. |
| Sandbox validated | The real provider test environment accepted and completed the required journey. |
| Deployed and verified | The journey works through the public HTTPS deployment. |
| Production approved | Provider UAT, security review, operational evidence, and release approval are complete. |

## 4. Corrective Delivery Window

The corrective programme is planned for four engineering weeks, followed by a contingency period of five to ten working days for external-provider account approval, credential issuance, or URA-supervised UAT scheduling.

Sprint 05 may continue concurrently under the Web Experience Team. Sprint 06 must avoid duplicating Sprint 05 interface work and must inspect incoming collaborator changes before modifying shared contracts or shared interface files.

---

# Week 1: Integration Audit and Contract Correction

## Objective

Establish the true implementation baseline, identify incomplete end-to-end paths, correct contract assumptions, and prevent further premature completion claims.

## Work

1. Fetch and inspect the upstream integration branch and all active collaborator branches.
2. Confirm that Sprint 04 pull-request corrections are included in the current integration baseline.
3. Build a capability matrix with the following classifications:
   - Implemented and reachable
   - Implemented but not exposed in the interface
   - Locally simulated only
   - Provider-sandbox validated
   - Publicly deployed and verified
   - Blocked by credentials, provider approval, hosting, or DNS
4. Trace every release-critical journey through:
   - Web route
   - API endpoint
   - Permission
   - Database records
   - Audit event
   - External callback or provider response
   - Operational evidence
5. Revalidate all migrations against an empty PostgreSQL database.
6. Confirm that all existing provider-success labels distinguish simulated, sandbox-confirmed, and production-confirmed transactions.
7. Audit MTN MoMo, Airtel Money, EFRIS, JulyHost, email, notification, and backup contracts.
8. Identify shared-file ownership before Sprint 05 and Sprint 06 changes proceed concurrently.

## Files to create

- `docs/validation/end-to-end-capability-matrix.md`
- `docs/validation/external-provider-readiness.md`
- `docs/architecture/integration-contract-register.md`
- `docs/operations/concurrent-development-ownership.md`
- `tests/integration/end-to-end-contract-audit.spec.ts`

## Files likely to be modified

- `README.md`
- `CONTRIBUTING.md`
- `docs/operations/release-checklist.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/ci.yml`
- `package.json`

## Validation

- Every release-critical capability has an owner and status.
- Every UI route maps to an API and permission contract.
- Every confirmed financial path maps to one ledger outcome.
- Empty-database migrations pass.
- No simulated transaction is labelled provider-confirmed.
- Shared Sprint 05 and Sprint 06 file ownership is documented.

## Gate 1

No capability may be described as end-to-end unless the interface, API, persistence, audit, test, external-provider, and operational paths are all verified where applicable.

---

# Week 2: Professional UI Integration and Product-Level Remediation

## Objective

Replace scaffolded or browser-default presentation with a coherent, accessible, production-grade LandaFlow experience while integrating Sprint 05 work safely.

## Work

1. Review and integrate the Sprint 05 design system and page architecture.
2. Rebuild authentication screens with a deliberate responsive layout.
3. Refine the authenticated application shell.
4. Establish consistent typography, spacing, colours, borders, elevation, focus states, and responsive breakpoints.
5. Provide role-specific dashboards using live foundation data only.
6. Apply the design system across:
   - Properties and units
   - Tenants and agreements
   - Billing, invoices, payments, receipts, and statements
   - Mobile-money initiation and status
   - Reconciliation and payment exceptions
   - Fiscal-document status and exceptions
7. Provide consistent loading, empty, error, conflict, unavailable-provider, and unauthorised states.
8. Test keyboard navigation, visible focus, colour contrast, mobile layouts, tablet layouts, laptop layouts, and wide-desktop layouts.
9. Capture screenshot evidence for principal journeys.

## Files to create

- `apps/web/src/app/(auth)/layout.tsx`
- `apps/web/src/app/(app)/dashboard/loading.tsx`
- `apps/web/src/app/(app)/dashboard/error.tsx`
- `apps/web/src/components/page-header.tsx`
- `apps/web/src/components/responsive-data-table.tsx`
- `apps/web/src/components/status-badge.tsx`
- `apps/web/src/components/metric-card.tsx`
- `apps/web/src/components/permission-boundary.tsx`
- `apps/web/src/features/dashboard/api.ts`
- `apps/web/src/features/dashboard/components/operations-overview.tsx`
- `apps/web/src/features/dashboard/components/financial-overview.tsx`
- `apps/web/src/features/dashboard/components/attention-queue.tsx`
- `packages/ui/src/card.tsx`
- `packages/ui/src/select.tsx`
- `packages/ui/src/textarea.tsx`
- `packages/ui/src/table.tsx`
- `packages/ui/src/badge.tsx`
- `packages/ui/src/tabs.tsx`
- `packages/ui/src/skeleton.tsx`
- `packages/ui/src/dropdown-menu.tsx`
- `tests/e2e/visual-authentication.spec.ts`
- `tests/e2e/visual-workspace.spec.ts`
- `tests/e2e/responsive-navigation.spec.ts`
- `tests/e2e/accessibility-critical-paths.spec.ts`
- `docs/design/interface-system.md`
- `docs/validation/ui-release-evidence.md`

## Files likely to be modified

- `apps/web/src/app/globals.css`
- `apps/web/src/app/layout.tsx`
- `apps/web/src/app/(app)/layout.tsx`
- `apps/web/src/app/(app)/dashboard/page.tsx`
- `apps/web/src/app/(auth)/login/page.tsx`
- `apps/web/src/app/(auth)/register/page.tsx`
- `apps/web/src/app/(auth)/forgot-password/page.tsx`
- `apps/web/src/app/(auth)/reset-password/page.tsx`
- `apps/web/src/components/app-shell.tsx`
- `apps/web/src/components/app-sidebar.tsx`
- `apps/web/src/components/app-header.tsx`
- `apps/web/src/components/organisation-switcher.tsx`
- `apps/web/src/components/user-menu.tsx`
- `packages/ui/src/button.tsx`
- `packages/ui/src/dialog.tsx`
- `packages/ui/src/form-field.tsx`
- `packages/ui/src/input.tsx`
- `packages/ui/src/notification.tsx`
- `packages/ui/src/index.ts`
- `apps/web/package.json`
- `pnpm-lock.yaml`

## Mandatory design controls

- No browser-default input, select, textarea, or button styling.
- One deliberate typography system.
- Consistent spacing, borders, radius, elevation, and colour tokens.
- WCAG-conscious contrast.
- Visible keyboard focus.
- Mobile verification between 360 and 430 pixels.
- Tablet verification between 768 and 1024 pixels.
- Laptop verification between 1366 and 1440 pixels.
- Wide-desktop verification at approximately 1920 pixels.
- No hard-coded financial, tenancy, payment, or property statistics.
- No generic dashboard-template appearance.
- No production approval while principal journeys remain visually scaffolded.

## Gate 2

The interface passes only when principal journeys are presentable, responsive, accessible, permission-aware, and connected to live application data.

---

# Week 3: MTN MoMo and Airtel Money Real Sandbox Acceptance

## Objective

Prove that the provider-neutral payment architecture works through the official MTN MoMo and Airtel Money test environments, not only through mocked responses.

## MTN MoMo acceptance journey

1. Provision official MTN sandbox credentials.
2. Configure credentials only in runtime environment variables.
3. Create an eligible posted invoice.
4. Initiate a collection from the LandaFlow interface.
5. Persist the payment attempt before the outbound provider request.
6. Receive and retain the MTN provider reference.
7. Display the pending state.
8. Process a valid callback.
9. Query MTN before financial confirmation.
10. Create exactly one payment record.
11. Post exactly one balanced journal.
12. Allocate the payment once.
13. Issue one immutable receipt.
14. Reconcile the provider transaction.
15. Replay the callback and prove that no duplicate financial record is created.

## Airtel Money acceptance journey

1. Provision official Airtel sandbox credentials.
2. Validate token acquisition, expiry, and refresh.
3. Normalise the Ugandan phone number before submission.
4. Initiate the collection from the LandaFlow interface.
5. Verify pending, successful, failed, expired, and ambiguous responses.
6. Validate an accepted callback.
7. Reject an invalid callback.
8. Reject repeated or replayed events.
9. Simulate a provider timeout and outage.
10. Create and resolve a reconciliation exception through an authorised workflow.
11. Verify exactly one payment, journal, allocation, and receipt for a confirmed provider transaction.

## Deterministic simulation lab

The following scenarios must remain available locally, even after real sandbox validation:

- Request timeout
- HTTP 429 response
- HTTP 500 response
- Malformed JSON
- Invalid signature or callback authentication
- Incorrect amount
- Incorrect currency
- Delayed callback
- Duplicate callback
- Replayed event
- Unknown transaction
- Ambiguous provider state
- Confirmed callback followed by failed status query
- Provider reference belonging to another organisation

## Files to create

- `tests/provider/mtn-sandbox.acceptance.spec.ts`
- `tests/provider/airtel-sandbox.acceptance.spec.ts`
- `tests/provider/payment-timeout.simulation.spec.ts`
- `tests/provider/payment-replay.simulation.spec.ts`
- `tests/provider/payment-mismatch.simulation.spec.ts`
- `tests/provider/provider-outage.simulation.spec.ts`
- `tests/e2e/mtn-live-sandbox-journey.spec.ts`
- `tests/e2e/airtel-live-sandbox-journey.spec.ts`
- `docs/validation/mtn-sandbox-acceptance.md`
- `docs/validation/airtel-sandbox-acceptance.md`
- `docs/operations/provider-sandbox-runbook.md`
- `scripts/validate-mtn-sandbox.sh`
- `scripts/validate-airtel-sandbox.sh`

## Files likely to be modified

- `.env.example`
- `apps/api/src/payment-providers/mtn/mtn.client.ts`
- `apps/api/src/payment-providers/mtn/mtn.provider.ts`
- `apps/api/src/payment-providers/airtel/airtel.client.ts`
- `apps/api/src/payment-providers/airtel/airtel.provider.ts`
- `apps/api/src/payment-orchestration/payment-orchestration.service.ts`
- `apps/api/src/payment-orchestration/callback.service.ts`
- `apps/api/src/reconciliation/reconciliation-runner.service.ts`
- `apps/api/src/reconciliation/exception.service.ts`
- `apps/web/src/features/mobile-money/api.ts`
- `apps/web/src/features/mobile-money/components/payment-initiation-form.tsx`
- `apps/web/src/features/mobile-money/components/payment-status.tsx`
- `.github/workflows/ci.yml`
- `package.json`
- `pnpm-lock.yaml`

## Validation

- Valid sandbox transactions complete through each provider.
- Provider status verification occurs before financial confirmation.
- Confirmed transactions generate one payment, one balanced ledger outcome, one allocation, and one receipt.
- Duplicate or replayed callbacks do not duplicate financial records.
- Ambiguous states enter review.
- Provider outages preserve balances.
- Sandbox and simulated transactions are clearly labelled.
- No provider credential appears in source, fixtures, logs, audit events, or Git history.

## Gate 3

MTN and Airtel must complete the same acceptance matrix. Every provider-confirmed sandbox transaction must reconcile to exactly one internal financial outcome.

---

# Week 4: EFRIS UAT, JulyHost Deployment and Release Acceptance

## Objective

Complete the fiscal integration path, deploy the complete platform to JulyHost, and prove production-like operation through the public HTTPS endpoint.

## EFRIS end-to-end implementation

1. Complete the provider-neutral EFRIS fiscal schema and contracts.
2. Register for the URA EFRIS test environment.
3. Obtain the current System-to-System technical package assigned to the taxpayer profile.
4. Confirm the assigned EFRIS interface version before implementing the transport adapter.
5. Construct fiscal documents from posted LandaFlow invoices and receipts.
6. Snapshot taxable lines, buyer information, totals, currency, and source-document references.
7. Validate taxpayer-profile and EFRIS configuration data.
8. Generate a unique fiscal business key.
9. Submit through the official URA test interface.
10. Retain request and response checksums.
11. Map accepted, rejected, pending, cancelled, reversed, and exception states.
12. Preserve the URA fiscal identifier and response timestamp.
13. Prevent duplicate fiscal submission and response replay.
14. Support fiscal invoice, receipt, credit note, cancellation, and reversal flows.
15. Create exceptions without mutating ledger history.
16. Reconcile fiscal documents against LandaFlow invoices and receipts.
17. Display fiscal status and authorised exception actions in the interface.
18. Record user and automated actions in the audit log.
19. Prepare and execute URA-supervised UAT.

## Files to create

- `apps/api/src/efris/efris.module.ts`
- `apps/api/src/efris/efris.controller.ts`
- `apps/api/src/efris/efris.service.ts`
- `apps/api/src/efris/efris-client.ts`
- `apps/api/src/efris/efris-mapper.ts`
- `apps/api/src/efris/efris.types.ts`
- `apps/api/src/efris/fiscal-orchestration.service.ts`
- `apps/api/src/efris/fiscal-reconciliation.service.ts`
- `apps/api/src/efris/fiscal-exception.service.ts`
- `apps/api/src/efris/dto/submit-fiscal-document.dto.ts`
- `apps/api/src/efris/dto/list-fiscal-documents.dto.ts`
- `apps/api/src/efris/dto/resolve-fiscal-exception.dto.ts`
- `apps/api/src/efris/efris.service.spec.ts`
- `apps/api/src/efris/efris-mapper.spec.ts`
- `apps/api/src/efris/fiscal-orchestration.service.spec.ts`
- `apps/web/src/app/(app)/operations/fiscal-documents/page.tsx`
- `apps/web/src/app/(app)/operations/fiscal-documents/[fiscalDocumentId]/page.tsx`
- `apps/web/src/app/(app)/operations/fiscal-exceptions/page.tsx`
- `apps/web/src/features/efris/api.ts`
- `apps/web/src/features/efris/schemas.ts`
- `apps/web/src/features/efris/components/fiscal-document-list.tsx`
- `apps/web/src/features/efris/components/fiscal-status.tsx`
- `apps/web/src/features/efris/components/fiscal-exception-list.tsx`
- `apps/web/src/features/efris/components/resolve-fiscal-exception-dialog.tsx`
- `tests/provider/efris-contract.simulation.spec.ts`
- `tests/provider/efris-uat.acceptance.spec.ts`
- `tests/e2e/efris-fiscalisation.spec.ts`
- `tests/e2e/efris-credit-note.spec.ts`
- `tests/e2e/efris-replay-protection.spec.ts`
- `docs/integrations/efris-system-to-system.md`
- `docs/validation/efris-uat-readiness.md`
- `docs/validation/efris-test-acceptance.md`
- `docs/operations/efris-incident-response.md`

## Files likely to be modified

- `packages/config/src/env.ts`
- `.env.example`
- `apps/api/src/app.module.ts`
- `apps/api/src/audit/audit.types.ts`
- `packages/types/src/authorisation.ts`
- `apps/web/src/components/app-sidebar.tsx`
- `apps/web/src/app/globals.css`
- `.github/workflows/ci.yml`
- `package.json`
- `pnpm-lock.yaml`

## JulyHost production deployment

1. Provision the JulyHost package.
2. Create a dedicated production Unix user.
3. Install Docker Engine and Docker Compose.
4. Configure the repository deploy key.
5. Configure the production domain and DNS records.
6. Store production secrets only in the JulyHost environment configuration.
7. Start Caddy and verify automatic HTTPS.
8. Deploy PostgreSQL and Redis with persistent volumes.
9. Apply database migrations before enabling application traffic.
10. Build and start the web and API containers.
11. Generate a PostgreSQL backup.
12. Restore the backup into an isolated PostgreSQL database.
13. Restart all containers and prove persistent data remains available.
14. Run end-to-end acceptance tests against the public HTTPS endpoint.
15. Verify that MTN, Airtel, and EFRIS callback endpoints are publicly reachable over HTTPS.
16. Verify health, logs, audit events, alerts, and incident procedures.

## Files to create

- `infrastructure/julyhost/production.env.template`
- `infrastructure/julyhost/verify-deployment.sh`
- `infrastructure/julyhost/verify-callback-endpoints.sh`
- `infrastructure/julyhost/verify-persistence.sh`
- `infrastructure/julyhost/verify-backup-restoration.sh`
- `tests/e2e/public-deployment.spec.ts`
- `tests/e2e/public-provider-callbacks.spec.ts`
- `docs/validation/julyhost-production-acceptance.md`
- `docs/validation/final-release-acceptance.md`
- `docs/operations/production-cutover.md`
- `docs/operations/production-rollback.md`

## Files likely to be modified

- `infrastructure/julyhost/docker-compose.production.yml`
- `infrastructure/julyhost/Caddyfile`
- `infrastructure/julyhost/deploy.sh`
- `infrastructure/julyhost/rollback.sh`
- `infrastructure/julyhost/backup-postgres.sh`
- `infrastructure/julyhost/restore-postgres.sh`
- `Dockerfile.api`
- `Dockerfile.web`
- `.dockerignore`
- `.env.example`
- `.github/workflows/ci.yml`
- `docs/operations/julyhost-deployment.md`
- `docs/operations/backup-and-restoration.md`
- `docs/operations/release-checklist.md`
- `README.md`

## Gate 4

The deployed endpoint, Git commit, CI result, migration state, backup evidence, provider evidence, and acceptance evidence must all reference the same commit.

---

# External Provisioning Checklist

## MTN MoMo

- Create or confirm the sandbox developer account.
- Obtain Collections subscription credentials.
- Obtain the sandbox API user and API key.
- Register the HTTPS callback URL.
- Store values only in runtime secrets.
- Record credential owner, issue date, expiry, and rotation procedure outside Git.

## Airtel Money

- Create or confirm the Airtel developer account.
- Request sandbox application access.
- Obtain the client ID and client secret.
- Register the HTTPS callback URL.
- Confirm country and currency configuration for Uganda and UGX.
- Store values only in runtime secrets.

## URA EFRIS

- Register for the EFRIS test environment.
- Confirm the taxpayer profile used for integration.
- Download the current System-to-System technical package.
- Confirm the assigned API or interface version.
- Obtain test credentials and approved endpoint details.
- Complete the URA UAT readiness checklist.
- Schedule joint UAT with URA.
- Retain approval evidence outside the repository where it contains sensitive taxpayer information.

## JulyHost

- Provision the hosting package.
- Obtain server hostname, IP address, SSH username, and deployment-key requirements.
- Configure the public domain and DNS.
- Confirm inbound ports 80 and 443.
- Confirm persistent storage and backup capacity.
- Confirm whether SMTP relay is available or whether a separate email service is required.

---

# Concurrent Development Rules

1. Sprint 05 owns product journeys, dashboard improvements, tenant experience, notifications, maintenance workflows, reporting interfaces, and visual refinement.
2. Sprint 06 owns EFRIS, provider acceptance, security hardening, performance, deployment, recovery, and final release evidence.
3. The following shared files require coordination before modification:

   - `apps/web/src/app/globals.css`
   - `apps/web/src/app/layout.tsx`
   - `apps/web/src/app/(app)/layout.tsx`
   - `apps/web/src/components/app-shell.tsx`
   - `apps/web/src/components/app-sidebar.tsx`
   - `apps/web/src/components/app-header.tsx`
   - `packages/ui/src/index.ts`
   - `package.json`
   - `pnpm-lock.yaml`
   - `packages/database/prisma/schema.prisma`
   - `packages/database/prisma/seed.ts`
   - `.env.example`
   - `.github/workflows/ci.yml`
   - `docker-compose.yml`
   - `infrastructure/julyhost/docker-compose.production.yml`

4. Dependency and lockfile changes must not be duplicated across competing pull requests.
5. Every Sprint 06 phase must fetch and inspect upstream and collaborator branches before implementation.
6. Incoming changes must be reviewed before integration and fully validated afterward.
7. Every completed phase must be committed and pushed to the dedicated development branch.
8. Pull requests must contain scope, implementation, controls, validation evidence, deployment impact, risks, rollback considerations, and reviewer focus.
9. No pull request may be submitted while required checks fail.

---

# Final Release Acceptance Matrix

| Capability | Local simulation | Provider sandbox or test | Public HTTPS deployment | Production approval |
|---|---:|---:|---:|---:|
| Authentication and sessions | Required | Not applicable | Required | Required |
| Organisation isolation and permissions | Required | Not applicable | Required | Required |
| Property, tenancy, and documents | Required | Not applicable | Required | Required |
| Billing and double-entry ledger | Required | Not applicable | Required | Required |
| MTN MoMo collections | Required | Required | Required | Required |
| Airtel Money collections | Required | Required | Required | Required |
| Reconciliation and exceptions | Required | Required | Required | Required |
| EFRIS fiscalisation | Required | Required | Required | URA UAT required |
| User interface and accessibility | Required | Not applicable | Required | Required |
| Backup and restoration | Required | Not applicable | Required | Required |
| Monitoring and incident response | Required | Not applicable | Required | Required |
| Security and dependency review | Required | Not applicable | Required | Required |

---

# Final Completion Conditions

LandaFlow MVP will be considered production-ready only when all of the following are true:

1. Sprint 05 interface and operational journeys are integrated.
2. The professional UI release gate passes.
3. MTN MoMo sandbox acceptance passes.
4. Airtel Money sandbox acceptance passes.
5. EFRIS test submission and URA UAT readiness pass.
6. JulyHost is provisioned and the public HTTPS deployment is healthy.
7. Database migrations apply to an empty database.
8. Backup creation and isolated restoration pass.
9. Provider callbacks are reachable and secure.
10. Trial balance remains equal after all financial acceptance scenarios.
11. No duplicate payment, receipt, ledger, provider-event, or fiscal-document state is produced.
12. No unresolved critical or high-severity security defect remains.
13. No credential or sensitive taxpayer secret exists in Git history.
14. CI checks, deployment evidence, provider evidence, and acceptance evidence match the release commit.
15. Rollback procedures are tested and documented.

## Revised overall timeline

- **Week 1:** Integration audit and contract correction
- **Week 2:** Professional UI integration and product-level remediation
- **Week 3:** MTN MoMo and Airtel Money real sandbox acceptance
- **Week 4:** EFRIS UAT readiness, JulyHost deployment, and final release acceptance
- **External contingency:** Five to ten working days for provider approval, credential issuance, or URA-led UAT scheduling

This timeline preserves completed engineering work while correcting the omitted end-to-end proof, real-provider validation, interface quality, deployment, and operational-readiness requirements.
