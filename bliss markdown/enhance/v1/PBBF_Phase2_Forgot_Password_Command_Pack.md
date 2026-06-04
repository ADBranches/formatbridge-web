# PBBF BLISS — Phase 2 Command Pack (Forgot Password End-to-End)

## Phase 2 objective
Close the MVP auth gap by implementing a **real password recovery flow** end-to-end. This command pack uses a **request-reset + tokenized reset completion** approach:

1. user submits email to `/auth/forgot-password`
2. backend always returns a **generic safe response**
3. if the user exists and is active, backend creates a short-lived **password reset token**
4. backend queues an **email notification** with a reset link
5. user opens `/reset-password?token=...`
6. user submits a new password to `/auth/reset-password`
7. backend validates token, updates password hash, and records audit events. citeturn74search1turn79search1

## Inspection boundary already satisfied
The file structures below were inspected before generating this pack, so the commands target known structures only:

### Backend
- `pbbf-api/app/modules/auth/router.py` citeturn76search7
- `pbbf-api/app/modules/auth/schemas.py` citeturn76search7
- `pbbf-api/app/modules/auth/service.py` citeturn76search7
- `pbbf-api/app/modules/auth/repository.py` citeturn79search1
- `pbbf-api/app/common/utils/security.py` citeturn79search1
- `pbbf-api/app/modules/auth/tokens.py` citeturn79search1
- `pbbf-api/app/modules/notifications/service.py` citeturn76search7
- `pbbf-api/app/modules/audit/service.py` citeturn76search7
- `pbbf-api/app/common/config/settings.py` citeturn79search1
- `pbbf-api/app/db/models/user.py` citeturn79search1

### Frontend
- `pbbf-telehealth/src/modules/auth/services/authApi.js` citeturn79search1
- `pbbf-telehealth/src/services/auth.service.js` citeturn79search1
- `pbbf-telehealth/src/modules/auth/hooks/useAuth.js` citeturn79search1
- `pbbf-telehealth/src/modules/auth/utils/validators.js` citeturn79search1
- `pbbf-telehealth/src/modules/auth/pages/ForgotPassword.jsx` citeturn76search7turn79search1
- `pbbf-telehealth/src/shared/constants/routes.js` citeturn79search1
- `pbbf-telehealth/src/app/AppRoutes.jsx` citeturn79search1
- auth test tree under `pbbf-telehealth/src/modules/auth/__tests__/` citeturn79search1

---

# 0) Go to repo root and create a backup area

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
export PHASE2_FORGOT_PASSWORD_BACKUP_DIR="backups/phase2_forgot_password_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR"
echo "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR"
```

---

# 1) Back up the files we will patch

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/modules/auth"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/modules/notifications"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/common/utils"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/modules/auth/services"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/modules/auth/hooks"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/modules/auth/utils"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/modules/auth/pages"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/shared/constants"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/app"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/services"
mkdir -p "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/modules/auth/__tests__"

cp pbbf-api/app/modules/auth/router.py "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/modules/auth/router.py"
cp pbbf-api/app/modules/auth/schemas.py "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/modules/auth/schemas.py"
cp pbbf-api/app/modules/auth/service.py "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/modules/auth/service.py"
cp pbbf-api/app/modules/auth/repository.py "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/modules/auth/repository.py"
cp pbbf-api/app/modules/auth/tokens.py "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/modules/auth/tokens.py"
cp pbbf-api/app/modules/notifications/service.py "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/modules/notifications/service.py"
cp pbbf-api/app/common/utils/security.py "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-api/app/common/utils/security.py"

cp pbbf-telehealth/src/modules/auth/services/authApi.js "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/modules/auth/services/authApi.js"
cp pbbf-telehealth/src/services/auth.service.js "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/services/auth.service.js"
cp pbbf-telehealth/src/modules/auth/hooks/useAuth.js "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/modules/auth/hooks/useAuth.js"
cp pbbf-telehealth/src/modules/auth/utils/validators.js "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/modules/auth/utils/validators.js"
cp pbbf-telehealth/src/modules/auth/pages/ForgotPassword.jsx "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/modules/auth/pages/ForgotPassword.jsx"
cp pbbf-telehealth/src/shared/constants/routes.js "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/shared/constants/routes.js"
cp pbbf-telehealth/src/app/AppRoutes.jsx "$PHASE2_FORGOT_PASSWORD_BACKUP_DIR/pbbf-telehealth/src/app/AppRoutes.jsx"
```

---

# 2) Patch backend auth repository

## Adds
- `update_password(user, password_hash)`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/auth/repository.py").write_text("""from __future__ import annotations\n\nfrom datetime import datetime, timezone\nfrom typing import Optional\n\nfrom sqlalchemy import select\nfrom sqlalchemy.orm import Session, joinedload\n\nfrom app.db.models.role import Role\nfrom app.db.models.user import User\n\n\nclass AuthRepository:\n    def __init__(self, db: Session) -> None:\n        self.db = db\n\n    @staticmethod\n    def _normalize_user_id(user_id: str | int) -> int | str:\n        if isinstance(user_id, str):\n            cleaned = user_id.strip()\n            if cleaned.isdigit():\n                return int(cleaned)\n            return cleaned\n        return user_id\n\n    def get_user_by_email(self, email: str) -> Optional[User]:\n        stmt = (\n            select(User)\n            .options(joinedload(User.role))\n            .where(User.email == email.strip().lower())\n        )\n        return self.db.execute(stmt).scalar_one_or_none()\n\n    def get_user_by_id(self, user_id: str | int) -> Optional[User]:\n        normalized_user_id = self._normalize_user_id(user_id)\n        stmt = (\n            select(User)\n            .options(joinedload(User.role))\n            .where(User.id == normalized_user_id)\n        )\n        return self.db.execute(stmt).scalar_one_or_none()\n\n    def get_role_by_name(self, role_name: str) -> Optional[Role]:\n        stmt = select(Role).where(Role.name == role_name.strip().lower())\n        return self.db.execute(stmt).scalar_one_or_none()\n\n    def create_user(\n        self,\n        *,\n        email: str,\n        full_name: str,\n        password_hash: str,\n        role_id,\n        phone_number: str | None = None,\n        is_active: bool = True,\n    ) -> User:\n        user = User(\n            email=email.strip().lower(),\n            full_name=full_name.strip(),\n            password_hash=password_hash,\n            role_id=role_id,\n            phone_number=phone_number,\n            is_active=is_active,\n        )\n        self.db.add(user)\n        self.db.commit()\n        self.db.refresh(user)\n        return self.get_user_by_id(user.id)\n\n    def update_last_login(self, user: User) -> User:\n        if hasattr(user, \"last_login_at\"):\n            user.last_login_at = datetime.now(timezone.utc)\n            self.db.add(user)\n            self.db.commit()\n            self.db.refresh(user)\n        return user\n\n    def update_password(self, user: User, password_hash: str) -> User:\n        user.password_hash = password_hash\n        if hasattr(user, \"must_change_password\"):\n            user.must_change_password = False\n        self.db.add(user)\n        self.db.commit()\n        self.db.refresh(user)\n        return self.get_user_by_id(user.id)\n""", encoding="utf-8")'
```

---

# 3) Patch backend security utils

## Adds
- `create_password_reset_token()`
- `decode_password_reset_token()`

This reuses the existing JWT token framework with a dedicated `password_reset` token type. citeturn79search1

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; p=Path("pbbf-api/app/common/utils/security.py"); text=p.read_text(encoding="utf-8"); marker="def preview_secret_rotation(secret_value: str) -> dict[str, str]:\n    return {\n        \"length\": str(len(secret_value)),\n        \"sha256\": hash_for_rotation_preview(secret_value),\n    }\n"; addition="\n\ndef create_password_reset_token(*, subject: str, email: Optional[str] = None, role: Optional[str] = None) -> str:\n    return create_token(\n        subject=subject,\n        token_type=\"password_reset\",\n        email=email,\n        role=role,\n        expires_delta=timedelta(minutes=30),\n        additional_claims={\"purpose\": \"password_reset\"},\n    )\n\n\ndef decode_password_reset_token(token: str) -> Dict[str, Any]:\n    payload = decode_token(token)\n    validate_token_type(payload, \"password_reset\")\n    return payload\n"; 
text=text.replace(marker, marker+addition); p.write_text(text, encoding="utf-8")'
```

