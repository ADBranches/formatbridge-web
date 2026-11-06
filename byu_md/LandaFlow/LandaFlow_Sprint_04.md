# LandaFlow Sprint 04

## Mobile Money Integrations and Payment Reconciliation

**Sprint duration:** One week  
**Delivery model:** Parallel team delivery through small, reviewable pull requests  
**Deployment target:** JulyHost-compatible, cloud-neutral Docker deployment  
**Cost constraint:** Free-tier, sandbox, open-source, or self-hosted services only  
**Prerequisite:** Sprint 03 approved and merged, with verified invoice, payment, allocation, receipt, double-entry ledger, organisation-isolation, audit, CI, backup, and restoration contracts available on the integration branch

---

## 1. Sprint Objective

Deliver a provider-neutral payment integration foundation for MTN Mobile Money and Airtel Money sandbox environments, with secure payment initiation, callback validation, provider-status verification, replay protection, duplicate-payment prevention, automated ledger posting, reconciliation, exception handling, and operational visibility.

Sprint 04 must consume the verified Sprint 03 payment and ledger services. Provider callbacks must never post financial value directly or bypass the existing idempotent payment-recording, allocation, receipt, and double-entry controls.

---

## 2. Sprint Outcomes

At completion:

1. LandaFlow supports provider-neutral Mobile Money payment initiation.
2. MTN Mobile Money and Airtel Money sandbox adapters implement one shared contract.
3. Provider credentials remain encrypted or environment-supplied and never enter Git, logs, or audit payloads.
4. Callback authenticity, replay protection, and duplicate prevention are enforced.
5. Provider status is verified before any payment is confirmed.
6. Confirmed provider payments enter the Sprint 03 ledger exactly once.
7. Failed, expired, cancelled, timed-out, and ambiguous transactions remain distinguishable.
8. Automated reconciliation identifies matched, unmatched, duplicated, underpaid, overpaid, and conflicting transactions.
9. Operators can investigate and resolve payment exceptions through permission-controlled workflows.
10. Tenants and managers can view accurate, live payment status without seeing provider secrets.
11. Cross-organisation identifiers cannot expose or post another organisation's transactions.
12. Provider outages do not corrupt invoices, allocations, receipts, or ledger balances.
13. CI, browser, sandbox, security, backup, and restoration checks pass before review.

---

## 3. Scope Boundaries

### Included

- Provider-adapter architecture
- MTN Mobile Money sandbox integration
- Airtel Money sandbox integration
- Collection-request initiation
- Callback or webhook processing
- Provider transaction-status polling
- Idempotency and replay protection
- Payment-attempt lifecycle management
- Provider-confirmed payment posting through the existing ledger
- Automated and manual reconciliation
- Payment-exception queues and resolution
- Operational dashboards and tenant-facing payment status
- Provider-health and structured-log visibility
- Sprint 04 acceptance evidence

### Excluded

- Production merchant activation or live-money movement
- Disbursements, payouts, or refunds through provider APIs
- Bank-card acquiring
- Bank-feed integrations
- Cross-border payments
- Currency conversion
- SMS or WhatsApp delivery charges
- Chargebacks beyond internal exception recording
- EFRIS fiscal documents
- Advanced fraud-scoring vendors
- Production settlement-account reconciliation

---

## 4. Payment Integration Conventions

### Provider abstraction

Application services must depend on a `PaymentProvider` interface rather than MTN- or Airtel-specific classes. Provider request and response formats remain inside adapter modules.

### Payment authority

A client redirect, browser response, or callback alone does not establish financial truth. A payment becomes `CONFIRMED` only after authenticated callback processing or explicit provider-status verification satisfies the adapter contract.

### Idempotency

Every initiation, callback, status update, posting, allocation, and receipt operation must use stable idempotency or business keys. Retries must return the original result without duplicating financial value.

### Replay protection

Callbacks require provider-specific authentication plus timestamp, nonce, event identifier, or transaction-reference controls where the sandbox supports them. Processed provider events must be retained and rejected on replay.

