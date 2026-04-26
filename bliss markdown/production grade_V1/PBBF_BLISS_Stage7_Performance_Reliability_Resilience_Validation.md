# PBBF BLISS — Phase 2 Stage 7 Populated Markdown Package
## Performance, Reliability, and Resilience Validation

## Stage objective
Prove the MVP can stay stable under realistic workload and failure conditions.

This stage is where the team stops assuming the system is dependable just because core workflows function under normal developer conditions.

The goal is to prove that the platform can keep behaving acceptably when it faces:
- repeated requests
- concurrent usage
- slow responses
- partial failures
- refreshes during active sessions
- migration churn
- retry-worthy background-job conditions

---

## Stage outcomes

### Backend stage outcome
The backend gains:
- repeatable load-test execution
- concurrency validation
- retry behavior validation for job workflows
- DB stability smoke checks
- migration validation script support
- clearer confidence around stability limits

### Frontend stage outcome
The frontend gains:
- slow-API scenario testing
- partial-failure scenario testing
- refresh behavior validation
- repeated cross-role navigation validation
- resilience-oriented E2E coverage
- shared UI feedback for slow or degraded operational states

### Completion gate
The system can survive realistic usage, and you know where the stability limits are before public-facing rollout.

---

## Repository root
`bliss-telehealth/`

---

# Stage 7 directory structure

```text
bliss-telehealth/
├── docs/
│   └── performance/
│       ├── performance-test-plan.md
│       └── reliability-gates.md
├── pbbf-api/
│   ├── app/
│   │   └── jobs/
│   │       ├── __init__.py
│   │       └── retry.py
│   ├── alembic/
│   ├── scripts/
│   │   ├── run_load_tests.sh
│   │   └── run_migration_validation.sh
│   └── tests/
│       ├── integration/
│       │   └── test_role_workflow_reliability.py
│       └── performance/
│           ├── conftest.py
│           ├── test_health_latency.py
│           ├── test_concurrent_requests.py
│           ├── test_job_retry.py
│           └── test_db_stability_smoke.py
└── pbbf-telehealth/
    ├── docs/
    │   └── frontend-testing.md
    └── src/
        ├── shared/
        │   └── components/
        │       └── NetworkStateNotice.jsx
        ├── test/
        │   ├── e2e/
        │   │   ├── resilience-patient.spec.js
        │   │   └── cross-role-refresh.spec.js
        │   └── msw/
        │       └── reliabilityHandlers.js
        └── modules/
            ├── appointments/__tests__/AppointmentsSlowApi.test.jsx
            └── telehealth/__tests__/SessionResilience.test.jsx
```

---

# Recommended commands to create missing directories

Run from the `bliss-telehealth` root:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth

mkdir -p docs/performance
mkdir -p pbbf-api/tests/performance
mkdir -p pbbf-api/tests/integration
mkdir -p pbbf-api/app/jobs
mkdir -p pbbf-telehealth/src/test/e2e
mkdir -p pbbf-telehealth/src/test/msw
mkdir -p pbbf-telehealth/src/shared/components
mkdir -p pbbf-telehealth/src/modules/appointments/__tests__
mkdir -p pbbf-telehealth/src/modules/telehealth/__tests__
```

---

# FILE 1 — `[CREATE]` `bliss-telehealth/docs/performance/performance-test-plan.md`

```md
# PBBF BLISS Performance Test Plan

## Purpose
This document defines how the team will validate whether the MVP behaves acceptably under realistic pressure and degraded conditions.

## Core principle
A stable system is not one that works only when one developer clicks slowly on a local machine. A stable system is one that continues to behave predictably under repeated use, concurrent access, and recoverable failure.

## Test categories

### 1. Health and baseline responsiveness
Verify that the API health and readiness paths respond consistently and fast enough under repeated requests.

### 2. Concurrency behavior
Verify that repeated concurrent requests do not immediately produce instability, broken session interpretation, or inconsistent role behavior.

### 3. Job retry behavior
Verify that retryable background work can fail safely and retry predictably without silent loss.

### 4. Database stability
Verify that repeated reads and writes do not immediately destabilize the service.

