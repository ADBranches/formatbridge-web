# Noviq Labs Full-Stack Platform

## Development Sprint 8: Lead Generation and Project Intake

**Sprint position:** Eighth production implementation sprint after secure identity and customer organizations  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure development and staging environments  
**Architecture:** Modular monolith with asynchronous integration and secure file-quarantine boundaries

## Sprint Objective

Implement the complete visitor-to-qualified-lead and project-intake journey. The sprint will deliver public contact submissions, guided service selection, consultation booking, a saveable Start a Project workflow, secure requirements uploads, malware scanning, consent evidence, confirmations, CRM synchronization, enquiry assignment, lead-status management, internal notes, follow-up reminders and privacy-conscious conversion analytics. The sprint will not create active customer projects, project workspaces, billing records or payment transactions.

---

## Phase 1: Sprint Entry and Dependency Verification

### Objectives

- Verify that Development Sprint 7 passed every completion-gate requirement.
- Confirm the verified Sprint 7 Git commit, pushed development branch and approved pull-request state.
- Confirm authentication, organization isolation, CMS, public website, development and staging environments remain healthy.
- Inspect the current repository, API contracts, database schema, Blob Storage and worker foundations before creating or modifying files.
- Confirm approved CRM, email, calendar and malware-scanning integration decisions.
- Confirm project-intake privacy, retention, consent and file-classification requirements.
- Create the Development Sprint 8 branch only after all entry checks pass.
- Stop if a required integration decision or blocking Sprint 7 dependency remains unresolved.

### Files to create

```text
/docs/evidence/sprint-8-entry-verification.md
/docs/intake/sprint-8-scope.md
/docs/intake/integration-readiness-register.md
/docs/intake/privacy-and-retention-prerequisites.md
/docs/delivery/sprint-8-branch-record.md
```

---

## Phase 2: Lead and Project-Intake Architecture

### Objectives

- Define public enquiry, consultation and project-intake boundaries.
- Separate anonymous lead capture from authenticated customer and project records.
- Define ownership between the Noviq database, CRM, scheduling service, email provider and Blob Storage.
- Define conversion from public enquiry to qualified lead without creating a customer project prematurely.
- Document consent, retention, deletion, assignment and audit behavior.
- Record integration failure and retry boundaries.

### Files to create

```text
/docs/architecture/lead-intake-context.md
/docs/architecture/lead-intake-sequence-flows.md
/docs/architecture/lead-intake-data-boundaries.md
/docs/architecture/adr/0029-use-noviq-as-lead-intake-system-of-record.md
/docs/architecture/adr/0030-use-outbox-for-lead-integrations.md
/docs/architecture/adr/0031-quarantine-project-intake-uploads.md
```

---

## Phase 3: Lead and Enquiry Domain Model

### Objectives

- Create lead, enquiry, contact, organization reference, source and lifecycle entities.
- Support anonymous and authenticated submissions.
- Define controlled lead states from new through archived.
- Preserve referral source, service interest, consent and assignment history.
- Prevent sensitive security details from being stored in general enquiry text.
- Use immutable identifiers and auditable timestamps.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Leads/Lead.cs
/apps/api/NoviqLabs.Domain/Leads/LeadStatus.cs
/apps/api/NoviqLabs.Domain/Leads/LeadSource.cs
/apps/api/NoviqLabs.Domain/Leads/LeadContact.cs
/apps/api/NoviqLabs.Domain/Leads/ServiceInterest.cs
/apps/api/NoviqLabs.Domain/Leads/LeadAssignment.cs
/apps/api/NoviqLabs.Domain/Leads/LeadNote.cs
/apps/api/NoviqLabs.Domain/Leads/LeadErrors.cs
/docs/intake/lead-lifecycle.md
```

---

## Phase 4: Project-Intake Domain Model

### Objectives

- Create project-intake, requirement, budget, timeframe and submission entities.
- Support draft, submitted, under review, changes requested, qualified, declined and converted states.
- Keep intake records distinct from active projects.
- Associate authenticated submissions with an authorized organization when applicable.
- Preserve submission version and consent evidence.
- Prevent direct modification of an accepted submission without a new revision.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Intake/ProjectIntake.cs
/apps/api/NoviqLabs.Domain/Intake/ProjectIntakeStatus.cs
/apps/api/NoviqLabs.Domain/Intake/ProjectRequirement.cs
/apps/api/NoviqLabs.Domain/Intake/BudgetRange.cs
/apps/api/NoviqLabs.Domain/Intake/DeliveryTimeframe.cs
/apps/api/NoviqLabs.Domain/Intake/IntakeRevision.cs
/apps/api/NoviqLabs.Domain/Intake/IntakeErrors.cs
/docs/intake/project-intake-lifecycle.md
```

