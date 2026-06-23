# BLISS Telehealth Scaling Implementation Phases

**Purpose:** Structural implementation roadmap for scaling BLISS Telehealth from a release-ready MVP into a competitive, intelligent, partner-ready telehealth platform.

**Current release baseline:** `v1.0.2-mvp-hotfix`

**Partner position:** Google partnership is active and should be treated as the primary partner path for cloud, AI, interoperability, notifications and deployment planning. Microsoft partnership is currently inactive pending response, so Microsoft products should remain documented as a standby or future co-partner option rather than the first implementation path.

---

## North Star

BLISS Telehealth should become more than a video appointment system. The product should become a coordinated digital care platform where patients, providers, care coordinators and administrators can move through care actions with clarity, trust, safety and measurable outcomes.

The next scaling cycle should focus on five product advantages:

1. A visibly more polished and reassuring user experience.
2. Better-controlled telehealth and communication integrations.
3. Smarter provider and coordinator workflows.
4. Data-driven operational and clinical insight.
5. Carefully governed AI assistance that supports care teams without replacing professional judgement.

---

# Current Internal API Foundation

The current platform is primarily powered by internal REST APIs built from scratch. External APIs have not yet taken over the core workflow. This is a strong position because BLISS owns the care logic and can add external services where those services improve reliability, scale or user reach.

## Internal APIs already implemented

### Authentication and session APIs

**Implementation status:** Built from scratch.

**Integration type:** Internal.

**Current role:** Login, registration, token refresh, password reset, logout and session handling.

**Core backend areas:**

- `pbbf-api/app/modules/auth/router.py`
- `pbbf-api/app/modules/auth/service.py`
- `pbbf-api/app/modules/auth/schemas.py`
- `pbbf-api/app/modules/auth/dependencies.py`
- `pbbf-api/app/common/utils/security.py`

**Core frontend areas:**

- `pbbf-telehealth/src/modules/auth/`
- `pbbf-telehealth/src/components/layout/Topbar.jsx`
- `pbbf-telehealth/src/modules/auth/store/`

---

### Admin user management APIs

**Implementation status:** Built from scratch.

**Integration type:** Internal.

**Current role:** Admin user provisioning, role changes, activation and deactivation.

**Core backend areas:**

- `pbbf-api/app/modules/users/router.py`
- `pbbf-api/app/modules/users/service.py`
- `pbbf-api/app/modules/users/repository.py`
- `pbbf-api/app/modules/users/schemas.py`

**Core frontend areas:**

- `pbbf-telehealth/src/pages/admin/Users.jsx`
- `pbbf-telehealth/src/modules/admin/services/adminApi.js`
- `pbbf-telehealth/src/modules/admin/__tests__/UsersActions.test.jsx`

---

### Patient intake APIs

**Implementation status:** Built from scratch.

**Integration type:** Internal.

**Current role:** Draft intake, submit intake, consent capture, provider/care-team review context and audit tracking.

**Core backend areas:**

- `pbbf-api/app/modules/intake/router.py`
- `pbbf-api/app/modules/intake/service.py`
- `pbbf-api/app/modules/intake/repository.py`
- `pbbf-api/app/modules/intake/schemas.py`

**Core frontend areas:**

- `pbbf-telehealth/src/modules/intake/`
- `pbbf-telehealth/src/pages/patient/Intake.jsx`

---

### Appointment APIs

**Implementation status:** Built from scratch.

**Integration type:** Internal.

**Current role:** Booking, cancellation, rescheduling, provider visibility, admin metrics and downstream notification creation.

**Core backend areas:**

- `pbbf-api/app/modules/appointments/router.py`
- `pbbf-api/app/modules/appointments/service.py`
- `pbbf-api/app/modules/appointments/repository.py`
- `pbbf-api/app/modules/appointments/schemas.py`
- `pbbf-api/app/db/models/appointment.py`

**Core frontend areas:**

- `pbbf-telehealth/src/modules/appointments/`
- `pbbf-telehealth/src/pages/patient/Appointments.jsx`
- `pbbf-telehealth/src/pages/provider/Dashboard.jsx`

---

### Screening APIs

**Implementation status:** Built from scratch.

**Integration type:** Internal.

**Current role:** EPDS submission, scoring, critical flagging, review visibility and admin metric updates.

**Core backend areas:**

- `pbbf-api/app/modules/screenings/router.py`
- `pbbf-api/app/modules/screenings/service.py`
- `pbbf-api/app/modules/screenings/repository.py`
- `pbbf-api/app/modules/screenings/schemas.py`
- `pbbf-api/app/db/models/screening.py`

**Core frontend areas:**

- `pbbf-telehealth/src/modules/screenings/`
- `pbbf-telehealth/src/pages/patient/Screening.jsx`

---

### Encounter and care-plan APIs

**Implementation status:** Built from scratch.

**Integration type:** Internal.

**Current role:** Draft encounter notes, finalize notes, patient care-plan aggregation and follow-up visibility.

**Core backend areas:**

- `pbbf-api/app/modules/encounters/router.py`
- `pbbf-api/app/modules/encounters/service.py`
- `pbbf-api/app/modules/encounters/repository.py`
- `pbbf-api/app/modules/encounters/schemas.py`
- `pbbf-api/app/db/models/encounter.py`

**Core frontend areas:**

- `pbbf-telehealth/src/modules/encounters/`
- `pbbf-telehealth/src/pages/provider/Notes.jsx`
- `pbbf-telehealth/src/pages/patient/CarePlan.jsx`

---

### Referral APIs

**Implementation status:** Built from scratch.

**Integration type:** Internal.

**Current role:** Create referrals, update referral status, complete outcomes, show referrals in care plan, update admin metrics and create audit/notification events.

**Core backend areas:**

- `pbbf-api/app/modules/referrals/router.py`
- `pbbf-api/app/modules/referrals/service.py`
- `pbbf-api/app/modules/referrals/repository.py`
- `pbbf-api/app/modules/referrals/schemas.py`
- `pbbf-api/app/db/models/referral.py`

**Core frontend areas:**

- `pbbf-telehealth/src/modules/referrals/`
- `pbbf-telehealth/src/pages/provider/Referrals.jsx`

