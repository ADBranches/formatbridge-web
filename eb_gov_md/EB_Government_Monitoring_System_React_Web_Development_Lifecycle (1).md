# EB Government Monitoring System — React Web App Development Lifecycle Guide

**Project:** EB Government Monitoring System  
**Platform for this lifecycle:** Web App MVP  
**Frontend stack:** React.js + TypeScript + Vite + Tailwind CSS  
**Backend assumption:** API-first backend, preferably NestJS/Node.js or equivalent REST API  
**Database assumption:** PostgreSQL  
**Product approach:** Modular MVP that can grow into production without being rewritten

---

## 0. Development Strategy Summary

The web app should be developed as a **React-based modular frontend**, not as a random collection of pages.

The MVP should start with the most important government monitoring workflows:

1. Authentication and role-based access
2. Government admin dashboard
3. Project management
4. Contractor management
5. Evidence and receipt upload/review
6. M&E review workflow
7. Approval workflow
8. Funds tracking
9. Audit and compliance
10. Reports and notifications
11. User management and settings

The frontend should be structured so that each major business area becomes a **feature module**.

---

## 1. Recommended Web App Folder Structure

Use this structure from the beginning.

```txt
eb-government-monitoring-web/
├── public/
│   ├── logo.svg
│   ├── favicon.ico
│   └── assets/
│
├── src/
│   ├── app/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── router.tsx
│   │   └── providers.tsx
│   │
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── illustrations/
│   │
│   ├── components/
│   │   ├── ui/
│   │   ├── layout/
│   │   ├── forms/
│   │   ├── tables/
│   │   ├── charts/
│   │   ├── modals/
│   │   └── feedback/
│   │
│   ├── config/
│   │   ├── env.ts
│   │   ├── routes.ts
│   │   ├── permissions.ts
│   │   └── constants.ts
│   │
│   ├── features/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── projects/
│   │   ├── contractors/
│   │   ├── evidence/
│   │   ├── monitoring/
│   │   ├── approvals/
│   │   ├── funds/
│   │   ├── audits/
│   │   ├── reports/
│   │   ├── notifications/
│   │   ├── users/
│   │   └── settings/
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useDebounce.ts
│   │   ├── usePagination.ts
│   │   └── usePermissions.ts
│   │
│   ├── lib/
│   │   ├── api.ts
│   │   ├── http.ts
│   │   ├── storage.ts
│   │   ├── logger.ts
│   │   ├── formatters.ts
│   │   └── validators.ts
│   │
│   ├── services/
│   │   ├── auth.service.ts
│   │   ├── projects.service.ts
│   │   ├── contractors.service.ts
│   │   ├── evidence.service.ts
│   │   ├── approvals.service.ts
│   │   ├── funds.service.ts
│   │   ├── audits.service.ts
│   │   └── reports.service.ts
│   │
│   ├── store/
│   │   ├── auth.store.ts
│   │   ├── ui.store.ts
│   │   └── index.ts
│   │
│   ├── styles/
│   │   ├── index.css
│   │   └── tailwind.css
│   │
│   ├── types/
│   │   ├── auth.types.ts
│   │   ├── user.types.ts
│   │   ├── project.types.ts
│   │   ├── contractor.types.ts
│   │   ├── evidence.types.ts
│   │   ├── approval.types.ts
│   │   ├── funds.types.ts
│   │   └── audit.types.ts
│   │
│   └── utils/
│       ├── date.ts
│       ├── currency.ts
│       ├── permissions.ts
│       ├── status.ts
│       └── file.ts
│
├── .env.example
├── .gitignore
├── eslint.config.js
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── tsconfig.json
├── vite.config.ts
└── README.md
```

---

# Phase 1: Project Initialization and Base Setup

## Objectives

- Create the React web app using Vite and TypeScript.
- Install and configure Tailwind CSS.
- Establish the base project folder structure.
- Configure linting, formatting, environment variables and Git hygiene.
- Prepare the app for modular feature-based development.

## Directories to Create

```txt
eb-government-monitoring-web/
├── public/
├── src/
│   ├── app/
│   ├── assets/
│   ├── components/
│   ├── config/
│   ├── features/
│   ├── hooks/
│   ├── lib/
│   ├── services/
│   ├── store/
│   ├── styles/
│   ├── types/
│   └── utils/
```

## Files to Create or Populate

```txt
package.json
vite.config.ts
tsconfig.json
index.html
.env.example
.gitignore
README.md
eslint.config.js
postcss.config.js
tailwind.config.js
src/app/main.tsx
src/app/App.tsx
src/app/router.tsx
src/app/providers.tsx
src/styles/index.css
src/styles/tailwind.css
src/config/env.ts
src/config/constants.ts
```

