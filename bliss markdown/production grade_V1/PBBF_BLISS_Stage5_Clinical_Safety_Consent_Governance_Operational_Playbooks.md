# PBBF BLISS — Phase 2 Stage 5 Populated Markdown Package
## Clinical Safety, Consent Governance, and Operational Playbooks

## Stage objective
Move from functional workflow to controlled care workflow.

This stage is where the platform stops being only “technically usable” and becomes operationally understandable for real care workflows. The goal is not to add broad new features. The goal is to make sensitive flows more governed, more reviewable, and less ambiguous for patients, providers, and administrators.

---

## Stage outcomes

### Backend stage outcome
The backend confirms and strengthens:
- consent versioning behavior
- screening safety flags
- role review rules
- no-show handling
- referral follow-up expectations
- audit capture for sensitive workflow transitions

### Frontend stage outcome
The frontend improves:
- clarity around screening completion
- consent acknowledgement visibility
- provider note finalization clarity
- telehealth readiness messaging
- safer and clearer care-workflow communication

### Completion gate
Sensitive care workflows are no longer just technically functional; they are operationally understandable and governance-aware.

---

## Repository root
`bliss-telehealth/`

---

# Stage 5 directory structure

```text
bliss-telehealth/
├── docs/
│   └── clinical-operations/
│       ├── consent-version-governance.md
│       ├── screening-escalation-playbook.md
│       ├── no-show-and-follow-up-playbook.md
│       └── referral-operating-guidelines.md
├── pbbf-api/
│   ├── app/
│   │   └── modules/
│   │       ├── intake/
│   │       │   ├── constants.py
│   │       │   ├── repository.py
│   │       │   ├── router.py
│   │       │   ├── schemas.py
│   │       │   ├── service.py
│   │       │   └── validators.py
│   │       ├── screenings/
│   │       │   ├── constants.py
│   │       │   ├── repository.py
│   │       │   ├── router.py
│   │       │   ├── schemas.py
│   │       │   ├── scoring.py
│   │       │   └── service.py
│   │       ├── encounters/
│   │       │   ├── repository.py
│   │       │   ├── router.py
│   │       │   ├── schemas.py
│   │       │   ├── service.py
│   │       │   └── templates.py
│   │       └── referrals/
│   │           ├── repository.py
│   │           ├── router.py
│   │           ├── schemas.py
│   │           └── service.py
│   └── tests/
│       └── modules/
│           ├── intake/
│           │   ├── test_consent_versioning.py
│           │   └── test_sensitive_transition_audit.py
│           ├── screenings/
│           │   ├── test_safety_flag_rules.py
│           │   └── test_role_review_rules.py
│           ├── encounters/
│           │   └── test_finalize_note_governance.py
│           └── referrals/
│               └── test_follow_up_expectations.py
└── pbbf-telehealth/
    ├── src/
    │   ├── modules/
    │   │   ├── intake/
    │   │   ├── screenings/
    │   │   ├── telehealth/
    │   │   ├── encounters/
    │   │   └── referrals/
    │   └── pages/
    │       ├── patient/
    │       │   ├── Dashboard.jsx
    │       │   ├── Screening.jsx
    │       │   └── Session.jsx
    │       └── provider/
    │           ├── Dashboard.jsx
    │           ├── Notes.jsx
    │           └── Referrals.jsx
```

---

# Recommended commands to create missing directories

Run from the `bliss-telehealth` root:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth

mkdir -p docs/clinical-operations
mkdir -p pbbf-api/tests/modules/intake
mkdir -p pbbf-api/tests/modules/screenings
mkdir -p pbbf-api/tests/modules/encounters
mkdir -p pbbf-api/tests/modules/referrals
```

---

# FILE 1 — `[CREATE]` `bliss-telehealth/docs/clinical-operations/consent-version-governance.md`

```md
# PBBF BLISS Consent Version Governance

## Purpose
This document defines how consent acknowledgement must be versioned and interpreted in the platform.

## Core rule
Consent is not only a checkbox. It is a governed acknowledgement tied to:
- a specific consent version
- a specific user
- a specific time
- an auditable transition in workflow state

## Governance requirements
1. The backend must store the consent version associated with the intake submission.
2. Consent acknowledgement must be required before final intake submission.
3. If consent language changes materially, a new consent version must be issued.
4. Historical submissions must remain traceable to the consent version active at the time.
5. Providers and admins should not rewrite historical consent acknowledgements directly.

## Minimum data expectations
Each consent capture should support:
- consent version identifier
- timestamp
- patient identity
- acknowledgement boolean
- audit trail of final submission

## Operational meaning
A patient intake should not be treated as governance-complete unless:
- consent is acknowledged
- the consent version is recorded
- the submission transition is auditable

