# PBBF BLISS — Phase 2 Stage 6 Populated Markdown Package
## Data Protection, Backup, Recovery, and Retention Controls

## Stage objective
Protect the system against data loss, unsafe retention, and weak recovery posture.

This stage is where the platform becomes operationally safer around:
- backup discipline
- restore confidence
- retention clarity
- export handling
- stale-record behavior
- recovery validation

It is not enough for data to exist. The team must be able to explain:
- how data is backed up
- how it is restored
- how long it is kept
- how exports are controlled
- how the UI avoids misleading users with stale or expired records

---

## Stage outcomes

### Backend stage outcome
The backend gains:
- documented backup strategy
- restore scripts
- restore validation guide
- retention and export handling rules
- recovery smoke validation
- stronger admin/audit support for operational data visibility

### Frontend stage outcome
The frontend improves:
- stale or archived record messaging
- report and audit views that acknowledge retention realities
- deployment/testing docs aligned with operational data handling
- safer admin-facing visibility around historical records and exports

### Completion gate
You can explain how data is backed up, how it is restored, and how long critical operational data is kept.

---

## Repository root
`bliss-telehealth/`

---

# Stage 6 directory structure

```text
bliss-telehealth/
├── docs/
│   └── data-governance/
│       ├── backup-and-restore-plan.md
│       ├── data-retention-policy.md
│       └── export-handling-policy.md
├── pbbf-api/
│   ├── docs/
│   │   └── backend-restore-validation.md
│   ├── scripts/
│   │   ├── backup_db.sh
│   │   └── restore_db.sh
│   ├── app/
│   │   └── modules/
│   │       ├── admin/
│   │       │   ├── repository.py
│   │       │   ├── router.py
│   │       │   ├── schemas.py
│   │       │   └── service.py
│   │       └── audit/
│   │           ├── repository.py
│   │           ├── router.py
│   │           ├── schemas.py
│   │           └── service.py
│   └── tests/
│       ├── integration/
│       │   └── test_admin_journey.py
│       └── test_recovery_smoke.py
└── pbbf-telehealth/
    ├── docs/
    │   ├── frontend-deployment.md
    │   └── frontend-testing.md
    ├── src/
    │   ├── pages/
    │   │   └── admin/
    │   │       ├── Reports.jsx
    │   │       └── AuditLogs.jsx
    │   └── modules/
    │       └── admin/
    │           ├── components/
    │           ├── hooks/
    │           ├── services/
    │           └── utils/
```

---

# Recommended commands to create missing directories

Run from the `bliss-telehealth` root:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth

mkdir -p docs/data-governance
mkdir -p pbbf-api/docs
mkdir -p pbbf-api/scripts
mkdir -p pbbf-api/tests/integration
mkdir -p pbbf-telehealth/docs
mkdir -p pbbf-telehealth/src/modules/admin/utils
```

---

# FILE 1 — `[CREATE]` `bliss-telehealth/docs/data-governance/backup-and-restore-plan.md`

```md
# PBBF BLISS Backup and Restore Plan

## Purpose
This document defines the minimum backup and restore posture for the platform.

## Core principle
A system is not operationally safe just because data is stored. It is operationally safer when the team can:
- create backups consistently
- verify they are usable
- restore them in a controlled way
- document what was restored and when

## Minimum backup scope
The following data domains should be considered in backup planning:
- users and role assignments
- intake submissions and consent versions
- appointments
- screening submissions and derived classifications
- telehealth session metadata
- encounter notes
- referrals
- notifications and audit visibility data where required for operations

## Backup expectations
- scheduled database backup
- timestamped backup file naming
- retention window for backup artifacts
- restore procedure documentation
- restore validation after backup or recovery drill

## Operational rule
Backups should be treated as incomplete until restore validation has been performed.

## Minimum recovery workflow
1. Identify incident and affected environment
2. Preserve logs and incident evidence
3. Select recovery point
4. Restore into a safe target
5. Validate record integrity and app boot behavior
6. Confirm role-based access and health endpoints
7. Document outcome
```

---

# FILE 2 — `[CREATE]` `bliss-telehealth/docs/data-governance/data-retention-policy.md`

```md
# PBBF BLISS Data Retention Policy

