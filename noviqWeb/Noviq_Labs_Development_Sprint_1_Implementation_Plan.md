# Noviq Labs Full-Stack Platform

## Development Sprint 1: Engineering Foundation

**Sprint position:** First production implementation sprint after the approved product, architecture, brand, UX and design stages  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Architecture:** Modular monolith with independently deployable web, API and worker applications  
**Approved stack:** Next.js, React, TypeScript, Tailwind CSS, ASP.NET Core, C#, Entity Framework Core, PostgreSQL, Redis and Docker

## Sprint Objective

Establish a secure, reproducible and testable engineering foundation for the complete end-to-end Noviq Labs platform. The sprint will create the monorepo, scaffold the frontend, backend and worker applications, configure local infrastructure, establish database migration control, introduce automated quality gates and prepare the codebase for continuous delivery in subsequent sprints.

---

## Phase 1: Workstation, Account and Repository Readiness

### Objectives

- Verify Git identity and GitHub authentication on Kali Debian.
- Confirm the development shell is Zsh and preserve the existing NVM-managed Node.js environment.
- Verify supported versions of Node.js, npm, .NET SDK, Docker, Docker Compose, Git and PostgreSQL client tools.
- Create the official GitHub repository under the approved Noviq Labs ownership model.
- Configure the default branch and protected development workflow.
- Prohibit direct development on the production branch.
- Create the Sprint 1 development branch.
- Establish pull-request review, status-check and commit requirements.
- Record all environment assumptions without committing credentials or secrets.

### Files to create

```text
/.gitignore
/.gitattributes
/.editorconfig
/.nvmrc
/global.json
/README.md
/CONTRIBUTING.md
/CODEOWNERS
/docs/development/workstation-requirements.md
/docs/development/github-workflow.md
/docs/development/branching-strategy.md
/docs/development/local-environment.md
```

---

## Phase 2: Monorepo and Workspace Foundation

### Objectives

- Create one monorepo for the web application, API, worker, shared packages, infrastructure, documentation and automated tests.
- Configure npm workspaces for JavaScript and TypeScript packages.
- Create the .NET solution and register all backend projects.
- Establish consistent root scripts for build, test, lint, format and local startup.
- Keep frontend, backend and worker boundaries explicit while preserving one coherent platform repository.
- Prevent premature microservice separation.

### Files to create

```text
/package.json
/package-lock.json
/tsconfig.base.json
/Directory.Build.props
/Directory.Packages.props
/NoviqLabs.Platform.sln
/apps/.gitkeep
/packages/.gitkeep
/infrastructure/.gitkeep
/docs/.gitkeep
/scripts/.gitkeep
/tests/.gitkeep
```

---

## Phase 3: Next.js Frontend Foundation

### Objectives

- Scaffold the production frontend with Next.js, React and TypeScript.
- Use the App Router and strict TypeScript settings.
- Configure Tailwind CSS as the responsive styling foundation.
- Establish the root application layout, metadata, error boundary, not-found state and loading state.
- Add a minimal health-facing application page without implementing public website features prematurely.
- Establish environment-variable validation and prohibit secret exposure to the browser.
- Add frontend formatting, linting, type-checking and unit-test foundations.
- Add the supplied Noviq logo resources as controlled application assets.

### Files to create

```text
/apps/web/package.json
/apps/web/next.config.ts
/apps/web/tsconfig.json
/apps/web/postcss.config.mjs
/apps/web/eslint.config.mjs
/apps/web/vitest.config.ts
/apps/web/vitest.setup.ts
/apps/web/src/app/layout.tsx
/apps/web/src/app/page.tsx
/apps/web/src/app/loading.tsx
/apps/web/src/app/error.tsx
/apps/web/src/app/not-found.tsx
/apps/web/src/app/globals.css
/apps/web/src/app/api/health/route.ts
/apps/web/src/components/README.md
/apps/web/src/features/README.md
/apps/web/src/lib/env.ts
/apps/web/src/lib/config.ts
/apps/web/src/lib/health.ts
/apps/web/src/types/environment.d.ts
/apps/web/src/app/page.test.tsx
/apps/web/public/brand/noviq-labs-horizontal.png
/apps/web/public/brand/noviq-labs-symbol.png
/apps/web/public/brand/noviq-labs-symbol-white-background.png
/apps/web/.env.example
/apps/web/Dockerfile
/apps/web/.dockerignore
```

---

## Phase 4: ASP.NET Core API Foundation

### Objectives

