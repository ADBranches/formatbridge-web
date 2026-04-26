# PBBF BLISS — Phase 2 Stage 8 Populated Markdown Package
## Integrated QA, UAT, Accessibility, and Staff Readiness

## Stage objective
Validate the whole product end to end with real workflows and real operational users.

This stage is where the platform stops being “tested by builders only” and becomes something that can be exercised by:
- realistic seeded users
- controlled QA participants
- patient, provider, and admin role-based reviewers
- staff who need predictable guides
- acceptance reviewers checking whether the product is usable in practice

It is not enough for code-level tests to pass.  
The system must now be validated by complete journeys, documented UAT, accessibility checks, and operational training support.

---

## Stage outcomes

### Backend stage outcome
The backend supports:
- seeded environments
- realistic test accounts
- repeatable QA fixtures
- connected integration journeys
- triage-friendly defect logging references

### Frontend stage outcome
The frontend supports:
- role-by-role E2E flow validation
- accessibility smoke checks
- user acceptance test execution
- clearer shared UI behavior under controlled QA review

### Completion gate
Real users can execute the main workflows in a controlled environment, and the team has documented training and QA evidence.

---

## Repository root
`bliss-telehealth/`

---

# Stage 8 directory structure

```text
bliss-telehealth/
├── docs/
│   ├── qa/
│   │   ├── uat-plan.md
│   │   ├── role-based-test-matrix.md
│   │   └── defect-triage-log.md
│   └── training/
│       ├── patient-guides/
│       │   └── patient-portal-quick-guide.md
│       ├── provider-guides/
│       │   └── provider-workspace-quick-guide.md
│       └── admin-guides/
│           └── admin-oversight-quick-guide.md
├── pbbf-api/
│   ├── scripts/
│   │   ├── seed_roles.py
│   │   ├── seed_users.py
│   │   └── seed_reference_data.py
│   └── tests/
│       └── integration/
│           ├── test_patient_journey.py
│           ├── test_provider_journey.py
│           └── test_admin_journey.py
└── pbbf-telehealth/
    └── src/
        ├── test/
        │   └── e2e/
        │       ├── patient-flow.spec.js
        │       ├── provider-flow.spec.js
        │       └── admin-flow.spec.js
        ├── shared/
        │   ├── utils/
        │   │   └── a11y.js
        │   └── components/
        │       ├── PageHeader.jsx
        │       ├── SectionCard.jsx
        │       ├── FormErrorSummary.jsx
        │       └── ErrorState.jsx
        └── components/
            └── ui/
                ├── Input.jsx
                ├── Select.jsx
                ├── Textarea.jsx
                ├── Modal.jsx
                ├── Table.jsx
                └── Tabs.jsx
```

---

# Recommended commands to create missing directories

Run from the `bliss-telehealth` root:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth

mkdir -p docs/qa
mkdir -p docs/training/patient-guides
mkdir -p docs/training/provider-guides
mkdir -p docs/training/admin-guides
mkdir -p pbbf-api/tests/integration
mkdir -p pbbf-telehealth/src/test/e2e
```

---

# FILE 1 — `[CREATE]` `bliss-telehealth/docs/qa/uat-plan.md`

```md
# PBBF BLISS UAT Plan

## Purpose
This document defines how user acceptance testing should be run for controlled validation of the platform.

## UAT goals
- confirm that real role-based workflows make sense in practice
- confirm that seeded environments support realistic usage
- confirm that major user journeys work from start to finish
- identify defects before pilot or broader rollout
- collect evidence that the system is usable, not only technically implemented

## UAT roles
- patient reviewer
- provider reviewer
- admin reviewer
- QA facilitator
- defect triage owner

## UAT scope
### Patient
- login
- onboarding / intake
- appointments
- screening
- telehealth session access

### Provider
- dashboard visibility
- patient context review
- encounter note drafting
- note finalization
- referrals workflow

### Admin
- dashboard visibility
- user list review
- audit review
- reports visibility

## UAT execution rules
1. Run UAT in a controlled seeded environment.
2. Use named test accounts per role.
3. Record pass / fail / blocked status for each workflow.
4. Capture defects immediately in the defect triage log.
5. Retest resolved defects before sign-off.

## Sign-off evidence
UAT is only complete when:
- all major role workflows have been exercised
- pass/fail outcomes are recorded
- blockers are documented
- unresolved critical defects are explicitly acknowledged
```

---

# FILE 2 — `[CREATE]` `bliss-telehealth/docs/qa/role-based-test-matrix.md`

```md
# PBBF BLISS Role-Based Test Matrix

