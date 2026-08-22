# Noviq Pay Sprint 1 Manual Implementation Runbook

## Enterprise Platform Runway

**Organization:** Noviq Labs Ltd.  
**Product:** Noviq Pay  
**Repository:** `noviqpay`  
**Exact local project directory:** `/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay`  
**Current branch:** `main`, with no commits  
**Remote:** `https://github.com/ADBranches/noviqpay.git`  
**Operating system:** Kali GNU/Linux Rolling 2025.2, x86_64  
**Delivery window:** 10 working days  
**Execution model:** Manual, terminal-guided, sequential, evidence-driven  
**Status:** Ready to begin repository foundation after explicit execution approval

## Working Increment

Deliver a secure and reproducible Noviq Pay staging runway through automated delivery. Authorized workforce users must be able to authenticate, inspect the deployed application version and health, access approved logs, metrics, and traces, and release or recover a tested application version without exposing secrets or introducing merchant or financial data.

## Inspected Local Baseline

### Repository

- The local repository exists at the exact directory stated above.
- The repository is empty apart from `.git` metadata.
- The current unborn branch is `main`.
- No tracked project files, source files, package manifests, lockfiles, application modules, infrastructure files, or workflows exist.
- The remote URL is sanitized and does not contain a credential.

### Available tools

```text
Git             2.53.0
Java            21.0.11-ea
Javac           21.0.11-ea
Node.js         22.22.2
npm             10.9.7
Docker          27.5.1
Docker Compose  2.40.3
Helm            3.19.0
Trivy           0.66.0
```

### Missing tools

```text
Kotlin compiler
Gradle
Terraform
kubectl
AWS CLI
Gitleaks
Syft
Cosign
```

Missing tools must not be installed automatically. Installation is approval-gated and must be handled individually only when the relevant objective becomes eligible.

### System-change policy

The implementation must not run:

```text
apt upgrade
apt full-upgrade
apt dist-upgrade
unattended-upgrade
```

The implementation must not perform blanket package updates, pipe remote scripts into a shell, add unreviewed package repositories, or globally install project dependencies without approval.

## Terminal Contract

Every command group in this runbook must begin with:

```bash
cd "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay"
```

Commands must:

- Use the exact full project path.
- Avoid wildcarded project paths.
- Avoid heredocs.
- Avoid HTML-escaped shell symbols.
- Avoid embedded credentials and private values.
- Avoid commands that terminate the active shell.
- Inspect existing files before modifying them.
- Apply only the smallest eligible change.
- Run targeted verification immediately afterward.
- Stop at failures and approval gates.

## Scope Included

- Repository and engineering foundation
- Architecture decision records
- Cloud landing-zone definitions
- Workforce identity design and integration
- Kotlin and Spring Boot application skeleton
- Next.js operations web shell
- Managed PostgreSQL runway
- Infrastructure as code
- Build, test, scan, artifact, and staging-delivery workflows
- OCI containers and Kubernetes packaging
- OpenTelemetry-based observability
- Secrets and key-management baseline
- Backup and restoration evidence
- Deployment, rollback, alert, access-review, and restoration runbooks
- Initial threat model, asset inventory, data classification, and control mapping

## Scope Excluded

- Merchant registration and tenant data
- KYB documents
- Merchant API credentials
- Payment resources
- MTN or Airtel integrations
- Ledger accounts and financial journals
- Merchant webhooks
- Refunds, settlement, reconciliation, and risk rules
- Production deployment
- Live partner credentials
- Real customer or merchant data

---

# Phase 1: Repository and Engineering Foundation

## Unique objective

Create and validate the minimum Noviq Pay repository structure, governance files, security boundaries, environment policy, architecture baseline, and toolchain policy without installing dependencies or adding application behavior.

## Files and directories

```text
README.md
SECURITY.md
CONTRIBUTING.md
CODEOWNERS
.editorconfig
.gitattributes
.gitignore
.env.example
.tool-versions.example
apps/
contracts/
containers/
docs/architecture/decisions/
docs/operations/
docs/releases/
docs/security/
docs/testing/
infrastructure/argocd/
infrastructure/helm/
infrastructure/policies/
infrastructure/terraform/
observability/
scripts/
```

## Repository pre-flight inspection

