
# PBBF BLISS — Backend Phase 1 Populated Files  
**Phase:** Backend Phase 1 — Foundation Audit and Structural Cleanup  
**Objective:** Stabilize the current FastAPI codebase, remove structural ambiguity, and make the backend safe to build on without rework later.

This package keeps your current modular layout and fills the Phase 1 foundation files so the backend can:
- boot cleanly,
- expose a stable app factory,
- expose stable health endpoints,
- initialize database sessions predictably,
- standardize responses and exception handling,
- support clean middleware and request context,
- provide test-safe settings and DB setup,
- give you a reusable repository base for later modules,
- run smoke tests before feature expansion continues.

---

## Structural cleanup note

If this path truly exists as shown:

```bash
app/jobs/{__init__.py}
```

correct it before anything else:

```bash
mkdir -p app/jobs
touch app/jobs/__init__.py
rm -f "app/jobs/{__init__.py}"
```

---

## 1) `app/main.py`

```python
from app import create_app

app = create_app()
```

---

## 2) `app/__init__.py`

```python
from __future__ import annotations

import logging
import pkgutil
from contextlib import asynccontextmanager
from importlib import import_module
from pathlib import Path

from fastapi import APIRouter, FastAPI

from app.common.config.settings import get_settings
from app.common.errors.handlers import register_exception_handlers
from app.common.middleware.logging import RequestLoggingMiddleware
from app.common.middleware.request_context import RequestContextMiddleware
from app.common.utils.response import success_response
from app.db.session import check_database_connection, init_db

logger = logging.getLogger(__name__)


def _discover_and_register_module_routers(app: FastAPI) -> None:
    """
    Discovers app.modules.<module>.router and includes `router` or `api_router`
    when present. This preserves your current modular layout without hardcoding
    every module import in the foundation phase.
    """
    settings = get_settings()
    modules_path = Path(__file__).resolve().parent / "modules"

    if not modules_path.exists():
        logger.warning("Modules directory not found: %s", modules_path)
        app.state.router_import_errors = []
        return

    import_errors: list[dict[str, str]] = []

    for module_info in sorted(pkgutil.iter_modules([str(modules_path)]), key=lambda item: item.name):
        module_name = module_info.name
        router_module_path = f"app.modules.{module_name}.router"

        try:
            router_module = import_module(router_module_path)
            router = getattr(router_module, "router", None) or getattr(router_module, "api_router", None)

            if isinstance(router, APIRouter):
                app.include_router(router)
                logger.info("Included router from %s", router_module_path)
            else:
                logger.info("No APIRouter found in %s; skipping.", router_module_path)

        except Exception as exc:  # foundation phase: keep boot stable, log failures clearly
            logger.exception("Failed to import router module: %s", router_module_path)
            import_errors.append(
                {
                    "module": module_name,
                    "router_module": router_module_path,
                    "error": str(exc),
                }
            )

            # Fail fast only in staging/production.
            if settings.app_env in {"staging", "production"}:
                raise

    app.state.router_import_errors = import_errors


def _register_core_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(RequestLoggingMiddleware)


def _register_system_routes(app: FastAPI) -> None:
    settings = get_settings()

    @app.get("/", include_in_schema=False)
    async def root():
        return success_response(
            message="PBBF Telehealth API is running.",
            data={
                "app_name": settings.app_name,
                "environment": settings.app_env,
                "version": settings.version,
            },
        )

    async def _health_payload():
        db_connected = check_database_connection()
        status = "ok" if db_connected else "degraded"
        return {
            "status": status,
            "environment": settings.app_env,
            "version": settings.version,
            "database": {
                "connected": db_connected,
                "url": settings.effective_database_url,
            },
            "router_import_errors": getattr(app.state, "router_import_errors", []),
        }

    @app.get(settings.healthcheck_path, tags=["system"])
    async def health():
        payload = await _health_payload()
        status_code = 200 if payload["database"]["connected"] else 503
        return success_response(
            message="Health check completed.",
            data=payload,
            status_code=status_code,
        )

    @app.get(f"{settings.api_v1_prefix}/health", tags=["system"])
    async def health_v1():
        payload = await _health_payload()
        status_code = 200 if payload["database"]["connected"] else 503
        return success_response(
            message="Health check completed.",
            data=payload,
            status_code=status_code,
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("Starting %s (%s)", settings.app_name, settings.app_env)
    init_db()
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.state.settings = settings

    _register_core_middleware(app)
    register_exception_handlers(app)
    _register_system_routes(app)
    _discover_and_register_module_routers(app)

    return app
```

