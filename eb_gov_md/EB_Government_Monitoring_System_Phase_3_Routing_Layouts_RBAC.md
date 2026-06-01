# Phase 3 — Routing, Layouts and Role-Based Navigation

**Project:** EB Government Monitoring System  
**Frontend:** React + TypeScript + Vite + Tailwind CSS v4  
**Phase Goal:** Create the protected navigation skeleton, role-based route access, sidebar/topbar integration, and placeholder pages for all MVP routes.

---

## Phase 2 Confirmation

Based on the successful `npm run build` output and the visible design system test screen, **Phase 2 is complete**.

Your build passed successfully:

```txt
✓ built in 635ms
```

That means the reusable UI foundation, Tailwind CSS setup, and component imports are working.

> Note: The terminal output where JSON appeared as shell commands happened because JSON content was pasted directly into the terminal instead of into a file. Since `python3 -m json.tool tsconfig.node.json` returned `OK`, the actual JSON file is valid.

---

# Phase 3 Objectives

Phase 3 will implement:

- All major web app routes.
- Protected routes for authenticated users.
- Role-based access guards.
- Role-aware sidebar navigation.
- Stable application layout with sidebar and topbar.
- Placeholder pages for every route so the navigation skeleton is testable immediately.

---

# 1. Create Phase 3 Directories

Run this command from the project root:

```bash
mkdir -p src/app src/config src/hooks src/components/layout
```

---

# 2. Create Phase 3 Files

Run this command from the project root:

```bash
touch src/app/router.tsx src/app/providers.tsx src/config/routes.ts src/config/permissions.ts src/hooks/useAuth.ts src/hooks/usePermissions.ts src/components/layout/ProtectedRoute.tsx src/components/layout/RoleGuard.tsx src/components/layout/AppLayout.tsx src/components/layout/Sidebar.tsx src/components/layout/Topbar.tsx
```

---

# 3. Populate Files

Copy each snippet into the matching file.

---

## `src/config/permissions.ts`

