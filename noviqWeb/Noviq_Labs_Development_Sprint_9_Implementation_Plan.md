# Noviq Labs Full-Stack Platform

## Development Sprint 9: Customer Portal and Project Management

**Sprint position:** Ninth production implementation sprint after verified lead generation and project intake  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure development and staging environments  
**Architecture:** Modular monolith with organization-scoped and project-scoped authorization

## Sprint Objective

Implement the secure customer portal and end-to-end project-delivery workspace. The sprint will deliver the customer dashboard, project workspaces, project teams, milestones, secure documents, deliverable submission and approval, project messaging, support requests, notifications, activity history, security-engagement workflows and tightly controlled security-report delivery. Commercial, invoice, subscription and payment capabilities remain outside this sprint.

---

## Phase 1: Sprint Entry and Dependency Verification

### Objectives

- Verify that Development Sprint 8 passed every completion-gate requirement.
- Confirm the verified Sprint 8 Git commit, pushed development branch and approved pull-request state.
- Confirm identity, organizations, project intake, secure uploads, notifications, CMS and staging environments remain healthy.
- Inspect the current repository, database schema, authorization policies, Blob Storage, worker jobs and audit foundations before modifications.
- Confirm project-governance, deliverable-approval, document-retention, support and security-engagement requirements.
- Create the Development Sprint 9 branch only after all entry checks pass.
- Stop if a blocking dependency or unresolved critical or high-risk issue remains.

### Files to create

```text
/docs/evidence/sprint-9-entry-verification.md
/docs/projects/sprint-9-scope.md
/docs/projects/project-governance-prerequisites.md
/docs/projects/security-engagement-prerequisites.md
/docs/delivery/sprint-9-branch-record.md
```

---

## Phase 2: Customer Portal and Project Architecture

### Objectives

- Define customer portal, project, milestone, deliverable, messaging, support and security-report boundaries.
- Define conversion from qualified intake to active project through an authorized internal workflow.
- Preserve strict organization and project membership isolation.
- Define ownership between PostgreSQL, Blob Storage, notifications and audit records.
- Define customer-visible and internal-only information boundaries.
- Record asynchronous event, retention and recovery behavior.

### Files to create

```text
/docs/architecture/customer-portal-context.md
/docs/architecture/project-management-sequence-flows.md
/docs/architecture/project-data-boundaries.md
/docs/architecture/adr/0032-use-project-scoped-authorization.md
/docs/architecture/adr/0033-separate-customer-visible-and-internal-project-data.md
/docs/architecture/adr/0034-use-private-blob-storage-for-project-documents.md
```

---

## Phase 3: Project Domain Model

### Objectives

- Create project, project status, project member, service category and project lifecycle entities.
- Associate every project with exactly one authorized customer organization.
- Support draft, planned, active, on hold, completed, cancelled and archived states.
- Separate customer-visible summary from internal project administration.
- Preserve immutable identifiers and auditable lifecycle history.
- Prevent project activation without an authorized organization and assigned Noviq owner.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Projects/Project.cs
/apps/api/NoviqLabs.Domain/Projects/ProjectStatus.cs
/apps/api/NoviqLabs.Domain/Projects/ProjectMember.cs
/apps/api/NoviqLabs.Domain/Projects/ProjectMemberRole.cs
/apps/api/NoviqLabs.Domain/Projects/ProjectServiceCategory.cs
/apps/api/NoviqLabs.Domain/Projects/ProjectLifecycleEvent.cs
/apps/api/NoviqLabs.Domain/Projects/ProjectErrors.cs
/docs/projects/project-lifecycle.md
```

---

## Phase 4: Milestone and Delivery-Status Domain Model

### Objectives

- Create milestone, milestone status, target date, sequence and progress entities.
- Support planned, in progress, blocked, ready for review, completed and cancelled states.
- Preserve baseline and revised target dates.
- Separate customer-visible status notes from internal delivery detail.
- Prevent impossible transition and completion sequences.
- Record milestone history and responsible owners.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Projects/Milestone.cs
/apps/api/NoviqLabs.Domain/Projects/MilestoneStatus.cs
/apps/api/NoviqLabs.Domain/Projects/MilestoneDependency.cs
/apps/api/NoviqLabs.Domain/Projects/MilestoneHistory.cs
/apps/api/NoviqLabs.Domain/Projects/MilestoneErrors.cs
/docs/projects/milestone-lifecycle.md
```

---

## Phase 5: Deliverable and Approval Domain Model

### Objectives