---

# 4) Patch backend auth token helpers

## Adds
- `decode_password_reset_token()` passthrough helper

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/auth/tokens.py").write_text("""from __future__ import annotations\n\nfrom typing import Dict\n\nfrom app.common.utils.security import (\n    decode_password_reset_token as decode_password_reset_token_payload,\n    decode_token,\n    issue_token_pair,\n    validate_token_type,\n)\n\n\ndef build_token_response(user_id: str, email: str, role: str) -> Dict[str, str]:\n    return issue_token_pair(user_id=str(user_id), email=email, role=role)\n\n\ndef decode_access_token(token: str) -> dict:\n    payload = decode_token(token)\n    validate_token_type(payload, \"access\")\n    return payload\n\n\ndef decode_refresh_token(token: str) -> dict:\n    payload = decode_token(token)\n    validate_token_type(payload, \"refresh\")\n    return payload\n\n\ndef decode_password_reset_token(token: str) -> dict:\n    return decode_password_reset_token_payload(token)\n""", encoding="utf-8")'
```

---

# 5) Patch backend auth schemas

## Adds
- `ForgotPasswordRequest`
- `ResetPasswordRequest`
- reuses `MessageResponse` for safe responses

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/auth/schemas.py").write_text("""from __future__ import annotations\n\nfrom typing import Optional\n\nfrom pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator\n\n\nclass RegisterRequest(BaseModel):\n    email: EmailStr\n    password: str = Field(min_length=8, max_length=128)\n    full_name: str = Field(min_length=2, max_length=120)\n    phone_number: Optional[str] = Field(default=None, max_length=30)\n\n    @field_validator(\"full_name\")\n    @classmethod\n    def validate_full_name(cls, value: str) -> str:\n        value = value.strip()\n        if len(value.split()) < 2:\n            raise ValueError(\"Full name must include at least two names.\")\n        return value\n\n    @field_validator(\"password\")\n    @classmethod\n    def validate_password_strength(cls, value: str) -> str:\n        has_upper = any(char.isupper() for char in value)\n        has_lower = any(char.islower() for char in value)\n        has_digit = any(char.isdigit() for char in value)\n        if not (has_upper and has_lower and has_digit):\n            raise ValueError(\n                \"Password must include at least one uppercase letter, one lowercase letter, and one digit.\"\n            )\n        return value\n\n\nclass LoginRequest(BaseModel):\n    email: EmailStr\n    password: str = Field(min_length=8, max_length=128)\n\n\nclass RefreshTokenRequest(BaseModel):\n    refresh_token: str = Field(min_length=20)\n\n\nclass LogoutRequest(BaseModel):\n    refresh_token: Optional[str] = None\n\n\nclass ForgotPasswordRequest(BaseModel):\n    email: EmailStr\n\n\nclass ResetPasswordRequest(BaseModel):\n    token: str = Field(min_length=20)\n    new_password: str = Field(min_length=8, max_length=128)\n\n    @field_validator(\"new_password\")\n    @classmethod\n    def validate_password_strength(cls, value: str) -> str:\n        has_upper = any(char.isupper() for char in value)\n        has_lower = any(char.islower() for char in value)\n        has_digit = any(char.isdigit() for char in value)\n        if not (has_upper and has_lower and has_digit):\n            raise ValueError(\n                \"Password must include at least one uppercase letter, one lowercase letter, and one digit.\"\n            )\n        return value\n\n\nclass AuthUserResponse(BaseModel):\n    model_config = ConfigDict(from_attributes=True)\n\n    id: str | int\n    email: EmailStr\n    full_name: str\n    phone_number: Optional[str] = None\n    is_active: bool\n    is_superuser: bool = False\n    role: str\n\n\nclass TokenPairResponse(BaseModel):\n    access_token: str\n    refresh_token: str\n    token_type: str = \"bearer\"\n\n\nclass AuthResponse(BaseModel):\n    user: AuthUserResponse\n    tokens: TokenPairResponse\n\n\nclass MessageResponse(BaseModel):\n    message: str\n\n\nclass CurrentUserResponse(BaseModel):\n    user: AuthUserResponse\n""", encoding="utf-8")'
```

---

# 6) Patch backend notification service

## Adds
- `create_password_reset_hook(user, reset_link)`

