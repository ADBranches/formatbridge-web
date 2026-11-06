# LandaFlow Sprint 06

## EFRIS Integration, Security Hardening and Production Release

**Sprint duration:** One week  
**Delivery model:** Parallel team delivery through small, reviewable pull requests  
**Deployment target:** JulyHost production environment after package provisioning  
**Cost constraint:** Free-tier, sandbox, open-source, or self-hosted services wherever possible  
**Prerequisite:** Sprints 01–05 approved and merged, with verified property, tenancy, billing, ledger, Mobile Money, reconciliation, tenant, maintenance, notification, reporting, audit, CI, backup, and restoration contracts available on the integration branch

---

## 1. Sprint Objective

Complete the LandaFlow MVP by integrating the Uganda Revenue Authority EFRIS sandbox, hardening the platform against production security and resilience risks, validating performance and disaster recovery, provisioning the real JulyHost environment, conducting pilot acceptance, and producing the operational evidence required for a controlled release.

Sprint 06 is the final planned MVP sprint. Production release must not proceed on mock infrastructure, unresolved critical or high-severity defects, unverified backups, failing CI, incomplete access controls, or unapproved fiscal and payment-provider configurations.

---

## 2. Sprint Outcomes

At completion:

1. Eligible invoices and receipts can be mapped to EFRIS fiscal-document contracts.
2. EFRIS sandbox submissions are authenticated, idempotent, traceable, and recoverable.
3. Fiscal-document failures cannot corrupt the financial ledger.
4. Security controls pass final authentication, authorisation, tenancy-isolation, secret, dependency, and abuse-case testing.
5. Performance tests establish practical MVP operating thresholds.
6. Backup restoration and disaster-recovery procedures are verified.
7. The real JulyHost environment is provisioned with DNS, HTTPS, persistent data, migrations, health checks, and restricted secrets.
8. MTN, Airtel, email, and EFRIS production integrations remain disabled until approved credentials exist.
9. Pilot users complete the critical end-to-end journeys.
10. Release, rollback, incident-response, support, and operator runbooks are complete.
11. CI, end-to-end acceptance, accessibility, vulnerability, and production-smoke checks pass on the release commit.
12. The MVP has no unresolved critical or high-severity defect.

---

## 3. Scope Boundaries

### Included

- URA EFRIS sandbox integration foundation
- Fiscal invoice, receipt, credit-note, and status mapping
- EFRIS submission, retry, response, and exception workflows
- Final authentication, session, role, tenant, and organisation security review
- Dependency, secret, container, and configuration scanning
- Performance, concurrency, reliability, and failure-recovery testing
- Real JulyHost provisioning and deployment
- DNS, Caddy HTTPS, persistent volumes, migrations, backups, and restoration
- Pilot-data preparation and user-acceptance testing
- Release documentation, runbooks, incident response, and handover

### Excluded

- Unapproved production EFRIS activation
- Unapproved live Mobile Money merchant processing
- Paid SMS or WhatsApp production delivery
- Native Android or iOS applications
- Advanced tax advisory or legal interpretation
- Multi-country fiscal compliance
- Artificial-intelligence features
- Enterprise data warehouse or business-intelligence tooling
- Microservices decomposition
- Features beyond the agreed MVP

---

## 4. Release Conventions

### Fiscal authority

EFRIS responses and identifiers are retained as external fiscal evidence. LandaFlow's double-entry ledger remains the internal financial system of record. EFRIS submission must never rewrite posted ledger history.

### Idempotency

Every fiscal submission uses a stable business key linked to one eligible invoice, receipt, credit note, or reversal. Retries must return or reconcile the original submission rather than create duplicate fiscal documents.

### Production activation

EFRIS, MTN Mobile Money, Airtel Money, email, SMS, and WhatsApp production adapters remain disabled until credentials, approval, callback URLs, and responsible owners are documented.

### Release integrity

The deployed commit, CI evidence, migration set, container image tags, environment checksum, acceptance record, backup identifier, and rollback target must all refer to the same release candidate.

