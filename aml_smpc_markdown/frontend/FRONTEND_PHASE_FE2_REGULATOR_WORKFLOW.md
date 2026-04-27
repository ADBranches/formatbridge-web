# Frontend Build Timeline — Phase FE2 (Regulator Workflow UI)

**Goal:** Replace terminal-only verification with an interactive regulator UI.

## Primary user flows to implement
1. **List proofs**
2. **View proof details**
3. **Verify selected proof**
4. **View audit timeline**

These flows map directly to the regulator-oriented exit criteria from Phase 5.

## Backend endpoints consumed
- `GET /proofs?tx_id=...`
- `GET /proofs/{proof_id}`
- `POST /proofs/{proof_id}/verify`
- `GET /audit/{tx_id}`

## UI Pages (micro-level)
### 1) Proofs Page — `/proofs`
- Search filter: by `tx_id`
- Table: proof rows
  - columns: `proof_id`, `tx_id`, `rule_id`, `public_signal`, `verification_status`, `created_at`
- Actions:
  - “View” → proof detail drawer/page
  - “Verify” → calls verify endpoint and shows result

### 2) Proof Detail Page — `/proofs/:proof_id`
- Read-only JSON view (safe fields only)
- Show:
  - `rule_id`
  - `claim_hash`
  - `public_signal`
  - `verification_status`
- Button:
  - “Verify proof” (POST verify)

### 3) Audit Timeline Page — `/audit`
- Search filter: by `tx_id`
- Timeline list ordered by `created_at`
- Each item shows:
  - `event_type`, `event_status`, `event_ref`, `created_at`
  - `details` collapsed JSON

## Data safety requirement
- UI must **not display raw customer identifiers**.
- Only pseudonymized IDs and proof/audit metadata should be shown.

## Acceptance criteria
- Regulator can complete: list → view → verify → audit timeline without terminal.
- Verification response displayed clearly: `verified`, `reason`.
- Errors displayed in UI (toast/banner).

## Evidence to capture
- Screenshots:
  - proofs list
  - proof detail
  - verification result
  - audit timeline
