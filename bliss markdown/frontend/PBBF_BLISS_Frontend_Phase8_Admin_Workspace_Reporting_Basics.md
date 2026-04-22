# PBBF BLISS Frontend — Phase 8 Populated Files
## Admin Workspace and Reporting Basics

## Objective
Implement the admin-facing area for users, oversight, reporting, and audit visibility.

Repository root:

`bliss-telehealth/pbbf-telehealth`

This phase completes the admin-facing interface so that an authenticated admin can:

- view platform KPIs
- see utilization/reporting snapshots
- review a user-management list view
- review audit logs with basic filters
- access settings and report screens from a real workspace

---

## Important alignment with your current structure

Your current app already supports this phase well:

- `src/app/AppRoutes.jsx` already contains admin routes
- `src/pages/admin/*` already exists
- the shell pattern using `AppLayout` is already correct

So this phase should **populate the admin workspace inside the existing structure**, not redesign routing.

### No route rewrite needed
You only need to confirm that your current route constants still expose:
- `ROUTES.admin.dashboard`
- `ROUTES.admin.users`
- `ROUTES.admin.reports`
- `ROUTES.admin.auditLogs`
- `ROUTES.admin.settings`

---

## Phase 8 backend assumptions

This frontend phase assumes the backend exposes routes similar to:

- `GET /api/v1/admin/dashboard-summary`
- `GET /api/v1/admin/metrics`
- `GET /api/v1/admin/provider-utilization`
- `GET /api/v1/users`
- `GET /api/v1/audit`

If your actual backend paths differ, update only:

- `src/modules/admin/services/adminApi.js`

---

## File list for this phase

### Modify these files
- `src/pages/admin/Dashboard.jsx`
- `src/pages/admin/Users.jsx`
- `src/pages/admin/AuditLogs.jsx`
- `src/pages/admin/Reports.jsx`
- `src/pages/admin/Settings.jsx`
- `src/modules/admin/pages/*`
- `src/modules/admin/components/*`
- `src/modules/admin/services/*`

### Create these files if missing
- `src/modules/admin/components/KpiCard.jsx`
- `src/modules/admin/components/UtilizationChart.jsx`
- `src/modules/admin/components/AuditLogTable.jsx`
- `src/modules/admin/hooks/useAdminMetrics.js`
- `src/modules/admin/services/adminApi.js`
- `src/modules/admin/__tests__/AdminDashboard.test.jsx`
- `src/modules/admin/__tests__/AuditLogTable.test.jsx`

### Recommended support test for required route protection coverage
- `src/pages/admin/__tests__/AdminRouteProtection.test.jsx`

---

# 1) `src/modules/admin/services/adminApi.js`

```jsx
import { api } from "../../../services/api";

export function getAdminDashboardSummaryRequest() {
  return api.get("/admin/dashboard-summary");
}

export function getAdminMetricsRequest() {
  return api.get("/admin/metrics");
}

export function getProviderUtilizationRequest() {
  return api.get("/admin/provider-utilization");
}

export function listUsersRequest() {
  return api.get("/users");
}

export function listAuditLogsRequest() {
  return api.get("/audit");
}
```

---

# 2) `src/modules/admin/hooks/useAdminMetrics.js`

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  getAdminDashboardSummaryRequest,
  getAdminMetricsRequest,
  getProviderUtilizationRequest,
  listAuditLogsRequest,
  listUsersRequest,
} from "../services/adminApi";

function normalizeMetricCard(summary = {}) {
  return {
    totalUsers: summary?.total_users ?? summary?.totalUsers ?? 0,
    activePatients: summary?.active_patients ?? summary?.activePatients ?? 0,
    totalAppointments: summary?.total_appointments ?? summary?.totalAppointments ?? 0,
    completedVisits: summary?.completed_visits ?? summary?.completedVisits ?? 0,
    noShowRate: summary?.no_show_rate ?? summary?.noShowRate ?? 0,
    screeningCompletionRate:
      summary?.screening_completion_rate ?? summary?.screeningCompletionRate ?? 0,
  };
}