```ts
export const USER_ROLES = {
  SUPER_ADMIN: 'SUPER_ADMIN',
  GOVERNMENT_ADMIN: 'GOVERNMENT_ADMIN',
  CONTRACTOR: 'CONTRACTOR',
  ME_OFFICER: 'ME_OFFICER',
  APPROVAL_AUTHORITY: 'APPROVAL_AUTHORITY',
  AUDITOR: 'AUDITOR',
  DISTRICT_OFFICER: 'DISTRICT_OFFICER',
  MINISTRY_OFFICER: 'MINISTRY_OFFICER',
} as const;

export type UserRole = (typeof USER_ROLES)[keyof typeof USER_ROLES];

export const PERMISSIONS = {
  VIEW_DASHBOARD: 'VIEW_DASHBOARD',

  VIEW_PROJECTS: 'VIEW_PROJECTS',
  CREATE_PROJECT: 'CREATE_PROJECT',
  EDIT_PROJECT: 'EDIT_PROJECT',
  VIEW_PROJECT_DETAILS: 'VIEW_PROJECT_DETAILS',

  VIEW_CONTRACTORS: 'VIEW_CONTRACTORS',
  MANAGE_CONTRACTORS: 'MANAGE_CONTRACTORS',

  VIEW_EVIDENCE: 'VIEW_EVIDENCE',
  UPLOAD_EVIDENCE: 'UPLOAD_EVIDENCE',
  VERIFY_EVIDENCE: 'VERIFY_EVIDENCE',

  VIEW_MONITORING: 'VIEW_MONITORING',
  SUBMIT_MONITORING_REVIEW: 'SUBMIT_MONITORING_REVIEW',
  CREATE_FIELD_INSPECTION: 'CREATE_FIELD_INSPECTION',

  VIEW_APPROVALS: 'VIEW_APPROVALS',
  SUBMIT_APPROVAL_DECISION: 'SUBMIT_APPROVAL_DECISION',

  VIEW_FUNDS: 'VIEW_FUNDS',
  MANAGE_FUNDS: 'MANAGE_FUNDS',

  VIEW_AUDITS: 'VIEW_AUDITS',
  CREATE_AUDIT_FINDING: 'CREATE_AUDIT_FINDING',

  VIEW_REPORTS: 'VIEW_REPORTS',
  VIEW_NOTIFICATIONS: 'VIEW_NOTIFICATIONS',

  VIEW_USERS: 'VIEW_USERS',
  MANAGE_USERS: 'MANAGE_USERS',

  VIEW_SETTINGS: 'VIEW_SETTINGS',
  MANAGE_SETTINGS: 'MANAGE_SETTINGS',

  VIEW_PROFILE: 'VIEW_PROFILE',
} as const;

export type Permission = (typeof PERMISSIONS)[keyof typeof PERMISSIONS];

export const ROLE_PERMISSIONS: Record<UserRole, Permission[]> = {
  [USER_ROLES.SUPER_ADMIN]: Object.values(PERMISSIONS),

  [USER_ROLES.GOVERNMENT_ADMIN]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_PROJECTS,
    PERMISSIONS.CREATE_PROJECT,
    PERMISSIONS.EDIT_PROJECT,
    PERMISSIONS.VIEW_PROJECT_DETAILS,
    PERMISSIONS.VIEW_CONTRACTORS,
    PERMISSIONS.MANAGE_CONTRACTORS,
    PERMISSIONS.VIEW_EVIDENCE,
    PERMISSIONS.VIEW_MONITORING,
    PERMISSIONS.VIEW_APPROVALS,
    PERMISSIONS.VIEW_FUNDS,
    PERMISSIONS.VIEW_AUDITS,
    PERMISSIONS.VIEW_REPORTS,
    PERMISSIONS.VIEW_NOTIFICATIONS,
    PERMISSIONS.VIEW_USERS,
    PERMISSIONS.MANAGE_USERS,
    PERMISSIONS.VIEW_SETTINGS,
    PERMISSIONS.VIEW_PROFILE,
  ],

  [USER_ROLES.CONTRACTOR]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_PROJECTS,
    PERMISSIONS.VIEW_PROJECT_DETAILS,
    PERMISSIONS.VIEW_EVIDENCE,
    PERMISSIONS.UPLOAD_EVIDENCE,
    PERMISSIONS.VIEW_FUNDS,
    PERMISSIONS.VIEW_NOTIFICATIONS,
    PERMISSIONS.VIEW_PROFILE,
  ],

  [USER_ROLES.ME_OFFICER]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_PROJECTS,
    PERMISSIONS.VIEW_PROJECT_DETAILS,
    PERMISSIONS.VIEW_EVIDENCE,
    PERMISSIONS.VERIFY_EVIDENCE,
    PERMISSIONS.VIEW_MONITORING,
    PERMISSIONS.SUBMIT_MONITORING_REVIEW,
    PERMISSIONS.CREATE_FIELD_INSPECTION,
    PERMISSIONS.VIEW_REPORTS,
    PERMISSIONS.VIEW_NOTIFICATIONS,
    PERMISSIONS.VIEW_PROFILE,
  ],

  [USER_ROLES.APPROVAL_AUTHORITY]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_PROJECTS,
    PERMISSIONS.VIEW_PROJECT_DETAILS,
    PERMISSIONS.VIEW_EVIDENCE,
    PERMISSIONS.VIEW_MONITORING,
    PERMISSIONS.VIEW_APPROVALS,
    PERMISSIONS.SUBMIT_APPROVAL_DECISION,
    PERMISSIONS.VIEW_FUNDS,
    PERMISSIONS.MANAGE_FUNDS,
    PERMISSIONS.VIEW_REPORTS,
    PERMISSIONS.VIEW_NOTIFICATIONS,
    PERMISSIONS.VIEW_PROFILE,
  ],

  [USER_ROLES.AUDITOR]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_PROJECTS,
    PERMISSIONS.VIEW_PROJECT_DETAILS,
    PERMISSIONS.VIEW_EVIDENCE,
    PERMISSIONS.VIEW_FUNDS,
    PERMISSIONS.VIEW_AUDITS,
    PERMISSIONS.CREATE_AUDIT_FINDING,
    PERMISSIONS.VIEW_REPORTS,
    PERMISSIONS.VIEW_NOTIFICATIONS,
    PERMISSIONS.VIEW_PROFILE,
  ],

  [USER_ROLES.DISTRICT_OFFICER]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_PROJECTS,
    PERMISSIONS.VIEW_PROJECT_DETAILS,
    PERMISSIONS.VIEW_EVIDENCE,
    PERMISSIONS.VIEW_MONITORING,
    PERMISSIONS.VIEW_REPORTS,
    PERMISSIONS.VIEW_NOTIFICATIONS,
    PERMISSIONS.VIEW_PROFILE,
  ],

  [USER_ROLES.MINISTRY_OFFICER]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_PROJECTS,
    PERMISSIONS.VIEW_PROJECT_DETAILS,
    PERMISSIONS.VIEW_CONTRACTORS,
    PERMISSIONS.VIEW_EVIDENCE,
    PERMISSIONS.VIEW_MONITORING,
    PERMISSIONS.VIEW_APPROVALS,
    PERMISSIONS.VIEW_FUNDS,
    PERMISSIONS.VIEW_REPORTS,
    PERMISSIONS.VIEW_NOTIFICATIONS,
    PERMISSIONS.VIEW_PROFILE,
  ],
};

export function roleHasPermission(role: UserRole, permission: Permission): boolean {
  return ROLE_PERMISSIONS[role]?.includes(permission) ?? false;
}

export function roleHasAnyPermission(
  role: UserRole,
  permissions: Permission[]
): boolean {
  return permissions.some((permission) => roleHasPermission(role, permission));
}
```

