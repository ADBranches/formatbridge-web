# PBBF BLISS — Phase 2 Stage 4 Populated Markdown Package
## Observability, Audit Enrichment, and Incident Readiness

## Stage objective
Make the system understandable when something goes wrong.

This stage turns failures from:
- silent
- confusing
- hard to trace
- hard to explain

into failures that are:
- observable
- traceable
- reviewable
- supportable

It is the stage that makes incident response possible instead of guesswork.

---

## Stage outcomes

### Backend stage outcome
The backend strengthens:
- structured logging
- request tracing
- request correlation IDs
- audit completeness
- health checks
- readiness signals
- observable failure paths
- notification task traceability

### Frontend stage outcome
The frontend improves:
- clear operational error display
- retry-friendly failure handling
- safer user-facing feedback
- non-leaky error surfaces
- clearer form-level failure summaries
- toast-driven operational feedback

### Completion gate
You can observe system health, trace major failures, and explain what happened during an incident or failed workflow.

---

## Repository root
`bliss-telehealth/`

---

# Stage 4 directory structure

```text
bliss-telehealth/
├── docs/
│   └── operations/
│       ├── incident-response-runbook.md
│       └── logging-and-monitoring-plan.md
├── pbbf-api/
│   ├── app/
│   │   ├── common/
│   │   │   └── middleware/
│   │   │       ├── logging.py
│   │   │       └── request_context.py
│   │   ├── modules/
│   │   │   ├── audit/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── notifications/
│   │   │       └── tasks.py
│   │   └── main.py
│   └── tests/
│       ├── test_health.py
│       ├── test_app_boot.py
│       └── modules/
│           └── audit/
│               ├── test_audit_logging.py
│               └── test_audit_filtering.py
└── pbbf-telehealth/
    └── src/
        ├── shared/
        │   ├── components/
        │   │   ├── ErrorState.jsx
        │   │   └── FormErrorSummary.jsx
        │   └── hooks/
        │       └── useToast.js
        └── modules/
            ├── auth/__tests__/
            ├── intake/__tests__/
            ├── appointments/__tests__/
            ├── screenings/__tests__/
            ├── telehealth/__tests__/
            ├── encounters/__tests__/
            ├── referrals/__tests__/
            └── admin/__tests__/
```

---

# Recommended commands to create missing directories

Run from the `bliss-telehealth` root:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth

mkdir -p docs/operations
mkdir -p pbbf-api/app/common/middleware
mkdir -p pbbf-api/tests/modules/audit
mkdir -p pbbf-telehealth/src/shared/components
mkdir -p pbbf-telehealth/src/shared/hooks
```

---

# FILE 1 — `[CREATE]` `bliss-telehealth/docs/operations/incident-response-runbook.md`

```md
# PBBF BLISS Incident Response Runbook

## Purpose
This runbook explains how the team should respond when the platform experiences:
- outage
- degraded performance
- auth failures
- data-access errors
- telehealth access failures
- unexpected screening or referral workflow failures

## Incident severity guide

### Sev 1
Critical service disruption affecting core platform availability or access to critical workflows.

Examples:
- login broadly failing
- backend cannot boot
- database unavailable
- telehealth join route broadly failing during live use

### Sev 2
Major workflow degradation without complete outage.

Examples:
- referrals failing to persist
- audit logs not being written
- appointment rescheduling failing
- provider notes finalization failing

### Sev 3
Localized issue with workaround available.

Examples:
- one admin report page failing
- one screen showing degraded UI but core flow still recoverable

## First-response checklist
1. Confirm whether the issue is frontend-only, backend-only, or cross-system
2. Check backend `/api/v1/health`
3. Check request correlation IDs in logs
4. Check most recent deploy or config change
5. Identify affected role(s): patient, provider, admin
6. Confirm whether data loss risk exists
7. Determine severity
8. Begin incident log entry

## Required incident evidence
- start time
- detection source
- affected services
- affected roles
- request IDs if available
- latest deploy/version context
- mitigation actions taken
- recovery time
- follow-up remediation items

## Communication rule
User-facing messages must remain safe and concise.
Do not expose stack traces, secret values, SQL details, or internal exception paths to end users.

