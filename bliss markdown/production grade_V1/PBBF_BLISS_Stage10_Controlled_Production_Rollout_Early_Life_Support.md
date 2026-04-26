# PBBF BLISS — Phase 2 Stage 10 Populated Markdown Package
## Controlled Production Rollout and Early-Life Support

## Stage objective
Move from staging confidence to controlled real-world rollout with early monitoring and rapid response discipline.

This stage is where the product stops being only “ready to deploy” and becomes:
- intentionally released
- actively monitored
- operationally reviewed
- rollback-ready
- corrected quickly when real usage exposes issues

It is the stage that turns the first real rollout into a controlled operation instead of an uncontrolled launch.

---

## Stage outcomes

### Backend stage outcome
The backend supports:
- gradual release discipline
- post-deploy smoke validation
- active review of failures and incident signals
- audit-informed operational monitoring
- rollback readiness
- early-life support guidance after deployment

### Frontend stage outcome
The frontend supports:
- early detection of broken user flows
- clearer production-facing error feedback
- tracking of cross-role regressions
- real browser/device follow-up during rollout
- repeatable E2E checks for post-release validation

### Completion gate
The product is not just deployed — it is being actively operated, observed, and corrected under a controlled rollout plan.

---

## Repository root
`bliss-telehealth/`

---

# Stage 10 directory structure

```text
bliss-telehealth/
├── docs/
│   └── rollout/
│       ├── production-rollout-plan.md
│       ├── rollback-plan.md
│       ├── early-life-support-log.md
│       └── community-pilot-observation-log.md
├── pbbf-api/
│   ├── docs/
│   │   └── operations/
│   │       └── post-launch-monitoring.md
│   ├── scripts/
│   │   └── post_deploy_smoke.sh
│   └── tests/
│       └── smoke/
│           ├── test_backend_smoke.py
│           └── test_post_deploy_health.py
└── pbbf-telehealth/
    ├── docs/
    │   └── frontend-deployment.md
    ├── src/
    │   ├── test/
    │   │   └── e2e/
    │   │       ├── patient-flow.spec.js
    │   │       ├── provider-flow.spec.js
    │   │       ├── admin-flow.spec.js
    │   │       └── post-release-smoke.spec.js
    │   └── shared/
    │       ├── hooks/
    │       │   └── useToast.js
    │       └── components/
    │           └── ErrorState.jsx
```

---

# Recommended commands to create missing directories

Run from the `bliss-telehealth` root:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth

mkdir -p docs/rollout
mkdir -p pbbf-api/docs/operations
mkdir -p pbbf-api/scripts
mkdir -p pbbf-api/tests/smoke
mkdir -p pbbf-telehealth/docs
mkdir -p pbbf-telehealth/src/test/e2e
mkdir -p pbbf-telehealth/src/shared/hooks
mkdir -p pbbf-telehealth/src/shared/components
```

---

# FILE 1 — `[CREATE]` `bliss-telehealth/docs/rollout/production-rollout-plan.md`

```md
# PBBF BLISS Production Rollout Plan

## Purpose
This document defines how the platform should move from validated staging state into controlled real-world rollout.

## Core rollout principle
Do not treat production as a one-time event. Treat it as a controlled transition with observation points, rollback readiness, and active follow-up.

## Rollout phases

### Phase A — Final pre-release confirmation
- confirm staging sign-off
- confirm smoke checks are current
- confirm runbooks exist
- confirm rollback path is known
- confirm responsible engineers are identified

### Phase B — Initial controlled release
- release backend and frontend intentionally
- validate health and readiness immediately
- validate core patient/provider/admin route availability
- capture first operational evidence in the early-life support log

### Phase C — Active observation window
- monitor health endpoint results
- monitor logs and audit signals
- review reported defects or regressions
- review major role workflows for breakage
- capture issues and mitigation actions

### Phase D — Stabilization and adjustment
- fix urgent issues
- re-run smoke checks
- document any operational changes
- update rollout status

## Required go-live checklist
- production environment variables validated
- smoke checks documented
- backup posture confirmed
- rollback plan approved
- operational owner identified
- known critical defects resolved or explicitly accepted

## Rule
Do not widen rollout confidence until early-life monitoring confirms the system is behaving acceptably in real use.
```

---

# FILE 2 — `[CREATE]` `bliss-telehealth/docs/rollout/rollback-plan.md`

```md
# PBBF BLISS Rollback Plan

## Purpose
This document defines the minimum rollback posture required for controlled rollout.

## Core principle
Rollback is not failure. Rollback is a safety control.

## When rollback should be considered
- critical role workflow fails after release
- login or auth behavior breaks broadly
- health or readiness checks fail persistently
- major route protection regression appears
- backend boot becomes unstable
- production issue cannot be mitigated fast enough in place

