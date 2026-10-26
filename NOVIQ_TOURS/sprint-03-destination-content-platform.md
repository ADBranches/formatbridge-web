# Sprint 03: Destination Content Platform

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Destination domain model

### Objectives

- Define destinations, attractions, seasons, practical guidance, accessibility facts and publishing states.
- Establish content ownership and revision rules.

### Files created or modified

- `packages/contracts/src/destination.ts`
- `packages/contracts/src/attraction.ts`
- `packages/contracts/src/media.ts`
- `packages/validation/src/destination.ts`
- `packages/validation/src/attraction.ts`
- `docs/content/destination-schema.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Editorial administration

### Objectives

- Build destination and attraction creation, review, preview, scheduling and publication workflows.
- Support controlled media attachment and content revision.

### Files created or modified

- `apps/web/src/app/(admin)/destinations/page.tsx`
- `apps/web/src/app/(admin)/destinations/new/page.tsx`
- `apps/web/src/app/(admin)/destinations/[destinationId]/page.tsx`
- `apps/web/src/features/destinations/destination-editor.tsx`
- `apps/web/src/features/destinations/attraction-editor.tsx`
- `apps/web/src/features/media/media-library.tsx`
- `apps/web/src/features/publishing/publish-controls.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Public destination experience

### Objectives

- Create bespoke editorial destination and attraction pages with strong hierarchy and responsive media.
- Expose practical, cultural, seasonal, safety and accessibility information.

### Files created or modified

- `apps/web/src/app/(public)/destinations/page.tsx`
- `apps/web/src/app/(public)/destinations/[slug]/page.tsx`
- `apps/web/src/app/(public)/attractions/[slug]/page.tsx`
- `apps/web/src/features/destinations/destination-hero.tsx`
- `apps/web/src/features/destinations/destination-overview.tsx`
- `apps/web/src/features/destinations/practical-information.tsx`
- `apps/web/src/features/destinations/nearby-attractions.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Media and discoverability

### Objectives

- Implement image optimisation, metadata, structured information and share previews.
- Support captions, rights notes and accessible alternatives.

### Files created or modified

- `apps/web/src/components/media/responsive-image.tsx`
- `apps/web/src/components/media/gallery.tsx`
- `apps/web/src/lib/metadata.ts`
- `apps/web/src/lib/structured-data.ts`
- `apps/web/src/app/sitemap.ts`
- `apps/web/src/app/robots.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Content lifecycle loop

### Objectives

- Validate authoring, approval, publication, revision and withdrawal as one operational loop.
- Inspect the destination-content graph for orphaned attractions, invalid media and broken public routes.

### Files created or modified

- `apps/web/tests/e2e/destination-publishing.spec.ts`
- `apps/web/tests/e2e/destination-browsing.spec.ts`
- `apps/web/src/features/destinations/destination-editor.test.tsx`
- `scripts/check-content-graph.ts`
- `docs/verification/sprint-03-report.md`

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
