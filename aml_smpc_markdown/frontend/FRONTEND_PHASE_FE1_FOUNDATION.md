# Frontend Build Timeline — Phase FE1 (Foundation UI Scaffold)

**Goal:** Establish a stable UI shell that can run locally and consume the existing backend services.

## Target location in repo
- `aml-system/services/regulator-api/frontend/`

## Outcomes
- A working frontend dev server (local) and production build.
- A clear routing structure for the regulator workflow.
- A shared API client wrapper for calling the backend services.

## Tasks (micro-level)
1. **Scaffold UI**
   - Choose framework: React + Vite (recommended for speed) or Next.js (if SSR desired).
   - Create structure:
     - `src/pages/` (or `src/routes/`)
     - `src/components/`
     - `src/api/`
     - `src/styles/`
2. **Environment config**
   - `.env` with:
     - `VITE_REGULATOR_API_BASE_URL=http://127.0.0.1:8085`
     - `VITE_ZK_PROVER_BASE_URL=http://127.0.0.1:8084` (optional)
3. **UI Layout**
   - Shell layout: top bar + side nav + content area.
   - Pages (empty placeholders):
     - `/dashboard`
     - `/proofs`
     - `/audit`
     - `/performance`
     - `/about`
4. **API Client**
   - `src/api/client.ts` implements:
     - `get(url)` / `post(url)`
     - standardized error handling
     - timeout and retry (light)

## Acceptance criteria
- `npm run dev` works.
- `npm run build` works.
- Navigating between pages works.
- Base URL configurable without code changes.

## Evidence (what to capture)
- Screenshot: UI shell running.
- Console output: successful dev build.
