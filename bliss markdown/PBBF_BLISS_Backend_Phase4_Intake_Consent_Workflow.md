# PBBF BLISS — Backend Phase 4 Populated Files
## Patient Intake and Consent Workflow

## Objective
Build the intake and consent flow that establishes patient onboarding, basic profile capture, consent acknowledgement, and triage readiness.

This phase completes the existing intake module and makes it usable by later modules such as scheduling, screenings, encounters, referrals, and admin/provider review.

---

## Scope for this phase

### Existing module to complete
- `app/modules/intake`

### Files modified in this phase
- `app/modules/intake/router.py`
- `app/modules/intake/schemas.py`
- `app/modules/intake/service.py`
- `app/modules/intake/repository.py`

### Files created if missing
- `app/modules/intake/constants.py`
- `app/modules/intake/validators.py`
- `tests/modules/intake/test_create_draft.py`
- `tests/modules/intake/test_submit_intake.py`
- `tests/modules/intake/test_consent_capture.py`

---

## Pre-flight assumptions

This phase assumes the earlier backend phases already exist and are working:

- Phase 1 startup and DB session plumbing are stable.
- Phase 2 models already exist, especially:
  - `User`
  - `Patient`
  - `IntakeSubmission`
  - `Role`
- Phase 3 auth already provides:
  - `get_current_active_user`
  - `require_roles(...)`
  - patient login and bearer-token auth
- `success_response(...)` already exists in `app/common/utils/response.py`.

### Important model assumptions from Phase 2
This implementation assumes these fields already exist:

#### `Patient`
- `id`
- `user_id`
- `date_of_birth`
- `address`
- `emergency_contact_name`
- `emergency_contact_phone`
- `preferred_language`
- `consent_status`

#### `IntakeSubmission`
- `id`
- `patient_id`
- `submitted_by_user_id`
- `status`
- `service_need`
- `preferred_contact_method`
- `screening_ready`
- `attachments_json`
- `submission_payload`
- `notes`

If your actual Phase 2 schema differs, align the model first and then run a migration before testing this phase.

---

## Functional outcomes covered by this phase

After pasting these files, the backend should support:

- patient intake draft save
- intake draft update
- intake final submit
- consent acknowledgement capture
- emergency contact capture
- service-need category capture
- intake status transitions
- provider/admin/care-coordinator read access for structured intake data

---

## Suggested routes after this phase

- `POST /intake/drafts`
- `PUT /intake/drafts/{intake_id}`
- `POST /intake/{intake_id}/submit`
- `GET /intake/me/latest`
- `GET /intake/{intake_id}`
- `GET /intake/patients/{patient_id}`

Because your app uses module router auto-discovery from `app/main.py`, keep the router prefix local to the module.

---

## 1) `app/modules/intake/constants.py`

```python
from __future__ import annotations

INTAKE_STATUS_DRAFT = "draft"
INTAKE_STATUS_SUBMITTED = "submitted"
INTAKE_STATUS_UNDER_REVIEW = "under_review"
INTAKE_STATUS_READY_TO_SCHEDULE = "ready_to_schedule"

INTAKE_STATUSES = {
    INTAKE_STATUS_DRAFT,
    INTAKE_STATUS_SUBMITTED,
    INTAKE_STATUS_UNDER_REVIEW,
    INTAKE_STATUS_READY_TO_SCHEDULE,
}

SERVICE_NEED_MENTAL_HEALTH = "mental_health"
SERVICE_NEED_LACTATION = "lactation"
SERVICE_NEED_WELLNESS_FOLLOW_UP = "wellness_follow_up"
SERVICE_NEED_COMMUNITY_SUPPORT = "community_support"

SERVICE_NEED_CHOICES = {
    SERVICE_NEED_MENTAL_HEALTH,
    SERVICE_NEED_LACTATION,
    SERVICE_NEED_WELLNESS_FOLLOW_UP,
    SERVICE_NEED_COMMUNITY_SUPPORT,
}

CONTACT_METHOD_EMAIL = "email"
CONTACT_METHOD_PHONE = "phone"
CONTACT_METHOD_SMS = "sms"

CONTACT_METHOD_CHOICES = {
    CONTACT_METHOD_EMAIL,
    CONTACT_METHOD_PHONE,
    CONTACT_METHOD_SMS,
}

PATIENT_ROLE = "patient"
PROVIDER_ROLE = "provider"
CARE_COORDINATOR_ROLE = "care_coordinator"
ADMIN_ROLE = "admin"

CLINICAL_REVIEW_ROLES = {
    PROVIDER_ROLE,
    CARE_COORDINATOR_ROLE,
    ADMIN_ROLE,
}

ALLOWED_STATUS_TRANSITIONS = {
    INTAKE_STATUS_DRAFT: {INTAKE_STATUS_DRAFT, INTAKE_STATUS_SUBMITTED},
    INTAKE_STATUS_SUBMITTED: {INTAKE_STATUS_SUBMITTED, INTAKE_STATUS_UNDER_REVIEW, INTAKE_STATUS_READY_TO_SCHEDULE},
    INTAKE_STATUS_UNDER_REVIEW: {INTAKE_STATUS_UNDER_REVIEW, INTAKE_STATUS_READY_TO_SCHEDULE},
    INTAKE_STATUS_READY_TO_SCHEDULE: {INTAKE_STATUS_READY_TO_SCHEDULE},
}
```

