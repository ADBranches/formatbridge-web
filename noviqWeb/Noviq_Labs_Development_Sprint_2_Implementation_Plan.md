# Noviq Labs Full-Stack Platform

## Development Sprint 2: Azure Infrastructure, CI/CD and Observability

**Sprint position:** Second production implementation sprint after the verified Engineering Foundation  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Cloud platform:** Microsoft Azure  
**Architecture:** Modular monolith with independently deployable web, API and worker workloads  
**Approved stack:** Next.js, React, TypeScript, ASP.NET Core, C#, PostgreSQL, Redis, Docker and Microsoft Azure

## Sprint Objective

Establish secure, reproducible and observable Microsoft Azure environments for the complete end-to-end Noviq Labs platform. The sprint will implement infrastructure as code, create development and staging cloud foundations, establish container-image publication, configure continuous delivery, connect secrets and configuration safely, verify telemetry and alerts, and prove that the platform can be deployed and rolled back without manual infrastructure drift.

---

## Phase 1: Sprint Entry and Foundation Verification

### Objectives

- Verify that Development Sprint 1 passed every completion-gate requirement.
- Confirm that the verified Sprint 1 Git commit exists on the approved development branch.
- Confirm that the frontend, API, worker, PostgreSQL, Redis and Docker foundations remain operational.
- Verify that all required pull-request checks pass before cloud implementation begins.
- Inspect the current repository before creating or modifying infrastructure files.
- Confirm the active GitHub repository ownership, remotes and branch-protection model.
- Confirm access to the approved Microsoft Azure tenant and subscription.
- Record cloud-region, environment, naming and ownership decisions.
- Stop the sprint if Sprint 1 evidence is incomplete or the approved cloud account is unavailable.

### Files to create

```text
/docs/evidence/sprint-2-entry-verification.md
/docs/cloud/azure-access-prerequisites.md
/docs/cloud/environment-ownership.md
/docs/cloud/resource-naming-standard.md
/docs/cloud/region-selection.md
```

---

## Phase 2: Azure Infrastructure Repository Structure

### Objectives

- Establish the infrastructure-as-code directory structure.
- Use Bicep as the primary Microsoft Azure infrastructure language.
- Separate reusable modules from environment-specific compositions.
- Keep development, staging and production configuration explicit.
- Prevent credentials, deployment outputs and local parameter overrides from entering source control.
- Establish consistent tags for environment, application, owner, cost center and data classification.
- Define deterministic resource naming without embedding secrets or personal identifiers.

### Files to create

```text
/infrastructure/azure/README.md
/infrastructure/azure/main.bicep
/infrastructure/azure/main.bicepparam
/infrastructure/azure/modules/resource-group.bicep
/infrastructure/azure/modules/log-analytics.bicep
/infrastructure/azure/modules/application-insights.bicep
/infrastructure/azure/modules/container-registry.bicep
/infrastructure/azure/modules/container-apps-environment.bicep
/infrastructure/azure/modules/container-app.bicep
/infrastructure/azure/modules/postgresql-flexible-server.bicep
/infrastructure/azure/modules/redis-cache.bicep
/infrastructure/azure/modules/storage-account.bicep
/infrastructure/azure/modules/key-vault.bicep
/infrastructure/azure/modules/managed-identity.bicep
/infrastructure/azure/modules/monitoring-alerts.bicep
/infrastructure/azure/environments/development.bicepparam
/infrastructure/azure/environments/staging.bicepparam
/infrastructure/azure/environments/production.bicepparam
/infrastructure/azure/config/tags.json
/infrastructure/azure/config/naming.json
/infrastructure/azure/.gitignore
```

---

## Phase 3: Identity, Access and Deployment Principals

### Objectives

- Configure workload identity federation between GitHub Actions and Microsoft Azure.
- Avoid long-lived Azure client secrets in GitHub.
- Create separate deployment identities for development, staging and production.
- Apply least-privilege role assignments to deployment identities.
- Separate infrastructure deployment permissions from application runtime permissions.
- Create managed identities for the web, API and worker workloads.
- Define human administrator access separately from automated deployment access.
- Document privilege activation, approval and revocation procedures.
- Ensure production deployment permissions are not granted to untrusted branches or pull requests.

### Files to create

