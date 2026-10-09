# Noviq Labs Full-Stack Platform

## Development Sprint 10: Commercial and Payment Capabilities

**Sprint position:** Tenth production implementation sprint after the verified Customer Portal and Project Management sprint  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure development and staging environments  
**Architecture:** Modular monolith with provider-neutral payment boundaries and immutable financial records

## Sprint Objective

Implement the complete commercial workflow from approved proposal through invoice, payment, receipt, refund and reconciliation. The sprint will deliver proposal review and acceptance, contract-document access, invoice management, online payments, mobile-money readiness, transaction records, payment notifications, subscription foundations, financial-role separation, duplicate-transaction prevention and reconciliation support. Production hardening and launch remain outside this sprint.

---

## Phase 1: Sprint Entry and Dependency Verification

### Objectives

- Verify that Development Sprint 9 passed every completion-gate requirement.
- Confirm the verified Sprint 9 Git commit, pushed development branch and approved pull-request state.
- Confirm identity, organizations, customer portal, project workspaces, deliverables, documents, audit trails and staging environments remain healthy.
- Inspect the current repository, database schema, authorization policies, notification outbox and worker foundations before modifications.
- Confirm approved payment provider, mobile-money provider, settlement accounts, currencies, tax treatment and finance ownership.
- Confirm proposal, contract, invoice, receipt, refund, reconciliation and retention requirements.
- Create the Development Sprint 10 branch only after all entry checks pass.
- Stop if a financial, legal, provider or security prerequisite remains unresolved.

### Files to create

```text
/docs/evidence/sprint-10-entry-verification.md
/docs/commercial/sprint-10-scope.md
/docs/commercial/provider-readiness-register.md
/docs/commercial/finance-and-legal-prerequisites.md
/docs/delivery/sprint-10-branch-record.md
```

---

## Phase 2: Commercial and Payment Architecture

### Objectives

- Define quotation, proposal, contract, invoice, payment, receipt, reconciliation and subscription boundaries.
- Keep Noviq authoritative for commercial records while payment providers remain authoritative for processing outcomes.
- Define webhook, idempotency, settlement, refund and dispute boundaries.
- Separate customer-facing records from internal financial controls.
- Define financial audit, retention and access requirements.
- Record provider-failure and recovery behavior.

### Files to create

```text
/docs/architecture/commercial-context.md
/docs/architecture/payment-sequence-flows.md
/docs/architecture/commercial-data-boundaries.md
/docs/architecture/adr/0035-use-provider-agnostic-payment-boundary.md
/docs/architecture/adr/0036-use-immutable-financial-ledger-records.md
/docs/architecture/adr/0037-use-idempotent-payment-commands-and-webhooks.md
```

---

## Phase 3: Currency, Money and Tax Foundations

### Objectives

- Implement an immutable money value object using minor units.
- Support approved currencies without floating-point arithmetic.
- Define exchange-rate boundaries without performing unapproved currency conversion.
- Define tax category, tax amount, discount and rounding rules.
- Prevent mixed-currency arithmetic inside one commercial document.
- Test boundary values, zero values and rounding.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Financial/Money.cs
/apps/api/NoviqLabs.Domain/Financial/Currency.cs
/apps/api/NoviqLabs.Domain/Financial/TaxCategory.cs
/apps/api/NoviqLabs.Domain/Financial/TaxAmount.cs
/apps/api/NoviqLabs.Domain/Financial/Discount.cs
/apps/api/NoviqLabs.Domain/Financial/FinancialErrors.cs
/tests/api/NoviqLabs.Api.UnitTests/Financial/MoneyTests.cs
/docs/commercial/money-currency-and-rounding.md
```

---

## Phase 4: Quotation and Proposal Domain Model

### Objectives

- Create quotation, proposal, line item, version, validity and acceptance entities.
- Associate proposals with one organization, lead or project.
- Support draft, review, issued, accepted, declined, expired, withdrawn and superseded states.
- Preserve issued versions and prevent accepted proposals from being overwritten.
- Define customer-visible terms and internal approval metadata separately.
- Record complete proposal lifecycle history.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Commercial/Proposal.cs
/apps/api/NoviqLabs.Domain/Commercial/ProposalVersion.cs
/apps/api/NoviqLabs.Domain/Commercial/ProposalLineItem.cs
/apps/api/NoviqLabs.Domain/Commercial/ProposalStatus.cs
/apps/api/NoviqLabs.Domain/Commercial/ProposalAcceptance.cs
/apps/api/NoviqLabs.Domain/Commercial/ProposalErrors.cs
/docs/commercial/proposal-lifecycle.md
```

---

## Phase 5: Contract Domain Model

### Objectives

