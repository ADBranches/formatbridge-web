# LandaFlow Sprint 05

## User Journeys, Operations and Tenant Experience

**Sprint duration:** One week  
**Delivery model:** Parallel team delivery through small, reviewable pull requests  
**Deployment target:** JulyHost-compatible, cloud-neutral Docker deployment  
**Cost constraint:** Free-tier, open-source, sandbox, or self-hosted services only  
**Prerequisite:** Sprint 04 approved and merged, with verified property, tenancy, billing, ledger, Mobile Money sandbox, reconciliation, organisation-isolation, audit, CI, backup, and restoration contracts available on the integration branch

---

## 1. Sprint Objective

Deliver the operational experience required for landlords, property managers, accountants, support users, and tenants to use LandaFlow effectively through role-specific dashboards, a tenant Progressive Web App, notification preferences, rent reminders, maintenance workflows, reports, exports, and internal support tooling.

Sprint 05 must consume verified data from previous sprints. The interface must not invent occupancy, balance, payment, receipt, arrears, or reconciliation figures. Financial values must come from the Sprint 03 ledger, and payment status must come from Sprint 04 provider-confirmed records.

---

## 2. Sprint Outcomes

At completion:

1. Landlords and property managers have an operational dashboard based only on verified live data.
2. Tenants can install and use a responsive Progressive Web App.
3. Tenants can view their agreement, balance, invoices, receipts, payments, and property contacts.
4. Authorised users can create, assign, update, and close maintenance requests.
5. Notification preferences, templates, delivery attempts, and reminder schedules are organisation-scoped.
6. Email and in-app notifications operate through free or self-hosted capabilities.
7. SMS and WhatsApp remain provider-adapter placeholders unless approved paid access exists.
8. Reports and exports reconcile to source records and ledger totals.
9. Internal support users have auditable, least-privilege operational tools.
10. Dashboards remain usable on mobile, tablet, and desktop widths.
11. Cross-organisation and tenant-self-service boundaries are enforced.
12. Backup, restoration, browser, accessibility, security, and CI checks pass before review.

---

## 3. Scope Boundaries

### Included

- Role-specific operational dashboards
- Tenant Progressive Web App foundation
- Tenant agreement, invoices, balance, payment, receipt, and profile views
- Notification preferences and in-app notification centre
- Free-tier transactional email adapter
- Rent-reminder scheduling and delivery tracking
- Maintenance requests, comments, assignments, priorities, and lifecycle
- Operational reports and CSV exports
- Internal support and administration views
- Accessibility, responsive design, observability, and acceptance evidence

### Excluded

- Paid SMS production delivery
- Paid WhatsApp Business production delivery
- Native Android or iOS applications
- AI-generated recommendations or automated tenant scoring
- Property marketplace or public listings
- Vendor procurement and contractor payments
- Inventory and asset depreciation
- Full accounting-suite integration
- EFRIS fiscal-document integration
- Production JulyHost activation before provisioning

---

## 4. Operational Conventions

### Verified-data rule

Dashboards, reports, notifications, and exports must use persisted domain records and ledger-derived totals. Placeholder financial or property figures are prohibited outside clearly labelled test fixtures.

### Tenant self-service boundary

A tenant user may access only tenant profiles, agreements, invoices, payments, receipts, maintenance requests, documents, and notifications explicitly linked to that authenticated user within the active organisation.

### Notification truth

A notification marked `SENT` means the selected delivery adapter accepted the message. A notification marked `DELIVERED` requires provider evidence where available. In-app notifications may be marked delivered when persisted and made available to the intended user.

### Delivery cost control

Email may use a free-tier provider such as Resend during development, subject to its current allowance. In-app delivery remains self-hosted. SMS and WhatsApp adapters remain disabled until costs and production onboarding are approved.

### Time and scheduling

Schedules are stored in UTC and evaluated using the organisation's configured timezone. A reminder business key prevents duplicate delivery for the same recipient, invoice, reminder type, and schedule occurrence.

### Maintenance history

Maintenance status changes, assignments, comments, and closure information remain auditable. Closed or cancelled requests are not destructively deleted.

### Export safety

Exports require the same permissions and organisation scope as interactive views. Formula-injection characters in CSV cells must be escaped or neutralised.

---

## 5. Phase 1: Operational Data Foundation

### Objective

Establish notification, reminder, maintenance, reporting-job, and support-operation models with organisation isolation, histories, indexes, and shared contracts.

### Work