---

## 2) `app/modules/intake/validators.py`

```python
from __future__ import annotations

from fastapi import HTTPException, status

from app.modules.intake.constants import (
    ALLOWED_STATUS_TRANSITIONS,
    CONTACT_METHOD_CHOICES,
    INTAKE_STATUS_DRAFT,
    SERVICE_NEED_CHOICES,
)


def _normalize(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    return normalized or None



def validate_service_need(value: str | None) -> str | None:
    normalized = _normalize(value)
    if normalized is None:
        return None

    if normalized not in SERVICE_NEED_CHOICES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported service_need '{value}'.",
        )

    return normalized



def validate_contact_method(value: str | None) -> str | None:
    normalized = _normalize(value)
    if normalized is None:
        return None

    if normalized not in CONTACT_METHOD_CHOICES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported preferred_contact_method '{value}'.",
        )

    return normalized



def validate_status_transition(current_status: str, new_status: str) -> None:
    current = _normalize(current_status) or INTAKE_STATUS_DRAFT
    new = _normalize(new_status) or INTAKE_STATUS_DRAFT

    allowed_targets = ALLOWED_STATUS_TRANSITIONS.get(current, set())
    if new not in allowed_targets:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot transition intake from '{current}' to '{new}'.",
        )



def ensure_draft_editable(current_status: str) -> None:
    normalized = _normalize(current_status)
    if normalized != INTAKE_STATUS_DRAFT:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only draft intakes can be edited.",
        )



def ensure_submission_requirements(
    *,
    consent_acknowledged: bool,
    consent_version: str | None,
    privacy_policy_version: str | None,
    service_need: str | None,
) -> None:
    if not consent_acknowledged:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consent acknowledgement is required before final submission.",
        )

    if not consent_version:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consent version is required before final submission.",
        )

    if not privacy_policy_version:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Privacy policy version is required before final submission.",
        )

    normalized_service_need = validate_service_need(service_need)
    if not normalized_service_need:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service need category is required before final submission.",
        )



def compute_screening_ready(*, consent_acknowledged: bool, service_need: str | None) -> bool:
    normalized_service_need = _normalize(service_need)
    return bool(consent_acknowledged and normalized_service_need in SERVICE_NEED_CHOICES)
```

---

## 3) `app/modules/intake/schemas.py`

```python
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class IntakeDraftRequest(BaseModel):
    date_of_birth: date | None = None
    address: str | None = Field(default=None, max_length=1000)
    preferred_language: str | None = Field(default=None, max_length=50)
    preferred_contact_method: str | None = Field(default=None, max_length=30)

    emergency_contact_name: str | None = Field(default=None, max_length=150)
    emergency_contact_phone: str | None = Field(default=None, max_length=30)
    emergency_contact_relationship: str | None = Field(default=None, max_length=80)

    service_need: str | None = Field(default=None, max_length=100)
    consent_acknowledged: bool = False
    consent_version: str | None = Field(default=None, max_length=50)
    privacy_policy_version: str | None = Field(default=None, max_length=50)

    postpartum_questionnaire: dict[str, Any] = Field(default_factory=dict)
    attachments: list[dict[str, Any]] = Field(default_factory=list)
    notes: str | None = Field(default=None, max_length=5000)


class IntakeSubmitRequest(IntakeDraftRequest):
    service_need: str = Field(..., max_length=100)
    consent_acknowledged: bool = True
    consent_version: str = Field(..., max_length=50)
    privacy_policy_version: str = Field(..., max_length=50)


class EmergencyContactResponse(BaseModel):
    name: str | None = None
    phone: str | None = None
    relationship: str | None = None


class IntakeResponse(BaseModel):
    id: int
    patient_id: int
    status: str
    service_need: str | None = None
    preferred_contact_method: str | None = None
    screening_ready: bool
    notes: str | None = None
    attachments: list[dict[str, Any]] = Field(default_factory=list)
    submission_payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class IntakeSummaryResponse(BaseModel):
    id: int
    patient_id: int
    status: str
    service_need: str | None = None
    screening_ready: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
```