---

## 3) `app/common/config/settings.py`

```python
from __future__ import annotations

from functools import lru_cache
from typing import Any, Literal

from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PBBF Telehealth API"
    app_env: Literal["development", "testing", "staging", "production"] = "development"
    version: str = "0.1.0"
    debug: bool = True

    api_v1_prefix: str = "/api/v1"
    healthcheck_path: str = "/health"

    host: str = "0.0.0.0"
    port: int = 8000

    secret_key: str = "change-this-in-env"
    access_token_expire_minutes: int = 60

    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    database_url: str = "sqlite:///./bliss_telehealth.db"
    test_database_url: str = "sqlite:///./bliss_telehealth_test.db"
    sqlalchemy_echo: bool = False
    sqlalchemy_pool_pre_ping: bool = True

    log_level: str = "INFO"
    request_id_header: str = "X-Request-ID"
    timezone: str = "UTC"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return []
            if stripped.startswith("[") and stripped.endswith("]"):
                stripped = stripped[1:-1]
            return [item.strip().strip('"').strip("'") for item in stripped.split(",") if item.strip()]
        raise ValueError("allowed_origins must be a list or comma-separated string")

    @computed_field
    @property
    def is_testing(self) -> bool:
        return self.app_env == "testing"

    @computed_field
    @property
    def effective_database_url(self) -> str:
        return self.test_database_url if self.is_testing else self.database_url

    @computed_field
    @property
    def database_connect_args(self) -> dict[str, Any]:
        if self.effective_database_url.startswith("sqlite"):
            return {"check_same_thread": False}
        return {}


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reload_settings() -> Settings:
    get_settings.cache_clear()
    return get_settings()
```

---

## 4) `app/db/session.py`

```python
from __future__ import annotations

from contextlib import contextmanager
from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.common.config.settings import get_settings
from app.db.base import Base
from app.db.models import import_all_models


@lru_cache
def get_engine():
    settings = get_settings()

    engine_kwargs = {
        "echo": settings.sqlalchemy_echo,
        "future": True,
        "pool_pre_ping": settings.sqlalchemy_pool_pre_ping,
    }

    if settings.database_connect_args:
        engine_kwargs["connect_args"] = settings.database_connect_args

    return create_engine(settings.effective_database_url, **engine_kwargs)


@lru_cache
def get_session_factory() -> sessionmaker:
    return sessionmaker(
        bind=get_engine(),
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=Session,
    )


def reset_session_state() -> None:
    """
    Useful in tests when environment variables change between test runs.
    """
    try:
        get_engine().dispose()
    except Exception:
        pass

    get_session_factory.cache_clear()
    get_engine.cache_clear()


def init_db() -> None:
    """
    Imports all models first, then creates metadata-bound tables.
    For this phase, this provides a stable local/test startup path.
    """
    import_all_models()
    Base.metadata.create_all(bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    db = get_session_factory()()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session_context() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def check_database_connection() -> bool:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
```

---

## 5) `app/db/base.py`

```python
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )
```

---

## 6) `app/db/__init__.py`

```python
from app.db.base import Base, TimestampMixin
from app.db.session import (
    check_database_connection,
    db_session_context,
    get_db,
    get_engine,
    get_session_factory,
    init_db,
    reset_session_state,
)

__all__ = [
    "Base",
    "TimestampMixin",
    "get_engine",
    "get_session_factory",
    "get_db",
    "db_session_context",
    "init_db",
    "reset_session_state",
    "check_database_connection",
]
```

---

## 7) `requirements.txt`

```text
fastapi>=0.115,<1.0
uvicorn[standard]>=0.30,<1.0
sqlalchemy>=2.0,<3.0
alembic>=1.13,<2.0
pydantic>=2.7,<3.0
pydantic-settings>=2.4,<3.0
python-dotenv>=1.0,<2.0
redis>=5.0,<6.0
httpx>=0.27,<1.0
pytest>=8.0,<9.0
pytest-cov>=5.0,<6.0
passlib[bcrypt]>=1.7,<2.0
email-validator>=2.0,<3.0
anyio>=4.0,<5.0
```

---

## 8) `scripts/seed_users.py`

