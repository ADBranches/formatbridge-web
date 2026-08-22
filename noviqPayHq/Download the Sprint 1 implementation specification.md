# Noviq Pay Enterprise Platform Runway Implementation Specification

**Organization:** Noviq Labs Ltd.  
**Product:** Noviq Pay  
**Delivery increment:** Enterprise Platform Runway  
**Planned active delivery window:** 10 working days  
**Status:** Implementation-ready specification, subject to external dependency and approval gates  
**Primary objective:** Deliver a secure, reproducible Noviq Pay staging environment through automated delivery, with authorized workforce access, application health and version visibility, centralized observability, managed PostgreSQL persistence, controlled secrets, backup evidence, and deployment rollback protection.

---

## 1. Implementation-Agent Operating Instructions

The implementation agent must treat this document as the controlling specification for the Enterprise Platform Runway increment.

Before modifying any file, the agent must:

1. Inspect the live project directory and current repository state.
2. Confirm whether any named file or equivalent implementation already exists.
3. Compare the live structure against the directory plan in this specification.
4. Report conflicts, stale assumptions, duplicate implementations, or incompatible tooling.
5. Stop before installing dependencies, changing lockfiles, applying infrastructure, staging, committing, pushing, opening a pull request, or deploying unless explicit approval has been provided.

The agent must not introduce merchant, customer, payment, ledger, settlement, reconciliation, provider, or other financial-domain data in this increment.

---

## 2. Approved Technology Direction

Use the following approved direction unless live repository inspection shows an already approved equivalent:

- **Architecture:** Domain-driven modular monolith with explicit module boundaries.
- **Backend:** Kotlin, Spring Boot, current approved Java LTS, Gradle Kotlin DSL.
- **Frontend shell:** TypeScript, React, Next.js.
- **Database:** Managed PostgreSQL.
- **Database access foundation:** jOOQ-ready configuration, without financial schemas.
- **Migrations:** Flyway.
- **Observability:** OpenTelemetry, Prometheus, Grafana, Loki, Tempo.
- **Containers:** OCI-compatible images.
- **Primary cloud:** AWS, subject to formal account and architecture approval.
- **Infrastructure as code:** Terraform.
- **Kubernetes packaging:** Helm.
- **Staging orchestration:** Managed Kubernetes, preferably Amazon EKS when AWS is approved.
- **GitOps delivery:** Argo CD where the approved staging environment supports it.
- **Identity:** Microsoft Entra ID for workforce authentication.
- **Secrets:** Cloud secret manager, preferably AWS Secrets Manager when AWS is approved.
- **Key management:** Cloud KMS, preferably AWS KMS when AWS is approved.
- **Static analysis:** Semgrep and SonarQube or the approved available equivalent.
- **Dependency analysis:** Snyk, GitHub Advanced Security, or approved equivalent.
- **Secret detection:** Gitleaks.
- **Container scanning:** Trivy.
- **SBOM:** Syft.
- **Artifact signing:** Cosign.

Technology installation, provider provisioning, and lockfile changes remain approval-gated.

---

## 3. Working Increment

At completion:

- A tested Noviq Pay backend and web shell are deployed to staging through an automated pipeline.
- Authorized workforce users authenticate through approved identity controls.
- Authorized operators can view the deployed version, health status, logs, metrics, and traces.
- PostgreSQL is privately reachable from approved workloads only.
- Infrastructure is reproducible from version-controlled definitions.
- Secrets are supplied at runtime through managed secret storage.
- A failed deployment is blocked or rolled back without replacing the last healthy release.
- Backup creation is proven and a restoration test is documented.
- Build, approval, deployment, and rollback evidence is traceable.

---

## 4. Delivery Boundaries

### Included

- Project and repository foundation
- Architecture decision records
- Cloud landing-zone definitions
- Workforce identity integration
- Backend application skeleton
- Operations web shell
- PostgreSQL persistence runway
- Infrastructure as code
- CI validation pipeline
- Staging delivery pipeline
- Container image production and scanning
- Artifact registry integration
- OpenTelemetry instrumentation
- Centralized logs, metrics, traces, dashboards, and alerts
- Secrets and key-management baseline
- Service identities and audit logging
- Backup and restoration evidence
- Deployment and rollback runbooks
- Initial threat model, asset inventory, data classification, and control mapping

### Excluded

- Merchant registration or tenant data
- KYB documents
- API keys for merchants
- Payment intents
- Mobile-money provider integrations
- Ledger accounts or journals
- Webhooks for merchant systems
- Refunds, settlement, reconciliation, or risk rules
- Production deployment
- Live partner credentials
- Real customer or merchant data

---

## 5. Target Project Structure

The implementation agent must verify this structure against the live repository before creating files.