```text
/infrastructure/azure/modules/federated-identity.bicep
/infrastructure/azure/modules/role-assignments.bicep
/infrastructure/azure/modules/runtime-identities.bicep
/infrastructure/azure/environments/development.identity.bicepparam
/infrastructure/azure/environments/staging.identity.bicepparam
/infrastructure/azure/environments/production.identity.bicepparam
/docs/security/azure-identity-and-access.md
/docs/security/github-azure-workload-identity.md
/docs/security/production-privilege-activation.md
/docs/security/cloud-role-matrix.md
```

---

## Phase 4: Azure Container Registry

### Objectives

- Provision Azure Container Registry for trusted application images.
- Disable anonymous pull access.
- Use managed identity for image pulls by Azure Container Apps.
- Establish repositories for the web, API and worker images.
- Define immutable image-tagging conventions based on verified Git commits.
- Prohibit the use of mutable `latest` tags for production releases.
- Configure retention and cleanup rules for unreferenced development images.
- Enable container-image scanning through the approved security workflow.
- Verify authenticated push and pull operations from trusted pipelines.

### Files to create

```text
/infrastructure/azure/modules/container-registry-repositories.bicep
/infrastructure/azure/config/container-image-policy.json
/docs/delivery/container-registry.md
/docs/delivery/container-image-tagging.md
/docs/security/container-image-governance.md
/scripts/cloud/verify-container-registry.zsh
```

---

## Phase 5: Azure Container Apps Environment

### Objectives

- Provision the Azure Container Apps environment for development and staging.
- Deploy the Next.js web application as an independently scalable container app.
- Deploy the ASP.NET Core API as an independently scalable container app.
- Deploy the background worker as an independently scalable container app.
- Configure internal and external ingress boundaries deliberately.
- Keep the API private where the selected frontend integration permits it.
- Configure workload profiles, resource limits and initial scaling rules.
- Configure revision management and controlled traffic shifting.
- Establish health probes using the verified Sprint 1 health endpoints.
- Verify that failed revisions do not receive production traffic.

### Files to create

```text
/infrastructure/azure/modules/web-container-app.bicep
/infrastructure/azure/modules/api-container-app.bicep
/infrastructure/azure/modules/worker-container-app.bicep
/infrastructure/azure/modules/container-app-ingress.bicep
/infrastructure/azure/modules/container-app-scaling.bicep
/infrastructure/azure/config/web-scaling.json
/infrastructure/azure/config/api-scaling.json
/infrastructure/azure/config/worker-scaling.json
/docs/cloud/container-apps-architecture.md
/docs/cloud/container-app-revision-strategy.md
/scripts/cloud/verify-container-apps.zsh
```

---

## Phase 6: Azure Database for PostgreSQL

### Objectives

- Provision Azure Database for PostgreSQL Flexible Server for development and staging.
- Define environment-specific compute, storage, backup and availability settings.
- Require encrypted connections.
- Restrict network access to approved workloads and administrators.
- Store database credentials and connection information outside source control.
- Configure migration execution as a controlled deployment step.
- Prevent simultaneous or uncontrolled migration execution by multiple application replicas.
- Configure backup retention suitable for each environment.
- Verify connectivity from the API and migration process.
- Verify that the initial migration can be applied to an empty Azure database.

### Files to create

```text
/infrastructure/azure/modules/postgresql-networking.bicep
/infrastructure/azure/modules/postgresql-configuration.bicep
/infrastructure/azure/modules/postgresql-database.bicep
/infrastructure/azure/config/postgresql-development.json
/infrastructure/azure/config/postgresql-staging.json
/infrastructure/azure/config/postgresql-production.json
/apps/api/NoviqLabs.Infrastructure/Persistence/MigrationRunner.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/MigrationOptions.cs
/scripts/cloud/run-azure-migrations.zsh
/scripts/cloud/verify-postgresql.zsh
/docs/database/azure-postgresql.md
/docs/database/cloud-migration-procedure.md
/docs/database/backup-retention.md
```

---

## Phase 7: Azure Managed Redis

### Objectives

- Provision the approved Azure-managed Redis service for development and staging.
- Require encrypted connections.
- Restrict network access to approved workloads.
- Configure environment-specific capacity and expiry policies.
- Store connection details securely.
- Verify cache connectivity from the API.
- Verify that Redis failure does not corrupt durable business data.
- Confirm that cache state can be recreated from authoritative sources.
- Add telemetry for connection failures, latency and resource pressure.

### Files to create