- Create deliverable, deliverable version, submission, review and approval entities.
- Support draft, submitted, changes requested, approved, superseded and withdrawn states.
- Preserve authorship, version, integrity hash and submission timestamp.
- Require authorized customer approval for acceptance decisions.
- Prevent approved deliverables from being overwritten.
- Record decision comments and complete approval history.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Deliverables/Deliverable.cs
/apps/api/NoviqLabs.Domain/Deliverables/DeliverableVersion.cs
/apps/api/NoviqLabs.Domain/Deliverables/DeliverableStatus.cs
/apps/api/NoviqLabs.Domain/Deliverables/DeliverableReview.cs
/apps/api/NoviqLabs.Domain/Deliverables/ApprovalDecision.cs
/apps/api/NoviqLabs.Domain/Deliverables/DeliverableErrors.cs
/docs/projects/deliverable-approval-lifecycle.md
```

---

## Phase 6: Project Document Domain Model

### Objectives

- Create project document, document version, classification and access-grant entities.
- Associate every document with one project and approved audience.
- Support customer-shared, Noviq-internal, confidential and restricted-security classifications.
- Preserve integrity hashes, malware-scan status and retention metadata.
- Prevent public access and anonymous sharing.
- Record upload, access, download, replacement and deletion events.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Documents/ProjectDocument.cs
/apps/api/NoviqLabs.Domain/Documents/ProjectDocumentVersion.cs
/apps/api/NoviqLabs.Domain/Documents/DocumentClassification.cs
/apps/api/NoviqLabs.Domain/Documents/DocumentAccessGrant.cs
/apps/api/NoviqLabs.Domain/Documents/DocumentAuditEvent.cs
/apps/api/NoviqLabs.Domain/Documents/DocumentErrors.cs
/docs/projects/project-document-boundaries.md
```

---

## Phase 7: Messaging and Activity Domain Model

### Objectives

- Create project conversation, message, participant and activity-event entities.
- Restrict messages to authorized project participants.
- Separate ordinary project communication from restricted security communications.
- Preserve message ordering, edit restrictions and audit history.
- Prevent executable content and unsafe markup.
- Define notification and retention behavior.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Messaging/ProjectConversation.cs
/apps/api/NoviqLabs.Domain/Messaging/ProjectMessage.cs
/apps/api/NoviqLabs.Domain/Messaging/ConversationParticipant.cs
/apps/api/NoviqLabs.Domain/Messaging/MessageClassification.cs
/apps/api/NoviqLabs.Domain/Activity/ProjectActivityEvent.cs
/apps/api/NoviqLabs.Domain/Messaging/MessagingErrors.cs
/docs/projects/project-messaging-boundaries.md
```

---

## Phase 8: Support Request Domain Model

### Objectives

- Create support request, priority, category, status, assignment and response entities.
- Associate requests with an organization and optionally a project.
- Support new, acknowledged, in progress, waiting for customer, resolved and closed states.
- Keep severity separate from customer-selected priority.
- Prevent confidential security incidents from entering ordinary support queues.
- Record assignment and status history.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Support/SupportRequest.cs
/apps/api/NoviqLabs.Domain/Support/SupportStatus.cs
/apps/api/NoviqLabs.Domain/Support/SupportPriority.cs
/apps/api/NoviqLabs.Domain/Support/SupportCategory.cs
/apps/api/NoviqLabs.Domain/Support/SupportAssignment.cs
/apps/api/NoviqLabs.Domain/Support/SupportErrors.cs
/docs/support/support-request-lifecycle.md
```

---

## Phase 9: Security-Engagement Domain Model

### Objectives

- Create security engagement, scope, authorization reference, testing window and report entities.
- Require written authorization before an engagement can become active.
- Preserve target, scope, exclusion and testing-window versions.
- Separate security reports and evidence from ordinary project documents.
- Apply stricter participant and access requirements.
- Record every privileged action and report-delivery event.

### Files to create

```text
/apps/api/NoviqLabs.Domain/SecurityEngagements/SecurityEngagement.cs
/apps/api/NoviqLabs.Domain/SecurityEngagements/RulesOfEngagement.cs
/apps/api/NoviqLabs.Domain/SecurityEngagements/TestingWindow.cs
/apps/api/NoviqLabs.Domain/SecurityEngagements/SecurityReport.cs
/apps/api/NoviqLabs.Domain/SecurityEngagements/SecurityEvidence.cs
/apps/api/NoviqLabs.Domain/SecurityEngagements/SecurityEngagementErrors.cs
/docs/security-engagements/security-engagement-lifecycle.md
```

---

## Phase 10: Persistence and Database Migration

### Objectives

