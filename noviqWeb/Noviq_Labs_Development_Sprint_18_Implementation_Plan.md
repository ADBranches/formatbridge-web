# Noviq Labs Full-Stack Platform

## Development Sprint 18: Workflow Automation and Intelligent Orchestration

**Sprint position:** Governed post-launch automation sprint after the Responsible AI Assistance pilot  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure production environment with controlled automation rollout  
**Architecture:** Durable, event-driven workflow orchestration with human approval and compensating controls

## Sprint Objective

Implement secure, durable workflow automation for repetitive operational processes without allowing automation to bypass authorization, financial truth, security controls or human review. The sprint will deliver versioned workflow definitions, approved triggers and actions, durable execution, retries and compensation, approval tasks, secure connectors, operational templates, an accessible workflow designer, operations console, audit trails and a controlled production pilot.

---

## Phase 1: Sprint Entry and Automation Readiness

### Objectives

- Verify Sprint 17 completion, production health, AI pilot safeguards, error budgets and approved automation demand.

### Files to create

```text
/docs/evidence/sprint-18-entry-verification.md
/docs/automation/sprint-18-scope.md
/docs/automation/readiness-register.md
/docs/delivery/sprint-18-branch-record.md
```

---

## Phase 2: Workflow Automation Architecture

### Objectives

- Define workflow, trigger, action, approval, retry, compensation and audit boundaries without bypassing authoritative domain rules.

### Files to create

```text
/docs/architecture/workflow-automation-context.md
/docs/architecture/workflow-execution-flows.md
/docs/architecture/automation-trust-boundaries.md
/docs/architecture/adr/0054-use-durable-workflow-orchestration.md
/docs/architecture/adr/0055-require-approval-for-consequential-automation.md
```

---

## Phase 3: Workflow Domain Model

### Objectives

- Create workflow definitions, versions, instances, steps, transitions and terminal states with immutable execution history.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Automation/WorkflowDefinition.cs
/apps/api/NoviqLabs.Domain/Automation/WorkflowVersion.cs
/apps/api/NoviqLabs.Domain/Automation/WorkflowInstance.cs
/apps/api/NoviqLabs.Domain/Automation/WorkflowStep.cs
/apps/api/NoviqLabs.Domain/Automation/WorkflowStatus.cs
/apps/api/NoviqLabs.Domain/Automation/AutomationErrors.cs
```

---

## Phase 4: Trigger and Action Model

### Objectives

- Create approved trigger, condition and action types while preventing arbitrary code, SQL or unrestricted network execution.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Automation/WorkflowTrigger.cs
/apps/api/NoviqLabs.Domain/Automation/WorkflowCondition.cs
/apps/api/NoviqLabs.Domain/Automation/WorkflowAction.cs
/apps/api/NoviqLabs.Domain/Automation/ActionType.cs
/docs/automation/trigger-action-catalogue.md
```

---

## Phase 5: Approval and Human Task Model

### Objectives

- Create approval tasks, assignments, decisions, due dates and escalation rules for consequential workflow steps.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Automation/ApprovalTask.cs
/apps/api/NoviqLabs.Domain/Automation/ApprovalDecision.cs
/apps/api/NoviqLabs.Domain/Automation/HumanTask.cs
/apps/api/NoviqLabs.Domain/Automation/HumanTaskStatus.cs
/docs/automation/human-approval-lifecycle.md
```

---

## Phase 6: Persistence and Migration

### Objectives

- Map workflow, execution, approval and automation entities to PostgreSQL with concurrency controls and indexes.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/WorkflowDefinitionConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/WorkflowInstanceConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ApprovalTaskConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddWorkflowAutomation.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddWorkflowAutomation.Designer.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/WorkflowAutomationMigrationTests.cs
```

---

## Phase 7: Workflow Authorization

### Objectives

- Define automation designer, publisher, operator and approver policies while preserving organization, project, finance and security authorization.

### Files to create

```text
/apps/api/NoviqLabs.Application/Authorization/AutomationDesignerRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/AutomationPublisherRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/AutomationOperatorRequirement.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/AutomationAuthorizationHandlers.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Authorization/AutomationAuthorizationTests.cs
```

---

## Phase 8: Workflow Definition Validation

### Objectives

- Validate graphs, transitions, cycles, timeouts, permissions and compensating actions before publication.

### Files to create