Run before creating anything:

```bash
cd "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay"
printf '%s\n' "=== DIRECTORY ==="
pwd
printf '%s\n' "=== STATUS ==="
git status --short --branch
printf '%s\n' "=== BRANCH ==="
git branch --show-current
printf '%s\n' "=== REMOTE ==="
git remote -v
printf '%s\n' "=== EXISTING NON-GIT CONTENT ==="
find "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay" -mindepth 1 -maxdepth 3 -not -path "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/.git" -not -path "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/.git/*" -printf '%y %P\n' | sort
```

### Stop conditions

Stop if:

- The project directory differs.
- The current branch is not `main`.
- The remote differs from the sanitized URL.
- A non-Git file or directory exists unexpectedly.
- Git reports an unexpected tracked or modified file.

## Repository directory creation

```bash
cd "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay"
mkdir -p "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/apps" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/contracts" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/containers" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/docs/architecture/decisions" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/docs/operations" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/docs/releases" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/docs/security" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/docs/testing" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/infrastructure/argocd" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/infrastructure/helm" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/infrastructure/policies" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/infrastructure/terraform" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/observability" "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/scripts"
printf '%s\n' "Repository foundation directories created."
```

## Directory verification

```bash
cd "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay"
find "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay" -mindepth 1 -maxdepth 3 -type d -not -path "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/.git" -not -path "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/.git/*" -printf '%P\n' | sort
printf '%s\n' "=== FILES ==="
find "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay" -mindepth 1 -type f -not -path "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/.git/*" -printf '%P\n' | sort
printf '%s\n' "=== STATUS ==="
git status --short --branch
```

The files section must remain empty. Empty directories will not appear in Git status because Git does not track directories.

## Governance-file creation policy

Governance files are created only after the directory structure has been returned and inspected. Their exact contents must not be written based on assumptions. The next approved command batch will create:

```text
README.md
SECURITY.md
CONTRIBUTING.md
.gitignore
.gitattributes
.editorconfig
.env.example
```

`CODEOWNERS` must wait until repository ownership identities are confirmed. `.tool-versions.example` must wait until runtime-version decisions are validated.

## Phase 1 targeted validation

After the governance files are created in a later approved batch, run:

```bash
cd "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay"
printf '%s\n' "=== EXPECTED GOVERNANCE FILES ==="
for file in README.md SECURITY.md CONTRIBUTING.md .gitignore .gitattributes .editorconfig .env.example; do
    if test -f "$file"; then
        printf 'PRESENT %s\n' "$file"
    else
        printf 'MISSING %s\n' "$file"
    fi
done
printf '%s\n' "=== WHITESPACE VALIDATION ==="
git diff --check
printf '%s\n' "=== SENSITIVE-NAME SCAN ==="
grep -RInE --exclude-dir=.git --exclude='*.md' '(password|passwd|secret|token|api[_-]?key|private[_-]?key)[[:space:]]*[:=][[:space:]]*[^[:space:]#]+' . || true
printf '%s\n' "=== STATUS ==="
git status --short
```

The scan output must be reviewed manually. A text match is not automatically a secret, and the absence of a match does not replace Gitleaks once installation is approved.

## Phase 1 completion evidence

- Exact repository path confirmed.
- Empty starting state confirmed.
- Sanitized remote confirmed.
- Directory structure created and reviewed.
- Governance files created through inspected commands.
- No secrets or private endpoints included.
- No dependencies installed.
- No lockfile created.
- No staging, commit, push, or pull request performed.
- Architecture decisions remain pending until cloud, identity, runtime, and ownership choices are confirmed.

## Phase 1 approval gate

Stop before:

- Installing Gradle or Kotlin.
- Generating a Gradle Wrapper through a downloaded distribution.
- Running `npm install` or creating a frontend lockfile.
- Creating GitHub Actions workflows.
- Staging or committing the repository foundation.

---

# Phase 2: Runtime Decisions and Project-Local Build Foundation

## Unique objective

Pin the approved Java, Kotlin, Gradle, Node.js, npm, Spring Boot, and Next.js project versions and create reproducible project-local build foundations without relying on globally installed Gradle or Kotlin.

## Expected files and directories

