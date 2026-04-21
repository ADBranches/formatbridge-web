# PBBF BLISS — Backend Phase 6 Populated Files
## Phase 6 — Screenings and EPDS Logic

## Objective
Implement the first screening workflow, with EPDS scoring, risk banding, and provider review visibility.

This phase completes the existing `app/modules/screenings` module and adds the scoring helpers and tests required for a stable MVP screening workflow.

---

## Important integration note before pasting code
This phase assumes your earlier backend phases already provide:

- the `Screening`, `Patient`, `Encounter`, `Appointment`, `Provider`, and `User` SQLAlchemy models
- a working `get_db()` dependency from `app/db/session.py`
- working auth dependencies such as `get_current_active_user()` and role guards from `app/common/permissions/dependencies.py`
- response helpers such as `success_response()` from `app/common/utils/response.py`
- user roles such as `patient`, `provider`, `care_coordinator`, and `admin`

This phase is designed to work with the Phase 2 model assumptions already used in the earlier generated files:

- `Screening.answers_json`
- `Screening.score`
- `Screening.severity_band`
- `Screening.interpretation`
- `Screening.critical_flag`
- `Screening.review_notes`
- `Screening.patient_id`
- `Screening.created_by_user_id`
- `Screening.encounter_id`

If your current model field names differ, align the imports and field names before running tests.

---

## EPDS implementation note
This phase treats EPDS as a **screening workflow**, not a diagnosis workflow. The backend computes the score from raw answer positions so that scoring remains centralized and consistent. Item 10 is treated as a safety flag whenever its scored value is greater than 0.

For the MVP, the banding used here is:

- `0–9` → `within_range_monitor`
- `10–12` → `follow_up_recommended`
- `13+` → `urgent_clinical_review`

Keep these thresholds under clinical review before production release.

---

## Files included in this phase

### Modify these files
- `app/modules/screenings/router.py`
- `app/modules/screenings/schemas.py`
- `app/modules/screenings/service.py`
- `app/modules/screenings/repository.py`

### Create these files if missing
- `app/modules/screenings/scoring.py`
- `app/modules/screenings/constants.py`
- `tests/modules/screenings/test_epds_submission.py`
- `tests/modules/screenings/test_epds_scoring.py`
- `tests/modules/screenings/test_epds_risk_flags.py`

---

# 1) `app/modules/screenings/constants.py`

```python
from __future__ import annotations

SCREENING_TYPE_EPDS = "EPDS"
SCREENING_STATUS_COMPLETED = "completed"
SCREENING_STATUS_REVIEWED = "reviewed"

SCREENING_STATUSES = {
    SCREENING_STATUS_COMPLETED,
    SCREENING_STATUS_REVIEWED,
}

EPDS_QUESTION_COUNT = 10
EPDS_MIN_OPTION_INDEX = 0
EPDS_MAX_OPTION_INDEX = 3

# Questions scored in the same direction as they are presented.
EPDS_DIRECT_SCORED_QUESTIONS = {1, 2, 4}

# Questions that must be reverse-scored from the selected option index.
EPDS_REVERSE_SCORED_QUESTIONS = {3, 5, 6, 7, 8, 9, 10}

EPDS_ALLOWED_QUESTION_KEYS = tuple(f"q{i}" for i in range(1, EPDS_QUESTION_COUNT + 1))

# Operational MVP banding. Keep under clinical review before production release.
EPDS_BAND_WITHIN_RANGE = "within_range_monitor"
EPDS_BAND_FOLLOW_UP = "follow_up_recommended"
EPDS_BAND_URGENT = "urgent_clinical_review"

EPDS_SCORE_BANDS = (
    (0, 9, EPDS_BAND_WITHIN_RANGE),
    (10, 12, EPDS_BAND_FOLLOW_UP),
    (13, 30, EPDS_BAND_URGENT),
)

EPDS_ITEM_10_CRITICAL_SCORES = {1, 2, 3}

EPDS_INTERPRETATIONS = {
    EPDS_BAND_WITHIN_RANGE: (
        "Score suggests symptoms should be monitored and reviewed again if concerns persist."
    ),
    EPDS_BAND_FOLLOW_UP: (
        "Score suggests follow-up review is recommended and repeat screening should be considered."
    ),
    EPDS_BAND_URGENT: (
        "Score suggests urgent clinical review is recommended."
    ),
}
```