### Phone numbers

Mobile numbers must be normalised to E.164 format. Uganda numbers use the `+256` country code. Raw user formatting must not be sent directly to providers.

### Monetary values

All amounts use integer currency units. The adapter must reject provider amounts or currencies that do not match the initiated payment intent.

### Ledger integration

Only the verified Sprint 03 payment service may create the confirmed payment, allocation, journal entries, and receipt. Provider adapters never write ledger entries directly.

### Organisation isolation

Every payment attempt, provider event, reconciliation record, and exception must derive or verify `organisationId`, tenant, invoice, and payment intent relationships.

### Sensitive data

Provider secrets, access tokens, callback credentials, full authentication headers, PINs, OTPs, and raw sensitive payloads must not be stored in application logs or audit records.

---

## 5. Phase 1: Provider-Neutral Payment Data Foundation

### Objective

Establish payment-attempt, provider-event, reconciliation, and exception models with strict lifecycle, uniqueness, indexing, and organisation-isolation controls.

### Work

1. Add payment-provider and payment-attempt models.
2. Add provider-event and status-history models.
3. Add reconciliation-run, reconciliation-item, and payment-exception models.
4. Define provider-neutral transaction states.
5. Add unique provider reference, event identifier, idempotency, and replay-prevention constraints.
6. Index organisation, provider, status, invoice, tenant, timestamps, and reconciliation fields.
7. Add safe non-production seed data without provider credentials.
8. Document lifecycle and rollback considerations.

### Files to create

- `packages/types/src/payment-providers.ts`
- `packages/types/src/reconciliation.ts`
- `packages/database/src/provider-payment-scope.ts`
- `packages/database/src/provider-payment-scope.spec.ts`
- `packages/database/prisma/migrations/<timestamp>_provider_payments_and_reconciliation/migration.sql`
- `docs/architecture/provider-payment-model.md`
- `docs/architecture/payment-attempt-lifecycle.md`

### Files likely to be modified

- `packages/database/prisma/schema.prisma`
- `packages/database/prisma/seed.ts`
- `packages/database/src/index.ts`
- `packages/types/src/index.ts`
- `docs/development/database-migrations.md`

### Required models

- `PaymentProviderConfiguration`
- `PaymentAttempt`
- `PaymentAttemptStatusHistory`
- `ProviderEvent`
- `ReconciliationRun`
- `ReconciliationItem`
- `PaymentException`

### Required states

- `CREATED`
- `PENDING_PROVIDER`
- `PENDING_CUSTOMER`
- `PROCESSING`
- `CONFIRMED`
- `FAILED`
- `CANCELLED`
- `EXPIRED`
- `TIMED_OUT`
- `REQUIRES_REVIEW`

### Validation

```text
pnpm --filter @landaflow/database prisma validate
pnpm --filter @landaflow/database prisma migrate deploy
pnpm --filter @landaflow/database seed
pnpm --filter @landaflow/database test
```

### Completion evidence

- Migrations apply to an empty database.
- Duplicate provider references and event identifiers are rejected.
- Provider payment records cannot reference another organisation's tenant or invoice.
- Replayed events are rejected transactionally.
- Production seed execution remains prohibited.
- Provider credentials are absent from tracked database seed files.

---

## 6. Phase 2: Provider Adapter Framework

### Objective

Create the shared provider contract, adapter registry, normalisation utilities, retry policy, and safe provider-error translation.

### Work

1. Define initiation, status, callback, and health contracts.
2. Add adapter registration and provider selection.
3. Normalise phone numbers, currency, amounts, references, and provider statuses.
4. Add bounded retry with exponential backoff and jitter for safe operations.
5. Prevent automatic retries of ambiguous non-idempotent requests unless the provider contract supports idempotency.
6. Implement timeouts and circuit-breaking controls using free, in-process capabilities.
7. Map provider errors to safe internal error categories.
8. Redact provider credentials and payload fields from logs.

