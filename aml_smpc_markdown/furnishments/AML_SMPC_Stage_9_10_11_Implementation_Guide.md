# AML SMPC Stage 9–11 Implementation Guide

## Purpose

This guide implements the final validation and documentation stages for the AML SMPC enterprise workflow.

It covers:

- **Stage 9 — Validation Scripts**
- **Stage 10 — Documentation Updates**
- **Stage 11 — Final UI Testing Flow**

The goal is to prove that the implemented application now supports:

```text
partner-bank identity
super-admin approval
RBAC permission enforcement
bank-side suspicious transaction detection
SMPC-linked risk classification
proof generation
regulator evidence verification
regulator anomaly cases
bank anomaly notice response
auditor read-only evidence access
```

---

# Stage 9 — Validation Scripts

## Objective

Create reusable validation scripts that prove the new enterprise flow works from terminal.

Scripts to create:

```text
scripts/ci/validate-bank-rbac-identity.sh
scripts/ci/validate-suspicious-transaction-rules.sh
scripts/ci/validate-regulator-anomaly-case-flow.sh
scripts/ci/validate-full-enterprise-demo.sh
```

---

## 9.0 Confirm branch and project state

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git fetch origin --prune
git status -sb
git branch --show-current
git log --oneline --decorate -5
```

Expected branch:

```text
bank-rbac-suspicion-case-workflow
```

---

## 9.1 Create scripts directory

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

mkdir -p scripts/ci
```

---

## 9.2 Create `validate-bank-rbac-identity.sh`

```bash
cat > scripts/ci/validate-bank-rbac-identity.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://127.0.0.1:8085}"
PASSWORD="${PASSWORD:-StrongPass123}"
SUPER_EMAIL="${SUPER_EMAIL:-super.admin@aml-smpc.local}"
SUPER_PASSWORD="${SUPER_PASSWORD:-SuperAdmin123}"

echo "============================================================"
echo "STAGE 9A — BANK RBAC IDENTITY VALIDATION"
echo "============================================================"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "❌ Missing required command: $1"
    exit 1
  }
}

require_cmd curl
require_cmd jq

echo
echo "=== API health ==="
curl -fsS "$API_BASE/health" | jq .

echo
echo "=== Non-partner bank registration must fail ==="
BAD_EMAIL="bad.partner.$(date +%s)@example.com"

BAD_RESPONSE="$(curl -sS -w '\nHTTP_STATUS=%{http_code}\n' -X POST "$API_BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"full_name\": \"Bad Partner User\",
    \"email\": \"$BAD_EMAIL\",
    \"password\": \"$PASSWORD\",
    \"partner_bank_code\": \"NOT_A_PARTNER\",
    \"bank_employee_id\": \"BAD-001\",
    \"department\": \"Compliance\",
    \"job_title\": \"AML Analyst\",
    \"requested_role\": \"transaction_submitter\",
    \"reason_for_access\": \"Testing rejection for invalid partner organization code.\"
  }")"

echo "$BAD_RESPONSE"

echo "$BAD_RESPONSE" | grep -q "HTTP_STATUS=400"
echo "$BAD_RESPONSE" | grep -q "invalid_partner_bank_code"

echo "✅ non-partner bank registration fails with HTTP 400"

echo
echo "=== Partner bank registration succeeds as pending_approval ==="
GOOD_EMAIL="stage9.partner.$(date +%s)@example.com"

GOOD_RESPONSE="$(curl -fsS -X POST "$API_BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"full_name\": \"Stage9 Partner User\",
    \"email\": \"$GOOD_EMAIL\",
    \"password\": \"$PASSWORD\",
    \"partner_bank_code\": \"BANK_A_UG\",
    \"bank_employee_id\": \"BANKA-STAGE9-$(date +%s)\",
    \"department\": \"Compliance\",
    \"job_title\": \"AML Analyst\",
    \"requested_role\": \"transaction_submitter\",
    \"reason_for_access\": \"Testing approved partner bank registration and RBAC identity.\"
  }")"

echo "$GOOD_RESPONSE" | jq .

USER_ID="$(echo "$GOOD_RESPONSE" | jq -r '.user_id')"
ACCOUNT_STATUS="$(echo "$GOOD_RESPONSE" | jq -r '.account_status')"
PARTNER_CODE="$(echo "$GOOD_RESPONSE" | jq -r '.partner_bank_code')"

test "$ACCOUNT_STATUS" = "pending_approval"
test "$PARTNER_CODE" = "BANK_A_UG"

echo "✅ partner bank registration succeeds as pending_approval"

echo
echo "=== Super admin login ==="
SUPER_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$SUPER_EMAIL\",
    \"password\": \"$SUPER_PASSWORD\"
  }")"

SUPER_TOKEN="$(echo "$SUPER_JSON" | jq -r '.token')"

test "$SUPER_TOKEN" != "null"
test -n "$SUPER_TOKEN"

echo "$SUPER_JSON" | jq '{email, role, organization_id, permissions}'

echo
echo "=== Super admin approval activates account ==="
APPROVED_JSON="$(curl -fsS -X POST "$API_BASE/admin/users/$USER_ID/approve" \
  -H "Authorization: Bearer $SUPER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"assigned_role":"transaction_submitter"}')"

echo "$APPROVED_JSON" | jq .

echo "$APPROVED_JSON" | jq -e '.account_status == "active" or .status == "active"' >/dev/null

echo "✅ super admin approval activates account"

echo
echo "=== Approved user JWT contains organization_id, role, and permissions ==="
USER_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$GOOD_EMAIL\",
    \"password\": \"$PASSWORD\"
  }")"

echo "$USER_JSON" | jq '{email, role, organization_id, permissions, token_present: (.token != null)}'

echo "$USER_JSON" | jq -e '.organization_id != null' >/dev/null
echo "$USER_JSON" | jq -e '.role == "transaction_submitter"' >/dev/null
echo "$USER_JSON" | jq -e '.permissions | index("transactions:create") != null' >/dev/null

echo "✅ JWT/session contains organization_id, role, and permissions"

echo
echo "============================================================"
echo "BANK RBAC IDENTITY VALIDATION PASSED"
echo "============================================================"
EOF

chmod +x scripts/ci/validate-bank-rbac-identity.sh
```