## Expected Output

- The app starts successfully in development mode.
- Tailwind classes work correctly.
- Routing foundation is ready.
- Environment configuration is separated from source code.

---

# Phase 2: Design System and UI Foundation

## Objectives

- Create a consistent government-style visual system.
- Define colors, spacing, cards, buttons, forms and dashboard layout standards.
- Use dark navy, green and orange as the primary design direction.
- Build reusable UI components before building full screens.

## Directories to Create

```txt
src/components/ui/
src/components/layout/
src/components/forms/
src/components/tables/
src/components/charts/
src/components/modals/
src/components/feedback/
src/assets/icons/
src/assets/images/
src/assets/illustrations/
```

## Files to Create or Populate

```txt
src/components/ui/Button.tsx
src/components/ui/Card.tsx
src/components/ui/Badge.tsx
src/components/ui/Input.tsx
src/components/ui/Select.tsx
src/components/ui/Textarea.tsx
src/components/ui/Avatar.tsx
src/components/ui/ProgressBar.tsx
src/components/ui/StatusPill.tsx
src/components/ui/Dropdown.tsx
src/components/ui/Tabs.tsx
src/components/ui/Breadcrumb.tsx
src/components/ui/Pagination.tsx
src/components/ui/EmptyState.tsx
src/components/ui/LoadingSpinner.tsx
src/components/ui/ConfirmDialog.tsx

src/components/layout/AppLayout.tsx
src/components/layout/AuthLayout.tsx
src/components/layout/Sidebar.tsx
src/components/layout/Topbar.tsx
src/components/layout/PageHeader.tsx
src/components/layout/PageContainer.tsx

src/components/forms/FormField.tsx
src/components/forms/FileUpload.tsx
src/components/forms/SearchInput.tsx
src/components/forms/DateRangePicker.tsx

src/components/tables/DataTable.tsx
src/components/tables/TableActions.tsx
src/components/tables/TableFilters.tsx

src/components/feedback/Toast.tsx
src/components/feedback/AlertBox.tsx
src/components/feedback/ErrorMessage.tsx

src/config/theme.ts
src/config/statusColors.ts
```

## Expected Output

- All screens can use a shared design system.
- Dashboard cards, buttons, forms and tables have one consistent style.
- The UI does not become duplicated or inconsistent across modules.

---

# Phase 3: Routing, Layouts and Role-Based Navigation

## Objectives

- Define all major web app routes.
- Create protected routes for authenticated users.
- Create role-based navigation menus.
- Prepare different dashboards for different roles.
- Ensure unauthorized users cannot access restricted pages.

## Directories to Create

```txt
src/app/
src/config/
src/hooks/
src/components/layout/
```

## Files to Create or Populate

```txt
src/app/router.tsx
src/app/providers.tsx
src/config/routes.ts
src/config/permissions.ts
src/hooks/useAuth.ts
src/hooks/usePermissions.ts
src/components/layout/ProtectedRoute.tsx
src/components/layout/RoleGuard.tsx
src/components/layout/AppLayout.tsx
src/components/layout/Sidebar.tsx
src/components/layout/Topbar.tsx
```

## Routes to Define

```txt
/login
/forgot-password
/dashboard
/projects
/projects/new
/projects/:projectId
/projects/:projectId/edit
/contractors
/contractors/:contractorId
/evidence
/evidence/:evidenceId
/monitoring/review-queue
/monitoring/field-inspections
/approvals
/approvals/:approvalId
/funds
/audits
/reports
/notifications
/users
/settings
/profile
```

## Expected Output

- The application has a stable navigation skeleton.
- Sidebar and topbar display correctly.
- Routes are protected based on user login state and role.

---

# Phase 4: API Client, Services and Data Types

## Objectives

- Create a clean API communication layer.
- Centralize HTTP requests, tokens and error handling.
- Define TypeScript types for all core entities.
- Keep API calls out of UI components.

## Directories to Create

```txt
src/lib/
src/services/
src/types/
src/utils/
```

## Files to Create or Populate