```python
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from passlib.context import CryptContext
from sqlalchemy import select

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.common.utils.datetime import utc_now  # noqa: E402
from app.db.models import get_model_class  # noqa: E402
from app.db.session import db_session_context, init_db  # noqa: E402

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class SeedUser:
    email: str
    role: str
    full_name: str
    password: str = "ChangeMe123!"


DEFAULT_USERS = [
    SeedUser(email="admin@pbbf.local", role="admin", full_name="Foundation Admin"),
    SeedUser(email="provider@pbbf.local", role="provider", full_name="Primary Provider"),
    SeedUser(email="patient@pbbf.local", role="patient", full_name="Demo Patient"),
]


def hash_password(raw_password: str) -> str:
    return pwd_context.hash(raw_password)


def build_user_payload(user_model, seed: SeedUser) -> dict:
    columns = {column.name for column in user_model.__table__.columns}
    now = utc_now()

    payload: dict = {}

    if "email" in columns:
        payload["email"] = seed.email

    if "role" in columns:
        payload["role"] = seed.role

    if "full_name" in columns:
        payload["full_name"] = seed.full_name

    if "first_name" in columns and "last_name" in columns:
        parts = seed.full_name.split(maxsplit=1)
        payload["first_name"] = parts[0]
        payload["last_name"] = parts[1] if len(parts) > 1 else ""

    if "password_hash" in columns:
        payload["password_hash"] = hash_password(seed.password)

    if "is_active" in columns:
        payload["is_active"] = True

    if "status" in columns:
        payload["status"] = "active"

    if "created_at" in columns:
        payload["created_at"] = now

    if "updated_at" in columns:
        payload["updated_at"] = now

    return payload


def main() -> int:
    init_db()

    user_model = get_model_class("User")
    if user_model is None:
        print("User model not found in app.db.models. Seed skipped safely.")
        return 0

    if not hasattr(user_model, "email"):
        print("User model does not expose an `email` field. Seed skipped safely.")
        return 0

    created_count = 0

    with db_session_context() as session:
        for seed in DEFAULT_USERS:
            existing_user = session.execute(
                select(user_model).where(user_model.email == seed.email)
            ).scalar_one_or_none()

            if existing_user:
                print(f"Already exists: {seed.email}")
                continue

            payload = build_user_payload(user_model, seed)
            new_user = user_model(**payload)
            session.add(new_user)
            created_count += 1
            print(f"Created seed user: {seed.email} [{seed.role}]")

    print(f"Seeding complete. Users created: {created_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

---

## 9) `app/common/errors/http_exceptions.py`

```python
from __future__ import annotations

from typing import Any


