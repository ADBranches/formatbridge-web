# PBBF BLISS Frontend — Phase 10 Populated Files
## Integration, E2E Readiness, and Deployment Support

## Objective
Prepare the frontend for staging and real integrated QA.

Repository root:

`bliss-telehealth/pbbf-telehealth`

This phase makes the frontend safer to validate in realistic conditions by adding:

- mocked integration support with MSW
- E2E test skeletons for patient, provider, and admin flows
- environment templates
- testing and deployment docs
- package scripts for local QA and staging packaging
- Vite and ESLint support for the testing layer

---

## Phase 10 decisions

### 1. Mocked integration strategy
Use **MSW** for frontend integration-style tests so the UI can be tested without depending on a live backend during every local run.

### 2. E2E strategy
Use **Playwright** for browser-based end-to-end tests.

This matches the file style you requested:

- `patient-flow.spec.js`
- `provider-flow.spec.js`
- `admin-flow.spec.js`

### 3. Environment strategy
Use:

- `.env.example`

as the committed reference file, and keep real `.env` files uncommitted.

### 4. Deployment target assumption
This frontend remains a Vite-built React app that can be packaged as static assets for staging deployment behind a web server or served by a platform that supports static frontends.

### 5. Central architecture rule
Continue the same rule from Phase 9:

- API services make requests
- hooks normalize data
- pages compose sections
- do not scatter mapping logic inside pages

This phase adds test infrastructure around that rule; it does not replace it.

---

## Directories to modify
- `src`
- `public`
- project root config files

## Modify these files
- `package.json`
- `vite.config.js`
- `eslint.config.js`
- `README.md`

## Create these files if missing
- `src/test/msw/server.js`
- `src/test/msw/handlers.js`
- `src/test/e2e/patient-flow.spec.js`
- `src/test/e2e/provider-flow.spec.js`
- `src/test/e2e/admin-flow.spec.js`
- `.env.example`
- `docs/frontend-testing.md`
- `docs/frontend-deployment.md`

## Recommended support patch
Because you already created `src/test/setup.jsx` in earlier phases, this phase should also patch that existing file so MSW starts automatically for mocked integration tests.

---

# 1) `package.json`

Use this as the target shape or merge the relevant parts into your existing file.

```json
{
  "name": "pbbf-telehealth",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:ui": "vitest --ui",
    "test:e2e": "playwright test",
    "test:e2e:headed": "playwright test --headed",
    "test:all": "npm run test && npm run test:e2e"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@eslint/js": "^9.0.0",
    "@playwright/test": "^1.52.0",
    "@testing-library/jest-dom": "^6.6.0",
    "@testing-library/react": "^16.0.0",
    "@testing-library/user-event": "^14.5.2",
    "@vitest/coverage-v8": "^2.1.0",
    "eslint": "^9.0.0",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-react-refresh": "^0.4.12",
    "globals": "^15.0.0",
    "jsdom": "^25.0.0",
    "msw": "^2.7.0",
    "vite": "^6.0.0",
    "vitest": "^2.1.0"
  }
}
```

## Notes
- Keep any existing dependencies you already have.
- Add:
  - `msw`
  - `@playwright/test`
- Keep your existing UI/testing packages if they are already present.

---

# 2) `vite.config.js`

This version enables Vite test configuration directly.

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
  preview: {
    host: "0.0.0.0",
    port: 4173,
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/test/setup.jsx",
    css: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
    },
  },
});
```

---

# 3) `eslint.config.js`

Merge this shape into your current ESLint flat config if you already have one.

```js
import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";

export default [
  {
    ignores: ["dist", "coverage", "playwright-report", "test-results"],
  },
  js.configs.recommended,
  {
    files: ["**/*.{js,jsx}"],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: "module",
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "react-refresh/only-export-components": ["warn", { allowConstantExport: true }],
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
    },
  },
  {
    files: ["src/test/**/*.{js,jsx}", "**/*.test.{js,jsx}", "**/*.spec.{js,jsx}"],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        describe: true,
        it: true,
        expect: true,
        beforeAll: true,
        afterAll: true,
        afterEach: true,
        beforeEach: true,
        vi: true,
      },
    },
  },
];
```

---

# 4) Patch existing file: `src/test/setup.jsx`

This is the recommended Phase 10 support patch so mocked integration tests actually use MSW.

```jsx
import "@testing-library/jest-dom";
import { afterAll, afterEach, beforeAll } from "vitest";
import { server } from "./msw/server";