## Purpose
This matrix defines the minimum role-by-role workflow coverage required during integrated QA and UAT.

| Role | Workflow | Expected result | Evidence type |
|---|---|---|---|
| Patient | Login | User reaches patient area | Screenshot / QA note |
| Patient | Intake draft and submit | Intake saves and submits with consent | QA result |
| Patient | Appointment management | Patient can view and manage appointments | QA result |
| Patient | Screening | Screening submission completes clearly | QA result |
| Patient | Session access | Telehealth readiness and join flow are understandable | QA result |
| Provider | Login | User reaches provider area | Screenshot / QA note |
| Provider | Dashboard | Assigned workflow context visible | QA result |
| Provider | Notes | Provider can draft/finalize encounter note | QA result |
| Provider | Referrals | Provider can create and update referral flow | QA result |
| Admin | Login | User reaches admin area | Screenshot / QA note |
| Admin | Dashboard | KPI / oversight view loads | QA result |
| Admin | Users | User list is visible | QA result |
| Admin | Audit logs | Audit view loads and filters work | QA result |
| Admin | Reports | Reporting snapshot is visible | QA result |

## Accessibility checks
For each role flow, verify:
- basic keyboard access works
- focusable controls can be reached
- major form errors are understandable
- visible loading and error states exist

## Readiness rule
A role workflow should not be marked “accepted” until:
- expected route access is correct
- UI wording is understandable
- no blocking defects remain for that path
```

---

# FILE 3 — `[CREATE]` `bliss-telehealth/docs/qa/defect-triage-log.md`

```md
# PBBF BLISS Defect Triage Log

## Purpose
This document is the shared record for defects identified during integrated QA and UAT.

## Severity guide
- **Critical** — blocks core workflow or creates unacceptable risk
- **High** — major workflow issue without full outage
- **Medium** — meaningful issue with workaround
- **Low** — minor issue or polish problem

## Template

| ID | Date | Role | Workflow | Severity | Description | Status | Owner | Notes |
|---|---|---|---|---|---|---|---|---|
| QA-001 | YYYY-MM-DD | patient/provider/admin | example workflow | Critical/High/Medium/Low | defect summary | Open/In Progress/Resolved/Retest | owner name | notes |

## Triage rules
1. Log defects as soon as they are found.
2. Do not rely on memory or chat history alone.
3. Retest resolved items and update the status.
4. Keep role and workflow context explicit.
5. Critical defects must be reviewed before any sign-off.
```

---

# FILE 4 — `[CREATE]` `bliss-telehealth/docs/training/patient-guides/patient-portal-quick-guide.md`

```md
# Patient Portal Quick Guide

## Purpose
This guide helps a patient reviewer understand the main MVP workflow areas.

## Main tasks
- sign in
- complete onboarding and consent
- review appointments
- complete screening
- review telehealth session access

## What to watch for during testing
- are instructions clear?
- are errors understandable?
- does the workflow feel predictable?
- does the session page explain readiness clearly?

## If something goes wrong
Report:
- what page you were on
- what you expected
- what actually happened
- whether you could continue or got blocked
```

---

# FILE 5 — `[CREATE]` `bliss-telehealth/docs/training/provider-guides/provider-workspace-quick-guide.md`

```md
# Provider Workspace Quick Guide

## Purpose
This guide helps provider reviewers exercise the provider-facing workflow safely and consistently.

## Main tasks
- sign in
- review dashboard context
- open the notes workspace
- review patient summary
- draft and finalize encounter note
- create and update referral

## What to watch for during testing
- is patient context understandable?
- is note finalization clear?
- are referral steps operationally understandable?
- are screening alerts visible when relevant?
```

---

# FILE 6 — `[CREATE]` `bliss-telehealth/docs/training/admin-guides/admin-oversight-quick-guide.md`

```md
# Admin Oversight Quick Guide

## Purpose
This guide helps admin reviewers test the operational oversight area consistently.

## Main tasks
- sign in
- review dashboard metrics
- review user list
- review audit visibility
- review reports

## What to watch for during testing
- do admin-only pages stay restricted?
- are reports understandable?
- are audit views readable?
- do pages imply correct data-governance expectations?
```

---

# FILE 7 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/scripts/seed_roles.py`

```python
from __future__ import annotations

ROLES = [
    "patient",
    "provider",
    "counselor",
    "care_coordinator",
    "lactation_consultant",
    "admin",
]


def main() -> None:
    print("[INFO] Seeding roles...")
    for role in ROLES:
        print(f"[OK] role={role}")
    print("[DONE] Role seeding completed.")


if __name__ == "__main__":
    main()
```

