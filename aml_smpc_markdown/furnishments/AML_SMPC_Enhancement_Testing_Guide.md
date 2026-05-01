# AML SMPC Enhancement Testing Guide — Terminal + UI Validation

## Purpose

This guide combines the terminal and UI validation steps for the AML SMPC enhancement branch.

Core demonstration:

- Bank A, Bank B, and Bank C are SMPC-style participants.
- Banks contribute private/pseudonymized data.
- SMPC returns aggregate evidence.
- The regulator does not receive raw bank inputs.
- Suspicious transaction identification starts from the bank side before regulator verification.

---

## Global Run Commands

### Backend terminal

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
source env/bin/activate
./scripts/demo/run-frontend-backend.sh
```

Expected backend services:

```text
encryption-service: http://127.0.0.1:8081
he-orchestrator:    http://127.0.0.1:8082
smpc-orchestrator:  http://127.0.0.1:8083
zk-prover:          http://127.0.0.1:8084
regulator-api:      http://127.0.0.1:8085
```

### Frontend terminal

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system/services/regulator-api/frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173
```

### Build checks

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
cargo build --manifest-path services/regulator-api/backend/Cargo.toml

cd services/regulator-api/frontend
npm run build
```

Expected:

```text
Finished dev profile
✓ built
```

---

# Stage 0 — Branch and Inspection

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git fetch origin --prune
git status -sb
git rev-list --left-right --count HEAD...origin/main

if git show-ref --verify --quiet refs/heads/bank-rbac-suspicion-case-workflow; then
  git checkout bank-rbac-suspicion-case-workflow
else
  git checkout -b bank-rbac-suspicion-case-workflow
fi

git status -sb
git branch --show-current
```

Expected:

```text
bank-rbac-suspicion-case-workflow
```

Inspection:

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
  echo "=== Current DB schema ==="
  export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2-)"
  psql "$DATABASE_URL" -c '\d app_users' || true
  psql "$DATABASE_URL" -c '\d organizations' || true
  psql "$DATABASE_URL" -c '\d transactions' || true
  psql "$DATABASE_URL" -c '\d audit_logs' || true
  psql "$DATABASE_URL" -c '\d proofs' || true
} | tee .inspection/BANK_RBAC_CASE_WORKFLOW_INSPECTION.txt
```

Expected:

```text
Inspection file exists.
No core file modified.
```

---

# Stage 1 — Partner Bank Identity Model

## Migration validation

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2-)"

psql "$DATABASE_URL" -v ON_ERROR_STOP=1   -f infra/postgres/migrations/008_partner_bank_identity_and_permissions.sql

psql "$DATABASE_URL" -c "\d organizations"
psql "$DATABASE_URL" -c "\d app_users"
```

Expected `organizations` fields:

```text
bank_code
organization_type
country
license_number
is_partner
status
```

Expected `app_users` fields:

```text
bank_employee_id
department
job_title
identity_verified
approved_partner_scope
```

## Invalid partner code test

```bash
BAD_EMAIL="bad.partner.$(date +%s)@example.com"

curl -i -sS -X POST "http://127.0.0.1:8085/auth/register"   -H "Content-Type: application/json"   -d "{
    \"full_name\": \"Bad Partner User\",
    \"email\": \"$BAD_EMAIL\",
    \"password\": \"StrongPass123\",
    \"partner_bank_code\": \"NOT_A_PARTNER\",
    \"bank_employee_id\": \"BAD-001\",
    \"department\": \"Compliance\",
    \"job_title\": \"AML Analyst\",
    \"requested_role\": \"transaction_submitter\",
    \"reason_for_access\": \"Testing rejection for invalid partner organization code.\"
  }"
```

Expected:

```text
HTTP/1.1 400 Bad Request
invalid_partner_bank_code
```

## Valid partner registration test

