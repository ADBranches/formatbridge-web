
# PBBF BLISS — Backend Phase 3 Populated Files  
## Authentication, Authorization, and Identity Controls

## Objective
Finish secure authentication and role-based authorization for patients, providers, care coordinators, and admins so that all later backend modules can rely on a stable identity layer without rewriting auth logic.

This phase populates and/or completes the following areas:

- `app/modules/auth`
- `app/modules/users`
- `app/common/utils/security.py`
- `app/common/permissions/dependencies.py`
- auth and user test suites

This implementation assumes the Phase 1 and Phase 2 foundation already exist:
- app factory or clean FastAPI startup path
- SQLAlchemy session dependency
- core models and relationships
- seeded roles table
- stable test fixtures in `tests/conftest.py`

---

## Pre-flight notes before pasting code

1. **Keep the current modular layout.**
2. **Do not create new auth logic elsewhere.** All later modules should depend on this phase.
3. If these packages are **missing** from `requirements.txt`, add them before running tests:
   - `python-jose[cryptography]`
   - `passlib[bcrypt]`
   - `email-validator`
4. This phase does **not require a migration** unless your Phase 2 models still differ from the assumptions below.
5. Assumed model relationships:
   - `User.role -> Role`
   - `Role.name` exists
   - `User` includes at least:
     - `id`
     - `email`
     - `full_name`
     - `password_hash`
     - `is_active`
     - `role_id`
     - optional `last_login_at`, `phone_number`

---

## Expected endpoints after this phase

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

- `GET /api/v1/users/me`
- `PATCH /api/v1/users/me`
- `GET /api/v1/users`
- `GET /api/v1/users/{user_id}`
- `PATCH /api/v1/users/{user_id}/role`
- `PATCH /api/v1/users/{user_id}/status`

---

## File 1 — `app/common/utils/security.py`

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.common.config.settings import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _token_expiry_delta(token_type: str) -> timedelta:
    settings = get_settings()

    if token_type == "refresh":
        refresh_days = getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 7)
        return timedelta(days=refresh_days)

    access_minutes = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    return timedelta(minutes=access_minutes)


def create_token(
    *,
    subject: str,
    token_type: str,
    email: Optional[str] = None,
    role: Optional[str] = None,
    additional_claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    settings = get_settings()
    now = utcnow()
    expire = now + (expires_delta or _token_expiry_delta(token_type))

    payload: Dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    if email:
        payload["email"] = email

    if role:
        payload["role"] = role

    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=getattr(settings, "JWT_ALGORITHM", "HS256"),
    )


def decode_token(token: str) -> Dict[str, Any]:
    settings = get_settings()
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[getattr(settings, "JWT_ALGORITHM", "HS256")],
        )
    except JWTError as exc:
        raise ValueError("Invalid or expired token.") from exc


def create_access_token(
    *,
    subject: str,
    email: Optional[str] = None,
    role: Optional[str] = None,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    return create_token(
        subject=subject,
        token_type="access",
        email=email,
        role=role,
        additional_claims=additional_claims,
    )


def create_refresh_token(
    *,
    subject: str,
    email: Optional[str] = None,
    role: Optional[str] = None,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    return create_token(
        subject=subject,
        token_type="refresh",
        email=email,
        role=role,
        additional_claims=additional_claims,
    )


def validate_token_type(payload: Dict[str, Any], expected_type: str) -> None:
    token_type = payload.get("type")
    if token_type != expected_type:
        raise ValueError(f"Expected a {expected_type} token.")


def issue_token_pair(user_id: str, email: str, role: str) -> Dict[str, str]:
    return {
        "access_token": create_access_token(subject=user_id, email=email, role=role),
        "refresh_token": create_refresh_token(subject=user_id, email=email, role=role),
        "token_type": "bearer",
    }
```

---

## File 2 — `app/common/permissions/dependencies.py`

```python
from __future__ import annotations

from typing import Callable

from fastapi import Depends, HTTPException, status

from app.modules.auth.dependencies import get_current_active_user


def require_roles(*allowed_roles: str) -> Callable:
    allowed = {role.strip().lower() for role in allowed_roles if role}

    def dependency(current_user=Depends(get_current_active_user)):
        user_role = getattr(getattr(current_user, "role", None), "name", None)
        normalized_role = (user_role or "").strip().lower()

        if normalized_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return current_user

    return dependency


def require_admin(current_user=Depends(get_current_active_user)):
    return require_roles("admin")(current_user)


def require_staff(current_user=Depends(get_current_active_user)):
    return require_roles("admin", "provider", "care_coordinator")(current_user)
```

---

## File 3 — `app/modules/auth/tokens.py`

```python
from __future__ import annotations

from typing import Dict

from app.common.utils.security import decode_token, issue_token_pair, validate_token_type


def build_token_response(user_id: str, email: str, role: str) -> Dict[str, str]:
    return issue_token_pair(user_id=str(user_id), email=email, role=role)


def decode_access_token(token: str) -> dict:
    payload = decode_token(token)
    validate_token_type(payload, "access")
    return payload


def decode_refresh_token(token: str) -> dict:
    payload = decode_token(token)
    validate_token_type(payload, "refresh")
    return payload
```

---

## File 4 — `app/modules/auth/dependencies.py`

```python
from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.repository import AuthRepository
from app.modules.auth.tokens import decode_access_token


bearer_scheme = HTTPBearer(auto_error=False)


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
        )
    return credentials.credentials


def get_current_user(
    token: str = Depends(get_bearer_token),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject is missing.",
        )

    repository = AuthRepository(db)
    user = repository.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with token was not found.",
        )

    return user