---

# 2) `app/modules/screenings/scoring.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.modules.screenings.constants import (
    EPDS_ALLOWED_QUESTION_KEYS,
    EPDS_DIRECT_SCORED_QUESTIONS,
    EPDS_INTERPRETATIONS,
    EPDS_ITEM_10_CRITICAL_SCORES,
    EPDS_MAX_OPTION_INDEX,
    EPDS_MIN_OPTION_INDEX,
    EPDS_QUESTION_COUNT,
    EPDS_REVERSE_SCORED_QUESTIONS,
    EPDS_SCORE_BANDS,
)


class EPDSValidationError(ValueError):
    pass


@dataclass(slots=True)
class EPDSScoreResult:
    raw_answers: dict[str, int]
    scored_answers: dict[str, int]
    total_score: int
    severity_band: str
    interpretation: str
    critical_flag: bool


class EPDSEngine:
    """
    Accepts EPDS answers as raw selected option indexes from 0..3.

    Example:
    - q1 = 0 means the first option was selected for question 1.
    - q1 = 3 means the fourth option was selected for question 1.

    Scoring is applied centrally on the backend so the frontend does not
    need to implement reverse-scoring rules.
    """

    @staticmethod
    def normalize_answers(answers: dict[str, Any] | list[Any]) -> dict[str, int]:
        if isinstance(answers, list):
            if len(answers) != EPDS_QUESTION_COUNT:
                raise EPDSValidationError(
                    f"EPDS requires exactly {EPDS_QUESTION_COUNT} answers."
                )
            answers = {f"q{index + 1}": value for index, value in enumerate(answers)}

        if not isinstance(answers, dict):
            raise EPDSValidationError("EPDS answers must be a dict or a list.")

        normalized: dict[str, int] = {}
        expected_keys = set(EPDS_ALLOWED_QUESTION_KEYS)
        actual_keys = set(answers.keys())

        if actual_keys != expected_keys:
            missing = sorted(expected_keys - actual_keys)
            extra = sorted(actual_keys - expected_keys)
            details = []
            if missing:
                details.append(f"missing keys: {', '.join(missing)}")
            if extra:
                details.append(f"unexpected keys: {', '.join(extra)}")
            raise EPDSValidationError("Invalid EPDS answer payload: " + "; ".join(details))

        for question_key in EPDS_ALLOWED_QUESTION_KEYS:
            value = answers[question_key]
            if not isinstance(value, int):
                raise EPDSValidationError(f"{question_key} must be an integer from 0 to 3.")
            if value < EPDS_MIN_OPTION_INDEX or value > EPDS_MAX_OPTION_INDEX:
                raise EPDSValidationError(f"{question_key} must be between 0 and 3.")
            normalized[question_key] = value

        return normalized

    @staticmethod
    def score_answers(raw_answers: dict[str, int]) -> dict[str, int]:
        scored: dict[str, int] = {}

        for question_number in range(1, EPDS_QUESTION_COUNT + 1):
            question_key = f"q{question_number}"
            raw_value = raw_answers[question_key]

            if question_number in EPDS_DIRECT_SCORED_QUESTIONS:
                scored_value = raw_value
            elif question_number in EPDS_REVERSE_SCORED_QUESTIONS:
                scored_value = 3 - raw_value
            else:
                raise EPDSValidationError(f"Question {question_number} is not configured for scoring.")

            scored[question_key] = scored_value

        return scored

    @staticmethod
    def classify(total_score: int) -> tuple[str, str]:
        for minimum, maximum, band in EPDS_SCORE_BANDS:
            if minimum <= total_score <= maximum:
                return band, EPDS_INTERPRETATIONS[band]
        raise EPDSValidationError("EPDS score is outside the supported range.")

    @staticmethod
    def has_critical_flag(scored_answers: dict[str, int]) -> bool:
        return scored_answers["q10"] in EPDS_ITEM_10_CRITICAL_SCORES

    @classmethod
    def evaluate(cls, answers: dict[str, Any] | list[Any]) -> EPDSScoreResult:
        raw_answers = cls.normalize_answers(answers)
        scored_answers = cls.score_answers(raw_answers)
        total_score = sum(scored_answers.values())
        severity_band, interpretation = cls.classify(total_score)
        critical_flag = cls.has_critical_flag(scored_answers)

        return EPDSScoreResult(
            raw_answers=raw_answers,
            scored_answers=scored_answers,
            total_score=total_score,
            severity_band=severity_band,
            interpretation=interpretation,
            critical_flag=critical_flag,
        )