---

### Telehealth session APIs

**Implementation status:** Built from scratch with provider-ready abstraction.

**Integration type:** Internal now; external-ready.

**Current role:** Session creation, meeting-link updates, join tracking, start, end, no-show, persisted meeting metadata and enriched session context.

**Core backend areas:**

- `pbbf-api/app/modules/telehealth/router.py`
- `pbbf-api/app/modules/telehealth/service.py`
- `pbbf-api/app/modules/telehealth/repository.py`
- `pbbf-api/app/modules/telehealth/schemas.py`
- `pbbf-api/app/modules/telehealth/providers.py`
- `pbbf-api/app/db/models/telehealth_session.py`
- `pbbf-api/scripts/migrations/20260623_telehealth_session_meeting_metadata.sql`

**Core frontend areas:**

- `pbbf-telehealth/src/pages/patient/Session.jsx`
- `pbbf-telehealth/src/modules/telehealth/hooks/useSessionAccess.js`
- `pbbf-telehealth/src/modules/telehealth/components/JoinSessionCard.jsx`
- `pbbf-telehealth/src/modules/telehealth/services/telehealthApi.js`

---

### Notification APIs

**Implementation status:** Built from scratch with channel abstraction.

**Integration type:** Internal now; external-ready.

**Current role:** In-app notifications, mark read, mark all read, delivery status tracking, dispatch job and workflow-triggered notifications.

**Core backend areas:**

- `pbbf-api/app/modules/notifications/router.py`
- `pbbf-api/app/modules/notifications/service.py`
- `pbbf-api/app/modules/notifications/repository.py`
- `pbbf-api/app/modules/notifications/channels.py`
- `pbbf-api/app/jobs/notification_jobs.py`
- `pbbf-api/app/jobs/reminder_jobs.py`

**Core frontend areas:**

- `pbbf-telehealth/src/modules/notifications/`
- `pbbf-telehealth/src/shared/hooks/useToast.js`
- `pbbf-telehealth/src/shared/components/ToastViewport.jsx`
- `pbbf-telehealth/src/components/layout/Topbar.jsx`

---

### Audit and admin reporting APIs

**Implementation status:** Built from scratch.

**Integration type:** Internal.

**Current role:** Server-side audit filters, pagination support, event details, dashboard metrics and operational CSV export.

**Core backend areas:**

- `pbbf-api/app/modules/audit/router.py`
- `pbbf-api/app/modules/audit/service.py`
- `pbbf-api/app/modules/audit/repository.py`
- `pbbf-api/app/modules/admin/router.py`
- `pbbf-api/app/modules/admin/service.py`
- `pbbf-api/app/modules/admin/repository.py`

**Core frontend areas:**

- `pbbf-telehealth/src/pages/admin/Reports.jsx`
- `pbbf-telehealth/src/pages/admin/AuditLogs.jsx`
- `pbbf-telehealth/src/modules/admin/components/AuditLogTable.jsx`
- `pbbf-telehealth/src/modules/admin/services/adminApi.js`

---

# Preferred External Partner Direction

## Active partner path: Google

Google should be treated as the primary implementation path where external cloud, AI, interoperability, video, messaging and analytics services are needed.

Recommended Google-aligned products:

- Google Cloud Run or Google Kubernetes Engine for application hosting.
- Cloud SQL for managed PostgreSQL.
- Secret Manager for environment secrets.
- Cloud Healthcare API for FHIR, HL7v2 and DICOM interoperability.
- Vertex AI and Vertex AI Search for Healthcare for AI-assisted summaries and intelligent data retrieval.
- Google Meet REST API or Calendar API conference data for meeting creation and meeting artifact workflows.
- Firebase Cloud Messaging for web and future mobile push notifications.
- Pub/Sub, Cloud Tasks and Cloud Scheduler for background jobs, reminders and asynchronous workflows.
- BigQuery and Looker Studio for analytics and operational dashboards.
- Cloud Logging, Cloud Monitoring and Error Reporting for observability.

## Standby partner path: Microsoft

Microsoft should remain documented as a future or standby partner path until the partnership extension receives confirmation.

Potential Microsoft options when the partnership becomes active again:

- Azure Health Data Services for FHIR, DICOM and healthcare data services.
- Azure OpenAI or Microsoft Copilot Studio for controlled AI workflows.
- Microsoft Teams Virtual Appointments or Teams EHR connector for video and EHR-connected virtual visit workflows.
- Power BI for partner-facing and leadership analytics.
- Microsoft Entra ID for enterprise identity.

---

# Phase L — Product Experience Upgrade

## Objective

Make BLISS visibly richer, easier to navigate and more reassuring for patients, providers, care coordinators and administrators. This phase should deliver the largest visible product improvement without depending on external APIs.

## Recommended implementation model

Build from scratch inside the existing frontend. This phase should be BLISS-owned because the user experience is the product identity.

## External API recommendation

No external API required for the base implementation. If user analytics are needed later, evaluate privacy-safe analytics only after health-data review.

## Backend files to inspect or modify

Generally no major backend changes are required unless new dashboard payloads are needed.

Inspect first:

- `pbbf-api/app/modules/admin/service.py`
- `pbbf-api/app/modules/appointments/service.py`
- `pbbf-api/app/modules/encounters/service.py`
- `pbbf-api/app/modules/referrals/service.py`
- `pbbf-api/app/modules/notifications/service.py`

Optional new backend files:

- `pbbf-api/app/modules/dashboard/router.py`
- `pbbf-api/app/modules/dashboard/service.py`
- `pbbf-api/app/modules/dashboard/schemas.py`
- `pbbf-api/tests/modules/dashboard/test_role_dashboard_context.py`

Suggested backend position:

- Place the new dashboard module under `pbbf-api/app/modules/dashboard/`.
- Register the router under `/api/v1/dashboard` in the existing application router registration flow.

## Frontend files to edit