## Pilot-ready rule
Before controlled rollout, the team must know exactly:
- what version is currently active
- how a new version would be introduced
- how old submissions remain interpretable after version changes
```

---

# FILE 2 — `[CREATE]` `bliss-telehealth/docs/clinical-operations/screening-escalation-playbook.md`

```md
# PBBF BLISS Screening Escalation Playbook

## Purpose
This document defines the minimum operational response expectations for screening results that require follow-up attention.

## Core principle
Screening results are not only stored data. They may represent care-follow-up signals that need human review.

## Workflow expectations
1. Patient completes screening
2. Backend calculates score and classification
3. Safety-sensitive responses are flagged
4. Care-team visibility rules determine who may review
5. The result is logged and available for follow-up planning

## Minimum escalation levels

### Lower concern range
- normal provider review cadence
- standard documentation and follow-up visibility

### Moderate follow-up range
- provider review expected
- follow-up plan should be visible in subsequent care workflow

### Higher follow-up range
- care-team review should be more explicit
- note, referral, or scheduling action may be needed depending on operating policy

## Safety-sensitive flag expectation
When a safety-sensitive answer is flagged:
- the care team should be able to see that the submission needs attention
- the platform should not present confusing or casual language to the patient
- the workflow should support documented follow-up

## Operational warning
The platform can support safety-flag visibility and workflow discipline, but it should not rely on vague assumptions about who will notice a serious response. Review ownership must be explicit in team operations.
```

---

# FILE 3 — `[CREATE]` `bliss-telehealth/docs/clinical-operations/no-show-and-follow-up-playbook.md`

```md
# PBBF BLISS No-Show and Follow-Up Playbook

## Purpose
This document defines the minimum workflow expectations when a scheduled visit is missed or follow-up is required.

## Core principle
A missed appointment is not just a status label. It is an operational event that may affect screening review, referral continuity, and ongoing care coordination.

## Minimum no-show workflow
1. Appointment is marked as missed according to platform rules
2. The status change is auditable
3. The care team can view the missed state
4. Follow-up expectations are visible
5. Referral or rescheduling implications can be tracked

## Recommended operational actions
Depending on program policy:
- attempt contact using the preferred contact method
- document follow-up intent
- reschedule where appropriate
- review whether recent screening or referral status increases follow-up urgency

## Governance requirement
No-show handling should not be ambiguous in the system. The platform should make it clear:
- when a visit was missed
- who can see it
- what follow-up state exists afterward
```

---

# FILE 4 — `[CREATE]` `bliss-telehealth/docs/clinical-operations/referral-operating-guidelines.md`

```md
# PBBF BLISS Referral Operating Guidelines

## Purpose
This document defines the minimum expectations for referral creation, review, and follow-up tracking.

## Core principle
A referral is not complete when it is merely created. It becomes operationally useful when it has:
- context
- destination
- status visibility
- follow-up expectation
- auditable change history

## Minimum referral data expectations
- patient context
- originating visit or encounter context where applicable
- referral category
- referral destination
- referral notes
- follow-up date or expectation
- status updates over time

## Status expectations
Typical statuses should remain operationally understandable, for example:
- created
- acknowledged
- completed
- closed or equivalent workflow end state

## Governance rules
1. Referral creation should be role-restricted to the appropriate care-team workflow.
2. Referral status changes should be visible and auditable.
3. Follow-up expectations should not be lost after creation.
4. Referral notes should support later interpretation of why the referral was made.
```

---

# FILE 5 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/intake/constants.py`

> Create this file if it does not yet exist. This centralizes consent-version defaults and intake-sensitive state labels.

```python
CURRENT_CONSENT_VERSION = "2026.05"
INTAKE_STATUS_DRAFT = "draft"
INTAKE_STATUS_SUBMITTED = "submitted"

SERVICE_NEEDS = {
    "mental_health",
    "lactation",
    "wellness_follow_up",
    "community_support",
}
```

---

# FILE 6 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/intake/validators.py`

> Create this file if it does not yet exist. This keeps consent-version and final-submit governance checks explicit.

```python
from __future__ import annotations

from app.modules.intake.constants import CURRENT_CONSENT_VERSION, SERVICE_NEEDS


def validate_service_needs(values: list[str]) -> None:
    if not values:
        raise ValueError("At least one service need must be selected.")

    invalid = [value for value in values if value not in SERVICE_NEEDS]
    if invalid:
        raise ValueError(f"Invalid service need values: {', '.join(invalid)}")


def validate_consent_for_submission(
    *,
    consent_accepted: bool,
    privacy_accepted: bool,
    consent_version: str | None,
) -> None:
    if not consent_accepted:
        raise ValueError("Consent acknowledgement is required before final submission.")
    if not privacy_accepted:
        raise ValueError("Privacy acknowledgement is required before final submission.")
    if consent_version != CURRENT_CONSENT_VERSION:
        raise ValueError("Consent version is missing or outdated.")
```