- Scaffold the ASP.NET Core Web API using the approved supported .NET version.
- Establish the modular-monolith project boundaries for API, Application, Domain, Infrastructure and Contracts.
- Add dependency injection, configuration validation and environment-specific configuration.
- Implement health, readiness and liveness endpoints.
- Establish standardized problem responses and correlation identifiers.
- Add structured application logging.
- Configure OpenAPI for development and staging use.
- Establish backend unit, integration and architecture-test foundations.
- Keep authentication integration prepared but deferred to the approved identity sprint.

### Files to create

```text
/apps/api/NoviqLabs.Api/NoviqLabs.Api.csproj
/apps/api/NoviqLabs.Api/Program.cs
/apps/api/NoviqLabs.Api/appsettings.json
/apps/api/NoviqLabs.Api/appsettings.Development.json
/apps/api/NoviqLabs.Api/Properties/launchSettings.json
/apps/api/NoviqLabs.Api/Configuration/ApiOptions.cs
/apps/api/NoviqLabs.Api/Configuration/DependencyInjection.cs
/apps/api/NoviqLabs.Api/Endpoints/HealthEndpoints.cs
/apps/api/NoviqLabs.Api/Middleware/CorrelationIdMiddleware.cs
/apps/api/NoviqLabs.Api/Middleware/ExceptionHandlingMiddleware.cs
/apps/api/NoviqLabs.Api/Errors/ApiProblemDetails.cs
/apps/api/NoviqLabs.Api/OpenApi/OpenApiConfiguration.cs
/apps/api/NoviqLabs.Api/.env.example
/apps/api/NoviqLabs.Api/Dockerfile
/apps/api/NoviqLabs.Api/.dockerignore
/apps/api/NoviqLabs.Application/NoviqLabs.Application.csproj
/apps/api/NoviqLabs.Application/DependencyInjection.cs
/apps/api/NoviqLabs.Domain/NoviqLabs.Domain.csproj
/apps/api/NoviqLabs.Domain/Common/Entity.cs
/apps/api/NoviqLabs.Domain/Common/AuditableEntity.cs
/apps/api/NoviqLabs.Infrastructure/NoviqLabs.Infrastructure.csproj
/apps/api/NoviqLabs.Infrastructure/DependencyInjection.cs
/apps/api/NoviqLabs.Contracts/NoviqLabs.Contracts.csproj
/tests/api/NoviqLabs.Api.UnitTests/NoviqLabs.Api.UnitTests.csproj
/tests/api/NoviqLabs.Api.UnitTests/HealthEndpointsTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/NoviqLabs.Api.IntegrationTests.csproj
/tests/api/NoviqLabs.Api.IntegrationTests/ApiWebApplicationFactory.cs
/tests/api/NoviqLabs.Api.IntegrationTests/HealthEndpointTests.cs
/tests/api/NoviqLabs.ArchitectureTests/NoviqLabs.ArchitectureTests.csproj
/tests/api/NoviqLabs.ArchitectureTests/LayerDependencyTests.cs
```

---

## Phase 5: Background Worker Foundation

### Objectives

- Scaffold the background worker as a separate deployable application.
- Establish structured logging, configuration validation and health reporting.
- Prepare the worker for future notifications, file scanning, scheduled publishing, webhook processing and asynchronous jobs.
- Avoid implementing business jobs before their feature sprints.
- Add worker unit-test foundations.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/NoviqLabs.Worker.csproj
/apps/worker/NoviqLabs.Worker/Program.cs
/apps/worker/NoviqLabs.Worker/Worker.cs
/apps/worker/NoviqLabs.Worker/appsettings.json
/apps/worker/NoviqLabs.Worker/appsettings.Development.json
/apps/worker/NoviqLabs.Worker/Configuration/WorkerOptions.cs
/apps/worker/NoviqLabs.Worker/Configuration/DependencyInjection.cs
/apps/worker/NoviqLabs.Worker/.env.example
/apps/worker/NoviqLabs.Worker/Dockerfile
/apps/worker/NoviqLabs.Worker/.dockerignore
/tests/worker/NoviqLabs.Worker.UnitTests/NoviqLabs.Worker.UnitTests.csproj
/tests/worker/NoviqLabs.Worker.UnitTests/WorkerTests.cs
```

---

## Phase 6: PostgreSQL and Entity Framework Core Foundation

### Objectives

- Configure PostgreSQL as the transactional system of record.
- Create the platform database context and initial schema boundary.
- Establish naming, migration and audit conventions.
- Create the initial migration without introducing premature feature tables.
- Configure resilient database connections and development-time diagnostics.
- Establish design-time migration support.
- Add migration and connectivity integration tests.
- Ensure database migrations are explicit, reviewable and pipeline-controlled.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Persistence/NoviqDbContext.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/NoviqDbContextFactory.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/DatabaseOptions.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/ModelConfigurationExtensions.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Interceptors/AuditableEntityInterceptor.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/InitialCreate.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/InitialCreate.Designer.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/NoviqDbContextModelSnapshot.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/DatabaseConnectivityTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/MigrationTests.cs
/docs/database/migration-policy.md
/docs/database/naming-conventions.md
```

