# PBBF BLISS — Backend Phase 5 Populated Files
## Phase 5 — Scheduling and Appointment Management

## Objective
Implement appointment booking, provider assignment, rescheduling, cancellation, and status control.

This phase completes the existing `app/modules/appointments` module and adds the missing scheduling helpers and tests needed for a stable MVP appointment workflow.

---

## Important integration note before pasting code
This phase assumes your earlier phases already provide these pieces:

- SQLAlchemy models in `app/db/models/*`
- a working `Session` dependency from `app/db/session.py`
- auth dependencies such as `get_current_user()` and role guards from `app/common/permissions/dependencies.py`
- consistent response helpers in `app/common/utils/response.py`
- user roles such as `patient`, `provider`, `care_coordinator`, and `admin`

If any of your earlier field names differ, adjust imports and column names accordingly before running tests.

---

## Files included in this phase

### Modify these files
- `app/modules/appointments/router.py`
- `app/modules/appointments/schemas.py`
- `app/modules/appointments/service.py`
- `app/modules/appointments/repository.py`

### Create these files if missing
- `app/modules/appointments/constants.py`
- `app/modules/appointments/availability.py`
- `tests/modules/appointments/test_booking.py`
- `tests/modules/appointments/test_reschedule.py`
- `tests/modules/appointments/test_cancel.py`
- `tests/modules/appointments/test_provider_assignment.py`

---

# 1) `app/modules/appointments/constants.py`

```python
from __future__ import annotations

APPOINTMENT_STATUSES = {
    "booked",
    "confirmed",
    "rescheduled",
    "cancelled",
    "completed",
    "no_show",
}

ACTIVE_APPOINTMENT_STATUSES = {
    "booked",
    "confirmed",
    "rescheduled",
}

CANCELLABLE_APPOINTMENT_STATUSES = {
    "booked",
    "confirmed",
    "rescheduled",
}

RESCHEDULABLE_APPOINTMENT_STATUSES = {
    "booked",
    "confirmed",
    "rescheduled",
}

DEFAULT_APPOINTMENT_STATUS = "booked"

SERVICE_TYPES = {
    "mental_health",
    "lactation",
    "wellness_follow_up",
    "community_support",
}

MAX_REASON_LENGTH = 500
MAX_CANCELLATION_REASON_LENGTH = 500
MAX_TIMEZONE_LENGTH = 100
DEFAULT_TIMEZONE = "UTC"
```

---

# 2) `app/modules/appointments/availability.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


@dataclass(slots=True)
class TimeWindow:
    start: datetime
    end: datetime

    def overlaps(self, other: "TimeWindow") -> bool:
        return self.start < other.end and other.start < self.end


class AvailabilityService:
    """
    Simple availability guard for MVP scheduling.

    Notes:
    - This does not attempt to solve full calendar management.
    - It only protects against overlapping active appointments.
    - Provider working-hours policy can be layered later without
      changing the calling pattern.
    """

    @staticmethod
    def normalize_window(
        *,
        start_at: datetime,
        end_at: datetime,
        timezone_name: str,
    ) -> TimeWindow:
        tz = ZoneInfo(timezone_name)

        if start_at.tzinfo is None:
            start_at = start_at.replace(tzinfo=tz)
        else:
            start_at = start_at.astimezone(tz)

        if end_at.tzinfo is None:
            end_at = end_at.replace(tzinfo=tz)
        else:
            end_at = end_at.astimezone(tz)

        return TimeWindow(start=start_at, end=end_at)

    @staticmethod
    def validate_window(window: TimeWindow) -> None:
        if window.end <= window.start:
            raise ValueError("Appointment end time must be after start time.")

        minimum_duration = timedelta(minutes=15)
        if (window.end - window.start) < minimum_duration:
            raise ValueError("Appointment duration must be at least 15 minutes.")

    @staticmethod
    def has_conflict(candidate: TimeWindow, existing_windows: list[TimeWindow]) -> bool:
        return any(candidate.overlaps(existing) for existing in existing_windows)
```

---

# 3) `app/modules/appointments/schemas.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.appointments.constants import (
    APPOINTMENT_STATUSES,
    DEFAULT_TIMEZONE,
    MAX_CANCELLATION_REASON_LENGTH,
    MAX_REASON_LENGTH,
    MAX_TIMEZONE_LENGTH,
    SERVICE_TYPES,
)


