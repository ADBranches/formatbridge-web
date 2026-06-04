# PBBF BLISS — Role-Aware UI + Superuser Override Patch Pack

**Purpose:** Make the frontend show only the actions/options a logged-in user is privileged to see, with a **superuser override** across all roles.  
**Execution style:** Independent commands/snippets only. Run each section independently.  
**Repository root:** `/home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth`

---

## Scope verified before patching

The patch plan below is based on the currently inspected structures of:

- `pbbf-telehealth/src/components/layout/Sidebar.jsx`
- `pbbf-telehealth/src/components/layout/Topbar.jsx`
- `pbbf-telehealth/src/shared/constants/navigation.js`
- `pbbf-telehealth/src/shared/constants/roles.js`
- `pbbf-telehealth/src/shared/guards/RoleGuard.jsx`
- `pbbf-telehealth/src/store/authStore.js`
- `pbbf-api/app/modules/auth/schemas.py`
- `pbbf-api/app/modules/auth/service.py`
- `pbbf-api/app/modules/users/schemas.py`
- `pbbf-api/app/modules/users/service.py`

The backend auth/users serializers currently return role and activity state, but **do not currently expose `is_superuser`** in the serialized user payload, so the frontend cannot reliably implement a superuser override until that is added. citeturn54search2

---

# 0. Create a Stage 3 backup directory

## Command 0.1 — Create backup directory variable

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
export STAGE3_UI_ROLE_BACKUP_DIR="backups/stage3_ui_role_visibility_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR"
echo "$STAGE3_UI_ROLE_BACKUP_DIR"
```

---

# 1. Frontend navigation configuration

## File updated

```text
pbbf-telehealth/src/shared/constants/navigation.js
```

## Why this file

This file already defines `allowedRoles`, but the sidebar currently renders all sections/items without applying those rules. The patch adds helper functions for:

- role normalization
- superuser detection
- item access checks
- visible section filtering

## Command 1.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/shared/constants"
cp pbbf-telehealth/src/shared/constants/navigation.js "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/shared/constants/navigation.js"
```

## Command 1.2 — Open file in editor

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
code pbbf-telehealth/src/shared/constants/navigation.js
```

## Command 1.3 — Replace entire file content with

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
        label: "Onboarding",
        shortLabel: "OB",
        to: ROUTES.patient.onboarding.consent,
        allowedRoles: [ROLES.PATIENT],
        description: "Patient consent and intake onboarding",
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
        allowedRoles: [
          ROLES.PROVIDER,
          ROLES.COUNSELOR,
          ROLES.LACTATION_CONSULTANT,
          ROLES.CARE_COORDINATOR,
        ],
        description: "Clinical overview and assigned work",
      },
      {
        label: "Notes",
        shortLabel: "NT",
        to: ROUTES.provider.notes,
        allowedRoles: [
          ROLES.PROVIDER,
          ROLES.COUNSELOR,
          ROLES.LACTATION_CONSULTANT,
        ],
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

export function normalizeRole(role) {
  return String(role || "").trim().toLowerCase();
}

export function isSuperuser(user) {
  return Boolean(user?.is_superuser || user?.isSuperuser);
}

export function canAccessNavItem(user, item) {
  if (isSuperuser(user)) return true;
  const role = normalizeRole(user?.role);
  return item.allowedRoles?.includes(role);
}

export function getVisibleNavigationSections(user) {
  if (isSuperuser(user)) return NAVIGATION_SECTIONS;

  return NAVIGATION_SECTIONS
    .map((section) => ({
      ...section,
      items: section.items.filter((item) => canAccessNavItem(user, item)),
    }))
    .filter((section) => section.items.length > 0);
}
```

---

# 2. Frontend sidebar rendering

## File updated

```text
pbbf-telehealth/src/components/layout/Sidebar.jsx
```

## Why this file

This is the current root cause. The current sidebar renders **every** section/item from `NAVIGATION_SECTIONS` and ignores `allowedRoles`.