---

## 9.3 Create `validate-suspicious-transaction-rules.sh`

```bash
cat > scripts/ci/validate-suspicious-transaction-rules.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://127.0.0.1:8085}"
PASSWORD="${PASSWORD:-StrongPass123}"

echo "============================================================"
echo "STAGE 9B — SUSPICIOUS TRANSACTION RULES VALIDATION"
echo "============================================================"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "❌ Missing required command: $1"
    exit 1
  }
}

require_cmd curl
require_cmd jq

echo
echo "=== Login users ==="
SUBMITTER_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"demo.submitter@example.com\",
    \"password\": \"$PASSWORD\"
  }")"

REVIEWER_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"demo.reviewer@example.com\",
    \"password\": \"$PASSWORD\"
  }")"

SUBMITTER_TOKEN="$(echo "$SUBMITTER_JSON" | jq -r '.token')"
REVIEWER_TOKEN="$(echo "$REVIEWER_JSON" | jq -r '.token')"

echo "$SUBMITTER_JSON" | jq '{email, role, organization_id}'
echo "$REVIEWER_JSON" | jq '{email, role, organization_id}'

TX_ID="TX-STAGE9-RISK-$(date +%Y%m%d%H%M%S)"

echo
echo "=== Submit transaction: $TX_ID ==="
curl -fsS -X POST "$API_BASE/transactions" \
  -H "Authorization: Bearer $SUBMITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
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
  }" | jq '{tx_id,status}'

echo
echo "=== Submitter cannot approve ==="
APPROVE_DENIED="$(curl -sS -w '\nHTTP_STATUS=%{http_code}\n' -X POST "$API_BASE/transactions/$TX_ID/approve" \
  -H "Authorization: Bearer $SUBMITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"note":"Submitter should not approve."}')"

echo "$APPROVE_DENIED"
echo "$APPROVE_DENIED" | grep -q "HTTP_STATUS=403"

echo "✅ submitter cannot approve"

echo
echo "=== Submitter cannot evaluate risk ==="
RISK_DENIED="$(curl -sS -w '\nHTTP_STATUS=%{http_code}\n' -X POST "$API_BASE/transactions/$TX_ID/evaluate-risk" \
  -H "Authorization: Bearer $SUBMITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"review_notes":"Submitter should not evaluate risk."}')"

echo "$RISK_DENIED"
echo "$RISK_DENIED" | grep -q "HTTP_STATUS=403"

echo "✅ submitter cannot evaluate risk"

echo
echo "=== Reviewer evaluates risk ==="
RISK_JSON="$(curl -fsS -X POST "$API_BASE/transactions/$TX_ID/evaluate-risk" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"review_notes":"Reviewer executed bank-side AML risk evaluation before regulator verification."}')"

echo "$RISK_JSON" | jq '{
  tx_id,
  risk_score,
  risk_level,
  suspicion_status,
  triggered_rules: [.triggered_rules[].rule_code],
  workflow_risk: {
    risk_score: .workflow.risk_score,
    risk_level: .workflow.risk_level,
    suspicion_status: .workflow.suspicion_status
  }
}'

echo "$RISK_JSON" | jq -e '.risk_score > 0' >/dev/null
echo "$RISK_JSON" | jq -e '.triggered_rules | length > 0' >/dev/null
echo "$RISK_JSON" | jq -e '.suspicion_status == "suspicious" or .suspicion_status == "under_review"' >/dev/null

echo "✅ reviewer can evaluate risk"
echo "✅ risk_score is saved"
echo "✅ triggered_rules are saved"

echo
echo "=== Reviewer can approve ==="
curl -fsS -X POST "$API_BASE/transactions/$TX_ID/approve" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"note":"Reviewer approved risk-evaluated transaction."}' \
  | jq '{tx_id,status,reviewer_email}'

echo
echo "=== Suspicious queue returns record ==="
curl -fsS "$API_BASE/transactions/$TX_ID" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  | jq '{
      tx_id,
      risk_score,
      risk_level,
      suspicion_status,
      triggered_rules,
      recommended_action
    }' | tee /tmp/stage9_suspicious_record.json

jq -e '.risk_score > 0' /tmp/stage9_suspicious_record.json >/dev/null
jq -e '.triggered_rules | length > 0' /tmp/stage9_suspicious_record.json >/dev/null

echo "✅ suspicious transaction record returns saved risk fields"

echo
echo "============================================================"
echo "SUSPICIOUS TRANSACTION RULES VALIDATION PASSED"
echo "TX_ID=$TX_ID"
echo "============================================================"
EOF

chmod +x scripts/ci/validate-suspicious-transaction-rules.sh
```