1. Add notification preference, template, message, and delivery-attempt models.
2. Add reminder-policy and reminder-occurrence models.
3. Add maintenance request, comment, assignment, and status-history models.
4. Add report-export job and generated-file metadata.
5. Add internal support-action records without duplicating immutable audit events.
6. Define lifecycle states, timestamps, archival rules, and indexes.
7. Add safe non-production seed data.
8. Document operational model and rollback considerations.

### Files to create

- `packages/types/src/notifications.ts`
- `packages/types/src/maintenance.ts`
- `packages/types/src/operations.ts`
- `packages/database/src/operations-scope.ts`
- `packages/database/src/operations-scope.spec.ts`
- `packages/database/prisma/migrations/<timestamp>_operations_notifications_maintenance/migration.sql`
- `docs/architecture/operations-and-notifications-model.md`
- `docs/architecture/maintenance-lifecycle.md`

### Files likely to be modified

- `packages/database/prisma/schema.prisma`
- `packages/database/prisma/seed.ts`
- `packages/database/src/index.ts`
- `packages/types/src/index.ts`
- `docs/development/database-migrations.md`

### Required models

- `NotificationPreference`
- `NotificationTemplate`
- `NotificationMessage`
- `NotificationDeliveryAttempt`
- `ReminderPolicy`
- `ReminderOccurrence`
- `MaintenanceRequest`
- `MaintenanceComment`
- `MaintenanceAssignment`
- `MaintenanceStatusHistory`
- `ReportExportJob`
- `SupportAction`

### Validation

```text
pnpm --filter @landaflow/database prisma validate
pnpm --filter @landaflow/database prisma migrate deploy
pnpm --filter @landaflow/database seed
pnpm --filter @landaflow/database test
```

### Completion evidence

- Migrations apply to an empty PostgreSQL database.
- Duplicate reminder business keys are rejected.
- Maintenance records cannot cross organisation boundaries.
- Tenant-linked operations queries return no records belonging to another tenant.
- Production seed execution remains prohibited.
- Notification and maintenance histories survive archival.

---

## 6. Phase 2: Dashboard Read Models and Operational API

### Objective

Provide efficient, permission-aware dashboards built from verified property, tenancy, ledger, payment, and maintenance data.

### Work

1. Create organisation dashboard read models.
2. Create property-manager operational summaries.
3. Create accountant financial-operation summaries.
4. Create tenant self-service summaries.
5. Add date-range, property, and status filters.
6. Return source timestamps and data-freshness metadata.
7. Avoid expensive unbounded queries.
8. Add audit events for sensitive support and export operations.

### Files to create

- `apps/api/src/dashboard/dashboard.module.ts`
- `apps/api/src/dashboard/dashboard.controller.ts`
- `apps/api/src/dashboard/dashboard.service.ts`
- `apps/api/src/dashboard/dashboard.types.ts`
- `apps/api/src/dashboard/dto/dashboard-query.dto.ts`
- `apps/api/src/dashboard/dashboard.service.spec.ts`
- `docs/architecture/dashboard-read-models.md`

### Files likely to be modified

- `apps/api/src/app.module.ts`
- `packages/types/src/authorisation.ts`
- `docs/security/roles-and-permissions.md`

### Required dashboard data

- Property and unit counts
- Verified occupancy and vacancy counts
- Active and ending tenancy counts
- Ledger-derived billed, collected, outstanding, and arrears totals
- Confirmed and pending payment counts
- Open maintenance counts by priority and status
- Recent auditable operational events

### Validation

- Every total reconciles to its authoritative source.
- Draft, voided, reversed, and failed financial records do not inflate totals.
- Tenant dashboards expose only linked tenant records.
- Accountants do not receive owner-only administrative data.
- Support viewers remain read-only.
- Cross-organisation filters cannot leak records.
- Large data sets use bounded queries and indexes.

---

## 7. Phase 3: Tenant Progressive Web App Foundation

### Objective

Deliver an installable, mobile-first tenant experience that works reliably with intermittent connectivity while protecting sensitive data.

### Work

1. Add web-app manifest and tenant-specific navigation.
2. Add service-worker registration and an offline application shell.
3. Cache only non-sensitive static assets.
4. Prevent caching of authentication responses, financial APIs, and private documents.
5. Add tenant home, agreement, invoices, payments, receipts, profile, and notifications screens.
6. Add safe session-expiry and offline states.
7. Add installability metadata and icons.
8. Ensure keyboard, screen-reader, and touch usability.

### Files to create

