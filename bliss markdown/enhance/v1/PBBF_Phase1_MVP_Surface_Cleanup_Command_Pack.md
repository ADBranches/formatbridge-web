# PBBF BLISS — Phase 1 Command Pack

## Phase 1 objective
Hide or remove UI features that the MVP backlog explicitly defers beyond Release 1 or that are still obvious placeholders, so the shipped product exposes only features that are truly supported. Based on the inspected code and backlog alignment, the immediate candidates are **Patient Messages**, **Patient Resources**, and **Admin Settings**. citeturn74search1turn78search8

## Important implementation boundary
This Phase 1 pack only patches files whose structures have already been inspected directly in the conversation:

- `pbbf-telehealth/src/shared/constants/routes.js` citeturn78search8
- `pbbf-telehealth/src/shared/constants/navigation.js` citeturn78search8
- `pbbf-telehealth/src/app/AppRoutes.jsx` citeturn78search8
- `pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx` *(inspected earlier in the conversation and already updated once for role-aware navigation)* citeturn78search8

The page files below are **not deleted** in this phase; they are simply removed from the shipped route/nav surface so the MVP does not expose deferred or placeholder workflows:

- `pbbf-telehealth/src/pages/patient/Messages.jsx` citeturn78search8
- `pbbf-telehealth/src/pages/patient/Resources.jsx` citeturn78search8
- `pbbf-telehealth/src/pages/admin/Settings.jsx` *(explicit placeholder shell)* citeturn78search8

For any **other** route/navigation tests under `pbbf-telehealth/src/app/__tests__`, `pbbf-telehealth/src/modules/admin/__tests__`, or patient-page tests, this pack includes **inspection commands only** first, because their structures were not fully inspected yet and should not be edited blindly. citeturn78search8

---

# 0) Go to repo root and create a dedicated backup area

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
export PHASE1_MVP_CLEANUP_BACKUP_DIR="backups/phase1_mvp_surface_cleanup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$PHASE1_MVP_CLEANUP_BACKUP_DIR"
echo "$PHASE1_MVP_CLEANUP_BACKUP_DIR"
```

---

# 1) Reconfirm the exact files we are patching in this phase

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

sed -n '1,260p' pbbf-telehealth/src/shared/constants/routes.js
sed -n '1,320p' pbbf-telehealth/src/shared/constants/navigation.js
sed -n '1,320p' pbbf-telehealth/src/app/AppRoutes.jsx
sed -n '1,260p' pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx
```

---

# 2) Back up the confirmed patch targets

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

mkdir -p "$PHASE1_MVP_CLEANUP_BACKUP_DIR/pbbf-telehealth/src/shared/constants"
mkdir -p "$PHASE1_MVP_CLEANUP_BACKUP_DIR/pbbf-telehealth/src/app"
mkdir -p "$PHASE1_MVP_CLEANUP_BACKUP_DIR/pbbf-telehealth/src/components/layout/__tests__"