def get_current_active_user(current_user=Depends(get_current_user)):
    if not getattr(current_user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive.",
        )
    return current_user
```

---

## File 5 — `app/modules/auth/repository.py`

```python
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models.role import Role
from app.db.models.user import User


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .where(User.email == email.strip().lower())
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_user_by_id(self, user_id: str | int) -> Optional[User]:
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .where(User.id == user_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_role_by_name(self, role_name: str) -> Optional[Role]:
        stmt = select(Role).where(Role.name == role_name.strip().lower())
        return self.db.execute(stmt).scalar_one_or_none()

    def create_user(
        self,
        *,
        email: str,
        full_name: str,
        password_hash: str,
        role_id,
        phone_number: str | None = None,
        is_active: bool = True,
    ) -> User:
        user = User(
            email=email.strip().lower(),
            full_name=full_name.strip(),
            password_hash=password_hash,
            role_id=role_id,
            phone_number=phone_number,
            is_active=is_active,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self.get_user_by_id(user.id)

    def update_last_login(self, user: User) -> User:
        if hasattr(user, "last_login_at"):
            user.last_login_at = datetime.now(timezone.utc)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user
```

---

## File 6 — `app/modules/auth/schemas.py`

```python
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=120)
    phone_number: Optional[str] = Field(default=None, max_length=30)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()
        if len(value.split()) < 2:
            raise ValueError("Full name must include at least two names.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        has_upper = any(char.isupper() for char in value)
        has_lower = any(char.islower() for char in value)
        has_digit = any(char.isdigit() for char in value)
        if not (has_upper and has_lower and has_digit):
            raise ValueError(
                "Password must include at least one uppercase letter, one lowercase letter, and one digit."
            )
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=20)


class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = None


class AuthUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | int
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    is_active: bool
    role: str


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    user: AuthUserResponse
    tokens: TokenPairResponse


class MessageResponse(BaseModel):
    message: str


class CurrentUserResponse(BaseModel):
    user: AuthUserResponse
```

---

## File 7 — `app/modules/auth/service.py`

```python
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.common.utils.security import hash_password, verify_password
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import RegisterRequest
from app.modules.auth.tokens import build_token_response, decode_refresh_token


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = AuthRepository(db)

    @staticmethod
    def _serialize_user(user):
        role_name = getattr(getattr(user, "role", None), "name", None)
        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "phone_number": getattr(user, "phone_number", None),
            "is_active": user.is_active,
            "role": role_name or "unknown",
        }

    def register_patient(self, payload: RegisterRequest) -> dict:
        existing_user = self.repository.get_user_by_email(payload.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with that email already exists.",
            )

        patient_role = self.repository.get_role_by_name("patient")
        if patient_role is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Default patient role is missing. Seed roles first.",
            )

        user = self.repository.create_user(
            email=payload.email,
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
            role_id=patient_role.id,
            phone_number=payload.phone_number,
            is_active=True,
        )

        tokens = build_token_response(
            user_id=str(user.id),
            email=user.email,
            role=getattr(user.role, "name", "patient"),
        )

        return {
            "user": self._serialize_user(user),
            "tokens": tokens,
        }

    def login(self, email: str, password: str) -> dict:
        user = self.repository.get_user_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is inactive.",
            )

        user = self.repository.update_last_login(user)
        role_name = getattr(getattr(user, "role", None), "name", "unknown")

        tokens = build_token_response(
            user_id=str(user.id),
            email=user.email,
            role=role_name,
        )

        return {
            "user": self._serialize_user(user),
            "tokens": tokens,
        }

    def refresh_access_token(self, refresh_token: str) -> dict:
        try:
            payload = decode_refresh_token(refresh_token)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token subject is missing.",
            )

        user = self.repository.get_user_by_id(user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User for refresh token is invalid.",
            )

        role_name = getattr(getattr(user, "role", None), "name", "unknown")
        tokens = build_token_response(
            user_id=str(user.id),
            email=user.email,
            role=role_name,
        )
        return {
            "user": self._serialize_user(user),
            "tokens": tokens,
        }

    def logout(self) -> dict:
        return {"message": "Logout successful."}

    def current_user(self, user) -> dict:
        return {"user": self._serialize_user(user)}
