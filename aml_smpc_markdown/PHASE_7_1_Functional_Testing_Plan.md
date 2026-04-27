# PHASE 7.1 — Functional Testing Plan (Planning‑Only)

> **Status:** Planning & validation definition only (no code populated yet)
>
> **Purpose:** Precisely define *what* will be tested, *which existing files are under test*, *which new test files will be introduced*, and *what evidence each test must produce* for the project report.

---

## Phase Context
Phase 7 is the **evidence-production phase**. It validates correctness, integration, and compliance alignment of what was implemented in **Phases 1–6**. Phase 7.1 focuses exclusively on **functional correctness** (not performance yet).

**Functional scope:**
- HE encryption/decryption
- SMPC equality checks
- zk‑SNARK proof generation & verification
- API flows end‑to‑end

No production features are added in this phase.

---

## 7.1.1 HE Encryption / Decryption

### Objective
Validate that homomorphic encryption correctly:
- encrypts plaintext amounts,
- performs arithmetic over ciphertexts,
- decrypts (test‑only path) to expected numeric values.

### Existing files under test
```text
services/he-orchestrator/seal-core/CMakeLists.txt
services/he-orchestrator/seal-core/include/seal_bridge.hpp
services/he-orchestrator/seal-core/src/context.cpp
services/he-orchestrator/seal-core/src/encrypt.cpp
services/he-orchestrator/seal-core/src/sum.cpp
services/he-orchestrator/seal-core/src/decrypt.cpp

services/he-orchestrator/rust-gateway/Cargo.toml
services/he-orchestrator/rust-gateway/build.rs
services/he-orchestrator/rust-gateway/src/main.rs
services/he-orchestrator/rust-gateway/src/ffi.rs
services/he-orchestrator/rust-gateway/src/routes.rs
```

### New test files to be created (later)
```text
tests/integration/he_encrypt_decrypt_test.sh
tests/integration/he_gateway_api_test.sh
tests/fixtures/he_test_vectors.json
tests/fixtures/he_expected_outputs.json
```

### Responsibility of new files
- **he_encrypt_decrypt_test.sh** — encrypt → sum → decrypt flow, numeric correctness check.
- **he_gateway_api_test.sh** — exercise `/he/encrypt`, `/he/sum`, `/he/decrypt-test` endpoints.
- **he_test_vectors.json** — canonical input values.
- **he_expected_outputs.json** — expected decrypted results.

### Evidence produced
- Logs showing ciphertext generation.
- Decrypted values matching expected outputs within tolerance.

---

## 7.1.2 SMPC Equality Checks

### Objective
Validate that SMPC screening correctly returns **match / no_match** without revealing inputs.

### Existing files under test
```text
services/smpc-orchestrator/programs/sanction_check.mpc
services/smpc-orchestrator/programs/entity_match.mpc
services/smpc-orchestrator/programs/threshold_alert.mpc

services/smpc-orchestrator/runtime/Cargo.toml
services/smpc-orchestrator/runtime/src/main.rs
services/smpc-orchestrator/runtime/src/routes.rs
services/smpc-orchestrator/runtime/src/mp_spdz.rs
services/smpc-orchestrator/runtime/src/parser.rs

scripts/dev/run_mp_spdz_local.sh
scripts/dev/seed_sanction_list.sh
```

### New test files to be created (later)
```text
tests/integration/smpc_match_test.sh
tests/integration/smpc_no_match_test.sh
tests/integration/smpc_api_test.sh
tests/fixtures/smpc_test_cases.json
```

### Responsibility of new files
- **smpc_match_test.sh** — known sanctioned entity → `match`.
- **smpc_no_match_test.sh** — known clean entity → `no_match`.
- **smpc_api_test.sh** — `/smpc/screen` API validation.
- **smpc_test_cases.json** — test entities + expected outcomes.

### Evidence produced
- Deterministic screening results.
- Logs proving MPC execution path ran.

---