---

## 4) `app/modules/intake/repository.py`

```python
from __future__ import annotations

from datetime import date
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models.intake_submission import IntakeSubmission
from app.db.models.patient import Patient
from app.db.models.user import User


class IntakeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_patient_by_user_id(self, user_id: int) -> Optional[Patient]:
        stmt = select(Patient).where(Patient.user_id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create_patient_profile(self, *, user_id: int) -> Patient:
        patient = Patient(user_id=user_id)
        self.db.add(patient)
        self.db.flush()
        self.db.refresh(patient)
        return patient

    def update_patient_profile(
        self,
        patient: Patient,
        *,
        date_of_birth: date | None,
        address: str | None,
        preferred_language: str | None,
        emergency_contact_name: str | None,
        emergency_contact_phone: str | None,
        consent_status: bool | None = None,
    ) -> Patient:
        patient.date_of_birth = date_of_birth
        patient.address = address
        patient.preferred_language = preferred_language
        patient.emergency_contact_name = emergency_contact_name
        patient.emergency_contact_phone = emergency_contact_phone

        if consent_status is not None:
            patient.consent_status = consent_status

        self.db.add(patient)
        self.db.flush()
        self.db.refresh(patient)
        return patient

    def create_intake(
        self,
        *,
        patient_id: int,
        submitted_by_user_id: int | None,
        status: str,
        service_need: str | None,
        preferred_contact_method: str | None,
        screening_ready: bool,
        attachments_json: list[dict[str, Any]] | None,
        submission_payload: dict[str, Any],
        notes: str | None,
    ) -> IntakeSubmission:
        intake = IntakeSubmission(
            patient_id=patient_id,
            submitted_by_user_id=submitted_by_user_id,
            status=status,
            service_need=service_need,
            preferred_contact_method=preferred_contact_method,
            screening_ready=screening_ready,
            attachments_json=attachments_json or [],
            submission_payload=submission_payload,
            notes=notes,
        )
        self.db.add(intake)
        self.db.flush()
        self.db.refresh(intake)
        return intake

    def get_intake_by_id(self, intake_id: int) -> Optional[IntakeSubmission]:
        stmt = (
            select(IntakeSubmission)
            .options(
                joinedload(IntakeSubmission.patient).joinedload(Patient.user),
                joinedload(IntakeSubmission.submitted_by_user),
            )
            .where(IntakeSubmission.id == intake_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_intake_for_patient(self, *, intake_id: int, patient_id: int) -> Optional[IntakeSubmission]:
        stmt = (
            select(IntakeSubmission)
            .options(joinedload(IntakeSubmission.patient))
            .where(
                IntakeSubmission.id == intake_id,
                IntakeSubmission.patient_id == patient_id,
            )
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_latest_intake_for_patient(self, patient_id: int) -> Optional[IntakeSubmission]:
        stmt = (
            select(IntakeSubmission)
            .where(IntakeSubmission.patient_id == patient_id)
            .order_by(IntakeSubmission.created_at.desc(), IntakeSubmission.id.desc())
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_intakes_for_patient(self, patient_id: int) -> list[IntakeSubmission]:
        stmt = (
            select(IntakeSubmission)
            .where(IntakeSubmission.patient_id == patient_id)
            .order_by(IntakeSubmission.created_at.desc(), IntakeSubmission.id.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def update_intake(
        self,
        intake: IntakeSubmission,
        *,
        status: str,
        service_need: str | None,
        preferred_contact_method: str | None,
        screening_ready: bool,
        attachments_json: list[dict[str, Any]] | None,
        submission_payload: dict[str, Any],
        notes: str | None,
        submitted_by_user_id: int | None,
    ) -> IntakeSubmission:
        intake.status = status
        intake.service_need = service_need
        intake.preferred_contact_method = preferred_contact_method
        intake.screening_ready = screening_ready
        intake.attachments_json = attachments_json or []
        intake.submission_payload = submission_payload
        intake.notes = notes
        intake.submitted_by_user_id = submitted_by_user_id

        self.db.add(intake)
        self.db.flush()
        self.db.refresh(intake)
        return intake

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
```

---

## 5) `app/modules/intake/service.py`

