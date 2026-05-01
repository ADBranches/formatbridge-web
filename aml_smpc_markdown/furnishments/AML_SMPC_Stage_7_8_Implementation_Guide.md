# AML SMPC Stage 7 + Stage 8 Implementation Guide

## Current Status Before Starting

The previous stage passed based on the latest runtime evidence:

- Regulator anomaly case was created from SMPC-linked suspicious evidence.
- Bank anomaly notice was visible to the reviewer.
- Bank reviewer successfully responded to the notice.
- Transaction submitter was blocked from anomaly notices with HTTP 403.
- Stage 5/6 commit was pushed to `origin/bank-rbac-suspicion-case-workflow`.

Latest pushed commit:

```text
47566a7 Add regulator anomaly case workflow and bank dashboard notices
```

Stage 7 and Stage 8 should now make the regulator side presentation-ready and add one resettable demo seeder.

---

# Stage 7 — Regulator Dashboard Furnishment

## Objective

Make the regulator dashboard show the full evidence governance story.

The dashboard should summarize:

```text
verified proofs
pending proof reviews
high-risk cases
open anomaly cases
closed anomaly cases
FATF R.10 evidence
FATF R.11 evidence
FATF R.16 evidence
```

Regulator should also have clear navigation to:

```text
/regulator/proofs
/regulator/audit
/regulator/compliance-report
/regulator/three-bank-smpc-demo
/regulator/anomaly-cases
```

---

## 7.1 Confirm current branch

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git fetch origin --prune
git status -sb
git branch --show-current
git log --oneline --decorate -5
```

Expected:

```text
bank-rbac-suspicion-case-workflow
```

---

## 7.2 Create regulator dashboard API client

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

cat > services/regulator-api/frontend/src/api/regulatorDashboardApi.ts <<'EOF'
import { ApiError } from "./client";
import { env } from "../config/env";
import { getStoredSession } from "../auth/authStore";
import { anomalyCasesApi, type AnomalyCase } from "./anomalyCasesApi";

export type ProofEvidence = {
  id?: string;
  tx_id?: string;
  rule_id?: string;
  verification_status?: string;
  public_signal?: boolean;
  claim_hash?: string;
  proof_blob?: Record<string, unknown>;
};

export type RegulatorDashboardSummary = {
  proofs: ProofEvidence[];
  cases: AnomalyCase[];
  verifiedProofs: number;
  pendingProofReviews: number;
  highRiskCases: number;
  openAnomalyCases: number;
  closedAnomalyCases: number;
  fatfRec10Evidence: number;
  fatfRec11Evidence: number;
  fatfRec16Evidence: number;
};

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const session = getStoredSession();
  const headers = new Headers(init.headers);

  headers.set("Content-Type", "application/json");

  if (session?.token) {
    headers.set("Authorization", `Bearer ${session.token}`);
  }

  const response = await fetch(`${env.regulatorApiBaseUrl}${path}`, {
    ...init,
    headers,
  });

  const text = await response.text();
  const payload = text ? JSON.parse(text) : null;

  if (!response.ok) {
    const message =
      payload?.message ||
      payload?.error ||
      `Request failed with HTTP ${response.status}`;

    throw new ApiError(response.status, message, payload);
  }

  return payload as T;
}

export const regulatorDashboardApi = {
  async summary(): Promise<RegulatorDashboardSummary> {
    const [proofs, cases] = await Promise.all([
      request<ProofEvidence[]>("/proofs").catch(() => []),
      anomalyCasesApi.listCases().catch(() => []),
    ]);

    const verifiedProofs = proofs.filter(
      (proof) => proof.verification_status === "verified"
    ).length;

    const pendingProofReviews = proofs.filter(
      (proof) =>
        !proof.verification_status ||
        proof.verification_status === "pending" ||
        proof.verification_status === "unverified"
    ).length;

    const highRiskCases = cases.filter((item) => item.risk_level === "high").length;
    const openAnomalyCases = cases.filter((item) => item.case_status !== "closed").length;
    const closedAnomalyCases = cases.filter((item) => item.case_status === "closed").length;
    const fatfRec10Evidence = proofs.filter((proof) => proof.rule_id === "FATF_REC10").length;
    const fatfRec11Evidence = proofs.filter((proof) => proof.rule_id === "FATF_REC11").length;
    const fatfRec16Evidence = proofs.filter((proof) => proof.rule_id === "FATF_REC16").length;

    return {
      proofs,
      cases,
      verifiedProofs,
      pendingProofReviews,
      highRiskCases,
      openAnomalyCases,
      closedAnomalyCases,
      fatfRec10Evidence,
      fatfRec11Evidence,
      fatfRec16Evidence,
    };
  },
};
EOF
```

