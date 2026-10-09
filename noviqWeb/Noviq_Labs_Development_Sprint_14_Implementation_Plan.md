# Noviq Labs Full-Stack Platform

## Development Sprint 14: Data Intelligence, Reporting and Decision Support

**Sprint position:** Governed post-launch expansion sprint after Enterprise Readiness and Partner Integrations  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure production environment with controlled reporting rollout  
**Architecture:** Transactional platform with read-optimized reporting models and classified analytical boundaries

## Sprint Objective

Implement secure, evidence-led reporting and decision-support capabilities for customers and authorized Noviq operators. The sprint will deliver classified reporting models, executive and customer dashboards, project, lead, support, financial and security reporting, asynchronous exports, scheduled reports, data-quality monitoring, lineage governance and reporting audit trails. Every report must preserve tenant isolation, financial truth, privacy, security, accessibility and transactional performance.

---

## Phase 1: Sprint Entry and Evidence Verification

### Objectives

- Verify that Development Sprint 13 passed every completion-gate requirement.
- Confirm the verified Sprint 13 Git commit, pushed branch, pull-request state and controlled production rollout evidence.
- Confirm production health, partner API isolation, webhook delivery, financial correctness and error budgets remain within approved limits.
- Review customer reporting demand, operator reporting needs, data-quality findings and analytics backlog.
- Create the Sprint 14 development branch only after entry verification passes.
- Stop if any active incident, critical vulnerability, integration failure or financial inconsistency remains unresolved.

### Files to create

```text
/docs/evidence/sprint-14-entry-verification.md
/docs/data/sprint-14-scope.md
/docs/data/reporting-demand-evidence.md
/docs/data/data-readiness-register.md
/docs/delivery/sprint-14-branch-record.md
```

---

## Phase 2: Data and Reporting Architecture

### Objectives

- Define operational reporting, analytical reporting, export and dashboard boundaries.
- Keep PostgreSQL transactional workloads authoritative and isolated from expensive analytical queries.
- Define data movement, freshness, lineage, retention and recovery requirements.
- Separate customer, staff, finance, security and executive reporting boundaries.
- Avoid premature adoption of a large data platform without measured need.
- Record approved architectural decisions.

### Files to create

```text
/docs/architecture/data-reporting-context.md
/docs/architecture/reporting-data-flows.md
/docs/architecture/analytics-trust-boundaries.md
/docs/architecture/adr/0043-use-read-optimized-reporting-models.md
/docs/architecture/adr/0044-separate-operational-and-analytical-workloads.md
/docs/architecture/adr/0045-enforce-reporting-data-lineage.md
```

---

## Phase 3: Reporting Data Classification

### Objectives

- Classify fields as public, internal, customer-confidential, restricted-security, personal or financial.
- Define which classifications may appear in each report family.
- Prevent confidential free text, document bodies, secrets and authentication data from entering general analytics.
- Define aggregation and suppression rules for small groups.
- Require review for new report fields.
- Document classification ownership.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Reporting/ReportingDataClassification.cs
/apps/api/NoviqLabs.Domain/Reporting/ReportFieldPolicy.cs
/apps/api/NoviqLabs.Application/Reporting/ReportFieldPolicyService.cs
/tests/api/NoviqLabs.Api.UnitTests/Reporting/ReportFieldPolicyTests.cs
/docs/data/reporting-classification-matrix.md
/docs/privacy/analytics-data-boundary.md
```

---

## Phase 4: Reporting Roles and Authorization

### Objectives

- Define customer analyst, project reporter, finance reporter, security reporter and executive reporter policies.
- Require organization, project and subject-matter authorization in addition to report roles.
- Keep restricted-security and financial datasets excluded by default.
- Prevent report filters from bypassing tenant isolation.
- Audit report execution, export and privileged drill-down actions.
- Test deny-by-default behavior.

### Files to create

```text
/apps/api/NoviqLabs.Application/Authorization/CustomerAnalystRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/FinanceReporterRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/SecurityReporterRequirement.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/ReportingAuthorizationHandlers.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Authorization/ReportingAuthorizationTests.cs
/docs/security/reporting-authorization.md
```

---

## Phase 5: Reporting Domain Model

### Objectives

- Create report definition, parameter, execution, result, schedule and export entities.
- Support draft, active, paused, retired and failed states.
- Preserve report version, owner, audience and classification.
- Record execution timestamps, duration, row count and outcome.
- Prevent arbitrary SQL or executable expressions in user-managed definitions.
- Define bounded result and retention limits.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Reporting/ReportDefinition.cs
/apps/api/NoviqLabs.Domain/Reporting/ReportParameter.cs
/apps/api/NoviqLabs.Domain/Reporting/ReportExecution.cs
/apps/api/NoviqLabs.Domain/Reporting/ReportSchedule.cs
/apps/api/NoviqLabs.Domain/Reporting/ReportExport.cs
/apps/api/NoviqLabs.Domain/Reporting/ReportStatus.cs
/apps/api/NoviqLabs.Domain/Reporting/ReportingErrors.cs
/docs/data/report-lifecycle.md
```