beforeAll(() => {
  server.listen({ onUnhandledRequest: "warn" });
});

afterEach(() => {
  server.resetHandlers();
});

afterAll(() => {
  server.close();
});
```

---

# 5) `src/test/msw/handlers.js`

These handlers provide mocked data for core patient, provider, and admin flows.

```js
import { http, HttpResponse } from "msw";

const API_BASE_URL =
  (import.meta?.env?.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1").replace(/\/$/, "");

function ok(data, message = "Request successful.") {
  return HttpResponse.json({
    message,
    data,
  });
}

export const handlers = [
  http.post(`${API_BASE_URL}/auth/login`, async ({ request }) => {
    const body = await request.json();
    const email = body?.email || "";

    let role = "patient";
    if (email.includes("provider")) role = "provider";
    if (email.includes("admin")) role = "admin";

    return ok(
      {
        access_token: "mock-access-token",
        refresh_token: "mock-refresh-token",
        user: {
          id: `${role}-1`,
          full_name:
            role === "admin"
              ? "Admin User"
              : role === "provider"
              ? "Provider User"
              : "Patient User",
          email,
          role,
        },
      },
      "Login successful."
    );
  }),

  http.post(`${API_BASE_URL}/auth/register`, async ({ request }) => {
    const body = await request.json();

    return ok(
      {
        access_token: "mock-access-token",
        refresh_token: "mock-refresh-token",
        user: {
          id: "patient-1",
          full_name: body?.full_name || "Patient User",
          email: body?.email || "patient@example.com",
          role: body?.role || "patient",
        },
      },
      "Registration successful."
    );
  }),

  http.get(`${API_BASE_URL}/auth/me`, () => {
    return ok({
      user: {
        id: "patient-1",
        full_name: "Patient User",
        email: "patient@example.com",
        role: "patient",
      },
    });
  }),

  http.get(`${API_BASE_URL}/intake/me`, () => {
    return ok({
      intake: {
        status: "submitted",
        full_name: "Patient User",
        preferred_contact_method: "email",
        service_needs: ["mental_health"],
        consent_accepted: true,
        privacy_accepted: true,
      },
    });
  }),

  http.get(`${API_BASE_URL}/appointments`, () => {
    return ok({
      appointments: [
        {
          id: "appt-1",
          patient_id: "patient-1",
          patient_name: "Patient User",
          service_type: "mental_health",
          visit_reason: "Follow-up counseling visit",
          scheduled_at: "2026-05-10T10:00:00Z",
          timezone: "Africa/Kampala",
          provider_name: "Provider User",
          status: "booked",
          location_label: "Virtual visit",
          screening_alert_level: "moderate",
          screening_alert_text: "Recent screening requires provider review.",
        },
      ],
    });
  }),

  http.post(`${API_BASE_URL}/appointments`, async ({ request }) => {
    const body = await request.json();

    return ok(
      {
        id: "appt-2",
        service_type: body?.service_type,
        visit_reason: body?.visit_reason,
        scheduled_at: body?.scheduled_at,
        timezone: body?.timezone || "Africa/Kampala",
        status: "booked",
      },
      "Appointment booked successfully."
    );
  }),

  http.patch(`${API_BASE_URL}/appointments/:appointmentId/reschedule`, () => {
    return ok({}, "Appointment rescheduled successfully.");
  }),

  http.patch(`${API_BASE_URL}/appointments/:appointmentId/cancel`, () => {
    return ok({}, "Appointment cancelled successfully.");
  }),

  http.get(`${API_BASE_URL}/screenings/me`, () => {
    return ok({
      screenings: [
        {
          id: "screen-1",
          submitted_at: "2026-05-01T10:00:00Z",
          score: 8,
          band: "lower concern range",
          safety_flag: false,
        },
      ],
    });
  }),

  http.post(`${API_BASE_URL}/screenings/epds`, () => {
    return ok(
      {
        score: 8,
        band: "lower concern range",
        safety_flag: false,
      },
      "Your screening has been submitted successfully."
    );
  }),

  http.get(`${API_BASE_URL}/telehealth/sessions/next`, () => {
    return ok({
      session: {
        id: "session-1",
        appointment_id: "appt-1",
        appointment_time: "2026-05-10T10:00:00Z",
        session_status: "ready",
        provider_name: "Provider User",
        service_type: "Telehealth follow-up",
        join_url: "https://example.test/join/session-1",
        reminder_message:
          "Your next visit is coming up. Please review your device readiness before joining.",
      },
    });
  }),

  http.post(`${API_BASE_URL}/telehealth/sessions/:sessionId/join`, ({ params }) => {
    return ok(
      {
        session: {
          id: params.sessionId,
          session_status: "in_progress",
          join_url: `https://example.test/join/${params.sessionId}`,
        },
      },
      "Joining session..."
    );
  }),

  http.get(`${API_BASE_URL}/encounters/by-appointment/:appointmentId`, () => {
    return ok({
      encounter: {
        id: "enc-1",
        appointment_id: "appt-1",
        note: "Patient discussed postpartum stressors.",
        assessment: "Moderate emotional strain with need for continued support.",
        follow_up_plan: "Weekly follow-up and counseling referral.",
        status: "draft",
      },
    });
  }),

  http.post(`${API_BASE_URL}/encounters`, async ({ request }) => {
    const body = await request.json();

    return ok({
      encounter: {
        id: "enc-1",
        appointment_id: body?.appointment_id,
        note: body?.note || "",
        assessment: body?.assessment || "",
        follow_up_plan: body?.follow_up_plan || "",
        status: "draft",
      },
    });
  }),

  http.patch(`${API_BASE_URL}/encounters/:encounterId/save`, () => {
    return ok({}, "Encounter draft saved successfully.");
  }),

  http.patch(`${API_BASE_URL}/encounters/:encounterId/finalize`, () => {
    return ok({}, "Encounter finalized successfully.");
  }),

  http.get(`${API_BASE_URL}/referrals`, () => {
    return ok({
      referrals: [
        {
          id: "ref-1",
          patient_name: "Patient User",
          category: "counseling",
          destination: "Community Counseling Center",
          status: "created",
          notes: "Patient requires structured follow-up support.",
          follow_up_date: "2026-05-20",
        },
      ],
    });
  }),

  http.post(`${API_BASE_URL}/referrals`, () => {
    return ok({}, "Referral created successfully.");
  }),

  http.patch(`${API_BASE_URL}/referrals/:referralId/status`, () => {
    return ok({}, "Referral status updated.");
  }),

  http.get(`${API_BASE_URL}/admin/dashboard-summary`, () => {
    return ok({
      summary: {
        total_users: 24,
        active_patients: 18,
        total_appointments: 42,
        completed_visits: 30,
        no_show_rate: 12,
        screening_completion_rate: 76,
      },
    });
  }),

  http.get(`${API_BASE_URL}/admin/metrics`, () => {
    return ok({
      report_snapshot: "Mocked report snapshot data for UI integration testing.",
    });
  }),

  http.get(`${API_BASE_URL}/admin/provider-utilization`, () => {
    return ok({
      rows: [
        { label: "Provider User", value: 12 },
        { label: "Counselor User", value: 7 },
      ],
    });
  }),

  http.get(`${API_BASE_URL}/users`, () => {
    return ok({
      users: [
        {
          id: "user-1",
          full_name: "Patient User",
          email: "patient@example.com",
          role: "patient",
          is_active: true,
        },
        {
          id: "user-2",
          full_name: "Provider User",
          email: "provider@example.com",
          role: "provider",
          is_active: true,
        },
      ],
    });
  }),

  http.get(`${API_BASE_URL}/audit`, () => {
    return ok({
      events: [
        {
          id: "audit-1",
          actor_name: "Admin User",
          action: "user.updated",
          target_type: "user",
          created_at: "2026-05-02T09:00:00Z",
        },
      ],
    });
  }),
];
```

---

# 6) `src/test/msw/server.js`

```js
import { setupServer } from "msw/node";
import { handlers } from "./handlers";

export const server = setupServer(...handlers);
```

---

# 7) `src/test/e2e/patient-flow.spec.js`

This file assumes Playwright is configured and the frontend is running. The selectors follow the component text patterns used throughout the earlier phases.

```js
import { test, expect } from "@playwright/test";

test("patient flow", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Email address").fill("patient@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/patient/);

  await page.goto("/patient/appointments");
  await expect(page.getByText("Appointments")).toBeVisible();

  await page.getByRole("link", { name: /book appointment/i }).click();
  await expect(page).toHaveURL(/\/patient\/appointments\/book/);

  await page.getByLabel("Service type").selectOption("mental_health");
  await page.getByLabel("Visit reason").fill("Need postpartum counseling support.");
  await page.getByLabel("Preferred date and time").fill("2026-05-15T10:30");
  await page.getByRole("button", { name: /book appointment/i }).click();

  await page.goto("/patient/screening");
  await expect(page.getByText("Self-assessment")).toBeVisible();

  await page.goto("/patient/session");
  await expect(page.getByText("Join your visit")).toBeVisible();
});
```

---

# 8) `src/test/e2e/provider-flow.spec.js`

```js
import { test, expect } from "@playwright/test";