```text
noviq-pay/
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
├── CODEOWNERS
├── .editorconfig
├── .gitignore
├── .gitattributes
├── .env.example
├── settings.gradle.kts
├── build.gradle.kts
├── gradle.properties
├── gradle/
│   └── libs.versions.toml
├── apps/
│   ├── platform-api/
│   │   ├── build.gradle.kts
│   │   └── src/
│   │       ├── main/
│   │       │   ├── kotlin/com/noviqlabs/pay/platform/
│   │       │   │   ├── NoviqPayApplication.kt
│   │       │   │   ├── configuration/
│   │       │   │   │   ├── ApplicationProperties.kt
│   │       │   │   │   ├── CorrelationIdFilter.kt
│   │       │   │   │   ├── ObservabilityConfiguration.kt
│   │       │   │   │   └── SecurityConfiguration.kt
│   │       │   │   └── system/
│   │       │   │       ├── HealthController.kt
│   │       │   │       ├── VersionController.kt
│   │       │   │       └── VersionResponse.kt
│   │       │   └── resources/
│   │       │       ├── application.yml
│   │       │       ├── application-local.yml
│   │       │       ├── application-staging.yml
│   │       │       └── db/migration/V001__platform_runway.sql
│   │       └── test/
│   │           └── kotlin/com/noviqlabs/pay/platform/
│   │               ├── ArchitectureTest.kt
│   │               ├── ApplicationContextTest.kt
│   │               ├── CorrelationIdFilterTest.kt
│   │               ├── HealthControllerTest.kt
│   │               └── VersionControllerTest.kt
│   └── operations-web/
│       ├── package.json
│       ├── package-lock.json
│       ├── next.config.ts
│       ├── tsconfig.json
│       ├── eslint.config.mjs
│       ├── vitest.config.ts
│       ├── playwright.config.ts
│       ├── middleware.ts
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx
│       │   ├── health/page.tsx
│       │   ├── observability/page.tsx
│       │   └── unauthorized/page.tsx
│       ├── components/
│       │   ├── AuthenticationBoundary.tsx
│       │   ├── ServiceHealthCard.tsx
│       │   ├── SystemVersionCard.tsx
│       │   └── TelemetryLinks.tsx
│       ├── lib/
│       │   ├── auth.ts
│       │   ├── configuration.ts
│       │   ├── platform-api.ts
│       │   └── correlation-id.ts
│       └── tests/
│           ├── health-page.test.tsx
│           ├── authentication-boundary.test.tsx
│           └── platform-runway.spec.ts
├── contracts/
│   └── openapi/
│       └── platform-system-api.yaml
├── infrastructure/
│   ├── terraform/
│   │   ├── versions.tf
│   │   ├── providers.tf
│   │   ├── backend.tf.example
│   │   ├── modules/
│   │   │   ├── landing-zone/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── network/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── database/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── kubernetes/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── observability/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── security/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   └── dns/
│   │   │       ├── main.tf
│   │   │       ├── variables.tf
│   │   │       └── outputs.tf
│   │   └── environments/
│   │       ├── development/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── terraform.tfvars.example
│   │       └── staging/
│   │           ├── main.tf
│   │           ├── variables.tf
│   │           └── terraform.tfvars.example
│   ├── helm/noviq-pay/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   ├── values-staging.yaml
│   │   └── templates/
│   │       ├── platform-api-deployment.yaml
│   │       ├── platform-api-service.yaml
│   │       ├── operations-web-deployment.yaml
│   │       ├── operations-web-service.yaml
│   │       ├── ingress.yaml
│   │       ├── service-account.yaml
│   │       ├── network-policy.yaml
│   │       ├── pod-disruption-budget.yaml
│   │       └── servicemonitor.yaml
│   ├── argocd/
│   │   └── staging-application.yaml
│   └── policies/
│       ├── terraform.rego
│       ├── kubernetes.rego
│       └── container.rego
├── observability/
│   ├── otel/collector-config.yaml
│   ├── prometheus/alerts/platform-runway.yaml
│   ├── grafana/dashboards/platform-overview.json
│   ├── grafana/provisioning/dashboards.yaml
│   ├── grafana/provisioning/datasources.yaml
│   ├── loki/loki-config.yaml
│   └── tempo/tempo-config.yaml
├── containers/
│   ├── platform-api.Dockerfile
│   └── operations-web.Dockerfile
├── scripts/
│   ├── verify-toolchain.sh
│   ├── validate-configuration.sh
│   ├── validate-migrations.sh
│   ├── validate-terraform.sh
│   ├── validate-helm.sh
│   ├── scan-secrets.sh
│   ├── scan-dependencies.sh
│   ├── scan-containers.sh
│   ├── generate-sbom.sh
│   ├── smoke-test-staging.sh
│   ├── verify-backup.sh
│   └── verify-rollback.sh
├── .github/
│   ├── dependabot.yml
│   ├── pull_request_template.md
│   └── workflows/
│       ├── pull-request-validation.yml
│       ├── build-and-publish.yml
│       ├── deploy-staging.yml
│       ├── infrastructure-plan.yml
│       ├── infrastructure-apply.yml
│       └── security-scan.yml
└── docs/
    ├── architecture/
    │   ├── system-context.md
    │   ├── container-view.md
    │   ├── module-boundaries.md
    │   └── decisions/
    │       ├── ADR-001-primary-cloud.md
    │       ├── ADR-002-application-runtime.md
    │       ├── ADR-003-managed-postgresql.md
    │       ├── ADR-004-deployment-model.md
    │       ├── ADR-005-observability-stack.md
    │       └── ADR-006-workforce-identity.md
    ├── security/
    │   ├── initial-threat-model.md
    │   ├── asset-inventory.md
    │   ├── data-classification.md
    │   ├── access-control-baseline.md
    │   ├── secrets-management-standard.md
    │   └── control-mapping.md
    ├── operations/
    │   ├── deployment-runbook.md
    │   ├── rollback-runbook.md
    │   ├── alert-triage-runbook.md
    │   ├── database-backup-runbook.md
    │   ├── database-restoration-runbook.md
    │   └── access-review-runbook.md
    ├── testing/
    │   ├── platform-runway-test-plan.md
    │   ├── restoration-test-record.md
    │   └── rollback-test-record.md
    └── releases/
        ├── release-evidence-template.md
        └── platform-runway-release-notes.md
```