```text
/apps/api/NoviqLabs.Application/Automation/WorkflowDefinitionValidator.cs
/apps/api/NoviqLabs.Application/Automation/WorkflowGraphValidator.cs
/apps/api/NoviqLabs.Application/Automation/WorkflowPolicyValidator.cs
/tests/api/NoviqLabs.Api.UnitTests/Automation/WorkflowDefinitionValidatorTests.cs
/docs/automation/workflow-validation.md
```

---

## Phase 9: Durable Workflow Engine

### Objectives

- Implement durable execution with checkpoints, leases, idempotency and deterministic state transitions.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/WorkflowEngine.cs
/apps/worker/NoviqLabs.Worker/Automation/WorkflowExecutionContext.cs
/apps/worker/NoviqLabs.Worker/Automation/WorkflowCheckpointStore.cs
/apps/worker/NoviqLabs.Worker/Jobs/WorkflowExecutionJob.cs
/tests/worker/NoviqLabs.Worker.UnitTests/WorkflowExecutionJobTests.cs
```

---

## Phase 10: Retry, Timeout and Compensation

### Objectives

- Apply bounded retries, timeouts, cancellation and compensating actions without duplicating financial or external effects.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/WorkflowRetryPolicy.cs
/apps/worker/NoviqLabs.Worker/Automation/WorkflowTimeoutService.cs
/apps/worker/NoviqLabs.Worker/Automation/WorkflowCompensationService.cs
/tests/worker/NoviqLabs.Worker.UnitTests/WorkflowCompensationTests.cs
/docs/automation/retry-timeout-compensation.md
```

---

## Phase 11: Event Trigger Integration

### Objectives

- Start approved workflows from versioned domain events using idempotent event consumption and tenant scoping.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/WorkflowEventSubscriber.cs
/apps/worker/NoviqLabs.Worker/Automation/WorkflowTriggerMatcher.cs
/apps/api/NoviqLabs.Infrastructure/Automation/WorkflowEventInbox.cs
/tests/worker/NoviqLabs.Worker.UnitTests/WorkflowEventTriggerTests.cs
```

---

## Phase 12: Scheduled Trigger Integration

### Objectives

- Execute approved time-based workflows with time-zone awareness, misfire handling and duplicate-run prevention.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/ScheduledWorkflowJob.cs
/apps/worker/NoviqLabs.Worker/Automation/ScheduleCalculator.cs
/apps/api/NoviqLabs.Domain/Automation/WorkflowSchedule.cs
/tests/worker/NoviqLabs.Worker.UnitTests/ScheduledWorkflowJobTests.cs
```

---

## Phase 13: Action Connector Framework

### Objectives

- Create controlled connectors for notifications, support, projects, customer success and approved partner APIs.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/IWorkflowActionHandler.cs
/apps/worker/NoviqLabs.Worker/Automation/WorkflowActionRegistry.cs
/apps/worker/NoviqLabs.Worker/Automation/Handlers/NotificationActionHandler.cs
/apps/worker/NoviqLabs.Worker/Automation/Handlers/SupportActionHandler.cs
/apps/worker/NoviqLabs.Worker/Automation/Handlers/ProjectActionHandler.cs
/tests/worker/NoviqLabs.Worker.UnitTests/WorkflowActionRegistryTests.cs
```

---

## Phase 14: Secure HTTP Connector

### Objectives

- Implement allowlisted outbound HTTP actions with SSRF defenses, scoped credentials, signing and response limits.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/Handlers/SecureHttpActionHandler.cs
/apps/worker/NoviqLabs.Worker/Automation/SecureHttpDestinationPolicy.cs
/apps/worker/NoviqLabs.Worker/Automation/HttpActionCredentialResolver.cs
/tests/worker/NoviqLabs.Worker.UnitTests/SecureHttpActionHandlerTests.cs
/docs/security/workflow-http-connectors.md
```

---

## Phase 15: Workflow Template Catalogue

### Objectives

- Create versioned templates for onboarding, support escalation, project reminders, collection reminders and customer-success follow-up.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Automation/WorkflowTemplate.cs
/apps/api/NoviqLabs.Application/Automation/WorkflowTemplateCatalogue.cs
/apps/api/NoviqLabs.Application/Automation/InstantiateWorkflowTemplateCommand.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Automation/WorkflowTemplateTests.cs
/docs/automation/workflow-template-catalogue.md
```

---

## Phase 16: Onboarding Automation

### Objectives

- Automate approved reminders, assignments and evidence checks while keeping completion decisions authoritative and reviewable.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/Templates/OnboardingWorkflowTemplate.cs
/apps/api/NoviqLabs.Application/Onboarding/StartOnboardingAutomationCommand.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Automation/OnboardingAutomationTests.cs
/docs/automation/onboarding-automation.md
```

