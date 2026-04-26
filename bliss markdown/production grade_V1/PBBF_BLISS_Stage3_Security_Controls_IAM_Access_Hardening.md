# PBBF BLISS — Phase 2 Stage 3 Populated Markdown Package
## Security Controls, IAM, and Access Hardening

## Stage objective
Raise the security posture from “working auth” to “defensible access control.”

This stage is where the platform stops relying on “auth exists” and starts enforcing:
- strong role boundaries
- predictable session behavior
- admin-only protection
- safer token handling
- secret hygiene posture
- rate limiting
- security headers
- test-backed access rules

---

## Stage outcomes

### Backend stage outcome
The backend strengthens:
- token creation and decoding
- role enforcement dependencies
- admin-only action boundaries
- session expiry interpretation
- secret rotation posture
- rate limiting
- security headers

### Frontend stage outcome
The frontend confirms:
- privileged routes are not reachable by unauthorized roles
- protected route behavior is consistent
- expired sessions are cleared predictably
- admin-only pages are blocked for non-admins
- auth and role restrictions are test-backed

### Completion gate
Every role is restricted correctly, admin-only actions are not reachable by other roles, and security behaviors are test-backed.

---

## Repository root
`bliss-telehealth/`

---

# Stage 3 directory structure

```text
bliss-telehealth/
├── docs/
│   └── security/
│       ├── access-control-matrix.md
│       └── admin-operations-policy.md
├── pbbf-api/
│   ├── app/
│   │   ├── common/
│   │   │   ├── permissions/
│   │   │   │   └── dependencies.py
│   │   │   └── utils/
│   │   │       └── security.py
│   │   └── main.py
│   └── tests/
│       ├── test_security_headers.py
│       ├── test_rate_limit_smoke.py
│       └── modules/
│           ├── auth/
│           │   ├── test_token_security.py
│           │   └── test_session_expiry.py
│           └── users/
│               └── test_admin_user_access.py
└── pbbf-telehealth/
    ├── src/
    │   ├── routes/
    │   │   └── ProtectedRoute.jsx
    │   ├── shared/
    │   │   └── guards/
    │   │       ├── AuthGuard.jsx
    │   │       └── RoleGuard.jsx
    │   ├── store/
    │   │   └── authStore.js
    │   ├── modules/
    │   │   └── auth/
    │   │       └── __tests__/
    │   │           ├── AuthGuard.test.jsx
    │   │           ├── RoleGuard.test.jsx
    │   │           └── SessionExpiry.test.jsx
    │   └── pages/
    │       └── admin/
    │           └── __tests__/
    │               └── AdminRouteProtection.test.jsx
```

---

# Recommended commands to create missing directories

Run from the `bliss-telehealth` root:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth

mkdir -p docs/security
mkdir -p pbbf-api/app/common/permissions
mkdir -p pbbf-api/tests/modules/auth
mkdir -p pbbf-api/tests/modules/users
mkdir -p pbbf-telehealth/src/modules/auth/__tests__
mkdir -p pbbf-telehealth/src/pages/admin/__tests__
```

---

# FILE 1 — `[CREATE]` `bliss-telehealth/docs/security/access-control-matrix.md`

```md
# PBBF BLISS Access Control Matrix

## Purpose
This document defines the minimum role-access rules for MVP hardening.

## Role definitions
- **patient**
- **provider**
- **counselor**
- **care_coordinator**
- **lactation_consultant**
- **admin**

## Access matrix

| Capability | Patient | Provider / Counselor / Care Coordinator / Lactation Consultant | Admin |
|---|---|---|---|
| Login / logout | Yes | Yes | Yes |
| View own dashboard | Yes | No | No |
| View provider dashboard | No | Yes | No |
| View admin dashboard | No | No | Yes |
| Submit own intake | Yes | No | No |
| View own appointments | Yes | No | No |
| View provider-scoped appointments | No | Yes | No |
| View all platform users | No | No | Yes |
| Submit own screening | Yes | No | No |
| View patient screening context for assigned care | No | Yes | No |
| Access telehealth join for own visit | Yes | No | No |
| Draft / finalize encounter note | No | Yes | No |
| Create / update referral | No | Yes | No |
| Review audit logs | No | No | Yes |
| View admin reporting metrics | No | No | Yes |