```text
/infrastructure/azure/modules/redis-networking.bicep
/infrastructure/azure/modules/redis-configuration.bicep
/infrastructure/azure/config/redis-development.json
/infrastructure/azure/config/redis-staging.json
/infrastructure/azure/config/redis-production.json
/scripts/cloud/verify-redis.zsh
/docs/cloud/azure-redis.md
/docs/operations/redis-degraded-mode.md
```

---

## Phase 8: Azure Blob Storage Foundation

### Objectives

- Provision Azure Blob Storage for public assets, operational files and future customer uploads.
- Create separate containers according to data purpose and classification.
- Disable public access by default.
- Permit public delivery only for explicitly approved brand or website assets.
- Use managed identities and short-lived access mechanisms.
- Configure encryption, retention and lifecycle rules.
- Prepare quarantine and approved-file containers for future malware-scanning workflows.
- Enable appropriate logging and diagnostic settings.
- Verify controlled upload, read and deletion operations.

### Files to create

```text
/infrastructure/azure/modules/storage-containers.bicep
/infrastructure/azure/modules/storage-lifecycle.bicep
/infrastructure/azure/modules/storage-networking.bicep
/infrastructure/azure/config/storage-containers.json
/infrastructure/azure/config/storage-lifecycle.json
/apps/api/NoviqLabs.Infrastructure/Storage/BlobStorageOptions.cs
/apps/api/NoviqLabs.Infrastructure/Storage/BlobStorageClientFactory.cs
/apps/api/NoviqLabs.Infrastructure/Health/BlobStorageHealthCheck.cs
/scripts/cloud/verify-blob-storage.zsh
/docs/storage/blob-storage-boundaries.md
/docs/storage/blob-retention-and-lifecycle.md
```

---

## Phase 9: Azure Key Vault and Secure Configuration

### Objectives

- Provision separate Key Vaults for development, staging and production.
- Use Azure role-based access control instead of legacy access policies.
- Grant workloads access only to the secrets each workload requires.
- Configure soft delete and purge protection.
- Store database, Redis, storage and external-service secrets securely.
- Keep non-secret configuration separate from secrets.
- Load secrets through managed identity at runtime.
- Prevent secrets from entering application settings, pipeline logs or deployment outputs.
- Establish secret naming, rotation and revocation procedures.
- Verify that the application fails safely when a required secret is unavailable.

### Files to create

```text
/infrastructure/azure/modules/key-vault-secrets.bicep
/infrastructure/azure/modules/key-vault-role-assignments.bicep
/infrastructure/azure/config/key-vault-secret-names.json
/apps/api/NoviqLabs.Infrastructure/Configuration/KeyVaultConfiguration.cs
/apps/worker/NoviqLabs.Worker/Configuration/KeyVaultConfiguration.cs
/apps/web/src/lib/server/azure-config.ts
/scripts/cloud/verify-key-vault.zsh
/docs/security/key-vault.md
/docs/security/secret-rotation.md
/docs/security/secret-revocation.md
```

---

## Phase 10: Azure Monitor, Application Insights and Diagnostics

### Objectives

- Provision Log Analytics and Application Insights.
- Connect the web, API and worker workloads to centralized telemetry.
- Propagate correlation identifiers across frontend, API and worker activity.
- Capture structured logs, metrics, traces, dependencies and exceptions.
- Exclude passwords, access tokens, connection strings and sensitive customer data from telemetry.
- Configure environment and application dimensions consistently.
- Add dashboards for availability, failed requests, latency, dependency health and resource pressure.
- Configure data-retention settings appropriate to each environment.
- Verify that a test request can be traced across the deployed platform.

### Files to create

```text
/infrastructure/azure/modules/diagnostic-settings.bicep
/infrastructure/azure/modules/application-insights-workbook.bicep
/infrastructure/azure/config/telemetry-retention.json
/infrastructure/azure/workbooks/platform-overview.workbook.json
/apps/api/NoviqLabs.Infrastructure/Observability/ApplicationInsightsConfiguration.cs
/apps/worker/NoviqLabs.Worker/Observability/ApplicationInsightsConfiguration.cs
/apps/web/src/lib/observability/application-insights.ts
/scripts/cloud/verify-telemetry.zsh
/docs/operations/azure-observability.md
/docs/operations/telemetry-data-policy.md
```

---

## Phase 11: Monitoring, Alerts and Operational Ownership

### Objectives

