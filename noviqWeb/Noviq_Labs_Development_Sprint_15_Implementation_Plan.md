# Noviq Labs Full-Stack Platform

## Development Sprint 15: Customer Success, Onboarding and Lifecycle Management

**Sprint position:** Governed post-launch expansion sprint after Data Intelligence and Reporting  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure production environment with controlled pilot rollout  
**Architecture:** Organization-scoped customer-success domain built on approved operational and reporting evidence

## Sprint Objective

Implement secure, evidence-led customer onboarding and lifecycle-management capabilities. The sprint will deliver onboarding plans and templates, customer success plans, explainable customer-health indicators, adoption insights, guided education, lifecycle communications, risk reviews, renewal readiness and customer outcome reporting. Every capability must preserve tenant isolation, privacy, fairness, financial truth, accessibility, security and production reliability.

---

## Phase 1: Entry and dependency verification

### Objectives

- Verify Sprint 14 completion evidence, Git state, production health, reporting accuracy and error budgets.
- Review customer demand, product adoption, support trends and approved roadmap priorities.
- Confirm no active incident, critical vulnerability, financial inconsistency or data-quality failure blocks the sprint.
- Create the Sprint 15 branch only after every entry gate passes.

### Files to create

```text
/docs/evidence/sprint-15-entry-verification.md
/docs/customer-success/sprint-15-scope.md
/docs/customer-success/demand-evidence.md
/docs/customer-success/dependency-register.md
/docs/delivery/sprint-15-branch-record.md
```

---

## Phase 2: Customer success architecture

### Objectives

- Define onboarding, adoption, health, success-plan and renewal-support boundaries.
- Keep commercial truth in billing records and customer-success observations in dedicated records.
- Separate customer-visible guidance from internal account management.
- Document privacy, authorization, retention and escalation boundaries.

### Files to create

```text
/docs/architecture/customer-success-context.md
/docs/architecture/customer-lifecycle-flows.md
/docs/architecture/customer-success-data-boundaries.md
/docs/architecture/adr/0046-introduce-customer-success-domain.md
/docs/architecture/adr/0047-use-evidence-based-customer-health.md
```

---

## Phase 3: Customer success domain model

### Objectives

- Create customer-success account, lifecycle stage, owner, outcome and engagement entities.
- Associate every record with one authorized organization.
- Support onboarding, adopting, established, at risk, renewing and inactive stages.
- Preserve lifecycle history and accountable ownership.

### Files to create

```text
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerSuccessAccount.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerLifecycleStage.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerSuccessOwner.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerOutcome.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerEngagement.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerSuccessErrors.cs
/docs/customer-success/customer-lifecycle.md
```

---

## Phase 4: Onboarding-plan domain model

### Objectives

- Create onboarding plans, steps, dependencies, owners, target dates and completion evidence.
- Support template-derived and organization-specific plans.
- Separate customer tasks from internal tasks.
- Prevent completion without required evidence.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Onboarding/OnboardingPlan.cs
/apps/api/NoviqLabs.Domain/Onboarding/OnboardingStep.cs
/apps/api/NoviqLabs.Domain/Onboarding/OnboardingStepStatus.cs
/apps/api/NoviqLabs.Domain/Onboarding/OnboardingEvidence.cs
/apps/api/NoviqLabs.Domain/Onboarding/OnboardingErrors.cs
/docs/customer-success/onboarding-plan-lifecycle.md
```

---

## Phase 5: Success-plan domain model

### Objectives

- Create success plans, objectives, measures, checkpoints and review decisions.
- Require measurable customer outcomes and explicit ownership.
- Preserve baseline, target and actual values separately.
- Avoid unsupported promises or automatic commercial commitments.

### Files to create

```text
/apps/api/NoviqLabs.Domain/CustomerSuccess/SuccessPlan.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/SuccessObjective.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/SuccessMeasure.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/SuccessCheckpoint.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/SuccessPlanErrors.cs
/docs/customer-success/success-plan-lifecycle.md
```

---

## Phase 6: Customer-health model

### Objectives

- Define explainable health indicators based on approved product, support, project and payment signals.
- Keep health scores advisory and reviewable.
- Prevent sensitive content and protected attributes from influencing scores.
- Record score version, inputs, limitations and overrides.

### Files to create

```text
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerHealthScore.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerHealthSignal.cs
/apps/api/NoviqLabs.Application/CustomerSuccess/CustomerHealthCalculator.cs
/apps/api/NoviqLabs.Application/CustomerSuccess/CustomerHealthPolicy.cs
/tests/api/NoviqLabs.Api.UnitTests/CustomerSuccess/CustomerHealthCalculatorTests.cs
/docs/customer-success/customer-health-methodology.md
```

---

## Phase 7: Renewal-readiness model

### Objectives

- Create renewal window, readiness, risk, decision and follow-up entities.
- Use contract and subscription dates as authoritative commercial inputs.
- Prevent renewal forecasts from modifying contracts or subscriptions.
- Record review history and accountable owners.

### Files to create

```text
/apps/api/NoviqLabs.Domain/CustomerSuccess/RenewalReadiness.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/RenewalRisk.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/RenewalReview.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/RenewalErrors.cs
/docs/customer-success/renewal-readiness.md
```

---

## Phase 8: Persistence and migration

### Objectives

- Map customer-success, onboarding, success-plan, health and renewal entities to PostgreSQL.
- Add organization scope, concurrency controls and lifecycle indexes.
- Preserve historical health and lifecycle records.
- Create and validate the controlled Sprint 15 migration.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/CustomerSuccessAccountConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/OnboardingPlanConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/SuccessPlanConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/CustomerHealthScoreConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/RenewalReadinessConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddCustomerSuccessCapabilities.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddCustomerSuccessCapabilities.Designer.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/CustomerSuccessMigrationTests.cs
```

