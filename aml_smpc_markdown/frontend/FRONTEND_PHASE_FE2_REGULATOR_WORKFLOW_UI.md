# Frontend Phase FE2 — Regulator Workflow UI

## Objective

Build the interactive regulator workflow:

```text
list proofs -> view proof details -> verify proof -> inspect audit timeline
```

## Backend Endpoints

```text
GET  /proofs?tx_id=...
GET  /proofs/{proof_id}
POST /proofs/{proof_id}/verify
GET  /audit/{tx_id}
```

## Target Directory

```text
aml-system/services/regulator-api/frontend/
```

## Files and Directories

```text
src/api/proofsApi.ts
src/api/auditApi.ts
src/types/proof.ts
src/types/audit.ts
src/components/proofs/ProofSearchForm.tsx
src/components/proofs/ProofsTable.tsx
src/components/proofs/ProofDetailPanel.tsx
src/components/proofs/VerifyProofButton.tsx
src/components/audit/AuditSearchForm.tsx
src/components/audit/AuditTimeline.tsx
src/components/audit/AuditEventCard.tsx
src/pages/ProofsPage.tsx
src/pages/ProofDetailPage.tsx
src/pages/AuditPage.tsx
```

## Step 1 — Start from Frontend Directory

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system/services/regulator-api/frontend

mkdir -p src/api src/types src/components/proofs src/components/audit
```

## Step 2 — Create Types

```bash
cat > src/types/proof.ts <<'EOF'
export type ProofRow = {
  id: string;
  tx_id: string;
  rule_id: string;
  claim_hash?: string;
  public_signal: boolean;
  verification_status: string;
  created_at?: string;
};

export type ProofDetail = ProofRow & {
  proof_blob?: Record<string, unknown>;
};

export type VerifyProofResponse = {
  proof_id: string;
  tx_id: string;
  rule_id: string;
  verified: boolean;
  reason: string;
};
EOF

cat > src/types/audit.ts <<'EOF'
export type AuditEvent = {
  id?: string;
  tx_id?: string;
  event_type: string;
  event_status: string;
  event_ref?: string | null;
  details?: Record<string, unknown>;
  created_at?: string;
};
EOF
```

## Step 3 — Create API Wrappers

```bash
cat > src/api/proofsApi.ts <<'EOF'
import { apiClient } from "./client";
import { env } from "../config/env";
import type { ProofDetail, ProofRow, VerifyProofResponse } from "../types/proof";

const baseUrl = env.regulatorApiBaseUrl;

export const proofsApi = {
  listByTransaction(txId: string) {
    return apiClient.get<ProofRow[]>(`${baseUrl}/proofs?tx_id=${encodeURIComponent(txId)}`);
  },

  getProof(proofId: string) {
    return apiClient.get<ProofDetail>(`${baseUrl}/proofs/${encodeURIComponent(proofId)}`);
  },

  verifyProof(proofId: string) {
    return apiClient.post<VerifyProofResponse>(`${baseUrl}/proofs/${encodeURIComponent(proofId)}/verify`);
  },
};
EOF

cat > src/api/auditApi.ts <<'EOF'
import { apiClient } from "./client";
import { env } from "../config/env";
import type { AuditEvent } from "../types/audit";

const baseUrl = env.regulatorApiBaseUrl;

export const auditApi = {
  listByTransaction(txId: string) {
    return apiClient.get<AuditEvent[]>(`${baseUrl}/audit/${encodeURIComponent(txId)}`);
  },
};
EOF
```

## Step 4 — Create Regulator Components

Create these files with UI logic:

```text
src/components/proofs/ProofSearchForm.tsx
src/components/proofs/ProofsTable.tsx
src/components/proofs/ProofDetailPanel.tsx
src/components/proofs/VerifyProofButton.tsx
src/components/audit/AuditSearchForm.tsx
src/components/audit/AuditTimeline.tsx
src/components/audit/AuditEventCard.tsx
```

Recommended component responsibilities:

```text
ProofSearchForm.tsx      -> tx_id input and search button
ProofsTable.tsx          -> proof list with View and Verify actions
ProofDetailPanel.tsx     -> read-only safe proof metadata
VerifyProofButton.tsx    -> displays verification response
AuditSearchForm.tsx      -> tx_id input for audit lookup
AuditTimeline.tsx        -> ordered audit events
AuditEventCard.tsx       -> event_type, event_status, created_at, collapsed details
```

## Step 5 — Replace Pages

Update:

```text
src/pages/ProofsPage.tsx
src/pages/AuditPage.tsx
```

Expected page behavior:

```text
/proofs searches by transaction ID.
/proofs displays proof rows.
/proofs can verify selected proof.
/audit searches by transaction ID.
/audit shows timeline events.
```

## Step 6 — Build and Run

```bash
npm run build
npm run dev -- --host 127.0.0.1 --port 5173
```

## Acceptance Criteria

```text
Regulator can search proofs by tx_id.
Regulator can view safe proof metadata.
Regulator can verify selected proof.
Regulator can view audit timeline.
UI shows clear errors.
UI does not expose raw customer identifiers.
```

## Git Commands

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git add aml-system/services/regulator-api/frontend/src

git commit -m "Add regulator proof and audit workflow UI"

git push origin main
```
