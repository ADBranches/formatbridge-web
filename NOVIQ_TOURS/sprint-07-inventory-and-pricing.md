# Sprint 07: Inventory and Pricing

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Inventory contracts

### Objectives

- Model accommodation units, activities, transport, departures, equipment, capacity and availability.
- Define versioned price and policy rules.

### Files created or modified

- `packages/contracts/src/inventory.ts`
- `packages/contracts/src/availability.ts`
- `packages/contracts/src/pricing.ts`
- `packages/contracts/src/policy.ts`
- `packages/validation/src/inventory.ts`
- `packages/validation/src/pricing.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Supplier inventory workspace

### Objectives

- Build service creation, calendars, capacity controls and temporary closures.
- Support bulk changes with review before application.

### Files created or modified

- `apps/web/src/app/(supplier)/inventory/page.tsx`
- `apps/web/src/app/(supplier)/inventory/new/page.tsx`
- `apps/web/src/features/inventory/inventory-editor.tsx`
- `apps/web/src/features/inventory/availability-calendar.tsx`
- `apps/web/src/features/inventory/capacity-editor.tsx`
- `apps/web/src/features/inventory/bulk-update.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Pricing and policy management

### Objectives

- Implement seasonal rates, occupancy rules, add-ons, taxes, fees and cancellation terms.
- Display the effective price produced by overlapping rules before publication.

### Files created or modified

- `apps/web/src/app/(supplier)/pricing/page.tsx`
- `apps/web/src/features/pricing/rate-plan-editor.tsx`
- `apps/web/src/features/pricing/seasonal-rules.tsx`
- `apps/web/src/features/pricing/add-on-editor.tsx`
- `apps/web/src/features/pricing/cancellation-policy.tsx`
- `apps/web/src/features/pricing/price-preview.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Public availability presentation

### Objectives

- Show accurate dates, remaining capacity, inclusions, exclusions and full price composition.
- Prevent stale inventory from appearing confirmable.

### Files created or modified

- `apps/web/src/features/commerce/availability-picker.tsx`
- `apps/web/src/features/commerce/occupancy-selector.tsx`
- `apps/web/src/features/commerce/price-breakdown.tsx`
- `apps/web/src/features/commerce/policy-summary.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Inventory loop and dependency graph

### Objectives

- Test create-publish-search-reserve-release cycles under concurrent requests.
- Audit service-capacity-rate-policy dependencies for contradictions and orphan rules.

### Files created or modified

- `apps/web/tests/e2e/inventory-management.spec.ts`
- `packages/validation/src/pricing.test.ts`
- `scripts/audit-inventory-graph.ts`
- `docs/verification/sprint-07-report.md`

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