```text
settings.gradle.kts
build.gradle.kts
gradle.properties
gradle/libs.versions.toml
gradlew
gradlew.bat
gradle/wrapper/gradle-wrapper.jar
gradle/wrapper/gradle-wrapper.properties
.nvmrc
apps/platform-api/
apps/operations-web/
scripts/verify-toolchain.sh
```

## Required inspection command

```bash
cd "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay"
printf '%s\n' "=== JAVA ==="
java -version
javac -version
printf '%s\n' "=== NODE AND NPM ==="
node --version
npm --version
printf '%s\n' "=== EXISTING BUILD FILES ==="
find "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay" -maxdepth 4 -type f \( -name 'settings.gradle.kts' -o -name 'build.gradle.kts' -o -name 'gradle.properties' -o -name 'libs.versions.toml' -o -name 'package.json' -o -name 'package-lock.json' -o -name 'gradlew' \) -printf '%P\n' | sort
```

## Approval requirements

Explicit approval is required before:

- Downloading or installing Gradle.
- Creating the Gradle Wrapper.
- Adding Kotlin or Spring dependencies.
- Running `npm install`.
- Creating or modifying lockfiles.

## Validation required after implementation

```bash
cd "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay"
./gradlew --version
./gradlew projects
node --version
npm --version
npm --prefix "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/apps/operations-web" run typecheck
```

Commands become executable only after the relevant files and dependencies have been inspected and approved.

---

# Phase 3: Modular Backend and Operations Web Shell

## Unique objective

Create a locally buildable Kotlin and Spring Boot platform API plus a TypeScript, React, and Next.js operations shell that expose only non-sensitive health and version information with correlation identifiers.

## Directories

```text
apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/
apps/platform-api/src/main/resources/
apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/
apps/operations-web/app/
apps/operations-web/components/
apps/operations-web/lib/
apps/operations-web/tests/
contracts/openapi/
```

## Principal files

```text
apps/platform-api/build.gradle.kts
apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/NoviqPayApplication.kt
apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/ApplicationProperties.kt
apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/CorrelationIdFilter.kt
apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/system/VersionController.kt
apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/system/VersionResponse.kt
apps/platform-api/src/main/resources/application.yml
apps/platform-api/src/main/resources/application-local.yml
apps/platform-api/src/main/resources/application-staging.yml
apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/ApplicationContextTest.kt
apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/CorrelationIdFilterTest.kt
apps/platform-api/src/test/kotlin/com/noviqlabs/pay/platform/VersionControllerTest.kt
apps/operations-web/package.json
apps/operations-web/package-lock.json
apps/operations-web/app/layout.tsx
apps/operations-web/app/page.tsx
apps/operations-web/app/health/page.tsx
apps/operations-web/components/ServiceHealthCard.tsx
apps/operations-web/components/SystemVersionCard.tsx
apps/operations-web/lib/configuration.ts
apps/operations-web/lib/platform-api.ts
apps/operations-web/tests/health-page.test.tsx
contracts/openapi/platform-system-api.yaml
```

## Implementation sequence

1. Inspect all build files created in Phase 2.
2. Create the backend module directories.
3. Create and inspect the backend module build definition.
4. Create the minimal application entry point.
5. Add Actuator health exposure with restricted details.
6. Add version response behavior.
7. Add correlation-ID generation and propagation.
8. Add backend tests.
9. Run targeted backend tests.
10. Create the Next.js shell using approved project-local dependencies.
11. Add the health and version view.
12. Add frontend tests.
13. Run targeted frontend tests before combined builds.

## Validation

```bash
cd "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay"
./gradlew :apps:platform-api:test
./gradlew :apps:platform-api:build
npm --prefix "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/apps/operations-web" run lint
npm --prefix "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/apps/operations-web" run test
npm --prefix "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/apps/operations-web" run build
git diff --check
git status --short
```

---

# Phase 4: Containerized Local Platform Validation

## Unique objective

Package and run the platform API, operations web shell, and local PostgreSQL dependency through non-root OCI containers before any cloud provisioning.

## Files

```text
containers/platform-api.Dockerfile
containers/operations-web.Dockerfile
docker-compose.yml
.env.example
scripts/validate-configuration.sh
scripts/smoke-test-local.sh
```

