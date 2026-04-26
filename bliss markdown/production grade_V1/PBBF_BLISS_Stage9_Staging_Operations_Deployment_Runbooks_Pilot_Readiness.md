# PBBF BLISS — Phase 2 Stage 9 Populated Markdown Package
## Staging Operations, Deployment Runbooks, and Pilot Readiness

## Stage objective
Make staging behave like a real operational environment and prepare for a controlled pilot.

This stage is where the product stops being merely "deployable" and becomes:
- repeatedly deployable
- operationally understandable
- recoverable without guesswork
- ready for controlled pilot validation

It is the stage that turns staging into a true rehearsal environment for pilot rollout.

---

## Stage outcomes

### Backend stage outcome
The backend gains:
- repeatable staging deployment support
- containerized service boot guidance
- reverse-proxy baseline
- backend API documentation
- backend testing strategy documentation
- smoke validation structure for post-deploy checks
- backend operational runbook

### Frontend stage outcome
The frontend gains:
- clearer staging deployment instructions
- packaging expectations for staging
- route-refresh handling guidance
- test and build command alignment
- frontend operational runbook
- updated package and Vite expectations for staging readiness

### Completion gate
Staging can be deployed and operated repeatedly without undocumented manual rescue steps.

---

## Repository root
`bliss-telehealth/`

---

# Stage 9 directory structure

```text
bliss-telehealth/
├── docs/
│   ├── deployment/
│   │   ├── staging-release-checklist.md
│   │   └── pilot-readiness-checklist.md
│   └── operations/
│       └── runbooks/
│           ├── frontend-runbook.md
│           └── backend-runbook.md
├── pbbf-api/
│   ├── docs/
│   │   ├── backend-api.md
│   │   └── backend-test-strategy.md
│   ├── infra/
│   │   ├── docker-compose.backend.yml
│   │   ├── Dockerfile.backend
│   │   └── nginx.backend.conf
│   └── tests/
│       └── smoke/
│           ├── test_backend_smoke.py
│           └── test_post_deploy_health.py
└── pbbf-telehealth/
    ├── README.md
    ├── docs/
    │   ├── frontend-deployment.md
    │   └── frontend-testing.md
    ├── vite.config.js
    ├── package.json
    └── public/
        └── .gitkeep
```

---

# Recommended commands to create missing directories

Run from the `bliss-telehealth` root:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth

mkdir -p docs/deployment
mkdir -p docs/operations/runbooks
mkdir -p pbbf-api/docs
mkdir -p pbbf-api/infra
mkdir -p pbbf-api/tests/smoke
mkdir -p pbbf-telehealth/docs
mkdir -p pbbf-telehealth/public
touch pbbf-telehealth/public/.gitkeep
```

---

# FILE 1 — `[CREATE]` `bliss-telehealth/docs/deployment/staging-release-checklist.md`

```md
# PBBF BLISS Staging Release Checklist

## Purpose
This checklist is used before every staging release so the team can validate that the environment is deployable, testable, and supportable.

## Pre-release checks
- backend environment variables are present and validated
- frontend environment variables are present and validated
- database migration plan is known
- backup posture is known
- latest test suite has been run
- smoke suite is available
- release notes or deployment notes are prepared

## Backend checks
- container build succeeds
- API boots successfully
- migrations run cleanly
- health endpoint responds
- readiness endpoint responds
- protected routes still enforce role restrictions

## Frontend checks
- production build succeeds
- route refresh behavior is understood
- API base URL is correct for staging
- protected routes still work after refresh
- patient/provider/admin routes render correctly

## Operational checks
- runbooks are available
- rollback approach is known
- smoke commands are documented
- on-call or responsible engineer is identified

## Sign-off rule
Do not mark staging release as complete until smoke checks pass after deployment.
```

---

# FILE 2 — `[CREATE]` `bliss-telehealth/docs/deployment/pilot-readiness-checklist.md`

```md
# PBBF BLISS Pilot Readiness Checklist

## Purpose
This checklist confirms whether the platform is ready for a controlled pilot rollout after staging validation.

## Product readiness
- MVP scope is frozen
- hardening stages completed to the required level
- role workflows are validated
- known critical defects are resolved or explicitly accepted

## Operational readiness
- deployment runbooks exist
- backup and restore plan exists
- incident response runbook exists
- QA and UAT evidence exists
- training guides exist for operational reviewers

## Environment readiness
- staging has been exercised successfully
- environment configuration is explicit
- no hidden machine-specific deploy steps remain
- post-deploy smoke checks are repeatable

## Pilot release decision
Pilot readiness should only be approved when:
- the team can deploy repeatedly
- the team can explain rollback steps
- the team can support the first operational users
```

---

# FILE 3 — `[CREATE]` `bliss-telehealth/docs/operations/runbooks/backend-runbook.md`

```md
# PBBF BLISS Backend Runbook