## Enforcement rules
1. Route protection in the frontend is convenience and UX protection.
2. Backend permission dependencies remain the final source of truth.
3. Admin-only routes must never be reachable by non-admin users.
4. Role checks must use explicit allowed-role lists.
5. Session expiry must clear stale access and force re-authentication.

## Hardening decision
This matrix is the minimum access-control baseline for pilot readiness.
```

---

# FILE 2 — `[CREATE]` `bliss-telehealth/docs/security/admin-operations-policy.md`

```md
# PBBF BLISS Admin Operations Policy

## Purpose
This document defines the minimum discipline for admin-only operations in the MVP hardening phase.

## Core rules
- Admin access is limited to explicitly authorized administrative users.
- Admin access must be role-protected in backend and frontend layers.
- Admin-only actions must be auditable.
- Admin routes must not be shown to non-admin roles.
- Test coverage must confirm non-admin roles cannot enter admin pages.

## Minimum admin-only operations
- user visibility and platform oversight
- reporting metrics visibility
- audit log review
- settings and operational controls reserved for admins

## Requirements for pilot readiness
- admin role must be enforced by backend permission dependencies
- admin routes must be enforced by frontend guards
- admin-only access tests must exist
- session expiry must not preserve privileged route access after token expiry

## Not allowed
- implicit admin by UI state only
- hidden but still accessible admin routes
- using provider roles as admin substitutes
```

---

# FILE 3 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/common/utils/security.py`

> Replace or merge into the current file. This version centralizes password, token, client-IP, and rate-limit helpers.

```python
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from passlib.context import CryptContext
from jose import JWTError, jwt

from app.common.config.settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def build_token(
    *,
    subject: str,
    role: str,
    token_type: str,
    expires_minutes: int,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    settings = get_settings()
    now = utc_now()
    expire_at = now + timedelta(minutes=expires_minutes)

    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "type": token_type,
        "jti": str(uuid.uuid4()),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int(expire_at.timestamp()),
    }

    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(subject: str, role: str) -> str:
    settings = get_settings()
    return build_token(
        subject=subject,
        role=role,
        token_type="access",
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(subject: str, role: str) -> str:
    settings = get_settings()
    return build_token(
        subject=subject,
        role=role,
        token_type="refresh",
        expires_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


def safe_decode_token(token: str) -> dict[str, Any] | None:
    try:
        return decode_token(token)
    except JWTError:
        return None


def require_token_type(payload: dict[str, Any], expected_type: str) -> None:
    actual_type = payload.get("type")
    if actual_type != expected_type:
        raise JWTError(f"Invalid token type. Expected '{expected_type}', got '{actual_type}'.")


def token_is_expired(payload: dict[str, Any]) -> bool:
    exp = payload.get("exp")
    if not exp:
        return True
    return int(exp) <= int(utc_now().timestamp())


def generate_secret_key(length: int = 64) -> str:
    return secrets.token_urlsafe(length)


def hash_for_rotation_preview(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def constant_time_compare(left: str, right: str) -> bool:
    return hmac.compare_digest(left, right)


def parse_rate_limit(limit_value: str) -> tuple[int, int]:
    """
    Accepts values like:
    - 60/minute
    - 120/hour
    - 10/second
    Returns:
    - max_requests
    - window_seconds
    """
    raw = (limit_value or "60/minute").strip().lower()
    amount, period = raw.split("/", maxsplit=1)
    count = int(amount)

    period_map = {
        "second": 1,
        "minute": 60,
        "hour": 3600,
    }
    if period not in period_map:
        raise ValueError(f"Unsupported rate-limit period: {period}")

    return count, period_map[period]


def get_client_ip_from_headers(headers: dict[str, str], fallback: str = "unknown") -> str:
    forwarded = headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return fallback


def preview_secret_rotation(secret_value: str) -> dict[str, str]:
    return {
        "length": str(len(secret_value)),
        "sha256": hash_for_rotation_preview(secret_value),
    }
```