- Map project, milestone, deliverable, document, messaging, support and security-engagement entities to PostgreSQL.
- Apply organization and project scope to every relevant entity.
- Add concurrency tokens, indexes, unique constraints and lifecycle checks.
- Create the controlled Sprint 9 migration.
- Verify clean database application and upgrade behavior.
- Document forward-fix and rollback boundaries.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ProjectConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/MilestoneConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/DeliverableConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ProjectDocumentConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ProjectMessageConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/SupportRequestConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/SecurityEngagementConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddCustomerPortalAndProjectManagement.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddCustomerPortalAndProjectManagement.Designer.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/ProjectPortalMigrationTests.cs
/docs/database/customer-portal-schema.md
```

---

## Phase 11: Project-Scoped Authorization

### Objectives

- Define project member, project manager, customer reviewer, security engagement member and support operator policies.
- Require organization membership and explicit project membership where applicable.
- Keep backend authorization authoritative.
- Apply stronger policy to security reports and evidence.
- Prevent identifier-based cross-project access.
- Test removed and suspended membership behavior.

### Files to create

```text
/apps/api/NoviqLabs.Application/Authorization/ProjectMemberRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/ProjectManagerRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/CustomerReviewerRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/SecurityEngagementMemberRequirement.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/ProjectMemberHandler.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/ProjectManagerHandler.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/CustomerReviewerHandler.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/SecurityEngagementMemberHandler.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Authorization/ProjectAuthorizationTests.cs
/docs/security/project-scoped-authorization.md
```

---

## Phase 12: Intake-to-Project Conversion

### Objectives

- Implement an authorized internal workflow for converting a qualified intake into an active project draft.
- Copy only approved and relevant intake information.
- Link rather than duplicate protected intake files where appropriate.
- Require organization, project owner and service category.
- Make conversion idempotent.
- Record source intake and conversion audit events.

### Files to create

```text
/apps/api/NoviqLabs.Application/Projects/ConvertIntakeToProjectCommand.cs
/apps/api/NoviqLabs.Application/Projects/ConvertIntakeToProjectHandler.cs
/apps/api/NoviqLabs.Application/Projects/ConvertIntakeToProjectValidator.cs
/apps/api/NoviqLabs.Api/Endpoints/Projects/ConvertIntakeToProjectEndpoint.cs
/apps/api/NoviqLabs.Contracts/Projects/ConvertIntakeToProjectRequest.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Projects/IntakeConversionTests.cs
/docs/projects/intake-to-project-conversion.md
```

---

## Phase 13: Project Creation and Administration

### Objectives

- Implement project creation, update, activation, hold, completion and archive commands.
- Restrict lifecycle changes to approved internal roles.
- Require reasons for hold, cancellation and reopening.
- Preserve customer-visible summary and internal administration fields separately.
- Record every lifecycle change.
- Prevent project deletion when audit or commercial records exist.

### Files to create

```text
/apps/api/NoviqLabs.Application/Projects/CreateProjectCommand.cs
/apps/api/NoviqLabs.Application/Projects/UpdateProjectCommand.cs
/apps/api/NoviqLabs.Application/Projects/ChangeProjectStatusCommand.cs
/apps/api/NoviqLabs.Application/Projects/GetProjectAdministrationQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Projects/CreateProjectEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Projects/ChangeProjectStatusEndpoint.cs
/apps/api/NoviqLabs.Contracts/Projects/CreateProjectRequest.cs
/apps/web/src/app/(admin)/admin/projects/page.tsx
/apps/web/src/features/admin/projects/ProjectAdministrationPage.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Projects/ProjectAdministrationTests.cs
/docs/operations/project-administration.md
```

---

## Phase 14: Project Team Access

### Objectives

- Implement customer and Noviq project membership management.
- Allow only authorized organization members to be added as customer participants.
- Support project manager, contributor, customer reviewer and read-only roles.
- Prevent removal of required project ownership without transfer.
- Apply immediate access revocation.
- Audit membership and role changes.

### Files to create

```text
/apps/api/NoviqLabs.Application/Projects/AddProjectMemberCommand.cs
/apps/api/NoviqLabs.Application/Projects/RemoveProjectMemberCommand.cs
/apps/api/NoviqLabs.Application/Projects/ChangeProjectMemberRoleCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Projects/AddProjectMemberEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Projects/RemoveProjectMemberEndpoint.cs
/apps/web/src/features/projects/ProjectTeam.tsx
/apps/web/src/features/projects/ProjectMemberEditor.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Projects/ProjectMembershipTests.cs
/docs/projects/project-team-access.md
```

---

## Phase 15: Customer Dashboard

### Objectives

- Implement the authenticated customer dashboard.
- Show organization-scoped project summaries, pending actions, recent deliverables, messages and support status.
- Avoid exposing internal-only notes or other organizations' data.
- Provide clear empty, loading, restricted and error states.
- Support mobile, tablet and desktop layouts.
- Keep commercial payment widgets outside this sprint.

### Files to create

```text
/apps/web/src/app/(account)/dashboard/page.tsx
/apps/web/src/app/(account)/dashboard/loading.tsx
/apps/web/src/app/(account)/dashboard/error.tsx
/apps/web/src/features/dashboard/CustomerDashboardPage.tsx
/apps/web/src/features/dashboard/ProjectSummaryGrid.tsx
/apps/web/src/features/dashboard/PendingCustomerActions.tsx
/apps/web/src/features/dashboard/RecentDeliverables.tsx
/apps/web/src/features/dashboard/RecentProjectActivity.tsx
/apps/web/src/features/dashboard/SupportSummary.tsx
/apps/web/src/features/dashboard/CustomerDashboardPage.test.tsx
/docs/projects/customer-dashboard.md
```

---

## Phase 16: Project Workspace

### Objectives

- Implement the project workspace and navigation.
- Show approved project summary, status, participants, milestones, deliverables, documents, messages and activity.
- Preserve project-scoped authorization for every section.
- Render restricted sections only after backend authorization.
- Provide safe not-found and forbidden behavior.
- Support responsive and keyboard-first navigation.

### Files to create

```text
/apps/web/src/app/(account)/projects/[projectId]/layout.tsx
/apps/web/src/app/(account)/projects/[projectId]/page.tsx
/apps/web/src/app/(account)/projects/[projectId]/loading.tsx
/apps/web/src/app/(account)/projects/[projectId]/error.tsx
/apps/web/src/features/projects/ProjectWorkspace.tsx
/apps/web/src/features/projects/ProjectWorkspaceNavigation.tsx
/apps/web/src/features/projects/ProjectOverview.tsx
/apps/web/src/features/projects/ProjectStatusSummary.tsx
/apps/web/src/features/projects/ProjectWorkspace.test.tsx
/docs/projects/project-workspace.md
```

---

## Phase 17: Milestone Management

### Objectives

- Implement authorized milestone creation, update, sequencing and status changes.
- Show customer-visible progress and target dates.
- Keep internal blockers private unless explicitly shared.
- Validate dependencies and completion order.
- Notify affected participants of material changes.
- Record complete milestone history.

### Files to create

```text
/apps/api/NoviqLabs.Application/Projects/Milestones/CreateMilestoneCommand.cs
/apps/api/NoviqLabs.Application/Projects/Milestones/UpdateMilestoneCommand.cs
/apps/api/NoviqLabs.Application/Projects/Milestones/ChangeMilestoneStatusCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Projects/CreateMilestoneEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Projects/ChangeMilestoneStatusEndpoint.cs
/apps/web/src/app/(account)/projects/[projectId]/milestones/page.tsx
/apps/web/src/features/projects/MilestoneTimeline.tsx
/apps/web/src/features/projects/MilestoneEditor.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Projects/MilestoneTests.cs
/docs/projects/milestone-management.md
```

---

## Phase 18: Secure Project Document Upload

### Objectives

- Implement project-scoped document upload through private quarantine storage.
- Require project membership and appropriate document classification.
- Use short-lived upload authorization.
- Apply file-type, size, integrity and malware-scanning controls.
- Prevent access before scanning and authorization approval.
- Record document and version metadata.

### Files to create

```text
/apps/api/NoviqLabs.Application/Documents/CreateProjectDocumentUploadCommand.cs
/apps/api/NoviqLabs.Application/Documents/CreateProjectDocumentUploadHandler.cs
/apps/api/NoviqLabs.Api/Endpoints/Documents/CreateProjectDocumentUploadEndpoint.cs
/apps/api/NoviqLabs.Contracts/Documents/CreateProjectDocumentUploadRequest.cs
/apps/web/src/features/projects/documents/ProjectDocumentUpload.tsx
/apps/web/src/features/projects/documents/DocumentClassificationField.tsx
/apps/worker/NoviqLabs.Worker/Jobs/ProjectDocumentScanJob.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Documents/ProjectDocumentUploadTests.cs
/docs/security/project-document-uploads.md
```

---

## Phase 19: Project Document Access and Download

### Objectives

- Implement authorized project-document listing, metadata and download.
- Use short-lived, audience-restricted download authorization.
- Recheck authorization at access time.
- Prevent direct storage paths and public URLs.
- Record access and download events for confidential documents.
- Handle revoked membership immediately.

### Files to create

```text
/apps/api/NoviqLabs.Application/Documents/GetProjectDocumentsQuery.cs
/apps/api/NoviqLabs.Application/Documents/CreateDocumentDownloadCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Documents/GetProjectDocumentsEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Documents/CreateDocumentDownloadEndpoint.cs
/apps/web/src/app/(account)/projects/[projectId]/documents/page.tsx
/apps/web/src/features/projects/documents/ProjectDocumentList.tsx
/apps/web/src/features/projects/documents/ProjectDocumentDownload.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Documents/ProjectDocumentAccessTests.cs
/docs/security/project-document-access.md
```

---

## Phase 20: Deliverable Submission

### Objectives

- Implement deliverable creation, version upload and customer submission.
- Require clean files and approved customer visibility.
- Prevent duplicate version numbers and mutable approved versions.
- Associate deliverables with relevant milestones.
- Queue customer notification after successful submission.
- Record integrity and submission evidence.

### Files to create

```text
/apps/api/NoviqLabs.Application/Deliverables/CreateDeliverableCommand.cs
/apps/api/NoviqLabs.Application/Deliverables/SubmitDeliverableVersionCommand.cs
/apps/api/NoviqLabs.Application/Deliverables/GetDeliverablesQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Deliverables/CreateDeliverableEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Deliverables/SubmitDeliverableVersionEndpoint.cs
/apps/web/src/app/(account)/projects/[projectId]/deliverables/page.tsx
/apps/web/src/features/projects/deliverables/DeliverableList.tsx
/apps/web/src/features/projects/deliverables/DeliverableSubmission.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Deliverables/DeliverableSubmissionTests.cs
/docs/projects/deliverable-submission.md
```

---

## Phase 21: Deliverable Review and Approval

### Objectives

- Implement customer review, approval and changes-requested decisions.
- Require authorized customer reviewer policy.
- Capture a clear decision and optional structured comments.
- Prevent duplicate or conflicting decisions.
- Preserve review and approval history.
- Notify project participants after an accepted decision.

### Files to create

```text
/apps/api/NoviqLabs.Application/Deliverables/ReviewDeliverableCommand.cs
/apps/api/NoviqLabs.Application/Deliverables/ApproveDeliverableCommand.cs
/apps/api/NoviqLabs.Application/Deliverables/RequestDeliverableChangesCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Deliverables/ApproveDeliverableEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Deliverables/RequestDeliverableChangesEndpoint.cs
/apps/web/src/features/projects/deliverables/DeliverableReview.tsx
/apps/web/src/features/projects/deliverables/DeliverableDecisionForm.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Deliverables/DeliverableApprovalTests.cs
/docs/projects/deliverable-review-and-approval.md
```

---

## Phase 22: Secure Project Messaging

### Objectives

- Implement project conversation creation, listing and messaging.
- Restrict participation to current authorized project members.
- Sanitize content and restrict attachments to approved project documents.
- Use pagination and deterministic ordering.
- Notify participants without exposing message bodies in insecure channels.
- Record message and access audit events.

### Files to create

```text
/apps/api/NoviqLabs.Application/Messaging/CreateConversationCommand.cs
/apps/api/NoviqLabs.Application/Messaging/PostProjectMessageCommand.cs
/apps/api/NoviqLabs.Application/Messaging/GetProjectMessagesQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Messaging/PostProjectMessageEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Messaging/GetProjectMessagesEndpoint.cs
/apps/web/src/app/(account)/projects/[projectId]/messages/page.tsx
/apps/web/src/features/projects/messages/ProjectConversation.tsx
/apps/web/src/features/projects/messages/ProjectMessageComposer.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Messaging/ProjectMessagingTests.cs
/docs/projects/secure-project-messaging.md
```

---

## Phase 23: Support Requests

### Objectives

- Implement customer support-request creation and authorized status viewing.
- Implement internal assignment, response and status management.
- Provide guidance for security incidents and emergencies.
- Prevent ordinary support requests from carrying restricted security evidence.
- Notify authorized participants of material changes.
- Preserve status and response history.

### Files to create

```text
/apps/api/NoviqLabs.Application/Support/CreateSupportRequestCommand.cs
/apps/api/NoviqLabs.Application/Support/AssignSupportRequestCommand.cs
/apps/api/NoviqLabs.Application/Support/ChangeSupportStatusCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Support/CreateSupportRequestEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Support/ChangeSupportStatusEndpoint.cs
/apps/web/src/app/(account)/support/page.tsx
/apps/web/src/features/support/SupportRequestForm.tsx
/apps/web/src/features/support/SupportRequestList.tsx
/apps/web/src/features/admin/support/SupportQueuePage.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Support/SupportRequestTests.cs
/docs/support/customer-support-workflow.md
```

---

## Phase 24: Project Notifications

### Objectives

- Generate notifications for project assignment, milestone changes, deliverable submission, review decisions, messages and support updates.
- Respect user preferences while preserving required operational notifications.
- Avoid exposing confidential content in email subjects or bodies.
- Use the verified outbox and worker delivery mechanism.
- Support read and unread in-application status.
- Record delivery and failure state.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Notifications/InAppNotification.cs
/apps/api/NoviqLabs.Application/Notifications/GetNotificationsQuery.cs
/apps/api/NoviqLabs.Application/Notifications/MarkNotificationReadCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Notifications/GetNotificationsEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Notifications/MarkNotificationReadEndpoint.cs
/apps/web/src/components/notifications/NotificationCenter.tsx
/apps/web/src/components/notifications/NotificationItem.tsx
/apps/worker/NoviqLabs.Worker/Templates/ProjectNotificationTemplates.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Notifications/ProjectNotificationTests.cs
/docs/notifications/project-notifications.md
```