## Rollback checklist
1. identify release version causing the problem
2. halt further rollout activity
3. confirm whether issue is backend, frontend, or both
4. revert to the last known-good version
5. re-run health and readiness checks
6. re-run basic role workflow smoke checks
7. document rollback reason and time
8. create follow-up remediation item

## Required rollback evidence
- version rolled back from
- version rolled back to
- reason for rollback
- affected roles or workflows
- validation checks performed after rollback

## Rule
A release is not operationally safe unless rollback is both documented and practically executable.
```

---

# FILE 3 — `[CREATE]` `bliss-telehealth/docs/rollout/early-life-support-log.md`

```md
# PBBF BLISS Early-Life Support Log

## Purpose
This log is used immediately after rollout to capture real operational observations, issues, and corrective actions.

## Template

| ID | Date/Time | Area | Role affected | Observation / issue | Severity | Action taken | Status | Owner |
|---|---|---|---|---|---|---|---|---|
| ELS-001 | YYYY-MM-DD HH:MM | backend/frontend/workflow | patient/provider/admin | example issue | Critical/High/Medium/Low | mitigation | Open/Monitoring/Resolved | owner |

## Logging rules
- record issues as they happen
- keep workflow context explicit
- capture mitigation, not only symptoms
- update status after retest
- link major issues to incident or defect records when appropriate
```

---

# FILE 4 — `[CREATE]` `bliss-telehealth/docs/rollout/community-pilot-observation-log.md`

```md
# PBBF BLISS Community Pilot Observation Log

## Purpose
This log captures controlled rollout observations during real pilot use.

## What to record
- role and workflow context
- repeated confusion points
- browser or device-specific problems
- slow or broken user journeys
- operational misunderstandings
- improvement opportunities discovered in real use

## Template

| ID | Date | Role | Workflow | Observation | Impact | Follow-up needed | Owner |
|---|---|---|---|---|---|---|---|
| PILOT-001 | YYYY-MM-DD | patient/provider/admin | example workflow | example note | Low/Medium/High | yes/no | owner |

## Rule
Pilot observations are not noise. They are controlled learning signals for post-release stabilization.
```

---

# FILE 5 — `[CREATE]` `bliss-telehealth/pbbf-api/docs/operations/post-launch-monitoring.md`

```md
# Backend Post-Launch Monitoring Guide

## Purpose
This document defines what the backend team should watch immediately after controlled production rollout.

## Minimum monitoring signals
- health endpoint status
- readiness endpoint status
- startup and request lifecycle logs
- auth failures
- permission denials
- unhandled exceptions
- audit-write behavior
- post-deploy smoke results

## Review cadence
### Immediately after deploy
- confirm health
- confirm readiness
- confirm one protected route still behaves correctly

### During early-life support window
- review logs for repeated failure patterns
- review request IDs tied to reported incidents
- review whether one role is affected more than others
- review whether failures correlate to recent deploy changes

## Backend action rule
If repeated severe failure appears and cannot be mitigated quickly, escalate to rollback review.
```

---

# FILE 6 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/scripts/post_deploy_smoke.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:8000}"

echo "[INFO] Running post-deploy smoke checks against ${BASE_URL}"

echo "[INFO] Checking /api/v1/health"
curl -fsS "${BASE_URL}/api/v1/health" >/dev/null

echo "[INFO] Checking /api/v1/ready"
curl -fsS "${BASE_URL}/api/v1/ready" >/dev/null

echo "[OK] Post-deploy smoke checks passed."
```

---

# FILE 7 — `[UPDATE GUIDANCE]` `bliss-telehealth/pbbf-api/tests/smoke/`

> Keep the Stage 9 smoke files and use Stage 10 to make them part of the rollout discipline.

Required smoke set:
- `test_backend_smoke.py`
- `test_post_deploy_health.py`

## Stage 10 expectation
These tests should now be treated as part of:
- post-release confirmation
- rollback validation
- early-life support evidence

No full replacement is required if your Stage 9 smoke tests already exist and are correct.
```

---

# FILE 8 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/docs/frontend-deployment.md`

> Append this section to the current frontend deployment guide.

```md
## Controlled production rollout reminder
After production deployment, the team should:
- verify login and main dashboards for patient, provider, and admin
- verify nested route refresh behavior
- confirm frontend points to the correct production backend
- review visible error-state behavior
- log early-life issues in the rollout support log
```

---

# FILE 9 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/shared/hooks/useToast.js`

> Replace or merge into the current file so production-facing operational feedback remains structured and dismissible during early-life support.

