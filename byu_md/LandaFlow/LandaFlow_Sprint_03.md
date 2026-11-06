# LandaFlow Sprint 03

## Billing and Financial Ledger

**Sprint duration:** One week  
**Delivery model:** Parallel team delivery through small, reviewable pull requests  
**Deployment target:** JulyHost-compatible, cloud-neutral Docker deployment  
**Cost constraint:** Free-tier, open-source, or self-hosted services only  
**Prerequisite:** Sprint 02 approved and merged, with verified property, unit, tenant, tenancy, occupancy, document, organisation-isolation, audit, CI, and backup contracts available on the integration branch

---

## 1. Sprint Objective

Deliver the accounting foundation required to generate recurring rent invoices, record contractual charges and adjustments, allocate partial payments, calculate balances and arrears, manage deposits, issue immutable receipts, and produce tenant statements within strict organisation boundaries.

Sprint 03 must introduce a reliable double-entry financial ledger rather than derive balances from mutable invoice totals. Payment-provider integrations, Mobile Money callbacks, automated bank reconciliation, EFRIS fiscal documents, advanced accounting reports, and production payment collection remain outside this sprint.

---

## 2. Sprint Outcomes

At completion:

1. Authorised users can define organisation-scoped billing policies and charge types.
2. Active tenancy agreements can produce idempotent recurring rent invoices.
3. Invoices contain immutable line-item snapshots of the contractual charge basis.
4. Manual charges, credits, waivers, and corrections require explicit audit records.
5. Payments can be recorded manually for MVP operations without pretending to be provider-confirmed transactions.
6. Partial and overpayments are allocated deterministically.
7. Tenant balances and arrears are derived from posted ledger entries.
8. Security deposits remain distinguishable from rent income and tenant credits.
9. Posted financial records cannot be silently edited or deleted.
10. Receipts and tenant statements are reproducible from ledger data.
11. Cross-organisation identifiers cannot expose or alter financial records.
12. Billing and ledger journeys are available through the authenticated workspace.
13. CI, database, browser, audit, backup, and restoration checks pass before review.

---

## 3. Scope Boundaries

### Included

- Billing configuration and charge types
- Recurring rent invoice generation
- Invoice line items and lifecycle management
- Manual payment recording with controlled source labels
- Payment allocation to invoices
- Partial payments, overpayments, and unapplied credit
- Adjustments, credits, waivers, and reversals
- Security-deposit liability tracking
- Double-entry ledger accounts, journals, and entries
- Tenant balances, ageing, arrears, receipts, and statements
- Organisation-scoped API and web journeys
- Audit records and Sprint 03 acceptance evidence

### Excluded

- MTN Mobile Money and Airtel Money production integrations
- Payment webhooks and provider reconciliation
- Bank-feed integrations
- Cash-register or point-of-sale functionality
- EFRIS fiscal invoices and receipts
- General-ledger exports for external accounting suites
- Tax calculation beyond stored invoice metadata
- Automated debt collection
- SMS, email, or WhatsApp reminder delivery
- Multi-currency conversion
- Revenue forecasting or investment analytics

---

## 4. Financial Domain Conventions

### Monetary representation

All monetary values must use integers in the currency's minor unit. Uganda Shillings use whole UGX values. Floating-point numbers are prohibited in database, API, and calculation code.

### Currency

Every financial record must include an ISO 4217 currency code. Sprint 03 supports one currency per organisation ledger. Cross-currency posting is rejected.

### Double-entry accounting

Every posted journal must balance: total debits must equal total credits. Ledger balances must be derived from entries, never directly overwritten.

### Posting and immutability

Draft invoices may be changed before posting. Posted invoices, journals, allocations, receipts, and deposit transactions must not be edited or deleted through ordinary application operations. Corrections require reversing or compensating records.

### Idempotency

Recurring invoice generation and all mutation endpoints that can be retried must use deterministic business keys or supplied idempotency keys. Repeating the same operation must not create duplicate invoices, payments, receipts, or ledger postings.

### Organisation isolation

Every billing, invoice, payment, allocation, receipt, deposit, account, journal, entry, statement, and ageing query must derive or verify `organisationId`. Valid identifiers from another organisation must not bypass access controls.

### Dates and periods