- `apps/web/src/app/manifest.ts`
- `apps/web/public/sw.js`
- `apps/web/public/icons/landaflow-192.png`
- `apps/web/public/icons/landaflow-512.png`
- `apps/web/src/components/service-worker-registration.tsx`
- `apps/web/src/app/(tenant)/layout.tsx`
- `apps/web/src/app/(tenant)/tenant/page.tsx`
- `apps/web/src/app/(tenant)/tenant/agreement/page.tsx`
- `apps/web/src/app/(tenant)/tenant/invoices/page.tsx`
- `apps/web/src/app/(tenant)/tenant/payments/page.tsx`
- `apps/web/src/app/(tenant)/tenant/receipts/page.tsx`
- `apps/web/src/app/(tenant)/tenant/notifications/page.tsx`
- `apps/web/src/app/(tenant)/tenant/profile/page.tsx`
- `apps/web/src/features/tenant-portal/api.ts`
- `apps/web/src/features/tenant-portal/components/tenant-navigation.tsx`
- `apps/web/src/features/tenant-portal/components/offline-state.tsx`
- `docs/architecture/tenant-pwa.md`

### Files likely to be modified

- `apps/web/src/app/layout.tsx`
- `apps/web/src/app/globals.css`
- `apps/web/next.config.ts`
- `apps/web/src/proxy.ts`

### Validation

- The application meets browser installability requirements.
- Static shell assets remain available offline.
- Private API responses and documents are absent from service-worker caches.
- Tenant users cannot open manager routes.
- Manager users do not accidentally enter tenant-only context without a linked tenant profile.
- Mobile, tablet, and desktop layouts remain usable.
- Accessibility checks reveal no critical violations.

---

## 8. Phase 4: Notification Preferences and Delivery Framework

### Objective

Implement provider-neutral notifications with in-app delivery, a free-tier email adapter, recipient preferences, retries, redaction, and delivery evidence.

### Work

1. Define notification-channel and template contracts.
2. Add in-app notification delivery.
3. Add email adapter using a free-tier transactional provider or local development catcher.
4. Add user and tenant notification preferences.
5. Add template variable validation.
6. Add bounded retries and dead-letter state for failed deliveries.
7. Add delivery-attempt histories.
8. Redact recipient and provider-sensitive fields from logs.
9. Keep SMS and WhatsApp adapters disabled placeholders.

### Files to create

- `apps/api/src/notifications/notifications.module.ts`
- `apps/api/src/notifications/notifications.controller.ts`
- `apps/api/src/notifications/notifications.service.ts`
- `apps/api/src/notifications/template.service.ts`
- `apps/api/src/notifications/delivery.service.ts`
- `apps/api/src/notifications/adapters/notification-adapter.interface.ts`
- `apps/api/src/notifications/adapters/in-app.adapter.ts`
- `apps/api/src/notifications/adapters/email.adapter.ts`
- `apps/api/src/notifications/adapters/disabled-sms.adapter.ts`
- `apps/api/src/notifications/dto/update-notification-preferences.dto.ts`
- `apps/api/src/notifications/delivery.service.spec.ts`
- `apps/api/src/notifications/template.service.spec.ts`
- `docs/architecture/notification-delivery.md`

### Files likely to be modified

- `packages/config/src/env.ts`
- `.env.example`
- `apps/api/src/app.module.ts`
- `apps/api/src/common/interceptors/request-logging.interceptor.ts`
- `infrastructure/julyhost/.env.production.example`

### Validation

- In-app notifications persist once per business key.
- Disabled channels cannot send.
- Recipient preferences are respected unless a documented mandatory-security exception applies.
- Invalid template variables fail before delivery.
- Retry limits are enforced.
- Failed deliveries remain visible for operations.
- Email credentials and recipient data are absent from logs.
- A tenant cannot read another tenant's notifications.

---

## 9. Phase 5: Rent Reminders and Scheduling

### Objective

Generate accurate, idempotent rent reminders from ledger-derived invoice and arrears data without requiring paid messaging channels.

### Work

1. Add organisation reminder policies.
2. Support before-due, due-date, overdue, and configurable arrears reminders.
3. Select recipients from active tenancy and preference data.
4. Derive amounts and due dates from posted invoice and ledger data.
5. Prevent reminders for paid, voided, reversed, inactive, or disputed records as defined by policy.
6. Generate one occurrence per business key.
7. Deliver through in-app and enabled email channels.
8. Provide manual preview and controlled resend operations.
9. Add audit and operational metrics.

### Files to create

