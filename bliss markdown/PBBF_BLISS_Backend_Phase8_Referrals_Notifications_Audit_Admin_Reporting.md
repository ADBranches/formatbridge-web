
# PBBF BLISS — Backend Phase 8 Populated Files
## Referrals, Notifications, Audit, and Admin Reporting

This markdown packages the **fully populated Phase 8 backend files** for the BLISS / PBBF Telehealth backend.

### Phase objective
Complete the operational backbone required for follow-up, accountability, and basic reporting.

### Existing modules completed in this phase
- `app/modules/referrals`
- `app/modules/notifications`
- `app/modules/audit`
- `app/modules/admin`

### Important implementation note
This phase assumes your earlier phases already provide:
- working FastAPI app boot and router registration
- SQLAlchemy models exported from `app/db/models/__init__.py`
- authentication utilities from Phase 3
- intake, appointment, screening, telehealth, and encounter workflows from earlier phases

If your actual Phase 2 model field names differ from the assumptions below, align the field names before running tests.

---

## 1) `app/modules/referrals/router.py`

```python
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.referrals.schemas import (
    ReferralCreateRequest,
    ReferralListResponse,
    ReferralResponse,
    ReferralStatusUpdateRequest,
)
from app.modules.referrals.service import ReferralService

router = APIRouter(prefix="/api/v1/referrals", tags=["referrals"])


@router.post(
    "/",
    response_model=ReferralResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_referral(
    payload: ReferralCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ReferralService(db)
    return service.create_referral(payload=payload, actor=current_user)


@router.get("/", response_model=ReferralListResponse)
def list_referrals(
    patient_id: int | None = Query(default=None),
    status_filter: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ReferralService(db)
    items = service.list_referrals(
        actor=current_user,
        patient_id=patient_id,
        status_filter=status_filter,
    )
    return ReferralListResponse(items=items, total=len(items))


@router.get("/{referral_id}", response_model=ReferralResponse)
def get_referral(
    referral_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ReferralService(db)
    return service.get_referral(referral_id=referral_id, actor=current_user)


@router.patch("/{referral_id}/status", response_model=ReferralResponse)
def update_referral_status(
    referral_id: int,
    payload: ReferralStatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ReferralService(db)
    return service.update_referral_status(
        referral_id=referral_id,
        payload=payload,
        actor=current_user,
    )
```

---

## 2) `app/modules/referrals/schemas.py`

```python
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ReferralCategory(str, Enum):
    MENTAL_HEALTH = "mental_health"
    LACTATION = "lactation"
    WELLNESS_FOLLOW_UP = "wellness_follow_up"
    COMMUNITY_SUPPORT = "community_support"
    FOOD = "food"
    HOUSING = "housing"
    COUNSELING = "counseling"
    CLINIC = "clinic"
    OTHER = "other"


class ReferralStatus(str, Enum):
    CREATED = "created"
    SENT = "sent"
    ACKNOWLEDGED = "acknowledged"
    COMPLETED = "completed"
    CLOSED = "closed"


class ReferralCreateRequest(BaseModel):
    patient_id: int = Field(..., gt=0)
    encounter_id: int | None = Field(default=None, gt=0)
    category: ReferralCategory
    destination_name: str = Field(..., min_length=2, max_length=255)
    destination_contact: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=5000)
    follow_up_at: datetime | None = None


class ReferralStatusUpdateRequest(BaseModel):
    status: ReferralStatus
    completion_outcome: str | None = Field(default=None, max_length=3000)
    notes: str | None = Field(default=None, max_length=3000)


class ReferralResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    encounter_id: int | None = None
    created_by_user_id: int
    category: str
    destination_name: str
    destination_contact: str | None = None
    notes: str | None = None
    status: str
    follow_up_at: datetime | None = None
    completion_outcome: str | None = None
    created_at: datetime
    updated_at: datetime


class ReferralListResponse(BaseModel):
    items: list[ReferralResponse]
    total: int
```

---

## 3) `app/modules/referrals/service.py`

