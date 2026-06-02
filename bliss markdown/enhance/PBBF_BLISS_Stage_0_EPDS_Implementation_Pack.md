# Stage 0 Implementation Pack — EPDS International Standard Lock

**Project:** PBBF BLISS Telehealth Platform  
**Stage:** 0 — EPDS International Standard Lock  
**Goal:** Replace the current custom/paraphrased EPDS implementation with a standard Edinburgh Postnatal Depression Scale workflow.

---

## 0.1 Implementation Position

This implementation pack assumes the following files already exist in the inspected repository and should be **updated**, not rediscovered:

### Backend files to update

```text
pbbf-api/app/modules/screenings/constants.py
pbbf-api/app/modules/screenings/scoring.py
pbbf-api/app/modules/screenings/schemas.py
pbbf-api/app/modules/screenings/service.py
pbbf-api/app/modules/screenings/router.py
pbbf-api/tests/modules/screenings/test_epds_submission.py
pbbf-api/tests/modules/screenings/test_epds_scoring.py
pbbf-api/tests/modules/screenings/test_epds_risk_flags.py
pbbf-api/tests/modules/screenings/test_safety_flag_rules.py
```

### Frontend files to update

```text
pbbf-telehealth/src/modules/screenings/utils/epdsQuestions.js
pbbf-telehealth/src/modules/screenings/hooks/useEpdsForm.js
pbbf-telehealth/src/modules/screenings/components/EpdsQuestionnaire.jsx
pbbf-telehealth/src/modules/screenings/components/ScoreSummaryCard.jsx
pbbf-telehealth/src/pages/patient/Screening.jsx
pbbf-telehealth/src/modules/screenings/__tests__/EpdsQuestionnaire.test.jsx
pbbf-telehealth/src/modules/screenings/__tests__/ScreeningPage.test.jsx
pbbf-telehealth/src/modules/screenings/__tests__/useEpdsForm.test.jsx
```

### New files to create

```text
pbbf-api/docs/clinical-operations/epds-standard-implementation.md
pbbf-api/tests/modules/screenings/test_epds_standard_question_order.py
pbbf-api/tests/modules/screenings/test_epds_item10_review_required.py
pbbf-api/tests/modules/screenings/test_epds_threshold_config.py
pbbf-telehealth/src/modules/screenings/utils/epdsStandard.js
pbbf-telehealth/src/modules/screenings/__tests__/EpdsStandard.test.js
```

---

## 0.2 Standard EPDS Rules Locked for Implementation

The platform must implement the Edinburgh Postnatal Depression Scale as a standard 10-item screening workflow.

Rules to enforce:

```text
- The questionnaire has 10 items.
- The recall period is “in the past 7 days.”
- Items 1, 2, and 4 are scored normally: top response = 0, bottom response = 3.
- Items 3 and 5–10 are reverse-scored: top response = 3, bottom response = 0.
- Maximum score is 30.
- Score >= 10 is treated as a possible positive screen / follow-up threshold.
- Score > 13 is treated as higher concern and requires careful clinical review.
- Item 10 must always be reviewed independently.
- EPDS score supports clinical workflow but must not override clinical judgment.
```

Clinical safety note:

```text
The platform must not diagnose. It stores and displays screening results for qualified care-team review.
```

---

# 1. Backend Implementation

---

## 1.1 Update: `pbbf-api/app/modules/screenings/constants.py`

### Action

**Replace the EPDS-specific constants section** with the following standard configuration. If the file contains unrelated role/status constants, keep them and replace only the EPDS block.

