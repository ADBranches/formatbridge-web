# Sprint 17: Administration, Analytics and Destination Intelligence

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Administrative command centre

### Objectives

- Unify operational oversight without bypassing domain permissions.
- Provide actionable queues for accounts, suppliers, bookings, payments, content and support.

### Files created or modified

- `apps/web/src/app/(admin)/dashboard/page.tsx`
- `apps/web/src/features/admin/operations-overview.tsx`
- `apps/web/src/features/admin/priority-queues.tsx`
- `apps/web/src/features/admin/system-status.tsx`
- `apps/web/src/features/admin/audit-search.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Product and commercial analytics

### Objectives

- Implement acquisition, search, booking, cancellation, revenue and retention views.
- Apply privacy thresholds and clear metric definitions.

### Files created or modified

- `packages/contracts/src/analytics.ts`
- `apps/web/src/app/(admin)/analytics/page.tsx`
- `apps/web/src/features/analytics/funnel-view.tsx`
- `apps/web/src/features/analytics/revenue-view.tsx`
- `apps/web/src/features/analytics/retention-view.tsx`
- `docs/analytics/metric-catalogue.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Supplier performance

### Objectives

- Deliver inventory, conversion, fulfilment, cancellation, payout and quality reporting.
- Provide evidence-backed improvement signals rather than unexplained scores.

### Files created or modified

- `apps/web/src/app/(supplier)/analytics/page.tsx`
- `apps/web/src/features/analytics/supplier-performance.tsx`
- `apps/web/src/features/analytics/occupancy-report.tsx`
- `apps/web/src/features/analytics/quality-trends.tsx`
- `apps/web/src/features/analytics/recommendation-explanation.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Destination intelligence

### Objectives

- Provide aggregated demand, origin, seasonality, visitor flow, sentiment and capacity views.
- Prevent exposure of individual traveller movements.

### Files created or modified

- `apps/web/src/app/(authority)/dashboard/page.tsx`
- `apps/web/src/features/destination-intelligence/demand-map.tsx`
- `apps/web/src/features/destination-intelligence/seasonality.tsx`
- `apps/web/src/features/destination-intelligence/capacity-monitor.tsx`
- `apps/web/src/features/destination-intelligence/sentiment-summary.tsx`
- `apps/web/src/features/destination-intelligence/privacy-notice.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Insight loop and analytics graph

### Objectives

- Reconcile dashboards against transaction records and test aggregation thresholds.
- Trace metrics to governed facts, transformations, dimensions and authorised audiences.

### Files created or modified

- `apps/web/tests/e2e/admin-analytics.spec.ts`
- `apps/web/tests/e2e/destination-intelligence.spec.ts`
- `scripts/reconcile-analytics.ts`
- `scripts/audit-metric-graph.ts`
- `docs/verification/sprint-17-report.md`

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