---

## Phase 5: Consultation Domain Model

### Objectives

- Create consultation request, availability reference and booking lifecycle entities.
- Support requested, confirmed, rescheduled, cancelled, completed and no-show states.
- Preserve external scheduling references without making the scheduler authoritative for lead status.
- Store time-zone-aware timestamps.
- Record cancellation and rescheduling reasons safely.
- Prevent duplicate confirmed bookings for one consultation request.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Consultations/Consultation.cs
/apps/api/NoviqLabs.Domain/Consultations/ConsultationStatus.cs
/apps/api/NoviqLabs.Domain/Consultations/ConsultationType.cs
/apps/api/NoviqLabs.Domain/Consultations/SchedulingReference.cs
/apps/api/NoviqLabs.Domain/Consultations/ConsultationErrors.cs
/docs/intake/consultation-lifecycle.md
```

---

## Phase 6: Consent and Communication Records

### Objectives

- Create purpose-specific consent records for enquiry processing and optional marketing.
- Separate required processing acknowledgement from optional communications consent.
- Record policy version, timestamp, source and withdrawal state.
- Prevent optional consent from being preselected.
- Preserve consent history without overwriting prior evidence.
- Define lawful operational notifications that cannot be disabled during an active request.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Consent/ConsentRecord.cs
/apps/api/NoviqLabs.Domain/Consent/ConsentPurpose.cs
/apps/api/NoviqLabs.Domain/Consent/ConsentStatus.cs
/apps/api/NoviqLabs.Domain/Consent/PolicyReference.cs
/apps/api/NoviqLabs.Domain/Consent/ConsentErrors.cs
/docs/privacy/lead-intake-consent.md
/docs/privacy/lead-intake-processing-record.md
```

---

## Phase 7: Persistence and Database Migration

### Objectives