test("provider flow", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Email address").fill("provider@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/provider/);
  await expect(page.getByText("Clinical dashboard")).toBeVisible();

  await page.goto("/provider/notes");
  await expect(page.getByText("Encounter workspace")).toBeVisible();

  await page.goto("/provider/referrals");
  await expect(page.getByText("Referral management")).toBeVisible();
});
```

---

# 9) `src/test/e2e/admin-flow.spec.js`

```js
import { test, expect } from "@playwright/test";

test("admin flow", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Email address").fill("admin@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page).toHaveURL(/\/admin/);
  await expect(page.getByText("Platform oversight dashboard")).toBeVisible();

  await page.goto("/admin/users");
  await expect(page.getByText("User management view")).toBeVisible();

  await page.goto("/admin/audit-logs");
  await expect(page.getByText("Audit visibility")).toBeVisible();
});
```

---

# 10) `.env.example`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
VITE_APP_NAME=PBBF Telehealth
VITE_APP_ENV=local
```

---

# 11) `docs/frontend-testing.md`

```md
# Frontend Testing Guide

## Purpose
This document explains how to validate the frontend with both mocked integration tests and browser-level E2E tests.

## Test layers

### 1. Component and hook tests
These run with Vitest and Testing Library.

Examples:
- shared UI components
- auth forms
- intake forms
- appointment forms
- screening flow
- telehealth join states
- provider encounter editor
- admin audit log table

Run:
```bash
npm run test
```

### 2. Mocked integration tests with MSW
MSW intercepts network calls during tests so UI behavior can be tested without requiring the backend to be running.

MSW files:
- `src/test/msw/handlers.js`
- `src/test/msw/server.js`

The test setup file starts and stops the mock server automatically.

### 3. E2E tests with Playwright
These validate cross-page user flows in a real browser.

Files:
- `src/test/e2e/patient-flow.spec.js`
- `src/test/e2e/provider-flow.spec.js`
- `src/test/e2e/admin-flow.spec.js`

Run:
```bash
npm run test:e2e
```

## Recommended local workflow

### Fast frontend-only feedback
```bash
npm run test
```

### Full browser flow validation
Start the frontend:
```bash
npm run dev
```

Then in another terminal:
```bash
npm run test:e2e
```

## Suggested QA order
1. shared UI tests  
2. patient flow  
3. provider flow  
4. admin flow  
5. connected QA against the real backend

## Connected QA note
MSW is useful for isolated frontend validation, but before staging sign-off you should also run the frontend against the real backend and confirm:
- auth works
- intake works
- appointments work
- screening submission works
- telehealth readiness works
- provider notes work
- admin metrics render correctly

## Troubleshooting
If E2E tests fail because selectors changed:
- prefer role-based and label-based selectors
- avoid brittle selectors tied to random class names
```