```python
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Encounter, Patient, Referral, User
from app.modules.audit.service import AuditService
from app.modules.notifications.service import NotificationService
from app.modules.referrals.repository import ReferralRepository
from app.modules.referrals.schemas import (
    ReferralCreateRequest,
    ReferralStatus,
    ReferralStatusUpdateRequest,
)


ALLOWED_CREATE_ROLES = {"provider", "care_coordinator", "admin"}
ALLOWED_UPDATE_ROLES = {"provider", "care_coordinator", "admin"}


class ReferralService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ReferralRepository(db)
        self.audit_service = AuditService(db)
        self.notification_service = NotificationService(db)

    @staticmethod
    def _role_name(user: User) -> str:
        if hasattr(user, "role_name") and user.role_name:
            return str(user.role_name).lower()
        if hasattr(user, "role") and user.role and hasattr(user.role, "name"):
            return str(user.role.name).lower()
        return "patient"

    def _require_role(self, actor: User, allowed: set[str]) -> None:
        role_name = self._role_name(actor)
        if role_name not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to perform this action.",
            )

    def _ensure_patient_exists(self, patient_id: int) -> Patient:
        patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found.",
            )
        return patient

    def _ensure_encounter_exists(self, encounter_id: int | None) -> Encounter | None:
        if not encounter_id:
            return None
        encounter = self.db.query(Encounter).filter(Encounter.id == encounter_id).first()
        if not encounter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Encounter not found.",
            )
        return encounter

    def create_referral(self, payload: ReferralCreateRequest, actor: User) -> Referral:
        self._require_role(actor, ALLOWED_CREATE_ROLES)

        patient = self._ensure_patient_exists(payload.patient_id)
        encounter = self._ensure_encounter_exists(payload.encounter_id)

        referral = self.repository.create(
            patient_id=patient.id,
            encounter_id=encounter.id if encounter else None,
            created_by_user_id=actor.id,
            category=payload.category.value,
            destination_name=payload.destination_name,
            destination_contact=payload.destination_contact,
            notes=payload.notes,
            status=ReferralStatus.CREATED.value,
            follow_up_at=payload.follow_up_at,
        )

        self.audit_service.log_event(
            actor_user_id=actor.id,
            action="referral.created",
            entity_type="referral",
            entity_id=referral.id,
            details={
                "patient_id": patient.id,
                "category": referral.category,
                "status": referral.status,
                "destination_name": referral.destination_name,
            },
        )

        self.notification_service.create_referral_follow_up_hook(
            referral=referral,
            actor=actor,
        )

        return referral

    def get_referral(self, referral_id: int, actor: User) -> Referral:
        referral = self.repository.get_by_id(referral_id)
        if not referral:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Referral not found.",
            )

        role_name = self._role_name(actor)
        if role_name == "patient":
            patient_profile = getattr(actor, "patient_profile", None)
            if not patient_profile or patient_profile.id != referral.patient_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not allowed to view this referral.",
                )

        return referral

    def list_referrals(
        self,
        actor: User,
        patient_id: int | None = None,
        status_filter: str | None = None,
    ) -> list[Referral]:
        role_name = self._role_name(actor)

        if role_name == "patient":
            patient_profile = getattr(actor, "patient_profile", None)
            if not patient_profile:
                return []
            return self.repository.list_for_patient(
                patient_id=patient_profile.id,
                status_filter=status_filter,
            )

        if role_name in {"provider", "care_coordinator", "admin"}:
            if patient_id:
                return self.repository.list_for_patient(
                    patient_id=patient_id,
                    status_filter=status_filter,
                )
            return self.repository.list_all(status_filter=status_filter)

        return []

    def update_referral_status(
        self,
        referral_id: int,
        payload: ReferralStatusUpdateRequest,
        actor: User,
    ) -> Referral:
        self._require_role(actor, ALLOWED_UPDATE_ROLES)

        referral = self.repository.get_by_id(referral_id)
        if not referral:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Referral not found.",
            )

        updated = self.repository.update_status(
            referral=referral,
            status_value=payload.status.value,
            completion_outcome=payload.completion_outcome,
            notes=payload.notes,
        )

        self.audit_service.log_event(
            actor_user_id=actor.id,
            action="referral.status_updated",
            entity_type="referral",
            entity_id=updated.id,
            details={
                "status": updated.status,
                "completion_outcome": updated.completion_outcome,
            },
        )

        return updated
```

---

