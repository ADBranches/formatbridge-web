# AML SMPC Next-Generation Furnishment Implementation Guide

## Purpose

This guide is the combined implementation plan for the next enterprise-grade furnishments to add to the existing AML SMPC application.

Core research framing:

> Bank A, Bank B, and Bank C are the SMPC-style participants.  
> They contribute private or pseudonymized information.  
> The SMPC runtime returns aggregate evidence.  
> The regulator does not receive raw bank inputs.

The new goal is to strengthen the application so that the UI, backend, data model, RBAC, and underlying AML logic demonstrate a realistic financial-institution workflow:

1. Only approved partner banks can participate.
2. Every user belongs to a specific partner bank, regulator authority, auditor body, or platform organization.
3. Bank-side users identify suspicious transactions through rule evaluation.
4. SMPC collaboration supports privacy-preserving cross-bank risk evidence.
5. The regulator verifies proof/audit evidence and can open anomaly cases.
6. Banks receive regulator case feedback without seeing other banks' raw private data.
7. Every role clearly exposes read/write/execute/approve/verify/manage permissions.

---

## Current Confirmed Baseline

The existing system already has:

- Public pages: `/`, `/about`, `/login`, `/register`
- JWT login/session
- Super-admin user approval
- Role-based access control
- Institution transaction workflow
- Transaction submitter and reviewer separation
- Screening and proof-generation workflow
- Regulator proof/audit/compliance dashboard
- Auditor read-only evidence access
- Three-bank SMPC frontend demo page
- Vite proxy wiring for regulator, encryption, HE, SMPC, and zk services
- Final repository audit and presentation rehearsal checks

Current important backend files:

```text
services/regulator-api/backend/src/audit.rs
services/regulator-api/backend/src/auth.rs
services/regulator-api/backend/src/db.rs
services/regulator-api/backend/src/main.rs
services/regulator-api/backend/src/proofs.rs
services/regulator-api/backend/src/routes.rs
services/regulator-api/backend/src/transactions.rs
```

Current important frontend areas:

```text
services/regulator-api/frontend/src/api/
services/regulator-api/frontend/src/auth/
services/regulator-api/frontend/src/pages/auth/
services/regulator-api/frontend/src/pages/institution/
services/regulator-api/frontend/src/pages/regulator/
services/regulator-api/frontend/src/pages/super-admin/
services/regulator-api/frontend/src/routes/AppRoutes.tsx
services/regulator-api/frontend/src/components/navigation/Sidebar.tsx
```

Current migrations:

```text
infra/postgres/migrations/001_create_transactions.sql
infra/postgres/migrations/002_create_audit_logs.sql
infra/postgres/migrations/003_create_proofs.sql
infra/postgres/migrations/004_create_regulator_views.sql
infra/postgres/migrations/005_retention_policy.sql
infra/postgres/migrations/006_create_auth_rbac_foundation.sql
infra/postgres/migrations/007_create_transaction_approval_workflow.sql
```

---

# Stage 0 — Safety Inspection and Branch Setup

## Objective

Create a safe implementation branch and inspect the current project before modifying the database, backend, frontend, and validation scripts.

## Commands

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git fetch origin --prune
git status -sb
git rev-list --left-right --count HEAD...origin/main

git checkout -b bank-rbac-suspicion-case-workflow
```

## Inspection Command

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

mkdir -p .inspection

{
  echo "=== Git state ==="
  git -C .. status -sb

  echo
  echo "=== Backend Rust files ==="
  find services/regulator-api/backend/src -maxdepth 2 -type f | sort

  echo
  echo "=== Frontend source files ==="
  find services/regulator-api/frontend/src -maxdepth 4 -type f | sort

  echo
  echo "=== Migrations ==="
  find infra/postgres/migrations -type f | sort

  echo
  echo "=== Auth / org / bank / permission / suspicious search ==="
  grep -RIn \
    "register\|login\|permissions\|requested_role\|organization\|bank\|suspicious\|risk_score\|screening_status\|approve\|reject" \
    services/regulator-api/backend/src \
    services/regulator-api/frontend/src \
    infra/postgres/migrations \
    | sed -n '1,360p'

  echo
  echo "=== Current DB schema ==="
  export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2-)"
  psql "$DATABASE_URL" -c '\d app_users' || true
  psql "$DATABASE_URL" -c '\d organizations' || true
  psql "$DATABASE_URL" -c '\d transactions' || true
  psql "$DATABASE_URL" -c '\d audit_logs' || true
  psql "$DATABASE_URL" -c '\d proofs' || true
} | tee .inspection/BANK_RBAC_CASE_WORKFLOW_INSPECTION.txt
```

