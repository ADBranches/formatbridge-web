# Sprint 09: Booking Engine

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Booking contracts

### Objectives

- Define quotation, hold, booking, confirmation, amendment, cancellation and fulfilment states.
- Establish idempotency and state-transition rules.

### Files created or modified

- `packages/contracts/src/booking.ts`
- `packages/contracts/src/quotation.ts`
- `packages/validation/src/booking.ts`
- `packages/booking/src/state-machine.ts`
- `packages/booking/src/idempotency.ts`
- `docs/commerce/booking-lifecycle.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Checkout journey

### Objectives

- Build traveller details, service review, policy acceptance and confirmation preparation.
- Support single and packaged service checkout.

### Files created or modified

- `apps/web/src/app/(checkout)/checkout/page.tsx`
- `apps/web/src/features/checkout/checkout-shell.tsx`
- `apps/web/src/features/checkout/traveller-details.tsx`
- `apps/web/src/features/checkout/service-review.tsx`
- `apps/web/src/features/checkout/policy-consent.tsx`
- `apps/web/src/features/checkout/order-summary.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Reservation management

### Objectives

- Provide booking history, details, vouchers, amendments and cancellation requests.
- Present authoritative status and next actions.

### Files created or modified

- `apps/web/src/app/(account)/bookings/page.tsx`
- `apps/web/src/app/(account)/bookings/[bookingId]/page.tsx`
- `apps/web/src/features/bookings/booking-status.tsx`
- `apps/web/src/features/bookings/voucher.tsx`
- `apps/web/src/features/bookings/amendment-form.tsx`
- `apps/web/src/features/bookings/cancellation-form.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Supplier fulfilment

### Objectives

- Deliver reservation queues, acknowledgement, manifests and fulfilment updates.
- Surface approaching deadlines and exceptions.

### Files created or modified

- `apps/web/src/app/(supplier)/reservations/page.tsx`
- `apps/web/src/app/(supplier)/reservations/[bookingId]/page.tsx`
- `apps/web/src/features/reservations/reservation-queue.tsx`
- `apps/web/src/features/reservations/fulfilment-actions.tsx`
- `apps/web/src/features/reservations/guest-manifest.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Transactional loop and booking graph

### Objectives

- Test quotation-hold-confirm-amend-cancel-release workflows, retries and concurrent inventory pressure.
- Validate booking links to traveller, supplier, inventory, policy and itinerary.

### Files created or modified

- `apps/web/tests/e2e/booking.spec.ts`
- `apps/web/tests/e2e/booking-amendment.spec.ts`
- `packages/booking/src/state-machine.test.ts`
- `scripts/audit-booking-graph.ts`
- `docs/verification/sprint-09-report.md`

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