## 4) `app/modules/referrals/repository.py`

```python
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.models import Referral
from app.common.utils.datetime import utcnow


class ReferralRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        patient_id: int,
        encounter_id: int | None,
        created_by_user_id: int,
        category: str,
        destination_name: str,
        destination_contact: str | None,
        notes: str | None,
        status: str,
        follow_up_at,
    ) -> Referral:
        referral = Referral(
            patient_id=patient_id,
            encounter_id=encounter_id,
            created_by_user_id=created_by_user_id,
            category=category,
            destination_name=destination_name,
            destination_contact=destination_contact,
            notes=notes,
            status=status,
            follow_up_at=follow_up_at,
        )
        self.db.add(referral)
        self.db.commit()
        self.db.refresh(referral)
        return referral

    def get_by_id(self, referral_id: int) -> Referral | None:
        return self.db.query(Referral).filter(Referral.id == referral_id).first()

    def list_all(self, status_filter: str | None = None) -> list[Referral]:
        query = self.db.query(Referral)
        if status_filter:
            query = query.filter(Referral.status == status_filter)
        return query.order_by(desc(Referral.created_at)).all()

    def list_for_patient(
        self,
        patient_id: int,
        status_filter: str | None = None,
    ) -> list[Referral]:
        query = self.db.query(Referral).filter(Referral.patient_id == patient_id)
        if status_filter:
            query = query.filter(Referral.status == status_filter)
        return query.order_by(desc(Referral.created_at)).all()

    def update_status(
        self,
        *,
        referral: Referral,
        status_value: str,
        completion_outcome: str | None,
        notes: str | None,
    ) -> Referral:
        referral.status = status_value
        if completion_outcome is not None:
            referral.completion_outcome = completion_outcome
        if notes is not None:
            referral.notes = notes
        referral.updated_at = utcnow()

        self.db.add(referral)
        self.db.commit()
        self.db.refresh(referral)
        return referral
```

---