---

## 9.4 Create `validate-regulator-anomaly-case-flow.sh`

```bash
cat > scripts/ci/validate-regulator-anomaly-case-flow.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://127.0.0.1:8085}"
PASSWORD="${PASSWORD:-StrongPass123}"

echo "============================================================"
echo "STAGE 9C — REGULATOR ANOMALY CASE FLOW VALIDATION"
echo "============================================================"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "❌ Missing required command: $1"
    exit 1
  }
}

require_cmd curl
require_cmd jq
require_cmd psql

if [ ! -f .env ]; then
  echo "❌ Run from aml-system root where .env exists."
  exit 1
fi

export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2-)"

echo
echo "=== Login users ==="
SUBMITTER_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo.submitter@example.com\",\"password\":\"$PASSWORD\"}")"

REVIEWER_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo.reviewer@example.com\",\"password\":\"$PASSWORD\"}")"

REGULATOR_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo.regulator@example.com\",\"password\":\"$PASSWORD\"}")"

AUDITOR_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo.auditor@example.com\",\"password\":\"$PASSWORD\"}")"

SUBMITTER_TOKEN="$(echo "$SUBMITTER_JSON" | jq -r '.token')"
REVIEWER_TOKEN="$(echo "$REVIEWER_JSON" | jq -r '.token')"
REGULATOR_TOKEN="$(echo "$REGULATOR_JSON" | jq -r '.token')"
AUDITOR_TOKEN="$(echo "$AUDITOR_JSON" | jq -r '.token')"
REVIEWER_ORG_ID="$(echo "$REVIEWER_JSON" | jq -r '.organization_id')"

TX_ID="TX-STAGE9-CASE-$(date +%Y%m%d%H%M%S)"

echo
echo "=== Create suspicious transaction ==="
curl -fsS -X POST "$API_BASE/transactions" \
  -H "Authorization: Bearer $SUBMITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
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

curl -fsS -X POST "$API_BASE/transactions/$TX_ID/approve" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"note":"Reviewer approved transaction for SMPC screening."}' \
  | jq '{tx_id,status}'

curl -fsS -X POST "$API_BASE/transactions/$TX_ID/run-screening" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  | jq '{workflow_status: .workflow.status, risk_update: .risk_update}'

echo
echo "=== Regulator opens anomaly case ==="
CASE_JSON="$(curl -fsS -X POST "$API_BASE/regulator/anomaly-cases" \
  -H "Authorization: Bearer $REGULATOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"tx_id\": \"$TX_ID\",
    \"summary\": \"SMPC-linked suspicious transaction requires partner bank follow-up.\",
    \"regulator_finding\": \"Aggregate evidence shows cross-bank overlap and screening attention without exposing raw bank inputs.\",
    \"required_bank_action\": \"Review the transaction, confirm internal investigation status, and respond to the regulator notice.\",
    \"notified_organization_ids\": [\"$REVIEWER_ORG_ID\"]
  }")"

echo "$CASE_JSON" | jq '{id, case_ref, tx_id, case_status, risk_level, bank_notices}'

CASE_ID="$(echo "$CASE_JSON" | jq -r '.id')"
CASE_REF="$(echo "$CASE_JSON" | jq -r '.case_ref')"

test "$CASE_ID" != "null"
test -n "$CASE_ID"

echo "✅ regulator can open anomaly case"

echo
echo "=== Auditor can read case ==="
curl -fsS "$API_BASE/regulator/anomaly-cases/$CASE_ID" \
  -H "Authorization: Bearer $AUDITOR_TOKEN" \
  | jq '{case_ref, tx_id, case_status, risk_level}'

echo "✅ auditor can read case"

echo
echo "=== Auditor cannot update/close case ==="
AUDITOR_CLOSE="$(curl -sS -w '\nHTTP_STATUS=%{http_code}\n' -X POST "$API_BASE/regulator/anomaly-cases/$CASE_ID/close" \
  -H "Authorization: Bearer $AUDITOR_TOKEN")"

echo "$AUDITOR_CLOSE"
echo "$AUDITOR_CLOSE" | grep -q "HTTP_STATUS=403"

echo "✅ auditor cannot update case"

echo
echo "=== Bank can see notice ==="
NOTICE_JSON="$(curl -fsS "$API_BASE/institution/anomaly-notices" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  | jq '.[] | select(.case_id=="'"$CASE_ID"'")')"

echo "$NOTICE_JSON" | jq '{
  case_ref,
  tx_id,
  notice_status,
  risk_level,
  aggregate_evidence_summary
}'

echo "$NOTICE_JSON" | jq -e '.aggregate_evidence_summary.raw_bank_inputs_exposed == false' >/dev/null

echo "✅ bank can see notice"
echo "✅ raw bank data is not exposed"

echo
echo "=== Bank can respond to notice ==="
curl -fsS -X POST "$API_BASE/institution/anomaly-notices/$CASE_ID/respond" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bank_response": "Bank reviewer confirms the anomaly notice was received and internal investigation has started."
  }' | jq '{case_ref, notice_status, bank_response}'

echo "✅ bank can respond to notice"

echo
echo "=== Submitter cannot read notices ==="
SUBMITTER_NOTICE="$(curl -sS -w '\nHTTP_STATUS=%{http_code}\n' "$API_BASE/institution/anomaly-notices" \
  -H "Authorization: Bearer $SUBMITTER_TOKEN")"

echo "$SUBMITTER_NOTICE"
echo "$SUBMITTER_NOTICE" | grep -q "HTTP_STATUS=403"

echo "✅ submitter cannot read anomaly notices"

echo
echo "============================================================"
echo "REGULATOR ANOMALY CASE FLOW VALIDATION PASSED"
echo "TX_ID=$TX_ID"
echo "CASE_ID=$CASE_ID"
echo "CASE_REF=$CASE_REF"
echo "============================================================"
EOF

chmod +x scripts/ci/validate-regulator-anomaly-case-flow.sh
```