---

## Phase 25: Project Activity History

### Objectives

- Generate customer-visible activity events for approved project actions.
- Keep internal-only and security-sensitive events out of the customer feed.
- Support pagination and date filtering.
- Use immutable event records rather than reconstructing critical history from mutable tables.
- Preserve actor and correlation references.
- Test visibility rules.

### Files to create

```text
/apps/api/NoviqLabs.Application/Activity/GetProjectActivityQuery.cs
/apps/api/NoviqLabs.Infrastructure/Activity/ProjectActivityWriter.cs
/apps/api/NoviqLabs.Api/Endpoints/Activity/GetProjectActivityEndpoint.cs
/apps/api/NoviqLabs.Contracts/Activity/ProjectActivityResponse.cs
/apps/web/src/app/(account)/projects/[projectId]/activity/page.tsx
/apps/web/src/features/projects/activity/ProjectActivityFeed.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Activity/ProjectActivityTests.cs
/docs/projects/project-activity-history.md
```

---

## Phase 26: Security Engagement Workflow

### Objectives

- Implement authorized creation and management of security engagements.
- Require approved rules of engagement and testing window before activation.
- Restrict scope changes after activation to a versioned approval workflow.
- Keep targets, exclusions and testing details restricted.
- Notify only approved security-engagement participants.
- Audit every privileged lifecycle action.