This queues a generic email notification for password reset without requiring a logged-in actor. Audit logging stays in `AuthService` so auth events are tracked centrally. citeturn76search7turn79search1

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/notifications/service.py").write_text("""from fastapi import HTTPException, status\nfrom sqlalchemy.orm import Session\n\nfrom app.db.models import Notification, Patient, Referral, User\nfrom app.modules.audit.service import AuditService\nfrom app.modules.notifications.channels import dispatch_channel_message\nfrom app.modules.notifications.repository import NotificationRepository\nfrom app.modules.notifications.schemas import (\n    NotificationCreateRequest,\n    NotificationStatus,\n)\nfrom app.modules.notifications.tasks import build_referral_follow_up_notification\n\n\nclass NotificationService:\n    def __init__(self, db: Session):\n        self.db = db\n        self.repository = NotificationRepository(db)\n        self.audit_service = AuditService(db)\n\n    @staticmethod\n    def _role_name(user: User) -> str:\n        if hasattr(user, \"role_name\") and user.role_name:\n            return str(user.role_name).lower()\n        if hasattr(user, \"role\") and user.role and hasattr(user.role, \"name\"):\n            return str(user.role.name).lower()\n        return \"patient\"\n\n    def _require_actor_can_send(self, actor: User) -> None:\n        role_name = self._role_name(actor)\n        if role_name not in {\"provider\", \"care_coordinator\", \"admin\"}:\n            raise HTTPException(\n                status_code=status.HTTP_403_FORBIDDEN,\n                detail=\"You are not allowed to create notifications.\",\n            )\n\n    def create_notification(self, payload: NotificationCreateRequest, actor: User) -> Notification:\n        self._require_actor_can_send(actor)\n        notification = self.repository.create(\n            user_id=payload.user_id,\n            channel=payload.channel.value,\n            notification_type=payload.notification_type.value,\n            subject=payload.subject,\n            body=payload.body,\n            status=NotificationStatus.PENDING.value,\n            metadata_json=payload.metadata,\n            scheduled_for=payload.scheduled_for,\n        )\n        self.audit_service.log_event(\n            actor_user_id=actor.id,\n            action=\"notification.created\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"user_id\": notification.user_id,\n                \"channel\": notification.channel,\n                \"notification_type\": notification.notification_type,\n            },\n        )\n        return notification\n\n    def list_for_user(self, user_id: int) -> list[Notification]:\n        return self.repository.list_for_user(user_id)\n\n    def dispatch_notification(self, notification_id: int, actor: User) -> Notification:\n        notification = self.repository.get_by_id(notification_id)\n        if not notification:\n            raise HTTPException(\n                status_code=status.HTTP_404_NOT_FOUND,\n                detail=\"Notification not found.\",\n            )\n\n        role_name = self._role_name(actor)\n        if role_name == \"patient\" and actor.id != notification.user_id:\n            raise HTTPException(\n                status_code=status.HTTP_403_FORBIDDEN,\n                detail=\"You are not allowed to dispatch this notification.\",\n            )\n\n        try:\n            dispatch_result = dispatch_channel_message(\n                channel=notification.channel,\n                notification=notification,\n            )\n            notification = self.repository.mark_sent(\n                notification=notification,\n                provider_message_id=dispatch_result[\"provider_message_id\"],\n            )\n        except Exception as exc:  # pragma: no cover\n            notification = self.repository.mark_failed(\n                notification=notification,\n                failure_reason=str(exc),\n            )\n\n        self.audit_service.log_event(\n            actor_user_id=actor.id,\n            action=\"notification.dispatched\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"status\": notification.status,\n                \"channel\": notification.channel,\n            },\n        )\n        return notification\n\n    def create_referral_follow_up_hook(self, referral: Referral, actor: User) -> Notification | None:\n        patient = self.db.query(Patient).filter(Patient.id == referral.patient_id).first()\n        if not patient:\n            return None\n\n        patient_user_id = getattr(patient, \"user_id\", None)\n        if not patient_user_id:\n            return None\n\n        payload = build_referral_follow_up_notification(\n            referral=referral,\n            patient_user_id=patient_user_id,\n        )\n\n        notification = self.repository.create(\n            user_id=payload[\"user_id\"],\n            channel=payload[\"channel\"],\n            notification_type=payload[\"notification_type\"],\n            subject=payload[\"subject\"],\n            body=payload[\"body\"],\n            status=NotificationStatus.PENDING.value,\n            metadata_json=payload[\"metadata\"],\n            scheduled_for=payload[\"scheduled_for\"],\n        )\n\n        self.audit_service.log_event(\n            actor_user_id=actor.id,\n            action=\"notification.referral_follow_up_created\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"referral_id\": referral.id,\n                \"user_id\": notification.user_id,\n            },\n        )\n        return notification\n\n    def create_password_reset_hook(self, *, user: User, reset_link: str) -> Notification:\n        return self.repository.create(\n            user_id=user.id,\n            channel=\"email\",\n            notification_type=\"generic\",\n            subject=\"Reset your password\",\n            body=(\n                \"We received a request to reset your password. \"\n                f\"Use this link to continue: {reset_link}\"\n            ),\n            status=NotificationStatus.PENDING.value,\n            metadata_json={\n                \"purpose\": \"password_reset\",\n                \"reset_link\": reset_link,\n            },\n            scheduled_for=None,\n        )\n""", encoding="utf-8")'
```

---

# 7) Patch backend auth service

## Adds
- `request_password_reset(email)`
- `reset_password(token, new_password)`
- audit logging for request/completion
- queued password-reset notification creation

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/auth/service.py").write_text("""from __future__ import annotations\n\nfrom fastapi import HTTPException, status\n\nfrom app.common.config.settings import get_settings\nfrom app.common.utils.security import create_password_reset_token, hash_password, verify_password\nfrom app.modules.audit.service import AuditService\nfrom app.modules.auth.repository import AuthRepository\nfrom app.modules.auth.schemas import RegisterRequest\nfrom app.modules.auth.tokens import build_token_response, decode_password_reset_token, decode_refresh_token\nfrom app.modules.notifications.service import NotificationService\n\n\nclass AuthService:\n    def __init__(self, db):\n        self.db = db\n        self.repository = AuthRepository(db)\n        self.audit_service = AuditService(db)\n        self.notification_service = NotificationService(db)\n\n    @staticmethod\n    def _serialize_user(user):\n        role_name = getattr(getattr(user, \"role\", None), \"name\", None)\n        return {\n            \"id\": str(user.id),\n            \"email\": user.email,\n            \"full_name\": user.full_name,\n            \"phone_number\": getattr(user, \"phone_number\", None),\n            \"is_active\": user.is_active,\n            \"is_superuser\": getattr(user, \"is_superuser\", False),\n            \"role\": role_name or \"unknown\",\n        }\n\n    def register_patient(self, payload: RegisterRequest) -> dict:\n        existing_user = self.repository.get_user_by_email(payload.email)\n        if existing_user is not None:\n            raise HTTPException(\n                status_code=status.HTTP_409_CONFLICT,\n                detail=\"An account with that email already exists.\",\n            )\n\n        patient_role = self.repository.get_role_by_name(\"patient\")\n        if patient_role is None:\n            raise HTTPException(\n                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,\n                detail=\"Default patient role is missing. Seed roles first.\",\n            )\n\n        user = self.repository.create_user(\n            email=payload.email,\n            full_name=payload.full_name,\n            password_hash=hash_password(payload.password),\n            role_id=patient_role.id,\n            phone_number=payload.phone_number,\n            is_active=True,\n        )\n\n        tokens = build_token_response(\n            user_id=str(user.id),\n            email=user.email,\n            role=getattr(user.role, \"name\", \"patient\"),\n        )\n\n        return {\n            \"user\": self._serialize_user(user),\n            \"tokens\": tokens,\n        }\n\n    def login(self, email: str, password: str) -> dict:\n        user = self.repository.get_user_by_email(email)\n        if user is None or not verify_password(password, user.password_hash):\n            raise HTTPException(\n                status_code=status.HTTP_401_UNAUTHORIZED,\n                detail=\"Invalid email or password.\",\n            )\n\n        if not user.is_active:\n            raise HTTPException(\n                status_code=status.HTTP_403_FORBIDDEN,\n                detail=\"This account is inactive.\",\n            )\n\n        user = self.repository.update_last_login(user)\n        role_name = getattr(getattr(user, \"role\", None), \"name\", \"unknown\")\n        tokens = build_token_response(\n            user_id=str(user.id),\n            email=user.email,\n            role=role_name,\n        )\n\n        return {\n            \"user\": self._serialize_user(user),\n            \"tokens\": tokens,\n        }\n\n    def refresh_access_token(self, refresh_token: str) -> dict:\n        try:\n            payload = decode_refresh_token(refresh_token)\n        except ValueError as exc:\n            raise HTTPException(\n                status_code=status.HTTP_401_UNAUTHORIZED,\n                detail=str(exc),\n            ) from exc\n\n        user_id = payload.get(\"sub\")\n        if not user_id:\n            raise HTTPException(\n                status_code=status.HTTP_401_UNAUTHORIZED,\n                detail=\"Refresh token subject is missing.\",\n            )\n\n        user = self.repository.get_user_by_id(user_id)\n        if user is None or not user.is_active:\n            raise HTTPException(\n                status_code=status.HTTP_401_UNAUTHORIZED,\n                detail=\"User for refresh token is invalid.\",\n            )\n\n        role_name = getattr(getattr(user, \"role\", None), \"name\", \"unknown\")\n        tokens = build_token_response(\n            user_id=str(user.id),\n            email=user.email,\n            role=role_name,\n        )\n\n        return {\n            \"user\": self._serialize_user(user),\n            \"tokens\": tokens,\n        }\n\n    def request_password_reset(self, email: str) -> dict:\n        generic_message = {\n            \"message\": \"If the account exists, password recovery instructions have been sent.\"\n        }\n\n        user = self.repository.get_user_by_email(email)\n        if user is None or not user.is_active:\n            self.audit_service.log_event(\n                actor_user_id=None,\n                action=\"auth.password_reset_requested\",\n                entity_type=\"user\",\n                entity_id=None,\n                details={\n                    \"email\": email.strip().lower(),\n                    \"resolved_user\": False,\n                },\n            )\n            return generic_message\n\n        role_name = getattr(getattr(user, \"role\", None), \"name\", \"unknown\")\n        token = create_password_reset_token(\n            subject=str(user.id),\n            email=user.email,\n            role=role_name,\n        )\n\n        settings = get_settings()\n        base_url = (settings.base_external_url or \"http://127.0.0.1:5173\").rstrip(\"/\")\n        reset_link = f\"{base_url}/reset-password?token={token}\"\n\n        self.notification_service.create_password_reset_hook(user=user, reset_link=reset_link)\n        self.audit_service.log_event(\n            actor_user_id=user.id,\n            action=\"auth.password_reset_requested\",\n            entity_type=\"user\",\n            entity_id=user.id,\n            details={\n                \"email\": user.email,\n                \"delivery_channel\": \"email\",\n            },\n        )\n        return generic_message\n\n    def reset_password(self, token: str, new_password: str) -> dict:\n        try:\n            payload = decode_password_reset_token(token)\n        except ValueError as exc:\n            raise HTTPException(\n                status_code=status.HTTP_401_UNAUTHORIZED,\n                detail=str(exc),\n            ) from exc\n\n        user_id = payload.get(\"sub\")\n        if not user_id:\n            raise HTTPException(\n                status_code=status.HTTP_401_UNAUTHORIZED,\n                detail=\"Reset token subject is missing.\",\n            )\n\n        user = self.repository.get_user_by_id(user_id)\n        if user is None or not user.is_active:\n            raise HTTPException(\n                status_code=status.HTTP_401_UNAUTHORIZED,\n                detail=\"User for reset token is invalid.\",\n            )\n\n        updated_user = self.repository.update_password(user, hash_password(new_password))\n        self.audit_service.log_event(\n            actor_user_id=updated_user.id,\n            action=\"auth.password_reset_completed\",\n            entity_type=\"user\",\n            entity_id=updated_user.id,\n            details={\n                \"email\": updated_user.email,\n            },\n        )\n\n        return {\n            \"message\": \"Password has been reset successfully. You can now sign in with your new password.\"\n        }\n\n    def logout(self) -> dict:\n        return {\"message\": \"Logout successful.\"}\n\n    def current_user(self, user) -> dict:\n        return {\"user\": self._serialize_user(user)}\n""", encoding="utf-8")'
```