---

## Phase 17: Support Escalation Automation

### Objectives

- Automate acknowledgement, routing, follow-up and escalation without changing severity or closing requests without authorized review.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/Templates/SupportEscalationWorkflowTemplate.cs
/apps/api/NoviqLabs.Application/Support/StartSupportEscalationWorkflowCommand.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Automation/SupportEscalationAutomationTests.cs
/docs/automation/support-escalation-automation.md
```

---

## Phase 18: Project Delivery Automation

### Objectives

- Automate milestone reminders, review requests and overdue follow-up without modifying deliverable approval decisions.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/Templates/ProjectDeliveryWorkflowTemplate.cs
/apps/api/NoviqLabs.Application/Projects/StartProjectDeliveryWorkflowCommand.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Automation/ProjectDeliveryAutomationTests.cs
/docs/automation/project-delivery-automation.md
```

---

## Phase 19: Customer Success Automation

### Objectives

- Automate approved onboarding, checkpoint and renewal follow-up while preserving human review for health and risk interventions.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/Templates/CustomerSuccessWorkflowTemplate.cs
/apps/api/NoviqLabs.Application/CustomerSuccess/StartCustomerSuccessWorkflowCommand.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Automation/CustomerSuccessAutomationTests.cs
/docs/automation/customer-success-automation.md
```

---

## Phase 20: Billing Reminder Automation

### Objectives

- Automate invoice and payment reminders without initiating charges, changing balances or making unsupported commitments.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Automation/Templates/BillingReminderWorkflowTemplate.cs
/apps/api/NoviqLabs.Application/Billing/StartBillingReminderWorkflowCommand.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Automation/BillingReminderAutomationTests.cs
/docs/automation/billing-reminder-automation.md
```

---

## Phase 21: AI-Assisted Workflow Drafting

### Objectives

- Allow governed AI to draft workflow definitions from approved requirements while requiring validation and human publication approval.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/DraftWorkflowDefinitionCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/ArtificialIntelligence/DraftWorkflowDefinitionEndpoint.cs
/apps/web/src/features/automation/AiWorkflowDraft.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/WorkflowDraftTests.cs
/docs/automation/ai-assisted-workflow-drafting.md
```

---

## Phase 22: Workflow Designer

### Objectives

- Implement an accessible visual and form-based workflow designer with validation, version comparison and draft preservation.

### Files to create

```text
/apps/web/src/app/(admin)/admin/automation/page.tsx
/apps/web/src/features/automation/WorkflowDesignerPage.tsx
/apps/web/src/features/automation/WorkflowStepEditor.tsx
/apps/web/src/features/automation/WorkflowValidationPanel.tsx
/apps/web/src/features/automation/WorkflowVersionDiff.tsx
/apps/web/src/features/automation/WorkflowDesignerPage.test.tsx
```

---

## Phase 23: Workflow Publication and Versioning

### Objectives

- Implement review, approval, publication, pause, retirement and rollback of workflow versions.

### Files to create

```text
/apps/api/NoviqLabs.Application/Automation/PublishWorkflowCommand.cs
/apps/api/NoviqLabs.Application/Automation/PauseWorkflowCommand.cs
/apps/api/NoviqLabs.Application/Automation/RollbackWorkflowVersionCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Automation/PublishWorkflowEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Automation/WorkflowPublicationTests.cs
```

---

## Phase 24: Operations Console

### Objectives

- Provide authorized visibility into running, waiting, failed, compensated and completed workflow instances.

### Files to create

```text
/apps/web/src/app/(admin)/admin/automation/operations/page.tsx
/apps/web/src/features/automation/WorkflowOperationsPage.tsx
/apps/web/src/features/automation/WorkflowInstanceDetail.tsx
/apps/web/src/features/automation/WorkflowFailurePanel.tsx
/apps/api/NoviqLabs.Api/Endpoints/Automation/GetWorkflowOperationsEndpoint.cs
```

---

## Phase 25: Manual Intervention and Replay

### Objectives

- Allow authorized operators to retry, cancel, resume or compensate eligible steps with reasons and safeguards.

### Files to create

```text
/apps/api/NoviqLabs.Application/Automation/RetryWorkflowStepCommand.cs
/apps/api/NoviqLabs.Application/Automation/CancelWorkflowCommand.cs
/apps/api/NoviqLabs.Application/Automation/ResumeWorkflowCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Automation/RetryWorkflowStepEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Automation/WorkflowInterventionTests.cs
```

---

## Phase 26: Automation Audit Trails

### Objectives

- Audit definition, publication, execution, approval, intervention and connector actions without logging secrets or sensitive payloads.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Audit/AutomationAuditEvent.cs
/apps/api/NoviqLabs.Domain/Audit/AutomationAuditAction.cs
/apps/api/NoviqLabs.Application/Audit/IAutomationAuditWriter.cs
/apps/api/NoviqLabs.Infrastructure/Audit/AutomationAuditWriter.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Audit/AutomationAuditTests.cs
/docs/security/automation-audit-trails.md
```

