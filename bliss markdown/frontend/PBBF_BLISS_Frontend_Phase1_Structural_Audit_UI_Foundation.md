# PBBF BLISS Frontend — Phase 1 Populated Files  
## Structural Audit and UI Foundation Cleanup

## Objective
Clean and standardize the current React structure so new features land into a coherent application shell instead of scattered files.

## Phase 1 decisions
For this phase, the frontend should adopt these foundation rules:

1. Use **one application shell** built from:
   - `AppLayout`
   - `AppShell`
   - `Sidebar`
   - `Topbar`

2. Use **one route map** driven by:
   - `src/shared/constants/routes.js`
   - `src/shared/constants/navigation.js`

3. Keep **feature-specific logic** under:
   - `src/modules/*`

4. Keep **route-level composition only** under:
   - `src/pages/*`

5. Use **one canonical API client strategy**:
   - Prefer `src/shared/services/api.js`
   - If `src/services/api.js` still exists, convert it into a thin compatibility re-export instead of maintaining duplicate logic

6. Add **basic reusable state components**:
   - `Loader`
   - `EmptyState`
   - `ErrorState`

7. Add **frontend test utilities** now so later feature phases do not have to invent testing structure again.

---

## Files populated in this package

### Modify
- `src/App.jsx`
- `src/main.jsx`
- `src/app/AppLayout.jsx`
- `src/app/AppRoutes.jsx`
- `src/index.css`
- `src/App.css`
- `src/components/layout/AppShell.jsx`
- `src/components/layout/Sidebar.jsx`
- `src/components/layout/Topbar.jsx`
- `src/shared/constants/routes.js`
- `src/shared/constants/roles.js`

### Create if missing
- `src/shared/constants/navigation.js`
- `src/shared/utils/storage.js`
- `src/shared/utils/formatters.js`
- `src/shared/components/Loader.jsx`
- `src/shared/components/EmptyState.jsx`
- `src/shared/components/ErrorState.jsx`
- `src/test/setup.jsx`
- `src/test/renderWithProviders.jsx`

### Additional test files strongly recommended for this phase
- `src/app/__tests__/app-smoke.test.jsx`
- `src/app/__tests__/route-shell.test.jsx`
- `src/components/layout/__tests__/sidebar.test.jsx`
- `src/components/layout/__tests__/topbar.test.jsx`

### Optional cleanup file for the “one API client strategy” rule
- `src/services/api.js`  
  Convert it into a re-export shim if duplicate logic still exists there.

---

# 1) `src/App.jsx`

```jsx
import AppRoutes from "./app/AppRoutes";

export default function App() {
  return <AppRoutes />;
}
```

---

# 2) `src/main.jsx`

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

---

# 3) `src/app/AppLayout.jsx`

```jsx
import { Outlet } from "react-router-dom";
import AppShell from "../components/layout/AppShell";

export default function AppLayout() {
  return (
    <AppShell>
      <Outlet />
    </AppShell>
  );
}
```

---

# 4) `src/app/AppRoutes.jsx`

```jsx
import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "./AppLayout";
import { ROUTES } from "../shared/constants/routes";

// Existing route-level pages
import LoginPage from "../pages/auth/Login";

import PatientDashboardPage from "../pages/patient/Dashboard";
import PatientAppointmentsPage from "../pages/patient/Appointments";
import PatientMessagesPage from "../pages/patient/Messages";
import PatientResourcesPage from "../pages/patient/Resources";
import PatientScreeningPage from "../pages/patient/Screening";
import PatientSessionPage from "../pages/patient/Session";
import PatientCarePlanPage from "../pages/patient/CarePlan";

import ProviderDashboardPage from "../pages/provider/Dashboard";
import ProviderNotesPage from "../pages/provider/Notes";
import ProviderReferralsPage from "../pages/provider/Referrals";

import AdminDashboardPage from "../pages/admin/Dashboard";
import AdminUsersPage from "../pages/admin/Users";
import AdminReportsPage from "../pages/admin/Reports";
import AdminAuditLogsPage from "../pages/admin/AuditLogs";
import AdminSettingsPage from "../pages/admin/Settings";

function NotFoundPage() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
      <h1 className="text-2xl font-semibold text-slate-900">Page not found</h1>
      <p className="mt-2 text-sm text-slate-600">
        The page you requested does not exist in the current route map.
      </p>
    </div>
  );
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route path={ROUTES.root} element={<Navigate to={ROUTES.login} replace />} />
      <Route path={ROUTES.login} element={<LoginPage />} />

      <Route element={<AppLayout />}>
        <Route path={ROUTES.patient.dashboard} element={<PatientDashboardPage />} />
        <Route path={ROUTES.patient.appointments} element={<PatientAppointmentsPage />} />
        <Route path={ROUTES.patient.messages} element={<PatientMessagesPage />} />
        <Route path={ROUTES.patient.resources} element={<PatientResourcesPage />} />
        <Route path={ROUTES.patient.screening} element={<PatientScreeningPage />} />
        <Route path={ROUTES.patient.session} element={<PatientSessionPage />} />
        <Route path={ROUTES.patient.carePlan} element={<PatientCarePlanPage />} />

        <Route path={ROUTES.provider.dashboard} element={<ProviderDashboardPage />} />
        <Route path={ROUTES.provider.notes} element={<ProviderNotesPage />} />
        <Route path={ROUTES.provider.referrals} element={<ProviderReferralsPage />} />

        <Route path={ROUTES.admin.dashboard} element={<AdminDashboardPage />} />
        <Route path={ROUTES.admin.users} element={<AdminUsersPage />} />
        <Route path={ROUTES.admin.reports} element={<AdminReportsPage />} />
        <Route path={ROUTES.admin.auditLogs} element={<AdminAuditLogsPage />} />
        <Route path={ROUTES.admin.settings} element={<AdminSettingsPage />} />

        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
```

