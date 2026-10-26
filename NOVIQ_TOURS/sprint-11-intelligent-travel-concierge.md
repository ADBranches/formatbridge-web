# Sprint 11: Intelligent Travel Concierge

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Concierge contracts and boundaries

### Objectives

- Define conversation, recommendation, evidence, tool request and approval contracts.
- Prevent intelligence services from directly executing financial or destructive actions.

### Files created or modified

- `packages/contracts/src/concierge.ts`
- `packages/contracts/src/ai-tooling.ts`
- `packages/validation/src/concierge.ts`
- `packages/ai-client/src/client.ts`
- `packages/ai-client/src/types.ts`
- `docs/ai/concierge-guardrails.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Conversational interface

### Objectives

- Build a premium assistant integrated into discovery and trip planning without dominating the product.
- Support streaming, interruption, retry and accessible transcripts.

### Files created or modified

- `apps/web/src/app/(account)/concierge/page.tsx`
- `apps/web/src/features/concierge/concierge-panel.tsx`
- `apps/web/src/features/concierge/message-list.tsx`
- `apps/web/src/features/concierge/composer.tsx`
- `apps/web/src/features/concierge/stream-status.tsx`
- `apps/web/src/features/concierge/evidence-panel.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Bookable recommendations

### Objectives

- Transform traveller intent into destination, itinerary and supplier suggestions grounded in current records.
- Require explicit approval before adding or booking recommendations.

### Files created or modified

- `apps/web/src/features/concierge/recommendation-card.tsx`
- `apps/web/src/features/concierge/itinerary-proposal.tsx`
- `apps/web/src/features/concierge/budget-summary.tsx`
- `apps/web/src/features/concierge/approval-step.tsx`
- `apps/web/src/lib/concierge-tools.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Assistance and human handover

### Objectives

- Add packing, document, cultural and budget support.
- Transfer context safely to customer support when automation is unsuitable.

### Files created or modified

- `apps/web/src/features/concierge/packing-list.tsx`
- `apps/web/src/features/concierge/document-checklist.tsx`
- `apps/web/src/features/concierge/cultural-guidance.tsx`
- `apps/web/src/features/concierge/human-handover.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Intelligence loop and knowledge graph

### Objectives

- Evaluate groundedness, recommendation utility, refusal correctness, latency and cost.
- Trace each recommendation through traveller intent, destination evidence, availability and approval.

### Files created or modified

- `apps/web/tests/e2e/concierge.spec.ts`
- `packages/ai-client/src/client.test.ts`
- `scripts/evaluate-concierge.ts`
- `scripts/audit-recommendation-graph.ts`
- `docs/verification/sprint-11-report.md`

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
