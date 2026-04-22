# PBBF BLISS Backend — Phase 10 Populated Files  
## Production Hardening and API Documentation

## Objective
Make the backend release-ready for staging or MVP deployment by tightening environment handling, documenting the API clearly, improving runtime safety, standardizing Docker/Nginx deployment assets, and adding smoke tests for security headers and rate limiting.

## Important implementation note
This Phase 10 package is written against the FastAPI modular-monolith structure you have already been building in earlier phases. It assumes:

- your backend entrypoint remains `app/main.py`
- your settings object is loaded from `app/common/config/settings.py`
- routers continue to live under `app/modules/*/router.py`
- earlier phases already established core exception handling, DB session wiring, and health behavior

Because I cannot directly inspect the exact current contents of your local files, treat this as a **production-grade drop-in template** aligned to the structure you showed. Where an import or field name differs in your actual codebase, keep the structure and adjust the exact symbol names.

## Phase 10 file list
This package populates the following files:

- `app/main.py`
- `app/common/config/settings.py`
- `requirements.txt`
- `docs/backend-api.md`
- `docs/backend-env.md`
- `docs/backend-test-strategy.md`
- `infra/docker-compose.backend.yml`
- `infra/Dockerfile.backend`
- `infra/nginx.backend.conf`
- `tests/test_security_headers.py`
- `tests/test_rate_limit_smoke.py`

---

## 1) `app/main.py`

