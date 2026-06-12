# PBBF BLISS — Stage 3 Auth, Registration, and Session Governance Implementation Pack

**Stage:** 3 — Auth, Registration, and Session Governance  
**Version:** Stage 3.e — Safe Updated Pack  
**Repository root:** `/home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth`  
**Backend:** `pbbf-api/`  
**Frontend:** `pbbf-telehealth/`  
**Development OS:** Debian/Linux  
**Execution style:** Independent commands/snippets only. Run one command at a time.

---

## Objective

Make authentication behavior consistent, secure, and aligned with the MVP role model.

This updated pack keeps the original Stage 3 direction, but corrects the unsafe parts of the earlier Stage 3.d guide. The main correction is: **do not replace `AuthService` wholesale**, because the existing backend already contains password-reset, audit, and notification behavior that must remain intact.

---

## Stage 3 Contract Decisions

```text
1. Public registration remains patient-only.
2. Public RegisterForm must not show a role selector.
3. Public RegisterForm must not send role.
4. Admin-only internal user provisioning is created under /users.
5. lactation_consultant redirects to the provider workspace.
6. Frontend password validation matches backend: 8-128 chars, uppercase, lowercase, digit.
7. Refresh tokens are stored as server-side auth_sessions.
8. Refresh rotates the refresh session.
9. Logout revokes the refresh session when refresh_token is supplied.
10. Forgot-password/reset-password behavior must remain working.
11. resetPasswordRequest must remain exported by frontend authApi.js.
12. This stage does not move browser tokens to httpOnly cookies.
```

---

## Confirmed Repository Facts

```text
- Current Alembic head: c93a7f6d0b21
- Backend auth schemas already include RefreshTokenRequest and LogoutRequest.
- LogoutRequest already supports optional refresh_token.
- Users module currently has list, profile, role update, and status update routes.
- Frontend RegisterForm currently exposes a public role selector and sends role.
- Login/Register redirect mapping currently omits lactation_consultant.
```

---

# 0. Preflight Positioning

Run from repository root:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
pwd
ls
```

Expected root entries:

```text
pbbf-api
pbbf-telehealth
docs
infra
scripts
```

If already inside `pbbf-api`, do **not** run `cd pbbf-api`; first return to root:

```bash
cd ..
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

## Command 1.2 — Backup targeted files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

mkdir -p "$STAGE3_BACKUP_DIR/pbbf-api/app/db/models"
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/auth"
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users"
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/components"
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/services"
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/hooks"
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/utils"
mkdir -p "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/services"

cp pbbf-api/app/db/models/__init__.py "$STAGE3_BACKUP_DIR/pbbf-api/app/db/models/__init__.py"
cp pbbf-api/app/modules/auth/router.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/auth/router.py"
cp pbbf-api/app/modules/auth/service.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/auth/service.py"
cp pbbf-api/app/modules/auth/schemas.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/auth/schemas.py"
cp pbbf-api/app/modules/users/schemas.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users/schemas.py"
cp pbbf-api/app/modules/users/repository.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users/repository.py"
cp pbbf-api/app/modules/users/service.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users/service.py"
cp pbbf-api/app/modules/users/router.py "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/users/router.py"
cp pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx"
cp pbbf-telehealth/src/modules/auth/components/LoginForm.jsx "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/components/LoginForm.jsx"
cp pbbf-telehealth/src/modules/auth/services/authApi.js "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/services/authApi.js"
cp pbbf-telehealth/src/modules/auth/hooks/useAuth.js "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/hooks/useAuth.js"
cp pbbf-telehealth/src/modules/auth/utils/validators.js "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/modules/auth/utils/validators.js"
cp pbbf-telehealth/src/services/auth.service.js "$STAGE3_BACKUP_DIR/pbbf-telehealth/src/services/auth.service.js"
```

---

# 2. Backend Auth Session Model

## Files created/updated

```text
pbbf-api/app/db/models/auth_session.py
pbbf-api/app/db/models/__init__.py
pbbf-api/alembic/versions/f20260612_stage3_add_auth_sessions.py
```

## Command 2.1 — Create model

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
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
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

## Command 2.2 — Register model

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/db/models/__init__.py")
text = path.read_text()

if '    "auth_session",' not in text:
    text = text.replace('    "audit_log",\n', '    "audit_log",\n    "auth_session",\n')

if "from app.db.models.auth_session import AuthSession" not in text:
    text = text.replace(
        "from app.db.models.audit_log import AuditLog\n",
        "from app.db.models.audit_log import AuditLog\nfrom app.db.models.auth_session import AuthSession\n",
    )

if '    "AuthSession": AuthSession,' not in text:
    text = text.replace(
        '    "AuditLog": AuditLog,\n',
        '    "AuditLog": AuditLog,\n    "AuthSession": AuthSession,\n',
    )

if '    "AuthSession",' not in text:
    text = text.replace(
        '    "AuditLog",\n',
        '    "AuditLog",\n    "AuthSession",\n',
    )

path.write_text(text)
PY
```