```txt
src/lib/http.ts
src/lib/api.ts
src/lib/storage.ts
src/lib/logger.ts
src/lib/validators.ts
src/utils/date.ts
src/utils/currency.ts
src/utils/status.ts
src/utils/file.ts

src/types/auth.types.ts
src/types/user.types.ts
src/types/project.types.ts
src/types/contractor.types.ts
src/types/evidence.types.ts
src/types/monitoring.types.ts
src/types/approval.types.ts
src/types/funds.types.ts
src/types/audit.types.ts
src/types/report.types.ts
src/types/notification.types.ts

src/services/auth.service.ts
src/services/projects.service.ts
src/services/contractors.service.ts
src/services/evidence.service.ts
src/services/monitoring.service.ts
src/services/approvals.service.ts
src/services/funds.service.ts
src/services/audits.service.ts
src/services/reports.service.ts
src/services/notifications.service.ts
src/services/users.service.ts
src/services/settings.service.ts
```

## Expected Output

- Frontend has one standard way of calling backend APIs.
- UI components remain clean and focused on presentation.
- Types are ready for safer development.

---

# Phase 5: Authentication Module

## Objectives

- Implement login and forgot password screens.
- Add role-based login handling.
- Store authentication state safely.
- Redirect users to the correct dashboard.
- Prepare for future MFA support.

## Directories to Create

```txt
src/features/auth/
├── components/
├── pages/
├── hooks/
└── schemas/
```

## Files to Create or Populate

```txt
src/features/auth/pages/LoginPage.tsx
src/features/auth/pages/ForgotPasswordPage.tsx
src/features/auth/components/LoginForm.tsx
src/features/auth/components/ForgotPasswordForm.tsx
src/features/auth/components/RoleSelect.tsx
src/features/auth/hooks/useLogin.ts
src/features/auth/hooks/useLogout.ts
src/features/auth/schemas/auth.schema.ts
src/services/auth.service.ts
src/store/auth.store.ts
src/types/auth.types.ts
```

## Expected Output

- Users can log in.
- Authenticated users are redirected to their dashboard.
- Invalid login attempts are handled with safe error messages.
- Logout works correctly.

---

# Phase 6: Dashboard Module

## Objectives

- Build the main government admin dashboard.
- Display project totals, active monitoring, pending reviews and delayed projects.
- Show funds utilization and project status charts.
- Show recent activities and high-risk flags.
- Prepare role-specific dashboard variations.

## Directories to Create

```txt
src/features/dashboard/
├── components/
├── pages/
├── hooks/
└── widgets/
```

## Files to Create or Populate

```txt
src/features/dashboard/pages/AdminDashboardPage.tsx
src/features/dashboard/pages/ContractorDashboardPage.tsx
src/features/dashboard/pages/MonitoringDashboardPage.tsx
src/features/dashboard/pages/ApprovalDashboardPage.tsx
src/features/dashboard/pages/AuditorDashboardPage.tsx

src/features/dashboard/components/DashboardKpiGrid.tsx
src/features/dashboard/components/RecentActivities.tsx
src/features/dashboard/components/RiskFlagSummary.tsx
src/features/dashboard/components/FundsUtilizationCard.tsx
src/features/dashboard/components/ProjectStatusOverview.tsx

src/features/dashboard/widgets/KpiCard.tsx
src/features/dashboard/widgets/StatusDonutChart.tsx
src/features/dashboard/widgets/FundsProgressChart.tsx
src/features/dashboard/hooks/useDashboardStats.ts
```

## Expected Output

- Admin dashboard matches the MVP design direction.
- Different roles can have different dashboard cards.
- Dashboard is connected to mock data or live API data.

---

# Phase 7: Project Management Module

## Objectives

- Allow government admins to create and update projects.
- Display project list with search, filtering and sorting.
- Display full project details including milestones, contractor, district, funds and evidence.
- Enforce project status visibility.

## Directories to Create

```txt
src/features/projects/
├── components/
├── pages/
├── hooks/
├── schemas/
└── utils/
```

## Files to Create or Populate

```txt
src/features/projects/pages/ProjectsListPage.tsx
src/features/projects/pages/CreateProjectPage.tsx
src/features/projects/pages/EditProjectPage.tsx
src/features/projects/pages/ProjectDetailsPage.tsx

src/features/projects/components/ProjectForm.tsx
src/features/projects/components/ProjectFilters.tsx
src/features/projects/components/ProjectTable.tsx
src/features/projects/components/ProjectSummaryCards.tsx
src/features/projects/components/ProjectMilestones.tsx
src/features/projects/components/ProjectDocuments.tsx
src/features/projects/components/ProjectTimeline.tsx
src/features/projects/components/ProjectStatusBadge.tsx

src/features/projects/hooks/useProjects.ts
src/features/projects/hooks/useProjectDetails.ts
src/features/projects/hooks/useCreateProject.ts
src/features/projects/hooks/useUpdateProject.ts

src/features/projects/schemas/project.schema.ts
src/features/projects/utils/projectStatus.ts
src/services/projects.service.ts
src/types/project.types.ts
```