```bash
GOOD_EMAIL="bank.a.submitter.$(date +%s)@example.com"

curl -fsS -X POST "http://127.0.0.1:8085/auth/register"   -H "Content-Type: application/json"   -d "{
    \"full_name\": \"Bank A Submitter Demo\",
    \"email\": \"$GOOD_EMAIL\",
    \"password\": \"StrongPass123\",
    \"partner_bank_code\": \"BANK_A_UG\",
    \"bank_employee_id\": \"BANKA-EMP-$(date +%s)\",
    \"department\": \"Compliance\",
    \"job_title\": \"AML Transaction Submitter\",
    \"requested_role\": \"transaction_submitter\",
    \"reason_for_access\": \"I need access to submit synthetic AML transactions for partner-bank testing.\"
  }" | jq .
```

Expected:

```text
partner_bank_code = BANK_A_UG
account_status = pending_approval
```

## Incompatible organization/role test

```bash
ROLE_EMAIL="bad.role.$(date +%s)@example.com"

curl -i -sS -X POST "http://127.0.0.1:8085/auth/register"   -H "Content-Type: application/json"   -d "{
    \"full_name\": \"Bad Role User\",
    \"email\": \"$ROLE_EMAIL\",
    \"password\": \"StrongPass123\",
    \"partner_bank_code\": \"BANK_A_UG\",
    \"bank_employee_id\": \"BANKA-BADROLE-001\",
    \"department\": \"Compliance\",
    \"job_title\": \"AML Analyst\",
    \"requested_role\": \"regulator\",
    \"reason_for_access\": \"Testing rejection for incompatible role and organization type.\"
  }"
```

Expected:

```text
HTTP/1.1 400 Bad Request
role_not_allowed_for_organization_type
```

## Pending user identity visibility

```bash
SUPER_JSON="$(curl -fsS -X POST http://127.0.0.1:8085/auth/login   -H "Content-Type: application/json"   -d '{
    "email": "super.admin@aml-smpc.local",
    "password": "SuperAdmin123"
  }')"

SUPER_TOKEN="$(echo "$SUPER_JSON" | jq -r '.token')"

curl -fsS http://127.0.0.1:8085/admin/users/pending   -H "Authorization: Bearer $SUPER_TOKEN"   | jq '.[] | {
      full_name,
      email,
      organization_name,
      bank_code,
      organization_type,
      bank_employee_id,
      department,
      job_title,
      requested_role,
      approval_status
    }'
```

Expected fields:

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

## UI validation

Open:

```text
/register
```

Confirm fields:

```text
Full Name
Email
Password
Partner Bank / Organization Code
Bank Employee ID
Department
Job Title
Requested Role
Reason for Access
```

Login:

```text
super.admin@aml-smpc.local
SuperAdmin123
```

Open:

```text
/super-admin/pending-users
/super-admin/users
/super-admin/organizations
```

Expected:

```text
Bank code, organization type, employee ID, department, job title visible.
```

---

# Stage 2 — Permission Attributes and RBAC Matrix

## Super-admin permission matrix test

```bash
SUPER_JSON="$(curl -fsS -X POST http://127.0.0.1:8085/auth/login   -H "Content-Type: application/json"   -d '{
    "email": "super.admin@aml-smpc.local",
    "password": "SuperAdmin123"
  }')"

SUPER_TOKEN="$(echo "$SUPER_JSON" | jq -r '.token')"

curl -fsS http://127.0.0.1:8085/admin/roles   -H "Authorization: Bearer $SUPER_TOKEN"   | jq '.[] | select(.role=="transaction_reviewer" or .role=="regulator" or .role=="super_admin") | {
      role,
      permissions
    }'
```

Expected permissions include:

```text
users:manage
organizations:manage
roles:read
transactions:screen
transactions:reject
transactions:flag_suspicious
cases:create
cases:read
cases:update
cases:respond
```

## Non-super-admin blocked from roles

