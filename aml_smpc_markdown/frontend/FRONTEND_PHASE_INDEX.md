# AML SMPC Frontend Phase Guides

## Purpose

These Markdown guides help the team build a professional browser-based frontend for the AML SMPC project.

The frontend replaces terminal-only demonstration with a modern regulator/examiner console.

## Confirmed Backend Position

The backend is ready for frontend integration at prototype/demo scope because:

```text
Phase 7.1 functional evidence passes.
Phase 7.2 performance evidence passes.
Phase 7.3 compliance evidence passes.
run-final-demo.sh completes successfully.
Git status is clean and synced with origin/main.
```

## Recommended Frontend Stack

```text
React + Vite + TypeScript + Tailwind CSS
```

Recommended packages:

```text
react-router-dom
lucide-react
recharts
```

## Frontend Phase Order

```text
FE0 — Backend Contract & Frontend Readiness Check
FE1 — Foundation UI Scaffold
FE2 — Regulator Workflow UI
FE3 — Evidence Dashboard & Performance Visualization
FE4 — Polish, Packaging, and Demo Stability
FE5 — Final Examiner Frontend Package
```

## Target Frontend Location

```text
aml-system/services/regulator-api/frontend/
```

## Execution Rule

Follow the files in order. Do not skip FE0, because it confirms the backend response contract before UI implementation.
