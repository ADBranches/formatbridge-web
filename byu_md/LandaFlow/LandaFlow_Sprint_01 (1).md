# LandaFlow Sprint 01

## Platform Foundation, Development Environment, Identity and Organisation Access

**Sprint duration:** 1 week  
**Sprint objective:** Establish a secure, reproducible and deployable foundation for LandaFlow, including the repository structure, local development environment, continuous integration, database baseline, authentication, organisation isolation, user roles, audit logging and the first JulyHost deployment path.

---

## 1. Sprint Outcome

At the end of Sprint 01, the team must have a working platform foundation on which all later property, tenant, billing and payment capabilities can be built safely.

A user must be able to:

1. Open the LandaFlow web application.
2. Register or receive an invitation.
3. Sign in and sign out securely.
4. Create or join an organisation.
5. Access only the organisation and functions permitted by their role.
6. Recover access through the supported password-reset flow.
7. View a minimal authenticated workspace.

The development team must also be able to:

1. Start the complete development environment with documented commands.
2. run database migrations and seed non-production data;
3. execute linting, type checks, unit tests and build checks;
4. develop through protected branches and reviewed pull requests;
5. deploy the initial containerised application to JulyHost; and
6. inspect health, logs and audit events without exposing secrets.

---

## 2. Scope

### Included

- Monorepo and workspace configuration
- Web application and backend API foundations
- PostgreSQL and Redis development services
- Docker-based local environment
- Environment-variable validation
- Database schema and migration framework
- User authentication and session handling
- Organisation creation and membership
- Role-based access control
- Organisation-level data isolation
- User invitation workflow
- Password recovery workflow
- Minimal authenticated dashboard shell
- Structured logging and health checks
- Foundational audit logging
- Continuous integration checks
- JulyHost deployment preparation
- Initial technical and contributor documentation

### Excluded

- Property and unit management
- Tenant profiles and tenancy assignment
- Rental agreements
- Invoice generation
- Rent ledger and reconciliation
- Mobile Money integrations
- EFRIS integration
- Maintenance requests
- Subscription billing
- AI-assisted features

These capabilities will be implemented in later sprints after the platform foundation is verified.

---

## 3. Delivery Principles

- All work must be performed on dedicated branches and submitted through pull requests.
- No contributor may push implementation changes directly to the protected integration or production branch.
- Each phase must have a focused objective, limited file surface and explicit validation evidence.
- Shared contracts, database rules and access controls must be agreed before dependent user-interface work is merged.
- Secrets, tokens, passwords and production credentials must never enter Git history.
- Free-tier or open-source services must be used unless a paid requirement is separately documented and approved.
- The application must remain portable and deployable through containers.
- A phase is complete only when its required checks pass and the expected evidence has been attached to its pull request.
- Later phases may begin in parallel only when they do not depend on unmerged contracts from an earlier phase.

---

## 4. Proposed Repository Structure

```text
landaflow/
├── apps/
│   ├── web/
│   └── api/
├── packages/
│   ├── config/
│   ├── database/
│   ├── eslint-config/
│   ├── types/
│   └── ui/
├── infrastructure/
│   ├── docker/
│   └── julyhost/
├── docs/
│   ├── architecture/
│   ├── development/
│   ├── operations/
│   └── security/
├── scripts/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── docker-compose.yml
├── package.json
├── pnpm-lock.yaml
├── pnpm-workspace.yaml
├── turbo.json
├── tsconfig.base.json
├── .env.example
├── .gitignore
├── CODEOWNERS
├── CONTRIBUTING.md
├── README.md
└── SECURITY.md
```

---

# 5. Sprint Phases

## Phase 1: Repository and Collaboration Foundation

### Objective

Create the shared repository structure, development conventions, branch protections, pull-request workflow and baseline documentation required for parallel team delivery.

### Work

- Initialise the monorepo using pnpm workspaces and Turborepo.
- Create the Next.js web application and NestJS API application.
- Establish shared TypeScript, linting and formatting configuration.
- Add repository ownership and contribution rules.
- Add issue and pull-request templates.
- Define branch naming and commit conventions.
- Document the local setup and pull-request workflow.

### Files to create