---

# FILE 7 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/intake/schemas.py`

> Merge these fields into your existing intake schemas so consent governance is explicit.

```python
from __future__ import annotations

from pydantic import BaseModel, Field


class IntakeSubmissionBase(BaseModel):
    full_name: str
    date_of_birth: str
    phone_number: str
    preferred_contact_method: str
    service_needs: list[str]
    postpartum_summary: str
    emergency_contact_name: str
    emergency_contact_relationship: str
    emergency_contact_phone: str
    consent_accepted: bool = False
    privacy_accepted: bool = False
    consent_version: str | None = None


class IntakeSubmissionRead(IntakeSubmissionBase):
    status: str = "draft"


class IntakeSubmitResponse(BaseModel):
    message: str = Field(default="Intake submitted successfully.")
    consent_version: str
    status: str
```

> Merge note:
> Keep your existing schema classes if they already exist; add `consent_version` and explicit response fields if missing.

---

# FILE 8 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/intake/service.py`

> Merge this governance logic into your existing intake service. The important part is:
> - apply current consent version automatically when drafting if missing
> - require exact consent version on final submit
> - record governance-relevant transition metadata

```python
from __future__ import annotations

from app.modules.intake.constants import CURRENT_CONSENT_VERSION, INTAKE_STATUS_DRAFT, INTAKE_STATUS_SUBMITTED
from app.modules.intake.validators import validate_consent_for_submission, validate_service_needs


class IntakeService:
    def __init__(self, repository, audit_service=None):
        self.repository = repository
        self.audit_service = audit_service

    def save_draft(self, payload):
        payload.consent_version = payload.consent_version or CURRENT_CONSENT_VERSION
        validate_service_needs(payload.service_needs)

        item = self.repository.save_draft(payload, status=INTAKE_STATUS_DRAFT)

        if self.audit_service:
            self.audit_service.create_event(
                actor_name="patient",
                action="intake.draft_saved",
                target_type="intake_submission",
                target_id=str(item.get("id", "")),
                metadata={"consent_version": payload.consent_version},
            )

        return item

    def submit(self, payload):
        payload.consent_version = payload.consent_version or CURRENT_CONSENT_VERSION
        validate_service_needs(payload.service_needs)
        validate_consent_for_submission(
            consent_accepted=payload.consent_accepted,
            privacy_accepted=payload.privacy_accepted,
            consent_version=payload.consent_version,
        )

        item = self.repository.submit(payload, status=INTAKE_STATUS_SUBMITTED)

        if self.audit_service:
            self.audit_service.create_event(
                actor_name="patient",
                action="intake.submitted",
                target_type="intake_submission",
                target_id=str(item.get("id", "")),
                metadata={
                    "consent_version": payload.consent_version,
                    "status": INTAKE_STATUS_SUBMITTED,
                },
            )

        return {
            "message": "Intake submitted successfully.",
            "consent_version": payload.consent_version,
            "status": INTAKE_STATUS_SUBMITTED,
            "intake": item,
        }
```

---

# FILE 9 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/screenings/constants.py`

> Create this file if it does not yet exist.

```python
EPDS_BAND_LOWER = "lower concern range"
EPDS_BAND_MODERATE = "moderate follow-up range"
EPDS_BAND_HIGHER = "higher follow-up range"

SAFETY_SENSITIVE_QUESTION_ID = "q10"

CARE_TEAM_REVIEW_ROLES = {
    "provider",
    "counselor",
    "care_coordinator",
    "lactation_consultant",
    "admin",
}
```

---

# FILE 10 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/screenings/scoring.py`

> Merge into your existing scoring file if it already exists.

```python
from __future__ import annotations

from app.modules.screenings.constants import (
    EPDS_BAND_HIGHER,
    EPDS_BAND_LOWER,
    EPDS_BAND_MODERATE,
    SAFETY_SENSITIVE_QUESTION_ID,
)


def calculate_epds_score(answers: list[dict]) -> int:
    return sum(int(item.get("score", 0)) for item in answers)


def classify_epds_band(score: int) -> str:
    if score <= 9:
        return EPDS_BAND_LOWER
    if score <= 12:
        return EPDS_BAND_MODERATE
    return EPDS_BAND_HIGHER


def has_safety_sensitive_flag(answers: list[dict]) -> bool:
    for item in answers:
        if item.get("question_id") == SAFETY_SENSITIVE_QUESTION_ID and int(item.get("score", 0)) > 0:
            return True
    return False
```