```python
from __future__ import annotations

EPDS_SCREENING_TYPE = "epds"
EPDS_QUESTION_COUNT = 10
EPDS_MIN_OPTION_INDEX = 0
EPDS_MAX_OPTION_INDEX = 3
EPDS_MAX_SCORE = 30

EPDS_ALLOWED_QUESTION_KEYS = tuple(f"q{index}" for index in range(1, EPDS_QUESTION_COUNT + 1))

# Standard EPDS scoring direction:
# Items 1, 2, and 4: top answer = 0, bottom answer = 3.
# Items 3 and 5-10: top answer = 3, bottom answer = 0.
EPDS_NORMAL_SCORED_QUESTIONS = {1, 2, 4}
EPDS_REVERSE_SCORED_QUESTIONS = {3, 5, 6, 7, 8, 9, 10}

# Backwards-compatible alias if existing code/tests use this name.
EPDS_DIRECT_SCORED_QUESTIONS = EPDS_NORMAL_SCORED_QUESTIONS

EPDS_POSSIBLE_POSITIVE_THRESHOLD = 10
EPDS_HIGHER_CONCERN_THRESHOLD = 14

EPDS_SEVERITY_LOWER = "lower_concern"
EPDS_SEVERITY_POSSIBLE_DEPRESSION = "possible_depression"
EPDS_SEVERITY_HIGHER_CONCERN = "higher_concern"

EPDS_SCORE_BANDS = (
    (0, 9, EPDS_SEVERITY_LOWER),
    (10, 13, EPDS_SEVERITY_POSSIBLE_DEPRESSION),
    (14, 30, EPDS_SEVERITY_HIGHER_CONCERN),
)

EPDS_INTERPRETATIONS = {
    EPDS_SEVERITY_LOWER: (
        "Score is below the common EPDS follow-up threshold. Continue routine clinical judgment."
    ),
    EPDS_SEVERITY_POSSIBLE_DEPRESSION: (
        "Score is at or above the common EPDS follow-up threshold and should be reviewed by the care team."
    ),
    EPDS_SEVERITY_HIGHER_CONCERN: (
        "Score is above 13 and indicates higher likelihood of depressive illness; careful clinical review is required."
    ),
}

# Item 10 must always be reviewed independently.
# Raw item 10 options are selected top-to-bottom from 0..3.
# Because item 10 is reverse-scored, raw values 0, 1, and 2 indicate some level of concern,
# while raw value 3 corresponds to "Never" and scores 0.
EPDS_ITEM_10_KEY = "q10"
EPDS_ITEM_10_REVIEW_RAW_VALUES = {0, 1, 2}
EPDS_ITEM_10_NO_CONCERN_RAW_VALUE = 3

# After reverse scoring, any scored value greater than 0 requires review.
EPDS_ITEM_10_CRITICAL_SCORES = {1, 2, 3}

CARE_TEAM_REVIEW_ROLES = {
    "provider",
    "counselor",
    "care_coordinator",
    "lactation_consultant",
    "admin",
}
```

### Why this file changes

The existing frontend currently uses simplified custom wording and local scoring. This constants file locks the standard scoring rules centrally on the backend.

---

## 1.2 Update: `pbbf-api/app/modules/screenings/scoring.py`

### Action

**Replace the file content** with the following backend-authoritative EPDS scoring engine.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.modules.screenings.constants import (
    EPDS_ALLOWED_QUESTION_KEYS,
    EPDS_INTERPRETATIONS,
    EPDS_ITEM_10_CRITICAL_SCORES,
    EPDS_ITEM_10_KEY,
    EPDS_MAX_OPTION_INDEX,
    EPDS_MAX_SCORE,
    EPDS_MIN_OPTION_INDEX,
    EPDS_NORMAL_SCORED_QUESTIONS,
    EPDS_QUESTION_COUNT,
    EPDS_REVERSE_SCORED_QUESTIONS,
    EPDS_SCORE_BANDS,
)


class EPDSValidationError(ValueError):
    """Raised when an EPDS answer payload is incomplete or invalid."""


@dataclass(slots=True)
class EPDSScoreResult:
    raw_answers: dict[str, int]
    scored_answers: dict[str, int]
    total_score: int
    severity_band: str
    interpretation: str
    critical_flag: bool
    item_10_score: int
    item_10_requires_review: bool


class EPDSEngine:
    """
    Backend-authoritative EPDS scoring engine.

    Input answers are raw selected option indexes from 0..3, where 0 is the top
    option shown to the patient and 3 is the bottom option shown to the patient.
    """

    @staticmethod
    def normalize_answers(answers: dict[str, Any] | list[Any]) -> dict[str, int]:
        if isinstance(answers, list):
            if len(answers) != EPDS_QUESTION_COUNT:
                raise EPDSValidationError(f"EPDS requires exactly {EPDS_QUESTION_COUNT} answers.")
            answers = {f"q{index + 1}": value for index, value in enumerate(answers)}

        if not isinstance(answers, dict):
            raise EPDSValidationError("EPDS answers must be an object keyed by q1 through q10.")

        expected = set(EPDS_ALLOWED_QUESTION_KEYS)
        actual = set(answers.keys())

        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            details: list[str] = []
            if missing:
                details.append(f"missing keys: {', '.join(missing)}")
            if extra:
                details.append(f"unexpected keys: {', '.join(extra)}")
            raise EPDSValidationError("Invalid EPDS answer payload: " + "; ".join(details))

        normalized: dict[str, int] = {}
        for key in EPDS_ALLOWED_QUESTION_KEYS:
            value = answers[key]
            if isinstance(value, bool) or not isinstance(value, int):
                raise EPDSValidationError(f"{key} must be an integer from 0 to 3.")
            if value < EPDS_MIN_OPTION_INDEX or value > EPDS_MAX_OPTION_INDEX:
                raise EPDSValidationError(f"{key} must be between 0 and 3.")
            normalized[key] = value

        return normalized

    @staticmethod
    def score_answers(raw_answers: dict[str, int]) -> dict[str, int]:
        scored: dict[str, int] = {}

        for question_number in range(1, EPDS_QUESTION_COUNT + 1):
            key = f"q{question_number}"
            raw_value = raw_answers[key]

            if question_number in EPDS_NORMAL_SCORED_QUESTIONS:
                scored_value = raw_value
            elif question_number in EPDS_REVERSE_SCORED_QUESTIONS:
                scored_value = EPDS_MAX_OPTION_INDEX - raw_value
            else:
                raise EPDSValidationError(f"Question {question_number} is not configured for scoring.")

            scored[key] = scored_value

        return scored

    @staticmethod
    def classify(total_score: int) -> tuple[str, str]:
        if total_score < 0 or total_score > EPDS_MAX_SCORE:
            raise EPDSValidationError("EPDS score is outside the supported range.")

        for minimum, maximum, band in EPDS_SCORE_BANDS:
            if minimum <= total_score <= maximum:
                return band, EPDS_INTERPRETATIONS[band]

        raise EPDSValidationError("EPDS score could not be classified.")

    @staticmethod
    def item_10_score(scored_answers: dict[str, int]) -> int:
        return scored_answers[EPDS_ITEM_10_KEY]

    @classmethod
    def has_critical_flag(cls, scored_answers: dict[str, int]) -> bool:
        return cls.item_10_score(scored_answers) in EPDS_ITEM_10_CRITICAL_SCORES

    @classmethod
    def evaluate(cls, answers: dict[str, Any] | list[Any]) -> EPDSScoreResult:
        raw_answers = cls.normalize_answers(answers)
        scored_answers = cls.score_answers(raw_answers)
        total_score = sum(scored_answers.values())
        severity_band, interpretation = cls.classify(total_score)
        item_10_score = cls.item_10_score(scored_answers)
        critical_flag = cls.has_critical_flag(scored_answers)

        return EPDSScoreResult(
            raw_answers=raw_answers,
            scored_answers=scored_answers,
            total_score=total_score,
            severity_band=severity_band,
            interpretation=interpretation,
            critical_flag=critical_flag,
            item_10_score=item_10_score,
            item_10_requires_review=critical_flag,
        )