## Implementation sequence

1. Inspect backend and frontend build outputs and runtime requirements.
2. Create minimal multi-stage Dockerfiles.
3. Run application containers as non-root.
4. Add read-only filesystem settings where supported.
5. Add local PostgreSQL with synthetic runway data only.
6. Add health checks and controlled local networking.
7. Build images.
8. Scan images with existing Trivy.
9. Start the local stack.
10. Run local smoke tests.
11. Stop the local stack and verify cleanup.

## Validation

```bash
cd "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay"
docker compose config
docker compose build
trivy image --severity HIGH,CRITICAL --exit-code 1 noviqpay-platform-api:local
trivy image --severity HIGH,CRITICAL --exit-code 1 noviqpay-operations-web:local
docker compose up -d
docker compose ps
bash "/home/trovas/Downloads/projects/byupw/stripe clone/noviqpay/scripts/smoke-test-local.sh"
docker compose down
```

Image names must be verified against the inspected Compose configuration before running scan commands.

---

# Phase 5: Cloud Landing Zone and Environment Separation

## Unique objective

Define, without applying, an AWS-oriented Terraform landing zone with isolated development and staging boundaries, private application and database subnets, controlled ingress and egress, private service access, DNS boundaries, and remote-state requirements.

## Directories

```text
infrastructure/terraform/modules/landing-zone/
infrastructure/terraform/modules/network/
infrastructure/terraform/modules/dns/
infrastructure/terraform/environments/development/
infrastructure/terraform/environments/staging/
infrastructure/policies/
```

## Principal files

```text
infrastructure/terraform/versions.tf
infrastructure/terraform/providers.tf
infrastructure/terraform/backend.tf.example
infrastructure/terraform/modules/landing-zone/main.tf
infrastructure/terraform/modules/landing-zone/variables.tf
infrastructure/terraform/modules/landing-zone/outputs.tf
infrastructure/terraform/modules/network/main.tf
infrastructure/terraform/modules/network/variables.tf
infrastructure/terraform/modules/network/outputs.tf
infrastructure/terraform/modules/dns/main.tf
infrastructure/terraform/modules/dns/variables.tf
infrastructure/terraform/modules/dns/outputs.tf
infrastructure/terraform/environments/development/main.tf
infrastructure/terraform/environments/development/variables.tf
infrastructure/terraform/environments/development/terraform.tfvars.example
infrastructure/terraform/environments/staging/main.tf
infrastructure/terraform/environments/staging/variables.tf
infrastructure/terraform/environments/staging/terraform.tfvars.example
infrastructure/policies/terraform.rego
scripts/validate-terraform.sh
```

## Blockers and gates

Terraform is not installed locally. AWS CLI is not installed. The primary cloud account, account hierarchy, DNS ownership, remote-state resources, regions, CIDR ranges, and security owner are not yet confirmed.

Do not install Terraform or AWS CLI and do not run `terraform apply` without explicit approval.

---

# Phase 6: Workforce Identity and Privileged Access

## Unique objective

Protect operational interfaces using Microsoft Entra ID OIDC, MFA policy, workforce role groups, server-side authorization, time-bound privileged elevation, and access logging.

## Principal files

```text
apps/operations-web/middleware.ts
apps/operations-web/app/unauthorized/page.tsx
apps/operations-web/components/AuthenticationBoundary.tsx
apps/operations-web/lib/auth.ts
apps/operations-web/tests/authentication-boundary.test.tsx
apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/SecurityConfiguration.kt
docs/security/access-control-baseline.md
docs/operations/access-review-runbook.md
docs/architecture/decisions/ADR-006-workforce-identity.md
```

## External dependencies

- Approved Microsoft Entra tenant
- Application registrations
- Redirect-domain decisions
- Role-group owners
- MFA and privileged-access policy ownership

No real client secret may be placed in the repository. Workload federation and managed identity are preferred where supported.

---

# Phase 7: Managed PostgreSQL and Persistence Runway

## Unique objective

Define a private, encrypted managed PostgreSQL runway with separate application and migration identities, Flyway migration control, backup retention, point-in-time recovery, and an isolated restoration test.

## Principal files