---

## Phase 6: Data-Quality Domain Model

### Objectives

- Create data-quality rule, execution, result, exception and remediation entities.
- Support completeness, validity, uniqueness, consistency, freshness and referential-integrity checks.
- Assign severity, owner and remediation target.
- Preserve historical outcomes and evidence.
- Prevent automatic destructive correction of transactional data.
- Escalate critical financial and tenant-isolation quality failures.

### Files to create

```text
/apps/api/NoviqLabs.Domain/DataQuality/DataQualityRule.cs
/apps/api/NoviqLabs.Domain/DataQuality/DataQualityResult.cs
/apps/api/NoviqLabs.Domain/DataQuality/DataQualityException.cs
/apps/api/NoviqLabs.Domain/DataQuality/DataQualitySeverity.cs
/apps/api/NoviqLabs.Domain/DataQuality/DataQualityErrors.cs
/docs/data/data-quality-lifecycle.md
```

---

## Phase 7: Reporting Persistence and Migration

### Objectives

- Map report definitions, schedules, executions, exports and data-quality entities to PostgreSQL.
- Add tenant, owner, classification, status and execution indexes.
- Apply unique constraints to stable report identifiers and active schedules.
- Store large report files outside transactional tables.
- Create the controlled Sprint 14 migration.
- Validate clean application, upgrade and rollback boundaries.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ReportDefinitionConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ReportExecutionConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ReportScheduleConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/DataQualityRuleConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddReportingAndDataQuality.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddReportingAndDataQuality.Designer.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/ReportingMigrationTests.cs
/docs/database/reporting-schema.md
```

---

## Phase 8: Read-Optimized Reporting Models

### Objectives

- Create approved read models for organizations, projects, intake, support, billing and payments.
- Exclude restricted fields by construction.
- Preserve authoritative identifiers and timestamps.
- Use incremental refresh and idempotent rebuild behavior.
- Measure freshness and lag.
- Document source-to-field lineage.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Reporting/Models/OrganizationReportingModel.cs
/apps/api/NoviqLabs.Infrastructure/Reporting/Models/ProjectReportingModel.cs
/apps/api/NoviqLabs.Infrastructure/Reporting/Models/IntakeReportingModel.cs
/apps/api/NoviqLabs.Infrastructure/Reporting/Models/SupportReportingModel.cs
/apps/api/NoviqLabs.Infrastructure/Reporting/Models/BillingReportingModel.cs
/apps/api/NoviqLabs.Infrastructure/Reporting/Models/PaymentReportingModel.cs
/docs/data/reporting-model-lineage.md
```

---

## Phase 9: Reporting Model Refresh

### Objectives

