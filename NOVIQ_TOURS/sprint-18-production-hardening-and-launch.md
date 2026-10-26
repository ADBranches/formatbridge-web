# Sprint 18: Production Hardening and Launch

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: End-to-end regression

### Objectives

- Validate all critical traveller, supplier, administrator and institutional journeys.
- Close cross-module defects with targeted regression coverage.

### Files created or modified

- `apps/web/tests/e2e/full-traveller-journey.spec.ts`
- `apps/web/tests/e2e/full-supplier-journey.spec.ts`
- `apps/web/tests/e2e/full-admin-journey.spec.ts`
- `apps/web/tests/e2e/full-organisation-journey.spec.ts`
- `docs/quality/regression-matrix.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Performance, accessibility and security

### Objectives

- Test realistic load, slow networks, keyboard use, screen readers and common attack paths.
- Resolve critical findings and verify remediations.

### Files created or modified

- `tests/performance/booking-flow.js`
- `tests/performance/search-flow.js`
- `tests/performance/active-trip-flow.js`
- `scripts/run-accessibility-audit.ts`
- `scripts/run-security-baseline.ts`
- `docs/quality/performance-report.md`
- `docs/quality/accessibility-report.md`
- `docs/quality/security-report.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Resilience and recovery

### Objectives

- Exercise dependency outages, retries, backup restoration, reconciliation and graceful degradation.
- Document operational responses and recovery objectives.

### Files created or modified

- `docs/operations/incident-response.md`
- `docs/operations/backup-restore.md`
- `docs/operations/payment-recovery.md`
- `docs/operations/provider-outage.md`
- `docs/operations/disaster-recovery.md`
- `scripts/verify-backup-restore.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Launch operations

### Objectives

- Prepare production configuration, monitoring, release controls, support readiness and supplier launch materials.
- Ensure deployments and rollback are repeatable and observable.

### Files created or modified

- `.github/workflows/release.yml`
- `deploy/production/compose.yaml`
- `deploy/production/.env.example`
- `docs/operations/deployment.md`
- `docs/operations/rollback.md`
- `docs/operations/monitoring.md`
- `docs/support/launch-playbook.md`
- `docs/suppliers/go-live-guide.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Final loop and whole-product graph

### Objectives

- Run the complete inspect-build-test-observe-refine loop until every launch blocker is closed.
- Audit the whole system graph for broken dependencies, unauthorised paths, orphaned records and missing observability.

### Files created or modified

- `scripts/validate-release.ts`
- `scripts/audit-system-graph.ts`
- `docs/verification/sprint-18-report.md`
- `docs/verification/production-readiness.md`
- `CHANGELOG.md`

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