## Expected Output

- Projects can be listed, opened, created and edited.
- Project data is organized for later approval, evidence and audit workflows.

---

# Phase 8: Contractor Management Module

## Objectives

- Register and manage contractors.
- View contractor profiles, assigned projects and compliance status.
- Allow admins to suspend, activate or flag contractors.
- Show contractor performance history.

## Directories to Create

```txt
src/features/contractors/
├── components/
├── pages/
├── hooks/
└── schemas/
```

## Files to Create or Populate

```txt
src/features/contractors/pages/ContractorsListPage.tsx
src/features/contractors/pages/ContractorDetailsPage.tsx
src/features/contractors/pages/CreateContractorPage.tsx
src/features/contractors/pages/EditContractorPage.tsx

src/features/contractors/components/ContractorForm.tsx
src/features/contractors/components/ContractorTable.tsx
src/features/contractors/components/ContractorStatusBadge.tsx
src/features/contractors/components/ContractorProjects.tsx
src/features/contractors/components/ContractorPerformance.tsx
src/features/contractors/components/ContractorDocuments.tsx

src/features/contractors/hooks/useContractors.ts
src/features/contractors/hooks/useContractorDetails.ts
src/features/contractors/hooks/useCreateContractor.ts
src/features/contractors/hooks/useUpdateContractor.ts

src/features/contractors/schemas/contractor.schema.ts
src/services/contractors.service.ts
src/types/contractor.types.ts
```

## Expected Output

- Contractors can be managed as official entities.
- Contractor performance and compliance status become visible.

---

# Phase 9: Evidence and Receipt Management Module

## Objectives

- Allow contractors to upload receipts, invoices, photos and documents.
- Allow M&E officers to review submitted evidence.
- Track evidence status as pending, approved, rejected or clarification requested.
- Enforce file validation and clear evidence ownership.

## Directories to Create

```txt
src/features/evidence/
├── components/
├── pages/
├── hooks/
├── schemas/
└── utils/
```

## Files to Create or Populate

```txt
src/features/evidence/pages/EvidenceListPage.tsx
src/features/evidence/pages/EvidenceUploadPage.tsx
src/features/evidence/pages/EvidenceDetailsPage.tsx
src/features/evidence/pages/ReceiptVerificationPage.tsx

src/features/evidence/components/EvidenceUploadForm.tsx
src/features/evidence/components/EvidenceTable.tsx
src/features/evidence/components/EvidencePreview.tsx
src/features/evidence/components/ReceiptCard.tsx
src/features/evidence/components/VerificationDecisionForm.tsx
src/features/evidence/components/EvidenceStatusBadge.tsx
src/features/evidence/components/FileDropzone.tsx

src/features/evidence/hooks/useEvidence.ts
src/features/evidence/hooks/useUploadEvidence.ts
src/features/evidence/hooks/useVerifyEvidence.ts
src/features/evidence/hooks/useEvidenceDetails.ts

src/features/evidence/schemas/evidence.schema.ts
src/features/evidence/utils/fileValidation.ts
src/services/evidence.service.ts
src/types/evidence.types.ts
```

## Expected Output

- Evidence can be uploaded, previewed and reviewed.
- Review decisions are clearly tracked.
- Invalid files are rejected before upload.

---

# Phase 10: Monitoring and Evaluation Module

## Objectives

- Build M&E review queue.
- Allow officers to review contractor submissions.
- Capture field inspection reports.
- Flag delayed, risky or poor-quality projects.
- Submit recommendations to approval authorities.

## Directories to Create

```txt
src/features/monitoring/
├── components/
├── pages/
├── hooks/
└── schemas/
```

## Files to Create or Populate

```txt
src/features/monitoring/pages/ReviewQueuePage.tsx
src/features/monitoring/pages/MonitoringReviewPage.tsx
src/features/monitoring/pages/FieldInspectionPage.tsx
src/features/monitoring/pages/InspectionDetailsPage.tsx

src/features/monitoring/components/ReviewQueueTable.tsx
src/features/monitoring/components/MonitoringDecisionPanel.tsx
src/features/monitoring/components/InspectionForm.tsx
src/features/monitoring/components/InspectionChecklist.tsx
src/features/monitoring/components/RiskFlagForm.tsx
src/features/monitoring/components/RecommendationBox.tsx

src/features/monitoring/hooks/useReviewQueue.ts
src/features/monitoring/hooks/useSubmitReview.ts
src/features/monitoring/hooks/useFieldInspection.ts

src/features/monitoring/schemas/monitoring.schema.ts
src/services/monitoring.service.ts
src/types/monitoring.types.ts
```

