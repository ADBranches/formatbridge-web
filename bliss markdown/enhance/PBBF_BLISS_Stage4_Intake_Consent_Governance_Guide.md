# PBBF BLISS — Stage 4 Intake and Consent Governance Implementation Pack

**Stage:** 4 — Intake and Consent Governance  
**Version:** Stage 4.b — Final Implementation Pack After Inspection  
**Repository root:** `/home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth`  
**Backend:** `pbbf-api/`  
**Frontend:** `pbbf-telehealth/`  
**Development OS:** Debian/Linux  
**Execution style:** Independent commands/snippets only. Run one command at a time.

---

## Objective

Make intake and consent reliable, auditable, and aligned between frontend and backend.

Stage 4 completes consent governance by converting consent from a transient UI checkbox plus intake payload field into a durable append-only backend consent event. Consent versions and privacy policy versions remain present in the intake submission payload, but the authoritative proof of consent becomes the `consent_events` table.

---

## Inspection-Based Decisions

These decisions are based on the inspected repository state:

```text
1. Canonical backend intake field remains service_need, not service_needs.
2. Frontend may keep serviceNeeds as a UI multi-select array, but it submits the first selected value as service_need.
3. Postpartum summary is already mapped to notes and postpartum_questionnaire.summary.
4. Existing consent_version and privacy_policy_version fields are retained.
5. Existing CURRENT_CONSENT_VERSION is 2026.04.
6. Existing intake routes remain unchanged except for adding consent event history retrieval.
7. Consent event persistence happens during final intake submission, not draft save.
8. Consent event history is append-only.
9. Frontend consent handoff between ConsentPage and IntakeFormPage uses sessionStorage only as temporary onboarding state, not as final persistence.
10. Backend consent event remains the source of truth.
```

---

## Files Updated

```text
pbbf-api/app/db/models/__init__.py
pbbf-api/app/modules/intake/router.py
pbbf-api/app/modules/intake/schemas.py
pbbf-api/app/modules/intake/service.py
pbbf-api/app/modules/intake/repository.py
pbbf-api/app/modules/intake/validators.py
pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
pbbf-telehealth/src/modules/intake/utils/intakeSchema.js
pbbf-telehealth/src/modules/intake/pages/ConsentPage.jsx
pbbf-telehealth/src/modules/intake/pages/IntakeFormPage.jsx
```

## Files Created

```text
pbbf-api/app/db/models/consent_event.py
pbbf-api/alembic/versions/f20260612_stage4_add_consent_events.py
pbbf-api/tests/modules/intake/test_consent_event_history.py
pbbf-telehealth/src/modules/intake/__tests__/ConsentPersistence.test.jsx
```

---

# 0. Preflight

Run from repository root:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
pwd
```

Expected:

```text
/home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
```

---

# 1. Backup

You already created a Stage 4 backup directory during inspection:

```text
backups/stage4_intake_consent_governance_20260612_123734
```

If you want a fresh backup before applying this implementation, run:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
export STAGE4_BACKUP_DIR="backups/stage4_intake_consent_governance_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$STAGE4_BACKUP_DIR"
echo "$STAGE4_BACKUP_DIR"

mkdir -p "$STAGE4_BACKUP_DIR/pbbf-api/app/modules/intake"
mkdir -p "$STAGE4_BACKUP_DIR/pbbf-api/app/db/models"
mkdir -p "$STAGE4_BACKUP_DIR/pbbf-telehealth/src/modules/intake/hooks"
mkdir -p "$STAGE4_BACKUP_DIR/pbbf-telehealth/src/modules/intake/utils"
mkdir -p "$STAGE4_BACKUP_DIR/pbbf-telehealth/src/modules/intake/pages"
mkdir -p "$STAGE4_BACKUP_DIR/pbbf-telehealth/src/modules/intake/components"

cp pbbf-api/app/modules/intake/router.py "$STAGE4_BACKUP_DIR/pbbf-api/app/modules/intake/router.py"
cp pbbf-api/app/modules/intake/schemas.py "$STAGE4_BACKUP_DIR/pbbf-api/app/modules/intake/schemas.py"
cp pbbf-api/app/modules/intake/service.py "$STAGE4_BACKUP_DIR/pbbf-api/app/modules/intake/service.py"
cp pbbf-api/app/modules/intake/repository.py "$STAGE4_BACKUP_DIR/pbbf-api/app/modules/intake/repository.py"
cp pbbf-api/app/modules/intake/validators.py "$STAGE4_BACKUP_DIR/pbbf-api/app/modules/intake/validators.py"
cp pbbf-api/app/db/models/__init__.py "$STAGE4_BACKUP_DIR/pbbf-api/app/db/models/__init__.py"
cp pbbf-api/app/db/models/intake_submission.py "$STAGE4_BACKUP_DIR/pbbf-api/app/db/models/intake_submission.py"

cp pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js "$STAGE4_BACKUP_DIR/pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js"
cp pbbf-telehealth/src/modules/intake/utils/intakeSchema.js "$STAGE4_BACKUP_DIR/pbbf-telehealth/src/modules/intake/utils/intakeSchema.js"
cp pbbf-telehealth/src/modules/intake/pages/ConsentPage.jsx "$STAGE4_BACKUP_DIR/pbbf-telehealth/src/modules/intake/pages/ConsentPage.jsx"
cp pbbf-telehealth/src/modules/intake/pages/IntakeFormPage.jsx "$STAGE4_BACKUP_DIR/pbbf-telehealth/src/modules/intake/pages/IntakeFormPage.jsx"
cp pbbf-telehealth/src/modules/intake/components/IntakeForm.jsx "$STAGE4_BACKUP_DIR/pbbf-telehealth/src/modules/intake/components/IntakeForm.jsx"
```