## Command 2.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/components/layout"
cp pbbf-telehealth/src/components/layout/Sidebar.jsx "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/components/layout/Sidebar.jsx"
```

## Command 2.2 — Open file in editor

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
code pbbf-telehealth/src/components/layout/Sidebar.jsx
```

## Command 2.3 — Replace entire file content with

```jsx
import { useMemo } from "react";
import { NavLink } from "react-router-dom";

import { useAuthStore } from "../../store/authStore";
import {
  getVisibleNavigationSections,
  isSuperuser,
} from "../../shared/constants/navigation";

function getNavItemClassName(isActive) {
  return [
    "group flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition-all",
    isActive
      ? "bg-blue-600 text-white shadow-sm"
      : "text-slate-700 hover:bg-slate-100 hover:text-slate-900",
  ].join(" ");
}

function formatRoleLabel(user) {
  if (isSuperuser(user)) return "Superuser";
  return String(user?.role || "workspace")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

export default function Sidebar() {
  const user = useAuthStore((state) => state.user);

  const sections = useMemo(() => getVisibleNavigationSections(user), [user]);

  return (
    <aside className="sticky top-0 hidden min-h-screen w-72 shrink-0 border-r border-slate-200 bg-white/90 backdrop-blur lg:block">
      <div className="flex h-full flex-col px-4 py-5">
        <div className="rounded-2xl bg-slate-900 px-4 py-4 text-white shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-300">
            Post Baby Bliss
          </p>
          <h1 className="mt-2 text-lg font-semibold">BLISS Telehealth</h1>
          <p className="mt-1 text-sm text-slate-300">{formatRoleLabel(user)} workspace</p>
        </div>

        <nav className="mt-6 flex-1 space-y-6" aria-label="Sidebar navigation">
          {sections.map((section) => (
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
                    <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-black/5 text-xs font-semibold">
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
          <p className="text-sm font-medium text-slate-900">Role-aware workspace</p>
          <p className="mt-1 text-xs leading-5 text-slate-600">
            Visible options are filtered by your granted role and superuser status.
          </p>
        </div>
      </div>
    </aside>
  );
}
```

---

# 3. Frontend topbar role display

## File updated

```text
pbbf-telehealth/src/components/layout/Topbar.jsx
```

## Why this file

Topbar is not the source of the wrong sidebar bug, but it should be made role-aware so the UI looks consistent and professional.

## Command 3.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/components/layout"
cp pbbf-telehealth/src/components/layout/Topbar.jsx "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/components/layout/Topbar.jsx"
```

## Command 3.2 — Open file in editor

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
code pbbf-telehealth/src/components/layout/Topbar.jsx
```

## Command 3.3 — Replace entire file content with

```jsx
import { useMemo } from "react";
import { useLocation } from "react-router-dom";

import { useAuthStore } from "../../store/authStore";
import {
  isSuperuser,
  NAVIGATION_ITEMS_BY_PATH,
} from "../../shared/constants/navigation";

function resolvePageMeta(pathname) {
  return (
    NAVIGATION_ITEMS_BY_PATH[pathname] ?? {
      label: "Workspace",
      description: "BLISS Telehealth application workspace",
    }
  );
}

function getUserInitials(user) {
  const fullName = String(user?.full_name || user?.fullName || "").trim();
  if (!fullName) return "PB";

  const parts = fullName.split(/\s+/).filter(Boolean);
  return parts.slice(0, 2).map((part) => part[0]?.toUpperCase()).join("") || "PB";
}

function getRoleLabel(user) {
  if (isSuperuser(user)) return "Superuser";
  return String(user?.role || "workspace")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

export default function Topbar() {
  const location = useLocation();
  const user = useAuthStore((state) => state.user);

  const pageMeta = useMemo(() => resolvePageMeta(location.pathname), [location.pathname]);

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/85 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Current workspace
          </p>
          <h2 className="truncate text-xl font-semibold text-slate-900">{pageMeta.label}</h2>
          <p className="truncate text-sm text-slate-600">{pageMeta.description}</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden rounded-full border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-600 sm:block">
            {getRoleLabel(user)}
          </div>

          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white shadow-sm">
            {getUserInitials(user)}
          </div>
        </div>
      </div>
    </header>
  );
}
```