## Exit Criteria

- Branch is created.
- Inspection file exists.
- No core file has been modified yet.

---

# Stage 1 — Partner Bank Identity Model

## Objective

Make the application explicitly partner-bank based. A user should request access under a known partner bank, regulator authority, auditor body, or platform organization.

## Backend Data Model Additions

Create:

```text
infra/postgres/migrations/008_partner_bank_identity_and_permissions.sql
```

Add or confirm these fields.

### `organizations`

```text
bank_code VARCHAR(32) UNIQUE
organization_type VARCHAR(32)
country VARCHAR(64)
license_number VARCHAR(64)
is_partner BOOLEAN DEFAULT false
status VARCHAR(32) DEFAULT 'active'
```

Allowed `organization_type` values:

```text
bank
regulator
auditor
platform
```

### `app_users`

```text
bank_employee_id VARCHAR(64)
department VARCHAR(64)
job_title VARCHAR(128)
identity_verified BOOLEAN DEFAULT false
approved_partner_scope BOOLEAN DEFAULT false
```

## Registration Fields

The registration form should require:

```text
full_name
email
password
partner_bank_code
bank_employee_id
department
job_title
requested_role
reason_for_access
```

## Backend Logic

Modify:

```text
services/regulator-api/backend/src/auth.rs
```

Registration should:

1. Require `partner_bank_code`.
2. Look up organization by `bank_code`.
3. Reject if the organization does not exist.
4. Reject if the organization is not an active partner.
5. Store `bank_employee_id`, `department`, and `job_title`.
6. Keep account status as `pending_approval`.
7. Create an approval request for the super admin.

## Frontend Logic

Modify:

```text
services/regulator-api/frontend/src/pages/auth/RegisterPage.tsx
services/regulator-api/frontend/src/api/authApi.ts
```

Registration UI should show:

```text
Full Name
Email
Password
Partner Bank Code
Bank Employee ID
Department
Job Title
Requested Role
Reason for Access
```

## Super Admin UI

Update:

```text
services/regulator-api/frontend/src/pages/super-admin/PendingUsersPage.tsx
services/regulator-api/frontend/src/pages/super-admin/UserManagementPage.tsx
services/regulator-api/frontend/src/pages/super-admin/OrganizationManagementPage.tsx
```

Display:

```text
organization_name
bank_code
organization_type
bank_employee_id
department
job_title
requested_role
approval_status
```

## Validation Commands

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2-)"

psql "$DATABASE_URL" -f infra/postgres/migrations/008_partner_bank_identity_and_permissions.sql