```python
from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.intake.constants import (
    CLINICAL_REVIEW_ROLES,
    INTAKE_STATUS_DRAFT,
    INTAKE_STATUS_SUBMITTED,
    PATIENT_ROLE,
)
from app.modules.intake.repository import IntakeRepository
from app.modules.intake.schemas import IntakeDraftRequest, IntakeSubmitRequest
from app.modules.intake.validators import (
    compute_screening_ready,
    ensure_draft_editable,
    ensure_submission_requirements,
    validate_contact_method,
    validate_service_need,
    validate_status_transition,
)


class IntakeService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = IntakeRepository(db)

    @staticmethod
    def _role_name(user) -> str:
        return ((getattr(getattr(user, "role", None), "name", None) or "").strip().lower())

    @staticmethod
    def _serialize_submission_payload(payload: IntakeDraftRequest | IntakeSubmitRequest) -> dict[str, Any]:
        return {
            "date_of_birth": payload.date_of_birth.isoformat() if payload.date_of_birth else None,
            "address": payload.address,
            "preferred_language": payload.preferred_language,
            "consent": {
                "acknowledged": payload.consent_acknowledged,
                "version": payload.consent_version,
                "privacy_policy_version": payload.privacy_policy_version,
            },
            "emergency_contact": {
                "name": payload.emergency_contact_name,
                "phone": payload.emergency_contact_phone,
                "relationship": payload.emergency_contact_relationship,
            },
            "postpartum_questionnaire": payload.postpartum_questionnaire or {},
        }

    @staticmethod
    def _serialize_intake(intake) -> dict[str, Any]:
        return {
            "id": intake.id,
            "patient_id": intake.patient_id,
            "status": intake.status,
            "service_need": intake.service_need,
            "preferred_contact_method": intake.preferred_contact_method,
            "screening_ready": intake.screening_ready,
            "notes": intake.notes,
            "attachments": intake.attachments_json or [],
            "submission_payload": intake.submission_payload or {},
            "created_at": getattr(intake, "created_at", None),
            "updated_at": getattr(intake, "updated_at", None),
        }

    def _ensure_patient_role(self, current_user) -> None:
        if self._role_name(current_user) != PATIENT_ROLE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only patients may create or submit intake forms.",
            )

    def _ensure_patient_profile(self, current_user):
        patient = self.repository.get_patient_by_user_id(current_user.id)
        if patient is None:
            patient = self.repository.create_patient_profile(user_id=current_user.id)
        return patient

    def _upsert_patient_from_payload(self, patient, payload: IntakeDraftRequest | IntakeSubmitRequest):
        consent_status = payload.consent_acknowledged if payload.consent_acknowledged else None
        return self.repository.update_patient_profile(
            patient,
            date_of_birth=payload.date_of_birth,
            address=payload.address,
            preferred_language=payload.preferred_language,
            emergency_contact_name=payload.emergency_contact_name,
            emergency_contact_phone=payload.emergency_contact_phone,
            consent_status=consent_status,
        )

    def save_draft(self, *, current_user, payload: IntakeDraftRequest) -> dict[str, Any]:
        self._ensure_patient_role(current_user)

        service_need = validate_service_need(payload.service_need)
        contact_method = validate_contact_method(payload.preferred_contact_method)
        screening_ready = compute_screening_ready(
            consent_acknowledged=payload.consent_acknowledged,
            service_need=service_need,
        )

        patient = self._ensure_patient_profile(current_user)
        self._upsert_patient_from_payload(patient, payload)

        intake = self.repository.create_intake(
            patient_id=patient.id,
            submitted_by_user_id=current_user.id,
            status=INTAKE_STATUS_DRAFT,
            service_need=service_need,
            preferred_contact_method=contact_method,
            screening_ready=screening_ready,
            attachments_json=payload.attachments,
            submission_payload=self._serialize_submission_payload(payload),
            notes=payload.notes,
        )
        self.repository.commit()
        return self._serialize_intake(intake)

    def update_draft(self, *, intake_id: int, current_user, payload: IntakeDraftRequest) -> dict[str, Any]:
        self._ensure_patient_role(current_user)
        patient = self._ensure_patient_profile(current_user)

        intake = self.repository.get_intake_for_patient(intake_id=intake_id, patient_id=patient.id)
        if intake is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Intake draft was not found.",
            )

        ensure_draft_editable(intake.status)
        validate_status_transition(intake.status, INTAKE_STATUS_DRAFT)

        service_need = validate_service_need(payload.service_need)
        contact_method = validate_contact_method(payload.preferred_contact_method)
        screening_ready = compute_screening_ready(
            consent_acknowledged=payload.consent_acknowledged,
            service_need=service_need,
        )

        self._upsert_patient_from_payload(patient, payload)

        intake = self.repository.update_intake(
            intake,
            status=INTAKE_STATUS_DRAFT,
            service_need=service_need,
            preferred_contact_method=contact_method,
            screening_ready=screening_ready,
            attachments_json=payload.attachments,
            submission_payload=self._serialize_submission_payload(payload),
            notes=payload.notes,
            submitted_by_user_id=current_user.id,
        )
        self.repository.commit()
        return self._serialize_intake(intake)

    def submit_intake(self, *, intake_id: int, current_user, payload: IntakeSubmitRequest) -> dict[str, Any]:
        self._ensure_patient_role(current_user)
        patient = self._ensure_patient_profile(current_user)

        intake = self.repository.get_intake_for_patient(intake_id=intake_id, patient_id=patient.id)
        if intake is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Intake record was not found.",
            )

        ensure_draft_editable(intake.status)
        ensure_submission_requirements(
            consent_acknowledged=payload.consent_acknowledged,
            consent_version=payload.consent_version,
            privacy_policy_version=payload.privacy_policy_version,
            service_need=payload.service_need,
        )
        validate_status_transition(intake.status, INTAKE_STATUS_SUBMITTED)

        service_need = validate_service_need(payload.service_need)
        contact_method = validate_contact_method(payload.preferred_contact_method)
        screening_ready = compute_screening_ready(
            consent_acknowledged=payload.consent_acknowledged,
            service_need=service_need,
        )

        self._upsert_patient_from_payload(patient, payload)
        patient.consent_status = True

        intake = self.repository.update_intake(
            intake,
            status=INTAKE_STATUS_SUBMITTED,
            service_need=service_need,
            preferred_contact_method=contact_method,
            screening_ready=screening_ready,
            attachments_json=payload.attachments,
            submission_payload=self._serialize_submission_payload(payload),
            notes=payload.notes,
            submitted_by_user_id=current_user.id,
        )
        self.repository.commit()
        return self._serialize_intake(intake)

    def get_latest_for_current_patient(self, *, current_user) -> dict[str, Any]:
        self._ensure_patient_role(current_user)
        patient = self._ensure_patient_profile(current_user)

        intake = self.repository.get_latest_intake_for_patient(patient.id)
        if intake is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No intake records were found for the current patient.",
            )

        return self._serialize_intake(intake)

    def get_intake_by_id(self, *, intake_id: int, current_user) -> dict[str, Any]:
        intake = self.repository.get_intake_by_id(intake_id)
        if intake is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Intake record was not found.",
            )

        role_name = self._role_name(current_user)
        if role_name == PATIENT_ROLE:
            patient = self._ensure_patient_profile(current_user)
            if intake.patient_id != patient.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You may only access your own intake records.",
                )
        elif role_name not in CLINICAL_REVIEW_ROLES:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view intake records.",
            )

        return self._serialize_intake(intake)

    def list_intakes_for_patient(self, *, patient_id: int, current_user) -> list[dict[str, Any]]:
        role_name = self._role_name(current_user)
        if role_name not in CLINICAL_REVIEW_ROLES:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only provider, care coordinator, or admin roles may review patient intakes.",
            )

        return [
            self._serialize_intake(item)
            for item in self.repository.list_intakes_for_patient(patient_id)
        ]
```