---

## Phase 9: Customer-success authorization

### Objectives

- Define customer-success manager, onboarding manager and renewal reviewer policies.
- Require organization authorization for customer-facing records.
- Keep internal risk notes and commercial forecasts restricted.
- Audit privileged lifecycle, health and renewal actions.

### Files to create

```text
/apps/api/NoviqLabs.Application/Authorization/CustomerSuccessManagerRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/OnboardingManagerRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/RenewalReviewerRequirement.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/CustomerSuccessAuthorizationHandlers.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Authorization/CustomerSuccessAuthorizationTests.cs
/docs/security/customer-success-authorization.md
```

---

## Phase 10: Onboarding templates

### Objectives

- Create controlled onboarding templates by approved service or product.
- Define required, optional and conditional steps.
- Version templates without rewriting active plans.
- Require accessibility, security and ownership guidance in relevant steps.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Onboarding/OnboardingTemplate.cs
/apps/api/NoviqLabs.Application/Onboarding/CreateOnboardingTemplateCommand.cs
/apps/api/NoviqLabs.Application/Onboarding/InstantiateOnboardingPlanCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Onboarding/CreateOnboardingTemplateEndpoint.cs
/apps/web/src/features/admin/onboarding/OnboardingTemplateEditor.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Onboarding/OnboardingTemplateTests.cs
/docs/customer-success/onboarding-template-governance.md
```

---

## Phase 11: Customer onboarding workspace

### Objectives

- Implement an organization-scoped onboarding workspace.
- Show progress, owners, target dates, dependencies and approved guidance.
- Allow authorized customers to complete assigned steps and provide evidence.
- Keep internal tasks and notes hidden.

### Files to create

```text
/apps/web/src/app/(account)/onboarding/page.tsx
/apps/web/src/features/onboarding/CustomerOnboardingPage.tsx
/apps/web/src/features/onboarding/OnboardingProgress.tsx
/apps/web/src/features/onboarding/OnboardingStepList.tsx
/apps/web/src/features/onboarding/OnboardingEvidenceUpload.tsx
/apps/web/src/features/onboarding/CustomerOnboardingPage.test.tsx
/docs/customer-success/customer-onboarding-workspace.md
```

---

## Phase 12: Onboarding administration

### Objectives

- Allow authorized staff to create, assign, sequence and update onboarding plans.
- Require reasons for skipped or waived required steps.
- Track overdue and blocked steps.
- Record lifecycle and assignment history.

### Files to create

```text
/apps/api/NoviqLabs.Application/Onboarding/CreateOnboardingPlanCommand.cs
/apps/api/NoviqLabs.Application/Onboarding/UpdateOnboardingStepCommand.cs
/apps/api/NoviqLabs.Application/Onboarding/WaiveOnboardingStepCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Onboarding/CreateOnboardingPlanEndpoint.cs
/apps/web/src/app/(admin)/admin/onboarding/page.tsx
/apps/web/src/features/admin/onboarding/OnboardingAdministrationPage.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Onboarding/OnboardingAdministrationTests.cs
```

---

## Phase 13: Success-plan management

### Objectives

- Implement creation, review and update of customer success plans.
- Allow authorized customers to view approved objectives and progress.
- Preserve internal account-management notes separately.
- Notify participants of material checkpoint changes.

### Files to create

```text
/apps/api/NoviqLabs.Application/CustomerSuccess/CreateSuccessPlanCommand.cs
/apps/api/NoviqLabs.Application/CustomerSuccess/UpdateSuccessCheckpointCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/CustomerSuccess/CreateSuccessPlanEndpoint.cs
/apps/web/src/app/(account)/success-plan/page.tsx
/apps/web/src/features/customer-success/SuccessPlanPage.tsx
/apps/web/src/features/customer-success/SuccessObjectiveList.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/CustomerSuccess/SuccessPlanTests.cs
```

---

## Phase 14: Customer-health calculation

### Objectives

- Calculate health on a controlled schedule and after approved material events.
- Use versioned, explainable signal weights.
- Handle missing data without falsely lowering health.
- Require human review for high-impact escalations.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/CustomerHealthCalculationJob.cs
/apps/worker/NoviqLabs.Worker/Services/CustomerHealthSignalCollector.cs
/apps/api/NoviqLabs.Application/CustomerSuccess/GetCustomerHealthQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/CustomerSuccess/GetCustomerHealthEndpoint.cs
/tests/worker/NoviqLabs.Worker.UnitTests/CustomerHealthCalculationJobTests.cs
/docs/customer-success/customer-health-operations.md
```

