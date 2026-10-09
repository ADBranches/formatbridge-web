# Noviq Labs Full-Stack Platform

## Development Sprint 17: Responsible AI Assistance and Knowledge Automation

**Sprint position:** Governed post-launch innovation sprint after Regional Expansion and Market Readiness  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure production environment with a controlled AI pilot  
**Architecture:** Central server-side AI gateway with grounded retrieval, human review and strict data controls

## Sprint Objective

Introduce carefully governed AI assistance without allowing generated output to become authoritative business truth automatically. The sprint will deliver an Azure-hosted AI gateway, prompt governance, input redaction, output validation, scoped knowledge retrieval, grounded customer assistance, reviewed drafting for support, knowledge, projects and customer success, repeatable evaluations, adversarial testing, audit trails, quotas and a controlled production pilot. All capabilities must preserve tenant isolation, privacy, security, accessibility, financial correctness and reliable non-AI fallbacks.

---

## Phase 1: Sprint Entry and AI Readiness Verification

### Objectives

- Verify Sprint 16 completion evidence, Git state, production health and pilot-market stability.
- Review validated automation demand, support workload, content operations and customer-success use cases.
- Confirm approved AI provider, Azure region, data-processing terms, model availability and cost controls.
- Create the Sprint 17 branch only after security, privacy, legal and operational prerequisites pass.

### Files to create

```text
/docs/evidence/sprint-17-entry-verification.md
/docs/ai/sprint-17-scope.md
/docs/ai/use-case-readiness-register.md
/docs/ai/provider-readiness-register.md
/docs/delivery/sprint-17-branch-record.md
```

---

## Phase 2: Responsible AI Architecture

### Objectives

- Define AI gateway, retrieval, prompt, response, evaluation and audit boundaries.
- Keep authoritative business decisions in deterministic application workflows.
- Require human review for consequential customer, financial, security and legal actions.
- Document failure, fallback, disablement and provider-switching behavior.

### Files to create

```text
/docs/architecture/ai-assistance-context.md
/docs/architecture/ai-trust-boundaries.md
/docs/architecture/ai-data-flows.md
/docs/architecture/adr/0051-use-central-ai-gateway.md
/docs/architecture/adr/0052-require-human-review-for-consequential-ai-output.md
/docs/architecture/adr/0053-separate-ai-suggestions-from-authoritative-records.md
```

---

## Phase 3: AI Use-Case Governance

### Objectives

- Create an approved use-case register with owner, purpose, data classification and risk level.
- Define prohibited, restricted and low-risk use cases.
- Require measurable benefit, evaluation criteria and rollback plan.
- Prevent unreviewed AI features from reaching production.

### Files to create

```text
/docs/ai/ai-use-case-register.yaml
/docs/ai/prohibited-ai-use-cases.md
/docs/ai/ai-risk-classification.md
/tools/ai-governance/package.json
/tools/ai-governance/src/validate-use-cases.ts
/scripts/ai/validate-use-case-register.zsh
/.github/workflows/validate-ai-governance.yml
```

---

## Phase 4: AI Configuration Domain Model

### Objectives

- Create AI feature, provider configuration, model deployment, policy and status entities.
- Support disabled, evaluation, pilot, active, paused and retired states.
- Version configuration and preserve approval history.
- Prevent activation without evaluation and risk approval.

### Files to create

```text
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiFeature.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiProviderConfiguration.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiModelDeployment.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiFeatureStatus.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiPolicy.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiErrors.cs
```

---

## Phase 5: AI Interaction and Feedback Domain Model

### Objectives

- Create AI interaction, suggestion, citation, review decision and feedback entities.
- Associate interactions with authorized users and organizations where applicable.
- Separate prompts, generated suggestions and accepted business records.
- Define retention, redaction and deletion behavior.

### Files to create

```text
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiInteraction.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiSuggestion.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiCitation.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiReviewDecision.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiFeedback.cs
/docs/ai/ai-interaction-lifecycle.md
```

---

## Phase 6: Persistence and Migration

### Objectives

