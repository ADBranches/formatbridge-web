# Frontend Phase FE1 — Foundation UI Scaffold

## Objective

Create the base frontend app with routing, layout, environment config, styling, and a reusable API client.

## Target Directory

```text
aml-system/services/regulator-api/frontend/
```

## Files and Directories

```text
package.json
vite.config.ts
tsconfig.json
index.html
.env.example
src/main.tsx
src/App.tsx
src/routes/AppRoutes.tsx
src/layouts/AppLayout.tsx
src/config/env.ts
src/api/client.ts
src/styles/globals.css
src/pages/DashboardPage.tsx
src/pages/ProofsPage.tsx
src/pages/ProofDetailPage.tsx
src/pages/AuditPage.tsx
src/pages/PerformancePage.tsx
src/pages/AboutPage.tsx
src/components/navigation/Sidebar.tsx
src/components/navigation/Topbar.tsx
src/components/ui/StatusBadge.tsx
src/components/ui/LoadingState.tsx
src/components/ui/ErrorBanner.tsx
```

## Step 1 — Scaffold App

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

mkdir -p services/regulator-api
cd services/regulator-api

npm create vite@latest frontend -- --template react-ts
cd frontend

npm install
npm install react-router-dom lucide-react recharts
npm install -D tailwindcss @tailwindcss/vite
```

## Step 2 — Create Environment File

```bash
cat > .env.example <<'EOF'
VITE_REGULATOR_API_BASE_URL=http://127.0.0.1:8085
VITE_ZK_PROVER_BASE_URL=http://127.0.0.1:8084
VITE_APP_NAME=AML SMPC Regulator Console
EOF

cp .env.example .env
```

## Step 3 — Create Project Structure

```bash
mkdir -p src/api src/config src/routes src/layouts src/styles src/pages
mkdir -p src/components/navigation src/components/ui
```

## Step 4 — Create Env Config

```bash
cat > src/config/env.ts <<'EOF'
export const env = {
  appName: import.meta.env.VITE_APP_NAME ?? "AML SMPC Regulator Console",
  regulatorApiBaseUrl:
    import.meta.env.VITE_REGULATOR_API_BASE_URL ?? "http://127.0.0.1:8085",
  zkProverBaseUrl:
    import.meta.env.VITE_ZK_PROVER_BASE_URL ?? "http://127.0.0.1:8084",
};
EOF
```

## Step 5 — Create API Client

```bash
cat > src/api/client.ts <<'EOF'
type RequestOptions = {
  timeoutMs?: number;
};

async function request<T>(
  url: string,
  init: RequestInit = {},
  options: RequestOptions = {}
): Promise<T> {
  const controller = new AbortController();
  const timeout = window.setTimeout(
    () => controller.abort(),
    options.timeoutMs ?? 10000
  );

  try {
    const response = await fetch(url, {
      ...init,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(init.headers ?? {}),
      },
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`HTTP ${response.status}: ${body}`);
    }

    return (await response.json()) as T;
  } finally {
    window.clearTimeout(timeout);
  }
}

export const apiClient = {
  get<T>(url: string, options?: RequestOptions) {
    return request<T>(url, { method: "GET" }, options);
  },

  post<T>(url: string, body?: unknown, options?: RequestOptions) {
    return request<T>(
      url,
      {
        method: "POST",
        body: body === undefined ? undefined : JSON.stringify(body),
      },
      options
    );
  },
};
EOF
```

## Step 6 — Create Basic UI Components

```bash
cat > src/components/ui/StatusBadge.tsx <<'EOF'
type StatusBadgeProps = {
  status: string;
};

export function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span className="rounded-full border px-3 py-1 text-xs font-semibold">
      {status}
    </span>
  );
}
EOF

cat > src/components/ui/LoadingState.tsx <<'EOF'
export function LoadingState() {
  return <div className="rounded-xl border p-4 text-sm">Loading...</div>;
}
EOF

cat > src/components/ui/ErrorBanner.tsx <<'EOF'
type ErrorBannerProps = {
  message: string;
};