function normalizeUtilizationRows(rows = []) {
  return rows.map((row) => ({
    label: row?.label || row?.provider_name || row?.providerName || "Provider",
    value: row?.value ?? row?.visit_count ?? row?.visitCount ?? 0,
  }));
}

function normalizeUsers(rows = []) {
  return rows.map((row) => ({
    id: row?.id || row?.user_id || "temp-user-id",
    fullName: row?.full_name || row?.fullName || "Unknown user",
    email: row?.email || "No email",
    role: row?.role || "unknown",
    isActive: Boolean(row?.is_active ?? row?.isActive ?? true),
  }));
}

function normalizeAuditLogs(rows = []) {
  return rows.map((row) => ({
    id: row?.id || row?.event_id || "temp-audit-id",
    actorName: row?.actor_name || row?.actorName || "System",
    action: row?.action || "unknown_action",
    targetType: row?.target_type || row?.targetType || "record",
    createdAt: row?.created_at || row?.createdAt || "",
  }));
}

export function useAdminMetrics() {
  const [summary, setSummary] = useState(null);
  const [metricDetails, setMetricDetails] = useState(null);
  const [providerUtilization, setProviderUtilization] = useState([]);
  const [users, setUsers] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  const loadAdminData = useCallback(async () => {
    try {
      setIsLoading(true);
      setLoadError("");

      const [
        summaryResponse,
        metricsResponse,
        utilizationResponse,
        usersResponse,
        auditResponse,
      ] = await Promise.all([
        getAdminDashboardSummaryRequest(),
        getAdminMetricsRequest(),
        getProviderUtilizationRequest(),
        listUsersRequest(),
        listAuditLogsRequest(),
      ]);

      const summaryPayload = summaryResponse?.data || summaryResponse || {};
      const metricsPayload = metricsResponse?.data || metricsResponse || {};
      const utilizationPayload = utilizationResponse?.data || utilizationResponse || {};
      const usersPayload = usersResponse?.data || usersResponse || {};
      const auditPayload = auditResponse?.data || auditResponse || {};

      setSummary(normalizeMetricCard(summaryPayload?.summary || summaryPayload));
      setMetricDetails(metricsPayload);
      setProviderUtilization(
        normalizeUtilizationRows(utilizationPayload?.rows || utilizationPayload?.providers || utilizationPayload)
      );
      setUsers(normalizeUsers(usersPayload?.users || usersPayload));
      setAuditLogs(normalizeAuditLogs(auditPayload?.events || auditPayload?.logs || auditPayload));
    } catch (error) {
      setLoadError(error?.message || "Unable to load admin workspace data.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAdminData();
  }, [loadAdminData]);

  return {
    summary,
    metricDetails,
    providerUtilization,
    users,
    auditLogs,
    isLoading,
    loadError,
    reload: loadAdminData,
  };
}
```

---

# 3) `src/modules/admin/components/KpiCard.jsx`

```jsx
export default function KpiCard({ title, value, helperText = "" }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">
        {title}
      </p>
      <p className="mt-3 text-3xl font-semibold text-slate-900">{value}</p>
      {helperText ? (
        <p className="mt-2 text-sm text-slate-600">{helperText}</p>
      ) : null}
    </div>
  );
}
```

---

# 4) `src/modules/admin/components/UtilizationChart.jsx`

```jsx
export default function UtilizationChart({ rows = [] }) {
  const maxValue = Math.max(...rows.map((row) => row.value), 1);

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-900">Provider utilization</h2>
      <p className="mt-2 text-sm text-slate-600">
        Basic workload snapshot by provider or grouped utilization source.
      </p>

      {!rows.length ? (
        <p className="mt-6 text-sm text-slate-600">No utilization data is visible yet.</p>
      ) : (
        <div className="mt-6 grid gap-4">
          {rows.map((row) => (
            <div key={row.label}>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium text-slate-900">{row.label}</span>
                <span className="text-slate-600">{row.value}</span>
              </div>
              <div className="h-3 rounded-full bg-slate-100">
                <div
                  className="h-3 rounded-full bg-sky-700"
                  style={{ width: `${(row.value / maxValue) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
```

---

# 5) `src/modules/admin/components/AuditLogTable.jsx`

```jsx
import { useMemo, useState } from "react";

function formatDateTime(value) {
  if (!value) return "Not available";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export default function AuditLogTable({ logs = [] }) {
  const [query, setQuery] = useState("");

  const filteredLogs = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    if (!normalizedQuery) return logs;

    return logs.filter((log) => {
      return (
        log.actorName.toLowerCase().includes(normalizedQuery) ||
        log.action.toLowerCase().includes(normalizedQuery) ||
        log.targetType.toLowerCase().includes(normalizedQuery)
      );
    });
  }, [logs, query]);

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Audit log visibility</h2>
          <p className="mt-2 text-sm text-slate-600">
            Review recent audit activity and filter by actor, action, or target type.
          </p>
        </div>

        <input
          type="text"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100 md:max-w-xs"
          placeholder="Filter audit logs..."
        />
      </div>

      {!filteredLogs.length ? (
        <p className="mt-6 text-sm text-slate-600">No audit logs match the current filter.</p>
      ) : (
        <div className="mt-6 overflow-x-auto">
          <table className="min-w-full border-collapse text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="py-3 pr-4 font-semibold">Actor</th>
                <th className="py-3 pr-4 font-semibold">Action</th>
                <th className="py-3 pr-4 font-semibold">Target</th>
                <th className="py-3 pr-0 font-semibold">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {filteredLogs.map((log) => (
                <tr key={log.id} className="border-b border-slate-100">
                  <td className="py-3 pr-4 text-slate-900">{log.actorName}</td>
                  <td className="py-3 pr-4 text-slate-700">{log.action}</td>
                  <td className="py-3 pr-4 text-slate-700">{log.targetType}</td>
                  <td className="py-3 pr-0 text-slate-600">{formatDateTime(log.createdAt)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
```

---

# 6) `src/pages/admin/Dashboard.jsx`

```jsx
import KpiCard from "../../modules/admin/components/KpiCard";
import UtilizationChart from "../../modules/admin/components/UtilizationChart";
import { useAdminMetrics } from "../../modules/admin/hooks/useAdminMetrics";
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";

export default function AdminDashboard() {
  const { summary, providerUtilization, isLoading, loadError } = useAdminMetrics();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading admin dashboard..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load admin dashboard" message={loadError} />;
  }

  return (
    <div className="space-y-8">
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Admin workspace</p>
        <h1 className="mt-2 text-3xl font-semibold">Platform oversight dashboard</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Monitor utilization, care activity, screening completion, no-show patterns, and core operational visibility.
        </p>
      </section>

      <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        <KpiCard title="Total users" value={summary?.totalUsers ?? 0} />
        <KpiCard title="Active patients" value={summary?.activePatients ?? 0} />
        <KpiCard title="Appointments" value={summary?.totalAppointments ?? 0} />
        <KpiCard title="Completed visits" value={summary?.completedVisits ?? 0} />
        <KpiCard title="No-show rate" value={`${summary?.noShowRate ?? 0}%`} />
        <KpiCard
          title="Screening completion"
          value={`${summary?.screeningCompletionRate ?? 0}%`}
        />
      </section>

      <UtilizationChart rows={providerUtilization} />
    </div>
  );
}
```

---

# 7) `src/pages/admin/Users.jsx`

```jsx
import { useAdminMetrics } from "../../modules/admin/hooks/useAdminMetrics";
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";

export default function AdminUsersPage() {
  const { users, isLoading, loadError } = useAdminMetrics();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading users..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load users" message={loadError} />;
  }

  return (
    <div className="space-y-8">
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Admin users</p>
        <h1 className="mt-2 text-3xl font-semibold">User management view</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Review core account information, role visibility, and activity status.
        </p>
      </section>

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        {!users.length ? (
          <p className="text-sm text-slate-600">No users are visible yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full border-collapse text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500">
                  <th className="py-3 pr-4 font-semibold">Name</th>
                  <th className="py-3 pr-4 font-semibold">Email</th>
                  <th className="py-3 pr-4 font-semibold">Role</th>
                  <th className="py-3 pr-0 font-semibold">Status</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id} className="border-b border-slate-100">
                    <td className="py-3 pr-4 text-slate-900">{user.fullName}</td>
                    <td className="py-3 pr-4 text-slate-700">{user.email}</td>
                    <td className="py-3 pr-4 text-slate-700 capitalize">{user.role}</td>
                    <td className="py-3 pr-0 text-slate-700">
                      {user.isActive ? "Active" : "Inactive"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
```

---

# 8) `src/pages/admin/AuditLogs.jsx`

```jsx
import AuditLogTable from "../../modules/admin/components/AuditLogTable";
import { useAdminMetrics } from "../../modules/admin/hooks/useAdminMetrics";
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
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Admin audit</p>
        <h1 className="mt-2 text-3xl font-semibold">Audit visibility</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Review operational activity and basic accountability events from the admin workspace.
        </p>
      </section>

      <AuditLogTable logs={auditLogs} />
    </div>
  );
}
```

---

# 9) `src/pages/admin/Reports.jsx`

```jsx
import { useAdminMetrics } from "../../modules/admin/hooks/useAdminMetrics";
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
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Admin reports</p>
        <h1 className="mt-2 text-3xl font-semibold">Reporting snapshots</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Review basic summary metrics and reporting-ready operational snapshots.
        </p>
      </section>

      <section className="grid gap-5 md:grid-cols-2">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">Core snapshot</h2>
          <div className="mt-5 grid gap-3 text-sm text-slate-700">
            <p>Total users: <span className="font-medium">{summary?.totalUsers ?? 0}</span></p>
            <p>Active patients: <span className="font-medium">{summary?.activePatients ?? 0}</span></p>
            <p>Total appointments: <span className="font-medium">{summary?.totalAppointments ?? 0}</span></p>
            <p>Completed visits: <span className="font-medium">{summary?.completedVisits ?? 0}</span></p>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">Extended snapshot</h2>
          <pre className="mt-5 overflow-x-auto rounded-2xl bg-slate-50 p-4 text-xs text-slate-700">
{JSON.stringify(metricDetails || {}, null, 2)}
          </pre>
        </div>
      </section>
    </div>
  );
}
```

---

# 10) `src/pages/admin/Settings.jsx`

```jsx
export default function AdminSettingsPage() {
  return (
    <div className="space-y-8">
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Admin settings</p>
        <h1 className="mt-2 text-3xl font-semibold">Workspace settings</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          This page can later expand into notification preferences, admin defaults, and platform controls.
        </p>
      </section>

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Settings placeholder</h2>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          Phase 8 only requires a real admin-facing page shell here so the workspace is complete and navigable.
          Full settings controls can be expanded later.
        </p>
      </section>
    </div>
  );
}
```

---

# 11) `src/modules/admin/__tests__/AdminDashboard.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import AdminDashboard from "../../../pages/admin/Dashboard";

vi.mock("../hooks/useAdminMetrics", () => ({
  useAdminMetrics: () => ({
    summary: {
      totalUsers: 24,
      activePatients: 18,
      totalAppointments: 42,
      completedVisits: 30,
      noShowRate: 12,
      screeningCompletionRate: 76,
    },
    providerUtilization: [
      { label: "Provider A", value: 12 },
      { label: "Provider B", value: 8 },
    ],
    isLoading: false,
    loadError: "",
  }),
}));

describe("AdminDashboard", () => {
  it("renders admin KPI metrics", () => {
    render(<AdminDashboard />);

    expect(screen.getByText("Platform oversight dashboard")).toBeInTheDocument();
    expect(screen.getByText("24")).toBeInTheDocument();
    expect(screen.getByText("Provider utilization")).toBeInTheDocument();
  });
});
```

---

# 12) `src/modules/admin/__tests__/AuditLogTable.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import AuditLogTable from "../components/AuditLogTable";

describe("AuditLogTable", () => {
  it("renders audit rows", () => {
    render(
      <AuditLogTable
        logs={[
          {
            id: "log-1",
            actorName: "Admin User",
            action: "user.updated",
            targetType: "user",
            createdAt: "2026-05-03T09:00:00Z",
          },
        ]}
      />
    );

    expect(screen.getByText("Admin User")).toBeInTheDocument();
    expect(screen.getByText("user.updated")).toBeInTheDocument();
  });

  it("filters audit rows by query", () => {
    render(
      <AuditLogTable
        logs={[
          {
            id: "log-1",
            actorName: "Admin User",
            action: "user.updated",
            targetType: "user",
            createdAt: "2026-05-03T09:00:00Z",
          },
          {
            id: "log-2",
            actorName: "Provider User",
            action: "encounter.finalized",
            targetType: "encounter",
            createdAt: "2026-05-03T10:00:00Z",
          },
        ]}
      />
    );

    fireEvent.change(screen.getByPlaceholderText(/filter audit logs/i), {
      target: { value: "provider" },
    });

    expect(screen.getByText("Provider User")).toBeInTheDocument();
  });
});
```

---

# 13) Recommended support test for route protection requirement
## `src/pages/admin/__tests__/AdminRouteProtection.test.jsx`

```jsx
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import ProtectedRoute from "../../../routes/ProtectedRoute";
import AdminDashboard from "../Dashboard";

const useAuthStoreMock = vi.fn();

vi.mock("../../../store/authStore", () => ({
  useAuthStore: (selector) =>
    selector(
      useAuthStoreMock() || {
        isHydrated: true,
        isAuthenticated: false,
        user: null,
      }
    ),
}));

describe("Admin route protection", () => {
  it("blocks a non-admin user from the admin area", () => {
    useAuthStoreMock.mockReturnValue({
      isHydrated: true,
      isAuthenticated: true,
      user: { role: "patient" },
    });

    render(
      <MemoryRouter initialEntries={["/admin"]}>
        <Routes>
          <Route path="/patient" element={<div>Patient Home</div>} />
          <Route
            path="/admin"
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Patient Home")).toBeInTheDocument();
  });
});
```

---

# Exact commands to run after pasting these files

## 1. Run the admin-focused tests
```bash
npx vitest run src/modules/admin/__tests__/AdminDashboard.test.jsx src/modules/admin/__tests__/AuditLogTable.test.jsx src/pages/admin/__tests__/AdminRouteProtection.test.jsx
```

## 2. Start the frontend
```bash
npm run dev
```

## 3. Manual validation flow
After the frontend boots, validate this path:

1. Sign in as an admin  
2. Open the admin dashboard  
3. Confirm KPI cards render  
4. Confirm provider utilization snapshot renders  
5. Open the users page and confirm the list loads  
6. Open audit logs and test the filter input  
7. Open reports and confirm snapshot data renders  
8. Open settings and confirm the admin workspace remains navigable  

---

# Completion checklist

This phase is complete when all of the following are true:

- admin dashboard renders KPI metrics
- utilization snapshot is visible
- users list view renders
- audit log list and filter render
- report snapshot page renders
- admin route protection test passes
- audit table render test passes
- dashboard metrics render test passes
- admins can monitor the platform from a real interface, not just backend endpoints

---

# Practical note before Phase 9
Before moving on, make sure the backend admin summary and audit endpoints return stable, role-protected payloads. The frontend can present admin oversight cleanly, but those views still depend on trustworthy backend authorization and reporting logic.