---

# 2. Backend Consent Event Model

## Command 2.1 — Create `consent_event.py`

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/app/db/models/consent_event.py <<'PY'
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.intake_submission import IntakeSubmission
    from app.db.models.patient import Patient
    from app.db.models.user import User


class ConsentEvent(Base, TimestampMixin):
    __tablename__ = "consent_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    intake_submission_id: Mapped[int | None] = mapped_column(
        ForeignKey("intake_submissions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    consent_policy_version: Mapped[str] = mapped_column(String(50), nullable=False)
    privacy_policy_version: Mapped[str] = mapped_column(String(50), nullable=False)
    terms_policy_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    source: Mapped[str] = mapped_column(String(80), nullable=False, default="intake_submit", server_default="intake_submit")
    request_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    metadata_json: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)

    patient: Mapped["Patient"] = relationship("Patient")
    user: Mapped["User | None"] = relationship("User")
    intake_submission: Mapped["IntakeSubmission | None"] = relationship("IntakeSubmission")

    def __repr__(self) -> str:
        return f"ConsentEvent(id={self.id}, patient_id={self.patient_id}, event_type={self.event_type!r})"
PY
```

## Command 2.2 — Register model

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/db/models/__init__.py")
text = path.read_text()

if '    "consent_event",' not in text:
    text = text.replace('    "auth_session",\n', '    "auth_session",\n    "consent_event",\n')

if "from app.db.models.consent_event import ConsentEvent" not in text:
    text = text.replace(
        "from app.db.models.auth_session import AuthSession\n",
        "from app.db.models.auth_session import AuthSession\nfrom app.db.models.consent_event import ConsentEvent\n",
    )

if '    "ConsentEvent": ConsentEvent,' not in text:
    text = text.replace(
        '    "AuthSession": AuthSession,\n',
        '    "AuthSession": AuthSession,\n    "ConsentEvent": ConsentEvent,\n',
    )

if '    "ConsentEvent",' not in text:
    text = text.replace(
        '    "AuthSession",\n',
        '    "AuthSession",\n    "ConsentEvent",\n',
    )

path.write_text(text)
PY
```

## Command 2.3 — Create migration

Current Alembic head after Stage 3 is:

```text
f20260612_stage3
```

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/alembic/versions/f20260612_stage4_add_consent_events.py <<'PY'
from alembic import op
import sqlalchemy as sa

