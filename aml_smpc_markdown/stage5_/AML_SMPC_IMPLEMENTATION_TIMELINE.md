# AML‑SMPC Missing & Partial Implementation Timeline

> **Rule observed:** This Markdown is provided as a **real, downloadable file**, not inline text.

Scope: Completing **only what is missing or partially implemented**, based strictly on the **verified codebase state**.

---

## Phase 1 — Frontend Structure Alignment

**Objective**  
Confirm where anomaly-related UI fits within existing frontend routing, role boundaries, and navigation patterns.

**Directories / Files involved**
```
aml-system/services/regulator-api/frontend/src/
├── routes/
│   └── AppRoutes.tsx
├── components/
│   └── navigation/
│       └── Sidebar.tsx
├── pages/
│   ├── institution/
│   ├── regulator/
│   └── super-admin/
```

**Outcome**
- Confident placement for new regulator & institution pages
- No structural refactors later

---

## Phase 2 — Frontend API Client (Anomaly Cases)

**Objective**  
Expose already-existing backend anomaly APIs to the frontend in a reusable, typed way.

**Files involved**
```
aml-system/services/regulator-api/frontend/src/api/
└── anomalyCases.ts   (NEW)
```

**Covers backend endpoints**
- `/regulator/anomaly-cases`
- `/regulator/anomaly-cases/:case_id`
- `/regulator/anomaly-cases/:case_id/close`
- `/institution/anomaly-notices`
- `/institution/anomaly-notices/:case_id`
- `/institution/anomaly-notices/:case_id/respond`

**Outcome**
- Frontend ready to read/write anomaly lifecycle data

---

## Phase 3 — Regulator Anomaly Case UI

**Objective**  
Allow regulators to list, inspect, and close anomaly cases from the UI.

**Files / Directories involved**
```
aml-system/services/regulator-api/frontend/src/
├── pages/
│   └── regulator/
│       ├── AnomalyCases.tsx        (NEW)
│       └── AnomalyCaseDetail.tsx   (NEW)
├── routes/
│   └── AppRoutes.tsx               (MODIFY)
└── components/
    └── navigation/
        └── Sidebar.tsx             (MODIFY)
```

**UI Capabilities**
- View all anomaly cases
- Inspect case evidence & bank notices
- Close anomaly case

---

## Phase 4 — Institution / Bank Anomaly Notice UI

**Objective**  
Enable banks to view and respond to regulator anomaly notices.

**Files / Directories involved**
```
aml-system/services/regulator-api/frontend/src/
├── pages/
│   └── institution/
│       ├── AnomalyNotices.tsx        (NEW)
│       └── AnomalyNoticeDetail.tsx   (NEW)
├── routes/
│   └── AppRoutes.tsx                 (MODIFY)
└── components/
    └── navigation/
        └── Sidebar.tsx               (MODIFY)
```

**UI Capabilities**
- Bank-scoped notice listing
- Read-only case context
- Response submission

---

## Phase 5 — End‑to‑End Demo Validation

**Objective**  
Ensure terminal, UI, and audit logs fully align with report claims.

**Files involved**
```
(Validation only — no code changes)
```

**Validation points**
- Regulator opens anomaly case
- Bank responds
- Regulator closes case
- Audit logs reflect full lifecycle

---

## Phase 6 — Report & Demo Alignment

**Objective**  
Guarantee written report statements match demonstrable system behavior.

**Files involved**
```
docs/
├── final-report.md
├── demo-script.md
├── presentation-slides.md
```

---

## Timeline Summary

| Phase | Estimated Effort |
|-----|------------------|
| Phase 1 | 0.5 day |
| Phase 2 | 0.5 day |
| Phase 3 | 1 day |
| Phase 4 | 1 day |
| Phase 5 | 0.5 day |
| Phase 6 | 0.25 day |

**Total remaining time:** ~3.75 days

---

## Final State After Completion

✅ All report claims demonstrable  
✅ No backend changes required  
✅ Complete regulator ↔ bank anomaly workflow  
✅ Defense‑ready demo