- Implement incremental refresh from authoritative transactional changes.
- Use checkpoints and idempotent processing.
- Handle missed, duplicate and out-of-order events safely.
- Provide controlled full rebuild for recovery.
- Monitor freshness, failures and backlog.
- Prevent refresh jobs from blocking customer transactions.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/ReportingModelRefreshJob.cs
/apps/worker/NoviqLabs.Worker/Jobs/ReportingModelRebuildJob.cs
/apps/worker/NoviqLabs.Worker/Services/ReportingCheckpointStore.cs
/apps/worker/NoviqLabs.Worker/Services/ReportingModelBuilder.cs
/tests/worker/NoviqLabs.Worker.UnitTests/ReportingModelRefreshJobTests.cs
/docs/operations/reporting-model-refresh.md
```

---

## Phase 10: Executive Metrics Catalogue

### Objectives

- Define approved executive metrics with formulas, sources, owners and refresh frequency.
- Cover acquisition, conversion, delivery, support, revenue, payment and reliability indicators.
- Avoid unsupported vanity metrics and ambiguous definitions.
- Preserve consistent time-zone and currency treatment.
- Document limitations and interpretation guidance.
- Require approval before metric changes.

### Files to create

```text
/docs/data/executive-metrics-catalogue.md
/docs/data/metric-definition-template.md
/apps/api/NoviqLabs.Application/Reporting/ExecutiveMetricDefinitions.cs
/apps/api/NoviqLabs.Application/Reporting/ExecutiveMetricService.cs
/tests/api/NoviqLabs.Api.UnitTests/Reporting/ExecutiveMetricTests.cs
/docs/evidence/sprint-14-metric-validation.md
```

---

## Phase 11: Executive Dashboard

### Objectives

- Implement a restricted executive dashboard.
- Display approved acquisition, project, support, revenue, payment and reliability metrics.
- Support controlled date, service and organization-segment filters.
- Prevent drill-down into restricted customer content without separate authorization.
- Show freshness and data-quality status.
- Provide accessible chart alternatives and summaries.

### Files to create

```text
/apps/web/src/app/(admin)/admin/analytics/executive/page.tsx
/apps/web/src/features/admin/analytics/ExecutiveDashboardPage.tsx
/apps/web/src/features/admin/analytics/ExecutiveMetricCard.tsx
/apps/web/src/features/admin/analytics/ExecutiveTrendChart.tsx
/apps/web/src/features/admin/analytics/MetricFreshnessIndicator.tsx
/apps/web/src/features/admin/analytics/ExecutiveDashboardPage.test.tsx
/docs/data/executive-dashboard.md
```

---

## Phase 12: Customer Reporting Dashboard

### Objectives

- Implement organization-scoped customer reporting.
- Show project delivery, milestone, support, invoice and payment summaries.
- Prevent cross-organization aggregation and internal-data exposure.
- Provide date and project filters with bounded ranges.
- Show data freshness and definitions.
- Support responsive and accessible presentation.

### Files to create

```text
/apps/web/src/app/(account)/reports/page.tsx
/apps/web/src/features/reporting/CustomerReportsPage.tsx
/apps/web/src/features/reporting/ProjectDeliverySummary.tsx
/apps/web/src/features/reporting/SupportSummaryReport.tsx
/apps/web/src/features/reporting/BillingSummaryReport.tsx
/apps/web/src/features/reporting/ReportFilterBar.tsx
/apps/web/src/features/reporting/CustomerReportsPage.test.tsx
/docs/data/customer-reporting.md
```

---

## Phase 13: Project Delivery Reporting

### Objectives

- Create project status, milestone predictability, deliverable cycle-time and approval reporting.
- Separate customer-visible and internal delivery metrics.
- Preserve baseline and revised dates.
- Avoid ranking individuals from incomplete context.
- Provide project and portfolio-level views for authorized users.
- Document metric limitations.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reporting/GetProjectDeliveryReportQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Reporting/GetProjectDeliveryReportEndpoint.cs
/apps/web/src/features/reporting/ProjectDeliveryReport.tsx
/apps/web/src/features/admin/analytics/PortfolioDeliveryReport.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Reporting/ProjectDeliveryReportTests.cs
/docs/data/project-delivery-reporting.md
```

---

## Phase 14: Lead and Conversion Reporting

### Objectives