- Configure alerts for platform availability, container restarts, failed requests, latency and dependency failures.
- Configure PostgreSQL, Redis, storage and Key Vault health alerts.
- Configure budget and cost anomaly notifications.
- Assign an accountable owner and response route for every alert.
- Prevent alerts from exposing sensitive information.
- Define severity levels, acknowledgement expectations and escalation paths.
- Create an initial staging availability dashboard.
- Test representative alerts without disrupting unrelated resources.

### Files to create

```text
/infrastructure/azure/modules/action-groups.bicep
/infrastructure/azure/modules/platform-alerts.bicep
/infrastructure/azure/modules/database-alerts.bicep
/infrastructure/azure/modules/cache-alerts.bicep
/infrastructure/azure/modules/storage-alerts.bicep
/infrastructure/azure/modules/security-alerts.bicep
/infrastructure/azure/config/alert-thresholds.json
/infrastructure/azure/config/budget-alerts.json
/docs/operations/alert-catalogue.md
/docs/operations/alert-severity-and-escalation.md
/docs/operations/operational-ownership.md
/scripts/cloud/test-alerts.zsh
```

---

## Phase 12: GitHub Actions Build and Image Publication

### Objectives

- Extend the verified Sprint 1 continuous-integration workflows into trusted image-publication workflows.
- Build reproducible production images for the web, API and worker.
- Tag images with the full verified Git commit identifier.
- Generate image metadata suitable for audit and rollback.
- Authenticate to Azure through workload identity federation.
- Push images only from trusted branches after required validation passes.
- Prevent forked or untrusted pull requests from accessing Azure credentials.
- Preserve complete build and scan logs.
- Fail publication when build, test or security gates fail.

### Files to create

```text
/.github/workflows/build-web-image.yml
/.github/workflows/build-api-image.yml
/.github/workflows/build-worker-image.yml
/.github/workflows/publish-container-images.yml
/.github/actions/setup-build-context/action.yml
/.github/actions/generate-image-tags/action.yml
/.github/actions/azure-login/action.yml
/scripts/ci/generate-image-metadata.zsh
/scripts/ci/verify-image-tags.zsh
/docs/delivery/image-publication-pipeline.md
```

---

## Phase 13: Infrastructure Validation Pipeline

### Objectives

- Validate Bicep syntax and module references on every relevant pull request.
- Run linting and static validation for infrastructure files.
- Generate Azure deployment previews for trusted branches.
- Detect destructive or unexpected infrastructure changes before deployment.
- Prevent production changes from being applied automatically from ordinary pull requests.
- Preserve deployment preview output as review evidence.
- Verify environment parameter completeness.
- Fail the pipeline when required infrastructure outputs are missing.

### Files to create

```text
/.github/workflows/validate-infrastructure.yml
/.github/workflows/preview-azure-changes.yml
/.github/actions/setup-azure-cli/action.yml
/scripts/ci/validate-bicep.zsh
/scripts/ci/validate-azure-parameters.zsh
/scripts/ci/preview-azure-deployment.zsh
/scripts/ci/check-destructive-changes.zsh
/docs/delivery/infrastructure-validation.md
/docs/delivery/infrastructure-change-review.md
```

---

## Phase 14: Development Environment Deployment

### Objectives

- Deploy the approved Microsoft Azure development environment from infrastructure as code.
- Publish verified web, API and worker images.
- Configure development workload identities and Key Vault access.
- Apply the initial PostgreSQL migration through the controlled migration process.
- Verify PostgreSQL, Redis and Blob Storage connectivity.
- Verify liveness and readiness checks.
- Verify centralized telemetry and diagnostics.
- Execute automated smoke tests against the deployed development environment.
- Record every deployed resource and output needed by later phases.

### Files to create

```text
/.github/workflows/deploy-development.yml
/scripts/cloud/deploy-development.zsh
/scripts/cloud/smoke-test-development.zsh
/scripts/cloud/verify-development-environment.zsh
/tests/deployment/development-smoke-tests.json
/docs/environments/development.md
/docs/evidence/sprint-2-development-deployment.md
```

---

## Phase 15: Staging Environment Deployment

### Objectives

- Deploy the approved Microsoft Azure staging environment from infrastructure as code.
- Keep staging configuration isolated from development.
- Publish only verified commit-tagged images.
- Apply database migrations through the controlled deployment workflow.
- Verify runtime secrets, identities, network paths and health probes.
- Verify the web, API and worker workloads operate together.
- Verify telemetry, alerts and diagnostic settings.
- Execute staging smoke and integration tests.
- Confirm that staging is suitable for later public website and feature validation.

### Files to create