### Severity threshold

No unresolved critical or high-severity security, data-integrity, payment, fiscal, tenancy-isolation, backup, or availability defect may enter production.

### Evidence boundary

Mock acceptance, sandbox acceptance, and public production acceptance must remain clearly distinguished in documentation and pull requests.

---

## 5. Phase 1: EFRIS Data and Contract Foundation

### Objective

Establish fiscal-document, submission, response, status-history, and exception models without coupling the ledger to provider-specific payloads.

### Work

1. Add EFRIS configuration and taxpayer-profile models.
2. Add fiscal-document and fiscal-line models.
3. Add submission-attempt, response, status-history, and exception models.
4. Define invoice, receipt, credit-note, cancellation, and reversal mappings.
5. Add unique business keys, provider identifiers, indexes, and replay controls.
6. Preserve original response checksums without persisting unnecessary sensitive data.
7. Add safe non-production fixtures.
8. Document fiscal lifecycle, retention, and rollback considerations.

### Files to create

- `packages/types/src/efris.ts`
- `packages/database/src/fiscal-scope.ts`
- `packages/database/src/fiscal-scope.spec.ts`
- `packages/database/prisma/migrations/<timestamp>_efris_fiscal_documents/migration.sql`
- `docs/architecture/efris-fiscal-model.md`
- `docs/architecture/fiscal-document-lifecycle.md`

### Files likely to be modified

- `packages/database/prisma/schema.prisma`
- `packages/database/prisma/seed.ts`
- `packages/database/src/index.ts`
- `packages/types/src/index.ts`
- `docs/development/database-migrations.md`

### Required models

- `EfrisConfiguration`
- `FiscalDocument`
- `FiscalDocumentLine`
- `FiscalSubmissionAttempt`
- `FiscalResponse`
- `FiscalStatusHistory`
- `FiscalException`

### Validation

```text
pnpm --filter @landaflow/database prisma validate
pnpm --filter @landaflow/database prisma migrate deploy
pnpm --filter @landaflow/database seed
pnpm --filter @landaflow/database test
```

### Completion evidence

- Migrations apply to an empty PostgreSQL database.
- Duplicate fiscal business keys and provider identifiers are rejected.
- Fiscal records cannot reference another organisation's invoices or receipts.
- Repeated responses cannot duplicate fiscal-document state.
- Production seed execution remains prohibited.
- No EFRIS credential appears in tracked fixtures or seed files.

---

## 6. Phase 2: EFRIS Adapter and Sandbox Integration

### Objective

Implement a provider-isolated EFRIS sandbox adapter with validated configuration, authentication, payload mapping, status verification, retries, and safe error translation.

### Work

1. Define the EFRIS adapter interface and sandbox client.
2. Validate taxpayer identity and sandbox environment configuration.
3. Map LandaFlow invoices, receipts, credits, and reversals to fiscal contracts.
4. Implement authentication and request signing required by the approved sandbox contract.
5. Add bounded retries for idempotent operations.
6. Add submission-status verification.
7. Map provider statuses and errors into internal categories.
8. Redact credentials, signatures, tokens, and sensitive payload fields.
9. Add deterministic contract tests using mocked sandbox responses.
10. Document URA sandbox onboarding and credential handling.

### Files to create

- `apps/api/src/efris/efris.module.ts`
- `apps/api/src/efris/efris-provider.interface.ts`
- `apps/api/src/efris/efris.client.ts`
- `apps/api/src/efris/efris.mapper.ts`
- `apps/api/src/efris/efris.service.ts`
- `apps/api/src/efris/efris.types.ts`
- `apps/api/src/efris/efris-error.ts`
- `apps/api/src/efris/efris.client.spec.ts`
- `apps/api/src/efris/efris.mapper.spec.ts`
- `apps/api/src/efris/efris.service.spec.ts`
- `docs/integrations/ura-efris-sandbox.md`

### Files likely to be modified