---

# 8) Patch backend auth router

## Adds
- `POST /auth/forgot-password`
- `POST /auth/reset-password`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/auth/router.py").write_text("""from __future__ import annotations\n\nfrom fastapi import APIRouter, Depends, status\nfrom sqlalchemy.orm import Session\n\nfrom app.db.session import get_db\nfrom app.modules.auth.dependencies import get_current_active_user\nfrom app.modules.auth.schemas import (\n    AuthResponse,\n    CurrentUserResponse,\n    ForgotPasswordRequest,\n    LoginRequest,\n    LogoutRequest,\n    MessageResponse,\n    RefreshTokenRequest,\n    RegisterRequest,\n    ResetPasswordRequest,\n)\nfrom app.modules.auth.service import AuthService\n\nrouter = APIRouter(prefix=\"/auth\", tags=[\"Authentication\"])\n\n\n@router.post(\n    \"/register\",\n    response_model=AuthResponse,\n    status_code=status.HTTP_201_CREATED,\n)\ndef register(payload: RegisterRequest, db: Session = Depends(get_db)):\n    service = AuthService(db)\n    return service.register_patient(payload)\n\n\n@router.post(\"/login\", response_model=AuthResponse)\ndef login(payload: LoginRequest, db: Session = Depends(get_db)):\n    service = AuthService(db)\n    return service.login(email=payload.email, password=payload.password)\n\n\n@router.post(\"/refresh\", response_model=AuthResponse)\ndef refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):\n    service = AuthService(db)\n    return service.refresh_access_token(payload.refresh_token)\n\n\n@router.post(\"/logout\", response_model=MessageResponse)\ndef logout(\n    payload: LogoutRequest,\n    current_user=Depends(get_current_active_user),\n    db: Session = Depends(get_db),\n):\n    service = AuthService(db)\n    return service.logout()\n\n\n@router.get(\"/me\", response_model=CurrentUserResponse)\ndef get_current_user_profile(current_user=Depends(get_current_active_user)):\n    return AuthService.current_user(AuthService, current_user)\n\n\n@router.post(\"/forgot-password\", response_model=MessageResponse)\ndef forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):\n    service = AuthService(db)\n    return service.request_password_reset(payload.email)\n\n\n@router.post(\"/reset-password\", response_model=MessageResponse)\ndef reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):\n    service = AuthService(db)\n    return service.reset_password(token=payload.token, new_password=payload.new_password)\n""", encoding="utf-8")'
```

---

# 9) Patch frontend auth API service

## Adds
- `resetPasswordRequest(payload)`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/modules/auth/services/authApi.js").write_text("""import { api } from \"../../../services/api\";\n\nexport function loginRequest(payload) {\n  return api.post(\"/auth/login\", payload);\n}\n\nexport function registerRequest(payload) {\n  return api.post(\"/auth/register\", payload);\n}\n\nexport function logoutRequest() {\n  return api.post(\"/auth/logout\", {});\n}\n\nexport function getCurrentUserRequest() {\n  return api.get(\"/auth/me\");\n}\n\nexport function forgotPasswordRequest(payload) {\n  return api.post(\"/auth/forgot-password\", payload);\n}\n\nexport function resetPasswordRequest(payload) {\n  return api.post(\"/auth/reset-password\", payload);\n}\n""", encoding="utf-8")'
```

---

# 10) Patch frontend auth service

