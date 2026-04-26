# PBBF BLISS — Phase 2 Stage 2 Populated Markdown Package
## Environment Separation, Secrets, and Configuration Governance

## Stage objective
Make local, test, staging, and production environments behave predictably and safely.

This stage exists to remove hidden boot assumptions from both backend and frontend so that:
- local setup is repeatable
- tests do not accidentally hit live systems
- staging behaves like a real pre-production environment
- production runs with explicit, controlled configuration
- no one depends on undocumented manual tweaks

---

## Stage outcomes

### Backend stage outcome
All environment configuration is separated cleanly and ambiguous defaults are eliminated for:
- database URLs
- secrets
- docs exposure
- CORS behavior
- host restrictions
- logging behavior

### Frontend stage outcome
The frontend is locked to explicit environment variables for:
- API base URL
- deployment environment label
- frontend app name
- feature flags where needed later

### Completion gate
No developer, tester, or deployment target should need hidden manual tweaks to make the app boot correctly in each environment.

---

## Repository root
`bliss-telehealth/`

---

# Stage 2 directory structure

```text
bliss-telehealth/
├── docs/
│   └── environment/
│       ├── environment-matrix.md
│       └── secrets-governance.md
├── pbbf-api/
│   ├── .env.example
│   ├── app/
│   │   └── common/
│   │       └── config/
│   │           └── settings.py
│   ├── docs/
│   │   └── backend-env.md
│   ├── infra/
│   │   ├── docker-compose.backend.yml
│   │   └── Dockerfile.backend
│   └── scripts/
│       └── validate_env.py
└── pbbf-telehealth/
    ├── .env.example
    ├── docs/
    │   └── frontend-deployment.md
    ├── src/
    │   └── services/
    │       └── api.js
    └── vite.config.js
```

---

# Recommended commands to create missing directories

Run from the `bliss-telehealth` root:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth

mkdir -p docs/environment
mkdir -p pbbf-api/docs
mkdir -p pbbf-api/infra
mkdir -p pbbf-api/scripts
mkdir -p pbbf-telehealth/docs
mkdir -p pbbf-telehealth/src/services
```

---

# FILE 1 — `[CREATE]` `bliss-telehealth/docs/environment/environment-matrix.md`

```md
# PBBF BLISS Environment Matrix

## Purpose
This document defines how configuration differs across local, test, staging, and production environments. It exists to stop hidden assumptions and environment drift.

## Core principle
Each environment must behave intentionally.

That means:
- no live production secret should be reused in local or test
- no test run should depend on production services
- staging should mirror production structure as closely as possible
- production must have the strictest rules for docs exposure, logging, CORS, and hosts

## Environment table

| Setting area | Local | Test | Staging | Production |
|---|---|---|---|---|
| Purpose | Developer iteration | Automated validation | Pre-release verification | Real service operation |
| Backend app env | `local` | `test` | `staging` | `production` |
| Frontend app env | `local` | `test` | `staging` | `production` |
| Database | Local DB or local container DB | Isolated test DB | Staging DB | Production DB |
| Redis | Optional local or local container | Optional isolated test Redis | Staging Redis | Production Redis |
| Docs exposure | Enabled | Enabled or optional | Internal only | Disabled |
| Debug | Allowed | Minimal | Disabled | Disabled |
| CORS | Localhost-focused | Test-focused | Explicit staging domains | Explicit production domains |
| Allowed hosts | Localhost-focused | Test-safe | Explicit staging hosts | Explicit production hosts |
| Logging | Readable local logs | Test-focused | Structured logs preferred | Structured logs required |
| Secrets | Developer-safe placeholders | Fake test secrets | Real staging secrets | Real production secrets |
| E2E target | Local frontend/backend | Mocked or isolated | Connected staging | Limited smoke only |

## Minimum environment rules

### Local
- safe defaults
- docs visible
- developer-friendly logging
- local API base URL
- no real production secrets

### Test
- isolated DB
- deterministic values
- no dependency on real production infrastructure
- suitable for CI and automated validation

### Staging
- same boot pattern as production
- real deployment structure
- explicit domains
- production-like environment variables
- safe but realistic secrets handling

### Production
- docs disabled
- strict hosts and CORS
- secure secrets source
- explicit external URLs
- structured logging
- no debug mode
- rollback-ready deployment path

## Required ownership
Any new environment variable added by backend or frontend work must be reflected in:
- `.env.example`
- the relevant environment documentation
- deployment configuration if it affects staging or production
```

---

# FILE 2 — `[CREATE]` `bliss-telehealth/docs/environment/secrets-governance.md`

```md
# PBBF BLISS Secrets Governance