---

# 12) `docs/frontend-deployment.md`

```md
# Frontend Deployment Guide

## Purpose
This document describes how to package and verify the frontend for staging deployment.

## Build command
```bash
npm run build
```

This produces a static production build in:
- `dist/`

## Preview locally
```bash
npm run preview
```

## Required environment variables
The frontend should be configured from environment variables rather than hardcoded URLs.

Minimum expected variable:
```env
VITE_API_BASE_URL=https://your-backend-host/api/v1
```

## Pre-deployment checklist
Before shipping a staging build, verify:

- `npm install` completes cleanly
- `npm run lint` passes
- `npm run test` passes
- `npm run build` passes
- environment variables are correct
- backend base URL points to the correct staging API
- protected routes behave correctly after login
- patient, provider, and admin workspaces render against staging backend data

## Static hosting compatibility
Because this project is a Vite React SPA, the deployment target must support:
- static assets
- client-side routing fallback to `index.html`

Examples:
- Nginx static hosting
- Vercel
- Netlify
- Render static site
- Azure Static Web Apps

## SPA routing reminder
If deployed behind Nginx, configure routing fallback so direct route refreshes do not 404.

Example concept:
- unknown frontend route → serve `index.html`

## Suggested staging verification
After deployment, manually verify:
1. login page loads
2. patient dashboard loads
3. provider dashboard loads
4. admin dashboard loads
5. browser refresh on nested route works
6. API requests hit the correct backend base URL
```