Billing periods and due dates use date-only semantics. Posting timestamps use UTC. Ageing calculations are based on the organisation's configured business date and documented bucket boundaries.

### Auditability

Financial audit events must identify the actor, organisation, action, affected record, before-and-after business state where appropriate, correlation identifier, and reason for controlled adjustments. Credentials and sensitive payment data must never enter audit payloads.

---

## 5. Phase 1: Ledger and Billing Data Foundation

### Objective

Establish the relational billing and double-entry ledger model, constraints, indexes, initial chart of accounts, migrations, seed data, and shared TypeScript contracts.

### Work

1. Add organisation billing-settings and charge-type models.
2. Add ledger-account, journal, and journal-entry models.
3. Define debit and credit conventions.
4. Add invoice, invoice-line, payment, payment-allocation, adjustment, receipt, and deposit models.
5. Define posting statuses and immutable-record conventions.
6. Add composite uniqueness for business and idempotency keys.
7. Index organisation, tenant, agreement, invoice, due-date, status, and posting fields.
8. Seed a minimal non-production chart of accounts.
9. Document ledger invariants and rollback considerations.

### Files to create

- `packages/types/src/billing.ts`
- `packages/types/src/ledger.ts`
- `packages/database/src/financial-scope.ts`
- `packages/database/src/financial-scope.spec.ts`
- `packages/database/prisma/migrations/<timestamp>_billing_and_ledger_foundation/migration.sql`
- `docs/architecture/billing-and-ledger-model.md`
- `docs/architecture/financial-posting-rules.md`

### Files likely to be modified

- `packages/database/prisma/schema.prisma`
- `packages/database/prisma/seed.ts`
- `packages/database/src/index.ts`
- `packages/types/src/index.ts`
- `docs/development/database-migrations.md`

### Required models

- `BillingSettings`
- `ChargeType`
- `LedgerAccount`
- `LedgerJournal`
- `LedgerEntry`
- `Invoice`
- `InvoiceLine`
- `Payment`
- `PaymentAllocation`
- `FinancialAdjustment`
- `Receipt`
- `SecurityDeposit`

### Required constraints

- Unique ledger-account code per organisation
- Unique invoice number per organisation
- Unique receipt number per organisation
- Unique recurring invoice business key per agreement and billing period
- Unique external or manual payment reference where supplied
- Positive line and payment values
- Allocations cannot exceed the available payment amount
- Journal entries must reference accounts from the same organisation
- Financial records must reference tenants, agreements, and units from the same organisation

### Validation

```text
pnpm --filter @landaflow/database prisma validate
pnpm --filter @landaflow/database prisma migrate deploy
pnpm --filter @landaflow/database seed
pnpm --filter @landaflow/database test
```

### Completion evidence

- Migrations apply to an empty PostgreSQL database.
- Seed execution remains prohibited in production.
- Duplicate account codes, invoice numbers, receipt numbers, and recurring business keys are rejected.
- Cross-organisation financial relationships are rejected.
- Financial-scope queries cannot return another organisation's records.
- The seeded journal structure balances correctly.

---

## 6. Phase 2: Ledger Posting Engine

### Objective

Implement a transaction-safe, double-entry posting service that becomes the only supported path for financial balance changes.

### Work

1. Create account lookup and posting services.
2. Validate that every journal balances before insertion.
3. Post journals and entries atomically.
4. Add deterministic idempotency handling.
5. Add reversal journals instead of record mutation.
6. Prevent posting into archived accounts.
7. Expose organisation-scoped journal and account read endpoints.
8. Add correlation identifiers and financial audit events.

### Files to create

- `apps/api/src/ledger/ledger.module.ts`
- `apps/api/src/ledger/ledger.controller.ts`
- `apps/api/src/ledger/ledger.service.ts`
- `apps/api/src/ledger/posting.service.ts`
- `apps/api/src/ledger/posting.types.ts`
- `apps/api/src/ledger/dto/list-ledger-accounts.dto.ts`
- `apps/api/src/ledger/dto/list-journals.dto.ts`
- `apps/api/src/ledger/posting.service.spec.ts`
- `apps/api/src/ledger/ledger.service.spec.ts`

### Files likely to be modified

- `apps/api/src/app.module.ts`
- `apps/api/src/audit/audit.types.ts`
- `packages/types/src/authorisation.ts`
- `docs/security/roles-and-permissions.md`