---

# 4. Route-level role guard with superuser bypass

## File updated

```text
pbbf-telehealth/src/shared/guards/RoleGuard.jsx
```

## Why this file

Route access is already working, but if superuser must have exclusive rights across all roles, `RoleGuard` must explicitly honor that.

## Command 4.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/shared/guards"
cp pbbf-telehealth/src/shared/guards/RoleGuard.jsx "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/shared/guards/RoleGuard.jsx"
```

## Command 4.2 — Open file in editor

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
code pbbf-telehealth/src/shared/guards/RoleGuard.jsx
```

## Command 4.3 — Replace entire file content with

```jsx
import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import { ROUTES } from "../constants/routes";

function isSuperuser(user) {
  return Boolean(user?.is_superuser || user?.isSuperuser);
}

function getHomePathForRole(user) {
  if (isSuperuser(user)) return ROUTES.admin.dashboard;

  switch (user?.role) {
    case "admin":
      return ROUTES.admin.dashboard;
    case "provider":
    case "counselor":
    case "care_coordinator":
    case "lactation_consultant":
      return ROUTES.provider.dashboard;
    case "patient":
    default:
      return ROUTES.patient.dashboard;
  }
}

export default function RoleGuard({ allowedRoles = [], children }) {
  const user = useAuthStore((state) => state.user);

  if (!allowedRoles.length) {
    return children || <Outlet />;
  }

  if (isSuperuser(user)) {
    return children || <Outlet />;
  }

  if (!user?.role || !allowedRoles.includes(user.role)) {
    return <Navigate to={getHomePathForRole(user)} replace />;
  }

  return children || <Outlet />;
}
```

---

# 5. Frontend auth store helper update

## File updated

```text
pbbf-telehealth/src/store/authStore.js
```

## Why this file

The store already keeps `user`, but `hasRole()` should honor superuser so any local UI checks behave consistently.

## Command 5.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/store"
cp pbbf-telehealth/src/store/authStore.js "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-telehealth/src/store/authStore.js"
```

## Command 5.2 — Open file at the `hasRole` function

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
code -g pbbf-telehealth/src/store/authStore.js:165
```

## Command 5.3 — Replace only the `hasRole` function with

```js
function hasRole(allowedRoles = []) {
  if (!allowedRoles.length) return true;

  const user = state.user;
  if (user?.is_superuser || user?.isSuperuser) return true;

  const role = user?.role;
  return allowedRoles.includes(role);
}
```

---

# 6. Backend auth schema — expose superuser flag to frontend

## File updated

```text
pbbf-api/app/modules/auth/schemas.py
```

## Why this file

The frontend cannot honor superuser override unless the backend actually returns `is_superuser` in the auth payload. The inspected auth schema currently exposes role and is_active, but not `is_superuser`. citeturn54search2

## Command 6.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-api/app/modules/auth"
cp pbbf-api/app/modules/auth/schemas.py "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-api/app/modules/auth/schemas.py"
```

## Command 6.2 — Open file in editor

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
code pbbf-api/app/modules/auth/schemas.py
```

## Command 6.3 — In `AuthUserResponse`, add this field

```python
    is_superuser: bool = False
```

### Resulting shape should be

```python
class AuthUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | int
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    is_active: bool
    is_superuser: bool = False
    role: str
```

---

# 7. Backend auth service — serialize superuser flag

## File updated

```text
pbbf-api/app/modules/auth/service.py
```

## Why this file

The inspected `_serialize_user()` currently returns id/email/full_name/phone_number/is_active/role, but not `is_superuser`. citeturn54search2

## Command 7.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-api/app/modules/auth"
cp pbbf-api/app/modules/auth/service.py "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-api/app/modules/auth/service.py"
```

## Command 7.2 — Open file at `_serialize_user`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
code -g pbbf-api/app/modules/auth/service.py:15
```

