# Sprint 16: Corporate, School and Organised Travel

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Organisation contracts

### Objectives

- Model organisations, departments, travel policies, approvals, guardians and group manifests.
- Define delegated authority and consent boundaries.

### Files created or modified

- `packages/contracts/src/organisation.ts`
- `packages/contracts/src/travel-policy.ts`
- `packages/contracts/src/approval.ts`
- `packages/contracts/src/guardian-consent.ts`
- `packages/validation/src/organisation.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Organisation administration

### Objectives

- Build account structure, members, roles, cost centres and policy configuration.
- Support auditable delegation and revocation.

### Files created or modified

- `apps/web/src/app/(organisation)/settings/page.tsx`
- `apps/web/src/features/organisations/member-management.tsx`
- `apps/web/src/features/organisations/role-management.tsx`
- `apps/web/src/features/organisations/cost-centres.tsx`
- `apps/web/src/features/organisations/policy-editor.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Requests and approvals

### Objectives

- Create travel requests, policy checks, budget review and layered approval.
- Expose reasons for policy exceptions and rejected requests.

### Files created or modified

- `apps/web/src/app/(organisation)/requests/page.tsx`
- `apps/web/src/app/(organisation)/requests/[requestId]/page.tsx`
- `apps/web/src/features/approvals/request-form.tsx`
- `apps/web/src/features/approvals/policy-check.tsx`
- `apps/web/src/features/approvals/approval-panel.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Group and school operations

### Objectives

- Manage manifests, room allocation, transport, guardian consent and duty-of-care status.
- Share sensitive instructions only with authorised service providers.

### Files created or modified

- `apps/web/src/app/(organisation)/groups/[groupId]/page.tsx`
- `apps/web/src/features/groups/manifest.tsx`
- `apps/web/src/features/groups/rooming-list.tsx`
- `apps/web/src/features/groups/transport-allocation.tsx`
- `apps/web/src/features/groups/guardian-consent.tsx`
- `apps/web/src/features/groups/duty-of-care.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Approval loop and organisation graph

### Objectives

- Test request-review-approve-book-travel-reconcile cycles across multiple roles.
- Validate organisation-member-policy-request-booking-traveller-consent relationships.

### Files created or modified

- `apps/web/tests/e2e/organisation-travel.spec.ts`
- `apps/web/tests/e2e/school-trip.spec.ts`
- `scripts/audit-organisation-graph.ts`
- `docs/verification/sprint-16-report.md`

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