- `pbbf-telehealth/src/pages/patient/Dashboard.jsx`
- `pbbf-telehealth/src/pages/provider/Dashboard.jsx`
- `pbbf-telehealth/src/pages/admin/Dashboard.jsx`
- `pbbf-telehealth/src/pages/patient/CarePlan.jsx`
- `pbbf-telehealth/src/pages/patient/Session.jsx`
- `pbbf-telehealth/src/components/layout/Sidebar.jsx`
- `pbbf-telehealth/src/components/layout/Topbar.jsx`
- `pbbf-telehealth/src/components/layout/AppShell.jsx`

## New frontend files to create

- `pbbf-telehealth/src/shared/components/StatusBadge.jsx`
- `pbbf-telehealth/src/shared/components/ActionPanel.jsx`
- `pbbf-telehealth/src/shared/components/EmptyState.jsx`
- `pbbf-telehealth/src/shared/components/MetricCard.jsx`
- `pbbf-telehealth/src/shared/components/Timeline.jsx`
- `pbbf-telehealth/src/modules/dashboard/components/PatientJourneyCard.jsx`
- `pbbf-telehealth/src/modules/dashboard/components/ProviderWorkQueue.jsx`
- `pbbf-telehealth/src/modules/dashboard/components/AdminOperationsSnapshot.jsx`
- `pbbf-telehealth/src/modules/dashboard/components/CareCoordinatorQueuePreview.jsx`
- `pbbf-telehealth/src/modules/dashboard/__tests__/PatientDashboardExperience.test.jsx`
- `pbbf-telehealth/src/modules/dashboard/__tests__/ProviderDashboardExperience.test.jsx`

## Implementation structure

1. Introduce a shared visual language with reusable status badges, metric cards and action cards.
2. Redesign patient dashboard around next best action, upcoming visit, care plan progress and unread notifications.
3. Redesign provider dashboard around assigned appointments, pending screenings, open note drafts and referral follow-up.
4. Redesign care coordinator view around referral status and overdue follow-up.
5. Redesign admin dashboard around operational trends and release-readiness confidence.
6. Add consistent loading, error and empty states across all dashboards.

## Acceptance criteria

- Each role has a visibly improved dashboard.
- No dashboard shows generic placeholder wording where real data exists.
- The patient journey is understandable within five seconds of opening the dashboard.
- The provider can identify the next clinical action quickly.
- The care coordinator can identify pending follow-up work quickly.
- Frontend test suite and build pass.

---

# Phase M — Google-First Telehealth Video Integration

## Objective

Move from managed external links to a real partner-backed telehealth meeting workflow using Google as the active partner path.

## Recommended implementation model

Hybrid. Keep BLISS appointment, session, audit and role-access logic internal. Use Google Meet or Google Calendar conference creation for meeting generation and meeting metadata.

## External API recommendation

Primary path:

- Google Meet REST API for creating and managing Meet spaces where available.
- Google Calendar API conference data if the product prefers appointment-calendar synchronization with generated Meet links.

Standby path:

- Microsoft Teams Virtual Appointments or Teams EHR connector only when the Microsoft partnership becomes active again.

## Backend files to edit

- `pbbf-api/app/modules/telehealth/providers.py`
- `pbbf-api/app/modules/telehealth/service.py`
- `pbbf-api/app/modules/telehealth/repository.py`
- `pbbf-api/app/modules/telehealth/schemas.py`
- `pbbf-api/app/db/models/telehealth_session.py`
- `pbbf-api/app/common/config/settings.py`

## Backend files to create

- `pbbf-api/app/modules/telehealth/google_meet_provider.py`
- `pbbf-api/app/modules/telehealth/google_calendar_provider.py`
- `pbbf-api/app/modules/telehealth/provider_contracts.py`
- `pbbf-api/app/modules/telehealth/webhooks.py`
- `pbbf-api/tests/modules/telehealth/test_google_meet_provider_contract.py`
- `pbbf-api/tests/modules/telehealth/test_meeting_artifact_sync.py`
- `pbbf-api/scripts/migrations/2026xxxx_telehealth_google_meet_fields.sql`

Suggested backend position:

- Keep all provider-specific code under `pbbf-api/app/modules/telehealth/`.
- Keep one internal provider interface and allow provider selection by settings.
- Store Google meeting identifiers in `telehealth_sessions` while keeping BLISS session status as the system of record.

## Frontend files to edit

- `pbbf-telehealth/src/pages/patient/Session.jsx`
- `pbbf-telehealth/src/modules/telehealth/components/JoinSessionCard.jsx`
- `pbbf-telehealth/src/modules/telehealth/hooks/useSessionAccess.js`
- `pbbf-telehealth/src/modules/telehealth/services/telehealthApi.js`
- `pbbf-telehealth/src/pages/provider/Dashboard.jsx`

## Frontend files to create

- `pbbf-telehealth/src/modules/telehealth/components/MeetingLinkManager.jsx`
- `pbbf-telehealth/src/modules/telehealth/components/ProviderSessionControls.jsx`
- `pbbf-telehealth/src/modules/telehealth/components/MeetingArtifactPanel.jsx`
- `pbbf-telehealth/src/modules/telehealth/__tests__/MeetingLinkManager.test.jsx`
- `pbbf-telehealth/src/modules/telehealth/__tests__/ProviderSessionControls.test.jsx`

## Environment variables to add

- `PBBF_TELEHEALTH_PROVIDER=local|google_meet|google_calendar|manual`
- `PBBF_GOOGLE_PROJECT_ID=`
- `PBBF_GOOGLE_WORKSPACE_DOMAIN=`
- `PBBF_GOOGLE_SERVICE_ACCOUNT_JSON=`
- `PBBF_GOOGLE_MEET_ORGANIZER_EMAIL=`
- `PBBF_TELEHEALTH_PUBLIC_BASE_URL=`

## Implementation structure

1. Define a provider contract that returns `external_meeting_id`, `patient_join_url`, `provider_join_url`, optional transcript reference and optional recording reference.
2. Implement a Google provider behind the provider contract.
3. Keep the existing local/manual provider for development and testing.
4. Add meeting artifact synchronization for transcripts and recordings only after privacy and consent decisions are approved.
5. Add provider-side meeting link manager for staff to regenerate or update meeting links.
6. Add audit events for meeting creation, link update, join, leave, start, end, no-show and artifact retrieval.

## Acceptance criteria

