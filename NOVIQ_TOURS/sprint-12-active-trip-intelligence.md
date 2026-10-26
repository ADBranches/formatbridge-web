# Sprint 12: Active-Trip Intelligence

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Active-trip state

### Objectives

- Define live trip status, reminders, disruptions, check-ins and re-planning proposals.
- Distinguish observed events from predictions and recommendations.

### Files created or modified

- `packages/contracts/src/active-trip.ts`
- `packages/contracts/src/disruption.ts`
- `packages/contracts/src/check-in.ts`
- `packages/validation/src/active-trip.ts`
- `packages/trips/src/status.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Journey dashboard

### Objectives

- Build a focused next-action view for travellers already on a trip.
- Provide immediate access to bookings, vouchers, directions and contacts.

### Files created or modified

- `apps/web/src/app/(account)/trips/[tripId]/live/page.tsx`
- `apps/web/src/features/active-trip/journey-dashboard.tsx`
- `apps/web/src/features/active-trip/next-action.tsx`
- `apps/web/src/features/active-trip/live-status.tsx`
- `apps/web/src/features/active-trip/quick-access.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Disruption and re-planning

### Objectives

- Receive delay, weather, closure and supplier events.
- Offer safe alternatives while preserving confirmed services and traveller approval.

### Files created or modified

- `apps/web/src/features/disruptions/disruption-alert.tsx`
- `apps/web/src/features/disruptions/replanning-proposal.tsx`
- `apps/web/src/features/disruptions/impact-summary.tsx`
- `apps/web/src/features/disruptions/approval-actions.tsx`
- `apps/web/src/lib/disruption-rules.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Offline journey essentials

### Objectives

- Cache critical itinerary, contacts, tickets and route summaries.
- Synchronise queued acknowledgements and check-ins safely after reconnection.

### Files created or modified

- `apps/web/src/lib/offline/trip-cache.ts`
- `apps/web/src/lib/offline/sync-queue.ts`
- `apps/web/src/features/offline/offline-status.tsx`
- `apps/web/src/features/offline/sync-conflict.tsx`
- `apps/web/public/sw.js`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Operational loop and event graph

### Objectives

- Test normal travel, missed events, delayed feeds, offline use and recovery.
- Validate event-disruption-proposal-booking-check-in dependencies and temporal order.

### Files created or modified

- `apps/web/tests/e2e/active-trip.spec.ts`
- `apps/web/tests/e2e/offline-trip.spec.ts`
- `scripts/audit-trip-event-graph.ts`
- `docs/verification/sprint-12-report.md`

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
