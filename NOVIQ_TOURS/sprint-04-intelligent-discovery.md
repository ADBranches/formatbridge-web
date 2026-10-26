# Sprint 04: Intelligent Discovery

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Search contracts and indexing

### Objectives

- Define searchable entities, filters, ranking explanations and pagination.
- Prepare ingestion interfaces for text, geography and semantic representations.

### Files created or modified

- `packages/contracts/src/search.ts`
- `packages/contracts/src/recommendation.ts`
- `packages/validation/src/search.ts`
- `packages/search/src/types.ts`
- `packages/search/src/index.ts`
- `docs/search/ranking-policy.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Search experience

### Objectives

- Build natural-language input, structured filters, result views and responsive suggestion behaviour.
- Preserve query state in shareable URLs.

### Files created or modified

- `apps/web/src/app/(public)/search/page.tsx`
- `apps/web/src/features/search/search-bar.tsx`
- `apps/web/src/features/search/filter-panel.tsx`
- `apps/web/src/features/search/result-card.tsx`
- `apps/web/src/features/search/result-grid.tsx`
- `apps/web/src/features/search/active-filters.tsx`
- `apps/web/src/hooks/use-search-params.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Personalised discovery

### Objectives

- Deliver interest-based recommendations, seasonal collections, hidden gems and recently viewed experiences.
- Expose clear recommendation reasons and user controls.

### Files created or modified

- `apps/web/src/app/(public)/discover/page.tsx`
- `apps/web/src/features/discovery/recommendation-rail.tsx`
- `apps/web/src/features/discovery/editorial-collection.tsx`
- `apps/web/src/features/discovery/recommendation-reason.tsx`
- `apps/web/src/features/discovery/preference-controls.tsx`
- `apps/web/src/lib/recommendations.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Saved discovery workflows

### Objectives

- Add saved searches, wish lists and availability notifications.
- Synchronise discovery state across authenticated devices.

### Files created or modified

- `apps/web/src/app/(account)/saved/page.tsx`
- `apps/web/src/features/saved/saved-searches.tsx`
- `apps/web/src/features/saved/wish-list.tsx`
- `apps/web/src/features/saved/alert-settings.tsx`
- `apps/web/src/stores/discovery-store.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Ranking loop and search graph

### Objectives

- Measure relevance, empty-result recovery, latency and recommendation acceptance.
- Validate entity links from queries to destinations, attractions and suppliers.

### Files created or modified

- `apps/web/tests/e2e/search.spec.ts`
- `apps/web/tests/e2e/discovery.spec.ts`
- `packages/search/src/ranking.test.ts`
- `scripts/audit-search-graph.ts`
- `docs/verification/sprint-04-report.md`

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
