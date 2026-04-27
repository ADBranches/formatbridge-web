# PHASE 7.3 — Compliance Validation Plan (FATF Recommendations) (Planning‑Only)

> **Status:** Planning & validation definition only (no compliance test scripts populated yet)
>
> **Purpose:** Define exactly how compliance evidence will be validated, which system artifacts are used, what files will be created, and what must be produced for the final report.

---

## Correct Standard Naming (What to use in the professional work)
Use **FATF Recommendations** (not “rules”) and reference them as:
- **Recommendation 10 (R.10)** — Customer Due Diligence (CDD)
- **Recommendation 11 (R.11)** — Record Keeping
- **Recommendation 16 (R.16)** — Payment Transparency / Travel Rule

---

## Compliance validation goals (Phase 7.3)

### R.10 (Customer Due Diligence)
**Validation goal:** Evidence is generated that CDD/KYC-related checks were performed for the transaction workflow.

### R.11 (Record Keeping)
**Validation goal:** Proof-to-transaction-to-audit linkage is retrievable and sufficient to reconstruct event history.

### R.16 (Payment Transparency / Travel Rule)
**Validation goal:** Evidence exists that required payment-transparency metadata is present (originator/beneficiary fields) and a verifiable artifact is generated over that claim.

---

## Existing files under compliance validation

### Proof & verification stack
```
services/zk-prover/circuits/fatf-rec10/src/lib.rs
services/zk-prover/circuits/fatf-rec11/src/lib.rs
services/zk-prover/circuits/fatf-rec16/src/lib.rs

services/zk-prover/prover/src/prove.rs
services/zk-prover/verifier/src/verify.rs
```

### Regulator-facing linkage & retrieval
```
services/regulator-api/backend/src/routes.rs
services/regulator-api/backend/src/db.rs
services/regulator-api/backend/src/proofs.rs
services/regulator-api/backend/src/audit.rs
```

### Database schema and regulator views
```
infra/postgres/migrations/001_create_transactions.sql
infra/postgres/migrations/002_create_audit_logs.sql
infra/postgres/migrations/003_create_proofs.sql
infra/postgres/migrations/004_create_regulator_views.sql
infra/postgres/migrations/005_retention_policy.sql
```

### Compliance documentation baseline
```
docs/compliance/fatf-mapping.md
docs/compliance/audit-traceability.md
docs/compliance/gdpr-controls.md
```

---

## New compliance validation files to create (later)

### Scripted validations
```
tests/compliance/r10_cdd_validation.sh
tests/compliance/r11_recordkeeping_validation.sh
tests/compliance/r16_travelrule_validation.sh
```

### Compliance assertions and results documentation
```
tests/compliance/compliance_assertions.md
tests/compliance/compliance_results_template.md
```

### Optional automation wrapper (recommended)
```
scripts/demo/run-phase7-3-compliance.sh
```

---

## Responsibilities (file-by-file)

### `tests/compliance/r10_cdd_validation.sh`
- Seeds or selects a known transaction.
- Confirms R.10-aligned proof artifact exists for that `tx_id`.
- Confirms the workflow records show CDD screening steps were executed (based on audit events and proof claim fields).

### `tests/compliance/r11_recordkeeping_validation.sh`
- Confirms:
  - transaction row exists,
  - audit log entries exist and are timestamped,
  - proof rows exist and link to the transaction,
  - regulator views return a coherent timeline.

### `tests/compliance/r16_travelrule_validation.sh`
- Confirms payment transparency fields are present (originator/beneficiary institution, etc.).
- Confirms the R.16 proof artifact exists and verifies.

### `tests/compliance/compliance_assertions.md`
- Defines *pass/fail semantics* for each recommendation.
- Defines what fields count as “present” for R.16.
- Defines what counts as “sufficient records” for R.11.

### `tests/compliance/compliance_results_template.md`
- Standardized reporting format:
  - transactions tested
  - proof IDs + rule IDs
  - verification outcomes
  - audit timeline excerpts
  - screenshots/curl outputs

### `scripts/demo/run-phase7-3-compliance.sh` (optional)
- Automation-first wrapper:
  - runs end-to-end transaction submission
  - triggers proof generation
  - performs regulator verification
  - extracts and stores compliance evidence

---

## Evidence to capture (what “passed” looks like)

### R.10 evidence
- Proof artifacts exist for **R.10** and verify.
- Claim does **not** contain raw sensitive payload.

### R.11 evidence
- Transaction, audit, and proof records are retrievable.
- Timeline reconstructable from DB + regulator API.

### R.16 evidence
- Payment transparency metadata fields are present.
- Proof artifact exists for **R.16** and verifies.

---

## Phase 7.3 Exit Criteria
Phase 7.3 is **passed** once:
- R.10, R.11, and R.16 evidence is generated and verified,
- regulator can retrieve proofs and audit metadata,
- and results are documented using the results template.

> **Note:** Implementation (validation scripts + assertions + evidence packaging) happens after this planning definition.
