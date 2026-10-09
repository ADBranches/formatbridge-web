# Noviq Labs Full-Stack Platform

## Development Sprint 6: Content Management and Editorial Administration

**Sprint position:** Sixth production implementation sprint after the verified complete public website  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure development and staging environments  
**Architecture:** Modular monolith with a separated headless editorial-content boundary  
**Application stack:** Next.js, React, TypeScript, ASP.NET Core, C#, PostgreSQL, Redis, Docker and Microsoft Azure

## Sprint Objective

Integrate the approved headless content-management system and establish secure editorial administration for the complete Noviq Labs public website. The sprint will implement controlled content schemas, roles, approvals, revision history, scheduling, preview, webhooks, media governance, content migration, search and sitemap synchronization, editorial audit records and operational recovery. The CMS will manage editorial content only and will not become the system of record for customer accounts, enquiries, projects, payments, security evidence or other transactional business data.

---

## Phase 1: Sprint Entry and Dependency Verification

### Objectives

- Verify that Development Sprint 5 passed every completion-gate requirement.
- Confirm the verified Sprint 5 Git commit, pushed development branch and approved pull-request state.
- Confirm the complete public website remains healthy in development and staging.
- Re-run required content, route, search, accessibility, performance, privacy, security and deployment checks.
- Inspect the current repository, public content models and deployment configuration before modifying files.
- Confirm the selected headless CMS, hosting model, licensing, regional availability and administrative ownership.
- Create the Development Sprint 6 branch only after entry verification passes.
- Stop the sprint if the CMS decision is unresolved or a blocking Sprint 5 regression remains.

### Files to create

```text
/docs/evidence/sprint-6-entry-verification.md
/docs/cms/cms-selection-record.md
/docs/cms/cms-access-prerequisites.md
/docs/cms/sprint-6-scope.md
/docs/delivery/sprint-6-branch-record.md
```

---

## Phase 2: CMS Architecture and System Boundaries

### Objectives

- Define the CMS as the source of truth for approved editorial content only.
- Keep customer accounts, organizations, enquiries, projects, payments, security evidence and audit-critical business records outside the CMS.
- Document the trust boundary between the CMS, Next.js frontend, ASP.NET Core API, Blob Storage and identity systems.
- Define preview, publication, revalidation and failure behavior.
- Prevent direct browser access to privileged CMS credentials.
- Record the selected CMS architecture as an approved decision.

### Files to create

```text
/docs/architecture/cms-context.md
/docs/architecture/cms-data-boundaries.md
/docs/architecture/cms-trust-boundary.md
/docs/architecture/adr/0023-use-headless-cms.md
/docs/architecture/adr/0024-separate-editorial-and-transactional-data.md
/docs/architecture/adr/0025-use-server-side-cms-access.md
/docs/cms/publication-lifecycle.md
```

---

## Phase 3: CMS Workspace and Environment Configuration

### Objectives

- Create separate CMS environments for development, staging and production.
- Keep production publishing credentials isolated from development and staging.
- Define environment-specific project, space, dataset or repository identifiers according to the selected CMS.
- Validate required configuration without exposing secrets to the browser.
- Load privileged CMS configuration through Azure Key Vault.
- Provide safe local environment examples for Kali Debian and Zsh.

### Files to create

```text
/apps/web/src/lib/cms/cms-env.ts
/apps/web/src/lib/cms/cms-env.test.ts
/apps/web/src/lib/cms/cms-config.ts
/apps/web/src/lib/cms/cms-config.test.ts
/apps/web/.env.cms.example
/infrastructure/azure/config/cms-secret-names.json
/infrastructure/azure/modules/cms-key-vault-secrets.bicep
/docs/cms/environment-configuration.md
/docs/development/cms-kali-debian-zsh.md
```

---

## Phase 4: CMS Client and Server-Side Access Layer

### Objectives

- Implement one controlled server-side CMS client.
- Separate published-content access from authenticated preview access.
- Add request timeouts, cancellation, retry boundaries and safe error handling.
- Prevent privileged tokens from entering client bundles, browser storage or public logs.
- Add correlation identifiers and privacy-safe telemetry.
- Provide typed response boundaries before content reaches page components.

### Files to create