- Create contract document, version, party, status and access entities.
- Support draft, issued, awaiting signature, active, completed, terminated and superseded states.
- Preserve immutable issued and executed versions.
- Keep electronic-signature provider references separate from contract content.
- Restrict contract access to authorized organization members and finance or legal roles.
- Record issuance, access, signature and status events.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Contracts/Contract.cs
/apps/api/NoviqLabs.Domain/Contracts/ContractVersion.cs
/apps/api/NoviqLabs.Domain/Contracts/ContractParty.cs
/apps/api/NoviqLabs.Domain/Contracts/ContractStatus.cs
/apps/api/NoviqLabs.Domain/Contracts/SignatureReference.cs
/apps/api/NoviqLabs.Domain/Contracts/ContractErrors.cs
/docs/commercial/contract-lifecycle.md
```

---

## Phase 6: Invoice Domain Model

### Objectives

- Create invoice, invoice line item, tax, due date, status and balance entities.
- Support draft, issued, partially paid, paid, overdue, void and written-off states.
- Associate invoices with one organization and optionally one project or accepted proposal.
- Preserve issued invoice numbers and versions.
- Prevent paid invoices from being edited destructively.
- Record all balance-affecting events.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Billing/Invoice.cs
/apps/api/NoviqLabs.Domain/Billing/InvoiceLineItem.cs
/apps/api/NoviqLabs.Domain/Billing/InvoiceStatus.cs
/apps/api/NoviqLabs.Domain/Billing/InvoiceNumber.cs
/apps/api/NoviqLabs.Domain/Billing/InvoiceBalance.cs
/apps/api/NoviqLabs.Domain/Billing/InvoiceErrors.cs
/docs/commercial/invoice-lifecycle.md
```

---

## Phase 7: Payment and Transaction Domain Model

### Objectives

- Create payment intent, payment attempt, transaction, provider reference and payment status entities.
- Support initiated, pending, succeeded, failed, cancelled, expired, refunded and disputed states.
- Preserve every attempt and provider response reference.
- Keep provider payloads sanitized and separate from normalized transaction records.
- Prevent duplicate successful payment application.
- Record immutable financial events.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Payments/PaymentIntent.cs
/apps/api/NoviqLabs.Domain/Payments/PaymentAttempt.cs
/apps/api/NoviqLabs.Domain/Payments/PaymentTransaction.cs
/apps/api/NoviqLabs.Domain/Payments/PaymentStatus.cs
/apps/api/NoviqLabs.Domain/Payments/PaymentMethodType.cs
/apps/api/NoviqLabs.Domain/Payments/ProviderReference.cs
/apps/api/NoviqLabs.Domain/Payments/PaymentErrors.cs
/docs/payments/payment-lifecycle.md
```

---

## Phase 8: Refund, Receipt and Reconciliation Domain Models

### Objectives

- Create refund, receipt, settlement, reconciliation batch and reconciliation item entities.
- Support full and partial refunds where the provider and policy permit.
- Preserve receipt numbering and issued records.
- Represent matched, unmatched, duplicate and exception reconciliation outcomes.
- Keep settlement data restricted to finance roles.
- Record audit history for every financial adjustment.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Payments/Refund.cs
/apps/api/NoviqLabs.Domain/Payments/RefundStatus.cs
/apps/api/NoviqLabs.Domain/Billing/Receipt.cs
/apps/api/NoviqLabs.Domain/Reconciliation/Settlement.cs
/apps/api/NoviqLabs.Domain/Reconciliation/ReconciliationBatch.cs
/apps/api/NoviqLabs.Domain/Reconciliation/ReconciliationItem.cs
/apps/api/NoviqLabs.Domain/Reconciliation/ReconciliationStatus.cs
/docs/payments/refund-receipt-reconciliation-lifecycle.md
```

---

## Phase 9: Subscription Foundation

### Objectives

- Create subscription, plan reference, billing interval, status and renewal entities.
- Support inactive, trial, active, past due, paused, cancelled and ended states.
- Implement only the foundation required for future recurring services.
- Do not activate public recurring billing until products and provider rules are approved.
- Preserve provider and internal subscription identifiers separately.
- Record lifecycle and authorization events.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Subscriptions/Subscription.cs
/apps/api/NoviqLabs.Domain/Subscriptions/SubscriptionStatus.cs
/apps/api/NoviqLabs.Domain/Subscriptions/BillingInterval.cs
/apps/api/NoviqLabs.Domain/Subscriptions/SubscriptionPlanReference.cs
/apps/api/NoviqLabs.Domain/Subscriptions/SubscriptionErrors.cs
/docs/payments/subscription-foundation.md
```

---

## Phase 10: Persistence and Database Migration

### Objectives

- Map commercial and payment entities to PostgreSQL.
- Use precise minor-unit amounts and approved currency codes.
- Add unique constraints for invoice, receipt, provider and idempotency references.
- Add concurrency controls and financial lifecycle indexes.
- Create the controlled Sprint 10 migration.
- Validate clean-database application, upgrade and rollback boundaries.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ProposalConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ContractConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/InvoiceConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/PaymentTransactionConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/RefundConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ReconciliationConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/SubscriptionConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddCommercialAndPaymentCapabilities.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddCommercialAndPaymentCapabilities.Designer.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/CommercialMigrationTests.cs
/docs/database/commercial-and-payment-schema.md
```

---

## Phase 11: Financial Roles and Authorization

### Objectives

- Define proposal manager, contract manager, billing operator, payment operator, reconciliation operator and finance approver policies.
- Separate invoice issuance, payment operations, refunds and reconciliation duties.
- Require strong authentication for financial administration.
- Prevent customer roles from invoking internal financial actions.
- Require organization authorization for customer-facing records.
- Test deny-by-default and privilege-escalation resistance.