- `apps/api/src/app.module.ts`
- `packages/config/src/env.ts`
- `.env.example`
- `turbo.json`
- `apps/api/src/common/interceptors/request-logging.interceptor.ts`
- `infrastructure/julyhost/.env.production.example`

### Required environment variables

- `EFRIS_ENABLED`
- `EFRIS_ENVIRONMENT`
- `EFRIS_BASE_URL`
- `EFRIS_TIN`
- `EFRIS_DEVICE_NUMBER`
- `EFRIS_CLIENT_ID`
- `EFRIS_CLIENT_SECRET`
- `EFRIS_PRIVATE_KEY_PATH`
- `EFRIS_REQUEST_TIMEOUT_MS`

### Validation

- Missing values stop startup only when EFRIS is enabled.
- Disabled EFRIS does not block core MVP operation.
- Fiscal payloads reconcile to posted source documents.
- Authentication and signatures follow the approved sandbox contract.
- Retries do not duplicate fiscal submissions.
- Provider errors do not expose internal credentials or payloads.
- Configuration secrets remain absent from Git, logs, audits, and fixtures.

---

## 7. Phase 3: Fiscal Orchestration and Exception Handling

### Objective

Coordinate eligible-document selection, submission, status verification, fiscal evidence, controlled retries, exceptions, and operator resolution.

### Work

1. Add fiscal-submission endpoints and background processing.
2. Validate source financial document eligibility.
3. Persist submission intent before external communication.
4. Use stable idempotency and correlation identifiers.
5. Store safe response evidence and fiscal identifiers.
6. Add status polling for unresolved submissions.
7. Create exceptions for rejection, ambiguity, timeout, mapping conflict, and provider outage.
8. Add controlled retry, reject, acknowledge, and compensating-document operations.
9. Prevent direct modification of posted financial or fiscal history.
10. Emit complete audit events.

### Files to create

- `apps/api/src/fiscal/fiscal.module.ts`
- `apps/api/src/fiscal/fiscal.controller.ts`
- `apps/api/src/fiscal/fiscal.service.ts`
- `apps/api/src/fiscal/fiscal-runner.service.ts`
- `apps/api/src/fiscal/fiscal-exception.service.ts`
- `apps/api/src/fiscal/dto/submit-fiscal-document.dto.ts`
- `apps/api/src/fiscal/dto/list-fiscal-documents.dto.ts`
- `apps/api/src/fiscal/dto/resolve-fiscal-exception.dto.ts`
- `apps/api/src/fiscal/fiscal.service.spec.ts`
- `apps/api/src/fiscal/fiscal-exception.service.spec.ts`
- `docs/architecture/fiscal-orchestration.md`

### Files likely to be modified

- `apps/api/src/billing/billing.service.ts`
- `apps/api/src/payments/receipt.service.ts`
- `apps/api/src/adjustments/adjustments.service.ts`
- `apps/api/src/audit/audit.types.ts`
- `packages/types/src/authorisation.ts`

### Required permissions

- `fiscal.read`
- `fiscal.submit`
- `fiscal.exception.read`
- `fiscal.exception.manage`

### Validation

- Draft, voided, or ineligible financial documents cannot be submitted.
- One business key produces one fiscal submission.
- Repeated responses do not duplicate fiscal identifiers.
- Rejected documents enter review without altering the ledger.
- Credit and reversal documents reference the original fiscal document.
- Cross-organisation identifiers cannot submit or resolve fiscal records.
- Exception resolution requires permission, reason, and audit evidence.

---

## 8. Phase 4: Final Security Hardening

### Objective

Complete production-focused security verification for authentication, sessions, authorisation, tenancy isolation, input handling, secrets, dependencies, containers, headers, and abuse resistance.

### Work