# Compatibility helpers for older tests/imports.
def calculate_epds_score(answers: dict[str, int] | list[int]) -> int:
    return EPDSEngine.evaluate(answers).total_score


def classify_epds_band(score: int) -> str:
    return EPDSEngine.classify(score)[0]


def has_safety_sensitive_flag(answers: dict[str, int] | list[int]) -> bool:
    return EPDSEngine.evaluate(answers).critical_flag
```

### Why this file changes

The backend becomes the source of truth for scoring, classification, and item-10 review. The frontend must not own final EPDS scoring.

---

## 1.3 Update: `pbbf-api/app/modules/screenings/schemas.py`

### Action

**Add or replace the EPDS answer schema section** with the following. Keep unrelated schemas if they already exist.

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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
    answers: EPDSAnswers
    patient_id: int | None = Field(default=None, gt=0)
    encounter_id: int | None = Field(default=None, gt=0)


class ScreeningReviewUpdate(BaseModel):
    status: Literal["completed", "reviewed", "follow_up_required", "closed"] = "reviewed"
    review_notes: str | None = Field(default=None, max_length=5000)


class ScreeningResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    encounter_id: int | None = None
    screening_type: str
    answers_json: dict
    score: int
    severity_band: str | None = None
    interpretation: str | None = None
    critical_flag: bool = False
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
```

### Why this file changes

The frontend must submit a `q1` through `q10` object, not an array of `{question_id, score}` items.

---

## 1.4 Update: `pbbf-api/app/modules/screenings/service.py`

### Action

**Update the `submit_epds` method** to use the standard scoring engine and persist item-10 metadata.

Locate:

```python
def submit_epds(...):
```

Replace the scoring/persistence block with:

```python
try:
    evaluation = EPDSEngine.evaluate(payload.answers.model_dump())
except EPDSValidationError as exc:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(exc),
    ) from exc

answers_json = {
    "format": "epds_standard_v1",
    "recall_period": "past_7_days",
    "raw_answers": evaluation.raw_answers,
    "scored_answers": evaluation.scored_answers,
    "item_10": {
        "score": evaluation.item_10_score,
        "requires_review": evaluation.item_10_requires_review,
    },
    "scoring_rules": {
        "normal_scored_questions": [1, 2, 4],
        "reverse_scored_questions": [3, 5, 6, 7, 8, 9, 10],
        "maximum_score": 30,
    },
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
```

### Optional audit hook for later stage

If audit wiring is already safe in your branch, add:

```python
if evaluation.critical_flag:
    # Later Stage 8 should create a formal audit/care-team review event here.
    pass
```

Do **not** invent a clinical diagnosis or automated treatment action here. This stage only flags review.

---

## 1.5 Update: `pbbf-api/app/modules/screenings/router.py`

### Action

Keep the existing route shape if already used by frontend:

```text
POST /screenings/epds
GET /screenings/me
GET /screenings/patients/{patient_id}
GET /screenings/{screening_id}
PATCH /screenings/{screening_id}/review
```

Ensure the submit route returns backend scoring fields.

```python
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
```

---

# 2. Backend Tests

---

## 2.1 Update: `pbbf-api/tests/modules/screenings/test_epds_scoring.py`