### Files to create

```text
/apps/api/NoviqLabs.Application/Authorization/ProposalManagerRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/BillingOperatorRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/PaymentOperatorRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/ReconciliationOperatorRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/FinanceApproverRequirement.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/FinancialAuthorizationHandlers.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Authorization/FinancialAuthorizationTests.cs
/docs/security/financial-role-separation.md
```

---

## Phase 12: Proposal Creation and Internal Approval

### Objectives

- Implement proposal creation, versioning, review and internal approval.
- Generate totals from validated line items, taxes and discounts.
- Prevent issue before internal approval.
- Require validity dates and approved customer organization.
- Preserve every issued version.
- Audit drafting, approval and issuance.

### Files to create

```text
/apps/api/NoviqLabs.Application/Commercial/CreateProposalCommand.cs
/apps/api/NoviqLabs.Application/Commercial/CreateProposalVersionCommand.cs
/apps/api/NoviqLabs.Application/Commercial/ApproveProposalCommand.cs
/apps/api/NoviqLabs.Application/Commercial/IssueProposalCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Commercial/CreateProposalEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Commercial/IssueProposalEndpoint.cs
/apps/web/src/app/(admin)/admin/proposals/page.tsx
/apps/web/src/features/admin/commercial/ProposalEditor.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Commercial/ProposalManagementTests.cs
/docs/commercial/proposal-management.md
```

---

## Phase 13: Customer Proposal Review and Acceptance

### Objectives

- Present issued proposals to authorized customer reviewers.
- Show scope, pricing, validity and terms clearly.
- Implement accept and decline decisions with idempotency.
- Prevent acceptance after expiry, withdrawal or supersession.
- Capture actor, timestamp, proposal version and decision evidence.
- Notify approved participants after a valid decision.

### Files to create

```text
/apps/api/NoviqLabs.Application/Commercial/AcceptProposalCommand.cs
/apps/api/NoviqLabs.Application/Commercial/DeclineProposalCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Commercial/AcceptProposalEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Commercial/DeclineProposalEndpoint.cs
/apps/web/src/app/(account)/proposals/[proposalId]/page.tsx
/apps/web/src/features/commercial/ProposalReviewPage.tsx
/apps/web/src/features/commercial/ProposalDecisionForm.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Commercial/ProposalAcceptanceTests.cs
/docs/commercial/customer-proposal-review.md
```

---

## Phase 14: Contract Document Access

### Objectives

- Implement secure contract upload, issuance, listing and download.
- Use private storage and short-lived authorized downloads.
- Preserve document integrity and version history.
- Integrate approved signature-provider references without storing provider secrets in records.
- Restrict access to authorized parties and legal or finance roles.
- Audit issuance, access, signature and supersession.

### Files to create

```text
/apps/api/NoviqLabs.Application/Contracts/IssueContractCommand.cs
/apps/api/NoviqLabs.Application/Contracts/GetContractsQuery.cs
/apps/api/NoviqLabs.Application/Contracts/CreateContractDownloadCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Contracts/IssueContractEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Contracts/CreateContractDownloadEndpoint.cs
/apps/web/src/app/(account)/contracts/page.tsx
/apps/web/src/features/commercial/ContractList.tsx
/apps/web/src/features/commercial/ContractDownload.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Contracts/ContractAccessTests.cs
/docs/commercial/contract-document-access.md
```

---

## Phase 15: Invoice Creation and Issuance

### Objectives

- Implement invoice creation from approved proposals, contracts, projects or authorized manual entries.
- Generate immutable invoice numbers through a controlled sequence.
- Calculate totals, taxes, discounts and balance using approved money rules.
- Prevent issue when required billing information is incomplete.
- Queue customer notification after successful issuance.
- Audit creation, approval, issue, void and write-off events.

### Files to create

```text
/apps/api/NoviqLabs.Application/Billing/CreateInvoiceCommand.cs
/apps/api/NoviqLabs.Application/Billing/ApproveInvoiceCommand.cs
/apps/api/NoviqLabs.Application/Billing/IssueInvoiceCommand.cs
/apps/api/NoviqLabs.Application/Billing/InvoiceNumberService.cs
/apps/api/NoviqLabs.Api/Endpoints/Billing/CreateInvoiceEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Billing/IssueInvoiceEndpoint.cs
/apps/web/src/app/(admin)/admin/invoices/page.tsx
/apps/web/src/features/admin/commercial/InvoiceEditor.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Billing/InvoiceIssuanceTests.cs
/docs/commercial/invoice-issuance.md
```

---

## Phase 16: Customer Invoice Experience

### Objectives

- Display authorized organization invoices and balances.
- Show amount, currency, due date, status, line items and payment options.
- Keep internal notes, settlement details and provider internals hidden.
- Provide accessible invoice document download.
- Handle paid, partially paid, overdue, void and unavailable states.
- Support mobile, tablet and desktop layouts.

### Files to create