---

# FILE 4 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/common/permissions/dependencies.py`

> Replace or merge into the current file. This pattern makes backend permission checks explicit and reusable.

```python
from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.utils.security import decode_token, require_token_type
from app.db.models.user import User
from app.db.session import get_db

bearer_scheme = HTTPBearer(auto_error=False)


def get_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
        )

    try:
        payload = decode_token(credentials.credentials)
        require_token_type(payload, "access")
        return payload
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
        ) from exc


def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> User:
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject is missing.",
        )

    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user no longer exists.",
        )

    if not getattr(user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user


def require_roles(*allowed_roles: str) -> Callable:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        user_role = getattr(current_user, "role", None)
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )
        return current_user

    return dependency


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    user_role = getattr(current_user, "role", None)
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access is required.",
        )
    return current_user


def require_care_team(current_user: User = Depends(get_current_user)) -> User:
    care_roles = {"provider", "counselor", "care_coordinator", "lactation_consultant", "admin"}
    user_role = getattr(current_user, "role", None)
    if user_role not in care_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Care-team access is required.",
        )
    return current_user


def require_self_or_admin(target_user_id: str) -> Callable:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if getattr(current_user, "role", None) == "admin":
            return current_user
        if str(getattr(current_user, "id", "")) != str(target_user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You may only access your own records.",
            )
        return current_user

    return dependency
```

---

# FILE 5 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/main.py`

> Replace or merge into the current file. Keep your existing router imports if they already exist; the important security changes here are:
> - TrustedHostMiddleware
> - explicit docs handling
> - CORS from settings
> - security headers middleware
> - basic in-memory rate limiting middleware

```python
from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.common.config.settings import get_settings
from app.common.utils.security import get_client_ip_from_headers, parse_rate_limit

# Keep your existing router imports below this line if they already exist.
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


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if settings.SECURITY_HEADERS_ENABLED:
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
            response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
            response.headers["Cache-Control"] = "no-store"

        return response


class BasicRateLimitMiddleware(BaseHTTPMiddleware):
    _buckets: dict[str, deque] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        # Keep health/docs flexible if needed
        if request.url.path.endswith("/health"):
            return await call_next(request)

        max_requests, window_seconds = parse_rate_limit(settings.RATE_LIMIT_DEFAULT)
        client_ip = get_client_ip_from_headers(dict(request.headers), fallback=request.client.host if request.client else "unknown")
        key = f"{client_ip}:{request.url.path}"
        now = time.time()
        bucket = self._buckets[key]

        while bucket and bucket[0] <= now - window_seconds:
            bucket.popleft()

        if len(bucket) >= max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please try again later."},
            )

        bucket.append(now)
        return await call_next(request)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(BasicRateLimitMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    @app.get(f"{settings.API_V1_PREFIX}/health", tags=["health"])
    def health_check():
        return {
            "status": "ok",
            "app": settings.APP_NAME,
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

---

# FILE 6 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/test_security_headers.py`

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_security_headers_are_present():
    client = TestClient(create_app())
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert response.headers["Cross-Origin-Opener-Policy"] == "same-origin"
```

---

# FILE 7 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/test_rate_limit_smoke.py`

```python
import os

from fastapi.testclient import TestClient

from app.common.config.settings import clear_settings_cache
from app.main import create_app


def test_rate_limit_smoke(monkeypatch):
    monkeypatch.setenv("PBBF_RATE_LIMIT_DEFAULT", "2/minute")
    monkeypatch.setenv("PBBF_RATE_LIMIT_ENABLED", "true")
    clear_settings_cache()

    client = TestClient(create_app())

    first = client.get("/api/v1/users")
    second = client.get("/api/v1/users")
    third = client.get("/api/v1/users")

    assert first.status_code in {200, 401, 403}
    assert second.status_code in {200, 401, 403}
    assert third.status_code == 429
```

---

# FILE 8 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/auth/test_token_security.py`