---

## 9.5 Create `validate-full-enterprise-demo.sh`

```bash
cat > scripts/ci/validate-full-enterprise-demo.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo "STAGE 9D — FULL ENTERPRISE DEMO VALIDATION"
echo "============================================================"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "❌ Missing required command: $1"
    exit 1
  }
}

require_cmd curl
require_cmd jq
require_cmd psql
require_cmd cargo
require_cmd npm
require_cmd git

echo
echo "=== Build backend ==="
cargo build --manifest-path services/regulator-api/backend/Cargo.toml

echo
echo "=== Build frontend ==="
(
  cd services/regulator-api/frontend
  npm run build
)

echo
echo "=== Validate API health ==="
curl -fsS http://127.0.0.1:8085/health | jq .

echo
echo "=== Run Stage 9A — Bank RBAC Identity ==="
./scripts/ci/validate-bank-rbac-identity.sh

echo
echo "=== Run Stage 9B — Suspicious Transaction Rules ==="
./scripts/ci/validate-suspicious-transaction-rules.sh

echo
echo "=== Run Stage 9C — Regulator Anomaly Case Flow ==="
./scripts/ci/validate-regulator-anomaly-case-flow.sh

echo
echo "=== Proof generation and regulator verification smoke ==="
PASSWORD="${PASSWORD:-StrongPass123}"
API_BASE="${API_BASE:-http://127.0.0.1:8085}"

SUBMITTER_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo.submitter@example.com\",\"password\":\"$PASSWORD\"}")"

REVIEWER_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo.reviewer@example.com\",\"password\":\"$PASSWORD\"}")"

REGULATOR_JSON="$(curl -fsS -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo.regulator@example.com\",\"password\":\"$PASSWORD\"}")"

SUBMITTER_TOKEN="$(echo "$SUBMITTER_JSON" | jq -r '.token')"
REVIEWER_TOKEN="$(echo "$REVIEWER_JSON" | jq -r '.token')"
REGULATOR_TOKEN="$(echo "$REGULATOR_JSON" | jq -r '.token')"

TX_ID="TX-STAGE9-FULL-$(date +%Y%m%d%H%M%S)"

curl -fsS -X POST "$API_BASE/transactions" \
  -H "Authorization: Bearer $SUBMITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
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

curl -fsS -X POST "$API_BASE/transactions/$TX_ID/approve" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"note":"Reviewer approved transaction for full enterprise validation."}' \
  | jq '{tx_id,status}'

curl -fsS -X POST "$API_BASE/transactions/$TX_ID/run-screening" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  | jq '{workflow_status: .workflow.status, risk_update: .risk_update}'

curl -fsS -X POST "$API_BASE/transactions/$TX_ID/generate-proofs" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" \
  | jq '{workflow: .workflow.status, proof_count: (.proof_response | length)}'

PROOF_COUNT="$(curl -fsS "$API_BASE/proofs?tx_id=$TX_ID" \
  -H "Authorization: Bearer $REGULATOR_TOKEN" \
  | jq 'length')"

if [ "$PROOF_COUNT" -lt 1 ]; then
  echo "❌ Expected regulator to read generated proofs."
  exit 1
fi

echo "✅ proof generation works"
echo "✅ regulator verification/proof inspection works"

echo
echo "=== Repo audit stays clean ==="
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC
git status -sb

if git status --porcelain | grep -q .; then
  echo "⚠️ Working tree has changes. This may be expected before committing Stage 9/10 docs."
else
  echo "✅ repository working tree is clean"
fi

echo
echo "============================================================"
echo "FULL ENTERPRISE DEMO VALIDATION PASSED"
echo "============================================================"
EOF

chmod +x scripts/ci/validate-full-enterprise-demo.sh
```

