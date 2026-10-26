# Sprint 02: Identity and Traveller Profiles

**Duration:** 2 weeks  
**Product stage:** End-to-end production development  
**Primary implementation language:** TypeScript for web, contracts, tooling and client integration  

## Working method

This sprint uses short, evidence-led development loops: **inspect -> model -> build -> test -> observe -> refine -> integrate**. Graph engineering is applied to dependencies, domain relationships, permissions, events and user journeys. No phase is complete merely because code exists; the affected graph must remain coherent and the vertical workflow must pass.

## Sprint completion rule

The sprint is complete only when every phase objective is implemented, all listed artefacts are present and reviewed, required tests pass, no critical security or accessibility defect remains, and the sprint verification report records the evidence.

## Phase 1: Identity contracts

### Objectives

- Define account, session, traveller and consent contracts shared by the web client and backend.
- Model secure authentication states and policy-aware access.

### Files created or modified

- `packages/contracts/src/identity.ts`
- `packages/contracts/src/traveller.ts`
- `packages/contracts/src/consent.ts`
- `packages/contracts/src/index.ts`
- `packages/validation/src/identity.ts`
- `packages/validation/src/traveller.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 2: Authentication experience

### Objectives

- Build registration, sign-in, recovery, verification and multifactor user journeys.
- Provide accessible validation, safe errors and device-aware session controls.

### Files created or modified

- `apps/web/src/app/(auth)/sign-in/page.tsx`
- `apps/web/src/app/(auth)/register/page.tsx`
- `apps/web/src/app/(auth)/verify/page.tsx`
- `apps/web/src/app/(auth)/mfa/page.tsx`
- `apps/web/src/app/(auth)/recover/page.tsx`
- `apps/web/src/features/auth/auth-form.tsx`
- `apps/web/src/features/auth/session-provider.tsx`
- `apps/web/src/lib/auth.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 3: Traveller profile experience

### Objectives

- Implement personal details, preferences, accessibility needs, emergency contacts and privacy settings.
- Support saved interests and separate travel modes.

### Files created or modified

- `apps/web/src/app/(account)/profile/page.tsx`
- `apps/web/src/app/(account)/preferences/page.tsx`
- `apps/web/src/app/(account)/privacy/page.tsx`
- `apps/web/src/features/profile/profile-form.tsx`
- `apps/web/src/features/profile/preferences-form.tsx`
- `apps/web/src/features/profile/emergency-contacts.tsx`
- `apps/web/src/features/profile/privacy-controls.tsx`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 4: Identity integration

### Objectives

- Connect authenticated requests, route protection and permission-aware rendering.
- Add audit-friendly account actions and consent updates.

### Files created or modified

- `apps/web/src/middleware.ts`
- `apps/web/src/lib/api-client.ts`
- `apps/web/src/lib/session.ts`
- `apps/web/src/hooks/use-current-user.ts`
- `apps/web/src/hooks/use-permissions.ts`
- `packages/contracts/src/audit.ts`

### Phase exit gate

- Intended behaviour is demonstrated through the smallest complete vertical path.
- Targeted tests pass before broader sprint validation begins.
- Dependency, data, permission and event relationships remain valid.
- Failures produce explicit evidence and return the work to the appropriate earlier step in the loop.

## Phase 5: Closed validation loop

### Objectives

- Exercise registration through profile completion as a complete vertical journey.
- Verify the identity-to-profile graph, permission boundaries, failure paths and accessibility.

### Files created or modified

- `apps/web/tests/e2e/authentication.spec.ts`
- `apps/web/tests/e2e/profile.spec.ts`
- `apps/web/src/features/auth/auth-form.test.tsx`
- `apps/web/src/features/profile/profile-form.test.tsx`
- `docs/verification/sprint-02-report.md`

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