---

## 7.3 Replace regulator dashboard page

```bash
cat > services/regulator-api/frontend/src/pages/regulator/RegulatorDashboardPage.tsx <<'EOF'
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  regulatorDashboardApi,
  type RegulatorDashboardSummary,
} from "../../api/regulatorDashboardApi";
import { Card } from "../../components/ui/Card";
import { ErrorBanner } from "../../components/ui/ErrorBanner";
import { LoadingState } from "../../components/ui/LoadingState";
import { PageHeader } from "../../components/ui/PageHeader";
import { StatusBadge } from "../../components/ui/StatusBadge";

const initialSummary: RegulatorDashboardSummary = {
  proofs: [],
  cases: [],
  verifiedProofs: 0,
  pendingProofReviews: 0,
  highRiskCases: 0,
  openAnomalyCases: 0,
  closedAnomalyCases: 0,
  fatfRec10Evidence: 0,
  fatfRec11Evidence: 0,
  fatfRec16Evidence: 0,
};

export function RegulatorDashboardPage() {
  const [summary, setSummary] = useState<RegulatorDashboardSummary>(initialSummary);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");

    try {
      setSummary(await regulatorDashboardApi.summary());
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load regulator dashboard summary."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Regulator Evidence Governance Dashboard"
        description="Regulator view of proofs, audit-facing evidence, compliance coverage, SMPC collaboration, and anomaly case governance without raw bank input exposure."
      />

      {loading ? <LoadingState /> : null}
      {error ? <ErrorBanner message={error} /> : null}

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Verified Proofs" value={summary.verifiedProofs} to="/regulator/proofs" />
        <MetricCard label="Pending Proof Reviews" value={summary.pendingProofReviews} to="/regulator/proofs" />
        <MetricCard label="High-Risk Cases" value={summary.highRiskCases} to="/regulator/anomaly-cases" />
        <MetricCard label="Open Anomaly Cases" value={summary.openAnomalyCases} to="/regulator/anomaly-cases" />
        <MetricCard label="Closed Anomaly Cases" value={summary.closedAnomalyCases} to="/regulator/anomaly-cases" />
        <MetricCard label="FATF R.10 Evidence" value={summary.fatfRec10Evidence} to="/regulator/compliance-report" />
        <MetricCard label="FATF R.11 Evidence" value={summary.fatfRec11Evidence} to="/regulator/compliance-report" />
        <MetricCard label="FATF R.16 Evidence" value={summary.fatfRec16Evidence} to="/regulator/compliance-report" />
      </section>

      <section className="grid gap-6 xl:grid-cols-2">
        <Card>
          <div className="flex items-center justify-between gap-3">
            <h3 className="font-bold">Evidence Governance Routes</h3>
            <button onClick={load} className="rounded-xl border px-4 py-2 text-sm font-semibold">
              Refresh
            </button>
          </div>

          <div className="mt-5 grid gap-3 md:grid-cols-2">
            <RouteCard title="Proof Verification" to="/regulator/proofs" />
            <RouteCard title="Audit Evidence" to="/regulator/audit" />
            <RouteCard title="Compliance Report" to="/regulator/compliance-report" />
            <RouteCard title="Three-Bank SMPC Demo" to="/regulator/three-bank-smpc-demo" />
            <RouteCard title="Anomaly Cases" to="/regulator/anomaly-cases" />
          </div>
        </Card>

        <Card>
          <h3 className="font-bold">Privacy Boundary</h3>
          <div className="mt-4 rounded-2xl border bg-slate-50 p-4 text-sm leading-6 text-slate-700">
            The regulator sees proof status, risk level, case references, FATF evidence coverage,
            audit summaries, and aggregate SMPC evidence. The regulator does not receive raw
            customer account data from other banks.
          </div>

          <div className="mt-4 grid gap-3">
            <EvidenceFact label="Raw bank inputs disclosed" value="false" />
            <EvidenceFact label="Bank identifies suspicion first" value="true" />
            <EvidenceFact label="Regulator verifies evidence" value="true" />
            <EvidenceFact label="Banks receive scoped feedback" value="true" />
          </div>
        </Card>
      </section>

      <Card>
        <h3 className="font-bold">Recent Anomaly Cases</h3>

        <div className="mt-5 overflow-x-auto rounded-2xl border">
          <table className="min-w-[900px] w-full text-left text-sm">
            <thead className="bg-slate-100 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-4 py-3">Case</th>
                <th className="px-4 py-3">Transaction</th>
                <th className="px-4 py-3">Risk</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Banks Notified</th>
                <th className="px-4 py-3">Action</th>
              </tr>
            </thead>

            <tbody>
              {summary.cases.slice(0, 8).map((item) => (
                <tr key={item.id} className="border-t align-top">
                  <td className="px-4 py-3">
                    <div className="font-mono text-xs font-bold">{item.case_ref}</div>
                    <div className="mt-1 text-xs text-slate-500">{item.summary}</div>
                  </td>
                  <td className="px-4 py-3 font-mono text-xs">{item.tx_id}</td>
                  <td className="px-4 py-3"><StatusBadge status={item.risk_level} /></td>
                  <td className="px-4 py-3"><StatusBadge status={item.case_status} /></td>
                  <td className="px-4 py-3">{item.bank_notices.length}</td>
                  <td className="px-4 py-3">
                    <Link
                      to={`/regulator/anomaly-cases/${item.id}`}
                      className="rounded-xl bg-slate-950 px-3 py-2 text-xs font-semibold text-white"
                    >
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {summary.cases.length === 0 ? (
          <div className="mt-5 rounded-xl border border-dashed p-6 text-sm text-slate-500">
            No anomaly cases yet. Open a case from `/regulator/anomaly-cases`.
          </div>
        ) : null}
      </Card>
    </div>
  );
}

function MetricCard({ label, value, to }: { label: string; value: number; to: string }) {
  return (
    <Card>
      <p className="text-xs font-bold uppercase text-slate-500">{label}</p>
      <h3 className="mt-2 text-3xl font-black">{value}</h3>
      <Link to={to} className="mt-3 inline-block text-xs font-semibold text-slate-700">
        Open
      </Link>
    </Card>
  );
}

function RouteCard({ title, to }: { title: string; to: string }) {
  return (
    <Link to={to} className="rounded-2xl border p-4 text-sm font-bold hover:bg-slate-50">
      {title}
    </Link>
  );
}

function EvidenceFact({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between rounded-xl border p-3 text-sm">
      <span className="font-semibold text-slate-600">{label}</span>
      <span className="font-mono text-xs font-bold">{value}</span>
    </div>
  );
}
EOF
```