1. Review the application against OWASP ASVS Level 1 and relevant Level 2 controls.
2. Review API risks against the OWASP API Security Top 10.
3. Add brute-force, session-reuse, refresh replay, reset-token, and enumeration tests.
4. Add cross-organisation and cross-tenant object-level authorisation tests.
5. Add request-size, malformed-payload, path-traversal, CSV-injection, and upload-abuse tests.
6. Validate CORS, CSP, HSTS, secure cookies, headers, and reverse-proxy trust.
7. Scan dependencies, Git history, containers, and production configuration.
8. Remove unnecessary runtime privileges and exposed ports.
9. Review audit immutability and sensitive-field redaction.
10. Produce a remediation record with severity, owner, and disposition.

### Files to create

- `tests/security/authentication-abuse.spec.ts`
- `tests/security/session-replay.spec.ts`
- `tests/security/object-authorisation.spec.ts`
- `tests/security/input-and-upload-abuse.spec.ts`
- `tests/security/security-headers.spec.ts`
- `docs/security/security-hardening-assessment.md`
- `docs/security/owasp-asvs-checklist.md`
- `docs/security/release-risk-register.md`

### Files likely to be modified

- `apps/api/src/main.ts`
- `apps/web/next.config.ts`
- `infrastructure/julyhost/Caddyfile`
- `infrastructure/julyhost/docker-compose.production.yml`
- `.github/workflows/ci.yml`
- `.github/workflows/dependency-review.yml`
- `Dockerfile.api`
- `Dockerfile.web`

### Validation

- Authentication and recovery public responses resist enumeration.
- Refresh-token reuse and replay are rejected.
- Object-level authorisation rejects valid identifiers from another organisation or tenant.
- Upload and path-traversal attempts fail safely.
- CSV exports neutralise formula injection.
- Production cookies carry `Secure`, `HttpOnly`, and appropriate `SameSite` attributes.
- Public responses contain no stack traces, SQL, Prisma details, or credentials.
- Secret and dependency scans have no unresolved critical or high-severity finding.

---

## 9. Phase 5: Performance, Resilience and Recovery

### Objective

Establish practical MVP capacity, timeout, retry, degraded-dependency, backup, restoration, and disaster-recovery evidence.

### Work

1. Define representative read and write workloads.
2. Add load tests for authentication, dashboards, properties, invoices, payments, maintenance, and readiness.
3. Measure latency, throughput, error rate, CPU, memory, and database connections.
4. Validate pagination and query-index behaviour.
5. Test PostgreSQL, Redis, email, Mobile Money, and EFRIS dependency failures.
6. Test container restart and persistent-volume recovery.
7. Verify scheduled backups and isolated restoration.
8. Define recovery-time and recovery-point targets for the MVP.
9. Document capacity thresholds and scaling triggers.
10. Confirm background-job idempotency after restart.

### Files to create

- `tests/performance/k6-authentication.js`
- `tests/performance/k6-dashboard.js`
- `tests/performance/k6-financial-journeys.js`
- `tests/performance/k6-maintenance.js`
- `scripts/validate-disaster-recovery.sh`
- `docs/operations/performance-baseline.md`
- `docs/operations/disaster-recovery.md`
- `docs/operations/capacity-and-scaling.md`

### Files likely to be modified

- `docker-compose.yml`
- `infrastructure/julyhost/docker-compose.production.yml`
- `apps/api/src/health/health.service.ts`
- `docs/operations/backup-and-restoration.md`
- `docs/operations/release-checklist.md`

### Initial MVP thresholds

- Liveness p95 below 250 ms under normal test load
- Read API p95 below 750 ms for indexed, paginated queries
- Write API p95 below 1,500 ms excluding external-provider latency
- Application error rate below 1% during the agreed baseline test
- No lost or duplicated financial, payment, notification, or fiscal operation after controlled restart
- Verified daily backup procedure
- Target recovery point of 24 hours or better until more frequent backups are funded
- Target recovery time of 4 hours or better for the initial pilot

### Validation

- Load tests meet documented thresholds or produce an approved capacity limitation.
- Dependency outages return safe degraded states.
- Restarted workers do not duplicate business operations.
- Persistent data survives container recreation.
- Backup catalogue validates and isolated restoration succeeds.
- Restored data includes migrations, organisations, tenancies, ledger, payments, maintenance, notifications, audit, and fiscal records.