```text
/.github/workflows/deploy-staging.yml
/scripts/cloud/deploy-staging.zsh
/scripts/cloud/smoke-test-staging.zsh
/scripts/cloud/verify-staging-environment.zsh
/tests/deployment/staging-smoke-tests.json
/docs/environments/staging.md
/docs/evidence/sprint-2-staging-deployment.md
```

---

## Phase 16: Database Migration Deployment Control

### Objectives

- Establish one controlled migration job for each deployment.
- Prevent application replicas from applying migrations concurrently at startup.
- Require migration validation before workload promotion.
- Stop deployment when migration execution fails.
- Preserve migration output as deployment evidence.
- Define forward-fix and rollback boundaries for schema changes.
- Verify migration application against development and staging databases.
- Verify that a newly provisioned empty database can reach the expected schema state.

### Files to create

```text
/.github/workflows/run-database-migrations.yml
/infrastructure/azure/modules/migration-job.bicep
/apps/api/NoviqLabs.Migrator/NoviqLabs.Migrator.csproj
/apps/api/NoviqLabs.Migrator/Program.cs
/apps/api/NoviqLabs.Migrator/appsettings.json
/apps/api/NoviqLabs.Migrator/Dockerfile
/apps/api/NoviqLabs.Migrator/.dockerignore
/tests/api/NoviqLabs.Migrator.IntegrationTests/NoviqLabs.Migrator.IntegrationTests.csproj
/tests/api/NoviqLabs.Migrator.IntegrationTests/MigrationExecutionTests.cs
/scripts/cloud/verify-migration-job.zsh
/docs/database/deployment-migration-control.md
```

---

## Phase 17: Revision Promotion and Rollback

### Objectives

- Establish controlled promotion of verified container revisions.
- Keep the previously healthy revision available during deployment verification.
- Shift traffic only after health and smoke checks pass.
- Roll back traffic automatically or manually when verification fails.
- Ensure rollback does not silently reverse incompatible database changes.
- Record the deployed commit, image digest, revision and migration state.
- Verify rollback for the web and API workloads.
- Verify worker rollback without duplicate job execution.

### Files to create

```text
/.github/workflows/promote-container-revisions.yml
/.github/workflows/rollback-container-revisions.yml
/scripts/cloud/promote-revision.zsh
/scripts/cloud/rollback-revision.zsh
/scripts/cloud/verify-revision-health.zsh
/docs/delivery/revision-promotion.md
/docs/delivery/rollback-procedure.md
/docs/delivery/database-and-application-rollback-boundaries.md
/docs/evidence/sprint-2-rollback-verification.md
```

---

## Phase 18: Cloud Security Baseline

### Objectives

- Verify that public access exists only where explicitly required.
- Verify that managed identities replace embedded credentials.
- Verify Key Vault soft delete, purge protection and role assignments.
- Verify encrypted connections to PostgreSQL and Redis.
- Verify storage-account public-access restrictions.
- Verify that container images are pulled only from the approved registry.
- Verify that logs and deployment outputs contain no secrets.
- Run infrastructure and container security scans.
- Record accepted risks and remediation actions.
- Stop the sprint if any critical or high-risk cloud finding remains unresolved.

### Files to create

```text
/.github/workflows/cloud-security-scan.yml
/scripts/security/scan-bicep.zsh
/scripts/security/scan-azure-resources.zsh
/scripts/security/scan-published-images.zsh
/scripts/security/verify-no-public-exposure.zsh
/docs/security/azure-security-baseline.md
/docs/security/cloud-network-boundaries.md
/docs/security/cloud-risk-register.md
/docs/evidence/sprint-2-cloud-security-scan.md
```

---

## Phase 19: Cost, Resource and Retention Governance

### Objectives

- Establish initial Azure budgets and cost alerts.
- Apply environment-appropriate resource sizes.
- Prevent development and staging resources from scaling without defined limits.
- Define image, log, backup and storage retention.
- Identify resources that may be stopped or scaled down outside working hours.
- Document cost ownership and review frequency.
- Verify that all resources carry approved tags.
- Prevent production economy measures from weakening required security or resilience controls.

### Files to create

```text
/infrastructure/azure/modules/budget.bicep
/infrastructure/azure/modules/resource-locks.bicep
/infrastructure/azure/config/resource-sizes.json
/infrastructure/azure/config/retention-policy.json
/scripts/cloud/verify-resource-tags.zsh
/scripts/cloud/report-environment-costs.zsh
/docs/cloud/cost-governance.md
/docs/cloud/resource-sizing.md
/docs/cloud/retention-governance.md
```

