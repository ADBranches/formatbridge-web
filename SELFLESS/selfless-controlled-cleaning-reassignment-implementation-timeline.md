# Selfless Controlled Cleaning-Assignment Reassignment Patch

## Implementation Timeline and Development Plan

**Prepared for:** Selfless repository contribution workflow  
**Patch objective:** Allow an authenticated user to change an existing cleaning date or working group up to **three successful times**, subject to registration status, tech-center eligibility, capacity controls, atomic enforcement, and auditability.  
**Project directory:** `/home/trovas/Downloads/projects/byupw/selfless`  
**Planning principle:** No existing file may be altered until its current structure, responsibilities, dependencies, and related call paths have been inspected and documented.

---

## 1. Delivery Rules

The implementation will follow these controls throughout the development cycle:

1. Inspect before editing. Every existing file listed in this plan is a **candidate file** until its contents and dependencies have been reviewed.
2. Do not create a replacement implementation where an existing abstraction can be extended safely.
3. Do not rename, move, delete, or rewrite existing files during inspection.
4. Preserve the current authentication, authorization, tech-center isolation, capacity, and transaction controls unless evidence proves a targeted correction is required.
5. Count only a **successful assignment change** against the limit of three.
6. A failed request, unchanged selection, validation failure, capacity rejection, or unauthorized attempt must not consume the user's allowance.
7. Student cancellation without a replacement assignment is outside the proposed patch and must remain disallowed unless the Integration Owner approves it separately.
8. Administrative corrections must remain separate from the student's three-change allowance unless the Integration Owner directs otherwise.
9. Each implementation phase must end with targeted validation and a verified Git commit before the next implementation phase begins.
10. Work must stop at every phase gate until the outcome has been reviewed and the next phase is explicitly authorized.

---

## 2. Proposed Timeline Summary

The timeline assumes one developer working in a prepared local environment. Actual duration may change after the inspection phase reveals the existing schema, route behavior, testing framework, or migration requirements.

- **Phase 1: Baseline and structural inspection**: 2 to 3 hours
- **Phase 2: Requirement and technical design finalization**: 1 to 2 hours
- **Phase 3: Data-model and migration preparation**: 2 to 4 hours
- **Phase 4: Server-side reassignment enforcement**: 4 to 6 hours
- **Phase 5: Client hook and interface integration**: 3 to 5 hours
- **Phase 6: Automated regression coverage**: 3 to 5 hours
- **Phase 7: Full validation and security review**: 2 to 4 hours
- **Phase 8: Documentation, commit verification, and pull-request preparation**: 1 to 2 hours

**Estimated total:** 18 to 31 hours, subject to inspection findings and Integration Owner decisions.

---

# Phase 1: Baseline and Structural Inspection

## Objective

Establish the exact current implementation of cleaning registration, reassignment, deletion, capacity management, authentication, tenant scoping, database persistence, and interface controls before changing any file.

## Inspection activities

- Confirm the current branch, upstream alignment, worktree status, and latest commit.
- Inspect the Prisma models related to users, tech centers, cleaning days, working groups, registrations, and audit records.
- Inspect every student-facing cleaning route and identify supported HTTP methods.
- Inspect every administrative cleaning route that can assign, move, or remove a student.
- Inspect authentication and authorization helpers used by those routes.
- Inspect cleaning-related hooks, pages, forms, dialogs, and state management.
- Search for all references to cleaning registration, change-day, assignment deletion, capacity counters, and working-group identifiers.
- Determine whether an automated test framework already exists.
- Identify transaction boundaries, uniqueness constraints, and possible count-then-write race conditions.
- Record current request shapes, response shapes, error messages, and status codes.

## Existing directories to inspect

```text
app/api/cleaning/
app/api/admin/cleaning/
app/dashboard/cleaning/
app/dashboard/admin/cleaning/
hooks/
lib/auth/
lib/prisma/
prisma/
```

## Existing candidate files to inspect

```text
prisma/schema.prisma
lib/auth/nextauth.ts
lib/auth/server.ts
lib/auth/types.ts
lib/prisma/client.ts
hooks/useCleaning.ts
hooks/useCleaningStudent.ts
app/dashboard/cleaning/page.tsx
```

The following route files must be located and inspected where present:

```text
app/api/cleaning/register/route.ts
app/api/cleaning/change-day/route.ts
app/api/cleaning/student/route.ts
app/api/admin/cleaning/change/route.ts
app/api/admin/cleaning/manual-assign/route.ts
app/api/admin/cleaning/remove-student/route.ts
app/api/admin/cleaning/remove/[userId]/route.ts
```

Additional files discovered through imports, route references, component composition, or schema relationships must be added to the inspection record before implementation.

## Files to create

```text
docs/cleaning-reassignment-inspection.md
```

Creation of the `docs/` directory is conditional. If the repository already uses another documentation directory or naming convention, the existing convention must be used instead.

## Files to modify

```text
None
```

## Deliverables

- Current workflow map from UI action to database write
- Verified list of affected files
- Existing authorization and tech-center controls
- Existing capacity and transaction behavior
- Confirmed data-model gaps
- Testing and migration strategy recommendation
- Explicit list of files proposed for creation or modification in subsequent phases

## Completion criteria

- Every relevant existing file has been inspected.
- No application file has been modified.
- The worktree remains clean.
- The inspection document records evidence rather than assumptions.
- The implementation file list has been revised to match the actual repository structure.

## Gate

Stop after completing the inspection record. Do not begin design finalization or implementation without explicit authorization.

---

# Phase 2: Requirement and Technical Design Finalization

## Objective

Translate the confirmed business requirement and Phase 1 findings into an implementation design that defines the three-change allowance, API contract, data changes, transaction behavior, auditability, and user experience.

## Rules to formalize

- Maximum of three successful user-initiated changes
- Failed or rejected requests do not increment the counter
- Selecting the current assignment does not increment the counter
- Reassignment is permitted only while the applicable registration window is open
- The replacement day or working group must belong to the user's tech center
- The replacement must have capacity
- A reassignment and counter increment must succeed or fail as one operation
- The response must include the updated assignment and remaining allowance
- Student cancellation without replacement is not included
- Administrative corrections remain independently authorized and audited

## Existing files to inspect again before modification

```text
prisma/schema.prisma
app/api/cleaning/change-day/route.ts
app/api/cleaning/register/route.ts
app/api/cleaning/student/route.ts
hooks/useCleaning.ts
hooks/useCleaningStudent.ts
app/dashboard/cleaning/page.tsx
```

## Files to create

```text
docs/cleaning-reassignment-design.md
```

The exact location and name remain conditional on the documentation convention confirmed during Phase 1.

## Files to modify

```text
None
```

## Deliverables

- Approved state-transition rules
- Proposed request and response contract
- Proposed error codes and user-facing messages
- Proposed database fields or audit model
- Transaction and concurrency strategy
- Final implementation file map
- Test matrix covering success and denied paths

## Completion criteria

- The Integration Owner has confirmed ambiguous business rules.
- The design specifies how the limit is persisted and enforced.
- Administrative and student-initiated changes are clearly separated.
- No source file has been modified.

## Gate

Stop after design approval. Do not create a migration or edit the schema before explicit authorization.

---

# Phase 3: Data Model and Migration Preparation

## Objective

Introduce the minimum persistent data needed to enforce the three-change allowance and preserve reassignment history, based only on the approved design and inspected schema.

## Candidate data-model approach

The exact approach must be decided from the existing schema. A likely design may require:

- A successful-change counter associated with the student's cleaning registration
- A reassignment-history model or existing audit-log integration
- Previous and replacement cleaning-day or working-group references
- Initiating user reference
- Change source, such as student or administrator
- Timestamp and optional administrative reason
- Appropriate indexes and uniqueness constraints

The counter must not be implemented as an unverified field addition if an existing history or audit model can calculate or enforce the allowance safely.

## Existing files to inspect immediately before modification

```text
prisma/schema.prisma
package.json
```

Any existing migration directory must also be inspected before a migration is generated.

## Candidate files to modify

```text
prisma/schema.prisma
```

## Candidate files to create

```text
prisma/migrations/<generated_timestamp>_add_cleaning_reassignment_controls/migration.sql
```

The migration directory name must be generated by the project's established Prisma workflow. It must not be invented manually before the current migration structure is inspected.

Possible test-support files may be created only if Phase 1 confirms the relevant convention:

```text
prisma/seed-cleaning-reassignment-test-data.ts
```

A seed file must not be introduced if the repository uses fixtures or another test-data mechanism.

## Validation

- Prisma format check
- Prisma schema validation
- Migration SQL inspection
- Migration status review against a safe local or designated development database
- Verification that existing records receive safe default behavior
- Verification that no production migration is applied from the local inspection workflow

## Completion criteria

- The schema reflects only the approved minimum changes.
- The migration is reversible or has a documented rollback approach.
- Existing records behave consistently.
- No unauthorized database environment is modified.
- All required validation succeeds.
- A verified Git commit records the completed data-model work.

## Gate

Stop after the verified commit. Do not implement API behavior until explicitly authorized.

---

# Phase 4: Server-Side Reassignment Enforcement

## Objective

Implement secure, atomic, and tenant-scoped reassignment behavior that permits no more than three successful user-initiated changes.

## Existing files to inspect immediately before modification

```text
app/api/cleaning/change-day/route.ts
app/api/cleaning/register/route.ts
app/api/cleaning/student/route.ts
lib/auth/server.ts
lib/prisma/client.ts
```

All direct imports and shared utilities discovered in these files must also be inspected before editing.

## Candidate files to modify

```text
app/api/cleaning/change-day/route.ts
app/api/cleaning/student/route.ts
```

Modification of `app/api/cleaning/register/route.ts` is conditional. It should be changed only if initial assignment creation must initialize reassignment state explicitly and the database default is insufficient.

## Candidate files to create

The following are conditional and must align with the actual project conventions:

```text
lib/cleaning/reassignment-policy.ts
lib/cleaning/reassignment-service.ts
lib/validation/cleaning-reassignment.ts
```

Possible directory creation:

```text
lib/cleaning/
lib/validation/
```

Do not create these directories or files if equivalent policy, service, or validation abstractions already exist.

## Required implementation behavior

- Obtain the user identity from the authenticated server session.
- Ignore or reject caller-supplied ownership identifiers.
- Load the current assignment and verify ownership.
- Verify that the replacement differs from the current assignment.
- Verify matching tech-center scope.
- Verify registration-window status.
- Verify replacement capacity.
- Reject a fourth successful change.
- Update the assignment, increment the counter, update capacity state, and create history atomically.
- Return the number of changes used and remaining.
- Use stable status codes and non-sensitive errors.
- Ensure repeated or concurrent requests cannot exceed the allowance or capacity.

## Validation

- Targeted route tests
- Unauthorized request test
- Cross-user request test
- Cross-tech-center request test
- Closed-registration test
- Full-capacity test
- Unchanged-selection test
- First, second, and third successful reassignment tests
- Fourth reassignment rejection test
- Concurrent request test
- Transaction rollback test
- Targeted lint and TypeScript validation

## Completion criteria

- The server is the authoritative enforcement layer.
- Exactly three successful changes are possible.
- Rejected attempts do not consume allowance.
- Tenant and capacity controls are preserved.
- History is recorded for successful changes.
- All required validation succeeds.
- A verified Git commit records the server-side implementation.

## Gate

Stop after the verified commit. Do not begin user-interface changes without explicit authorization.

---

# Phase 5: Client Hook and Interface Integration

## Objective

Expose the controlled reassignment capability clearly and professionally while ensuring the interface reflects, but does not replace, server-side enforcement.

## Existing files to inspect immediately before modification

```text
hooks/useCleaning.ts
hooks/useCleaningStudent.ts
app/dashboard/cleaning/page.tsx
```

Any imported cleaning components, dialogs, shared buttons, notification utilities, or type definitions must be inspected before editing.

## Candidate files to modify

```text
hooks/useCleaning.ts
hooks/useCleaningStudent.ts
app/dashboard/cleaning/page.tsx
```

## Candidate files to create

Only if the current page structure supports component extraction:

```text
app/dashboard/cleaning/components/CleaningReassignmentForm.tsx
app/dashboard/cleaning/components/ReassignmentAllowance.tsx
```

Possible directory creation:

```text
app/dashboard/cleaning/components/
```

Do not create these files if the existing interface uses another component directory or if extraction would add unnecessary complexity.

## Required user experience