---

## `src/config/routes.ts`

```ts
import {
  PERMISSIONS,
  type Permission,
  USER_ROLES,
  type UserRole,
} from './permissions';

export type AppRoute = {
  path: string;
  label: string;
  permission?: Permission;
  allowedRoles?: UserRole[];
  showInSidebar?: boolean;
};

export const PUBLIC_ROUTES = {
  LOGIN: '/login',
  FORGOT_PASSWORD: '/forgot-password',
} as const;

export const PRIVATE_ROUTES = {
  DASHBOARD: '/dashboard',
  PROJECTS: '/projects',
  PROJECT_NEW: '/projects/new',
  PROJECT_DETAILS: '/projects/:projectId',
  PROJECT_EDIT: '/projects/:projectId/edit',
  CONTRACTORS: '/contractors',
  CONTRACTOR_DETAILS: '/contractors/:contractorId',
  EVIDENCE: '/evidence',
  EVIDENCE_DETAILS: '/evidence/:evidenceId',
  MONITORING_REVIEW_QUEUE: '/monitoring/review-queue',
  MONITORING_FIELD_INSPECTIONS: '/monitoring/field-inspections',
  APPROVALS: '/approvals',
  APPROVAL_DETAILS: '/approvals/:approvalId',
  FUNDS: '/funds',
  AUDITS: '/audits',
  REPORTS: '/reports',
  NOTIFICATIONS: '/notifications',
  USERS: '/users',
  SETTINGS: '/settings',
  PROFILE: '/profile',
} as const;

export const DEFAULT_AUTHENTICATED_ROUTE = PRIVATE_ROUTES.DASHBOARD;
export const DEFAULT_PUBLIC_ROUTE = PUBLIC_ROUTES.LOGIN;

export const appRoutes: AppRoute[] = [
  {
    path: PRIVATE_ROUTES.DASHBOARD,
    label: 'Dashboard',
    permission: PERMISSIONS.VIEW_DASHBOARD,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.PROJECTS,
    label: 'Projects',
    permission: PERMISSIONS.VIEW_PROJECTS,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.PROJECT_NEW,
    label: 'New Project',
    permission: PERMISSIONS.CREATE_PROJECT,
  },
  {
    path: PRIVATE_ROUTES.PROJECT_DETAILS,
    label: 'Project Details',
    permission: PERMISSIONS.VIEW_PROJECT_DETAILS,
  },
  {
    path: PRIVATE_ROUTES.PROJECT_EDIT,
    label: 'Edit Project',
    permission: PERMISSIONS.EDIT_PROJECT,
  },
  {
    path: PRIVATE_ROUTES.CONTRACTORS,
    label: 'Contractors',
    permission: PERMISSIONS.VIEW_CONTRACTORS,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.CONTRACTOR_DETAILS,
    label: 'Contractor Details',
    permission: PERMISSIONS.VIEW_CONTRACTORS,
  },
  {
    path: PRIVATE_ROUTES.EVIDENCE,
    label: 'Evidence & Receipts',
    permission: PERMISSIONS.VIEW_EVIDENCE,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.EVIDENCE_DETAILS,
    label: 'Evidence Details',
    permission: PERMISSIONS.VIEW_EVIDENCE,
  },
  {
    path: PRIVATE_ROUTES.MONITORING_REVIEW_QUEUE,
    label: 'M&E Review Queue',
    permission: PERMISSIONS.VIEW_MONITORING,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.MONITORING_FIELD_INSPECTIONS,
    label: 'Field Inspections',
    permission: PERMISSIONS.CREATE_FIELD_INSPECTION,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.APPROVALS,
    label: 'Approvals',
    permission: PERMISSIONS.VIEW_APPROVALS,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.APPROVAL_DETAILS,
    label: 'Approval Details',
    permission: PERMISSIONS.VIEW_APPROVALS,
  },
  {
    path: PRIVATE_ROUTES.FUNDS,
    label: 'Funds',
    permission: PERMISSIONS.VIEW_FUNDS,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.AUDITS,
    label: 'Audits',
    permission: PERMISSIONS.VIEW_AUDITS,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.REPORTS,
    label: 'Reports',
    permission: PERMISSIONS.VIEW_REPORTS,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.NOTIFICATIONS,
    label: 'Notifications',
    permission: PERMISSIONS.VIEW_NOTIFICATIONS,
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.USERS,
    label: 'User Management',
    permission: PERMISSIONS.VIEW_USERS,
    allowedRoles: [USER_ROLES.SUPER_ADMIN, USER_ROLES.GOVERNMENT_ADMIN],
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.SETTINGS,
    label: 'Settings',
    permission: PERMISSIONS.VIEW_SETTINGS,
    allowedRoles: [USER_ROLES.SUPER_ADMIN, USER_ROLES.GOVERNMENT_ADMIN],
    showInSidebar: true,
  },
  {
    path: PRIVATE_ROUTES.PROFILE,
    label: 'Profile',
    permission: PERMISSIONS.VIEW_PROFILE,
  },
];

export function getRouteLabel(pathname: string): string {
  const exactRoute = appRoutes.find((route) => route.path === pathname);

  if (exactRoute) return exactRoute.label;

  if (pathname.startsWith('/projects/')) return 'Project Details';
  if (pathname.startsWith('/contractors/')) return 'Contractor Details';
  if (pathname.startsWith('/evidence/')) return 'Evidence Details';
  if (pathname.startsWith('/approvals/')) return 'Approval Details';

  return 'EB Government Monitoring System';
}
```