class AppointmentBase(BaseModel):
    service_type: str = Field(..., description="Requested care service type")
    reason: Optional[str] = Field(default=None, max_length=MAX_REASON_LENGTH)
    timezone: str = Field(default=DEFAULT_TIMEZONE, max_length=MAX_TIMEZONE_LENGTH)

    @field_validator("service_type")
    @classmethod
    def validate_service_type(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in SERVICE_TYPES:
            raise ValueError(f"service_type must be one of: {', '.join(sorted(SERVICE_TYPES))}")
        return normalized

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("timezone is required")
        return value


class AppointmentCreate(AppointmentBase):
    provider_id: Optional[UUID] = None
    start_at: datetime
    end_at: datetime


class AppointmentReschedule(BaseModel):
    start_at: datetime
    end_at: datetime
    timezone: str = Field(default=DEFAULT_TIMEZONE, max_length=MAX_TIMEZONE_LENGTH)
    reason: Optional[str] = Field(default=None, max_length=MAX_REASON_LENGTH)


class AppointmentCancel(BaseModel):
    reason: Optional[str] = Field(default=None, max_length=MAX_CANCELLATION_REASON_LENGTH)


class AppointmentAssignProvider(BaseModel):
    provider_id: UUID


class AppointmentStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in APPOINTMENT_STATUSES:
            raise ValueError(f"status must be one of: {', '.join(sorted(APPOINTMENT_STATUSES))}")
        return normalized


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | int
    patient_id: UUID | int
    provider_id: UUID | int | None = None
    service_type: str
    reason: Optional[str] = None
    timezone: str
    start_at: datetime
    end_at: datetime
    status: str
    cancellation_reason: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppointmentListResponse(BaseModel):
    items: list[AppointmentResponse]
    total: int
```

---

# 4) `app/modules/appointments/repository.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.db.models.appointment import Appointment
from app.modules.appointments.constants import ACTIVE_APPOINTMENT_STATUSES


class AppointmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, appointment: Appointment) -> Appointment:
        self.db.add(appointment)
        self.db.flush()
        self.db.refresh(appointment)
        return appointment

    def get_by_id(self, appointment_id: UUID | int) -> Appointment | None:
        stmt = select(Appointment).where(Appointment.id == appointment_id)
        return self.db.scalar(stmt)

    def list_for_patient(self, patient_id: UUID | int) -> Sequence[Appointment]:
        stmt = (
            select(Appointment)
            .where(Appointment.patient_id == patient_id)
            .order_by(Appointment.start_at.desc())
        )
        return self.db.scalars(stmt).all()

    def list_for_provider(self, provider_id: UUID | int) -> Sequence[Appointment]:
        stmt = (
            select(Appointment)
            .where(Appointment.provider_id == provider_id)
            .order_by(Appointment.start_at.desc())
        )
        return self.db.scalars(stmt).all()

    def list_all(self) -> Sequence[Appointment]:
        stmt = select(Appointment).order_by(Appointment.start_at.desc())
        return self.db.scalars(stmt).all()

    def count_all(self) -> int:
        stmt = select(func.count()).select_from(Appointment)
        return int(self.db.scalar(stmt) or 0)

    def get_active_conflicts(
        self,
        *,
        provider_id: UUID | int,
        start_at: datetime,
        end_at: datetime,
        exclude_appointment_id: UUID | int | None = None,
    ) -> Sequence[Appointment]:
        conditions = [
            Appointment.provider_id == provider_id,
            Appointment.status.in_(ACTIVE_APPOINTMENT_STATUSES),
            and_(Appointment.start_at < end_at, Appointment.end_at > start_at),
        ]

        if exclude_appointment_id is not None:
            conditions.append(Appointment.id != exclude_appointment_id)

        stmt = select(Appointment).where(*conditions).order_by(Appointment.start_at.asc())
        return self.db.scalars(stmt).all()

    def save(self, appointment: Appointment) -> Appointment:
        self.db.add(appointment)
        self.db.flush()
        self.db.refresh(appointment)
        return appointment