```text
/apps/web/src/app/(account)/billing/invoices/page.tsx
/apps/web/src/app/(account)/billing/invoices/[invoiceId]/page.tsx
/apps/web/src/features/billing/InvoiceListPage.tsx
/apps/web/src/features/billing/InvoiceDetailPage.tsx
/apps/web/src/features/billing/InvoiceStatusBadge.tsx
/apps/web/src/features/billing/InvoiceBalanceSummary.tsx
/apps/web/src/features/billing/InvoiceDocumentDownload.tsx
/apps/web/src/features/billing/InvoiceDetailPage.test.tsx
/docs/commercial/customer-invoice-experience.md
```

---

## Phase 17: Payment Provider Abstraction

### Objectives

- Create a provider-neutral payment gateway interface.
- Define create, query, cancel, refund and webhook-normalization operations.
- Keep provider-specific payloads inside infrastructure adapters.
- Map provider states into normalized internal states.
- Apply timeouts, retries and circuit-breaking only where safe.
- Prevent automatic retries that could duplicate charges.

### Files to create

```text
/apps/api/NoviqLabs.Application/Payments/IPaymentGateway.cs
/apps/api/NoviqLabs.Application/Payments/PaymentGatewayModels.cs
/apps/api/NoviqLabs.Infrastructure/Payments/PaymentGateway.cs
/apps/api/NoviqLabs.Infrastructure/Payments/PaymentGatewayOptions.cs
/apps/api/NoviqLabs.Infrastructure/Payments/PaymentProviderMapper.cs
/apps/api/NoviqLabs.Infrastructure/Payments/PaymentProviderException.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/PaymentGatewayContractTests.cs
/docs/payments/payment-provider-boundary.md
```

---

## Phase 18: Online Payment Initiation

### Objectives

- Implement payment initiation for authorized payable invoices.
- Calculate the payable amount server-side.
- Create and enforce idempotency keys.
- Prevent payment initiation for paid, void, unauthorized or incompatible invoices.
- Persist the payment intent before calling the provider.
- Return only safe customer-facing provider instructions.

### Files to create

```text
/apps/api/NoviqLabs.Application/Payments/CreatePaymentIntentCommand.cs
/apps/api/NoviqLabs.Application/Payments/CreatePaymentIntentHandler.cs
/apps/api/NoviqLabs.Application/Payments/CreatePaymentIntentValidator.cs
/apps/api/NoviqLabs.Api/Endpoints/Payments/CreatePaymentIntentEndpoint.cs
/apps/api/NoviqLabs.Contracts/Payments/CreatePaymentIntentRequest.cs
/apps/api/NoviqLabs.Contracts/Payments/PaymentIntentResponse.cs
/apps/web/src/features/payments/PaymentMethodSelector.tsx
/apps/web/src/features/payments/PaymentInitiation.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/PaymentInitiationTests.cs
/docs/payments/payment-initiation.md
```

---

## Phase 19: Mobile-Money Payment Readiness

### Objectives

- Implement approved mobile-money initiation and status handling through the provider boundary.
- Validate supported network, telephone and currency combinations.
- Avoid storing mobile-money PINs or provider authentication secrets.
- Present clear customer instructions and pending-state expectations.
- Handle delayed, cancelled, rejected and timed-out requests.
- Keep transactions idempotent across repeated status checks.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Payments/MobileMoney/MobileMoneyGateway.cs
/apps/api/NoviqLabs.Infrastructure/Payments/MobileMoney/MobileMoneyOptions.cs
/apps/api/NoviqLabs.Infrastructure/Payments/MobileMoney/MobileMoneyRequestMapper.cs
/apps/api/NoviqLabs.Infrastructure/Payments/MobileMoney/MobileMoneyStatusMapper.cs
/apps/web/src/features/payments/MobileMoneyPaymentForm.tsx
/apps/web/src/features/payments/MobileMoneyPaymentStatus.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/MobileMoneyPaymentTests.cs
/docs/payments/mobile-money-readiness.md
```

---

## Phase 20: Payment Webhooks

### Objectives

- Implement authenticated payment-provider webhook endpoints.
- Verify signatures, timestamps and provider identity.
- Reject replayed and malformed events.
- Store normalized events before processing.
- Process duplicates idempotently.
- Do not trust browser redirects as payment confirmation.

### Files to create

```text
/apps/api/NoviqLabs.Api/Endpoints/Payments/PaymentWebhookEndpoint.cs
/apps/api/NoviqLabs.Infrastructure/Payments/PaymentWebhookVerifier.cs
/apps/api/NoviqLabs.Infrastructure/Payments/PaymentWebhookNormalizer.cs
/apps/api/NoviqLabs.Domain/Payments/PaymentWebhookEvent.cs
/apps/worker/NoviqLabs.Worker/Jobs/PaymentWebhookProcessingJob.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/PaymentWebhookTests.cs
/tests/worker/NoviqLabs.Worker.UnitTests/PaymentWebhookProcessingJobTests.cs
/docs/security/payment-webhooks.md
```

---

## Phase 21: Payment Status and Invoice Application

### Objectives

- Apply successful transactions to invoice balances exactly once.
- Support partial payments where approved.
- Preserve failed attempt history without reducing invoice balance.
- Handle out-of-order events and delayed provider confirmation.
- Update paid or partially paid states transactionally.
- Generate financial audit events.

### Files to create

```text
/apps/api/NoviqLabs.Application/Payments/ApplyPaymentResultCommand.cs
/apps/api/NoviqLabs.Application/Payments/ApplyPaymentResultHandler.cs
/apps/api/NoviqLabs.Application/Billing/InvoicePaymentApplicationService.cs
/apps/api/NoviqLabs.Infrastructure/Payments/PaymentEventInbox.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/PaymentApplicationTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/OutOfOrderPaymentEventTests.cs
/docs/payments/invoice-payment-application.md
```

---

## Phase 22: Duplicate-Transaction Prevention

### Objectives

- Enforce idempotency across initiation, provider requests, webhooks and invoice application.
- Use unique database constraints as a final protection boundary.
- Reject conflicting reuse of an idempotency key.
- Handle timeout uncertainty without blind charge retries.
- Preserve original response replay for safe duplicate requests.
- Test concurrent and repeated requests.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Payments/IdempotencyRecord.cs
/apps/api/NoviqLabs.Application/Payments/IIdempotencyService.cs
/apps/api/NoviqLabs.Infrastructure/Payments/IdempotencyService.cs
/apps/api/NoviqLabs.Api/Middleware/PaymentIdempotencyMiddleware.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/PaymentIdempotencyTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/ConcurrentPaymentTests.cs
/docs/security/payment-idempotency.md
```