## Recovery closeout checklist
- issue resolved
- health checks passing
- affected workflows re-tested
- logs and audit evidence reviewed
- root cause recorded
- preventive action assigned
```

---

# FILE 2 — `[CREATE]` `bliss-telehealth/docs/operations/logging-and-monitoring-plan.md`

```md
# PBBF BLISS Logging and Monitoring Plan

## Purpose
This document defines the minimum observability baseline for pilot-ready operations.

## Goals
The system should allow the team to answer:
- What failed?
- When did it fail?
- Which role and workflow were affected?
- Which request caused the issue?
- Was data written or rolled back?
- Is the service healthy now?

## Required logging principles
- log in structured format where possible
- include request correlation ID
- include environment and service context
- log workflow boundaries for critical operations
- log failures with enough context to debug safely
- never log secrets, tokens, or raw passwords

## Minimum backend observability events
- app startup
- router registration success/failure
- request start
- request end
- request duration
- request correlation ID
- auth failure
- permission denial
- audit write
- notification task trigger
- unhandled exception

## Minimum health/readiness signals
- API health endpoint available
- app boot validation test exists
- health endpoint test exists
- readiness signal distinguishes “service alive” from “service ready”

## Frontend monitoring expectations
- user-facing error states are readable
- retry is possible where appropriate
- error messages do not leak unsafe backend detail
- toasts are used for operational feedback, not silent failure

## Review cadence
This plan should be reviewed again before:
- staging sign-off
- pilot release
- production rollout
```

---

# FILE 3 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/app/common/middleware/request_context.py`

> Use this to generate and attach a request correlation ID to every request and response.

```python
from __future__ import annotations

import uuid
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="unknown")


def get_request_id() -> str:
    return request_id_ctx_var.get()


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        incoming_request_id = request.headers.get("X-Request-ID")
        request_id = incoming_request_id or str(uuid.uuid4())

        token = request_id_ctx_var.set(request_id)
        request.state.request_id = request_id

        try:
          response = await call_next(request)
        finally:
          request_id_ctx_var.reset(token)

        response.headers["X-Request-ID"] = request_id
        return response
```

---

# FILE 4 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/app/common/middleware/logging.py`

> Use this middleware for request lifecycle logging and response timing.

```python
from __future__ import annotations

import json
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.common.config.settings import get_settings
from app.common.middleware.request_context import get_request_id

settings = get_settings()
logger = logging.getLogger("pbbf.api")


def configure_logging() -> None:
    if logger.handlers:
        return

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(settings.LOG_LEVEL.upper())
    logger.propagate = False


def _serialize_log(payload: dict) -> str:
    if settings.LOG_JSON:
        return json.dumps(payload, default=str)
    return " | ".join(f"{key}={value}" for key, value in payload.items())


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        logger.info(
            _serialize_log(
                {
                    "event": "request.start",
                    "request_id": request.headers.get("X-Request-ID") or getattr(request.state, "request_id", "unknown"),
                    "method": request.method,
                    "path": request.url.path,
                }
            )
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.exception(
                _serialize_log(
                    {
                        "event": "request.error",
                        "request_id": get_request_id(),
                        "method": request.method,
                        "path": request.url.path,
                        "duration_ms": duration_ms,
                        "error_type": type(exc).__name__,
                    }
                )
            )
            raise

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.info(
            _serialize_log(
                {
                    "event": "request.end",
                    "request_id": get_request_id(),
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                }
            )
        )
        return response
```

---

# FILE 5 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/main.py`

> Merge these additions into your current hardened `main.py` from Stage 3.  
> The key additions here are:
> - `configure_logging()`
> - `RequestContextMiddleware`
> - `RequestLoggingMiddleware`
> - readiness route
> - startup/shutdown log events