## 5) `app/modules/notifications/router.py`

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.notifications.schemas import (
    NotificationCreateRequest,
    NotificationListResponse,
    NotificationResponse,
)
from app.modules.notifications.service import NotificationService

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(
    payload: NotificationCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = NotificationService(db)
    return service.create_notification(payload=payload, actor=current_user)


@router.get("/me", response_model=NotificationListResponse)
def list_my_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = NotificationService(db)
    items = service.list_for_user(current_user.id)
    return NotificationListResponse(items=items, total=len(items))


@router.post("/{notification_id}/dispatch", response_model=NotificationResponse)
def dispatch_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = NotificationService(db)
    return service.dispatch_notification(notification_id=notification_id, actor=current_user)
```

---

## 6) `app/modules/notifications/schemas.py`

```python
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"


class NotificationType(str, Enum):
    GENERIC = "generic"
    APPOINTMENT_CONFIRMATION = "appointment_confirmation"
    APPOINTMENT_REMINDER = "appointment_reminder"
    APPOINTMENT_CANCELLATION = "appointment_cancellation"
    MISSED_VISIT_FOLLOW_UP = "missed_visit_follow_up"
    REFERRAL_FOLLOW_UP = "referral_follow_up"


class NotificationCreateRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    channel: NotificationChannel
    body: str = Field(..., min_length=1, max_length=4000)
    subject: str | None = Field(default=None, max_length=255)
    notification_type: NotificationType = NotificationType.GENERIC
    scheduled_for: datetime | None = None
    metadata: dict = Field(default_factory=dict)


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    channel: str
    notification_type: str
    subject: str | None = None
    body: str
    status: str
    metadata_json: dict | None = None
    provider_message_id: str | None = None
    failure_reason: str | None = None
    scheduled_for: datetime | None = None
    delivered_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
```

---

## 7) `app/modules/notifications/service.py`

```python
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Notification, Patient, Referral, User
from app.modules.audit.service import AuditService
from app.modules.notifications.channels import dispatch_channel_message
from app.modules.notifications.repository import NotificationRepository
from app.modules.notifications.schemas import (
    NotificationCreateRequest,
    NotificationStatus,
)
from app.modules.notifications.tasks import build_referral_follow_up_notification


class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = NotificationRepository(db)
        self.audit_service = AuditService(db)

    @staticmethod
    def _role_name(user: User) -> str:
        if hasattr(user, "role_name") and user.role_name:
            return str(user.role_name).lower()
        if hasattr(user, "role") and user.role and hasattr(user.role, "name"):
            return str(user.role.name).lower()
        return "patient"

    def _require_actor_can_send(self, actor: User) -> None:
        role_name = self._role_name(actor)
        if role_name not in {"provider", "care_coordinator", "admin"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to create notifications.",
            )

    def create_notification(
        self,
        payload: NotificationCreateRequest,
        actor: User,
    ) -> Notification:
        self._require_actor_can_send(actor)

        notification = self.repository.create(
            user_id=payload.user_id,
            channel=payload.channel.value,
            notification_type=payload.notification_type.value,
            subject=payload.subject,
            body=payload.body,
            status=NotificationStatus.PENDING.value,
            metadata_json=payload.metadata,
            scheduled_for=payload.scheduled_for,
        )

        self.audit_service.log_event(
            actor_user_id=actor.id,
            action="notification.created",
            entity_type="notification",
            entity_id=notification.id,
            details={
                "user_id": notification.user_id,
                "channel": notification.channel,
                "notification_type": notification.notification_type,
            },
        )

        return notification

    def list_for_user(self, user_id: int) -> list[Notification]:
        return self.repository.list_for_user(user_id)

    def dispatch_notification(self, notification_id: int, actor: User) -> Notification:
        notification = self.repository.get_by_id(notification_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found.",
            )

        role_name = self._role_name(actor)
        if role_name == "patient" and actor.id != notification.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to dispatch this notification.",
            )

        try:
            dispatch_result = dispatch_channel_message(
                channel=notification.channel,
                notification=notification,
            )
            notification = self.repository.mark_sent(
                notification=notification,
                provider_message_id=dispatch_result["provider_message_id"],
            )
        except Exception as exc:  # pragma: no cover
            notification = self.repository.mark_failed(
                notification=notification,
                failure_reason=str(exc),
            )

        self.audit_service.log_event(
            actor_user_id=actor.id,
            action="notification.dispatched",
            entity_type="notification",
            entity_id=notification.id,
            details={
                "status": notification.status,
                "channel": notification.channel,
            },
        )
        return notification

    def create_referral_follow_up_hook(self, referral: Referral, actor: User) -> Notification | None:
        patient = self.db.query(Patient).filter(Patient.id == referral.patient_id).first()
        if not patient:
            return None

        patient_user_id = getattr(patient, "user_id", None)
        if not patient_user_id:
            return None

        payload = build_referral_follow_up_notification(
            referral=referral,
            patient_user_id=patient_user_id,
        )

        notification = self.repository.create(
            user_id=payload["user_id"],
            channel=payload["channel"],
            notification_type=payload["notification_type"],
            subject=payload["subject"],
            body=payload["body"],
            status=NotificationStatus.PENDING.value,
            metadata_json=payload["metadata"],
            scheduled_for=payload["scheduled_for"],
        )

        self.audit_service.log_event(
            actor_user_id=actor.id,
            action="notification.referral_follow_up_created",
            entity_type="notification",
            entity_id=notification.id,
            details={
                "referral_id": referral.id,
                "user_id": notification.user_id,
            },
        )

        return notification
```

---

## 8) `app/modules/notifications/repository.py`

```python
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.common.utils.datetime import utcnow
from app.db.models import Notification


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        user_id: int,
        channel: str,
        notification_type: str,
        subject: str | None,
        body: str,
        status: str,
        metadata_json: dict | None,
        scheduled_for,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            channel=channel,
            notification_type=notification_type,
            subject=subject,
            body=body,
            status=status,
            metadata_json=metadata_json or {},
            scheduled_for=scheduled_for,
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_by_id(self, notification_id: int) -> Notification | None:
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def list_for_user(self, user_id: int) -> list[Notification]:
        return (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(desc(Notification.created_at))
            .all()
        )

    def mark_sent(self, *, notification: Notification, provider_message_id: str) -> Notification:
        notification.status = "sent"
        notification.provider_message_id = provider_message_id
        notification.delivered_at = utcnow()
        notification.updated_at = utcnow()

        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_failed(self, *, notification: Notification, failure_reason: str) -> Notification:
        notification.status = "failed"
        notification.failure_reason = failure_reason
        notification.updated_at = utcnow()

        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