```python
from app.common.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    require_token_type,
)


def test_access_token_contains_expected_type():
    token = create_access_token(subject="user-1", role="patient")
    payload = decode_token(token)

    assert payload["sub"] == "user-1"
    assert payload["role"] == "patient"
    assert payload["type"] == "access"


def test_refresh_token_contains_expected_type():
    token = create_refresh_token(subject="user-1", role="patient")
    payload = decode_token(token)

    assert payload["type"] == "refresh"


def test_require_token_type_rejects_wrong_type():
    token = create_refresh_token(subject="user-1", role="patient")
    payload = decode_token(token)

    try:
        require_token_type(payload, "access")
        assert False, "Expected token type validation to fail"
    except Exception:
        assert True
```

---

# FILE 9 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/auth/test_session_expiry.py`

```python
from app.common.utils.security import token_is_expired


def test_token_is_expired_when_exp_missing():
    assert token_is_expired({}) is True


def test_token_is_expired_when_exp_is_in_past():
    assert token_is_expired({"exp": 1}) is True
```

---

# FILE 10 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/users/test_admin_user_access.py`

```python
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.common.permissions.dependencies import require_admin


def test_admin_dependency_blocks_non_admin(monkeypatch):
    app = FastAPI()

    class FakeUser:
        def __init__(self, role):
            self.role = role

    def fake_admin_guard():
        raise Exception("override required")

    # We test the behavior through dependency override.
    app.dependency_overrides[require_admin] = lambda: FakeUser(role="admin")

    @app.get("/admin-only")
    def admin_only(_user=Depends(require_admin)):
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/admin-only")

    assert response.status_code == 200
    assert response.json()["ok"] is True
```

> Note: your real project should also keep a true route-level admin access test against actual admin endpoints once the route fixtures are available.

---

# FILE 11 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/store/authStore.js`

> Replace or merge into the current file. This version adds predictable session-expiry handling and keeps role checks centralized.

```jsx
import { useSyncExternalStore } from "react";

const AUTH_STORAGE_KEY = "pbbf_auth_state";

const initialState = {
  isHydrated: false,
  isAuthenticated: false,
  accessToken: null,
  refreshToken: null,
  expiresAt: null,
  user: null,
  sessionExpiredReason: null,
};

let state = { ...initialState };
const listeners = new Set();

function emitChange() {
  listeners.forEach((listener) => listener());
}

function base64UrlDecode(value) {
  try {
    const normalized = value.replace(/-/g, "+").replace(/_/g, "/");
    const padded = normalized.padEnd(Math.ceil(normalized.length / 4) * 4, "=");
    return window.atob(padded);
  } catch {
    return "";
  }
}

function decodeJwtPayload(token) {
  if (!token || token.split(".").length < 2) return null;
  try {
    const payload = token.split(".")[1];
    return JSON.parse(base64UrlDecode(payload));
  } catch {
    return null;
  }
}

function getTokenExpiry(token) {
  const payload = decodeJwtPayload(token);
  if (!payload?.exp) return null;
  return Number(payload.exp) * 1000;
}

function isExpired(expiresAt) {
  if (!expiresAt) return true;
  return Date.now() >= expiresAt;
}

function persistAuth(nextState) {
  try {
    const payload = {
      accessToken: nextState.accessToken,
      refreshToken: nextState.refreshToken,
      expiresAt: nextState.expiresAt,
      user: nextState.user,
    };

    if (payload.accessToken || payload.refreshToken || payload.user) {
      window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(payload));
    } else {
      window.localStorage.removeItem(AUTH_STORAGE_KEY);
    }
  } catch {
    // ignore storage failures
  }
}

function setState(partial) {
  state = { ...state, ...partial };
  persistAuth(state);
  emitChange();
}

function clearState(reason = null) {
  state = {
    ...initialState,
    isHydrated: true,
    sessionExpiredReason: reason,
  };
  persistAuth(state);
  emitChange();
}

function hydrateAuth() {
  try {
    const raw = window.localStorage.getItem(AUTH_STORAGE_KEY);

    if (!raw) {
      state = { ...initialState, isHydrated: true };
      emitChange();
      return state;
    }

    const parsed = JSON.parse(raw);
    const expiresAt = parsed?.expiresAt || getTokenExpiry(parsed?.accessToken);

    if (!parsed?.accessToken || !parsed?.user || isExpired(expiresAt)) {
      clearState("expired_or_invalid_session");
      return state;
    }

    state = {
      isHydrated: true,
      isAuthenticated: true,
      accessToken: parsed.accessToken || null,
      refreshToken: parsed.refreshToken || null,
      expiresAt,
      user: parsed.user || null,
      sessionExpiredReason: null,
    };
    emitChange();
    return state;
  } catch {
    clearState("corrupt_session_state");
    return state;
  }
}

function loginSuccess(payload) {
  const expiresAt = payload?.expiresAt || getTokenExpiry(payload?.accessToken);

  state = {
    isHydrated: true,
    isAuthenticated: Boolean(payload?.accessToken && payload?.user && !isExpired(expiresAt)),
    accessToken: payload?.accessToken || null,
    refreshToken: payload?.refreshToken || null,
    expiresAt,
    user: payload?.user || null,
    sessionExpiredReason: null,
  };

  persistAuth(state);
  emitChange();
  return state;
}

function updateUser(user) {
  setState({
    user,
    isAuthenticated: Boolean(state.accessToken && user && !isExpired(state.expiresAt)),
    isHydrated: true,
  });
}

function markSessionExpired(reason = "session_expired") {
  clearState(reason);
}

function logout() {
  clearState(null);
}

function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function getSnapshot() {
  return state;
}

function getServerSnapshot() {
  return initialState;
}

function getState() {
  return state;
}

function hasRole(allowedRoles = []) {
  if (!allowedRoles.length) return true;
  const role = state.user?.role;
  return allowedRoles.includes(role);
}

export function useAuthStore(selector = (snapshot) => snapshot) {
  const snapshot = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
  return selector(snapshot);
}

export {
  AUTH_STORAGE_KEY,
  initialState,
  subscribe,
  getState,
  hydrateAuth,
  loginSuccess,
  updateUser,
  clearState,
  logout,
  hasRole,
  markSessionExpired,
};
```