```text
/apps/web/src/lib/cms/client.ts
/apps/web/src/lib/cms/preview-client.ts
/apps/web/src/lib/cms/client-options.ts
/apps/web/src/lib/cms/cms-errors.ts
/apps/web/src/lib/cms/cms-telemetry.ts
/apps/web/src/lib/cms/index.ts
/apps/web/src/lib/cms/client.test.ts
/apps/web/src/lib/cms/preview-client.test.ts
/docs/cms/cms-client-governance.md
```

---

## Phase 5: Shared Editorial Schema Foundations

### Objectives

- Define shared fields for title, slug, summary, status, approval, author, revision, publication dates, metadata and media.
- Require publication status and approval state on every publishable record.
- Define reusable SEO, call-to-action, media, evidence and taxonomic structures.
- Prevent arbitrary HTML, script or executable content fields.
- Preserve compatibility with the approved frontend content contracts.
- Version schema changes and require migration review.

### Files to create

```text
/packages/cms-schema/package.json
/packages/cms-schema/tsconfig.json
/packages/cms-schema/src/index.ts
/packages/cms-schema/src/shared/document-fields.ts
/packages/cms-schema/src/shared/publication-status.ts
/packages/cms-schema/src/shared/approval-state.ts
/packages/cms-schema/src/shared/seo-fields.ts
/packages/cms-schema/src/shared/media-fields.ts
/packages/cms-schema/src/shared/call-to-action.ts
/packages/cms-schema/src/shared/evidence-reference.ts
/packages/cms-schema/src/shared/taxonomy-reference.ts
/packages/cms-schema/src/shared/index.ts
/docs/cms/schema-governance.md
```

---

## Phase 6: Corporate and Service Content Schemas

### Objectives

- Define CMS schemas for homepage, About, company, Services, individual service pages and Industries.
- Preserve the approved page hierarchy and required sections.
- Support controlled optional sections without permitting arbitrary layout construction.
- Require approved claims and evidence references where applicable.
- Prevent deletion of mandatory page records without administrative approval.
- Validate route and slug uniqueness.

### Files to create

```text
/packages/cms-schema/src/documents/homepage.ts
/packages/cms-schema/src/documents/about-page.ts
/packages/cms-schema/src/documents/company-page.ts
/packages/cms-schema/src/documents/services-page.ts
/packages/cms-schema/src/documents/service-detail.ts
/packages/cms-schema/src/documents/industries-page.ts
/packages/cms-schema/src/objects/service-capability.ts
/packages/cms-schema/src/objects/delivery-stage.ts
/packages/cms-schema/src/objects/industry-focus.ts
/packages/cms-schema/src/validation/corporate-validation.ts
/docs/cms/corporate-and-service-schemas.md
```

---

## Phase 7: Product, Portfolio and Case-Study Schemas

### Objectives

- Define CMS schemas for products, portfolio entries and case studies.
- Enforce controlled product readiness states.
- Require evidence references for quantitative case-study results.
- Support confidentiality classifications and client-identity disclosure controls.
- Require explicit labeling for concept, simulated, research and internal work.
- Prevent restricted records from public queries and previews without authorization.

### Files to create

```text
/packages/cms-schema/src/documents/product.ts
/packages/cms-schema/src/documents/portfolio-entry.ts
/packages/cms-schema/src/documents/case-study.ts
/packages/cms-schema/src/objects/product-status.ts
/packages/cms-schema/src/objects/project-classification.ts
/packages/cms-schema/src/objects/confidentiality-classification.ts
/packages/cms-schema/src/objects/measurable-result.ts
/packages/cms-schema/src/validation/product-validation.ts
/packages/cms-schema/src/validation/case-study-validation.ts
/docs/cms/product-and-evidence-schemas.md
```

---

## Phase 8: Insights, Careers and Supporting Content Schemas

### Objectives

- Define CMS schemas for insights, authors, careers content, opportunities, partnerships, contact and legal pages.
- Support controlled article blocks and approved content renderers only.
- Require publication and revision dates.
- Support opportunity open and closed states without collecting applications in the CMS.
- Control legal-document effective dates and approval references.
- Prevent unsupported biographies, vacancies or partnership claims.

### Files to create