cp pbbf-telehealth/src/shared/constants/routes.js "$PHASE1_MVP_CLEANUP_BACKUP_DIR/pbbf-telehealth/src/shared/constants/routes.js"
cp pbbf-telehealth/src/shared/constants/navigation.js "$PHASE1_MVP_CLEANUP_BACKUP_DIR/pbbf-telehealth/src/shared/constants/navigation.js"
cp pbbf-telehealth/src/app/AppRoutes.jsx "$PHASE1_MVP_CLEANUP_BACKUP_DIR/pbbf-telehealth/src/app/AppRoutes.jsx"
cp pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx "$PHASE1_MVP_CLEANUP_BACKUP_DIR/pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx"
```

---

# 3) Patch `routes.js`

## What changes here
- remove `messages` from patient routes
- remove `resources` from patient routes
- remove `settings` from admin routes
- remove matching route-title entries

The current inspected route constants still expose those pages. citeturn78search8

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; p=Path("pbbf-telehealth/src/shared/constants/routes.js"); p.write_text("""export const ROUTES = {\n  root: \"/\",\n  login: \"/login\",\n  register: \"/register\",\n  forgotPassword: \"/forgot-password\",\n\n  patient: {\n    dashboard: \"/patient/dashboard\",\n    onboarding: {\n      consent: \"/patient/onboarding/consent\",\n      intake: \"/patient/onboarding/intake\",\n    },\n    appointments: \"/patient/appointments\",\n    bookAppointment: \"/patient/appointments/book\",\n    screening: \"/patient/screening\",\n    session: \"/patient/session\",\n    carePlan: \"/patient/care-plan\",\n  },\n\n  provider: {\n    dashboard: \"/provider/dashboard\",\n    notes: \"/provider/notes\",\n    referrals: \"/provider/referrals\",\n  },\n\n  admin: {\n    dashboard: \"/admin/dashboard\",\n    users: \"/admin/users\",\n    reports: \"/admin/reports\",\n    auditLogs: \"/admin/audit-logs\",\n  },\n};\n\nexport const ROUTE_TITLES = {\n  [ROUTES.login]: \"Login\",\n  [ROUTES.register]: \"Register\",\n  [ROUTES.forgotPassword]: \"Forgot Password\",\n\n  [ROUTES.patient.dashboard]: \"Patient Dashboard\",\n  [ROUTES.patient.onboarding.consent]: \"Consent\",\n  [ROUTES.patient.onboarding.intake]: \"Intake Form\",\n  [ROUTES.patient.appointments]: \"My Appointments\",\n  [ROUTES.patient.bookAppointment]: \"Book Appointment\",\n  [ROUTES.patient.screening]: \"Screening\",\n  [ROUTES.patient.session]: \"Session Access\",\n  [ROUTES.patient.carePlan]: \"Care Plan\",\n\n  [ROUTES.provider.dashboard]: \"Provider Dashboard\",\n  [ROUTES.provider.notes]: \"Encounter Notes\",\n  [ROUTES.provider.referrals]: \"Provider Referrals\",\n\n  [ROUTES.admin.dashboard]: \"Admin Dashboard\",\n  [ROUTES.admin.users]: \"Users\",\n  [ROUTES.admin.reports]: \"Reports\",\n  [ROUTES.admin.auditLogs]: \"Audit Logs\",\n};\n""", encoding="utf-8")'
```

---

# 4) Patch `navigation.js`

## What changes here
- remove **Messages** from patient navigation
- remove **Resources** from patient navigation
- remove **Settings** from admin navigation
- keep role-aware filtering helpers intact