---

## 6) `app/modules/intake/router.py`

```python
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.permissions.dependencies import require_roles
from app.common.utils.response import success_response
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.intake.constants import ADMIN_ROLE, CARE_COORDINATOR_ROLE, PATIENT_ROLE, PROVIDER_ROLE
from app.modules.intake.schemas import IntakeDraftRequest, IntakeSubmitRequest
from app.modules.intake.service import IntakeService


router = APIRouter(prefix="/intake", tags=["Intake"])


@router.post("/drafts")
def create_intake_draft(
    payload: IntakeDraftRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = IntakeService(db)
    data = service.save_draft(current_user=current_user, payload=payload)
    return success_response(
        message="Intake draft saved successfully.",
        data=data,
        status_code=201,
    )


@router.put("/drafts/{intake_id}")
def update_intake_draft(
    intake_id: int,
    payload: IntakeDraftRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = IntakeService(db)
    data = service.update_draft(intake_id=intake_id, current_user=current_user, payload=payload)
    return success_response(
        message="Intake draft updated successfully.",
        data=data,
    )


@router.post("/{intake_id}/submit")
def submit_intake(
    intake_id: int,
    payload: IntakeSubmitRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = IntakeService(db)
    data = service.submit_intake(intake_id=intake_id, current_user=current_user, payload=payload)
    return success_response(
        message="Intake submitted successfully.",
        data=data,
    )


@router.get("/me/latest")
def get_my_latest_intake(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = IntakeService(db)
    data = service.get_latest_for_current_patient(current_user=current_user)
    return success_response(
        message="Latest intake record retrieved successfully.",
        data=data,
    )


@router.get("/patients/{patient_id}", dependencies=[Depends(require_roles(PROVIDER_ROLE, CARE_COORDINATOR_ROLE, ADMIN_ROLE))])
def list_patient_intakes(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = IntakeService(db)
    data = service.list_intakes_for_patient(patient_id=patient_id, current_user=current_user)
    return success_response(
        message="Patient intake records retrieved successfully.",
        data=data,
    )


@router.get("/{intake_id}")
def get_intake_by_id(
    intake_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = IntakeService(db)
    data = service.get_intake_by_id(intake_id=intake_id, current_user=current_user)
    return success_response(
        message="Intake record retrieved successfully.",
        data=data,
    )
```