class AppException(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        message: str,
        code: str | None = None,
        details: Any = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.code = code or "APP_ERROR"
        self.details = details
        super().__init__(message)


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request.", details: Any = None) -> None:
        super().__init__(status_code=400, message=message, code="BAD_REQUEST", details=details)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication required.", details: Any = None) -> None:
        super().__init__(status_code=401, message=message, code="UNAUTHORIZED", details=details)


class ForbiddenException(AppException):
    def __init__(self, message: str = "You do not have permission to perform this action.", details: Any = None) -> None:
        super().__init__(status_code=403, message=message, code="FORBIDDEN", details=details)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found.", details: Any = None) -> None:
        super().__init__(status_code=404, message=message, code="NOT_FOUND", details=details)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource conflict.", details: Any = None) -> None:
        super().__init__(status_code=409, message=message, code="CONFLICT", details=details)


class ServiceUnavailableException(AppException):
    def __init__(self, message: str = "Service unavailable.", details: Any = None) -> None:
        super().__init__(
            status_code=503,
            message=message,
            code="SERVICE_UNAVAILABLE",
            details=details,
        )
```

---

## 10) `app/common/errors/handlers.py`

```python
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.common.errors.http_exceptions import AppException

logger = logging.getLogger(__name__)


def _error_payload(
    *,
    message: str,
    code: str,
    details=None,
    request_id: str | None = None,
):
    return {
        "success": False,
        "message": message,
        "error": {
            "code": code,
            "details": details,
        },
        "meta": {
            "request_id": request_id,
        },
    }


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            _error_payload(
                message=exc.message,
                code=exc.code,
                details=exc.details,
                request_id=request_id,
            )
        ),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            _error_payload(
                message=str(exc.detail),
                code="HTTP_EXCEPTION",
                details=None,
                request_id=request_id,
            )
        ),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            _error_payload(
                message="Validation failed.",
                code="VALIDATION_ERROR",
                details=exc.errors(),
                request_id=request_id,
            )
        ),
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    logger.exception("Database error during request", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            _error_payload(
                message="A database error occurred.",
                code="DATABASE_ERROR",
                details=None,
                request_id=request_id,
            )
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    logger.exception("Unhandled application error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            _error_payload(
                message="An unexpected server error occurred.",
                code="INTERNAL_SERVER_ERROR",
                details=None,
                request_id=request_id,
            )
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
```

---

## 11) `app/common/middleware/request_context.py`

```python
from __future__ import annotations

from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.common.config.settings import get_settings
from app.common.utils.datetime import utc_now


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        settings = get_settings()

        request_id = request.headers.get(settings.request_id_header) or str(uuid4())
        request.state.request_id = request_id
        request.state.request_started_at = utc_now()

        response = await call_next(request)
        response.headers[settings.request_id_header] = request_id
        return response
```

---

## 12) `app/common/middleware/logging.py`

```python
from __future__ import annotations

import logging
from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("app.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        started = perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((perf_counter() - started) * 1000, 2)
            logger.exception(
                "Request failed | method=%s path=%s request_id=%s duration_ms=%s",
                request.method,
                request.url.path,
                getattr(request.state, "request_id", None),
                duration_ms,
            )
            raise

        duration_ms = round((perf_counter() - started) * 1000, 2)

        logger.info(
            "Request completed | method=%s path=%s status=%s request_id=%s duration_ms=%s",
            request.method,
            request.url.path,
            response.status_code,
            getattr(request.state, "request_id", None),
            duration_ms,
        )
        return response
```

---

## 13) `app/common/permissions/dependencies.py`

```python
from __future__ import annotations

from typing import Callable

from fastapi import Depends, Header, Request
from pydantic import BaseModel, Field

from app.common.errors.http_exceptions import ForbiddenException, UnauthorizedException


class AuthContext(BaseModel):
    user_id: str | None = None
    role: str | None = None
    scopes: set[str] = Field(default_factory=set)


def get_auth_context(
    request: Request,
    x_user_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
    x_user_scopes: str | None = Header(default=None),
) -> AuthContext:
    """
    Phase 1 foundation dependency:
    - Works with request.state.user if an auth middleware later injects it.
    - Falls back to simple headers during tests/dev.
    """
    state_user = getattr(request.state, "user", None)

    if isinstance(state_user, dict):
        scopes = state_user.get("scopes", []) or []
        return AuthContext(
            user_id=state_user.get("user_id"),
            role=state_user.get("role"),
            scopes=set(scopes),
        )

    parsed_scopes = set()
    if x_user_scopes:
        parsed_scopes = {scope.strip() for scope in x_user_scopes.split(",") if scope.strip()}

    return AuthContext(
        user_id=x_user_id,
        role=x_user_role,
        scopes=parsed_scopes,
    )


def require_authenticated_user(
    auth_context: AuthContext = Depends(get_auth_context),
) -> AuthContext:
    if not auth_context.user_id:
        raise UnauthorizedException()
    return auth_context


def require_roles(*allowed_roles: str) -> Callable:
    allowed = {role.strip() for role in allowed_roles if role.strip()}

    def dependency(auth_context: AuthContext = Depends(require_authenticated_user)) -> AuthContext:
        if allowed and auth_context.role not in allowed:
            raise ForbiddenException(
                message="You do not have the required role for this action.",
                details={"allowed_roles": sorted(allowed), "current_role": auth_context.role},
            )
        return auth_context

    return dependency


def require_scopes(*required_scopes: str) -> Callable:
    required = {scope.strip() for scope in required_scopes if scope.strip()}

    def dependency(auth_context: AuthContext = Depends(require_authenticated_user)) -> AuthContext:
        if not required.issubset(auth_context.scopes):
            raise ForbiddenException(
                message="You do not have the required scopes for this action.",
                details={
                    "required_scopes": sorted(required),
                    "granted_scopes": sorted(auth_context.scopes),
                },
            )
        return auth_context

    return dependency
```

---

## 14) `app/common/validators/pagination.py`

```python
from __future__ import annotations

from typing import Literal

from fastapi import Query
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    sort_by: str | None = None
    sort_order: Literal["asc", "desc"] = "asc"
    search: str | None = None

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


def pagination_params(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    sort_by: str | None = Query(default=None),
    sort_order: Literal["asc", "desc"] = Query(default="asc"),
    search: str | None = Query(default=None),
) -> PaginationParams:
    return PaginationParams(
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search,
    )
```

---

## 15) `app/common/utils/datetime.py`

```python
from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


UTC = timezone.utc


def utc_now() -> datetime:
    return datetime.now(UTC)


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def to_timezone(value: datetime, timezone_name: str) -> datetime:
    return ensure_utc(value).astimezone(ZoneInfo(timezone_name))


def parse_iso_datetime(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    return ensure_utc(datetime.fromisoformat(normalized))


def isoformat_z(value: datetime) -> str:
    return ensure_utc(value).isoformat().replace("+00:00", "Z")
```

---

## 16) `app/common/utils/pagination.py`

```python
from __future__ import annotations

from math import ceil
from typing import Any, Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.common.validators.pagination import PaginationParams


def build_pagination_meta(*, total_items: int, params: PaginationParams) -> dict[str, Any]:
    total_pages = ceil(total_items / params.per_page) if total_items else 1

    return {
        "page": params.page,
        "per_page": params.per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": params.page < total_pages,
        "has_previous": params.page > 1,
    }


def paginate_list(items: Sequence[Any], params: PaginationParams) -> tuple[list[Any], dict[str, Any]]:
    total_items = len(items)
    start = params.offset
    end = start + params.per_page
    paginated_items = list(items[start:end])
    meta = build_pagination_meta(total_items=total_items, params=params)
    return paginated_items, meta


def paginate_select(
    *,
    session: Session,
    statement: Select,
    params: PaginationParams,
) -> tuple[list[Any], dict[str, Any]]:
    count_subquery = statement.order_by(None).subquery()
    total_items = session.execute(select(func.count()).select_from(count_subquery)).scalar_one()

    paginated_statement = statement.offset(params.offset).limit(params.per_page)
    items = session.execute(paginated_statement).scalars().all()

    meta = build_pagination_meta(total_items=total_items, params=params)
    return items, meta
```

---

## 17) `app/common/utils/response.py`

```python
from __future__ import annotations

from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    *,
    message: str = "Request successful.",
    data: Any = None,
    meta: dict | None = None,
    status_code: int = 200,
) -> JSONResponse:
    payload = {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta or {},
    }
    return JSONResponse(status_code=status_code, content=jsonable_encoder(payload))


def error_response(
    *,
    message: str = "Request failed.",
    error_code: str = "REQUEST_FAILED",
    details: Any = None,
    meta: dict | None = None,
    status_code: int = 400,
) -> JSONResponse:
    payload = {
        "success": False,
        "message": message,
        "error": {
            "code": error_code,
            "details": details,
        },
        "meta": meta or {},
    }
    return JSONResponse(status_code=status_code, content=jsonable_encoder(payload))


def paginated_response(
    *,
    message: str = "Request successful.",
    items: list[Any],
    pagination: dict[str, Any],
    extra_meta: dict | None = None,
    status_code: int = 200,
) -> JSONResponse:
    meta = {"pagination": pagination}
    if extra_meta:
        meta.update(extra_meta)

    payload = {
        "success": True,
        "message": message,
        "data": items,
        "meta": meta,
    }
    return JSONResponse(status_code=status_code, content=jsonable_encoder(payload))
```

---

## 18) `app/db/models/__init__.py`

```python
from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from app.db.base import Base

MODELS_PACKAGE = __name__
MODELS_PATH = Path(__file__).resolve().parent


def import_all_models() -> list[str]:
    imported_modules: list[str] = []

    for module_info in pkgutil.iter_modules([str(MODELS_PATH)]):
        if module_info.name.startswith("_"):
            continue

        module_path = f"{MODELS_PACKAGE}.{module_info.name}"
        importlib.import_module(module_path)
        imported_modules.append(module_info.name)

    return imported_modules


def get_model_class(model_name: str):
    import_all_models()

    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        if model_class.__name__ == model_name:
            return model_class

    return None
```

---

## 19) `app/db/repositories/base.py`

```python
from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, record_id: Any) -> ModelType | None:
        return self.db.get(self.model, record_id)

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        order_by=None,
    ) -> list[ModelType]:
        statement: Select = select(self.model).offset(offset).limit(limit)

        if order_by is not None:
            statement = statement.order_by(order_by)

        return self.db.execute(statement).scalars().all()

    def count(self) -> int:
        statement = select(func.count()).select_from(self.model)
        return self.db.execute(statement).scalar_one()

    def create(self, payload: dict[str, Any]) -> ModelType:
        instance = self.model(**payload)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, instance: ModelType, payload: dict[str, Any]) -> ModelType:
        for field, value in payload.items():
            if hasattr(instance, field):
                setattr(instance, field, value)

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, instance: ModelType) -> None:
        self.db.delete(instance)
        self.db.commit()