```jsx
import { useCallback, useEffect, useState } from "react";

let listeners = new Set();
let toastQueue = [];

function emit() {
  listeners.forEach((listener) => listener([...toastQueue]));
}

function dismissToast(id) {
  toastQueue = toastQueue.filter((toast) => toast.id !== id);
  emit();
}

function pushToast(toast) {
  const entry = {
    id: toast?.id || `toast-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
    type: toast?.type || "info",
    title: toast?.title || "",
    message: toast?.message || "",
    duration: toast?.duration ?? 3500,
  };

  toastQueue = [...toastQueue, entry];
  emit();

  if (entry.duration > 0) {
    window.setTimeout(() => dismissToast(entry.id), entry.duration);
  }

  return entry.id;
}

export function useToast() {
  const [toasts, setToasts] = useState(toastQueue);

  useEffect(() => {
    const listener = (items) => setToasts(items);
    listeners.add(listener);
    return () => listeners.delete(listener);
  }, []);

  const success = useCallback((message, title = "Success") => {
    return pushToast({ type: "success", title, message });
  }, []);

  const error = useCallback((message, title = "Error") => {
    return pushToast({ type: "error", title, message, duration: 5000 });
  }, []);

  const info = useCallback((message, title = "Info") => {
    return pushToast({ type: "info", title, message });
  }, []);

  return {
    toasts,
    success,
    error,
    info,
    dismiss: dismissToast,
  };
}
```

---

# FILE 10 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/shared/components/ErrorState.jsx`

> Replace or merge into the current file so production-facing failures remain readable without leaking unsafe details.

```jsx
export default function ErrorState({
  title = "Something went wrong",
  message = "An unexpected issue occurred while loading this part of the application.",
  retryLabel = "",
  onRetry = null,
}) {
  return (
    <section className="rounded-3xl border border-rose-200 bg-rose-50 p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-rose-900">{title}</h2>
      <p className="mt-3 text-sm leading-6 text-rose-800">{message}</p>

      {retryLabel && onRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className="mt-5 rounded-xl bg-white px-4 py-3 text-sm font-semibold text-rose-800 transition hover:bg-rose-100"
        >
          {retryLabel}
        </button>
      ) : null}
    </section>
  );
}
```

---

# FILE 11 — `[UPDATE GUIDANCE]` `bliss-telehealth/pbbf-telehealth/src/test/e2e/`

> Keep the Stage 8 role-flow specs and add one rollout-smoke-oriented E2E file.

Required E2E set:
- `patient-flow.spec.js`
- `provider-flow.spec.js`
- `admin-flow.spec.js`
- `post-release-smoke.spec.js`

---

# FILE 12 — `[CREATE]` `bliss-telehealth/pbbf-telehealth/src/test/e2e/post-release-smoke.spec.js`

```js
import { test, expect } from "@playwright/test";

test("post-release smoke validates main entry points", async ({ page }) => {
  await page.goto("/login");
  await expect(page.getByText(/sign in/i)).toBeVisible();

  await page.getByLabel("Email address").fill("admin@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/admin/);
  await expect(page.getByText(/platform oversight dashboard/i)).toBeVisible();
});
```

---

# Recommended verification commands for Stage 10

## Backend rollout checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

chmod +x scripts/post_deploy_smoke.sh
./scripts/post_deploy_smoke.sh http://127.0.0.1:8000
pytest tests/smoke -q
```

## Frontend rollout checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth

npm run test:e2e
npm run build
```

> Then manually verify:
> - patient login and dashboard path
> - provider login and main workspace path
> - admin login and oversight path
> - nested route refresh still works
> - visible errors remain readable on degraded pages

---

# Git commit recommendation for this stage

Run from the `bliss-telehealth` root:

```bash
git add docs/rollout pbbf-api/docs/operations/post-launch-monitoring.md pbbf-api/scripts/post_deploy_smoke.sh pbbf-api/tests/smoke pbbf-telehealth/docs/frontend-deployment.md pbbf-telehealth/src/test/e2e pbbf-telehealth/src/shared/hooks/useToast.js pbbf-telehealth/src/shared/components/ErrorState.jsx
git commit -m "rollout: add controlled production rollout and early-life support baseline"
```

---

# Completion gate for Stage 10

This stage is complete only when:
- rollout docs exist
- rollback plan exists
- early-life support log exists
- pilot observation log exists
- backend post-launch monitoring guide exists
- post-deploy smoke script exists
- frontend deployment guide reflects controlled rollout checks
- frontend E2E smoke coverage includes a post-release check
- the team is actively observing and documenting early rollout behavior

---

# Final recommendation
Treat Stage 10 as the stage that proves the system is being operated, not merely hosted.

If the team still cannot answer:
- how rollout is observed
- how issues are logged after release
- how rollback is triggered
- how post-deploy smoke is performed
- how real pilot observations are recorded

then Stage 10 is not complete yet.
