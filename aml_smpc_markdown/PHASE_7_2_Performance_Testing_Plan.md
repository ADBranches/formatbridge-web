# PHASE 7.2 — Performance Testing Plan (Locust) (Planning‑Only)

> **Status:** Planning & validation definition only (no benchmarking code populated yet)
>
> **Purpose:** Define the exact performance targets, endpoints, datasets, test files to create, and evidence to capture for the project report.

---

## Scope (Phase 7.2)
This phase measures **throughput and latency** of the already-built system using **Locust**.

### Target benchmarks (project KPIs)
1. **1000 transactions < 5 seconds** (end‑to‑end submission throughput)
2. **zk proof generation < 100 ms** (per proof generation latency target)

---

## What will be benchmarked (micro‑level)

### A) Transaction submission throughput
**What is measured:**
- Requests/second and total time to submit **1000 valid transactions**.
- Error rate (HTTP failures, timeouts).
- Latency percentiles (P50, P95, P99).

**Primary endpoint(s) under load:**
- `POST /transactions/submit` (encryption-service)

**Supporting endpoints (optional):**
- `POST /he/encrypt` (he-gateway) — only if your submission flow triggers HE.
- `POST /smpc/screen` (smpc-runtime) — only if your submission triggers screening.

---

### B) zk Proof generation latency
**What is measured:**
- Per-request proof generation time (ms).
- Latency distribution (P50/P95/P99).
- System behavior under concurrent requests.

**Primary endpoint(s) under load:**
- `POST /proofs/generate` (zk-prover)

**Optional regulator workflow under load (not required for the KPI):**
- `GET /proofs?tx_id=...` (regulator-api)
- `POST /proofs/:proof_id/verify` (regulator-api)

---

## Existing files involved (already implemented)
These are the files that the Phase 7.2 load tests exercise indirectly via HTTP:

### Services under test
```
services/encryption-service/api/src/routes.rs
services/zk-prover/prover/src/routes.rs
services/regulator-api/backend/src/routes.rs
```

### Deployment/ops context used for measurement and evidence
```
infra/monitoring/prometheus/prometheus.yml
infra/monitoring/prometheus/alerts.yml
infra/monitoring/loki/loki-config.yml
infra/monitoring/dashboards/service-latency.json
infra/monitoring/dashboards/proof-throughput.json
infra/monitoring/dashboards/cpu-usage.json
```

---

## New files to create for Phase 7.2 (later)
> These are **new test assets** you will create *during* Phase 7.2 implementation.

### Locust workloads
```
tests/performance/locustfile.py
tests/performance/transactions_load_test.py
tests/performance/proof_generation_load_test.py
```

### Targets, evidence templates, and datasets
```
tests/performance/performance_targets.md
tests/performance/performance_results_template.md
tests/fixtures/performance_transactions.json
```

### Optional (recommended) automation wrapper
```
scripts/demo/run-phase7-2-performance.sh
```

---

## Responsibilities (file-by-file)

### `tests/performance/locustfile.py`
- Entry point that selects which scenario to run (transactions vs proofs).

### `tests/performance/transactions_load_test.py`
- Defines user behavior for submitting transactions.
- Uses `tests/fixtures/performance_transactions.json` to generate payloads.

### `tests/performance/proof_generation_load_test.py`
- Defines user behavior for proof generation.
- Uses an existing `tx_id` set (seeded before test) or creates tx_ids on the fly.

### `tests/performance/performance_targets.md`
- Explicit benchmark contract:
  - transaction throughput requirement
  - proof latency requirement
  - acceptable error rate
  - test hardware assumptions

### `tests/performance/performance_results_template.md`
- Standardized reporting format:
  - Locust config used
  - concurrency/users/spawn rate
  - total requests
  - P50/P95/P99 latencies
  - throughput achieved
  - screenshots/log excerpts
  - notes/observations

### `tests/fixtures/performance_transactions.json`
- Canonical 1000-transaction dataset (synthetic) for repeatability.

### `scripts/demo/run-phase7-2-performance.sh` (optional)
- Automation-first wrapper:
  - starts required services (or confirms k3s deploy is up)
  - seeds DB with initial data
  - runs Locust headless
  - exports results to `docs/research/phase7-results.md`

---

## Evidence to capture (what “passed” looks like)

### Minimum evidence (required)
- Locust run output showing:
  - **1000 successful transaction submissions**
  - total time **< 5 seconds**
- Locust latency output showing:
  - proof generation requests meet **< 100 ms** target (define whether P50 or P95)

### Recommended evidence (stronger)
- Prometheus screenshots for:
  - CPU usage during load
  - request latency (if /metrics is instrumented)
- Loki log queries showing:
  - service stability (no crashes)
  - no high error bursts

---

## Phase 7.2 Exit Criteria
Phase 7.2 is **passed** once:
- the transaction load test meets the 1000 tx / 5s benchmark,
- the proof generation latency target is measured and reported,
- and results are documented using the results template.

> **Note:** Implementation (Locust scripts + datasets + evidence capture) happens after this planning definition.