## Adds
- `resetPassword(token, newPassword)`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/services/auth.service.js").write_text("""import { ApiError } from \"./api\";\nimport { clearState, getState, hydrateAuth, loginSuccess, markSessionExpired, updateUser } from \"../store/authStore\";\nimport {\n  forgotPasswordRequest,\n  getCurrentUserRequest,\n  loginRequest,\n  logoutRequest,\n  registerRequest,\n  resetPasswordRequest,\n} from \"../modules/auth/services/authApi\";\n\nfunction normalizeAuthResponse(response) {\n  const data = response?.data || response;\n  const tokens = data?.tokens || {};\n\n  return {\n    accessToken:\n      tokens?.access_token ||\n      tokens?.accessToken ||\n      data?.access_token ||\n      data?.accessToken ||\n      null,\n    refreshToken:\n      tokens?.refresh_token ||\n      tokens?.refreshToken ||\n      data?.refresh_token ||\n      data?.refreshToken ||\n      null,\n    tokenType: data?.token_type || data?.tokenType || tokens?.token_type || \"bearer\",\n    user: data?.user || null,\n    message: data?.message || response?.message || \"Authentication successful.\",\n  };\n}\n\nasync function login(credentials) {\n  const response = await loginRequest(credentials);\n  const normalized = normalizeAuthResponse(response);\n\n  if (!normalized.accessToken || !normalized.user) {\n    throw new ApiError(\"Login response is missing token or user data.\", 500, response);\n  }\n\n  loginSuccess(normalized);\n  return normalized;\n}\n\nasync function register(payload) {\n  const response = await registerRequest(payload);\n  const normalized = normalizeAuthResponse(response);\n\n  if (normalized.accessToken && normalized.user) {\n    loginSuccess(normalized);\n  }\n\n  return normalized;\n}\n\nasync function hydrate() {\n  const hydrated = hydrateAuth();\n\n  if (!hydrated.isAuthenticated || !hydrated.accessToken) {\n    return hydrated;\n  }\n\n  try {\n    const response = await getCurrentUserRequest();\n    const data = response?.data || response;\n    const user = data?.user || data;\n    updateUser(user);\n    return getState();\n  } catch {\n    markSessionExpired(\"server_session_validation_failed\");\n    return getState();\n  }\n}\n\nasync function logout() {\n  try {\n    await logoutRequest();\n  } catch {\n    // best-effort logout\n  } finally {\n    clearState();\n  }\n}\n\nasync function requestPasswordReset(email) {\n  return forgotPasswordRequest({ email });\n}\n\nasync function resetPassword(token, newPassword) {\n  return resetPasswordRequest({ token, new_password: newPassword });\n}\n\nfunction getCurrentUser() {\n  return getState().user;\n}\n\nfunction isAuthenticated() {\n  return getState().isAuthenticated;\n}\n\nexport const authService = {\n  login,\n  register,\n  hydrate,\n  logout,\n  getCurrentUser,\n  isAuthenticated,\n  requestPasswordReset,\n  resetPassword,\n};\n""", encoding="utf-8")'
```

---

# 11) Patch frontend auth hook

## Adds
- `resetPassword` to the exposed hook surface

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/modules/auth/hooks/useAuth.js").write_text("""import { useMemo } from \"react\";\nimport { authService } from \"../../../services/auth.service\";\nimport { useAuthStore } from \"../../../store/authStore\";\n\nexport function useAuth() {\n  const authState = useAuthStore();\n\n  return useMemo(\n    () => ({\n      ...authState,\n      login: authService.login,\n      register: authService.register,\n      hydrate: authService.hydrate,\n      logout: authService.logout,\n      requestPasswordReset: authService.requestPasswordReset,\n      resetPassword: authService.resetPassword,\n    }),\n    [authState]\n  );\n}\n""", encoding="utf-8")'
```

---

# 12) Patch frontend auth validators

## Adds
- `validateResetPasswordForm(values)`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/modules/auth/utils/validators.js").write_text("""export function validateEmail(value) {\n  if (!value?.trim()) return \"Email is required.\";\n  const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;\n  if (!emailRegex.test(value.trim())) return \"Enter a valid email address.\";\n  return \"\";\n}\n\nexport function validatePassword(value) {\n  if (!value) return \"Password is required.\";\n  if (value.length < 8) return \"Password must be at least 8 characters.\";\n  return \"\";\n}\n\nexport function validateLoginForm(values) {\n  return {\n    email: validateEmail(values.email),\n    password: validatePassword(values.password),\n  };\n}\n\nexport function validateRegisterForm(values) {\n  const errors = {\n    fullName: \"\",\n    email: \"\",\n    password: \"\",\n    confirmPassword: \"\",\n  };\n\n  if (!values.fullName?.trim()) {\n    errors.fullName = \"Full name is required.\";\n  }\n\n  errors.email = validateEmail(values.email);\n  errors.password = validatePassword(values.password);\n\n  if (!values.confirmPassword) {\n    errors.confirmPassword = \"Please confirm your password.\";\n  } else if (values.confirmPassword !== values.password) {\n    errors.confirmPassword = \"Passwords do not match.\";\n  }\n\n  return errors;\n}\n\nexport function validateResetPasswordForm(values) {\n  const errors = {\n    password: validatePassword(values.password),\n    confirmPassword: \"\",\n  };\n\n  if (!values.confirmPassword) {\n    errors.confirmPassword = \"Please confirm your password.\";\n  } else if (values.confirmPassword !== values.password) {\n    errors.confirmPassword = \"Passwords do not match.\";\n  }\n\n  return errors;\n}\n\nexport function hasFormErrors(errors) {\n  return Object.values(errors).some(Boolean);\n}\n""", encoding="utf-8")'
```

---

# 13) Patch frontend route constants

## Adds
- `resetPassword: "/reset-password"`
- route title for reset-password

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/shared/constants/routes.js").write_text("""export const ROUTES = {\n  root: \"/\",\n  login: \"/login\",\n  register: \"/register\",\n  forgotPassword: \"/forgot-password\",\n  resetPassword: \"/reset-password\",\n\n  patient: {\n    dashboard: \"/patient/dashboard\",\n    onboarding: {\n      consent: \"/patient/onboarding/consent\",\n      intake: \"/patient/onboarding/intake\",\n    },\n    appointments: \"/patient/appointments\",\n    bookAppointment: \"/patient/appointments/book\",\n    screening: \"/patient/screening\",\n    session: \"/patient/session\",\n    carePlan: \"/patient/care-plan\",\n  },\n\n  provider: {\n    dashboard: \"/provider/dashboard\",\n    notes: \"/provider/notes\",\n    referrals: \"/provider/referrals\",\n  },\n\n  admin: {\n    dashboard: \"/admin/dashboard\",\n    users: \"/admin/users\",\n    reports: \"/admin/reports\",\n    auditLogs: \"/admin/audit-logs\",\n  },\n};\n\nexport const ROUTE_TITLES = {\n  [ROUTES.login]: \"Login\",\n  [ROUTES.register]: \"Register\",\n  [ROUTES.forgotPassword]: \"Forgot Password\",\n  [ROUTES.resetPassword]: \"Reset Password\",\n\n  [ROUTES.patient.dashboard]: \"Patient Dashboard\",\n  [ROUTES.patient.onboarding.consent]: \"Consent\",\n  [ROUTES.patient.onboarding.intake]: \"Intake Form\",\n  [ROUTES.patient.appointments]: \"My Appointments\",\n  [ROUTES.patient.bookAppointment]: \"Book Appointment\",\n  [ROUTES.patient.screening]: \"Screening\",\n  [ROUTES.patient.session]: \"Session Access\",\n  [ROUTES.patient.carePlan]: \"Care Plan\",\n\n  [ROUTES.provider.dashboard]: \"Provider Dashboard\",\n  [ROUTES.provider.notes]: \"Encounter Notes\",\n  [ROUTES.provider.referrals]: \"Provider Referrals\",\n\n  [ROUTES.admin.dashboard]: \"Admin Dashboard\",\n  [ROUTES.admin.users]: \"Users\",\n  [ROUTES.admin.reports]: \"Reports\",\n  [ROUTES.admin.auditLogs]: \"Audit Logs\",\n};\n""", encoding="utf-8")'
```