## Expected Output

- M&E officers can review submissions.
- Field inspection records can be created.
- Risk flags and recommendations are visible to approvers.

---

# Phase 11: Approval Workflow Module

## Objectives

- Allow approval authorities to view pending approvals.
- Review evidence, M&E recommendations and project status before approving.
- Approve or reject milestones and fund release requests.
- Require comments for rejection.
- Keep a full approval history.

## Directories to Create

```txt
src/features/approvals/
├── components/
├── pages/
├── hooks/
└── schemas/
```

## Files to Create or Populate

```txt
src/features/approvals/pages/ApprovalsDashboardPage.tsx
src/features/approvals/pages/PendingApprovalsPage.tsx
src/features/approvals/pages/ApprovalDetailsPage.tsx
src/features/approvals/pages/ApprovalHistoryPage.tsx

src/features/approvals/components/PendingApprovalsTable.tsx
src/features/approvals/components/ApprovalDecisionPanel.tsx
src/features/approvals/components/ApprovalSummaryCard.tsx
src/features/approvals/components/ApprovalTimeline.tsx
src/features/approvals/components/RejectionReasonForm.tsx

src/features/approvals/hooks/useApprovals.ts
src/features/approvals/hooks/useApprovalDetails.ts
src/features/approvals/hooks/useSubmitApprovalDecision.ts

src/features/approvals/schemas/approval.schema.ts
src/services/approvals.service.ts
src/types/approval.types.ts
```

## Expected Output

- Approval requests can be reviewed and decided.
- Approval history is visible and traceable.
- Approval decisions are protected by role and workflow rules.

---

# Phase 12: Funds and Payment Tracking Module

## Objectives

- Track project budgets, allocated funds, released funds and balances.
- Link fund releases to approved milestones.
- Display payment history.
- Prevent UI actions that attempt to release funds without approval.

## Directories to Create

```txt
src/features/funds/
├── components/
├── pages/
├── hooks/
└── schemas/
```

## Files to Create or Populate

```txt
src/features/funds/pages/FundsOverviewPage.tsx
src/features/funds/pages/FundReleasePage.tsx
src/features/funds/pages/PaymentTrackingPage.tsx
src/features/funds/pages/FundReleaseDetailsPage.tsx

src/features/funds/components/FundsSummaryCards.tsx
src/features/funds/components/FundsUtilizationChart.tsx
src/features/funds/components/FundReleaseTable.tsx
src/features/funds/components/FundReleaseForm.tsx
src/features/funds/components/PaymentStatusBadge.tsx
src/features/funds/components/BudgetVarianceCard.tsx

src/features/funds/hooks/useFundsOverview.ts
src/features/funds/hooks/useFundReleases.ts
src/features/funds/hooks/useCreateFundRelease.ts

src/features/funds/schemas/funds.schema.ts
src/services/funds.service.ts
src/types/funds.types.ts
```

## Expected Output

- Funds are visible per project and milestone.
- Fund releases are traceable.
- Payment status is clear to authorized users.

---

# Phase 13: Audit and Compliance Module

## Objectives

- Allow auditors to review project compliance.
- Display audit assignments.
- Show evidence, payments, approvals and activity logs for audit review.
- Allow creation of audit findings with severity.
- Generate compliance status.

## Directories to Create

```txt
src/features/audits/
├── components/
├── pages/
├── hooks/
└── schemas/
```

## Files to Create or Populate

```txt
src/features/audits/pages/AuditorDashboardPage.tsx
src/features/audits/pages/AuditAssignmentsPage.tsx
src/features/audits/pages/AuditReviewPage.tsx
src/features/audits/pages/AuditFindingsPage.tsx
src/features/audits/pages/ComplianceDetailsPage.tsx

src/features/audits/components/AuditAssignmentsTable.tsx
src/features/audits/components/AuditFindingForm.tsx
src/features/audits/components/ComplianceScoreCard.tsx
src/features/audits/components/RiskFlagSummary.tsx
src/features/audits/components/AuditTrailViewer.tsx
src/features/audits/components/FindingSeverityBadge.tsx

src/features/audits/hooks/useAuditAssignments.ts
src/features/audits/hooks/useAuditReview.ts
src/features/audits/hooks/useCreateFinding.ts

src/features/audits/schemas/audit.schema.ts
src/services/audits.service.ts
src/types/audit.types.ts
```