### Required permissions

- `ledger.read`
- `ledger.post`
- `finance.read`
- `finance.manage`

### Validation

- Unbalanced journals are rejected before database mutation.
- Balanced journals post atomically.
- Duplicate idempotency keys return the original result without reposting.
- Reversal creates equal and opposite entries.
- Archived accounts reject new postings.
- Accountants can post authorised journals.
- Property managers cannot access owner-only ledger administration.
- Tenants cannot access organisation-level ledger records.

---

## 7. Phase 3: Recurring Rent Invoicing

### Objective

Generate accurate, idempotent rent invoices from active tenancy agreements and billing rules.

### Work

1. Configure invoice numbering and due-date rules.
2. Define recurring rent charge schedules.
3. Generate invoices for eligible active agreements.
4. Snapshot agreement, tenant, unit, amount, currency, and billing-period data into invoice lines.
5. Support draft, posted, partially paid, paid, overdue, voided, and reversed states.
6. Prevent duplicate invoices for one agreement and billing period.
7. Post receivable and income journals when invoices are posted.
8. Add controlled void and reversal operations.
9. Record invoice-generation and lifecycle audit events.

### Files to create

- `apps/api/src/billing/billing.module.ts`
- `apps/api/src/billing/billing.controller.ts`
- `apps/api/src/billing/billing.service.ts`
- `apps/api/src/billing/invoice-number.service.ts`
- `apps/api/src/billing/recurring-invoice.service.ts`
- `apps/api/src/billing/dto/update-billing-settings.dto.ts`
- `apps/api/src/billing/dto/create-charge-type.dto.ts`
- `apps/api/src/billing/dto/generate-invoices.dto.ts`
- `apps/api/src/billing/dto/list-invoices.dto.ts`
- `apps/api/src/billing/dto/void-invoice.dto.ts`
- `apps/api/src/billing/recurring-invoice.service.spec.ts`
- `apps/api/src/billing/billing.service.spec.ts`
- `docs/architecture/invoice-lifecycle.md`

### Files likely to be modified

- `apps/api/src/app.module.ts`
- `packages/config/src/env.ts`
- `.env.example`
- `packages/types/src/authorisation.ts`

### Validation

- Only eligible active agreements generate recurring invoices.
- Running generation twice produces no duplicate invoice.
- Invoice line snapshots remain unchanged after tenancy updates.
- Posted invoices create balanced receivable and income entries.
- Invalid dates, currencies, or charge amounts are rejected.
- Voided or reversed invoices preserve history.
- Cross-organisation agreement identifiers are rejected.
- Generation audit events include actor or job identity, organisation, period, and affected invoices.

---

## 8. Phase 4: Payments, Allocations and Receipts

### Objective

Record controlled manual payments, allocate funds deterministically, maintain unapplied credit, and generate immutable receipts.

### Work

1. Add manual payment-recording endpoints for authorised MVP users.
2. Distinguish payment source, method, reference, received date, and recorded actor.
3. Post cash or clearing and tenant-receivable ledger entries.
4. Allocate payments to invoices by explicit instruction or documented oldest-due-first rule.
5. Support partial allocations and unapplied credit.
6. Prevent allocations above payment or invoice balance.
7. Issue immutable receipt numbers after successful posting.
8. Add payment reversal with compensating journals and allocation reversal.
9. Prevent provider-confirmed labels for manually entered payments.

### Files to create

- `apps/api/src/payments/payments.module.ts`
- `apps/api/src/payments/payments.controller.ts`
- `apps/api/src/payments/payments.service.ts`
- `apps/api/src/payments/allocation.service.ts`
- `apps/api/src/payments/receipt.service.ts`
- `apps/api/src/payments/dto/record-payment.dto.ts`
- `apps/api/src/payments/dto/allocate-payment.dto.ts`
- `apps/api/src/payments/dto/reverse-payment.dto.ts`
- `apps/api/src/payments/dto/list-payments.dto.ts`
- `apps/api/src/payments/allocation.service.spec.ts`
- `apps/api/src/payments/payments.service.spec.ts`
- `apps/api/src/payments/receipt.service.spec.ts`
- `docs/architecture/payment-allocation.md`

### Validation