- Patient sees real appointment time, provider name and Google meeting link.
- Provider can see the same meeting context and launch the provider meeting view.
- Meeting links persist after restart and refresh.
- Provider-generated link updates are audited.
- Local/manual provider remains available for development.
- External provider failures fall back to manual link entry.

---

# Phase N — Production Messaging and Patient Engagement

## Objective

Turn notifications from an internal foundation into reliable patient engagement across in-app, email, SMS, WhatsApp and future push notifications.

## Recommended implementation model

Hybrid. Keep notification rules, templates, preferences, audit and clinical workflow triggers inside BLISS. Use Google-aligned or best regional providers for delivery.

## External API recommendation

Primary Google path:

- Firebase Cloud Messaging for browser and future mobile push.
- Gmail API or SMTP only for limited internal use, not preferred for high-volume transactional email.

Best-of-best delivery path:

- SendGrid, Amazon SES or Mailgun for transactional email.
- Twilio, Africa’s Talking or a regional telecom aggregator for SMS and WhatsApp.

## Backend files to edit

- `pbbf-api/app/modules/notifications/channels.py`
- `pbbf-api/app/modules/notifications/service.py`
- `pbbf-api/app/modules/notifications/router.py`
- `pbbf-api/app/jobs/notification_jobs.py`
- `pbbf-api/app/common/config/settings.py`
- `pbbf-api/app/db/models/notification.py`

## Backend files to create

- `pbbf-api/app/modules/notifications/providers/base.py`
- `pbbf-api/app/modules/notifications/providers/sendgrid_provider.py`
- `pbbf-api/app/modules/notifications/providers/firebase_provider.py`
- `pbbf-api/app/modules/notifications/providers/twilio_provider.py`
- `pbbf-api/app/modules/notifications/providers/console_provider.py`
- `pbbf-api/app/modules/notifications/templates.py`
- `pbbf-api/app/modules/notifications/preferences.py`
- `pbbf-api/app/modules/notifications/webhooks.py`
- `pbbf-api/scripts/migrations/2026xxxx_notification_preferences_delivery.sql`
- `pbbf-api/tests/modules/notifications/test_provider_contracts.py`
- `pbbf-api/tests/modules/notifications/test_notification_preferences.py`
- `pbbf-api/tests/modules/notifications/test_delivery_webhooks.py`

## Frontend files to edit

- `pbbf-telehealth/src/modules/notifications/components/NotificationCenter.jsx`
- `pbbf-telehealth/src/modules/notifications/services/notificationsApi.js`
- `pbbf-telehealth/src/components/layout/Topbar.jsx`

## Frontend files to create

- `pbbf-telehealth/src/modules/notifications/components/NotificationPreferences.jsx`
- `pbbf-telehealth/src/modules/notifications/components/DeliveryHistory.jsx`
- `pbbf-telehealth/src/modules/notifications/hooks/usePushRegistration.js`
- `pbbf-telehealth/src/modules/notifications/services/firebaseMessaging.js`
- `pbbf-telehealth/public/firebase-messaging-sw.js`
- `pbbf-telehealth/src/modules/notifications/__tests__/NotificationPreferences.test.jsx`
- `pbbf-telehealth/src/modules/notifications/__tests__/PushRegistration.test.jsx`

## Environment variables to add

- `PBBF_EMAIL_PROVIDER=console|sendgrid|ses|smtp`
- `PBBF_SENDGRID_API_KEY=`
- `PBBF_SMS_PROVIDER=none|twilio|africas_talking`
- `PBBF_TWILIO_ACCOUNT_SID=`
- `PBBF_TWILIO_AUTH_TOKEN=`
- `PBBF_TWILIO_FROM_NUMBER=`
- `PBBF_FIREBASE_PROJECT_ID=`
- `PBBF_FIREBASE_SERVER_KEY=`
- `PBBF_NOTIFICATION_WEBHOOK_SECRET=`

## Implementation structure

1. Create provider contracts for email, SMS, WhatsApp and push.
2. Add patient notification preferences and consent controls.
3. Add channel-specific templates for appointment reminders, EPDS follow-up, referral follow-up and care-plan updates.
4. Add delivery webhooks for sent, failed, bounced, opened and unsubscribed where provider supports them.
5. Add retry policies and failure dashboard.
6. Add browser push registration using Firebase Cloud Messaging.

## Acceptance criteria

- In-app notification still works without external providers.
- Email provider can be configured without changing workflow code.
- SMS/WhatsApp cannot send unless consent exists.
- Delivery status is visible to admin.
- Failed messages can be retried safely.
- Browser push registration is optional and does not block core workflows.

---

# Phase O — Google Cloud Infrastructure and Deployment Scale

## Objective

Prepare BLISS for real production onboarding with stable hosting, environment separation, secrets, monitoring, backups, observability and CI/CD release gates.

## Recommended implementation model

Hybrid. Build release discipline internally, then run infrastructure on Google Cloud because the Google partnership is active.

## External API recommendation

Primary Google path:

- Cloud Run for API hosting.
- Cloud SQL for PostgreSQL.
- Secret Manager for secrets.
- Cloud Build or GitHub Actions for CI/CD.
- Cloud Logging, Cloud Monitoring and Error Reporting for observability.
- Cloud Scheduler, Pub/Sub and Cloud Tasks for background workflows.

Microsoft standby path:

- Azure App Service or Azure Container Apps, Azure Database for PostgreSQL, Azure Key Vault and Azure Monitor if Microsoft partnership becomes active.

## Backend files to edit

- `pbbf-api/app/common/config/settings.py`
- `pbbf-api/app/main.py`
- `pbbf-api/app/db/session.py`
- `pbbf-api/scripts/backup_db.sh`

## Backend files to create

- `pbbf-api/Dockerfile`
- `pbbf-api/cloudbuild.yaml`
- `pbbf-api/scripts/run_migrations.sh`
- `pbbf-api/scripts/restore_db.sh`
- `pbbf-api/scripts/verify_release.sh`
- `pbbf-api/docs/deployment/google-cloud-run.md`
- `pbbf-api/docs/operations/backup-restore.md`
- `pbbf-api/docs/operations/incident-response.md`

## Frontend files to create or edit