- Display the current cleaning date and working group.
- Display how many successful changes have been used and remain.
- Explain that no more than three successful changes are permitted.
- Allow only eligible options returned or accepted by the server.
- Require an explicit user confirmation before submitting a change.
- Confirm success and display the remaining allowance.
- Present clear messages for full capacity, closed registration, tenant mismatch, unchanged selection, and exhausted allowance.
- Disable or hide the action when the allowance is exhausted, while retaining server enforcement.
- Preserve accessibility, keyboard operation, loading states, and mobile responsiveness.

## Validation

- Hook request and response handling
- Loading, success, and error states
- First, second, and third change displays
- Exhausted-limit display
- Direct API rejection remains effective when the client control is bypassed
- Keyboard and screen-reader labels
- Responsive layout checks
- Targeted lint, TypeScript, and production build

## Completion criteria

- The user can complete an eligible reassignment successfully.
- Remaining allowance is accurate after every successful change.
- Failed requests do not alter displayed allowance after refreshed server state.
- Accessibility and responsive behavior are preserved.
- All required validation succeeds.
- A verified Git commit records the client integration.

## Gate

Stop after the verified commit. Do not proceed to broader remediation or unrelated UI changes without explicit authorization.

---

# Phase 6: Automated Regression Coverage

## Objective

Create durable tests proving the permitted and denied reassignment behaviors and preventing future regression.

## Existing directories and files to inspect

```text
package.json
eslint.config.mjs
tsconfig.json
app/api/cleaning/
hooks/
```

Any existing test configuration, fixtures, mocks, or test directories discovered during Phase 1 must be used rather than replaced.

## Candidate files to modify

```text
package.json
```

Modification is conditional on the absence of suitable test scripts or dependencies.

## Candidate files to create

The exact paths depend on the test framework confirmed during inspection. Possible locations include:

```text
tests/cleaning/reassignment-policy.test.ts
tests/cleaning/change-day-route.test.ts
tests/cleaning/reassignment-concurrency.test.ts
```

Possible supporting files:

```text
tests/fixtures/cleaning.ts
tests/helpers/auth-session.ts
tests/helpers/database.ts
```

Do not create the `tests/` hierarchy if the repository uses colocated tests, `__tests__/`, or another established convention.

## Required test coverage

- Initial assignment does not consume a change
- First successful change
- Second successful change
- Third successful change
- Fourth request rejected
- Failed validation does not consume allowance
- Unchanged selection does not consume allowance
- Unauthorized request rejected
- Cross-user request rejected
- Cross-tech-center request rejected
- Closed registration rejected
- Full replacement group rejected
- Concurrent request limit enforcement
- History record creation
- Administrative correction behavior, if approved

## Completion criteria

- All required success and denied paths are automated.
- Tests are deterministic and isolated.
- No test depends on production credentials or production data.
- All required validation succeeds.
- A verified Git commit records the regression suite.

## Gate

Stop after the verified commit. Do not begin broad lint cleanup or unrelated vulnerability remediation without explicit authorization.

---

# Phase 7: Full Validation and Security Review

## Objective

Confirm that the complete patch works correctly, introduces no unintended repository changes, and preserves security, tenant, capacity, and application-build behavior.

## Files to modify

```text
None, unless validation identifies a verified defect in the patch
```

Any correction required during this phase must begin with inspection of the affected file and must remain within the approved patch scope.

## Validation sequence

1. Verify branch and worktree state.
2. Install dependencies from the lockfile where necessary.
3. Validate the Prisma schema.
4. Review migration status and generated client state.
5. Run the new targeted tests.
6. Run the full available test suite.
7. Run targeted ESLint checks for changed files.
8. Run the repository lint command and distinguish pre-existing failures from new failures.
9. Run TypeScript validation.
10. Run the production build.
11. Review the complete Git diff.
12. Search changed files for secrets, debug output, bypasses, unsafe casts, rule suppression, and unintended data exposure.
13. Verify the expected final completion marker in the saved validation evidence file.

## Evidence file to create outside the repository

```text
/home/trovas/Downloads/projects/byupw/selfless-controlled-reassignment-validation.txt
```

This evidence file must not be committed to the repository.

## Completion criteria