---

## 10. Phase 6: Real JulyHost Production Provisioning

### Objective

Replace Sprint 01 mock deployment placeholders with a real, secured, observable JulyHost production environment.

### Work

1. Provision the approved JulyHost package.
2. Create a restricted deployment user and install the approved SSH public key.
3. Configure firewall access for SSH, HTTP, and HTTPS only.
4. Configure production DNS.
5. Generate independent production secrets on the host.
6. Deploy PostgreSQL, Redis, migration, API, web, and Caddy services.
7. Verify Caddy certificate issuance and HTTPS redirection.
8. Verify persistent volumes across container restart and recreation.
9. Configure scheduled PostgreSQL backups and encrypted off-host copies.
10. Record endpoint, commit, image identifiers, migration state, volume state, and backup evidence.
11. Keep live MTN, Airtel, email, SMS, WhatsApp, and EFRIS adapters disabled until their production credentials are approved.

### Files to create

- `infrastructure/julyhost/provision-server.sh`
- `infrastructure/julyhost/configure-firewall.sh`
- `infrastructure/julyhost/install-backup-schedule.sh`
- `infrastructure/julyhost/verify-production.sh`
- `docs/operations/julyhost-production-record.md`
- `docs/validation/production-deployment-evidence.md`

### Files likely to be modified

- `infrastructure/julyhost/docker-compose.production.yml`
- `infrastructure/julyhost/Caddyfile`
- `infrastructure/julyhost/.env.production.example`
- `infrastructure/julyhost/deploy.sh`
- `infrastructure/julyhost/rollback.sh`
- `infrastructure/julyhost/backup-postgres.sh`
- `infrastructure/julyhost/restore-postgres.sh`
- `docs/operations/julyhost-deployment.md`

### Validation

```text
docker compose -f infrastructure/julyhost/docker-compose.production.yml config
curl -I http://<production-domain>
curl -I https://<production-domain>
curl https://<production-domain>/api/health/live
curl https://<production-domain>/api/health/ready
```

### Completion evidence

- DNS resolves to the JulyHost server.
- HTTP redirects to HTTPS.
- The TLS certificate is valid and HSTS is present.
- PostgreSQL, Redis, API, web, and Caddy are healthy.
- Migrations finish before application traffic is accepted.
- Production secrets exist only on the host with restricted permissions.
- Database and application data survive container restart and recreation.
- Backup creation and isolated restoration pass.
- The deployed commit and endpoint are recorded.

---

## 11. Phase 7: Pilot Acceptance and Operational Readiness

### Objective

Complete role-based pilot acceptance, production smoke tests, operator training, support preparation, and release decision evidence.

### Work

1. Create sanitised pilot organisations, properties, units, tenants, agreements, invoices, and operational records.
2. Conduct owner, property-manager, accountant, support-viewer, and tenant acceptance journeys.
3. Validate registration, sign-in, recovery, organisation onboarding, property management, tenancy, billing, payments, reconciliation, reminders, maintenance, reports, and sign-out.
4. Validate sandbox fiscal submission and exception handling.
5. Verify operator access to health, logs, audit events, backups, and incident runbooks.
6. Verify no pilot data contains unapproved real personal or payment information.
7. Record defects, owners, severity, remediation, and retest evidence.
8. Conduct release, rollback, and incident-response walkthroughs.
9. Obtain named approval from required reviewers.

### Files to create

- `tests/e2e/production-smoke.spec.ts`
- `tests/e2e/pilot-owner-journey.spec.ts`
- `tests/e2e/pilot-manager-journey.spec.ts`
- `tests/e2e/pilot-accountant-journey.spec.ts`
- `tests/e2e/pilot-tenant-journey.spec.ts`
- `tests/e2e/pilot-support-journey.spec.ts`
- `docs/validation/pilot-acceptance.md`
- `docs/operations/operator-training.md`
- `docs/operations/support-handover.md`
- `docs/operations/incident-response.md`

### Validation

