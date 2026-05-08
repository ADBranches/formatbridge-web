# AML SMPC – Full Demo Alignment Implementation Timeline

## Purpose
This timeline describes **exact, verified work** required to bring the AML SMPC system to **100% parity with the report**, based strictly on the **actual backend implementation discovered** (not assumptions).

This is a *completion and hardening timeline*, not a greenfield plan.

---

## Verified Current State (as of discovery)

✅ Partner-bank onboarding – implemented
✅ RBAC & permission enforcement – implemented
✅ Bank-side risk evaluation – implemented
✅ SMPC risk linkage – implemented
✅ **Regulator anomaly case backend – already implemented**
✅ **Institution anomaly notice backend – already implemented**

❌ Frontend anomaly case pages – missing
❌ Frontend anomaly notice pages – missing
⚠️ Some lifecycle states not surfaced in UI
⚠️ Report wording slightly ahead of UI

---

## Phase 5C – Backend Anomaly Case APIs

### Status: ✅ COMPLETE (no code required)

The following endpoints already exist and are functional:

- `GET  /regulator/anomaly-cases`
- `POST /regulator/anomaly-cases`
- `GET  /regulator/anomaly-cases/:case_id`
- `POST /regulator/anomaly-cases/:case_id/close`
- `GET  /institution/anomaly-notices`
- `GET  /institution/anomaly-notices/:case_id`
- `POST /institution/anomaly-notices/:case_id/respond`

Verified in:
- `src/anomaly_cases.rs`
- `src/routes.rs`

✅ RBAC guards present
✅ Audit logs emitted
✅ Bank notification rows created

**Action:** No backend work needed.

---

## Phase 5D – Frontend Anomaly Case UI (MAIN WORK)

### Goal
Make existing backend functionality **visible and usable** in the UI.

### Required Pages

#### Regulator
- `/regulator/anomaly-cases`
- `/regulator/anomaly-cases/:case_id`

Capabilities:
- List cases
- View case details
- Close case

#### Institution
- `/institution/anomaly-notices`
- `/institution/anomaly-notices/:case_id`

Capabilities:
- View notices for own organization
- Submit response

---

### Implementation Order

**Day 1**
1. Add frontend API client: `src/api/anomalyCases.ts`
2. Regulator case list page
3. Regulator case detail page

**Day 2**
4. Institution notice list page
5. Institution notice detail + respond form
6. Sidebar + routing integration

---

## Phase 5E – End-to-End Validation

### Terminal Validation

```bash
# Regulator creates case
# Institution responds
# Regulator closes case
```

Audit check:

```sql
SELECT event_type FROM audit_logs
WHERE event_type LIKE '%anomaly%'
ORDER BY created_at DESC;
```

Expected:
- `regulator_anomaly_case_opened`
- `institution_anomaly_case_responded`
- `regulator_anomaly_case_closed`

---

## Phase 6 – Report & Demo Alignment

### Required Report Adjustment

Replace any wording suggesting *planned* anomaly cases with:

> “The anomaly case workflow is implemented end‑to‑end, with regulator‑initiated cases, institution responses, and full audit traceability. The demo focuses on a single‑transaction review path.”

---

## Final Timeline Summary

| Phase | Duration |
|-----|----------|
| Phase 5C | 0 days |
| Phase 5D | 2 days |
| Phase 5E | 1 day |
| Phase 6 | 0.5 day |

**Total remaining time: ~3.5 days**

---

## Status After Completion

✅ All report claims demonstrable
✅ No overstatement
✅ Clean regulator → bank workflow
✅ Confident defense-ready demo