---

## 6. Ten-Working-Day Timeline

### Phase 1: Architecture and Repository Foundation

**Timeline:** Working day 1  
**Unique objective:** Establish one reproducible repository structure, freeze the platform-runway boundaries, and record the architecture decisions required before cloud or application implementation.

**Directories:**

```text
/
/apps/
/contracts/
/infrastructure/
/observability/
/containers/
/scripts/
/docs/architecture/
/docs/architecture/decisions/
/docs/security/
/docs/operations/
/docs/testing/
/docs/releases/
/.github/workflows/
```

**Files:**

```text
/README.md
/SECURITY.md
/CONTRIBUTING.md
/CODEOWNERS
/.editorconfig
/.gitignore
/.gitattributes
/.env.example
/settings.gradle.kts
/build.gradle.kts
/gradle.properties
/gradle/libs.versions.toml
/docs/architecture/system-context.md
/docs/architecture/container-view.md
/docs/architecture/module-boundaries.md
/docs/architecture/decisions/ADR-001-primary-cloud.md
/docs/architecture/decisions/ADR-002-application-runtime.md
/docs/architecture/decisions/ADR-003-managed-postgresql.md
/docs/architecture/decisions/ADR-004-deployment-model.md
/docs/architecture/decisions/ADR-005-observability-stack.md
/docs/architecture/decisions/ADR-006-workforce-identity.md
```

**Implementation actions:**

1. Confirm the project root and package namespace.
2. Define the Gradle multi-project build.
3. Define repository ownership and review boundaries.
4. Record cloud, runtime, database, delivery, observability, and identity decisions.
5. Document that financial-domain modules are excluded from this increment.
6. Define safe environment-variable names without real values.
7. Define generated-file, build-output, lockfile, and source-map policies.

**Exit evidence:**

- Repository structure reviewed.
- Architecture decisions contain status, context, decision, consequences, alternatives, and approval owner.
- No application or infrastructure implementation begins with unresolved foundational decisions.

---

### Phase 2: Local Toolchain and Modular Application Skeleton

**Timeline:** Working days 1 and 2  
**Unique objective:** Produce a locally buildable backend and operations web shell that expose only non-sensitive system health and version information.

**Directories:**

```text
/apps/platform-api/
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/
/apps/platform-api/src/main/resources/
/apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/
/apps/operations-web/
/apps/operations-web/app/
/apps/operations-web/components/
/apps/operations-web/lib/
/apps/operations-web/tests/
/contracts/openapi/
```

**Files:**

```text
/apps/platform-api/build.gradle.kts
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/NoviqPayApplication.kt
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/ApplicationProperties.kt
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/CorrelationIdFilter.kt
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/ObservabilityConfiguration.kt
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/SecurityConfiguration.kt
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/system/HealthController.kt
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/system/VersionController.kt
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/system/VersionResponse.kt
/apps/platform-api/src/main/resources/application.yml
/apps/platform-api/src/main/resources/application-local.yml
/apps/platform-api/src/main/resources/application-staging.yml
/apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/ArchitectureTest.kt
/apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/ApplicationContextTest.kt
/apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/CorrelationIdFilterTest.kt
/apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/HealthControllerTest.kt
/apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/VersionControllerTest.kt
/apps/operations-web/package.json
/apps/operations-web/package-lock.json
/apps/operations-web/next.config.ts
/apps/operations-web/tsconfig.json
/apps/operations-web/eslint.config.mjs
/apps/operations-web/vitest.config.ts
/apps/operations-web/playwright.config.ts
/apps/operations-web/app/layout.tsx
/apps/operations-web/app/page.tsx
/apps/operations-web/app/health/page.tsx
/apps/operations-web/components/ServiceHealthCard.tsx
/apps/operations-web/components/SystemVersionCard.tsx
/apps/operations-web/lib/configuration.ts
/apps/operations-web/lib/platform-api.ts
/apps/operations-web/lib/correlation-id.ts
/apps/operations-web/tests/health-page.test.tsx
/contracts/openapi/platform-system-api.yaml
/scripts/verify-toolchain.sh
/scripts/validate-configuration.sh
```