---

# FILE 11 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/screenings/service.py`

> Merge this into your existing screening service to strengthen role review and audit behavior.

```python
from __future__ import annotations

from app.modules.screenings.constants import CARE_TEAM_REVIEW_ROLES
from app.modules.screenings.scoring import (
    calculate_epds_score,
    classify_epds_band,
    has_safety_sensitive_flag,
)


class ScreeningService:
    def __init__(self, repository, audit_service=None):
        self.repository = repository
        self.audit_service = audit_service

    def submit_epds(self, patient_id: str, answers: list[dict]):
        score = calculate_epds_score(answers)
        band = classify_epds_band(score)
        safety_flag = has_safety_sensitive_flag(answers)

        screening = self.repository.create_epds_result(
            patient_id=patient_id,
            answers=answers,
            score=score,
            band=band,
            safety_flag=safety_flag,
        )

        if self.audit_service:
            self.audit_service.create_event(
                actor_name="patient",
                action="screening.epds_submitted",
                target_type="screening",
                target_id=str(screening.get("id", "")),
                metadata={"score": score, "band": band, "safety_flag": safety_flag},
            )

        return {
            "score": score,
            "band": band,
            "safety_flag": safety_flag,
            "screening": screening,
        }

    def ensure_role_can_review(self, role: str) -> None:
        if role not in CARE_TEAM_REVIEW_ROLES:
            raise PermissionError("This role is not allowed to review screening results.")
```

---

# FILE 12 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/encounters/service.py`

> Merge these governance rules into your existing service so finalization becomes operationally understandable.

```python
from __future__ import annotations


class EncounterService:
    def __init__(self, repository, audit_service=None):
        self.repository = repository
        self.audit_service = audit_service

    def finalize(self, encounter_id: str, payload):
        if not payload.get("note"):
            raise ValueError("Encounter note is required before finalization.")
        if not payload.get("assessment"):
            raise ValueError("Assessment is required before finalization.")
        if not payload.get("follow_up_plan"):
            raise ValueError("Follow-up plan is required before finalization.")

        item = self.repository.finalize(encounter_id, payload)

        if self.audit_service:
            self.audit_service.create_event(
                actor_name="provider",
                action="encounter.finalized",
                target_type="encounter",
                target_id=str(encounter_id),
                metadata={"status": "finalized"},
            )

        return item
```

> Merge note:
> Keep your existing draft-save logic. This stage specifically raises the standard for **finalization**, not ordinary note editing.

---

# FILE 13 — `[UPDATE]` `bliss-telehealth/pbbf-api/app/modules/referrals/service.py`

> Merge this into your existing referral service so referral follow-up expectations are explicit.

```python
from __future__ import annotations


class ReferralService:
    def __init__(self, repository, audit_service=None):
        self.repository = repository
        self.audit_service = audit_service

    def create_referral(self, payload):
        if not payload.get("category"):
            raise ValueError("Referral category is required.")
        if not payload.get("destination"):
            raise ValueError("Referral destination is required.")
        if not payload.get("notes"):
            raise ValueError("Referral notes are required.")

        item = self.repository.create(payload)

        if self.audit_service:
            self.audit_service.create_event(
                actor_name="provider",
                action="referral.created",
                target_type="referral",
                target_id=str(item.get("id", "")),
                metadata={"follow_up_date": payload.get("follow_up_date")},
            )

        return item

    def update_status(self, referral_id: str, status: str):
        item = self.repository.update_status(referral_id, status)

        if self.audit_service:
            self.audit_service.create_event(
                actor_name="provider",
                action="referral.status_updated",
                target_type="referral",
                target_id=str(referral_id),
                metadata={"status": status},
            )

        return item
```

---

# FILE 14 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/intake/test_consent_versioning.py`

```python
import pytest

from app.modules.intake.constants import CURRENT_CONSENT_VERSION
from app.modules.intake.validators import validate_consent_for_submission


def test_consent_version_must_match_current_version():
    with pytest.raises(ValueError):
        validate_consent_for_submission(
            consent_accepted=True,
            privacy_accepted=True,
            consent_version="old-version",
        )


def test_consent_version_passes_when_current():
    validate_consent_for_submission(
        consent_accepted=True,
        privacy_accepted=True,
        consent_version=CURRENT_CONSENT_VERSION,
    )
```

---

# FILE 15 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/intake/test_sensitive_transition_audit.py`