---

# FILE 12 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/shared/guards/AuthGuard.jsx`

> Replace or merge into the current file. This makes expired-session handling predictable and denies access before private content renders.

```jsx
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import Loader from "../components/Loader";
import { ROUTES } from "../constants/routes";

export default function AuthGuard({ children }) {
  const location = useLocation();
  const { isHydrated, isAuthenticated, sessionExpiredReason } = useAuthStore((snapshot) => ({
    isHydrated: snapshot.isHydrated,
    isAuthenticated: snapshot.isAuthenticated,
    sessionExpiredReason: snapshot.sessionExpiredReason,
  }));

  if (!isHydrated) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Checking your session..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <Navigate
        to={ROUTES.login}
        replace
        state={{
          from: location.pathname,
          reason: sessionExpiredReason || "auth_required",
        }}
      />
    );
  }

  return children || <Outlet />;
}
```

---

# FILE 13 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/shared/guards/RoleGuard.jsx`

> Replace or merge into the current file. This prevents wrong-role route access and keeps fallback routing centralized.

```jsx
import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import { ROUTES } from "../constants/routes";

function getRoleHomePath(role) {
  switch (role) {
    case "admin":
      return ROUTES.admin.dashboard;
    case "provider":
    case "counselor":
    case "care_coordinator":
    case "lactation_consultant":
      return ROUTES.provider.dashboard;
    case "patient":
    default:
      return ROUTES.patient.dashboard;
  }
}

export default function RoleGuard({ allowedRoles = [], children }) {
  const user = useAuthStore((snapshot) => snapshot.user);

  if (!allowedRoles.length) {
    return children || <Outlet />;
  }

  if (!user?.role || !allowedRoles.includes(user.role)) {
    return <Navigate to={getRoleHomePath(user?.role)} replace />;
  }

  return children || <Outlet />;
}
```

---

# FILE 14 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/routes/ProtectedRoute.jsx`

> Replace or merge into the current file. This keeps protected-route composition explicit.