- Map AI configuration, interaction, review and feedback entities to PostgreSQL.
- Apply organization scope, classification, retention and status indexes.
- Avoid storing provider secrets or unnecessary raw sensitive content.
- Create and validate the controlled Sprint 17 migration.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/AiFeatureConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/AiInteractionConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/AiFeedbackConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddResponsibleAiCapabilities.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddResponsibleAiCapabilities.Designer.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/AiMigrationTests.cs
/docs/database/ai-capabilities-schema.md
```

---

## Phase 7: Azure AI Gateway

### Objectives

- Implement one server-side gateway for approved model deployments.
- Keep credentials in Azure Key Vault and use managed identity where supported.
- Apply timeouts, cancellation, quotas and safe retry boundaries.
- Normalize provider responses and prevent direct browser access to model credentials.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/IAiGateway.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/AiGatewayModels.cs
/apps/api/NoviqLabs.Infrastructure/ArtificialIntelligence/AzureAiGateway.cs
/apps/api/NoviqLabs.Infrastructure/ArtificialIntelligence/AzureAiGatewayOptions.cs
/apps/api/NoviqLabs.Infrastructure/ArtificialIntelligence/AiProviderException.cs
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/AiGatewayContractTests.cs
/docs/ai/azure-ai-gateway.md
```

---

## Phase 8: Prompt Template Governance

### Objectives

- Create versioned prompt templates with owner, purpose, inputs, outputs and risk classification.
- Separate system instructions from user content and retrieved evidence.
- Require review before activation.
- Prevent secrets and unrestricted HTML or executable instructions in templates.

### Files to create

```text
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/PromptTemplate.cs
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/PromptTemplateVersion.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/PromptTemplateService.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/PromptTemplateValidator.cs
/tests/api/NoviqLabs.Api.UnitTests/ArtificialIntelligence/PromptTemplateTests.cs
/docs/ai/prompt-template-governance.md
```

---

## Phase 9: Input Classification and Redaction

### Objectives

- Classify AI inputs before provider submission.
- Redact secrets, credentials, restricted-security evidence and prohibited personal data.
- Reject unsupported content classifications.
- Record redaction outcomes without retaining removed values.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/AiInputClassifier.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/AiInputRedactor.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/AiDataPolicy.cs
/tests/api/NoviqLabs.Api.UnitTests/ArtificialIntelligence/AiInputRedactorTests.cs
/scripts/security/test-ai-redaction.zsh
/docs/security/ai-input-protection.md
```

---

## Phase 10: Output Validation and Safety Filters

### Objectives

- Validate generated output against schema, length, classification and policy requirements.
- Block unsafe markup, unsupported claims and prohibited instructions.
- Require citations for evidence-based suggestions.
- Return safe fallback states when validation fails.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/AiOutputValidator.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/AiOutputPolicy.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/AiCitationValidator.cs
/tests/api/NoviqLabs.Api.UnitTests/ArtificialIntelligence/AiOutputValidatorTests.cs
/docs/security/ai-output-validation.md
```

---

## Phase 11: Knowledge Source and Retrieval Model

### Objectives

- Define approved knowledge sources, documents, chunks, access scope and freshness metadata.
- Exclude restricted sources unless the requesting user is independently authorized.
- Preserve source identifiers and revision references.
- Prevent retrieval from crossing organization or project boundaries.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Knowledge/KnowledgeSource.cs
/apps/api/NoviqLabs.Domain/Knowledge/KnowledgeDocument.cs
/apps/api/NoviqLabs.Domain/Knowledge/KnowledgeChunk.cs
/apps/api/NoviqLabs.Domain/Knowledge/KnowledgeAccessScope.cs
/apps/api/NoviqLabs.Domain/Knowledge/KnowledgeErrors.cs
/docs/ai/knowledge-source-governance.md
```

---

## Phase 12: Knowledge Ingestion Pipeline

### Objectives

- Ingest approved CMS, knowledge-base and operational documents.
- Verify file integrity, malware status, classification and source revision.
- Chunk and index content without losing access scope.
- Support idempotent refresh, withdrawal and rebuild.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/KnowledgeIngestionJob.cs
/apps/worker/NoviqLabs.Worker/Services/KnowledgeDocumentParser.cs
/apps/worker/NoviqLabs.Worker/Services/KnowledgeChunker.cs
/apps/worker/NoviqLabs.Worker/Services/KnowledgeIndexWriter.cs
/tests/worker/NoviqLabs.Worker.UnitTests/KnowledgeIngestionJobTests.cs
/docs/operations/knowledge-ingestion.md
```

---

## Phase 13: Vector Search Boundary

### Objectives