```python
from __future__ import annotations

import importlib
import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.common.config.settings import get_settings

logger = logging.getLogger("pbbf.api")


ROUTER_MODULES: tuple[str, ...] = (
    "auth",
    "users",
    "intake",
    "appointments",
    "screenings",
    "telehealth",
    "encounters",
    "referrals",
    "notifications",
    "audit",
    "admin",
)


def configure_logging() -> None:
    settings = get_settings()
    root_logger = logging.getLogger()

    if root_logger.handlers:
        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format=(
            '{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s",'
            '"message":"%(message)s"}'
            if settings.LOG_JSON
            else "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(
        "Starting %s in %s mode",
        settings.APP_NAME,
        settings.APP_ENV,
    )
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


def _module_import_candidates(module_name: str) -> tuple[str, ...]:
    return (
        f"app.modules.{module_name}.router",
        f"app.modules.{module_name}.routes",
    )


def _include_module_routers(app: FastAPI, api_router: APIRouter) -> None:
    settings = get_settings()

    for module_name in ROUTER_MODULES:
        imported = False

        for candidate in _module_import_candidates(module_name):
            try:
                module = importlib.import_module(candidate)
                router = getattr(module, "router", None)
                if router is None:
                    continue

                api_router.include_router(router)
                imported = True
                logger.info("Included router from %s", candidate)
                break
            except ModuleNotFoundError as exc:
                logger.debug("Router candidate not found: %s (%s)", candidate, exc)
            except Exception as exc:  # pragma: no cover
                logger.exception("Failed to import router for %s: %s", module_name, exc)
                if settings.FAIL_ON_ROUTER_IMPORT_ERROR:
                    raise

        if not imported:
            message = f"No router could be imported for module '{module_name}'."
            if settings.FAIL_ON_ROUTER_IMPORT_ERROR:
                raise RuntimeError(message)
            logger.warning(message)


def _build_openapi(app: FastAPI) -> dict:
    settings = get_settings()

    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Post Baby Bliss Foundation Telehealth Platform API. "
            "This API supports patient onboarding, scheduling, screenings, "
            "telehealth session access, encounter documentation, referrals, "
            "notifications, audit, and admin reporting."
        ),
        routes=app.routes,
    )

    schema["info"]["contact"] = {
        "name": "PBBF Engineering",
        "email": settings.SUPPORT_EMAIL,
    }

    schema["tags"] = [
        {"name": "health", "description": "Health and readiness endpoints."},
        {"name": "auth", "description": "Authentication and session endpoints."},
        {"name": "users", "description": "User profile and administrative user endpoints."},
        {"name": "intake", "description": "Patient intake and consent workflow endpoints."},
        {"name": "appointments", "description": "Scheduling and appointment lifecycle endpoints."},
        {"name": "screenings", "description": "EPDS and screening workflow endpoints."},
        {"name": "telehealth", "description": "Virtual session access and status endpoints."},
        {"name": "encounters", "description": "Provider encounter documentation endpoints."},
        {"name": "referrals", "description": "Referral creation and tracking endpoints."},
        {"name": "notifications", "description": "Reminder and delivery logging endpoints."},
        {"name": "audit", "description": "Audit and governance endpoints."},
        {"name": "admin", "description": "Admin reporting and operational metrics endpoints."},
    ]

    schema.setdefault("components", {}).setdefault("securitySchemes", {})
    schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    if settings.BASE_EXTERNAL_URL:
        schema["servers"] = [{"url": settings.BASE_EXTERNAL_URL}]

    app.openapi_schema = schema
    return app.openapi_schema


def _register_core_routes(app: FastAPI, api_router: APIRouter) -> None:
    settings = get_settings()

    @api_router.get("/health", tags=["health"])
    async def health() -> dict:
        return {
            "status": "ok",
            "service": settings.APP_NAME,
            "environment": settings.APP_ENV,
            "version": settings.APP_VERSION,
        }

    @api_router.get("/ready", tags=["health"])
    async def readiness() -> dict:
        return {
            "status": "ready",
            "service": settings.APP_NAME,
        }

    @api_router.get("/meta/rate-limit-smoke", tags=["health"])
    @app.state.limiter.limit(settings.RATE_LIMIT_DEFAULT)
    async def rate_limit_smoke(request: Request) -> dict:
        return {
            "ok": True,
            "message": "rate limit smoke endpoint",
        }


def _apply_standard_middleware(app: FastAPI) -> None:
    settings = get_settings()

    app.add_middleware(GZipMiddleware, minimum_size=1024)

    if settings.ALLOWED_HOSTS:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS,
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
        expose_headers=["X-Request-ID", "X-RateLimit-Limit", "X-RateLimit-Remaining"],
    )

    @app.middleware("http")
    async def request_id_and_security_headers(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        if settings.SECURITY_HEADERS_ENABLED:
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
            response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
            response.headers["Cross-Origin-Resource-Policy"] = "same-site"
            response.headers["Cache-Control"] = "no-store"

            if settings.CONTENT_SECURITY_POLICY:
                response.headers["Content-Security-Policy"] = settings.CONTENT_SECURITY_POLICY

            if settings.APP_ENV == "production":
                response.headers["Strict-Transport-Security"] = (
                    "max-age=31536000; includeSubDomains"
                )

        return response


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=lifespan,
    )

    limiter = Limiter(
        key_func=get_remote_address,
        enabled=settings.RATE_LIMIT_ENABLED,
        default_limits=[settings.RATE_LIMIT_DEFAULT] if settings.RATE_LIMIT_ENABLED else [],
        headers_enabled=True,
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    _apply_standard_middleware(app)

    api_router = APIRouter(prefix=settings.API_V1_PREFIX)
    _register_core_routes(app, api_router)
    _include_module_routers(app, api_router)
    app.include_router(api_router)

    @app.get("/", include_in_schema=False)
    async def root() -> JSONResponse:
        return JSONResponse(
            status_code=200,
            content={
                "service": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "status": "online",
                "docs": settings.DOCS_URL,
            },
        )

    app.openapi = lambda: _build_openapi(app)

    return app


app = create_app()
```

---