- `apps/api/src/reminders/reminders.module.ts`
- `apps/api/src/reminders/reminders.controller.ts`
- `apps/api/src/reminders/reminders.service.ts`
- `apps/api/src/reminders/reminder-runner.service.ts`
- `apps/api/src/reminders/reminder-recipient.service.ts`
- `apps/api/src/reminders/dto/update-reminder-policy.dto.ts`
- `apps/api/src/reminders/dto/preview-reminders.dto.ts`
- `apps/api/src/reminders/dto/run-reminders.dto.ts`
- `apps/api/src/reminders/reminder-runner.service.spec.ts`
- `docs/architecture/rent-reminders.md`

### Files likely to be modified

- `apps/api/src/app.module.ts`
- `packages/types/src/authorisation.ts`
- `docs/security/roles-and-permissions.md`

### Validation

- Reminder amounts reconcile to posted financial data.
- Paid or reversed invoices do not receive overdue reminders.
- Duplicate runs do not duplicate occurrences or notifications.
- Tenant preferences and enabled channels are respected.
- Cross-organisation reminders cannot be generated.
- Manual resend requires permission and creates audit evidence.
- Provider outages preserve scheduled occurrences for retry.

---

## 10. Phase 6: Maintenance Requests and Work Tracking

### Objective

Enable tenants and authorised organisation users to create, triage, assign, update, and close maintenance requests with complete history.

### Work

1. Add maintenance creation for tenants and managers.
2. Support categories, priorities, descriptions, property, unit, and tenant context.
3. Add assignment to authorised organisation members.
4. Implement lifecycle states: `OPEN`, `TRIAGED`, `ASSIGNED`, `IN_PROGRESS`, `BLOCKED`, `RESOLVED`, `CLOSED`, and `CANCELLED`.
5. Add comments, internal notes, and tenant-visible messages.
6. Add attachment metadata through the existing storage abstraction.
7. Add due dates and resolution summaries.
8. Emit notifications and audit events on relevant changes.
9. Prevent tenant access to internal-only notes.

### Files to create

- `apps/api/src/maintenance/maintenance.module.ts`
- `apps/api/src/maintenance/maintenance.controller.ts`
- `apps/api/src/maintenance/maintenance.service.ts`
- `apps/api/src/maintenance/maintenance-state-machine.ts`
- `apps/api/src/maintenance/dto/create-maintenance-request.dto.ts`
- `apps/api/src/maintenance/dto/update-maintenance-request.dto.ts`
- `apps/api/src/maintenance/dto/change-maintenance-status.dto.ts`
- `apps/api/src/maintenance/dto/add-maintenance-comment.dto.ts`
- `apps/api/src/maintenance/dto/assign-maintenance-request.dto.ts`
- `apps/api/src/maintenance/maintenance.service.spec.ts`
- `apps/api/src/maintenance/maintenance-state-machine.spec.ts`
- `docs/architecture/maintenance-workflow.md`

### Files likely to be modified

- `apps/api/src/app.module.ts`
- `packages/types/src/authorisation.ts`
- `docs/security/roles-and-permissions.md`

### Validation

- Tenants can create requests only for linked properties or units.
- Tenant users cannot view internal notes.
- Invalid lifecycle transitions are rejected.
- Assignments are limited to active organisation members with appropriate roles.
- Closed requests preserve complete history.
- Cross-organisation property, unit, tenant, request, and user identifiers are rejected.
- Notifications and audit events identify the correct actor and affected request.

---

## 11. Phase 7: Reports, Exports and Internal Operations

### Objective

Provide permission-aware operational reports, safe exports, and internal support tools without bypassing organisation isolation or audit controls.

### Work

1. Add occupancy, tenancy-expiry, arrears, collections, payment-exception, and maintenance reports.
2. Reuse verified property, tenancy, ledger, and provider data.
3. Add CSV exports with formula-injection protection.
4. Add asynchronous export jobs for larger data sets.
5. Add internal support search by organisation, user, tenant, invoice, payment, or correlation identifier.
6. Require explicit reason capture for support actions.
7. Prevent support tools from changing financial truth directly.
8. Add operator audit views and controlled impersonation-free troubleshooting.
9. Add retention and cleanup rules for generated exports.

### Files to create