- Implement approved vector search behind a controlled repository interface.
- Apply authorization filters before returning candidate evidence.
- Limit result count, similarity threshold and payload size.
- Record source freshness and retrieval diagnostics without exposing protected content.

### Files to create

```text
/apps/api/NoviqLabs.Application/Knowledge/IKnowledgeSearchRepository.cs
/apps/api/NoviqLabs.Infrastructure/Knowledge/AzureKnowledgeSearchRepository.cs
/apps/api/NoviqLabs.Infrastructure/Knowledge/KnowledgeSearchOptions.cs
/apps/api/NoviqLabs.Application/Knowledge/KnowledgeSearchService.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Knowledge/KnowledgeSearchTests.cs
/docs/ai/vector-search-boundary.md
```

---

## Phase 14: Grounded Answer Service

### Objectives

- Generate answers only from approved retrieved evidence for selected experiences.
- Return source citations and uncertainty messaging.
- Refuse or redirect when evidence is missing, stale or unauthorized.
- Never convert suggestions directly into authoritative records.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/GroundedAnswerService.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/GroundedAnswerRequest.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/GroundedAnswerResponse.cs
/apps/api/NoviqLabs.Api/Endpoints/ArtificialIntelligence/CreateGroundedAnswerEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/GroundedAnswerTests.cs
/docs/ai/grounded-answer-service.md
```

---

## Phase 15: Customer Knowledge Assistant

### Objectives

- Implement an organization-scoped assistant for approved help and onboarding content.
- Show citations, limitations and clear escalation routes.
- Prevent access to internal notes, other organizations and restricted reports.
- Keep the assistant optional and accessible.

### Files to create

```text
/apps/web/src/app/(account)/assistant/page.tsx
/apps/web/src/features/assistant/CustomerKnowledgeAssistant.tsx
/apps/web/src/features/assistant/AssistantConversation.tsx
/apps/web/src/features/assistant/AssistantCitationList.tsx
/apps/web/src/features/assistant/AssistantEscalation.tsx
/apps/web/src/features/assistant/CustomerKnowledgeAssistant.test.tsx
/docs/ai/customer-knowledge-assistant.md
```

---

## Phase 16: Support Response Drafting

### Objectives

- Generate draft support responses from approved knowledge and ticket context.
- Require operator review and editing before sending.
- Exclude restricted security evidence and unsupported commitments.
- Record whether a draft was accepted, modified or rejected.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/DraftSupportResponseCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/ArtificialIntelligence/DraftSupportResponseEndpoint.cs
/apps/web/src/features/admin/support/AiSupportDraft.tsx
/apps/web/src/features/admin/support/AiDraftReviewControls.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/SupportDraftTests.cs
/docs/ai/support-response-drafting.md
```

---

## Phase 17: Knowledge Article Drafting

### Objectives

- Generate draft knowledge articles only from approved resolved cases and verified documentation.
- Require editorial review, evidence citations and publication workflow.
- Prevent customer-specific or confidential content from entering drafts.
- Keep CMS publication controls authoritative.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/DraftKnowledgeArticleCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/ArtificialIntelligence/DraftKnowledgeArticleEndpoint.cs
/apps/cms/src/components/AiKnowledgeDraftReview.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/KnowledgeDraftTests.cs
/docs/ai/knowledge-article-drafting.md
```

---

## Phase 18: Project Summary Drafting

### Objectives

- Generate project-summary drafts from authorized milestones, activity and deliverables.
- Exclude internal notes, restricted security details and unapproved financial data.
- Require project-manager review before customer visibility.
- Cite source records and freshness.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/DraftProjectSummaryCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/ArtificialIntelligence/DraftProjectSummaryEndpoint.cs
/apps/web/src/features/projects/AiProjectSummaryDraft.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/ProjectSummaryDraftTests.cs
/docs/ai/project-summary-drafting.md
```

---

## Phase 19: Customer Success Brief Drafting

### Objectives

