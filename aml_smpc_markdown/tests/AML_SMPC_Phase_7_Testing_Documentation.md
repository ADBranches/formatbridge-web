# AML SMPC Phase 7 Testing Documentation

## Document Purpose

This document records the terminal-based testing process for:

- **Phase 7.1 — Functional Testing**
- **Phase 7.2 — Performance Testing**
- **Phase 7.3 — Compliance Validation**
- **Final Phase 7 Completion Gate**

It is written as a repeatable testing guide for the AML SMPC project located at:

```text
/home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
```

---

## Current Completion Position

Phase 7 is considered functionally complete when the final verification script prints:

```text
✅ PHASE 7.1, 7.2, AND 7.3 ARE COMPLETE
```

The final verification script used is:

```text
aml-system/scripts/ci/verify-phase7-completion.sh
```

---

## 1. Repository Setup and Cleanliness Check

Before testing any phase, start from the real Git root.

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git fetch origin --prune

git rev-list --left-right --count HEAD...origin/main

git status -sb
```

Expected remote sync output:

```text
0	0
```

Expected branch status:

```text
## main...origin/main
```

If evidence summaries were regenerated, Git may show modified files such as:

```text
M aml-system/tests/evidence/phase7_1/PHASE_7_1_FUNCTIONAL_EVIDENCE_SUMMARY.md
M aml-system/tests/evidence/phase7_2/PHASE_7_2_PERFORMANCE_RESULTS.md
M aml-system/tests/evidence/phase7_3/PHASE_7_3_COMPLIANCE_RESULTS.md
```

These are evidence-summary updates and may be committed if they reflect the final test results.

---

## 2. Required Runtime Services

The testing flow expects the following local services to be available or startable by scripts:

| Service | Default URL / Port | Purpose |
|---|---:|---|
| Encryption Service | `http://127.0.0.1:8081` | Transaction submission and pseudonymization |
| HE Gateway | `http://127.0.0.1:8082` | Homomorphic encryption endpoints |
| SMPC Runtime | `http://127.0.0.1:8083` | Match / no-match screening |
| zk Prover | `http://127.0.0.1:8084` | Proof generation and verification |
| Regulator API | `http://127.0.0.1:8085` | Proof and audit retrieval |

The helper scripts are designed to reuse existing running services where possible.

---

## 3. Phase 7.1 — Functional Testing

### 3.1 Objective

Phase 7.1 verifies functional correctness for:

- HE encryption, summation, and test-only decryption
- SMPC match and no-match screening
- zk proof generation and verification
- End-to-end transaction-to-regulator API flow

---

### 3.2 Important Phase 7.1 Files

```text
scripts/ci/test-functional-phase71.sh
scripts/ci/phase71_evidence_summary.sh
tests/integration/lib_phase71.sh
tests/integration/he_gateway_api_test.sh
tests/integration/he_encrypt_decrypt_test.sh
tests/integration/smpc_api_test.sh
tests/integration/smpc_match_test.sh
tests/integration/smpc_no_match_test.sh
tests/integration/zk_proof_generation_test.sh
tests/integration/zk_proof_verification_test.sh
tests/integration/api_end_to_end_test.sh
tests/integration/regulator_flow_test.sh
tests/compliance/rec10_proof_test.sh
tests/compliance/rec11_proof_test.sh
tests/compliance/rec16_proof_test.sh
```

Evidence directory:

```text
tests/evidence/phase7_1/
```

---

### 3.3 Phase 7.1 Syntax Checks

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

bash -n scripts/ci/test-functional-phase71.sh
bash -n tests/integration/lib_phase71.sh
bash -n tests/integration/he_gateway_api_test.sh
bash -n tests/integration/smpc_api_test.sh
bash -n tests/integration/zk_proof_generation_test.sh
bash -n tests/integration/zk_proof_verification_test.sh
bash -n tests/integration/api_end_to_end_test.sh
```

Expected result: no syntax errors.

---

### 3.4 Phase 7.1 Functional Test Execution

Run the full Phase 7.1 runner:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

./scripts/ci/test-functional-phase71.sh
```

Expected major output:

```text
============================================================
Phase 7.1 Functional Test Runner
============================================================
```

Expected pass signals include:

```text
HE gateway API test PASSED
SMPC match test PASSED
SMPC no-match test PASSED
zk proof generation test PASSED
zk proof verification test PASSED
FATF REC10 proof compliance test PASSED
FATF REC11 proof compliance test PASSED
FATF REC16 proof compliance test PASSED
Phase 7.1 API end-to-end test PASSED
```