The inspected navigation still includes those items in the shipped menu. citeturn78search8

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; p=Path("pbbf-telehealth/src/shared/constants/navigation.js"); p.write_text("""import { ROUTES } from \"./routes\";\nimport { ROLES } from \"./roles\";\n\nexport const NAVIGATION_SECTIONS = [\n  {\n    label: \"Patient\",\n    items: [\n      {\n        label: \"Dashboard\",\n        shortLabel: \"PD\",\n        to: ROUTES.patient.dashboard,\n        allowedRoles: [ROLES.PATIENT],\n        description: \"Patient home and care overview\",\n      },\n      {\n        label: \"Onboarding\",\n        shortLabel: \"OB\",\n        to: ROUTES.patient.onboarding.consent,\n        allowedRoles: [ROLES.PATIENT],\n        description: \"Patient consent and intake onboarding\",\n      },\n      {\n        label: \"Appointments\",\n        shortLabel: \"AP\",\n        to: ROUTES.patient.appointments,\n        allowedRoles: [ROLES.PATIENT],\n        description: \"Patient booking and visit history\",\n      },\n      {\n        label: \"Screening\",\n        shortLabel: \"SC\",\n        to: ROUTES.patient.screening,\n        allowedRoles: [ROLES.PATIENT],\n        description: \"Patient self-screening and assessment\",\n      },\n      {\n        label: \"Session\",\n        shortLabel: \"VS\",\n        to: ROUTES.patient.session,\n        allowedRoles: [ROLES.PATIENT],\n        description: \"Virtual session access and guidance\",\n      },\n      {\n        label: \"Care Plan\",\n        shortLabel: \"CP\",\n        to: ROUTES.patient.carePlan,\n        allowedRoles: [ROLES.PATIENT],\n        description: \"Follow-up and care plan summary\",\n      },\n    ],\n  },\n\n  {\n    label: \"Provider\",\n    items: [\n      {\n        label: \"Dashboard\",\n        shortLabel: \"PR\",\n        to: ROUTES.provider.dashboard,\n        allowedRoles: [\n          ROLES.PROVIDER,\n          ROLES.COUNSELOR,\n          ROLES.LACTATION_CONSULTANT,\n          ROLES.CARE_COORDINATOR,\n        ],\n        description: \"Clinical overview and assigned work\",\n      },\n      {\n        label: \"Notes\",\n        shortLabel: \"NT\",\n        to: ROUTES.provider.notes,\n        allowedRoles: [\n          ROLES.PROVIDER,\n          ROLES.COUNSELOR,\n          ROLES.LACTATION_CONSULTANT,\n        ],\n        description: \"Encounter documentation workspace\",\n      },\n      {\n        label: \"Referrals\",\n        shortLabel: \"RF\",\n        to: ROUTES.provider.referrals,\n        allowedRoles: [ROLES.PROVIDER, ROLES.CARE_COORDINATOR],\n        description: \"Referral follow-up and handoff tracking\",\n      },\n    ],\n  },\n\n  {\n    label: \"Admin\",\n    items: [\n      {\n        label: \"Dashboard\",\n        shortLabel: \"AD\",\n        to: ROUTES.admin.dashboard,\n        allowedRoles: [ROLES.ADMIN],\n        description: \"Operations dashboard and summary metrics\",\n      },\n      {\n        label: \"Users\",\n        shortLabel: \"US\",\n        to: ROUTES.admin.users,\n        allowedRoles: [ROLES.ADMIN],\n        description: \"User and role administration\",\n      },\n      {\n        label: \"Reports\",\n        shortLabel: \"RP\",\n        to: ROUTES.admin.reports,\n        allowedRoles: [ROLES.ADMIN],\n        description: \"Reporting and exports\",\n      },\n      {\n        label: \"Audit Logs\",\n        shortLabel: \"AL\",\n        to: ROUTES.admin.auditLogs,\n        allowedRoles: [ROLES.ADMIN],\n        description: \"Audit and governance activity\",\n      },\n    ],\n  },\n];\n\nexport const NAVIGATION_ITEMS = NAVIGATION_SECTIONS.flatMap((section) => section.items);\n\nexport const NAVIGATION_ITEMS_BY_PATH = Object.fromEntries(\n  NAVIGATION_ITEMS.map((item) => [\n    item.to,\n    {\n      label: item.label,\n      description: item.description,\n    },\n  ])\n);\n\nexport function normalizeRole(role) {\n  return String(role || \"\").trim().toLowerCase();\n}\n\nexport function isSuperuser(user) {\n  return Boolean(user?.is_superuser || user?.isSuperuser);\n}\n\nexport function canAccessNavItem(user, item) {\n  if (isSuperuser(user)) return true;\n  const role = normalizeRole(user?.role);\n  return item.allowedRoles?.includes(role);\n}\n\nexport function getVisibleNavigationSections(user) {\n  if (isSuperuser(user)) return NAVIGATION_SECTIONS;\n\n  return NAVIGATION_SECTIONS\n    .map((section) => ({\n      ...section,\n      items: section.items.filter((item) => canAccessNavItem(user, item)),\n    }))\n    .filter((section) => section.items.length > 0);\n}\n""", encoding="utf-8")'
```

---

# 5) Patch `AppRoutes.jsx`

## What changes here
- remove imports for `PatientMessagesPage`, `PatientResourcesPage`, and `AdminSettingsPage`
- remove their corresponding routes from the shipped route map
- leave the physical page files on disk for later post-MVP work, but make them unreachable in production navigation/routes

The current route map still exposes all three pages. citeturn78search8

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; p=Path("pbbf-telehealth/src/app/AppRoutes.jsx"); p.write_text("""import { Navigate, Route, Routes } from \"react-router-dom\";\n\nimport AppLayout from \"./AppLayout\";\nimport ProtectedRoute from \"../routes/ProtectedRoute\";\nimport { ROUTES } from \"../shared/constants/routes\";\n\nimport LoginPage from \"../pages/auth/Login\";\nimport RegisterPage from \"../modules/auth/pages/Register\";\nimport ForgotPasswordPage from \"../modules/auth/pages/ForgotPassword\";\n\nimport ConsentPage from \"../modules/intake/pages/ConsentPage\";\nimport IntakeFormPage from \"../modules/intake/pages/IntakeFormPage\";\n\nimport BookAppointmentPage from \"../modules/appointments/pages/BookAppointmentPage\";\n\nimport PatientDashboardPage from \"../pages/patient/Dashboard\";\nimport PatientAppointmentsPage from \"../pages/patient/Appointments\";\nimport PatientScreeningPage from \"../pages/patient/Screening\";\nimport PatientSessionPage from \"../pages/patient/Session\";\nimport PatientCarePlanPage from \"../pages/patient/CarePlan\";\n\nimport ProviderDashboardPage from \"../pages/provider/Dashboard\";\nimport ProviderNotesPage from \"../pages/provider/Notes\";\nimport ProviderReferralsPage from \"../pages/provider/Referrals\";\n\nimport AdminDashboardPage from \"../pages/admin/Dashboard\";\nimport AdminUsersPage from \"../pages/admin/Users\";\nimport AdminReportsPage from \"../pages/admin/Reports\";\nimport AdminAuditLogsPage from \"../pages/admin/AuditLogs\";\n\nfunction NotFoundPage() {\n  return (\n    <div className=\"rounded-2xl border border-slate-200 bg-white p-8 shadow-sm\">\n      <h1 className=\"text-2xl font-semibold text-slate-900\">Page not found</h1>\n      <p className=\"mt-2 text-sm text-slate-600\">\n        The page you requested does not exist in the current route map.\n      </p>\n    </div>\n  );\n}\n\nexport default function AppRoutes() {\n  return (\n    <Routes>\n      <Route path={ROUTES.root} element={<Navigate to={ROUTES.login} replace />} />\n\n      <Route path={ROUTES.login} element={<LoginPage />} />\n      <Route path={ROUTES.register} element={<RegisterPage />} />\n      <Route path={ROUTES.forgotPassword} element={<ForgotPasswordPage />} />\n\n      <Route\n        element={\n          <ProtectedRoute allowedRoles={[\"patient\"]}>\n            <AppLayout />\n          </ProtectedRoute>\n        }\n      >\n        <Route path={ROUTES.patient.dashboard} element={<PatientDashboardPage />} />\n        <Route path={ROUTES.patient.onboarding.consent} element={<ConsentPage />} />\n        <Route path={ROUTES.patient.onboarding.intake} element={<IntakeFormPage />} />\n        <Route path={ROUTES.patient.appointments} element={<PatientAppointmentsPage />} />\n        <Route path={ROUTES.patient.bookAppointment} element={<BookAppointmentPage />} />\n        <Route path={ROUTES.patient.screening} element={<PatientScreeningPage />} />\n        <Route path={ROUTES.patient.session} element={<PatientSessionPage />} />\n        <Route path={ROUTES.patient.carePlan} element={<PatientCarePlanPage />} />\n      </Route>\n\n      <Route\n        element={\n          <ProtectedRoute\n            allowedRoles={[\"provider\", \"counselor\", \"care_coordinator\", \"lactation_consultant\"]}\n          >\n            <AppLayout />\n          </ProtectedRoute>\n        }\n      >\n        <Route path={ROUTES.provider.dashboard} element={<ProviderDashboardPage />} />\n        <Route path={ROUTES.provider.notes} element={<ProviderNotesPage />} />\n        <Route path={ROUTES.provider.referrals} element={<ProviderReferralsPage />} />\n      </Route>\n\n      <Route\n        element={\n          <ProtectedRoute allowedRoles={[\"admin\"]}>\n            <AppLayout />\n          </ProtectedRoute>\n        }\n      >\n        <Route path={ROUTES.admin.dashboard} element={<AdminDashboardPage />} />\n        <Route path={ROUTES.admin.users} element={<AdminUsersPage />} />\n        <Route path={ROUTES.admin.reports} element={<AdminReportsPage />} />\n        <Route path={ROUTES.admin.auditLogs} element={<AdminAuditLogsPage />} />\n        <Route path=\"*\" element={<NotFoundPage />} />\n      </Route>\n\n      <Route path=\"*\" element={<Navigate to={ROUTES.login} replace />} />\n    </Routes>\n  );\n}\n""", encoding="utf-8")'
```