## Expected Output

- Auditors can review projects and create findings.
- Compliance status becomes visible to authorized users.
- Audit trail is accessible but not editable.

---

# Phase 14: Reports and Analytics Module

## Objectives

- Generate project, funds, contractor, district, ministry and audit reports.
- Add date range, district, status and ministry filters.
- Export reports where backend support exists.
- Display charts for project status, funds utilization and risk trends.

## Directories to Create

```txt
src/features/reports/
├── components/
├── pages/
├── hooks/
└── utils/
```

## Files to Create or Populate

```txt
src/features/reports/pages/ReportsPage.tsx
src/features/reports/pages/AnalyticsPage.tsx
src/features/reports/pages/ReportDetailsPage.tsx

src/features/reports/components/ReportFilters.tsx
src/features/reports/components/ReportCards.tsx
src/features/reports/components/ReportExportButtons.tsx
src/features/reports/components/ProjectStatusChart.tsx
src/features/reports/components/FundsUtilizationChart.tsx
src/features/reports/components/DistrictPerformanceChart.tsx
src/features/reports/components/RiskTrendChart.tsx

src/features/reports/hooks/useReports.ts
src/features/reports/hooks/useAnalytics.ts
src/features/reports/hooks/useExportReport.ts

src/features/reports/utils/reportFilters.ts
src/services/reports.service.ts
src/types/report.types.ts
```

## Expected Output

- Authorized users can view reports and analytics.
- Reports can be filtered.
- Export buttons are available where backend export endpoints exist.

---

# Phase 15: Notifications Module

## Objectives

- Show user notifications.
- Display unread notification count.
- Open the related project, evidence, approval or audit item from a notification.
- Mark notifications as read.

## Directories to Create

```txt
src/features/notifications/
├── components/
├── pages/
└── hooks/
```

## Files to Create or Populate

```txt
src/features/notifications/pages/NotificationsPage.tsx
src/features/notifications/components/NotificationList.tsx
src/features/notifications/components/NotificationItem.tsx
src/features/notifications/components/NotificationBadge.tsx
src/features/notifications/components/NotificationFilters.tsx
src/features/notifications/hooks/useNotifications.ts
src/features/notifications/hooks/useMarkNotificationRead.ts
src/services/notifications.service.ts
src/types/notification.types.ts
```

## Expected Output

- Users see actionable notifications.
- Important system events are easy to access.
- Notification status can be updated.

---

# Phase 16: User Management and Settings Module

## Objectives

- Allow super admins to create and manage users.
- Assign roles and permissions.
- Configure districts, ministries, project categories and system reference data.
- Prepare settings for approval levels and risk rules.

## Directories to Create

```txt
src/features/users/
├── components/
├── pages/
├── hooks/
└── schemas/

src/features/settings/
├── components/
├── pages/
├── hooks/
└── schemas/
```

## Files to Create or Populate

```txt
src/features/users/pages/UsersListPage.tsx
src/features/users/pages/CreateUserPage.tsx
src/features/users/pages/EditUserPage.tsx
src/features/users/pages/UserDetailsPage.tsx

src/features/users/components/UserForm.tsx
src/features/users/components/UserTable.tsx
src/features/users/components/UserRoleBadge.tsx
src/features/users/components/UserStatusBadge.tsx
src/features/users/components/UserPermissionsPanel.tsx

src/features/users/hooks/useUsers.ts
src/features/users/hooks/useCreateUser.ts
src/features/users/hooks/useUpdateUser.ts
src/features/users/schemas/user.schema.ts

src/features/settings/pages/SettingsPage.tsx
src/features/settings/pages/MinistriesSettingsPage.tsx
src/features/settings/pages/DistrictsSettingsPage.tsx
src/features/settings/pages/ProjectCategoriesSettingsPage.tsx
src/features/settings/pages/ApprovalLevelsSettingsPage.tsx
src/features/settings/pages/RiskRulesSettingsPage.tsx

src/features/settings/components/SettingsNav.tsx
src/features/settings/components/ReferenceDataTable.tsx
src/features/settings/components/ReferenceDataForm.tsx
src/features/settings/components/RiskRuleForm.tsx

src/features/settings/hooks/useSettings.ts
src/features/settings/hooks/useReferenceData.ts
src/features/settings/schemas/settings.schema.ts

src/services/users.service.ts
src/services/settings.service.ts
src/types/user.types.ts
src/types/settings.types.ts
```