---

## Phase 23: Payment Status Customer Experience

### Objectives

- Display pending, succeeded, failed, cancelled and expired payment outcomes.
- Poll or refresh payment status through an authorized server endpoint.
- Avoid claiming success before provider confirmation is applied.
- Provide safe retry guidance for failed or expired attempts.
- Prevent repeated customer actions while a transaction is uncertain.
- Support accessible live status updates.

### Files to create

```text
/apps/web/src/app/(account)/billing/payments/[paymentId]/page.tsx
/apps/web/src/features/payments/PaymentStatusPage.tsx
/apps/web/src/features/payments/PaymentPendingState.tsx
/apps/web/src/features/payments/PaymentSuccessState.tsx
/apps/web/src/features/payments/PaymentFailureState.tsx
/apps/web/src/lib/payments/payment-status-client.ts
/apps/api/NoviqLabs.Api/Endpoints/Payments/GetPaymentStatusEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/PaymentStatusTests.cs
/docs/payments/customer-payment-status.md
```

---

## Phase 24: Receipt Generation

### Objectives

- Generate receipts only after confirmed payment application.
- Use immutable receipt numbers and financial details.
- Associate every receipt with the underlying transaction and invoice.
- Generate accessible receipt documents.
- Prevent duplicate receipt issue for one applied transaction.
- Record issue and download events.

### Files to create

```text
/apps/api/NoviqLabs.Application/Billing/GenerateReceiptCommand.cs
/apps/api/NoviqLabs.Application/Billing/ReceiptNumberService.cs
/apps/api/NoviqLabs.Api/Endpoints/Billing/GetReceiptEndpoint.cs
/apps/worker/NoviqLabs.Worker/Jobs/ReceiptGenerationJob.cs
/apps/worker/NoviqLabs.Worker/Documents/ReceiptDocumentRenderer.cs
/apps/web/src/features/billing/ReceiptList.tsx
/apps/web/src/features/billing/ReceiptDownload.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Billing/ReceiptGenerationTests.cs
/docs/commercial/receipt-generation.md
```

---

## Phase 25: Refund Workflow

### Objectives

- Implement authorized full and partial refund requests.
- Require finance approval and a reason.
- Prevent refunds above the remaining refundable amount.
- Submit approved refunds idempotently through the provider boundary.
- Update invoice, transaction and receipt context without rewriting history.
- Audit request, approval, provider result and failure.

### Files to create

```text
/apps/api/NoviqLabs.Application/Payments/RequestRefundCommand.cs
/apps/api/NoviqLabs.Application/Payments/ApproveRefundCommand.cs
/apps/api/NoviqLabs.Application/Payments/SubmitRefundCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Payments/RequestRefundEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Payments/ApproveRefundEndpoint.cs
/apps/web/src/features/admin/commercial/RefundManagement.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Payments/RefundTests.cs
/docs/payments/refund-workflow.md
```

---

## Phase 26: Payment Notifications

### Objectives

- Generate operational notifications for invoice issue, payment pending, payment success, payment failure, receipt issue and refund outcomes.
- Do not expose sensitive payment identifiers in insecure channels.
- Use the verified outbox and worker delivery mechanism.
- Keep notification failure separate from payment status.
- Respect optional communication preferences where applicable.
- Record delivery and retry state.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Templates/InvoiceIssuedNotification.cs
/apps/worker/NoviqLabs.Worker/Templates/PaymentPendingNotification.cs
/apps/worker/NoviqLabs.Worker/Templates/PaymentSucceededNotification.cs
/apps/worker/NoviqLabs.Worker/Templates/PaymentFailedNotification.cs
/apps/worker/NoviqLabs.Worker/Templates/ReceiptIssuedNotification.cs
/apps/worker/NoviqLabs.Worker/Templates/RefundNotification.cs
/tests/worker/NoviqLabs.Worker.UnitTests/PaymentNotificationTests.cs
/docs/notifications/payment-notifications.md
```

---

## Phase 27: Reconciliation Import

### Objectives

- Import provider settlement and transaction reports through controlled files or APIs.
- Validate source, period, currency, totals and file integrity.
- Make imports idempotent.
- Preserve raw source references in protected storage.
- Prevent malformed data from partially applying.
- Audit import and rejection outcomes.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reconciliation/ImportSettlementCommand.cs
/apps/api/NoviqLabs.Application/Reconciliation/SettlementImportValidator.cs
/apps/api/NoviqLabs.Infrastructure/Reconciliation/SettlementFileParser.cs
/apps/api/NoviqLabs.Api/Endpoints/Reconciliation/ImportSettlementEndpoint.cs
/apps/worker/NoviqLabs.Worker/Jobs/SettlementImportJob.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Reconciliation/SettlementImportTests.cs
/docs/payments/settlement-import.md
```