### Files to create

```text
/apps/api/NoviqLabs.Application/SecurityEngagements/CreateSecurityEngagementCommand.cs
/apps/api/NoviqLabs.Application/SecurityEngagements/ApproveRulesOfEngagementCommand.cs
/apps/api/NoviqLabs.Application/SecurityEngagements/ActivateTestingWindowCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/SecurityEngagements/CreateSecurityEngagementEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/SecurityEngagements/ApproveRulesOfEngagementEndpoint.cs
/apps/web/src/features/security-engagements/SecurityEngagementWorkspace.tsx
/apps/web/src/features/security-engagements/RulesOfEngagementReview.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/SecurityEngagements/SecurityEngagementWorkflowTests.cs
/docs/security-engagements/rules-of-engagement-workflow.md
```

---

## Phase 27: Controlled Security-Report Delivery

### Objectives

- Implement isolated security-report upload, release and download.
- Require restricted-security classification and clean-file status.
- Require explicit report release by authorized Noviq security personnel.
- Require authorized recipient and strong authentication at download time.
- Use short-lived single-audience download authorization.
- Audit view, download, revocation and supersession events.

### Files to create

```text
/apps/api/NoviqLabs.Application/SecurityEngagements/UploadSecurityReportCommand.cs
/apps/api/NoviqLabs.Application/SecurityEngagements/ReleaseSecurityReportCommand.cs
/apps/api/NoviqLabs.Application/SecurityEngagements/CreateSecurityReportDownloadCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/SecurityEngagements/ReleaseSecurityReportEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/SecurityEngagements/CreateSecurityReportDownloadEndpoint.cs
/apps/web/src/features/security-engagements/SecurityReportList.tsx
/apps/web/src/features/security-engagements/SecurityReportDownload.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/SecurityEngagements/SecurityReportDeliveryTests.cs
/docs/security-engagements/security-report-delivery.md
```

