# Sprint 10: Payments and Financial Controls

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Payment contracts

### Objectives

- Define payment intents, attempts, authorisations, captures, refunds, payouts and reconciliation records.
- Specify provider-neutral webhook and idempotency behaviour.

### Files created or modified

- `packages/contracts/src/payment.ts`
- `packages/contracts/src/refund.ts`
- `packages/contracts/src/payout.ts`
- `packages/contracts/src/reconciliation.ts`
- `packages/validation/src/payment.ts`
- `packages/payments/src/provider.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Traveller payment experience

### Objectives

- Build methods, mobile-money initiation, card handoff, split contributions and payment status.
- Show currency, charges, deadlines and failure recovery clearly.

### Files created or modified

- `apps/web/src/app/(checkout)/payment/page.tsx`
- `apps/web/src/features/payments/payment-methods.tsx`
- `apps/web/src/features/payments/mobile-money-form.tsx`
- `apps/web/src/features/payments/card-payment.tsx`
- `apps/web/src/features/payments/split-payment.tsx`
- `apps/web/src/features/payments/payment-status.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Refunds and traveller finance

### Objectives

- Provide receipts, balances, refund requests and traceable outcomes.
- Prevent ambiguous success states during delayed provider callbacks.

### Files created or modified

- `apps/web/src/app/(account)/payments/page.tsx`
- `apps/web/src/features/payments/receipt.tsx`
- `apps/web/src/features/payments/balance-summary.tsx`
- `apps/web/src/features/refunds/refund-request.tsx`
- `apps/web/src/features/refunds/refund-status.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Payout and reconciliation operations

### Objectives

- Build supplier payout views, administrative exceptions and settlement reconciliation.
- Enforce approval thresholds and separation of duties.

### Files created or modified

- `apps/web/src/app/(supplier)/payouts/page.tsx`
- `apps/web/src/app/(admin)/finance/reconciliation/page.tsx`
- `apps/web/src/app/(admin)/finance/refunds/page.tsx`
- `apps/web/src/features/payouts/payout-statement.tsx`
- `apps/web/src/features/reconciliation/reconciliation-dashboard.tsx`
- `apps/web/src/features/reconciliation/exception-queue.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Financial loop and ledger graph

### Objectives

- Test callbacks, retries, duplicate events, partial refunds, failed payouts and reconciliation closure.
- Verify booking-payment-refund-payout-ledger relationships and immutable references.

### Files created or modified

- `apps/web/tests/e2e/payment.spec.ts`
- `apps/web/tests/e2e/refund.spec.ts`
- `packages/payments/src/provider.test.ts`
- `scripts/audit-financial-graph.ts`
- `docs/verification/sprint-10-report.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Sprint delivery gate

- All five phases are complete and integrated.
- Formatting, linting, type checking, unit tests and end-to-end tests pass.
- Responsive behaviour, accessibility and failure states are reviewed on real viewport sizes.
- The dependency and domain graphs contain no unexplained cycles, orphan nodes or unauthorised edges.
- The sprint report identifies delivered scope, validation evidence, known risks and the next sprint handoff.