---

## 7) `tests/modules/intake/test_create_draft.py`

```python
from __future__ import annotations

from sqlalchemy import select

from app.common.utils.security import hash_password
from app.db.models.patient import Patient
from app.db.models.role import Role
from app.db.models.user import User



def ensure_role(db_session, role_name: str) -> Role:
    role = db_session.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
    if role is None:
        role = Role(name=role_name, description=f"{role_name} role")
        db_session.add(role)
        db_session.commit()
        db_session.refresh(role)
    return role



def create_user(db_session, *, email: str, password: str, role_name: str) -> User:
    role = ensure_role(db_session, role_name)
    user = User(
        email=email,
        full_name=f"{role_name.title()} User",
        password_hash=hash_password(password),
        role_id=role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user



def login_headers(client, *, email: str, password: str) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.json()
    body = response.json()
    access_token = body["data"]["tokens"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}



def register_patient_and_login(client, *, email: str = "intake.draft@example.com", password: str = "StrongPass123"):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Draft Intake Patient",
        },
    )
    assert response.status_code in (200, 201), response.json()
    access_token = response.json()["data"]["tokens"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}



def test_patient_can_create_intake_draft(client, db_session):
    headers = register_patient_and_login(client)

    payload = {
        "address": "Kampala, Uganda",
        "preferred_language": "English",
        "preferred_contact_method": "email",
        "emergency_contact_name": "Jane Doe",
        "emergency_contact_phone": "+256700000001",
        "emergency_contact_relationship": "Sister",
        "service_need": "mental_health",
        "consent_acknowledged": False,
        "postpartum_questionnaire": {"sleep_quality": "poor", "mood": "low"},
        "attachments": [],
        "notes": "Patient saved onboarding draft.",
    }

    response = client.post("/api/v1/intake/drafts", json=payload, headers=headers)
    assert response.status_code == 201, response.json()

    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "draft"
    assert body["data"]["service_need"] == "mental_health"
    assert body["data"]["screening_ready"] is False
    assert body["data"]["submission_payload"]["emergency_contact"]["relationship"] == "Sister"

    patient = db_session.execute(select(Patient)).scalar_one_or_none()
    assert patient is not None
    assert patient.emergency_contact_name == "Jane Doe"
    assert patient.emergency_contact_phone == "+256700000001"



def test_invalid_service_need_returns_validation_error(client):
    headers = register_patient_and_login(client, email="bad.service.need@example.com")

    payload = {
        "service_need": "not_a_real_category",
        "consent_acknowledged": False,
    }

    response = client.post("/api/v1/intake/drafts", json=payload, headers=headers)
    assert response.status_code == 422, response.json()



def test_non_patient_cannot_create_intake_draft(client, db_session):
    create_user(
        db_session,
        email="provider.intake@example.com",
        password="StrongPass123",
        role_name="provider",
    )
    headers = login_headers(client, email="provider.intake@example.com", password="StrongPass123")

    payload = {
        "service_need": "mental_health",
        "consent_acknowledged": False,
    }

    response = client.post("/api/v1/intake/drafts", json=payload, headers=headers)
    assert response.status_code == 403, response.json()
```

---

## 8) `tests/modules/intake/test_submit_intake.py`