## 2) `app/common/config/settings.py`

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
    REDIS_URL: str = "redis://redis:6379/0"

    SECRET_KEY: str = "replace-me-in-non-local-env"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    JWT_ALGORITHM: str = "HS256"

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
        default_factory=lambda: ["localhost", "127.0.0.1", "*.pbbf.local", "*"]
    )

    ENABLE_DOCS: bool = True
    FAIL_ON_ROUTER_IMPORT_ERROR: bool = True

    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False
    SUPPORT_EMAIL: EmailStr = "engineering@postbabybliss.org"

    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "60/minute"

    SECURITY_HEADERS_ENABLED: bool = True
    CONTENT_SECURITY_POLICY: str = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; "
        "connect-src 'self' http://localhost:5173 http://127.0.0.1:5173;"
    )

    BASE_EXTERNAL_URL: str | None = None

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
    def DOCS_URL(self) -> str | None:
        return "/docs" if self.ENABLE_DOCS and self.APP_ENV != "production" else None

    @property
    def REDOC_URL(self) -> str | None:
        return "/redoc" if self.ENABLE_DOCS and self.APP_ENV != "production" else None

    @property
    def OPENAPI_URL(self) -> str | None:
        return "/openapi.json" if self.ENABLE_DOCS and self.APP_ENV != "production" else None

    @property
    def IS_PRODUCTION(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def EFFECTIVE_DATABASE_URL(self) -> str:
        return self.TEST_DATABASE_URL if self.APP_ENV == "test" else self.DATABASE_URL


@lru_cache
def get_settings() -> Settings:
    return Settings()


def clear_settings_cache() -> None:
    get_settings.cache_clear()
```

---

## 3) `requirements.txt`

```txt
fastapi==0.115.0
uvicorn[standard]==0.30.6
gunicorn==23.0.0
sqlalchemy==2.0.36
alembic==1.13.2
pydantic==2.9.2
pydantic-settings==2.5.2
email-validator==2.2.0
python-dotenv==1.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
psycopg[binary]==3.2.1
redis==5.0.8
orjson==3.10.7
python-json-logger==2.0.7
slowapi==0.1.9

pytest==8.3.3
pytest-asyncio==0.24.0
pytest-cov==5.0.0
httpx==0.27.2
ruff==0.6.8
```

---

## 4) `docs/backend-api.md`

```md
# PBBF BLISS Backend API Guide

## Purpose
This document describes the backend API surface for the PBBF BLISS Telehealth Platform MVP and the operational rules that surround it. It should be read together with the OpenAPI schema exposed by FastAPI in non-production environments.

## API base
By default, all application endpoints are versioned under:

`/api/v1`

Examples:
- `/api/v1/health`
- `/api/v1/auth/register`
- `/api/v1/auth/login`
- `/api/v1/intake`
- `/api/v1/appointments`
- `/api/v1/screenings`
- `/api/v1/telehealth`
- `/api/v1/encounters`
- `/api/v1/referrals`
- `/api/v1/notifications`
- `/api/v1/audit`
- `/api/v1/admin`

## Environments
Documentation endpoints are intentionally available only in non-production environments:

- `/docs`
- `/redoc`
- `/openapi.json`

Production should disable public docs exposure through environment settings.

## Authentication model
The API uses bearer-token authentication.

### Header format
```http
Authorization: Bearer <access_token>
```

### Identity expectations
The MVP backend supports role-based access for:
- patient
- provider
- care_coordinator
- counselor
- admin

Some endpoints will additionally enforce ownership or assignment rules. For example:
- patients should only view their own intake, screening history, appointments, referrals, and telehealth sessions
- providers should only access clinical records connected to their assigned appointments or authorized caseload
- admins may access broader system reporting and user management functions

## Endpoint groups

### Health
These routes are used for smoke checks, deployment validation, and container health probes.

- `GET /api/v1/health`
- `GET /api/v1/ready`
- `GET /api/v1/meta/rate-limit-smoke`

### Auth
These routes support registration, login, token refresh, logout, and current-user retrieval.

Typical routes:
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

### Users
These routes support user profile retrieval and admin-managed user operations.

Typical routes:
- `GET /api/v1/users/me`
- `GET /api/v1/users`
- `GET /api/v1/users/{user_id}`
- `PATCH /api/v1/users/{user_id}`

### Intake
These routes support patient onboarding, draft save, consent capture, and submission.

Typical routes:
- `POST /api/v1/intake/draft`
- `POST /api/v1/intake/submit`
- `GET /api/v1/intake/me`
- `GET /api/v1/intake/{intake_id}`

### Appointments
These routes support appointment creation, listing, rescheduling, cancellation, and provider assignment.

Typical routes:
- `POST /api/v1/appointments`
- `GET /api/v1/appointments`
- `PATCH /api/v1/appointments/{appointment_id}/reschedule`
- `PATCH /api/v1/appointments/{appointment_id}/cancel`
- `PATCH /api/v1/appointments/{appointment_id}/assign-provider`

### Screenings
These routes support EPDS capture, scoring, severity banding, critical flagging, and provider review access.

Typical routes:
- `POST /api/v1/screenings/epds`
- `GET /api/v1/screenings/me`
- `GET /api/v1/screenings/patient/{patient_id}`

### Telehealth
These routes support virtual-session metadata, join access control, and session lifecycle updates.

Typical routes:
- `POST /api/v1/telehealth/sessions`
- `POST /api/v1/telehealth/sessions/{session_id}/join`
- `PATCH /api/v1/telehealth/sessions/{session_id}/status`

### Encounters
These routes support documentation drafting, saving, and finalization.

Typical routes:
- `POST /api/v1/encounters`
- `PATCH /api/v1/encounters/{encounter_id}/save`
- `PATCH /api/v1/encounters/{encounter_id}/finalize`

### Referrals
These routes support referral creation, follow-up status changes, and timeline visibility.

Typical routes:
- `POST /api/v1/referrals`
- `PATCH /api/v1/referrals/{referral_id}/status`
- `GET /api/v1/referrals`

### Notifications
These routes support reminder scheduling and delivery visibility.

Typical routes:
- `POST /api/v1/notifications/reminders`
- `GET /api/v1/notifications`
- `PATCH /api/v1/notifications/{notification_id}/delivery-status`

### Audit
These routes support accountability, security review, and operational tracing.

Typical routes:
- `GET /api/v1/audit`
- `GET /api/v1/audit/{event_id}`

### Admin
These routes support dashboard metrics and reporting summaries.

Typical routes:
- `GET /api/v1/admin/dashboard-summary`
- `GET /api/v1/admin/metrics`
- `GET /api/v1/admin/provider-utilization`

## Response conventions
The backend should return consistent JSON envelopes wherever possible. For example:

```json
{
  "success": true,
  "message": "Appointment created successfully.",
  "data": {
    "id": "..."
  }
}
```

Validation failures, permission failures, and operational errors should remain structured and predictable.

## Error behavior
Recommended HTTP classes:
- `400` for bad input
- `401` for unauthenticated requests
- `403` for authenticated but forbidden access
- `404` for missing resources
- `409` for conflicts such as double booking
- `422` for schema validation failures
- `429` for rate limit violations
- `500` for internal server errors

## Documentation workflow
Keep the OpenAPI schema generated from the live FastAPI app. Do not maintain separate manual API specs that can drift from the code. Manual documentation should explain business intent, usage patterns, and role constraints, while OpenAPI remains the canonical technical route map.
```

---

## 5) `docs/backend-env.md`

```md
# PBBF BLISS Backend Environment Guide

## Purpose
This document defines the environment configuration strategy for the backend and explains how values should differ across local development, testing, staging, and production.

## Environment separation rule
Never run the backend with production secrets or production database credentials in a local or test environment. Each environment must have its own configuration file or secret source.

Recommended environment files:
- `.env.local`
- `.env.test`
- `.env.staging`
- `.env.production`

## Core variables

### Application identity
```env
PBBF_APP_NAME=PBBF BLISS Telehealth API
PBBF_APP_VERSION=0.1.0
PBBF_APP_ENV=local
PBBF_DEBUG=true
PBBF_API_V1_PREFIX=/api/v1
PBBF_HOST=0.0.0.0
PBBF_PORT=8000
```

### Database and cache
```env
PBBF_DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/pbbf_bliss
PBBF_TEST_DATABASE_URL=sqlite:///./bliss_telehealth_test.db
PBBF_REDIS_URL=redis://redis:6379/0
```

### Auth and token configuration
```env
PBBF_SECRET_KEY=replace-with-a-long-random-secret
PBBF_ACCESS_TOKEN_EXPIRE_MINUTES=30
PBBF_REFRESH_TOKEN_EXPIRE_MINUTES=10080
PBBF_JWT_ALGORITHM=HS256
```

### CORS and host restrictions
```env
PBBF_CORS_ALLOW_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
PBBF_CORS_ALLOW_METHODS=GET,POST,PUT,PATCH,DELETE,OPTIONS
PBBF_CORS_ALLOW_HEADERS=Authorization,Content-Type,X-Request-ID
PBBF_ALLOWED_HOSTS=localhost,127.0.0.1,api.localhost
```

### Documentation exposure
```env
PBBF_ENABLE_DOCS=true
PBBF_FAIL_ON_ROUTER_IMPORT_ERROR=true
PBBF_BASE_EXTERNAL_URL=http://localhost:8000
```

### Logging and safety controls
```env
PBBF_LOG_LEVEL=INFO
PBBF_LOG_JSON=false
PBBF_SUPPORT_EMAIL=engineering@postbabybliss.org
PBBF_RATE_LIMIT_ENABLED=true
PBBF_RATE_LIMIT_DEFAULT=60/minute
PBBF_SECURITY_HEADERS_ENABLED=true
```

## Recommended values by environment

### Local development
Use convenient values that support fast iteration:
- docs enabled
- debug enabled
- broad localhost CORS allowed
- local or container DB
- JSON logging optional

### Test
Use deterministic values:
- `PBBF_APP_ENV=test`
- docs optional
- test database isolated from local DB
- rate limits can be tightened for smoke tests
- secrets must be fake but defined

### Staging
Mirror production structure as much as possible:
- staging database
- staging Redis
- docs usually enabled only for internal access
- JSON logging preferred
- strict CORS and allowed hosts

### Production
Use locked-down values:
- `PBBF_APP_ENV=production`
- docs disabled
- debug disabled
- strict CORS
- strict allowed hosts
- secure secret source such as platform secret manager
- structured logging enabled
- public base URL explicitly set

## Secret handling rules
Do not commit real secrets into Git.
Do not store secrets inside Dockerfiles.
Do not hardcode tokens, SMTP credentials, or database passwords inside source files.
Use deployment secret management for staging and production.

## Minimum production sanity checklist
Before deployment, verify:
- production docs are disabled
- production CORS list is explicit
- allowed hosts are explicit
- secret key is not default
- DB URL points to the correct database
- Redis URL is correct
- logging level is sane
- base external URL is accurate
- health endpoint responds successfully

## Local backend boot example
```bash
export PBBF_APP_ENV=local
export PBBF_ENABLE_DOCS=true
export PBBF_DATABASE_URL=sqlite:///./bliss_telehealth.db
uvicorn app.main:app --reload
```

## Test run example
```bash
export PBBF_APP_ENV=test
export PBBF_TEST_DATABASE_URL=sqlite:///./bliss_telehealth_test.db
pytest -q
```
```

---

## 6) `docs/backend-test-strategy.md`

```md
# PBBF BLISS Backend Test Strategy

## Objective
This strategy explains how the backend should be validated before merge, before staging deployment, and before MVP release.

## Testing layers

### 1. Unit tests
These validate isolated utility logic and domain rules such as:
- EPDS scoring
- date serialization helpers
- pagination helpers
- token utilities
- validation helpers
- metrics aggregation helpers

Unit tests should be fast and should not require a live container stack.

### 2. Module tests
These validate each feature module through API or service-level behavior:
- auth
- users
- intake
- appointments
- screenings
- telehealth
- encounters
- referrals
- notifications
- audit
- admin

These tests verify the business behavior of a module in a focused way.

### 3. Integration tests
These validate cross-module journeys such as:
- patient onboarding to first appointment
- provider review and documentation flow
- admin reporting visibility after operational events
- referral generation after an encounter
- notification creation after appointment actions

These tests are slower and should run in CI and before staging deployment.

### 4. Deployment smoke tests
These verify that the release artifact is safe to boot:
- application starts successfully
- health endpoint responds
- docs exposure behaves correctly for the environment
- security headers exist
- rate limit enforcement responds with `429`
- database connectivity works
- migrations run cleanly

## Core test directories
Recommended structure:

```text
tests/
├── integration/
├── modules/
├── test_app_boot.py
├── test_health.py
├── test_rate_limit_smoke.py
└── test_security_headers.py
```

## Minimum pre-merge checks
Run these on every meaningful backend change:

```bash
pytest -q
ruff check .
```

## Strong pre-release checks
Before staging or production promotion, run:

```bash
pytest tests/test_app_boot.py -q
pytest tests/test_health.py -q
pytest tests/test_security_headers.py -q
pytest tests/test_rate_limit_smoke.py -q
pytest tests/integration -q
```

## Database-related validation
Whenever models or migrations change, also run:

```bash
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

This confirms both forward and backward migration reliability.

## Environment-focused test expectations

### Local
Local testing should optimize for developer speed while still preserving realistic route behavior.

### CI
CI should use deterministic test database setup and fail on lint or critical smoke regressions.

### Staging
Staging validation should include:
- live health endpoint
- representative seed data
- authentication flow
- one patient journey
- one provider journey
- one admin metrics check

## Security-focused test expectations
At minimum, validate:
- unauthorized access is rejected
- forbidden access is rejected for wrong roles
- sensitive endpoints require authentication
- security headers are present
- rate limiting returns `429` at the expected threshold

## Documentation and tests
The backend docs and test strategy should evolve together. Whenever you add a new critical endpoint or role-restricted workflow, add both:
- API documentation update
- test coverage update
```

---

## 7) `infra/docker-compose.backend.yml`

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
      PBBF_SECRET_KEY: change-me-before-real-deployment
      PBBF_CORS_ALLOW_ORIGINS: http://localhost:5173,http://127.0.0.1:5173
      PBBF_ALLOWED_HOSTS: localhost,127.0.0.1,api.localhost
      PBBF_BASE_EXTERNAL_URL: http://localhost:8000
      PBBF_RATE_LIMIT_ENABLED: "true"
      PBBF_RATE_LIMIT_DEFAULT: 60/minute
      PBBF_LOG_LEVEL: INFO
      PBBF_LOG_JSON: "true"
    ports:
      - "8000:8000"
    command: >
      sh -c "alembic upgrade head &&
             gunicorn app.main:app
             --worker-class uvicorn.workers.UvicornWorker
             --workers 2
             --bind 0.0.0.0:8000
             --access-logfile -
             --error-logfile -"
    healthcheck:
      test: ["CMD-SHELL", "curl -fsS http://localhost:8000/api/v1/health || exit 1"]
      interval: 20s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:1.27-alpine
    container_name: pbbf_backend_nginx
    restart: unless-stopped
    depends_on:
      api:
        condition: service_healthy
    ports:
      - "8080:80"
    volumes:
      - ./nginx.backend.conf:/etc/nginx/conf.d/default.conf:ro

volumes:
  postgres_backend_data:
  redis_backend_data:
```

---

## 8) `infra/Dockerfile.backend`

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pbbf-api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY pbbf-api /app

RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--workers", "2", "--bind", "0.0.0.0:8000"]
```

---

## 9) `infra/nginx.backend.conf`

```nginx
server {
    listen 80;
    server_name _;

    client_max_body_size 20M;

    location / {
        proxy_pass http://api:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Request-ID $request_id;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 120s;
        proxy_connect_timeout 30s;
        proxy_send_timeout 120s;
    }

    location /api/v1/health {
        proxy_pass http://api:8000/api/v1/health;
        access_log off;
    }

    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```

---

## 10) `tests/test_security_headers.py`

```python
from fastapi.testclient import TestClient

from app.common.config.settings import clear_settings_cache
from app.main import create_app


def test_security_headers_exist(monkeypatch):
    monkeypatch.setenv("PBBF_APP_ENV", "test")
    monkeypatch.setenv("PBBF_ENABLE_DOCS", "true")
    monkeypatch.setenv("PBBF_SECURITY_HEADERS_ENABLED", "true")
    monkeypatch.setenv("PBBF_FAIL_ON_ROUTER_IMPORT_ERROR", "false")

    clear_settings_cache()
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "Permissions-Policy" in response.headers
    assert "X-Request-ID" in response.headers
```

---

## 11) `tests/test_rate_limit_smoke.py`

```python
from fastapi.testclient import TestClient

from app.common.config.settings import clear_settings_cache
from app.main import create_app


def test_rate_limit_smoke(monkeypatch):
    monkeypatch.setenv("PBBF_APP_ENV", "test")
    monkeypatch.setenv("PBBF_ENABLE_DOCS", "false")
    monkeypatch.setenv("PBBF_RATE_LIMIT_ENABLED", "true")
    monkeypatch.setenv("PBBF_RATE_LIMIT_DEFAULT", "2/minute")
    monkeypatch.setenv("PBBF_FAIL_ON_ROUTER_IMPORT_ERROR", "false")

    clear_settings_cache()
    app = create_app()
    client = TestClient(app)

    response_1 = client.get("/api/v1/meta/rate-limit-smoke")
    response_2 = client.get("/api/v1/meta/rate-limit-smoke")
    response_3 = client.get("/api/v1/meta/rate-limit-smoke")

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 429
```

---

## Commands to run after adding these files

### 1. Install or refresh dependencies
```bash
pip install -r requirements.txt
```

### 2. Run basic backend smoke tests
```bash
pytest tests/test_security_headers.py tests/test_rate_limit_smoke.py -q
```

### 3. Run full backend test suite
```bash
pytest -q
```

### 4. Boot locally
```bash
uvicorn app.main:app --reload
```

### 5. Boot with Docker compose
From the `bliss-telehealth` root:
```bash
docker compose -f infra/docker-compose.backend.yml up --build
```

---

## No migration note for this phase
This phase does **not** introduce model changes by itself, so no Alembic migration is required **unless** you choose to adjust database-related settings, seed logic, or any model-backed implementation detail while merging these changes.

If you do make model changes while integrating this phase, run:

```bash
alembic revision --autogenerate -m "phase 10 hardening alignment"
alembic upgrade head
```

---

## Completion checklist

This phase should be considered complete when all of the following are true:

- backend starts cleanly in local and containerized environments
- `GET /api/v1/health` responds successfully
- docs exposure is disabled in production configuration
- CORS origins are explicit and environment-specific
- allowed hosts are explicit
- security headers are present
- rate limit smoke test returns `429` at the expected threshold
- Nginx proxies correctly to the FastAPI app
- backend API and environment docs are present and understandable
- test strategy is documented and usable by the team
- no environment-specific startup surprises remain before staging deployment