```

---

## File 8 — `app/modules/auth/router.py`

```python
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.auth.schemas import (
    AuthResponse,
    CurrentUserResponse,
    LoginRequest,
    LogoutRequest,
    MessageResponse,
    RefreshTokenRequest,
    RegisterRequest,
)
from app.modules.auth.service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register_patient(payload)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(email=payload.email, password=payload.password)


@router.post("/refresh", response_model=AuthResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.refresh_access_token(payload.refresh_token)


@router.post("/logout", response_model=MessageResponse)
def logout(
    payload: LogoutRequest,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.logout()


@router.get("/me", response_model=CurrentUserResponse)
def get_current_user_profile(current_user=Depends(get_current_active_user)):
    return AuthService.current_user(AuthService, current_user)
```

---

## File 9 — `app/modules/users/dependencies.py`

```python
from __future__ import annotations

from fastapi import Depends

from app.common.permissions.dependencies import require_admin
from app.modules.auth.dependencies import get_current_active_user


def get_authenticated_user(current_user=Depends(get_current_active_user)):
    return current_user


def get_admin_user(current_user=Depends(require_admin)):
    return current_user
```

---

## File 10 — `app/modules/users/repository.py`

```python
from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models.role import Role
from app.db.models.user import User


class UsersRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_id(self, user_id: str | int) -> Optional[User]:
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .where(User.id == user_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .where(User.email == email.strip().lower())
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_users(self, *, offset: int = 0, limit: int = 20):
        stmt = (
            select(User)
            .options(joinedload(User.role))
            .offset(offset)
            .limit(limit)
            .order_by(User.id)
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_role_by_name(self, role_name: str) -> Optional[Role]:
        stmt = select(Role).where(Role.name == role_name.strip().lower())
        return self.db.execute(stmt).scalar_one_or_none()

    def update_profile(
        self,
        user: User,
        *,
        full_name: str | None = None,
        phone_number: str | None = None,
    ) -> User:
        if full_name is not None:
            user.full_name = full_name.strip()
        if phone_number is not None:
            user.phone_number = phone_number.strip() or None

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self.get_user_by_id(user.id)

    def update_role(self, user: User, role: Role) -> User:
        user.role_id = role.id
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self.get_user_by_id(user.id)

    def update_active_status(self, user: User, is_active: bool) -> User:
        user.is_active = is_active
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self.get_user_by_id(user.id)
```

---

## File 11 — `app/modules/users/schemas.py`

```python
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | int
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    is_active: bool
    role: str


class UserProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    phone_number: Optional[str] = Field(default=None, max_length=30)

    @field_validator("full_name")
    @classmethod
    def normalize_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if len(value.split()) < 2:
            raise ValueError("Full name must include at least two names.")
        return value


class UserListResponse(BaseModel):
    users: list[UserProfileResponse]
    total: int
    offset: int
    limit: int


class RoleUpdateRequest(BaseModel):
    role_name: str = Field(min_length=3, max_length=50)


class StatusUpdateRequest(BaseModel):
    is_active: bool
```

---

## File 12 — `app/modules/users/service.py`

```python
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.users.repository import UsersRepository
from app.modules.users.schemas import UserProfileUpdateRequest


class UsersService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = UsersRepository(db)

    @staticmethod
    def _serialize_user(user) -> dict:
        role_name = getattr(getattr(user, "role", None), "name", None)
        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "phone_number": getattr(user, "phone_number", None),
            "is_active": user.is_active,
            "role": role_name or "unknown",
        }

    def get_me(self, current_user) -> dict:
        return self._serialize_user(current_user)

    def update_me(self, current_user, payload: UserProfileUpdateRequest) -> dict:
        user = self.repository.update_profile(
            current_user,
            full_name=payload.full_name,
            phone_number=payload.phone_number,
        )
        return self._serialize_user(user)

    def list_users(self, *, offset: int = 0, limit: int = 20) -> dict:
        users = self.repository.list_users(offset=offset, limit=limit)
        return {
            "users": [self._serialize_user(user) for user in users],
            "total": len(users),
            "offset": offset,
            "limit": limit,
        }

    def get_user(self, user_id: str | int) -> dict:
        user = self.repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return self._serialize_user(user)

    def update_user_role(self, user_id: str | int, role_name: str) -> dict:
        user = self.repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        role = self.repository.get_role_by_name(role_name)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found.",
            )

        updated_user = self.repository.update_role(user, role)
        return self._serialize_user(updated_user)

    def update_user_status(self, user_id: str | int, is_active: bool) -> dict:
        user = self.repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        updated_user = self.repository.update_active_status(user, is_active)
        return self._serialize_user(updated_user)
```

---

## File 13 — `app/modules/users/router.py`

```python
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.users.dependencies import get_admin_user, get_authenticated_user
from app.modules.users.schemas import (
    RoleUpdateRequest,
    StatusUpdateRequest,
    UserListResponse,
    UserProfileResponse,
    UserProfileUpdateRequest,
)
from app.modules.users.service import UsersService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    current_user=Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    service = UsersService(db)
    return service.get_me(current_user)


@router.patch("/me", response_model=UserProfileResponse)
def update_my_profile(
    payload: UserProfileUpdateRequest,
    current_user=Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    service = UsersService(db)
    return service.update_me(current_user, payload)


@router.get("", response_model=UserListResponse)
def list_users(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    admin_user=Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    service = UsersService(db)
    return service.list_users(offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user(
    user_id: str,
    admin_user=Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    service = UsersService(db)
    return service.get_user(user_id)


@router.patch("/{user_id}/role", response_model=UserProfileResponse)
def update_user_role(
    user_id: str,
    payload: RoleUpdateRequest,
    admin_user=Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    service = UsersService(db)
    return service.update_user_role(user_id=user_id, role_name=payload.role_name)


@router.patch("/{user_id}/status", response_model=UserProfileResponse)
def update_user_status(
    user_id: str,
    payload: StatusUpdateRequest,
    admin_user=Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    service = UsersService(db)
    return service.update_user_status(user_id=user_id, is_active=payload.is_active)
```

---

## File 14 — `tests/modules/auth/test_register.py`

```python
from __future__ import annotations


def test_patient_registration_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "patient.phase3@example.com",
            "password": "StrongPass123",
            "full_name": "Patient Example",
            "phone_number": "+256700000001",
        },
    )

    assert response.status_code == 201, response.text
    body = response.json()

    assert body["user"]["email"] == "patient.phase3@example.com"
    assert body["user"]["role"] == "patient"
    assert "access_token" in body["tokens"]
    assert "refresh_token" in body["tokens"]


def test_registration_rejects_duplicate_email(client):
    payload = {
        "email": "duplicate.phase3@example.com",
        "password": "StrongPass123",
        "full_name": "Duplicate Patient",
    }

    first = client.post("/api/v1/auth/register", json=payload)
    second = client.post("/api/v1/auth/register", json=payload)

    assert first.status_code == 201, first.text
    assert second.status_code == 409, second.text
    assert second.json()["detail"] == "An account with that email already exists."
```

---

## File 15 — `tests/modules/auth/test_login.py`

```python
from __future__ import annotations


def register_default_user(client, email="login.phase3@example.com", password="StrongPass123"):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Login Phase User",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_login_success(client):
    email = "success.phase3@example.com"
    password = "StrongPass123"
    register_default_user(client, email=email, password=password)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["user"]["email"] == email
    assert "access_token" in body["tokens"]
    assert body["tokens"]["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    email = "wrongpass.phase3@example.com"
    register_default_user(client, email=email, password="StrongPass123")

    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "WrongPass123"},
    )

    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Invalid email or password."
```

---

## File 16 — `tests/modules/auth/test_refresh_token.py`

```python
from __future__ import annotations


def register_and_login(client, email="refresh.phase3@example.com", password="StrongPass123"):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Refresh Token User",
        },
    )
    assert register_response.status_code == 201, register_response.text
    return register_response.json()


def test_refresh_token_success(client):
    auth_payload = register_and_login(client)
    refresh_token = auth_payload["tokens"]["refresh_token"]

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert "access_token" in body["tokens"]
    assert "refresh_token" in body["tokens"]
    assert body["tokens"]["token_type"] == "bearer"


def test_refresh_token_rejects_invalid_token(client):
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "this.is.not.valid"},
    )

    assert response.status_code == 401, response.text
```

---

## File 17 — `tests/modules/auth/test_role_access.py`

```python
from __future__ import annotations

from sqlalchemy import select

from app.common.utils.security import hash_password
from app.db.models.role import Role
from app.db.models.user import User


def ensure_role(db_session, role_name: str):
    role = db_session.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
    if role is None:
        role = Role(name=role_name)
        db_session.add(role)
        db_session.commit()
        db_session.refresh(role)
    return role


def create_admin_user(db_session):
    admin_role = ensure_role(db_session, "admin")
    existing = db_session.execute(
        select(User).where(User.email == "admin.phase3@example.com")
    ).scalar_one_or_none()

    if existing is not None:
        return existing

    user = User(
        email="admin.phase3@example.com",
        full_name="Admin Phase Three",
        password_hash=hash_password("AdminPass123"),
        role_id=admin_role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def login(client, email: str, password: str):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )


def test_non_admin_cannot_access_admin_users_list(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "patient.forbidden@example.com",
            "password": "StrongPass123",
            "full_name": "Forbidden Patient",
        },
    )
    assert register_response.status_code == 201, register_response.text

    access_token = register_response.json()["tokens"]["access_token"]

    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403, response.text