### Files to create

- `apps/api/src/payment-providers/payment-providers.module.ts`
- `apps/api/src/payment-providers/payment-provider.interface.ts`
- `apps/api/src/payment-providers/payment-provider.registry.ts`
- `apps/api/src/payment-providers/payment-provider.types.ts`
- `apps/api/src/payment-providers/provider-error.ts`
- `apps/api/src/payment-providers/provider-retry.service.ts`
- `apps/api/src/payment-providers/phone-number.service.ts`
- `apps/api/src/payment-providers/payment-provider.registry.spec.ts`
- `apps/api/src/payment-providers/provider-retry.service.spec.ts`
- `apps/api/src/payment-providers/phone-number.service.spec.ts`

### Files likely to be modified

- `apps/api/src/app.module.ts`
- `packages/config/src/env.ts`
- `.env.example`
- `apps/api/src/common/interceptors/request-logging.interceptor.ts`
- `turbo.json`

### Validation

- Unsupported providers are rejected safely.
- Ugandan phone numbers normalise consistently to `+256` format.
- Invalid or unsupported numbers are rejected before provider calls.
- Provider timeouts do not generate confirmed payments.
- Safe retries respect configured limits and idempotency rules.
- Provider error details are absent from public responses.
- Secrets and access tokens are absent from logs.

---

## 7. Phase 3: MTN Mobile Money Sandbox Adapter

### Objective

Implement MTN Mobile Money sandbox collection requests, token handling, status verification, callback processing, and health checks through the shared provider contract.

### Work

1. Add MTN sandbox environment validation.
2. Implement access-token acquisition and expiry-aware caching.
3. Implement collection-request initiation.
4. Generate and retain stable provider references.
5. Implement transaction-status queries.
6. Implement callback validation and mapping.
7. Add request timeout, retry, and provider-health handling.
8. Add contract tests using deterministic mocked provider responses.
9. Document sandbox onboarding without committing credentials.

### Files to create

- `apps/api/src/payment-providers/mtn/mtn.module.ts`
- `apps/api/src/payment-providers/mtn/mtn.provider.ts`
- `apps/api/src/payment-providers/mtn/mtn.client.ts`
- `apps/api/src/payment-providers/mtn/mtn.mapper.ts`
- `apps/api/src/payment-providers/mtn/mtn.types.ts`
- `apps/api/src/payment-providers/mtn/mtn.provider.spec.ts`
- `apps/api/src/payment-providers/mtn/mtn.mapper.spec.ts`
- `docs/integrations/mtn-mobile-money-sandbox.md`

### Files likely to be modified

- `packages/config/src/env.ts`
- `.env.example`
- `docs/development/environment-variables.md`

### Required environment variables

- `MTN_MOMO_ENABLED`
- `MTN_MOMO_BASE_URL`
- `MTN_MOMO_SUBSCRIPTION_KEY`
- `MTN_MOMO_API_USER`
- `MTN_MOMO_API_KEY`
- `MTN_MOMO_TARGET_ENVIRONMENT`
- `MTN_MOMO_CALLBACK_URL`

### Validation

- Missing variables stop startup only when the adapter is enabled.
- Token caching respects expiry.
- Collection initiation maps the internal request correctly.
- Provider pending, successful, failed, timeout, and unknown responses map correctly.
- Repeated initiation with one idempotency key does not create duplicate attempts.
- Status verification precedes financial confirmation.
- MTN secrets never appear in logs, fixtures, audit events, or Git history.

---

## 8. Phase 4: Airtel Money Sandbox Adapter

### Objective

Implement Airtel Money sandbox collection requests, authentication, status verification, callback processing, and health checks through the same provider contract.

### Work

1. Add Airtel sandbox environment validation.
2. Implement authentication and expiry-aware token caching.
3. Implement collection-request initiation.
4. Implement provider-reference and transaction-status handling.
5. Validate and map callbacks.
6. Add timeout, retry, and provider-health controls.
7. Add contract tests using deterministic mocked provider responses.
8. Document sandbox onboarding without committing credentials.

