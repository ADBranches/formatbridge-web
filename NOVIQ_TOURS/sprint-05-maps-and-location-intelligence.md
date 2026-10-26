# Sprint 05: Maps and Location Intelligence

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Location contracts

### Objectives

- Define coordinates, places, service areas, routes, geofences and provider-neutral map responses.
- Separate platform geography from vendor-specific payloads.

### Files created or modified

- `packages/contracts/src/location.ts`
- `packages/contracts/src/route.ts`
- `packages/validation/src/location.ts`
- `packages/maps/src/provider.ts`
- `packages/maps/src/types.ts`
- `packages/maps/src/index.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Interactive map system

### Objectives

- Create reusable map, marker, cluster, popup and layer controls.
- Support keyboard access and a list-view alternative.

### Files created or modified

- `apps/web/src/components/maps/map-canvas.tsx`
- `apps/web/src/components/maps/marker.tsx`
- `apps/web/src/components/maps/cluster-layer.tsx`
- `apps/web/src/components/maps/place-popup.tsx`
- `apps/web/src/components/maps/map-list-toggle.tsx`
- `apps/web/src/components/maps/map-provider.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Destination geography

### Objectives

- Integrate destination maps, nearby discovery, essential services and journey estimates.
- Present pickup locations and meeting points accurately.

### Files created or modified

- `apps/web/src/features/maps/destination-map.tsx`
- `apps/web/src/features/maps/nearby-places.tsx`
- `apps/web/src/features/maps/essential-services.tsx`
- `apps/web/src/features/maps/route-summary.tsx`
- `apps/web/src/features/maps/pickup-point.tsx`
- `apps/web/src/app/(public)/map/page.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Offline and degraded operation

### Objectives

- Cache critical map metadata and route summaries.
- Provide clear behaviour when tiles, routing or location permission is unavailable.

### Files created or modified

- `apps/web/src/lib/offline/maps-cache.ts`
- `apps/web/src/components/maps/map-fallback.tsx`
- `apps/web/src/components/maps/location-permission.tsx`
- `apps/web/src/components/maps/offline-route-card.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Geospatial loop and graph checks

### Objectives

- Test distance, radius, cluster and route behaviour against controlled fixtures.
- Audit geographic relations and reject invalid or impossible coordinates.

### Files created or modified

- `apps/web/tests/e2e/maps.spec.ts`
- `packages/maps/src/provider.test.ts`
- `scripts/validate-location-graph.ts`
- `docs/verification/sprint-05-report.md`

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
