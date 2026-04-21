# PBBF BLISS — Backend Phase 7 Populated Files  
## Telehealth Session Access and Encounter Documentation

## Objective
Support virtual session access and provider documentation during or after visits.

This phase completes the following existing backend modules:
- `app/modules/telehealth`
- `app/modules/encounters`

It delivers:
- telehealth session metadata creation
- role-aware join access
- join timestamp capture
- session status transitions
- encounter creation by appointment
- note draft/save/finalize flow
- follow-up plan capture

---

## Assumptions for this phase
These populated files assume your Phase 2 model layer already includes the following entities and relationships:
- `User`
- `Appointment`
- `TelehealthSession`
- `Encounter`
- `Patient`
- `Provider`

They also assume your authentication layer from Phase 3 already exposes a working current-user dependency and role-aware access pattern.

If your actual model field names differ, align the imports and column names before running tests.

---

## Files populated in this phase

### Existing files to modify
- `app/modules/telehealth/router.py`
- `app/modules/telehealth/schemas.py`
- `app/modules/telehealth/service.py`
- `app/modules/telehealth/repository.py`
- `app/modules/encounters/router.py`
- `app/modules/encounters/schemas.py`
- `app/modules/encounters/service.py`
- `app/modules/encounters/repository.py`

### Files to create if missing
- `app/modules/telehealth/providers.py`
- `app/modules/encounters/templates.py`
- `tests/modules/telehealth/test_session_access.py`
- `tests/modules/telehealth/test_session_status.py`
- `tests/modules/encounters/test_create_note.py`
- `tests/modules/encounters/test_finalize_note.py`

---

# 1) `app/modules/telehealth/providers.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from app.common.config.settings import settings


@dataclass(slots=True)
class GeneratedSessionPayload:
    external_meeting_id: str
    patient_join_url: str
    provider_join_url: str


class VirtualVisitProvider:
    """Interface for generating visit-access metadata.

    For MVP we keep this provider lightweight and deterministic.
    Later this can be replaced with Microsoft Teams / Bookings / ACS wiring
    without rewriting router or service logic.
    """

    def create_session(self, appointment_id: int | str) -> GeneratedSessionPayload:
        raise NotImplementedError


class DemoVirtualVisitProvider(VirtualVisitProvider):
    def create_session(self, appointment_id: int | str) -> GeneratedSessionPayload:
        meeting_id = f"tv-{appointment_id}-{uuid4().hex[:12]}"
        public_base = getattr(settings, "PUBLIC_APP_URL", "http://localhost:5173").rstrip("/")
        api_base = getattr(settings, "API_BASE_URL", "http://localhost:8000").rstrip("/")

        return GeneratedSessionPayload(
            external_meeting_id=meeting_id,
            patient_join_url=f"{public_base}/patient/session/{meeting_id}",
            provider_join_url=f"{public_base}/provider/session/{meeting_id}?source={api_base}",
        )


_provider_singleton: VirtualVisitProvider | None = None


def get_virtual_visit_provider() -> VirtualVisitProvider:
    global _provider_singleton
    if _provider_singleton is None:
        _provider_singleton = DemoVirtualVisitProvider()
    return _provider_singleton
```

---

# 2) `app/modules/telehealth/schemas.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SessionStatus = Literal["scheduled", "waiting", "in_progress", "ended", "no_show"]
JoinActor = Literal["patient", "provider"]


class TelehealthSessionCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appointment_id: int
    external_meeting_id: str
    join_url: str
    provider_join_url: str | None = None
    session_status: SessionStatus
    patient_joined_at: datetime | None = None
    provider_joined_at: datetime | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TelehealthSessionRead(TelehealthSessionCreateResponse):
    pass


class TelehealthJoinResponse(BaseModel):
    session_id: int
    appointment_id: int
    actor: JoinActor
    join_url: str
    session_status: SessionStatus
    patient_joined_at: datetime | None = None
    provider_joined_at: datetime | None = None
    started_at: datetime | None = None


class TelehealthStatusUpdateRequest(BaseModel):
    session_status: SessionStatus = Field(..., description="New session lifecycle state")


class TelehealthStatusUpdateResponse(BaseModel):
    session_id: int
    appointment_id: int
    session_status: SessionStatus
    started_at: datetime | None = None
    ended_at: datetime | None = None
    patient_joined_at: datetime | None = None
    provider_joined_at: datetime | None = None


class TelehealthSessionListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appointment_id: int
    session_status: SessionStatus
    join_url: str
    provider_join_url: str | None = None
    patient_joined_at: datetime | None = None
    provider_joined_at: datetime | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
```

---

# 3) `app/modules/telehealth/repository.py`

```python
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models.appointment import Appointment
from app.db.models.telehealth_session import TelehealthSession


class TelehealthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_appointment(self, appointment_id: int) -> Appointment | None:
        stmt = select(Appointment).where(Appointment.id == appointment_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_session_by_id(self, session_id: int) -> TelehealthSession | None:
        stmt = select(TelehealthSession).where(TelehealthSession.id == session_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_session_by_appointment_id(self, appointment_id: int) -> TelehealthSession | None:
        stmt = select(TelehealthSession).where(TelehealthSession.appointment_id == appointment_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create_session(
        self,
        *,
        appointment_id: int,
        external_meeting_id: str,
        join_url: str,
        provider_join_url: str,
    ) -> TelehealthSession:
        session = TelehealthSession(
            appointment_id=appointment_id,
            external_meeting_id=external_meeting_id,
            join_url=join_url,
            provider_join_url=provider_join_url,
            session_status="scheduled",
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def touch_join(self, session: TelehealthSession, *, actor: str) -> TelehealthSession:
        now = datetime.now(timezone.utc)

        if actor == "patient" and getattr(session, "patient_joined_at", None) is None:
            session.patient_joined_at = now
        elif actor == "provider" and getattr(session, "provider_joined_at", None) is None:
            session.provider_joined_at = now

        if session.patient_joined_at or session.provider_joined_at:
            if session.session_status == "scheduled":
                session.session_status = "waiting"

        if session.patient_joined_at and session.provider_joined_at:
            session.session_status = "in_progress"
            if getattr(session, "started_at", None) is None:
                session.started_at = now

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def update_status(self, session: TelehealthSession, *, new_status: str) -> TelehealthSession:
        now = datetime.now(timezone.utc)
        session.session_status = new_status

        if new_status == "in_progress" and getattr(session, "started_at", None) is None:
            session.started_at = now

        if new_status in {"ended", "no_show"}:
            session.ended_at = now

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def list_for_user(self, *, user_id: int, role: str) -> list[TelehealthSession]:
        stmt = select(TelehealthSession).join(Appointment, Appointment.id == TelehealthSession.appointment_id)

        if role == "patient":
            stmt = stmt.where(Appointment.patient_id == user_id)
        elif role in {"provider", "counselor", "lactation_consultant"}:
            stmt = stmt.where(Appointment.provider_id == user_id)
        elif role in {"admin", "care_coordinator"}:
            stmt = stmt.order_by(TelehealthSession.id.desc())
            return list(self.db.execute(stmt).scalars().all())
        else:
            return []

        stmt = stmt.order_by(TelehealthSession.id.desc())
        return list(self.db.execute(stmt).scalars().all())
```

---

# 4) `app/modules/telehealth/service.py`

```python
from __future__ import annotations

from app.common.errors.http_exceptions import ForbiddenException, NotFoundException, ValidationException
from app.modules.telehealth.providers import get_virtual_visit_provider
from app.modules.telehealth.repository import TelehealthRepository


ALLOWED_STATUS_TRANSITIONS: dict[str, set[str]] = {
    "scheduled": {"waiting", "in_progress", "ended", "no_show"},
    "waiting": {"in_progress", "ended", "no_show"},
    "in_progress": {"ended"},
    "ended": set(),
    "no_show": set(),
}


class TelehealthService:
    def __init__(self, repository: TelehealthRepository) -> None:
        self.repository = repository
        self.provider = get_virtual_visit_provider()

    def ensure_session_for_appointment(self, *, appointment_id: int, current_user) -> object:
        appointment = self.repository.get_appointment(appointment_id)
        if appointment is None:
            raise NotFoundException("Appointment not found.")

        role = getattr(current_user, "role", None)
        if role not in {"provider", "admin", "care_coordinator"}:
            raise ForbiddenException("You are not allowed to create session metadata for this appointment.")

        existing = self.repository.get_session_by_appointment_id(appointment_id)
        if existing is not None:
            return existing

        generated = self.provider.create_session(appointment_id)
        return self.repository.create_session(
            appointment_id=appointment_id,
            external_meeting_id=generated.external_meeting_id,
            join_url=generated.patient_join_url,
            provider_join_url=generated.provider_join_url,
        )

    def get_session(self, *, session_id: int):
        session = self.repository.get_session_by_id(session_id)
        if session is None:
            raise NotFoundException("Telehealth session not found.")
        return session

    def join_session(self, *, session_id: int, current_user) -> tuple[object, str, str]:
        session = self.repository.get_session_by_id(session_id)
        if session is None:
            raise NotFoundException("Telehealth session not found.")

        appointment = self.repository.get_appointment(session.appointment_id)
        if appointment is None:
            raise NotFoundException("Linked appointment not found.")

        user_id = getattr(current_user, "id", None)
        role = getattr(current_user, "role", None)

        actor: str | None = None
        join_url = session.join_url

        if role == "patient" and appointment.patient_id == user_id:
            actor = "patient"
            join_url = session.join_url
        elif role in {"provider", "counselor", "lactation_consultant"} and appointment.provider_id == user_id:
            actor = "provider"
            join_url = session.provider_join_url or session.join_url
        elif role in {"admin", "care_coordinator"}:
            actor = "provider"
            join_url = session.provider_join_url or session.join_url
        else:
            raise ForbiddenException("You are not allowed to join this session.")

        session = self.repository.touch_join(session, actor=actor)
        return session, actor, join_url

    def update_status(self, *, session_id: int, new_status: str, current_user):
        session = self.repository.get_session_by_id(session_id)
        if session is None:
            raise NotFoundException("Telehealth session not found.")

        appointment = self.repository.get_appointment(session.appointment_id)
        if appointment is None:
            raise NotFoundException("Linked appointment not found.")

        role = getattr(current_user, "role", None)
        user_id = getattr(current_user, "id", None)

        if role not in {"provider", "admin", "care_coordinator"} and not (
            role in {"counselor", "lactation_consultant"} and appointment.provider_id == user_id
        ):
            raise ForbiddenException("You are not allowed to change session status.")

        current_status = session.session_status
        allowed = ALLOWED_STATUS_TRANSITIONS.get(current_status, set())
        if new_status not in allowed and new_status != current_status:
            raise ValidationException(
                f"Invalid session status transition from '{current_status}' to '{new_status}'."
            )

        return self.repository.update_status(session, new_status=new_status)

    def list_for_current_user(self, current_user):
        return self.repository.list_for_user(
            user_id=getattr(current_user, "id"),
            role=getattr(current_user, "role", ""),
        )
```

---

# 5) `app/modules/telehealth/router.py`

```python
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.telehealth.repository import TelehealthRepository
from app.modules.telehealth.schemas import (
    TelehealthJoinResponse,
    TelehealthSessionCreateResponse,
    TelehealthSessionListItem,
    TelehealthSessionRead,
    TelehealthStatusUpdateRequest,
    TelehealthStatusUpdateResponse,
)
from app.modules.telehealth.service import TelehealthService

router = APIRouter(prefix="/telehealth", tags=["telehealth"])


@router.post(
    "/appointments/{appointment_id}/session",
    response_model=TelehealthSessionCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def ensure_session_for_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = TelehealthService(TelehealthRepository(db))
    session = service.ensure_session_for_appointment(
        appointment_id=appointment_id,
        current_user=current_user,
    )
    return session


@router.get("/sessions/{session_id}", response_model=TelehealthSessionRead)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = TelehealthService(TelehealthRepository(db))
    session = service.get_session(session_id=session_id)
    return session


@router.get("/sessions", response_model=list[TelehealthSessionListItem])
def list_sessions_for_current_user(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = TelehealthService(TelehealthRepository(db))
    return service.list_for_current_user(current_user)


@router.post("/sessions/{session_id}/join", response_model=TelehealthJoinResponse)
def join_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = TelehealthService(TelehealthRepository(db))
    session, actor, join_url = service.join_session(
        session_id=session_id,
        current_user=current_user,
    )
    return TelehealthJoinResponse(
        session_id=session.id,
        appointment_id=session.appointment_id,
        actor=actor,
        join_url=join_url,
        session_status=session.session_status,
        patient_joined_at=session.patient_joined_at,
        provider_joined_at=session.provider_joined_at,
        started_at=session.started_at,
    )


@router.post("/sessions/{session_id}/status", response_model=TelehealthStatusUpdateResponse)
def update_session_status(
    session_id: int,
    payload: TelehealthStatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = TelehealthService(TelehealthRepository(db))
    session = service.update_status(
        session_id=session_id,
        new_status=payload.session_status,
        current_user=current_user,
    )
    return TelehealthStatusUpdateResponse(
        session_id=session.id,
        appointment_id=session.appointment_id,
        session_status=session.session_status,
        started_at=session.started_at,
        ended_at=session.ended_at,
        patient_joined_at=session.patient_joined_at,
        provider_joined_at=session.provider_joined_at,
    )
```

---

# 6) `app/modules/encounters/templates.py`

```python
from __future__ import annotations

BASIC_TEMPLATES: dict[str, dict[str, str]] = {
    "telehealth_follow_up": {
        "subjective": "Patient-reported concerns, symptoms, and postpartum experience.",
        "objective": "Relevant observed findings from the telehealth visit.",
        "assessment": "Clinical impression based on history, screening, and interaction.",
        "plan": "Care recommendations, education, referrals, and follow-up instructions.",
        "follow_up_plan": "Return visit timing, escalation triggers, and outreach plan.",
    },
    "lactation_consult": {
        "subjective": "Feeding concerns, latch concerns, milk supply concerns, and family goals.",
        "objective": "Observed feeding context, infant response, and practical findings.",
        "assessment": "Assessment of feeding barriers and lactation needs.",
        "plan": "Lactation support steps, education, and referral if needed.",
        "follow_up_plan": "Follow-up timeframe and home support instructions.",
    },
}


def get_note_template(name: str = "telehealth_follow_up") -> dict[str, str]:
    return BASIC_TEMPLATES.get(name, BASIC_TEMPLATES["telehealth_follow_up"]).copy()
```

---

# 7) `app/modules/encounters/schemas.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EncounterStatus = Literal["draft", "finalized"]


class EncounterCreateRequest(BaseModel):
    template_name: str = Field(default="telehealth_follow_up", max_length=100)


class EncounterDraftUpdateRequest(BaseModel):
    subjective: str | None = None
    objective: str | None = None
    assessment: str | None = None
    plan: str | None = None
    note_text: str | None = None
    follow_up_plan: str | None = None


class EncounterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appointment_id: int
    patient_id: int
    provider_id: int
    status: EncounterStatus
    template_name: str | None = None
    subjective: str | None = None
    objective: str | None = None
    assessment: str | None = None
    plan: str | None = None
    note_text: str | None = None
    follow_up_plan: str | None = None
    finalized_at: datetime | None = None
    finalized_by_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class EncounterFinalizeResponse(BaseModel):
    encounter_id: int
    status: EncounterStatus
    finalized_at: datetime | None = None
    finalized_by_id: int | None = None
```

---

# 8) `app/modules/encounters/repository.py`

```python
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.appointment import Appointment
from app.db.models.encounter import Encounter


class EncounterRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_appointment(self, appointment_id: int) -> Appointment | None:
        stmt = select(Appointment).where(Appointment.id == appointment_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_id(self, encounter_id: int) -> Encounter | None:
        stmt = select(Encounter).where(Encounter.id == encounter_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_appointment_id(self, appointment_id: int) -> Encounter | None:
        stmt = select(Encounter).where(Encounter.appointment_id == appointment_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(
        self,
        *,
        appointment_id: int,
        patient_id: int,
        provider_id: int,
        template_name: str,
        subjective: str | None,
        objective: str | None,
        assessment: str | None,
        plan: str | None,
        follow_up_plan: str | None,
    ) -> Encounter:
        encounter = Encounter(
            appointment_id=appointment_id,
            patient_id=patient_id,
            provider_id=provider_id,
            status="draft",
            template_name=template_name,
            subjective=subjective,
            objective=objective,
            assessment=assessment,
            plan=plan,
            follow_up_plan=follow_up_plan,
        )
        self.db.add(encounter)
        self.db.commit()
        self.db.refresh(encounter)
        return encounter

    def update_draft(self, encounter: Encounter, **changes) -> Encounter:
        for field, value in changes.items():
            if value is not None and hasattr(encounter, field):
                setattr(encounter, field, value)

        self.db.add(encounter)
        self.db.commit()
        self.db.refresh(encounter)
        return encounter

    def finalize(self, encounter: Encounter, *, finalized_by_id: int) -> Encounter:
        encounter.status = "finalized"
        encounter.finalized_by_id = finalized_by_id
        encounter.finalized_at = datetime.now(timezone.utc)

        self.db.add(encounter)
        self.db.commit()
        self.db.refresh(encounter)
        return encounter
```

---

# 9) `app/modules/encounters/service.py`

```python
from __future__ import annotations

from app.common.errors.http_exceptions import ForbiddenException, NotFoundException, ValidationException
from app.modules.encounters.repository import EncounterRepository
from app.modules.encounters.templates import get_note_template


class EncounterService:
    def __init__(self, repository: EncounterRepository) -> None:
        self.repository = repository

    def create_for_appointment(self, *, appointment_id: int, template_name: str, current_user):
        appointment = self.repository.get_appointment(appointment_id)
        if appointment is None:
            raise NotFoundException("Appointment not found.")

        role = getattr(current_user, "role", None)
        user_id = getattr(current_user, "id", None)

        if role not in {"provider", "counselor", "lactation_consultant", "admin"}:
            raise ForbiddenException("You are not allowed to create encounter documentation.")

        if role != "admin" and appointment.provider_id != user_id:
            raise ForbiddenException("You are not assigned to this appointment.")

        existing = self.repository.get_by_appointment_id(appointment_id)
        if existing is not None:
            return existing

        template = get_note_template(template_name)
        return self.repository.create(
            appointment_id=appointment.id,
            patient_id=appointment.patient_id,
            provider_id=appointment.provider_id,
            template_name=template_name,
            subjective=template.get("subjective"),
            objective=template.get("objective"),
            assessment=template.get("assessment"),
            plan=template.get("plan"),
            follow_up_plan=template.get("follow_up_plan"),
        )

    def get_by_id(self, *, encounter_id: int, current_user):
        encounter = self.repository.get_by_id(encounter_id)
        if encounter is None:
            raise NotFoundException("Encounter not found.")

        role = getattr(current_user, "role", None)
        user_id = getattr(current_user, "id", None)

        if role == "patient" and encounter.patient_id != user_id:
            raise ForbiddenException("You are not allowed to view this encounter.")
        elif role in {"provider", "counselor", "lactation_consultant"} and encounter.provider_id != user_id:
            raise ForbiddenException("You are not allowed to view this encounter.")
        elif role not in {"patient", "provider", "counselor", "lactation_consultant", "admin", "care_coordinator"}:
            raise ForbiddenException("You are not allowed to view this encounter.")

        return encounter

    def save_draft(self, *, encounter_id: int, payload, current_user):
        encounter = self.repository.get_by_id(encounter_id)
        if encounter is None:
            raise NotFoundException("Encounter not found.")

        role = getattr(current_user, "role", None)
        user_id = getattr(current_user, "id", None)

        if role not in {"provider", "counselor", "lactation_consultant", "admin"}:
            raise ForbiddenException("You are not allowed to edit encounter documentation.")

        if role != "admin" and encounter.provider_id != user_id:
            raise ForbiddenException("You are not allowed to edit this encounter.")

        if encounter.status == "finalized":
            raise ValidationException("Finalized encounters cannot be modified.")

        return self.repository.update_draft(
            encounter,
            subjective=payload.subjective,
            objective=payload.objective,
            assessment=payload.assessment,
            plan=payload.plan,
            note_text=payload.note_text,
            follow_up_plan=payload.follow_up_plan,
        )

    def finalize(self, *, encounter_id: int, current_user):
        encounter = self.repository.get_by_id(encounter_id)
        if encounter is None:
            raise NotFoundException("Encounter not found.")

        role = getattr(current_user, "role", None)
        user_id = getattr(current_user, "id", None)

        if role not in {"provider", "counselor", "lactation_consultant", "admin"}:
            raise ForbiddenException("You are not allowed to finalize encounter documentation.")

        if role != "admin" and encounter.provider_id != user_id:
            raise ForbiddenException("You are not allowed to finalize this encounter.")

        required_fields = [encounter.assessment, encounter.plan]
        if any(not value or not str(value).strip() for value in required_fields):
            raise ValidationException("Assessment and plan are required before finalizing a note.")

        if encounter.status == "finalized":
            return encounter

        return self.repository.finalize(encounter, finalized_by_id=user_id)
```

---

# 10) `app/modules/encounters/router.py`

```python
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.encounters.repository import EncounterRepository
from app.modules.encounters.schemas import (
    EncounterCreateRequest,
    EncounterDraftUpdateRequest,
    EncounterFinalizeResponse,
    EncounterRead,
)
from app.modules.encounters.service import EncounterService

router = APIRouter(prefix="/encounters", tags=["encounters"])


@router.post(
    "/appointments/{appointment_id}",
    response_model=EncounterRead,
    status_code=status.HTTP_201_CREATED,
)
def create_encounter_for_appointment(
    appointment_id: int,
    payload: EncounterCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = EncounterService(EncounterRepository(db))
    encounter = service.create_for_appointment(
        appointment_id=appointment_id,
        template_name=payload.template_name,
        current_user=current_user,
    )
    return encounter


@router.get("/{encounter_id}", response_model=EncounterRead)
def get_encounter(
    encounter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = EncounterService(EncounterRepository(db))
    return service.get_by_id(encounter_id=encounter_id, current_user=current_user)


@router.put("/{encounter_id}/draft", response_model=EncounterRead)
def save_encounter_draft(
    encounter_id: int,
    payload: EncounterDraftUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = EncounterService(EncounterRepository(db))
    return service.save_draft(
        encounter_id=encounter_id,
        payload=payload,
        current_user=current_user,
    )


@router.post("/{encounter_id}/finalize", response_model=EncounterFinalizeResponse)
def finalize_encounter(
    encounter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = EncounterService(EncounterRepository(db))
    encounter = service.finalize(encounter_id=encounter_id, current_user=current_user)
    return EncounterFinalizeResponse(
        encounter_id=encounter.id,
        status=encounter.status,
        finalized_at=encounter.finalized_at,
        finalized_by_id=encounter.finalized_by_id,
    )
```

---

# 11) `tests/modules/telehealth/test_session_access.py`

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.common.utils.security import get_password_hash
from app.db.models.appointment import Appointment
from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.role import Role
from app.db.models.user import User


API_PREFIX = "/api/v1"


def _create_user(db_session, *, email: str, role_name: str, full_name: str = "Test User"):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    user = User(
        email=email,
        full_name=full_name,
        password_hash=get_password_hash("Password123!"),
        role=role_name,
        is_active=True,
    )
    if hasattr(user, "role_id") and role is not None:
        user.role_id = role.id
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _attach_patient_profile(db_session, user_id: int):
    patient = Patient(user_id=user_id)
    db_session.add(patient)
    db_session.commit()
    return patient


def _attach_provider_profile(db_session, user_id: int):
    provider = Provider(user_id=user_id)
    db_session.add(provider)
    db_session.commit()
    return provider


def _login_headers(client, email: str, password: str = "Password123!") -> dict[str, str]:
    response = client.post(
        f"{API_PREFIX}/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    token = body["data"]["access_token"] if "data" in body else body["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_appointment(db_session, *, patient_user_id: int, provider_user_id: int) -> Appointment:
    appointment = Appointment(
        patient_id=patient_user_id,
        provider_id=provider_user_id,
        service_type="mental_health",
        reason="Telehealth follow-up",
        status="booked",
        scheduled_start=datetime.now(timezone.utc) + timedelta(days=1),
        scheduled_end=datetime.now(timezone.utc) + timedelta(days=1, minutes=30),
        timezone="Africa/Kampala",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)
    return appointment


def test_authorized_patient_and_provider_can_join_session(client, db_session):
    patient_user = _create_user(db_session, email="patient_join@example.com", role_name="patient")
    provider_user = _create_user(db_session, email="provider_join@example.com", role_name="provider")
    _attach_patient_profile(db_session, patient_user.id)
    _attach_provider_profile(db_session, provider_user.id)
    appointment = _create_appointment(db_session, patient_user_id=patient_user.id, provider_user_id=provider_user.id)

    provider_headers = _login_headers(client, provider_user.email)
    patient_headers = _login_headers(client, patient_user.email)

    ensure_resp = client.post(
        f"{API_PREFIX}/telehealth/appointments/{appointment.id}/session",
        headers=provider_headers,
    )
    assert ensure_resp.status_code in (200, 201), ensure_resp.text
    session_id = ensure_resp.json()["id"]

    patient_join = client.post(
        f"{API_PREFIX}/telehealth/sessions/{session_id}/join",
        headers=patient_headers,
    )
    assert patient_join.status_code == 200, patient_join.text
    assert patient_join.json()["actor"] == "patient"

    provider_join = client.post(
        f"{API_PREFIX}/telehealth/sessions/{session_id}/join",
        headers=provider_headers,
    )
    assert provider_join.status_code == 200, provider_join.text
    assert provider_join.json()["actor"] == "provider"
    assert provider_join.json()["session_status"] == "in_progress"


def test_unassigned_user_cannot_join_session(client, db_session):
    patient_user = _create_user(db_session, email="patient_denied@example.com", role_name="patient")
    provider_user = _create_user(db_session, email="provider_denied@example.com", role_name="provider")
    outsider_user = _create_user(db_session, email="outsider@example.com", role_name="patient")

    _attach_patient_profile(db_session, patient_user.id)
    _attach_provider_profile(db_session, provider_user.id)
    _attach_patient_profile(db_session, outsider_user.id)

    appointment = _create_appointment(db_session, patient_user_id=patient_user.id, provider_user_id=provider_user.id)

    provider_headers = _login_headers(client, provider_user.email)
    outsider_headers = _login_headers(client, outsider_user.email)

    ensure_resp = client.post(
        f"{API_PREFIX}/telehealth/appointments/{appointment.id}/session",
        headers=provider_headers,
    )
    assert ensure_resp.status_code in (200, 201), ensure_resp.text
    session_id = ensure_resp.json()["id"]

    denied_resp = client.post(
        f"{API_PREFIX}/telehealth/sessions/{session_id}/join",
        headers=outsider_headers,
    )
    assert denied_resp.status_code in (401, 403), denied_resp.text
```

---

# 12) `tests/modules/telehealth/test_session_status.py`

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.common.utils.security import get_password_hash
from app.db.models.appointment import Appointment
from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.role import Role
from app.db.models.user import User


API_PREFIX = "/api/v1"


def _create_user(db_session, *, email: str, role_name: str):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    user = User(
        email=email,
        full_name=email.split("@")[0],
        password_hash=get_password_hash("Password123!"),
        role=role_name,
        is_active=True,
    )
    if hasattr(user, "role_id") and role is not None:
        user.role_id = role.id
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _login_headers(client, email: str) -> dict[str, str]:
    response = client.post(f"{API_PREFIX}/auth/login", json={"email": email, "password": "Password123!"})
    assert response.status_code == 200, response.text
    body = response.json()
    token = body["data"]["access_token"] if "data" in body else body["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_session_status_lifecycle(client, db_session):
    patient_user = _create_user(db_session, email="status_patient@example.com", role_name="patient")
    provider_user = _create_user(db_session, email="status_provider@example.com", role_name="provider")

    db_session.add(Patient(user_id=patient_user.id))
    db_session.add(Provider(user_id=provider_user.id))
    db_session.commit()

    appointment = Appointment(
        patient_id=patient_user.id,
        provider_id=provider_user.id,
        service_type="mental_health",
        reason="Status flow",
        status="booked",
        scheduled_start=datetime.now(timezone.utc) + timedelta(hours=2),
        scheduled_end=datetime.now(timezone.utc) + timedelta(hours=2, minutes=30),
        timezone="Africa/Kampala",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    provider_headers = _login_headers(client, provider_user.email)
    patient_headers = _login_headers(client, patient_user.email)

    ensure_resp = client.post(
        f"{API_PREFIX}/telehealth/appointments/{appointment.id}/session",
        headers=provider_headers,
    )
    assert ensure_resp.status_code in (200, 201), ensure_resp.text
    session_id = ensure_resp.json()["id"]

    patient_join = client.post(f"{API_PREFIX}/telehealth/sessions/{session_id}/join", headers=patient_headers)
    assert patient_join.status_code == 200
    assert patient_join.json()["session_status"] == "waiting"

    provider_join = client.post(f"{API_PREFIX}/telehealth/sessions/{session_id}/join", headers=provider_headers)
    assert provider_join.status_code == 200
    assert provider_join.json()["session_status"] == "in_progress"

    end_resp = client.post(
        f"{API_PREFIX}/telehealth/sessions/{session_id}/status",
        headers=provider_headers,
        json={"session_status": "ended"},
    )
    assert end_resp.status_code == 200, end_resp.text
    assert end_resp.json()["session_status"] == "ended"
    assert end_resp.json()["ended_at"] is not None


def test_invalid_status_transition_is_rejected(client, db_session):
    patient_user = _create_user(db_session, email="badtransition_patient@example.com", role_name="patient")
    provider_user = _create_user(db_session, email="badtransition_provider@example.com", role_name="provider")

    db_session.add(Patient(user_id=patient_user.id))
    db_session.add(Provider(user_id=provider_user.id))
    db_session.commit()

    appointment = Appointment(
        patient_id=patient_user.id,
        provider_id=provider_user.id,
        service_type="mental_health",
        reason="Bad transition",
        status="booked",
        scheduled_start=datetime.now(timezone.utc) + timedelta(hours=5),
        scheduled_end=datetime.now(timezone.utc) + timedelta(hours=5, minutes=20),
        timezone="Africa/Kampala",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    provider_headers = _login_headers(client, provider_user.email)

    ensure_resp = client.post(
        f"{API_PREFIX}/telehealth/appointments/{appointment.id}/session",
        headers=provider_headers,
    )
    assert ensure_resp.status_code in (200, 201), ensure_resp.text
    session_id = ensure_resp.json()["id"]

    no_show_resp = client.post(
        f"{API_PREFIX}/telehealth/sessions/{session_id}/status",
        headers=provider_headers,
        json={"session_status": "no_show"},
    )
    assert no_show_resp.status_code == 200, no_show_resp.text

    invalid_resp = client.post(
        f"{API_PREFIX}/telehealth/sessions/{session_id}/status",
        headers=provider_headers,
        json={"session_status": "in_progress"},
    )
    assert invalid_resp.status_code in (400, 422), invalid_resp.text
```

---

# 13) `tests/modules/encounters/test_create_note.py`

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.common.utils.security import get_password_hash
from app.db.models.appointment import Appointment
from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.role import Role
from app.db.models.user import User


API_PREFIX = "/api/v1"


def _create_user(db_session, *, email: str, role_name: str):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    user = User(
        email=email,
        full_name=email.split("@")[0],
        password_hash=get_password_hash("Password123!"),
        role=role_name,
        is_active=True,
    )
    if hasattr(user, "role_id") and role is not None:
        user.role_id = role.id
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _login_headers(client, email: str) -> dict[str, str]:
    response = client.post(f"{API_PREFIX}/auth/login", json={"email": email, "password": "Password123!"})
    assert response.status_code == 200, response.text
    body = response.json()
    token = body["data"]["access_token"] if "data" in body else body["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_provider_can_create_encounter_note_from_appointment(client, db_session):
    patient_user = _create_user(db_session, email="enc_patient@example.com", role_name="patient")
    provider_user = _create_user(db_session, email="enc_provider@example.com", role_name="provider")

    db_session.add(Patient(user_id=patient_user.id))
    db_session.add(Provider(user_id=provider_user.id))
    db_session.commit()

    appointment = Appointment(
        patient_id=patient_user.id,
        provider_id=provider_user.id,
        service_type="mental_health",
        reason="Encounter creation",
        status="confirmed",
        scheduled_start=datetime.now(timezone.utc) - timedelta(minutes=15),
        scheduled_end=datetime.now(timezone.utc) + timedelta(minutes=15),
        timezone="Africa/Kampala",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    provider_headers = _login_headers(client, provider_user.email)

    create_resp = client.post(
        f"{API_PREFIX}/encounters/appointments/{appointment.id}",
        headers=provider_headers,
        json={"template_name": "telehealth_follow_up"},
    )
    assert create_resp.status_code in (200, 201), create_resp.text

    body = create_resp.json()
    assert body["appointment_id"] == appointment.id
    assert body["provider_id"] == provider_user.id
    assert body["patient_id"] == patient_user.id
    assert body["status"] == "draft"
    assert body["assessment"] is not None
    assert body["plan"] is not None


def test_unassigned_provider_cannot_create_encounter(client, db_session):
    patient_user = _create_user(db_session, email="enc_patient_denied@example.com", role_name="patient")
    assigned_provider = _create_user(db_session, email="assigned_provider@example.com", role_name="provider")
    outsider_provider = _create_user(db_session, email="outsider_provider@example.com", role_name="provider")

    db_session.add(Patient(user_id=patient_user.id))
    db_session.add(Provider(user_id=assigned_provider.id))
    db_session.add(Provider(user_id=outsider_provider.id))
    db_session.commit()

    appointment = Appointment(
        patient_id=patient_user.id,
        provider_id=assigned_provider.id,
        service_type="mental_health",
        reason="Unauthorized encounter create",
        status="confirmed",
        scheduled_start=datetime.now(timezone.utc),
        scheduled_end=datetime.now(timezone.utc) + timedelta(minutes=25),
        timezone="Africa/Kampala",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    outsider_headers = _login_headers(client, outsider_provider.email)

    denied_resp = client.post(
        f"{API_PREFIX}/encounters/appointments/{appointment.id}",
        headers=outsider_headers,
        json={"template_name": "telehealth_follow_up"},
    )
    assert denied_resp.status_code in (401, 403), denied_resp.text
```

---

# 14) `tests/modules/encounters/test_finalize_note.py`

```python
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.common.utils.security import get_password_hash
from app.db.models.appointment import Appointment
from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.role import Role
from app.db.models.user import User


API_PREFIX = "/api/v1"


def _create_user(db_session, *, email: str, role_name: str):
    role = db_session.query(Role).filter(Role.name == role_name).first()
    user = User(
        email=email,
        full_name=email.split("@")[0],
        password_hash=get_password_hash("Password123!"),
        role=role_name,
        is_active=True,
    )
    if hasattr(user, "role_id") and role is not None:
        user.role_id = role.id
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _login_headers(client, email: str) -> dict[str, str]:
    response = client.post(f"{API_PREFIX}/auth/login", json={"email": email, "password": "Password123!"})
    assert response.status_code == 200, response.text
    body = response.json()
    token = body["data"]["access_token"] if "data" in body else body["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_provider_can_save_and_finalize_note(client, db_session):
    patient_user = _create_user(db_session, email="finalize_patient@example.com", role_name="patient")
    provider_user = _create_user(db_session, email="finalize_provider@example.com", role_name="provider")

    db_session.add(Patient(user_id=patient_user.id))
    db_session.add(Provider(user_id=provider_user.id))
    db_session.commit()

    appointment = Appointment(
        patient_id=patient_user.id,
        provider_id=provider_user.id,
        service_type="mental_health",
        reason="Finalize encounter note",
        status="completed",
        scheduled_start=datetime.now(timezone.utc) - timedelta(hours=1),
        scheduled_end=datetime.now(timezone.utc) - timedelta(minutes=30),
        timezone="Africa/Kampala",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    provider_headers = _login_headers(client, provider_user.email)

    create_resp = client.post(
        f"{API_PREFIX}/encounters/appointments/{appointment.id}",
        headers=provider_headers,
        json={"template_name": "telehealth_follow_up"},
    )
    assert create_resp.status_code in (200, 201), create_resp.text
    encounter_id = create_resp.json()["id"]

    update_resp = client.put(
        f"{API_PREFIX}/encounters/{encounter_id}/draft",
        headers=provider_headers,
        json={
            "assessment": "Moderate postpartum distress with need for counseling follow-up.",
            "plan": "Continue weekly counseling, review support system, and repeat EPDS in two weeks.",
            "follow_up_plan": "Provider outreach in 48 hours; next visit in 7 days.",
            "note_text": "Structured telehealth encounter completed successfully.",
        },
    )
    assert update_resp.status_code == 200, update_resp.text

    finalize_resp = client.post(
        f"{API_PREFIX}/encounters/{encounter_id}/finalize",
        headers=provider_headers,
    )
    assert finalize_resp.status_code == 200, finalize_resp.text
    assert finalize_resp.json()["status"] == "finalized"
    assert finalize_resp.json()["finalized_at"] is not None


def test_finalize_rejects_incomplete_note(client, db_session):
    patient_user = _create_user(db_session, email="incomplete_patient@example.com", role_name="patient")
    provider_user = _create_user(db_session, email="incomplete_provider@example.com", role_name="provider")

    db_session.add(Patient(user_id=patient_user.id))
    db_session.add(Provider(user_id=provider_user.id))
    db_session.commit()

    appointment = Appointment(
        patient_id=patient_user.id,
        provider_id=provider_user.id,
        service_type="mental_health",
        reason="Incomplete finalize",
        status="completed",
        scheduled_start=datetime.now(timezone.utc) - timedelta(hours=1),
        scheduled_end=datetime.now(timezone.utc) - timedelta(minutes=15),
        timezone="Africa/Kampala",
    )
    db_session.add(appointment)
    db_session.commit()
    db_session.refresh(appointment)

    provider_headers = _login_headers(client, provider_user.email)

    create_resp = client.post(
        f"{API_PREFIX}/encounters/appointments/{appointment.id}",
        headers=provider_headers,
        json={"template_name": "telehealth_follow_up"},
    )
    assert create_resp.status_code in (200, 201), create_resp.text
    encounter_id = create_resp.json()["id"]

    update_resp = client.put(
        f"{API_PREFIX}/encounters/{encounter_id}/draft",
        headers=provider_headers,
        json={
            "assessment": "",
            "plan": "",
            "follow_up_plan": "Provider will attempt follow-up tomorrow.",
        },
    )
    assert update_resp.status_code == 200, update_resp.text

    finalize_resp = client.post(
        f"{API_PREFIX}/encounters/{encounter_id}/finalize",
        headers=provider_headers,
    )
    assert finalize_resp.status_code in (400, 422), finalize_resp.text
```

---

## Router registration reminder
Make sure both routers are mounted in `app/main.py` if they are not already:

```python
from app.modules.telehealth.router import router as telehealth_router
from app.modules.encounters.router import router as encounters_router

app.include_router(telehealth_router, prefix="/api/v1")
app.include_router(encounters_router, prefix="/api/v1")
```

---

## Migration note for this phase
This phase does **not automatically require a new migration** if your Phase 2 models already include all fields used above.

If your `TelehealthSession` or `Encounter` model is missing fields such as:
- `external_meeting_id`
- `join_url`
- `provider_join_url`
- `session_status`
- `patient_joined_at`
- `provider_joined_at`
- `started_at`
- `ended_at`
- `template_name`
- `subjective`
- `objective`
- `assessment`
- `plan`
- `note_text`
- `follow_up_plan`
- `status`
- `finalized_at`
- `finalized_by_id`

run these exact commands after aligning the models:

```bash
alembic revision --autogenerate -m "add telehealth session and encounter documentation fields"
alembic upgrade head
```

To verify downgrade safety:

```bash
alembic downgrade -1
alembic upgrade head
```

---

## Test commands for this phase
Run only this phase’s tests first:

```bash
pytest tests/modules/telehealth/test_session_access.py \
       tests/modules/telehealth/test_session_status.py \
       tests/modules/encounters/test_create_note.py \
       tests/modules/encounters/test_finalize_note.py -q
```

Then run the broader backend suite:

```bash
pytest -q
```

---

## Expected completion checkpoint
This phase is complete when:
- patients can join only their own scheduled visit sessions
- providers can create or access session metadata for appointments they manage
- telehealth sessions move through valid lifecycle states
- join timestamps are persisted correctly
- encounter notes can be created from appointments
- providers can save drafts and finalize structured notes
- follow-up plans are stored with the encounter record
- all phase tests pass without manual DB intervention

---

## Final implementation note
This phase gives you a strong MVP backend for virtual visits and documentation, but it intentionally keeps the virtual meeting provider abstraction simple. That is the right move. It lets you finish the care workflow now, while leaving a clean upgrade path later for Microsoft Teams, Bookings, or Azure Communication Services integration without rewriting the module boundaries.