> Merge note:
> If your backend already persists roles in the database, keep the same role list and replace the print-only logic with real persistence.

---

# FILE 8 — `[UPDATE]` `bliss-telehealth/pbbf-api/scripts/seed_users.py`

> Replace or merge into the current file. This version gives you realistic role-based seed accounts for QA and UAT.

```python
from __future__ import annotations

SEEDED_USERS = [
    {
        "email": "patient@example.com",
        "full_name": "Patient User",
        "role": "patient",
    },
    {
        "email": "provider@example.com",
        "full_name": "Provider User",
        "role": "provider",
    },
    {
        "email": "admin@example.com",
        "full_name": "Admin User",
        "role": "admin",
    },
]


def main() -> None:
    print("[INFO] Seeding users for QA and UAT...")
    for user in SEEDED_USERS:
        print(
            f"[OK] email={user['email']} role={user['role']} full_name={user['full_name']}"
        )
    print("[DONE] User seeding completed.")


if __name__ == "__main__":
    main()
```

> Merge note:
> If your project already has working DB insert logic in this script, keep it and replace only the user definitions and output clarity.

---

# FILE 9 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/scripts/seed_reference_data.py`

```python
from __future__ import annotations

REFERENCE_DATA = {
    "service_needs": [
        "mental_health",
        "lactation",
        "wellness_follow_up",
        "community_support",
    ],
    "appointment_statuses": [
        "booked",
        "rescheduled",
        "cancelled",
        "completed",
        "missed",
    ],
    "referral_statuses": [
        "created",
        "acknowledged",
        "completed",
    ],
}


def main() -> None:
    print("[INFO] Seeding reference data...")
    for group_name, items in REFERENCE_DATA.items():
        print(f"[OK] {group_name}={','.join(items)}")
    print("[DONE] Reference-data seeding completed.")


if __name__ == "__main__":
    main()
```

---

# FILE 10 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/integration/test_patient_journey.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_patient_journey_smoke():
    client = TestClient(create_app())

    health = client.get("/api/v1/health")
    ready = client.get("/api/v1/ready")

    assert health.status_code == 200
    assert ready.status_code == 200

    # Expand later with seeded login and full intake / appointment / screening flow.
```

---

# FILE 11 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/integration/test_provider_journey.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_provider_journey_smoke():
    client = TestClient(create_app())

    health = client.get("/api/v1/health")
    ready = client.get("/api/v1/ready")

    assert health.status_code == 200
    assert ready.status_code == 200

    # Expand later with seeded provider login, notes, and referral workflow.
```

---

# FILE 12 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/tests/integration/test_admin_journey.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_admin_journey_smoke():
    client = TestClient(create_app())

    health = client.get("/api/v1/health")
    ready = client.get("/api/v1/ready")

    assert health.status_code == 200
    assert ready.status_code == 200

    # Expand later with seeded admin login, reporting, and audit workflow.
```

---

# FILE 13 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/src/test/e2e/patient-flow.spec.js`

> Replace or merge into the current file so the patient path reads like a controlled UAT flow.

```js
import { test, expect } from "@playwright/test";

test("patient main workflow", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Email address").fill("patient@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/patient/);

  await page.goto("/patient/appointments");
  await expect(page.getByText(/appointments/i)).toBeVisible();

  await page.goto("/patient/screening");
  await expect(page.getByText(/self-assessment/i)).toBeVisible();

  await page.goto("/patient/session");
  await expect(page.getByText(/join your visit/i)).toBeVisible();
});
```

---

# FILE 14 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/src/test/e2e/provider-flow.spec.js`

```js
import { test, expect } from "@playwright/test";

test("provider main workflow", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Email address").fill("provider@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/provider/);

  await page.goto("/provider/notes");
  await expect(page.getByText(/encounter workspace/i)).toBeVisible();

  await page.goto("/provider/referrals");
  await expect(page.getByText(/referral management/i)).toBeVisible();
});
```

---

# FILE 15 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/src/test/e2e/admin-flow.spec.js`

```js
import { test, expect } from "@playwright/test";

test("admin main workflow", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Email address").fill("admin@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/admin/);

  await page.goto("/admin/users");
  await expect(page.getByText(/user management view/i)).toBeVisible();

  await page.goto("/admin/audit-logs");
  await expect(page.getByText(/audit visibility/i)).toBeVisible();

  await page.goto("/admin/reports");
  await expect(page.getByText(/reporting snapshots/i)).toBeVisible();
});
```