- Map lead, intake, consultation and consent entities to PostgreSQL.
- Add organization and submitter scoping where applicable.
- Add concurrency tokens, lifecycle indexes and uniqueness constraints.
- Apply retention markers without performing destructive deletion inside ordinary requests.
- Create the controlled Sprint 8 migration.
- Validate upgrade, empty-database application and rollback boundaries.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/LeadConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ProjectIntakeConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ConsultationConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/ConsentRecordConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddLeadGenerationAndProjectIntake.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddLeadGenerationAndProjectIntake.Designer.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/LeadIntakeMigrationTests.cs
/docs/database/lead-intake-schema.md
```

---

## Phase 8: Public Contact Submission API

### Objectives

- Implement the public contact-submission endpoint.
- Validate contact details, enquiry category, message length and consent.
- Apply rate limiting, anti-automation controls and safe duplicate detection.
- Reject sensitive files and security evidence from the generic contact workflow.
- Return a non-enumerating confirmation response.
- Create audit, notification and integration events transactionally.

### Files to create

```text
/apps/api/NoviqLabs.Application/Leads/CreateContactEnquiryCommand.cs
/apps/api/NoviqLabs.Application/Leads/CreateContactEnquiryHandler.cs
/apps/api/NoviqLabs.Application/Leads/CreateContactEnquiryValidator.cs
/apps/api/NoviqLabs.Api/Endpoints/Leads/CreateContactEnquiryEndpoint.cs
/apps/api/NoviqLabs.Contracts/Leads/CreateContactEnquiryRequest.cs
/apps/api/NoviqLabs.Contracts/Leads/ContactEnquiryResponse.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Leads/ContactEnquiryTests.cs
/docs/api/contact-enquiry-api.md
```

---

## Phase 9: Service-Selection Guidance

### Objectives

- Implement deterministic service-selection guidance based on stated customer needs.
- Provide recommendations without preventing users from choosing another service.
- Avoid presenting guidance as professional, security or legal advice.
- Preserve selected outcomes and referral context into project intake.
- Keep guidance accessible and functional without animation.
- Test ambiguous and multi-service needs.

### Files to create

```text
/apps/web/src/features/intake/ServiceSelectionGuide.tsx
/apps/web/src/features/intake/ServiceSelectionQuestions.tsx
/apps/web/src/features/intake/ServiceRecommendation.tsx
/apps/web/src/features/intake/service-selection.types.ts
/apps/web/src/lib/intake/service-selection.ts
/apps/web/src/lib/intake/service-selection.test.ts
/docs/intake/service-selection-guidance.md
```

---

## Phase 10: Start a Project Route and Wizard Shell

### Objectives

- Implement the Start a Project route and multi-step wizard shell.
- Show progress, step names and save status clearly.
- Support back and forward navigation without losing valid data.
- Avoid collecting unnecessary information early.
- Provide a clear exit and return path.
- Preserve mobile, tablet, desktop and keyboard usability.

### Files to create

```text
/apps/web/src/app/(public)/(intake)/start-a-project/page.tsx
/apps/web/src/app/(public)/(intake)/start-a-project/loading.tsx
/apps/web/src/app/(public)/(intake)/start-a-project/error.tsx
/apps/web/src/features/intake/StartProjectPage.tsx
/apps/web/src/features/intake/ProjectIntakeWizard.tsx
/apps/web/src/features/intake/IntakeProgress.tsx
/apps/web/src/features/intake/IntakeNavigation.tsx
/apps/web/src/features/intake/intake-wizard.types.ts
/apps/web/src/features/intake/index.ts
/docs/intake/start-a-project-experience.md
```

---

## Phase 11: Project Outcome and Service Step

### Objectives

- Capture the required outcome and relevant service interests.
- Support one primary service and additional related interests.
- Provide plain-language examples without forcing a technical solution.
- Validate minimum and maximum text lengths.
- Prevent scripts and unsafe markup.
- Preserve the selected service recommendation source.

### Files to create

```text
/apps/web/src/features/intake/steps/OutcomeStep.tsx
/apps/web/src/features/intake/steps/ServiceInterestStep.tsx
/apps/web/src/features/intake/steps/outcome-step.schema.ts
/apps/web/src/features/intake/steps/OutcomeStep.test.tsx
/apps/web/src/features/intake/steps/ServiceInterestStep.test.tsx
/docs/intake/outcome-and-service-step.md
```

---

## Phase 12: Organization and Contact Step

### Objectives

- Capture organization and contact information required to respond.
- Reuse authenticated profile and organization data where authorized.
- Allow correction without silently changing identity-provider attributes.
- Avoid collecting sensitive identification data.
- Validate telephone, email, locale and time-zone values.
- Explain how the information will be used.

### Files to create

```text
/apps/web/src/features/intake/steps/OrganizationContactStep.tsx
/apps/web/src/features/intake/steps/organization-contact.schema.ts
/apps/web/src/features/intake/steps/OrganizationContactStep.test.tsx
/apps/web/src/lib/intake/profile-prefill.ts
/apps/web/src/lib/intake/profile-prefill.test.ts
/docs/intake/organization-contact-step.md
```

---

## Phase 13: Requirements, Budget and Timeframe Step

### Objectives

- Capture structured requirements, budget range, desired timeframe and urgency.
- Use ranges rather than demanding false precision.
- Allow users to indicate uncertainty.
- Provide security-specific warnings against submitting secrets or live credentials.
- Validate combinations without rejecting legitimate atypical projects.
- Preserve accessible explanatory text and error summaries.

### Files to create

```text
/apps/web/src/features/intake/steps/RequirementsStep.tsx
/apps/web/src/features/intake/steps/BudgetAndTimeframeStep.tsx
/apps/web/src/features/intake/steps/requirements-step.schema.ts
/apps/web/src/features/intake/steps/budget-timeframe.schema.ts
/apps/web/src/features/intake/steps/RequirementsStep.test.tsx
/apps/web/src/features/intake/steps/BudgetAndTimeframeStep.test.tsx
/docs/intake/requirements-budget-timeframe.md
```

---

## Phase 14: Draft Creation and Save-and-Resume API

### Objectives

- Create draft intake records for authenticated users and secure resumable references for anonymous users.
- Use unpredictable, expiring resume secrets.
- Store protected or hashed resume secrets.
- Prevent one user from resuming another user's draft.
- Use optimistic concurrency and reject stale updates safely.
- Audit draft creation, update, expiry and deletion.

### Files to create

```text
/apps/api/NoviqLabs.Application/Intake/CreateIntakeDraftCommand.cs
/apps/api/NoviqLabs.Application/Intake/UpdateIntakeDraftCommand.cs
/apps/api/NoviqLabs.Application/Intake/GetIntakeDraftQuery.cs
/apps/api/NoviqLabs.Application/Intake/ResumeTokenService.cs
/apps/api/NoviqLabs.Api/Endpoints/Intake/CreateIntakeDraftEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Intake/UpdateIntakeDraftEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Intake/GetIntakeDraftEndpoint.cs
/apps/web/src/lib/intake/draft-client.ts
/apps/web/src/lib/intake/resume-token.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Intake/IntakeDraftTests.cs
/docs/intake/save-and-resume.md
```

---

## Phase 15: Secure Requirements Upload

### Objectives

- Implement direct-to-quarantine upload initiation for approved file types and sizes.
- Use short-lived upload authorization.
- Associate uploads with one draft and authorized submitter.
- Prevent public container access and executable content delivery.
- Capture filename, media type, size, hash, classification and retention metadata.
- Keep uploaded files unavailable until security scanning passes.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Files/IntakeFile.cs
/apps/api/NoviqLabs.Domain/Files/FileScanStatus.cs
/apps/api/NoviqLabs.Application/Files/CreateIntakeUploadCommand.cs
/apps/api/NoviqLabs.Application/Files/CreateIntakeUploadHandler.cs
/apps/api/NoviqLabs.Api/Endpoints/Files/CreateIntakeUploadEndpoint.cs
/apps/api/NoviqLabs.Contracts/Files/CreateUploadRequest.cs
/apps/web/src/features/intake/steps/RequirementsUploadStep.tsx
/apps/web/src/features/intake/components/SecureFileUpload.tsx
/apps/web/src/features/intake/components/FileUploadStatus.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Files/IntakeUploadTests.cs
/docs/security/project-intake-uploads.md
```