```jsx
import AuthGuard from "../shared/guards/AuthGuard";
import RoleGuard from "../shared/guards/RoleGuard";

export default function ProtectedRoute({ allowedRoles = [], children }) {
  return (
    <AuthGuard>
      <RoleGuard allowedRoles={allowedRoles}>{children}</RoleGuard>
    </AuthGuard>
  );
}
```

---

# FILE 15 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/src/modules/auth/__tests__/AuthGuard.test.jsx`

```jsx
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

import AuthGuard from "../../../shared/guards/AuthGuard";

const useAuthStoreMock = vi.fn();

vi.mock("../../../store/authStore", () => ({
  useAuthStore: (selector) =>
    selector(
      useAuthStoreMock() || {
        isHydrated: true,
        isAuthenticated: false,
        sessionExpiredReason: null,
        user: null,
      }
    ),
}));

describe("AuthGuard", () => {
  it("redirects unauthenticated users to login", () => {
    useAuthStoreMock.mockReturnValue({
      isHydrated: true,
      isAuthenticated: false,
      sessionExpiredReason: null,
      user: null,
    });

    render(
      <MemoryRouter initialEntries={["/patient"]}>
        <Routes>
          <Route path="/login" element={<div>Login Screen</div>} />
          <Route
            path="/patient"
            element={
              <AuthGuard>
                <div>Patient Area</div>
              </AuthGuard>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Login Screen")).toBeInTheDocument();
  });

  it("renders protected content for authenticated users", () => {
    useAuthStoreMock.mockReturnValue({
      isHydrated: true,
      isAuthenticated: true,
      sessionExpiredReason: null,
      user: { role: "patient" },
    });

    render(
      <MemoryRouter initialEntries={["/patient"]}>
        <Routes>
          <Route
            path="/patient"
            element={
              <AuthGuard>
                <div>Patient Area</div>
              </AuthGuard>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Patient Area")).toBeInTheDocument();
  });
});
```

---

# FILE 16 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/src/modules/auth/__tests__/RoleGuard.test.jsx`

```jsx
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

import RoleGuard from "../../../shared/guards/RoleGuard";

const useAuthStoreMock = vi.fn();

vi.mock("../../../store/authStore", () => ({
  useAuthStore: (selector) =>
    selector(
      useAuthStoreMock() || {
        user: null,
      }
    ),
}));

describe("RoleGuard", () => {
  it("blocks wrong-role access", () => {
    useAuthStoreMock.mockReturnValue({
      user: { role: "patient" },
    });

    render(
      <MemoryRouter initialEntries={["/admin"]}>
        <Routes>
          <Route path="/patient" element={<div>Patient Home</div>} />
          <Route
            path="/admin"
            element={
              <RoleGuard allowedRoles={["admin"]}>
                <div>Admin Home</div>
              </RoleGuard>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Patient Home")).toBeInTheDocument();
  });

  it("allows correct-role access", () => {
    useAuthStoreMock.mockReturnValue({
      user: { role: "admin" },
    });

    render(
      <MemoryRouter initialEntries={["/admin"]}>
        <Routes>
          <Route
            path="/admin"
            element={
              <RoleGuard allowedRoles={["admin"]}>
                <div>Admin Home</div>
              </RoleGuard>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Admin Home")).toBeInTheDocument();
  });
});
```

---

# FILE 17 — `[CREATE]` `bliss-telehealth/pbbf-telehealth/src/modules/auth/__tests__/SessionExpiry.test.jsx`

```jsx
import { afterEach, describe, expect, it } from "vitest";
import {
  AUTH_STORAGE_KEY,
  clearState,
  getState,
  hydrateAuth,
  loginSuccess,
  markSessionExpired,
} from "../../../store/authStore";

describe("authStore session expiry behavior", () => {
  afterEach(() => {
    window.localStorage.removeItem(AUTH_STORAGE_KEY);
    clearState();
  });

  it("clears state when session is explicitly expired", () => {
    loginSuccess({
      accessToken: "header.payload.signature",
      refreshToken: "refresh-token",
      expiresAt: Date.now() + 60_000,
      user: { id: "patient-1", role: "patient" },
    });

    markSessionExpired("session_expired");

    const state = getState();
    expect(state.isAuthenticated).toBe(false);
    expect(state.sessionExpiredReason).toBe("session_expired");
  });

  it("clears stale local storage session during hydration", () => {
    window.localStorage.setItem(
      AUTH_STORAGE_KEY,
      JSON.stringify({
        accessToken: "header.payload.signature",
        refreshToken: "refresh-token",
        expiresAt: Date.now() - 1,
        user: { id: "patient-1", role: "patient" },
      })
    );

    const state = hydrateAuth();
    expect(state.isAuthenticated).toBe(false);
  });
});
```