```

---

## 9) `app/modules/notifications/channels.py`

```python
from uuid import uuid4


def _fake_provider_message_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def dispatch_email(notification) -> dict:
    return {
        "provider_message_id": _fake_provider_message_id("email"),
        "status": "queued",
    }


def dispatch_sms(notification) -> dict:
    return {
        "provider_message_id": _fake_provider_message_id("sms"),
        "status": "queued",
    }


def dispatch_in_app(notification) -> dict:
    return {
        "provider_message_id": _fake_provider_message_id("inapp"),
        "status": "queued",
    }


def dispatch_channel_message(*, channel: str, notification) -> dict:
    if channel == "email":
        return dispatch_email(notification)
    if channel == "sms":
        return dispatch_sms(notification)
    if channel == "in_app":
        return dispatch_in_app(notification)
    raise ValueError(f"Unsupported notification channel: {channel}")
```

---

## 10) `app/modules/notifications/tasks.py`

```python
from datetime import timedelta

from app.common.utils.datetime import utcnow


def build_referral_follow_up_notification(*, referral, patient_user_id: int) -> dict:
    scheduled_for = referral.follow_up_at or (utcnow() + timedelta(hours=24))

    return {
        "user_id": patient_user_id,
        "channel": "email",
        "notification_type": "referral_follow_up",
        "subject": "Referral follow-up reminder",
        "body": (
            f"You have a referral for {referral.category.replace('_', ' ')} "
            f"to {referral.destination_name}. Please review your next steps."
        ),
        "scheduled_for": scheduled_for,
        "metadata": {
            "referral_id": referral.id,
            "patient_id": referral.patient_id,
            "destination_name": referral.destination_name,
        },
    }
```

---

## 11) `app/modules/audit/router.py`

```python
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.audit.schemas import AuditLogListResponse
from app.modules.audit.service import AuditService
from app.modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/audit", tags=["audit"])