- Report service interest, intake completion, consultation and lead-conversion trends.
- Exclude sensitive free text and uploaded requirement contents.
- Respect analytics consent for non-essential events.
- Separate operational counts from attribution estimates.
- Support source, service and date dimensions.
- Document attribution limitations.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reporting/GetLeadConversionReportQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Reporting/GetLeadConversionReportEndpoint.cs
/apps/web/src/features/admin/analytics/LeadConversionDashboard.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Reporting/LeadConversionReportTests.cs
/docs/data/lead-conversion-reporting.md
```

---

## Phase 15: Support Reporting

### Objectives

- Report request volume, acknowledgement time, resolution time, reopen rate and recurring categories.
- Separate customer-selected priority from operational severity.
- Exclude message content and personal data from aggregates.
- Provide trend and backlog views.
- Show data-quality and classification caveats.
- Avoid incentivizing premature closure.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reporting/GetSupportPerformanceReportQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Reporting/GetSupportPerformanceReportEndpoint.cs
/apps/web/src/features/admin/analytics/SupportPerformanceDashboard.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Reporting/SupportPerformanceReportTests.cs
/docs/data/support-reporting.md
```

---

## Phase 16: Financial Reporting

### Objectives

- Report invoiced, collected, outstanding, overdue, refunded and reconciled amounts.
- Use immutable financial records and minor-unit arithmetic.
- Preserve currency separation unless an approved exchange-rate source exists.
- Restrict settlement and exception detail to finance roles.
- Show reconciliation state and freshness.
- Verify totals against authoritative records.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reporting/GetFinancialSummaryReportQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Reporting/GetFinancialSummaryReportEndpoint.cs
/apps/web/src/features/admin/analytics/FinancialReportingDashboard.tsx
/apps/web/src/features/admin/analytics/ReconciliationSummary.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Reporting/FinancialReportingTests.cs
/docs/data/financial-reporting.md
```

---

## Phase 17: Security and Compliance Reporting

### Objectives

- Report access reviews, privileged actions, credential age, findings, remediation and control status.
- Exclude exploit detail, security evidence and restricted report contents from general dashboards.
- Require security-reporting authorization and strong authentication.
- Provide control-level evidence references.
- Track overdue remediation without exposing sensitive targets.
- Audit report access.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reporting/GetSecurityPostureReportQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Reporting/GetSecurityPostureReportEndpoint.cs
/apps/web/src/features/admin/analytics/SecurityPostureDashboard.tsx
/apps/web/src/features/admin/analytics/ControlEvidenceSummary.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Reporting/SecurityReportingTests.cs
/docs/security/security-reporting-boundary.md
```

---

## Phase 18: Report Export Service

### Objectives

- Generate approved CSV and PDF report exports asynchronously.
- Apply authorization and field classification at generation time.
- Use private storage and short-lived download authorization.
- Limit row count, file size and retention.
- Record integrity hash, creator, scope and download events.
- Prevent formula injection in spreadsheet-compatible output.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reporting/CreateReportExportCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Reporting/CreateReportExportEndpoint.cs
/apps/worker/NoviqLabs.Worker/Jobs/ReportExportJob.cs
/apps/worker/NoviqLabs.Worker/Documents/ReportPdfRenderer.cs
/apps/worker/NoviqLabs.Worker/Documents/ReportCsvRenderer.cs
/apps/api/NoviqLabs.Infrastructure/Reporting/ReportExportStorage.cs
/tests/worker/NoviqLabs.Worker.UnitTests/ReportExportJobTests.cs
/docs/security/report-export-controls.md
```

---

## Phase 19: Scheduled Reports

### Objectives

- Allow authorized users to schedule approved reports.
- Validate recipient, scope, frequency, time zone and expiry.
- Send secure links rather than sensitive attachments where required.
- Pause schedules after repeated delivery failures.
- Prevent schedules from retaining access after role removal.
- Audit creation, update, delivery and cancellation.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reporting/CreateReportScheduleCommand.cs
/apps/api/NoviqLabs.Application/Reporting/CancelReportScheduleCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Reporting/CreateReportScheduleEndpoint.cs
/apps/worker/NoviqLabs.Worker/Jobs/ScheduledReportJob.cs
/apps/web/src/features/reporting/ReportScheduleForm.tsx
/apps/web/src/features/reporting/ReportScheduleList.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Reporting/ScheduledReportTests.cs
/docs/data/scheduled-reports.md
```

---

## Phase 20: Data-Quality Rules and Monitoring

### Objectives