---

## Phase 28: Automated Reconciliation

### Objectives

- Match settlements against internal transaction and invoice records.
- Classify exact matches, partial matches, duplicates, missing records and amount discrepancies.
- Never silently resolve financial exceptions.
- Require finance review for unresolved items.
- Prevent the same settlement line from being applied twice.
- Generate reconciliation evidence and audit events.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reconciliation/ReconcileSettlementCommand.cs
/apps/api/NoviqLabs.Application/Reconciliation/ReconciliationEngine.cs
/apps/api/NoviqLabs.Application/Reconciliation/ReconciliationRules.cs
/apps/api/NoviqLabs.Api/Endpoints/Reconciliation/ReconcileSettlementEndpoint.cs
/apps/worker/NoviqLabs.Worker/Jobs/ReconciliationJob.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Reconciliation/ReconciliationTests.cs
/docs/payments/automated-reconciliation.md
```

---

## Phase 29: Reconciliation Administration

### Objectives

- Implement restricted reconciliation batch, exception and resolution views.
- Require finance roles and strong authentication.
- Show settlement totals, matched totals and outstanding differences.
- Require reasons for manual resolution.
- Prevent one user from both creating and approving sensitive manual adjustments where separation is required.
- Audit every resolution.

### Files to create

```text
/apps/web/src/app/(admin)/admin/reconciliation/page.tsx
/apps/web/src/features/admin/commercial/ReconciliationDashboard.tsx
/apps/web/src/features/admin/commercial/ReconciliationBatchDetail.tsx
/apps/web/src/features/admin/commercial/ReconciliationExceptionList.tsx
/apps/web/src/features/admin/commercial/ReconciliationResolutionForm.tsx
/apps/api/NoviqLabs.Application/Reconciliation/ResolveReconciliationExceptionCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Reconciliation/ResolveReconciliationExceptionEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Reconciliation/ReconciliationAdministrationTests.cs
/docs/operations/reconciliation-administration.md
```

---

## Phase 30: Commercial and Financial Audit Trails

### Objectives

- Audit proposal, contract, invoice, payment, refund, receipt and reconciliation actions.
- Record actor, organization, record, financial action, result, timestamp and correlation identifier.
- Exclude full provider secrets and unnecessary card or mobile-money data.
- Make financial audit records immutable and access restricted.
- Support controlled export for authorized review.
- Define retention and legal-hold behavior.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Audit/FinancialAuditEvent.cs
/apps/api/NoviqLabs.Domain/Audit/FinancialAuditAction.cs
/apps/api/NoviqLabs.Application/Audit/IFinancialAuditWriter.cs
/apps/api/NoviqLabs.Infrastructure/Audit/FinancialAuditWriter.cs
/apps/api/NoviqLabs.Api/Endpoints/Administration/GetFinancialAuditEventsEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Audit/FinancialAuditTests.cs
/docs/security/financial-audit-trails.md
```

---

## Phase 31: Financial Retention and Data Minimization

### Objectives