**Implementation actions:**

1. Create a Spring Boot application with explicit package boundaries.
2. Add health endpoints through Spring Boot Actuator and a minimal version endpoint.
3. Return build version, commit identifier when supplied, and build timestamp without exposing environment secrets.
4. Generate or propagate a correlation ID for every request.
5. Create a Next.js operations shell consuming the system endpoints.
6. Add unit, context, architecture, and component tests.
7. Publish the system endpoint contract through OpenAPI 3.1.

**Exit evidence:**

- Backend build passes.
- Frontend type-check, lint, unit tests, and production build pass.
- Health and version responses contain no secrets or internal configuration.
- Architecture test rejects unauthorized module coupling.

---

### Phase 3: Cloud Landing Zone and Environment Separation

**Timeline:** Working days 2 and 3  
**Unique objective:** Define a policy-controlled cloud foundation with isolated development and staging environments, private workload boundaries, controlled ingress, private service access, and auditable network configuration.

**Directories:**

```text
/infrastructure/terraform/
/infrastructure/terraform/modules/landing-zone/
/infrastructure/terraform/modules/network/
/infrastructure/terraform/modules/dns/
/infrastructure/terraform/environments/development/
/infrastructure/terraform/environments/staging/
/infrastructure/policies/
```

**Files:**

```text
/infrastructure/terraform/versions.tf
/infrastructure/terraform/providers.tf
/infrastructure/terraform/backend.tf.example
/infrastructure/terraform/modules/landing-zone/main.tf
/infrastructure/terraform/modules/landing-zone/variables.tf
/infrastructure/terraform/modules/landing-zone/outputs.tf
/infrastructure/terraform/modules/network/main.tf
/infrastructure/terraform/modules/network/variables.tf
/infrastructure/terraform/modules/network/outputs.tf
/infrastructure/terraform/modules/dns/main.tf
/infrastructure/terraform/modules/dns/variables.tf
/infrastructure/terraform/modules/dns/outputs.tf
/infrastructure/terraform/environments/development/main.tf
/infrastructure/terraform/environments/development/variables.tf
/infrastructure/terraform/environments/development/terraform.tfvars.example
/infrastructure/terraform/environments/staging/main.tf
/infrastructure/terraform/environments/staging/variables.tf
/infrastructure/terraform/environments/staging/terraform.tfvars.example
/infrastructure/policies/terraform.rego
/scripts/validate-terraform.sh
```

**Implementation actions:**

1. Define separate environment boundaries.
2. Define VPC, public ingress subnets where strictly needed, private application subnets, and isolated database subnets.
3. Deny direct public database exposure.
4. Define controlled egress and private service endpoints.
5. Define DNS zones and staging-domain integration without embedding private domain values.
6. Define remote Terraform state and locking configuration as an example until the approved backend exists.
7. Add formatting, validation, linting, policy, and plan checks.
8. Require human review before infrastructure apply.

**Exit evidence:**

- Terraform formatting and validation pass.
- Policy tests reject public database access, unrestricted administrative ingress, and missing encryption.
- Development and staging definitions remain isolated.
- No infrastructure apply occurs without approval.

---

### Phase 4: Workforce Identity and Privileged Access

**Timeline:** Working days 3 and 4  
**Unique objective:** Restrict the operations web shell and administrative observability access to approved workforce identities with MFA, role groups, privileged elevation, and access evidence.

**Directories:**

```text
/apps/operations-web/app/unauthorized/
/apps/operations-web/components/
/apps/operations-web/lib/
/docs/security/
/docs/operations/
```

**Files:**

```text
/apps/operations-web/middleware.ts
/apps/operations-web/app/unauthorized/page.tsx
/apps/operations-web/components/AuthenticationBoundary.tsx
/apps/operations-web/lib/auth.ts
/apps/operations-web/tests/authentication-boundary.test.tsx
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/SecurityConfiguration.kt
/docs/security/access-control-baseline.md
/docs/operations/access-review-runbook.md
/docs/architecture/decisions/ADR-006-workforce-identity.md
```

**Implementation actions:**

1. Integrate Microsoft Entra ID through standards-based OIDC.
2. Define separate viewer, operator, platform administrator, security reviewer, and auditor groups.
3. Require server-side authorization for protected backend endpoints.
4. Require MFA through identity-provider policy.
5. Define privileged access as time-bound elevation, not permanent assignment.
6. Record successful access, denied access, privilege changes, and administrative actions.
7. Add tests for unauthenticated, unauthorized, expired-session, and permitted access.

**Exit evidence:**