- `pbbf-telehealth/Dockerfile`
- `pbbf-telehealth/nginx.conf`
- `pbbf-telehealth/.env.production.example`
- `pbbf-telehealth/docs/deployment/google-cloud-run.md`
- `.github/workflows/release.yml`
- `.github/workflows/backend-tests.yml`
- `.github/workflows/frontend-tests.yml`

## Environment variables to add

- `PBBF_APP_ENV=staging|production`
- `PBBF_DATABASE_URL=`
- `PBBF_SECRET_KEY=`
- `PBBF_CORS_ALLOW_ORIGINS=`
- `PBBF_BASE_EXTERNAL_URL=`
- `PBBF_LOG_JSON=true`
- `PBBF_RATE_LIMIT_ENABLED=true`

## Implementation structure

1. Create separate staging and production configs.
2. Containerize backend and frontend separately.
3. Add CI/CD gates for backend tests, frontend tests and build.
4. Add Cloud Run deployment scripts.
5. Move secrets to Secret Manager.
6. Add structured logs and request IDs to production logs.
7. Add uptime checks and alerting.
8. Add backup and restore validation jobs.

## Acceptance criteria

- Staging deploy runs without manual code edits.
- Production deploy requires a tagged release and passing CI.
- Secrets do not live in source code.
- Database backups run and restore validation is documented.
- API health and readiness checks are monitored.

---

# Phase P — AI-Assisted Care Intelligence

## Objective

Add safe AI assistance for providers, care coordinators and administrators while protecting clinical judgement and patient trust.

## Recommended implementation model

Hybrid. Build workflow, safety, audit, review and data boundaries internally. Use Google Vertex AI as the primary AI provider because Google partnership is active.

## External API recommendation

Primary Google path:

- Vertex AI.
- Vertex AI Search for Healthcare when indexed clinical documents and FHIR-aligned records become available.
- MedLM or Gemini medical/healthcare-capable models only if approved under proper commercial and privacy review.

Microsoft standby path:

- Azure OpenAI only if Microsoft partnership becomes active and the required compliance agreements are confirmed.

## Backend files to edit

- `pbbf-api/app/modules/intake/service.py`
- `pbbf-api/app/modules/screenings/service.py`
- `pbbf-api/app/modules/encounters/service.py`
- `pbbf-api/app/modules/referrals/service.py`
- `pbbf-api/app/modules/audit/service.py`
- `pbbf-api/app/common/config/settings.py`

## Backend files to create

- `pbbf-api/app/modules/ai/router.py`
- `pbbf-api/app/modules/ai/service.py`
- `pbbf-api/app/modules/ai/repository.py`
- `pbbf-api/app/modules/ai/schemas.py`
- `pbbf-api/app/modules/ai/providers/base.py`
- `pbbf-api/app/modules/ai/providers/google_vertex_provider.py`
- `pbbf-api/app/modules/ai/safety.py`
- `pbbf-api/app/modules/ai/prompts.py`
- `pbbf-api/app/modules/ai/redaction.py`
- `pbbf-api/app/db/models/ai_assistance_event.py`
- `pbbf-api/scripts/migrations/2026xxxx_ai_assistance_events.sql`
- `pbbf-api/tests/modules/ai/test_ai_safety_contracts.py`
- `pbbf-api/tests/modules/ai/test_ai_audit_events.py`

## Frontend files to create

- `pbbf-telehealth/src/modules/ai/components/AiSummaryPanel.jsx`
- `pbbf-telehealth/src/modules/ai/components/AiDraftNotePanel.jsx`
- `pbbf-telehealth/src/modules/ai/components/AiReviewNotice.jsx`
- `pbbf-telehealth/src/modules/ai/services/aiApi.js`
- `pbbf-telehealth/src/modules/ai/hooks/useAiAssistance.js`
- `pbbf-telehealth/src/modules/ai/__tests__/AiSummaryPanel.test.jsx`
- `pbbf-telehealth/src/modules/ai/__tests__/AiDraftNotePanel.test.jsx`

## Frontend files to edit

- `pbbf-telehealth/src/pages/provider/Notes.jsx`
- `pbbf-telehealth/src/pages/provider/Dashboard.jsx`
- `pbbf-telehealth/src/pages/admin/Dashboard.jsx`
- `pbbf-telehealth/src/pages/patient/CarePlan.jsx`

## Environment variables to add

- `PBBF_AI_PROVIDER=disabled|google_vertex|azure_openai|local_mock`
- `PBBF_GOOGLE_VERTEX_PROJECT_ID=`
- `PBBF_GOOGLE_VERTEX_LOCATION=`
- `PBBF_GOOGLE_VERTEX_MODEL=`
- `PBBF_AI_MAX_TOKENS=`
- `PBBF_AI_REDACTION_ENABLED=true`
- `PBBF_AI_HUMAN_REVIEW_REQUIRED=true`

## Implementation structure

1. Start with provider-only AI summaries.
2. Add intake summary, EPDS summary and visit preparation summary.
3. Add encounter draft-note assistant behind review-and-edit only.
4. Add care-plan plain-language explanation only after clinician approval workflow exists.
5. Store every request, response, user edit and acceptance event in audit records.
6. Add redaction and prompt templates before enabling production use.

## Acceptance criteria

- AI cannot finalize clinical notes automatically.
- AI outputs are clearly marked as assistive.
- AI requests are audited.
- Providers must review and edit before saving AI-generated draft text.
- Patient-facing AI content requires approval rules.

---

# Phase Q — Provider Productivity Workspace

## Objective

Create a provider workspace that gives clinicians a complete patient context before, during and after a visit.

## Recommended implementation model

Build from scratch using existing internal APIs. Add AI components only after Phase P establishes AI safety and audit controls.

## Backend files to edit

- `pbbf-api/app/modules/appointments/service.py`
- `pbbf-api/app/modules/intake/service.py`
- `pbbf-api/app/modules/screenings/service.py`
- `pbbf-api/app/modules/encounters/service.py`
- `pbbf-api/app/modules/referrals/service.py`

## Backend files to create