---

## `src/hooks/useAuth.ts`

```ts
import { useMemo, useState } from 'react';

import { USER_ROLES, type UserRole } from '@/config/permissions';

type AuthUser = {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  title: string;
};

type LoginPayload = {
  email: string;
  password: string;
  role?: UserRole;
};

const AUTH_STORAGE_KEY = 'eb_gms_auth_user';

const demoUser: AuthUser = {
  id: 'user_demo_admin',
  name: 'Admin User',
  email: 'admin@eb-gms.local',
  role: USER_ROLES.GOVERNMENT_ADMIN,
  title: 'Government Administrator',
};

function readStoredUser(): AuthUser | null {
  try {
    const stored = window.localStorage.getItem(AUTH_STORAGE_KEY);
    return stored ? (JSON.parse(stored) as AuthUser) : demoUser;
  } catch {
    return demoUser;
  }
}

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(() => readStoredUser());

  const isAuthenticated = Boolean(user);

  function login(payload: LoginPayload) {
    const nextUser: AuthUser = {
      id: 'user_demo_login',
      name: 'Demo User',
      email: payload.email,
      role: payload.role || USER_ROLES.GOVERNMENT_ADMIN,
      title: 'Authorized System User',
    };

    window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(nextUser));
    setUser(nextUser);
  }

  function logout() {
    window.localStorage.removeItem(AUTH_STORAGE_KEY);
    setUser(null);
  }

  return useMemo(
    () => ({
      user,
      role: user?.role,
      isAuthenticated,
      login,
      logout,
    }),
    [user, isAuthenticated]
  );
}
```

### Important MVP Note

For Phase 3, `useAuth.ts` uses a temporary demo authenticated user so protected routes can be tested immediately.

In the Authentication phase, this temporary logic will be replaced by real API-based login, token handling, and server-validated sessions.

---

## `src/hooks/usePermissions.ts`

```ts
import {
  roleHasAnyPermission,
  roleHasPermission,
  type Permission,
  type UserRole,
} from '@/config/permissions';
import { useAuth } from './useAuth';

export function usePermissions() {
  const { role } = useAuth();

  function can(permission: Permission): boolean {
    if (!role) return false;
    return roleHasPermission(role, permission);
  }

  function canAny(permissions: Permission[]): boolean {
    if (!role) return false;
    return roleHasAnyPermission(role, permissions);
  }

  function hasRole(allowedRoles: UserRole[]): boolean {
    if (!role) return false;
    return allowedRoles.includes(role);
  }

  return {
    role,
    can,
    canAny,
    hasRole,
  };
}
```