---

## Phase 15: Customer-success dashboard

### Objectives

- Implement a restricted staff dashboard for lifecycle, onboarding, health, support and renewal readiness.
- Show signal explanations and freshness.
- Prevent cross-organization leakage.
- Provide filters with bounded ranges and accessible summaries.

### Files to create

```text
/apps/web/src/app/(admin)/admin/customer-success/page.tsx
/apps/web/src/features/admin/customer-success/CustomerSuccessDashboardPage.tsx
/apps/web/src/features/admin/customer-success/CustomerHealthSummary.tsx
/apps/web/src/features/admin/customer-success/OnboardingPortfolio.tsx
/apps/web/src/features/admin/customer-success/RenewalReadinessPanel.tsx
/apps/web/src/features/admin/customer-success/CustomerSuccessDashboardPage.test.tsx
```

---

## Phase 16: Adoption insights

### Objectives

- Create organization-scoped adoption summaries from approved product and workflow events.
- Use aggregated signals and respect analytics consent boundaries.
- Exclude message, document and confidential free-text contents.
- Show limitations and freshness.

### Files to create

```text
/apps/api/NoviqLabs.Application/CustomerSuccess/GetAdoptionInsightsQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/CustomerSuccess/GetAdoptionInsightsEndpoint.cs
/apps/web/src/features/customer-success/AdoptionInsights.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/CustomerSuccess/AdoptionInsightsTests.cs
/docs/customer-success/adoption-insights.md
```

---

## Phase 17: Customer education and guided adoption

### Objectives

- Deliver approved contextual guidance and knowledge content.
- Use customer lifecycle and enabled capabilities without revealing restricted data.
- Allow users to dismiss optional guidance.
- Prevent guidance from replacing support or security escalation.

### Files to create

```text
/apps/web/src/features/customer-success/GuidedAdoptionPanel.tsx
/apps/web/src/features/customer-success/ContextualGuidance.tsx
/apps/web/src/lib/customer-success/guidance-selection.ts
/apps/web/src/lib/customer-success/guidance-selection.test.ts
/packages/cms-schema/src/documents/adoption-guide.ts
/docs/customer-success/guided-adoption.md
```

---

## Phase 18: Lifecycle communications

### Objectives

