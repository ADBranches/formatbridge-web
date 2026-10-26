# Sprint 13: Guide, Driver and Transport Operations

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Workforce and transport contracts

### Objectives

- Model professionals, vehicles, credentials, assignments, manifests and expenses.
- Define assignment acceptance and completion states.

### Files created or modified

- `packages/contracts/src/guide.ts`
- `packages/contracts/src/driver.ts`
- `packages/contracts/src/vehicle.ts`
- `packages/contracts/src/assignment.ts`
- `packages/validation/src/assignment.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Guide workspace

### Objectives

- Create profiles, availability, assignments, traveller instructions and completion evidence.
- Support offline access to essential assignment details.

### Files created or modified

- `apps/web/src/app/(guide)/dashboard/page.tsx`
- `apps/web/src/app/(guide)/assignments/[assignmentId]/page.tsx`
- `apps/web/src/features/guides/guide-profile.tsx`
- `apps/web/src/features/guides/assignment-details.tsx`
- `apps/web/src/features/guides/completion-form.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Driver and dispatch workspace

### Objectives

- Implement dispatch queues, pickup verification, status updates, navigation handoff and manifests.
- Limit location sharing to active authorised assignments.

### Files created or modified

- `apps/web/src/app/(driver)/dashboard/page.tsx`
- `apps/web/src/app/(driver)/assignments/[assignmentId]/page.tsx`
- `apps/web/src/app/(supplier)/dispatch/page.tsx`
- `apps/web/src/features/drivers/pickup-verification.tsx`
- `apps/web/src/features/drivers/trip-status.tsx`
- `apps/web/src/features/dispatch/dispatch-board.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Vehicle and expense operations

### Objectives

- Track vehicle credentials, inspections, maintenance dates and assignment expenses.
- Expose earnings and payout links without revealing unrelated financial data.

### Files created or modified

- `apps/web/src/features/vehicles/vehicle-profile.tsx`
- `apps/web/src/features/vehicles/inspection-record.tsx`
- `apps/web/src/features/vehicles/maintenance-alerts.tsx`
- `apps/web/src/features/assignments/expense-form.tsx`
- `apps/web/src/features/assignments/earnings-summary.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Fulfilment loop and assignment graph

### Objectives

- Test dispatch-accept-pickup-deliver-complete and exception paths.
- Validate booking-assignment-professional-vehicle-manifest relationships and credential validity.

### Files created or modified

- `apps/web/tests/e2e/guide-assignment.spec.ts`
- `apps/web/tests/e2e/driver-dispatch.spec.ts`
- `scripts/audit-assignment-graph.ts`
- `docs/verification/sprint-13-report.md`

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