- Unauthenticated access is redirected or denied.
- Authorized roles receive only intended access.
- Privileged roles are not permanently granted by application configuration.
- Access events are visible without storing tokens or sensitive claims.

---

### Phase 5: Managed PostgreSQL and Persistence Runway

**Timeline:** Working days 3 through 5  
**Unique objective:** Provision an encrypted, private PostgreSQL staging foundation with controlled migrations, backup retention, point-in-time recovery configuration, and documented restoration verification.

**Directories:**

```text
/infrastructure/terraform/modules/database/
/apps/platform-api/src/main/resources/db/migration/
/docs/operations/
/docs/testing/
```

**Files:**

```text
/infrastructure/terraform/modules/database/main.tf
/infrastructure/terraform/modules/database/variables.tf
/infrastructure/terraform/modules/database/outputs.tf
/apps/platform-api/src/main/resources/db/migration/V001__platform_runway.sql
/scripts/validate-migrations.sh
/scripts/verify-backup.sh
/docs/operations/database-backup-runbook.md
/docs/operations/database-restoration-runbook.md
/docs/testing/restoration-test-record.md
/docs/architecture/decisions/ADR-003-managed-postgresql.md
```

**Implementation actions:**

1. Define managed PostgreSQL in private subnets.
2. Enforce encryption at rest and in transit.
3. Configure backup retention and point-in-time recovery.
4. Define least-privilege application and migration identities separately.
5. Configure connection limits and managed proxy or PgBouncer where approved.
6. Add Flyway with one non-financial platform migration used only to prove migration delivery.
7. Document backup creation and isolated restoration testing.
8. Verify restoration without introducing merchant or financial data.

**Exit evidence:**

- Database has no public endpoint.
- Flyway migration validation passes.
- Backup creation evidence exists.
- Restoration test records time, target, result, responsible operator, and cleanup.
- Application credentials cannot perform administrative database operations.

---

### Phase 6: Secrets, Key Management, Service Identities, and Audit Baseline

**Timeline:** Working days 4 and 5  
**Unique objective:** Remove static credentials from code and delivery configuration by using managed secrets, managed keys, workload identities, least privilege, and auditable access.

**Directories:**

```text
/infrastructure/terraform/modules/security/
/infrastructure/helm/noviq-pay/templates/
/docs/security/
```

**Files:**

```text
/infrastructure/terraform/modules/security/main.tf
/infrastructure/terraform/modules/security/variables.tf
/infrastructure/terraform/modules/security/outputs.tf
/infrastructure/helm/noviq-pay/templates/service-account.yaml
/docs/security/secrets-management-standard.md
/docs/security/asset-inventory.md
/docs/security/data-classification.md
/scripts/scan-secrets.sh
```

**Implementation actions:**

1. Define managed secret storage and encryption keys.
2. Define service identities for backend, web, deployment, migration, observability, and backup operations.
3. Bind permissions to workloads instead of long-lived access keys.
4. Define secret naming, ownership, rotation, access, and emergency revocation rules.
5. Enable audit trails for secret access, key usage, identity changes, and infrastructure administration.
6. Add Gitleaks scanning and safe fixtures that prove detection without containing real secrets.
7. Ensure `.env.example` contains names and documentation only.

**Exit evidence:**

- Secret scan passes.
- No credential value appears in source, image definitions, pipeline definitions, logs, or documentation.
- Every service identity has an explicit purpose and constrained policy.
- Secret and key access produce auditable events.

---

### Phase 7: Containerization, Kubernetes Runtime, and Staging Packaging

**Timeline:** Working days 5 and 6  
**Unique objective:** Package the backend and operations web shell as non-root, immutable, scan-ready OCI images deployable to a controlled staging Kubernetes environment.

**Directories:**

```text
/containers/
/infrastructure/terraform/modules/kubernetes/
/infrastructure/helm/noviq-pay/
/infrastructure/helm/noviq-pay/templates/
/infrastructure/argocd/
```

**Files:**

```text
/containers/platform-api.Dockerfile
/containers/operations-web.Dockerfile
/infrastructure/terraform/modules/kubernetes/main.tf
/infrastructure/terraform/modules/kubernetes/variables.tf
/infrastructure/terraform/modules/kubernetes/outputs.tf
/infrastructure/helm/noviq-pay/Chart.yaml
/infrastructure/helm/noviq-pay/values.yaml
/infrastructure/helm/noviq-pay/values-staging.yaml
/infrastructure/helm/noviq-pay/templates/platform-api-deployment.yaml
/infrastructure/helm/noviq-pay/templates/platform-api-service.yaml
/infrastructure/helm/noviq-pay/templates/operations-web-deployment.yaml
/infrastructure/helm/noviq-pay/templates/operations-web-service.yaml
/infrastructure/helm/noviq-pay/templates/ingress.yaml
/infrastructure/helm/noviq-pay/templates/network-policy.yaml
/infrastructure/helm/noviq-pay/templates/pod-disruption-budget.yaml
/infrastructure/helm/noviq-pay/templates/servicemonitor.yaml
/infrastructure/argocd/staging-application.yaml
/infrastructure/policies/kubernetes.rego
/infrastructure/policies/container.rego
/scripts/validate-helm.sh
/scripts/scan-containers.sh
/scripts/generate-sbom.sh
```