### Action

Replace or complete test content with:

```python
from app.modules.screenings.scoring import EPDSEngine


def test_epds_standard_all_bottom_answers_scores_expected_mix():
    answers = {
        "q1": 3,
        "q2": 3,
        "q3": 3,
        "q4": 3,
        "q5": 3,
        "q6": 3,
        "q7": 3,
        "q8": 3,
        "q9": 3,
        "q10": 3,
    }

    result = EPDSEngine.evaluate(answers)

    assert result.scored_answers["q1"] == 3
    assert result.scored_answers["q2"] == 3
    assert result.scored_answers["q4"] == 3
    assert result.scored_answers["q3"] == 0
    assert result.scored_answers["q5"] == 0
    assert result.scored_answers["q10"] == 0
    assert result.total_score == 9
    assert result.critical_flag is False


def test_epds_standard_all_top_answers_scores_expected_mix():
    answers = {f"q{i}": 0 for i in range(1, 11)}

    result = EPDSEngine.evaluate(answers)

    assert result.scored_answers["q1"] == 0
    assert result.scored_answers["q2"] == 0
    assert result.scored_answers["q4"] == 0
    assert result.scored_answers["q3"] == 3
    assert result.scored_answers["q5"] == 3
    assert result.scored_answers["q10"] == 3
    assert result.total_score == 21
    assert result.critical_flag is True


def test_epds_max_score_is_30():
    answers = {
        "q1": 3,
        "q2": 3,
        "q3": 0,
        "q4": 3,
        "q5": 0,
        "q6": 0,
        "q7": 0,
        "q8": 0,
        "q9": 0,
        "q10": 0,
    }

    result = EPDSEngine.evaluate(answers)

    assert result.total_score == 30
```

---

## 2.2 Create: `pbbf-api/tests/modules/screenings/test_epds_standard_question_order.py`

```python
from app.modules.screenings.constants import EPDS_ALLOWED_QUESTION_KEYS, EPDS_QUESTION_COUNT


def test_epds_question_keys_are_q1_to_q10_in_order():
    assert EPDS_QUESTION_COUNT == 10
    assert EPDS_ALLOWED_QUESTION_KEYS == (
        "q1",
        "q2",
        "q3",
        "q4",
        "q5",
        "q6",
        "q7",
        "q8",
        "q9",
        "q10",
    )
```

---

## 2.3 Create: `pbbf-api/tests/modules/screenings/test_epds_item10_review_required.py`

```python
from app.modules.screenings.scoring import EPDSEngine


def base_answers():
    return {
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


def test_item_10_never_does_not_raise_critical_flag():
    answers = base_answers()
    answers["q10"] = 3

    result = EPDSEngine.evaluate(answers)

    assert result.item_10_score == 0
    assert result.critical_flag is False
    assert result.item_10_requires_review is False


def test_item_10_any_nonzero_scored_value_requires_review():
    for raw_value in [0, 1, 2]:
        answers = base_answers()
        answers["q10"] = raw_value

        result = EPDSEngine.evaluate(answers)

        assert result.item_10_score > 0
        assert result.critical_flag is True
        assert result.item_10_requires_review is True
```

---

## 2.4 Create: `pbbf-api/tests/modules/screenings/test_epds_threshold_config.py`

```python
from app.modules.screenings.scoring import EPDSEngine


def test_score_9_is_lower_concern():
    band, interpretation = EPDSEngine.classify(9)
    assert band == "lower_concern"
    assert "below" in interpretation.lower()


def test_score_10_is_possible_depression_threshold():
    band, interpretation = EPDSEngine.classify(10)
    assert band == "possible_depression"
    assert "threshold" in interpretation.lower() or "review" in interpretation.lower()


def test_score_14_is_higher_concern():
    band, interpretation = EPDSEngine.classify(14)
    assert band == "higher_concern"
    assert "higher" in interpretation.lower() or "careful" in interpretation.lower()
```

---

## 2.5 Update: `pbbf-api/tests/modules/screenings/test_epds_risk_flags.py`

Add or ensure:

```python
from app.modules.screenings.scoring import EPDSEngine


def test_high_total_score_without_item10_still_needs_score_review_but_not_item10_flag():
    answers = {
        "q1": 3,
        "q2": 3,
        "q3": 0,
        "q4": 3,
        "q5": 0,
        "q6": 0,
        "q7": 0,
        "q8": 0,
        "q9": 0,
        "q10": 3,
    }

    result = EPDSEngine.evaluate(answers)

    assert result.total_score == 27
    assert result.severity_band == "higher_concern"
    assert result.critical_flag is False


def test_low_total_score_with_item10_flag_still_requires_review():
    answers = {
        "q1": 0,
        "q2": 0,
        "q3": 3,
        "q4": 0,
        "q5": 3,
        "q6": 3,
        "q7": 3,
        "q8": 3,
        "q9": 3,
        "q10": 2,
    }

    result = EPDSEngine.evaluate(answers)

    assert result.total_score == 1
    assert result.critical_flag is True
```