- Partial payment reduces invoice balance correctly.
- Overpayment leaves an explicit unapplied tenant credit.
- Allocation never exceeds payment or invoice availability.
- Duplicate payment references or idempotency keys do not repost funds.
- Receipt numbers are unique and immutable.
- Payment reversal restores balances through compensating records.
- Manually recorded funds remain labelled as manual or offline.
- Cross-organisation invoice or tenant identifiers cannot receive an allocation.

---

## 9. Phase 5: Adjustments, Credits and Security Deposits

### Objective

Provide controlled corrections and deposit tracking without compromising ledger integrity.

### Work

1. Add debit adjustments, credit adjustments, waivers, and write-off requests.
2. Require a reason and authorised actor for every adjustment.
3. Post adjustments through the ledger engine.
4. Track security deposits as liabilities, not rent income.
5. Support deposit receipt, partial application, refund, and retained amount with reasons.
6. Prevent direct balance editing.
7. Add owner-only approval for material write-offs above a configurable threshold.
8. Emit complete audit events.

### Files to create

- `apps/api/src/adjustments/adjustments.module.ts`
- `apps/api/src/adjustments/adjustments.controller.ts`
- `apps/api/src/adjustments/adjustments.service.ts`
- `apps/api/src/adjustments/dto/create-adjustment.dto.ts`
- `apps/api/src/adjustments/dto/reverse-adjustment.dto.ts`
- `apps/api/src/adjustments/adjustments.service.spec.ts`
- `apps/api/src/deposits/deposits.module.ts`
- `apps/api/src/deposits/deposits.controller.ts`
- `apps/api/src/deposits/deposits.service.ts`
- `apps/api/src/deposits/dto/record-deposit.dto.ts`
- `apps/api/src/deposits/dto/apply-deposit.dto.ts`
- `apps/api/src/deposits/dto/refund-deposit.dto.ts`
- `apps/api/src/deposits/deposits.service.spec.ts`
- `docs/architecture/adjustments-and-deposits.md`

### Files likely to be modified

- `packages/config/src/env.ts`
- `.env.example`
- `packages/types/src/authorisation.ts`
- `docs/security/roles-and-permissions.md`

### Validation

- Direct invoice or ledger-balance edits are unavailable.
- Every adjustment requires a reason.
- Adjustments post balanced entries.
- Deposits remain liabilities until applied or refunded.
- Material write-offs require the configured permission.
- Reversals preserve the original record.
- Tenant and organisation isolation remains enforced.

---

## 10. Phase 6: Balances, Arrears and Statements

### Objective

Derive tenant balances, invoice status, ageing, arrears, receipts, and statements from posted ledger and allocation data.

### Work

1. Implement tenant balance queries.
2. Implement invoice balance and payment-status projections.
3. Define ageing buckets: current, 1–30, 31–60, 61–90, and over 90 days.
4. Calculate arrears from due posted invoices less valid allocations and credits.
5. Exclude voided, reversed, and draft records.
6. Generate tenant statements over a requested date range.
7. Generate receipt views from immutable payment data.
8. Add pagination, deterministic ordering, and CSV export for authorised users.
9. Verify all totals against ledger control accounts.

### Files to create

- `apps/api/src/reporting/reporting.module.ts`
- `apps/api/src/reporting/reporting.controller.ts`
- `apps/api/src/reporting/reporting.service.ts`
- `apps/api/src/reporting/ageing.service.ts`
- `apps/api/src/reporting/statement.service.ts`
- `apps/api/src/reporting/dto/tenant-statement.dto.ts`
- `apps/api/src/reporting/dto/ageing-report.dto.ts`
- `apps/api/src/reporting/dto/export-report.dto.ts`
- `apps/api/src/reporting/ageing.service.spec.ts`
- `apps/api/src/reporting/statement.service.spec.ts`
- `docs/architecture/balances-and-ageing.md`

### Validation

- Tenant balances equal ledger-derived balances.
- Invoice status changes correctly after partial and complete allocation.
- Ageing boundaries are tested at 0, 1, 30, 31, 60, 61, 90, and 91 days.
- Reversed and voided records do not inflate arrears.
- Statement opening and closing balances reconcile.
- Reports cannot access another organisation's tenants or invoices.
- Exported totals equal on-screen totals.

---

## 11. Phase 7: Billing and Financial Web Experience

### Objective