---

## Phase 28: Customer and Staff Audit Trails

### Objectives

- Audit project lifecycle, membership, milestone, deliverable, document, message, support and security-report actions.
- Separate customer-visible activity from protected audit records.
- Record actor, organization, project, action, result, timestamp and correlation identifier.
- Avoid storing message bodies, document content or secrets in audit records.
- Restrict audit access to approved roles.
- Define retention and export behavior.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Audit/ProjectAuditEvent.cs
/apps/api/NoviqLabs.Domain/Audit/ProjectAuditAction.cs
/apps/api/NoviqLabs.Application/Audit/IProjectAuditWriter.cs
/apps/api/NoviqLabs.Infrastructure/Audit/ProjectAuditWriter.cs
/apps/api/NoviqLabs.Api/Endpoints/Administration/GetProjectAuditEventsEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Audit/ProjectAuditTests.cs
/docs/security/project-audit-trails.md
```

---

## Phase 29: Retention and Project Closure

### Objectives

- Implement controlled project closure and archive behavior.
- Apply retention rules by document and evidence classification.
- Prevent deletion of records subject to contractual, legal or audit retention.
- Revoke unnecessary project access after closure.
- Preserve approved customer access where contractually required.
- Produce retention and deletion evidence.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/ProjectRetentionJob.cs
/apps/worker/NoviqLabs.Worker/Services/ProjectRetentionService.cs
/apps/api/NoviqLabs.Application/Projects/CloseProjectCommand.cs
/apps/api/NoviqLabs.Application/Projects/ArchiveProjectCommand.cs
/tests/worker/NoviqLabs.Worker.UnitTests/ProjectRetentionJobTests.cs
/docs/privacy/project-data-retention.md
/docs/operations/project-closure-runbook.md
```

---

## Phase 30: Security and Isolation Testing

### Objectives

- Test cross-organization and cross-project access attempts.
- Test removed-member access, stale authorization cache and identifier tampering.
- Test document and report download authorization.
- Test message and support data leakage.
- Test security-engagement scope and report controls.
- Resolve all critical and high-risk findings.

### Files to create