---

# 3. Backend Documentation

---

## 3.1 Create: `pbbf-api/docs/clinical-operations/epds-standard-implementation.md`

```markdown
# EPDS Standard Implementation

## Purpose

The PBBF BLISS platform implements the Edinburgh Postnatal Depression Scale as a standardized screening workflow for perinatal/postnatal depression risk review.

## Scope

This implementation supports:

- patient EPDS submission,
- backend-authoritative scoring,
- severity banding,
- item-10 independent review flagging,
- care-team review visibility.

## Standard scoring rules

- The EPDS has 10 items.
- The recall period is the past 7 days.
- Items 1, 2, and 4 are scored normally: top answer = 0, bottom answer = 3.
- Items 3 and 5–10 are reverse-scored: top answer = 3, bottom answer = 0.
- Maximum total score is 30.
- Score >= 10 is treated as possible follow-up threshold.
- Score > 13 is treated as higher concern requiring careful clinical review.
- Item 10 must always be reviewed independently.

## Clinical safety note

The EPDS is a screening tool and does not replace clinical judgment. The platform must not present EPDS results as a diagnosis.

## Backend authority

The backend scoring engine in `app/modules/screenings/scoring.py` is the scoring authority. Frontend calculations are not authoritative.

## Item 10 handling

Item 10 is reverse-scored. Any scored value greater than 0 creates `critical_flag=True` and `item_10_requires_review=True`.
```

---

# 4. Frontend Implementation

---

## 4.1 Create: `pbbf-telehealth/src/modules/screenings/utils/epdsStandard.js`

```javascript
export const EPDS_RECALL_PERIOD_LABEL = "In the past 7 days";

export const EPDS_STANDARD_VERSION = "epds_standard_v1";

export const EPDS_RESPONSE_VALUES = Object.freeze({
  FIRST_OPTION: 0,
  SECOND_OPTION: 1,
  THIRD_OPTION: 2,
  FOURTH_OPTION: 3,
});

export const EPDS_NORMAL_SCORED_ITEMS = [1, 2, 4];
export const EPDS_REVERSE_SCORED_ITEMS = [3, 5, 6, 7, 8, 9, 10];

export const EPDS_THRESHOLDS = Object.freeze({
  POSSIBLE_POSITIVE: 10,
  HIGHER_CONCERN: 14,
  MAX_SCORE: 30,
});

export const EPDS_QUESTIONS_STANDARD = [
  {
    id: "q1",
    number: 1,
    prompt: "I have been able to laugh and see the funny side of things",
    scoring: "normal",
    options: [
      "As much as I always could",
      "Not quite so much now",
      "Definitely not so much now",
      "Not at all",
    ],
  },
  {
    id: "q2",
    number: 2,
    prompt: "I have looked forward with enjoyment to things",
    scoring: "normal",
    options: [
      "As much as I ever did",
      "Rather less than I used to",
      "Definitely less than I used to",
      "Hardly at all",
    ],
  },
  {
    id: "q3",
    number: 3,
    prompt: "I have blamed myself unnecessarily when things went wrong",
    scoring: "reverse",
    options: [
      "Yes, most of the time",
      "Yes, some of the time",
      "Not very often",
      "No, never",
    ],
  },
  {
    id: "q4",
    number: 4,
    prompt: "I have been anxious or worried for no good reason",
    scoring: "normal",
    options: [
      "No, not at all",
      "Hardly ever",
      "Yes, sometimes",
      "Yes, very often",
    ],
  },
  {
    id: "q5",
    number: 5,
    prompt: "I have felt scared or panicky for no very good reason",
    scoring: "reverse",
    options: [
      "Yes, quite a lot",
      "Yes, sometimes",
      "No, not much",
      "No, not at all",
    ],
  },
  {
    id: "q6",
    number: 6,
    prompt: "Things have been getting on top of me",
    scoring: "reverse",
    options: [
      "Yes, most of the time I haven’t been able to cope at all",
      "Yes, sometimes I haven’t been coping as well as usual",
      "No, most of the time I have coped quite well",
      "No, I have been coping as well as ever",
    ],
  },
  {
    id: "q7",
    number: 7,
    prompt: "I have been so unhappy that I have had difficulty sleeping",
    scoring: "reverse",
    options: [
      "Yes, most of the time",
      "Yes, sometimes",
      "Not very often",
      "No, not at all",
    ],
  },
  {
    id: "q8",
    number: 8,
    prompt: "I have felt sad or miserable",
    scoring: "reverse",
    options: [
      "Yes, most of the time",
      "Yes, quite often",
      "Not very often",
      "No, not at all",
    ],
  },
  {
    id: "q9",
    number: 9,
    prompt: "I have been so unhappy that I have been crying",
    scoring: "reverse",
    options: [
      "Yes, most of the time",
      "Yes, quite often",
      "Only occasionally",
      "No, never",
    ],
  },
  {
    id: "q10",
    number: 10,
    prompt: "The thought of harming myself has occurred to me",
    scoring: "reverse",
    safetySensitive: true,
    options: [
      "Yes, quite often",
      "Sometimes",
      "Hardly ever",
      "Never",
    ],
  },
];

export function getInitialEpdsAnswers() {
  return EPDS_QUESTIONS_STANDARD.reduce((accumulator, question) => {
    accumulator[question.id] = null;
    return accumulator;
  }, {});
}

export function areAllEpdsQuestionsAnswered(answers) {
  return EPDS_QUESTIONS_STANDARD.every((question) => answers[question.id] !== null);
}

export function buildEpdsSubmissionPayload(answers) {
  return {
    answers: Object.fromEntries(
      EPDS_QUESTIONS_STANDARD.map((question) => [question.id, Number(answers[question.id])])
    ),
  };
}
```