---

## Phase 27: Automation Security Testing

### Objectives

- Test privilege escalation, cross-tenant execution, SSRF, replay, forged events, secret exposure and approval bypass.

### Files to create

```text
/tests/api/NoviqLabs.Api.IntegrationTests/Security/WorkflowAuthorizationTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/WorkflowTenantIsolationTests.cs
/tests/worker/NoviqLabs.Worker.UnitTests/WorkflowSsrfDefenseTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/WorkflowReplayTests.cs
/scripts/security/scan-sprint-18-automation.zsh
/docs/evidence/sprint-18-security-results.md
```

---

## Phase 28: Privacy and Data-Minimization Review

### Objectives

- Verify workflow payloads, logs, retention, connectors and exports contain only necessary authorized data.

### Files to create

```text
/docs/privacy/automation-data-inventory.md
/docs/privacy/automation-processing-record.md
/docs/privacy/automation-retention.md
/scripts/privacy/verify-automation-data-controls.zsh
/tests/api/NoviqLabs.Api.IntegrationTests/Privacy/AutomationPrivacyTests.cs
/docs/evidence/sprint-18-privacy-review.md
```

---

## Phase 29: Accessibility and Usability Validation

### Objectives

- Validate designer, approvals, operations and failure recovery with keyboard and assistive technology.

### Files to create

```text
/apps/web/tests/accessibility/workflow-designer.spec.ts
/apps/web/tests/accessibility/workflow-approvals.spec.ts
/apps/web/tests/accessibility/workflow-operations.spec.ts
/apps/web/tests/usability/sprint-18-automation-designer-tasks.spec.ts
/apps/web/tests/usability/sprint-18-automation-operator-tasks.spec.ts
/docs/evidence/sprint-18-accessibility-usability.md
```

---

## Phase 30: End-to-End and Resilience Testing

### Objectives

- Test trigger-to-completion, approvals, retries, compensation, pause, rollback and dependency failures.

### Files to create

```text
/apps/web/tests/e2e/onboarding-automation.spec.ts
/apps/web/tests/e2e/support-escalation-automation.spec.ts
/apps/web/tests/e2e/project-delivery-automation.spec.ts
/apps/web/tests/e2e/workflow-approval.spec.ts
/apps/web/tests/e2e/workflow-failure-recovery.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Resilience/WorkflowDependencyFailureTests.cs
/docs/evidence/sprint-18-end-to-end-results.md
```

---

## Phase 31: Performance and Scale Validation

### Objectives

- Measure trigger, execution, approval and connector latency while proving automation cannot starve critical workloads.

### Files to create

```text
/tests/load/sprint-18-workflow-triggers.js
/tests/load/sprint-18-workflow-execution.js
/tests/load/sprint-18-approval-queues.js
/scripts/quality/validate-sprint-18-performance.zsh
/docs/evidence/sprint-18-performance-results.md
```

---

## Phase 32: CI/CD Automation Quality Gates

### Objectives

- Add migration, graph validation, idempotency, connector, approval, privacy, accessibility, security and load checks.

### Files to create

```text
/.github/workflows/ci-workflow-automation.yml
/.github/workflows/test-workflow-idempotency.yml
/.github/workflows/test-workflow-connectors.yml
/.github/workflows/test-automation-security.yml
/.github/workflows/test-automation-accessibility.yml
/.github/workflows/test-automation-load.yml
/scripts/ci/verify-sprint-18-automation.zsh
/scripts/ci/verify-sprint-18-quality-gates.zsh
/docs/delivery/sprint-18-quality-gates.md
```

---

## Phase 33: Azure Infrastructure and Staging Deployment

### Objectives

- Provision workflow queues, state, alerts and scaling through infrastructure as code and deploy verified artifacts to staging.

### Files to create