**Implementation actions:**

1. Build minimal multi-stage images.
2. Run containers as non-root with read-only filesystems where possible.
3. Add health, readiness, and startup probes.
4. Define CPU and memory requests and limits.
5. Define network policy default-deny rules and required communication paths.
6. Define disruption protection and rolling-update behavior.
7. Generate SBOMs and scan images before publication.
8. Sign approved immutable artifacts.
9. Reference released images by digest in staging delivery.

**Exit evidence:**

- Container builds pass.
- Critical scan findings block publication.
- Images contain no source secrets, package-manager cache, test data, or development tools.
- Helm lint and policy validation pass.
- Deployment definitions support safe rolling updates and rollback.

---

### Phase 8: Observability and Operator Visibility

**Timeline:** Working days 5 through 7  
**Unique objective:** Make every staging request and deployment diagnosable through correlated logs, metrics, traces, dashboards, and actionable alerts without exposing private information.

**Directories:**

```text
/observability/otel/
/observability/prometheus/alerts/
/observability/grafana/dashboards/
/observability/grafana/provisioning/
/observability/loki/
/observability/tempo/
/infrastructure/terraform/modules/observability/
/apps/operations-web/app/observability/
```

**Files:**

```text
/observability/otel/collector-config.yaml
/observability/prometheus/alerts/platform-runway.yaml
/observability/grafana/dashboards/platform-overview.json
/observability/grafana/provisioning/dashboards.yaml
/observability/grafana/provisioning/datasources.yaml
/observability/loki/loki-config.yaml
/observability/tempo/tempo-config.yaml
/infrastructure/terraform/modules/observability/main.tf
/infrastructure/terraform/modules/observability/variables.tf
/infrastructure/terraform/modules/observability/outputs.tf
/apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/ObservabilityConfiguration.kt
/apps/operations-web/app/observability/page.tsx
/apps/operations-web/components/TelemetryLinks.tsx
/docs/operations/alert-triage-runbook.md
```

**Implementation actions:**

1. Instrument HTTP requests, database connectivity, application startup, and deployment version.
2. Propagate correlation IDs across web, API, logs, and traces.
3. Emit structured logs with explicit redaction rules.
4. Create health, request-rate, latency, error-rate, saturation, restart, deployment, and database dashboards.
5. Add alerts for service unavailability, elevated errors, failed probes, deployment failure, database connection exhaustion, missing telemetry, and backup failure.
6. Protect observability interfaces with workforce identity and role controls.
7. Link observability views from the operations shell without exposing private endpoints to unauthorized users.

**Exit evidence:**

- A request can be followed from the web shell through the API using one correlation ID.
- Logs contain no tokens, credentials, authorization headers, or sensitive payloads.
- Dashboards show deployed version and service health.
- Every alert names severity, condition, owner, runbook, and recovery expectation.

---

### Phase 9: Pull-Request Validation and Automated Delivery

**Timeline:** Working days 6 through 8  
**Unique objective:** Establish a gated supply chain that validates source, tests, infrastructure, dependencies, secrets, containers, and release metadata before an immutable staging artifact can be deployed.

**Directories:**

```text
/.github/
/.github/workflows/
/scripts/
/docs/releases/
```

**Files:**

```text
/.github/dependabot.yml
/.github/pull_request_template.md
/.github/workflows/pull-request-validation.yml
/.github/workflows/build-and-publish.yml
/.github/workflows/deploy-staging.yml
/.github/workflows/infrastructure-plan.yml
/.github/workflows/infrastructure-apply.yml
/.github/workflows/security-scan.yml
/scripts/scan-dependencies.sh
/scripts/smoke-test-staging.sh
/scripts/verify-rollback.sh
/docs/releases/release-evidence-template.md
/docs/releases/platform-runway-release-notes.md
```

**Implementation actions:**

1. Define required pull-request checks.
2. Build backend and frontend independently, then together.
3. Run unit, component, architecture, contract, migration, infrastructure, policy, secret, dependency, and container checks.
4. Produce immutable version metadata.
5. Generate and retain SBOM, scan reports, test reports, image digest, and signature evidence.
6. Publish only after all required checks pass.
7. Require an approved environment gate before staging deployment.
8. Deploy by immutable image digest.
9. Run post-deployment smoke checks.
10. Automatically halt or roll back when health verification fails.
11. Preserve the last healthy release.

**Exit evidence:**

- Failed required checks prevent merge or deployment.
- No long-lived cloud credential is stored in pipeline variables.
- Every release maps source revision to build, image digest, SBOM, scans, approval, deployment, and rollback evidence.
- Infrastructure apply and staging deployment remain separately approval-gated.