- Define retention for proposals, contracts, invoices, transactions, receipts, refunds, settlements and audit records.
- Minimize provider payload storage.
- Exclude prohibited payment-authentication data.
- Apply controlled archive and deletion jobs only where legally permitted.
- Preserve required tax, contractual and audit records.
- Produce retention and exception evidence.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/FinancialRetentionJob.cs
/apps/worker/NoviqLabs.Worker/Services/FinancialRetentionService.cs
/tests/worker/NoviqLabs.Worker.UnitTests/FinancialRetentionJobTests.cs
/docs/privacy/commercial-data-inventory.md
/docs/privacy/financial-retention.md
/docs/privacy/payment-data-minimization.md
/docs/operations/financial-retention-runbook.md
```

---

## Phase 32: Payment Security Testing

### Objectives

- Test idempotency, replay, forged webhooks, amount tampering and provider-reference manipulation.
- Test unauthorized invoice, payment, refund and reconciliation access.
- Test cross-organization financial data access.
- Test duplicate and concurrent payment initiation.
- Test secret and sensitive-data leakage in logs and client bundles.
- Resolve all critical and high-risk findings.

### Files to create

```text
/apps/web/tests/security/payment-amount-tampering.spec.ts
/apps/web/tests/security/payment-status-access.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Security/PaymentWebhookForgeryTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/PaymentReplayTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/CrossOrganizationFinancialAccessTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/RefundAuthorizationTests.cs
/scripts/security/scan-sprint-10-payments.zsh
/docs/evidence/sprint-10-payment-security-results.md
```

---

## Phase 33: Accessibility and Usability Validation

### Objectives

- Test proposals, contracts, invoices, payment initiation, mobile-money status, receipts and reconciliation interfaces.
- Verify keyboard operation, focus, labels, tables, status updates and error summaries.
- Verify mobile, tablet, desktop and 200 percent zoom behavior.
- Verify money, currency, due-date and payment-status clarity.
- Conduct representative customer and finance-operator tasks.
- Resolve all blocking usability and accessibility defects.

### Files to create

```text
/apps/web/tests/accessibility/proposal-review.spec.ts
/apps/web/tests/accessibility/contracts.spec.ts
/apps/web/tests/accessibility/invoices.spec.ts
/apps/web/tests/accessibility/payment-initiation.spec.ts
/apps/web/tests/accessibility/mobile-money-status.spec.ts
/apps/web/tests/accessibility/receipts.spec.ts
/apps/web/tests/accessibility/reconciliation.spec.ts
/apps/web/tests/usability/sprint-10-customer-tasks.spec.ts
/apps/web/tests/usability/sprint-10-finance-tasks.spec.ts
/docs/evidence/sprint-10-accessibility-and-usability.md
```

---

## Phase 34: Integration, End-to-End and Failure Testing

### Objectives

- Test proposal creation through acceptance.
- Test contract access and invoice issuance.
- Test online and mobile-money payment success, pending, failure, cancellation and timeout.
- Test receipt and refund workflows.
- Test settlement import and reconciliation.
- Test provider, webhook, notification and worker failures.
- Verify audit completeness and recovery.

### Files to create

```text
/apps/web/tests/e2e/proposal-acceptance.spec.ts
/apps/web/tests/e2e/contract-and-invoice.spec.ts
/apps/web/tests/e2e/online-payment.spec.ts
/apps/web/tests/e2e/mobile-money-payment.spec.ts
/apps/web/tests/e2e/payment-failure-recovery.spec.ts
/apps/web/tests/e2e/receipt-and-refund.spec.ts
/apps/web/tests/e2e/reconciliation.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Resilience/PaymentProviderFailureTests.cs
/docs/evidence/sprint-10-end-to-end-results.md
```

---

## Phase 35: Performance and Load Validation

### Objectives

- Measure proposal, invoice, payment initiation, status and reconciliation latency.
- Load test payment initiation with idempotency enabled.
- Test webhook bursts, worker throughput and reconciliation batches.
- Verify bounded queries and financial indexes.
- Verify provider latency does not exhaust application resources.
- Record staging performance evidence.

### Files to create

```text
/tests/load/sprint-10-invoices.js
/tests/load/sprint-10-payment-initiation.js
/tests/load/sprint-10-payment-webhooks.js
/tests/load/sprint-10-reconciliation.js
/scripts/quality/validate-sprint-10-performance.zsh
/docs/evidence/sprint-10-performance-results.md
```

---

## Phase 36: CI/CD Quality-Gate Expansion

### Objectives

- Add commercial migration, financial authorization, payment, webhook, idempotency, reconciliation, accessibility, security and load tests.
- Use provider sandboxes or deterministic test doubles only in trusted workflows.
- Preserve evidence as workflow artifacts.
- Build and publish verified web, API and worker images only after all gates pass.
- Prevent sandbox credentials and financial fixtures from entering production.
- Fail the pipeline when any required underlying command fails.

### Files to create

```text
/.github/workflows/ci-commercial-payments.yml
/.github/workflows/test-financial-authorization.yml
/.github/workflows/test-payment-webhooks.yml
/.github/workflows/test-payment-idempotency.yml
/.github/workflows/test-reconciliation.yml
/.github/workflows/test-payment-accessibility.yml
/.github/workflows/test-payment-security.yml
/.github/workflows/test-payment-load.yml
/.github/workflows/validate-commercial-migration.yml
/scripts/ci/verify-sprint-10-payments.zsh
/scripts/ci/verify-sprint-10-quality-gates.zsh
/docs/delivery/sprint-10-quality-gates.md
```

---

## Phase 37: Azure Infrastructure and Deployment

### Objectives

- Provision payment secrets, webhook configuration, financial storage, queues, alerts and worker scaling.
- Apply the Sprint 10 migration through the controlled migration job.
- Deploy verified web, API and worker images to development and staging.
- Use provider sandbox credentials in non-production environments.
- Verify Key Vault, private storage, callbacks, telemetry and alerts.
- Keep production payment processing disabled until formal production authorization.

### Files to create

```text
/infrastructure/azure/modules/payment-key-vault-secrets.bicep
/infrastructure/azure/modules/payment-webhook-configuration.bicep
/infrastructure/azure/modules/financial-document-storage.bicep
/infrastructure/azure/modules/payment-queues.bicep
/infrastructure/azure/modules/payment-alerts.bicep
/infrastructure/azure/config/payment-alert-thresholds.json
/infrastructure/azure/config/payment-worker-scaling.json
/.github/workflows/deploy-payments-development.yml
/.github/workflows/deploy-payments-staging.yml
/scripts/cloud/deploy-sprint-10-development.zsh
/scripts/cloud/deploy-sprint-10-staging.zsh
/scripts/cloud/smoke-test-sprint-10-payments.zsh
/docs/evidence/sprint-10-development-deployment.md
/docs/evidence/sprint-10-staging-deployment.md
```

---

## Phase 38: Rollback, Recovery and Operational Documentation

### Objectives

- Verify rollback for web, API, worker, migration and payment configuration.
- Ensure rollback never reverses confirmed financial facts.
- Document recovery for uncertain payments, webhook replay, notification failure and reconciliation exceptions.
- Document provider credential compromise and financial incident response.
- Prepare customer, billing, payment and reconciliation operating guides.
- Keep commands Zsh-compatible for Kali Debian.

### Files to create

```text
/.github/workflows/rollback-commercial-release.yml
/scripts/cloud/rollback-sprint-10-commercial.zsh
/scripts/operations/replay-payment-webhooks.zsh
/scripts/operations/reprocess-payment-outbox.zsh
/scripts/operations/retry-reconciliation-batch.zsh
/docs/operations/commercial-rollback-runbook.md
/docs/operations/uncertain-payment-recovery.md
/docs/operations/payment-incident-response.md
/docs/operations/billing-operator-handbook.md
/docs/operations/reconciliation-operator-handbook.md
/docs/commercial/customer-billing-guide.md
/docs/development/sprint-10-kali-debian-zsh.md
/docs/evidence/sprint-10-rollback-verification.md
```

---

## Phase 39: Integrated Validation and Sprint Closure

### Objectives

- Validate the complete commercial and payment implementation from a clean checkout.
- Execute build, migration, unit, integration, end-to-end, accessibility, usability, load, privacy and security tests.
- Verify development and staging deployments, sandbox payments, telemetry, alerts, rollback and recovery.
- Verify no duplicate transaction or unauthorized financial action succeeds.
- Confirm production hardening and launch work has not started.
- Create and push the verified Sprint 10 Git commit.
- Create a pull request only after every required validation passes.
- Stop before Sprint 11.

### Files to create

```text
/scripts/release/sprint-10-final-validation.zsh
/docs/evidence/sprint-10-migration-summary.md
/docs/evidence/sprint-10-proposal-contract-summary.md
/docs/evidence/sprint-10-invoice-summary.md
/docs/evidence/sprint-10-payment-summary.md
/docs/evidence/sprint-10-mobile-money-summary.md
/docs/evidence/sprint-10-refund-receipt-summary.md
/docs/evidence/sprint-10-reconciliation-summary.md
/docs/evidence/sprint-10-accessibility-summary.md
/docs/evidence/sprint-10-performance-summary.md
/docs/evidence/sprint-10-security-and-privacy-summary.md
/docs/evidence/sprint-10-deployment-summary.md
/docs/evidence/sprint-10-completion-record.md
/docs/delivery/sprint-10-pull-request.md
```

---

## Development Sprint 10 Completion Gate

Development Sprint 10 is complete only when every condition below passes:

- Money, currency, tax, discount and rounding rules pass all tests.
- Proposal creation, approval, issue, customer review, acceptance and decline work.
- Accepted and issued proposal versions are immutable.
- Contract documents are private, versioned and available only to authorized parties.
- Invoice creation, approval, issuance and customer viewing work.
- Invoice numbers are unique and issued invoices are not destructively editable.
- Financial duties and permissions are separated.
- Payment initiation calculates the amount server-side.
- Payment-provider operations pass through the provider-neutral boundary.
- Online-payment and mobile-money sandbox flows work.
- Payment webhooks verify signatures and reject replay.
- Browser redirects are not treated as payment confirmation.
- Idempotency prevents duplicate payment creation and application.
- Concurrent and repeated payment requests do not produce duplicate transactions.
- Successful payments update invoice balances exactly once.
- Pending, failed, cancelled, expired and out-of-order events recover predictably.
- Customer payment-status interfaces show confirmed states accurately.
- Receipts are issued only after confirmed payment application.
- Refund requests, approvals and provider submissions work securely.
- Payment notifications are reliable and do not alter financial truth.
- Subscription foundations are implemented without premature public recurring billing.
- Settlement import is validated and idempotent.
- Automated reconciliation identifies matches and exceptions correctly.
- Manual reconciliation resolutions require authorization, reasons and audit records.
- Financial audit trails are complete, immutable and protected.
- Payment-data minimization and retention controls pass.
- Accessibility and usability checks pass.
- Security tests pass with no unresolved critical or high-risk finding.
- Performance and load budgets pass.
- The Sprint 10 migration succeeds in development and staging.
- Development and staging deployment smoke tests pass.
- Azure Key Vault, queues, private storage, telemetry and alerts operate correctly.
- Rollback and uncertain-payment recovery are verified without reversing confirmed financial facts.
- Documentation matches the verified implementation.
- A verified Development Sprint 10 Git commit exists.
- The Development Sprint 10 branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- Production payment processing remains disabled until formal launch authorization.
- No unresolved blocking defect remains.
- The next sprint has not started.

## Development Sprint 10 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_10_COMPLETE
```