## Purpose
This runbook explains how to operate the backend in staging and pilot-prep environments.

## Standard startup
1. confirm environment variables
2. run migration validation in the correct environment
3. deploy backend container or service
4. confirm `/api/v1/health`
5. confirm `/api/v1/ready`
6. run smoke tests

## Standard checks
- app boots cleanly
- DB connection works
- migrations are current
- rate limiting and security middleware remain active
- request IDs appear in responses
- logs show startup and request lifecycle events

## If startup fails
- inspect environment values
- inspect migration state
- inspect database connectivity
- inspect container logs
- inspect reverse-proxy configuration

## Post-deploy smoke
- health endpoint
- readiness endpoint
- one protected route check
- one admin route access check
- one representative role workflow smoke check

## Rollback reminder
If deployment introduces blocking failures:
- stop rollout
- revert to previous known-good backend image or release
- restore prior environment configuration if changed
- re-run smoke validation
```

---

# FILE 4 — `[CREATE]` `bliss-telehealth/docs/operations/runbooks/frontend-runbook.md`

```md
# PBBF BLISS Frontend Runbook

## Purpose
This runbook explains how to package, deploy, and validate the frontend in staging and pilot-prep environments.

## Standard startup / deployment path
1. confirm frontend environment variables
2. run build
3. publish the build artifact
4. verify route fallback behavior
5. verify protected routes after login
6. verify API connectivity against staging backend

## Standard checks
- build succeeds
- app loads at the expected base URL
- refresh on nested routes does not 404
- patient/provider/admin pages remain reachable only for correct roles
- visible error states remain readable if backend is partially degraded

## If frontend deployment fails
- inspect environment values
- inspect build logs
- inspect hosting route fallback configuration
- inspect API base URL mismatch
- inspect stale cache or old artifact problems

## Post-deploy smoke
- login page loads
- patient dashboard path works
- provider dashboard path works
- admin dashboard path works
- refresh on nested routes works
- frontend points to the intended staging backend
```

---

# FILE 5 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/infra/docker-compose.backend.yml`

> Merge or replace with this staging-oriented baseline if your current file is weaker.  
> Keep any environment values that are already correct for your real setup.

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16-alpine
    container_name: pbbf_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: pbbf_bliss
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_backend_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d pbbf_bliss"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: pbbf_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis_backend_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: ..
      dockerfile: infra/Dockerfile.backend
    container_name: pbbf_api
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      PBBF_APP_ENV: staging
      PBBF_DEBUG: "false"
      PBBF_ENABLE_DOCS: "true"
      PBBF_DATABASE_URL: postgresql+psycopg://postgres:postgres@postgres:5432/pbbf_bliss
      PBBF_REDIS_URL: redis://redis:6379/0
      PBBF_SECRET_KEY: change-this-before-real-deployment
      PBBF_CORS_ALLOW_ORIGINS: http://localhost:5173,http://127.0.0.1:5173
      PBBF_ALLOWED_HOSTS: localhost,127.0.0.1,api.localhost
      PBBF_BASE_EXTERNAL_URL: http://localhost:8000
      PBBF_LOG_LEVEL: INFO
      PBBF_LOG_JSON: "true"
    ports:
      - "8000:8000"
    command: >
      sh -c "alembic upgrade head &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000"
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:8000/api/v1/health || exit 1"]
      interval: 20s
      timeout: 5s
      retries: 5

volumes:
  postgres_backend_data:
  redis_backend_data:
```

---

# FILE 6 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/infra/Dockerfile.backend`

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# FILE 7 — `[CREATE]` `bliss-telehealth/pbbf-api/infra/nginx.backend.conf`

```nginx
server {
    listen 80;
    server_name _;

    client_max_body_size 10m;

    location / {
        proxy_pass http://api:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID $request_id;
    }
}
```

---

# FILE 8 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/docs/backend-api.md`

```md
# Backend API Guide

## Purpose
This document is the operational reference for the backend API during staging and pilot readiness.

## Base path
Default API prefix:
```text
/api/v1
```

## Core route families
- `/auth`
- `/users`
- `/intake`
- `/appointments`
- `/screenings`
- `/telehealth`
- `/encounters`
- `/referrals`
- `/notifications`
- `/audit`
- `/admin`

## Core operational endpoints
- `/api/v1/health`
- `/api/v1/ready`

## Deployment note
API docs may be available in local or staging depending on environment settings, but production should follow the configured docs exposure policy.
```

---

# FILE 9 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/docs/backend-test-strategy.md`