- `pbbf-api/app/modules/provider_workspace/router.py`
- `pbbf-api/app/modules/provider_workspace/service.py`
- `pbbf-api/app/modules/provider_workspace/repository.py`
- `pbbf-api/app/modules/provider_workspace/schemas.py`
- `pbbf-api/tests/modules/provider_workspace/test_provider_visit_context.py`

## Frontend files to edit

- `pbbf-telehealth/src/pages/provider/Dashboard.jsx`
- `pbbf-telehealth/src/pages/provider/Notes.jsx`
- `pbbf-telehealth/src/pages/provider/Referrals.jsx`

## Frontend files to create

- `pbbf-telehealth/src/pages/provider/VisitWorkspace.jsx`
- `pbbf-telehealth/src/modules/providerWorkspace/components/PatientSnapshot.jsx`
- `pbbf-telehealth/src/modules/providerWorkspace/components/VisitTimeline.jsx`
- `pbbf-telehealth/src/modules/providerWorkspace/components/ClinicalActionPanel.jsx`
- `pbbf-telehealth/src/modules/providerWorkspace/components/ScreeningAlertCard.jsx`
- `pbbf-telehealth/src/modules/providerWorkspace/services/providerWorkspaceApi.js`
- `pbbf-telehealth/src/modules/providerWorkspace/__tests__/VisitWorkspace.test.jsx`

## Implementation structure

1. Create `/api/v1/provider-workspace/patients/{patient_id}/context`.
2. Return patient profile, latest intake, screenings, appointments, notes, referrals and notifications summary.
3. Add provider visit workspace route.
4. Add action buttons for note draft, finalize encounter, create referral and open session.
5. Add timeline of patient activity.

## Acceptance criteria

- Provider can open one page and understand the patient context.
- Provider does not need to jump between four pages before a session.
- Role boundaries remain enforced.
- Workspace does not expose unrelated patient records.

---

# Phase R — Care Coordinator Command Center

## Objective

Turn care coordination into a measurable operational workflow with referral queues, missed visit recovery and follow-up accountability.

## Recommended implementation model

Build from scratch because the workflow is BLISS-specific.

## External API recommendation

Use SMS/WhatsApp providers after Phase N if coordinators need patient outreach directly from the command center.

## Backend files to edit

- `pbbf-api/app/modules/referrals/service.py`
- `pbbf-api/app/modules/referrals/repository.py`
- `pbbf-api/app/modules/appointments/service.py`
- `pbbf-api/app/modules/notifications/service.py`

## Backend files to create

- `pbbf-api/app/modules/care_coordination/router.py`
- `pbbf-api/app/modules/care_coordination/service.py`
- `pbbf-api/app/modules/care_coordination/repository.py`
- `pbbf-api/app/modules/care_coordination/schemas.py`
- `pbbf-api/app/db/models/care_task.py`
- `pbbf-api/app/db/models/contact_attempt.py`
- `pbbf-api/scripts/migrations/2026xxxx_care_coordination_tasks.sql`
- `pbbf-api/tests/modules/care_coordination/test_care_task_queue.py`
- `pbbf-api/tests/modules/care_coordination/test_contact_attempts.py`

## Frontend files to create

- `pbbf-telehealth/src/pages/careCoordinator/CommandCenter.jsx`
- `pbbf-telehealth/src/modules/careCoordination/components/ReferralQueue.jsx`
- `pbbf-telehealth/src/modules/careCoordination/components/MissedVisitQueue.jsx`
- `pbbf-telehealth/src/modules/careCoordination/components/ContactAttemptForm.jsx`
- `pbbf-telehealth/src/modules/careCoordination/components/FollowUpAgingBadge.jsx`
- `pbbf-telehealth/src/modules/careCoordination/services/careCoordinationApi.js`
- `pbbf-telehealth/src/modules/careCoordination/__tests__/CommandCenter.test.jsx`

## Frontend files to edit

- `pbbf-telehealth/src/app/AppRoutes.jsx`
- `pbbf-telehealth/src/shared/constants/navigation.js`
- `pbbf-telehealth/src/components/layout/Sidebar.jsx`

## Implementation structure

1. Create care tasks for referral follow-up, missed visit recovery and critical screening follow-up.
2. Create assignable queues by status, due date and coordinator.
3. Add contact attempts and outcomes.
4. Add escalation states.
5. Add admin metrics for overdue tasks and completion rate.

## Acceptance criteria

- Coordinator sees a true work queue, not only referral records.
- Every follow-up attempt is auditable.
- Overdue tasks are visible.
- Completion outcomes update patient care-plan and admin reporting.

---

# Phase S — Healthcare Interoperability and FHIR Foundation

## Objective

Prepare BLISS for partner and health-system interoperability by mapping internal records to FHIR-compatible resources.

## Recommended implementation model

Hybrid. Build internal FHIR mapping from scratch first. Use Google Cloud Healthcare API as the first external FHIR store when partner integration requires it.

## External API recommendation

Primary Google path:

- Google Cloud Healthcare API with FHIR stores.

Microsoft standby path:

- Azure Health Data Services FHIR service after Microsoft partnership activation.

## Backend files to create

- `pbbf-api/app/modules/interoperability/router.py`
- `pbbf-api/app/modules/interoperability/service.py`
- `pbbf-api/app/modules/interoperability/schemas.py`
- `pbbf-api/app/modules/interoperability/fhir_mapper.py`
- `pbbf-api/app/modules/interoperability/google_healthcare_api.py`
- `pbbf-api/app/modules/interoperability/export_jobs.py`
- `pbbf-api/tests/modules/interoperability/test_fhir_patient_mapping.py`
- `pbbf-api/tests/modules/interoperability/test_fhir_appointment_mapping.py`
- `pbbf-api/tests/modules/interoperability/test_fhir_observation_mapping.py`

## Internal resource mapping

- Patient profile → FHIR Patient
- Appointment → FHIR Appointment
- EPDS screening → FHIR Observation or QuestionnaireResponse
- Encounter note → FHIR Encounter and DocumentReference
- Care plan → FHIR CarePlan
- Referral → FHIR ServiceRequest
- Notification/audit event → internal only unless partner requires export

## Frontend files to create