### Files to create

- `apps/api/src/payment-providers/airtel/airtel.module.ts`
- `apps/api/src/payment-providers/airtel/airtel.provider.ts`
- `apps/api/src/payment-providers/airtel/airtel.client.ts`
- `apps/api/src/payment-providers/airtel/airtel.mapper.ts`
- `apps/api/src/payment-providers/airtel/airtel.types.ts`
- `apps/api/src/payment-providers/airtel/airtel.provider.spec.ts`
- `apps/api/src/payment-providers/airtel/airtel.mapper.spec.ts`
- `docs/integrations/airtel-money-sandbox.md`

### Files likely to be modified

- `packages/config/src/env.ts`
- `.env.example`
- `docs/development/environment-variables.md`

### Required environment variables

- `AIRTEL_MONEY_ENABLED`
- `AIRTEL_MONEY_BASE_URL`
- `AIRTEL_MONEY_CLIENT_ID`
- `AIRTEL_MONEY_CLIENT_SECRET`
- `AIRTEL_MONEY_COUNTRY`
- `AIRTEL_MONEY_CURRENCY`
- `AIRTEL_MONEY_CALLBACK_URL`

### Validation

- Missing variables stop startup only when Airtel is enabled.
- Token caching respects expiry.
- Internal requests map correctly to Airtel sandbox requests.
- Provider states map to the shared lifecycle consistently.
- Status verification precedes confirmation.
- Retries cannot duplicate payment attempts.
- Airtel credentials remain absent from source, logs, audits, and fixtures.

---

## 9. Phase 5: Payment Orchestration and Secure Callback Processing

### Objective

Coordinate initiation, callback handling, status verification, replay prevention, and exactly-once posting into the Sprint 03 financial services.

### Work

1. Add payment-initiation endpoints.
2. Resolve the organisation, tenant, invoice, amount, currency, and provider before initiation.
3. Persist the payment attempt before calling the provider.
4. Authenticate callbacks using provider-supported controls.
5. Retain a checksum of raw provider events without storing unnecessary sensitive content.
6. Reject duplicate and replayed events.
7. Verify final provider status before confirmation.
8. Invoke the Sprint 03 payment service exactly once.
9. Allocate the payment according to explicit intent or approved allocation policy.
10. Issue the existing immutable receipt.
11. Record status transitions and audit events.
12. Return fast callback acknowledgements without exposing processing details.

### Files to create

- `apps/api/src/payment-orchestration/payment-orchestration.module.ts`
- `apps/api/src/payment-orchestration/payment-orchestration.controller.ts`
- `apps/api/src/payment-orchestration/payment-orchestration.service.ts`
- `apps/api/src/payment-orchestration/callback.controller.ts`
- `apps/api/src/payment-orchestration/callback.service.ts`
- `apps/api/src/payment-orchestration/provider-event.service.ts`
- `apps/api/src/payment-orchestration/dto/initiate-mobile-money.dto.ts`
- `apps/api/src/payment-orchestration/dto/query-payment-status.dto.ts`
- `apps/api/src/payment-orchestration/payment-orchestration.service.spec.ts`
- `apps/api/src/payment-orchestration/callback.service.spec.ts`
- `docs/architecture/payment-orchestration.md`

### Files likely to be modified

- `apps/api/src/app.module.ts`
- `apps/api/src/payments/payments.service.ts`
- `apps/api/src/payments/allocation.service.ts`
- `apps/api/src/audit/audit.types.ts`
- `packages/types/src/authorisation.ts`

### Required permissions

- `payment.initiate`
- `payment.read`
- `payment.exception.read`
- `payment.exception.manage`

### Validation