```python
from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.common.config.settings import get_settings
from app.common.middleware.logging import RequestLoggingMiddleware, configure_logging
from app.common.middleware.request_context import RequestContextMiddleware
from app.common.utils.security import get_client_ip_from_headers, parse_rate_limit

# keep your existing imports for SecurityHeadersMiddleware / BasicRateLimitMiddleware
# and router imports below this line
from app.modules.admin.router import router as admin_router
from app.modules.appointments.router import router as appointments_router
from app.modules.audit.router import router as audit_router
from app.modules.auth.router import router as auth_router
from app.modules.encounters.router import router as encounters_router
from app.modules.intake.router import router as intake_router
from app.modules.notifications.router import router as notifications_router
from app.modules.referrals.router import router as referrals_router
from app.modules.screenings.router import router as screenings_router
from app.modules.telehealth.router import router as telehealth_router
from app.modules.users.router import router as users_router

settings = get_settings()
configure_logging()
logger = logging.getLogger("pbbf.api")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    # Keep your Stage 3 middleware here as well:
    # - SecurityHeadersMiddleware
    # - BasicRateLimitMiddleware
    # - CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    @app.on_event("startup")
    async def startup_event():
        logger.info(
            f"event=app.startup app={settings.APP_NAME} env={settings.APP_ENV} docs_enabled={bool(settings.docs_url)}"
        )

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info(f"event=app.shutdown app={settings.APP_NAME} env={settings.APP_ENV}")

    @app.get(f"{settings.API_V1_PREFIX}/health", tags=["health"])
    def health_check():
        return {
            "status": "ok",
            "service": settings.APP_NAME,
            "env": settings.APP_ENV,
            "ready": True,
        }

    @app.get(f"{settings.API_V1_PREFIX}/ready", tags=["health"])
    def readiness_check():
        return {
            "status": "ready",
            "service": settings.APP_NAME,
            "env": settings.APP_ENV,
        }

    app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(users_router, prefix=settings.API_V1_PREFIX)
    app.include_router(intake_router, prefix=settings.API_V1_PREFIX)
    app.include_router(appointments_router, prefix=settings.API_V1_PREFIX)
    app.include_router(screenings_router, prefix=settings.API_V1_PREFIX)
    app.include_router(telehealth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(encounters_router, prefix=settings.API_V1_PREFIX)
    app.include_router(referrals_router, prefix=settings.API_V1_PREFIX)
    app.include_router(notifications_router, prefix=settings.API_V1_PREFIX)
    app.include_router(audit_router, prefix=settings.API_V1_PREFIX)
    app.include_router(admin_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
```

> Important merge note:
> Keep your existing Stage 3 `SecurityHeadersMiddleware` and `BasicRateLimitMiddleware` in `main.py`.  
> This Stage 4 patch adds observability; it does not replace the Stage 3 hardening.

---

# FILE 6 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/app/modules/audit/schemas.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditLogRead(BaseModel):
    id: str | int
    actor_name: str
    action: str
    target_type: str
    target_id: str | None = None
    request_id: str | None = None
    metadata: dict[str, Any] = {}
    created_at: datetime


class AuditLogCreate(BaseModel):
    actor_name: str
    action: str
    target_type: str
    target_id: str | None = None
    request_id: str | None = None
    metadata: dict[str, Any] = {}
```

---

# FILE 7 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/app/modules/audit/service.py`

> This service adds a reusable write helper and simple read/list helpers for observability-friendly audit access.

```python
from __future__ import annotations

import logging
from typing import Any

from app.common.middleware.request_context import get_request_id
from app.modules.audit.schemas import AuditLogCreate

logger = logging.getLogger("pbbf.audit")


class AuditService:
    def __init__(self, repository):
        self.repository = repository

    def create_event(
        self,
        *,
        actor_name: str,
        action: str,
        target_type: str,
        target_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        payload = AuditLogCreate(
            actor_name=actor_name,
            action=action,
            target_type=target_type,
            target_id=target_id,
            request_id=get_request_id(),
            metadata=metadata or {},
        )
        event = self.repository.create(payload)

        logger.info(
            f"event=audit.write request_id={payload.request_id} action={payload.action} "
            f"target_type={payload.target_type} actor={payload.actor_name}"
        )
        return event

    def list_events(self):
        return self.repository.list_all()
```

---

# FILE 8 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/app/modules/audit/router.py`

```python
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.common.permissions.dependencies import require_admin
from app.modules.audit.repository import AuditRepository
from app.modules.audit.service import AuditService

router = APIRouter(prefix="/audit", tags=["audit"])


def get_audit_service() -> AuditService:
    repository = AuditRepository()
    return AuditService(repository)


@router.get("")
def list_audit_events(_admin=Depends(require_admin), service: AuditService = Depends(get_audit_service)):
    events = service.list_events()
    return {"events": events}
```

---

# FILE 9 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/app/modules/audit/repository.py`

> This is a minimal repository shape that you should adapt to your actual DB model implementation.