- Every role completes only authorised journeys.
- Tenant and organisation isolation remain intact.
- Production smoke tests pass over HTTPS.
- Audit records identify actors, organisations, actions, and affected records.
- Logs remain readable and credential-free.
- Backup and restoration operators can follow the runbook successfully.
- Rollback limitations and migration compatibility are understood.
- All critical and high-severity defects are resolved and retested.

---

## 12. Phase 8: Release Candidate, Acceptance and Handover

### Objective

Create the final MVP release candidate, prove all quality gates, publish acceptance evidence, and prepare the controlled production-release pull request and tag.

### Work

1. Freeze MVP scope and release candidate.
2. Validate all migrations from an empty database.
3. Run unit, integration, browser, security, accessibility, performance, backup, restoration, and production-smoke tests.
4. Run dependency, secret, container, and configuration scans.
5. Confirm production environment, DNS, HTTPS, persistence, observability, and backups.
6. Verify release and rollback procedures against the candidate commit.
7. Produce final risk register and known limitations.
8. Prepare a comprehensive release pull request.
9. Create the release tag only after approval and merge.
10. Publish operator, support, development, and pilot handover documentation.

### Files to create

- `docs/validation/sprint-06-acceptance.md`
- `docs/validation/mvp-release-acceptance.md`
- `docs/operations/production-runbook.md`
- `docs/operations/release-and-rollback.md`
- `docs/operations/known-limitations.md`
- `docs/operations/post-release-monitoring.md`
- `CHANGELOG.md`

### Files likely to be modified

- `.github/workflows/ci.yml`
- `.github/workflows/dependency-review.yml`
- `README.md`
- `SECURITY.md`
- `package.json`
- `docs/operations/release-checklist.md`
- `infrastructure/julyhost/docker-compose.production.yml`

### Validation commands

```text
pnpm install --frozen-lockfile
pnpm --filter @landaflow/database prisma validate
pnpm --filter @landaflow/database prisma migrate deploy
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm build
docker compose config
docker compose up --build -d
docker compose ps
```

### Completion evidence

1. Empty-database migrations pass from Sprint 01 through Sprint 06.
2. All unit, integration, browser, accessibility, and security tests pass.
3. Performance results meet approved MVP thresholds or documented capacity limits.
4. EFRIS sandbox submission, status, retry, and exception tests pass.
5. Cross-organisation, cross-tenant, session, payment, ledger, notification, maintenance, export, and fiscal controls pass.
6. Real JulyHost HTTPS deployment and health checks pass.
7. Persistent data survives restart and recreation.
8. Backup and isolated restoration pass with complete representative data.
9. CI quality gates pass on the release commit.
10. Dependency, secret, and container scans have no unresolved critical or high-severity finding.
11. Pilot acceptance and required reviewer approvals are recorded.
12. The release pull request evidence matches the submitted commit.

---

## 13. Team Work Allocation

### Platform and Infrastructure Team

Owns:

- JulyHost provisioning and production deployment
- DNS, Caddy, HTTPS, firewall, SSH, volumes, and backups
- CI, scanning, performance infrastructure, and release automation
- Disaster recovery, monitoring, and operational runbooks

### Backend and Data Team

Owns:

- EFRIS data model and sandbox adapter
- Fiscal orchestration and exceptions
- Migration integrity and representative restoration
- Performance-sensitive API and database corrections
- Audit and fiscal-document integration

### Web Experience Team

Owns:

- Fiscal-document and exception interfaces
- Final responsive and accessibility corrections
- Production error, loading, unauthorised, offline, and degraded states
- Pilot and production browser journeys

### Quality and Security Review

Owns:

- OWASP ASVS and API-security assessment
- Object-level authorisation and session testing
- Dependency, secret, container, and configuration review
- Performance, resilience, backup, and disaster-recovery evidence
- Pilot acceptance and release-readiness assessment

Teams may work concurrently only after EFRIS contracts, production environment boundaries, release thresholds, test data, and deployment responsibilities are reviewed. Production secrets must never be shared through pull requests, chat, terminal-result files, or tracked configuration.