```text
/infrastructure/azure/modules/workflow-queues.bicep
/infrastructure/azure/modules/workflow-alerts.bicep
/infrastructure/azure/config/workflow-worker-scaling.json
/infrastructure/azure/config/workflow-alert-thresholds.json
/.github/workflows/deploy-automation-staging.yml
/scripts/cloud/deploy-sprint-18-staging.zsh
/scripts/cloud/smoke-test-sprint-18-automation.zsh
/docs/evidence/sprint-18-staging-deployment.md
```

---

## Phase 34: Controlled Production Pilot

### Objectives

- Deploy approved templates behind feature flags and allowlists with monitoring, pause and rollback controls.

### Files to create

```text
/.github/workflows/deploy-sprint-18-production.yml
/scripts/cloud/deploy-sprint-18-production.zsh
/scripts/cloud/verify-sprint-18-production.zsh
/scripts/operations/monitor-automation-pilot.zsh
/docs/release/sprint-18-automation-pilot-rollout.md
/docs/evidence/sprint-18-production-deployment.md
/docs/evidence/sprint-18-rollout-stabilization.md
```

---

## Phase 35: Documentation, Training and Handover

### Objectives

- Document workflow design, approval, operations, connectors, incidents and recovery; train authorized operators.

### Files to create

```text
/docs/automation/workflow-designer-guide.md
/docs/automation/workflow-approver-guide.md
/docs/operations/workflow-operator-runbook.md
/docs/operations/workflow-incident-response.md
/docs/operations/workflow-recovery.md
/docs/training/sprint-18-training-record.md
/docs/development/sprint-18-kali-debian-zsh.md
/docs/evidence/sprint-18-handover-verification.md
```

---

## Phase 36: Integrated Validation and Sprint Closure

### Objectives

- Validate all workflow-automation capabilities, create and push the verified Sprint 18 commit, and open a pull request only after every gate passes.

### Files to create

```text
/scripts/release/sprint-18-final-validation.zsh
/docs/evidence/sprint-18-engine-summary.md
/docs/evidence/sprint-18-templates-summary.md
/docs/evidence/sprint-18-approval-summary.md
/docs/evidence/sprint-18-accessibility-summary.md
/docs/evidence/sprint-18-performance-summary.md
/docs/evidence/sprint-18-security-privacy-summary.md
/docs/evidence/sprint-18-deployment-summary.md
/docs/evidence/sprint-18-completion-record.md
/docs/delivery/sprint-18-pull-request.md
```

---

## Development Sprint 18 Completion Gate

Development Sprint 18 is complete only when every condition below passes:

- Sprint 17 completion and production-health verification pass.
- Workflow definitions are versioned, validated, approved and auditable.
- Arbitrary code, SQL and unrestricted network execution remain prohibited.
- Automation authorization preserves organization, project, finance and security boundaries.
- Durable execution uses checkpoints, leases and idempotent transitions.
- Retries and replay cannot duplicate payments, notifications or external effects.
- Timeouts, cancellation and compensation behave predictably.
- Event and scheduled triggers prevent duplicate workflow starts.
- Secure HTTP connectors enforce destination allowlists and SSRF defenses.
- Consequential workflow steps require approved human review.
- Rejected approval tasks cannot alter authoritative records.
- Onboarding automation cannot waive mandatory controls automatically.
- Support automation cannot change severity or close requests without authorization.
- Project automation cannot approve deliverables.
- Customer-success automation cannot trigger punitive action from health scores.
- Billing automation cannot initiate charges or change balances.
- AI-assisted workflow drafts require validation and human publication approval.
- Workflow publication, pause, retirement and rollback work correctly.
- Manual intervention is authorized, reasoned and audited.
- Automation audit trails are complete and protected.
- Privacy and data-minimization review passes.
- Security testing finds no unresolved critical or high-risk issue.
- Accessibility and usability checks pass.
- End-to-end, compensation and failure-recovery tests pass.
- Performance and load-isolation budgets pass.
- CI/CD workflow-automation quality gates pass.
- Development, staging and controlled production pilot checks pass.
- Automation access remains feature-flagged and allowlisted until expansion approval.
- Documentation, training and ownership handover are complete.
- A verified Development Sprint 18 Git commit exists.
- The Development Sprint 18 branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- The production platform remains live, secure, monitored and recoverable.

## Development Sprint 18 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_18_COMPLETE
NOVIQ_LABS_WORKFLOW_AUTOMATION_PILOT_ACTIVE
```