- Implement approved completeness, validity, uniqueness, consistency and freshness rules.
- Run rules on transactional and reporting models without blocking ordinary reads.
- Escalate critical financial, tenant-isolation and authorization-quality failures.
- Provide rule history and remediation status.
- Prevent automatic destructive correction.
- Expose quality status to report owners.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/DataQualityEvaluationJob.cs
/apps/api/NoviqLabs.Application/DataQuality/DataQualityRuleCatalogue.cs
/apps/api/NoviqLabs.Application/DataQuality/GetDataQualityResultsQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/DataQuality/GetDataQualityResultsEndpoint.cs
/apps/web/src/app/(admin)/admin/data-quality/page.tsx
/apps/web/src/features/admin/data-quality/DataQualityDashboard.tsx
/tests/worker/NoviqLabs.Worker.UnitTests/DataQualityEvaluationJobTests.cs
/docs/data/data-quality-monitoring.md
```

---

## Phase 21: Data-Lineage Register

### Objectives

- Record source, transformation, destination, owner and classification for every approved metric and report field.
- Link report versions to lineage versions.
- Detect unregistered report fields in continuous integration.
- Document transformation assumptions and freshness.
- Restrict sensitive lineage details appropriately.
- Assign review dates.

### Files to create

```text
/docs/data/data-lineage-register.yaml
/tools/data-lineage/package.json
/tools/data-lineage/src/validate.ts
/scripts/data/validate-data-lineage.zsh
/.github/workflows/validate-data-lineage.yml
/docs/data/data-lineage-governance.md
```

---

## Phase 22: Reporting Audit Trails

### Objectives

- Audit report execution, export, download, schedule and privileged drill-down actions.
- Record actor, organization, report, parameters, result, timestamp and correlation identifier.
- Exclude report contents and sensitive values from audit records.
- Restrict audit access and define retention.
- Detect unusual export and download activity.
- Test audit completeness.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Audit/ReportingAuditEvent.cs
/apps/api/NoviqLabs.Domain/Audit/ReportingAuditAction.cs
/apps/api/NoviqLabs.Application/Audit/IReportingAuditWriter.cs
/apps/api/NoviqLabs.Infrastructure/Audit/ReportingAuditWriter.cs
/apps/api/NoviqLabs.Api/Endpoints/Administration/GetReportingAuditEventsEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Audit/ReportingAuditTests.cs
/docs/security/reporting-audit-trails.md
```

---

## Phase 23: Reporting Security Testing

### Objectives

- Test report-filter manipulation, tenant bypass and unauthorized drill-down.
- Test export authorization, expired links and revoked access.
- Test CSV formula injection, PDF rendering and large-result abuse.
- Test financial and security-report role boundaries.
- Test inference risks from small cohorts.
- Resolve all critical and high-risk findings.

### Files to create

```text
/apps/web/tests/security/report-filter-isolation.spec.ts
/apps/web/tests/security/report-export-access.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Security/ReportingTenantIsolationTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/ReportExportInjectionTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/ReportingRoleBoundaryTests.cs
/scripts/security/scan-sprint-14-reporting.zsh
/docs/evidence/sprint-14-reporting-security.md
```

---

## Phase 24: Accessibility and Data Usability

### Objectives

- Validate dashboards, charts, filters, tables, exports and schedules with keyboard and assistive technology.
- Provide text alternatives and tabular equivalents for charts.
- Verify color is not the only status indicator.
- Test mobile, tablet, desktop and 200 percent zoom.
- Conduct representative customer, finance, security and executive tasks.
- Resolve all blocking defects.

### Files to create

```text
/apps/web/tests/accessibility/customer-reporting.spec.ts
/apps/web/tests/accessibility/executive-dashboard.spec.ts
/apps/web/tests/accessibility/financial-reporting.spec.ts
/apps/web/tests/accessibility/security-reporting.spec.ts
/apps/web/tests/accessibility/report-scheduling.spec.ts
/apps/web/tests/usability/sprint-14-reporting-tasks.spec.ts
/docs/evidence/sprint-14-accessibility-usability.md
```

---

## Phase 25: Performance and Scale Validation

### Objectives

- Measure dashboard, report, export and refresh latency.
- Load test bounded concurrent reports and scheduled exports.
- Verify analytical workloads do not starve transactional workflows.
- Test refresh backlog, full rebuild and failure recovery.
- Validate indexes, caching and storage throughput.
- Record capacity and scaling recommendations.