## Command 2.3 — Create migration

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/alembic/versions/f20260612_stage3_add_auth_sessions.py <<'PY'
from alembic import op
import sqlalchemy as sa

revision = "f20260612_stage3"
down_revision = "c93a7f6d0b21"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("refresh_token_jti", sa.String(length=120), nullable=False),
        sa.Column("refresh_token_hash", sa.Text(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_reason", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_auth_sessions_id", "auth_sessions", ["id"])
    op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"])
    op.create_index("ix_auth_sessions_refresh_token_jti", "auth_sessions", ["refresh_token_jti"], unique=True)
    op.create_index("ix_auth_sessions_expires_at", "auth_sessions", ["expires_at"])
    op.create_index("ix_auth_sessions_revoked_at", "auth_sessions", ["revoked_at"])


def downgrade() -> None:
    op.drop_index("ix_auth_sessions_revoked_at", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_expires_at", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_refresh_token_jti", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_user_id", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_id", table_name="auth_sessions")
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

# 4. Backend Auth Service Session Governance — Safe Patch

## Critical rule

```text
Do not replace pbbf-api/app/modules/auth/service.py wholesale.
Preserve request_password_reset(), reset_password(), AuditService, NotificationService, and reset token behavior.
```

## Command 4.1 — Patch imports, session repository, token helper, refresh, and logout

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/modules/auth/service.py")
text = path.read_text()

if "from datetime import datetime, timezone" not in text:
    text = text.replace("from __future__ import annotations\n", "from __future__ import annotations\nfrom datetime import datetime, timezone\n")

if "from app.modules.auth.session_repository import AuthSessionRepository" not in text:
    text = text.replace(
        "from app.modules.auth.schemas import RegisterRequest\n",
        "from app.modules.auth.schemas import RegisterRequest\nfrom app.modules.auth.session_repository import AuthSessionRepository\n",
    )

if "self.sessions = AuthSessionRepository(db)" not in text:
    text = text.replace(
        "        self.notification_service = NotificationService(db)\n",
        "        self.notification_service = NotificationService(db)\n        self.sessions = AuthSessionRepository(db)\n",
    )

if "def _build_and_store_tokens" not in text:
    marker = "    def register_patient(self, payload: RegisterRequest) -> dict:\n"
    helper = '''    def _build_and_store_tokens(self, user) -> dict:\n        role_name = getattr(getattr(user, "role", None), "name", "unknown")\n        tokens = build_token_response(user_id=str(user.id), email=user.email, role=role_name)\n        refresh_payload = decode_refresh_token(tokens["refresh_token"])\n        refresh_jti = refresh_payload.get("jti")\n        refresh_exp = refresh_payload.get("exp")\n        if not refresh_jti or not refresh_exp:\n            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Refresh token metadata is missing.")\n        self.sessions.create_session(\n            user_id=user.id,\n            refresh_token=tokens["refresh_token"],\n            refresh_token_jti=refresh_jti,\n            expires_at=datetime.fromtimestamp(int(refresh_exp), tz=timezone.utc),\n        )\n        return tokens\n\n'''
    if marker not in text:
        raise SystemExit("register_patient marker not found. Inspect auth/service.py manually.")
    text = text.replace(marker, helper + marker)

old_register = '''        tokens = build_token_response(\n            user_id=str(user.id),\n            email=user.email,\n            role=getattr(user.role, "name", "patient"),\n        )\n'''
text = text.replace(old_register, "        tokens = self._build_and_store_tokens(user)\n")

old_login = '''        role_name = getattr(getattr(user, "role", None), "name", "unknown")\n        tokens = build_token_response(\n            user_id=str(user.id),\n            email=user.email,\n            role=role_name,\n        )\n'''
text = text.replace(old_login, "        tokens = self._build_and_store_tokens(user)\n")

start = text.find("    def refresh_access_token(self, refresh_token: str) -> dict:\n")
end = text.find("    def request_password_reset(self, email: str) -> dict:\n")
if start == -1 or end == -1:
    raise SystemExit("Refresh/password-reset boundaries not found. Inspect auth/service.py manually.")

new_refresh = '''    def refresh_access_token(self, refresh_token: str) -> dict:\n        try:\n            payload = decode_refresh_token(refresh_token)\n        except ValueError as exc:\n            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc\n\n        user_id = payload.get("sub")\n        refresh_jti = payload.get("jti")\n        if not user_id or not refresh_jti:\n            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token metadata is missing.")\n\n        session = self.sessions.get_active_session(refresh_token=refresh_token, refresh_token_jti=refresh_jti)\n        if session is None:\n            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh session is invalid or has been revoked.")\n\n        user = self.repository.get_user_by_id(user_id)\n        if user is None or not user.is_active:\n            self.sessions.revoke_session(session, reason="invalid_user")\n            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User for refresh token is invalid.")\n\n        self.sessions.revoke_session(session, reason="rotated")\n        tokens = self._build_and_store_tokens(user)\n        return {"user": self._serialize_user(user), "tokens": tokens}\n\n'''
text = text[:start] + new_refresh + text[end:]

start = text.find("    def logout(self) -> dict:\n")
if start != -1:
    end = text.find("    def current_user(self, user) -> dict:\n", start)
    if end == -1:
        raise SystemExit("Logout/current_user boundary not found. Inspect auth/service.py manually.")
    new_logout = '''    def logout(self, refresh_token: str | None = None) -> dict:\n        if refresh_token:\n            try:\n                payload = decode_refresh_token(refresh_token)\n                refresh_jti = payload.get("jti")\n                if refresh_jti:\n                    self.sessions.revoke_by_refresh_token(refresh_token=refresh_token, refresh_token_jti=refresh_jti, reason="logout")\n            except ValueError:\n                pass\n        return {"message": "Logout successful."}\n\n'''
    text = text[:start] + new_logout + text[end:]

path.write_text(text)
PY
```

---

# 5. Backend Auth Router Fixes

## Command 5.1 — Patch logout and `/auth/me`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/modules/auth/router.py")
text = path.read_text()

text = text.replace("return service.logout()", "return service.logout(refresh_token=payload.refresh_token)")

old = '''@router.get("/me", response_model=CurrentUserResponse)\ndef get_current_user_profile(current_user=Depends(get_current_active_user)):\n    return AuthService.current_user(AuthService, current_user)\n'''
new = '''@router.get("/me", response_model=CurrentUserResponse)\ndef get_current_user_profile(\n    current_user=Depends(get_current_active_user),\n    db: Session = Depends(get_db),\n):\n    service = AuthService(db)\n    return service.current_user(current_user)\n'''

if old in text:
    text = text.replace(old, new)
elif "return AuthService.current_user(AuthService, current_user)" in text:
    raise SystemExit("Legacy /auth/me return found but route shape differed. Patch manually.")

path.write_text(text)
PY
```

---

# 6. Backend Admin-Only Internal User Provisioning

## Boundary

```text
This creates internal user accounts only.
Provider/care-team profile enrichment remains separate unless future tests require immediate provider_profile creation.
```

## Command 6.1 — Add `AdminCreateUserRequest`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/modules/users/schemas.py")
text = path.read_text()

if "class AdminCreateUserRequest" not in text:
    text += '''\n\nclass AdminCreateUserRequest(BaseModel):\n    email: EmailStr\n    password: str = Field(min_length=8, max_length=128)\n    full_name: str = Field(min_length=2, max_length=120)\n    phone_number: Optional[str] = Field(default=None, max_length=30)\n    role_name: str = Field(min_length=3, max_length=50)\n\n    @field_validator("full_name")\n    @classmethod\n    def normalize_full_name(cls, value: str) -> str:\n        value = value.strip()\n        if len(value.split()) < 2:\n            raise ValueError("Full name must include at least two names.")\n        return value\n\n    @field_validator("password")\n    @classmethod\n    def validate_password_strength(cls, value: str) -> str:\n        has_upper = any(char.isupper() for char in value)\n        has_lower = any(char.islower() for char in value)\n        has_digit = any(char.isdigit() for char in value)\n        if not (has_upper and has_lower and has_digit):\n            raise ValueError("Password must include at least one uppercase letter, one lowercase letter, and one digit.")\n        return value\n\n    @field_validator("role_name")\n    @classmethod\n    def normalize_role_name(cls, value: str) -> str:\n        return value.strip().lower()\n'''

path.write_text(text)
PY
```

## Command 6.2 — Add repository create method

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/modules/users/repository.py")
text = path.read_text()

if "def create_user(" not in text:
    insert = '''\n    def create_user(\n        self,\n        *,\n        email: str,\n        full_name: str,\n        password_hash: str,\n        role_id: int,\n        phone_number: str | None = None,\n        is_active: bool = True,\n    ) -> User:\n        user = User(\n            email=email.strip().lower(),\n            full_name=full_name.strip(),\n            password_hash=password_hash,\n            role_id=role_id,\n            phone_number=phone_number,\n            is_active=is_active,\n        )\n        self.db.add(user)\n        self.db.commit()\n        self.db.refresh(user)\n        return self.get_user_by_id(user.id)\n'''
    text = text.replace("    def update_profile(\n", insert + "\n    def update_profile(\n")

path.write_text(text)
PY
```

## Command 6.3 — Add service method

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/modules/users/service.py")
text = path.read_text()

if "from app.common.utils.security import hash_password" not in text:
    text = text.replace("from sqlalchemy.orm import Session\n\n", "from sqlalchemy.orm import Session\n\nfrom app.common.utils.security import hash_password\n")

if "AdminCreateUserRequest" not in text:
    text = text.replace(
        "from app.modules.users.schemas import UserProfileUpdateRequest\n",
        "from app.modules.users.schemas import AdminCreateUserRequest, UserProfileUpdateRequest\n",
    )

if "def create_user_by_admin(" not in text:
    method = '''\n    def create_user_by_admin(self, payload: AdminCreateUserRequest) -> dict:\n        role_name = payload.role_name.strip().lower()\n        if role_name == "patient":\n            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Use public registration or patient onboarding flow for patient accounts.")\n\n        existing = self.repository.get_user_by_email(payload.email)\n        if existing is not None:\n            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with that email already exists.")\n\n        role = self.repository.get_role_by_name(role_name)\n        if role is None:\n            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found.")\n\n        user = self.repository.create_user(\n            email=payload.email,\n            full_name=payload.full_name,\n            password_hash=hash_password(payload.password),\n            role_id=role.id,\n            phone_number=payload.phone_number,\n            is_active=True,\n        )\n        return self._serialize_user(user)\n'''
    text = text.replace("    def get_me(self, current_user) -> dict:\n", method + "\n    def get_me(self, current_user) -> dict:")

path.write_text(text)
PY
```

## Command 6.4 — Add route

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/modules/users/router.py")
text = path.read_text()

if "AdminCreateUserRequest" not in text:
    text = text.replace("from app.modules.users.schemas import (\n", "from app.modules.users.schemas import (\n    AdminCreateUserRequest,\n")

if "def create_user(" not in text:
    route = '''\n@router.post("", response_model=UserProfileResponse, status_code=201)\ndef create_user(\n    payload: AdminCreateUserRequest,\n    admin_user=Depends(get_admin_user),\n    db: Session = Depends(get_db),\n):\n    service = UsersService(db)\n    return service.create_user_by_admin(payload)\n\n'''
    text = text.replace("@router.get(\"\", response_model=UserListResponse)\n", route + "@router.get(\"\", response_model=UserListResponse)\n")

path.write_text(text)
PY
```

---

# 7. Frontend Public Registration Cleanup

## Command 7.1 — Remove public role selector and role payload

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
import re

path = Path("pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx")
text = path.read_text()

text = text.replace(
    '    case "care_coordinator":\n      return "/provider";',
    '    case "care_coordinator":\n    case "lactation_consultant":\n      return "/provider";',
)

text = text.replace('    role: "patient",\n', '')
text = text.replace('        role: values.role,\n', '')

pattern = re.compile(r'\n\s*<div>\n\s*<label htmlFor="register-role"[\s\S]*?</select>\n\s*</div>\n', re.MULTILINE)
text, count = pattern.subn("\n", text)

path.write_text(text)
print(f"Removed role selector blocks: {count}")
PY
```

## Command 7.2 — Add `lactation_consultant` login redirect

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-telehealth/src/modules/auth/components/LoginForm.jsx")
text = path.read_text()
text = text.replace(
    '    case "care_coordinator":\n      return ROUTES.provider.dashboard;',
    '    case "care_coordinator":\n    case "lactation_consultant":\n      return ROUTES.provider.dashboard;',
)
path.write_text(text)
PY
```

---

# 8. Frontend Password Validation Parity

## Command 8.1

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-telehealth/src/modules/auth/utils/validators.js")
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

if old in text:
    text = text.replace(old, new)
elif "Password must include at least one uppercase letter" not in text:
    raise SystemExit("validatePassword shape differed. Inspect validators.js manually.")

path.write_text(text)
PY
```

---

# 9. Frontend Refresh/Logout API and Service

## Command 9.1 — Replace `authApi.js` but preserve reset-password API

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
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

export function resetPasswordRequest(payload) {
  return api.post("/auth/reset-password", payload);
}
EOF
```

## Command 9.2 — Patch `auth.service.js`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-telehealth/src/services/auth.service.js")
text = path.read_text()

if "refreshTokenRequest" not in text:
    text = text.replace("logoutRequest,\n  registerRequest,", "logoutRequest,\n  refreshTokenRequest,\n  registerRequest,")

if "async function refreshAccessToken()" not in text:
    insert = '''\nasync function refreshAccessToken() {\n  const refreshToken = getState().refreshToken;\n  if (!refreshToken) {\n    markSessionExpired("missing_refresh_token");\n    return getState();\n  }\n  try {\n    const response = await refreshTokenRequest({ refresh_token: refreshToken });\n    const normalized = normalizeAuthResponse(response);\n    if (!normalized.accessToken || !normalized.user) {\n      throw new ApiError("Refresh response is missing token or user data.", 500, response);\n    }\n    loginSuccess(normalized);\n    return getState();\n  } catch {\n    markSessionExpired("refresh_failed");\n    return getState();\n  }\n}\n'''
    text = text.replace("async function logout() {", insert + "\nasync function logout() {")

text = text.replace("await logoutRequest();", "await logoutRequest({ refresh_token: getState().refreshToken });")

if "refreshAccessToken," not in text:
    text = text.replace("hydrate,\n  logout,", "hydrate,\n  refreshAccessToken,\n  logout,")

path.write_text(text)
PY
```

## Command 9.3 — Expose refresh through hook

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-telehealth/src/modules/auth/hooks/useAuth.js")
text = path.read_text()

if "refreshAccessToken" not in text:
    text = text.replace("      logout: authService.logout,", "      refreshAccessToken: authService.refreshAccessToken,\n      logout: authService.logout,")

path.write_text(text)
PY
```

---

# 10. Tests

## Command 10.1 — Refresh rotation test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/tests/modules/auth/test_refresh_token.py <<'PY'
from __future__ import annotations


def register_user(client, email="refresh.stage3@example.com", password="StrongPass123"):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Refresh Stage"},
    )
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

