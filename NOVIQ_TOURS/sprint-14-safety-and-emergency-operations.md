# Sprint 14: Safety and Emergency Operations

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Safety contracts and policy

### Objectives

- Define safety cases, severity, evidence, check-ins, trusted contacts and escalation states.
- Document strict access, retention and notification controls.

### Files created or modified

- `packages/contracts/src/safety.ts`
- `packages/contracts/src/incident.ts`
- `packages/contracts/src/emergency-contact.ts`
- `packages/validation/src/safety.ts`
- `docs/safety/response-policy.md`
- `docs/safety/data-handling.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Traveller safety controls

### Objectives

- Build emergency assistance, safety check-ins and explicit location-sharing controls.
- Show what data is shared, with whom and for how long.

### Files created or modified

- `apps/web/src/features/safety/emergency-action.tsx`
- `apps/web/src/features/safety/safety-check-in.tsx`
- `apps/web/src/features/safety/location-sharing.tsx`
- `apps/web/src/features/safety/trusted-contacts.tsx`
- `apps/web/src/app/(account)/safety/page.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Incident reporting

### Objectives

- Allow structured reporting, evidence submission and status tracking.
- Protect sensitive evidence and remove unnecessary exposure from general support views.

### Files created or modified

- `apps/web/src/app/(account)/incidents/new/page.tsx`
- `apps/web/src/app/(account)/incidents/[caseId]/page.tsx`
- `apps/web/src/features/incidents/incident-form.tsx`
- `apps/web/src/features/incidents/evidence-upload.tsx`
- `apps/web/src/features/incidents/case-status.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Emergency operations console

### Objectives

- Provide severity queues, ownership, escalation, welfare actions and restricted case history.
- Track response targets and unresolved safety checks.

### Files created or modified

- `apps/web/src/app/(admin)/safety/page.tsx`
- `apps/web/src/app/(admin)/safety/[caseId]/page.tsx`
- `apps/web/src/features/safety-ops/severity-queue.tsx`
- `apps/web/src/features/safety-ops/escalation-panel.tsx`
- `apps/web/src/features/safety-ops/welfare-log.tsx`
- `apps/web/src/features/safety-ops/overdue-checkins.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Response loop and safety graph

### Objectives

- Exercise report-triage-contact-escalate-resolve-review workflows with simulated incidents.
- Validate case-traveller-trip-location-contact-evidence relationships and access paths.

### Files created or modified

- `apps/web/tests/e2e/safety-checkin.spec.ts`
- `apps/web/tests/e2e/incident-response.spec.ts`
- `scripts/audit-safety-graph.ts`
- `docs/verification/sprint-14-report.md`

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