## Purpose
This document defines the minimum retention expectations for operational platform data.

## Core principle
Retention must be intentional. Data should not be kept forever by accident, and it should not disappear without policy.

## Retention categories

### Critical operational records
These include:
- audit events
- consent-linked submissions
- encounter finalization history
- referral state history

These should have a clearly defined retention period aligned with operational and governance needs.

### Active workflow data
These include:
- current appointments
- active referrals
- current telehealth session metadata
- recent notifications

These should remain visible while operationally relevant.

### Archived or expired workflow data
These include:
- completed historical flows
- expired session metadata
- outdated operational reminders

These may remain stored longer than they remain actively shown in UI.

## UI handling principle
The frontend should not mislead users by presenting archived, deleted, or expired records as though they are still active.

## Governance rule
Any retention rule adopted operationally must be reflected in:
- backend processing expectations
- admin reporting behavior
- audit visibility behavior
- export handling guidance
```

---

# FILE 3 — `[CREATE]` `bliss-telehealth/docs/data-governance/export-handling-policy.md`

```md
# PBBF BLISS Export Handling Policy

## Purpose
This document defines the minimum expectations for data exports and reporting outputs.

## Core principle
Exports are not just convenience artifacts. They can become operationally sensitive copies of platform data.

## Minimum rules
- exports should only be available to appropriate roles
- exports should reflect retention-aware data visibility
- exports should not silently expose fields beyond the intended reporting scope
- export generation should be auditable where operationally relevant
- stale or deleted record states should be represented accurately

## Admin-facing rule
Admin reports and audit views should not imply that exported data is timeless or context-free. The interface should make it clear when data is historical, archived, or subject to retention limits.

## Frontend rule
The UI should avoid labels that imply permanent availability where only current operational visibility is guaranteed.
```

---

# FILE 4 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/scripts/backup_db.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
DATABASE_URL="${PBBF_DATABASE_URL:-}"

mkdir -p "${BACKUP_DIR}"

if [[ -z "${DATABASE_URL}" ]]; then
  echo "[FAIL] PBBF_DATABASE_URL is not set."
  exit 1
fi

echo "[INFO] Starting backup at ${TIMESTAMP}"

if [[ "${DATABASE_URL}" == sqlite:* ]]; then
  DB_FILE="${DATABASE_URL#sqlite:///}"
  if [[ ! -f "${DB_FILE}" ]]; then
    echo "[FAIL] SQLite database file not found: ${DB_FILE}"
    exit 1
  fi

  cp "${DB_FILE}" "${BACKUP_DIR}/bliss_sqlite_${TIMESTAMP}.db"
  echo "[OK] SQLite backup created at ${BACKUP_DIR}/bliss_sqlite_${TIMESTAMP}.db"
else
  if ! command -v pg_dump >/dev/null 2>&1; then
    echo "[FAIL] pg_dump is required for non-SQLite backups."
    exit 1
  fi

  pg_dump "${DATABASE_URL}" > "${BACKUP_DIR}/bliss_postgres_${TIMESTAMP}.sql"
  echo "[OK] PostgreSQL backup created at ${BACKUP_DIR}/bliss_postgres_${TIMESTAMP}.sql"
fi
```

---

# FILE 5 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/scripts/restore_db.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_FILE="${1:-}"
DATABASE_URL="${PBBF_DATABASE_URL:-}"

if [[ -z "${BACKUP_FILE}" ]]; then
  echo "[FAIL] Usage: ./scripts/restore_db.sh <backup-file>"
  exit 1
fi

if [[ ! -f "${BACKUP_FILE}" ]]; then
  echo "[FAIL] Backup file not found: ${BACKUP_FILE}"
  exit 1
fi

if [[ -z "${DATABASE_URL}" ]]; then
  echo "[FAIL] PBBF_DATABASE_URL is not set."
  exit 1
fi

echo "[INFO] Starting restore from ${BACKUP_FILE}"

if [[ "${DATABASE_URL}" == sqlite:* ]]; then
  DB_FILE="${DATABASE_URL#sqlite:///}"
  cp "${BACKUP_FILE}" "${DB_FILE}"
  echo "[OK] SQLite restore completed to ${DB_FILE}"