```

---

# 3) `app/modules/screenings/schemas.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.screenings.constants import SCREENING_STATUS_COMPLETED, SCREENING_STATUS_REVIEWED


class EPDSAnswers(BaseModel):
    q1: int = Field(..., ge=0, le=3)
    q2: int = Field(..., ge=0, le=3)
    q3: int = Field(..., ge=0, le=3)
    q4: int = Field(..., ge=0, le=3)
    q5: int = Field(..., ge=0, le=3)
    q6: int = Field(..., ge=0, le=3)
    q7: int = Field(..., ge=0, le=3)
    q8: int = Field(..., ge=0, le=3)
    q9: int = Field(..., ge=0, le=3)
    q10: int = Field(..., ge=0, le=3)


class EPDSSubmissionCreate(BaseModel):
    patient_id: Optional[int] = None
    encounter_id: Optional[int] = None
    answers: EPDSAnswers


class ScreeningReviewUpdate(BaseModel):
    review_notes: Optional[str] = Field(default=None, max_length=2000)
    status: str = Field(default=SCREENING_STATUS_REVIEWED)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {SCREENING_STATUS_COMPLETED, SCREENING_STATUS_REVIEWED}:
            raise ValueError("status must be either 'completed' or 'reviewed'.")
        return normalized


class ScreeningSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    encounter_id: Optional[int] = None
    screening_type: str
    status: str
    score: Optional[int] = None
    severity_band: Optional[str] = None
    interpretation: Optional[str] = None
    critical_flag: bool
    review_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class EPDSSubmissionResponse(ScreeningSummaryResponse):
    answers_json: dict
```

---

# 4) `app/modules/screenings/repository.py`

```python
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models.appointment import Appointment
from app.db.models.encounter import Encounter
from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.screening import Screening
from app.db.repositories.base import BaseRepository


class ScreeningModuleRepository(BaseRepository[Screening]):
    def __init__(self, db: Session):
        super().__init__(Screening, db)

    def get_patient_by_user_id(self, user_id: int) -> Patient | None:
        statement = select(Patient).where(Patient.user_id == user_id)
        return self.db.execute(statement).scalars().first()

    def get_patient_by_id(self, patient_id: int) -> Patient | None:
        return self.db.get(Patient, patient_id)

    def get_provider_by_user_id(self, user_id: int) -> Provider | None:
        statement = select(Provider).where(Provider.user_id == user_id)
        return self.db.execute(statement).scalars().first()

    def get_encounter_by_id(self, encounter_id: int) -> Encounter | None:
        return self.db.get(Encounter, encounter_id)

    def create_epds(
        self,
        *,
        patient_id: int,
        created_by_user_id: int,
        encounter_id: int | None,
        answers_json: dict,
        score: int,
        severity_band: str,
        interpretation: str,
        critical_flag: bool,
    ) -> Screening:
        screening = self.create(
            patient_id=patient_id,
            encounter_id=encounter_id,
            created_by_user_id=created_by_user_id,
            screening_type="EPDS",
            status="completed",
            answers_json=answers_json,
            score=score,
            severity_band=severity_band,
            interpretation=interpretation,
            critical_flag=critical_flag,
        )
        self.db.commit()
        self.db.refresh(screening)
        return screening

    def update_review(self, screening: Screening, *, review_notes: str | None, status: str) -> Screening:
        screening.review_notes = review_notes
        screening.status = status
        self.db.add(screening)
        self.db.commit()
        self.db.refresh(screening)
        return screening

    def get_screening_by_id(self, screening_id: int) -> Screening | None:
        statement = (
            select(Screening)
            .options(
                joinedload(Screening.patient),
                joinedload(Screening.encounter),
                joinedload(Screening.created_by_user),
            )
            .where(Screening.id == screening_id)
        )
        return self.db.execute(statement).scalars().first()

    def list_for_patient(self, patient_id: int) -> list[Screening]:
        statement = (
            select(Screening)
            .where(Screening.patient_id == patient_id)
            .order_by(Screening.created_at.desc())
        )
        return self.db.execute(statement).scalars().all()

    def has_provider_access_to_patient(self, *, provider_id: int, patient_id: int) -> bool:
        statement = (
            select(Appointment.id)
            .where(Appointment.provider_id == provider_id)
            .where(Appointment.patient_id == patient_id)
            .limit(1)
        )
        result = self.db.execute(statement).scalar_one_or_none()
        return result is not None