```text
infrastructure/terraform/modules/database/main.tf
infrastructure/terraform/modules/database/variables.tf
infrastructure/terraform/modules/database/outputs.tf
apps/platform-api/src/main/resources/db/migration/V001__platform_runway.sql
scripts/validate-migrations.sh
scripts/verify-backup.sh
docs/operations/database-backup-runbook.md
docs/operations/database-restoration-runbook.md
docs/testing/restoration-test-record.md
docs/architecture/decisions/ADR-003-managed-postgresql.md
```

Database creation, migration application against shared infrastructure, and backup restoration remain approval-gated.

---

# Phase 8: Secrets, Keys, Service Identities, and Audit

## Unique objective

Use managed secrets, managed encryption keys, workload identities, least privilege, and audit records so no long-lived credential appears in source code, pipeline variables, images, documentation, or logs.

## Principal files

```text
infrastructure/terraform/modules/security/main.tf
infrastructure/terraform/modules/security/variables.tf
infrastructure/terraform/modules/security/outputs.tf
infrastructure/helm/noviq-pay/templates/service-account.yaml
docs/security/secrets-management-standard.md
docs/security/asset-inventory.md
docs/security/data-classification.md
scripts/scan-secrets.sh
```

Gitleaks is not installed. Installation is approval-gated. Until approved, Git and grep-based targeted checks are provisional and must not be described as equivalent to a dedicated secret scan.

---

# Phase 9: Kubernetes Packaging and Staging Runtime

## Unique objective

Package the approved images through Helm for a controlled managed Kubernetes staging runtime with least-privilege service accounts, default-deny network policy, health probes, resource limits, disruption protection, and rollback-aware deployment behavior.

## Principal files

```text
infrastructure/terraform/modules/kubernetes/main.tf
infrastructure/terraform/modules/kubernetes/variables.tf
infrastructure/terraform/modules/kubernetes/outputs.tf
infrastructure/helm/noviq-pay/Chart.yaml
infrastructure/helm/noviq-pay/values.yaml
infrastructure/helm/noviq-pay/values-staging.yaml
infrastructure/helm/noviq-pay/templates/platform-api-deployment.yaml
infrastructure/helm/noviq-pay/templates/platform-api-service.yaml
infrastructure/helm/noviq-pay/templates/operations-web-deployment.yaml
infrastructure/helm/noviq-pay/templates/operations-web-service.yaml
infrastructure/helm/noviq-pay/templates/ingress.yaml
infrastructure/helm/noviq-pay/templates/network-policy.yaml
infrastructure/helm/noviq-pay/templates/pod-disruption-budget.yaml
infrastructure/helm/noviq-pay/templates/servicemonitor.yaml
infrastructure/argocd/staging-application.yaml
scripts/validate-helm.sh
```

Helm is available. `kubectl` is not installed. Cluster provisioning, `kubectl` installation, Argo CD use, and staging deployment are approval-gated.

---

# Phase 10: Observability and Operator Visibility

## Unique objective

Make staging requests and deployments diagnosable through correlated OpenTelemetry logs, metrics, traces, dashboards, and alerts without exposing credentials or private business data.

## Principal files

```text
observability/otel/collector-config.yaml
observability/prometheus/alerts/platform-runway.yaml
observability/grafana/dashboards/platform-overview.json
observability/grafana/provisioning/dashboards.yaml
observability/grafana/provisioning/datasources.yaml
observability/loki/loki-config.yaml
observability/tempo/tempo-config.yaml
infrastructure/terraform/modules/observability/main.tf
infrastructure/terraform/modules/observability/variables.tf
infrastructure/terraform/modules/observability/outputs.tf
apps/platform-api/src/main/kotlin/com/noviqlabs/pay/platform/configuration/ObservabilityConfiguration.kt
apps/operations-web/app/observability/page.tsx
apps/operations-web/components/TelemetryLinks.tsx
docs/operations/alert-triage-runbook.md
```

---

# Phase 11: Pull-Request Validation and Automated Delivery

## Unique objective

Create a gated delivery chain that compiles, tests, scans, produces immutable release metadata, publishes approved images, deploys by digest, runs smoke checks, and preserves the last healthy staging release.

## Principal files