---

## `src/components/layout/ProtectedRoute.tsx`

```tsx
import type { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

import { PUBLIC_ROUTES } from '@/config/routes';
import { useAuth } from '@/hooks/useAuth';

type ProtectedRouteProps = {
  children: ReactNode;
};

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const location = useLocation();
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return (
      <Navigate
        to={PUBLIC_ROUTES.LOGIN}
        replace
        state={{ from: location.pathname }}
      />
    );
  }

  return children;
}
```

---

## `src/components/layout/RoleGuard.tsx`

```tsx
import type { ReactNode } from 'react';

import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import type { Permission, UserRole } from '@/config/permissions';
import { usePermissions } from '@/hooks/usePermissions';

type RoleGuardProps = {
  children: ReactNode;
  permission?: Permission;
  allowedRoles?: UserRole[];
  fallback?: ReactNode;
};

function DefaultUnauthorizedView() {
  return (
    <main className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-[#F4F7FB] px-6 py-10">
      <Card className="max-w-lg text-center">
        <CardHeader>
          <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-red-50 text-xl font-black text-red-600">
            !
          </div>
          <CardTitle>Access Restricted</CardTitle>
          <CardDescription>
            Your current role does not have permission to access this section.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <Button variant="outline" onClick={() => window.history.back()}>
            Go Back
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}

export function RoleGuard({
  children,
  permission,
  allowedRoles,
  fallback,
}: RoleGuardProps) {
  const { can, hasRole } = usePermissions();

  const permissionAllowed = permission ? can(permission) : true;
  const roleAllowed = allowedRoles ? hasRole(allowedRoles) : true;

  if (!permissionAllowed || !roleAllowed) {
    return fallback || <DefaultUnauthorizedView />;
  }

  return children;
}
```

---

## `src/components/layout/Sidebar.tsx`

```tsx
import { NavLink } from 'react-router-dom';
import {
  Bell,
  ClipboardCheck,
  FileText,
  FolderKanban,
  Home,
  Landmark,
  ReceiptText,
  Settings,
  ShieldCheck,
  Users,
  WalletCards,
} from 'lucide-react';

import { appRoutes, PRIVATE_ROUTES } from '@/config/routes';
import { usePermissions } from '@/hooks/usePermissions';
import { cn } from '@/utils/cn';

const routeIcons: Record<string, typeof Home> = {
  [PRIVATE_ROUTES.DASHBOARD]: Home,
  [PRIVATE_ROUTES.PROJECTS]: FolderKanban,
  [PRIVATE_ROUTES.CONTRACTORS]: Users,
  [PRIVATE_ROUTES.FUNDS]: WalletCards,
  [PRIVATE_ROUTES.EVIDENCE]: ReceiptText,
  [PRIVATE_ROUTES.MONITORING_REVIEW_QUEUE]: ClipboardCheck,
  [PRIVATE_ROUTES.MONITORING_FIELD_INSPECTIONS]: ClipboardCheck,
  [PRIVATE_ROUTES.APPROVALS]: ShieldCheck,
  [PRIVATE_ROUTES.AUDITS]: Landmark,
  [PRIVATE_ROUTES.REPORTS]: FileText,
  [PRIVATE_ROUTES.NOTIFICATIONS]: Bell,
  [PRIVATE_ROUTES.USERS]: Users,
  [PRIVATE_ROUTES.SETTINGS]: Settings,
};

export function Sidebar() {
  const { can, hasRole } = usePermissions();

  const visibleRoutes = appRoutes.filter((route) => {
    if (!route.showInSidebar) return false;
    if (route.permission && !can(route.permission)) return false;
    if (route.allowedRoles && !hasRole(route.allowedRoles)) return false;
    return true;
  });

  return (
    <aside className="fixed inset-y-0 left-0 hidden w-68 flex-col bg-[#051931] text-white lg:flex">
      <div className="flex h-16 items-center gap-3 border-b border-white/10 px-5">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#F58420] text-sm font-black">
          EB
        </div>

        <div>
          <p className="text-sm font-bold leading-tight">EB Government</p>
          <p className="text-xs text-slate-300">Monitoring System</p>
        </div>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        {visibleRoutes.map((item) => {
          const Icon = routeIcons[item.path] || Home;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition',
                  isActive
                    ? 'bg-[#009659] text-white'
                    : 'text-slate-300 hover:bg-white/10 hover:text-white'
                )
              }
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          );
        })}
      </nav>

      <div className="border-t border-white/10 p-4 text-xs text-slate-300">
        MVP Navigation Skeleton
      </div>
    </aside>
  );
}
```