```python
from __future__ import annotations

from datetime import datetime, timezone

from app.modules.audit.schemas import AuditLogCreate


class AuditRepository:
    def __init__(self):
        self._items = []

    def create(self, payload: AuditLogCreate):
        item = {
            "id": len(self._items) + 1,
            "actor_name": payload.actor_name,
            "action": payload.action,
            "target_type": payload.target_type,
            "target_id": payload.target_id,
            "request_id": payload.request_id,
            "metadata": payload.metadata,
            "created_at": datetime.now(timezone.utc),
        }
        self._items.append(item)
        return item

    def list_all(self):
        return list(reversed(self._items))
```

> Adaptation note:
> If your project already has a persistent audit model and DB session pattern, keep this repository interface but wire it to SQLAlchemy instead of in-memory storage.

---

# FILE 10 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-api/app/modules/notifications/tasks.py`

```python
from __future__ import annotations

import logging

from app.common.middleware.request_context import get_request_id

logger = logging.getLogger("pbbf.notifications")


def create_notification_task(*, task_name: str, target_user_id: str, metadata: dict | None = None) -> dict:
    payload = {
        "task_name": task_name,
        "target_user_id": target_user_id,
        "metadata": metadata or {},
        "request_id": get_request_id(),
    }

    logger.info(
        f"event=notification.task request_id={payload['request_id']} "
        f"task={payload['task_name']} target_user_id={payload['target_user_id']}"
    )
    return payload
```

---

# FILE 11 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/test_health.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_returns_ok():
    client = TestClient(create_app())
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["ready"] is True


def test_readiness_endpoint_returns_ready():
    client = TestClient(create_app())
    response = client.get("/api/v1/ready")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
```

---

# FILE 12 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/test_app_boot.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_application_boots_successfully():
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/v1/health")
    assert response.status_code == 200
```

---

# FILE 13 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/audit/test_audit_logging.py`

```python
from app.modules.audit.repository import AuditRepository
from app.modules.audit.service import AuditService


def test_audit_service_writes_event():
    repository = AuditRepository()
    service = AuditService(repository)

    event = service.create_event(
        actor_name="Admin User",
        action="user.updated",
        target_type="user",
        target_id="user-1",
        metadata={"field": "role"},
    )

    assert event["actor_name"] == "Admin User"
    assert event["action"] == "user.updated"
    assert event["target_type"] == "user"
```

---

# FILE 14 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/audit/test_audit_filtering.py`

```python
from app.modules.audit.repository import AuditRepository
from app.modules.audit.service import AuditService


def test_audit_list_returns_reverse_order():
    repository = AuditRepository()
    service = AuditService(repository)

    service.create_event(actor_name="Admin", action="first", target_type="user")
    service.create_event(actor_name="Admin", action="second", target_type="user")

    events = service.list_events()
    assert events[0]["action"] == "second"
    assert events[1]["action"] == "first"
```

---

# FILE 15 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/shared/components/ErrorState.jsx`

> Replace or merge into the current file so the product shows clearer, retry-friendly operational failures without leaking unsafe details.

```jsx
export default function ErrorState({
  title = "Something went wrong",
  message = "An unexpected issue occurred while loading this part of the application.",
  retryLabel = "",
  onRetry = null,
}) {
  return (
    <section className="rounded-3xl border border-rose-200 bg-rose-50 p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-rose-900">{title}</h2>
      <p className="mt-3 text-sm leading-6 text-rose-800">{message}</p>

      {retryLabel && onRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className="mt-5 rounded-xl bg-white px-4 py-3 text-sm font-semibold text-rose-800 transition hover:bg-rose-100"
        >
          {retryLabel}
        </button>
      ) : null}
    </section>
  );
}
```

---

# FILE 16 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/shared/hooks/useToast.js`

> Replace or merge into the current file so operational feedback is structured and dismissible.

```jsx
import { useCallback, useEffect, useState } from "react";

let listeners = new Set();
let toastQueue = [];

function emit() {
  listeners.forEach((listener) => listener([...toastQueue]));
}

function dismissToast(id) {
  toastQueue = toastQueue.filter((toast) => toast.id !== id);
  emit();
}

function pushToast(toast) {
  const entry = {
    id: toast?.id || `toast-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
    type: toast?.type || "info",
    title: toast?.title || "",
    message: toast?.message || "",
    duration: toast?.duration ?? 3500,
  };

  toastQueue = [...toastQueue, entry];
  emit();

  if (entry.duration > 0) {
    window.setTimeout(() => dismissToast(entry.id), entry.duration);
  }

  return entry.id;
}