- Every required validation command succeeds, except any explicitly documented pre-existing repository-wide lint failures.
- No new lint error is introduced by the changed files.
- Targeted reassignment tests pass completely.
- The production build succeeds.
- The worktree contains only intended patch changes.
- The final patch commit is verified.

## Gate

Stop after full validation and the verified final commit. Do not push or open a pull request without explicit authorization.

---

# Phase 8: Documentation and Pull-Request Preparation

## Objective

Prepare a concise, reviewable contribution package for the Integration Owner and upstream maintainers.

## Existing files to inspect before modification

```text
README.md
```

Also inspect any contribution, security, changelog, or pull-request template files discovered during Phase 1.

## Candidate files to modify

```text
README.md
```

README modification is conditional and should occur only if the reassignment policy is user- or operator-facing documentation that belongs there.

## Candidate files to create

Use the repository's confirmed documentation convention. Possible files include:

```text
docs/cleaning-reassignment-policy.md
docs/cleaning-reassignment-test-evidence.md
```

If governance files are absent, they should not be added silently as part of this functional patch unless separately approved.

## Pull-request content

- Problem being corrected
- Confirmed business rule
- Previous and new behavior
- Files changed
- Database or migration effects
- Security and tenant controls
- Test evidence
- Known limitations
- Deployment requirements
- Rollback approach
- Screenshots only where they help reviewers understand the interface change

## Completion criteria

- Documentation matches the implemented behavior.
- The pull-request narrative is concise and evidence-led.
- All commits are verified and scoped.
- No secret, local environment file, validation transcript, or generated dependency directory is staged.
- Push and pull-request actions remain pending explicit authorization.

## Final Gate

Stop after the contribution package is ready. Request explicit authorization before pushing the branch or opening the pull request.

---

## 3. Provisional File Impact Register

The following list is deliberately provisional. An entry does not authorize modification. Phase 1 must confirm whether each file exists, what responsibility it currently has, and whether another file owns the same concern.

### Existing files likely to require inspection

```text
prisma/schema.prisma
lib/auth/nextauth.ts
lib/auth/server.ts
lib/auth/types.ts
lib/prisma/client.ts
app/api/cleaning/register/route.ts
app/api/cleaning/change-day/route.ts
app/api/cleaning/student/route.ts
app/api/admin/cleaning/change/route.ts
app/api/admin/cleaning/manual-assign/route.ts
app/api/admin/cleaning/remove-student/route.ts
app/api/admin/cleaning/remove/[userId]/route.ts
hooks/useCleaning.ts
hooks/useCleaningStudent.ts
app/dashboard/cleaning/page.tsx
package.json
README.md
```

### Possible new files, subject to structural inspection

```text
docs/cleaning-reassignment-inspection.md
docs/cleaning-reassignment-design.md
lib/cleaning/reassignment-policy.ts
lib/cleaning/reassignment-service.ts
lib/validation/cleaning-reassignment.ts
tests/cleaning/reassignment-policy.test.ts
tests/cleaning/change-day-route.test.ts
tests/cleaning/reassignment-concurrency.test.ts
tests/fixtures/cleaning.ts
tests/helpers/auth-session.ts
tests/helpers/database.ts
docs/cleaning-reassignment-policy.md
docs/cleaning-reassignment-test-evidence.md
```

### Possible new directories, subject to repository conventions

```text
docs/
lib/cleaning/
lib/validation/
tests/
tests/cleaning/
tests/fixtures/
tests/helpers/
app/dashboard/cleaning/components/
```

---

## 4. Definition of Done

The controlled reassignment patch will be complete only when:

- The current implementation was inspected before any modification.
- The user can make up to three successful cleaning-assignment changes.
- A fourth successful change is impossible through both the interface and direct API access.
- Failed and unchanged requests do not consume the allowance.
- Reassignment remains constrained by authentication, ownership, tech center, registration status, and capacity.
- Counter enforcement and reassignment are atomic.
- Successful changes are auditable.
- Administrative behavior matches the Integration Owner's approved policy.
- Targeted automated tests cover all success and denied paths.
- Changed files introduce no new lint or TypeScript failures.
- Prisma and production-build validation succeed.
- The final worktree and Git diff contain only intended changes.
- Every completed implementation phase has a verified Git commit.
- The branch is not pushed and no pull request is opened without explicit authorization.