```text
/packages/cms-schema/src/documents/insight.ts
/packages/cms-schema/src/documents/author.ts
/packages/cms-schema/src/documents/careers-page.ts
/packages/cms-schema/src/documents/opportunity.ts
/packages/cms-schema/src/documents/partnerships-page.ts
/packages/cms-schema/src/documents/contact-page.ts
/packages/cms-schema/src/documents/legal-document.ts
/packages/cms-schema/src/objects/article-blocks.ts
/packages/cms-schema/src/validation/insight-validation.ts
/packages/cms-schema/src/validation/legal-validation.ts
/docs/cms/insights-and-supporting-schemas.md
```

---

## Phase 9: Editorial Roles and Permissions

### Objectives

- Define least-privilege editorial roles.
- Separate content creation, review, publication, schema administration and platform administration.
- Restrict legal, security and product-status changes to approved roles.
- Require stronger controls for production publication.
- Prevent editors from administering identities, integrations or secrets.
- Document joiner, mover and leaver procedures for editorial access.

### Files to create

```text
/packages/cms-schema/src/security/editorial-roles.ts
/packages/cms-schema/src/security/content-permissions.ts
/packages/cms-schema/src/security/restricted-fields.ts
/packages/cms-schema/src/security/index.ts
/docs/cms/editorial-role-matrix.md
/docs/cms/editorial-access-lifecycle.md
/docs/security/cms-least-privilege.md
```

---

## Phase 10: Draft, Review and Approval Workflow

### Objectives

- Implement draft, review requested, changes requested, approved, scheduled, published, archived and withdrawn states.
- Prevent ordinary editors from self-approving restricted content.
- Require publication approval for evidence claims, legal content, security content and product readiness changes.
- Record reviewer, decision, timestamp and revision reference.
- Support return-for-changes with an auditable explanation.
- Prevent publication when required approvals are missing.

### Files to create

```text
/packages/cms-schema/src/workflows/editorial-state.ts
/packages/cms-schema/src/workflows/editorial-transition.ts
/packages/cms-schema/src/workflows/approval-requirements.ts
/packages/cms-schema/src/workflows/workflow-validation.ts
/packages/cms-schema/src/workflows/workflow-validation.test.ts
/packages/cms-schema/src/workflows/index.ts
/docs/cms/editorial-workflow.md
/docs/cms/restricted-content-approval.md
```

---

## Phase 11: Revision History and Audit Records

### Objectives

- Enable revision history for editorial records.
- Capture content creation, updates, review decisions, scheduling, publication, withdrawal and deletion events.
- Record actor reference, timestamp, environment, document identifier and revision identifier.
- Avoid placing access tokens or sensitive content in audit messages.
- Define retention and access rules for editorial audit records.
- Make audit records read-only to ordinary editors.

### Files to create

```text
/packages/cms-schema/src/audit/editorial-audit-event.ts
/packages/cms-schema/src/audit/editorial-audit-types.ts
/packages/cms-schema/src/audit/audit-sanitization.ts
/packages/cms-schema/src/audit/audit-sanitization.test.ts
/packages/cms-schema/src/audit/index.ts
/docs/cms/revision-history.md
/docs/cms/editorial-audit-records.md
/docs/privacy/cms-audit-retention.md
```

---

## Phase 12: Scheduled Publishing

### Objectives