export function useToast() {
  const [toasts, setToasts] = useState(toastQueue);

  useEffect(() => {
    const listener = (items) => setToasts(items);
    listeners.add(listener);
    return () => listeners.delete(listener);
  }, []);

  const success = useCallback((message, title = "Success") => {
    return pushToast({ type: "success", title, message });
  }, []);

  const error = useCallback((message, title = "Error") => {
    return pushToast({ type: "error", title, message, duration: 5000 });
  }, []);

  const info = useCallback((message, title = "Info") => {
    return pushToast({ type: "info", title, message });
  }, []);

  return {
    toasts,
    success,
    error,
    info,
    dismiss: dismissToast,
  };
}
```

---

# FILE 17 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/shared/components/FormErrorSummary.jsx`

> Replace or merge into the current file so failed forms can explain operational issues cleanly.

```jsx
export default function FormErrorSummary({
  errors = {},
  title = "Please correct the following issues before continuing.",
}) {
  const items = Object.values(errors).filter(Boolean);

  if (!items.length) return null;

  return (
    <div
      role="alert"
      className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-4"
    >
      <h3 className="text-sm font-semibold text-rose-800">{title}</h3>
      <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-rose-700">
        {items.map((item, index) => (
          <li key={`${item}-${index}`}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

# FILE 18 — `[UPDATE OR CREATE TESTS]` `bliss-telehealth/pbbf-telehealth/src/modules/*/__tests__/`

> This stage does not force one new test in every module, but it requires the modules to keep improving observable error behavior.  
> Add at least one error-state or retry-oriented test where missing.

## Recommended examples to add where needed
- `src/modules/appointments/__tests__/AppointmentsErrorState.test.jsx`
- `src/modules/telehealth/__tests__/SessionErrorState.test.jsx`
- `src/modules/admin/__tests__/AuditErrorState.test.jsx`

Example pattern:

```jsx
import { render, screen } from "@testing-library/react";
import ErrorState from "../../../shared/components/ErrorState";

describe("ErrorState", () => {
  it("renders retry-friendly messaging", () => {
    render(
      <ErrorState
        title="Unable to load appointments"
        message="Please try again in a moment."
      />
    );

    expect(screen.getByText("Unable to load appointments")).toBeInTheDocument();
    expect(screen.getByText("Please try again in a moment.")).toBeInTheDocument();
  });
});
```

---

# Recommended verification commands for Stage 4

## Backend observability test run
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

pytest tests/test_health.py tests/test_app_boot.py tests/modules/audit -q
```

## Frontend shared-state verification
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth

npx vitest run src/shared/components/__tests__/PageHeader.test.jsx src/components/ui/__tests__/Input.test.jsx
```

> Add module-specific error-state tests and run them too as you wire them in.

---

# Git commit recommendation for this stage

Run from the `bliss-telehealth` root:

```bash
git add docs/operations pbbf-api/app/common/middleware/logging.py pbbf-api/app/common/middleware/request_context.py pbbf-api/app/modules/audit pbbf-api/app/modules/notifications/tasks.py pbbf-api/tests/modules/audit pbbf-api/tests/test_health.py pbbf-api/tests/test_app_boot.py pbbf-telehealth/src/shared/components/ErrorState.jsx pbbf-telehealth/src/shared/hooks/useToast.js pbbf-telehealth/src/shared/components/FormErrorSummary.jsx
git commit -m "ops: add observability, audit enrichment, and incident readiness baseline"
```

---

# Completion gate for Stage 4

This stage is complete only when:
- operations docs exist
- request correlation IDs are attached to requests
- backend request lifecycle logging is in place
- audit writes are observable
- health and readiness endpoints are test-backed
- notification task triggers are loggable
- frontend error states are clearer and retry-friendly
- form-level failures are readable
- incidents and failed workflows can be explained from logs and audit evidence

---

# Final recommendation
Treat Stage 4 as the stage that gives the team narrative power over failures.

If a workflow breaks and the team still cannot answer:
- what failed
- when it failed
- who was affected
- which request triggered it

then Stage 4 is not complete yet.