else
  if ! command -v psql >/dev/null 2>&1; then
    echo "[FAIL] psql is required for non-SQLite restores."
    exit 1
  fi

  psql "${DATABASE_URL}" < "${BACKUP_FILE}"
  echo "[OK] PostgreSQL restore completed from ${BACKUP_FILE}"
fi
```

---

# FILE 6 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/docs/backend-restore-validation.md`

```md
# Backend Restore Validation Guide

## Purpose
This document defines how to validate that a restore operation actually worked.

## Validation workflow

### 1. Run the restore
Use:
```bash
./scripts/restore_db.sh <backup-file>
```

### 2. Confirm service boot
Start the backend and confirm:
- app boots cleanly
- no migration panic occurs
- health endpoint responds

### 3. Confirm health endpoints
Check:
```bash
curl -sS http://127.0.0.1:8000/api/v1/health
curl -sS http://127.0.0.1:8000/api/v1/ready
```

### 4. Confirm core operational visibility
Validate that recovered data is still interpretable enough to support:
- admin reporting
- audit review
- auth login behavior
- at least one role-based workflow smoke check

### 5. Record validation evidence
Capture:
- restore date/time
- backup file used
- environment restored into
- health check result
- smoke result
- issues found

## Rule
A restore is not considered validated until health and at least one operational smoke flow have passed.
```

---

# FILE 7 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/audit/schemas.py`

> Merge these fields if they are not already present so audit records can better support data-governance interpretation.

```python
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditLogRead(BaseModel):
    id: str | int
    actor_name: str
    action: str
    target_type: str
    target_id: str | None = None
    request_id: str | None = None
    metadata: dict[str, Any] = {}
    created_at: datetime
    retention_class: str | None = None
    archived: bool = False


class AuditLogCreate(BaseModel):
    actor_name: str
    action: str
    target_type: str
    target_id: str | None = None
    request_id: str | None = None
    metadata: dict[str, Any] = {}
    retention_class: str | None = None
```

---

# FILE 8 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/audit/service.py`

> Merge this into your existing audit service so retention and export-related actions remain explainable.

```python
from __future__ import annotations

import logging
from typing import Any

from app.common.middleware.request_context import get_request_id
from app.modules.audit.schemas import AuditLogCreate

logger = logging.getLogger("pbbf.audit")


class AuditService:
    def __init__(self, repository):
        self.repository = repository

    def create_event(
        self,
        *,
        actor_name: str,
        action: str,
        target_type: str,
        target_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        retention_class: str | None = None,
    ):
        payload = AuditLogCreate(
            actor_name=actor_name,
            action=action,
            target_type=target_type,
            target_id=target_id,
            request_id=get_request_id(),
            metadata=metadata or {},
            retention_class=retention_class,
        )
        event = self.repository.create(payload)

        logger.info(
            f"event=audit.write request_id={payload.request_id} action={payload.action} "
            f"target_type={payload.target_type} actor={payload.actor_name} retention_class={payload.retention_class}"
        )
        return event

    def list_events(self):
        return self.repository.list_all()
```

---

# FILE 9 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/audit/repository.py`

> Keep your real persistence layer if already wired. This shows the additional retention fields.

```python
from __future__ import annotations

from datetime import datetime, timezone

from app.modules.audit.schemas import AuditLogCreate


class AuditRepository:
    def __init__(self):
        self._items = []

    def create(self, payload: AuditLogCreate):
        item = {
            "id": len(self._items) + 1,
            "actor_name": payload.actor_name,
            "action": payload.action,
            "target_type": payload.target_type,
            "target_id": payload.target_id,
            "request_id": payload.request_id,
            "metadata": payload.metadata,
            "retention_class": payload.retention_class,
            "archived": False,
            "created_at": datetime.now(timezone.utc),
        }
        self._items.append(item)
        return item

    def list_all(self):
        return list(reversed(self._items))
```

---

# FILE 10 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/admin/schemas.py`

> Merge these data-governance-oriented fields if your admin schemas do not already expose them.