revision = "f20260612_stage4"
down_revision = "f20260612_stage3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "consent_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("intake_submission_id", sa.Integer(), sa.ForeignKey("intake_submissions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("consent_policy_version", sa.String(length=50), nullable=False),
        sa.Column("privacy_policy_version", sa.String(length=50), nullable=False),
        sa.Column("terms_policy_version", sa.String(length=50), nullable=True),
        sa.Column("accepted", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=False, server_default="intake_submit"),
        sa.Column("request_id", sa.String(length=120), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_consent_events_id", "consent_events", ["id"])
    op.create_index("ix_consent_events_patient_id", "consent_events", ["patient_id"])
    op.create_index("ix_consent_events_user_id", "consent_events", ["user_id"])
    op.create_index("ix_consent_events_intake_submission_id", "consent_events", ["intake_submission_id"])
    op.create_index("ix_consent_events_event_type", "consent_events", ["event_type"])
    op.create_index("ix_consent_events_accepted_at", "consent_events", ["accepted_at"])
    op.create_index("ix_consent_events_request_id", "consent_events", ["request_id"])


def downgrade() -> None:
    op.drop_index("ix_consent_events_request_id", table_name="consent_events")
    op.drop_index("ix_consent_events_accepted_at", table_name="consent_events")
    op.drop_index("ix_consent_events_event_type", table_name="consent_events")
    op.drop_index("ix_consent_events_intake_submission_id", table_name="consent_events")
    op.drop_index("ix_consent_events_user_id", table_name="consent_events")
    op.drop_index("ix_consent_events_patient_id", table_name="consent_events")
    op.drop_index("ix_consent_events_id", table_name="consent_events")
    op.drop_table("consent_events")
PY
```

---

# 3. Backend Intake Constants, Schemas, Repository, Service, Router

## Command 3.1 — Add constants

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat >> pbbf-api/app/modules/intake/constants.py <<'PY'

CURRENT_PRIVACY_POLICY_VERSION = "2026.04"
CONSENT_EVENT_INTAKE_ACCEPTED = "intake_consent_accepted"
CONSENT_EVENT_PRIVACY_ACKNOWLEDGED = "privacy_policy_acknowledged"
CONSENT_SOURCE_INTAKE_SUBMIT = "intake_submit"
PY
```

## Command 3.2 — Add consent event response schemas

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat >> pbbf-api/app/modules/intake/schemas.py <<'PY'


class ConsentEventResponse(BaseModel):
    id: int
    patient_id: int
    user_id: int | None = None
    intake_submission_id: int | None = None
    event_type: str
    consent_policy_version: str
    privacy_policy_version: str
    terms_policy_version: str | None = None
    accepted: bool
    accepted_at: datetime | None = None
    source: str
    request_id: str | None = None
    metadata_json: dict[str, Any] | list[Any] | None = None

    model_config = ConfigDict(from_attributes=True)


class ConsentEventListResponse(BaseModel):
    events: list[ConsentEventResponse]
    total: int
PY
```

## Command 3.3 — Patch repository

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/modules/intake/repository.py")
text = path.read_text()

if "from datetime import date, datetime, timezone" not in text:
    text = text.replace("from datetime import date\n", "from datetime import date, datetime, timezone\n")

if "from app.db.models.consent_event import ConsentEvent" not in text:
    text = text.replace(
        "from app.db.models.intake_submission import IntakeSubmission\n",
        "from app.db.models.consent_event import ConsentEvent\nfrom app.db.models.intake_submission import IntakeSubmission\n",
    )

if "def create_consent_event(" not in text:
    insert = '''\n    def create_consent_event(\n        self,\n        *,\n        patient_id: int,\n        user_id: int | None,\n        intake_submission_id: int | None,\n        event_type: str,\n        consent_policy_version: str,\n        privacy_policy_version: str,\n        terms_policy_version: str | None = None,\n        accepted: bool = True,\n        source: str = "intake_submit",\n        request_id: str | None = None,\n        metadata_json: dict[str, Any] | None = None,\n    ) -> ConsentEvent:\n        event = ConsentEvent(\n            patient_id=patient_id,\n            user_id=user_id,\n            intake_submission_id=intake_submission_id,\n            event_type=event_type,\n            consent_policy_version=consent_policy_version,\n            privacy_policy_version=privacy_policy_version,\n            terms_policy_version=terms_policy_version,\n            accepted=accepted,\n            accepted_at=datetime.now(timezone.utc),\n            source=source,\n            request_id=request_id,\n            metadata_json=metadata_json or {},\n        )\n        self.db.add(event)\n        self.db.flush()\n        self.db.refresh(event)\n        return event\n\n    def list_consent_events_for_patient(self, patient_id: int) -> list[ConsentEvent]:\n        stmt = (\n            select(ConsentEvent)\n            .where(ConsentEvent.patient_id == patient_id)\n            .order_by(ConsentEvent.accepted_at.desc(), ConsentEvent.id.desc())\n        )\n        return list(self.db.execute(stmt).scalars().all())\n\n    def get_latest_consent_event_for_patient(self, patient_id: int) -> ConsentEvent | None:\n        stmt = (\n            select(ConsentEvent)\n            .where(ConsentEvent.patient_id == patient_id)\n            .order_by(ConsentEvent.accepted_at.desc(), ConsentEvent.id.desc())\n        )\n        return self.db.execute(stmt).scalar_one_or_none()\n'''
    text = text.replace("    def commit(self) -> None:\n", insert + "\n    def commit(self) -> None:\n")

path.write_text(text)
PY
```

## Command 3.4 — Patch service

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/modules/intake/service.py")
text = path.read_text()

if "CONSENT_EVENT_INTAKE_ACCEPTED" not in text:
    text = text.replace(
        "    INTAKE_STATUS_SUBMITTED,\n",
        "    CONSENT_EVENT_INTAKE_ACCEPTED,\n    CONSENT_SOURCE_INTAKE_SUBMIT,\n    INTAKE_STATUS_SUBMITTED,\n",
    )

# Preserve legacy consent.version and add explicit consent_policy_version.
old_consent = '''            "consent": {\n                "acknowledged": payload.consent_acknowledged,\n                "version": payload.consent_version,\n                "privacy_policy_version": payload.privacy_policy_version,\n            },\n'''
new_consent = '''            "consent": {\n                "acknowledged": payload.consent_acknowledged,\n                "version": payload.consent_version,\n                "consent_policy_version": payload.consent_version,\n                "privacy_policy_version": payload.privacy_policy_version,\n            },\n'''
text = text.replace(old_consent, new_consent)

if "def _serialize_consent_event" not in text:
    marker = "    def _ensure_patient_role(self, current_user) -> None:\n"
    helper = '''    @staticmethod\n    def _serialize_consent_event(event) -> dict[str, Any]:\n        return {\n            "id": event.id,\n            "patient_id": event.patient_id,\n            "user_id": event.user_id,\n            "intake_submission_id": event.intake_submission_id,\n            "event_type": event.event_type,\n            "consent_policy_version": event.consent_policy_version,\n            "privacy_policy_version": event.privacy_policy_version,\n            "terms_policy_version": event.terms_policy_version,\n            "accepted": event.accepted,\n            "accepted_at": event.accepted_at,\n            "source": event.source,\n            "request_id": event.request_id,\n            "metadata_json": event.metadata_json or {},\n        }\n\n'''
    text = text.replace(marker, helper + marker)

old_update = '''        intake = self.repository.update_intake(\n            intake,\n            status=INTAKE_STATUS_SUBMITTED,\n            service_need=service_need,\n            preferred_contact_method=contact_method,\n            screening_ready=screening_ready,\n            attachments_json=payload.attachments,\n            submission_payload=self._serialize_submission_payload(payload),\n            notes=payload.notes,\n            submitted_by_user_id=current_user.id,\n        )\n        self.repository.commit()\n        return self._serialize_intake(intake)\n'''
new_update = '''        intake = self.repository.update_intake(\n            intake,\n            status=INTAKE_STATUS_SUBMITTED,\n            service_need=service_need,\n            preferred_contact_method=contact_method,\n            screening_ready=screening_ready,\n            attachments_json=payload.attachments,\n            submission_payload=self._serialize_submission_payload(payload),\n            notes=payload.notes,\n            submitted_by_user_id=current_user.id,\n        )\n        consent_event = self.repository.create_consent_event(\n            patient_id=patient.id,\n            user_id=current_user.id,\n            intake_submission_id=intake.id,\n            event_type=CONSENT_EVENT_INTAKE_ACCEPTED,\n            consent_policy_version=payload.consent_version,\n            privacy_policy_version=payload.privacy_policy_version,\n            accepted=True,\n            source=CONSENT_SOURCE_INTAKE_SUBMIT,\n            metadata_json={\n                "service_need": service_need,\n                "preferred_contact_method": contact_method,\n                "intake_status": INTAKE_STATUS_SUBMITTED,\n            },\n        )\n        self.repository.commit()\n        data = self._serialize_intake(intake)\n        data["consent_event"] = self._serialize_consent_event(consent_event)\n        return data\n'''
text = text.replace(old_update, new_update)

if "def list_consent_events_for_current_patient" not in text:
    method = '''\n    def list_consent_events_for_current_patient(self, *, current_user) -> dict[str, Any]:\n        self._ensure_patient_role(current_user)\n        patient = self._ensure_patient_profile(current_user)\n        events = self.repository.list_consent_events_for_patient(patient.id)\n        return {\n            "events": [self._serialize_consent_event(event) for event in events],\n            "total": len(events),\n        }\n'''
    text = text + method

path.write_text(text)
PY
```

## Command 3.5 — Patch router

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-api/app/modules/intake/router.py")
text = path.read_text()

route = '''\n@router.get("/me/consent-events")\ndef get_my_consent_events(\n    db: Session = Depends(get_db),\n    current_user=Depends(get_current_active_user),\n):\n    service = IntakeService(db)\n    data = service.list_consent_events_for_current_patient(current_user=current_user)\n    return success_response(\n        message="Consent event history retrieved successfully.",\n        data=data,\n    )\n\n'''

if '"/me/consent-events"' not in text:
    text = text.replace("\n\n@router.get(\"/patients/{patient_id}\"", route + "\n@router.get(\"/patients/{patient_id}\"")

path.write_text(text)
PY
```

---

# 4. Frontend Consent Persistence

## Command 4.1 — Patch intake schema with storage key and privacy version

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-telehealth/src/modules/intake/utils/intakeSchema.js")
text = path.read_text()

if 'CURRENT_PRIVACY_POLICY_VERSION' not in text:
    text = text.replace(
        'export const CURRENT_CONSENT_VERSION = "2026.04";\n',
        'export const CURRENT_CONSENT_VERSION = "2026.04";\nexport const CURRENT_PRIVACY_POLICY_VERSION = "2026.04";\nexport const INTAKE_CONSENT_STORAGE_KEY = "pbbf_intake_consent_state";\n',
    )

if 'privacyPolicyVersion:' not in text:
    text = text.replace(
        '  consentVersion: CURRENT_CONSENT_VERSION,\n',
        '  consentVersion: CURRENT_CONSENT_VERSION,\n  privacyPolicyVersion: CURRENT_PRIVACY_POLICY_VERSION,\n',
    )

path.write_text(text)
PY
```

## Command 4.2 — Patch `useIntakeForm.js` for temporary consent handoff

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js")
text = path.read_text()

if "INTAKE_CONSENT_STORAGE_KEY" not in text:
    text = text.replace(
        "  hasIntakeErrors,\n  initialIntakeValues,",
        "  hasIntakeErrors,\n  INTAKE_CONSENT_STORAGE_KEY,\n  initialIntakeValues,",
    )

if "function readStoredConsentState" not in text:
    helper = '''\nfunction readStoredConsentState() {\n  try {\n    const raw = window.sessionStorage.getItem(INTAKE_CONSENT_STORAGE_KEY);\n    return raw ? JSON.parse(raw) : {};\n  } catch {\n    return {};\n  }\n}\n\nfunction persistConsentState(values) {\n  try {\n    const payload = {\n      consentAccepted: Boolean(values.consentAccepted),\n      privacyAccepted: Boolean(values.privacyAccepted),\n      consentVersion: values.consentVersion,\n      privacyPolicyVersion: values.privacyPolicyVersion || values.consentVersion,\n    };\n    window.sessionStorage.setItem(INTAKE_CONSENT_STORAGE_KEY, JSON.stringify(payload));\n  } catch {\n    // Ignore temporary storage failures. Backend remains source of truth.\n  }\n}\n\nfunction clearStoredConsentState() {\n  try {\n    window.sessionStorage.removeItem(INTAKE_CONSENT_STORAGE_KEY);\n  } catch {\n    // Ignore temporary storage failures.\n  }\n}\n'''
    text = text.replace("function extractIntakePayload(response) {", helper + "\nfunction extractIntakePayload(response) {")

text = text.replace(
    "  const [values, setValues] = useState(initialIntakeValues);",
    "  const [values, setValues] = useState(() => ({ ...initialIntakeValues, ...readStoredConsentState() }));",
)

old_update_field = '''  function updateField(field, value) {\n    setValues((current) => ({ ...current, [field]: value }));\n    setErrors((current) => ({ ...current, [field]: "" }));\n    setSubmitMessage("");\n    setDraftMessage("");\n  }\n'''
new_update_field = '''  function updateField(field, value) {\n    setValues((current) => {\n      const next = { ...current, [field]: value };\n      if (["consentAccepted", "privacyAccepted", "consentVersion", "privacyPolicyVersion"].includes(field)) {\n        persistConsentState(next);\n      }\n      return next;\n    });\n    setErrors((current) => ({ ...current, [field]: "" }));\n    setSubmitMessage("");\n    setDraftMessage("");\n  }\n'''
text = text.replace(old_update_field, new_update_field)

# Ensure loaded intake does not wipe session consent unless backend has values.
text = text.replace(
    "privacyAccepted: Boolean(\n        intake.submission_payload?.consent?.privacy_policy_version ?? intake.privacy_policy_version ?? intake.privacyAccepted ?? current.privacyAccepted\n      ),",
    "privacyAccepted: Boolean(\n        intake.submission_payload?.consent?.privacy_policy_version ?? intake.privacy_policy_version ?? intake.privacyAccepted ?? current.privacyAccepted\n      ),\n      consentVersion:\n        intake.submission_payload?.consent?.consent_policy_version ||\n        intake.submission_payload?.consent?.version ||\n        intake.consent_version ||\n        current.consentVersion,\n      privacyPolicyVersion:\n        intake.submission_payload?.consent?.privacy_policy_version ||\n        intake.privacy_policy_version ||\n        current.privacyPolicyVersion,",
)

# Submit payload already includes versions. Add clear after successful submit.
text = text.replace(
    '      setSubmitMessage(response?.message || "Intake submitted successfully.");\n      return { success: true, response };',
    '      clearStoredConsentState();\n      setSubmitMessage(response?.message || "Intake submitted successfully.");\n      return { success: true, response };',
)

path.write_text(text)
PY
```

## Command 4.3 — Patch ConsentPage to persist on continue

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path

path = Path("pbbf-telehealth/src/modules/intake/pages/ConsentPage.jsx")
text = path.read_text()

if "INTAKE_CONSENT_STORAGE_KEY" not in text:
    text = text.replace(
        'import ErrorState from "../../../shared/components/ErrorState";\n',
        'import ErrorState from "../../../shared/components/ErrorState";\nimport { INTAKE_CONSENT_STORAGE_KEY } from "../utils/intakeSchema";\n',
    )

old = '''  function handleContinue() {\n    const valid = validateConsentStep();\n    if (!valid) return;\n    navigate("/patient/onboarding/intake");\n  }\n'''
new = '''  function handleContinue() {\n    const valid = validateConsentStep();\n    if (!valid) return;\n    try {\n      window.sessionStorage.setItem(\n        INTAKE_CONSENT_STORAGE_KEY,\n        JSON.stringify({\n          consentAccepted: values.consentAccepted,\n          privacyAccepted: values.privacyAccepted,\n          consentVersion: values.consentVersion,\n          privacyPolicyVersion: values.privacyPolicyVersion || values.consentVersion,\n        })\n      );\n    } catch {\n      // Temporary client persistence is best-effort; backend submit remains source of truth.\n    }\n    navigate("/patient/onboarding/intake");\n  }\n'''
text = text.replace(old, new)
path.write_text(text)
PY
```

---

# 5. Tests

## Command 5.1 — Backend consent event history tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-api/tests/modules/intake/test_consent_event_history.py <<'PY'
from __future__ import annotations

from sqlalchemy import select

from app.db.models.consent_event import ConsentEvent


def register_patient_and_login(client, *, email: str = "consent.event@example.com", password: str = "StrongPass123"):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Consent Event Patient"},
    )
    assert response.status_code in (200, 201), response.json()
    access_token = response.json()["tokens"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def submit_intake_with_consent(client, headers, *, service_need="mental_health"):
    draft_response = client.post(
        "/api/v1/intake/drafts",
        json={"service_need": service_need},
        headers=headers,
    )
    assert draft_response.status_code == 201, draft_response.json()
    intake_id = draft_response.json()["data"]["id"]

    submit_payload = {
        "service_need": service_need,
        "consent_acknowledged": True,
        "consent_version": "2026.04",
        "privacy_policy_version": "2026.04",
        "preferred_contact_method": "email",
        "emergency_contact_name": "Grace",
        "emergency_contact_phone": "+256700002222",
        "emergency_contact_relationship": "Aunt",
    }
    response = client.post(f"/api/v1/intake/{intake_id}/submit", json=submit_payload, headers=headers)
    assert response.status_code == 200, response.json()
    return response.json()["data"]


def test_submit_intake_creates_durable_consent_event(client, db_session):
    headers = register_patient_and_login(client)
    data = submit_intake_with_consent(client, headers)

    event = db_session.execute(select(ConsentEvent)).scalar_one()
    assert event.patient_id == data["patient_id"]
    assert event.user_id is not None
    assert event.intake_submission_id == data["id"]
    assert event.event_type == "intake_consent_accepted"
    assert event.consent_policy_version == "2026.04"
    assert event.privacy_policy_version == "2026.04"
    assert event.accepted is True

    assert data["consent_event"]["id"] == event.id


def test_patient_can_fetch_consent_event_history(client):
    headers = register_patient_and_login(client, email="consent.history@example.com")
    submit_intake_with_consent(client, headers)

    response = client.get("/api/v1/intake/me/consent-events", headers=headers)
    assert response.status_code == 200, response.json()
    body = response.json()
    assert body["data"]["total"] == 1
    assert body["data"]["events"][0]["consent_policy_version"] == "2026.04"
    assert body["data"]["events"][0]["privacy_policy_version"] == "2026.04"
PY
```

## Command 5.2 — Extend existing versioning tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat >> pbbf-api/tests/modules/intake/test_consent_versioning.py <<'PY'


def test_privacy_policy_version_is_required():
    with pytest.raises(HTTPException) as exc:
        ensure_submission_requirements(
            consent_acknowledged=True,
            consent_version=CURRENT_CONSENT_VERSION,
            privacy_policy_version=None,
            service_need="mental_health",
        )

    assert exc.value.status_code == 400
    assert "Privacy policy version" in exc.value.detail
PY
```

## Command 5.3 — Frontend consent persistence test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-telehealth/src/modules/intake/__tests__/ConsentPersistence.test.jsx <<'JS'
import { act, renderHook } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { useIntakeForm } from "../hooks/useIntakeForm";
import { INTAKE_CONSENT_STORAGE_KEY } from "../utils/intakeSchema";
import { saveIntakeDraftRequest, submitIntakeRequest } from "../services/intakeApi";

vi.mock("../services/intakeApi", () => ({
  getMyIntakeRequest: vi.fn().mockRejectedValue({ status: 404 }),
  saveIntakeDraftRequest: vi.fn().mockResolvedValue({ data: { id: 44, service_need: "mental_health" } }),
  submitIntakeRequest: vi.fn().mockResolvedValue({
    message: "Intake submitted successfully.",
    data: { id: 44, status: "submitted", service_need: "mental_health" },
  }),
}));

describe("Consent persistence", () => {
  beforeEach(() => {
    window.sessionStorage.clear();
    vi.clearAllMocks();
  });

  it("rehydrates temporary consent state from session storage", () => {
    window.sessionStorage.setItem(
      INTAKE_CONSENT_STORAGE_KEY,
      JSON.stringify({
        consentAccepted: true,
        privacyAccepted: true,
        consentVersion: "2026.04",
        privacyPolicyVersion: "2026.04",
      })
    );

    const { result } = renderHook(() => useIntakeForm());

    expect(result.current.values.consentAccepted).toBe(true);
    expect(result.current.values.privacyAccepted).toBe(true);
    expect(result.current.values.consentVersion).toBe("2026.04");
    expect(result.current.values.privacyPolicyVersion).toBe("2026.04");
  });

  it("submits consent versions and clears temporary consent state", async () => {
    window.sessionStorage.setItem(
      INTAKE_CONSENT_STORAGE_KEY,
      JSON.stringify({
        consentAccepted: true,
        privacyAccepted: true,
        consentVersion: "2026.04",
        privacyPolicyVersion: "2026.04",
      })
    );

    const { result } = renderHook(() => useIntakeForm());

    await act(async () => {
      result.current.updateField("fullName", "Consent Patient");
      result.current.updateField("dateOfBirth", "1995-01-01");
      result.current.updateField("phoneNumber", "+256700000000");
      result.current.updateField("postpartumSummary", "Needs care follow-up.");
      result.current.updateField("emergencyContactName", "Grace");
      result.current.updateField("emergencyContactRelationship", "Aunt");
      result.current.updateField("emergencyContactPhone", "+256700000001");
      result.current.toggleServiceNeed("mental_health");
    });

    await act(async () => {
      await result.current.submitIntake();
    });

    expect(saveIntakeDraftRequest).toHaveBeenCalled();
    expect(submitIntakeRequest).toHaveBeenCalled();
    const submittedPayload = submitIntakeRequest.mock.calls[0][1];
    expect(submittedPayload.consent_acknowledged).toBe(true);
    expect(submittedPayload.consent_version).toBe("2026.04");
    expect(submittedPayload.privacy_policy_version).toBe("2026.04");
    expect(window.sessionStorage.getItem(INTAKE_CONSENT_STORAGE_KEY)).toBeNull();
  });
});
JS
```

---

# 6. Validation

## Command 6.1 — Backend compile

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
python -m py_compile \
  app/db/models/consent_event.py \
  app/modules/intake/router.py \
  app/modules/intake/schemas.py \
  app/modules/intake/service.py \
  app/modules/intake/repository.py \
  app/modules/intake/validators.py
```

## Command 6.2 — Alembic smoke

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
alembic heads
alembic history | tail -20
```

Expected head:

```text
f20260612_stage4 (head)
```

## Command 6.3 — Backend intake tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/intake/test_create_draft.py \
       tests/modules/intake/test_submit_intake.py \
       tests/modules/intake/test_consent_capture.py \
       tests/modules/intake/test_consent_versioning.py \
       tests/modules/intake/test_consent_event_history.py -q
```

## Command 6.4 — Frontend intake test and build

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm test -- --run src/modules/intake/__tests__/ConsentPersistence.test.jsx
npm run build
```

---

# 7. Post-Apply Inspection

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

grep -n "consent_event\|ConsentEvent" pbbf-api/app/db/models/__init__.py

grep -n "create_consent_event\|list_consent_events_for_patient" pbbf-api/app/modules/intake/repository.py

grep -n "list_consent_events_for_current_patient\|consent_event" pbbf-api/app/modules/intake/service.py

grep -n "me/consent-events" pbbf-api/app/modules/intake/router.py

grep -n "INTAKE_CONSENT_STORAGE_KEY\|privacyPolicyVersion" \
  pbbf-telehealth/src/modules/intake/utils/intakeSchema.js \
  pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js \
  pbbf-telehealth/src/modules/intake/pages/ConsentPage.jsx
```

---

# 8. Completion Checklist

```text
[ ] consent_events model exists.
[ ] consent_events migration uses f20260612_stage3 as down_revision.
[ ] consent_events model is registered.
[ ] Intake submit creates durable consent event.
[ ] Consent event stores patient_id.
[ ] Consent event stores user_id.
[ ] Consent event stores intake_submission_id.
[ ] Consent event stores consent_policy_version.
[ ] Consent event stores privacy_policy_version.
[ ] Consent event history endpoint works.
[ ] Frontend consent survives ConsentPage -> IntakeFormPage.
[ ] Frontend sends consent_version and privacy_policy_version.
[ ] Temporary frontend consent state clears after successful submit.
[ ] Backend intake tests pass.
[ ] Frontend consent persistence test passes.
[ ] Frontend build passes.
```

---

# 9. Rollback

If needed, restore from your Stage 4 backup:

```bash
echo "$STAGE4_BACKUP_DIR"
```

Remove created files only if rolling back Stage 4 fully:

```bash
rm -f pbbf-api/app/db/models/consent_event.py
rm -f pbbf-api/alembic/versions/f20260612_stage4_add_consent_events.py
rm -f pbbf-api/tests/modules/intake/test_consent_event_history.py
rm -f pbbf-telehealth/src/modules/intake/__tests__/ConsentPersistence.test.jsx
```

---

# 10. Suggested Commit Message

After validation passes:

```bash
git add .
git commit -m "Stage 4: persist durable intake consent events"
```

Optional detailed commit:

```bash
git commit -m "Stage 4: persist durable intake consent events" \
  -m "Add consent_events model and migration, persist consent/privacy versions during intake submit, expose patient consent history, and preserve frontend consent state between onboarding steps."
```