- `pbbf-telehealth/src/pages/admin/Interoperability.jsx`
- `pbbf-telehealth/src/modules/interoperability/components/FhirExportPanel.jsx`
- `pbbf-telehealth/src/modules/interoperability/components/PartnerConnectionStatus.jsx`
- `pbbf-telehealth/src/modules/interoperability/services/interoperabilityApi.js`

## Frontend files to edit

- `pbbf-telehealth/src/shared/constants/navigation.js`
- `pbbf-telehealth/src/app/AppRoutes.jsx`

## Environment variables to add

- `PBBF_INTEROP_PROVIDER=disabled|google_healthcare|azure_health_data_services`
- `PBBF_GOOGLE_HEALTHCARE_DATASET=`
- `PBBF_GOOGLE_HEALTHCARE_FHIR_STORE=`
- `PBBF_GOOGLE_HEALTHCARE_LOCATION=`

## Implementation structure

1. Build internal FHIR mapping and tests before connecting to any external FHIR server.
2. Add export-only first.
3. Add import/sync only after conflict-handling rules are clear.
4. Add partner-specific mapping profiles.
5. Add audit events for export, import and partner synchronization.

## Acceptance criteria

- Internal records map consistently to FHIR-compatible JSON.
- No external export happens without admin action and configuration.
- Partner exports are auditable.
- Data minimization rules are documented.

---

# Phase T — Analytics, Outcomes and Executive Intelligence

## Objective

Turn operational data into leadership-ready insight for care quality, patient engagement and partner reporting.

## Recommended implementation model

Start built from scratch using internal admin metrics. Add Google BigQuery and Looker Studio when data volume and reporting needs increase.

## External API recommendation

Primary Google path:

- BigQuery for analytics storage.
- Looker Studio or Looker for dashboards.
- Pub/Sub for event streaming.

Microsoft standby path:

- Power BI if Microsoft partnership becomes active.

## Backend files to edit

- `pbbf-api/app/modules/admin/repository.py`
- `pbbf-api/app/modules/admin/service.py`
- `pbbf-api/app/modules/audit/service.py`

## Backend files to create

- `pbbf-api/app/modules/analytics/router.py`
- `pbbf-api/app/modules/analytics/service.py`
- `pbbf-api/app/modules/analytics/repository.py`
- `pbbf-api/app/modules/analytics/schemas.py`
- `pbbf-api/app/modules/analytics/events.py`
- `pbbf-api/app/jobs/analytics_jobs.py`
- `pbbf-api/tests/modules/analytics/test_outcome_metrics.py`
- `pbbf-api/tests/modules/analytics/test_event_exports.py`

## Frontend files to create

- `pbbf-telehealth/src/pages/admin/Analytics.jsx`
- `pbbf-telehealth/src/modules/analytics/components/OutcomeDashboard.jsx`
- `pbbf-telehealth/src/modules/analytics/components/NoShowTrendChart.jsx`
- `pbbf-telehealth/src/modules/analytics/components/ReferralCompletionChart.jsx`
- `pbbf-telehealth/src/modules/analytics/components/ScreeningRiskTrend.jsx`
- `pbbf-telehealth/src/modules/analytics/services/analyticsApi.js`

## Frontend files to edit

- `pbbf-telehealth/src/shared/constants/navigation.js`
- `pbbf-telehealth/src/app/AppRoutes.jsx`

## Metrics to implement

- Appointment booking volume.
- Appointment completion rate.
- No-show rate.
- EPDS completion rate.
- Critical screening count and trend.
- Referral completion rate.
- Referral aging.
- Notification delivery success rate.
- Care-plan engagement.
- Provider documentation completion.

## Acceptance criteria

- Admin can filter metrics by date range.
- Metrics are tied to current workflow definitions.
- Reports can be exported.
- No patient-level sensitive analytics are exposed without authorization.

---

# Phase U — Mobile and Push Readiness

## Objective

Prepare BLISS for mobile-first adoption without rushing into a separate mobile app too early.

## Recommended implementation model

Start with a progressive web app and mobile-responsive web experience. Build a native mobile app only after core web workflows are polished and usage data proves patient demand.

## External API recommendation

Primary Google path:

- Firebase Cloud Messaging for push notifications.
- Firebase App Distribution only if mobile app testing begins.
- Google Play Console for Android distribution later.

## Frontend files to edit

- `pbbf-telehealth/src/main.jsx`
- `pbbf-telehealth/src/app/AppRoutes.jsx`
- `pbbf-telehealth/src/components/layout/AppShell.jsx`
- `pbbf-telehealth/src/pages/patient/Dashboard.jsx`
- `pbbf-telehealth/src/pages/patient/Session.jsx`

## Frontend files to create

- `pbbf-telehealth/public/manifest.webmanifest`
- `pbbf-telehealth/public/service-worker.js`
- `pbbf-telehealth/src/shared/hooks/useInstallPrompt.js`
- `pbbf-telehealth/src/shared/components/MobileBottomNav.jsx`
- `pbbf-telehealth/src/modules/mobile/components/AppInstallBanner.jsx`
- `pbbf-telehealth/src/modules/mobile/__tests__/MobileNavigation.test.jsx`

## Backend files to create or edit

- `pbbf-api/app/modules/devices/router.py`
- `pbbf-api/app/modules/devices/service.py`
- `pbbf-api/app/modules/devices/repository.py`
- `pbbf-api/app/modules/devices/schemas.py`
- `pbbf-api/app/db/models/user_device.py`
- `pbbf-api/scripts/migrations/2026xxxx_user_devices.sql`

## Implementation structure

1. Make the current web app excellent on mobile screens.
2. Add PWA install prompt and service worker.
3. Add user device registration for push notifications.
4. Use Firebase Cloud Messaging for web push first.
5. Consider native mobile only after web adoption is proven.

## Acceptance criteria

- Patient can complete key workflows on mobile web.
- Push token registration is tied to authenticated users.
- Logout removes or deactivates device tokens.
- PWA install does not break browser workflows.

---

# Phase V — Security, Compliance and Governance Scale

## Objective

Make privacy, auditability, consent and operational security strong enough for larger deployments and partner scrutiny.

## Recommended implementation model