---

## Phase 16: Malware-Scanning Workflow

### Objectives

- Trigger scanning when an upload completes.
- Verify file integrity before and after scanning.
- Move clean files to the approved private container.
- Retain or delete rejected files according to policy.
- Handle scanner timeout, failure and duplicate events safely.
- Notify users without exposing scanner internals.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/IntakeFileScanJob.cs
/apps/worker/NoviqLabs.Worker/Jobs/IntakeFileScanJobOptions.cs
/apps/worker/NoviqLabs.Worker/Services/IMalwareScanner.cs
/apps/worker/NoviqLabs.Worker/Services/MalwareScanner.cs
/apps/worker/NoviqLabs.Worker/Services/IntakeFileQuarantineService.cs
/tests/worker/NoviqLabs.Worker.UnitTests/IntakeFileScanJobTests.cs
/infrastructure/azure/modules/intake-file-scanning.bicep
/docs/security/malware-scanning-workflow.md
/docs/operations/file-scanning-degraded-mode.md
```

---

## Phase 17: Intake Review, Consent and Submission

### Objectives

- Present a complete review before submission.
- Display consent and privacy statements with current policy versions.
- Prevent submission while uploads are pending or rejected.
- Create the submitted intake, lead and audit events transactionally.
- Make submission idempotent to prevent duplicates.
- Issue a non-sensitive reference number and confirmation.

### Files to create

```text
/apps/web/src/features/intake/steps/ReviewAndConsentStep.tsx
/apps/web/src/features/intake/steps/review-consent.schema.ts
/apps/web/src/features/intake/steps/ReviewAndConsentStep.test.tsx
/apps/api/NoviqLabs.Application/Intake/SubmitProjectIntakeCommand.cs
/apps/api/NoviqLabs.Application/Intake/SubmitProjectIntakeHandler.cs
/apps/api/NoviqLabs.Api/Endpoints/Intake/SubmitProjectIntakeEndpoint.cs
/apps/api/NoviqLabs.Contracts/Intake/SubmitProjectIntakeRequest.cs
/apps/api/NoviqLabs.Contracts/Intake/ProjectIntakeSubmissionResponse.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Intake/SubmitProjectIntakeTests.cs
/docs/intake/review-consent-submission.md
```

---

## Phase 18: Submission Confirmation and Status

### Objectives

- Display a clear confirmation and next steps.
- Allow authenticated users to view authorized intake status.
- Avoid exposing status through guessable public identifiers.
- Provide safe recovery when confirmation delivery fails.
- Show only approved lifecycle information to customers.
- Keep internal qualification notes private.

### Files to create

```text
/apps/web/src/app/(public)/(intake)/start-a-project/confirmation/[reference]/page.tsx
/apps/web/src/app/(account)/account/intakes/[id]/page.tsx
/apps/web/src/features/intake/SubmissionConfirmation.tsx
/apps/web/src/features/intake/CustomerIntakeStatus.tsx
/apps/api/NoviqLabs.Application/Intake/GetCustomerIntakeStatusQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Intake/GetCustomerIntakeStatusEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Intake/CustomerIntakeStatusTests.cs
/docs/intake/customer-submission-status.md
```

---

## Phase 19: Consultation Booking

### Objectives

- Implement consultation request and scheduling-provider integration.
- Preserve time zone and availability accurately.
- Prevent double booking and duplicate requests.
- Support confirmation, rescheduling and cancellation.
- Make provider webhooks authenticated and idempotent.
- Keep provider failures from losing the original consultation request.

### Files to create

```text
/apps/api/NoviqLabs.Application/Consultations/CreateConsultationCommand.cs
/apps/api/NoviqLabs.Application/Consultations/RescheduleConsultationCommand.cs
/apps/api/NoviqLabs.Application/Consultations/CancelConsultationCommand.cs
/apps/api/NoviqLabs.Infrastructure/Scheduling/SchedulingProvider.cs
/apps/api/NoviqLabs.Api/Endpoints/Consultations/CreateConsultationEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Consultations/SchedulingWebhookEndpoint.cs
/apps/web/src/app/(public)/(intake)/consultation/page.tsx
/apps/web/src/features/consultations/ConsultationBookingPage.tsx
/apps/web/src/features/consultations/ConsultationBookingForm.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Consultations/ConsultationTests.cs
/docs/intake/consultation-booking.md
```

---

## Phase 20: Transactional Notifications

### Objectives

- Send enquiry, intake, consultation and assignment confirmations through the approved provider.
- Use versioned templates with no sensitive upload contents.
- Queue delivery through the worker and outbox.
- Retry transient failures and dead-letter permanent failures.
- Record delivery status without treating email delivery as workflow completion.
- Respect operational and optional communication preferences.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Notifications/NotificationOutboxMessage.cs
/apps/api/NoviqLabs.Infrastructure/Notifications/NotificationOutboxWriter.cs
/apps/worker/NoviqLabs.Worker/Jobs/NotificationDispatchJob.cs
/apps/worker/NoviqLabs.Worker/Services/TransactionalEmailService.cs
/apps/worker/NoviqLabs.Worker/Templates/ContactEnquiryConfirmation.cs
/apps/worker/NoviqLabs.Worker/Templates/ProjectIntakeConfirmation.cs
/apps/worker/NoviqLabs.Worker/Templates/ConsultationConfirmation.cs
/tests/worker/NoviqLabs.Worker.UnitTests/NotificationDispatchJobTests.cs
/docs/notifications/transactional-notifications.md
```