## Purpose
This document defines how secrets and sensitive configuration must be handled across environments.

## Core rules
- Never commit real secrets into Git
- Never hardcode secrets inside source files
- Never store production credentials in `.env.example`
- Never reuse production secrets in local or test
- Never expose sensitive values in screenshots, logs, or docs

## What counts as a secret
Examples include:
- backend secret keys
- JWT signing keys
- database passwords
- Redis passwords where enabled
- SMTP credentials
- cloud deployment tokens
- third-party integration credentials

## Approved pattern
### Backend
- real values come from deployment environment variables or secret managers
- local values live in an untracked `.env`
- `.env.example` contains placeholders only

### Frontend
- only non-sensitive build-time variables should be exposed through `VITE_*`
- do not place backend secrets in frontend environment variables
- the frontend should only receive public configuration such as API base URL and app environment

## Review rule
Any new configuration field added by a developer must be reviewed and classified as either:
- public configuration
- server-only sensitive configuration

## Redaction rule
When sharing logs or config evidence:
- redact secrets
- redact passwords
- redact tokens
- redact anything that can grant direct access
```

---

# FILE 3 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/common/config/settings.py`

> Replace or merge into the current file. This version gives you predictable backend environment behavior across local, test, staging, and production.

```python
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import EmailStr, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PBBF_",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "PBBF BLISS Telehealth API"
    APP_VERSION: str = "0.1.0"
    APP_ENV: Literal["local", "test", "staging", "production"] = "local"
    DEBUG: bool = False

    API_V1_PREFIX: str = "/api/v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./bliss_telehealth.db"
    TEST_DATABASE_URL: str = "sqlite:///./bliss_telehealth_test.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "replace-this-in-real-envs"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080
    JWT_ALGORITHM: str = "HS256"

    ENABLE_DOCS: bool = True
    FAIL_ON_ROUTER_IMPORT_ERROR: bool = True
    BASE_EXTERNAL_URL: str | None = None

    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )
    CORS_ALLOW_METHODS: list[str] = Field(
        default_factory=lambda: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )
    CORS_ALLOW_HEADERS: list[str] = Field(
        default_factory=lambda: ["Authorization", "Content-Type", "X-Request-ID"]
    )

    ALLOWED_HOSTS: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1", "api.localhost"]
    )

    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False
    SUPPORT_EMAIL: EmailStr = "engineering@postbabybliss.org"

    SECURITY_HEADERS_ENABLED: bool = True
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "60/minute"

    @field_validator("CORS_ALLOW_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("CORS_ALLOW_METHODS", mode="before")
    @classmethod
    def parse_cors_methods(cls, value):
        if isinstance(value, str):
            return [item.strip().upper() for item in value.split(",") if item.strip()]
        return value

    @field_validator("CORS_ALLOW_HEADERS", mode="before")
    @classmethod
    def parse_cors_headers(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def docs_url(self) -> str | None:
        if not self.ENABLE_DOCS or self.APP_ENV == "production":
            return None
        return "/docs"

    @property
    def redoc_url(self) -> str | None:
        if not self.ENABLE_DOCS or self.APP_ENV == "production":
            return None
        return "/redoc"

    @property
    def openapi_url(self) -> str | None:
        if not self.ENABLE_DOCS or self.APP_ENV == "production":
            return None
        return "/openapi.json"

    @property
    def effective_database_url(self) -> str:
        return self.TEST_DATABASE_URL if self.APP_ENV == "test" else self.DATABASE_URL

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


def clear_settings_cache() -> None:
    get_settings.cache_clear()
```

---

# FILE 4 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/.env.example`

```env
PBBF_APP_NAME=PBBF BLISS Telehealth API
PBBF_APP_VERSION=0.1.0
PBBF_APP_ENV=local
PBBF_DEBUG=true

PBBF_API_V1_PREFIX=/api/v1
PBBF_HOST=0.0.0.0
PBBF_PORT=8000

PBBF_DATABASE_URL=sqlite:///./bliss_telehealth.db
PBBF_TEST_DATABASE_URL=sqlite:///./bliss_telehealth_test.db
PBBF_REDIS_URL=redis://localhost:6379/0

PBBF_SECRET_KEY=replace-this-with-a-long-random-string
PBBF_ACCESS_TOKEN_EXPIRE_MINUTES=30
PBBF_REFRESH_TOKEN_EXPIRE_MINUTES=10080
PBBF_JWT_ALGORITHM=HS256

PBBF_ENABLE_DOCS=true
PBBF_FAIL_ON_ROUTER_IMPORT_ERROR=true
PBBF_BASE_EXTERNAL_URL=http://127.0.0.1:8000

PBBF_CORS_ALLOW_CREDENTIALS=true
PBBF_CORS_ALLOW_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
PBBF_CORS_ALLOW_METHODS=GET,POST,PUT,PATCH,DELETE,OPTIONS
PBBF_CORS_ALLOW_HEADERS=Authorization,Content-Type,X-Request-ID

PBBF_ALLOWED_HOSTS=localhost,127.0.0.1,api.localhost

PBBF_LOG_LEVEL=INFO
PBBF_LOG_JSON=false
PBBF_SUPPORT_EMAIL=engineering@postbabybliss.org

PBBF_SECURITY_HEADERS_ENABLED=true
PBBF_RATE_LIMIT_ENABLED=true
PBBF_RATE_LIMIT_DEFAULT=60/minute
```

