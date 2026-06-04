
# PBBF BLISS — Stage 3 Auth, Registration, and Session Governance Implementation Pack

**Stage:** 3 — Auth, Registration, and Session Governance  
**Execution style:** Independent commands/snippets only. Run one command at a time.  
**Repository root:** `/home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth`

---

## Objective

Make authentication behavior consistent, secure, and aligned with the MVP role model.

The inspected backend already keeps public registration patient-only through `AuthService.register_patient`, but logout currently returns success without revoking refresh/session state, and no `auth_session` model or auth session repository exists. The inspected frontend still has a public role selector and sends `role` during registration, while backend registration ignores privileged role creation. citeturn27search1

---

## Stage 3 Contract Decisions

```text
1. Public registration remains patient-only.
2. Public RegisterForm must not show role selector.
3. Public RegisterForm must not send role.
4. Admin-only internal user provisioning is created under /users.
5. lactation_consultant redirects to provider workspace.
6. Frontend password validation matches backend: 8-128 chars, uppercase, lowercase, digit.
7. Refresh tokens are stored as server-side auth_sessions.
8. Refresh rotates the refresh session.
9. Logout revokes the refresh session when refresh_token is supplied.
```

---

# 1. Prepare Backup Directory

## Command 1.1

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
export STAGE3_BACKUP_DIR="backups/stage3_auth_session_governance_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$STAGE3_BACKUP_DIR"
echo "$STAGE3_BACKUP_DIR"
```

---

# 2. Backend Auth Session Model

## Files created/updated

```text
pbbf-api/app/db/models/auth_session.py
pbbf-api/app/db/models/__init__.py
pbbf-api/alembic/versions/f20260604_stage3_add_auth_sessions.py
```

## Command 2.1 — Create auth_session model

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/app/db/models/auth_session.py <<'PY'
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.user import User


class AuthSession(Base, TimestampMixin):
    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    refresh_token_jti: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    refresh_token_hash: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    revoked_reason: Mapped[str | None] = mapped_column(String(120), nullable=True)

    user: Mapped["User"] = relationship("User")

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None
PY
```

## Command 2.2 — Register model in models init

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-api/app/db/models"
cp pbbf-api/app/db/models/__init__.py "$STAGE3_BACKUP_DIR/pbbf-api/app/db/models/__init__.py"
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/db/models/__init__.py')
text = path.read_text()
if '"auth_session"' not in text:
    text = text.replace('    "audit_log",', '    "audit_log",\n    "auth_session",')
if 'from app.db.models.auth_session import AuthSession' not in text:
    text = text.replace('from app.db.models.audit_log import AuditLog\n', 'from app.db.models.audit_log import AuditLog\nfrom app.db.models.auth_session import AuthSession\n')
if '"AuthSession": AuthSession,' not in text:
    text = text.replace('    "AuditLog": AuditLog,', '    "AuditLog": AuditLog,\n    "AuthSession": AuthSession,')
if '    "AuthSession",' not in text:
    text = text.replace('    "AuditLog",', '    "AuditLog",\n    "AuthSession",')
path.write_text(text)
PY
```

## Command 2.3 — Create Alembic migration

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/alembic/versions/f20260604_stage3_add_auth_sessions.py <<'PY'
from alembic import op
import sqlalchemy as sa

revision = "f20260604_stage3"
down_revision = "c93a7f6d0b21"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("refresh_token_jti", sa.String(length=120), nullable=False),
        sa.Column("refresh_token_hash", sa.Text(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_reason", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"])
    op.create_index("ix_auth_sessions_refresh_token_jti", "auth_sessions", ["refresh_token_jti"], unique=True)
    op.create_index("ix_auth_sessions_expires_at", "auth_sessions", ["expires_at"])
    op.create_index("ix_auth_sessions_revoked_at", "auth_sessions", ["revoked_at"])


def downgrade() -> None:
    op.drop_index("ix_auth_sessions_revoked_at", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_expires_at", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_refresh_token_jti", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_user_id", table_name="auth_sessions")
    op.drop_table("auth_sessions")
PY
```

---

# 3. Backend Auth Session Repository

## File created

```text
pbbf-api/app/modules/auth/session_repository.py
```

## Command 3.1

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/app/modules/auth/session_repository.py <<'PY'
from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.auth_session import AuthSession


def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


class AuthSessionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_session(self, *, user_id: int, refresh_token: str, refresh_token_jti: str, expires_at: datetime) -> AuthSession:
        session = AuthSession(
            user_id=user_id,
            refresh_token_jti=refresh_token_jti,
            refresh_token_hash=hash_refresh_token(refresh_token),
            expires_at=expires_at,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_active_session(self, *, refresh_token: str, refresh_token_jti: str) -> AuthSession | None:
        stmt = select(AuthSession).where(AuthSession.refresh_token_jti == refresh_token_jti)
        session = self.db.execute(stmt).scalar_one_or_none()
        if session is None or session.revoked_at is not None:
            return None
        if session.refresh_token_hash != hash_refresh_token(refresh_token):
            return None
        expires_at = session.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at <= datetime.now(timezone.utc):
            return None
        return session

    def revoke_session(self, session: AuthSession, *, reason: str = "revoked") -> AuthSession:
        if session.revoked_at is None:
            session.revoked_at = datetime.now(timezone.utc)
            session.revoked_reason = reason
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
        return session

    def revoke_by_refresh_token(self, *, refresh_token: str, refresh_token_jti: str, reason: str = "logout") -> bool:
        session = self.get_active_session(refresh_token=refresh_token, refresh_token_jti=refresh_token_jti)
        if session is None:
            return False
        self.revoke_session(session, reason=reason)
        return True
PY
```

---

# 4. Backend Auth Service Session Governance

## File updated

```text
pbbf-api/app/modules/auth/service.py
```

## Command 4.1 — Backup auth service

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/auth"
cp pbbf-api/app/modules/auth/service.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/auth/service.py"
```

## Command 4.2 — Replace auth service

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/app/modules/auth/service.py <<'PY'
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.common.utils.security import hash_password, verify_password
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import RegisterRequest
from app.modules.auth.session_repository import AuthSessionRepository
from app.modules.auth.tokens import build_token_response, decode_refresh_token


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = AuthRepository(db)
        self.sessions = AuthSessionRepository(db)

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

    def _build_and_store_tokens(self, user) -> dict:
        role_name = getattr(getattr(user, "role", None), "name", "unknown")
        tokens = build_token_response(user_id=str(user.id), email=user.email, role=role_name)
        refresh_payload = decode_refresh_token(tokens["refresh_token"])
        refresh_jti = refresh_payload.get("jti")
        refresh_exp = refresh_payload.get("exp")
        if not refresh_jti or not refresh_exp:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Refresh token metadata is missing.")
        self.sessions.create_session(
            user_id=user.id,
            refresh_token=tokens["refresh_token"],
            refresh_token_jti=refresh_jti,
            expires_at=datetime.fromtimestamp(int(refresh_exp), tz=timezone.utc),
        )
        return tokens

    def register_patient(self, payload: RegisterRequest) -> dict:
        existing_user = self.repository.get_user_by_email(payload.email)
        if existing_user is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with that email already exists.")
        patient_role = self.repository.get_role_by_name("patient")
        if patient_role is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Default patient role is missing. Seed roles first.")
        user = self.repository.create_user(
            email=payload.email,
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
            role_id=patient_role.id,
            phone_number=payload.phone_number,
            is_active=True,
        )
        return {"user": self._serialize_user(user), "tokens": self._build_and_store_tokens(user)}

    def login(self, email: str, password: str) -> dict:
        user = self.repository.get_user_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This account is inactive.")
        user = self.repository.update_last_login(user)
        return {"user": self._serialize_user(user), "tokens": self._build_and_store_tokens(user)}

    def refresh_access_token(self, refresh_token: str) -> dict:
        try:
            payload = decode_refresh_token(refresh_token)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
        user_id = payload.get("sub")
        refresh_jti = payload.get("jti")
        if not user_id or not refresh_jti:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token metadata is missing.")
        session = self.sessions.get_active_session(refresh_token=refresh_token, refresh_token_jti=refresh_jti)
        if session is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh session is invalid or has been revoked.")
        user = self.repository.get_user_by_id(user_id)
        if user is None or not user.is_active:
            self.sessions.revoke_session(session, reason="invalid_user")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User for refresh token is invalid.")
        self.sessions.revoke_session(session, reason="rotated")
        return {"user": self._serialize_user(user), "tokens": self._build_and_store_tokens(user)}

    def logout(self, refresh_token: str | None = None) -> dict:
        if refresh_token:
            try:
                payload = decode_refresh_token(refresh_token)
                refresh_jti = payload.get("jti")
                if refresh_jti:
                    self.sessions.revoke_by_refresh_token(refresh_token=refresh_token, refresh_token_jti=refresh_jti, reason="logout")
            except ValueError:
                pass
        return {"message": "Logout successful."}

    def current_user(self, user) -> dict:
        return {"user": self._serialize_user(user)}
PY
```

---

# 5. Backend Auth Router Fixes

## File updated

```text
pbbf-api/app/modules/auth/router.py
```

## Command 5.1

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/auth"
cp pbbf-api/app/modules/auth/router.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/auth/router.py"
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/auth/router.py')
text = path.read_text()
text = text.replace('return service.logout()', 'return service.logout(refresh_token=payload.refresh_token)')
text = text.replace('return AuthService.current_user(AuthService, current_user)', 'return AuthService(db).current_user(current_user)')
path.write_text(text)
PY
```

---

# 6. Backend Admin-Only Internal User Provisioning

## Files updated

```text
pbbf-api/app/modules/users/schemas.py
pbbf-api/app/modules/users/repository.py
pbbf-api/app/modules/users/service.py
pbbf-api/app/modules/users/router.py
```

## Command 6.1 — Backup users files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users"
cp pbbf-api/app/modules/users/schemas.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users/schemas.py"
cp pbbf-api/app/modules/users/repository.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users/repository.py"
cp pbbf-api/app/modules/users/service.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users/service.py"
cp pbbf-api/app/modules/users/router.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users/router.py"
```

## Command 6.2 — Add admin create schema

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat >> pbbf-api/app/modules/users/schemas.py <<'PY'

class AdminCreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=120)
    phone_number: Optional[str] = Field(default=None, max_length=30)
    role_name: str = Field(min_length=3, max_length=50)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        has_upper = any(char.isupper() for char in value)
        has_lower = any(char.islower() for char in value)
        has_digit = any(char.isdigit() for char in value)
        if not (has_upper and has_lower and has_digit):
            raise ValueError("Password must include at least one uppercase letter, one lowercase letter, and one digit.")
        return value
PY
```

## Command 6.3 — Add repository create_user method

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/users/repository.py')
text = path.read_text()
if 'def create_user(' not in text:
    insert = '''
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
'''
    text = text.replace('    def update_profile(', insert + '\n    def update_profile(')
path.write_text(text)
PY
```

## Command 6.4 — Add service create_user_by_admin method

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/users/service.py')
text = path.read_text()
if 'from app.common.utils.security import hash_password' not in text:
    text = text.replace('from fastapi import HTTPException, status\n', 'from fastapi import HTTPException, status\nfrom app.common.utils.security import hash_password\n')
if 'def create_user_by_admin(' not in text:
    method = '''
    def create_user_by_admin(self, payload) -> dict:
        if payload.role_name.strip().lower() == "patient":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Use public registration or patient onboarding flow for patient accounts.")
        existing = self.repository.get_user_by_email(payload.email)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with that email already exists.")
        role = self.repository.get_role_by_name(payload.role_name)
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found.")
        user = self.repository.create_user(
            email=payload.email,
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
            role_id=role.id,
            phone_number=payload.phone_number,
            is_active=True,
        )
        return self._serialize_user(user)
'''
    text = text.replace('    def get_me(self, current_user) -> dict:', method + '\n    def get_me(self, current_user) -> dict:')
path.write_text(text)
PY
```

## Command 6.5 — Add admin-only create user route

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/users/router.py')
text = path.read_text()
if 'AdminCreateUserRequest' not in text:
    text = text.replace('RoleUpdateRequest,', 'AdminCreateUserRequest,\n    RoleUpdateRequest,')
if 'def create_user(' not in text:
    route = '''
@router.post("", response_model=UserProfileResponse, status_code=201)
def create_user(
    payload: AdminCreateUserRequest,
    admin_user=Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    service = UsersService(db)
    return service.create_user_by_admin(payload)

'''
    text = text.replace('@router.get("", response_model=UserListResponse)', route + '@router.get("", response_model=UserListResponse)')
path.write_text(text)
PY
```

---

# 7. Frontend Public Registration Cleanup

## File updated

```text
pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx
```

## Command 7.1 — Remove public role selector and role payload

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/components"
cp pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx"
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx')
text = path.read_text()
text = text.replace('    role: "patient",\n', '')
text = text.replace('        role: values.role,\n', '')
text = text.replace('    case "care_coordinator":\n      return "/provider";', '    case "care_coordinator":\n    case "lactation_consultant":\n      return "/provider";')
start = text.find('      <div>\n        <label htmlFor="register-role"')
if start != -1:
    end_marker = '      {serverError ? ('
    end = text.find(end_marker, start)
    if end != -1:
        text = text[:start] + text[end:]
path.write_text(text)
PY
```

## Command 7.2 — Add lactation_consultant login redirect

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cp pbbf-telehealth/src/modules/auth/components/LoginForm.jsx "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/components/LoginForm.jsx"
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/auth/components/LoginForm.jsx')
text = path.read_text()
text = text.replace('    case "care_coordinator":\n      return ROUTES.provider.dashboard;', '    case "care_coordinator":\n    case "lactation_consultant":\n      return ROUTES.provider.dashboard;')
path.write_text(text)
PY
```

---

# 8. Frontend Password Validation Parity

## File updated

```text
pbbf-telehealth/src/modules/auth/utils/validators.js
```

## Command 8.1

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/utils"
cp pbbf-telehealth/src/modules/auth/utils/validators.js "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/utils/validators.js"
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/auth/utils/validators.js')
text = path.read_text()
old = '''export function validatePassword(value) {
  if (!value) return "Password is required.";
  if (value.length < 8) return "Password must be at least 8 characters.";
  return "";
}
'''
new = '''export function validatePassword(value) {
  if (!value) return "Password is required.";
  if (value.length < 8) return "Password must be at least 8 characters.";
  if (value.length > 128) return "Password must be 128 characters or fewer.";
  if (!/[A-Z]/.test(value)) return "Password must include at least one uppercase letter.";
  if (!/[a-z]/.test(value)) return "Password must include at least one lowercase letter.";
  if (!/[0-9]/.test(value)) return "Password must include at least one digit.";
  return "";
}
'''
text = text.replace(old, new)
path.write_text(text)
PY
```

---

# 9. Frontend Refresh/Logout API and Service

## Files updated

```text
pbbf-telehealth/src/modules/auth/services/authApi.js
pbbf-telehealth/src/services/auth.service.js
pbbf-telehealth/src/modules/auth/hooks/useAuth.js
```

## Command 9.1 — Replace auth API

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/services"
cp pbbf-telehealth/src/modules/auth/services/authApi.js "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/services/authApi.js"
cat > pbbf-telehealth/src/modules/auth/services/authApi.js <<'EOF'
import { api } from "../../../services/api";

export function loginRequest(payload) {
  return api.post("/auth/login", payload);
}

export function registerRequest(payload) {
  return api.post("/auth/register", payload);
}

export function refreshTokenRequest(payload) {
  return api.post("/auth/refresh", payload);
}

export function logoutRequest(payload = {}) {
  return api.post("/auth/logout", payload);
}

export function getCurrentUserRequest() {
  return api.get("/auth/me");
}

export function forgotPasswordRequest(payload) {
  return api.post("/auth/forgot-password", payload);
}
EOF
```

## Command 9.2 — Patch auth service refresh/logout behavior

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/services"
cp pbbf-telehealth/src/services/auth.service.js "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/services/auth.service.js"
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/services/auth.service.js')
text = path.read_text()
if 'refreshTokenRequest' not in text:
    text = text.replace('logoutRequest,\n  registerRequest,', 'logoutRequest,\n  refreshTokenRequest,\n  registerRequest,')
text = text.replace('await logoutRequest();', 'await logoutRequest({ refresh_token: getState().refreshToken });')
if 'async function refreshAccessToken()' not in text:
    insert = '''
async function refreshAccessToken() {
  const refreshToken = getState().refreshToken;
  if (!refreshToken) {
    markSessionExpired("missing_refresh_token");
    return getState();
  }
  try {
    const response = await refreshTokenRequest({ refresh_token: refreshToken });
    const normalized = normalizeAuthResponse(response);
    if (!normalized.accessToken || !normalized.user) {
      throw new ApiError("Refresh response is missing token or user data.", 500, response);
    }
    loginSuccess(normalized);
    return getState();
  } catch {
    markSessionExpired("refresh_failed");
    return getState();
  }
}
'''
    text = text.replace('async function logout() {', insert + '\nasync function logout() {')
text = text.replace('hydrate,\n  logout,', 'hydrate,\n  refreshAccessToken,\n  logout,')
path.write_text(text)
PY
```

## Command 9.3 — Expose refreshAccessToken from useAuth

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/hooks"
cp pbbf-telehealth/src/modules/auth/hooks/useAuth.js "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/hooks/useAuth.js"
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/auth/hooks/useAuth.js')
text = path.read_text()
if 'refreshAccessToken' not in text:
    text = text.replace('logout: authService.logout,', 'refreshAccessToken: authService.refreshAccessToken,\n      logout: authService.logout,')
path.write_text(text)
PY
```

---

# 10. Backend Tests

## Command 10.1 — Replace refresh token tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/tests/modules/auth/test_refresh_token.py <<'PY'
from __future__ import annotations


def register_user(client, email="refresh.stage3@example.com", password="StrongPass123"):
    response = client.post("/api/v1/auth/register", json={"email": email, "password": password, "full_name": "Refresh Stage"})
    assert response.status_code == 201, response.text
    return response.json()


def test_refresh_token_rotates_session(client):
    auth_payload = register_user(client)
    old_refresh = auth_payload["tokens"]["refresh_token"]
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": old_refresh})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["tokens"]["refresh_token"] != old_refresh
    reused = client.post("/api/v1/auth/refresh", json={"refresh_token": old_refresh})
    assert reused.status_code == 401, reused.text
PY
```

## Command 10.2 — Create logout revocation test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/tests/modules/auth/test_logout_revokes_session.py <<'PY'
from __future__ import annotations


def test_logout_revokes_refresh_session(client):
    register = client.post("/api/v1/auth/register", json={"email": "logout.stage3@example.com", "password": "StrongPass123", "full_name": "Logout Stage"})
    assert register.status_code == 201, register.text
    tokens = register.json()["tokens"]
    logout = client.post("/api/v1/auth/logout", json={"refresh_token": tokens["refresh_token"]}, headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert logout.status_code == 200, logout.text
    refresh = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refresh.status_code == 401, refresh.text
PY
```

## Command 10.3 — Append public role injection test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat >> pbbf-api/tests/modules/auth/test_register.py <<'PY'


def test_public_registration_remains_patient_even_if_role_is_supplied(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "role.inject.stage3@example.com", "password": "StrongPass123", "full_name": "Role Injection", "role": "admin"},
    )
    assert response.status_code == 201, response.text
    assert response.json()["user"]["role"] == "patient"
PY
```

---

# 11. Frontend Test

## File created

```text
pbbf-telehealth/src/modules/auth/__tests__/SessionRefresh.test.jsx
```

## Command 11.1

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p pbbf-telehealth/src/modules/auth/__tests__
cat > pbbf-telehealth/src/modules/auth/__tests__/SessionRefresh.test.jsx <<'JS'
import { describe, expect, it } from "vitest";
import { validatePassword } from "../utils/validators";

describe("Stage 3 auth governance", () => {
  it("matches backend password strength rules", () => {
    expect(validatePassword("weakpass")).toMatch(/uppercase/i);
    expect(validatePassword("WEAKPASS1")).toMatch(/lowercase/i);
    expect(validatePassword("Weakpass")).toMatch(/digit/i);
    expect(validatePassword("StrongPass123")).toBe("");
  });
});
JS
```

---

# 12. Validation Commands

Run independently.

## Command 12.1 — Backend compile

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
python -m py_compile app/db/models/auth_session.py app/modules/auth/session_repository.py app/modules/auth/service.py app/modules/auth/router.py app/modules/users/schemas.py app/modules/users/repository.py app/modules/users/service.py app/modules/users/router.py
```

## Command 12.2 — Auth register/login tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/auth/test_register.py tests/modules/auth/test_login.py -q
```

## Command 12.3 — Refresh/logout tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/auth/test_refresh_token.py tests/modules/auth/test_logout_revokes_session.py -q
```

## Command 12.4 — User profile tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/users/test_user_profile.py -q
```

## Command 12.5 — Frontend build

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm run build
```

## Command 12.6 — Frontend auth test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm test -- --run src/modules/auth/__tests__/SessionRefresh.test.jsx
```

---

# 13. Post-Apply Inspection Commands

## Command 13.1 — Confirm RegisterForm has no public role selector

```bash
grep -n "register-role\|role:" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx || true
```

## Command 13.2 — Confirm backend session files exist

```bash
ls -la /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/db/models/auth_session.py
ls -la /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/auth/session_repository.py
```

## Command 13.3 — Confirm frontend logout/refresh support

```bash
grep -n "refresh_token\|refreshAccessToken\|logoutRequest" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/services/auth.service.js
```

---

# 14. Completion Checklist

```text
[ ] Public /auth/register creates patient role only.
[ ] Frontend RegisterForm has no role selector.
[ ] Frontend RegisterForm does not send role.
[ ] Login/Register redirect mapping includes lactation_consultant.
[ ] Frontend password validation matches backend rules.
[ ] auth_sessions model exists.
[ ] AuthSessionRepository exists.
[ ] Refresh token creates server-side session.
[ ] Refresh token rotation revokes old session.
[ ] Logout revokes refresh session when refresh_token is supplied.
[ ] Admin-only user provisioning route exists under /users.
[ ] Refresh/logout tests pass.
[ ] Frontend build passes.
```

---

# 15. Boundary

This stage introduces server-side refresh-session governance. It does not yet move browser token storage to httpOnly cookies. That production hardening decision remains for the later frontend token-storage/security stage.