- Send onboarding, checkpoint, inactivity and renewal-readiness communications through approved workflows.
- Respect communication preferences and operational-notice rules.
- Avoid sensitive health or risk details in insecure channels.
- Queue delivery and record status independently from lifecycle truth.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Templates/OnboardingReminderNotification.cs
/apps/worker/NoviqLabs.Worker/Templates/SuccessCheckpointNotification.cs
/apps/worker/NoviqLabs.Worker/Templates/RenewalReadinessNotification.cs
/apps/worker/NoviqLabs.Worker/Jobs/CustomerLifecycleNotificationJob.cs
/tests/worker/NoviqLabs.Worker.UnitTests/CustomerLifecycleNotificationJobTests.cs
/docs/notifications/customer-lifecycle-notifications.md
```

---

## Phase 19: Risk review and intervention

### Objectives

- Create controlled risk review and intervention workflows.
- Require evidence, owner, due date and review status.
- Prevent automated punitive action from health scores.
- Escalate support, security, payment or delivery issues to the authoritative workflow.

### Files to create

```text
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerRiskReview.cs
/apps/api/NoviqLabs.Domain/CustomerSuccess/CustomerIntervention.cs
/apps/api/NoviqLabs.Application/CustomerSuccess/CreateRiskReviewCommand.cs
/apps/api/NoviqLabs.Application/CustomerSuccess/CompleteInterventionCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/CustomerSuccess/CreateRiskReviewEndpoint.cs
/apps/web/src/features/admin/customer-success/RiskReviewPanel.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/CustomerSuccess/RiskReviewTests.cs
```

---

## Phase 20: Renewal-readiness workflow

### Objectives

- Generate renewal-review windows from authoritative contract and subscription dates.
- Present approved usage, support, delivery and payment context.
- Require human review before customer contact or commercial action.
- Keep forecast and contract truth separate.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/RenewalReadinessJob.cs
/apps/api/NoviqLabs.Application/CustomerSuccess/GetRenewalReadinessQuery.cs
/apps/api/NoviqLabs.Application/CustomerSuccess/CompleteRenewalReviewCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/CustomerSuccess/GetRenewalReadinessEndpoint.cs
/apps/web/src/features/admin/customer-success/RenewalReviewWorkspace.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/CustomerSuccess/RenewalReadinessTests.cs
/docs/customer-success/renewal-review-workflow.md
```

---

## Phase 21: Customer outcome reporting

### Objectives

- Report success-plan objectives, onboarding progress, adoption and approved outcome measures.
- Separate customer-visible outcomes from internal risk analysis.
- Preserve metric definitions and baseline context.
- Never claim causation unsupported by evidence.

### Files to create

```text
/apps/api/NoviqLabs.Application/Reporting/GetCustomerOutcomeReportQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Reporting/GetCustomerOutcomeReportEndpoint.cs
/apps/web/src/features/reporting/CustomerOutcomeReport.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Reporting/CustomerOutcomeReportTests.cs
/docs/customer-success/customer-outcome-reporting.md
```

---

## Phase 22: Customer-success audit trails

### Objectives