```

---

# 5) `app/modules/appointments/service.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from sqlalchemy.orm import Session

from app.common.errors.http_exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
)
from app.db.models.appointment import Appointment
from app.db.models.provider import Provider
from app.db.models.user import User
from app.modules.appointments.availability import AvailabilityService
from app.modules.appointments.constants import (
    CANCELLABLE_APPOINTMENT_STATUSES,
    DEFAULT_APPOINTMENT_STATUS,
    RESCHEDULABLE_APPOINTMENT_STATUSES,
)
from app.modules.appointments.repository import AppointmentRepository


@dataclass(slots=True)
class ActorContext:
    id: int | str
    role: str


class AppointmentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = AppointmentRepository(db)

    def _ensure_provider_exists(self, provider_id: int | str) -> Provider:
        provider = self.db.get(Provider, provider_id)
        if provider is None:
            raise NotFoundException("Assigned provider was not found.")
        return provider

    def _patient_id_from_user(self, current_user: User) -> int | str:
        patient = getattr(current_user, "patient_profile", None)
        if patient is None:
            raise BadRequestException("Patient profile does not exist for this user.")
        return patient.id

    def _provider_id_from_user(self, current_user: User) -> int | str:
        provider = getattr(current_user, "provider_profile", None)
        if provider is None:
            raise BadRequestException("Provider profile does not exist for this user.")
        return provider.id

    def _check_conflict(
        self,
        *,
        provider_id: int | str,
        start_at: datetime,
        end_at: datetime,
        timezone: str,
        exclude_appointment_id: int | str | None = None,
    ) -> None:
        candidate = AvailabilityService.normalize_window(
            start_at=start_at,
            end_at=end_at,
            timezone_name=timezone,
        )
        AvailabilityService.validate_window(candidate)

        conflicts = self.repository.get_active_conflicts(
            provider_id=provider_id,
            start_at=candidate.start,
            end_at=candidate.end,
            exclude_appointment_id=exclude_appointment_id,
        )

        existing_windows = [
            AvailabilityService.normalize_window(
                start_at=appointment.start_at,
                end_at=appointment.end_at,
                timezone_name=appointment.timezone,
            )
            for appointment in conflicts
        ]

        if AvailabilityService.has_conflict(candidate, existing_windows):
            raise BadRequestException("The selected provider already has a conflicting appointment.")

    def create_appointment(self, *, current_user: User, payload) -> Appointment:
        if current_user.role != "patient":
            raise ForbiddenException("Only patients can create appointments in the MVP flow.")

        patient_id = self._patient_id_from_user(current_user)

        if payload.provider_id is None:
            raise BadRequestException("provider_id is required for appointment booking.")

        self._ensure_provider_exists(payload.provider_id)
        self._check_conflict(
            provider_id=payload.provider_id,
            start_at=payload.start_at,
            end_at=payload.end_at,
            timezone=payload.timezone,
        )

        appointment = Appointment(
            patient_id=patient_id,
            provider_id=payload.provider_id,
            service_type=payload.service_type,
            reason=payload.reason,
            timezone=payload.timezone,
            start_at=payload.start_at,
            end_at=payload.end_at,
            status=DEFAULT_APPOINTMENT_STATUS,
        )
        created = self.repository.create(appointment)
        self.db.commit()
        self.db.refresh(created)
        return created

    def list_appointments(self, *, current_user: User):
        if current_user.role == "patient":
            patient_id = self._patient_id_from_user(current_user)
            return self.repository.list_for_patient(patient_id)

        if current_user.role == "provider":
            provider_id = self._provider_id_from_user(current_user)
            return self.repository.list_for_provider(provider_id)

        if current_user.role in {"admin", "care_coordinator"}:
            return self.repository.list_all()

        raise ForbiddenException("You are not allowed to list appointments.")

    def get_appointment_for_actor(self, *, appointment_id, current_user: User) -> Appointment:
        appointment = self.repository.get_by_id(appointment_id)
        if appointment is None:
            raise NotFoundException("Appointment not found.")

        if current_user.role in {"admin", "care_coordinator"}:
            return appointment

        if current_user.role == "patient":
            patient_id = self._patient_id_from_user(current_user)
            if appointment.patient_id != patient_id:
                raise ForbiddenException("You cannot access this appointment.")
            return appointment

        if current_user.role == "provider":
            provider_id = self._provider_id_from_user(current_user)
            if appointment.provider_id != provider_id:
                raise ForbiddenException("You cannot access this appointment.")
            return appointment

        raise ForbiddenException("You cannot access this appointment.")

    def reschedule_appointment(self, *, appointment_id, current_user: User, payload) -> Appointment:
        appointment = self.get_appointment_for_actor(appointment_id=appointment_id, current_user=current_user)

        if appointment.status not in RESCHEDULABLE_APPOINTMENT_STATUSES:
            raise BadRequestException("This appointment cannot be rescheduled in its current state.")

        if current_user.role not in {"patient", "provider", "admin", "care_coordinator"}:
            raise ForbiddenException("You are not allowed to reschedule appointments.")

        if appointment.provider_id is None:
            raise BadRequestException("Cannot reschedule an appointment without an assigned provider.")

        self._check_conflict(
            provider_id=appointment.provider_id,
            start_at=payload.start_at,
            end_at=payload.end_at,
            timezone=payload.timezone,
            exclude_appointment_id=appointment.id,
        )

        appointment.start_at = payload.start_at
        appointment.end_at = payload.end_at
        appointment.timezone = payload.timezone
        if payload.reason:
            appointment.reason = payload.reason
        appointment.status = "rescheduled"

        updated = self.repository.save(appointment)
        self.db.commit()
        self.db.refresh(updated)
        return updated

    def cancel_appointment(self, *, appointment_id, current_user: User, cancellation_reason: str | None) -> Appointment:
        appointment = self.get_appointment_for_actor(appointment_id=appointment_id, current_user=current_user)

        if appointment.status not in CANCELLABLE_APPOINTMENT_STATUSES:
            raise BadRequestException("This appointment cannot be cancelled in its current state.")

        if current_user.role not in {"patient", "provider", "admin", "care_coordinator"}:
            raise ForbiddenException("You are not allowed to cancel appointments.")

        appointment.status = "cancelled"
        appointment.cancellation_reason = cancellation_reason

        updated = self.repository.save(appointment)
        self.db.commit()
        self.db.refresh(updated)
        return updated

    def assign_provider(self, *, appointment_id, provider_id, current_user: User) -> Appointment:
        if current_user.role not in {"admin", "care_coordinator"}:
            raise ForbiddenException("Only admin or care coordinator users can assign providers.")

        appointment = self.repository.get_by_id(appointment_id)
        if appointment is None:
            raise NotFoundException("Appointment not found.")

        self._ensure_provider_exists(provider_id)
        self._check_conflict(
            provider_id=provider_id,
            start_at=appointment.start_at,
            end_at=appointment.end_at,
            timezone=appointment.timezone,
            exclude_appointment_id=appointment.id,
        )

        appointment.provider_id = provider_id
        updated = self.repository.save(appointment)
        self.db.commit()
        self.db.refresh(updated)
        return updated
