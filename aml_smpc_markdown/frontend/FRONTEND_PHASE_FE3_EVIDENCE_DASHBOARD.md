# Frontend Build Timeline — Phase FE3 (Evidence Dashboard & Performance Visualization)

**Goal:** Present Phase 7 evidence as UI, not terminal logs.

## Data sources
- `tests/evidence/phase7_2/PHASE_7_2_PERFORMANCE_RESULTS.md`
- `tests/evidence/phase7_3/PHASE_7_3_COMPLIANCE_RESULTS.md`

> For the UI, you have two options:
> 1) **Serve evidence via backend endpoint** (recommended)
> 2) **Bundle static evidence files** into frontend (acceptable for offline demo)

## Recommended approach (best UX)
### A) Add an Evidence API (light)
Add a small endpoint in regulator-api (backend) to expose *sanitized evidence summaries*:
- `GET /evidence/phase7/performance` → parsed JSON summary
- `GET /evidence/phase7/compliance` → parsed JSON summary

### B) Evidence UI Pages
#### 1) Performance Page — `/performance`
- Cards:
  - Transaction throughput (req/s)
  - Implied time for 1000 tx (seconds)
  - Proof latency (median/P95/P99)
- Charts:
  - simple bar chart for latency percentiles
  - optionally, small time-series chart if you store multiple runs

#### 2) Compliance Page — `/dashboard`
- Summary chips:
  - R.10 status
  - R.11 status
  - R.16 status
- Evidence links:
  - “Open evidence JSON”
  - “Download evidence md/pdf” (optional)

## Acceptance criteria
- Evidence pages load without terminal commands.
- UI displays PASS/FAIL clearly.
- Evidence is privacy-safe (synthetic only).

## Evidence to capture
- Screenshots:
  - performance dashboard
  - compliance dashboard