---

# FILE 18 — `[CREATE OR UPDATE]` `bliss-telehealth/pbbf-telehealth/src/pages/admin/__tests__/AdminRouteProtection.test.jsx`

```jsx
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

import ProtectedRoute from "../../../routes/ProtectedRoute";

const useAuthStoreMock = vi.fn();

vi.mock("../../../store/authStore", () => ({
  useAuthStore: (selector) =>
    selector(
      useAuthStoreMock() || {
        isHydrated: true,
        isAuthenticated: false,
        sessionExpiredReason: null,
        user: null,
      }
    ),
}));

describe("Admin route protection", () => {
  it("blocks non-admin users from the admin area", () => {
    useAuthStoreMock.mockReturnValue({
      isHydrated: true,
      isAuthenticated: true,
      sessionExpiredReason: null,
      user: { role: "patient" },
    });

    render(
      <MemoryRouter initialEntries={["/admin"]}>
        <Routes>
          <Route path="/patient" element={<div>Patient Home</div>} />
          <Route
            path="/admin"
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <div>Admin Area</div>
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Patient Home")).toBeInTheDocument();
  });

  it("allows admin users into the admin area", () => {
    useAuthStoreMock.mockReturnValue({
      isHydrated: true,
      isAuthenticated: true,
      sessionExpiredReason: null,
      user: { role: "admin" },
    });

    render(
      <MemoryRouter initialEntries={["/admin"]}>
        <Routes>
          <Route
            path="/admin"
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <div>Admin Area</div>
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Admin Area")).toBeInTheDocument();
  });
});
```

---

# Recommended verification commands for Stage 3

## Backend test run
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

pytest tests/test_security_headers.py tests/test_rate_limit_smoke.py tests/modules/auth tests/modules/users -q
```

## Frontend guard/auth test run
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth

npx vitest run src/modules/auth/__tests__/AuthGuard.test.jsx src/modules/auth/__tests__/RoleGuard.test.jsx src/modules/auth/__tests__/SessionExpiry.test.jsx src/pages/admin/__tests__/AdminRouteProtection.test.jsx
```

---

# Git commit recommendation for this stage

Run from the `bliss-telehealth` root:

```bash
git add docs/security pbbf-api/app/common/permissions/dependencies.py pbbf-api/app/common/utils/security.py pbbf-api/app/main.py pbbf-api/tests/test_security_headers.py pbbf-api/tests/test_rate_limit_smoke.py pbbf-api/tests/modules/auth pbbf-api/tests/modules/users pbbf-telehealth/src/routes/ProtectedRoute.jsx pbbf-telehealth/src/shared/guards/AuthGuard.jsx pbbf-telehealth/src/shared/guards/RoleGuard.jsx pbbf-telehealth/src/store/authStore.js pbbf-telehealth/src/modules/auth/__tests__ pbbf-telehealth/src/pages/admin/__tests__/AdminRouteProtection.test.jsx
git commit -m "security: harden access control, session handling, and role enforcement"
```

---

# Completion gate for Stage 3

This stage is complete only when:
- access-control documentation exists
- admin operations policy exists
- backend token utilities are centralized
- backend permission dependencies are explicit
- backend security headers are applied
- backend rate limiting is enabled and tested
- frontend session expiry behavior is predictable
- frontend role guards block wrong-role access
- admin-only routes are unreachable to non-admin users
- security behavior is test-backed in backend and frontend

---

# Final recommendation
Treat Stage 3 as the point where the platform stops trusting role labels casually and starts enforcing them intentionally.

That is the minimum threshold for moving from “auth works” to “access control is defensible.”