```bash
SUBMITTER_JSON="$(curl -fsS -X POST http://127.0.0.1:8085/auth/login   -H "Content-Type: application/json"   -d '{
    "email": "demo.submitter@example.com",
    "password": "StrongPass123"
  }')"

SUBMITTER_TOKEN="$(echo "$SUBMITTER_JSON" | jq -r '.token')"

curl -i -sS http://127.0.0.1:8085/admin/roles   -H "Authorization: Bearer $SUBMITTER_TOKEN"
```

Expected:

```text
HTTP/1.1 403 Forbidden
```

## UI validation

Login as super admin:

```text
super.admin@aml-smpc.local
SuperAdmin123
```

Open:

```text
/super-admin/roles
/super-admin/users
```

Expected:

```text
Role
Permission
Attribute
read
write
execute
approve
verify
manage
```

---

# Stage 3 — Bank-Side Suspicious Transaction Rules Engine

## Migration validation

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2-)"

psql "$DATABASE_URL" -v ON_ERROR_STOP=1   -f infra/postgres/migrations/009_suspicion_rules_and_transaction_risk.sql

psql "$DATABASE_URL" -c "\d transactions"
psql "$DATABASE_URL" -c "\d aml_rules"

psql "$DATABASE_URL" -c "
SELECT rule_code, rule_type, risk_weight, is_active
FROM aml_rules
ORDER BY rule_code;
"
```

Expected AML rules:

```text
AMOUNT_HIGH_VALUE
CROSS_BORDER_TRANSFER
MISSING_PAYMENT_TRANSPARENCY
HIGH_RISK_COUNTERPARTY
CDD_INCOMPLETE
SMPC_CROSS_BANK_OVERLAP
SANCTIONS_SCREEN_ATTENTION
```

## Risk evaluation terminal test

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

SUBMITTER_JSON="$(curl -fsS -X POST http://127.0.0.1:8085/auth/login   -H "Content-Type: application/json"   -d '{
    "email": "demo.submitter@example.com",
    "password": "StrongPass123"
  }')"

REVIEWER_JSON="$(curl -fsS -X POST http://127.0.0.1:8085/auth/login   -H "Content-Type: application/json"   -d '{
    "email": "demo.reviewer@example.com",
    "password": "StrongPass123"
  }')"

SUBMITTER_TOKEN="$(echo "$SUBMITTER_JSON" | jq -r '.token')"
REVIEWER_TOKEN="$(echo "$REVIEWER_JSON" | jq -r '.token')"

TX_ID="TX-RISK-$(date +%Y%m%d%H%M%S)"

curl -i -sS -X POST http://127.0.0.1:8085/transactions   -H "Authorization: Bearer $SUBMITTER_TOKEN"   -H "Content-Type: application/json"   -d "{
    \"tx_id\": \"$TX_ID\",
    \"sender_id\": \"SENDER-$TX_ID\",
    \"receiver_id\": \"RECEIVER-$TX_ID\",
    \"sender_entity_id\": 1001,
    \"receiver_entity_id\": 2002,
    \"sender_pseudo\": \"bank_a_customer_hash_001\",
    \"receiver_pseudo\": \"shared_counterparty_hash_777\",
    \"amount\": 250000,
    \"amount_cipher_ref\": \"cipher_amount_250000_demo\",
    \"currency\": \"USD\",
    \"transaction_type\": \"cross_border_wire_transfer\",
    \"originator_name\": \"Demo Originator Customer\",
    \"beneficiary_name\": \"Demo Beneficiary Customer\",
    \"originator_institution\": \"Bank A Uganda\",
    \"beneficiary_institution\": \"Bank B Kenya\",
    \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"counterparty_risk\": \"high_risk_counterparty\",
    \"cdd_status\": \"cdd_incomplete\",
    \"screening_indicator\": \"watchlist_attention\",
    \"possible_cross_bank_overlap_count\": 1
  }"
```

Expected:

```text
HTTP/1.1 201 Created
```

Submitter blocked:

```bash
curl -i -sS -X POST "http://127.0.0.1:8085/transactions/$TX_ID/evaluate-risk"   -H "Authorization: Bearer $SUBMITTER_TOKEN"   -H "Content-Type: application/json"   -d '{"review_notes":"Submitter must not evaluate risk."}' | head -30
```

Expected:

```text
HTTP/1.1 403 Forbidden
```

Reviewer evaluates risk:

```bash
curl -fsS -X POST "http://127.0.0.1:8085/transactions/$TX_ID/evaluate-risk"   -H "Authorization: Bearer $REVIEWER_TOKEN"   -H "Content-Type: application/json"   -d '{"review_notes":"Reviewer executed bank-side AML risk evaluation before regulator verification."}'   | jq '{
      tx_id,
      risk_score,
      risk_level,
      suspicion_status,
      recommended_action,
      triggered_rules: [.triggered_rules[].rule_code],
      workflow_risk: {
        risk_score: .workflow.risk_score,
        risk_level: .workflow.risk_level,
        suspicion_status: .workflow.suspicion_status
      }
    }'
```

Expected:

```text
risk_score > 0
risk_level = high
suspicion_status = suspicious
triggered_rules include AML risk rules
```

DB persistence:

```bash
export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2-)"

psql "$DATABASE_URL" -c "
SELECT
  tx_id,
  risk_score,
  risk_level,
  suspicion_status,
  recommended_action,
  screened_at
FROM transactions
WHERE tx_id = '$TX_ID';
"

psql "$DATABASE_URL" -c "
SELECT
  tx_id,
  event_type,
  event_status,
  event_ref,
  details->>'bank_identifies_suspicion_before_regulator' AS bank_first
FROM audit_logs
WHERE tx_id = '$TX_ID'
  AND event_type = 'bank_side_risk_evaluation'
ORDER BY created_at DESC
LIMIT 1;
"
```

Expected:

```text
event_type = bank_side_risk_evaluation
bank_first = true
```

## UI validation

Login as reviewer:

```text
demo.reviewer@example.com
StrongPass123
```

Open:

```text
/institution/suspicious-transactions
/institution/risk-evaluation
/institution/transactions/<TX_ID>/risk
```

Expected:

```text
Risk score, risk level, suspicion status, triggered AML rules, recommended action visible.
```

Login as submitter:

```text
demo.submitter@example.com
StrongPass123
```

Try:

```text
/institution/suspicious-transactions
/institution/risk-evaluation
```

Expected:

```text
Blocked or redirected by frontend route guard.
```

---

# Stage 4 — Connect Bank-Side Risk to SMPC Collaboration

## Terminal validation

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

SUBMITTER_JSON="$(curl -fsS -X POST http://127.0.0.1:8085/auth/login   -H "Content-Type: application/json"   -d '{
    "email": "demo.submitter@example.com",
    "password": "StrongPass123"
  }')"

REVIEWER_JSON="$(curl -fsS -X POST http://127.0.0.1:8085/auth/login   -H "Content-Type: application/json"   -d '{
    "email": "demo.reviewer@example.com",
    "password": "StrongPass123"
  }')"

SUBMITTER_TOKEN="$(echo "$SUBMITTER_JSON" | jq -r '.token')"
REVIEWER_TOKEN="$(echo "$REVIEWER_JSON" | jq -r '.token')"

TX_ID="TX-SMPC-RISK-$(date +%Y%m%d%H%M%S)"