```python
from __future__ import annotations

from pydantic import BaseModel


class DataGovernanceSummary(BaseModel):
    backup_status: str
    last_backup_at: str | None = None
    restore_validation_status: str
    retention_policy_version: str
    export_policy_version: str
```

---

# FILE 11 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/admin/service.py`

> Merge this into your existing admin service so operational governance details can be surfaced in admin reporting.

```python
from __future__ import annotations


class AdminService:
    def __init__(self, repository):
        self.repository = repository

    def get_data_governance_summary(self):
        return {
            "backup_status": "configured",
            "last_backup_at": None,
            "restore_validation_status": "documented",
            "retention_policy_version": "2026.05",
            "export_policy_version": "2026.05",
        }
```

---

# FILE 12 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/admin/router.py`

> Merge a small admin governance summary endpoint into your existing router.

```python
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.common.permissions.dependencies import require_admin
from app.modules.admin.repository import AdminRepository
from app.modules.admin.service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])


def get_admin_service() -> AdminService:
    repository = AdminRepository()
    return AdminService(repository)


@router.get("/data-governance-summary")
def get_data_governance_summary(_admin=Depends(require_admin), service: AdminService = Depends(get_admin_service)):
    return {"summary": service.get_data_governance_summary()}
```

> Merge note:
> Keep your existing admin routes. This Stage 6 addition is a small governance endpoint, not a router rewrite.

---

# FILE 13 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/integration/test_admin_journey.py`

```python
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.modules.admin.router import router as admin_router


def test_admin_governance_summary_route_exists():
    app = FastAPI()
    app.include_router(admin_router, prefix="/api/v1")

    client = TestClient(app)
    response = client.get("/api/v1/admin/data-governance-summary")

    # Depending on auth dependency wiring this may be 401/403 without override,
    # but the route itself should exist and not 404.
    assert response.status_code in {200, 401, 403}
```

---

# FILE 14 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/test_recovery_smoke.py`

```python
import os
import subprocess
from pathlib import Path


def test_backup_script_exists():
    assert Path("scripts/backup_db.sh").exists()


def test_restore_script_exists():
    assert Path("scripts/restore_db.sh").exists()
```

---

# FILE 15 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/pages/admin/Reports.jsx`

> Merge this governance-aware reporting panel into your existing Reports page.

```jsx
import { useAdminMetrics } from "../../modules/admin/hooks/useAdminMetrics";
import PageHeader from "../../shared/components/PageHeader";
import SectionCard from "../../shared/components/SectionCard";
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";

export default function AdminReportsPage() {
  const { summary, metricDetails, isLoading, loadError } = useAdminMetrics();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading reports..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load reports" message={loadError} />;
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Admin reports"
        title="Reporting snapshots"
        description="Review operational reporting snapshots with awareness that report outputs may be affected by retention and archival rules over time."
      />

      <SectionCard
        title="Core snapshot"
        description="These metrics reflect the current operational reporting view."
      >
        <div className="grid gap-3 text-sm text-slate-700">
          <p>Total users: <span className="font-medium">{summary?.totalUsers ?? 0}</span></p>
          <p>Active patients: <span className="font-medium">{summary?.activePatients ?? 0}</span></p>
          <p>Total appointments: <span className="font-medium">{summary?.totalAppointments ?? 0}</span></p>
          <p>Completed visits: <span className="font-medium">{summary?.completedVisits ?? 0}</span></p>
        </div>
      </SectionCard>

      <SectionCard
        title="Data governance note"
        description="Exports and visible operational records may change over time according to retention and archival policy."
      >
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
          Report visibility should be interpreted together with retention and export-handling rules. Historical operational views do not necessarily imply indefinite active display.
        </div>
      </SectionCard>

      <SectionCard
        title="Extended snapshot"
        description="Detailed metrics payload for controlled admin review."
      >
        <pre className="overflow-x-auto rounded-2xl bg-slate-50 p-4 text-xs text-slate-700">
{JSON.stringify(metricDetails || {}, null, 2)}
        </pre>
      </SectionCard>
    </div>
  );
}
```

---

# FILE 16 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/pages/admin/AuditLogs.jsx`

