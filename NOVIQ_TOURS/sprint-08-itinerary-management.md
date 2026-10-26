# Sprint 08: Itinerary Management

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Itinerary contracts

### Objectives

- Model trips, days, items, participants, proposals, decisions and schedule conflicts.
- Represent confirmed and unconfirmed items distinctly.

### Files created or modified

- `packages/contracts/src/itinerary.ts`
- `packages/contracts/src/collaboration.ts`
- `packages/validation/src/itinerary.ts`
- `packages/itinerary/src/conflicts.ts`
- `packages/itinerary/src/timing.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Planning workspace

### Objectives

- Build day-by-day planning with timeline and map modes.
- Support insertion, movement, duration changes and unscheduled collections.

### Files created or modified

- `apps/web/src/app/(account)/trips/[tripId]/page.tsx`
- `apps/web/src/features/itinerary/itinerary-builder.tsx`
- `apps/web/src/features/itinerary/day-timeline.tsx`
- `apps/web/src/features/itinerary/itinerary-map.tsx`
- `apps/web/src/features/itinerary/unscheduled-items.tsx`
- `apps/web/src/features/itinerary/item-editor.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Conflict and travel-time handling

### Objectives

- Detect overlaps, closed venues and unrealistic transfers.
- Provide alternatives without silently changing confirmed reservations.

### Files created or modified

- `apps/web/src/features/itinerary/conflict-panel.tsx`
- `apps/web/src/features/itinerary/travel-segment.tsx`
- `apps/web/src/features/itinerary/alternative-suggestions.tsx`
- `apps/web/src/lib/itinerary-conflicts.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Trip collaboration

### Objectives

- Add invitations, permissions, proposals, comments and group voting.
- Maintain an intelligible history of accepted and rejected changes.

### Files created or modified

- `apps/web/src/features/collaboration/invite-travellers.tsx`
- `apps/web/src/features/collaboration/participant-list.tsx`
- `apps/web/src/features/collaboration/proposal-panel.tsx`
- `apps/web/src/features/collaboration/trip-poll.tsx`
- `apps/web/src/features/collaboration/decision-history.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Planning loop and itinerary graph

### Objectives

- Exercise draft-collaborate-resolve-publish-update cycles.
- Validate day-item-participant-booking edges and prohibit destructive edits to confirmed services.

### Files created or modified

- `apps/web/tests/e2e/itinerary-builder.spec.ts`
- `apps/web/tests/e2e/trip-collaboration.spec.ts`
- `packages/itinerary/src/conflicts.test.ts`
- `scripts/audit-itinerary-graph.ts`
- `docs/verification/sprint-08-report.md`

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