```text
/apps/web/tests/security/project-route-isolation.spec.ts
/apps/web/tests/security/project-document-access.spec.ts
/apps/web/tests/security/security-report-access.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Security/CrossProjectAccessTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/RemovedMemberAccessTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/DeliverableApprovalAuthorizationTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/SecurityEngagementIsolationTests.cs
/scripts/security/scan-sprint-9-portal.zsh
/docs/evidence/sprint-9-security-results.md
```

---

## Phase 31: Accessibility and Usability Validation

### Objectives

- Test dashboard, project workspace, milestones, documents, deliverables, messaging, support and security-report flows.
- Verify keyboard operation, focus, headings, status messages, tables and dialogs.
- Verify mobile, tablet, desktop and 200 percent zoom behavior.
- Verify upload, review and approval error recovery.
- Conduct representative customer, project manager and security-user tasks.
- Resolve all blocking usability and accessibility defects.

### Files to create

```text
/apps/web/tests/accessibility/customer-dashboard.spec.ts
/apps/web/tests/accessibility/project-workspace.spec.ts
/apps/web/tests/accessibility/project-documents.spec.ts
/apps/web/tests/accessibility/deliverable-review.spec.ts
/apps/web/tests/accessibility/project-messaging.spec.ts
/apps/web/tests/accessibility/support-requests.spec.ts
/apps/web/tests/accessibility/security-reports.spec.ts
/apps/web/tests/usability/sprint-9-customer-tasks.spec.ts
/apps/web/tests/usability/sprint-9-staff-tasks.spec.ts
/docs/evidence/sprint-9-accessibility-and-usability.md
```

---

## Phase 32: Integration, End-to-End and Resilience Testing

### Objectives

- Test intake conversion to active project.
- Test project membership, milestones, documents and deliverable approval.
- Test messages, notifications, support and activity history.
- Test security engagement and controlled report delivery.
- Test storage, notification and worker outages.
- Verify audit completeness and recovery behavior.

### Files to create

```text
/apps/web/tests/e2e/intake-to-project.spec.ts
/apps/web/tests/e2e/customer-project-workspace.spec.ts
/apps/web/tests/e2e/project-milestones.spec.ts
/apps/web/tests/e2e/project-document-lifecycle.spec.ts
/apps/web/tests/e2e/deliverable-approval.spec.ts
/apps/web/tests/e2e/project-messaging.spec.ts
/apps/web/tests/e2e/support-request-lifecycle.spec.ts
/apps/web/tests/e2e/security-report-delivery.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Resilience/ProjectDependencyFailureTests.cs
/docs/evidence/sprint-9-end-to-end-results.md
```

---

## Phase 33: Performance and Load Validation

### Objectives

- Measure dashboard, project list, milestone, activity, document and message query latency.
- Load test project lists, activity feeds and message pagination.
- Verify worker throughput for scans and notifications.
- Verify indexes, bounded queries and pagination.
- Test concurrent deliverable reviews and milestone updates.
- Record staging performance evidence.

### Files to create

```text
/tests/load/sprint-9-dashboard.js
/tests/load/sprint-9-project-workspace.js
/tests/load/sprint-9-activity-feed.js
/tests/load/sprint-9-project-messaging.js
/tests/load/sprint-9-deliverable-review.js
/scripts/quality/validate-sprint-9-performance.zsh
/docs/evidence/sprint-9-performance-results.md
```

---

## Phase 34: CI/CD Quality-Gate Expansion

### Objectives

- Add project migration, authorization, portal, file, messaging, support, security-report, accessibility, isolation and load tests.
- Preserve complete evidence as workflow artifacts.
- Build and publish verified web, API and worker images only after all gates pass.
- Prevent test fixtures from entering production storage.
- Fail the pipeline when any required underlying command fails.
- Keep commercial and payment features excluded.

### Files to create

```text
/.github/workflows/ci-customer-portal.yml
/.github/workflows/test-project-authorization.yml
/.github/workflows/test-project-documents.yml
/.github/workflows/test-deliverables-and-messaging.yml
/.github/workflows/test-security-report-delivery.yml
/.github/workflows/test-portal-accessibility.yml
/.github/workflows/test-portal-security.yml
/.github/workflows/test-portal-load.yml
/.github/workflows/validate-project-migration.yml
/scripts/ci/verify-sprint-9-portal.zsh
/scripts/ci/verify-sprint-9-quality-gates.zsh
/docs/delivery/sprint-9-quality-gates.md
```

---

## Phase 35: Azure Infrastructure and Deployment

### Objectives

- Provision project-document, restricted-security-report, queue, alert and worker-scaling configuration.
- Apply the Sprint 9 database migration through the controlled migration job.
- Deploy verified web, API and worker images to development and staging.
- Verify private storage, managed identities, telemetry, alerts and retention configuration.
- Execute portal and security-report smoke tests with non-production data.
- Keep production customer portal activation disabled until production authorization.

### Files to create