---

### Phase 10: Security, Control, and Operational Documentation

**Timeline:** Working days 7 through 9  
**Unique objective:** Produce the minimum governance and operational evidence required to approve the platform before merchant or financial data is introduced.

**Directories:**

```text
/docs/security/
/docs/operations/
/docs/testing/
/docs/releases/
```

**Files:**

```text
/docs/security/initial-threat-model.md
/docs/security/asset-inventory.md
/docs/security/data-classification.md
/docs/security/access-control-baseline.md
/docs/security/secrets-management-standard.md
/docs/security/control-mapping.md
/docs/operations/deployment-runbook.md
/docs/operations/rollback-runbook.md
/docs/operations/alert-triage-runbook.md
/docs/operations/database-backup-runbook.md
/docs/operations/database-restoration-runbook.md
/docs/operations/access-review-runbook.md
/docs/testing/platform-runway-test-plan.md
/docs/testing/restoration-test-record.md
/docs/testing/rollback-test-record.md
/docs/releases/platform-runway-release-notes.md
```

**Implementation actions:**

1. Model threats for identity, CI/CD, source control, artifact registry, Kubernetes, database, observability, backups, DNS, and administrator access.
2. Inventory assets, owners, classifications, retention, and protections.
3. Classify current platform data as configuration, identity metadata, telemetry, audit, and synthetic test data.
4. Map implemented controls to NIST CSF 2.0 and ISO/IEC 27001:2022 baseline outcomes.
5. Document deployment, rollback, alert triage, backup, restoration, and access-review procedures.
6. Document residual risks and unimplemented controls.
7. Prohibit unsupported certification or compliance claims.

**Exit evidence:**

- Every critical asset has an owner and classification.
- Every identified high-risk threat has a treatment or explicit blocker.
- Runbooks contain triggers, roles, commands or console actions, validation, evidence, escalation, and closure steps.
- Control mapping distinguishes implemented, planned, externally provided, and not applicable controls.

---

### Phase 11: End-to-End Staging Demonstration and Failure Recovery

**Timeline:** Working day 9  
**Unique objective:** Demonstrate the complete approved-change-to-staging workflow and prove that a failed release does not replace the last healthy version.

**Directories:**

```text
/scripts/
/docs/testing/
/docs/releases/
```

**Files:**

```text
/scripts/smoke-test-staging.sh
/scripts/verify-backup.sh
/scripts/verify-rollback.sh
/docs/testing/restoration-test-record.md
/docs/testing/rollback-test-record.md
/docs/releases/platform-runway-release-notes.md
```

**Implementation actions:**

1. Merge or simulate an approved change through the configured gate.
2. Build, test, scan, sign, publish, and deploy the release candidate.
3. Authenticate as an authorized operator.
4. View deployed version, health, logs, metrics, and a correlated trace.
5. Introduce a controlled deployment failure.
6. Verify that the failure is blocked or rolled back.
7. Confirm the previous healthy version remains available.
8. Verify backup evidence and perform the approved restoration exercise.
9. Record timestamps, identities, artifact digests, test outputs, deployment status, rollback status, and residual issues.

**Exit evidence:**

- Successful release demonstration recorded.
- Unauthorized access demonstration recorded.
- Failed deployment and recovery demonstration recorded.
- Backup and restoration evidence recorded.
- No destructive production action performed.

---

### Phase 12: Platform Runway Acceptance and Handoff

**Timeline:** Working day 10  
**Unique objective:** Reconcile all technical and control evidence, confirm that only intended platform-foundation changes remain, and prepare the explicit approval decision for the next product increment.

**Directories:**

```text
/docs/releases/
/docs/testing/
/docs/architecture/
/docs/security/
/docs/operations/
```

**Files:**

```text
/docs/releases/platform-runway-release-notes.md
/docs/releases/release-evidence-template.md
/docs/testing/platform-runway-test-plan.md
/docs/testing/restoration-test-record.md
/docs/testing/rollback-test-record.md
```

**Implementation actions:**

1. Review all created and modified files.
2. Run complete backend, frontend, contract, infrastructure, policy, migration, security, and container validations.
3. Compare deployment evidence with acceptance criteria.
4. Confirm that no merchant or financial data was introduced.
5. Confirm that no secret, private endpoint, local origin, debug configuration, or unapproved mock is present in release artifacts.
6. Confirm infrastructure reproducibility from version-controlled definitions.
7. Confirm the staging access boundary.
8. Record defects, blockers, residual risks, ownership, and remediation.
9. Prepare the approval request for the Merchant Workspace and Access Control increment.
10. Stop at the completion gate.

**Exit evidence:**

- Platform runway acceptance report is complete.
- Working tree contains only intended changes before any repository action.
- Release and rollback evidence is traceable.
- Required reviewers have an explicit approve-or-return decision.
- No subsequent increment begins automatically.

---

## 7. Dependency Graph

### Ready after repository inspection