psql "$DATABASE_URL" -c "\d organizations"
psql "$DATABASE_URL" -c "\d app_users"
```

## Exit Criteria

- Users cannot register under a non-partner organization.
- Pending users show bank code and employee identity.
- Super admin can approve/reject with bank identity visible.

---

# Stage 2 — Permission Attributes and RBAC Matrix

## Objective

Display and enforce role permissions in a way that examiners can understand.

Permissions should be grouped by action type:

```text
read
write
execute
approve
verify
manage
```

## Backend Role Permission Model

Modify:

```text
services/regulator-api/backend/src/auth.rs
```

Recommended permission names:

```text
transactions:create
transactions:read
transactions:read_own
transactions:review
transactions:approve
transactions:reject
transactions:screen
transactions:flag_suspicious
proofs:generate
proofs:read
proofs:verify
audit:read
compliance:read
cases:create
cases:read
cases:update
cases:respond
users:approve
users:manage
organizations:manage
roles:read
```

## Permission Attribute Mapping

Add frontend helper:

```text
services/regulator-api/frontend/src/auth/permissionAttributes.ts
```

Mapping:

```text
:create        -> write
:read          -> read
:read_own      -> read
:review        -> read
:approve       -> approve
:reject        -> approve
:screen        -> execute
:generate      -> execute
:verify        -> verify
:manage        -> manage
:update        -> write
:respond       -> write
```

## Frontend UI

Update:

```text
services/regulator-api/frontend/src/pages/super-admin/RoleManagementPage.tsx
services/regulator-api/frontend/src/pages/super-admin/UserManagementPage.tsx
services/regulator-api/frontend/src/components/navigation/Sidebar.tsx
```

Display:

| Role | Permission | Attribute |
|---|---|---|
| transaction_submitter | transactions:create | write |
| transaction_reviewer | transactions:screen | execute |
| regulator | proofs:verify | verify |
| super_admin | users:manage | manage |

## Exit Criteria

- Super admin can see every role and its permission attributes.
- Frontend sidebar still respects role-specific access.
- Backend still rejects unauthorized API calls.

---

# Stage 3 — Bank-Side Suspicious Transaction Rules Engine

## Objective

Make suspicious transaction detection start from the bank side. The bank identifies or flags suspicious transactions before the regulator verifies the evidence.

## Data Model Additions

Create:

```text
infra/postgres/migrations/009_suspicion_rules_and_transaction_risk.sql
```

Add to `transactions`:

```text
risk_score INTEGER DEFAULT 0
risk_level VARCHAR(32) DEFAULT 'low'
suspicion_status VARCHAR(32) DEFAULT 'not_evaluated'
triggered_rules JSONB DEFAULT '[]'::jsonb
recommended_action VARCHAR(128)
review_notes TEXT
screened_by UUID NULL
screened_at TIMESTAMPTZ NULL
```

Create table:

```text
aml_rules
```

Suggested columns:

```text
id UUID PRIMARY KEY
rule_code VARCHAR(64) UNIQUE NOT NULL
rule_name VARCHAR(128) NOT NULL
description TEXT NOT NULL
rule_type VARCHAR(64) NOT NULL
risk_weight INTEGER NOT NULL
is_active BOOLEAN DEFAULT true
created_at TIMESTAMPTZ DEFAULT now()
```

Seed rules:

```text
AMOUNT_HIGH_VALUE
CROSS_BORDER_TRANSFER
MISSING_PAYMENT_TRANSPARENCY
HIGH_RISK_COUNTERPARTY
CDD_INCOMPLETE
SMPC_CROSS_BANK_OVERLAP
SANCTIONS_SCREEN_ATTENTION
```

## Backend Logic

Create or extend:

```text
services/regulator-api/backend/src/transactions.rs
```

Add route:

```text
POST /transactions/{tx_id}/evaluate-risk
```

The evaluator should:

1. Read transaction details.
2. Apply bank-side AML rules.
3. Calculate risk score.
4. Set risk level:
   - `low`: 0–39
   - `medium`: 40–69
   - `high`: 70+
5. Save triggered rules.
6. Mark `suspicion_status` as one of:
   - `not_suspicious`
   - `under_review`
   - `suspicious`
7. Write an audit log event.

## Example Rule Behavior

```text
amount >= 100000                -> AMOUNT_HIGH_VALUE +25
originator/beneficiary missing  -> MISSING_PAYMENT_TRANSPARENCY +30
cross-border currency mismatch  -> CROSS_BORDER_TRANSFER +15
SMPC overlap count > 0          -> SMPC_CROSS_BANK_OVERLAP +35
screening match                 -> SANCTIONS_SCREEN_ATTENTION +50
```

## Frontend Pages

Create:

```text
services/regulator-api/frontend/src/pages/institution/SuspiciousTransactionsPage.tsx
services/regulator-api/frontend/src/pages/institution/RiskEvaluationPage.tsx
```

Update:

```text
services/regulator-api/frontend/src/pages/institution/TransactionReviewPage.tsx
services/regulator-api/frontend/src/pages/institution/ScreeningResultsPage.tsx
services/regulator-api/frontend/src/api/transactionsApi.ts
services/regulator-api/frontend/src/routes/AppRoutes.tsx
services/regulator-api/frontend/src/components/navigation/Sidebar.tsx
```

## UI Should Show

```text
tx_id
amount
currency
risk_score
risk_level
suspicion_status
triggered_rules
recommended_action
reviewer
screened_at
```

## Exit Criteria

- Reviewer can click `Evaluate Risk`.
- Transaction receives risk score and triggered rules.
- Suspicious transactions appear in a dedicated bank-side queue.
- Regulator is not the first actor discovering suspicious activity.

---

# Stage 4 — Connect Bank-Side Risk to SMPC Collaboration

## Objective

Make SMPC collaboration evidence influence bank-side suspicious transaction classification.

## Backend Logic

When reviewer runs:

```text
POST /transactions/{tx_id}/run-screening
```

the workflow should:

1. Call the SMPC runtime.
2. Read SMPC response:
   - `aggregate_risk_score`
   - `possible_cross_bank_overlap_count`
   - `screening_status`
   - `raw_bank_inputs_disclosed`
3. Update transaction risk fields.
4. Add triggered rule:
   - `SMPC_CROSS_BANK_OVERLAP`
5. Save audit event.

## UI Logic

Update:

```text
services/regulator-api/frontend/src/pages/institution/ScreeningResultsPage.tsx
services/regulator-api/frontend/src/pages/institution/TransactionReviewPage.tsx
```

Show:

```text
SMPC aggregate score
SMPC overlap count
raw_inputs_disclosed = false
screening_status
linked risk rules
```

## Exit Criteria

- SMPC evidence affects transaction risk state.
- Bank-side UI explains why a transaction is suspicious.
- No raw private data from other banks is displayed.

---

# Stage 5 — Regulator Anomaly Case Workflow

## Objective

Let the regulator convert verified suspicious evidence into an anomaly case.

Correct flow:

```text
1. Bank flags suspicious activity.
2. SMPC produces privacy-preserving aggregate evidence.
3. Proofs and audit records are generated.
4. Regulator verifies evidence.
5. Regulator opens an anomaly case/report.
6. Involved banks receive feedback without seeing raw information from other banks.
```

## Data Model

Create:

```text
infra/postgres/migrations/010_regulator_anomaly_cases.sql
```

Create table:

```text
anomaly_cases
```

Columns:

```text
id UUID PRIMARY KEY
case_ref VARCHAR(64) UNIQUE NOT NULL
tx_id VARCHAR(64) NOT NULL
opened_by UUID NOT NULL
case_status VARCHAR(32) NOT NULL DEFAULT 'open'
risk_level VARCHAR(32) NOT NULL
summary TEXT NOT NULL
regulator_finding TEXT
required_bank_action TEXT
created_at TIMESTAMPTZ DEFAULT now()
updated_at TIMESTAMPTZ DEFAULT now()
```

Create table:

```text
anomaly_case_banks
```

Columns:

```text
id UUID PRIMARY KEY
case_id UUID NOT NULL REFERENCES anomaly_cases(id) ON DELETE CASCADE
organization_id UUID NOT NULL REFERENCES organizations(id)
notice_status VARCHAR(32) DEFAULT 'sent'
bank_response TEXT
responded_by UUID NULL
responded_at TIMESTAMPTZ NULL
created_at TIMESTAMPTZ DEFAULT now()
```

## Backend Routes

Add:

```text
GET  /regulator/anomaly-cases
POST /regulator/anomaly-cases
GET  /regulator/anomaly-cases/{case_id}
POST /regulator/anomaly-cases/{case_id}/close