---

# FILE 5 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/docs/backend-env.md`

```md
# Backend Environment Guide

## Purpose
This document defines how the backend should be configured across local, test, staging, and production.

## Core rule
The backend must boot the same way everywhere:
- from explicit environment variables
- with no hidden machine-specific assumptions
- with no dependence on undocumented local edits

## Environment-specific expectations

### Local
- `PBBF_APP_ENV=local`
- docs enabled
- localhost CORS allowed
- local DB or local container DB
- readable logging

### Test
- `PBBF_APP_ENV=test`
- isolated test DB
- predictable values
- safe fake secrets
- suitable for automated validation

### Staging
- `PBBF_APP_ENV=staging`
- real deployment topology
- staging DB and Redis
- explicit hosts and CORS
- production-like boot behavior

### Production
- `PBBF_APP_ENV=production`
- docs disabled
- debug disabled
- explicit external URL
- explicit hosts and CORS
- structured logging
- deployment secret source required

## Key environment variables
Refer to `.env.example` for the current reference list.

The most critical fields are:
- `PBBF_APP_ENV`
- `PBBF_DATABASE_URL`
- `PBBF_TEST_DATABASE_URL`
- `PBBF_REDIS_URL`
- `PBBF_SECRET_KEY`
- `PBBF_ENABLE_DOCS`
- `PBBF_CORS_ALLOW_ORIGINS`
- `PBBF_ALLOWED_HOSTS`
- `PBBF_BASE_EXTERNAL_URL`

## Validation workflow
Before booting the backend in a new environment, run:

```bash
python scripts/validate_env.py
```

Then boot the app.

## Production rule
Production must never run with:
- default secret key
- overly broad CORS
- overly broad allowed hosts
- docs enabled
```

---

# FILE 6 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/infra/docker-compose.backend.yml`

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

# FILE 7 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/infra/Dockerfile.backend`

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update     && apt-get install -y --no-install-recommends build-essential curl libpq-dev wget     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip     && pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# FILE 8 — `[CREATE]` `bliss-telehealth/pbbf-api/scripts/validate_env.py`

```python
from __future__ import annotations

import os
import sys


def get_env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


def warn(message: str) -> None:
    print(f"[WARN] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def main() -> None:
    app_env = get_env("PBBF_APP_ENV", "local")
    secret_key = get_env("PBBF_SECRET_KEY", "")
    db_url = get_env("PBBF_DATABASE_URL", "")
    cors = get_env("PBBF_CORS_ALLOW_ORIGINS", "")
    hosts = get_env("PBBF_ALLOWED_HOSTS", "")
    docs_enabled = get_env("PBBF_ENABLE_DOCS", "true").lower() == "true"

    ok(f"Environment detected: {app_env}")

    if not db_url:
        fail("PBBF_DATABASE_URL is missing.")

    if not secret_key:
        fail("PBBF_SECRET_KEY is missing.")

    if app_env in {"staging", "production"} and "replace-this" in secret_key.lower():
        fail("Secret key still uses placeholder value in staging/production.")

    if app_env == "production":
        if docs_enabled:
            fail("Docs must be disabled in production.")

        if not cors:
            fail("PBBF_CORS_ALLOW_ORIGINS must be explicit in production.")

        if not hosts:
            fail("PBBF_ALLOWED_HOSTS must be explicit in production.")

    if app_env == "local" and not cors:
        warn("No local CORS origins set. Local frontend may fail to connect.")

    ok("Environment validation passed.")


if __name__ == "__main__":
    main()
```

---

# FILE 9 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/.env.example`

```env
VITE_APP_NAME=PBBF Telehealth
VITE_APP_ENV=local
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

---

# FILE 10 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/docs/frontend-deployment.md`