---

# 14) Create frontend Reset Password page

## New file
- `pbbf-telehealth/src/modules/auth/pages/ResetPassword.jsx`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/modules/auth/pages/ResetPassword.jsx").write_text("""import { useMemo, useState } from \"react\";\nimport { Link, useLocation, useNavigate } from \"react-router-dom\";\n\nimport AuthShell from \"../../../components/layout/AuthShell\";\nimport { ROUTES } from \"../../../shared/constants/routes\";\nimport { useAuth } from \"../hooks/useAuth\";\nimport { hasFormErrors, validateResetPasswordForm } from \"../utils/validators\";\n\nfunction useResetToken() {\n  const location = useLocation();\n  return useMemo(() => new URLSearchParams(location.search).get(\"token\") || \"\", [location.search]);\n}\n\nexport default function ResetPassword() {\n  const navigate = useNavigate();\n  const { resetPassword } = useAuth();\n  const token = useResetToken();\n\n  const [values, setValues] = useState({\n    password: \"\",\n    confirmPassword: \"\",\n  });\n  const [errors, setErrors] = useState({\n    password: \"\",\n    confirmPassword: \"\",\n  });\n  const [serverMessage, setServerMessage] = useState(\"\");\n  const [serverError, setServerError] = useState(\"\");\n  const [isSubmitting, setIsSubmitting] = useState(false);\n\n  function updateField(field, value) {\n    setValues((current) => ({ ...current, [field]: value }));\n    setErrors((current) => ({ ...current, [field]: \"\" }));\n    setServerError(\"\");\n  }\n\n  async function handleSubmit(event) {\n    event.preventDefault();\n    setServerMessage(\"\");\n    setServerError(\"\");\n\n    if (!token) {\n      setServerError(\"Reset link is invalid or missing.\");\n      return;\n    }\n\n    const nextErrors = validateResetPasswordForm(values);\n    setErrors(nextErrors);\n\n    if (hasFormErrors(nextErrors)) return;\n\n    try {\n      setIsSubmitting(true);\n      const response = await resetPassword(token, values.password);\n      const message = response?.data?.message || response?.message || \"Password reset successful.\";\n      setServerMessage(message);\n      setTimeout(() => {\n        navigate(ROUTES.login, { replace: true });\n      }, 1200);\n    } catch (error) {\n      setServerError(error?.message || \"Unable to reset password.\");\n    } finally {\n      setIsSubmitting(false);\n    }\n  }\n\n  return (\n    <AuthShell\n      title=\"Set a new password\"\n      description=\"Choose a strong password for your account.\"\n      sideTitle=\"Secure your account access.\"\n      sideDescription=\"Use the password reset flow to restore account access and return safely to the BLISS telehealth platform.\"\n      footer={\n        <p>\n          Back to{\" \"}\n          <Link to={ROUTES.login} className=\"font-medium text-sky-700 hover:text-sky-800\">\n            sign in\n          </Link>\n        </p>\n      }\n    >\n      <form className=\"space-y-5\" onSubmit={handleSubmit} noValidate>\n        <div>\n          <label htmlFor=\"reset-password\" className=\"mb-2 block text-sm font-medium text-slate-700\">\n            New password\n          </label>\n          <input\n            id=\"reset-password\"\n            name=\"password\"\n            type=\"password\"\n            autoComplete=\"new-password\"\n            value={values.password}\n            onChange={(event) => updateField(\"password\", event.target.value)}\n            className=\"w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100\"\n            placeholder=\"Create a strong password\"\n          />\n          {errors.password ? <p className=\"mt-2 text-sm text-rose-600\">{errors.password}</p> : null}\n        </div>\n\n        <div>\n          <label htmlFor=\"reset-confirm-password\" className=\"mb-2 block text-sm font-medium text-slate-700\">\n            Confirm password\n          </label>\n          <input\n            id=\"reset-confirm-password\"\n            name=\"confirmPassword\"\n            type=\"password\"\n            autoComplete=\"new-password\"\n            value={values.confirmPassword}\n            onChange={(event) => updateField(\"confirmPassword\", event.target.value)}\n            className=\"w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100\"\n            placeholder=\"Re-enter your password\"\n          />\n          {errors.confirmPassword ? <p className=\"mt-2 text-sm text-rose-600\">{errors.confirmPassword}</p> : null}\n        </div>\n\n        {serverError ? (\n          <div className=\"rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700\">\n            {serverError}\n          </div>\n        ) : null}\n\n        {serverMessage ? (\n          <div className=\"rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700\">\n            {serverMessage}\n          </div>\n        ) : null}\n\n        <button\n          type=\"submit\"\n          disabled={isSubmitting}\n          className=\"w-full rounded-xl bg-sky-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70\"\n        >\n          {isSubmitting ? \"Resetting...\" : \"Set new password\"}\n        </button>\n      </form>\n    </AuthShell>\n  );\n}\n""", encoding="utf-8")'
```

---

# 15) Patch frontend Forgot Password page

## Removes placeholder messaging and makes recovery request production-safe

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/modules/auth/pages/ForgotPassword.jsx").write_text("""import { useState } from \"react\";\nimport { Link } from \"react-router-dom\";\n\nimport AuthShell from \"../../../components/layout/AuthShell\";\nimport { ROUTES } from \"../../../shared/constants/routes\";\nimport { validateEmail } from \"../utils/validators\";\nimport { useAuth } from \"../hooks/useAuth\";\n\nexport default function ForgotPassword() {\n  const { requestPasswordReset } = useAuth();\n  const [email, setEmail] = useState(\"\");\n  const [error, setError] = useState(\"\");\n  const [serverMessage, setServerMessage] = useState(\"\");\n  const [isSubmitting, setIsSubmitting] = useState(false);\n\n  async function handleSubmit(event) {\n    event.preventDefault();\n    setServerMessage(\"\");\n\n    const emailError = validateEmail(email);\n    setError(emailError);\n\n    if (emailError) return;\n\n    try {\n      setIsSubmitting(true);\n      const response = await requestPasswordReset(email.trim());\n      setServerMessage(\n        response?.data?.message ||\n          response?.message ||\n          \"If the account exists, password recovery instructions have been sent.\"\n      );\n    } catch (requestError) {\n      setServerMessage(\n        requestError?.message ||\n          \"If the account exists, password recovery instructions have been sent.\"\n      );\n    } finally {\n      setIsSubmitting(false);\n    }\n  }\n\n  return (\n    <AuthShell\n      title=\"Reset your password\"\n      description=\"Enter your email address and we will send you password recovery instructions if the account exists.\"\n      sideTitle=\"Recover account access securely.\"\n      sideDescription=\"Use the password recovery flow to request access restoration without leaving the secure BLISS telehealth workspace.\"\n      footer={\n        <p>\n          Back to{\" \"}\n          <Link to={ROUTES.login} className=\"font-medium text-sky-700 hover:text-sky-800\">\n            sign in\n          </Link>\n        </p>\n      }\n    >\n      <form className=\"space-y-5\" onSubmit={handleSubmit}>\n        <div>\n          <label htmlFor=\"forgot-email\" className=\"mb-2 block text-sm font-medium text-slate-700\">\n            Email address\n          </label>\n          <input\n            id=\"forgot-email\"\n            type=\"email\"\n            value={email}\n            onChange={(event) => setEmail(event.target.value)}\n            className=\"w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100\"\n            placeholder=\"you@example.com\"\n          />\n          {error ? <p className=\"mt-2 text-sm text-rose-600\">{error}</p> : null}\n        </div>\n\n        {serverMessage ? (\n          <div className=\"rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700\">\n            {serverMessage}\n          </div>\n        ) : null}\n\n        <button\n          type=\"submit\"\n          disabled={isSubmitting}\n          className=\"w-full rounded-xl bg-sky-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70\"\n        >\n          {isSubmitting ? \"Submitting...\" : \"Send recovery request\"}\n        </button>\n      </form>\n    </AuthShell>\n  );\n}\n""", encoding="utf-8")'
```