---

# Stage 8 — Seeder and Demo Data

## Objective

Seed partner banks, users, AML rules, transactions, and anomaly case demo data for presentation.

The script should be safe to run repeatedly.

---

## 8.1 Create seeder script

```bash
mkdir -p scripts/dev

cat > scripts/dev/seed_bank_rbac_case_demo.py <<'EOF'
#!/usr/bin/env python3
"""
Seed AML SMPC partner-bank RBAC, suspicious transaction, SMPC, and anomaly-case demo data.

Run from aml-system:

    python3 scripts/dev/seed_bank_rbac_case_demo.py

Requires regulator API running on http://127.0.0.1:8085.
"""

from __future__ import annotations

import json
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

API_BASE = "http://127.0.0.1:8085"
PASSWORD = "StrongPass123"
SUPER_EMAIL = "super.admin@aml-smpc.local"
SUPER_PASSWORD = "SuperAdmin123"

@dataclass
class DemoUser:
    full_name: str
    email: str
    partner_bank_code: str
    bank_employee_id: str
    department: str
    job_title: str
    requested_role: str
    reason_for_access: str

DEMO_USERS = [
    DemoUser("Bank A Admin", "bank.a.admin@example.com", "BANK_A_UG", "BANKA-ADMIN-001", "Compliance", "Institution AML Administrator", "institution_admin", "Administers AML SMPC workflows for Bank A."),
    DemoUser("Bank A Submitter", "bank.a.submitter@example.com", "BANK_A_UG", "BANKA-SUB-001", "Operations", "Transaction Submitter", "transaction_submitter", "Submits AML transaction payloads for Bank A."),
    DemoUser("Bank A Reviewer", "bank.a.reviewer@example.com", "BANK_A_UG", "BANKA-REV-001", "Compliance", "AML Transaction Reviewer", "transaction_reviewer", "Reviews AML risk and SMPC screening outputs for Bank A."),
    DemoUser("Bank B Reviewer", "bank.b.reviewer@example.com", "BANK_B_KE", "BANKB-REV-001", "Compliance", "AML Transaction Reviewer", "transaction_reviewer", "Reviews AML risk and SMPC screening outputs for Bank B."),
    DemoUser("Bank C Reviewer", "bank.c.reviewer@example.com", "BANK_C_TZ", "BANKC-REV-001", "Compliance", "AML Transaction Reviewer", "transaction_reviewer", "Reviews AML risk and SMPC screening outputs for Bank C."),
]

def request(method: str, path: str, payload: dict[str, Any] | None = None, token: str | None = None) -> tuple[int, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{API_BASE}{path}", data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else None
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8")
        try:
            return err.code, json.loads(body)
        except json.JSONDecodeError:
            return err.code, body

def login(email: str, password: str) -> tuple[str, dict[str, Any]]:
    status, payload = request("POST", "/auth/login", {"email": email, "password": password})
    if status != 200:
        raise RuntimeError(f"Login failed for {email}: {status} {payload}")
    return payload["token"], payload

def database_url() -> str:
    for line in Path(".env").read_text().splitlines():
        if line.startswith("DATABASE_URL="):
            return line.split("=", 1)[1]
    raise RuntimeError("DATABASE_URL not found in .env")

def psql(sql: str) -> str:
    result = subprocess.run(["psql", database_url(), "-Atc", sql], check=True, text=True, capture_output=True)
    return result.stdout.strip()

def apply_migration(path: str) -> None:
    file_path = Path(path)
    if file_path.exists():
        subprocess.run(["psql", database_url(), "-v", "ON_ERROR_STOP=1", "-f", str(file_path)], check=True)

def register_and_approve_users(super_token: str) -> None:
    for user in DEMO_USERS:
        status, payload = request("POST", "/auth/register", {
            "full_name": user.full_name,
            "email": user.email,
            "password": PASSWORD,
            "partner_bank_code": user.partner_bank_code,
            "bank_employee_id": user.bank_employee_id,
            "department": user.department,
            "job_title": user.job_title,
            "requested_role": user.requested_role,
            "reason_for_access": user.reason_for_access,
        })
        if status in (200, 201):
            print(f"✅ Registered {user.email}")
        elif status == 409:
            print(f"ℹ️  User already exists: {user.email}")
        else:
            print(f"⚠️  Registration issue for {user.email}: {status} {payload}")

    status, pending = request("GET", "/admin/users/pending", token=super_token)
    if status != 200:
        print(f"⚠️ Could not list pending users: {status} {pending}")
        return
    target_roles = {user.email: user.requested_role for user in DEMO_USERS}
    for row in pending:
        email = row.get("email")
        if email not in target_roles:
            continue
        status, payload = request("POST", f"/admin/users/{row['user_id']}/approve", {"assigned_role": target_roles[email]}, token=super_token)
        if status in (200, 201):
            print(f"✅ Approved {email} as {target_roles[email]}")
        else:
            print(f"⚠️ Approval issue for {email}: {status} {payload}")

def create_transaction(token: str, tx_id: str, amount: int, overlap: int, screening_indicator: str) -> None:
    payload = {
        "tx_id": tx_id,
        "sender_id": f"SENDER-{tx_id}",
        "receiver_id": f"RECEIVER-{tx_id}",
        "sender_entity_id": 1001,
        "receiver_entity_id": 2002,
        "sender_pseudo": "bank_a_customer_hash_001",
        "receiver_pseudo": "shared_counterparty_hash_777",
        "amount": amount,
        "amount_cipher_ref": f"cipher_amount_{amount}_demo",
        "currency": "USD",
        "transaction_type": "cross_border_wire_transfer",
        "originator_name": "Demo Originator Customer",
        "beneficiary_name": "Demo Beneficiary Customer",
        "originator_institution": "Bank A Uganda",
        "beneficiary_institution": "Bank B Kenya",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "possible_cross_bank_overlap_count": overlap,
        "screening_indicator": screening_indicator,
        "counterparty_risk": "high_risk_counterparty" if amount >= 100000 else "normal",
        "cdd_status": "cdd_incomplete" if amount >= 100000 else "complete",
    }
    status, body = request("POST", "/transactions", payload, token=token)
    if status in (200, 201):
        print(f"✅ Created transaction {tx_id}")
    elif status == 409:
        print(f"ℹ️  Transaction already exists: {tx_id}")
    else:
        print(f"⚠️ Transaction create issue for {tx_id}: {status} {body}")

def approve_and_screen(reviewer_token: str, tx_id: str) -> None:
    request("POST", f"/transactions/{tx_id}/approve", {"note": "Demo reviewer approval for seeded workflow."}, token=reviewer_token)
    status, body = request("POST", f"/transactions/{tx_id}/run-screening", token=reviewer_token)
    if status in (200, 201):
        print(f"✅ SMPC screening linked risk for {tx_id}")
    else:
        print(f"ℹ️ Screening skipped/issue for {tx_id}: {status} {body}")

def open_demo_case(regulator_token: str, reviewer_org_id: str) -> None:
    status, body = request("POST", "/regulator/anomaly-cases", {
        "tx_id": "TX-SMPC-OVERLAP-001",
        "summary": "Seeded SMPC overlap case for final presentation.",
        "regulator_finding": "Aggregate evidence shows cross-bank overlap and screening attention without exposing raw bank inputs.",
        "required_bank_action": "Review the transaction, confirm internal investigation status, and respond to the regulator notice.",
        "notified_organization_ids": [reviewer_org_id],
    }, token=regulator_token)
    if status in (200, 201):
        print(f"✅ Opened demo anomaly case: {body.get('case_ref')}")
    else:
        print(f"ℹ️ Case open skipped/issue: {status} {body}")

def main() -> None:
    print("=== AML SMPC Demo Seeder ===")
    apply_migration("infra/postgres/migrations/008_partner_bank_identity_and_permissions.sql")
    apply_migration("infra/postgres/migrations/009_suspicion_rules_and_transaction_risk.sql")
    apply_migration("infra/postgres/migrations/010_regulator_anomaly_cases.sql")
    print("✅ Partner organizations, AML rules, and anomaly tables confirmed.")

    super_token, _ = login(SUPER_EMAIL, SUPER_PASSWORD)
    register_and_approve_users(super_token)

    submitter_token, _ = login("demo.submitter@example.com", PASSWORD)
    reviewer_token, reviewer_session = login("demo.reviewer@example.com", PASSWORD)
    regulator_token, _ = login("demo.regulator@example.com", PASSWORD)

    create_transaction(submitter_token, "TX-BANKA-LOW-001", 1200, 0, "clear")
    create_transaction(submitter_token, "TX-BANKA-SUSPICIOUS-001", 250000, 0, "watchlist_attention")
    create_transaction(submitter_token, "TX-SMPC-OVERLAP-001", 250000, 1, "watchlist_attention")

    approve_and_screen(reviewer_token, "TX-BANKA-SUSPICIOUS-001")
    approve_and_screen(reviewer_token, "TX-SMPC-OVERLAP-001")

    reviewer_org_id = reviewer_session.get("organization_id") or psql("SELECT organization_id FROM app_users WHERE email='demo.reviewer@example.com' LIMIT 1;")
    if reviewer_org_id:
        open_demo_case(regulator_token, reviewer_org_id)

    print("=== Seeder complete ===")

if __name__ == "__main__":
    main()
EOF

chmod +x scripts/dev/seed_bank_rbac_case_demo.py
```