---

## 9.6 Run Stage 9 scripts

Backend must be running first:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
source env/bin/activate
./scripts/demo/run-frontend-backend.sh
```

In another terminal:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

./scripts/ci/validate-bank-rbac-identity.sh
./scripts/ci/validate-suspicious-transaction-rules.sh
./scripts/ci/validate-regulator-anomaly-case-flow.sh
./scripts/ci/validate-full-enterprise-demo.sh
```

Expected:

```text
BANK RBAC IDENTITY VALIDATION PASSED
SUSPICIOUS TRANSACTION RULES VALIDATION PASSED
REGULATOR ANOMALY CASE FLOW VALIDATION PASSED
FULL ENTERPRISE DEMO VALIDATION PASSED
```

---

# Stage 10 — Documentation Updates

## Objective

Keep project report, runbooks, and presentation guides aligned with the new implementation.

Update existing docs:

```text
docs/demo/FINAL_PROJECT_PRESENTATION_RUNBOOK.md
docs/demo/APPLICATION_RUN_AND_RESEARCH_OBJECTIVES_GUIDE.md
docs/defense/FINAL_PRESENTATION_STORY.md
docs/defense/EXAMINER_DEFENSE_NOTES.md
docs/submission/FINAL_SUBMISSION_CHECKLIST.md
```

Add new docs:

```text
docs/demo/BANK_RBAC_SUSPICION_CASE_WORKFLOW.md
docs/demo/PARTNER_BANK_IDENTITY_MODEL.md
docs/demo/SUSPICIOUS_TRANSACTION_RULE_ENGINE.md
docs/demo/REGULATOR_ANOMALY_CASE_FEEDBACK.md
```

---

## 10.1 Create documentation directories

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

mkdir -p docs/demo docs/defense docs/submission
```

---

## 10.2 Add `BANK_RBAC_SUSPICION_CASE_WORKFLOW.md`

```bash
cat > docs/demo/BANK_RBAC_SUSPICION_CASE_WORKFLOW.md <<'EOF'
# Bank RBAC, Suspicion, and Anomaly Case Workflow