---

## Phase 7: Redis and Distributed-State Foundation

### Objectives

- Configure Redis connectivity for future cache, throttling and temporary distributed state.
- Keep Redis outside the durable business-data boundary.
- Implement connection health verification.
- Define cache-key naming and expiry standards.
- Add integration tests for Redis availability and safe failure behavior.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Caching/RedisOptions.cs
/apps/api/NoviqLabs.Infrastructure/Caching/RedisConnectionFactory.cs
/apps/api/NoviqLabs.Infrastructure/Caching/CacheKey.cs
/apps/api/NoviqLabs.Infrastructure/Health/RedisHealthCheck.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Caching/RedisConnectivityTests.cs
/docs/architecture/cache-boundary.md
```

---

## Phase 8: Local Containerized Development Environment

### Objectives

- Create a reproducible local environment for the web, API, worker, PostgreSQL and Redis services.
- Support Kali Debian and Zsh without requiring manual service installation for every dependency.
- Add persistent local volumes for development data.
- Add service health checks and startup ordering.
- Keep source-code development fast through suitable bind mounts or development targets.
- Confirm the entire stack starts and stops cleanly.
- Ensure no real secret is embedded in container definitions.

### Files to create

```text
/compose.yaml
/compose.override.yaml
/.env.example
/infrastructure/docker/postgres/init/001-create-development-database.sql
/infrastructure/docker/README.md
/scripts/dev/start.zsh
/scripts/dev/stop.zsh
/scripts/dev/status.zsh
/scripts/dev/reset-local-data.zsh
/scripts/dev/verify-environment.zsh
```

---

## Phase 9: Code Quality and Automated Testing Foundation

### Objectives

- Configure consistent formatting, linting, type checking and test execution.
- Add frontend unit-test coverage for the initial application shell.
- Add backend unit, integration and architecture tests.
- Add worker tests.
- Establish a single local validation command that does not hide underlying failures.
- Ensure every required validation reports its real exit status.
- Establish initial coverage reporting without using coverage percentage alone as a release decision.

### Files to create

```text
/.prettierrc.json
/.prettierignore
/.markdownlint.json
/.markdownlintignore
/scripts/quality/validate-all.zsh
/scripts/quality/validate-web.zsh
/scripts/quality/validate-api.zsh
/scripts/quality/validate-worker.zsh
/scripts/quality/validate-containers.zsh
/scripts/quality/validate-migrations.zsh
/docs/quality/testing-strategy.md
/docs/quality/definition-of-done.md
```

---

## Phase 10: Security Baseline and Secret Management

### Objectives

- Establish secure configuration boundaries for local, CI, staging and production environments.
- Keep credentials, tokens, connection strings and certificates outside source control.
- Configure dependency, secret and container scanning foundations.
- Define secure logging rules that prohibit sensitive-data leakage.
- Introduce baseline application security headers at the frontend boundary.
- Establish dependency-update governance.
- Add a responsible vulnerability-reporting document.
- Record a baseline threat model for the engineering foundation.

### Files to create

```text
/.github/dependabot.yml
/.github/SECURITY.md
/.github/pull_request_template.md
/.github/ISSUE_TEMPLATE/bug_report.yml
/.github/ISSUE_TEMPLATE/security_configuration.yml
/apps/web/src/middleware.ts
/apps/web/src/security/headers.ts
/apps/api/NoviqLabs.Api/Security/SecurityConfiguration.cs
/docs/security/secure-configuration.md
/docs/security/logging-and-sensitive-data.md
/docs/security/threat-model-sprint-1.md
/docs/security/dependency-management.md
```

---

## Phase 11: Continuous Integration and Pull-Request Gates

### Objectives

- Create GitHub Actions workflows for frontend, backend, worker, migration and container validation.
- Run linting, formatting, type checks and automated tests on pull requests.
- Run dependency, secret and container scans.
- Build production container images without publishing them from untrusted branches.
- Add migration validation against an ephemeral PostgreSQL service.
- Enforce required checks before merge.
- Preserve complete logs for failed validation.
- Prevent a failed underlying command from being reported as a pass.

### Files to create

```text
/.github/workflows/ci-web.yml
/.github/workflows/ci-api.yml
/.github/workflows/ci-worker.yml
/.github/workflows/ci-database.yml
/.github/workflows/ci-containers.yml
/.github/workflows/security-scan.yml
/.github/workflows/markdown-lint.yml
/.github/workflows/pr-quality-gate.yml
/docs/delivery/continuous-integration.md
/docs/delivery/pull-request-gates.md
```

---

## Phase 12: Logging, Health and Operational Readiness Foundation

### Objectives

- Standardize correlation identifiers across frontend, API and worker requests.
- Add structured logs suitable for future Azure Monitor and Application Insights integration.
- Expose liveness and readiness checks without disclosing sensitive internals.
- Define environment-safe log levels.
- Establish initial operational runbooks for startup, shutdown and degraded dependencies.
- Prepare observability interfaces without prematurely provisioning the complete Azure production environment.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Observability/LoggingConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Observability/TelemetryConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Health/PostgreSqlHealthCheck.cs
/apps/api/NoviqLabs.Infrastructure/Health/HealthResponseWriter.cs
/apps/worker/NoviqLabs.Worker/Observability/LoggingConfiguration.cs
/apps/worker/NoviqLabs.Worker/Observability/TelemetryConfiguration.cs
/apps/web/src/lib/observability/correlation.ts
/apps/web/src/lib/observability/logger.ts
/docs/operations/health-checks.md
/docs/operations/logging.md
/docs/operations/local-runbook.md
```