```text
package.json
pnpm-workspace.yaml
pnpm-lock.yaml
turbo.json
tsconfig.base.json
.gitignore
.editorconfig
.prettierignore
.prettierrc.json
README.md
CONTRIBUTING.md
SECURITY.md
CODEOWNERS
.github/PULL_REQUEST_TEMPLATE.md
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
apps/web/package.json
apps/web/next.config.ts
apps/web/tsconfig.json
apps/web/src/app/layout.tsx
apps/web/src/app/page.tsx
apps/api/package.json
apps/api/nest-cli.json
apps/api/tsconfig.json
apps/api/src/main.ts
apps/api/src/app.module.ts
packages/eslint-config/package.json
packages/eslint-config/base.js
packages/config/package.json
packages/types/package.json
packages/types/src/index.ts
```

### Files likely to be modified

```text
README.md
CONTRIBUTING.md
CODEOWNERS
package.json
turbo.json
```

### Validation

```text
pnpm install
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

### Completion evidence

- Fresh clone installs successfully.
- Web and API applications start without shell or runtime errors.
- Workspace-wide linting, type checking, testing and builds pass.
- Pull-request template and ownership rules are active.

---

## Phase 2: Local Infrastructure and Configuration

### Objective

Provide a reproducible local environment for the web application, API, PostgreSQL and Redis, with validated configuration and no committed secrets.

### Work

- Define Docker images for the web and API applications.
- Configure PostgreSQL and Redis in Docker Compose.
- Add health checks for all containers.
- Establish environment-variable validation.
- Create safe development defaults and a complete example environment file.
- Document environment startup, shutdown, reset and troubleshooting procedures.

### Files to create

```text
Dockerfile.web
Dockerfile.api
docker-compose.yml
.dockerignore
.env.example
infrastructure/docker/postgres/init.sql
packages/config/src/env.ts
packages/config/src/index.ts
apps/api/src/config/config.module.ts
apps/api/src/config/configuration.ts
apps/web/src/lib/env.ts
docs/development/local-environment.md
docs/development/environment-variables.md
scripts/dev-start.sh
scripts/dev-stop.sh
scripts/dev-reset.sh
```

### Files likely to be modified

```text
package.json
README.md
apps/api/src/app.module.ts
apps/api/src/main.ts
apps/web/next.config.ts
```

### Validation

```text
docker compose config
docker compose up --build -d
docker compose ps
docker compose logs --no-color api
docker compose logs --no-color web
```

### Completion evidence

- All containers become healthy.
- The API connects to PostgreSQL and Redis.
- Missing or invalid required variables cause a clear startup failure.
- No secrets are present in tracked files.
- A new contributor can start the environment from the documentation.

---

## Phase 3: Database Foundation and Organisation Isolation

### Objective

Establish the initial relational model, migrations, safe seed data and repository layer for users, organisations, memberships, roles and audit events.

### Work

- Configure Prisma with PostgreSQL.
- Define identifiers, timestamps and archival conventions.
- Model users, organisations, memberships, roles, invitations and audit events.
- Add unique constraints and indexes.
- Implement migrations and non-production seed data.
- Provide transaction helpers and organisation-scoped repository patterns.
- Document the database model and migration procedure.

### Files to create

```text
packages/database/package.json
packages/database/prisma/schema.prisma
packages/database/prisma/seed.ts
packages/database/src/client.ts
packages/database/src/index.ts
packages/database/src/transactions.ts
packages/database/src/tenant-scope.ts
packages/database/prisma/migrations/<timestamp>_initial_identity_schema/migration.sql
apps/api/src/database/database.module.ts
apps/api/src/database/prisma.service.ts
docs/architecture/database-model.md
docs/development/database-migrations.md
```

### Files likely to be modified

```text
.env.example
package.json
pnpm-workspace.yaml
apps/api/src/app.module.ts
```

### Required initial models

```text
User
Organisation
OrganisationMembership
Role
Permission
RolePermission
OrganisationInvitation
RefreshSession
PasswordResetToken
AuditEvent
```

### Validation

```text
pnpm --filter @landaflow/database prisma validate
pnpm --filter @landaflow/database prisma migrate deploy
pnpm --filter @landaflow/database seed
pnpm --filter @landaflow/database test
```

### Completion evidence

- Migrations apply correctly to an empty database.
- Seed data is prohibited in production mode.
- Duplicate memberships and invalid relationships are rejected.
- Organisation-scoped queries cannot return another organisation's records.
- Migration and rollback considerations are documented.

---

## Phase 4: Authentication and Session Security

### Objective

Implement secure user registration, sign-in, sign-out, token rotation, password recovery and authenticated request handling.

### Work

- Implement email-and-password authentication for the MVP.
- Hash passwords with Argon2id.
- Issue short-lived access tokens and rotating refresh sessions.
- Store refresh credentials using secure, HTTP-only cookies.
- Add sign-out and session revocation.
- Add password-reset request and completion workflows.
- Rate-limit authentication endpoints.
- Prevent account enumeration through public responses.
- Add authenticated API guards and current-user context.

### Files to create

```text
apps/api/src/auth/auth.module.ts
apps/api/src/auth/auth.controller.ts
apps/api/src/auth/auth.service.ts
apps/api/src/auth/dto/register.dto.ts
apps/api/src/auth/dto/login.dto.ts
apps/api/src/auth/dto/request-password-reset.dto.ts
apps/api/src/auth/dto/reset-password.dto.ts
apps/api/src/auth/guards/access-token.guard.ts
apps/api/src/auth/guards/refresh-token.guard.ts
apps/api/src/auth/strategies/access-token.strategy.ts
apps/api/src/auth/strategies/refresh-token.strategy.ts
apps/api/src/auth/decorators/current-user.decorator.ts
apps/api/src/auth/security/password.service.ts
apps/api/src/auth/security/token.service.ts
apps/api/src/auth/auth.service.spec.ts
apps/web/src/app/(auth)/login/page.tsx
apps/web/src/app/(auth)/register/page.tsx
apps/web/src/app/(auth)/forgot-password/page.tsx
apps/web/src/app/(auth)/reset-password/page.tsx
apps/web/src/features/auth/api.ts
apps/web/src/features/auth/schemas.ts
apps/web/src/features/auth/components/login-form.tsx
apps/web/src/features/auth/components/register-form.tsx
apps/web/src/middleware.ts
docs/security/authentication.md
```

### Files likely to be modified

```text
apps/api/src/app.module.ts
apps/api/src/main.ts
apps/web/src/app/layout.tsx
packages/database/prisma/schema.prisma
.env.example
```

### Validation

- Registration succeeds with valid input and rejects duplicates safely.
- Passwords are never stored or logged in plain text.
- Sign-in rejects invalid credentials without revealing whether an account exists.
- Refresh-session rotation invalidates the previous refresh credential.
- Sign-out revokes the active session.
- Password-reset tokens are single-use and expire.
- Protected routes reject unauthenticated requests.
- Authentication rate limits are enforced.

### Completion evidence

- Unit and integration tests cover successful and unsuccessful authentication paths.
- Browser tests cover registration, sign-in, sign-out and password reset.
- Cookies and security headers are verified in a production-like environment.

---

## Phase 5: Organisations, Memberships and Role-Based Access

### Objective

Implement multi-organisation onboarding, invitations, memberships and enforceable role-based permissions across the API and web interface.

### Work

- Create organisation onboarding.
- Allow authorised users to invite team members.
- Implement invitation acceptance and expiry.
- Define MVP roles and permissions.
- Enforce organisation membership on every organisation-scoped endpoint.
- Add permission guards and decorators.
- Create minimal organisation and team-management screens.
- Record administrative access changes in the audit log.

### MVP roles

```text
OWNER
PROPERTY_MANAGER
ACCOUNTANT
SUPPORT_VIEWER
TENANT
PLATFORM_ADMIN
```

### Files to create

```text
apps/api/src/organisations/organisations.module.ts
apps/api/src/organisations/organisations.controller.ts
apps/api/src/organisations/organisations.service.ts
apps/api/src/organisations/dto/create-organisation.dto.ts
apps/api/src/organisations/dto/update-organisation.dto.ts
apps/api/src/memberships/memberships.module.ts
apps/api/src/memberships/memberships.controller.ts
apps/api/src/memberships/memberships.service.ts
apps/api/src/memberships/dto/invite-member.dto.ts
apps/api/src/memberships/dto/update-member-role.dto.ts
apps/api/src/authorisation/authorisation.module.ts
apps/api/src/authorisation/permissions.ts
apps/api/src/authorisation/roles.ts
apps/api/src/authorisation/guards/organisation.guard.ts
apps/api/src/authorisation/guards/permissions.guard.ts
apps/api/src/authorisation/decorators/require-permissions.decorator.ts
apps/api/src/authorisation/decorators/current-organisation.decorator.ts
apps/api/src/authorisation/authorisation.service.spec.ts
apps/web/src/app/(app)/onboarding/organisation/page.tsx
apps/web/src/app/(app)/settings/organisation/page.tsx
apps/web/src/app/(app)/settings/team/page.tsx
apps/web/src/features/organisations/api.ts
apps/web/src/features/organisations/schemas.ts
apps/web/src/features/memberships/api.ts
apps/web/src/features/memberships/components/invite-member-form.tsx
packages/types/src/authorisation.ts
docs/security/roles-and-permissions.md
```

### Files likely to be modified

```text
packages/database/prisma/schema.prisma
apps/api/src/app.module.ts
apps/web/src/middleware.ts
apps/web/src/app/(app)/layout.tsx
```

### Validation

- Organisation owners can invite and manage permitted team members.
- Invitations expire and cannot be reused.
- A user without membership cannot access an organisation.
- A user cannot escalate their own role.
- Accountants cannot perform owner-only actions.
- Tenant permissions do not expose management records.
- Cross-organisation identifiers do not bypass access controls.

### Completion evidence

- Permission matrix tests pass.
- Cross-organisation isolation tests pass.
- Invitation and membership browser journeys pass.
- Audit records identify the actor, organisation, action and affected record.

---

## Phase 6: Authenticated Workspace and Shared Interface Foundation

### Objective

Deliver the minimal authenticated LandaFlow workspace and reusable user-interface foundation required by later feature teams.

### Work

- Create the authenticated application shell.
- Add accessible navigation for dashboard and settings.
- Display organisation context and current user details.
- Add loading, empty, error and unauthorised states.
- Establish reusable form, notification and dialog components.
- Implement a typed API client and standard error handling.
- Provide a minimal dashboard containing only verified foundation data.

### Files to create

```text
apps/web/src/app/(app)/layout.tsx
apps/web/src/app/(app)/dashboard/page.tsx
apps/web/src/app/(app)/settings/page.tsx
apps/web/src/app/unauthorised/page.tsx
apps/web/src/components/app-shell.tsx
apps/web/src/components/app-sidebar.tsx
apps/web/src/components/app-header.tsx
apps/web/src/components/organisation-switcher.tsx
apps/web/src/components/user-menu.tsx
apps/web/src/components/empty-state.tsx
apps/web/src/components/error-state.tsx
apps/web/src/components/loading-state.tsx
apps/web/src/lib/api-client.ts
apps/web/src/lib/query-client.ts
apps/web/src/lib/session.ts
packages/ui/package.json
packages/ui/src/button.tsx
packages/ui/src/dialog.tsx
packages/ui/src/form-field.tsx
packages/ui/src/input.tsx
packages/ui/src/notification.tsx
packages/ui/src/index.ts
```

### Files likely to be modified

```text
apps/web/src/app/layout.tsx
apps/web/src/app/globals.css
apps/web/package.json
packages/types/src/index.ts
```

### Validation

- Authenticated users reach the workspace after sign-in.
- Unauthenticated users are redirected to sign-in.
- Navigation reflects the user's permissions.
- The workspace remains usable at mobile, tablet and desktop widths.
- Keyboard navigation and visible focus states work correctly.
- API errors do not disclose internal exception details.

### Completion evidence

- Playwright tests cover authentication redirects, navigation and organisation context.
- Accessibility checks reveal no critical violations in covered screens.
- The interface uses only live foundation data, not hard-coded financial or property figures.

---

## Phase 7: Auditability, Health Monitoring and Continuous Integration

### Objective

Provide enforceable quality gates, operational health endpoints, structured logs and audit records before the first shared deployment.

### Work

- Add API liveness and readiness endpoints.
- Add structured application logging with correlation identifiers.
- Redact credentials and sensitive request fields from logs.
- Implement an audit service for security-sensitive and administrative events.
- Add GitHub Actions for linting, type checking, testing, migration validation and builds.
- Add dependency and secret scanning using free repository capabilities.
- Publish test evidence as pull-request checks.

### Files to create

```text
apps/api/src/health/health.module.ts
apps/api/src/health/health.controller.ts
apps/api/src/health/health.service.ts
apps/api/src/common/interceptors/correlation-id.interceptor.ts
apps/api/src/common/interceptors/request-logging.interceptor.ts
apps/api/src/common/filters/http-exception.filter.ts
apps/api/src/audit/audit.module.ts
apps/api/src/audit/audit.service.ts
apps/api/src/audit/audit.types.ts
apps/api/src/audit/audit.service.spec.ts
.github/workflows/ci.yml
.github/workflows/dependency-review.yml
.github/dependabot.yml
docs/operations/health-and-logging.md
docs/security/audit-events.md
```

### Files likely to be modified

```text
apps/api/src/main.ts
apps/api/src/app.module.ts
package.json
docker-compose.yml
```

### Validation

- Liveness succeeds when the application process is running.
- Readiness fails when required database or Redis dependencies are unavailable.
- Every request receives a traceable correlation identifier.
- Sensitive fields are absent from logs.
- Pull requests cannot pass when linting, typing, tests or builds fail.
- Audit events are immutable through ordinary application endpoints.

### Completion evidence

- CI completes successfully on the sprint branch.
- A forced failing test proves that CI blocks merge eligibility.
- Health checks correctly distinguish healthy and unavailable dependencies.
- Audit and application logs are readable and contain no credentials.

---

## Phase 8: JulyHost Deployment Foundation and Sprint Acceptance

### Objective

Deploy the integrated Sprint 01 foundation to JulyHost and prove that the complete authentication and organisation journey works in a production-like environment.

### Work

- Define the JulyHost deployment layout.
- Configure production Docker Compose services.
- Add reverse-proxy configuration and HTTPS expectations.
- Document DNS, environment variables, migrations, deployment and rollback.
- Configure persistent database and application data volumes.
- Add backup and restoration scripts for PostgreSQL.
- Execute end-to-end acceptance tests against the deployed environment.
- Prepare the sprint completion pull request and validation record.

### Files to create

```text
infrastructure/julyhost/docker-compose.production.yml
infrastructure/julyhost/Caddyfile
infrastructure/julyhost/.env.production.example
infrastructure/julyhost/deploy.sh
infrastructure/julyhost/rollback.sh
infrastructure/julyhost/backup-postgres.sh
infrastructure/julyhost/restore-postgres.sh
docs/operations/julyhost-deployment.md
docs/operations/backup-and-restoration.md
docs/operations/release-checklist.md
tests/e2e/authentication.spec.ts
tests/e2e/organisation-onboarding.spec.ts
tests/e2e/permissions.spec.ts
tests/e2e/health.spec.ts
docs/validation/sprint-01-acceptance.md
```

### Files likely to be modified

```text
.env.example
README.md
package.json
docker-compose.yml
apps/api/src/main.ts
apps/web/next.config.ts
```

### Validation

```text
docker compose -f infrastructure/julyhost/docker-compose.production.yml config
pnpm lint
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm build
```

### Production-like checks

- HTTPS is enforced at the public endpoint.
- Production secrets exist only in the hosting environment.
- Database migrations complete before application traffic is accepted.
- Persistent data remains available after container restart.
- Backup creation and restoration are successfully tested.
- Registration, sign-in, organisation creation, invitation, permission enforcement and sign-out work end to end.
- Logs, health checks and audit events are available to authorised operators.

### Completion evidence

- Deployment endpoint and commit identifier are recorded.
- All required CI checks pass.
- End-to-end acceptance results are attached to the pull request.
- Backup and restoration evidence is recorded.
- No unresolved critical or high-severity defect remains.

---

# 6. Team Work Allocation

## Platform and Infrastructure Team

Owns:

- Phases 1, 2, 7 and 8
- Docker, GitHub Actions and JulyHost deployment
- Environment configuration, health checks and operational documentation

## Backend and Data Team

Owns:

- Phases 3, 4 and 5 backend work
- Database schema, migrations and organisation isolation
- Authentication, sessions, permissions and audit integration

## Web Experience Team

Owns:

- Phases 4, 5 and 6 frontend work
- Authentication screens, organisation onboarding and team management
- Authenticated workspace and responsive shared components

## Quality and Security Review

Owns:

- Test strategy and acceptance evidence
- Cross-organisation access testing
- Session and password-recovery verification
- Dependency, secret and configuration review
- Release-readiness assessment

Teams may work concurrently after shared contracts have been reviewed and merged. Dependency changes must not be duplicated across competing pull requests.

---

# 7. Branch and Pull-Request Plan

Recommended branch names:

```text
foundation/repository-workspace
foundation/local-infrastructure
foundation/database-identity-model
feature/authentication-sessions
feature/organisation-access-control
feature/authenticated-workspace
operations/ci-audit-health
operations/julyhost-deployment
```

Each pull request must include:

- A precise title describing the delivered capability
- Scope and affected user journeys
- Technical implementation details
- Security and access-control considerations
- Database or migration impact
- Validation commands and complete results
- Deployment or configuration impact
- Risks and known limitations
- Rollback considerations
- Reviewer focus areas
- Screenshots only where they help verify interface behaviour

A pull request must not be merged when:

- required checks fail;
- migration effects are not understood;
- access controls are incomplete;
- secrets or credentials are exposed;
- required review is missing; or
- validation evidence does not match the submitted commit.

---

# 8. Sprint-Wide Testing Requirements

## Unit tests

- Password hashing and verification
- Token creation, expiry and rotation
- Organisation and membership services
- Permission evaluation
- Environment validation
- Audit-event construction

## Integration tests

- Registration and sign-in against PostgreSQL
- Refresh-session rotation and revocation
- Password-reset lifecycle
- Organisation creation and invitation acceptance
- Organisation-scoped queries
- Role and permission enforcement
- Readiness checks with available and unavailable dependencies

## End-to-end tests

- Register, create an organisation and reach the workspace
- Sign in, refresh the session and sign out
- Request and complete password reset
- Invite a user and accept the invitation
- Deny unauthorised role changes
- Prevent cross-organisation access
- Confirm responsive authenticated navigation

## Security checks

- Secret scanning
- Dependency review
- Authentication rate limits
- Cookie flags and transport security
- Input validation
- Error-message disclosure
- Log redaction
- Cross-organisation identifier manipulation

---

# 9. Definition of Done

Sprint 01 is complete only when all of the following are true:

- [ ] Repository structure and contributor workflow are documented.
- [ ] Local Docker environment starts successfully from a fresh clone.
- [ ] PostgreSQL and Redis health checks pass.
- [ ] Database migrations apply successfully to an empty database.
- [ ] Registration, sign-in, refresh, sign-out and password reset work.
- [ ] Organisation creation and member invitations work.
- [ ] Role-based permissions are enforced by the API.
- [ ] Cross-organisation access tests pass.
- [ ] The authenticated workspace is responsive and accessible.
- [ ] Audit records exist for relevant identity and access changes.
- [ ] Logs contain correlation identifiers and exclude sensitive fields.
- [ ] CI runs linting, type checks, tests and builds successfully.
- [ ] The integrated foundation is deployed to JulyHost.
- [ ] Backup and restoration are tested successfully.
- [ ] All required pull requests are reviewed and merged.
- [ ] No unresolved critical or high-severity defect remains.
- [ ] Acceptance evidence identifies the exact verified commit.

---

# 10. Sprint Acceptance Demonstration

The final demonstration must use the integrated JulyHost environment and show this uninterrupted journey:

1. A new user registers.
2. The user signs in.
3. The user creates an organisation.
4. The user reaches the authenticated workspace.
5. The organisation owner invites a second team member.
6. The invited member accepts the invitation.
7. The owner assigns an allowed role.
8. The second user accesses only the functions permitted by that role.
9. An attempted unauthorised action is rejected.
10. An attempted cross-organisation request is rejected.
11. Relevant actions appear in the audit record.
12. Both users sign out and their sessions are invalidated.
13. Health checks confirm that the deployed dependencies are operational.
14. The team identifies the deployed commit and associated validation evidence.

---

# 11. Risks and Controls

## Integration conflicts

Keep pull requests focused, merge shared contracts early and require dependent branches to rebase before final review.

## Authentication weaknesses

Use established cryptographic libraries, short-lived access tokens, rotating refresh sessions, secure cookies, rate limits and explicit revocation tests.

## Cross-organisation data exposure

Apply organisation scope in the service and repository layers, enforce membership guards and test identifier manipulation directly.

## Environment drift

Use Docker, committed example configuration, automated validation and the same container images across development and JulyHost.

## Free-tier limitations

Keep all optional external services behind adapters. Core authentication, authorisation and application operation must not depend on a paid service.

## Deployment failure

Use health checks, migration controls, persistent volumes, backups and a documented rollback procedure before accepting the deployment.

---

# 12. Handover to Sprint 02

Sprint 02 may begin only after Sprint 01 acceptance is complete. It will use the verified organisation, identity, permission and deployment foundation to implement:

- property registration;
- blocks, floors and unit structures;
- unit status and occupancy foundations;
- tenant registration;
- tenant-to-unit assignment;
- supporting document storage; and
- the first property and tenancy management interfaces.