```

---

## 20) `tests/__init__.py`

```python
# Test package marker for pytest discovery.
```

---

## 21) `tests/conftest.py`

```python
from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def test_db_url(tmp_path_factory) -> str:
    db_dir = tmp_path_factory.mktemp("db")
    db_file = db_dir / "phase1_test.db"
    return f"sqlite:///{db_file}"


@pytest.fixture(scope="session", autouse=True)
def configure_test_environment(test_db_url: str):
    os.environ["APP_ENV"] = "testing"
    os.environ["DATABASE_URL"] = test_db_url
    os.environ["TEST_DATABASE_URL"] = test_db_url
    os.environ["SECRET_KEY"] = "phase1-test-secret"
    os.environ["ALLOWED_ORIGINS"] = "http://localhost:5173"

    from app.common.config.settings import reload_settings
    from app.db.session import reset_session_state

    reload_settings()
    reset_session_state()

    yield

    reset_session_state()
    reload_settings()


@pytest.fixture()
def app(configure_test_environment):
    from app import create_app
    from app.db.session import init_db

    init_db()
    return create_app()


@pytest.fixture()
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def db_session(configure_test_environment):
    from app.db.session import get_session_factory

    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()
```

---

## 22) `tests/test_health.py`

```python
def test_health_endpoint_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Health check completed."
    assert body["data"]["status"] == "ok"
    assert body["data"]["database"]["connected"] is True