@router.get("/", response_model=AuditLogListResponse)
def list_audit_events(
    action: str | None = Query(default=None),
    entity_type: str | None = Query(default=None),
    actor_user_id: int | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = AuditService(db)
    items = service.list_events(
        actor=current_user,
        action=action,
        entity_type=entity_type,
        actor_user_id=actor_user_id,
        date_from=date_from,
        date_to=date_to,
    )
    return AuditLogListResponse(items=items, total=len(items))


@router.get("/me", response_model=AuditLogListResponse)
def list_my_audit_events(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = AuditService(db)
    items = service.list_events(actor=current_user, actor_user_id=current_user.id)
    return AuditLogListResponse(items=items, total=len(items))
```

---

## 12) `app/modules/audit/schemas.py`

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    actor_user_id: int | None = None
    action: str
    entity_type: str
    entity_id: int | None = None
    details_json: dict | None = None
    ip_address: str | None = None
    request_id: str | None = None
    created_at: datetime


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
```

---

## 13) `app/modules/audit/service.py`

```python
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import AuditLog, User
from app.modules.audit.repository import AuditRepository


class AuditService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AuditRepository(db)

    @staticmethod
    def _role_name(user: User) -> str:
        if hasattr(user, "role_name") and user.role_name:
            return str(user.role_name).lower()
        if hasattr(user, "role") and user.role and hasattr(user.role, "name"):
            return str(user.role.name).lower()
        return "patient"

    def log_event(
        self,
        *,
        actor_user_id: int | None,
        action: str,
        entity_type: str,
        entity_id: int | None = None,
        details: dict | None = None,
        ip_address: str | None = None,
        request_id: str | None = None,
    ) -> AuditLog:
        return self.repository.create(
            actor_user_id=actor_user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details_json=details or {},
            ip_address=ip_address,
            request_id=request_id,
        )

    def list_events(
        self,
        *,
        actor: User,
        action: str | None = None,
        entity_type: str | None = None,
        actor_user_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[AuditLog]:
        role_name = self._role_name(actor)

        if role_name != "admin":
            if actor_user_id and actor_user_id != actor.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not allowed to view these audit events.",
                )
            actor_user_id = actor.id

        return self.repository.list_events(
            action=action,
            entity_type=entity_type,
            actor_user_id=actor_user_id,
            date_from=date_from,
            date_to=date_to,
        )
```

---

## 14) `app/modules/audit/repository.py`

```python
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.models import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        actor_user_id: int | None,
        action: str,
        entity_type: str,
        entity_id: int | None,
        details_json: dict | None,
        ip_address: str | None,
        request_id: str | None,
    ) -> AuditLog:
        log = AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details_json=details_json or {},
            ip_address=ip_address,
            request_id=request_id,
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def list_events(
        self,
        *,
        action: str | None = None,
        entity_type: str | None = None,
        actor_user_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[AuditLog]:
        query = self.db.query(AuditLog)

        if action:
            query = query.filter(AuditLog.action == action)
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        if actor_user_id:
            query = query.filter(AuditLog.actor_user_id == actor_user_id)
        if date_from:
            query = query.filter(AuditLog.created_at >= date_from)
        if date_to:
            query = query.filter(AuditLog.created_at <= date_to)

        return query.order_by(desc(AuditLog.created_at)).all()
```

---

## 15) `app/modules/admin/router.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.admin.schemas import AdminDashboardSummaryResponse
from app.modules.admin.service import AdminService
from app.modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/dashboard/summary", response_model=AdminDashboardSummaryResponse)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = AdminService(db)
    return service.get_dashboard_summary(actor=current_user)
```

---

## 16) `app/modules/admin/schemas.py`

```python
from pydantic import BaseModel


class AdminDashboardSummaryResponse(BaseModel):
    total_users: int
    total_patients: int
    total_providers: int
    total_appointments: int
    completed_telehealth_visits: int
    no_show_rate: float
    epds_completion_rate: float
    referral_completion_rate: float
    notifications_sent: int
    audit_events_last_7_days: int
```

---

## 17) `app/modules/admin/service.py`

```python
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import User
from app.modules.admin.metrics import safe_rate
from app.modules.admin.repository import AdminRepository


class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AdminRepository(db)

    @staticmethod
    def _role_name(user: User) -> str:
        if hasattr(user, "role_name") and user.role_name:
            return str(user.role_name).lower()
        if hasattr(user, "role") and user.role and hasattr(user.role, "name"):
            return str(user.role.name).lower()
        return "patient"

    def get_dashboard_summary(self, actor: User) -> dict:
        if self._role_name(actor) != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access is required.",
            )

        raw = self.repository.fetch_dashboard_counts()

        return {
            "total_users": raw["total_users"],
            "total_patients": raw["total_patients"],
            "total_providers": raw["total_providers"],
            "total_appointments": raw["total_appointments"],
            "completed_telehealth_visits": raw["completed_telehealth_visits"],
            "no_show_rate": safe_rate(raw["no_show_appointments"], raw["total_appointments"]),
            "epds_completion_rate": safe_rate(raw["completed_epds"], raw["total_patients"]),
            "referral_completion_rate": safe_rate(raw["completed_referrals"], raw["total_referrals"]),
            "notifications_sent": raw["notifications_sent"],
            "audit_events_last_7_days": raw["audit_events_last_7_days"],
        }
```

---

## 18) `app/modules/admin/repository.py`

```python
from datetime import timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.utils.datetime import utcnow
from app.db.models import (
    Appointment,
    AuditLog,
    Notification,
    Patient,
    Provider,
    Referral,
    Screening,
    TelehealthSession,
    User,
)


class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    def fetch_dashboard_counts(self) -> dict:
        now = utcnow()
        seven_days_ago = now - timedelta(days=7)

        total_users = self.db.query(func.count(User.id)).scalar() or 0
        total_patients = self.db.query(func.count(Patient.id)).scalar() or 0
        total_providers = self.db.query(func.count(Provider.id)).scalar() or 0
        total_appointments = self.db.query(func.count(Appointment.id)).scalar() or 0

        no_show_appointments = (
            self.db.query(func.count(Appointment.id))
            .filter(Appointment.status == "no_show")
            .scalar()
            or 0
        )

        completed_telehealth_visits = (
            self.db.query(func.count(TelehealthSession.id))
            .filter(TelehealthSession.status == "ended")
            .scalar()
            or 0
        )

        completed_epds = (
            self.db.query(func.count(Screening.id))
            .filter(
                Screening.screening_type == "epds",
                Screening.status == "completed",
            )
            .scalar()
            or 0
        )

        total_referrals = self.db.query(func.count(Referral.id)).scalar() or 0
        completed_referrals = (
            self.db.query(func.count(Referral.id))
            .filter(Referral.status == "completed")
            .scalar()
            or 0
        )

        notifications_sent = (
            self.db.query(func.count(Notification.id))
            .filter(Notification.status == "sent")
            .scalar()
            or 0
        )

        audit_events_last_7_days = (
            self.db.query(func.count(AuditLog.id))
            .filter(AuditLog.created_at >= seven_days_ago)
            .scalar()
            or 0
        )

        return {
            "total_users": int(total_users),
            "total_patients": int(total_patients),
            "total_providers": int(total_providers),
            "total_appointments": int(total_appointments),
            "no_show_appointments": int(no_show_appointments),
            "completed_telehealth_visits": int(completed_telehealth_visits),
            "completed_epds": int(completed_epds),
            "total_referrals": int(total_referrals),
            "completed_referrals": int(completed_referrals),
            "notifications_sent": int(notifications_sent),
            "audit_events_last_7_days": int(audit_events_last_7_days),
        }
```

---

## 19) `app/modules/admin/metrics.py`

```python
def safe_rate(numerator: int, denominator: int, decimals: int = 2) -> float:
    if denominator <= 0:
        return 0.0
    return round((numerator / denominator) * 100, decimals)
```

---

## 20) `tests/modules/referrals/test_create_referral.py`

```python
def test_create_referral_success(client, provider_headers, patient_profile):
    payload = {
        "patient_id": patient_profile.id,
        "encounter_id": None,
        "category": "mental_health",
        "destination_name": "Community Wellness Partner",
        "destination_contact": "partner@example.org",
        "notes": "Initial referral from provider",
    }

    response = client.post(
        "/api/v1/referrals/",
        json=payload,
        headers=provider_headers,
    )

    assert response.status_code == 201, response.text
    body = response.json()
    assert body["patient_id"] == patient_profile.id
    assert body["status"] == "created"
    assert body["category"] == "mental_health"
    assert body["destination_name"] == "Community Wellness Partner"
```

---

## 21) `tests/modules/referrals/test_update_referral_status.py`

```python
def test_update_referral_status_success(
    client,
    provider_headers,
    care_coordinator_headers,
    patient_profile,
):
    create_payload = {
        "patient_id": patient_profile.id,
        "encounter_id": None,
        "category": "community_support",
        "destination_name": "Family Support Desk",
        "notes": "Needs follow-up coordination",
    }

    create_response = client.post(
        "/api/v1/referrals/",
        json=create_payload,
        headers=provider_headers,
    )
    assert create_response.status_code == 201, create_response.text

    referral_id = create_response.json()["id"]

    update_response = client.patch(
        f"/api/v1/referrals/{referral_id}/status",
        json={
            "status": "acknowledged",
            "completion_outcome": None,
            "notes": "Partner confirmed intake received.",
        },
        headers=care_coordinator_headers,
    )

    assert update_response.status_code == 200, update_response.text
    data = update_response.json()
    assert data["status"] == "acknowledged"
    assert data["notes"] == "Partner confirmed intake received."
```

---

## 22) `tests/modules/notifications/test_reminder_creation.py`

```python
def test_referral_follow_up_notification_created(
    client,
    provider_headers,
    patient_profile,
    db_session,
):
    from app.db.models import Notification

    create_payload = {
        "patient_id": patient_profile.id,
        "encounter_id": None,
        "category": "lactation",
        "destination_name": "Lactation Resource Center",
        "notes": "Please schedule support session.",
    }

    response = client.post(
        "/api/v1/referrals/",
        json=create_payload,
        headers=provider_headers,
    )

    assert response.status_code == 201, response.text

    notifications = (
        db_session.query(Notification)
        .filter(Notification.notification_type == "referral_follow_up")
        .all()
    )

    assert len(notifications) >= 1
    assert notifications[-1].status == "pending"
```

---

## 23) `tests/modules/audit/test_audit_logging.py`

```python
def test_audit_log_written_after_referral_create(
    client,
    provider_headers,
    patient_profile,
    db_session,
):
    from app.db.models import AuditLog

    payload = {
        "patient_id": patient_profile.id,
        "encounter_id": None,
        "category": "housing",
        "destination_name": "Safe Start Housing Desk",
        "notes": "Urgent social support referral",
    }

    response = client.post(
        "/api/v1/referrals/",
        json=payload,
        headers=provider_headers,
    )

    assert response.status_code == 201, response.text

    log = (
        db_session.query(AuditLog)
        .filter(AuditLog.action == "referral.created")
        .order_by(AuditLog.id.desc())
        .first()
    )

    assert log is not None
    assert log.entity_type == "referral"
    assert log.details_json["category"] == "housing"
```

---

## 24) `tests/modules/admin/test_dashboard_metrics.py`

```python
def test_admin_dashboard_summary(client, admin_headers):
    response = client.get("/api/v1/admin/dashboard/summary", headers=admin_headers)
    assert response.status_code == 200, response.text

    data = response.json()
    expected_keys = {
        "total_users",
        "total_patients",
        "total_providers",
        "total_appointments",
        "completed_telehealth_visits",
        "no_show_rate",
        "epds_completion_rate",
        "referral_completion_rate",
        "notifications_sent",
        "audit_events_last_7_days",
    }

    assert expected_keys.issubset(set(data.keys()))
```

---

## Suggested `tests/conftest.py` add-ons for this phase

Append the following **only if your current Phase 1–7 conftest does not already provide equivalent fixtures**.

```python
import uuid

import pytest
from sqlalchemy.orm import Session

from app.db.models import Patient, Provider


@pytest.fixture
def patient_profile(db_session: Session, patient_user):
    profile = db_session.query(Patient).filter(Patient.user_id == patient_user.id).first()
    if not profile:
        profile = Patient(
            user_id=patient_user.id,
            first_name="Phase8",
            last_name="Patient",
            preferred_contact_method="email",
            intake_status="ready_to_schedule",
        )
        db_session.add(profile)
        db_session.commit()
        db_session.refresh(profile)
    return profile


@pytest.fixture
def provider_profile(db_session: Session, provider_user):
    profile = db_session.query(Provider).filter(Provider.user_id == provider_user.id).first()
    if not profile:
        profile = Provider(
            user_id=provider_user.id,
            specialty="mental_health",
            license_number=f"LIC-{uuid.uuid4().hex[:8]}",
            is_active=True,
        )
        db_session.add(profile)
        db_session.commit()
        db_session.refresh(profile)
    return profile
```

---

## Router registration reminder

If your Phase 1 `app/main.py` does not already include these routers, make sure they are registered:

```python
from app.modules.referrals.router import router as referrals_router
from app.modules.notifications.router import router as notifications_router
from app.modules.audit.router import router as audit_router
from app.modules.admin.router import router as admin_router

app.include_router(referrals_router)
app.include_router(notifications_router)
app.include_router(audit_router)
app.include_router(admin_router)
```

---

## Migration note for this phase

This phase does **not necessarily** require a new migration **if** your Phase 2 models already contain the fields assumed above for:
- `Referral`
- `Notification`
- `AuditLog`

If any of those model fields are still missing or named differently, run:

```bash
alembic revision --autogenerate -m "align phase 8 operational workflow fields"
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

---

## Recommended validation commands

Run these from the backend root:

```bash
pytest tests/modules/referrals/test_create_referral.py \
       tests/modules/referrals/test_update_referral_status.py \
       tests/modules/notifications/test_reminder_creation.py \
       tests/modules/audit/test_audit_logging.py \
       tests/modules/admin/test_dashboard_metrics.py -q
```

Broader pass:

```bash
pytest -q
```

---

## Completion checkpoint for this phase

You should consider Phase 8 complete when:
- referrals can be created and tracked
- follow-up notification records are created automatically
- notification delivery state is persisted
- audit events are being written for key operational actions
- admin metrics endpoints return usable summary data
- care teams and admins no longer need manual spreadsheets for basic operational visibility