---

# 5) `src/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: light;
  font-family:
    Inter,
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
  line-height: 1.5;
  font-weight: 400;

  --background: #f8fafc;
  --foreground: #0f172a;
  --muted: #64748b;
  --border: #e2e8f0;
  --panel: #ffffff;
  --panel-soft: #f1f5f9;
  --brand: #2563eb;
  --brand-soft: #dbeafe;
  --danger: #dc2626;
  --success: #16a34a;
  --warning: #d97706;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

html,
body,
#root {
  min-height: 100%;
}

body {
  margin: 0;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.06), transparent 28%),
    linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
  color: var(--foreground);
  font-family:
    Inter,
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
}

button,
input,
textarea,
select {
  font: inherit;
}

.page-section {
  @apply rounded-2xl border border-slate-200 bg-white p-6 shadow-sm;
}

.page-title {
  @apply text-2xl font-semibold tracking-tight text-slate-900;
}

.page-subtitle {
  @apply mt-1 text-sm text-slate-600;
}
```

---

# 6) `src/App.css`

```css
.app-fade-in {
  animation: app-fade-in 180ms ease-out;
}

@keyframes app-fade-in {
  from {
    opacity: 0;
    transform: translateY(6px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

# 7) `src/components/layout/AppShell.jsx`

```jsx
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function AppShell({ children }) {
  return (
    <div className="min-h-screen bg-transparent text-slate-900">
      <div className="mx-auto flex min-h-screen max-w-[1600px]">
        <Sidebar />

        <div className="flex min-h-screen min-w-0 flex-1 flex-col">
          <Topbar />

          <main className="app-fade-in flex-1 px-4 pb-6 pt-4 sm:px-6 lg:px-8">
            <div className="mx-auto w-full max-w-7xl">{children}</div>
          </main>
        </div>
      </div>
    </div>
  );
}
```

---

# 8) `src/components/layout/Sidebar.jsx`

```jsx
import { NavLink } from "react-router-dom";
import { NAVIGATION_SECTIONS } from "../../shared/constants/navigation";

function getNavItemClassName(isActive) {
  return [
    "group flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition-all",
    isActive
      ? "bg-blue-600 text-white shadow-sm"
      : "text-slate-700 hover:bg-slate-100 hover:text-slate-900",
  ].join(" ");
}

export default function Sidebar() {
  return (
    <aside className="sticky top-0 hidden min-h-screen w-72 shrink-0 border-r border-slate-200 bg-white/90 backdrop-blur lg:block">
      <div className="flex h-full flex-col px-4 py-5">
        <div className="rounded-2xl bg-slate-900 px-4 py-4 text-white shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-300">
            Post Baby Bliss
          </p>
          <h1 className="mt-2 text-lg font-semibold">BLISS Telehealth</h1>
          <p className="mt-1 text-sm text-slate-300">
            Unified maternal care operations workspace
          </p>
        </div>

        <nav className="mt-6 flex-1 space-y-6" aria-label="Sidebar navigation">
          {NAVIGATION_SECTIONS.map((section) => (
            <div key={section.label}>
              <p className="mb-2 px-2 text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">
                {section.label}
              </p>

              <div className="space-y-1">
                {section.items.map((item) => (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    className={({ isActive }) => getNavItemClassName(isActive)}
                  >
                    <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-black/5 text-xs font-semibold group-[.active]:bg-white/20">
                      {item.shortLabel}
                    </span>
                    <span>{item.label}</span>
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>

        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <p className="text-sm font-medium text-slate-900">Foundation cleanup</p>
          <p className="mt-1 text-xs leading-5 text-slate-600">
            This shell is the base layer for all later patient, provider, and admin features.
          </p>
        </div>
      </div>
    </aside>
  );
}
```

---

# 9) `src/components/layout/Topbar.jsx`

```jsx
import { useMemo } from "react";
import { useLocation } from "react-router-dom";

import { NAVIGATION_ITEMS_BY_PATH } from "../../shared/constants/navigation";

function resolvePageMeta(pathname) {
  return (
    NAVIGATION_ITEMS_BY_PATH[pathname] ?? {
      label: "Workspace",
      description: "BLISS Telehealth application workspace",
    }
  );
}

export default function Topbar() {
  const location = useLocation();

  const pageMeta = useMemo(() => resolvePageMeta(location.pathname), [location.pathname]);

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/85 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Current workspace
          </p>
          <h2 className="truncate text-xl font-semibold text-slate-900">
            {pageMeta.label}
          </h2>
          <p className="truncate text-sm text-slate-600">{pageMeta.description}</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden rounded-full border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-600 sm:block">
            Phase 1 UI foundation
          </div>

          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white shadow-sm">
            PB
          </div>
        </div>
      </div>
    </header>
  );
}
```

---

# 10) `src/shared/constants/routes.js`

```js
export const ROUTES = {
  root: "/",
  login: "/login",

  patient: {
    dashboard: "/patient/dashboard",
    appointments: "/patient/appointments",
    messages: "/patient/messages",
    resources: "/patient/resources",
    screening: "/patient/screening",
    session: "/patient/session",
    carePlan: "/patient/care-plan",
  },

  provider: {
    dashboard: "/provider/dashboard",
    notes: "/provider/notes",
    referrals: "/provider/referrals",
  },

  admin: {
    dashboard: "/admin/dashboard",
    users: "/admin/users",
    reports: "/admin/reports",
    auditLogs: "/admin/audit-logs",
    settings: "/admin/settings",
  },
};

export const ROUTE_TITLES = {
  [ROUTES.login]: "Login",

  [ROUTES.patient.dashboard]: "Patient Dashboard",
  [ROUTES.patient.appointments]: "My Appointments",
  [ROUTES.patient.messages]: "Messages",
  [ROUTES.patient.resources]: "Resources",
  [ROUTES.patient.screening]: "Screening",
  [ROUTES.patient.session]: "Session Access",
  [ROUTES.patient.carePlan]: "Care Plan",

  [ROUTES.provider.dashboard]: "Provider Dashboard",
  [ROUTES.provider.notes]: "Encounter Notes",
  [ROUTES.provider.referrals]: "Provider Referrals",

  [ROUTES.admin.dashboard]: "Admin Dashboard",
  [ROUTES.admin.users]: "Users",
  [ROUTES.admin.reports]: "Reports",
  [ROUTES.admin.auditLogs]: "Audit Logs",
  [ROUTES.admin.settings]: "Settings",
};
```

---

# 11) `src/shared/constants/roles.js`

```js
export const ROLES = Object.freeze({
  PATIENT: "patient",
  PROVIDER: "provider",
  COUNSELOR: "counselor",
  LACTATION_CONSULTANT: "lactation_consultant",
  CARE_COORDINATOR: "care_coordinator",
  ADMIN: "admin",
});

export const ROLE_OPTIONS = [
  { value: ROLES.PATIENT, label: "Patient" },
  { value: ROLES.PROVIDER, label: "Provider" },
  { value: ROLES.COUNSELOR, label: "Counselor" },
  { value: ROLES.LACTATION_CONSULTANT, label: "Lactation Consultant" },
  { value: ROLES.CARE_COORDINATOR, label: "Care Coordinator" },
  { value: ROLES.ADMIN, label: "Admin" },
];

export const INTERNAL_ROLES = [
  ROLES.PROVIDER,
  ROLES.COUNSELOR,
  ROLES.LACTATION_CONSULTANT,
  ROLES.CARE_COORDINATOR,
  ROLES.ADMIN,
];
```

---

# 12) `src/shared/constants/navigation.js`

```js
import { ROUTES } from "./routes";
import { ROLES } from "./roles";

export const NAVIGATION_SECTIONS = [
  {
    label: "Patient",
    items: [
      {
        label: "Dashboard",
        shortLabel: "PD",
        to: ROUTES.patient.dashboard,
        allowedRoles: [ROLES.PATIENT],
        description: "Patient home and care overview",
      },
      {
        label: "Appointments",
        shortLabel: "AP",
        to: ROUTES.patient.appointments,
        allowedRoles: [ROLES.PATIENT],
        description: "Patient booking and visit history",
      },
      {
        label: "Messages",
        shortLabel: "MS",
        to: ROUTES.patient.messages,
        allowedRoles: [ROLES.PATIENT],
        description: "Patient communication center",
      },
      {
        label: "Resources",
        shortLabel: "RS",
        to: ROUTES.patient.resources,
        allowedRoles: [ROLES.PATIENT],
        description: "Patient education library",
      },
      {
        label: "Screening",
        shortLabel: "SC",
        to: ROUTES.patient.screening,
        allowedRoles: [ROLES.PATIENT],
        description: "Patient self-screening and assessment",
      },
      {
        label: "Session",
        shortLabel: "VS",
        to: ROUTES.patient.session,
        allowedRoles: [ROLES.PATIENT],
        description: "Virtual session access and guidance",
      },
      {
        label: "Care Plan",
        shortLabel: "CP",
        to: ROUTES.patient.carePlan,
        allowedRoles: [ROLES.PATIENT],
        description: "Follow-up and care plan summary",
      },
    ],
  },

  {
    label: "Provider",
    items: [
      {
        label: "Dashboard",
        shortLabel: "PR",
        to: ROUTES.provider.dashboard,
        allowedRoles: [ROLES.PROVIDER, ROLES.COUNSELOR, ROLES.LACTATION_CONSULTANT],
        description: "Clinical overview and assigned work",
      },
      {
        label: "Notes",
        shortLabel: "NT",
        to: ROUTES.provider.notes,
        allowedRoles: [ROLES.PROVIDER, ROLES.COUNSELOR, ROLES.LACTATION_CONSULTANT],
        description: "Encounter documentation workspace",
      },
      {
        label: "Referrals",
        shortLabel: "RF",
        to: ROUTES.provider.referrals,
        allowedRoles: [ROLES.PROVIDER, ROLES.CARE_COORDINATOR],
        description: "Referral follow-up and handoff tracking",
      },
    ],
  },

  {
    label: "Admin",
    items: [
      {
        label: "Dashboard",
        shortLabel: "AD",
        to: ROUTES.admin.dashboard,
        allowedRoles: [ROLES.ADMIN],
        description: "Operations dashboard and summary metrics",
      },
      {
        label: "Users",
        shortLabel: "US",
        to: ROUTES.admin.users,
        allowedRoles: [ROLES.ADMIN],
        description: "User and role administration",
      },
      {
        label: "Reports",
        shortLabel: "RP",
        to: ROUTES.admin.reports,
        allowedRoles: [ROLES.ADMIN],
        description: "Reporting and exports",
      },
      {
        label: "Audit Logs",
        shortLabel: "AL",
        to: ROUTES.admin.auditLogs,
        allowedRoles: [ROLES.ADMIN],
        description: "Audit and governance activity",
      },
      {
        label: "Settings",
        shortLabel: "ST",
        to: ROUTES.admin.settings,
        allowedRoles: [ROLES.ADMIN],
        description: "Administrative system settings",
      },
    ],
  },
];

export const NAVIGATION_ITEMS = NAVIGATION_SECTIONS.flatMap((section) => section.items);

export const NAVIGATION_ITEMS_BY_PATH = Object.fromEntries(
  NAVIGATION_ITEMS.map((item) => [
    item.to,
    {
      label: item.label,
      description: item.description,
    },
  ])
);
```

---

# 13) `src/shared/utils/storage.js`

```js
const isBrowser = typeof window !== "undefined";

function safeParse(value, fallback = null) {
  try {
    return JSON.parse(value);
  } catch {
    return fallback;
  }
}

export function getStorageItem(key, fallback = null) {
  if (!isBrowser) return fallback;

  const raw = window.localStorage.getItem(key);
  if (raw === null) return fallback;

  return safeParse(raw, fallback);
}

export function setStorageItem(key, value) {
  if (!isBrowser) return;

  window.localStorage.setItem(key, JSON.stringify(value));
}

export function removeStorageItem(key) {
  if (!isBrowser) return;
  window.localStorage.removeItem(key);
}

export function clearStorage() {
  if (!isBrowser) return;
  window.localStorage.clear();
}

export function getSessionItem(key, fallback = null) {
  if (!isBrowser) return fallback;

  const raw = window.sessionStorage.getItem(key);
  if (raw === null) return fallback;

  return safeParse(raw, fallback);
}

export function setSessionItem(key, value) {
  if (!isBrowser) return;
  window.sessionStorage.setItem(key, JSON.stringify(value));
}

export function removeSessionItem(key) {
  if (!isBrowser) return;
  window.sessionStorage.removeItem(key);
}
```

---

# 14) `src/shared/utils/formatters.js`

```js
export function titleCase(value = "") {
  return String(value)
    .replace(/[_-]+/g, " ")
    .split(" ")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase())
    .join(" ");
}

export function formatRole(value = "") {
  return titleCase(value);
}

export function formatStatus(value = "") {
  return titleCase(value);
}

export function formatDate(value, locale = "en-UG") {
  if (!value) return "—";

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";

  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(date);
}

export function formatDateTime(value, locale = "en-UG") {
  if (!value) return "—";

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";

  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

export function getInitials(name = "") {
  const parts = String(name).trim().split(/\s+/).filter(Boolean);
  if (!parts.length) return "NA";

  return parts
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join("");
}
```

---

# 15) `src/shared/components/Loader.jsx`

```jsx
export default function Loader({
  label = "Loading...",
  fullScreen = false,
  compact = false,
}) {
  const wrapperClass = fullScreen
    ? "flex min-h-[50vh] items-center justify-center"
    : "flex items-center justify-center";

  const spinnerSizeClass = compact ? "h-5 w-5" : "h-10 w-10";

  return (
    <div className={wrapperClass} role="status" aria-live="polite">
      <div className="flex flex-col items-center gap-3">
        <div
          className={`${spinnerSizeClass} animate-spin rounded-full border-4 border-slate-200 border-t-blue-600`}
        />
        <p className="text-sm font-medium text-slate-600">{label}</p>
      </div>
    </div>
  );
}
```

---

# 16) `src/shared/components/EmptyState.jsx`

```jsx
export default function EmptyState({
  title = "Nothing to show yet",
  description = "Once data becomes available, it will appear here.",
  action = null,
}) {
  return (
    <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm">
      <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-500">
        0
      </div>
      <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
      <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-600">
        {description}
      </p>
      {action ? <div className="mt-5">{action}</div> : null}
    </div>
  );
}
```

---

# 17) `src/shared/components/ErrorState.jsx`

```jsx
export default function ErrorState({
  title = "Something went wrong",
  description = "The requested content could not be loaded right now.",
  onRetry,
}) {
  return (
    <div className="rounded-2xl border border-red-200 bg-red-50 p-6 shadow-sm">
      <h3 className="text-lg font-semibold text-red-900">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-red-700">{description}</p>

      {typeof onRetry === "function" ? (
        <button
          type="button"
          onClick={onRetry}
          className="mt-4 inline-flex items-center rounded-xl bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700"
        >
          Try again
        </button>
      ) : null}
    </div>
  );
}
```

---

# 18) `src/test/setup.jsx`

```jsx
import "@testing-library/jest-dom/vitest";
```

---

# 19) `src/test/renderWithProviders.jsx`

```jsx
import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

export function renderWithProviders(ui, { route = "/" } = {}) {
  return render(<MemoryRouter initialEntries={[route]}>{ui}</MemoryRouter>);
}
```

---

# 20) `src/app/__tests__/app-smoke.test.jsx`

```jsx
import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import App from "../../App";
import { renderWithProviders } from "../../test/renderWithProviders";

describe("App smoke render", () => {
  it("renders the login route when opened at /login", () => {
    renderWithProviders(<App />, { route: "/login" });

    expect(document.body).toBeInTheDocument();
  });

  it("renders the patient dashboard route inside the application shell", () => {
    renderWithProviders(<App />, { route: "/patient/dashboard" });

    expect(screen.getByText(/current workspace/i)).toBeInTheDocument();
    expect(screen.getByText(/patient/i)).toBeInTheDocument();
  });
});
```

---

# 21) `src/app/__tests__/route-shell.test.jsx`

```jsx
import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import AppRoutes from "../AppRoutes";
import { renderWithProviders } from "../../test/renderWithProviders";

describe("Route shell render", () => {
  it("renders sidebar and topbar on application routes", () => {
    renderWithProviders(<AppRoutes />, { route: "/admin/dashboard" });

    expect(screen.getByText(/bliss telehealth/i)).toBeInTheDocument();
    expect(screen.getByText(/current workspace/i)).toBeInTheDocument();
    expect(screen.getByText(/admin dashboard/i)).toBeInTheDocument();
  });
});
```

---

# 22) `src/components/layout/__tests__/sidebar.test.jsx`

```jsx
import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Sidebar from "../Sidebar";
import { renderWithProviders } from "../../../test/renderWithProviders";

describe("Sidebar navigation render", () => {
  it("renders the core navigation sections", () => {
    renderWithProviders(<Sidebar />, { route: "/patient/dashboard" });

    expect(screen.getByText(/patient/i)).toBeInTheDocument();
    expect(screen.getByText(/provider/i)).toBeInTheDocument();
    expect(screen.getByText(/admin/i)).toBeInTheDocument();
  });

  it("renders key route labels", () => {
    renderWithProviders(<Sidebar />, { route: "/patient/dashboard" });

    expect(screen.getByText(/appointments/i)).toBeInTheDocument();
    expect(screen.getByText(/notes/i)).toBeInTheDocument();
    expect(screen.getByText(/audit logs/i)).toBeInTheDocument();
  });
});
```

---

# 23) `src/components/layout/__tests__/topbar.test.jsx`

```jsx
import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Topbar from "../Topbar";
import { renderWithProviders } from "../../../test/renderWithProviders";

describe("Topbar render", () => {
  it("renders the current page title from the route map", () => {
    renderWithProviders(<Topbar />, { route: "/provider/notes" });

    expect(screen.getByText(/encounter notes/i)).toBeInTheDocument();
    expect(screen.getByText(/current workspace/i)).toBeInTheDocument();
  });
});
```

---

# 24) Optional cleanup shim — `src/services/api.js`

Use this only if duplicate API logic already exists in both `src/services/api.js` and `src/shared/services/api.js`.

The cleaner rule for this project is:
- keep **`src/shared/services/api.js`** as the canonical API client
- convert **`src/services/api.js`** into a compatibility re-export

```js
export { default } from "../shared/services/api";
export * from "../shared/services/api";
```

This avoids breaking older imports while still enforcing one real API client source.

---

# 25) Recommended dev dependencies for frontend testing

If they are not already installed, run:

```bash
npm install -D vitest jsdom @testing-library/react @testing-library/jest-dom
```

---

# 26) If your current `vite.config.js` does not already include Vitest config

Add this **targeted block** to your existing `vite.config.js` so the Phase 1 tests can run correctly.

```js
/// add inside defineConfig(...)
test: {
  globals: true,
  environment: "jsdom",
  setupFiles: "./src/test/setup.jsx",
},
```

Do not replace the rest of your existing Vite config if it already contains project-specific setup.

---

# 27) Commands to run after pasting the files

From:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth
```

Run:

```bash
npm install
npm install -D vitest jsdom @testing-library/react @testing-library/jest-dom
npm run dev
```

Then run tests:

```bash
npx vitest run src/app/__tests__/app-smoke.test.jsx
npx vitest run src/app/__tests__/route-shell.test.jsx
npx vitest run src/components/layout/__tests__/sidebar.test.jsx
npx vitest run src/components/layout/__tests__/topbar.test.jsx
```

Or run all frontend tests:

```bash
npx vitest run
```

---

# 28) Completion checklist for this phase

This phase is complete when all of the following are true:

- `App.jsx` only delegates to one clean route system
- `main.jsx` boots the app through one clean router setup
- `AppLayout` and `AppShell` are the shared route shell
- `Sidebar` and `Topbar` render consistently for app routes
- `routes.js` and `navigation.js` define the canonical route map
- `roles.js` defines shared role constants cleanly
- reusable state components exist:
  - `Loader`
  - `EmptyState`
  - `ErrorState`
- one API client strategy is chosen
- smoke and shell tests run successfully
- future feature work can land into this shell without creating duplicate layout patterns

---

# 29) Important integration note before Phase 2

Because your existing route pages and feature modules already exist, **do not recreate those directories**.  
This phase is only meant to **stabilize the shell, constants, shared utilities, and test baseline**.

So after applying this phase:
- keep `src/modules/*`
- keep `src/pages/*`
- keep `src/providers/*`
- keep `src/store/*`

Then Phase 2 can safely focus on authentication and role-aware UI flow without first untangling structure again.