---

# 16) Patch frontend route map

## Adds
- reset-password route import and route entry

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/app/AppRoutes.jsx").write_text("""import { Navigate, Route, Routes } from \"react-router-dom\";\n\nimport AppLayout from \"./AppLayout\";\nimport ProtectedRoute from \"../routes/ProtectedRoute\";\nimport { ROUTES } from \"../shared/constants/routes\";\n\nimport LoginPage from \"../pages/auth/Login\";\nimport RegisterPage from \"../modules/auth/pages/Register\";\nimport ForgotPasswordPage from \"../modules/auth/pages/ForgotPassword\";\nimport ResetPasswordPage from \"../modules/auth/pages/ResetPassword\";\n\nimport ConsentPage from \"../modules/intake/pages/ConsentPage\";\nimport IntakeFormPage from \"../modules/intake/pages/IntakeFormPage\";\n\nimport BookAppointmentPage from \"../modules/appointments/pages/BookAppointmentPage\";\n\nimport PatientDashboardPage from \"../pages/patient/Dashboard\";\nimport PatientAppointmentsPage from \"../pages/patient/Appointments\";\nimport PatientScreeningPage from \"../pages/patient/Screening\";\nimport PatientSessionPage from \"../pages/patient/Session\";\nimport PatientCarePlanPage from \"../pages/patient/CarePlan\";\n\nimport ProviderDashboardPage from \"../pages/provider/Dashboard\";\nimport ProviderNotesPage from \"../pages/provider/Notes\";\nimport ProviderReferralsPage from \"../pages/provider/Referrals\";\n\nimport AdminDashboardPage from \"../pages/admin/Dashboard\";\nimport AdminUsersPage from \"../pages/admin/Users\";\nimport AdminReportsPage from \"../pages/admin/Reports\";\nimport AdminAuditLogsPage from \"../pages/admin/AuditLogs\";\n\nfunction NotFoundPage() {\n  return (\n    <div className=\"rounded-2xl border border-slate-200 bg-white p-8 shadow-sm\">\n      <h1 className=\"text-2xl font-semibold text-slate-900\">Page not found</h1>\n      <p className=\"mt-2 text-sm text-slate-600\">\n        The page you requested does not exist in the current route map.\n      </p>\n    </div>\n  );\n}\n\nexport default function AppRoutes() {\n  return (\n    <Routes>\n      <Route path={ROUTES.root} element={<Navigate to={ROUTES.login} replace />} />\n\n      <Route path={ROUTES.login} element={<LoginPage />} />\n      <Route path={ROUTES.register} element={<RegisterPage />} />\n      <Route path={ROUTES.forgotPassword} element={<ForgotPasswordPage />} />\n      <Route path={ROUTES.resetPassword} element={<ResetPasswordPage />} />\n\n      <Route\n        element={\n          <ProtectedRoute allowedRoles={[\"patient\"]}>\n            <AppLayout />\n          </ProtectedRoute>\n        }\n      >\n        <Route path={ROUTES.patient.dashboard} element={<PatientDashboardPage />} />\n        <Route path={ROUTES.patient.onboarding.consent} element={<ConsentPage />} />\n        <Route path={ROUTES.patient.onboarding.intake} element={<IntakeFormPage />} />\n        <Route path={ROUTES.patient.appointments} element={<PatientAppointmentsPage />} />\n        <Route path={ROUTES.patient.bookAppointment} element={<BookAppointmentPage />} />\n        <Route path={ROUTES.patient.screening} element={<PatientScreeningPage />} />\n        <Route path={ROUTES.patient.session} element={<PatientSessionPage />} />\n        <Route path={ROUTES.patient.carePlan} element={<PatientCarePlanPage />} />\n      </Route>\n\n      <Route\n        element={\n          <ProtectedRoute\n            allowedRoles={[\"provider\", \"counselor\", \"care_coordinator\", \"lactation_consultant\"]}\n          >\n            <AppLayout />\n          </ProtectedRoute>\n        }\n      >\n        <Route path={ROUTES.provider.dashboard} element={<ProviderDashboardPage />} />\n        <Route path={ROUTES.provider.notes} element={<ProviderNotesPage />} />\n        <Route path={ROUTES.provider.referrals} element={<ProviderReferralsPage />} />\n      </Route>\n\n      <Route\n        element={\n          <ProtectedRoute allowedRoles={[\"admin\"]}>\n            <AppLayout />\n          </ProtectedRoute>\n        }\n      >\n        <Route path={ROUTES.admin.dashboard} element={<AdminDashboardPage />} />\n        <Route path={ROUTES.admin.users} element={<AdminUsersPage />} />\n        <Route path={ROUTES.admin.reports} element={<AdminReportsPage />} />\n        <Route path={ROUTES.admin.auditLogs} element={<AdminAuditLogsPage />} />\n        <Route path=\"*\" element={<NotFoundPage />} />\n      </Route>\n\n      <Route path=\"*\" element={<Navigate to={ROUTES.login} replace />} />\n    </Routes>\n  );\n}\n""", encoding="utf-8")'
```

---

# 17) Create frontend auth tests for the new recovery flow

## New test: Forgot password page

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/modules/auth/__tests__/ForgotPasswordPage.test.jsx").write_text("""import { MemoryRouter } from \"react-router-dom\";\nimport { fireEvent, render, screen } from \"@testing-library/react\";\nimport { vi } from \"vitest\";\n\nimport ForgotPassword from \"../pages/ForgotPassword\";\n\nconst requestPasswordResetMock = vi.fn();\n\nvi.mock(\"../hooks/useAuth\", () => ({\n  useAuth: () => ({\n    requestPasswordReset: requestPasswordResetMock,\n  }),\n}));\n\ndescribe(\"ForgotPassword page\", () => {\n  beforeEach(() => {\n    requestPasswordResetMock.mockReset();\n  });\n\n  it(\"shows validation error for empty email\", async () => {\n    render(\n      <MemoryRouter>\n        <ForgotPassword />\n      </MemoryRouter>\n    );\n\n    fireEvent.click(screen.getByRole(\"button\", { name: /send recovery request/i }));\n\n    expect(await screen.findByText(\"Email is required.\")).toBeInTheDocument();\n  });\n\n  it(\"shows success message after request submission\", async () => {\n    requestPasswordResetMock.mockResolvedValue({\n      data: { message: \"If the account exists, password recovery instructions have been sent.\" },\n    });\n\n    render(\n      <MemoryRouter>\n        <ForgotPassword />\n      </MemoryRouter>\n    );\n\n    fireEvent.change(screen.getByLabelText(/email address/i), {\n      target: { value: \"user@example.com\" },\n    });\n\n    fireEvent.click(screen.getByRole(\"button\", { name: /send recovery request/i }));\n\n    expect(await screen.findByText(/password recovery instructions have been sent/i)).toBeInTheDocument();\n  });\n});\n""", encoding="utf-8")'
```