- Generate internal briefing drafts from authorized onboarding, health, support and renewal evidence.
- Keep advisory health signals explainable.
- Exclude protected attributes and unsupported inferences.
- Require customer-success-manager review before use.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/DraftCustomerSuccessBriefCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/ArtificialIntelligence/DraftCustomerSuccessBriefEndpoint.cs
/apps/web/src/features/admin/customer-success/AiCustomerBriefDraft.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/CustomerBriefDraftTests.cs
/docs/ai/customer-success-brief-drafting.md
```

---

## Phase 20: Human Review Workflow

### Objectives

- Create review queues for AI suggestions requiring approval.
- Capture reviewer, decision, modifications, reason and timestamp.
- Prevent self-approval where separation of duties is required.
- Keep rejected suggestions from affecting business records.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/ReviewAiSuggestionCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/ArtificialIntelligence/ReviewAiSuggestionEndpoint.cs
/apps/web/src/app/(admin)/admin/ai/review/page.tsx
/apps/web/src/features/admin/ai/AiReviewQueue.tsx
/apps/web/src/features/admin/ai/AiReviewDecisionForm.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/AiReviewWorkflowTests.cs
```

---

## Phase 21: AI Feedback and Quality Signals

### Objectives

- Collect structured feedback on accuracy, relevance, grounding and usefulness.
- Avoid collecting unnecessary personal or confidential data.
- Separate user feedback from authoritative correctness labels.
- Use feedback only after governance review.

### Files to create

```text
/apps/api/NoviqLabs.Application/ArtificialIntelligence/SubmitAiFeedbackCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/ArtificialIntelligence/SubmitAiFeedbackEndpoint.cs
/apps/web/src/features/assistant/AiFeedbackControls.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/AiFeedbackTests.cs
/docs/ai/ai-feedback-governance.md
```

---

## Phase 22: Evaluation Framework

### Objectives

- Create repeatable offline evaluations for grounding, citation, policy compliance and task quality.
- Use approved synthetic and de-identified evaluation datasets.
- Define pass thresholds per use case.
- Block model or prompt changes that regress required metrics.

### Files to create

```text
/tools/ai-evaluation/package.json
/tools/ai-evaluation/src/run-evaluations.ts
/tools/ai-evaluation/src/metrics.ts
/tests/ai/datasets/grounded-answer-cases.json
/tests/ai/datasets/support-draft-cases.json
/scripts/ai/run-ai-evaluations.zsh
/docs/ai/evaluation-standard.md
```

---

## Phase 23: Adversarial and Prompt-Injection Testing

### Objectives

- Test direct and indirect prompt injection, data exfiltration and instruction override attempts.
- Test malicious retrieved documents and encoded payloads.
- Verify retrieval authorization and output filters remain effective.
- Resolve all critical and high-risk findings.

### Files to create

```text
/tests/ai/security/prompt-injection-cases.json
/tests/ai/security/retrieval-poisoning-cases.json
/scripts/security/test-ai-prompt-injection.zsh
/scripts/security/test-ai-data-exfiltration.zsh
/docs/evidence/sprint-17-ai-adversarial-testing.md
```

---

## Phase 24: AI Audit Trails

### Objectives