```python
class FakeRepository:
    def submit(self, payload, status):
        return {"id": 1, "status": status}


class FakeAuditService:
    def __init__(self):
        self.events = []

    def create_event(self, **kwargs):
        self.events.append(kwargs)


def test_intake_submission_writes_audit_event():
    from app.modules.intake.service import IntakeService

    class Payload:
        full_name = "Patient User"
        service_needs = ["mental_health"]
        consent_accepted = True
        privacy_accepted = True
        consent_version = "2026.05"

    audit_service = FakeAuditService()
    service = IntakeService(FakeRepository(), audit_service=audit_service)
    service.submit(Payload())

    assert len(audit_service.events) == 1
    assert audit_service.events[0]["action"] == "intake.submitted"
```

---

# FILE 16 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/screenings/test_safety_flag_rules.py`

```python
from app.modules.screenings.scoring import has_safety_sensitive_flag


def test_safety_flag_detected():
    answers = [
        {"question_id": "q1", "score": 0},
        {"question_id": "q10", "score": 2},
    ]
    assert has_safety_sensitive_flag(answers) is True


def test_safety_flag_not_detected_when_q10_is_zero():
    answers = [
        {"question_id": "q10", "score": 0},
    ]
    assert has_safety_sensitive_flag(answers) is False
```

---

# FILE 17 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/screenings/test_role_review_rules.py`

```python
import pytest

from app.modules.screenings.service import ScreeningService


class FakeRepository:
    pass


def test_non_care_role_cannot_review_screenings():
    service = ScreeningService(FakeRepository())

    with pytest.raises(PermissionError):
        service.ensure_role_can_review("patient")


def test_care_team_role_can_review_screenings():
    service = ScreeningService(FakeRepository())
    service.ensure_role_can_review("provider")
```

---

# FILE 18 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/encounters/test_finalize_note_governance.py`

```python
import pytest

from app.modules.encounters.service import EncounterService


class FakeRepository:
    def finalize(self, encounter_id, payload):
        return {"id": encounter_id, "status": "finalized"}


def test_finalize_requires_follow_up_plan():
    service = EncounterService(FakeRepository())

    with pytest.raises(ValueError):
        service.finalize(
            "enc-1",
            {"note": "note", "assessment": "assessment", "follow_up_plan": ""},
        )
```

---

# FILE 19 — `[CREATE]` `bliss-telehealth/pbbf-api/tests/modules/referrals/test_follow_up_expectations.py`

```python
import pytest

from app.modules.referrals.service import ReferralService


class FakeRepository:
    def create(self, payload):
        return {"id": 1, **payload}


def test_referral_requires_destination_and_notes():
    service = ReferralService(FakeRepository())

    with pytest.raises(ValueError):
        service.create_referral(
            {
                "category": "counseling",
                "destination": "",
                "notes": "",
            }
        )
```

---

# FILE 20 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/modules/intake/utils/intakeSchema.js`

> Merge these governance helpers into your existing intake schema module so consent versioning is explicit in the UI contract.

```jsx
export const CURRENT_CONSENT_VERSION = "2026.05";

export const initialIntakeValues = {
  fullName: "",
  dateOfBirth: "",
  phoneNumber: "",
  preferredContactMethod: "email",
  serviceNeeds: [],
  postpartumSummary: "",
  emergencyContactName: "",
  emergencyContactRelationship: "",
  emergencyContactPhone: "",
  consentAccepted: false,
  privacyAccepted: false,
  consentVersion: CURRENT_CONSENT_VERSION,
};

export function validateConsent(values) {
  return {
    consentAccepted: values.consentAccepted ? "" : "You must accept care consent.",
    privacyAccepted: values.privacyAccepted ? "" : "You must accept the privacy acknowledgement.",
    consentVersion:
      values.consentVersion === CURRENT_CONSENT_VERSION
        ? ""
        : "The consent version is outdated. Please reload and review the latest consent.",
  };
}
```

> Merge note:
> Keep your existing schema file and add `CURRENT_CONSENT_VERSION`, `consentVersion`, and the version validation branch if they do not exist yet.

---

# FILE 21 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/modules/intake/components/ConsentCheckboxes.jsx`

> Replace or merge into the current file so the patient can see that consent is tied to a versioned acknowledgement.