> Merge this governance-aware wording into your existing Audit Logs page.

```jsx
import AuditLogTable from "../../modules/admin/components/AuditLogTable";
import { useAdminMetrics } from "../../modules/admin/hooks/useAdminMetrics";
import PageHeader from "../../shared/components/PageHeader";
import SectionCard from "../../shared/components/SectionCard";
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";

export default function AdminAuditLogsPage() {
  const { auditLogs, isLoading, loadError } = useAdminMetrics();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading audit logs..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load audit logs" message={loadError} />;
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Admin audit"
        title="Audit visibility"
        description="Review operational activity and accountability events. Historical visibility may still be subject to retention and archival policy."
      />

      <SectionCard
        title="Audit review notes"
        description="Interpret audit records in the context of current retention and archival rules."
      >
        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
          Audit visibility supports oversight, but the active interface should not imply that every historical event remains permanently visible in the same way forever.
        </div>
      </SectionCard>

      <AuditLogTable logs={auditLogs} />
    </div>
  );
}
```

---

# FILE 17 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/docs/frontend-deployment.md`

> Append this governance note to the deployment guide.

```md
## Data-governance reminder
Production and staging verification should include a check that admin-facing reporting and audit pages do not present stale or archived data in misleading ways. Deployment sign-off should consider retention-aware UI behavior, not only route availability.
```

---

# FILE 18 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/docs/frontend-testing.md`

> Append this governance note to the testing guide.

```md
## Retention-aware UI testing
During admin workflow testing, verify that:
- report wording does not imply permanent active visibility for all historical data
- audit wording does not imply indefinite display without policy
- deleted, archived, or expired operational states are not presented as active current records
```

---

# FILE 19 — `[RECOMMENDED CREATE]` `bliss-telehealth/pbbf-telehealth/src/modules/admin/utils/retention.js`

> This is optional but strongly recommended so retention-aware display logic stays centralized instead of being scattered across admin pages.

```jsx
export function describeRetentionAwareState({
  archived = false,
  expired = false,
  deleted = false,
}) {
  if (deleted) return "Deleted or unavailable by policy.";
  if (archived) return "Archived historical record.";
  if (expired) return "Expired operational record.";
  return "Active operational record.";
}
```

---

# Recommended verification commands for Stage 6

## Backend governance and recovery checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

chmod +x scripts/backup_db.sh scripts/restore_db.sh
pytest tests/integration/test_admin_journey.py tests/test_recovery_smoke.py -q
```

## Frontend admin view checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth

npm run test
npm run build
```

> Then manually verify:
> - Reports page governance note renders
> - Audit Logs page governance note renders
> - wording does not imply indefinite active visibility for all historical records

---

# Git commit recommendation for this stage

Run from the `bliss-telehealth` root:

```bash
git add docs/data-governance pbbf-api/scripts/backup_db.sh pbbf-api/scripts/restore_db.sh pbbf-api/docs/backend-restore-validation.md pbbf-api/app/modules/admin pbbf-api/app/modules/audit pbbf-api/tests/integration/test_admin_journey.py pbbf-api/tests/test_recovery_smoke.py pbbf-telehealth/src/pages/admin/Reports.jsx pbbf-telehealth/src/pages/admin/AuditLogs.jsx pbbf-telehealth/src/modules/admin pbbf-telehealth/docs/frontend-deployment.md pbbf-telehealth/docs/frontend-testing.md
git commit -m "ops: add data protection, recovery, and retention governance baseline"
```

---

# Completion gate for Stage 6

This stage is complete only when:
- data-governance docs exist
- backup script exists
- restore script exists
- backend restore validation guide exists
- admin governance summary path exists or is merged
- audit data supports retention-aware interpretation
- admin reports and audit UI wording acknowledge retention realities
- frontend docs reflect retention-aware deployment and testing checks
- the team can explain backup, restore, and retention behavior clearly

---

# Final recommendation
Treat Stage 6 as the stage that turns stored data into governed operational data.

If the team still cannot answer:
- how recovery works
- how restore is validated
- how long operational records are kept
- how exports should be interpreted

then Stage 6 is not complete yet.