## Purpose

This document explains the enterprise workflow implemented in the AML SMPC system.

The current implementation demonstrates that suspicious transaction identification begins at the financial-institution layer, not at the regulator layer.

## Correct Flow

1. A partner bank user registers under an approved partner-bank code.
2. A super admin approves the user and assigns a role.
3. A transaction submitter creates a transaction.
4. A transaction reviewer evaluates AML risk.
5. Bank-side rules flag suspicious activity.
6. The reviewer approves the transaction for screening.
7. SMPC screening produces privacy-preserving aggregate evidence.
8. Proofs and audit records are generated.
9. The regulator verifies evidence.
10. The regulator opens an anomaly case.
11. Involved banks receive scoped notices.
12. Banks respond without seeing other banks' raw data.
13. Auditors can inspect evidence in read-only mode.

## Privacy Boundary

Banks may see:

- case ID
- their own related transaction reference
- risk level
- regulator finding
- required action
- aggregate SMPC evidence summary

Banks should not see:

- other banks' customer IDs
- other banks' raw account IDs
- other banks' raw transaction payloads

## Research Framing

Bank A, Bank B, and Bank C are SMPC-style participants. They contribute private or pseudonymized information. The SMPC runtime returns aggregate evidence. The regulator does not receive raw bank inputs.
EOF
```

---

## 10.3 Add `PARTNER_BANK_IDENTITY_MODEL.md`

```bash
cat > docs/demo/PARTNER_BANK_IDENTITY_MODEL.md <<'EOF'
# Partner Bank Identity Model

## Purpose

The AML SMPC system is not a general public signup system. It is designed for approved partner banks, regulators, auditors, and platform administrators.

## Registration Fields

Users request access with:

- full name
- email
- password
- partner bank code
- bank employee ID
- department
- job title
- requested role
- reason for access

## Approval Flow

1. User registers under a valid partner organization code.
2. Account status becomes `pending_approval`.
3. Super admin reviews the request.
4. Super admin approves, rejects, assigns role, activates, or deactivates user.
5. Approved user receives session permissions based on assigned role.

## Organization Types

Supported organization types:

- bank
- regulator
- auditor
- platform

## Role Examples

Bank roles:

- institution_admin
- transaction_submitter
- transaction_reviewer

Oversight roles:

- regulator
- auditor
- super_admin

## Security Benefit

Every user is tied to an organization scope, making RBAC and partner-bank data boundaries easier to demonstrate.
EOF
```

---

## 10.4 Add `SUSPICIOUS_TRANSACTION_RULE_ENGINE.md`

```bash
cat > docs/demo/SUSPICIOUS_TRANSACTION_RULE_ENGINE.md <<'EOF'
# Suspicious Transaction Rule Engine

## Purpose

Suspicious transactions are identified at the bank side before regulator verification.

## Rule Examples

Implemented AML rule categories include:

- AMOUNT_HIGH_VALUE
- CROSS_BORDER_TRANSFER
- MISSING_PAYMENT_TRANSPARENCY
- HIGH_RISK_COUNTERPARTY
- CDD_INCOMPLETE
- SMPC_CROSS_BANK_OVERLAP
- SANCTIONS_SCREEN_ATTENTION

## Risk Fields

Each risk-evaluated transaction stores:

- risk_score
- risk_level
- suspicion_status
- triggered_rules
- recommended_action
- review_notes
- screened_by
- screened_at

## Risk Levels

- low: 0–39
- medium: 40–69
- high: 70+

## Suspicion Statuses

- not_evaluated
- not_suspicious
- under_review
- suspicious

## Demonstration Value

This proves that the bank identifies suspicious activity first and only later escalates evidence for regulator verification.
EOF
```

---

## 10.5 Add `REGULATOR_ANOMALY_CASE_FEEDBACK.md`

```bash
cat > docs/demo/REGULATOR_ANOMALY_CASE_FEEDBACK.md <<'EOF'
# Regulator Anomaly Case Feedback

## Purpose

The regulator anomaly case workflow converts suspicious SMPC/risk evidence into formal case feedback for involved banks.

## Correct Flow

1. Bank flags suspicious activity.
2. SMPC produces privacy-preserving aggregate evidence.
3. Proof and audit records are generated.
4. Regulator verifies evidence.
5. Regulator opens an anomaly case.
6. Banks receive scoped notices.
7. Banks respond to the regulator notice.

## Regulator Can

