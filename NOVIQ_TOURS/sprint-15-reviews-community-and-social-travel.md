# Sprint 15: Reviews, Community and Social Travel

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Reputation and community contracts

### Objectives

- Model verified reviews, responses, moderation, journals, collections and creator attribution.
- Define publication and appeal states.

### Files created or modified

- `packages/contracts/src/review.ts`
- `packages/contracts/src/community.ts`
- `packages/contracts/src/creator.ts`
- `packages/validation/src/review.ts`
- `packages/validation/src/community.ts`
- `docs/community/moderation-policy.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Verified reviews

### Objectives

- Build multi-dimensional review submission, evidence, supplier response and traveller reporting.
- Restrict review eligibility to completed bookings.

### Files created or modified

- `apps/web/src/features/reviews/review-form.tsx`
- `apps/web/src/features/reviews/rating-breakdown.tsx`
- `apps/web/src/features/reviews/review-list.tsx`
- `apps/web/src/features/reviews/supplier-response.tsx`
- `apps/web/src/app/(account)/reviews/page.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Travel community

### Objectives

- Create journals, collections, follows, questions and privacy-aware sharing.
- Prevent current precise location from being exposed by default.

### Files created or modified

- `apps/web/src/app/(public)/community/page.tsx`
- `apps/web/src/app/(public)/journals/[journalId]/page.tsx`
- `apps/web/src/features/community/journal-editor.tsx`
- `apps/web/src/features/community/collection-editor.tsx`
- `apps/web/src/features/community/follow-control.tsx`
- `apps/web/src/features/community/question-thread.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Moderation and creator operations

### Objectives

- Provide content queues, reports, appeals, creator disclosure and referral attribution.
- Maintain traceable moderation decisions.

### Files created or modified

- `apps/web/src/app/(admin)/moderation/page.tsx`
- `apps/web/src/features/moderation/moderation-queue.tsx`
- `apps/web/src/features/moderation/decision-panel.tsx`
- `apps/web/src/features/creators/creator-profile.tsx`
- `apps/web/src/features/creators/disclosure-form.tsx`
- `apps/web/src/features/creators/referral-summary.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Trust loop and social graph

### Objectives

- Test publish-review-respond-report-moderate-appeal workflows.
- Audit traveller-content-destination-booking-creator relationships and privacy visibility.

### Files created or modified

- `apps/web/tests/e2e/reviews.spec.ts`
- `apps/web/tests/e2e/community.spec.ts`
- `scripts/audit-community-graph.ts`
- `docs/verification/sprint-15-report.md`

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