---

## `src/components/layout/Topbar.tsx`

```tsx
import { Bell, LogOut, Menu, Search } from 'lucide-react';
import { useLocation } from 'react-router-dom';

import { Avatar } from '@/components/ui/Avatar';
import { Button } from '@/components/ui/Button';
import { getRouteLabel } from '@/config/routes';
import { useAuth } from '@/hooks/useAuth';

export function Topbar() {
  const location = useLocation();
  const { user, logout } = useAuth();
  const title = getRouteLabel(location.pathname);

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6 lg:ml-68">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="sm" className="lg:hidden">
          <Menu className="h-5 w-5" />
        </Button>

        <div>
          <h1 className="text-base font-bold text-slate-950">{title}</h1>
          <p className="text-xs text-slate-500">
            Government Project Accountability Platform
          </p>
        </div>
      </div>

      <div className="hidden w-full max-w-md items-center rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 md:flex">
        <Search className="mr-2 h-4 w-4 text-slate-400" />
        <input
          type="search"
          placeholder="Search projects, contractors, reports..."
          className="w-full bg-transparent text-sm outline-none placeholder:text-slate-400"
        />
      </div>

      <div className="flex items-center gap-3">
        <button
          type="button"
          className="relative rounded-full p-2 text-slate-600 hover:bg-slate-100"
          aria-label="Notifications"
        >
          <Bell className="h-5 w-5" />
          <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-500" />
        </button>

        <div className="hidden text-right md:block">
          <p className="text-sm font-bold text-slate-900">{user?.name}</p>
          <p className="text-xs text-slate-500">{user?.title}</p>
        </div>

        <Avatar name={user?.name || 'User'} />

        <Button variant="ghost" size="sm" onClick={logout} aria-label="Logout">
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
}
```

---

## `src/components/layout/AppLayout.tsx`

```tsx
import { Outlet } from 'react-router-dom';

import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';

export function AppLayout() {
  return (
    <div className="min-h-screen bg-[#F4F7FB]">
      <Sidebar />
      <Topbar />

      <div className="lg:ml-68">
        <Outlet />
      </div>
    </div>
  );
}
```

---

## `src/app/providers.tsx`

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import type { ReactNode } from 'react';

import { useAuth } from '@/hooks/useAuth';

type AppProvidersProps = {
  children: ReactNode;
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 1000 * 60,
    },
    mutations: {
      retry: 0,
    },
  },
});

function AuthBootstrapper({ children }: AppProvidersProps) {
  // This triggers the temporary local auth read during Phase 3.
  // In the Authentication phase, this becomes a real auth/session provider.
  useAuth();

  return children;
}

export function AppProviders({ children }: AppProvidersProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthBootstrapper>{children}</AuthBootstrapper>
    </QueryClientProvider>
  );
}
```

---

## `src/app/router.tsx`

```tsx
import { createBrowserRouter, Navigate } from 'react-router-dom';

import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { AppLayout } from '@/components/layout/AppLayout';
import { ProtectedRoute } from '@/components/layout/ProtectedRoute';
import { RoleGuard } from '@/components/layout/RoleGuard';
import { AuthLayout } from '@/components/layout/AuthLayout';
import { PRIVATE_ROUTES, PUBLIC_ROUTES } from '@/config/routes';
import { PERMISSIONS, USER_ROLES } from '@/config/permissions';
import { useAuth } from '@/hooks/useAuth';

function PlaceholderPage({
  title,
  description,
  badge = 'MVP Route',
}: {
  title: string;
  description: string;
  badge?: string;
}) {
  return (
    <PageContainer>
      <PageHeader
        title={title}
        description={description}
        actions={<Badge variant="success">{badge}</Badge>}
      />

      <Card>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>
            This screen is connected to the Phase 3 routing skeleton.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center">
            <p className="text-sm font-semibold text-slate-700">
              Full business UI for this module will be implemented in its dedicated feature phase.
            </p>
          </div>
        </CardContent>
      </Card>
    </PageContainer>
  );
}

function DashboardPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Dashboard"
        description="Role-aware overview for government project monitoring."
        actions={
          <>
            <Button variant="outline">Export Summary</Button>
            <Button>New Project</Button>
          </>
        }
      />

      <div className="grid gap-6 lg:grid-cols-4">
        {[
          ['Total Projects', '256'],
          ['Active Monitoring', '158'],
          ['Pending Reviews', '42'],
          ['Delayed Projects', '18'],
        ].map(([label, value]) => (
          <Card key={label}>
            <CardHeader>
              <CardDescription>{label}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-4xl font-black text-slate-950">{value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Navigation Skeleton Ready</CardTitle>
          <CardDescription>
            Sidebar, topbar, protected routes, and role guards are active.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p>
            Use the sidebar to test each MVP route. Unauthorized routes are protected by role and permission guards.
          </p>
        </CardContent>
      </Card>
    </PageContainer>
  );
}

function LoginPage() {
  const { login } = useAuth();

  return (
    <AuthLayout>
      <h1 className="text-center text-2xl font-bold text-white">
        EB Government Monitoring System
      </h1>
      <p className="mt-3 text-center text-sm text-slate-200">
        Temporary Phase 3 login placeholder.
      </p>

      <div className="mt-8 grid gap-3">
        <Button
          onClick={() =>
            login({
              email: 'admin@eb-gms.local',
              password: 'demo',
              role: USER_ROLES.GOVERNMENT_ADMIN,
            })
          }
        >
          Continue as Government Admin
        </Button>

        <Button
          variant="outline"
          className="border-white/30 bg-white/10 text-white hover:bg-white/20"
          onClick={() =>
            login({
              email: 'auditor@eb-gms.local',
              password: 'demo',
              role: USER_ROLES.AUDITOR,
            })
          }
        >
          Continue as Auditor
        </Button>
      </div>
    </AuthLayout>
  );
}

function ForgotPasswordPage() {
  return (
    <AuthLayout>
      <h1 className="text-center text-2xl font-bold text-white">Forgot Password</h1>
      <p className="mt-3 text-center text-sm text-slate-200">
        Password reset workflow will be implemented in the authentication phase.
      </p>
    </AuthLayout>
  );
}

function NotFoundPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#F4F7FB] px-6">
      <Card className="max-w-lg text-center">
        <CardHeader>
          <CardTitle>Page Not Found</CardTitle>
          <CardDescription>The requested route does not exist.</CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={() => window.location.assign(PRIVATE_ROUTES.DASHBOARD)}>
            Go to Dashboard
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to={PRIVATE_ROUTES.DASHBOARD} replace />,
  },
  {
    path: PUBLIC_ROUTES.LOGIN,
    element: <LoginPage />,
  },
  {
    path: PUBLIC_ROUTES.FORGOT_PASSWORD,
    element: <ForgotPasswordPage />,
  },
  {
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: PRIVATE_ROUTES.DASHBOARD,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_DASHBOARD}>
            <DashboardPage />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROJECTS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_PROJECTS}>
            <PlaceholderPage title="Projects" description="View and manage government projects." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROJECT_NEW,
        element: (
          <RoleGuard permission={PERMISSIONS.CREATE_PROJECT}>
            <PlaceholderPage title="Create Project" description="Create a new government monitoring project." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROJECT_DETAILS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_PROJECT_DETAILS}>
            <PlaceholderPage title="Project Details" description="View project milestones, funds, evidence, and audit status." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROJECT_EDIT,
        element: (
          <RoleGuard permission={PERMISSIONS.EDIT_PROJECT}>
            <PlaceholderPage title="Edit Project" description="Update government project details." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.CONTRACTORS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_CONTRACTORS}>
            <PlaceholderPage title="Contractors" description="Manage contractors and compliance profiles." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.CONTRACTOR_DETAILS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_CONTRACTORS}>
            <PlaceholderPage title="Contractor Details" description="View contractor profile, projects, and performance history." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.EVIDENCE,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_EVIDENCE}>
            <PlaceholderPage title="Evidence & Receipts" description="Track submitted receipts, invoices, and evidence." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.EVIDENCE_DETAILS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_EVIDENCE}>
            <PlaceholderPage title="Evidence Details" description="Review evidence package and verification history." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.MONITORING_REVIEW_QUEUE,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_MONITORING}>
            <PlaceholderPage title="M&E Review Queue" description="Review contractor submissions and monitoring tasks." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.MONITORING_FIELD_INSPECTIONS,
        element: (
          <RoleGuard permission={PERMISSIONS.CREATE_FIELD_INSPECTION}>
            <PlaceholderPage title="Field Inspections" description="Capture and review field inspection reports." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.APPROVALS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_APPROVALS}>
            <PlaceholderPage title="Approvals" description="Review pending milestone and fund release approvals." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.APPROVAL_DETAILS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_APPROVALS}>
            <PlaceholderPage title="Approval Details" description="Review approval request details and supporting evidence." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.FUNDS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_FUNDS}>
            <PlaceholderPage title="Funds" description="Track budget allocation, release, utilization, and balances." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.AUDITS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_AUDITS}>
            <PlaceholderPage title="Audits" description="Audit projects, evidence, payments, and compliance status." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.REPORTS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_REPORTS}>
            <PlaceholderPage title="Reports" description="Generate project, funds, audit, district, and ministry reports." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.NOTIFICATIONS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_NOTIFICATIONS}>
            <PlaceholderPage title="Notifications" description="View alerts, reminders, review tasks, and approval updates." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.USERS,
        element: (
          <RoleGuard
            permission={PERMISSIONS.VIEW_USERS}
            allowedRoles={[USER_ROLES.SUPER_ADMIN, USER_ROLES.GOVERNMENT_ADMIN]}
          >
            <PlaceholderPage title="User Management" description="Manage users, roles, and access permissions." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.SETTINGS,
        element: (
          <RoleGuard
            permission={PERMISSIONS.VIEW_SETTINGS}
            allowedRoles={[USER_ROLES.SUPER_ADMIN, USER_ROLES.GOVERNMENT_ADMIN]}
          >
            <PlaceholderPage title="Settings" description="Configure ministries, districts, categories, and workflow rules." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROFILE,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_PROFILE}>
            <PlaceholderPage title="Profile" description="View and update current user profile." />
          </RoleGuard>
        ),
      },
    ],
  },
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);
```

---

# 4. Confirm `src/app/main.tsx`

Your `src/app/main.tsx` should still look like this:

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';

import { AppProviders } from './providers';
import { router } from './router';

import '@/styles/index.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <AppProviders>
      <RouterProvider router={router} />
    </AppProviders>
  </React.StrictMode>
);
```