```

---

# 5) `app/modules/screenings/service.py`

```python
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.screening import Screening
from app.modules.screenings.repository import ScreeningModuleRepository
from app.modules.screenings.scoring import EPDSEngine, EPDSValidationError
from app.modules.screenings.schemas import EPDSSubmissionCreate, ScreeningReviewUpdate


class ScreeningService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ScreeningModuleRepository(db)

    @staticmethod
    def _role_name(user) -> str:
        return (getattr(getattr(user, "role", None), "name", "") or "").strip().lower()

    def _resolve_patient_for_submission(self, *, current_user, payload: EPDSSubmissionCreate) -> int:
        role_name = self._role_name(current_user)

        if role_name == "patient":
            patient = self.repository.get_patient_by_user_id(current_user.id)
            if patient is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Patient profile was not found for the authenticated user.",
                )
            return patient.id

        if role_name in {"admin", "care_coordinator", "provider"}:
            if payload.patient_id is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="patient_id is required for staff-submitted screenings.",
                )
            patient = self.repository.get_patient_by_id(payload.patient_id)
            if patient is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Patient was not found.",
                )
            return patient.id

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This role is not allowed to submit screenings.",
        )

    def _validate_encounter_patient_link(self, *, patient_id: int, encounter_id: int | None) -> None:
        if encounter_id is None:
            return

        encounter = self.repository.get_encounter_by_id(encounter_id)
        if encounter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Encounter was not found.",
            )
        if encounter.patient_id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Encounter does not belong to the supplied patient.",
            )

    def submit_epds(self, *, current_user, payload: EPDSSubmissionCreate) -> Screening:
        patient_id = self._resolve_patient_for_submission(current_user=current_user, payload=payload)
        self._validate_encounter_patient_link(patient_id=patient_id, encounter_id=payload.encounter_id)

        try:
            evaluation = EPDSEngine.evaluate(payload.answers.model_dump())
        except EPDSValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

        answers_json = {
            "format": "epds",
            "raw_answers": evaluation.raw_answers,
            "scored_answers": evaluation.scored_answers,
        }

        return self.repository.create_epds(
            patient_id=patient_id,
            created_by_user_id=current_user.id,
            encounter_id=payload.encounter_id,
            answers_json=answers_json,
            score=evaluation.total_score,
            severity_band=evaluation.severity_band,
            interpretation=evaluation.interpretation,
            critical_flag=evaluation.critical_flag,
        )

    def list_history_for_current_patient(self, *, current_user) -> list[Screening]:
        patient = self.repository.get_patient_by_user_id(current_user.id)
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient profile was not found for the authenticated user.",
            )
        return self.repository.list_for_patient(patient.id)

    def list_history_for_patient(self, *, current_user, patient_id: int) -> list[Screening]:
        role_name = self._role_name(current_user)

        if role_name == "patient":
            patient = self.repository.get_patient_by_user_id(current_user.id)
            if patient is None or patient.id != patient_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Patients may only view their own screening history.",
                )
            return self.repository.list_for_patient(patient_id)

        if role_name in {"admin", "care_coordinator"}:
            return self.repository.list_for_patient(patient_id)

        if role_name == "provider":
            provider = self.repository.get_provider_by_user_id(current_user.id)
            if provider is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Provider profile was not found for the authenticated user.",
                )
            if not self.repository.has_provider_access_to_patient(provider_id=provider.id, patient_id=patient_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Provider does not have access to this patient's screening history.",
                )
            return self.repository.list_for_patient(patient_id)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This role is not allowed to view screening history.",
        )

    def get_screening_detail(self, *, current_user, screening_id: int) -> Screening:
        screening = self.repository.get_screening_by_id(screening_id)
        if screening is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Screening was not found.",
            )

        allowed_history = self.list_history_for_patient(current_user=current_user, patient_id=screening.patient_id)
        allowed_ids = {item.id for item in allowed_history}
        if screening.id not in allowed_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this screening.",
            )

        return screening

    def review_screening(self, *, current_user, screening_id: int, payload: ScreeningReviewUpdate) -> Screening:
        role_name = self._role_name(current_user)
        if role_name not in {"admin", "care_coordinator", "provider"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only staff users may review a screening.",
            )

        screening = self.get_screening_detail(current_user=current_user, screening_id=screening_id)
        return self.repository.update_review(
            screening,
            review_notes=payload.review_notes,
            status=payload.status,
        )