- Invalid invoices, tenants, currencies, and amounts are rejected before provider calls.
- One idempotency key produces one attempt and one financial posting.
- Duplicate callbacks do not create duplicate payments or receipts.
- Replayed callbacks are rejected and audited.
- Unknown or ambiguous provider states enter review instead of confirmation.
- Callback processing cannot post another organisation's invoice.
- A confirmed provider transaction produces one balanced ledger outcome.
- Failed, cancelled, expired, and timed-out attempts do not affect financial balances.

---

## 10. Phase 6: Reconciliation and Payment Exceptions

### Objective

Reconcile provider transactions against LandaFlow payment attempts and ledger postings, then expose controlled exception-resolution workflows.

### Work

1. Add scheduled and manual reconciliation runs.
2. Query provider transaction status for unresolved attempts.
3. Match provider, internal attempt, payment, invoice, amount, currency, and reference.
4. Detect unmatched provider successes, missing callbacks, duplicate events, amount mismatches, currency mismatches, and conflicting statuses.
5. Create exception records instead of silently correcting financial data.
6. Add operator assignment, notes, resolution reason, and status.
7. Allow approved actions: retry verification, confirm already-posted match, reject invalid event, or initiate controlled compensating workflow.
8. Record every exception action in the audit log.
9. Add reconciliation metrics without exposing credentials.

### Files to create

- `apps/api/src/reconciliation/reconciliation.module.ts`
- `apps/api/src/reconciliation/reconciliation.controller.ts`
- `apps/api/src/reconciliation/reconciliation.service.ts`
- `apps/api/src/reconciliation/reconciliation-runner.service.ts`
- `apps/api/src/reconciliation/exception.service.ts`
- `apps/api/src/reconciliation/dto/run-reconciliation.dto.ts`
- `apps/api/src/reconciliation/dto/list-exceptions.dto.ts`
- `apps/api/src/reconciliation/dto/resolve-exception.dto.ts`
- `apps/api/src/reconciliation/reconciliation.service.spec.ts`
- `apps/api/src/reconciliation/exception.service.spec.ts`
- `docs/architecture/payment-reconciliation.md`

### Files likely to be modified

- `apps/api/src/app.module.ts`
- `packages/config/src/env.ts`
- `.env.example`
- `docs/operations/health-and-logging.md`

### Validation

- Missing callbacks are detected through status queries.
- Duplicate provider successes do not duplicate ledger values.
- Amount and currency mismatches enter review.
- Exceptions cannot be resolved by unauthorised roles.
- Resolution actions are immutable and auditable.
- Reconciliation never edits posted financial records directly.
- Cross-organisation exceptions are inaccessible.
- Provider outages delay reconciliation without corrupting balances.

---

## 11. Phase 7: Mobile Money and Reconciliation Web Experience

### Objective

Deliver responsive, accessible payment initiation, status, reconciliation, and exception-management journeys using live API data.

### Work

1. Add tenant and operator payment-initiation screens.
2. Add provider selection and phone-number validation.
3. Display pending, confirmed, failed, expired, and review states.
4. Add payment-history and receipt navigation.
5. Add reconciliation-run and exception-queue screens.
6. Add permission-aware exception-resolution dialogs.
7. Provide safe retry and refresh actions.
8. Show provider outages without exposing internal details.
9. Preserve mobile, tablet, and desktop usability.
10. Use live foundation data only.

### Files to create

- `apps/web/src/app/(app)/payments/mobile-money/page.tsx`
- `apps/web/src/app/(app)/payments/[paymentAttemptId]/page.tsx`
- `apps/web/src/app/(app)/operations/reconciliation/page.tsx`
- `apps/web/src/app/(app)/operations/payment-exceptions/page.tsx`
- `apps/web/src/features/mobile-money/api.ts`
- `apps/web/src/features/mobile-money/schemas.ts`
- `apps/web/src/features/mobile-money/components/payment-initiation-form.tsx`
- `apps/web/src/features/mobile-money/components/payment-status.tsx`
- `apps/web/src/features/reconciliation/api.ts`
- `apps/web/src/features/reconciliation/components/reconciliation-run-list.tsx`
- `apps/web/src/features/reconciliation/components/payment-exception-list.tsx`
- `apps/web/src/features/reconciliation/components/resolve-exception-dialog.tsx`