```md
# Frontend Deployment Guide

## Purpose
This document defines how the frontend should be configured and deployed across local, test, staging, and production.

## Core rule
The frontend must never rely on hidden machine-specific API URLs or undocumented environment overrides.

## Required frontend environment variables
Minimum expected variables:
- `VITE_APP_NAME`
- `VITE_APP_ENV`
- `VITE_API_BASE_URL`

## Environment expectations

### Local
- API base URL points to local backend
- frontend runs through Vite dev server
- localhost routes are expected

### Test
- test environment may use mocked APIs or dedicated backend
- no live production endpoints

### Staging
- API base URL points to staging backend
- deployment reflects real routing behavior
- route refresh handling must already work

### Production
- API base URL points to production backend
- environment variables are injected through deployment
- no debug-only assumptions remain

## Deployment checklist
Before deployment:
1. confirm `.env.example` matches actual expected variables
2. confirm `VITE_API_BASE_URL` points to the correct target
3. confirm `npm run build` succeeds
4. confirm protected routes still work after refresh
5. confirm staging and production use explicit API URLs

## SPA routing note
Any static hosting or Nginx configuration must support fallback to `index.html` for client-side routes.
```

---

# FILE 11 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/services/api.js`

> Replace or merge into the current file so the frontend is environment-driven and no route depends on hidden API defaults beyond the declared `VITE_*` variables.

```jsx
const RAW_API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";
export const API_BASE_URL = RAW_API_BASE_URL.replace(/\/$/, "");

class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

function readAuthState() {
  try {
    const raw = window.localStorage.getItem("pbbf_auth_state");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function buildHeaders({ headers = {}, token, isJson = true } = {}) {
  const finalHeaders = new Headers(headers);

  if (isJson && !finalHeaders.has("Content-Type")) {
    finalHeaders.set("Content-Type", "application/json");
  }

  if (token) {
    finalHeaders.set("Authorization", `Bearer ${token}`);
  }

  return finalHeaders;
}

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    return response.json();
  }

  return response.text();
}

export async function apiRequest(path, options = {}) {
  const authState = readAuthState();
  const token = options.token || authState?.accessToken || null;

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method || "GET",
    headers: buildHeaders({
      headers: options.headers,
      token,
      isJson: options.isJson !== false,
    }),
    body:
      options.body === undefined
        ? undefined
        : options.isJson === false
        ? options.body
        : JSON.stringify(options.body),
    credentials: options.credentials || "include",
  });

  const data = await parseResponse(response);

  if (!response.ok) {
    const message =
      (typeof data === "object" && data?.message) ||
      (typeof data === "object" && data?.detail) ||
      "Request failed.";
    throw new ApiError(message, response.status, data);
  }

  return data;
}

export const api = {
  get: (path, options = {}) => apiRequest(path, { ...options, method: "GET" }),
  post: (path, body, options = {}) => apiRequest(path, { ...options, method: "POST", body }),
  put: (path, body, options = {}) => apiRequest(path, { ...options, method: "PUT", body }),
  patch: (path, body, options = {}) => apiRequest(path, { ...options, method: "PATCH", body }),
  delete: (path, options = {}) => apiRequest(path, { ...options, method: "DELETE" }),
};

export { ApiError };
```

---

# FILE 12 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/vite.config.js`

> Replace or merge into the current file so the frontend behaves predictably for local dev, preview, and test execution.

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

# Recommended verification commands for Stage 2

Run these from the relevant directories after applying the changes.

## Backend environment validation
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

python scripts/validate_env.py
```

## Backend container boot check
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

docker compose -f infra/docker-compose.backend.yml up --build
```

## Frontend env + build check
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth

npm run build
npm run dev
```

---

# Git commit recommendation for this stage

Run from the `bliss-telehealth` root:

```bash
git add docs/environment pbbf-api/app/common/config/settings.py pbbf-api/.env.example pbbf-api/docs/backend-env.md pbbf-api/infra pbbf-api/scripts/validate_env.py pbbf-telehealth/.env.example pbbf-telehealth/docs/frontend-deployment.md pbbf-telehealth/src/services/api.js pbbf-telehealth/vite.config.js
git commit -m "config: separate environments and add configuration governance baseline"
```

---

# Completion gate for Stage 2

This stage is complete only when:
- environment docs exist
- secrets governance doc exists
- backend settings are environment-driven
- backend `.env.example` exists and is usable
- backend validation script runs cleanly
- frontend `.env.example` exists
- frontend API client uses explicit env configuration
- frontend Vite config supports predictable local/test behavior
- no hidden manual environment tweaks are required to boot local, test, or staging

---

# Final recommendation
Treat Stage 2 as the stage that removes “it works on my machine” risk from the project.

If this stage is done properly, every later hardening stage becomes easier because the team is no longer debugging invisible environment assumptions.