- `apps/api/src/operations/operations.module.ts`
- `apps/api/src/operations/operations.controller.ts`
- `apps/api/src/operations/operations.service.ts`
- `apps/api/src/operations/export.service.ts`
- `apps/api/src/operations/support.service.ts`
- `apps/api/src/operations/dto/report-query.dto.ts`
- `apps/api/src/operations/dto/create-export.dto.ts`
- `apps/api/src/operations/dto/support-search.dto.ts`
- `apps/api/src/operations/export.service.spec.ts`
- `apps/api/src/operations/support.service.spec.ts`
- `apps/web/src/app/(app)/reports/page.tsx`
- `apps/web/src/app/(app)/reports/occupancy/page.tsx`
- `apps/web/src/app/(app)/reports/arrears/page.tsx`
- `apps/web/src/app/(app)/reports/maintenance/page.tsx`
- `apps/web/src/app/(app)/operations/support/page.tsx`
- `apps/web/src/features/reports/api.ts`
- `apps/web/src/features/reports/components/report-table.tsx`
- `apps/web/src/features/reports/components/export-action.tsx`
- `apps/web/src/features/support/api.ts`
- `apps/web/src/features/support/components/support-search.tsx`
- `docs/security/internal-support-controls.md`

### Files likely to be modified

- `apps/web/src/components/app-sidebar.tsx`
- `apps/web/src/app/globals.css`
- `packages/config/src/env.ts`
- `.env.example`

### Validation

- Report totals reconcile to source domains.
- Cross-organisation filters cannot leak records.
- CSV cells beginning with `=`, `+`, `-`, or `@` are neutralised.
- Export download requires current authorisation.
- Expired export files are removed according to retention rules.
- Support actions require reasons and create audit records.
- Support users cannot mutate posted financial records.
- Tenant users cannot access operational reports.

---

## 12. Phase 8: Integration, Acceptance and Delivery

### Objective

Prove the integrated operational experience, tenant PWA, reminders, notifications, maintenance, reporting, support controls, and review readiness.

### Work

1. Add complete role-specific browser journeys.
2. Add tenant self-service and tenant-isolation tests.
3. Add notification preference, retry, and reminder-idempotency tests.
4. Add maintenance lifecycle and internal-note visibility tests.
5. Add report reconciliation and export-safety tests.
6. Validate PWA installation and offline static shell.
7. Validate migrations against an empty database.
8. Verify backup and isolated restoration retain operational histories.
9. Run dependency and secret scanning.
10. Build production containers with paid notification channels disabled.
11. Publish validation evidence and prepare the Sprint 05 pull request.

### Files to create

- `tests/e2e/landlord-dashboard.spec.ts`
- `tests/e2e/tenant-portal.spec.ts`
- `tests/e2e/tenant-isolation.spec.ts`
- `tests/e2e/notification-preferences.spec.ts`
- `tests/e2e/rent-reminders.spec.ts`
- `tests/e2e/maintenance-journey.spec.ts`
- `tests/e2e/reports-and-exports.spec.ts`
- `tests/e2e/internal-support-controls.spec.ts`
- `tests/e2e/pwa-offline-shell.spec.ts`
- `docs/validation/sprint-05-acceptance.md`
- `docs/operations/notification-incident-response.md`
- `docs/operations/maintenance-operations.md`

### Files likely to be modified

- `.github/workflows/ci.yml`
- `README.md`
- `docs/operations/release-checklist.md`
- `package.json`
- `docker-compose.yml`
- `infrastructure/julyhost/docker-compose.production.yml`
- `infrastructure/julyhost/.env.production.example`

### Validation commands

```text
pnpm install --frozen-lockfile
pnpm --filter @landaflow/database prisma validate
pnpm --filter @landaflow/database prisma migrate deploy
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm build
docker compose config
docker compose up --build -d
docker compose ps
```

### Completion evidence

1. Empty-database migrations pass.
2. Landlord, property-manager, accountant, support, and tenant dashboards use verified data.
3. Tenant self-service and cross-tenant isolation tests pass.
4. PWA installability and offline static-shell tests pass.
5. Notification preference, retry, redaction, and reminder-idempotency tests pass.
6. Maintenance creation, assignment, lifecycle, comments, visibility, and audit tests pass.
7. Reports reconcile to authoritative source records.
8. CSV export-safety and permission tests pass.
9. Backup and isolated restoration retain notifications, reminders, maintenance, exports, and audit history.
10. CI quality gates pass on the submitted commit.
11. No unresolved critical or high-severity defect remains.
12. Validation evidence matches the commit under review.

---

## 13. Team Work Allocation

### Platform and Infrastructure Team

Owns:

- PWA static-delivery and cache infrastructure
- Notification-provider environment configuration
- Reminder-job scheduling infrastructure
- Export storage and cleanup
- CI, backup, restoration, and operational documentation
- JulyHost placeholders for email and future paid channels

### Backend and Data Team

Owns:

- Operations, notification, reminder, maintenance, and export models
- Dashboard read models
- Notification and reminder services
- Maintenance workflows
- Reports, exports, and support controls
- Organisation and tenant isolation
- Audit integration

### Web Experience Team

Owns:

- Landlord and manager dashboards
- Tenant Progressive Web App
- Notification centre and preferences
- Maintenance journeys
- Reports and internal support screens
- Responsive and accessible shared experiences

### Quality and Security Review

Owns:

- Tenant isolation and permission tests
- Notification redaction and delivery-state review
- Reminder idempotency and financial-data reconciliation
- Maintenance internal-note visibility
- Export formula-injection protection
- PWA cache-safety review
- Release-readiness assessment

Teams may work concurrently only after operational models, dashboard contracts, notification channels, maintenance states, report definitions, and shared permissions are reviewed and merged. Provider and lockfile changes must be coordinated.

---

## 14. Branch and Pull-Request Plan

Recommended branches:

```text
foundation/operations-notifications-model
feature/operational-dashboards
feature/tenant-pwa
feature/notification-delivery
feature/rent-reminders
feature/maintenance-workflows
feature/reports-support-operations
operations/sprint-05-acceptance
```

Every pull request must include:

1. A precise capability-focused title.
2. Scope and affected operational or tenant journeys.
3. Technical implementation details.
4. Tenant isolation, permissions, privacy, and cache considerations.
5. Database and migration impact.
6. Validation commands and complete results.
7. Provider, deployment, and configuration impact.
8. Risks and known limitations.
9. Rollback considerations.
10. Reviewer focus areas.
11. Screenshots only where they verify interface behaviour.

A pull request must not be merged when required checks fail, dashboards use unverified totals, tenant isolation is incomplete, sensitive API responses can enter offline caches, reminders can duplicate, internal notes leak to tenants, exports permit formula injection, secrets appear in source or logs, required review is missing, or validation evidence does not match the submitted commit.

---

## 15. Sprint Security and Operational Controls

- Dashboards use verified source records and ledger-derived financial totals only.
- Tenant access is limited to explicitly linked tenant records.
- Private API and document responses are never cached by the service worker.
- Notification credentials and recipient data are redacted from logs.
- Paid SMS and WhatsApp providers remain disabled until approved.
- Reminder business keys prevent duplicate delivery.
- Maintenance internal notes remain hidden from tenant users.
- Support actions require reasons and immutable audit events.
- Support tooling cannot directly edit posted financial records.
- CSV exports neutralise spreadsheet formula injection.
- Export downloads recheck current authorisation.
- Generated export files follow retention and cleanup rules.
- Cross-organisation identifiers never establish access.
- Backup and restoration preserve operational and audit histories.

---

## 16. Definition of Done

Sprint 05 is complete only when:

1. Every phase is implemented and reviewed.
2. Operational migrations apply to an empty database.
3. Role-specific dashboards use verified live data.
4. Tenant PWA, tenant isolation, and offline cache-safety tests pass.
5. Notification preference, delivery, retry, and redaction tests pass.
6. Rent reminders are accurate and idempotent.
7. Maintenance lifecycle and visibility controls pass.
8. Reports reconcile and exports are safe.
9. Internal support controls and audit evidence pass.
10. Responsive and accessibility checks pass.
11. Backup and isolated restoration retain operational history.
12. CI quality gates pass on the final commit.
13. No unresolved critical or high-severity defect remains.
14. The branch is pushed and a reviewable pull request exists.
15. Paid notification channels and real JulyHost deployment remain explicitly deferred until approved and provisioned.

---

## 17. Sprint 06 Handover

Sprint 06 will consume the verified operational, financial, payment, tenant, maintenance, reporting, notification, and audit contracts to implement:

- URA EFRIS sandbox integration
- Fiscal-document mapping and submission
- Final security hardening and penetration-oriented testing
- Performance, resilience, backup, and disaster-recovery validation
- Real JulyHost production deployment after provisioning
- Production provider onboarding controls
- Pilot data preparation and user acceptance
- Release documentation, runbooks, and launch readiness

Sprint 06 must not calculate financial truth independently from the Sprint 03 ledger, infer payment success independently from Sprint 04 provider records, or expose tenant and operational data outside the verified Sprint 05 access boundaries.