```

---

# 6) `app/modules/screenings/router.py`

```python
from __future__ import annotations

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.common.permissions.dependencies import require_roles
from app.common.utils.response import success_response
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.screenings.schemas import (
    EPDSSubmissionCreate,
    ScreeningReviewUpdate,
)
from app.modules.screenings.service import ScreeningService


router = APIRouter(prefix="/screenings", tags=["Screenings"])


@router.post("/epds")
def submit_epds_screening(
    payload: EPDSSubmissionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    screening = ScreeningService(db).submit_epds(current_user=current_user, payload=payload)
    return success_response(
        message="EPDS screening submitted successfully.",
        data=screening,
        status_code=201,
    )


@router.get("/me")
def get_my_screening_history(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("patient")),
):
    history = ScreeningService(db).list_history_for_current_patient(current_user=current_user)
    return success_response(
        message="Patient screening history retrieved successfully.",
        data=history,
    )


@router.get("/patients/{patient_id}")
def get_patient_screening_history(
    patient_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    history = ScreeningService(db).list_history_for_patient(
        current_user=current_user,
        patient_id=patient_id,
    )
    return success_response(
        message="Patient screening history retrieved successfully.",
        data=history,
    )


@router.get("/{screening_id}")
def get_screening_detail(
    screening_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    screening = ScreeningService(db).get_screening_detail(
        current_user=current_user,
        screening_id=screening_id,
    )
    return success_response(
        message="Screening detail retrieved successfully.",
        data=screening,
    )


@router.patch("/{screening_id}/review")
def review_screening(
    screening_id: int,
    payload: ScreeningReviewUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("provider", "care_coordinator", "admin")),
):
    screening = ScreeningService(db).review_screening(
        current_user=current_user,
        screening_id=screening_id,
        payload=payload,
    )
    return success_response(
        message="Screening review updated successfully.",
        data=screening,
    )
```

---

# 7) `tests/modules/screenings/test_epds_scoring.py`

```python
from __future__ import annotations

from app.modules.screenings.constants import (
    EPDS_BAND_FOLLOW_UP,
    EPDS_BAND_URGENT,
    EPDS_BAND_WITHIN_RANGE,
)
from app.modules.screenings.scoring import EPDSEngine, EPDSValidationError


def test_epds_scoring_calculates_expected_total_for_mixed_answers():
    payload = {
        "q1": 0,
        "q2": 1,
        "q3": 0,
        "q4": 2,
        "q5": 1,
        "q6": 2,
        "q7": 3,
        "q8": 0,
        "q9": 1,
        "q10": 3,
    }

    result = EPDSEngine.evaluate(payload)

    assert result.raw_answers["q1"] == 0
    assert result.scored_answers["q1"] == 0
    assert result.scored_answers["q3"] == 3
    assert result.scored_answers["q5"] == 2
    assert result.scored_answers["q10"] == 0
    assert result.total_score == 14
    assert result.severity_band == EPDS_BAND_URGENT
    assert result.critical_flag is False


def test_epds_banding_within_range_monitor():
    payload = {
        "q1": 0,
        "q2": 0,
        "q3": 3,
        "q4": 0,
        "q5": 3,
        "q6": 3,
        "q7": 3,
        "q8": 3,
        "q9": 3,
        "q10": 3,
    }

    result = EPDSEngine.evaluate(payload)
    assert result.total_score == 0
    assert result.severity_band == EPDS_BAND_WITHIN_RANGE


def test_epds_banding_follow_up_recommended():
    payload = {
        "q1": 1,
        "q2": 1,
        "q3": 1,
        "q4": 1,
        "q5": 1,
        "q6": 2,
        "q7": 2,
        "q8": 2,
        "q9": 3,
        "q10": 3,
    }

    result = EPDSEngine.evaluate(payload)
    assert result.total_score == 10
    assert result.severity_band == EPDS_BAND_FOLLOW_UP


def test_epds_rejects_missing_question_keys():
    payload = {
        "q1": 0,
        "q2": 0,
        "q3": 0,
        "q4": 0,
        "q5": 0,
        "q6": 0,
        "q7": 0,
        "q8": 0,
        "q9": 0,
    }

    try:
        EPDSEngine.evaluate(payload)
        assert False, "Expected EPDSValidationError"
    except EPDSValidationError as exc:
        assert "missing keys" in str(exc)
```

---

# 8) `tests/modules/screenings/test_epds_risk_flags.py`

```python
from __future__ import annotations

from app.modules.screenings.scoring import EPDSEngine


BASE_SAFE_PAYLOAD = {
    "q1": 0,
    "q2": 0,
    "q3": 3,
    "q4": 0,
    "q5": 3,
    "q6": 3,
    "q7": 3,
    "q8": 3,
    "q9": 3,
    "q10": 3,
}


def test_item_10_never_selected_does_not_raise_critical_flag():
    result = EPDSEngine.evaluate(BASE_SAFE_PAYLOAD)
    assert result.scored_answers["q10"] == 0
    assert result.critical_flag is False


def test_item_10_hardly_ever_sets_critical_flag():
    payload = dict(BASE_SAFE_PAYLOAD)
    payload["q10"] = 2

    result = EPDSEngine.evaluate(payload)
    assert result.scored_answers["q10"] == 1
    assert result.critical_flag is True


def test_item_10_sometimes_sets_critical_flag():
    payload = dict(BASE_SAFE_PAYLOAD)
    payload["q10"] = 1

    result = EPDSEngine.evaluate(payload)
    assert result.scored_answers["q10"] == 2
    assert result.critical_flag is True


def test_item_10_quite_often_sets_critical_flag():
    payload = dict(BASE_SAFE_PAYLOAD)
    payload["q10"] = 0

    result = EPDSEngine.evaluate(payload)
    assert result.scored_answers["q10"] == 3
    assert result.critical_flag is True
```

---

# 9) `tests/modules/screenings/test_epds_submission.py`

```python
from __future__ import annotations

from datetime import datetime, timezone

from app.db.models.appointment import Appointment
from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.role import Role
from app.db.models.user import User


EPDS_PAYLOAD = {
    "answers": {
        "q1": 1,
        "q2": 1,
        "q3": 1,
        "q4": 1,
        "q5": 1,
        "q6": 1,
        "q7": 1,
        "q8": 1,
        "q9": 1,
        "q10": 3,
    }
}


def _create_role(db, name: str) -> Role:
    role = db.query(Role).filter(Role.name == name).first()
    if role is None:
        role = Role(name=name, description=f"{name.title()} role")
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


def _create_user(db, *, email: str, role_name: str) -> User:
    role = _create_role(db, role_name)
    user = User(
        first_name=role_name.title(),
        last_name="Tester",
        email=email,
        phone="0700000000",
        password_hash="not-used-in-this-test",
        role_id=role.id,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _create_patient_profile(db, *, email: str = "patient@example.com"):
    user = _create_user(db, email=email, role_name="patient")
    patient = Patient(user_id=user.id, consent_status=True)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return user, patient


def _create_provider_with_patient_access(db, patient_id: int):
    provider_user = _create_user(db, email="provider@example.com", role_name="provider")
    provider = Provider(user_id=provider_user.id, specialty="Mental Health")
    db.add(provider)
    db.commit()
    db.refresh(provider)

    appointment = Appointment(
        patient_id=patient_id,
        provider_id=provider.id,
        appointment_type="mental_health",
        reason="Follow-up visit",
        scheduled_start=datetime(2026, 1, 10, 9, 0, tzinfo=timezone.utc),
        scheduled_end=datetime(2026, 1, 10, 9, 30, tzinfo=timezone.utc),
        timezone_name="UTC",
        status="booked",
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return provider_user, provider


def test_patient_can_submit_epds_screening(client, db_session, auth_headers_for_user):
    patient_user, patient = _create_patient_profile(db_session, email="screen_patient@example.com")

    response = client.post(
        "/screenings/epds",
        json=EPDS_PAYLOAD,
        headers=auth_headers_for_user(patient_user),
    )

    assert response.status_code == 201, response.text
    body = response.json()
    assert body["success"] is True
    assert body["data"]["patient_id"] == patient.id
    assert body["data"]["screening_type"] == "EPDS"
    assert "score" in body["data"]
    assert "severity_band" in body["data"]


def test_patient_can_fetch_own_screening_history(client, db_session, auth_headers_for_user):
    patient_user, _patient = _create_patient_profile(db_session, email="history_patient@example.com")

    create_response = client.post(
        "/screenings/epds",
        json=EPDS_PAYLOAD,
        headers=auth_headers_for_user(patient_user),
    )
    assert create_response.status_code == 201, create_response.text

    history_response = client.get(
        "/screenings/me",
        headers=auth_headers_for_user(patient_user),
    )

    assert history_response.status_code == 200, history_response.text
    body = history_response.json()
    assert body["success"] is True
    assert len(body["data"]) >= 1


def test_provider_with_related_appointment_can_view_patient_history(client, db_session, auth_headers_for_user):
    patient_user, patient = _create_patient_profile(db_session, email="linked_patient@example.com")
    provider_user, _provider = _create_provider_with_patient_access(db_session, patient.id)

    submit_response = client.post(
        "/screenings/epds",
        json=EPDS_PAYLOAD,
        headers=auth_headers_for_user(patient_user),
    )
    assert submit_response.status_code == 201, submit_response.text

    history_response = client.get(
        f"/screenings/patients/{patient.id}",
        headers=auth_headers_for_user(provider_user),
    )

    assert history_response.status_code == 200, history_response.text
    assert history_response.json()["success"] is True


def test_provider_without_patient_relationship_is_denied(client, db_session, auth_headers_for_user):
    patient_user, patient = _create_patient_profile(db_session, email="guard_patient@example.com")
    unrelated_provider_user = _create_user(
        db_session,
        email="unrelated_provider@example.com",
        role_name="provider",
    )
    unrelated_provider = Provider(user_id=unrelated_provider_user.id, specialty="Lactation")
    db_session.add(unrelated_provider)
    db_session.commit()

    submit_response = client.post(
        "/screenings/epds",
        json=EPDS_PAYLOAD,
        headers=auth_headers_for_user(patient_user),
    )
    assert submit_response.status_code == 201, submit_response.text

    history_response = client.get(
        f"/screenings/patients/{patient.id}",
        headers=auth_headers_for_user(unrelated_provider_user),
    )

    assert history_response.status_code == 403, history_response.text
```

---

## Suggested `tests/conftest.py` addition if you do not already have it

If your current Phase 3 test setup does **not** already provide `auth_headers_for_user`, add this fixture into `tests/conftest.py`.

```python
from __future__ import annotations

import pytest

from app.common.utils.security import issue_token_pair


@pytest.fixture
def auth_headers_for_user():
    def _factory(user):
        role_name = getattr(getattr(user, "role", None), "name", "") or ""
        tokens = issue_token_pair(
            user_id=str(user.id),
            email=user.email,
            role=role_name,
        )
        return {"Authorization": f"Bearer {tokens['access_token']}"}

    return _factory
```

---

## Migration note for this phase
This phase does **not** require a migration **if** your `screenings` table already includes the Phase 2 fields assumed by this code:

- `answers_json`
- `score`
- `severity_band`
- `interpretation`
- `critical_flag`
- `review_notes`
- `patient_id`
- `encounter_id`
- `created_by_user_id`

If your actual model or migration history is missing any of those fields, run:

```bash
alembic revision --autogenerate -m "align screening schema for EPDS workflow"
alembic upgrade head
```

---

## Test commands for this phase

Run the screening-specific tests:

```bash
pytest tests/modules/screenings/test_epds_submission.py -q
pytest tests/modules/screenings/test_epds_scoring.py -q
pytest tests/modules/screenings/test_epds_risk_flags.py -q
```

Or run them together:

```bash
pytest tests/modules/screenings -q
```

---

## Completion checklist
You can treat this phase as done when all of the following are true:

- EPDS submissions are accepted and stored successfully
- score calculation is handled centrally on the backend
- severity banding is consistent and test-covered
- item 10 critical responses are flagged reliably
- patients can retrieve their own screening history
- providers can view screening history only when access is justified by relationship
- staff can add review notes without changing the underlying scoring logic

---

## Clinical safety note for implementation
This code supports structured screening and review workflows, but it must not be treated as autonomous clinical decision-making. Before production release, align the exact EPDS wording, response order, thresholds, escalation rules, and urgent-response workflow with the project's clinical and governance stakeholders.