### Files to create

```text
/tests/load/sprint-14-dashboards.js
/tests/load/sprint-14-report-queries.js
/tests/load/sprint-14-report-exports.js
/tests/load/sprint-14-report-refresh.js
/scripts/quality/validate-sprint-14-performance.zsh
/docs/evidence/sprint-14-performance-results.md
```

---

## Phase 26: Integration and End-to-End Testing

### Objectives

- Test reporting-model refresh through customer and administrative dashboards.
- Test organization, project, financial and security authorization boundaries.
- Test exports, schedules, secure downloads and expiry.
- Test data-quality detection and remediation status.
- Test refresh, storage and notification failure recovery.
- Verify audit completeness.

### Files to create

```text
/apps/web/tests/e2e/customer-reporting.spec.ts
/apps/web/tests/e2e/executive-reporting.spec.ts
/apps/web/tests/e2e/report-export-lifecycle.spec.ts
/apps/web/tests/e2e/scheduled-report-lifecycle.spec.ts
/apps/web/tests/e2e/data-quality-workflow.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Resilience/ReportingFailureTests.cs
/docs/evidence/sprint-14-end-to-end-results.md
```

---

## Phase 27: CI/CD Data and Reporting Gates

### Objectives

- Add reporting migration, lineage, metric, authorization, export, accessibility, security and load tests.
- Preserve evidence as workflow artifacts.
- Block unregistered report fields and metric-definition drift.
- Build verified web, API and worker images only after all gates pass.
- Fail when any required underlying command fails.
- Keep synthetic test datasets out of production.

### Files to create

```text
/.github/workflows/ci-data-reporting.yml
/.github/workflows/test-reporting-authorization.yml
/.github/workflows/test-report-exports.yml
/.github/workflows/test-data-quality.yml
/.github/workflows/test-reporting-accessibility.yml
/.github/workflows/test-reporting-security.yml
/.github/workflows/test-reporting-load.yml
/.github/workflows/validate-reporting-migration.yml
/scripts/ci/verify-sprint-14-reporting.zsh
/scripts/ci/verify-sprint-14-quality-gates.zsh
/docs/delivery/sprint-14-quality-gates.md
```

---

## Phase 28: Azure Infrastructure and Deployment

### Objectives

- Provision private report storage, queues, monitoring, worker scaling and approved reporting resources through infrastructure as code.
- Apply the Sprint 14 migration through the controlled migration job.
- Deploy verified web, API and worker images to development and staging.
- Verify managed identities, private networking, storage retention, telemetry and alerts.
- Keep production reporting access allowlisted until rollout approval.
- Execute smoke tests using synthetic non-production data.

### Files to create

```text
/infrastructure/azure/modules/reporting-storage.bicep
/infrastructure/azure/modules/reporting-queues.bicep
/infrastructure/azure/modules/reporting-alerts.bicep
/infrastructure/azure/config/reporting-worker-scaling.json
/infrastructure/azure/config/reporting-alert-thresholds.json
/.github/workflows/deploy-reporting-development.yml
/.github/workflows/deploy-reporting-staging.yml
/scripts/cloud/deploy-sprint-14-staging.zsh
/scripts/cloud/smoke-test-sprint-14-reporting.zsh
/docs/evidence/sprint-14-staging-deployment.md
```

---

## Phase 29: Controlled Production Rollout

### Objectives

- Deploy reporting capabilities through the approved production release process.
- Use feature flags and role allowlists for initial access.
- Verify data freshness, authorization, report totals, exports, monitoring and rollback.
- Monitor transactional latency and error budgets during rollout.
- Disable reporting access or roll back if agreed thresholds are breached.
- Record stabilization evidence.

### Files to create

```text
/.github/workflows/deploy-sprint-14-production.yml
/scripts/cloud/deploy-sprint-14-production.zsh
/scripts/cloud/verify-sprint-14-production.zsh
/scripts/operations/monitor-reporting-rollout.zsh
/docs/release/sprint-14-reporting-rollout.md
/docs/evidence/sprint-14-production-deployment.md
/docs/evidence/sprint-14-rollout-stabilization.md
```

