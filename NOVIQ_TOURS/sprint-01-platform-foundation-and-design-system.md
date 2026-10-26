# Sprint 01: Platform Foundation and Design System

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Repository and architecture baseline

### Objectives

- Establish the TypeScript workspace, development conventions and cloud-neutral deployment baseline.
- Define bounded modules and dependency direction for web, mobile-ready contracts and supporting services.

### Files created or modified

- `package.json`
- `pnpm-workspace.yaml`
- `turbo.json`
- `tsconfig.base.json`
- `.editorconfig`
- `.gitignore`
- `README.md`
- `docs/architecture/system-context.md`
- `docs/architecture/module-boundaries.md`
- `docs/engineering/standards.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Local platform and quality gates

### Objectives

- Provide repeatable local startup for the web application, API dependencies and infrastructure services.
- Enforce formatting, linting, type checking, tests and commit quality before integration.

### Files created or modified

- `compose.yaml`
- `.env.example`
- `apps/web/package.json`
- `apps/web/tsconfig.json`
- `apps/web/next.config.ts`
- `apps/web/src/app/layout.tsx`
- `apps/web/src/app/page.tsx`
- `eslint.config.mjs`
- `prettier.config.mjs`
- `vitest.workspace.ts`
- `.github/workflows/ci.yml`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Original visual system

### Objectives

- Create a distinctive tourism visual language without template-like layouts or decorative AI conventions.
- Define typography, spacing, motion, responsive behaviour and accessible primitives.

### Files created or modified

- `apps/web/src/styles/globals.css`
- `apps/web/src/styles/tokens.css`
- `apps/web/src/components/ui/button.tsx`
- `apps/web/src/components/ui/input.tsx`
- `apps/web/src/components/ui/dialog.tsx`
- `apps/web/src/components/ui/navigation.tsx`
- `apps/web/src/components/ui/index.ts`
- `apps/web/src/app/design-system/page.tsx`
- `docs/design/visual-direction.md`
- `docs/design/component-rules.md`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Application shell

### Objectives

- Deliver responsive public, authenticated and administrative shells.
- Implement navigation, route boundaries, loading states, error handling and metadata conventions.

### Files created or modified

- `apps/web/src/app/(public)/layout.tsx`
- `apps/web/src/app/(account)/layout.tsx`
- `apps/web/src/app/(admin)/layout.tsx`
- `apps/web/src/app/loading.tsx`
- `apps/web/src/app/error.tsx`
- `apps/web/src/app/not-found.tsx`
- `apps/web/src/components/layout/site-header.tsx`
- `apps/web/src/components/layout/site-footer.tsx`
- `apps/web/src/components/layout/account-shell.tsx`
- `apps/web/src/components/layout/admin-shell.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Loop and graph verification

### Objectives

- Run the first inspect-build-test-observe-refine loop across configuration, UI and build outputs.
- Capture the dependency graph and reject circular or unauthorised module coupling.

### Files created or modified

- `scripts/validate-workspace.ts`
- `scripts/check-dependency-graph.ts`
- `docs/engineering/loop-register.md`
- `docs/engineering/dependency-graph.md`
- `docs/verification/sprint-01-report.md`

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