```python
from __future__ import annotations

from sqlalchemy import select

from app.db.models.patient import Patient
from app.db.models.role import Role
from app.db.models.user import User
from app.common.utils.security import hash_password



def ensure_role(db_session, role_name: str) -> Role:
    role = db_session.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
    if role is None:
        role = Role(name=role_name, description=f"{role_name} role")
        db_session.add(role)
        db_session.commit()
        db_session.refresh(role)
    return role



def create_user(db_session, *, email: str, password: str, role_name: str) -> User:
    role = ensure_role(db_session, role_name)
    user = User(
        email=email,
        full_name=f"{role_name.title()} User",
        password_hash=hash_password(password),
        role_id=role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user



def register_patient_and_login(client, *, email: str = "submit.intake@example.com", password: str = "StrongPass123"):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Submit Intake Patient",
        },
    )
    assert response.status_code in (200, 201), response.json()
    access_token = response.json()["data"]["tokens"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}



def login_headers(client, *, email: str, password: str) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.json()
    access_token = response.json()["data"]["tokens"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}



def test_patient_can_submit_intake_after_draft_save(client, db_session):
    headers = register_patient_and_login(client)

    draft_payload = {
        "address": "Mbarara, Uganda",
        "preferred_language": "English",
        "preferred_contact_method": "sms",
        "emergency_contact_name": "John Doe",
        "emergency_contact_phone": "+256700000099",
        "service_need": "mental_health",
        "consent_acknowledged": False,
        "postpartum_questionnaire": {"epds_ready": True},
        "notes": "Draft before submit",
    }

    draft_response = client.post("/api/v1/intake/drafts", json=draft_payload, headers=headers)
    assert draft_response.status_code == 201, draft_response.json()
    intake_id = draft_response.json()["data"]["id"]

    submit_payload = {
        "address": "Mbarara, Uganda",
        "preferred_language": "English",
        "preferred_contact_method": "sms",
        "emergency_contact_name": "John Doe",
        "emergency_contact_phone": "+256700000099",
        "emergency_contact_relationship": "Mother",
        "service_need": "mental_health",
        "consent_acknowledged": True,
        "consent_version": "2026.04",
        "privacy_policy_version": "2026.04",
        "postpartum_questionnaire": {"epds_ready": True, "stress": "high"},
        "notes": "Final submit",
    }

    response = client.post(f"/api/v1/intake/{intake_id}/submit", json=submit_payload, headers=headers)
    assert response.status_code == 200, response.json()

    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "submitted"
    assert body["data"]["screening_ready"] is True
    assert body["data"]["submission_payload"]["consent"]["acknowledged"] is True
    assert body["data"]["submission_payload"]["consent"]["version"] == "2026.04"

    patient = db_session.execute(select(Patient)).scalar_one()
    assert patient.consent_status is True



def test_submit_requires_consent(client):
    headers = register_patient_and_login(client, email="consent.required@example.com")

    draft_response = client.post(
        "/api/v1/intake/drafts",
        json={"service_need": "mental_health"},
        headers=headers,
    )
    assert draft_response.status_code == 201, draft_response.json()
    intake_id = draft_response.json()["data"]["id"]

    bad_submit_payload = {
        "service_need": "mental_health",
        "consent_acknowledged": False,
        "consent_version": "2026.04",
        "privacy_policy_version": "2026.04",
    }

    response = client.post(f"/api/v1/intake/{intake_id}/submit", json=bad_submit_payload, headers=headers)
    assert response.status_code == 400, response.json()



def test_submitted_intake_cannot_be_edited_as_draft(client):
    headers = register_patient_and_login(client, email="submitted.lock@example.com")

    draft_response = client.post(
        "/api/v1/intake/drafts",
        json={"service_need": "lactation"},
        headers=headers,
    )
    assert draft_response.status_code == 201, draft_response.json()
    intake_id = draft_response.json()["data"]["id"]

    submit_payload = {
        "service_need": "lactation",
        "consent_acknowledged": True,
        "consent_version": "2026.04",
        "privacy_policy_version": "2026.04",
    }
    submit_response = client.post(f"/api/v1/intake/{intake_id}/submit", json=submit_payload, headers=headers)
    assert submit_response.status_code == 200, submit_response.json()

    edit_response = client.put(
        f"/api/v1/intake/drafts/{intake_id}",
        json={"service_need": "community_support"},
        headers=headers,
    )
    assert edit_response.status_code == 409, edit_response.json()



def test_provider_can_review_patient_intake_list(client, db_session):
    patient_headers = register_patient_and_login(client, email="review.patient@example.com")

    draft_response = client.post(
        "/api/v1/intake/drafts",
        json={"service_need": "wellness_follow_up"},
        headers=patient_headers,
    )
    assert draft_response.status_code == 201, draft_response.json()
    patient_id = draft_response.json()["data"]["patient_id"]

    create_user(
        db_session,
        email="review.provider@example.com",
        password="StrongPass123",
        role_name="provider",
    )
    provider_headers = login_headers(client, email="review.provider@example.com", password="StrongPass123")

    response = client.get(f"/api/v1/intake/patients/{patient_id}", headers=provider_headers)
    assert response.status_code == 200, response.json()
    assert isinstance(response.json()["data"], list)
    assert len(response.json()["data"]) >= 1
```

---

## 9) `tests/modules/intake/test_consent_capture.py`