---

# 13) `README.md`

Merge this structure into your existing README so the repo remains usable for developers and QA.

```md
# PBBF Telehealth Frontend

React + Vite frontend for the Post Baby Bliss Foundation telehealth platform.

## Core workspace areas
- patient workspace
- provider workspace
- admin workspace

## Local development
Install dependencies:
```bash
npm install
```

Start local dev server:
```bash
npm run dev
```

## Environment setup
Copy the example file and set real values as needed:
```bash
cp .env.example .env
```

Minimum expected value:
```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Testing
Run component and integration-style tests:
```bash
npm run test
```

Run end-to-end tests:
```bash
npm run test:e2e
```

Run both:
```bash
npm run test:all
```

## Build
Create a production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Key architecture notes
- API services perform requests
- hooks normalize backend data
- pages compose route-level UI
- shared UI components stay presentational
- avoid scattering payload mapping logic across page files
```

---

# 14) Optional but strongly recommended Playwright setup note

You did not explicitly ask for a Playwright config file, so I am not forcing one here.

But for clean E2E execution, you will usually also want a root-level:

- `playwright.config.js`

with:
- base URL
- browser settings
- test directory

If you want the next step after this phase, that would be the first support file I would add.

---

# 15) Exact commands to run after pasting these files

## 1. Install the new dev dependencies
```bash
npm install -D msw @playwright/test
```

## 2. Run mocked integration and component tests
```bash
npm run test
```

## 3. Start the frontend
```bash
npm run dev
```

## 4. In another terminal, run browser E2E tests
```bash
npm run test:e2e
```

## 5. Build for staging validation
```bash
npm run build
npm run preview
```

---

# 16) Completion checklist

This phase is complete when all of the following are true:

- mocked integration tests run through MSW
- patient E2E flow exists and runs
- provider E2E flow exists and runs
- admin E2E flow exists and runs
- `.env.example` exists
- frontend testing documentation exists
- frontend deployment documentation exists
- package scripts support QA and staging packaging
- frontend can be validated against mocked and real backend conditions with confidence

---

# Practical note after Phase 10
At this point, the frontend is ready for integrated QA, but do not treat mocked success as the final sign-off. The last validation step should always be connected QA against the real backend with role-based accounts and realistic data.