---

## 8.2 Run seeder

Backend must be running first.

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
source env/bin/activate
python3 scripts/dev/seed_bank_rbac_case_demo.py
```

Expected:

```text
Partner organizations, AML rules, and anomaly tables confirmed
Demo users registered or already exist
Demo transactions created or already exist
SMPC screening linked risk
Demo anomaly case opened or already handled
Seeder complete
```

---

# Stage 7/8 Build Validation

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

cargo build --manifest-path services/regulator-api/backend/Cargo.toml

cd services/regulator-api/frontend
npm run build
```

Expected:

```text
Finished dev profile
✓ built
```

---

# Stage 7/8 Runtime Validation

## Regulator metrics

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

REGULATOR_JSON="$(curl -fsS -X POST http://127.0.0.1:8085/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo.regulator@example.com",
    "password": "StrongPass123"
  }')"

REGULATOR_TOKEN="$(echo "$REGULATOR_JSON" | jq -r '.token')"

curl -fsS http://127.0.0.1:8085/regulator/anomaly-cases \
  -H "Authorization: Bearer $REGULATOR_TOKEN" \
  | jq '{
      case_count: length,
      high_risk_cases: [.[] | select(.risk_level=="high")] | length,
      open_cases: [.[] | select(.case_status!="closed")] | length
    }'