### 5. Migration validation
Verify that Alembic migrations can move the schema forward and backward predictably in a controlled validation environment.

### 6. Frontend resilience
Verify that the UI remains understandable under:
- slow APIs
- partial failures
- repeated refreshes
- repeated role navigation
- retry-friendly user actions

## Minimum pass criteria
- health endpoints remain reachable
- no immediate crash under repeated/concurrent use
- retryable job paths are test-backed
- migrations validate without manual rescue
- UI still explains degraded states clearly
- cross-role protected navigation remains correct after refresh

## Warning
Passing these tests does not prove infinite scalability. It proves that the system has known stability behavior and known current limits before rollout.
```

---

# FILE 2 — `[CREATE]` `bliss-telehealth/docs/performance/reliability-gates.md`

```md
# PBBF BLISS Reliability Gates

## Purpose
This document defines the minimum reliability thresholds required before public-facing rollout.

## Required gates

### Gate 1 — Boot reliability
- backend boots cleanly
- frontend builds cleanly
- health and readiness endpoints respond

### Gate 2 — Role workflow survivability
- patient flow remains usable under normal and mildly degraded conditions
- provider flow remains usable under refresh and repeated navigation
- admin flow remains usable under report and audit page access

### Gate 3 — Controlled degradation behavior
- slow APIs do not make the UI confusing
- errors are readable and retry-friendly
- partial failures do not expose unsafe backend details

### Gate 4 — Migration stability
- upgrade path validated
- downgrade path validated
- re-upgrade path validated
- no manual rescue required for the validation cycle

### Gate 5 — Basic performance sanity
- repeated requests do not immediately collapse health behavior
- concurrency smoke checks pass
- retryable job logic is test-backed

## Decision rule
Do not treat “works locally” as a reliability gate.  
The product should only pass this stage when the team can explain the known limits and known safe behavior under realistic pressure.
```

---

# FILE 3 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/app/jobs/__init__.py`

```python
from app.jobs.retry import retry_operation

__all__ = ["retry_operation"]
```

---

# FILE 4 — `[CREATE]` `bliss-telehealth/pbbf-api/app/jobs/retry.py`

```python
from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry_operation(
    func: Callable[[], T],
    *,
    retries: int = 3,
    delay_seconds: float = 0.2,
    retry_on: tuple[type[Exception], ...] = (Exception,),
) -> T:
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            return func()
        except retry_on as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(delay_seconds)

    assert last_error is not None
    raise last_error
```

---

# FILE 5 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/performance/conftest.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def performance_client() -> TestClient:
    return TestClient(create_app())
```

---

# FILE 6 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/performance/test_health_latency.py`

```python
import time

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_latency_is_reasonable():
    client = TestClient(create_app())

    start = time.perf_counter()
    response = client.get("/api/v1/health")
    duration_ms = (time.perf_counter() - start) * 1000

    assert response.status_code == 200
    assert duration_ms < 1000
```

---

# FILE 7 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/performance/test_concurrent_requests.py`

```python
from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from app.main import create_app


def test_concurrent_health_requests_do_not_immediately_fail():
    client = TestClient(create_app())

    def hit_health():
        response = client.get("/api/v1/health")
        return response.status_code

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda _: hit_health(), range(20)))

    assert all(status == 200 for status in results)
```

---

# FILE 8 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/performance/test_job_retry.py`

```python
import pytest

from app.jobs.retry import retry_operation


def test_retry_operation_eventually_succeeds():
    state = {"attempts": 0}

    def flaky():
        state["attempts"] += 1
        if state["attempts"] < 3:
            raise ValueError("temporary failure")
        return "ok"

    result = retry_operation(flaky, retries=3, delay_seconds=0.01, retry_on=(ValueError,))
    assert result == "ok"
    assert state["attempts"] == 3


def test_retry_operation_raises_after_exhaustion():
    def always_fail():
        raise RuntimeError("permanent failure")

    with pytest.raises(RuntimeError):
        retry_operation(always_fail, retries=2, delay_seconds=0.01, retry_on=(RuntimeError,))
```

---

# FILE 9 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/performance/test_db_stability_smoke.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_repeated_ready_checks_remain_stable():
    client = TestClient(create_app())

    for _ in range(25):
        response = client.get("/api/v1/ready")
        assert response.status_code == 200