```jsx
export default function ConsentCheckboxes({
  consentAccepted,
  privacyAccepted,
  consentVersion,
  errors = {},
  onChange,
}) {
  return (
    <div className="space-y-5">
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
          Consent version {consentVersion}
        </p>

        <label className="flex items-start gap-3">
          <input
            type="checkbox"
            checked={consentAccepted}
            onChange={(event) => onChange("consentAccepted", event.target.checked)}
            className="mt-1 h-4 w-4 rounded border-slate-300 text-sky-700 focus:ring-sky-500"
          />
          <span className="text-sm leading-6 text-slate-700">
            I acknowledge consent to participate in the telehealth onboarding and care workflow.
          </span>
        </label>
        {errors.consentAccepted ? (
          <p className="mt-2 text-sm text-rose-600">{errors.consentAccepted}</p>
        ) : null}
        {errors.consentVersion ? (
          <p className="mt-2 text-sm text-rose-600">{errors.consentVersion}</p>
        ) : null}
      </div>

      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
        <label className="flex items-start gap-3">
          <input
            type="checkbox"
            checked={privacyAccepted}
            onChange={(event) => onChange("privacyAccepted", event.target.checked)}
            className="mt-1 h-4 w-4 rounded border-slate-300 text-sky-700 focus:ring-sky-500"
          />
          <span className="text-sm leading-6 text-slate-700">
            I acknowledge the privacy notice and understand that my information will be used to support care coordination, screening, scheduling, and follow-up.
          </span>
        </label>
        {errors.privacyAccepted ? (
          <p className="mt-2 text-sm text-rose-600">{errors.privacyAccepted}</p>
        ) : null}
      </div>
    </div>
  );
}
```

---

# FILE 22 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/pages/patient/Screening.jsx`

> Merge these wording and completion-summary improvements into your existing patient screening page.

```jsx
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";
import PageHeader from "../../shared/components/PageHeader";
import SectionCard from "../../shared/components/SectionCard";
import EpdsQuestionnaire from "../../modules/screenings/components/EpdsQuestionnaire";
import ScoreSummaryCard, {
  ScreeningHistoryList,
} from "../../modules/screenings/components/ScoreSummaryCard";
import { useEpdsForm } from "../../modules/screenings/hooks/useEpdsForm";

export default function PatientScreeningPage() {
  const {
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
  } = useEpdsForm();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading screening..." />
      </div>
    );
  }

  if (loadError) {
    return (
      <ErrorState
        title="Unable to load screening"
        message={loadError}
        retryLabel="Retry"
        onRetry={() => window.location.reload()}
      />
    );
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Patient screening"
        title="Self-assessment"
        description="Complete your screening in one guided flow. Your responses help the care team review follow-up needs and continue support planning."
      />

      {submittedSummary ? (
        <ScoreSummaryCard
          score={submittedSummary.score}
          band={submittedSummary.band}
          safetyFlag={submittedSummary.safetyFlag}
          completionMessage={completionMessage}
        />
      ) : null}

      <EpdsQuestionnaire
        answers={answers}
        onAnswer={setAnswer}
        onSubmit={submit}
        isSubmitting={isSubmitting}
        submitError={submitError}
      />

      <SectionCard
        title="Prior screenings"
        description="Previous submissions are shown here when available from the backend."
      >
        <ScreeningHistoryList screenings={priorScreenings} />
      </SectionCard>
    </div>
  );
}
```

---

# FILE 23 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/modules/screenings/components/ScoreSummaryCard.jsx`

> Merge this wording refinement so the patient completion state is clearer without over-claiming clinical meaning.

```jsx
export default function ScoreSummaryCard({
  score = 0,
  band = "lower concern range",
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
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Score
          </p>
          <p className="mt-2 text-2xl font-semibold text-slate-900">{score}</p>
        </div>

        <div className="rounded-2xl bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Follow-up band
          </p>
          <p className="mt-2 text-base font-semibold capitalize text-slate-900">{band}</p>
        </div>

        <div className="rounded-2xl bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Review visibility
          </p>
          <p className="mt-2 text-sm font-medium text-slate-900">
            {safetyFlag
              ? "The care team may prioritize review of this submission."
              : "This submission will follow the standard review workflow."}
          </p>
        </div>
      </div>
    </div>
  );
}
```

---

# FILE 24 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/pages/patient/Session.jsx`

> Merge this wording improvement into your existing telehealth session page so readiness and waiting states feel more operationally understandable.

```jsx
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";
import PageHeader from "../../shared/components/PageHeader";
import DeviceCheckPanel from "../../modules/telehealth/components/DeviceCheckPanel";
import JoinSessionCard from "../../modules/telehealth/components/JoinSessionCard";
import { useSessionAccess } from "../../modules/telehealth/hooks/useSessionAccess";

export default function PatientSessionPage() {
  const {
    session,
    readiness,
    isLoading,
    isJoining,
    loadError,
    joinError,
    joinMessage,
    joinSession,
  } = useSessionAccess();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading session access..." />
      </div>
    );
  }

  if (loadError) {
    return (
      <ErrorState
        title="Unable to load session access"
        message={loadError}
        retryLabel="Retry"
        onRetry={() => window.location.reload()}
      />
    );
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Telehealth session"
        title="Join your visit"
        description="Review your visit status, confirm basic device readiness, and join when your session is available."
      />

      <JoinSessionCard
        session={session}
        readiness={readiness}
        isJoining={isJoining}
        joinError={joinError}
        joinMessage={joinMessage}
        onJoin={joinSession}
      />

      <DeviceCheckPanel />
    </div>
  );
}
```