curl -fsS http://127.0.0.1:8085/proofs \
  -H "Authorization: Bearer $REGULATOR_TOKEN" \
  | jq '{
      proof_count: length,
      verified: [.[] | select(.verification_status=="verified")] | length,
      fatf_rec10: [.[] | select(.rule_id=="FATF_REC10")] | length,
      fatf_rec11: [.[] | select(.rule_id=="FATF_REC11")] | length,
      fatf_rec16: [.[] | select(.rule_id=="FATF_REC16")] | length
    }'
```

Expected:

```text
case_count >= 1
high_risk_cases >= 1
proof endpoint returns an array
```

---

# Stage 7/8 UI Validation

Start frontend:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system/services/regulator-api/frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Login:

```text
demo.regulator@example.com
StrongPass123
```

Open:

```text
/regulator/dashboard
/regulator/proofs
/regulator/audit
/regulator/compliance-report
/regulator/three-bank-smpc-demo
/regulator/anomaly-cases
```

Expected dashboard cards:

```text
verified proofs
pending proof reviews
high-risk cases
open anomaly cases
closed anomaly cases
FATF R.10 evidence
FATF R.11 evidence
FATF R.16 evidence
```

Login as bank reviewer:

```text
demo.reviewer@example.com
StrongPass123
```

Open:

```text
/institution/dashboard
/institution/anomaly-notices
/institution/suspicious-transactions
```

Expected:

```text
dashboard shows live backend counts
anomaly notices visible
suspicious transactions visible
```

---

# Commit Stage 7 + Stage 8

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git status -sb

git add aml-system/services/regulator-api/frontend/src/api/regulatorDashboardApi.ts
git add aml-system/services/regulator-api/frontend/src/pages/regulator/RegulatorDashboardPage.tsx
git add aml-system/services/regulator-api/frontend/src/components/navigation/Sidebar.tsx
git add aml-system/scripts/dev/seed_bank_rbac_case_demo.py

git commit -m "Furnish regulator dashboard and add demo seeder"

git push
```