GET  /institution/anomaly-notices
GET  /institution/anomaly-notices/{case_id}
POST /institution/anomaly-notices/{case_id}/respond
```

## RBAC

```text
regulator:
  cases:create
  cases:read
  cases:update

institution_admin:
  cases:read
  cases:respond

transaction_reviewer:
  cases:read
  cases:respond

auditor:
  cases:read
```

## Frontend Pages

Create:

```text
services/regulator-api/frontend/src/pages/regulator/AnomalyCasesPage.tsx
services/regulator-api/frontend/src/pages/regulator/AnomalyCaseDetailPage.tsx
services/regulator-api/frontend/src/pages/institution/BankAnomalyNoticesPage.tsx
services/regulator-api/frontend/src/pages/institution/BankAnomalyNoticeDetailPage.tsx
```

Create API client:

```text
services/regulator-api/frontend/src/api/anomalyCasesApi.ts
```

## Privacy Rule

Banks should not see:

```text
other banks' customer IDs
other banks' raw account IDs
other banks' raw transaction payloads
```

Banks may see:

```text
case ID
their own related transaction reference
risk level
regulator finding
required action
aggregate SMPC evidence summary
```

## Exit Criteria

- Regulator can open case from suspicious/proof evidence.
- Bank sees case notice.
- Bank can respond.
- Other banks' raw data is never exposed.

---

# Stage 6 — Partner-Bank Dashboard Furnishment

## Objective

Make the bank dashboards feel complete and scoped to the logged-in bank.

## Add/Enhance Pages

```text
/institution/dashboard
/institution/transactions/new
/institution/transactions
/institution/reviews
/institution/suspicious-transactions
/institution/screening-results
/institution/anomaly-notices
/institution/approved-transactions
```

## Institution Dashboard Cards

Show:

```text
submitted transactions
under review transactions
suspicious transactions
proof generated transactions
open anomaly notices
high-risk transactions
```

## Data Source

Use real backend endpoints. Avoid hard-coded dashboard-only values except for clearly labelled demo seed controls.

## Exit Criteria

- Bank user sees their own organization scope.
- Dashboard summarizes real data.
- Suspicious transactions and anomaly notices are visible.

---

# Stage 7 — Regulator Dashboard Furnishment

## Objective

Make the regulator dashboard show the full evidence governance story.

## Routes

```text
/regulator/dashboard
/regulator/proofs
/regulator/audit
/regulator/compliance-report
/regulator/three-bank-smpc-demo
/regulator/anomaly-cases
```

## Dashboard Cards

```text
verified proofs
pending proof reviews
high-risk cases
open anomaly cases
closed anomaly cases
FATF R.10 evidence
FATF R.11 evidence
FATF R.16 evidence
```

## Exit Criteria

- Regulator can inspect evidence.
- Regulator can verify proof.
- Regulator can open anomaly case.
- Regulator can view three-bank collaboration evidence.
- Regulator does not see raw bank inputs.

---

# Stage 8 — Seeder and Demo Data

## Objective

Seed partner banks, users, rules, transactions, and anomaly cases for presentation.

## Create Script

```text
scripts/dev/seed_bank_rbac_case_demo.py
```

Seed organizations:

```text
BANK_A_UG
BANK_B_KE
BANK_C_TZ
REGULATOR_AUTHORITY
AUDITOR_BODY
AML_PLATFORM
```

Seed users:

```text
super.admin@aml-smpc.local
bank.a.admin@example.com
bank.a.submitter@example.com
bank.a.reviewer@example.com
bank.b.reviewer@example.com
bank.c.reviewer@example.com
demo.regulator@example.com
demo.auditor@example.com
```

Seed AML rules:

```text
AMOUNT_HIGH_VALUE
CROSS_BORDER_TRANSFER
MISSING_PAYMENT_TRANSPARENCY
HIGH_RISK_COUNTERPARTY
CDD_INCOMPLETE
SMPC_CROSS_BANK_OVERLAP
SANCTIONS_SCREEN_ATTENTION
```

Seed demo transactions:

```text
TX-BANKA-LOW-001
TX-BANKA-SUSPICIOUS-001
TX-SMPC-OVERLAP-001
```

## Exit Criteria

- Demo can be reset quickly.
- Users are attached to correct partner organizations.
- Suspicious transaction queue has sample records.
- Regulator case workflow has sample records.

---

# Stage 9 — Validation Scripts

## Objective

Create validation scripts that prove the new enterprise flow works.

## Scripts

```text
scripts/ci/validate-bank-rbac-identity.sh
scripts/ci/validate-suspicious-transaction-rules.sh
scripts/ci/validate-regulator-anomaly-case-flow.sh
scripts/ci/validate-full-enterprise-demo.sh
```

## Required Checks

### Bank Identity

```text
non-partner bank registration fails
partner bank registration succeeds as pending_approval
super admin approval activates account
JWT contains organization_id, bank_code, role, permissions
```

### Suspicion Rules

```text
reviewer can evaluate risk
submitter cannot approve
reviewer can approve
risk_score is saved
triggered_rules are saved
suspicious queue returns record
```

### Regulator Case Flow

```text
regulator can open anomaly case
auditor can read case
auditor cannot update case
bank can see notice
bank can respond to notice
raw bank data is not exposed
```

### Full Demo

```text
login works
transaction submission works
risk evaluation works
screening works
proof generation works
regulator verification works
anomaly case workflow works
repo audit stays clean
```

---

# Stage 10 — Documentation Updates

## Objective

Keep the project report, runbooks, and presentation guides aligned with the new implementation.

## Update Existing Docs

```text
docs/demo/FINAL_PROJECT_PRESENTATION_RUNBOOK.md
docs/demo/APPLICATION_RUN_AND_RESEARCH_OBJECTIVES_GUIDE.md
docs/defense/FINAL_PRESENTATION_STORY.md
docs/defense/EXAMINER_DEFENSE_NOTES.md
docs/submission/FINAL_SUBMISSION_CHECKLIST.md
```

## Add New Docs

```text
docs/demo/BANK_RBAC_SUSPICION_CASE_WORKFLOW.md
docs/demo/PARTNER_BANK_IDENTITY_MODEL.md
docs/demo/SUSPICIOUS_TRANSACTION_RULE_ENGINE.md
docs/demo/REGULATOR_ANOMALY_CASE_FEEDBACK.md
```

## Report Text to Add

```text
Suspicious transaction identification begins at the financial-institution layer. Bank-side submitters and reviewers process transactions under their approved partner-bank identity, and reviewers execute risk evaluation using AML rules before SMPC collaboration and proof generation. The SMPC layer supports cross-bank collaborative risk evidence without disclosing raw private bank data. The regulator then verifies proof and audit evidence, and may open anomaly cases for affected partner banks.
```

---

# Stage 11 — Final UI Testing Flow

## Backend

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
source env/bin/activate
./scripts/demo/run-frontend-backend.sh
```