---

## 4.2 Update: `pbbf-telehealth/src/modules/screenings/utils/epdsQuestions.js`

### Action

Replace the file with compatibility exports that point to the standard config.

```javascript
export {
  EPDS_QUESTIONS_STANDARD as EPDS_QUESTIONS,
  EPDS_RECALL_PERIOD_LABEL,
  areAllEpdsQuestionsAnswered as areAllQuestionsAnswered,
  buildEpdsSubmissionPayload,
  getInitialEpdsAnswers as getInitialAnswers,
} from "./epdsStandard";

export function calculateEpdsScore() {
  return null;
}

export function classifyEpdsBand() {
  return "backend_scored";
}

export function hasSafetyFlag(answers) {
  return Number(answers?.q10 ?? 3) < 3;
}
```

### Why this file changes

Existing imports continue working, but local frontend scoring is no longer treated as authoritative.

---

## 4.3 Update: `pbbf-telehealth/src/modules/screenings/components/EpdsQuestionnaire.jsx`

### Action

Replace option rendering so each question uses its own official response options.

```javascript
import { EPDS_RECALL_PERIOD_LABEL, EPDS_QUESTIONS } from "../utils/epdsQuestions";

export default function EpdsQuestionnaire({
  answers,
  onAnswer,
  onSubmit,
  isSubmitting = false,
  submitError = "",
}) {
  return (
    <form
      className="space-y-8"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
      noValidate
    >
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-sky-700">
          Patient screening
        </p>
        <h2 className="mt-2 text-2xl font-semibold text-slate-900">
          Edinburgh Postnatal Depression Scale
        </h2>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          Please check the answer that comes closest to how you have felt {EPDS_RECALL_PERIOD_LABEL.toLowerCase()}, not just how you feel today.
        </p>
      </div>

      {EPDS_QUESTIONS.map((question) => (
        <section
          key={question.id}
          className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <div className="mb-5">
            <p className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
              Question {question.number} of {EPDS_QUESTIONS.length}
            </p>
            <h3 className="mt-2 text-lg font-semibold text-slate-900">
              {question.prompt}
            </h3>
            {question.safetySensitive ? (
              <p className="mt-2 text-sm leading-6 text-amber-700">
                This item is reviewed independently by the care team.
              </p>
            ) : null}
          </div>

          <div className="grid gap-3">
            {question.options.map((label, index) => {
              const checked = answers[question.id] === index;

              return (
                <label
                  key={`${question.id}-${index}`}
                  className={`flex cursor-pointer items-start gap-3 rounded-2xl border px-4 py-4 transition ${
                    checked
                      ? "border-sky-700 bg-sky-50"
                      : "border-slate-200 bg-white hover:border-slate-300"
                  }`}
                >
                  <input
                    type="radio"
                    name={question.id}
                    checked={checked}
                    onChange={() => onAnswer(question.id, index)}
                    className="mt-1 h-4 w-4 border-slate-300 text-sky-700 focus:ring-sky-500"
                  />
                  <span className="text-sm leading-6 text-slate-700">{label}</span>
                </label>
              );
            })}
          </div>
        </section>
      ))}

      {submitError ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {submitError}
        </div>
      ) : null}

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded-xl bg-sky-700 px-6 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isSubmitting ? "Submitting..." : "Submit screening"}
        </button>
      </div>
    </form>
  );
}
```

---

## 4.4 Update: `pbbf-telehealth/src/modules/screenings/hooks/useEpdsForm.js`

### Action

Replace local scoring and array payload submission with backend-authoritative q1–q10 object submission.