---

# 6) Patch `sidebar.test.jsx`

## What changes here
Update the role-aware sidebar test so it stops expecting the removed nav items:
- **patient** should no longer see `Messages` or `Resources`
- **admin** should no longer see `Settings`
- **superuser** should no longer assert `Messages`, `Resources`, or `Settings`

This keeps the shipped MVP surface aligned with the Phase 1 cleanup. citeturn74search1turn78search8

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; p=Path("pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx"); p.write_text("""import { screen } from \"@testing-library/react\";\nimport { describe, expect, it } from \"vitest\";\n\nimport Sidebar from \"../Sidebar\";\nimport { renderWithProviders } from \"../../../test/renderWithProviders\";\n\nfunction authStateFor(user) {\n  return {\n    accessToken: \"test-access-token\",\n    refreshToken: \"test-refresh-token\",\n    expiresAt: Date.now() + 60 * 60 * 1000,\n    user,\n  };\n}\n\ndescribe(\"Sidebar role-aware navigation\", () => {\n  it(\"shows only patient navigation for a patient user\", () => {\n    renderWithProviders(<Sidebar />, {\n      route: \"/patient/dashboard\",\n      authState: authStateFor({\n        role: \"patient\",\n        full_name: \"Patient Example\",\n        is_superuser: false,\n      }),\n    });\n\n    expect(screen.getByText(/^Patient$/)).toBeInTheDocument();\n    expect(screen.queryByText(/^Provider$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Admin$/)).not.toBeInTheDocument();\n\n    expect(screen.getByText(/^Appointments$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Screening$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Care Plan$/)).toBeInTheDocument();\n\n    expect(screen.queryByText(/^Messages$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Resources$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Notes$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Referrals$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Audit Logs$/)).not.toBeInTheDocument();\n  });\n\n  it(\"shows only provider navigation for a provider user\", () => {\n    renderWithProviders(<Sidebar />, {\n      route: \"/provider/dashboard\",\n      authState: authStateFor({\n        role: \"provider\",\n        full_name: \"Provider Example\",\n        is_superuser: false,\n      }),\n    });\n\n    expect(screen.queryByText(/^Patient$/)).not.toBeInTheDocument();\n    expect(screen.getByText(/^Provider$/)).toBeInTheDocument();\n    expect(screen.queryByText(/^Admin$/)).not.toBeInTheDocument();\n\n    expect(screen.getByText(/^Dashboard$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Notes$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Referrals$/)).toBeInTheDocument();\n\n    expect(screen.queryByText(/^Appointments$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Audit Logs$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Settings$/)).not.toBeInTheDocument();\n  });\n\n  it(\"shows coordinator-safe provider-lite navigation for a care coordinator\", () => {\n    renderWithProviders(<Sidebar />, {\n      route: \"/provider/dashboard\",\n      authState: authStateFor({\n        role: \"care_coordinator\",\n        full_name: \"Care Coordinator Example\",\n        is_superuser: false,\n      }),\n    });\n\n    expect(screen.queryByText(/^Patient$/)).not.toBeInTheDocument();\n    expect(screen.getByText(/^Provider$/)).toBeInTheDocument();\n    expect(screen.queryByText(/^Admin$/)).not.toBeInTheDocument();\n\n    expect(screen.getByText(/^Dashboard$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Referrals$/)).toBeInTheDocument();\n\n    expect(screen.queryByText(/^Notes$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Audit Logs$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Appointments$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Settings$/)).not.toBeInTheDocument();\n  });\n\n  it(\"shows only admin navigation for an admin user\", () => {\n    renderWithProviders(<Sidebar />, {\n      route: \"/admin/dashboard\",\n      authState: authStateFor({\n        role: \"admin\",\n        full_name: \"Admin Example\",\n        is_superuser: false,\n      }),\n    });\n\n    expect(screen.queryByText(/^Patient$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Provider$/)).not.toBeInTheDocument();\n    expect(screen.getByText(/^Admin$/)).toBeInTheDocument();\n\n    expect(screen.getByText(/^Users$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Reports$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Audit Logs$/)).toBeInTheDocument();\n\n    expect(screen.queryByText(/^Appointments$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Notes$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Referrals$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Settings$/)).not.toBeInTheDocument();\n  });\n\n  it(\"shows all remaining shipped sections for a superuser\", () => {\n    renderWithProviders(<Sidebar />, {\n      route: \"/admin/dashboard\",\n      authState: authStateFor({\n        role: \"admin\",\n        full_name: \"Super User\",\n        is_superuser: true,\n      }),\n    });\n\n    expect(screen.getByText(/^Patient$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Provider$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Admin$/)).toBeInTheDocument();\n\n    expect(screen.getByText(/^Appointments$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Notes$/)).toBeInTheDocument();\n    expect(screen.getByText(/^Audit Logs$/)).toBeInTheDocument();\n\n    expect(screen.queryByText(/^Messages$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Resources$/)).not.toBeInTheDocument();\n    expect(screen.queryByText(/^Settings$/)).not.toBeInTheDocument();\n  });\n});\n""", encoding="utf-8")'
```

---

# 7) Inspect secondary tests before touching them

## Why this step exists
These tests were mentioned as potential update targets in the plan, but their internal structures have **not** yet been fully inspected in the conversation. To stay consistent with the inspection-first rule, inspect them before making any changes. citeturn78search8

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

find pbbf-telehealth/src/app/__tests__ -type f -maxdepth 2 2>/dev/null | sort | xargs -I{} sh -c 'echo "----- {} -----"; sed -n "1,260p" "{}"; echo'

find pbbf-telehealth/src/modules/admin/__tests__ -type f -maxdepth 2 2>/dev/null | sort | xargs -I{} sh -c 'echo "----- {} -----"; sed -n "1,260p" "{}"; echo'

find pbbf-telehealth/src/pages/patient -type f -maxdepth 1 2>/dev/null | sort | xargs -I{} sh -c 'echo "----- {} -----"; sed -n "1,260p" "{}"; echo'
```