---

# FILE 25 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/pages/provider/Notes.jsx`

> Merge this finalization clarity improvement into your existing provider notes page.

```jsx
import { useMemo, useState } from "react";
import PageHeader from "../../shared/components/PageHeader";
import ErrorState from "../../shared/components/ErrorState";
import Loader from "../../shared/components/Loader";
import EmptyState from "../../shared/components/EmptyState";
import PatientSummaryCard from "../../modules/encounters/components/PatientSummaryCard";
import EncounterEditor from "../../modules/encounters/components/EncounterEditor";
import { useEncounterEditor } from "../../modules/encounters/hooks/useEncounterEditor";
import { useAppointments } from "../../modules/appointments/hooks/useAppointments";

function normalizeProviderAppointment(raw) {
  return {
    id: raw?.id || raw?.appointment_id || "temp-appointment-id",
    patientId: raw?.patient_id || raw?.patientId || null,
    patientName: raw?.patient_name || raw?.patientName || "Unknown patient",
    serviceType: raw?.service_type || raw?.serviceType || "Visit",
    visitReason: raw?.visit_reason || raw?.visitReason || "",
    status: raw?.status || "booked",
    screeningAlertLevel: raw?.screening_alert_level || raw?.screeningAlertLevel || "none",
    screeningAlertText: raw?.screening_alert_text || raw?.screeningAlertText || "",
    encounterId: raw?.encounter_id || raw?.encounterId || null,
  };
}

export default function ProviderNotesPage() {
  const { appointments, isLoading, loadError } = useAppointments();
  const normalizedAppointments = useMemo(
    () => appointments.map(normalizeProviderAppointment),
    [appointments]
  );

  const [selectedAppointmentId, setSelectedAppointmentId] = useState(
    normalizedAppointments[0]?.id || ""
  );

  const selectedAppointment =
    normalizedAppointments.find((item) => item.id === selectedAppointmentId) ||
    normalizedAppointments[0] ||
    null;

  const {
    values,
    errors,
    status,
    isLoading: encounterLoading,
    isSaving,
    message,
    loadError: encounterLoadError,
    updateField,
    saveDraft,
    finalize,
  } = useEncounterEditor(selectedAppointment?.id);

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading provider notes..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load provider notes" message={loadError} />;
  }

  if (!normalizedAppointments.length) {
    return (
      <EmptyState
        title="No appointments available"
        message="No provider appointments are available yet for note drafting."
      />
    );
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Provider notes"
        title="Encounter workspace"
        description="Select an appointment, review patient context, and complete structured documentation. Finalized notes should represent the completed provider record for that visit."
      />

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <label className="mb-2 block text-sm font-medium text-slate-700">
          Select appointment
        </label>
        <select
          value={selectedAppointment?.id || ""}
          onChange={(event) => setSelectedAppointmentId(event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
        >
          {normalizedAppointments.map((appointment) => (
            <option key={appointment.id} value={appointment.id}>
              {appointment.patientName} — {appointment.serviceType}
            </option>
          ))}
        </select>
      </section>

      <PatientSummaryCard appointment={selectedAppointment} />

      {encounterLoadError ? (
        <ErrorState title="Unable to load encounter" message={encounterLoadError} />
      ) : encounterLoading ? (
        <div className="flex min-h-[20vh] items-center justify-center">
          <Loader label="Loading encounter..." />
        </div>
      ) : (
        <EncounterEditor
          values={values}
          errors={errors}
          status={status}
          isSaving={isSaving}
          message={message}
          onChange={updateField}
          onSaveDraft={saveDraft}
          onFinalize={finalize}
        />
      )}
    </div>
  );
}
```

---

# FILE 26 — `[UPDATE]` `bliss-telehealth/pbbf-telehealth/src/pages/provider/Referrals.jsx`

> Merge this wording clarification so referral follow-up context feels more operational and less ambiguous.