## Expected Output

- Admin users can manage accounts and system reference data.
- Role and permission management is available.
- The system becomes configurable instead of hardcoded.

---

# Phase 17: Defensive Programming and Frontend Security Hardening

## Objectives

- Validate forms before submission.
- Never trust frontend role checks only; backend must also enforce authorization.
- Handle API errors safely.
- Prevent accidental destructive actions.
- Avoid exposing sensitive data in logs, local storage or UI.

## Directories to Create

```txt
src/lib/
src/utils/
src/components/feedback/
src/components/modals/
src/config/
```

## Files to Create or Populate

```txt
src/lib/http.ts
src/lib/logger.ts
src/lib/storage.ts
src/lib/validators.ts
src/utils/permissions.ts
src/utils/file.ts
src/config/permissions.ts
src/components/modals/ConfirmActionModal.tsx
src/components/feedback/ErrorBoundary.tsx
src/components/feedback/ApiErrorView.tsx
```

## Specific Controls to Implement

```txt
- Token expiry handling
- Automatic logout on unauthorized API response
- Confirmation dialog for approvals, rejections, deletions and fund release actions
- File type and file size validation before upload
- Safe error messages without exposing stack traces
- Form validation for all create/edit workflows
- Role-based UI visibility
- Backend-enforced permissions for every sensitive action
```

## Expected Output

- The frontend fails safely.
- Users receive clear error messages.
- Sensitive actions require confirmation.
- Invalid submissions are blocked early.

---

# Phase 18: Testing and Quality Assurance

## Objectives

- Add unit tests for utilities and components.
- Add integration tests for key workflows.
- Add role-based access tests.
- Test forms, tables, filters and API error states.
- Prepare the MVP for user acceptance testing.

## Directories to Create

```txt
src/__tests__/
src/test/
src/test/mocks/
src/test/fixtures/
src/test/utils/
```

## Files to Create or Populate

```txt
src/test/setup.ts
src/test/test-utils.tsx
src/test/mocks/server.ts
src/test/mocks/handlers.ts
src/test/fixtures/projects.fixture.ts
src/test/fixtures/users.fixture.ts
src/test/fixtures/evidence.fixture.ts

src/__tests__/auth/LoginPage.test.tsx
src/__tests__/dashboard/AdminDashboardPage.test.tsx
src/__tests__/projects/ProjectForm.test.tsx
src/__tests__/projects/ProjectsListPage.test.tsx
src/__tests__/evidence/EvidenceUploadForm.test.tsx
src/__tests__/approvals/ApprovalDecisionPanel.test.tsx
src/__tests__/permissions/RoleGuard.test.tsx
```

## Test Scenarios

```txt
- User cannot access dashboard when logged out
- Contractor cannot access user management
- Admin can open project creation form
- Evidence upload rejects unsupported file types
- Approval rejection requires a comment
- Fund release button is disabled without milestone approval
- API failure shows safe error message
```

## Expected Output

- Core workflows are tested.
- Permission errors are caught early.
- MVP is stable enough for stakeholder review.

---

# Phase 19: Mock Data, API Integration and Environment Switching

## Objectives

- Support mock data during early frontend development.
- Switch cleanly between mock API and live backend API.
- Integrate backend endpoints module by module.
- Avoid blocking frontend progress while backend is under development.

## Directories to Create

```txt
src/mocks/
src/mocks/data/
src/mocks/handlers/
src/config/
```

## Files to Create or Populate

```txt
src/mocks/browser.ts
src/mocks/server.ts
src/mocks/data/projects.mock.ts
src/mocks/data/users.mock.ts
src/mocks/data/contractors.mock.ts
src/mocks/data/evidence.mock.ts
src/mocks/data/approvals.mock.ts
src/mocks/data/funds.mock.ts
src/mocks/data/audits.mock.ts

src/mocks/handlers/auth.handlers.ts
src/mocks/handlers/projects.handlers.ts
src/mocks/handlers/contractors.handlers.ts
src/mocks/handlers/evidence.handlers.ts
src/mocks/handlers/approvals.handlers.ts
src/mocks/handlers/funds.handlers.ts
src/mocks/handlers/audits.handlers.ts

src/config/env.ts
.env.example
```

## Environment Variables

```txt
VITE_API_BASE_URL=http://localhost:4000/api
VITE_USE_MOCK_API=true
VITE_APP_NAME=EB Government Monitoring System
VITE_APP_ENV=development
```

## Expected Output