export function ErrorBanner({ message }: ErrorBannerProps) {
  return (
    <div className="rounded-xl border border-red-300 bg-red-50 p-4 text-sm text-red-700">
      {message}
    </div>
  );
}
EOF
```

## Step 7 — Create Navigation Layout

```bash
cat > src/components/navigation/Sidebar.tsx <<'EOF'
import { NavLink } from "react-router-dom";

const links = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/proofs", label: "Proofs" },
  { to: "/audit", label: "Audit" },
  { to: "/performance", label: "Performance" },
  { to: "/about", label: "About" },
];

export function Sidebar() {
  return (
    <aside className="min-h-screen w-64 border-r bg-slate-950 p-4 text-white">
      <div className="mb-8 text-lg font-bold">AML SMPC</div>
      <nav className="space-y-2">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `block rounded-xl px-4 py-3 text-sm ${
                isActive ? "bg-white text-slate-950" : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
EOF

cat > src/components/navigation/Topbar.tsx <<'EOF'
import { env } from "../../config/env";

export function Topbar() {
  return (
    <header className="border-b bg-white px-6 py-4">
      <h1 className="text-xl font-semibold text-slate-900">{env.appName}</h1>
      <p className="text-sm text-slate-500">Privacy-preserving AML evidence console</p>
    </header>
  );
}
EOF

cat > src/layouts/AppLayout.tsx <<'EOF'
import { Outlet } from "react-router-dom";
import { Sidebar } from "../components/navigation/Sidebar";
import { Topbar } from "../components/navigation/Topbar";

export function AppLayout() {
  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex min-h-screen flex-1 flex-col">
        <Topbar />
        <section className="flex-1 p-6">
          <Outlet />
        </section>
      </main>
    </div>
  );
}
EOF
```

## Step 8 — Create Placeholder Pages

```bash
for page in Dashboard Proofs ProofDetail Audit Performance About; do
  cat > "src/pages/${page}Page.tsx" <<EOF
export function ${page}Page() {
  return (
    <div>
      <h2 className="text-2xl font-bold">${page}</h2>
      <p className="mt-2 text-slate-600">Frontend page ready for implementation.</p>
    </div>
  );
}
EOF
done
```

## Step 9 — Create Routes and App

```bash
cat > src/routes/AppRoutes.tsx <<'EOF'
import { Navigate, createBrowserRouter } from "react-router-dom";
import { AppLayout } from "../layouts/AppLayout";
import { DashboardPage } from "../pages/DashboardPage";
import { ProofsPage } from "../pages/ProofsPage";
import { ProofDetailPage } from "../pages/ProofDetailPage";
import { AuditPage } from "../pages/AuditPage";
import { PerformancePage } from "../pages/PerformancePage";
import { AboutPage } from "../pages/AboutPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: "dashboard", element: <DashboardPage /> },
      { path: "proofs", element: <ProofsPage /> },
      { path: "proofs/:proofId", element: <ProofDetailPage /> },
      { path: "audit", element: <AuditPage /> },
      { path: "performance", element: <PerformancePage /> },
      { path: "about", element: <AboutPage /> },
    ],
  },
]);
EOF

cat > src/App.tsx <<'EOF'
import { RouterProvider } from "react-router-dom";
import { router } from "./routes/AppRoutes";

export default function App() {
  return <RouterProvider router={router} />;
}
EOF

cat > src/main.tsx <<'EOF'
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles/globals.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF
```

## Step 10 — Add Tailwind and Vite Config

```bash
cat > src/styles/globals.css <<'EOF'
@import "tailwindcss";

:root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #0f172a;
  background: #f8fafc;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
}
EOF

cat > vite.config.ts <<'EOF'
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
EOF
```

## Step 11 — Build and Run

```bash
npm run build
npm run dev -- --host 127.0.0.1 --port 5173
```

## Acceptance Criteria

```text
npm run dev works.
npm run build works.
/dashboard opens.
/proofs opens.
/audit opens.
/performance opens.
/about opens.
API base URL is controlled through .env.
```

## Git Commands

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git add aml-system/services/regulator-api/frontend

git commit -m "Add frontend foundation UI scaffold"

git push origin main
```