```text
/infrastructure/azure/modules/project-document-storage.bicep
/infrastructure/azure/modules/security-report-storage.bicep
/infrastructure/azure/modules/project-queues.bicep
/infrastructure/azure/modules/project-alerts.bicep
/infrastructure/azure/config/project-alert-thresholds.json
/infrastructure/azure/config/project-worker-scaling.json
/.github/workflows/deploy-portal-development.yml
/.github/workflows/deploy-portal-staging.yml
/scripts/cloud/deploy-sprint-9-development.zsh
/scripts/cloud/deploy-sprint-9-staging.zsh
/scripts/cloud/smoke-test-sprint-9-portal.zsh
/docs/evidence/sprint-9-development-deployment.md
/docs/evidence/sprint-9-staging-deployment.md
```

---

## Phase 36: Rollback, Recovery and Operational Documentation

### Objectives

- Verify rollback for web, API, worker, migration and storage configuration.
- Ensure rollback does not lose accepted deliverable decisions, messages or audit records.
- Document recovery for scans, notifications, project events and report delivery.
- Document unauthorized-access and restricted-report incidents.
- Prepare customer, project-manager, support and security-operator guidance.
- Keep commands Zsh-compatible for Kali Debian.

### Files to create

```text
/.github/workflows/rollback-portal-release.yml
/scripts/cloud/rollback-sprint-9-portal.zsh
/scripts/operations/replay-project-outbox.zsh
/scripts/operations/retry-project-document-scan.zsh
/docs/operations/customer-portal-rollback-runbook.md
/docs/operations/project-workflow-recovery.md
/docs/operations/security-report-incident-response.md
/docs/projects/customer-portal-guide.md
/docs/operations/project-manager-handbook.md
/docs/operations/support-operator-handbook.md
/docs/operations/security-engagement-operator-handbook.md
/docs/development/sprint-9-kali-debian-zsh.md
/docs/evidence/sprint-9-rollback-verification.md
```

---

## Phase 37: Integrated Validation and Sprint Closure

### Objectives

- Validate the complete customer portal and project-management implementation from a clean checkout.
- Execute build, migration, unit, integration, end-to-end, accessibility, usability, isolation, load, privacy and security tests.
- Verify development and staging deployments, telemetry, alerts, rollback and recovery.
- Verify customer-visible and internal data remain correctly separated.
- Confirm commercial, invoice, subscription and payment features have not started.
- Create and push the verified Sprint 9 Git commit.
- Create a pull request only after every required validation passes.
- Stop before Sprint 10.

### Files to create

```text
/scripts/release/sprint-9-final-validation.zsh
/docs/evidence/sprint-9-migration-summary.md
/docs/evidence/sprint-9-project-workspace-summary.md
/docs/evidence/sprint-9-document-and-deliverable-summary.md
/docs/evidence/sprint-9-messaging-and-support-summary.md
/docs/evidence/sprint-9-security-engagement-summary.md
/docs/evidence/sprint-9-accessibility-summary.md
/docs/evidence/sprint-9-performance-summary.md
/docs/evidence/sprint-9-security-and-isolation-summary.md
/docs/evidence/sprint-9-deployment-summary.md
/docs/evidence/sprint-9-completion-record.md
/docs/delivery/sprint-9-pull-request.md
```

---

## Development Sprint 9 Completion Gate

Development Sprint 9 is complete only when every condition below passes:

- Qualified project intake can be converted into an authorized project exactly once.
- Every project belongs to one authorized customer organization.
- Customer and Noviq project-team access is enforced.
- Cross-organization and cross-project access is blocked.
- The customer dashboard displays only authorized information.
- Project workspaces operate across mobile, tablet and desktop.
- Project status and milestone management work with complete history.
- Secure project-document upload, scanning, listing and download work.
- Documents are private, classified and inaccessible through public storage URLs.
- Deliverable submission and versioning work.
- Customer review, approval and changes-requested decisions are traceable.
- Approved deliverables cannot be overwritten.
- Secure project messaging works only for current participants.
- Support requests, assignment and status management work.
- Project notifications respect required and optional preferences.
- Customer-visible activity excludes internal-only and restricted events.
- Security engagements require approved rules of engagement.
- Security-report delivery uses stricter authorization and strong authentication.
- Security-report view, download, revocation and supersession events are audited.
- Project and security audit trails are complete and protected.
- Project closure and retention controls operate correctly.
- Accessibility and usability checks pass.
- Isolation and security tests pass with no unresolved critical or high-risk findings.
- Performance and load budgets pass.
- The Sprint 9 migration succeeds in development and staging.
- Development and staging deployment smoke tests pass.
- Azure private storage, queues, telemetry and alerts operate correctly.
- Rollback and workflow recovery are verified without losing accepted decisions or messages.
- Documentation matches the verified implementation.
- A verified Development Sprint 9 Git commit exists.
- The Development Sprint 9 branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- No unresolved blocking defect remains.
- Commercial and payment implementation has not started.
- The next sprint has not started.

## Development Sprint 9 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_9_COMPLETE
```