```jsx
import { useMemo, useState } from "react";
import PageHeader from "../../shared/components/PageHeader";
import Loader from "../../shared/components/Loader";
import EmptyState from "../../shared/components/EmptyState";
import ErrorState from "../../shared/components/ErrorState";
import ReferralForm from "../../modules/referrals/components/ReferralForm";
import ReferralTimeline from "../../modules/referrals/components/ReferralTimeline";
import { useReferrals } from "../../modules/referrals/hooks/useReferrals";
import { useAppointments } from "../../modules/appointments/hooks/useAppointments";

function normalizeProviderAppointment(raw) {
  return {
    id: raw?.id || raw?.appointment_id || "temp-appointment-id",
    patientId: raw?.patient_id || raw?.patientId || null,
    patientName: raw?.patient_name || raw?.patientName || "Unknown patient",
    serviceType: raw?.service_type || raw?.serviceType || "Visit",
    encounterId: raw?.encounter_id || raw?.encounterId || null,
  };
}

export default function ProviderReferralsPage() {
  const { appointments, isLoading: appointmentsLoading, loadError: appointmentsError } = useAppointments();
  const {
    referrals,
    isLoading: referralsLoading,
    isSaving,
    loadError: referralsError,
    message,
    createReferral,
    updateStatus,
  } = useReferrals();

  const normalizedAppointments = useMemo(
    () => appointments.map(normalizeProviderAppointment),
    [appointments]
  );

  const [selectedAppointmentId, setSelectedAppointmentId] = useState(
    normalizedAppointments[0]?.id || ""
  );

  const selectedAppointment =
    normalizedAppointments.find((item) => item.id === selectedAppointmentId) ||
    normalizedAppointments[0] ||
    null;

  if (appointmentsLoading || referralsLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading provider referrals..." />
      </div>
    );
  }

  if (appointmentsError) {
    return <ErrorState title="Unable to load provider appointments" message={appointmentsError} />;
  }

  if (referralsError) {
    return <ErrorState title="Unable to load referrals" message={referralsError} />;
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Provider referrals"
        title="Referral management"
        description="Create referrals for follow-up support and track progress over time. Each referral should remain understandable after the visit, not only at the moment it is created."
      />

      {!normalizedAppointments.length ? (
        <EmptyState
          title="No patient appointments available"
          message="Appointments are required to create referrals from the provider workspace."
        />
      ) : (
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Select appointment / patient context
          </label>
          <select
            value={selectedAppointment?.id || ""}
            onChange={(event) => setSelectedAppointmentId(event.target.value)}
            className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          >
            {normalizedAppointments.map((appointment) => (
              <option key={appointment.id} value={appointment.id}>
                {appointment.patientName} — {appointment.serviceType}
              </option>
            ))}
          </select>
        </section>
      )}

      <ReferralForm
        selectedAppointment={selectedAppointment}
        onSubmit={createReferral}
        isSaving={isSaving}
        message={message}
      />

      <ReferralTimeline
        referrals={referrals}
        onUpdateStatus={updateStatus}
        isSaving={isSaving}
      />
    </div>
  );
}
```

---

# Recommended verification commands for Stage 5

## Backend governance-focused tests
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

pytest tests/modules/intake tests/modules/screenings tests/modules/encounters tests/modules/referrals -q
```

## Frontend clarity and workflow regression checks
```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-telehealth

npx vitest run src/modules/screenings/__tests__/ScreeningPage.test.jsx src/modules/telehealth/__tests__/SessionPage.test.jsx src/modules/referrals/__tests__/ReferralForm.test.jsx src/modules/encounters/__tests__/EncounterEditor.test.jsx
```

---

# Git commit recommendation for this stage

Run from the `bliss-telehealth` root:

```bash
git add docs/clinical-operations pbbf-api/app/modules/intake pbbf-api/app/modules/screenings pbbf-api/app/modules/encounters pbbf-api/app/modules/referrals pbbf-api/tests/modules/intake pbbf-api/tests/modules/screenings pbbf-api/tests/modules/encounters pbbf-api/tests/modules/referrals pbbf-telehealth/src/modules/intake pbbf-telehealth/src/modules/screenings pbbf-telehealth/src/modules/telehealth pbbf-telehealth/src/modules/encounters pbbf-telehealth/src/modules/referrals pbbf-telehealth/src/pages/patient pbbf-telehealth/src/pages/provider
git commit -m "ops: add clinical safety governance and care workflow playbooks"
```

---

# Completion gate for Stage 5

This stage is complete only when:
- clinical-operations docs exist
- consent version governance is explicit
- screening safety-flag behavior is test-backed
- care-team review rules are explicit
- encounter finalization is governed
- referral follow-up expectations are operationally clear
- patient-facing screening/session messaging is clearer
- provider-facing note/referral workflow language is more operationally understandable
- sensitive care workflows are governance-aware, not only technically functional

---

# Final recommendation
Treat Stage 5 as the stage that explains how the product should behave when care workflows matter, not just when API requests succeed.

That is the point where the platform becomes safer to operate in a real human-service context.