## Command 7.3 — Add this line inside the returned dict

```python
            "is_superuser": getattr(user, "is_superuser", False),
```

### Resulting block should be

```python
    @staticmethod
    def _serialize_user(user):
        role_name = getattr(getattr(user, "role", None), "name", None)
        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "phone_number": getattr(user, "phone_number", None),
            "is_active": user.is_active,
            "is_superuser": getattr(user, "is_superuser", False),
            "role": role_name or "unknown",
        }
```

---

# 8. Backend users schema — expose superuser flag on /users/me and admin user views

## File updated

```text
pbbf-api/app/modules/users/schemas.py
```

## Why this file

`/users/me` and user-management responses should stay aligned with auth payload shape.

## Command 8.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-api/app/modules/users"
cp pbbf-api/app/modules/users/schemas.py "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-api/app/modules/users/schemas.py"
```

## Command 8.2 — Open file in editor

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
code pbbf-api/app/modules/users/schemas.py
```

## Command 8.3 — In `UserProfileResponse`, add this field

```python
    is_superuser: bool = False
```

### Resulting shape should be

```python
class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | int
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    is_active: bool
    is_superuser: bool = False
    role: str
```

---

# 9. Backend users service — serialize superuser flag

## File updated

```text
pbbf-api/app/modules/users/service.py
```

## Why this file

The inspected users service serializer also omits `is_superuser`. citeturn54search2

## Command 9.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-api/app/modules/users"
cp pbbf-api/app/modules/users/service.py "$STAGE3_UI_ROLE_BACKUP_DIR/pbbf-api/app/modules/users/service.py"
```

## Command 9.2 — Open file at `_serialize_user`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
code -g pbbf-api/app/modules/users/service.py:10
```

## Command 9.3 — Add this line inside the returned dict

```python
            "is_superuser": getattr(user, "is_superuser", False),
```

### Resulting block should be

```python
    @staticmethod
    def _serialize_user(user) -> dict:
        role_name = getattr(getattr(user, "role", None), "name", None)
        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "phone_number": getattr(user, "phone_number", None),
            "is_active": user.is_active,
            "is_superuser": getattr(user, "is_superuser", False),
            "role": role_name or "unknown",
        }
```

---

# 10. Optional frontend test updates

## File to inspect/update

```text
pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx
```

## Recommended checks to add

- patient sees only patient items
- provider sees only provider items
- care coordinator sees dashboard + referrals only
- admin sees only admin items
- superuser sees all sections

## Command 10.1 — Inspect existing sidebar test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
sed -n '1,260p' pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx
```

---

# 11. Validation commands

Run these independently after patching.

## Command 11.1 — Backend syntax check

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
source .venv/bin/activate
python -m py_compile app/modules/auth/schemas.py app/modules/auth/service.py app/modules/users/schemas.py app/modules/users/service.py
```

## Command 11.2 — Frontend build

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm run build
```

## Command 11.3 — Manual login behavior verification

```text
1. Log in as patient@example.com      -> only patient sidebar items visible
2. Log in as provider@example.com     -> only provider sidebar items visible
3. Log in as care.coordinator@example.com -> provider-lite/coordinator-safe items only
4. Log in as admin@example.com        -> only admin sidebar items visible
5. Log in as a superuser account      -> all sections visible
```

---

# 12. Completion checklist

```text
[ ] Sidebar shows only allowed items for the logged-in role.
[ ] Admin no longer sees patient sidebar items.
[ ] Provider no longer sees patient or admin sidebar items.
[ ] Care coordinator sees only coordinator-safe/provider-lite options.
[ ] Superuser bypasses role-based UI restrictions.
[ ] Backend auth payload includes is_superuser.
[ ] Backend users/me payload includes is_superuser.
[ ] Frontend build passes.
[ ] Manual login checks pass for all target roles.
```

---

# 13. Boundary

This patch pack focuses on **frontend role-aware visibility** and **superuser override support**.  
It does **not** replace backend object-level authorization and should be used alongside the existing backend guards and permissions already implemented in Stage 2.