---

## Phase 20: Documentation and Operational Runbooks

### Objectives

- Document the deployed Azure architecture.
- Document environment differences and promotion boundaries.
- Document infrastructure deployment, application deployment and migration procedures.
- Document rollback, secret rotation, alert handling and degraded-dependency behavior.
- Document GitHub Actions and Azure workload identity troubleshooting.
- Keep runbooks executable from Kali Debian with Zsh-compatible commands.
- Ensure documentation matches the deployed and verified environment.

### Files to create

```text
/docs/architecture/azure-container-view.md
/docs/architecture/azure-deployment-view.md
/docs/architecture/adr/0008-use-microsoft-azure.md
/docs/architecture/adr/0009-use-azure-container-apps.md
/docs/architecture/adr/0010-use-bicep-infrastructure-as-code.md
/docs/architecture/adr/0011-use-github-workload-identity.md
/docs/architecture/adr/0012-use-controlled-migration-jobs.md
/docs/operations/azure-deployment-runbook.md
/docs/operations/azure-rollback-runbook.md
/docs/operations/azure-incident-triage.md
/docs/operations/azure-service-degradation.md
/docs/development/azure-cli-kali-debian-zsh.md
/docs/development/azure-troubleshooting.md
```

---

## Phase 21: Integrated Validation and Sprint Closure

### Objectives

- Validate all Bicep modules and environment parameter files.
- Recreate the development environment from infrastructure as code.
- Verify the staging environment from a clean deployment path.
- Build and publish commit-tagged web, API, worker and migrator images.
- Apply migrations through the controlled migration job.
- Verify application, database, Redis, storage and Key Vault connectivity.
- Verify liveness, readiness, telemetry, alerts and operational dashboards.
- Execute development and staging smoke tests.
- Execute cloud and container security scans.
- Verify image and application revision rollback.
- Verify no secret appears in source control, workflow logs or deployment outputs.
- Update documentation to match verified implementation.
- Create the verified Development Sprint 2 Git commit.
- Push the development branch to GitHub.
- Create a pull request only after every required validation passes.
- Stop at the Development Sprint 2 completion gate before beginning the next sprint.

### Files to create

```text
/scripts/release/sprint-2-final-validation.zsh
/docs/evidence/sprint-2-infrastructure-validation.md
/docs/evidence/sprint-2-image-publication-verification.md
/docs/evidence/sprint-2-migration-verification.md
/docs/evidence/sprint-2-observability-verification.md
/docs/evidence/sprint-2-alert-verification.md
/docs/evidence/sprint-2-rollback-verification.md
/docs/evidence/sprint-2-security-summary.md
/docs/evidence/sprint-2-completion-record.md
/docs/delivery/sprint-2-pull-request.md
```

---

## Development Sprint 2 Completion Gate

Development Sprint 2 is complete only when every condition below passes:

- Development infrastructure deploys reproducibly from Bicep.
- Staging infrastructure deploys reproducibly from Bicep.
- Azure Container Registry accepts only authenticated image publication and pull operations.
- Web, API, worker and migrator images are tagged with verified Git commit identifiers.
- Next.js web, ASP.NET Core API and background worker revisions deploy successfully.
- PostgreSQL is reachable through the approved secure path.
- The initial database migration succeeds through the controlled migration job.
- Redis is reachable through the approved secure path.
- Azure Blob Storage access respects the approved container boundaries.
- Azure Key Vault supplies runtime secrets through managed identities.
- GitHub Actions authenticates to Microsoft Azure through workload identity federation.
- CI/CD pipelines fail when build, test, migration or security checks fail.
- Development and staging smoke tests pass.
- Health, readiness and liveness probes pass.
- Logs, metrics, traces and dependency telemetry reach the approved Azure monitoring resources.
- Required alerts are active and tested.
- Resource tags, budgets and retention policies are applied.
- Revision promotion works.
- Web, API and worker rollback procedures are verified.
- No secret exists in source control, images, workflow logs or deployment outputs.
- No unresolved critical or high-risk cloud or container security finding remains.
- Operational documentation matches the verified deployment.
- A verified Development Sprint 2 Git commit exists.
- The Development Sprint 2 development branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- No unresolved blocking error remains.
- The next sprint has not started.

## Development Sprint 2 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_2_COMPLETE
```