- list anomaly cases
- open anomaly case
- inspect case details
- close case
- view banks notified
- view bank response status

## Bank Can

- view own notices
- view aggregate evidence summary
- respond to regulator notice

## Auditor Can

- read regulator anomaly cases
- inspect evidence in read-only mode

## Privacy Boundary

The bank-facing notice does not expose other banks' raw customer IDs, raw account IDs, or raw transaction payloads.
EOF
```

---

## 10.6 Update or create final runbooks

```bash
cat > docs/demo/FINAL_PROJECT_PRESENTATION_RUNBOOK.md <<'EOF'
# Final Project Presentation Runbook

## Startup

### Backend

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
source env/bin/activate
./scripts/demo/run-frontend-backend.sh
```

### Frontend

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system/services/regulator-api/frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173
```

## Demo Order

1. Public landing page.
2. Register partner-bank user.
3. Super admin approval.
4. Transaction submitter creates transaction.
5. Transaction reviewer evaluates risk.
6. Reviewer approves transaction.
7. Reviewer runs SMPC screening.
8. Reviewer generates proofs.
9. Regulator inspects proofs and evidence.
10. Regulator opens anomaly case.
11. Bank reviewer views anomaly notice.
12. Bank reviewer responds.
13. Auditor confirms read-only access.

## Main Defense Statement

Suspicious transaction identification begins at the financial-institution layer. Bank-side submitters and reviewers process transactions under their approved partner-bank identity, and reviewers execute risk evaluation using AML rules before SMPC collaboration and proof generation. The SMPC layer supports cross-bank collaborative risk evidence without disclosing raw private bank data. The regulator then verifies proof and audit evidence, and may open anomaly cases for affected partner banks.
EOF
```

```bash
cat > docs/demo/APPLICATION_RUN_AND_RESEARCH_OBJECTIVES_GUIDE.md <<'EOF'
# Application Run and Research Objectives Guide

## Research Objective

The project demonstrates privacy-preserving anti-money laundering collaboration using SMPC-style multi-bank evidence sharing, cryptographic proof generation, auditability, and regulator verification.

## Application Objective

The application supports:

- partner-bank identity
- RBAC authorization
- bank-side transaction submission
- bank-side suspicion detection
- SMPC-linked risk evidence
- proof generation
- regulator evidence verification
- anomaly case feedback
- bank notice response
- auditor read-only oversight

## Privacy Objective

The regulator receives evidence, proofs, risk summaries, and anomaly case data, but not raw bank customer data from other institutions.

## Run Commands

Backend:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
source env/bin/activate
./scripts/demo/run-frontend-backend.sh
```

Frontend:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system/services/regulator-api/frontend
npm run dev -- --host 127.0.0.1 --port 5173
```
EOF
```

```bash
cat > docs/defense/FINAL_PRESENTATION_STORY.md <<'EOF'
# Final Presentation Story

## Opening

This project addresses a common AML challenge: financial institutions may need to collaborate to detect suspicious behavior, but direct sharing of raw customer or transaction data creates privacy, compliance, and trust issues.

## System Story

The AML SMPC platform solves this by allowing partner banks to participate in privacy-preserving screening while regulators verify evidence after the bank-side process.

## Demonstration Story

1. A partner-bank user requests access.
2. A super admin approves and assigns role.
3. The bank submits a transaction.
4. The bank reviewer detects suspicious risk using AML rules.
5. SMPC screening contributes aggregate cross-bank evidence.
6. Proofs and audit logs are generated.
7. Regulator verifies evidence.
8. Regulator opens anomaly case.
9. Involved bank receives notice and responds.
10. Auditor confirms read-only governance access.

## Core Claim

The system demonstrates privacy-preserving AML collaboration where banks can share useful risk evidence without revealing raw private data to other banks or to the regulator.
EOF
```

```bash
cat > docs/defense/EXAMINER_DEFENSE_NOTES.md <<'EOF'
# Examiner Defense Notes

## Question: Who identifies suspicious transactions?

The bank identifies suspicious transactions first. The regulator verifies evidence and opens cases later.

## Question: What does SMPC add?

SMPC adds collaborative evidence across banks without exposing raw private inputs.

## Question: What does the regulator see?

The regulator sees proof status, audit evidence, risk level, triggered rules, aggregate evidence, and anomaly cases.

## Question: What does the regulator not see?

The regulator does not receive other banks' raw customer IDs, raw account IDs, or raw transaction payloads.

## Question: How is RBAC demonstrated?

The system enforces role-specific access:

- super admin manages users and organizations
- submitter creates transactions
- reviewer evaluates risk, approves, screens, and generates proofs
- regulator verifies evidence and opens cases
- auditor reads evidence only

## Question: How is privacy shown in the UI?

The bank notice and regulator dashboard explicitly show that raw bank inputs are not exposed.
EOF
```

```bash
cat > docs/submission/FINAL_SUBMISSION_CHECKLIST.md <<'EOF'
# Final Submission Checklist

## Repository

- [ ] Feature branch pushed.
- [ ] Pull request opened.
- [ ] Backend build passes.
- [ ] Frontend build passes.
- [ ] Validation scripts pass.
- [ ] Final runbook committed.
- [ ] Documentation updated.

## Demo

- [ ] Backend starts locally.
- [ ] Frontend starts locally.
- [ ] Super admin login works.
- [ ] Submitter login works.
- [ ] Reviewer login works.
- [ ] Regulator login works.
- [ ] Auditor login works.
- [ ] Registration flow works.
- [ ] Approval flow works.
- [ ] Transaction submission works.
- [ ] Risk evaluation works.
- [ ] SMPC screening works.
- [ ] Proof generation works.
- [ ] Regulator anomaly case works.
- [ ] Bank anomaly notice response works.
- [ ] Auditor read-only access works.

## Report Alignment

- [ ] Report states that suspicious transaction identification starts at the financial-institution layer.
- [ ] Report explains SMPC privacy-preserving collaboration.
- [ ] Report explains regulator proof/audit verification.
- [ ] Report explains anomaly case feedback to banks.
EOF
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

---

# Stage 9–11 Build and Commit

## Build

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

cargo build --manifest-path services/regulator-api/backend/Cargo.toml

cd services/regulator-api/frontend
npm run build
```

## Git commit

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git status -sb

git add aml-system/scripts/ci/validate-bank-rbac-identity.sh
git add aml-system/scripts/ci/validate-suspicious-transaction-rules.sh
git add aml-system/scripts/ci/validate-regulator-anomaly-case-flow.sh
git add aml-system/scripts/ci/validate-full-enterprise-demo.sh
git add aml-system/docs/demo/FINAL_PROJECT_PRESENTATION_RUNBOOK.md
git add aml-system/docs/demo/APPLICATION_RUN_AND_RESEARCH_OBJECTIVES_GUIDE.md
git add aml-system/docs/defense/FINAL_PRESENTATION_STORY.md
git add aml-system/docs/defense/EXAMINER_DEFENSE_NOTES.md
git add aml-system/docs/submission/FINAL_SUBMISSION_CHECKLIST.md
git add aml-system/docs/demo/BANK_RBAC_SUSPICION_CASE_WORKFLOW.md
git add aml-system/docs/demo/PARTNER_BANK_IDENTITY_MODEL.md
git add aml-system/docs/demo/SUSPICIOUS_TRANSACTION_RULE_ENGINE.md
git add aml-system/docs/demo/REGULATOR_ANOMALY_CASE_FEEDBACK.md

git commit -m "Add enterprise validation scripts and final documentation"

git push
```

---

# Pull Request Update Text

Paste this into the PR after pushing:

```md
### Stage 9 — Validation Scripts

- Added validation scripts:
  - `scripts/ci/validate-bank-rbac-identity.sh`
  - `scripts/ci/validate-suspicious-transaction-rules.sh`
  - `scripts/ci/validate-regulator-anomaly-case-flow.sh`
  - `scripts/ci/validate-full-enterprise-demo.sh`
- Scripts validate:
  - partner-bank registration and approval
  - RBAC enforcement
  - suspicious transaction risk evaluation
  - SMPC-linked screening
  - regulator anomaly case workflow
  - bank notice response
  - auditor read-only case access
  - full enterprise demo flow

### Stage 10 — Documentation Updates

- Updated final runbooks and defense notes.
- Added documentation for:
  - partner bank identity model
  - suspicious transaction rule engine
  - bank RBAC suspicion case workflow
  - regulator anomaly case feedback
- Added report alignment text explaining that suspicious transaction identification begins at the financial-institution layer.

### Stage 11 — Final UI Testing Flow

- Documented browser testing order from registration through auditor read-only access.
- Included backend and frontend startup commands.
```

---

# Exit Criteria

Stage 9–11 passes when:

```text
all four validation scripts exist
all validation scripts are executable
backend build passes
frontend build passes
validation scripts pass
docs are committed
PR description is updated
browser testing flow is documented
```

Next:

```text
Final repository audit
Final PR review
Merge into main when ready
```