## Command 10.2 — Logout revocation test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/tests/modules/auth/test_logout_revokes_session.py <<'PY'
from __future__ import annotations


def test_logout_revokes_refresh_session(client):
    register = client.post(
        "/api/v1/auth/register",
        json={"email": "logout.stage3@example.com", "password": "StrongPass123", "full_name": "Logout Stage"},
    )
    assert register.status_code == 201, register.text
    tokens = register.json()["tokens"]

    logout = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": tokens["refresh_token"]},
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
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
        json={
            "email": "role.inject.stage3@example.com",
            "password": "StrongPass123",
            "full_name": "Role Injection",
            "role": "admin",
        },
    )
    assert response.status_code == 201, response.text
    assert response.json()["user"]["role"] == "patient"
PY
```

## Command 10.4 — Create frontend auth governance test

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

# 11. Validation Commands

## Backend compile

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
python -m py_compile \
  app/db/models/auth_session.py \
  app/modules/auth/session_repository.py \
  app/modules/auth/service.py \
  app/modules/auth/router.py \
  app/modules/users/schemas.py \
  app/modules/users/repository.py \
  app/modules/users/service.py \
  app/modules/users/router.py
```

## Migration smoke

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
alembic heads
alembic history | tail -20
```

## Backend auth tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/auth/test_register.py tests/modules/auth/test_login.py -q
pytest tests/modules/auth/test_refresh_token.py tests/modules/auth/test_logout_revokes_session.py -q
pytest tests/modules/auth -q
```