- Audit lifecycle, owner, onboarding, success-plan, health review, risk and renewal actions.
- Record actor, organization, action, result, timestamp and correlation identifier.
- Exclude sensitive notes and signal contents from audit records.
- Restrict access and define retention.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Audit/CustomerSuccessAuditEvent.cs
/apps/api/NoviqLabs.Domain/Audit/CustomerSuccessAuditAction.cs
/apps/api/NoviqLabs.Application/Audit/ICustomerSuccessAuditWriter.cs
/apps/api/NoviqLabs.Infrastructure/Audit/CustomerSuccessAuditWriter.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Audit/CustomerSuccessAuditTests.cs
/docs/security/customer-success-audit-trails.md
```

---

## Phase 23: Privacy and fairness review

### Objectives

- Review customer-health and adoption inputs for necessity, proportionality and explainability.
- Exclude protected, intrusive and unsupported inferred attributes.
- Provide correction and review procedures for inaccurate source data.
- Document retention and access controls.
- Test organization isolation and export boundaries.

### Files to create

```text
/docs/privacy/customer-success-data-inventory.md
/docs/privacy/customer-health-fairness-review.md
/docs/privacy/customer-success-retention.md
/scripts/privacy/verify-customer-success-controls.zsh
/tests/api/NoviqLabs.Api.IntegrationTests/Privacy/CustomerSuccessPrivacyTests.cs
/docs/evidence/sprint-15-privacy-fairness-review.md
```

---

## Phase 24: Security testing

### Objectives

- Test customer-success authorization, tenant isolation and internal-note boundaries.
- Test health-signal manipulation and unauthorized lifecycle changes.
- Test onboarding evidence and customer-outcome export access.
- Resolve all critical and high-risk findings.

### Files to create

```text
/apps/web/tests/security/customer-success-route-isolation.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Security/CustomerSuccessAuthorizationTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/CustomerHealthManipulationTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/OnboardingEvidenceAccessTests.cs
/scripts/security/scan-sprint-15-customer-success.zsh
/docs/evidence/sprint-15-security-results.md
```

---

## Phase 25: Accessibility and usability

### Objectives

- Validate onboarding, success plans, adoption guidance and customer-success administration.
- Verify keyboard operation, focus, status, progress and error messaging.
- Test mobile, tablet, desktop and 200 percent zoom.
- Conduct representative customer and customer-success-manager tasks.
- Resolve all blocking defects.

### Files to create

```text
/apps/web/tests/accessibility/customer-onboarding.spec.ts
/apps/web/tests/accessibility/success-plan.spec.ts
/apps/web/tests/accessibility/customer-success-dashboard.spec.ts
/apps/web/tests/accessibility/renewal-review.spec.ts
/apps/web/tests/usability/sprint-15-customer-tasks.spec.ts
/apps/web/tests/usability/sprint-15-customer-success-tasks.spec.ts
/docs/evidence/sprint-15-accessibility-usability.md
```

---

## Phase 26: Integration and end-to-end testing

### Objectives

- Test onboarding plan creation through customer completion.
- Test success plans, health calculation, risk review and renewal readiness.
- Test notifications, adoption guidance and outcome reporting.
- Test missing data, delayed jobs and notification failures.
- Verify audit completeness.

### Files to create

```text
/apps/web/tests/e2e/customer-onboarding-lifecycle.spec.ts
/apps/web/tests/e2e/success-plan-lifecycle.spec.ts
/apps/web/tests/e2e/customer-health-review.spec.ts
/apps/web/tests/e2e/customer-risk-intervention.spec.ts
/apps/web/tests/e2e/renewal-readiness.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Resilience/CustomerSuccessFailureTests.cs
/docs/evidence/sprint-15-end-to-end-results.md
```

---

## Phase 27: Performance and scale validation

### Objectives

- Measure customer-success dashboard, health calculation and onboarding latency.
- Load test portfolio views and lifecycle jobs.
- Verify customer-success analytics do not starve transactional workflows.
- Test job backlog and recovery.
- Record capacity and scaling recommendations.

### Files to create

```text
/tests/load/sprint-15-customer-success-dashboard.js
/tests/load/sprint-15-health-calculation.js
/tests/load/sprint-15-onboarding.js
/scripts/quality/validate-sprint-15-performance.zsh
/docs/evidence/sprint-15-performance-results.md
```

---

## Phase 28: CI/CD customer-success gates

### Objectives

- Add migration, authorization, health, onboarding, privacy, accessibility, security and load checks.
- Preserve evidence as workflow artifacts.
- Block unreviewed health-policy changes.
- Build verified web, API and worker images only after all gates pass.

### Files to create

```text
/.github/workflows/ci-customer-success.yml
/.github/workflows/test-customer-health.yml
/.github/workflows/test-customer-success-privacy.yml
/.github/workflows/test-customer-success-accessibility.yml
/.github/workflows/test-customer-success-security.yml
/.github/workflows/test-customer-success-load.yml
/.github/workflows/validate-customer-success-migration.yml
/scripts/ci/verify-sprint-15-customer-success.zsh
/scripts/ci/verify-sprint-15-quality-gates.zsh
/docs/delivery/sprint-15-quality-gates.md
```

---

## Phase 29: Azure infrastructure and staging deployment

### Objectives

- Provision approved queues, alerts, storage and worker scaling through infrastructure as code.
- Apply the Sprint 15 migration through the controlled migration job.
- Deploy verified web, API and worker images to development and staging.
- Verify telemetry, privacy boundaries, health jobs and notifications.
- Keep production access behind feature flags and role allowlists.

### Files to create

```text
/infrastructure/azure/modules/customer-success-queues.bicep
/infrastructure/azure/modules/customer-success-alerts.bicep
/infrastructure/azure/config/customer-success-worker-scaling.json
/infrastructure/azure/config/customer-success-alert-thresholds.json
/.github/workflows/deploy-customer-success-staging.yml
/scripts/cloud/deploy-sprint-15-staging.zsh
/scripts/cloud/smoke-test-sprint-15-customer-success.zsh
/docs/evidence/sprint-15-staging-deployment.md
```

---

## Phase 30: Controlled production rollout

### Objectives

- Deploy through the approved production release process.
- Use feature flags and allowlists for pilot organizations and operators.
- Verify lifecycle, onboarding, health, privacy, notifications, monitoring and rollback.
- Monitor error budgets and transactional performance.
- Disable or roll back if agreed thresholds are breached.

### Files to create

```text
/.github/workflows/deploy-sprint-15-production.yml
/scripts/cloud/deploy-sprint-15-production.zsh
/scripts/cloud/verify-sprint-15-production.zsh
/scripts/operations/monitor-customer-success-rollout.zsh
/docs/release/sprint-15-customer-success-rollout.md
/docs/evidence/sprint-15-production-deployment.md
/docs/evidence/sprint-15-rollout-stabilization.md
```

---

## Phase 31: Documentation, training and handover

### Objectives

- Document onboarding, success-plan, health, risk, renewal and customer-communication procedures.
- Train authorized customer-success, support, product and operations users.
- Verify least-privilege access after training.
- Document support boundaries and review dates.
- Keep terminal procedures Zsh-compatible for Kali Debian.

### Files to create

```text
/docs/customer-success/customer-onboarding-guide.md
/docs/customer-success/customer-success-manager-guide.md
/docs/customer-success/customer-health-operator-guide.md
/docs/customer-success/renewal-review-guide.md
/docs/operations/customer-success-runbook.md
/docs/training/sprint-15-training-record.md
/docs/development/sprint-15-kali-debian-zsh.md
/docs/evidence/sprint-15-handover-verification.md
```

---

## Phase 32: Integrated validation and sprint closure

### Objectives

- Validate every customer-success capability from a clean checkout.
- Execute build, migration, unit, integration, end-to-end, accessibility, privacy, fairness, security and load tests.
- Verify staging and controlled production rollout evidence.
- Verify tenant isolation, financial truth, privacy and security remain intact.
- Create and push the verified Sprint 15 Git commit.
- Create a pull request only after all required validations pass.
- Stop at the Sprint 15 completion gate.

### Files to create

```text
/scripts/release/sprint-15-final-validation.zsh
/docs/evidence/sprint-15-onboarding-summary.md
/docs/evidence/sprint-15-success-plan-summary.md
/docs/evidence/sprint-15-customer-health-summary.md
/docs/evidence/sprint-15-renewal-summary.md
/docs/evidence/sprint-15-accessibility-summary.md
/docs/evidence/sprint-15-performance-summary.md
/docs/evidence/sprint-15-security-privacy-summary.md
/docs/evidence/sprint-15-deployment-summary.md
/docs/evidence/sprint-15-completion-record.md
/docs/delivery/sprint-15-pull-request.md
```

---

## Development Sprint 15 Completion Gate

Development Sprint 15 is complete only when every condition below passes:

- Sprint 14 completion and production-health verification pass.
- Customer-success records are strictly organization scoped.
- Lifecycle stages, owners and history are complete and auditable.
- Onboarding templates are versioned and do not rewrite active plans.
- Customer and internal onboarding tasks remain correctly separated.
- Required onboarding steps cannot complete without approved evidence.
- Success plans contain measurable outcomes, owners and checkpoints.
- Customer-health calculations are explainable, versioned and reviewable.
- Protected, intrusive and unsupported inferred attributes are excluded from health calculations.
- Missing data does not produce misleading negative health outcomes.
- Automated health scores do not trigger punitive or commercial actions without human review.
- Customer-success dashboards prevent cross-organization access.
- Adoption insights enforce consent and data-minimization boundaries.
- Guided adoption remains optional and does not replace support or security escalation.
- Lifecycle communications respect preferences and do not expose sensitive risk details.
- Risk review and intervention workflows are evidence-based and auditable.
- Renewal readiness uses authoritative contract and subscription dates.
- Renewal forecasts do not modify commercial truth.
- Customer outcome reporting avoids unsupported causal claims.
- Customer-success audit trails are complete and protected.
- Privacy and fairness review passes.
- Security testing finds no unresolved critical or high-risk issue.
- Accessibility and usability checks pass.
- Performance and load budgets pass.
- CI/CD customer-success gates pass.
- Development, staging and controlled production rollout checks pass.
- Customer-success access remains pilot-restricted until expansion approval.
- Documentation, training and ownership handover are complete.
- A verified Development Sprint 15 Git commit exists.
- The Development Sprint 15 branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- The production platform remains live, secure, monitored and recoverable.

## Development Sprint 15 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_15_COMPLETE
NOVIQ_LABS_CUSTOMER_SUCCESS_PLATFORM_ACTIVE
```