```

---

# 6) `app/modules/appointments/router.py`

```python
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.permissions.dependencies import get_current_user
from app.db.models.user import User
from app.db.session import get_db
from app.modules.appointments.schemas import (
    AppointmentAssignProvider,
    AppointmentCancel,
    AppointmentCreate,
    AppointmentListResponse,
    AppointmentResponse,
    AppointmentReschedule,
)
from app.modules.appointments.service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    return service.create_appointment(current_user=current_user, payload=payload)


@router.get("", response_model=AppointmentListResponse)
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    items = service.list_appointments(current_user=current_user)
    return AppointmentListResponse(items=items, total=len(items))


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    return service.get_appointment_for_actor(appointment_id=appointment_id, current_user=current_user)


@router.patch("/{appointment_id}/reschedule", response_model=AppointmentResponse)
def reschedule_appointment(
    appointment_id: int,
    payload: AppointmentReschedule,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    return service.reschedule_appointment(
        appointment_id=appointment_id,
        current_user=current_user,
        payload=payload,
    )


@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: int,
    payload: AppointmentCancel,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    return service.cancel_appointment(
        appointment_id=appointment_id,
        current_user=current_user,
        cancellation_reason=payload.reason,
    )


@router.patch("/{appointment_id}/assign-provider", response_model=AppointmentResponse)
def assign_provider(
    appointment_id: int,
    payload: AppointmentAssignProvider,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    return service.assign_provider(
        appointment_id=appointment_id,
        provider_id=payload.provider_id,
        current_user=current_user,
    )
```

---

# 7) `tests/modules/appointments/test_booking.py`

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db.models.appointment import Appointment


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_patient_can_book_appointment(client, patient_token, provider_user, patient_user):
    start_at = datetime.now(timezone.utc) + timedelta(days=1)
    end_at = start_at + timedelta(minutes=45)

    response = client.post(
        "/appointments",
        json={
            "provider_id": provider_user.provider_profile.id,
            "service_type": "mental_health",
            "reason": "Initial postpartum counseling request",
            "timezone": "UTC",
            "start_at": start_at.isoformat(),
            "end_at": end_at.isoformat(),
        },
        headers=_auth_headers(patient_token),
    )

    assert response.status_code == 201, response.text
    body = response.json()
    assert body["status"] == "booked"
    assert body["patient_id"] == patient_user.patient_profile.id
    assert body["provider_id"] == provider_user.provider_profile.id
    assert body["service_type"] == "mental_health"


def test_schedule_conflict_is_rejected(client, patient_token, provider_user, db_session, patient_user):
    start_at = datetime.now(timezone.utc) + timedelta(days=2)
    end_at = start_at + timedelta(minutes=30)

    existing = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=provider_user.provider_profile.id,
        service_type="mental_health",
        reason="Existing booking",
        timezone="UTC",
        start_at=start_at,
        end_at=end_at,
        status="booked",
    )
    db_session.add(existing)
    db_session.commit()

    response = client.post(
        "/appointments",
        json={
            "provider_id": provider_user.provider_profile.id,
            "service_type": "mental_health",
            "reason": "Conflicting booking",
            "timezone": "UTC",
            "start_at": (start_at + timedelta(minutes=10)).isoformat(),
            "end_at": (end_at + timedelta(minutes=10)).isoformat(),
        },
        headers=_auth_headers(patient_token),
    )

    assert response.status_code == 400, response.text
    assert "conflicting appointment" in response.text.lower()
```

---

# 8) `tests/modules/appointments/test_reschedule.py`

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db.models.appointment import Appointment


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_patient_can_reschedule_own_appointment(client, patient_token, provider_user, patient_user, db_session):
    start_at = datetime.now(timezone.utc) + timedelta(days=3)
    end_at = start_at + timedelta(minutes=30)

    appointment = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=provider_user.provider_profile.id,
        service_type="mental_health",
        reason="Original time",
        timezone="UTC",
        start_at=start_at,
        end_at=end_at,
        status="booked",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    new_start = start_at + timedelta(hours=2)
    new_end = end_at + timedelta(hours=2)

    response = client.patch(
        f"/appointments/{appointment.id}/reschedule",
        json={
            "start_at": new_start.isoformat(),
            "end_at": new_end.isoformat(),
            "timezone": "UTC",
            "reason": "Need a later time",
        },
        headers=_auth_headers(patient_token),
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "rescheduled"
    assert body["timezone"] == "UTC"


def test_reschedule_rejects_conflicting_time(client, patient_token, provider_user, patient_user, db_session):
    base_start = datetime.now(timezone.utc) + timedelta(days=4)
    base_end = base_start + timedelta(minutes=30)

    target = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=provider_user.provider_profile.id,
        service_type="mental_health",
        reason="Appointment to reschedule",
        timezone="UTC",
        start_at=base_start,
        end_at=base_end,
        status="booked",
    )

    blocking = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=provider_user.provider_profile.id,
        service_type="mental_health",
        reason="Blocking appointment",
        timezone="UTC",
        start_at=base_start + timedelta(hours=1),
        end_at=base_end + timedelta(hours=1),
        status="booked",
    )

    db_session.add_all([target, blocking])
    db_session.commit()
    db_session.refresh(target)

    response = client.patch(
        f"/appointments/{target.id}/reschedule",
        json={
            "start_at": (base_start + timedelta(hours=1, minutes=10)).isoformat(),
            "end_at": (base_end + timedelta(hours=1, minutes=10)).isoformat(),
            "timezone": "UTC",
            "reason": "Conflicting shift",
        },
        headers=_auth_headers(patient_token),
    )

    assert response.status_code == 400, response.text
    assert "conflicting appointment" in response.text.lower()
```

---

# 9) `tests/modules/appointments/test_cancel.py`

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db.models.appointment import Appointment


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_patient_can_cancel_own_appointment(client, patient_token, provider_user, patient_user, db_session):
    start_at = datetime.now(timezone.utc) + timedelta(days=5)
    end_at = start_at + timedelta(minutes=30)

    appointment = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=provider_user.provider_profile.id,
        service_type="mental_health",
        reason="Need to cancel",
        timezone="UTC",
        start_at=start_at,
        end_at=end_at,
        status="booked",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    response = client.patch(
        f"/appointments/{appointment.id}/cancel",
        json={"reason": "Family emergency"},
        headers=_auth_headers(patient_token),
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "cancelled"
    assert body["cancellation_reason"] == "Family emergency"


def test_cancelled_appointment_cannot_be_cancelled_again(client, patient_token, provider_user, patient_user, db_session):
    start_at = datetime.now(timezone.utc) + timedelta(days=6)
    end_at = start_at + timedelta(minutes=30)

    appointment = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=provider_user.provider_profile.id,
        service_type="mental_health",
        reason="Already cancelled",
        timezone="UTC",
        start_at=start_at,
        end_at=end_at,
        status="cancelled",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    response = client.patch(
        f"/appointments/{appointment.id}/cancel",
        json={"reason": "Another reason"},
        headers=_auth_headers(patient_token),
    )

    assert response.status_code == 400, response.text
    assert "cannot be cancelled" in response.text.lower()
```

---

# 10) `tests/modules/appointments/test_provider_assignment.py`

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.db.models.appointment import Appointment


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_admin_can_assign_provider(client, admin_token, provider_user, patient_user, db_session):
    start_at = datetime.now(timezone.utc) + timedelta(days=7)
    end_at = start_at + timedelta(minutes=30)

    appointment = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=None,
        service_type="lactation",
        reason="Need provider assignment",
        timezone="UTC",
        start_at=start_at,
        end_at=end_at,
        status="booked",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    response = client.patch(
        f"/appointments/{appointment.id}/assign-provider",
        json={"provider_id": provider_user.provider_profile.id},
        headers=_auth_headers(admin_token),
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["provider_id"] == provider_user.provider_profile.id


def test_patient_cannot_assign_provider(client, patient_token, provider_user, patient_user, db_session):
    start_at = datetime.now(timezone.utc) + timedelta(days=8)
    end_at = start_at + timedelta(minutes=30)

    appointment = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=None,
        service_type="wellness_follow_up",
        reason="Unauthorized assignment attempt",
        timezone="UTC",
        start_at=start_at,
        end_at=end_at,
        status="booked",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    response = client.patch(
        f"/appointments/{appointment.id}/assign-provider",
        json={"provider_id": provider_user.provider_profile.id},
        headers=_auth_headers(patient_token),
    )

    assert response.status_code == 403, response.text


def test_provider_specific_listing_returns_only_own_appointments(client, provider_token, provider_user, other_provider_user, patient_user, db_session):
    start_at = datetime.now(timezone.utc) + timedelta(days=9)

    own_appointment = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=provider_user.provider_profile.id,
        service_type="mental_health",
        reason="Mine",
        timezone="UTC",
        start_at=start_at,
        end_at=start_at + timedelta(minutes=30),
        status="booked",
    )

    other_appointment = Appointment(
        patient_id=patient_user.patient_profile.id,
        provider_id=other_provider_user.provider_profile.id,
        service_type="mental_health",
        reason="Not mine",
        timezone="UTC",
        start_at=start_at + timedelta(hours=1),
        end_at=start_at + timedelta(hours=1, minutes=30),
        status="booked",
    )

    db_session.add_all([own_appointment, other_appointment])
    db_session.commit()

    response = client.get("/appointments", headers=_auth_headers(provider_token))
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["provider_id"] == provider_user.provider_profile.id
```

---

## Suggested additions to `tests/conftest.py`
If your existing test setup does not yet expose these fixtures, add equivalents for them so the appointment tests can run cleanly.

```python
from __future__ import annotations

from datetime import datetime

import pytest
from passlib.context import CryptContext

from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.role import Role
from app.db.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _make_user(db_session, *, email: str, role_name: str, full_name: str):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    user = User(
        email=email,
        full_name=full_name,
        password_hash=pwd_context.hash("Password123!"),
        is_active=True,
        role=role_name,
        role_id=role.id if role else None,
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def patient_user(db_session):
    user = _make_user(
        db_session,
        email="patient@example.com",
        role_name="patient",
        full_name="Patient Example",
    )
    patient = Patient(user_id=user.id)
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(user)
    db_session.refresh(patient)
    setattr(user, "patient_profile", patient)
    return user


@pytest.fixture
def provider_user(db_session):
    user = _make_user(
        db_session,
        email="provider@example.com",
        role_name="provider",
        full_name="Provider Example",
    )
    provider = Provider(user_id=user.id, specialty="mental_health")
    db_session.add(provider)
    db_session.commit()
    db_session.refresh(user)
    db_session.refresh(provider)
    setattr(user, "provider_profile", provider)
    return user


@pytest.fixture
def other_provider_user(db_session):
    user = _make_user(
        db_session,
        email="provider2@example.com",
        role_name="provider",
        full_name="Provider Example Two",
    )
    provider = Provider(user_id=user.id, specialty="lactation")
    db_session.add(provider)
    db_session.commit()
    db_session.refresh(user)
    db_session.refresh(provider)
    setattr(user, "provider_profile", provider)
    return user


@pytest.fixture
def admin_user(db_session):
    user = _make_user(
        db_session,
        email="admin@example.com",
        role_name="admin",
        full_name="Admin Example",
    )
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def patient_token(client, patient_user):
    response = client.post(
        "/auth/login",
        json={"email": patient_user.email, "password": "Password123!"},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


@pytest.fixture
def provider_token(client, provider_user):
    response = client.post(
        "/auth/login",
        json={"email": provider_user.email, "password": "Password123!"},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


@pytest.fixture
def admin_token(client, admin_user):
    response = client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "Password123!"},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]
```

---

## Expected model assumptions for this phase
These appointment files assume your `Appointment` model from Phase 2 contains at least:

```python
id
patient_id
provider_id
service_type
reason
timezone
start_at
end_at
status
cancellation_reason
created_at
updated_at
```

They also assume:
- `User` has a `role` field with simple string values
- `User.patient_profile` exists for patient users
- `User.provider_profile` exists for provider users
- `Provider.id` is the provider-profile primary key used by appointments

If your actual Phase 2 model differs, adjust the service and tests to match your real relationship names.

---

## Commands to run after pasting the files

### 1. Run only the appointment tests
```bash
pytest tests/modules/appointments/test_booking.py \
       tests/modules/appointments/test_reschedule.py \
       tests/modules/appointments/test_cancel.py \
       tests/modules/appointments/test_provider_assignment.py -q
```

### 2. Run auth + intake + appointment flow together
```bash
pytest tests/modules/auth tests/modules/intake tests/modules/appointments -q
```

### 3. Run the full backend suite
```bash
pytest -q
```

---

## Migration note for this phase
Run a migration **only if** your appointment model does not yet include the fields used here.

Use:

```bash
alembic revision --autogenerate -m "align appointment workflow schema"
alembic upgrade head
```

If the model already matches, no new migration is necessary for this phase.

---

## Completion checklist for Backend Phase 5
- patients can create appointments
- patients can list only their own appointments
- providers can list only their assigned appointments
- admins and care coordinators can list all appointments
- conflicting provider schedules are blocked
- appointments can be rescheduled through valid lifecycle states
- appointments can be cancelled through valid lifecycle states
- provider assignment is restricted to admin or care coordinator roles
- responses serialize timestamps and timezone fields consistently

---

## Final note
This phase is populated to be strong enough for the MVP path, but it still keeps scheduling logic intentionally simple. Full calendar rules, provider availability templates, external calendar sync, buffer times, reminder pipelines, and multi-timezone UX refinement can be added in later phases without needing to rewrite the structure established here.