### Files likely to be modified

- `apps/web/src/components/app-sidebar.tsx`
- `apps/web/src/app/globals.css`
- `packages/ui/src/index.ts`

### Validation

- Valid Ugandan numbers can initiate sandbox requests.
- Invalid numbers fail before API submission.
- Pending state remains visible during provider processing.
- Successful payment shows the linked receipt only after verified posting.
- Failed attempts never display as paid.
- Operators see exception tools only with required permissions.
- Tenants cannot access organisation reconciliation records.
- Keyboard navigation and visible focus states pass.
- Accessibility checks reveal no critical violations.

---

## 12. Phase 8: Integration, Acceptance and Delivery

### Objective

Prove provider abstraction, callback security, exactly-once posting, reconciliation, exception handling, operational recovery, and review readiness.

### Work

1. Add provider contract and sandbox integration tests.
2. Add signed callback, invalid callback, replay, duplicate, timeout, and ambiguous-status tests.
3. Add browser journeys for initiation, status, receipt, reconciliation, and exception resolution.
4. Validate migrations against an empty database.
5. Verify trial balance after provider-confirmed acceptance scenarios.
6. Verify backup and isolated restoration preserve provider and financial history.
7. Run dependency and secret scanning.
8. Build production containers with providers disabled by default.
9. Publish validation evidence and prepare the Sprint 04 pull request.

### Files to create

- `tests/e2e/mtn-sandbox-payment.spec.ts`
- `tests/e2e/airtel-sandbox-payment.spec.ts`
- `tests/e2e/payment-callback-security.spec.ts`
- `tests/e2e/payment-replay-protection.spec.ts`
- `tests/e2e/payment-reconciliation.spec.ts`
- `tests/e2e/payment-exception-resolution.spec.ts`
- `tests/e2e/provider-outage.spec.ts`
- `docs/validation/sprint-04-acceptance.md`
- `docs/operations/mobile-money-incident-response.md`

### Files likely to be modified

- `.github/workflows/ci.yml`
- `README.md`
- `docs/operations/release-checklist.md`
- `package.json`
- `docker-compose.yml`
- `infrastructure/julyhost/docker-compose.production.yml`
- `infrastructure/julyhost/.env.production.example`

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

1. Empty-database migrations pass.
2. Both provider adapters satisfy the shared contract tests.
3. Callback authentication, duplicate prevention, and replay tests pass.
4. Provider-confirmed payments post exactly once through the Sprint 03 ledger.
5. Trial balance remains equal after all acceptance scenarios.
6. Reconciliation identifies missing, duplicated, mismatched, and ambiguous transactions.
7. Payment-exception permissions and audit tests pass.
8. Provider-outage tests preserve financial integrity.
9. Backup and isolated restoration retain payment attempts, events, reconciliations, exceptions, ledger postings, receipts, and audits.
10. CI quality gates pass on the submitted commit.
11. No provider credential or high-severity defect remains unresolved.
12. Validation evidence matches the commit under review.

---

## 13. Team Work Allocation

### Platform and Infrastructure Team

Owns:

- Provider environment configuration
- Sandbox network and callback infrastructure
- Retry, timeout, and health configuration
- CI sandbox mocks and contract-test infrastructure
- Backup, restoration, and incident documentation
- JulyHost configuration placeholders

### Backend and Data Team

Owns:

- Provider-neutral data model
- Adapter framework
- MTN and Airtel sandbox adapters
- Payment orchestration and callback processing
- Ledger integration
- Reconciliation and exception workflows
- Organisation isolation and audit integration

### Web Experience Team

Owns:

- Payment-initiation and status interfaces
- Mobile-friendly tenant payment journey
- Reconciliation and exception screens
- Permission-aware operational controls
- Responsive and accessible states