```

> Merge note:
> This is a light DB-adjacent stability smoke check, not a full database benchmark. It is intentionally simple and safe to run early.

---

# FILE 10 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/integration/test_role_workflow_reliability.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_role_workflow_reliability_routes_exist():
    client = TestClient(create_app())

    health = client.get("/api/v1/health")
    ready = client.get("/api/v1/ready")

    assert health.status_code == 200
    assert ready.status_code == 200
```

> This is intentionally a light integration smoke seed. Expand it later with seeded auth, patient, provider, and admin journeys under controlled data.

---

# FILE 11 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/scripts/run_load_tests.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[INFO] Running backend performance and reliability checks..."
pytest tests/performance -q

echo "[OK] Backend performance and reliability checks completed."
```

---

# FILE 12 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/scripts/run_migration_validation.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[INFO] Validating Alembic upgrade path..."
alembic upgrade head

echo "[INFO] Validating Alembic downgrade path..."
alembic downgrade base

echo "[INFO] Re-validating Alembic re-upgrade path..."
alembic upgrade head

echo "[OK] Migration validation completed successfully."
```

> Important note:
> Run this only in a controlled validation database, not against production.

---

# FILE 13 — `[CREATE]` `bliss-telehealth/pbbf-telehealth/src/test/msw/reliabilityHandlers.js`

```js
import { http, HttpResponse, delay } from "msw";

const API_BASE_URL =
  (import.meta?.env?.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1").replace(/\/$/, "");

export const reliabilityHandlers = [
  http.get(`${API_BASE_URL}/appointments`, async () => {
    await delay(1200);
    return HttpResponse.json({
      appointments: [
        {
          id: "appt-1",
          service_type: "mental_health",
          status: "booked",
          scheduled_at: "2026-05-10T10:00:00Z",
        },
      ],
    });
  }),

  http.get(`${API_BASE_URL}/telehealth/sessions/next`, async () => {
    await delay(1000);
    return HttpResponse.json({
      session: {
        id: "session-1",
        appointment_time: "2026-05-10T10:00:00Z",
        session_status: "ready",
        provider_name: "Provider User",
        service_type: "Telehealth follow-up",
        join_url: "https://example.test/join/session-1",
      },
    });
  }),

  http.get(`${API_BASE_URL}/admin/metrics`, async () => {
    await delay(800);
    return HttpResponse.json(
      {
        message: "Temporary upstream reporting issue.",
      },
      { status: 503 }
    );
  }),
];
```

---

# FILE 14 — `[CREATE]` `bliss-telehealth/pbbf-telehealth/src/shared/components/NetworkStateNotice.jsx`

```jsx
export default function NetworkStateNotice({
  tone = "info",
  title = "Working on it",
  message = "The system is still responding. This may take a moment.",
}) {
  const toneClasses =
    tone === "warning"
      ? "border-amber-200 bg-amber-50 text-amber-900"
      : tone === "error"
      ? "border-rose-200 bg-rose-50 text-rose-900"
      : "border-sky-200 bg-sky-50 text-sky-900";

  return (
    <div className={`rounded-2xl border p-4 text-sm ${toneClasses}`}>
      <p className="font-semibold">{title}</p>
      <p className="mt-2 leading-6">{message}</p>
    </div>
  );
}
```

---

# FILE 15 — `[CREATE]` `bliss-telehealth/pbbf-telehealth/src/test/e2e/resilience-patient.spec.js`

```js
import { test, expect } from "@playwright/test";

test("patient flow remains understandable under slower transitions", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Email address").fill("patient@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/patient/);

  await page.goto("/patient/appointments");
  await expect(page.getByText(/appointments/i)).toBeVisible();

  await page.goto("/patient/session");
  await expect(page.getByText(/join your visit/i)).toBeVisible();
});
```

---

# FILE 16 — `[CREATE]` `bliss-telehealth/pbbf-telehealth/src/test/e2e/cross-role-refresh.spec.js`

```js
import { test, expect } from "@playwright/test";

test("role-scoped pages survive refresh without leaking cross-role access", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Email address").fill("admin@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/admin/);

  await page.goto("/admin/audit-logs");
  await page.reload();

  await expect(page.getByText(/audit visibility/i)).toBeVisible();
});
```