---

## Phase 30: Documentation, Training and Handover

### Objectives

- Document report ownership, metric definitions, exports, schedules, data quality and recovery procedures.
- Train authorized customer, executive, finance, security and operational users.
- Verify least-privilege access after training.
- Document support boundaries and review dates.
- Keep terminal procedures Zsh-compatible for Kali Debian.
- Remove obsolete reporting instructions.

### Files to create

```text
/docs/reporting/customer-reporting-guide.md
/docs/reporting/executive-reporting-guide.md
/docs/reporting/finance-reporting-guide.md
/docs/reporting/security-reporting-guide.md
/docs/operations/reporting-operator-runbook.md
/docs/operations/reporting-recovery-runbook.md
/docs/training/sprint-14-training-record.md
/docs/development/sprint-14-kali-debian-zsh.md
/docs/evidence/sprint-14-handover-verification.md
```

---

## Phase 31: Integrated Validation and Sprint Closure

### Objectives

- Validate all reporting, data-quality, export and scheduling capabilities from a clean checkout.
- Execute build, migration, lineage, unit, integration, end-to-end, accessibility, security and load tests.
- Verify controlled production rollout and stabilization evidence.
- Verify tenant isolation, financial correctness, privacy and security remain intact.
- Create and push the verified Sprint 14 Git commit.
- Create a pull request only after all required validation passes.
- Record remaining reporting improvements in the governed backlog.
- Stop at the Sprint 14 completion gate.

### Files to create

```text
/scripts/release/sprint-14-final-validation.zsh
/docs/evidence/sprint-14-reporting-model-summary.md
/docs/evidence/sprint-14-dashboard-summary.md
/docs/evidence/sprint-14-export-schedule-summary.md
/docs/evidence/sprint-14-data-quality-summary.md
/docs/evidence/sprint-14-accessibility-summary.md
/docs/evidence/sprint-14-performance-summary.md
/docs/evidence/sprint-14-security-privacy-summary.md
/docs/evidence/sprint-14-deployment-summary.md
/docs/evidence/sprint-14-completion-record.md
/docs/delivery/sprint-14-pull-request.md
```

---

## Development Sprint 14 Completion Gate

Development Sprint 14 is complete only when every condition below passes:

- Sprint 13 completion and production-health verification pass.
- Reporting architecture separates analytical and transactional workloads appropriately.
- Reporting fields are classified and approved before use.
- Reporting roles do not bypass organization, project, finance or security authorization.
- Reporting entities and the Sprint 14 migration validate successfully.
- Read-optimized models exclude restricted fields by construction.
- Refresh processing is incremental, idempotent and recoverable.
- Reporting freshness and backlog monitoring operate correctly.
- Executive metric definitions have formulas, sources, owners and limitations.
- Executive dashboards show approved metrics and data-quality status.
- Customer dashboards enforce strict organization isolation.
- Project, lead, support, financial and security reports pass correctness checks.
- Financial reports reconcile with authoritative invoice, payment and settlement records.
- Security reports do not expose restricted evidence or exploit detail.
- Report exports enforce authorization, classification, size and retention controls.
- CSV exports resist formula injection.
- Scheduled reports honor current authorization and expire correctly.
- Data-quality rules detect approved completeness, validity, uniqueness, consistency and freshness failures.
- Critical financial and tenant-isolation quality failures escalate.
- Data lineage covers every approved report field and metric.
- Reporting audit trails are complete and protected.
- Reporting security tests find no unresolved critical or high-risk issue.
- Accessibility and data-usability checks pass.
- Reporting performance and load-isolation budgets pass.
- Analytical workloads do not degrade critical transactional workflows beyond approved limits.
- CI/CD data and reporting gates pass.
- Development, staging and controlled production rollout checks pass.
- Reporting access remains allowlisted until formal expansion approval.
- Documentation, training and ownership handover are complete.
- A verified Development Sprint 14 Git commit exists.
- The Development Sprint 14 branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- The production platform remains live, secure, monitored and recoverable.

## Development Sprint 14 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_14_COMPLETE
NOVIQ_LABS_DATA_INTELLIGENCE_PLATFORM_ACTIVE
```