- Implement scheduled publication and unpublication controls.
- Require valid future dates and an approved content state.
- Use a controlled worker or CMS-native scheduling mechanism according to the approved architecture.
- Handle missed, duplicate and failed schedule execution safely.
- Record schedule creation, change, cancellation and execution.
- Verify time-zone handling explicitly.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/ContentPublicationJob.cs
/apps/worker/NoviqLabs.Worker/Jobs/ContentPublicationJobOptions.cs
/apps/worker/NoviqLabs.Worker/Jobs/ContentPublicationJobResult.cs
/apps/worker/NoviqLabs.Worker/Services/CmsPublicationService.cs
/apps/worker/NoviqLabs.Worker/Services/ICmsPublicationService.cs
/tests/worker/NoviqLabs.Worker.UnitTests/ContentPublicationJobTests.cs
/packages/cms-schema/src/workflows/schedule-validation.ts
/docs/cms/scheduled-publishing.md
```

---

## Phase 13: Preview Mode

### Objectives

- Implement secure preview for authorized editors.
- Use short-lived signed preview sessions.
- Prevent preview tokens from appearing in URLs, analytics or logs where avoidable.
- Prevent unauthorized users from previewing drafts or restricted content.
- Display a persistent preview indicator and exit control.
- Ensure preview pages remain non-indexable and non-cacheable by public caches.

### Files to create

```text
/apps/web/src/app/api/cms/preview/route.ts
/apps/web/src/app/api/cms/preview/exit/route.ts
/apps/web/src/lib/cms/preview-session.ts
/apps/web/src/lib/cms/preview-session.test.ts
/apps/web/src/components/cms/PreviewBanner.tsx
/apps/web/src/components/cms/PreviewExitButton.tsx
/apps/web/src/components/cms/index.ts
/apps/web/tests/security/cms-preview-authorization.spec.ts
/docs/cms/preview-mode.md
```

---

## Phase 14: Publication Webhooks and Cache Revalidation

### Objectives

- Implement authenticated CMS publication webhooks.
- Verify webhook signatures and reject replayed or expired requests.
- Map content changes to specific cache tags and routes.
- Avoid full-site rebuilds when targeted revalidation is sufficient.
- Record successful and failed revalidation attempts.
- Handle duplicate webhook delivery idempotently.

### Files to create

```text
/apps/web/src/app/api/cms/webhooks/publish/route.ts
/apps/web/src/lib/cms/webhook-signature.ts
/apps/web/src/lib/cms/webhook-signature.test.ts
/apps/web/src/lib/cms/webhook-replay-protection.ts
/apps/web/src/lib/cms/revalidation-map.ts
/apps/web/src/lib/cms/revalidation-service.ts
/apps/web/src/lib/cms/revalidation-service.test.ts
/apps/web/tests/security/cms-webhook-security.spec.ts
/docs/cms/publication-webhooks.md
```

---

## Phase 15: CMS Query Layer

### Objectives

- Create typed queries for every public content type.
- Return published content only by default.
- Keep preview queries explicit and separately authorized.
- Centralize projection fields to avoid accidental sensitive-field retrieval.
- Apply deterministic ordering, pagination and relationship expansion limits.
- Test missing, malformed and unpublished content behavior.

### Files to create

```text
/apps/web/src/lib/cms/queries/homepage-query.ts
/apps/web/src/lib/cms/queries/corporate-queries.ts
/apps/web/src/lib/cms/queries/service-queries.ts
/apps/web/src/lib/cms/queries/product-queries.ts
/apps/web/src/lib/cms/queries/portfolio-queries.ts
/apps/web/src/lib/cms/queries/insight-queries.ts
/apps/web/src/lib/cms/queries/supporting-queries.ts
/apps/web/src/lib/cms/queries/legal-queries.ts
/apps/web/src/lib/cms/queries/query-fragments.ts
/apps/web/src/lib/cms/queries/index.ts
/apps/web/src/lib/cms/queries/queries.test.ts
/docs/cms/query-layer.md
```

---

## Phase 16: CMS Repository and Mapping Layer

### Objectives

- Map CMS responses into approved frontend content contracts.
- Prevent page components from depending directly on vendor-specific response shapes.
- Normalize missing optional values and reject missing required values.
- Preserve evidence, publication status and confidentiality controls.
- Support future CMS replacement without rewriting public page components.
- Test mapping for every content family.

### Files to create

```text
/apps/web/src/lib/cms/repositories/corporate-repository.ts
/apps/web/src/lib/cms/repositories/service-repository.ts
/apps/web/src/lib/cms/repositories/product-repository.ts
/apps/web/src/lib/cms/repositories/portfolio-repository.ts
/apps/web/src/lib/cms/repositories/insight-repository.ts
/apps/web/src/lib/cms/repositories/supporting-repository.ts
/apps/web/src/lib/cms/repositories/legal-repository.ts
/apps/web/src/lib/cms/repositories/repository.types.ts
/apps/web/src/lib/cms/repositories/index.ts
/apps/web/src/lib/cms/repositories/repositories.test.ts
/docs/cms/repository-and-mapping-layer.md
```

---

## Phase 17: Public Website CMS Integration

### Objectives

- Replace approved local content sources with CMS repository access.
- Preserve the complete Sprint 4 and Sprint 5 page behavior and design.
- Retain safe fallback behavior for temporary CMS unavailability where approved.
- Prevent stale unpublished content from remaining accessible after withdrawal.
- Keep metadata, sitemap, search index and structured data synchronized with published CMS content.
- Verify every public route against development and staging CMS environments.

### Files to create

```text
/apps/web/src/lib/content/content-source.ts
/apps/web/src/lib/content/content-source.types.ts
/apps/web/src/lib/content/cms-content-source.ts
/apps/web/src/lib/content/local-content-source.ts
/apps/web/src/lib/content/content-source.test.ts
/apps/web/src/lib/content/index.ts
/apps/web/tests/integration/cms-public-pages.spec.ts
/apps/web/tests/integration/cms-content-withdrawal.spec.ts
/docs/cms/public-website-integration.md
```

---

## Phase 18: Media Library Controls

### Objectives

- Configure approved image, video, document and brand-asset types.
- Require title, alternative text, ownership, source, approval and classification metadata.
- Restrict file type and maximum size.
- Remove or reject unsafe metadata where applicable.
- Integrate approved assets with Azure Blob Storage where required by the architecture.
- Prevent unapproved, quarantined or restricted media from rendering publicly.

### Files to create

```text
/packages/cms-schema/src/documents/media-asset.ts
/packages/cms-schema/src/objects/media-approval.ts
/packages/cms-schema/src/validation/media-validation.ts
/packages/cms-schema/src/validation/media-validation.test.ts
/apps/web/src/lib/cms/media/cms-media-mapper.ts
/apps/web/src/lib/cms/media/cms-media-url.ts
/apps/web/src/lib/cms/media/cms-media.test.ts
/scripts/media/validate-cms-media.zsh
/docs/cms/media-library-controls.md
/docs/security/cms-media-security.md
```

---

## Phase 19: Editorial Administration Interface

### Objectives

- Configure the CMS editorial workspace or studio according to the selected CMS.
- Organize content types by corporate, services, products, evidence, insights, supporting and legal groups.
- Provide clear status, validation and workflow indicators.
- Hide administrative and schema controls from ordinary editors.
- Provide contextual guidance for claims, evidence, accessibility and metadata.
- Keep the editorial interface separate from the future operational administration dashboard.

### Files to create

```text
/apps/cms/package.json
/apps/cms/tsconfig.json
/apps/cms/cms.config.ts
/apps/cms/cms.cli.ts
/apps/cms/src/index.ts
/apps/cms/src/navigation/desk-structure.ts
/apps/cms/src/navigation/content-groups.ts
/apps/cms/src/components/PublicationStatus.tsx
/apps/cms/src/components/ApprovalNotice.tsx
/apps/cms/src/components/EvidenceGuidance.tsx
/apps/cms/src/components/AccessibilityGuidance.tsx
/apps/cms/src/security/editorial-access.ts
/apps/cms/.env.example
/apps/cms/Dockerfile
/apps/cms/.dockerignore
/docs/cms/editorial-interface.md
```

---

## Phase 20: Content Migration and Seed Records

### Objectives

- Migrate approved Sprint 4 and Sprint 5 local content into the CMS.
- Preserve slugs, metadata, publication status, revisions and evidence references.
- Avoid migrating placeholder, draft or unsupported claims as published content.
- Make migration idempotent and reviewable.
- Verify source-to-target counts and required relationships.
- Produce a discrepancy report before switching the public site to CMS content.

### Files to create

```text
/scripts/cms/export-local-content.zsh
/scripts/cms/transform-local-content.zsh
/scripts/cms/import-cms-content.zsh
/scripts/cms/verify-cms-migration.zsh
/scripts/cms/rollback-cms-migration.zsh
/tools/cms-migration/package.json
/tools/cms-migration/src/export.ts
/tools/cms-migration/src/transform.ts
/tools/cms-migration/src/import.ts
/tools/cms-migration/src/verify.ts
/tools/cms-migration/src/types.ts
/docs/cms/content-migration-plan.md
/docs/evidence/sprint-6-content-migration.md
```

---

## Phase 21: Search Index and Sitemap Synchronization

### Objectives

- Rebuild the public search index from published CMS content only.
- Update sitemap generation from published and approved CMS routes only.
- Remove withdrawn, archived and restricted records promptly.
- Preserve deterministic URLs and canonical metadata.
- Trigger targeted rebuild or revalidation after content changes.
- Test search and sitemap consistency after publish, update and withdrawal events.

### Files to create

```text
/apps/web/src/lib/search/cms-search-source.ts
/apps/web/src/lib/search/cms-search-source.test.ts
/apps/web/src/lib/seo/cms-sitemap-source.ts
/apps/web/src/lib/seo/cms-sitemap-source.test.ts
/apps/worker/NoviqLabs.Worker/Jobs/SearchIndexRefreshJob.cs
/apps/worker/NoviqLabs.Worker/Jobs/SearchIndexRefreshJobOptions.cs
/tests/worker/NoviqLabs.Worker.UnitTests/SearchIndexRefreshJobTests.cs
/docs/cms/search-and-sitemap-synchronization.md
```

---

## Phase 22: CMS Failure and Degraded-Mode Behavior

### Objectives

- Define public-site behavior during CMS latency, timeout or outage.
- Serve safe cached published content where permitted.
- Never fall back to drafts, previews or unapproved local content.
- Provide safe editorial error messages without exposing tokens or vendor details.
- Add telemetry and alerts for repeated CMS failures.
- Document recovery and content-consistency checks.

### Files to create

```text
/apps/web/src/lib/cms/cms-resilience.ts
/apps/web/src/lib/cms/cms-resilience.test.ts
/apps/web/src/components/cms/CmsUnavailableState.tsx
/apps/web/src/components/cms/CmsUnavailableState.test.tsx
/apps/web/tests/resilience/cms-outage.spec.ts
/infrastructure/azure/modules/cms-alerts.bicep
/infrastructure/azure/config/cms-alert-thresholds.json
/docs/operations/cms-degraded-mode.md
/docs/operations/cms-recovery-runbook.md
```

---

## Phase 23: CMS Security Validation

### Objectives

- Verify privileged CMS tokens remain server-side and in Azure Key Vault.
- Verify preview and webhook authentication, replay protection and rate controls.
- Verify editorial role separation and restricted-field controls.
- Verify arbitrary HTML and script execution are blocked.
- Verify unpublished and restricted content cannot be enumerated publicly.
- Run dependency, container and configuration scans.
- Resolve all critical and high-risk findings before sprint closure.

### Files to create

```text
/apps/web/tests/security/cms-token-exposure.spec.ts
/apps/web/tests/security/cms-preview-session.spec.ts
/apps/web/tests/security/cms-webhook-replay.spec.ts
/apps/web/tests/security/cms-content-enumeration.spec.ts
/apps/cms/tests/editorial-permissions.spec.ts
/apps/cms/tests/restricted-fields.spec.ts
/scripts/security/scan-cms-application.zsh
/scripts/security/verify-cms-secrets.zsh
/docs/evidence/sprint-6-cms-security-scan.md
```

---

## Phase 24: CMS Accessibility and Editorial Usability Validation

### Objectives

- Verify public content rendered from the CMS preserves accessible headings, labels, alternative text and landmarks.
- Verify required media accessibility metadata is enforced.
- Verify the editorial interface supports keyboard operation for required workflows.
- Verify validation messages identify the field and recovery action.
- Conduct representative editor tasks for create, review, approve, schedule, publish and withdraw.
- Record defects and resolve all blocking editorial-usability issues.

### Files to create

```text
/apps/web/tests/accessibility/cms-rendered-content.spec.ts
/apps/web/tests/accessibility/cms-media-accessibility.spec.ts
/apps/cms/tests/accessibility/editorial-workflow.spec.ts
/apps/cms/tests/accessibility/schema-validation.spec.ts
/apps/cms/tests/usability/editorial-tasks.spec.ts
/docs/evidence/sprint-6-cms-accessibility.md
/docs/evidence/sprint-6-editorial-usability.md
```

---

## Phase 25: Integration and End-to-End Testing

### Objectives

- Test content creation through public rendering.
- Test draft, review, approval, scheduling, publication, update, withdrawal and archive workflows.
- Test preview authorization and preview exit.
- Test publication webhook and targeted revalidation.
- Test search and sitemap synchronization.
- Test audit-event creation for privileged editorial actions.
- Verify public behavior during CMS failure.

### Files to create

```text
/apps/web/tests/e2e/cms-publish-to-public.spec.ts
/apps/web/tests/e2e/cms-preview.spec.ts
/apps/web/tests/e2e/cms-scheduled-publication.spec.ts
/apps/web/tests/e2e/cms-content-withdrawal.spec.ts
/apps/web/tests/e2e/cms-search-synchronization.spec.ts
/apps/web/tests/e2e/cms-sitemap-synchronization.spec.ts
/apps/cms/tests/e2e/editorial-workflow.spec.ts
/apps/cms/tests/e2e/editorial-audit.spec.ts
/docs/evidence/sprint-6-cms-end-to-end-results.md
```

---

## Phase 26: Performance and Cache Validation

### Objectives

- Measure CMS query duration, page rendering, cache hit behavior and revalidation time.
- Verify published content remains within public performance budgets.
- Prevent excessive query expansion, over-fetching and unbounded result sets.
- Verify targeted revalidation does not rebuild unrelated content.
- Verify preview mode is uncached by public caches.
- Record staging performance evidence.

### Files to create

```text
/apps/web/tests/performance/cms-page-rendering.spec.ts
/apps/web/tests/performance/cms-query-limits.spec.ts
/apps/web/tests/performance/cms-revalidation.spec.ts
/apps/web/tests/performance/cms-preview-cache.spec.ts
/scripts/quality/validate-cms-performance.zsh
/scripts/quality/report-cms-query-performance.zsh
/docs/evidence/sprint-6-cms-performance.md
/docs/cms/query-performance-standard.md
```

---

## Phase 27: CI/CD Quality-Gate Expansion

### Objectives

- Add CMS schema, studio, migration, preview, webhook, accessibility, security and integration checks to pull-request validation.
- Build the CMS administrative application and public website in continuous integration.
- Validate schema changes and migration compatibility.
- Preserve complete evidence as workflow artifacts.
- Deploy CMS components only after all required checks pass.
- Fail the pipeline when any required underlying command fails.

### Files to create

```text
/.github/workflows/ci-cms-schema.yml
/.github/workflows/ci-cms-application.yml
/.github/workflows/test-cms-integration.yml
/.github/workflows/test-cms-accessibility.yml
/.github/workflows/test-cms-security.yml
/.github/workflows/validate-cms-migration.yml
/scripts/ci/verify-cms-schema.zsh
/scripts/ci/verify-cms-application.zsh
/scripts/ci/verify-cms-quality-gates.zsh
/docs/delivery/sprint-6-quality-gates.md
```

---

## Phase 28: Azure Infrastructure and Deployment

### Objectives

- Provision or configure the approved CMS administrative runtime and required Azure resources.
- Configure Key Vault, managed identities, network boundaries, telemetry and alerts.
- Deploy the CMS schema and administrative interface to development and staging.
- Migrate approved content and verify public rendering.
- Verify preview, webhook, schedule and rollback procedures.
- Keep production publication disabled until final production authorization.

### Files to create

```text
/infrastructure/azure/modules/cms-container-app.bicep
/infrastructure/azure/modules/cms-managed-identity.bicep
/infrastructure/azure/modules/cms-diagnostic-settings.bicep
/infrastructure/azure/config/cms-scaling.json
/.github/workflows/deploy-cms-development.yml
/.github/workflows/deploy-cms-staging.yml
/scripts/cloud/deploy-sprint-6-development.zsh
/scripts/cloud/deploy-sprint-6-staging.zsh
/scripts/cloud/smoke-test-cms.zsh
/scripts/cloud/verify-cms-staging.zsh
/docs/evidence/sprint-6-development-deployment.md
/docs/evidence/sprint-6-staging-deployment.md
```

---

## Phase 29: CMS Rollback and Recovery

### Objectives

- Define rollback for CMS application revisions, schema changes and content migration.
- Verify rollback does not erase valid editorial history.
- Preserve previous healthy public and CMS revisions during validation.
- Define forward-fix requirements for incompatible schema changes.
- Test restoration of CMS configuration and content from the approved backup mechanism.
- Record image, schema, migration and content revision evidence.

### Files to create

```text
/.github/workflows/rollback-cms.yml
/scripts/cloud/rollback-cms-revision.zsh
/scripts/cms/restore-cms-content.zsh
/scripts/cms/verify-cms-restore.zsh
/docs/operations/cms-rollback-runbook.md
/docs/operations/cms-content-restore-runbook.md
/docs/evidence/sprint-6-cms-rollback-verification.md
/docs/evidence/sprint-6-cms-restore-verification.md
```

---

## Phase 30: Editorial Documentation and Training

### Objectives

- Document content creation, review, approval, scheduling, publication, withdrawal and archive procedures.
- Document media preparation, alternative text, claims, evidence and legal-content requirements.
- Document role responsibilities and prohibited actions.
- Prepare concise editor and approver training materials.
- Document troubleshooting and escalation routes.
- Keep training aligned with the verified editorial interface.

### Files to create

```text
/docs/cms/editor-handbook.md
/docs/cms/approver-handbook.md
/docs/cms/schema-administrator-handbook.md
/docs/cms/media-preparation-guide.md
/docs/cms/claims-and-evidence-guide.md
/docs/cms/legal-content-guide.md
/docs/cms/editorial-troubleshooting.md
/docs/cms/editor-training-plan.md
/docs/cms/approver-training-plan.md
```

---

## Phase 31: Integrated Validation and Sprint Closure

### Objectives

- Validate the CMS schema, administrative application, public integration and worker jobs from a clean checkout.
- Verify content migration, preview, approval, scheduling, publication, withdrawal, search and sitemap synchronization.
- Execute all unit, integration, end-to-end, accessibility, usability, performance, security and deployment tests.
- Verify development and staging deployments, telemetry, alerts, rollback and restore.
- Verify no privileged token or draft content is exposed publicly.
- Confirm identity, project intake, customer portal and payment features have not been started outside approved scope.
- Update documentation to match the verified implementation.
- Create the verified Development Sprint 6 Git commit and push the development branch.
- Create a pull request only after every required validation passes.
- Stop at the Development Sprint 6 completion gate before beginning the next sprint.

### Files to create

```text
/scripts/release/sprint-6-final-validation.zsh
/docs/evidence/sprint-6-schema-validation.md
/docs/evidence/sprint-6-content-migration-summary.md
/docs/evidence/sprint-6-editorial-workflow-summary.md
/docs/evidence/sprint-6-preview-and-webhook-summary.md
/docs/evidence/sprint-6-accessibility-and-usability-summary.md
/docs/evidence/sprint-6-performance-summary.md
/docs/evidence/sprint-6-security-summary.md
/docs/evidence/sprint-6-deployment-summary.md
/docs/evidence/sprint-6-rollback-and-restore-summary.md
/docs/evidence/sprint-6-completion-record.md
/docs/delivery/sprint-6-pull-request.md
```

---


## Development Sprint 6 Completion Gate

Development Sprint 6 is complete only when every condition below passes:

- The approved headless CMS decision is recorded and implemented.
- Development and staging CMS environments are isolated and operational.
- CMS privileged credentials remain in Azure Key Vault and server-side boundaries.
- Editorial content and transactional business data remain separated.
- Corporate, service, product, portfolio, case-study, insight, careers, partnership, contact and legal schemas validate successfully.
- Publication status, approval state, evidence and confidentiality controls are enforced.
- Editorial roles and least-privilege permissions are enforced.
- Restricted content cannot be self-approved by ordinary editors.
- Draft, review, approval, scheduled, published, withdrawn and archived workflows operate correctly.
- Revision history and editorial audit records are retained.
- Scheduled publication and unpublication execute reliably and idempotently.
- Preview mode is authorized, non-indexable and non-cacheable by public caches.
- Publication webhooks verify signatures and resist replay.
- Targeted cache revalidation works.
- CMS queries return published content only by default.
- Vendor-specific CMS responses do not leak into page components.
- Approved Sprint 4 and Sprint 5 content is migrated accurately.
- Placeholder, unsupported and unapproved content is not migrated as published content.
- Public pages render correctly from CMS content.
- Search and sitemap output include only approved published content.
- Withdrawn and restricted content is removed from public discovery.
- Media-library type, size, ownership, approval and accessibility controls are enforced.
- CMS outage behavior serves only safe approved cached content where permitted.
- Editorial accessibility and usability tests pass.
- CMS integration and end-to-end workflows pass.
- CMS performance and cache budgets pass.
- CMS security checks pass with no unresolved critical or high-risk findings.
- Development and staging CMS deployments pass smoke tests.
- CMS telemetry and alerts reach the approved Azure monitoring resources.
- CMS application rollback is verified.
- CMS content restore is verified.
- Editorial and approver documentation matches the verified implementation.
- A verified Development Sprint 6 Git commit exists.
- The Development Sprint 6 development branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- No unresolved blocking defect remains.
- The next sprint has not started.

## Development Sprint 6 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_6_COMPLETE
```