```text
.github/dependabot.yml
.github/pull_request_template.md
.github/workflows/pull-request-validation.yml
.github/workflows/build-and-publish.yml
.github/workflows/deploy-staging.yml
.github/workflows/infrastructure-plan.yml
.github/workflows/infrastructure-apply.yml
.github/workflows/security-scan.yml
scripts/scan-dependencies.sh
scripts/scan-containers.sh
scripts/generate-sbom.sh
scripts/smoke-test-staging.sh
scripts/verify-rollback.sh
docs/releases/release-evidence-template.md
docs/releases/platform-runway-release-notes.md
```

Syft and Cosign are not installed. GitHub Actions configuration, workflow permissions, OIDC federation, artifact registry, SBOM tooling, signing tooling, publication, and deployment are approval-gated.

---

# Phase 12: Security, Recovery, Demonstration, and Acceptance

## Unique objective

Complete the security and operational evidence, demonstrate approved change-to-staging delivery, verify unauthorized access denial, prove failed-release recovery and database restoration, and stop at the platform-runway approval gate.

## Principal files

```text
docs/security/initial-threat-model.md
docs/security/asset-inventory.md
docs/security/data-classification.md
docs/security/access-control-baseline.md
docs/security/secrets-management-standard.md
docs/security/control-mapping.md
docs/operations/deployment-runbook.md
docs/operations/rollback-runbook.md
docs/operations/alert-triage-runbook.md
docs/operations/database-backup-runbook.md
docs/operations/database-restoration-runbook.md
docs/operations/access-review-runbook.md
docs/testing/platform-runway-test-plan.md
docs/testing/restoration-test-record.md
docs/testing/rollback-test-record.md
docs/releases/platform-runway-release-notes.md
```

## End-to-end demonstration

1. An approved change passes the configured review gate.
2. The pipeline compiles, tests, scans, packages, and publishes an immutable release.
3. The approved release is deployed to staging.
4. An authorized operator signs in.
5. The operator views the deployed version and service health.
6. The operator follows one request across logs, metrics, and traces using a correlation ID.
7. An unauthorized user is denied and the denial is logged safely.
8. A controlled invalid release is blocked or rolled back.
9. The previous healthy release remains available.
10. Backup creation and isolated restoration are demonstrated and documented.

## Final acceptance criteria

- Staging is reachable only through approved paths.
- Application and database infrastructure are reproducible from reviewed definitions.
- No long-lived secret exists in source, pipeline variables, images, or logs.
- A backup exists and restoration evidence is documented.
- Every release maps source revision, tests, scans, image digest, approval, deployment, health, and rollback evidence.
- Backend and frontend builds pass.
- Infrastructure definitions pass available format, validation, lint, and policy checks.
- Logs, metrics, and traces are correlated.
- A failed release does not displace the last healthy release.
- No merchant or financial data has been introduced.
- All blockers and residual risks are recorded.

## Mandatory completion gate

Stop when the Enterprise Platform Runway evidence is ready for review. Do not begin Merchant Workspace and Access Control automatically.

Explicit approval is required before staging, committing, pushing, opening a pull request, changing shared infrastructure, or beginning the next sprint.

---

# Timeline Summary

## Working day 1

- Repository pre-flight
- Directory foundation
- Governance files
- Initial architecture and ownership decisions

## Working days 2 and 3

- Runtime-version decisions
- Gradle Wrapper and project-local build foundation
- Backend and operations-web skeleton
- Local targeted tests

## Working days 3 and 4

- Containerized local platform
- Local PostgreSQL runway
- Initial security and configuration validation

## Working days 4 through 6

- Cloud landing-zone definitions
- Managed PostgreSQL definitions
- Secrets, keys, service identities, and audit definitions
- Workforce identity integration design

## Working days 6 through 8

- Kubernetes and Helm packaging
- Observability
- Pull-request validation and automated delivery definitions

## Working days 8 and 9

- Approved staging deployment
- Operator authentication and visibility
- Backup, restoration, and rollback demonstration

## Working day 10

- Complete regression, security, infrastructure, and release review
- Evidence reconciliation
- Approve-or-return decision
- Mandatory stop before the next sprint

---

# Current Action

Execute only the Phase 1 repository pre-flight inspection. If the inspected state still matches this runbook, proceed to the Phase 1 directory-creation command. Return the full verification output before any governance file is created.