Build security policy enforcement internally while using Google Cloud security products where helpful.

## External API recommendation

Primary Google path:

- Secret Manager.
- Cloud Armor.
- Cloud Audit Logs.
- Cloud IAM.
- Cloud KMS.
- Security Command Center when the environment matures.

Microsoft standby path:

- Microsoft Entra ID, Microsoft Purview and Azure Key Vault if Microsoft partnership becomes active.

## Backend files to inspect or edit

- `pbbf-api/app/common/config/settings.py`
- `pbbf-api/app/common/middleware/`
- `pbbf-api/app/modules/audit/`
- `pbbf-api/app/modules/auth/`
- `pbbf-api/app/modules/users/`
- `pbbf-api/tests/security/`

## Backend files to create

- `pbbf-api/app/modules/consent/router.py`
- `pbbf-api/app/modules/consent/service.py`
- `pbbf-api/app/modules/consent/repository.py`
- `pbbf-api/app/modules/consent/schemas.py`
- `pbbf-api/app/db/models/consent_event.py`
- `pbbf-api/app/db/models/data_access_event.py`
- `pbbf-api/docs/security/role-boundary-matrix.md`
- `pbbf-api/docs/security/data-retention-policy.md`
- `pbbf-api/docs/security/ai-governance-policy.md`
- `pbbf-api/docs/security/incident-response-playbook.md`

## Frontend files to create or edit

- `pbbf-telehealth/src/pages/admin/DataGovernance.jsx`
- `pbbf-telehealth/src/modules/admin/components/ConsentPolicyPanel.jsx`
- `pbbf-telehealth/src/modules/admin/components/DataAccessReview.jsx`
- `pbbf-telehealth/src/modules/admin/components/AiGovernancePanel.jsx`

## Implementation structure

1. Formalize role-boundary matrix.
2. Add data access audit review.
3. Add consent versioning visible to admin and patient.
4. Add AI governance policy before any patient-facing AI.
5. Add incident response and backup restore drills.
6. Add security test coverage for every new integration.

## Acceptance criteria

- Every sensitive view has a role-boundary test.
- Consent changes are versioned.
- Admin can review high-risk access events.
- External integrations are documented with data-flow diagrams.

---

# Recommended Build Order

1. **Phase L — Product Experience Upgrade**
2. **Phase N — Production Messaging and Patient Engagement**
3. **Phase M — Google-First Telehealth Video Integration**
4. **Phase Q — Provider Productivity Workspace**
5. **Phase R — Care Coordinator Command Center**
6. **Phase O — Google Cloud Infrastructure and Deployment Scale**
7. **Phase P — AI-Assisted Care Intelligence**
8. **Phase T — Analytics, Outcomes and Executive Intelligence**
9. **Phase S — Healthcare Interoperability and FHIR Foundation**
10. **Phase U — Mobile and Push Readiness**
11. **Phase V — Security, Compliance and Governance Scale**

The first three phases should be treated as the immediate competitive upgrade package because they are the most visible and foundational: product polish, production messaging and Google-backed telehealth integration.

---

# Release Discipline for Every Scaling Phase

Every phase should follow the same disciplined implementation structure:

1. Confirm clean repo.
2. Inspect current files before editing.
3. Add backend tests first where behavior is critical.
4. Add frontend tests for UI behavior.
5. Run targeted tests.
6. Run safety suites.
7. Commit one functional package at a time.
8. Push after tests pass.
9. Tag only after release-level validation.

Recommended commit pattern:

```text
feat: upgrade patient and provider dashboard experience
feat: add production notification provider contracts
feat: integrate google meet telehealth provider
feat: add provider visit workspace
feat: add care coordination command center
feat: deploy google cloud run production baseline
feat: add google vertex ai provider summaries
feat: add outcome analytics dashboard
feat: add fhir interoperability export foundation
feat: add mobile push readiness
chore: add security governance and data access review
```

---

# Recommended Google-first Architecture

```text
Frontend
  React/Vite web app
  Progressive web app readiness
  Firebase Cloud Messaging for push

Backend
  FastAPI REST API
  PostgreSQL via Cloud SQL
  Cloud Run deployment
  Secret Manager for secrets
  Cloud Scheduler for recurring reminders
  Cloud Tasks for targeted retries
  Pub/Sub for event-driven notification and analytics workflows

Healthcare data layer
  Internal PostgreSQL operational schema first
  Google Cloud Healthcare API FHIR store later
  BigQuery analytics export later

AI layer
  Internal AI governance module
  Google Vertex AI provider adapter
  Prompt templates and clinical review workflow

Video layer
  Internal telehealth session model remains source of truth
  Google Meet provider adapter generates meeting spaces and artifacts

Observability
  Cloud Logging
  Cloud Monitoring
  Error Reporting
  Uptime checks
```

---

# Source Notes for Partner Product Planning

Google Cloud Healthcare API supports healthcare data storage and access, including FHIR stores and healthcare interoperability use cases. It also provides a managed bridge between existing care systems and applications built on Google Cloud.

Google Meet REST API provides a way to create and manage meetings, retrieve conference records, list participants, and access meeting artifacts such as recordings and transcripts.

Firebase Cloud Messaging supports web push notifications through browser push APIs and service workers, making it a strong fit for patient engagement and future mobile readiness.

Google Cloud Tasks and Pub/Sub support asynchronous workloads, retries and background processing patterns. Cloud Scheduler supports cron-style scheduled work that can trigger HTTP endpoints or Pub/Sub topics.

Microsoft Azure Health Data Services and Microsoft Teams EHR connector should remain as standby options while the Microsoft partnership response is pending. Azure Health Data Services supports FHIR/DICOM healthcare data services, and Microsoft Teams EHR connector supports virtual appointment workflows with Epic and related healthcare scenarios.

---

# Closing Recommendation

The best next move is to treat the next cycle as a competitive transformation, not a random feature expansion. The product should become visibly better first, then more connected, then more intelligent.

The recommended immediate package is:

1. Product Experience Upgrade.
2. Production Messaging and Patient Engagement.
3. Google-First Telehealth Video Integration.

That package will make BLISS feel more valuable to users, more credible to partners and more prepared for AI-powered care coordination.