---

### 3.5 Phase 7.1 Evidence Verification

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

grep -R "PASSED" tests/evidence/phase7_1/*.log | sort

test -f tests/evidence/phase7_1/api_end_to_end_test.log
test -f tests/evidence/phase7_1/smpc_match_test.log
test -f tests/evidence/phase7_1/smpc_no_match_test.log
test -f tests/evidence/phase7_1/rec10_proof_test.log
test -f tests/evidence/phase7_1/rec11_proof_test.log
test -f tests/evidence/phase7_1/rec16_proof_test.log

echo "✅ Phase 7.1 functional validation evidence exists"
```

Expected output:

```text
✅ Phase 7.1 functional validation evidence exists
```

---

### 3.6 Generate Phase 7.1 Evidence Summary

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

./scripts/ci/phase71_evidence_summary.sh

sed -n '1,220p' tests/evidence/phase7_1/PHASE_7_1_FUNCTIONAL_EVIDENCE_SUMMARY.md
```

Expected file:

```text
tests/evidence/phase7_1/PHASE_7_1_FUNCTIONAL_EVIDENCE_SUMMARY.md
```

---

### 3.7 Phase 7.1 Troubleshooting Note: SEAL CMake Cache

If the HE/SEAL build fails with a CMake cache path mismatch, clean the generated build directory and rerun:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

rm -rf services/he-orchestrator/seal-core/build

./tests/integration/he_gateway_api_test.sh
```

This is safe because the `build/` directory is generated output.

---

## 4. Phase 7.2 — Performance Testing

### 4.1 Objective

Phase 7.2 validates performance using Locust.

Primary targets:

- Submit at least **1000 transactions**
- Maintain **0 transaction failures**
- Achieve at least **200 requests/second**, which is the equivalent throughput for 1000 transactions in 5 seconds
- Generate zk proofs with **0 failures**
- Keep zk proof generation **P95 latency below 100 ms**

---

### 4.2 Important Phase 7.2 Files

```text
scripts/demo/run-phase7-2-performance.sh
tests/performance/locustfile.py
tests/performance/transactions_load_test.py
tests/performance/proof_generation_load_test.py
tests/performance/phase72_generate_report.py
tests/performance/performance_targets.md
tests/performance/performance_results_template.md
tests/fixtures/performance_transactions.json
```

Evidence directory:

```text
tests/evidence/phase7_2/
```

---

### 4.3 Phase 7.2 Syntax and Python Checks

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

bash -n scripts/demo/run-phase7-2-performance.sh

python3 -m py_compile tests/performance/phase72_generate_report.py
python3 -m py_compile tests/performance/locustfile.py
python3 -m py_compile tests/performance/transactions_load_test.py
python3 -m py_compile tests/performance/proof_generation_load_test.py
```

Expected result: no syntax or compilation errors.

---

### 4.4 Run Phase 7.2 Performance Test

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

./scripts/demo/run-phase7-2-performance.sh all
```

Expected sections:

```text
============================================================
Phase 7.2 Transaction Throughput Benchmark
============================================================

============================================================
Phase 7.2 zk Proof Generation Benchmark
============================================================
```

Expected Locust evidence files:

```text
tests/evidence/phase7_2/transactions_stats.csv
tests/evidence/phase7_2/transactions_failures.csv
tests/evidence/phase7_2/transactions_report.html
tests/evidence/phase7_2/transactions_locust.log
tests/evidence/phase7_2/proofs_stats.csv
tests/evidence/phase7_2/proofs_failures.csv
tests/evidence/phase7_2/proofs_report.html
tests/evidence/phase7_2/proofs_locust.log
tests/evidence/phase7_2/PHASE_7_2_PERFORMANCE_RESULTS.md
```

---

### 4.5 View Phase 7.2 Report

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

sed -n '1,260p' tests/evidence/phase7_2/PHASE_7_2_PERFORMANCE_RESULTS.md
```

Expected result example:

```text
Request count: 13636
Failure count: 0
Requests per second: 466.11574037415073
Proof P95 response time: 96
```

---

### 4.6 Strict Phase 7.2 Verification Script

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

python3 - <<'PY'
import csv
from pathlib import Path

root = Path("tests/evidence/phase7_2")

def aggregated(prefix):
    path = root / f"{prefix}_stats.csv"
    if not path.exists():
        raise SystemExit(f"Missing {path}")

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        if row.get("Name") == "Aggregated":
            return row

    raise SystemExit(f"No Aggregated row found in {path}")

def as_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0

tx = aggregated("transactions")
proofs = aggregated("proofs")

tx_requests = as_float(tx.get("Request Count", 0))
tx_failures = as_float(tx.get("Failure Count", 0))
tx_rps = as_float(tx.get("Requests/s", 0))

proof_requests = as_float(proofs.get("Request Count", 0))
proof_failures = as_float(proofs.get("Failure Count", 0))
proof_p95 = as_float(proofs.get("95%", 0))

print("Phase 7.2 transaction requests:", tx_requests)
print("Phase 7.2 transaction failures:", tx_failures)
print("Phase 7.2 transaction RPS:", tx_rps)
print("Phase 7.2 proof requests:", proof_requests)
print("Phase 7.2 proof failures:", proof_failures)
print("Phase 7.2 proof P95 ms:", proof_p95)

assert tx_requests >= 1000, "Phase 7.2 transaction benchmark did not reach 1000 requests"
assert tx_failures == 0, "Phase 7.2 transaction benchmark has failures"
assert tx_rps >= 200, "Phase 7.2 transaction throughput is below 1000 tx / 5 sec equivalent"

assert proof_requests > 0, "Phase 7.2 proof benchmark did not run"
assert proof_failures == 0, "Phase 7.2 proof benchmark has failures"
assert proof_p95 < 100, "Phase 7.2 proof P95 latency is not under 100 ms"

print("✅ Phase 7.2 performance validation PASSED")
PY
```

Expected output:

```text
✅ Phase 7.2 performance validation PASSED
```

---

### 4.7 Phase 7.2 Interpretation Note

The generated Markdown report may show the transaction benchmark status as `REVIEW REQUIRED` if it uses wall-clock run duration, because Locust was configured to run for a longer fixed time window.

However, the strict pass criteria used by the final validator are:

```text
transaction_requests >= 1000
transaction_failures == 0
transaction_requests_per_second >= 200
proof_requests > 0
proof_failures == 0
proof_p95 < 100
```

If those assertions pass, Phase 7.2 is accepted for this project validation stage.

---

## 5. Phase 7.3 — Compliance Validation

### 5.1 Objective

Phase 7.3 validates compliance evidence aligned with:

- **Recommendation 10 (R.10)** — Customer Due Diligence
- **Recommendation 11 (R.11)** — Record Keeping
- **Recommendation 16 (R.16)** — Payment Transparency / Travel Rule

---

### 5.2 Important Phase 7.3 Files

```text
scripts/demo/run-phase7-3-compliance.sh
tests/compliance/lib_phase73.sh
tests/compliance/r10_cdd_validation.sh
tests/compliance/r11_recordkeeping_validation.sh
tests/compliance/r16_travelrule_validation.sh
tests/compliance/phase73_generate_report.py
tests/compliance/compliance_assertions.md
tests/compliance/compliance_results_template.md
```

Evidence directory:

```text
tests/evidence/phase7_3/
```

---

### 5.3 Phase 7.3 Syntax Checks

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

bash -n scripts/demo/run-phase7-3-compliance.sh
bash -n tests/compliance/lib_phase73.sh
bash -n tests/compliance/r10_cdd_validation.sh
bash -n tests/compliance/r11_recordkeeping_validation.sh
bash -n tests/compliance/r16_travelrule_validation.sh

python3 -m py_compile tests/compliance/phase73_generate_report.py
```

Expected result: no syntax or compilation errors.

---

### 5.4 Run Individual Phase 7.3 Validations

Run R.10:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

./tests/compliance/r10_cdd_validation.sh
```

Expected output:

```text
R.10 Customer Due Diligence validation PASSED
```

Run R.11:

```bash
./tests/compliance/r11_recordkeeping_validation.sh
```

Expected output:

```text
R.11 Record Keeping validation PASSED
```

Run R.16:

```bash
./tests/compliance/r16_travelrule_validation.sh
```

Expected output:

```text
R.16 Payment Transparency / Travel Rule validation PASSED
```

---

### 5.5 Run Full Phase 7.3 Compliance Wrapper

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

./scripts/demo/run-phase7-3-compliance.sh all
```

Expected output:

```text
R.10 Customer Due Diligence validation PASSED
R.11 Record Keeping validation PASSED
R.16 Payment Transparency / Travel Rule validation PASSED
Wrote tests/evidence/phase7_3/PHASE_7_3_COMPLIANCE_RESULTS.md
```

---

### 5.6 Verify Phase 7.3 Report

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

sed -n '1,260p' tests/evidence/phase7_3/PHASE_7_3_COMPLIANCE_RESULTS.md
```

Expected result:

```text
## Overall Status

`PASSED`
```

---

### 5.7 Verify Phase 7.3 Proof Responses

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

grep -q 'Overall Status' tests/evidence/phase7_3/PHASE_7_3_COMPLIANCE_RESULTS.md
grep -q '`PASSED`' tests/evidence/phase7_3/PHASE_7_3_COMPLIANCE_RESULTS.md

test -f tests/evidence/phase7_3/TX-PHASE73-R10-001_r10_verify_response.json
test -f tests/evidence/phase7_3/TX-PHASE73-R11-001_r11_verify_response.json
test -f tests/evidence/phase7_3/TX-PHASE73-R16-001_r16_verify_response.json

jq -e '.verified == true' tests/evidence/phase7_3/TX-PHASE73-R10-001_r10_verify_response.json
jq -e '.verified == true' tests/evidence/phase7_3/TX-PHASE73-R11-001_r11_verify_response.json
jq -e '.verified == true' tests/evidence/phase7_3/TX-PHASE73-R16-001_r16_verify_response.json

echo "✅ Phase 7.3 compliance validation PASSED"
```

Expected output:

```text
true
true
true
✅ Phase 7.3 compliance validation PASSED
```

---

## 6. Final Phase 7 Completion Verification

### 6.1 Final Verification Script

The final gate script is:

```text
scripts/ci/verify-phase7-completion.sh
```

Run:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

./scripts/ci/verify-phase7-completion.sh
```

Expected output:

```text
============================================================
PHASE 7 COMPLETION VERIFICATION
============================================================

Checking Phase 7.1 evidence...
✅ Phase 7.1 evidence found

Checking Phase 7.2 performance evidence...
✅ Phase 7.2 performance evidence passed

Checking Phase 7.3 compliance evidence...
✅ Phase 7.3 compliance evidence passed

============================================================
✅ PHASE 7.1, 7.2, AND 7.3 ARE COMPLETE
============================================================
```

---

## 7. Final Git Commands After Testing

From the real Git root:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git status -sb
```

If only the three evidence summaries changed, stage and commit them:

```bash
git add aml-system/tests/evidence/phase7_1/PHASE_7_1_FUNCTIONAL_EVIDENCE_SUMMARY.md
git add aml-system/tests/evidence/phase7_2/PHASE_7_2_PERFORMANCE_RESULTS.md
git add aml-system/tests/evidence/phase7_3/PHASE_7_3_COMPLIANCE_RESULTS.md

git commit -m "Update Phase 7 validation evidence summaries"

git push origin main
```

Then verify remote sync:

```bash
git fetch origin --prune

git rev-list --left-right --count HEAD...origin/main

git status -sb
```

Expected:

```text
0	0
## main...origin/main
```

---

## 8. Files That Should Usually Stay Ignored

Generated raw evidence should normally remain ignored unless required by the supervisor:

```text
tests/evidence/**/*.log
tests/evidence/**/*.json
tests/evidence/**/*.csv
tests/evidence/**/*.html
tests/evidence/**/*.txt
tests/**/*.bak.*
```

Recommended committed evidence:

```text
tests/evidence/phase7_1/PHASE_7_1_FUNCTIONAL_EVIDENCE_SUMMARY.md
tests/evidence/phase7_2/PHASE_7_2_PERFORMANCE_RESULTS.md
tests/evidence/phase7_3/PHASE_7_3_COMPLIANCE_RESULTS.md
```

---

## 9. Final Phase 7 Completion Statement

Phase 7 is complete when the following are true:

1. Phase 7.1 evidence logs exist and contain functional `PASSED` markers.
2. Phase 7.2 Locust output confirms:
   - transaction request count is at least 1000,
   - transaction failures are zero,
   - transaction throughput is at least 200 requests/second,
   - proof request count is greater than zero,
   - proof failures are zero,
   - proof P95 latency is below 100 ms.
3. Phase 7.3 report shows:
   - R.10 passed,
   - R.11 passed,
   - R.16 passed,
   - overall compliance status is `PASSED`.
4. `scripts/ci/verify-phase7-completion.sh` prints:

```text
✅ PHASE 7.1, 7.2, AND 7.3 ARE COMPLETE
```

At that point, the project is ready to proceed to the next phase.