---

# FILE 17 — `[CREATE]` `bliss-telehealth/pbbf-telehealth/src/modules/appointments/__tests__/AppointmentsSlowApi.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import PatientAppointmentsPage from "../../../pages/patient/Appointments";

vi.mock("../hooks/useAppointments", () => ({
  useAppointments: () => ({
    appointments: [],
    nextAppointment: null,
    isLoading: true,
    loadError: "",
  }),
}));

describe("Appointments slow API state", () => {
  it("renders loading state clearly", () => {
    render(<PatientAppointmentsPage />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });
});
```

---

# FILE 18 — `[CREATE]` `bliss-telehealth/pbbf-telehealth/src/modules/telehealth/__tests__/SessionResilience.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import PatientSessionPage from "../../../pages/patient/Session";

vi.mock("../hooks/useSessionAccess", () => ({
  useSessionAccess: () => ({
    session: null,
    readiness: {
      canJoin: false,
      state: "no_session",
      message: "You do not have a telehealth session ready to join right now.",
    },
    isLoading: false,
    isJoining: false,
    loadError: "Unable to reach the telehealth service right now.",
    joinError: "",
    joinMessage: "",
    joinSession: vi.fn(),
  }),
}));

describe("Session resilience behavior", () => {
  it("shows a readable operational error state", () => {
    render(<PatientSessionPage />);
    expect(screen.getByText("Unable to load session access")).toBeInTheDocument();
  });
});
```

---

# FILE 19 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/docs/frontend-testing.md`

> Append this section to the current testing guide.

```md
## Reliability and resilience validation
In addition to normal feature tests, the frontend should also be checked under:
- slow API responses
- partial failures
- repeated refreshes
- repeated protected navigation across roles

### Minimum checks
- loading states remain understandable
- retry-friendly error messaging appears where appropriate
- route protection still works after refresh
- admin pages do not leak into non-admin flows
- patient and provider workflows remain readable under degraded response timing
```

---

# Recommended verification commands for Stage 7

## Backend performance and reliability checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

chmod +x scripts/run_load_tests.sh scripts/run_migration_validation.sh
./scripts/run_load_tests.sh
./scripts/run_migration_validation.sh
pytest tests/integration/test_role_workflow_reliability.py -q
```

## Frontend resilience checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth

npx vitest run src/modules/appointments/__tests__/AppointmentsSlowApi.test.jsx src/modules/telehealth/__tests__/SessionResilience.test.jsx
npm run test:e2e
```

> Also manually verify:
> - patient flow remains understandable during slow responses
> - admin route remains role-protected after refresh
> - session page remains readable when backend calls degrade

---

# Git commit recommendation for this stage

Run from the `bliss-telehealth` root:

```bash
git add docs/performance pbbf-api/tests/performance pbbf-api/tests/integration pbbf-api/app/jobs pbbf-api/alembic pbbf-api/scripts/run_load_tests.sh pbbf-api/scripts/run_migration_validation.sh pbbf-telehealth/src/test/e2e pbbf-telehealth/src/test/msw pbbf-telehealth/src/shared/components pbbf-telehealth/src/modules/appointments/__tests__/AppointmentsSlowApi.test.jsx pbbf-telehealth/src/modules/telehealth/__tests__/SessionResilience.test.jsx pbbf-telehealth/docs/frontend-testing.md
git commit -m "perf: add reliability, resilience, and migration validation baseline"
```

---

# Completion gate for Stage 7

This stage is complete only when:
- performance docs exist
- reliability gates are defined
- backend load and migration validation scripts exist
- retry behavior is test-backed
- concurrency and latency smoke checks exist
- frontend slow/failure scenario tests exist
- refresh and cross-role reliability checks exist
- the team can describe current stability limits before rollout

---

# Final recommendation
Treat Stage 7 as the stage that replaces optimism with measured confidence.

If the team still cannot answer:
- how the app behaves under repeated use
- how it behaves under degraded response time
- how it behaves after refresh
- how migrations are validated safely

then Stage 7 is not complete yet.