```md
# Backend Test Strategy

## Purpose
This document explains how the backend should be validated before and after staging deployment.

## Test layers

### Unit / module tests
Used to validate internal business and governance logic.

### Integration tests
Used to validate route families, health/readiness, and representative workflow behavior.

### Performance / reliability checks
Used to validate repeated-request and migration behavior.

### Smoke tests
Used immediately after deployment to confirm the service is healthy and role-relevant endpoints still behave as expected.

## Post-deploy smoke expectations
At minimum, confirm:
- health endpoint returns 200
- readiness endpoint returns 200
- one protected route is still guarded
- one representative role workflow remains intact
```

---

# FILE 10 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/smoke/test_backend_smoke.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_backend_smoke_health_and_ready():
    client = TestClient(create_app())

    health = client.get("/api/v1/health")
    ready = client.get("/api/v1/ready")

    assert health.status_code == 200
    assert ready.status_code == 200
```

---

# FILE 11 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/smoke/test_post_deploy_health.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_post_deploy_health_contract():
    client = TestClient(create_app())
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
```

---

# FILE 12 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/README.md`

```md
# PBBF Telehealth Frontend

React + Vite frontend for the PBBF BLISS telehealth platform.

## Core workspace areas
- patient workspace
- provider workspace
- admin workspace

## Local development
Install dependencies:
```bash
npm install
```

Start local dev server:
```bash
npm run dev
```

## Environment setup
Copy the example file and set real values as needed:
```bash
cp .env.example .env
```

Minimum expected value:
```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Testing
Run component and integration-style tests:
```bash
npm run test
```

Run end-to-end tests:
```bash
npm run test:e2e
```

Run both:
```bash
npm run test:all
```

## Build
Create a production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Staging note
Treat staging as a real rehearsal environment. Route refresh behavior, API base URL correctness, and role-protected navigation should all be validated before pilot sign-off.
```

---

# FILE 13 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/docs/frontend-deployment.md`

> Append this section if the file already exists.

```md
## Staging operations reminder
Before pilot readiness sign-off, verify:
- frontend build artifact is the expected release artifact
- route refresh fallback works in staging
- patient/provider/admin route protections still behave correctly
- the frontend is pointing at the intended staging backend
- smoke validation is documented after deployment
```

---

# FILE 14 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/docs/frontend-testing.md`

> Append this section if the file already exists.

```md
## Staging smoke checks
After staging deployment, verify:
- login page loads
- patient dashboard loads
- provider dashboard loads
- admin dashboard loads
- nested route refresh works
- operational error states remain readable
```

---

# FILE 15 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/vite.config.js`

> Keep your current test config if already present. Ensure this staging-friendly baseline remains intact.

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
  preview: {
    host: "0.0.0.0",
    port: 4173,
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/test/setup.jsx",
    css: true,
  },
});
```

---

# FILE 16 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/package.json`

> Merge these scripts into your existing `package.json` if they are missing.

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:e2e": "playwright test",
    "test:all": "npm run test && npm run test:e2e"
  }
}
```

> Merge note:
> Keep your full dependency list. This stage only ensures the staging-support scripts are present and consistent.

---

# FILE 17 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/public/.gitkeep`

```text
# keep public directory tracked for staging assets
```

---

# Recommended verification commands for Stage 9

## Backend staging packaging and smoke checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

docker compose -f infra/docker-compose.backend.yml up --build
pytest tests/smoke -q
```

## Frontend staging build and smoke checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth

npm install
npm run build
npm run preview
npm run test:e2e
```

---

# Git commit recommendation for this stage

Run from the `bliss-telehealth` root:

```bash
git add docs/deployment docs/operations/runbooks pbbf-api/infra/docker-compose.backend.yml pbbf-api/infra/Dockerfile.backend pbbf-api/infra/nginx.backend.conf pbbf-api/docs/backend-api.md pbbf-api/docs/backend-test-strategy.md pbbf-api/tests/smoke pbbf-telehealth/README.md pbbf-telehealth/docs/frontend-deployment.md pbbf-telehealth/docs/frontend-testing.md pbbf-telehealth/vite.config.js pbbf-telehealth/package.json pbbf-telehealth/public
git commit -m "deploy: add staging runbooks and pilot readiness baseline"
```

---

# Completion gate for Stage 9

This stage is complete only when:
- deployment docs exist
- backend and frontend runbooks exist
- backend container and reverse-proxy baseline exists
- backend API and test strategy docs exist
- smoke tests exist
- frontend build and test scripts support staging use
- staging can be deployed and validated repeatedly
- no undocumented manual rescue steps are required after deployment

---

# Final recommendation
Treat Stage 9 as the stage that proves the system can be run repeatedly by a team, not just started once by a developer.

If the team still cannot answer:
- how to deploy staging repeatably
- how to smoke-check after deploy
- how to roll forward or roll back safely
- what documents to follow during operations

then Stage 9 is not complete yet.