curl -fsS -X POST http://127.0.0.1:8085/transactions   -H "Authorization: Bearer $SUBMITTER_TOKEN"   -H "Content-Type: application/json"   -d "{
    \"tx_id\": \"$TX_ID\",
    \"sender_id\": \"SENDER-$TX_ID\",
    \"receiver_id\": \"RECEIVER-$TX_ID\",
    \"sender_entity_id\": 1001,
    \"receiver_entity_id\": 2002,
    \"sender_pseudo\": \"bank_a_customer_hash_001\",
    \"receiver_pseudo\": \"shared_counterparty_hash_777\",
    \"amount\": 250000,
    \"amount_cipher_ref\": \"cipher_amount_250000_demo\",
    \"currency\": \"USD\",
    \"transaction_type\": \"cross_border_wire_transfer\",
    \"originator_name\": \"Demo Originator Customer\",
    \"beneficiary_name\": \"Demo Beneficiary Customer\",
    \"originator_institution\": \"Bank A Uganda\",
    \"beneficiary_institution\": \"Bank B Kenya\",
    \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"possible_cross_bank_overlap_count\": 1,
    \"screening_indicator\": \"watchlist_attention\"
  }" | jq '{tx_id,status}'

curl -fsS -X POST "http://127.0.0.1:8085/transactions/$TX_ID/approve"   -H "Authorization: Bearer $REVIEWER_TOKEN"   -H "Content-Type: application/json"   -d '{"note":"Reviewer approved transaction for SMPC screening."}'   | jq '{tx_id,status,reviewer_email}'

curl -fsS -X POST "http://127.0.0.1:8085/transactions/$TX_ID/run-screening"   -H "Authorization: Bearer $REVIEWER_TOKEN"   | jq '{
      workflow_status: .workflow.status,
      risk_update: .risk_update
    }'

curl -fsS "http://127.0.0.1:8085/transactions/$TX_ID"   -H "Authorization: Bearer $REVIEWER_TOKEN"   | jq '{
      tx_id,
      status,
      risk_score,
      risk_level,
      suspicion_status,
      triggered_rules,
      recommended_action,
      risk_screened_by_email,
      risk_screened_at
    }'
```

Expected:

```text
workflow_status = screened
risk_score > 0
risk_level = medium or high
suspicion_status = under_review or suspicious
triggered_rules includes SMPC_CROSS_BANK_OVERLAP and/or SANCTIONS_SCREEN_ATTENTION
raw_bank_inputs_disclosed = false
```

Audit evidence:

```bash
export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2-)"

psql "$DATABASE_URL" -c "
SELECT
  tx_id,
  event_type,
  event_status,
  details->>'bank_side_risk_connected_to_smpc' AS smpc_linked
FROM audit_logs
WHERE tx_id = '$TX_ID'
  AND event_type = 'smpc_screening_risk_linked'
ORDER BY created_at DESC
LIMIT 1;
"
```

Expected:

```text
event_type = smpc_screening_risk_linked
smpc_linked = true
```

## UI validation

Login as reviewer:

```text
demo.reviewer@example.com
StrongPass123
```

Open:

```text
/institution/screening-results
```

Enter:

```text
TX-SMPC-RISK-...
```

Click:

```text
Load Workflow
Run SMPC Screening
```

Expected:

```text
Workflow status = screened
Risk score visible
Risk level visible
Suspicion status visible
Linked AML rules visible
Raw Screening Response visible
Risk Update From SMPC Screening visible
No audit-read permission error for transaction reviewer
```

---

# Stage 5A/5B — Regulator Anomaly Case Foundation

## Migration validation

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2-)"

psql "$DATABASE_URL" -v ON_ERROR_STOP=1   -f infra/postgres/migrations/010_regulator_anomaly_cases.sql

psql "$DATABASE_URL" -c "\d anomaly_cases"
psql "$DATABASE_URL" -c "\d anomaly_case_banks"
```

Expected:

```text
anomaly_cases table exists
anomaly_case_banks table exists
```

Expected `anomaly_cases` fields:

```text
id
case_ref
tx_id
opened_by
case_status
risk_level
summary
regulator_finding
required_bank_action
created_at
updated_at
```

Expected `anomaly_case_banks` fields:

```text
id
case_id
organization_id
notice_status
bank_response
responded_by
responded_at
created_at
```

## Stage 5 source context inspection

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

mkdir -p .inspection

