# Sprint 06: Supplier Onboarding and Verification

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Supplier contracts

### Objectives

- Model businesses, representatives, credentials, licences, settlement profiles and approval states.
- Define evidence requirements by supplier category.

### Files created or modified

- `packages/contracts/src/supplier.ts`
- `packages/contracts/src/verification.ts`
- `packages/validation/src/supplier.ts`
- `packages/validation/src/verification.ts`
- `docs/suppliers/verification-policy.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Supplier registration

### Objectives

- Build guided business registration, representative details and service-category selection.
- Save progress and explain outstanding requirements.

### Files created or modified

- `apps/web/src/app/(supplier)/onboarding/page.tsx`
- `apps/web/src/features/suppliers/onboarding-wizard.tsx`
- `apps/web/src/features/suppliers/business-details.tsx`
- `apps/web/src/features/suppliers/service-categories.tsx`
- `apps/web/src/features/suppliers/onboarding-progress.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Evidence and settlement setup

### Objectives

- Support secure document submission, expiry dates and payout-account setup.
- Prevent unreviewed changes to sensitive settlement information.

### Files created or modified

- `apps/web/src/features/suppliers/document-upload.tsx`
- `apps/web/src/features/suppliers/credential-list.tsx`
- `apps/web/src/features/suppliers/settlement-form.tsx`
- `apps/web/src/features/suppliers/representatives.tsx`
- `apps/web/src/lib/uploads.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Administrative verification

### Objectives

- Provide review queues, correction requests, approval, rejection, suspension and renewal.
- Record reasons and complete decision history.

### Files created or modified

- `apps/web/src/app/(admin)/suppliers/page.tsx`
- `apps/web/src/app/(admin)/suppliers/[supplierId]/page.tsx`
- `apps/web/src/features/verification/review-panel.tsx`
- `apps/web/src/features/verification/decision-form.tsx`
- `apps/web/src/features/verification/renewal-queue.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Onboarding loop and trust graph

### Objectives

- Run supplier registration through approval and first authorised staff access.
- Verify business-representative-credential-settlement relationships and privilege boundaries.

### Files created or modified

- `apps/web/tests/e2e/supplier-onboarding.spec.ts`
- `apps/web/tests/e2e/supplier-verification.spec.ts`
- `scripts/audit-supplier-graph.ts`
- `docs/verification/sprint-06-report.md`

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