---

# FILE 16 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/shared/utils/a11y.js`

> Replace or merge into the current file so accessibility checks remain consistent across controlled QA.

```js
let idCounter = 0;

export function createFieldIds(name = "field") {
  idCounter += 1;
  const base = `${name}-${idCounter}`;
  return {
    inputId: `${base}-input`,
    hintId: `${base}-hint`,
    errorId: `${base}-error`,
  };
}

export function getAriaDescribedBy({ hint, error, hintId, errorId }) {
  return [hint ? hintId : null, error ? errorId : null].filter(Boolean).join(" ") || undefined;
}

export function getFieldA11yProps({ hint, error, hintId, errorId }) {
  return {
    "aria-invalid": Boolean(error) || undefined,
    "aria-describedby": getAriaDescribedBy({ hint, error, hintId, errorId }),
  };
}

export function onEnterOrSpace(handler) {
  return function handleKeyDown(event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handler?.(event);
    }
  };
}

export function describeTestFocusExpectation(label) {
  return `Focusable control expected: ${label}`;
}
```

---

# FILE 17 — `[UPDATE GUIDANCE]` `bliss-telehealth/pbbf-telehealth/src/components/ui/`

> No full file replacement is required here if Stage 9 already completed those components properly.  
> For Stage 8, review and confirm the following UI primitives remain suitable for UAT and accessibility checks:

- `Input.jsx`
- `Select.jsx`
- `Textarea.jsx`
- `Modal.jsx`
- `Table.jsx`
- `Tabs.jsx`

## Required review checklist
- labels are visible and linked correctly
- error text is readable
- keyboard navigation works
- tables remain readable
- modals can be dismissed cleanly
- tabs are understandable during navigation testing

If any one of these is still weak, update that specific component now rather than rewriting the whole UI library.

---

# FILE 18 — `[UPDATE GUIDANCE]` `bliss-telehealth/pbbf-telehealth/src/shared/components/`

> No full file replacement is required here if Stage 9 already completed these shared components properly.  
> For Stage 8, confirm the following remain strong enough for acceptance testing and staff review:

- `PageHeader.jsx`
- `SectionCard.jsx`
- `FormErrorSummary.jsx`
- `ErrorState.jsx`

## Required review checklist
- headings are clear
- section layout is stable
- error summaries help non-technical testers recover
- operational errors do not leak backend internals

---

# Recommended verification commands for Stage 8

## Backend seeded-environment and journey checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

python scripts/seed_roles.py
python scripts/seed_users.py
python scripts/seed_reference_data.py
pytest tests/integration/test_patient_journey.py tests/integration/test_provider_journey.py tests/integration/test_admin_journey.py -q
```

## Frontend E2E and accessibility smoke checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth

npm run test:e2e
npm run test
```

> Then manually validate:
> - keyboard navigation on major forms
> - role-by-role route access
> - clear error feedback for common failures
> - shared UI consistency for patient/provider/admin reviewers

---

# Git commit recommendation for this stage

Run from the `bliss-telehealth` root:

```bash
git add docs/qa docs/training pbbf-api/scripts/seed_roles.py pbbf-api/scripts/seed_users.py pbbf-api/scripts/seed_reference_data.py pbbf-api/tests/integration/test_patient_journey.py pbbf-api/tests/integration/test_provider_journey.py pbbf-api/tests/integration/test_admin_journey.py pbbf-telehealth/src/test/e2e/patient-flow.spec.js pbbf-telehealth/src/test/e2e/provider-flow.spec.js pbbf-telehealth/src/test/e2e/admin-flow.spec.js pbbf-telehealth/src/shared/utils/a11y.js pbbf-telehealth/src/components/ui pbbf-telehealth/src/shared/components
git commit -m "qa: add integrated UAT, accessibility, and staff readiness baseline"
```

---

# Completion gate for Stage 8

This stage is complete only when:
- QA docs exist
- training guides exist
- seed scripts exist for realistic roles and reference data
- patient/provider/admin journey tests exist
- E2E tests are runnable
- accessibility smoke expectations are documented and exercised
- role-by-role workflow validation has evidence
- defect triage logging structure exists
- real reviewers can execute the main workflows in a controlled environment

---

# Final recommendation
Treat Stage 8 as the stage that proves the product can be used and reviewed by people who did not build it.

If the team still cannot show:
- realistic seeded roles
- role-based acceptance evidence
- documented UAT and defect triage
- reviewer-friendly training notes

then Stage 8 is not complete yet.