```javascript
import { useCallback, useEffect, useState } from "react";
import { listMyScreeningsRequest, submitEpdsRequest } from "../services/screeningsApi";
import {
  areAllQuestionsAnswered,
  buildEpdsSubmissionPayload,
  getInitialAnswers,
} from "../utils/epdsQuestions";

function normalizeScreening(raw) {
  return {
    id: raw?.id || raw?.screening_id || "temp-screening-id",
    submittedAt: raw?.submitted_at || raw?.submittedAt || raw?.created_at || "",
    score: raw?.score ?? 0,
    band: raw?.severity_band || raw?.band || "not_available",
    interpretation: raw?.interpretation || "",
    status: raw?.status || "completed",
    safetyFlag: Boolean(raw?.critical_flag ?? raw?.safety_flag ?? false),
  };
}

export function useEpdsForm() {
  const [answers, setAnswers] = useState(getInitialAnswers());
  const [priorScreenings, setPriorScreenings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loadError, setLoadError] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [completionMessage, setCompletionMessage] = useState("");
  const [submittedSummary, setSubmittedSummary] = useState(null);

  const loadHistory = useCallback(async () => {
    try {
      setIsLoading(true);
      setLoadError("");

      const response = await listMyScreeningsRequest();
      const payload = response?.data || response;
      const rows = payload?.items || payload?.screenings || payload || [];

      setPriorScreenings(Array.isArray(rows) ? rows.map(normalizeScreening) : []);
    } catch (error) {
      setLoadError(error?.message || "Unable to load screening history.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  function setAnswer(questionId, value) {
    setAnswers((current) => ({
      ...current,
      [questionId]: Number(value),
    }));
    setSubmitError("");
    setCompletionMessage("");
  }

  function resetForm() {
    setAnswers(getInitialAnswers());
    setSubmitError("");
    setCompletionMessage("");
    setSubmittedSummary(null);
  }

  async function submit() {
    if (!areAllQuestionsAnswered(answers)) {
      setSubmitError("Please answer all questions before submitting the screening.");
      return { success: false };
    }

    try {
      setIsSubmitting(true);
      setSubmitError("");

      const response = await submitEpdsRequest(buildEpdsSubmissionPayload(answers));
      const data = response?.data || response;

      const summary = {
        score: data?.score ?? 0,
        band: data?.severity_band || "not_available",
        interpretation: data?.interpretation || "",
        safetyFlag: Boolean(data?.critical_flag ?? false),
      };

      setSubmittedSummary(summary);
      setCompletionMessage(response?.message || "Your screening has been submitted successfully.");

      await loadHistory();

      return { success: true, response, summary };
    } catch (error) {
      setSubmitError(error?.message || "Unable to submit screening.");
      return { success: false, error };
    } finally {
      setIsSubmitting(false);
    }
  }

  return {
    answers,
    priorScreenings,
    isLoading,
    isSubmitting,
    loadError,
    submitError,
    completionMessage,
    submittedSummary,
    setAnswer,
    submit,
    resetForm,
    reload: loadHistory,
  };
}
```

---

## 4.5 Update: `pbbf-telehealth/src/modules/screenings/components/ScoreSummaryCard.jsx`

### Action

Update props to display backend interpretation.

```javascript
function formatSubmittedAt(value) {
  if (!value) return "Not available";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function ScreeningHistoryList({ screenings = [] }) {
  if (!screenings.length) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm">
        No prior screenings are visible yet.
      </div>
    );
  }

  return (
    <div className="grid gap-4">
      {screenings.map((screening) => (
        <div key={screening.id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-sm font-semibold text-slate-900">
                Screening submitted {formatSubmittedAt(screening.submittedAt)}
              </p>
              <p className="mt-1 text-sm text-slate-600">
                Score: <span className="font-medium">{screening.score}</span>
              </p>
              <p className="mt-1 text-sm text-slate-600">
                Band: <span className="font-medium capitalize">{screening.band.replace(/_/g, " ")}</span>
              </p>
            </div>

            <div className="text-sm text-slate-600">
              {screening.safetyFlag ? "Item 10 requires care-team review." : "No item-10 review flag shown."}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default function ScoreSummaryCard({
  score = 0,
  band = "not_available",
  interpretation = "",
  safetyFlag = false,
  completionMessage = "",
}) {
  return (
    <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6 shadow-sm">
      <p className="text-sm font-medium uppercase tracking-[0.2em] text-emerald-700">
        Screening complete
      </p>
      <h2 className="mt-2 text-2xl font-semibold text-emerald-900">
        Submission received
      </h2>

      <p className="mt-3 text-sm leading-6 text-emerald-800">
        {completionMessage || "Your screening has been recorded for care-team review."}
      </p>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Score</p>
          <p className="mt-2 text-2xl font-semibold text-slate-900">{score}</p>
        </div>

        <div className="rounded-2xl bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Follow-up band</p>
          <p className="mt-2 text-base font-semibold capitalize text-slate-900">
            {band.replace(/_/g, " ")}
          </p>
        </div>

        <div className="rounded-2xl bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Item 10 review</p>
          <p className="mt-2 text-sm font-medium text-slate-900">
            {safetyFlag ? "Requires care-team review." : "No item-10 review flag shown."}
          </p>
        </div>
      </div>

      {interpretation ? (
        <div className="mt-5 rounded-2xl border border-emerald-200 bg-white px-4 py-3 text-sm leading-6 text-slate-700">
          {interpretation}
        </div>
      ) : null}
    </div>
  );
}
```