---

# 5. Important Fix If `w-68` or `lg:ml-68` Does Not Work

Tailwind CSS spacing scale may not include `68` by default in some setups. If the sidebar width does not apply correctly, replace:

```txt
w-68
lg:ml-68
```

With arbitrary Tailwind values:

```txt
w-[17rem]
lg:ml-[17rem]
```

Specifically update these files if needed:

```txt
src/components/layout/Sidebar.tsx
src/components/layout/Topbar.tsx
src/components/layout/AppLayout.tsx
```

---

# 6. Run the App

Run:

```bash
npm run dev
```

Visit:

```txt
http://localhost:5173
```

You should be redirected to:

```txt
http://localhost:5173/dashboard
```

---

# 7. Build Test

Run:

```bash
npm run build
```

Expected result:

```txt
✓ built
```

---

# 8. Routes to Test Manually

Open these routes in the browser:

```txt
/login
/forgot-password
/dashboard
/projects
/projects/new
/projects/EB-001
/projects/EB-001/edit
/contractors
/contractors/CON-001
/evidence
/evidence/EVD-001
/monitoring/review-queue
/monitoring/field-inspections
/approvals
/approvals/APP-001
/funds
/audits
/reports
/notifications
/users
/settings
/profile
```

---

# 9. Role Guard Test

To test restricted access:

1. Go to `/login`.
2. Click **Continue as Auditor**.
3. Try opening:

```txt
/users
/settings
```

Expected result:

```txt
Access Restricted
```

Then go back to `/login` and click **Continue as Government Admin** to regain admin access.

---

# 10. Phase 3 Completion Checklist

Phase 3 is complete when:

- `/dashboard` renders inside the sidebar/topbar layout.
- Sidebar displays role-allowed navigation links.
- Topbar shows the current route label.
- `/login` and `/forgot-password` render outside the app layout.
- Protected routes redirect unauthenticated users to `/login`.
- Role guards block unauthorized pages.
- `npm run build` passes.

---

# Phase 3 Expected Output

After completing this phase, the application has:

- A stable route skeleton.
- A protected application shell.
- Sidebar and topbar layout.
- Permission-aware navigation.
- Placeholder pages for all MVP routes.
- A foundation ready for Phase 4: API Client, Services and Data Types.

---

# Next Phase

After Phase 3 passes build and browser testing, proceed to:

```txt
Phase 4: API Client, Services and Data Types
```