def test_versioned_health_endpoint_returns_ok(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["data"]["database"]["connected"] is True
```

---

## 23) `tests/test_app_boot.py`

```python
from sqlalchemy import text


def test_app_boot_smoke(client):
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["data"]["app_name"] == "PBBF Telehealth API"
    assert body["data"]["environment"] == "testing"


def test_settings_loading():
    from app.common.config.settings import get_settings

    settings = get_settings()

    assert settings.app_env == "testing"
    assert settings.is_testing is True
    assert settings.effective_database_url.startswith("sqlite")


def test_db_session_creation(db_session):
    result = db_session.execute(text("SELECT 1")).scalar_one()
    assert result == 1
```

---

# Apply commands

From the backend root:

```bash
mkdir -p app/common/errors \
         app/common/middleware \
         app/common/permissions \
         app/common/validators \
         app/common/utils \
         app/db/models \
         app/db/repositories \
         tests
```

Then create/update the files above.

---

# Test commands for this phase

Install/update dependencies:

```bash
pip install -r requirements.txt
```

Run the backend smoke tests:

```bash
pytest -q tests/test_health.py tests/test_app_boot.py
```

Run the app locally:

```bash
uvicorn app.main:app --reload
```

Quick manual checks:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/health
```

Seed safe demo users later when a concrete `User` model exists:

```bash
python scripts/seed_users.py
```

---

# Phase 1 completion checkpoint

You can consider **Backend Phase 1 complete** when all of the following are true:

- `uvicorn app.main:app --reload` starts without app boot errors.
- `GET /health` returns HTTP 200 with database connected.
- `GET /api/v1/health` returns HTTP 200 with database connected.
- `pytest -q tests/test_health.py tests/test_app_boot.py` passes.
- `get_settings()` resolves correctly in test mode.
- DB session creation works without import-path or initialization issues.
- `app/jobs/__init__.py` exists as a normal package file if that odd path was real.

---

# Migration note

**No Alembic migration command is required in this phase** because this phase does **not** introduce or alter concrete database tables/models.  
You only added the Phase 1 DB foundation layer, model registry support, and test-safe startup/session plumbing.

Once you begin adding actual SQLAlchemy models in later phases, use the exact migration flow:

```bash
alembic revision --autogenerate -m "describe_the_model_change"
alembic upgrade head
```
