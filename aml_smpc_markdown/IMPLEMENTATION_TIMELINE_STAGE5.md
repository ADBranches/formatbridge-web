# AML SMPC — Completion Timeline for Full Demo Parity

## Objective

Bring the AML SMPC system into **full alignment with the written report** by implementing:
- Missing backend APIs
- Missing frontend flows
- Completing partially implemented stages
- Ensuring every report claim can be demonstrated live via UI + terminal

This timeline assumes:
- Existing backend and frontend are stable
- Changes are applied using **terminal patch workflows only**
- Each phase ends with demonstrable proof

---

## Snapshot: Current Reality vs Report

| Area | Status |
|---|---|
| Partner-bank onboarding | ✅ Complete |
| RBAC enforcement | ✅ Complete |
| Bank-side risk evaluation | ✅ Complete |
| SMPC risk linkage | ✅ Complete |
| Regulator anomaly cases | ⚠️ Schema only |
| Regulator case UI | ❌ Missing |
| Bank response to regulator | ❌ Missing |
| Multi-bank live SMPC | ⚠️ Simulated |

---

## OVERALL TIMELINE (REALISTIC)

| Phase | Scope | Est. Time |
|---|---|---|
| Phase 5C | Backend anomaly case APIs | 1.5 days |
| Phase 5D | Frontend anomaly case UI | 2 days |
| Phase 5E | End-to-end validation | 1 day |
| Phase 6 | Report alignment & demo hardening | 0.5 day |

**Total:** ~5 days

---

# PHASE 5C — Backend Anomaly Case APIs (CRITICAL)

## Goal

Make regulator anomaly cases **real, not just schema-theoretical**.

### APIs to Implement

```text
GET  /regulator/anomaly-cases
POST /regulator/anomaly-cases
GET  /regulator/anomaly-cases/:id
POST /regulator/anomaly-cases/:id/close

GET  /institution/anomaly-notices
GET  /institution/anomaly-notices/:id
POST /institution/anomaly-notices/:id/respond