---

## Phase 13: Documentation and Architecture Records

### Objectives

- Document the repository structure and module boundaries.
- Record why the platform begins as a modular monolith.
- Record the approved frontend, backend, database, cache and container decisions.
- Document local setup specifically for Kali Debian and Zsh.
- Document migration, testing, branching, validation and troubleshooting procedures.
- Keep documentation executable and aligned with the actual repository.

### Files to create

```text
/docs/architecture/system-context.md
/docs/architecture/container-view.md
/docs/architecture/module-boundaries.md
/docs/architecture/adr/0001-use-monorepo.md
/docs/architecture/adr/0002-use-nextjs-typescript-frontend.md
/docs/architecture/adr/0003-use-aspnet-core-backend.md
/docs/architecture/adr/0004-use-postgresql.md
/docs/architecture/adr/0005-use-redis-for-transient-state.md
/docs/architecture/adr/0006-use-modular-monolith.md
/docs/architecture/adr/0007-use-docker-for-local-development.md
/docs/development/kali-debian-zsh-setup.md
/docs/development/troubleshooting.md
```

---

## Phase 14: Integrated Validation and Sprint Closure

### Objectives

- Execute the complete local environment from a clean checkout.
- Verify frontend, API and worker builds.
- Verify PostgreSQL migrations from an empty database.
- Verify Redis connectivity and failure handling.
- Execute all frontend, backend, worker, architecture and integration tests.
- Verify formatting, linting and strict TypeScript checks.
- Build all production container images.
- Verify no secret is committed or printed in logs.
- Verify protected-branch and pull-request quality gates.
- Update documentation to match the validated implementation.
- Create the verified Sprint 1 Git commit.
- Push the development branch to GitHub.
- Create a pull request only after all required validations pass and no unresolved error remains.
- Stop at the Sprint 1 completion gate before beginning the next sprint.

### Files to create

```text
/scripts/release/sprint-1-final-validation.zsh
/docs/evidence/sprint-1-validation-report.md
/docs/evidence/sprint-1-security-scan-summary.md
/docs/evidence/sprint-1-migration-verification.md
/docs/evidence/sprint-1-container-verification.md
/docs/evidence/sprint-1-completion-record.md
/docs/delivery/sprint-1-pull-request.md
```

---

## Sprint 1 Completion Gate

Sprint 1 is complete only when every condition below passes:

- Frontend application builds successfully.
- ASP.NET Core API builds successfully.
- Background worker builds successfully.
- PostgreSQL starts and the initial migration succeeds against an empty database.
- Redis starts and connectivity checks pass.
- Docker Compose starts the complete local platform successfully.
- Frontend, backend, worker, architecture and integration tests pass.
- Formatting, linting and strict TypeScript validation pass.
- Production container images build successfully.
- Health, readiness and liveness checks return expected results.
- Secret, dependency and container scanning are operational.
- No secret or confidential value exists in source control or validation logs.
- Pull-request quality gates are configured and passing.
- Development documentation matches the verified implementation.
- A verified Sprint 1 Git commit exists.
- The Sprint 1 development branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- No unresolved blocking error remains.
- The next sprint has not started.

## Sprint 1 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_1_COMPLETE
```