- Frontend can be developed before backend completion.
- Switching to live API does not require rewriting components.
- Mock data follows the same structure expected from the backend.

---

# Phase 20: Performance, Accessibility and UX Polish

## Objectives

- Improve loading states, empty states and error states.
- Ensure dashboards and tables remain usable with large data.
- Improve keyboard accessibility and focus states.
- Ensure responsive behavior for tablets and smaller laptop screens.
- Prepare the app for low-bandwidth environments.

## Directories to Update

```txt
src/components/ui/
src/components/tables/
src/components/feedback/
src/features/*/
src/styles/
```

## Files to Create or Populate

```txt
src/components/feedback/Skeleton.tsx
src/components/feedback/PageLoader.tsx
src/components/feedback/RetryState.tsx
src/components/ui/Tooltip.tsx
src/components/ui/AccessibleIconButton.tsx
src/hooks/useDebounce.ts
src/hooks/usePagination.ts
src/hooks/useTableFilters.ts
src/styles/index.css
```

## Expected Output

- Pages feel polished and responsive.
- Slow API responses are handled gracefully.
- Tables support pagination and filtering.
- The system is usable by keyboard and screen reader users as much as possible.

---

# Phase 21: Build, Deployment Preparation and Documentation

## Objectives

- Prepare the React app for staging deployment.
- Add build scripts and deployment documentation.
- Verify environment variables and production build behavior.
- Document how developers should run, test and build the project.

## Directories to Create

```txt
docs/
docs/development/
docs/deployment/
docs/testing/
```

## Files to Create or Populate

```txt
README.md
docs/development/project-setup.md
docs/development/folder-structure.md
docs/development/coding-standards.md
docs/deployment/staging-deployment.md
docs/deployment/production-readiness.md
docs/testing/testing-guide.md
.env.example
package.json
vite.config.ts
```

## Build Scripts to Include

```txt
npm run dev
npm run build
npm run preview
npm run lint
npm run test
npm run test:coverage
```

## Expected Output

- The app can be built for staging.
- Developers know how to set up and contribute.
- Deployment requirements are documented.

---

# Phase 22: MVP User Acceptance Testing and Release Readiness

## Objectives

- Validate core workflows with real stakeholders.
- Confirm role dashboards and permissions.
- Confirm project, evidence, approval and reporting flows.
- Capture change requests for post-MVP.
- Prepare final MVP release checklist.

## Directories to Create

```txt
docs/uat/
docs/release/
```

## Files to Create or Populate

```txt
docs/uat/uat-plan.md
docs/uat/uat-test-cases.md
docs/uat/uat-feedback-log.md
docs/release/mvp-release-checklist.md
docs/release/known-limitations.md
docs/release/post-mvp-roadmap.md
```

## UAT Workflows to Test

```txt
- Login as Government Admin
- Create project
- Assign contractor and M&E officer
- Login as Contractor
- Submit progress update and evidence
- Login as M&E Officer
- Review evidence and submit recommendation
- Login as Approval Authority
- Approve milestone
- Track funds release status
- Login as Auditor
- Review project compliance
- Generate report
```

## Expected Output

- MVP is validated by stakeholders.
- Critical issues are fixed before release.
- Non-critical improvements are moved to post-MVP roadmap.

---

# Recommended MVP Build Order

Follow this order strictly for fastest delivery:

```txt
1. Project setup
2. Design system
3. Routing and layout
4. API client and types
5. Authentication
6. Admin dashboard
7. Project management
8. Contractor management
9. Evidence and receipt management
10. M&E review queue
11. Approval workflow
12. Funds tracking
13. Audit and compliance
14. Reports and analytics
15. Notifications
16. User management and settings
17. Testing and hardening
18. UAT and MVP release
```

---

# Recommended React Web MVP Stack

```txt
Frontend Framework: React.js
Build Tool: Vite
Language: TypeScript
Styling: Tailwind CSS
Routing: React Router
Forms: React Hook Form
Validation: Zod or Yup
API Calls: Axios or Fetch wrapper
Server State: TanStack Query
Client State: Zustand or Redux Toolkit
Charts: Recharts or Chart.js
Tables: TanStack Table or custom DataTable
Testing: Vitest + React Testing Library
Mock API: MSW
Icons: Lucide React or Heroicons
Date Handling: date-fns
```

---

# Final Development Rule

Do not build screens randomly.

Build the project in this sequence:

```txt
Foundation → Design System → Routing → API Layer → Auth → Core Modules → Reviews → Approvals → Reports → Testing → UAT
```

This keeps the MVP clean, modular and ready for production expansion.