---

## 4.6 Update: `pbbf-telehealth/src/pages/patient/Screening.jsx`

### Action

Pass backend interpretation into `ScoreSummaryCard`.

Replace:

```javascript
<ScoreSummaryCard
  score={submittedSummary.score}
  band={submittedSummary.band}
  safetyFlag={submittedSummary.safetyFlag}
  completionMessage={completionMessage}
/>
```

with:

```javascript
<ScoreSummaryCard
  score={submittedSummary.score}
  band={submittedSummary.band}
  interpretation={submittedSummary.interpretation}
  safetyFlag={submittedSummary.safetyFlag}
  completionMessage={completionMessage}
/>
```

---

# 5. Frontend Tests

---

## 5.1 Create: `pbbf-telehealth/src/modules/screenings/__tests__/EpdsStandard.test.js`

```javascript
import {
  areAllEpdsQuestionsAnswered,
  buildEpdsSubmissionPayload,
  EPDS_QUESTIONS_STANDARD,
  getInitialEpdsAnswers,
} from "../utils/epdsStandard";

test("EPDS standard config contains 10 questions", () => {
  expect(EPDS_QUESTIONS_STANDARD).toHaveLength(10);
  expect(EPDS_QUESTIONS_STANDARD.map((item) => item.id)).toEqual([
    "q1",
    "q2",
    "q3",
    "q4",
    "q5",
    "q6",
    "q7",
    "q8",
    "q9",
    "q10",
  ]);
});

test("initial answers contain q1 through q10 as null", () => {
  expect(getInitialEpdsAnswers()).toEqual({
    q1: null,
    q2: null,
    q3: null,
    q4: null,
    q5: null,
    q6: null,
    q7: null,
    q8: null,
    q9: null,
    q10: null,
  });
});

test("buildEpdsSubmissionPayload returns backend q1-q10 object", () => {
  const answers = {
    q1: 0,
    q2: 1,
    q3: 2,
    q4: 3,
    q5: 0,
    q6: 1,
    q7: 2,
    q8: 3,
    q9: 0,
    q10: 3,
  };

  expect(areAllEpdsQuestionsAnswered(answers)).toBe(true);
  expect(buildEpdsSubmissionPayload(answers)).toEqual({ answers });
});
```

---

## 5.2 Update: `pbbf-telehealth/src/modules/screenings/__tests__/EpdsQuestionnaire.test.jsx`

Add assertions that:

```text
- The heading contains Edinburgh Postnatal Depression Scale.
- The page mentions past 7 days.
- All 10 questions render.
- Question 10 renders the safety review note.
```

Example:

```javascript
import { render, screen } from "@testing-library/react";
import EpdsQuestionnaire from "../components/EpdsQuestionnaire";
import { getInitialAnswers } from "../utils/epdsQuestions";

test("renders standard EPDS questionnaire", () => {
  render(
    <EpdsQuestionnaire
      answers={getInitialAnswers()}
      onAnswer={() => {}}
      onSubmit={() => {}}
    />
  );

  expect(screen.getByText(/Edinburgh Postnatal Depression Scale/i)).toBeInTheDocument();
  expect(screen.getByText(/past 7 days/i)).toBeInTheDocument();
  expect(screen.getByText(/Question 10 of 10/i)).toBeInTheDocument();
  expect(screen.getByText(/reviewed independently/i)).toBeInTheDocument();
});
```

---

# 6. Validation Commands

## Backend

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/screenings/test_epds_scoring.py -q
pytest tests/modules/screenings/test_epds_risk_flags.py -q
pytest tests/modules/screenings/test_safety_flag_rules.py -q
pytest tests/modules/screenings/test_epds_standard_question_order.py -q
pytest tests/modules/screenings/test_epds_item10_review_required.py -q
pytest tests/modules/screenings/test_epds_threshold_config.py -q
```

## Frontend

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm test -- --run src/modules/screenings/__tests__/EpdsStandard.test.js
npm test -- --run src/modules/screenings/__tests__/EpdsQuestionnaire.test.jsx
npm run build
```

---

# 7. Completion Checklist

Stage 0 is complete only when:

```text
[ ] Backend constants encode standard EPDS scoring rules.
[ ] Backend scoring engine scores normal and reverse-scored items correctly.
[ ] Backend rejects incomplete or invalid q1-q10 payloads.
[ ] Backend flags item 10 independently.
[ ] Backend classifies thresholds consistently.
[ ] Frontend renders standard EPDS items and response options.
[ ] Frontend submits q1-q10 object payload.
[ ] Frontend displays backend score and interpretation.
[ ] Frontend does not treat local score as final clinical score.
[ ] Backend and frontend EPDS tests pass.
[ ] EPDS standard implementation doc exists.
```

---

# 8. Important Clinical-Safety Boundary

This implementation does not diagnose postpartum depression and does not replace care-team judgment. It standardizes screening capture, backend scoring, and review flagging so qualified care staff can make appropriate clinical decisions.