- Repository and architecture foundation
- Backend and web-shell skeleton
- Local health, version, correlation, and test implementation
- Terraform and Helm structure
- Security and operational documentation
- Local validation scripts

### Externally blocked until supplied

- Approved primary cloud account
- Approved AWS organization or equivalent cloud hierarchy
- Enterprise domain and DNS control
- Microsoft Entra ID tenant and application registrations
- Named security owner
- Remote Terraform state resources
- Managed artifact registry
- Managed PostgreSQL staging instance
- Managed Kubernetes staging cluster
- Approved observability environment
- Approved CI/CD repository and runner environment

### Approval-gated

- Dependency installation
- Lockfile creation or modification
- Cloud provisioning
- Terraform apply
- Identity-tenant configuration
- DNS changes
- Database creation
- Staging deployment
- Artifact publication
- Staging smoke tests against externally hosted resources
- Backup restoration exercise
- Staging, committing, pushing, opening a pull request, or merging

### Required order

```text
Architecture decisions
    -> application skeleton
    -> cloud and identity foundations
    -> database and security foundations
    -> runtime packaging
    -> observability
    -> delivery pipeline
    -> staging deployment
    -> failure and restoration demonstrations
    -> evidence review
    -> platform-runway approval gate
```

---

## 8. Required Validation

### Backend

- Gradle compilation
- Unit tests
- Spring context test
- Architecture-boundary test
- Health and version endpoint tests
- Correlation-ID tests
- Flyway migration validation
- OpenAPI contract validation

### Frontend

- Package integrity validation
- Type-check
- Lint
- Unit and component tests
- Production build
- Playwright authentication and health-view flow
- Accessibility checks for the operator shell

### Infrastructure

- Terraform format
- Terraform validate
- Terraform lint
- Terraform policy tests
- Terraform plan review
- Helm lint
- Kubernetes schema validation
- Kubernetes policy tests
- Argo CD manifest validation where applicable

### Security and supply chain

- Secret scan
- Dependency vulnerability scan
- Static application-security scan
- Container scan
- SBOM generation
- Artifact-signature verification
- Non-root container verification
- Prohibited-origin and placeholder scan
- Sensitive-log review

### Staging and recovery

- Approved-access-path verification
- Unauthorized-access denial
- Health and version smoke tests
- Log, metric, and trace correlation
- Failed-deployment blocking or rollback
- Last-healthy-release availability
- Backup creation
- Restoration test
- Audit-evidence review

---

## 9. Acceptance Criteria Traceability

### Staging is reachable only through approved access paths

Required evidence:

- Network policy and ingress review
- Identity enforcement test
- Unauthorized request result
- Administrative access review

### Application and database infrastructure can be recreated from version-controlled definitions

Required evidence:

- Terraform plan from clean state
- Helm render or deployment validation
- Environment-input inventory
- Restoration and recreation runbook

### No long-lived secret exists in source, pipeline variables, images, or logs

Required evidence:

- Gitleaks output
- Pipeline authentication design using workload federation
- Container filesystem inspection
- Structured-log redaction test
- Secret-store access evidence

### A backup is created and restoration is documented

Required evidence:

- Backup identifier and timestamp
- Retention and point-in-time recovery configuration
- Isolated restoration result
- Integrity verification
- Cleanup evidence

### A release produces traceable build, approval, deployment, and rollback evidence

Required evidence:

- Source revision
- Test results
- Scan results
- SBOM
- Image digest
- Signature
- Approval identity and timestamp
- Deployment revision
- Health verification
- Rollback or failed-release evidence

---

## 10. Completion Gate

The Enterprise Platform Runway is complete only when:

- The staging environment is deployed through approved automated delivery.
- Workforce identity, MFA, role groups, privileged elevation, and access logging are operating.
- Backend and web-shell builds and tests pass.
- Health and version information is available to authorized operators.
- Logs, metrics, and traces are correlated and accessible through approved paths.
- PostgreSQL is private, encrypted, backed up, and restoration-tested.
- Infrastructure definitions are reproducible and policy-checked.
- No long-lived secret appears in source, pipelines, images, or logs.
- A failed deployment is blocked or rolled back without displacing the last healthy release.
- Architecture decisions, threat model, inventories, control mapping, and runbooks are complete.
- All executable validation evidence is recorded.
- External blockers and residual risks are documented.
- Platform engineering, DevOps, security engineering, backend engineering, and QA automation provide an explicit approve-or-return decision.

**Mandatory stop condition:** Do not introduce merchant or financial data and do not begin the Merchant Workspace and Access Control increment until the platform runway receives explicit approval.

---

## 11. Implementation Agent's First Action

Inspect the exact live project directory, repository state, current files, remotes, branches, package manifests, lockfiles, and existing infrastructure definitions. Then report:

- Existing relevant implementation
- Differences from this specification
- Duplicate or conflict risks
- Ready work
- External blockers
- Approval-gated actions
- Exact first eligible implementation batch

Do not modify files before completing that inspection.