Deliver responsive, accessible billing, payment, receipt, statement, and arrears journeys using live financial data only.

### Work

1. Add invoice list, creation, details, and lifecycle screens.
2. Add payment-recording and allocation interfaces.
3. Add adjustment and deposit dialogs.
4. Add tenant balance and statement screens.
5. Add ageing and arrears views.
6. Hide controls when permissions are absent.
7. Provide loading, empty, error, conflict, and unauthorised states.
8. Display clear source labels for manually recorded payments.
9. Avoid hard-coded financial totals or demonstration figures.

### Files to create

- `apps/web/src/app/(app)/billing/page.tsx`
- `apps/web/src/app/(app)/billing/invoices/[invoiceId]/page.tsx`
- `apps/web/src/app/(app)/billing/payments/new/page.tsx`
- `apps/web/src/app/(app)/billing/receipts/[receiptId]/page.tsx`
- `apps/web/src/app/(app)/billing/ageing/page.tsx`
- `apps/web/src/app/(app)/tenants/[tenantId]/statement/page.tsx`
- `apps/web/src/features/billing/api.ts`
- `apps/web/src/features/billing/schemas.ts`
- `apps/web/src/features/billing/components/invoice-list.tsx`
- `apps/web/src/features/billing/components/invoice-details.tsx`
- `apps/web/src/features/payments/api.ts`
- `apps/web/src/features/payments/schemas.ts`
- `apps/web/src/features/payments/components/payment-form.tsx`
- `apps/web/src/features/payments/components/allocation-form.tsx`
- `apps/web/src/features/adjustments/components/adjustment-dialog.tsx`
- `apps/web/src/features/deposits/components/deposit-dialog.tsx`
- `apps/web/src/features/reporting/api.ts`
- `apps/web/src/features/reporting/components/tenant-statement.tsx`
- `apps/web/src/features/reporting/components/ageing-table.tsx`

### Files likely to be modified

- `apps/web/src/components/app-sidebar.tsx`
- `apps/web/src/app/globals.css`
- `packages/ui/src/index.ts`

### Validation

- Accountants can perform permitted billing and payment journeys.
- Read-only roles can view permitted financial records without mutation controls.
- Tenants see only their own statement and receipts where tenant access is enabled.
- Financial values use consistent currency formatting.
- Keyboard navigation and visible focus states work.
- Mobile, tablet, and desktop layouts remain usable.
- Accessibility checks reveal no critical violations.
- API errors do not reveal internal ledger or database details.

---

## 12. Phase 8: Integration, Acceptance and Delivery

### Objective

Prove financial integrity, organisation isolation, user journeys, backup restoration, and pull-request readiness for Sprint 03.

### Work

1. Add financial integration tests.
2. Add Playwright billing and payment journeys.
3. Validate all migrations against an empty database.
4. Verify trial-balance equality after each acceptance scenario.
5. Verify backup and isolated restoration retain financial history.
6. Run dependency and secret review.
7. Build production containers.
8. Publish validation evidence and prepare the Sprint 03 pull request.

### Files to create

- `tests/e2e/recurring-invoicing.spec.ts`
- `tests/e2e/partial-payment.spec.ts`
- `tests/e2e/payment-allocation.spec.ts`
- `tests/e2e/adjustments-and-deposits.spec.ts`
- `tests/e2e/tenant-statement.spec.ts`
- `tests/e2e/financial-isolation.spec.ts`
- `tests/e2e/arrears-ageing.spec.ts`
- `docs/validation/sprint-03-acceptance.md`
- `docs/operations/financial-data-backup.md`

### Files likely to be modified

- `.github/workflows/ci.yml`
- `README.md`
- `docs/operations/release-checklist.md`
- `package.json`

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
2. Every posted test journal balances.
3. Recurring invoice idempotency tests pass.
4. Partial payment, overpayment, allocation, reversal, adjustment, and deposit tests pass.
5. Cross-organisation financial isolation tests pass.
6. Tenant statement and ageing calculations reconcile.
7. Browser journeys pass for authorised roles.
8. Backup and isolated restoration retain invoices, payments, allocations, journals, receipts, deposits, and audit records.
9. CI quality gates pass on the submitted commit.
10. Dependency and secret checks have no unresolved critical or high-severity finding.
11. Validation evidence matches the commit under review.

---

## 13. Team Work Allocation

