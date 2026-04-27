# Frontend Phase FE0 — Backend Contract & Frontend Readiness Check

## Objective

Confirm the exact backend API contract before building the frontend.

This phase prevents frontend/backend mismatch errors.

## Target Directories

```text
aml-system/docs/frontend/
aml-system/scripts/demo/
```

## Files to Create

```text
aml-system/docs/frontend/api-contract.md
aml-system/docs/frontend/frontend-build-plan.md
aml-system/scripts/demo/frontend-api-smoke.sh
```

## Backend Endpoints to Confirm

```text
GET  /proofs?tx_id=...
GET  /proofs/{proof_id}
POST /proofs/{proof_id}/verify
GET  /audit/{tx_id}
```

Optional evidence endpoints for FE3:

```text
GET /evidence/phase7/functional
GET /evidence/phase7/performance
GET /evidence/phase7/compliance
```

## Step 1 — Start from Project Root

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
mkdir -p docs/frontend scripts/demo
```

## Step 2 — Create Frontend API Smoke Script

```bash
cat > scripts/demo/frontend-api-smoke.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

REGULATOR_API_BASE_URL="${REGULATOR_API_BASE_URL:-http://127.0.0.1:8085}"
TX_ID="${1:-TX-PHASE73-R16-001}"

echo "Frontend API smoke check"
echo "Regulator API: $REGULATOR_API_BASE_URL"
echo "Transaction ID: $TX_ID"

echo
echo "1. List proofs"
curl -fsS "$REGULATOR_API_BASE_URL/proofs?tx_id=$TX_ID" | jq .

PROOF_ID="$(curl -fsS "$REGULATOR_API_BASE_URL/proofs?tx_id=$TX_ID" | jq -r '.[0].id')"

if [ -z "$PROOF_ID" ] || [ "$PROOF_ID" = "null" ]; then
  echo "No proof ID found for tx_id=$TX_ID"
  exit 1
fi

echo
echo "2. Proof detail"
curl -fsS "$REGULATOR_API_BASE_URL/proofs/$PROOF_ID" | jq .

echo
echo "3. Verify proof"
curl -fsS -X POST "$REGULATOR_API_BASE_URL/proofs/$PROOF_ID/verify" | jq .

echo
echo "4. Audit timeline"
curl -fsS "$REGULATOR_API_BASE_URL/audit/$TX_ID" | jq .

echo
echo "✅ Frontend API smoke check passed"
EOF

chmod +x scripts/demo/frontend-api-smoke.sh
```

## Step 3 — Run the Smoke Test

```bash
./scripts/demo/frontend-api-smoke.sh
```

Expected:

```text
✅ Frontend API smoke check passed
```

## Step 4 — Create API Contract Document

```bash
cat > docs/frontend/api-contract.md <<'EOF'
# AML SMPC Frontend API Contract

## Base URL

```text
VITE_REGULATOR_API_BASE_URL=http://127.0.0.1:8085
```

## Endpoints

### List Proofs

```text
GET /proofs?tx_id={tx_id}
```

Safe fields:

```text
id
tx_id
rule_id
public_signal
verification_status
created_at
```

### Proof Detail

```text
GET /proofs/{proof_id}
```

Safe fields:

```text
id
tx_id
rule_id
claim_hash
public_signal
verification_status
proof_blob
created_at
```

### Verify Proof

```text
POST /proofs/{proof_id}/verify
```

Expected fields:

```text
proof_id
tx_id
rule_id
verified
reason
```

### Audit Timeline

```text
GET /audit/{tx_id}
```

Expected fields:

```text
event_type
event_status
event_ref
details
created_at
```

## Data Safety Rule

The frontend must not display raw customer identifiers or real customer data.
EOF
```

## Step 5 — Create Build Plan

```bash
cat > docs/frontend/frontend-build-plan.md <<'EOF'
# AML SMPC Frontend Build Plan

## Stack

```text
React + Vite + TypeScript + Tailwind CSS
```

## Phase Order

```text
FE0 — Backend Contract & Frontend Readiness Check
FE1 — Foundation UI Scaffold
FE2 — Regulator Workflow UI
FE3 — Evidence Dashboard & Performance Visualization
FE4 — Polish, Packaging, and Demo Stability
FE5 — Final Examiner Frontend Package
```
EOF
```

## Acceptance Criteria

```text
API smoke script passes.
API contract document exists.
Frontend build plan exists.
Backend response shapes are confirmed.
```

## Git Commands

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git add aml-system/docs/frontend/api-contract.md
git add aml-system/docs/frontend/frontend-build-plan.md
git add aml-system/scripts/demo/frontend-api-smoke.sh

git commit -m "Add frontend API contract readiness checks"
git push origin main
```