### Quality and Security Review

Owns:

- Callback authentication and replay tests
- Idempotency and duplicate-posting tests
- Provider credential and log-redaction review
- Cross-organisation payment isolation
- Trial-balance verification
- Provider-outage and recovery testing
- Release-readiness assessment

Teams may work concurrently only after provider-neutral contracts, payment-attempt states, callback controls, environment-variable names, and ledger entry points are reviewed and merged. Provider SDK and lockfile changes must be coordinated.

---

## 14. Branch and Pull-Request Plan

Recommended branches:

```text
foundation/provider-payment-model
feature/payment-provider-framework
feature/mtn-momo-sandbox
feature/airtel-money-sandbox
feature/payment-orchestration
feature/payment-reconciliation
feature/mobile-money-web
operations/sprint-04-acceptance
```

Every pull request must include:

1. A precise capability-focused title.
2. Scope and affected payment journeys.
3. Technical implementation details.
4. Callback, authentication, replay, and organisation-isolation controls.
5. Database, migration, payment, and ledger impact.
6. Validation commands and complete results.
7. Provider configuration and deployment impact.
8. Risks, outage behaviour, and known limitations.
9. Rollback and compensating-entry considerations.
10. Reviewer focus areas.
11. Screenshots only where they verify interface behaviour.

A pull request must not be merged when required checks fail, callback authenticity is unverified, replay protection is incomplete, duplicate posting is possible, provider status can bypass the ledger, migration effects are unclear, secrets appear in source or logs, required review is missing, or validation evidence does not match the submitted commit.

---

## 15. Sprint Security and Payment Controls

- Providers are disabled unless explicitly configured.
- Credentials exist only in environment or host secret storage.
- Provider access tokens are redacted and never persisted as audit data.
- Callback authentication follows the available provider-specific mechanism.
- Event IDs, references, checksums, timestamps, and nonces prevent replay.
- Provider status is verified before confirmation.
- Exactly-once ledger posting is enforced transactionally.
- Client-side success messages never establish payment truth.
- Amount and currency must match the initiated intent.
- Phone numbers use validated E.164 normalisation.
- Reconciliation never edits posted financial records directly.
- Exceptions require authorised, audited resolution.
- Cross-organisation payment access is denied even with valid identifiers.
- Provider outages preserve invoices, balances, and ledger integrity.
- Sandbox credentials and mock payloads are never represented as production activation.

---

## 16. Definition of Done

Sprint 04 is complete only when:

1. Every phase is implemented and reviewed.
2. Provider and reconciliation migrations apply to an empty database.
3. MTN and Airtel adapters pass the shared contract suite.
4. Initiation, status, callback, replay, duplicate, timeout, and outage tests pass.
5. Provider-confirmed payments enter the Sprint 03 ledger exactly once.
6. Trial balance remains equal across all scenarios.
7. Reconciliation and exception workflows pass.
8. Cross-organisation payment isolation passes.
9. Responsive and accessibility checks pass.
10. Backup and isolated restoration retain provider and financial history.
11. CI quality gates pass on the final commit.
12. No unresolved critical or high-severity defect remains.
13. The branch is pushed and a reviewable pull request exists.
14. Production merchant activation remains explicitly deferred until provider onboarding and JulyHost provisioning are complete.

---

## 17. Sprint 05 Handover

Sprint 05 will consume the verified property, tenancy, billing, payment, receipt, reconciliation, and audit contracts to implement:

- Landlord and property-manager operational dashboards
- Tenant Progressive Web App journeys
- Rent reminders and notification preferences
- Maintenance requests and work tracking
- Reports, exports, and operational summaries
- Internal administration and support tooling
- Production-quality responsive experience across core journeys

Sprint 05 must use live financial and operational data only. It must not calculate balances independently from the Sprint 03 ledger or infer payment success independently from the Sprint 04 provider-confirmed payment records.