```python
from __future__ import annotations

from sqlalchemy import select

from app.db.models.patient import Patient



def register_patient_and_login(client, *, email: str = "consent.capture@example.com", password: str = "StrongPass123"):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Consent Capture Patient",
        },
    )
    assert response.status_code in (200, 201), response.json()
    access_token = response.json()["data"]["tokens"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}



def test_consent_details_are_persisted_in_submission_payload(client, db_session):
    headers = register_patient_and_login(client)

    draft_response = client.post(
        "/api/v1/intake/drafts",
        json={"service_need": "mental_health"},
        headers=headers,
    )
    assert draft_response.status_code == 201, draft_response.json()
    intake_id = draft_response.json()["data"]["id"]

    submit_payload = {
        "service_need": "mental_health",
        "consent_acknowledged": True,
        "consent_version": "2026.04",
        "privacy_policy_version": "2026.04",
        "preferred_contact_method": "email",
        "emergency_contact_name": "Grace",
        "emergency_contact_phone": "+256700002222",
        "emergency_contact_relationship": "Aunt",
        "postpartum_questionnaire": {"sleep": "poor", "support": "low"},
    }

    response = client.post(f"/api/v1/intake/{intake_id}/submit", json=submit_payload, headers=headers)
    assert response.status_code == 200, response.json()

    body = response.json()
    intake_data = body["data"]
    consent_block = intake_data["submission_payload"]["consent"]
    emergency_contact = intake_data["submission_payload"]["emergency_contact"]

    assert consent_block["acknowledged"] is True
    assert consent_block["version"] == "2026.04"
    assert consent_block["privacy_policy_version"] == "2026.04"
    assert emergency_contact["name"] == "Grace"
    assert emergency_contact["relationship"] == "Aunt"

    patient = db_session.execute(select(Patient)).scalar_one()
    assert patient.consent_status is True
    assert patient.emergency_contact_name == "Grace"
    assert patient.emergency_contact_phone == "+256700002222"



def test_patient_can_fetch_latest_own_intake(client):
    headers = register_patient_and_login(client, email="latest.intake@example.com")

    create_response = client.post(
        "/api/v1/intake/drafts",
        json={"service_need": "community_support", "preferred_contact_method": "phone"},
        headers=headers,
    )
    assert create_response.status_code == 201, create_response.json()

    response = client.get("/api/v1/intake/me/latest", headers=headers)
    assert response.status_code == 200, response.json()
    assert response.json()["data"]["service_need"] == "community_support"



def test_patient_cannot_view_another_patients_intake(client):
    headers_one = register_patient_and_login(client, email="owner.one@example.com")
    headers_two = register_patient_and_login(client, email="owner.two@example.com")

    create_response = client.post(
        "/api/v1/intake/drafts",
        json={"service_need": "mental_health"},
        headers=headers_one,
    )
    assert create_response.status_code == 201, create_response.json()
    intake_id = create_response.json()["data"]["id"]

    response = client.get(f"/api/v1/intake/{intake_id}", headers=headers_two)
    assert response.status_code == 403, response.json()
```

---

## Notes on the existing structure

- Keep the current modular layout.
- Do **not** move intake behavior into `users` or `appointments`.
- The `IntakeSubmission.submission_payload` field is intentionally used to preserve the structured onboarding snapshot that existed at submission time.
- The `Patient` profile table is updated from intake input so later workflows do not need to re-ask for baseline onboarding data.
- This service creates a `Patient` profile on demand if a patient account exists but the profile row does not yet exist.

---

## Test coverage achieved in this phase

The test files above cover the required areas:

- draft save test
- final submit test
- validation error test
- consent required test
- role access test

They also cover a few practical extras:

- submitted draft lock behavior
- latest-intake retrieval
- patient ownership access restriction
- provider review access for patient intake records

---

## Commands to run after pasting Phase 4

If your Phase 2 schema already matches the assumed model fields, run:

```bash
pytest tests/modules/intake/test_create_draft.py tests/modules/intake/test_submit_intake.py tests/modules/intake/test_consent_capture.py -q
```

If you discover your actual `Patient` or `IntakeSubmission` model still differs from the assumptions above, align the model first and then run:

```bash
alembic revision --autogenerate -m "align intake workflow schema"
alembic upgrade head
pytest tests/modules/intake/test_create_draft.py tests/modules/intake/test_submit_intake.py tests/modules/intake/test_consent_capture.py -q
```

---

## Completion checkpoint

This phase is complete when all of the following are true:

- patients can save intake drafts
- patients can submit intake with consent captured
- emergency contact and service-need data persist correctly
- intake status changes from `draft` to `submitted` cleanly
- providers/admins/care coordinators can read structured intake records
- tests pass without import-path or app boot issues

