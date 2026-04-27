# Frontend Phase FE3 — Evidence Dashboard and Performance Visualization

## Objective

Present Phase 7 evidence inside the browser instead of relying on terminal logs.

## Target Directory

```text
aml-system/services/regulator-api/frontend/
```

## Evidence Sources

```text
tests/evidence/phase7_1/PHASE_7_1_FUNCTIONAL_EVIDENCE_SUMMARY.md
tests/evidence/phase7_2/PHASE_7_2_PERFORMANCE_RESULTS.md
tests/evidence/phase7_3/PHASE_7_3_COMPLIANCE_RESULTS.md
```

## Files and Directories

```text
src/types/evidence.ts
src/data/phase7Evidence.ts
src/components/dashboard/PhaseStatusCard.tsx
src/components/dashboard/ComplianceSummaryCards.tsx
src/components/performance/ThroughputCard.tsx
src/components/performance/LatencyCard.tsx
src/components/performance/LatencyBarChart.tsx
src/components/performance/PerformanceSummary.tsx
src/components/evidence/EvidenceLinkList.tsx
src/pages/DashboardPage.tsx
src/pages/PerformancePage.tsx
```

## Step 1 — Create Directories

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system/services/regulator-api/frontend

mkdir -p src/data src/types src/components/dashboard src/components/performance src/components/evidence
```

## Step 2 — Create Evidence Types

```bash
cat > src/types/evidence.ts <<'EOF'
export type PhaseStatus = "PASSED" | "REVIEW_REQUIRED" | "PENDING";

export type PerformanceEvidence = {
  transactionRequestCount: number;
  transactionFailureCount: number;
  transactionRequestsPerSecond: number;
  proofRequestCount: number;
  proofFailureCount: number;
  proofMedianMs: number;
  proofP95Ms: number;
  proofP99Ms: number;
};

export type ComplianceStatus = {
  recommendation: string;
  title: string;
  status: PhaseStatus;
  description: string;
};
EOF
```

## Step 3 — Create Static Evidence Data

```bash
cat > src/data/phase7Evidence.ts <<'EOF'
import type { ComplianceStatus, PerformanceEvidence } from "../types/evidence";

export const phaseStatus = [
  {
    phase: "Phase 7.1",
    title: "Functional Testing",
    status: "PASSED",
    description: "HE, SMPC, zk proof generation, and end-to-end API flow validated.",
  },
  {
    phase: "Phase 7.2",
    title: "Performance Testing",
    status: "PASSED",
    description: "Transaction throughput and zk proof latency passed strict validation.",
  },
  {
    phase: "Phase 7.3",
    title: "Compliance Validation",
    status: "PASSED",
    description: "FATF Recommendation 10, 11, and 16 evidence validated.",
  },
] as const;

export const complianceEvidence: ComplianceStatus[] = [
  {
    recommendation: "R.10",
    title: "Customer Due Diligence",
    status: "PASSED",
    description: "CDD-aligned proof and audit evidence verified.",
  },
  {
    recommendation: "R.11",
    title: "Record Keeping",
    status: "PASSED",
    description: "Transaction, proof, and audit linkage is reconstructable.",
  },
  {
    recommendation: "R.16",
    title: "Payment Transparency / Travel Rule",
    status: "PASSED",
    description: "Payment metadata presence evidence verified.",
  },
];

export const performanceEvidence: PerformanceEvidence = {
  transactionRequestCount: 10091,
  transactionFailureCount: 0,
  transactionRequestsPerSecond: 339.92353492474865,
  proofRequestCount: 628,
  proofFailureCount: 0,
  proofMedianMs: 46,
  proofP95Ms: 58,
  proofP99Ms: 66,
};
EOF
```

## Step 4 — Components to Build

Create these components:

```text
PhaseStatusCard.tsx
ComplianceSummaryCards.tsx
ThroughputCard.tsx
LatencyCard.tsx
LatencyBarChart.tsx
PerformanceSummary.tsx
EvidenceLinkList.tsx
```

Functional expectations:

```text
PhaseStatusCard shows Phase 7.1/7.2/7.3 status.
ComplianceSummaryCards shows R.10/R.11/R.16 status.
ThroughputCard shows req/s and implied 1000 tx time.
LatencyCard shows median/P95/P99 proof latency.
LatencyBarChart visualizes latency percentiles.
EvidenceLinkList lists evidence summary paths.
```

## Step 5 — Replace Dashboard and Performance Pages

Update:

```text
src/pages/DashboardPage.tsx
src/pages/PerformancePage.tsx
```

Expected UI:

```text
/dashboard shows phase status and compliance cards.
/performance shows throughput, latency, and chart.
```

## Acceptance Criteria

```text
Dashboard shows Phase 7.1, 7.2, and 7.3 status.
Dashboard shows R.10, R.11, and R.16 status.
Performance page shows transaction throughput.
Performance page shows proof latency P95 below 100 ms.
Evidence file references are visible.
```

## Build and Commit

```bash
npm run build

cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git add aml-system/services/regulator-api/frontend/src

git commit -m "Add frontend evidence dashboard and performance visualization"

git push origin main
```