---

## 14. Branch and Pull-Request Plan

Recommended branches:

```text
foundation/efris-fiscal-model
feature/efris-sandbox-adapter
feature/fiscal-orchestration
security/final-hardening
operations/performance-recovery
operations/julyhost-production
operations/pilot-acceptance
release/mvp-candidate
```

Every pull request must include:

1. A precise capability-focused title.
2. Scope and affected fiscal, security, operational, or release journeys.
3. Technical implementation details.
4. Organisation, tenant, session, payment, fiscal, and privacy controls.
5. Database and migration impact.
6. Validation commands and complete results.
7. Deployment, DNS, HTTPS, configuration, and credential impact.
8. Risks, known limitations, and severity assessment.
9. Rollback, migration, and compensating-document considerations.
10. Reviewer focus areas.
11. Screenshots only where they verify interface behaviour.

A pull request must not be merged when required checks fail, EFRIS idempotency is unverified, fiscal history can be silently edited, access controls are incomplete, critical or high-severity defects remain, backups or restoration are unverified, production secrets are exposed, deployment evidence does not match the commit, required review is missing, or public acceptance is represented by mock evidence.

---

## 15. Sprint Security and Release Controls

- EFRIS is disabled unless explicitly configured.
- Fiscal submissions use stable business keys and retain traceable evidence.
- Fiscal failures never rewrite posted ledger history.
- Production credentials exist only in restricted host configuration.
- Cross-organisation and cross-tenant object access is tested explicitly.
- Refresh replay, reset-token reuse, brute force, and enumeration controls are verified.
- Upload, path, CSV, request-size, and malformed-input abuse cases are tested.
- Public responses contain no stack traces, Prisma errors, SQL, secrets, or provider payloads.
- Containers expose only required public ports and use least practical privilege.
- CI blocks release on failed validation.
- Production data, backups, and secrets never enter Git.
- Real JulyHost evidence replaces mock placeholders before release.
- Backup and restoration evidence is mandatory.
- Release and rollback targets reference verified commits.

---

## 16. Definition of Done

Sprint 06 and the planned LandaFlow MVP are complete only when:

1. Every phase is implemented and reviewed.
2. EFRIS sandbox models, mapping, submission, status, retry, and exceptions pass.
3. All migrations apply to an empty database.
4. All functional, browser, accessibility, security, and performance tests pass.
5. Cross-organisation and tenant isolation remain intact.
6. Financial and fiscal histories remain immutable and traceable.
7. Real JulyHost deployment, DNS, HTTPS, persistence, health, and logs pass.
8. Backup and isolated restoration preserve complete representative data.
9. Pilot acceptance is completed and signed off.
10. CI and scanning checks pass on the final commit.
11. No unresolved critical or high-severity defect remains.
12. Release, rollback, incident, support, and operator runbooks are complete.
13. The release branch is pushed and a comprehensive pull request exists.
14. The production endpoint, commit, tag, image identifiers, migrations, and evidence are recorded.
15. Production provider activation status is explicit for EFRIS, MTN, Airtel, email, SMS, and WhatsApp.

---

## 17. Post-MVP Handover

After Sprint 06, work moves from planned MVP construction into controlled pilot operation and prioritised product development.

The immediate post-release backlog should include:

- Real provider onboarding and production certification where still pending
- Higher-frequency and encrypted off-host backups
- Prometheus, Grafana, and OpenTelemetry observability expansion
- Production email, SMS, and WhatsApp decisions based on approved cost
- Native application assessment only after PWA usage evidence
- Advanced accounting exports and integrations
- Vendor and maintenance-cost management
- Property-owner portfolio analytics
- Additional Ugandan compliance requirements identified during pilot operation
- Multi-country localisation only after Uganda-first stability

No post-MVP feature should bypass the organisation-isolation, ledger, payment-verification, audit, notification, maintenance, security, CI, backup, and release contracts established across Sprints 01–06.