{
  echo "============================================================"
  echo "STAGE 5 SOURCE CONTEXT"
  echo "============================================================"

  echo
  echo "=== backend src files ==="
  find services/regulator-api/backend/src -maxdepth 2 -type f | sort

  echo
  echo "=== main.rs ==="
  sed -n '1,220p' services/regulator-api/backend/src/main.rs

  echo
  echo "=== routes.rs ==="
  sed -n '1,260p' services/regulator-api/backend/src/routes.rs

  echo
  echo "=== auth.rs permissions area ==="
  grep -n "fn permissions_for_role" -A120 services/regulator-api/backend/src/auth.rs

  echo
  echo "=== frontend routes ==="
  sed -n '1,280p' services/regulator-api/frontend/src/routes/AppRoutes.tsx

  echo
  echo "=== sidebar ==="
  sed -n '1,240p' services/regulator-api/frontend/src/components/navigation/Sidebar.tsx

  echo
  echo "=== existing API clients ==="
  find services/regulator-api/frontend/src/api -maxdepth 1 -type f | sort

} | tee .inspection/STAGE_5_SOURCE_CONTEXT.txt
```

Expected:

```text
Stage 5 context captured
Backend routes do not yet include anomaly case APIs
Frontend routes do not yet include anomaly case pages
```

---

# Git and Pull Request Workflow

## Check status

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git fetch origin --prune
git status -sb
git log --oneline --decorate -5
```

## Push feature branch

```bash
git push --set-upstream origin bank-rbac-suspicion-case-workflow
```

If upstream already exists:

```bash
git push
```

## Pull Request

GitHub:

```text
Pull requests → New pull request
base: main
compare: bank-rbac-suspicion-case-workflow
```

PR title:

```text
Enhance partner-bank RBAC and suspicious transaction workflow
```

PR summary:

```md
## Summary

This branch enhances AML SMPC with partner-bank identity, stronger RBAC, bank-side suspicious transaction detection, SMPC-linked risk classification, and regulator anomaly case foundations.

## Implemented

- Partner-bank-only access request workflow
- Super-admin approval with bank identity visibility
- Role permission attribute matrix
- Bank-side suspicious transaction risk evaluation
- Suspicious transaction frontend pages
- SMPC screening evidence linked into bank-side risk fields
- Anomaly case database foundation

## Validation

- Backend build passed.
- Frontend build passed.
- Invalid partner code returns HTTP 400.
- Incompatible bank/regulator role returns HTTP 400.
- Non-super-admin access to `/admin/roles` returns HTTP 403.
- Reviewer can evaluate risk.
- Submitter cannot evaluate risk.
- SMPC screening updates risk score, risk level, suspicion status, triggered rules, and audit evidence.
```

Do not merge yet if Stage 5C/5D/5E are not complete.

---

# Current Completion Matrix

| Stage | Status |
|---|---|
| Stage 0 — branch and inspection | Passed |
| Stage 1 — partner bank identity | Passed |
| Stage 2 — RBAC permission attributes | Passed |
| Stage 3C — backend risk evaluation | Passed |
| Stage 3D — frontend suspicious transaction pages | Passed |
| Stage 4 — SMPC evidence to risk linkage | Passed |
| Stage 5A — anomaly case migration | Passed |
| Stage 5B — source context inspection | Passed |
| Stage 5C — backend anomaly case APIs | Next |
| Stage 5D — frontend anomaly case pages | Pending |
| Stage 5E — full anomaly case validation | Pending |

---

# Next Implementation Stage

Proceed to:

```text
Stage 5C — Backend anomaly case APIs
```

Required routes:

```text
GET  /regulator/anomaly-cases
POST /regulator/anomaly-cases
GET  /regulator/anomaly-cases/:case_id
POST /regulator/anomaly-cases/:case_id/close

GET  /institution/anomaly-notices
GET  /institution/anomaly-notices/:case_id
POST /institution/anomaly-notices/:case_id/respond
```

RBAC:

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