---

## Phase 21: CRM Integration

### Objectives

- Synchronize qualified lead data to the approved CRM through the outbox.
- Keep Noviq authoritative for original intake and consent evidence.
- Map only approved fields and minimize personal data.
- Handle duplicate, rejected and unavailable CRM responses.
- Record external identifiers and synchronization status.
- Do not block customer submission on CRM availability.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Integrations/CrmSyncRecord.cs
/apps/api/NoviqLabs.Infrastructure/Crm/CrmClient.cs
/apps/api/NoviqLabs.Infrastructure/Crm/CrmOptions.cs
/apps/worker/NoviqLabs.Worker/Jobs/CrmLeadSyncJob.cs
/apps/worker/NoviqLabs.Worker/Mapping/CrmLeadMapper.cs
/tests/worker/NoviqLabs.Worker.UnitTests/CrmLeadSyncJobTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Crm/CrmSynchronizationTests.cs
/docs/integrations/crm-integration.md
/docs/privacy/crm-data-boundary.md
```

---

## Phase 22: Lead Assignment and Status Management

### Objectives

- Allow authorized staff to assign leads to approved operators.
- Implement controlled status transitions and reasons.
- Prevent invalid transitions and unauthorized reassignment.
- Record assignment and status history.
- Support unassigned and reassignment queues.
- Keep customer-visible status separate from internal lead status.

### Files to create

```text
/apps/api/NoviqLabs.Application/Leads/AssignLeadCommand.cs
/apps/api/NoviqLabs.Application/Leads/ChangeLeadStatusCommand.cs
/apps/api/NoviqLabs.Application/Leads/GetLeadQueueQuery.cs
/apps/api/NoviqLabs.Api/Endpoints/Leads/AssignLeadEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Leads/ChangeLeadStatusEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Leads/GetLeadQueueEndpoint.cs
/apps/web/src/app/(admin)/admin/leads/page.tsx
/apps/web/src/features/admin/leads/LeadQueuePage.tsx
/apps/web/src/features/admin/leads/LeadAssignmentControl.tsx
/apps/web/src/features/admin/leads/LeadStatusControl.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Leads/LeadManagementTests.cs
/docs/operations/lead-management.md
```

---

## Phase 23: Internal Notes and Follow-Up Reminders

### Objectives

- Implement private internal notes with author and timestamp.
- Prevent notes from appearing in customer responses or CRM mappings unless explicitly approved.
- Implement follow-up reminders with owner, due date and completion state.
- Prevent reminders from becoming a substitute for durable lead status.
- Audit note creation, modification restrictions and reminder completion.
- Avoid storing secrets or sensitive security evidence in notes.

### Files to create

```text
/apps/api/NoviqLabs.Application/Leads/AddLeadNoteCommand.cs
/apps/api/NoviqLabs.Application/Leads/CreateFollowUpReminderCommand.cs
/apps/api/NoviqLabs.Application/Leads/CompleteFollowUpReminderCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Leads/AddLeadNoteEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Leads/CreateFollowUpReminderEndpoint.cs
/apps/web/src/features/admin/leads/LeadNotes.tsx
/apps/web/src/features/admin/leads/FollowUpReminders.tsx
/apps/worker/NoviqLabs.Worker/Jobs/LeadFollowUpReminderJob.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Leads/LeadNotesAndRemindersTests.cs
/docs/operations/lead-notes-and-reminders.md
```

---

## Phase 24: Conversion Analytics

### Objectives

- Define privacy-conscious funnel events from service discovery to qualified lead.
- Measure step completion, abandonment and conversion without storing sensitive free text.
- Require analytics consent for non-essential tracking.
- Keep operational submission records separate from analytics.
- Define allowed dimensions and retention.
- Validate that analytics failures never block submissions.

### Files to create

```text
/apps/web/src/lib/analytics/intake-events.ts
/apps/web/src/lib/analytics/intake-event.types.ts
/apps/web/src/lib/analytics/intake-event-sanitization.ts
/apps/web/src/lib/analytics/intake-event-sanitization.test.ts
/apps/web/src/components/analytics/IntakeAnalytics.tsx
/apps/web/tests/analytics/intake-funnel.spec.ts
/docs/analytics/project-intake-funnel.md
/docs/privacy/intake-analytics-boundary.md
```

---

## Phase 25: Retention and Draft Expiry

### Objectives

- Expire abandoned anonymous drafts and resume secrets according to policy.
- Retain submitted records according to business and legal requirements.
- Delete or anonymize data only through controlled jobs.
- Preserve required consent and audit evidence.
- Handle files and database records consistently.
- Produce deletion and exception evidence.

### Files to create

```text
/apps/worker/NoviqLabs.Worker/Jobs/ExpiredIntakeDraftCleanupJob.cs
/apps/worker/NoviqLabs.Worker/Jobs/LeadRetentionJob.cs
/apps/worker/NoviqLabs.Worker/Services/IntakeRetentionService.cs
/tests/worker/NoviqLabs.Worker.UnitTests/ExpiredIntakeDraftCleanupJobTests.cs
/tests/worker/NoviqLabs.Worker.UnitTests/LeadRetentionJobTests.cs
/docs/privacy/lead-and-intake-retention.md
/docs/operations/intake-retention-runbook.md
```

---

## Phase 26: Security and Abuse Testing

### Objectives

- Test rate limits, bot controls, duplicate submissions and idempotency.
- Test upload bypass, malicious file, path, media-type and size attacks.
- Test unauthorized draft resume, status access and lead administration.
- Test webhook forgery and replay.
- Test cross-organization access and data leakage.
- Resolve all critical and high-risk findings.

### Files to create

```text
/apps/web/tests/security/intake-rate-limits.spec.ts
/apps/web/tests/security/intake-resume-token.spec.ts
/apps/web/tests/security/intake-upload-bypass.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Security/LeadAuthorizationTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/IntakeIdempotencyTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/SchedulingWebhookSecurityTests.cs
/scripts/security/scan-sprint-8-intake.zsh
/docs/evidence/sprint-8-security-results.md
```

---

## Phase 27: Accessibility and Usability Validation

### Objectives

- Test contact, service guidance, project intake, upload, review, consultation and administration workflows.
- Verify keyboard operation, focus, labels, error summaries and live status updates.
- Verify mobile, tablet, desktop and 200 percent zoom behavior.
- Verify time-zone and date communication.
- Test save-and-resume and interrupted uploads.
- Resolve all blocking usability and accessibility defects.

### Files to create

```text
/apps/web/tests/accessibility/contact-enquiry.spec.ts
/apps/web/tests/accessibility/project-intake.spec.ts
/apps/web/tests/accessibility/intake-file-upload.spec.ts
/apps/web/tests/accessibility/consultation-booking.spec.ts
/apps/web/tests/accessibility/lead-administration.spec.ts
/apps/web/tests/usability/sprint-8-customer-tasks.spec.ts
/apps/web/tests/usability/sprint-8-staff-tasks.spec.ts
/docs/evidence/sprint-8-accessibility-and-usability.md
```

---

## Phase 28: Integration, End-to-End and Resilience Testing

### Objectives

- Test visitor-to-qualified-lead flow.
- Test authenticated project-intake and organization association.
- Test save-and-resume, uploads, scanning, submission and confirmation.
- Test consultation booking, rescheduling and cancellation.
- Test CRM, email, scheduling and scanning outages.
- Test assignment, notes, reminders and status history.
- Verify audit completeness.

### Files to create

```text
/apps/web/tests/e2e/contact-to-lead.spec.ts
/apps/web/tests/e2e/start-project-anonymous.spec.ts
/apps/web/tests/e2e/start-project-authenticated.spec.ts
/apps/web/tests/e2e/intake-save-and-resume.spec.ts
/apps/web/tests/e2e/intake-upload-and-scan.spec.ts
/apps/web/tests/e2e/consultation-lifecycle.spec.ts
/apps/web/tests/e2e/lead-administration.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Resilience/LeadIntegrationFailureTests.cs
/docs/evidence/sprint-8-end-to-end-results.md
```

---

## Phase 29: Performance and Load Validation

### Objectives

- Measure draft-save, submission, lead-queue and upload-initiation latency.
- Load test public submission endpoints with abuse protections active.
- Verify worker throughput for scanning, notifications and CRM synchronization.
- Verify database indexes and bounded queries.
- Ensure external integration latency does not block accepted submissions.
- Record staging performance evidence.

### Files to create

```text
/tests/load/sprint-8-contact-enquiry.js
/tests/load/sprint-8-project-intake.js
/tests/load/sprint-8-lead-queue.js
/tests/load/sprint-8-worker-throughput.js
/scripts/quality/validate-sprint-8-performance.zsh
/docs/evidence/sprint-8-performance-results.md
```

---

## Phase 30: CI/CD Quality-Gate Expansion

### Objectives

- Add migration, intake, file, scanning, consultation, CRM, notification, accessibility, security and load checks.
- Use safe test doubles for external providers in untrusted pull requests.
- Preserve evidence as workflow artifacts.
- Build and publish verified web, API and worker images only after all gates pass.
- Prevent failed integrations from being reported as passing.
- Keep customer-portal project management and payments excluded.

### Files to create

```text
/.github/workflows/ci-lead-intake.yml
/.github/workflows/test-intake-uploads.yml
/.github/workflows/test-intake-integrations.yml
/.github/workflows/test-intake-accessibility.yml
/.github/workflows/test-intake-security.yml
/.github/workflows/test-intake-load.yml
/.github/workflows/validate-intake-migration.yml
/scripts/ci/verify-sprint-8-intake.zsh
/scripts/ci/verify-sprint-8-quality-gates.zsh
/docs/delivery/sprint-8-quality-gates.md
```

---

## Phase 31: Azure Infrastructure and Deployment

### Objectives

- Provision configuration for intake storage, scanning, integrations, queues, alerts and worker scaling.
- Apply the Sprint 8 database migration through the controlled migration job.
- Deploy verified web, API and worker images to development and staging.
- Verify Key Vault, Blob Storage, queues, telemetry and provider callbacks.
- Execute smoke tests with non-production integration credentials.
- Keep production intake submission disabled until production authorization.

### Files to create

```text
/infrastructure/azure/modules/intake-storage.bicep
/infrastructure/azure/modules/intake-queues.bicep
/infrastructure/azure/modules/intake-alerts.bicep
/infrastructure/azure/config/intake-alert-thresholds.json
/infrastructure/azure/config/intake-worker-scaling.json
/.github/workflows/deploy-intake-development.yml
/.github/workflows/deploy-intake-staging.yml
/scripts/cloud/deploy-sprint-8-development.zsh
/scripts/cloud/deploy-sprint-8-staging.zsh
/scripts/cloud/smoke-test-sprint-8-intake.zsh
/docs/evidence/sprint-8-development-deployment.md
/docs/evidence/sprint-8-staging-deployment.md
```

---

## Phase 32: Rollback, Recovery and Operational Documentation

### Objectives

- Verify rollback for web, API, worker, migration and integration configuration.
- Ensure rollback does not lose accepted submissions or scanning state.
- Document replay and recovery for outbox, notifications, CRM sync and file scans.
- Document privacy incident and malicious-upload response.
- Document customer and staff operating procedures.
- Keep all commands Zsh-compatible for Kali Debian.

### Files to create

```text
/.github/workflows/rollback-intake-release.yml
/scripts/cloud/rollback-sprint-8-intake.zsh
/scripts/operations/replay-intake-outbox.zsh
/scripts/operations/retry-intake-file-scan.zsh
/docs/operations/intake-rollback-runbook.md
/docs/operations/intake-integration-recovery.md
/docs/operations/malicious-upload-response.md
/docs/intake/customer-intake-guide.md
/docs/operations/lead-operator-handbook.md
/docs/development/sprint-8-kali-debian-zsh.md
/docs/evidence/sprint-8-rollback-verification.md
```

---

## Phase 33: Integrated Validation and Sprint Closure

### Objectives

- Validate the complete lead-generation and project-intake implementation from a clean checkout.
- Execute build, migration, unit, integration, end-to-end, accessibility, usability, load, privacy and security tests.
- Verify development and staging deployments, telemetry, alerts, rollback and integration recovery.
- Verify accepted submissions survive downstream provider failures.
- Confirm customer-project management, commercial and payments features have not started.
- Create and push the verified Sprint 8 Git commit.
- Create a pull request only after every required validation passes.
- Stop before Sprint 9.

### Files to create

```text
/scripts/release/sprint-8-final-validation.zsh
/docs/evidence/sprint-8-migration-summary.md
/docs/evidence/sprint-8-contact-and-intake-summary.md
/docs/evidence/sprint-8-upload-and-scanning-summary.md
/docs/evidence/sprint-8-consultation-summary.md
/docs/evidence/sprint-8-integration-summary.md
/docs/evidence/sprint-8-accessibility-summary.md
/docs/evidence/sprint-8-performance-summary.md
/docs/evidence/sprint-8-security-and-privacy-summary.md
/docs/evidence/sprint-8-deployment-summary.md
/docs/evidence/sprint-8-completion-record.md
/docs/delivery/sprint-8-pull-request.md
```

---

## Development Sprint 8 Completion Gate

Development Sprint 8 is complete only when every condition below passes:

- A visitor can submit a valid contact enquiry.
- Service-selection guidance works without blocking user choice.
- The Start a Project wizard works across mobile, tablet and desktop.
- Anonymous and authenticated users can save and resume authorized drafts.
- Draft resume secrets are unpredictable, expiring and protected.
- Organization and profile prefill respects authorization boundaries.
- Requirements, budget and timeframe validation works.
- Secure uploads enter a private quarantine boundary.
- File type, size, integrity and ownership controls pass.
- Malware scanning accepts clean files and isolates rejected files.
- Pending or rejected uploads cannot be submitted as approved requirements.
- Review, consent and final project-intake submission work.
- Submission is idempotent and duplicate records are prevented.
- Consent evidence records the correct purpose and policy version.
- Submission confirmation and authorized status views work.
- Consultation booking, rescheduling and cancellation work.
- Transactional confirmations are queued and delivered reliably.
- CRM outages do not lose accepted submissions.
- Lead assignment and controlled status transitions work.
- Internal notes remain private and follow-up reminders work.
- Conversion analytics exclude sensitive free text and respect consent.
- Abandoned draft and lead-retention jobs follow approved policy.
- Public endpoints enforce rate limiting and abuse controls.
- Cross-organization and unauthorized intake access is blocked.
- Integration, webhook and replay security checks pass.
- Accessibility and usability checks pass.
- Load and worker-throughput budgets pass.
- No unresolved critical or high-risk security or privacy finding remains.
- Development and staging migrations and deployments pass.
- Azure storage, queues, telemetry and alerts operate correctly.
- Rollback and downstream-integration recovery are verified.
- Documentation matches the verified implementation.
- A verified Development Sprint 8 Git commit exists.
- The Development Sprint 8 branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- No unresolved blocking defect remains.
- The next sprint has not started.

## Development Sprint 8 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_8_COMPLETE
```