def test_admin_can_access_users_list(client, db_session):
    create_admin_user(db_session)

    login_response = login(client, "admin.phase3@example.com", "AdminPass123")
    assert login_response.status_code == 200, login_response.text

    access_token = login_response.json()["tokens"]["access_token"]
    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200, response.text
    assert "users" in response.json()


def test_missing_token_is_unauthorized(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401, response.text
```

---

## File 18 — `tests/modules/users/test_user_profile.py`

```python
from __future__ import annotations


def register_user(client, email="profile.phase3@example.com", password="StrongPass123"):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Profile Phase User",
            "phone_number": "+256700111222",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_current_user_endpoint(client):
    auth_payload = register_user(client, email="me.phase3@example.com")
    access_token = auth_payload["tokens"]["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200, response.text
    assert response.json()["user"]["email"] == "me.phase3@example.com"


def test_get_my_profile_endpoint(client):
    auth_payload = register_user(client, email="profile.self@example.com")
    access_token = auth_payload["tokens"]["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200, response.text
    assert response.json()["email"] == "profile.self@example.com"


def test_update_my_profile_endpoint(client):
    auth_payload = register_user(client, email="profile.update@example.com")
    access_token = auth_payload["tokens"]["access_token"]

    response = client.patch(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "full_name": "Updated Profile User",
            "phone_number": "+256700999888",
        },
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["full_name"] == "Updated Profile User"
    assert body["phone_number"] == "+256700999888"
```

---

## Main integration reminder

Your `app/main.py` from Phase 1 must include the auth and users routers under the API prefix. Make sure the application registers them, for example:

```python
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
```

If your project already uses a central router registry, keep that pattern and just ensure both module routers are wired in.

---

## Commands to run after pasting Phase 3

### 1. Install missing dependencies if absent
```bash
pip install "python-jose[cryptography]" "passlib[bcrypt]" email-validator
```

### 2. Run targeted auth and users tests
```bash
pytest \
  tests/modules/auth/test_register.py \
  tests/modules/auth/test_login.py \
  tests/modules/auth/test_refresh_token.py \
  tests/modules/auth/test_role_access.py \
  tests/modules/users/test_user_profile.py -q
```

### 3. Run the broader backend suite
```bash
pytest -q
```

### 4. Manual smoke-check endpoints
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "manual.patient@example.com",
    "password": "StrongPass123",
    "full_name": "Manual Patient"
  }'

curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "manual.patient@example.com",
    "password": "StrongPass123"
  }'
```

---

## Expected completion checkpoint for Phase 3

This phase is complete when all of the following are true:

- patient registration works
- login works
- password hashing and verification work
- refresh token flow works
- unauthorized requests are rejected
- role-restricted routes enforce admin access correctly
- current-user endpoint works
- user self-profile view and update work
- auth logic is stable enough for all future feature modules

---

## Implementation caution

Because I cannot inspect your exact local Phase 2 model definitions from your machine, you must verify these assumptions before pasting:

- `User.role` relationship exists
- `Role.name` exists and stores normalized values like `patient`, `provider`, `care_coordinator`, `admin`
- `User.password_hash` is the stored credential field
- `get_db()` already yields a SQLAlchemy session
- route prefixing remains consistent with `/api/v1`

If your actual model field names differ, align the repository and serializer field references before running tests.