---

# Pull Request Update Text

Paste this into the PR after pushing:

```md
### Stage 7 — Regulator Dashboard Furnishment

- Added regulator dashboard summary API client.
- Furnished `/regulator/dashboard` with evidence governance cards:
  - verified proofs
  - pending proof reviews
  - high-risk cases
  - open anomaly cases
  - closed anomaly cases
  - FATF R.10 evidence
  - FATF R.11 evidence
  - FATF R.16 evidence
- Added clear governance route links:
  - `/regulator/proofs`
  - `/regulator/audit`
  - `/regulator/compliance-report`
  - `/regulator/three-bank-smpc-demo`
  - `/regulator/anomaly-cases`
- Added explicit privacy boundary statement that regulator does not receive raw bank inputs.

### Stage 8 — Seeder and Demo Data

- Added `scripts/dev/seed_bank_rbac_case_demo.py`.
- Seeder confirms partner organizations and AML rules.
- Seeder registers/approves demo users where needed.
- Seeder creates presentation transactions:
  - `TX-BANKA-LOW-001`
  - `TX-BANKA-SUSPICIOUS-001`
  - `TX-SMPC-OVERLAP-001`
- Seeder runs approval/screening for high-risk demo transactions.
- Seeder opens a demo regulator anomaly case for bank notice workflow.
```

---

# Exit Criteria

Stage 7/8 passes when:

```text
backend build passes
frontend build passes
seeder runs successfully
regulator dashboard shows evidence governance metrics
regulator can inspect proofs/audit/compliance/anomaly cases/three-bank SMPC demo
bank dashboard shows real transaction and notice metrics
privacy boundary is clearly displayed
```

Next stage after this:

```text
Stage 9 — Final Validation Scripts and Submission Runbook
```