## Fast grep for stale test/page references

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

grep -R -n "patient/messages\|patient/resources\|admin/settings\|Messages\|Resources\|Settings" pbbf-telehealth/src/app/__tests__ pbbf-telehealth/src/modules/admin/__tests__ pbbf-telehealth/src/modules pbbf-telehealth/src/pages 2>/dev/null
```

If those inspections reveal tests that assert the removed pages remain visible, update those specific tests **after** inspection.

---

# 8) Validate the Phase 1 patch

## Re-inspect the patched files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

echo "===== routes.js ====="
sed -n '1,260p' pbbf-telehealth/src/shared/constants/routes.js

echo

echo "===== navigation.js ====="
sed -n '1,320p' pbbf-telehealth/src/shared/constants/navigation.js

echo

echo "===== AppRoutes.jsx ====="
sed -n '1,320p' pbbf-telehealth/src/app/AppRoutes.jsx

echo

echo "===== sidebar.test.jsx ====="
sed -n '1,260p' pbbf-telehealth/src/components/layout/__tests__/sidebar.test.jsx
```

## Run the sidebar test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm test -- --run src/components/layout/__tests__/sidebar.test.jsx
```

## Build the frontend

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm run build
```

---

# 9) Completion checklist for Phase 1

```text
[ ] Messages removed from patient navigation.
[ ] Messages route removed from the shipped route map.
[ ] Resources removed from patient navigation.
[ ] Resources route removed from the shipped route map.
[ ] Admin Settings removed from admin navigation.
[ ] Admin Settings route removed from the shipped route map.
[ ] Sidebar test updated to match the new MVP surface.
[ ] Secondary route/navigation tests inspected before any further edits.
[ ] Frontend build passes after patching.
```

---

# 10) What remains intentionally untouched in Phase 1

- `pbbf-telehealth/src/pages/patient/Messages.jsx`
- `pbbf-telehealth/src/pages/patient/Resources.jsx`
- `pbbf-telehealth/src/pages/admin/Settings.jsx`

Those files remain on disk for later archival/removal or future post-MVP work, but they should no longer be reachable from the production route and navigation surface once this phase is complete. citeturn74search1turn78search8