## Frontend

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system/services/regulator-api/frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

## Browser Testing Order

```text
1. Register user under partner bank code.
2. Login as super admin.
3. Approve pending user.
4. Login as transaction submitter.
5. Submit transaction.
6. Login as transaction reviewer.
7. Evaluate risk.
8. Approve transaction.
9. Run screening.
10. Generate proofs.
11. Login as regulator.
12. Verify proof.
13. Open anomaly case.
14. Login as bank admin/reviewer.
15. View anomaly notice.
16. Respond to regulator notice.
17. Login as auditor.
18. Confirm read-only evidence access.
```

---

# Stage 12 — Git and Final Audit

## Commit Commands

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git status -sb

git add aml-system/infra/postgres/migrations/008_partner_bank_identity_and_permissions.sql
git add aml-system/infra/postgres/migrations/009_suspicion_rules_and_transaction_risk.sql
git add aml-system/infra/postgres/migrations/010_regulator_anomaly_cases.sql
git add aml-system/services/regulator-api/backend/src
git add aml-system/services/regulator-api/frontend/src
git add aml-system/scripts/dev/seed_bank_rbac_case_demo.py
git add aml-system/scripts/ci/validate-bank-rbac-identity.sh
git add aml-system/scripts/ci/validate-suspicious-transaction-rules.sh
git add aml-system/scripts/ci/validate-regulator-anomaly-case-flow.sh
git add aml-system/scripts/ci/validate-full-enterprise-demo.sh
git add aml-system/docs/demo
git add aml-system/docs/defense
git add aml-system/docs/submission

git commit -m "Add partner bank RBAC suspicion and anomaly case workflow"

git push origin bank-rbac-suspicion-case-workflow
```

After review:

```bash
git checkout main
git pull origin main
git merge bank-rbac-suspicion-case-workflow
git push origin main
```

Final checks:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git fetch origin --prune
git rev-list --left-right --count HEAD...origin/main
git status -sb

./aml-system/scripts/ci/final-repository-audit.sh
./aml-system/scripts/demo/final-presentation-rehearsal-check.sh
```

Expected:

```text
0 0
## main...origin/main
FINAL-4 REPOSITORY AUDIT PASSED
FINAL-5 PRESENTATION REHEARSAL CHECK PASSED
```

---

# Final Target State

After completing this guide, the application should demonstrate:

```text
1. Partner-bank-only user onboarding.
2. Strong identity binding between user and bank.
3. Explicit RBAC permission attributes.
4. Bank-side suspicious transaction identification.
5. SMPC-supported cross-bank collaboration.
6. Regulator proof/audit verification.
7. Regulator anomaly case creation.
8. Bank-side anomaly notice response.
9. Auditor read-only evidence inspection.
10. No raw private bank data exposed across banks or to regulator.
```

This is the stronger enterprise-grade version of the AML SMPC prototype.