## User tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/users/test_user_profile.py -q
```

## Frontend build and auth test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm run build
npm test -- --run src/modules/auth/__tests__/SessionRefresh.test.jsx
```

---

# 12. Post-Apply Inspection Commands

## Confirm RegisterForm cleanup

```bash
grep -n "register-role\|role:" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/modules/auth/components/RegisterForm.jsx || true
```

Expected: no `register-role` selector and no registration `role:` payload.

## Confirm session files

```bash
ls -la /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/db/models/auth_session.py
ls -la /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/auth/session_repository.py
```

## Confirm reset-password preservation

```bash
grep -n "request_password_reset\|reset_password\|_build_and_store_tokens\|def logout" \
  /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/auth/service.py

grep -n "refreshTokenRequest\|refreshAccessToken\|logoutRequest\|resetPasswordRequest" \
  /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/modules/auth/services/authApi.js \
  /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/services/auth.service.js
```

---

# 13. Completion Checklist

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
[ ] Forgot-password/reset-password behavior remains present.
[ ] resetPasswordRequest remains exported in frontend authApi.js.
[ ] Admin-only user provisioning route exists under POST /users.
[ ] Refresh/logout tests pass.
[ ] Frontend build passes.
```

---

# 14. Boundary

```text
This stage introduces server-side refresh-session governance.
This stage does not move browser token storage to httpOnly cookies.
This stage does not create full provider/care-team profile enrichment unless future tests require it.
This stage does not change object-level authorization.
This stage does not add major new auth features beyond session governance and admin-only user provisioning.
```

---

# 15. Rollback Note

If a patch fails or tests regress badly, restore targeted files from:

```bash
echo "$STAGE3_BACKUP_DIR"
```

Example:

```bash
cp "$STAGE3_BACKUP_DIR/pbbf-api/app/modules/auth/service.py" \
  /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/auth/service.py
```

Remove newly created Stage 3 files only if needed:

```bash
rm -f pbbf-api/app/db/models/auth_session.py
rm -f pbbf-api/app/modules/auth/session_repository.py
rm -f pbbf-api/alembic/versions/f20260612_stage3_add_auth_sessions.py
rm -f pbbf-api/tests/modules/auth/test_logout_revokes_session.py
rm -f pbbf-telehealth/src/modules/auth/__tests__/SessionRefresh.test.jsx
```