### Platform and Infrastructure Team

Owns:

- Billing-job execution infrastructure
- Environment and Docker changes
- CI extensions and evidence publication
- Financial backup and restoration validation
- Operational documentation

### Backend and Data Team

Owns:

- Financial database models and migrations
- Ledger posting engine
- Recurring invoicing
- Payments and allocations
- Adjustments and deposits
- Balances, statements, ageing, and arrears
- Organisation isolation and audit integration

### Web Experience Team

Owns:

- Invoice and payment interfaces
- Receipt and statement views
- Adjustment and deposit workflows
- Ageing and arrears screens
- Responsive, accessible financial components

### Quality and Security Review

Owns:

- Double-entry and trial-balance tests
- Idempotency and duplicate-prevention tests
- Cross-organisation financial isolation
- Role and permission verification
- Ledger immutability and reversal review
- PII and credential-redaction review
- Release-readiness assessment

Teams may work concurrently only after the financial schema, account conventions, posting types, invoice lifecycle, and shared API contracts are reviewed and merged. Lockfile and migration changes must be coordinated.

---

## 14. Branch and Pull-Request Plan

Recommended branches:

```text
foundation/billing-ledger-model
feature/ledger-posting-engine
feature/recurring-invoicing
feature/payment-allocation
feature/financial-adjustments-deposits
feature/statements-arrears-reporting
feature/billing-web-experience
operations/sprint-03-acceptance
```

Every pull request must include:

1. A precise capability-focused title.
2. Scope and affected financial journeys.
3. Technical implementation details.
4. Organisation-isolation and permission considerations.
5. Database, migration, and ledger impact.
6. Validation commands and complete results.
7. Deployment and configuration impact.
8. Risks and known limitations.
9. Rollback and compensating-entry considerations.
10. Reviewer focus areas.
11. Screenshots only where they verify interface behaviour.

A pull request must not be merged when required checks fail, journal entries do not balance, migration effects are unclear, organisation isolation is incomplete, posted records can be edited or deleted, duplicate protection is unverified, secrets are exposed, required review is missing, or validation evidence does not match the submitted commit.

---

## 15. Sprint Security and Financial Controls

- Every financial query derives or verifies `organisationId`.
- Monetary values use integer units, never floating point.
- Every posted journal balances.
- Posted financial records are immutable through ordinary endpoints.
- Corrections use reversals or compensating records.
- Idempotency protects recurring generation and retried mutations.
- Payment source labels cannot misrepresent manually entered funds as provider-confirmed.
- Raw Mobile Money credentials or full payment secrets are not stored.
- Tenant financial records are available only to authorised organisation members or the linked tenant.
- Audit events exclude passwords, tokens, and sensitive provider payloads.
- Receipt and invoice numbers are unique and traceable.
- Deposits remain liabilities until valid application or refund.
- Backup and restoration are verified with representative financial records.

---

## 16. Definition of Done

Sprint 03 is complete only when:

1. Every phase is implemented and reviewed.
2. All billing and ledger migrations apply to an empty database.
3. Every posted journal balances.
4. Recurring invoice generation is idempotent.
5. Partial payment, overpayment, allocation, adjustment, reversal, deposit, receipt, statement, and ageing workflows pass.
6. Posted financial history cannot be silently modified or deleted.
7. Cross-organisation financial isolation tests pass.
8. Responsive and accessibility checks pass.
9. Backup and isolated restoration retain financial and audit history.
10. CI quality gates pass on the final commit.
11. No unresolved critical or high-severity defect remains.
12. The branch is pushed and a reviewable pull request exists.
13. JulyHost production placeholders remain explicitly identified until real provisioning occurs.

---

## 17. Sprint 04 Handover

Sprint 04 will consume the verified invoice, payment, allocation, receipt, and ledger contracts to implement:

- MTN Mobile Money sandbox integration
- Airtel Money sandbox integration
- Provider-adapter architecture
- Payment initiation and callback validation
- Webhook authentication and replay protection
- Duplicate-payment prevention
- Provider status verification
- Automated and manual reconciliation
- Payment exceptions and operational queues

Sprint 04 must not bypass the Sprint 03 ledger. Every provider-confirmed payment must enter through the existing idempotent payment-recording and allocation services and produce the same balanced accounting outcome as validated manual payments.