- Audit AI configuration, prompt versions, interactions, retrieval sources, reviews and privileged actions.
- Record model deployment, policy version, outcome and correlation identifier.
- Exclude secrets and unnecessary raw sensitive content from audit records.
- Define restricted access and retention.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Audit/AiAuditEvent.cs
/apps/api/NoviqLabs.Domain/Audit/AiAuditAction.cs
/apps/api/NoviqLabs.Application/Audit/IAiAuditWriter.cs
/apps/api/NoviqLabs.Infrastructure/Audit/AiAuditWriter.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Audit/AiAuditTests.cs
/docs/security/ai-audit-trails.md
```

---

## Phase 25: AI Cost and Quota Controls

### Objectives

- Track token, request and cost estimates by feature, organization and environment.
- Apply feature and organization quotas from approved budgets.
- Prevent cost controls from silently changing authoritative workflows.
- Alert on anomalies and disable non-critical features safely.

### Files to create

```text
/apps/api/NoviqLabs.Domain/ArtificialIntelligence/AiUsageRecord.cs
/apps/api/NoviqLabs.Application/ArtificialIntelligence/AiQuotaService.cs
/apps/worker/NoviqLabs.Worker/Jobs/AiUsageAggregationJob.cs
/infrastructure/azure/config/ai-quotas.json
/infrastructure/azure/config/ai-cost-alerts.json
/tests/api/NoviqLabs.Api.IntegrationTests/ArtificialIntelligence/AiQuotaTests.cs
/docs/operations/ai-cost-control.md
```

---

## Phase 26: Privacy and Responsible AI Review

### Objectives

- Document processing purposes, provider transfers, retention and user notices.
- Verify consent and lawful processing boundaries where applicable.
- Review explainability, human oversight, correction and contestability.
- Exclude prohibited sensitive data and unsupported profiling.

### Files to create

```text
/docs/privacy/ai-data-inventory.md
/docs/privacy/ai-processing-record.md
/docs/privacy/ai-retention-policy.md
/docs/ai/responsible-ai-impact-assessment.md
/scripts/privacy/verify-ai-data-controls.zsh
/docs/evidence/sprint-17-responsible-ai-review.md
```

---

## Phase 27: Accessibility and Usability Validation

### Objectives

- Validate assistant, citations, review queues, feedback and fallback states.
- Verify keyboard operation, focus, status announcements and readable source links.
- Test mobile, tablet, desktop and 200 percent zoom.
- Conduct representative customer and operator tasks.

### Files to create

```text
/apps/web/tests/accessibility/customer-assistant.spec.ts
/apps/web/tests/accessibility/ai-review-queue.spec.ts
/apps/web/tests/accessibility/ai-citations.spec.ts
/apps/web/tests/usability/sprint-17-customer-ai-tasks.spec.ts
/apps/web/tests/usability/sprint-17-operator-ai-tasks.spec.ts
/docs/evidence/sprint-17-accessibility-usability.md
```

---

## Phase 28: Integration, End-to-End and Failure Testing

### Objectives

- Test knowledge ingestion through grounded responses and citations.
- Test drafting, review, acceptance, modification and rejection workflows.
- Test provider timeout, quota exhaustion, stale index and feature disablement.
- Verify authoritative workflows remain available when AI is unavailable.

### Files to create

```text
/apps/web/tests/e2e/customer-assistant.spec.ts
/apps/web/tests/e2e/ai-support-draft.spec.ts
/apps/web/tests/e2e/ai-project-summary.spec.ts
/apps/web/tests/e2e/ai-review-workflow.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Resilience/AiProviderFailureTests.cs
/docs/evidence/sprint-17-end-to-end-results.md
```

---

## Phase 29: Performance and Scale Validation

### Objectives

- Measure gateway, retrieval, generation and review-queue latency.
- Load test bounded concurrent AI requests and ingestion jobs.
- Verify AI traffic cannot starve critical transactional workloads.
- Record quota, capacity and scaling recommendations.

### Files to create

```text
/tests/load/sprint-17-ai-gateway.js
/tests/load/sprint-17-knowledge-search.js
/tests/load/sprint-17-knowledge-ingestion.js
/scripts/quality/validate-sprint-17-performance.zsh
/docs/evidence/sprint-17-performance-results.md
```

---

## Phase 30: CI/CD AI Quality Gates

### Objectives

- Add governance, migration, redaction, evaluation, adversarial, privacy, accessibility, security and load checks.
- Block unapproved model, prompt and policy changes.
- Preserve evaluation and security evidence as workflow artifacts.
- Build verified artifacts only after every required gate passes.

### Files to create

```text
/.github/workflows/ci-responsible-ai.yml
/.github/workflows/test-ai-evaluations.yml
/.github/workflows/test-ai-security.yml
/.github/workflows/test-ai-privacy.yml
/.github/workflows/test-ai-accessibility.yml
/.github/workflows/test-ai-load.yml
/scripts/ci/verify-sprint-17-ai.zsh
/scripts/ci/verify-sprint-17-quality-gates.zsh
/docs/delivery/sprint-17-quality-gates.md
```

---

## Phase 31: Azure Infrastructure and Staging Deployment

### Objectives

- Provision approved Azure AI, search, queues, alerts and scaling through infrastructure as code.
- Apply the Sprint 17 migration through the controlled migration job.
- Deploy verified web, API and worker images to development and staging.
- Keep production AI features disabled until pilot approval.

### Files to create

```text
/infrastructure/azure/modules/azure-ai-services.bicep
/infrastructure/azure/modules/ai-search.bicep
/infrastructure/azure/modules/ai-queues.bicep
/infrastructure/azure/modules/ai-alerts.bicep
/infrastructure/azure/config/ai-worker-scaling.json
/.github/workflows/deploy-ai-staging.yml
/scripts/cloud/deploy-sprint-17-staging.zsh
/scripts/cloud/smoke-test-sprint-17-ai.zsh
/docs/evidence/sprint-17-staging-deployment.md
```

---

## Phase 32: Controlled Production Pilot

### Objectives

- Deploy through the approved production release process.
- Use feature flags, organization allowlists and role restrictions.
- Verify privacy, grounding, citations, review, quotas, monitoring and rollback.
- Disable AI features immediately when agreed thresholds are breached.

### Files to create

```text
/.github/workflows/deploy-sprint-17-production.yml
/scripts/cloud/deploy-sprint-17-production.zsh
/scripts/cloud/verify-sprint-17-production.zsh
/scripts/operations/monitor-ai-pilot.zsh
/docs/release/sprint-17-ai-pilot-rollout.md
/docs/evidence/sprint-17-production-deployment.md
/docs/evidence/sprint-17-rollout-stabilization.md
```

---

## Phase 33: Documentation, Training and Handover

### Objectives

- Document AI governance, knowledge ingestion, review, incident, privacy and operator procedures.
- Train authorized support, content, project and customer-success operators.
- Verify least-privilege access after training.
- Keep terminal procedures Zsh-compatible for Kali Debian.

### Files to create

```text
/docs/ai/ai-user-guide.md
/docs/ai/ai-reviewer-guide.md
/docs/operations/ai-operator-runbook.md
/docs/operations/ai-incident-response.md
/docs/operations/knowledge-index-recovery.md
/docs/training/sprint-17-training-record.md
/docs/development/sprint-17-kali-debian-zsh.md
/docs/evidence/sprint-17-handover-verification.md
```

---

## Phase 34: Integrated Validation and Sprint Closure

### Objectives

- Validate all responsible-AI capabilities from a clean checkout.
- Execute build, migration, evaluation, integration, end-to-end, accessibility, privacy, security and load tests.
- Verify staging and controlled production pilot evidence.
- Create and push the verified Sprint 17 Git commit and create a pull request only after all gates pass.

### Files to create

```text
/scripts/release/sprint-17-final-validation.zsh
/docs/evidence/sprint-17-governance-summary.md
/docs/evidence/sprint-17-knowledge-summary.md
/docs/evidence/sprint-17-assistant-summary.md
/docs/evidence/sprint-17-evaluation-summary.md
/docs/evidence/sprint-17-accessibility-summary.md
/docs/evidence/sprint-17-performance-summary.md
/docs/evidence/sprint-17-security-privacy-summary.md
/docs/evidence/sprint-17-deployment-summary.md
/docs/evidence/sprint-17-completion-record.md
/docs/delivery/sprint-17-pull-request.md
```

---

## Development Sprint 17 Completion Gate

Development Sprint 17 is complete only when every condition below passes:

- Sprint 16 completion and production-health verification pass.
- Every AI use case is approved, owned, risk-classified and reversible.
- Prohibited AI use cases remain blocked.
- Model credentials remain server-side and protected by Azure Key Vault.
- AI inputs are classified and restricted data is redacted or rejected.
- AI outputs pass schema, citation, policy and unsafe-content validation.
- Knowledge sources are approved, current, classified and access scoped.
- Knowledge retrieval cannot cross organization, project or restricted-data boundaries.
- Grounded answers provide valid source citations and uncertainty handling.
- Customer assistance remains optional and has clear escalation routes.
- Support, knowledge, project and customer-success drafts require human review.
- Rejected AI suggestions cannot alter authoritative records.
- Human review decisions and modifications are auditable.
- Evaluation datasets are approved, synthetic or appropriately de-identified.
- Required grounding, policy and task-quality thresholds pass.
- Prompt-injection, retrieval-poisoning and data-exfiltration tests pass.
- AI audit trails are complete and protected.
- Usage, quota and cost controls operate correctly.
- Privacy and responsible-AI review passes.
- Accessibility and usability checks pass.
- Provider-failure tests prove critical non-AI workflows remain available.
- Performance and load-isolation budgets pass.
- CI/CD responsible-AI quality gates pass.
- Development, staging and controlled production pilot checks pass.
- AI access remains feature-flagged and allowlisted until expansion approval.
- Documentation, training and ownership handover are complete.
- No unresolved critical or high-risk finding remains.
- A verified Development Sprint 17 Git commit exists.
- The Development Sprint 17 branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- The production platform remains live, secure, monitored and recoverable.

## Development Sprint 17 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_17_COMPLETE
NOVIQ_LABS_RESPONSIBLE_AI_ASSISTANCE_PILOT_ACTIVE
```