## 7.1.3 zk‑SNARK Proof Generation & Verification

### Objective
Validate that proof artifacts for FATF Recommendations 10, 11, and 16:
- are generated,
- are verifiable,
- do not expose raw transaction payloads.

### Existing files under test
```text
services/zk-prover/circuits/fatf-rec10/src/lib.rs
services/zk-prover/circuits/fatf-rec10/src/circuit.rs
services/zk-prover/circuits/fatf-rec10/src/tests.rs

services/zk-prover/circuits/fatf-rec11/src/lib.rs
services/zk-prover/circuits/fatf-rec11/src/circuit.rs
services/zk-prover/circuits/fatf-rec11/src/tests.rs

services/zk-prover/circuits/fatf-rec16/src/lib.rs
services/zk-prover/circuits/fatf-rec16/src/circuit.rs
services/zk-prover/circuits/fatf-rec16/src/tests.rs

services/zk-prover/prover/src/main.rs
services/zk-prover/prover/src/routes.rs
services/zk-prover/prover/src/prove.rs

services/zk-prover/verifier/src/lib.rs
services/zk-prover/verifier/src/verify.rs
```

### New test files to be created (later)
```text
tests/integration/zk_proof_generation_test.sh
tests/integration/zk_proof_verification_test.sh
tests/compliance/rec10_proof_test.sh
tests/compliance/rec11_proof_test.sh
tests/compliance/rec16_proof_test.sh
tests/fixtures/zk_claim_cases.json
```

### Responsibility of new files
- **zk_proof_generation_test.sh** — generate and persist proofs.
- **zk_proof_verification_test.sh** — verify proofs via verifier.
- **rec10/11/16_proof_test.sh** — rule‑specific proof existence.
- **zk_claim_cases.json** — canonical proof scenarios.

### Evidence produced
- Proof artifacts stored.
- Verifier returns `verified = true` where expected.

---

## 7.1.4 API Flows End‑to‑End

### Objective
Validate the integrated pipeline:
transaction → pseudonymization → SMPC screening → proof generation → regulator retrieval.

### Existing files under test
```text
services/encryption-service/api/src/main.rs
services/encryption-service/api/src/routes.rs
services/encryption-service/api/src/pseudonymize.rs
services/encryption-service/api/src/smpc_client.rs
services/encryption-service/fpe/mod.rs

services/he-orchestrator/rust-gateway/src/main.rs
services/he-orchestrator/rust-gateway/src/routes.rs

services/smpc-orchestrator/runtime/src/main.rs
services/smpc-orchestrator/runtime/src/routes.rs

services/zk-prover/prover/src/main.rs
services/zk-prover/prover/src/routes.rs

services/regulator-api/backend/src/main.rs
services/regulator-api/backend/src/routes.rs
services/regulator-api/backend/src/proofs.rs
services/regulator-api/backend/src/audit.rs
services/regulator-api/backend/src/db.rs
```

### New test files to be created (later)
```text
tests/integration/api_end_to_end_test.sh
tests/integration/regulator_flow_test.sh
tests/fixtures/e2e_transactions.json
```

### Responsibility of new files
- **api_end_to_end_test.sh** — full transaction lifecycle.
- **regulator_flow_test.sh** — proof listing, verification, audit timeline.
- **e2e_transactions.json** — canonical E2E payloads.

### Evidence produced
- End‑to‑end success logs.
- Regulator‑visible proof & audit linkage.

---

## Phase 7.1 Exit Criteria
Phase 7.1 will be considered **passed** once:
- HE tests succeed,
- SMPC tests succeed,
- zk proof generation & verification succeed,
- end‑to‑end API flow tests succeed,
- and all results are recorded for reporting.

---

## Output of Phase 7.1
- Structured functional test definitions
- Clear mapping of files under test
- Defined test artifacts and evidence
- Ready foundation for implementation and execution in later steps

> **Note:** Code population and execution will be done in subsequent steps.