## New test: Reset password page

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/modules/auth/__tests__/ResetPasswordPage.test.jsx").write_text("""import { MemoryRouter } from \"react-router-dom\";\nimport { fireEvent, render, screen } from \"@testing-library/react\";\nimport { vi } from \"vitest\";\n\nimport ResetPassword from \"../pages/ResetPassword\";\n\nconst resetPasswordMock = vi.fn();\n\nvi.mock(\"../hooks/useAuth\", () => ({\n  useAuth: () => ({\n    resetPassword: resetPasswordMock,\n  }),\n}));\n\ndescribe(\"ResetPassword page\", () => {\n  beforeEach(() => {\n    resetPasswordMock.mockReset();\n  });\n\n  it(\"shows mismatch validation error\", async () => {\n    render(\n      <MemoryRouter initialEntries={[\"/reset-password?token=test-token\"]}>\n        <ResetPassword />\n      </MemoryRouter>\n    );\n\n    fireEvent.change(screen.getByLabelText(/new password/i), {\n      target: { value: \"StrongPass123\" },\n    });\n    fireEvent.change(screen.getByLabelText(/confirm password/i), {\n      target: { value: \"Different123\" },\n    });\n\n    fireEvent.click(screen.getByRole(\"button\", { name: /set new password/i }));\n\n    expect(await screen.findByText(\"Passwords do not match.\")).toBeInTheDocument();\n  });\n\n  it(\"submits reset password successfully\", async () => {\n    resetPasswordMock.mockResolvedValue({\n      data: { message: \"Password has been reset successfully. You can now sign in with your new password.\" },\n    });\n\n    render(\n      <MemoryRouter initialEntries={[\"/reset-password?token=test-token\"]}>\n        <ResetPassword />\n      </MemoryRouter>\n    );\n\n    fireEvent.change(screen.getByLabelText(/new password/i), {\n      target: { value: \"StrongPass123\" },\n    });\n    fireEvent.change(screen.getByLabelText(/confirm password/i), {\n      target: { value: \"StrongPass123\" },\n    });\n\n    fireEvent.click(screen.getByRole(\"button\", { name: /set new password/i }));\n\n    expect(await screen.findByText(/password has been reset successfully/i)).toBeInTheDocument();\n  });\n});\n""", encoding="utf-8")'
```

---

# 18) Inspect the patched/new files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

sed -n '1,260p' pbbf-api/app/modules/auth/repository.py
sed -n '1,420p' pbbf-api/app/modules/auth/schemas.py
sed -n '1,520p' pbbf-api/app/modules/auth/service.py
sed -n '1,320p' pbbf-api/app/modules/auth/router.py
sed -n '1,420p' pbbf-api/app/modules/notifications/service.py
sed -n '1,420p' pbbf-api/app/common/utils/security.py
sed -n '1,220p' pbbf-api/app/modules/auth/tokens.py

sed -n '1,220p' pbbf-telehealth/src/modules/auth/services/authApi.js
sed -n '1,320p' pbbf-telehealth/src/services/auth.service.js
sed -n '1,220p' pbbf-telehealth/src/modules/auth/hooks/useAuth.js
sed -n '1,320p' pbbf-telehealth/src/modules/auth/utils/validators.js
sed -n '1,320p' pbbf-telehealth/src/modules/auth/pages/ForgotPassword.jsx
sed -n '1,360p' pbbf-telehealth/src/modules/auth/pages/ResetPassword.jsx
sed -n '1,260p' pbbf-telehealth/src/shared/constants/routes.js
sed -n '1,340p' pbbf-telehealth/src/app/AppRoutes.jsx
sed -n '1,260p' pbbf-telehealth/src/modules/auth/__tests__/ForgotPasswordPage.test.jsx
sed -n '1,260p' pbbf-telehealth/src/modules/auth/__tests__/ResetPasswordPage.test.jsx
```

---

# 19) Validate backend syntax

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
source .venv/bin/activate
python -m py_compile \
  app/modules/auth/repository.py \
  app/modules/auth/schemas.py \
  app/modules/auth/service.py \
  app/modules/auth/router.py \
  app/modules/auth/tokens.py \
  app/modules/notifications/service.py \
  app/common/utils/security.py
```

---

# 20) Run frontend auth tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm test -- --run src/modules/auth/__tests__/ForgotPasswordPage.test.jsx src/modules/auth/__tests__/ResetPasswordPage.test.jsx src/modules/auth/__tests__/LoginForm.test.jsx src/modules/auth/__tests__/RegisterForm.test.jsx src/modules/auth/__tests__/AuthGuard.test.jsx src/modules/auth/__tests__/RoleGuard.test.jsx src/modules/auth/__tests__/SessionExpiry.test.jsx
```

If your script rejects multiple file arguments, run:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npx vitest run src/modules/auth/__tests__/ForgotPasswordPage.test.jsx src/modules/auth/__tests__/ResetPasswordPage.test.jsx src/modules/auth/__tests__/LoginForm.test.jsx src/modules/auth/__tests__/RegisterForm.test.jsx src/modules/auth/__tests__/AuthGuard.test.jsx src/modules/auth/__tests__/RoleGuard.test.jsx src/modules/auth/__tests__/SessionExpiry.test.jsx
```

---

# 21) Build the frontend

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm run build
```

---

# 22) Manual verification checklist

```text
[ ] Forgot Password page submits any email and always shows the generic safe message.
[ ] Existing/inactive/nonexistent emails do not reveal account existence.
[ ] Notification row is created for an existing active user requesting recovery.
[ ] Reset link resolves to /reset-password?token=...
[ ] Reset Password page validates password + confirmation.
[ ] Backend rejects invalid/expired reset tokens.
[ ] Successful reset changes password and allows login with the new password.
[ ] Audit events exist for password_reset_requested and password_reset_completed.
```

---

# 23) Completion checklist for Phase 2

```text
[ ] /auth/forgot-password exists.
[ ] /auth/reset-password exists.
[ ] Password reset token helper exists in security/tokens layer.
[ ] Auth repository can update password hashes.
[ ] Password reset request queues notification email.
[ ] ForgotPassword frontend no longer says the feature is unavailable.
[ ] Reset password page exists and is routable.
[ ] Frontend auth tests pass.
[ ] Backend py_compile passes.
[ ] Frontend build passes.
```

---

# 24) Production note
This Phase 2 pack deliberately implements a **real reset completion flow**, not just a request-only placeholder, because the release intent is production readiness. It still avoids creating a new database table by using a short-lived signed reset token over the existing JWT utility framework. Ensure `PBBF_BASE_EXTERNAL_URL` is configured appropriately in non-local environments so the reset link in queued notifications points to the correct frontend host. citeturn79search1
