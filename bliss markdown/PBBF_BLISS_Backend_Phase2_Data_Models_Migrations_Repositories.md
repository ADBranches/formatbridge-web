# PBBF BLISS — Backend Phase 2 Populated Files
**Phase:** Backend Phase 2 — Data Models, Migrations, and Repository Base Layer  
**Objective:** Create or finalize the core database model layer and make migrations reliable enough for the rest of the system.

This package assumes the **Phase 1 foundation files** are already in place, especially:
- `app/db/base.py`
- `app/db/session.py`
- `app/db/models/__init__.py`
- `app/db/repositories/base.py`
- `tests/conftest.py`

The code below is designed to be **dropped into your current FastAPI modular backend** and keep the architecture clean for later module expansion.

---

## Phase 2 outcome

After applying this phase:
- all core MVP entities exist as concrete SQLAlchemy models,
- relationships are explicitly defined,
- repository access is reusable and predictable,
- Alembic can generate and apply the initial migration cleanly,
- reference roles can be seeded,
- repository CRUD and relationship integrity can be tested before service-layer expansion.

---

## Model and repository conventions used in this phase

1. **SQLAlchemy 2.0 style** is used consistently.
2. **Integer primary keys** are used for simplicity and stable local development.
3. **TimestampMixin** from Phase 1 is reused everywhere appropriate.
4. All model relationships use clear `back_populates` names to avoid ambiguity.
5. Soft-delete is not introduced yet in this phase; it can be added later if needed.
6. The migration included below is written as an explicit initial schema migration so the downgrade path is also clear.

---

## 1) `app/db/models/user.py`

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.appointment import Appointment
    from app.db.models.audit_log import AuditLog
    from app.db.models.encounter import Encounter
    from app.db.models.intake_submission import IntakeSubmission
    from app.db.models.notification import Notification
    from app.db.models.patient import Patient
    from app.db.models.provider import Provider
    from app.db.models.referral import Referral
    from app.db.models.role import Role
    from app.db.models.screening import Screening


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    must_change_password: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")

    role: Mapped[Role | None] = relationship("Role", back_populates="users")
    patient_profile: Mapped[Patient | None] = relationship("Patient", back_populates="user", uselist=False)
    provider_profile: Mapped[Provider | None] = relationship("Provider", back_populates="user", uselist=False)

    notifications: Mapped[list[Notification]] = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    audit_logs: Mapped[list[AuditLog]] = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    created_intake_submissions: Mapped[list[IntakeSubmission]] = relationship(
        "IntakeSubmission",
        back_populates="submitted_by_user",
        foreign_keys="IntakeSubmission.submitted_by_user_id",
    )
    created_screenings: Mapped[list[Screening]] = relationship(
        "Screening",
        back_populates="created_by_user",
        foreign_keys="Screening.created_by_user_id",
    )
    created_referrals: Mapped[list[Referral]] = relationship(
        "Referral",
        back_populates="created_by_user",
        foreign_keys="Referral.created_by_user_id",
    )
    documented_encounters: Mapped[list[Encounter]] = relationship(
        "Encounter",
        back_populates="documented_by_user",
        foreign_keys="Encounter.documented_by_user_id",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email!r})"
```

---

## 2) `app/db/models/role.py`

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.user import User


class Role(Base, TimestampMixin):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    users: Mapped[list[User]] = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id}, name={self.name!r})"
```

---

## 3) `app/db/models/patient.py`

```python
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.appointment import Appointment
    from app.db.models.encounter import Encounter
    from app.db.models.intake_submission import IntakeSubmission
    from app.db.models.referral import Referral
    from app.db.models.screening import Screening
    from app.db.models.user import User


class Patient(Base, TimestampMixin):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    emergency_contact_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    insurance_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    preferred_language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    consent_status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")

    user: Mapped[User] = relationship("User", back_populates="patient_profile")
    appointments: Mapped[list[Appointment]] = relationship(
        "Appointment",
        back_populates="patient",
        cascade="all, delete-orphan",
    )
    intake_submissions: Mapped[list[IntakeSubmission]] = relationship(
        "IntakeSubmission",
        back_populates="patient",
        cascade="all, delete-orphan",
    )
    screenings: Mapped[list[Screening]] = relationship(
        "Screening",
        back_populates="patient",
        cascade="all, delete-orphan",
    )
    encounters: Mapped[list[Encounter]] = relationship("Encounter", back_populates="patient")
    referrals: Mapped[list[Referral]] = relationship("Referral", back_populates="patient")

    def __repr__(self) -> str:
        return f"Patient(id={self.id}, user_id={self.user_id})"
```

---

## 4) `app/db/models/provider.py`

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.appointment import Appointment
    from app.db.models.encounter import Encounter
    from app.db.models.user import User


class Provider(Base, TimestampMixin):
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    specialty: Mapped[str | None] = mapped_column(String(120), nullable=True)
    license_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    availability_profile: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_accepting_patients: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")

    user: Mapped[User] = relationship("User", back_populates="provider_profile")
    appointments: Mapped[list[Appointment]] = relationship("Appointment", back_populates="provider")
    encounters: Mapped[list[Encounter]] = relationship("Encounter", back_populates="provider")

    def __repr__(self) -> str:
        return f"Provider(id={self.id}, user_id={self.user_id})"
```

---

## 5) `app/db/models/appointment.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.encounter import Encounter
    from app.db.models.patient import Patient
    from app.db.models.provider import Provider
    from app.db.models.telehealth_session import TelehealthSession


class Appointment(Base, TimestampMixin):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id", ondelete="RESTRICT"), nullable=False, index=True)

    appointment_type: Mapped[str] = mapped_column(String(80), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheduled_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    scheduled_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    timezone_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="booked", server_default="booked")
    meeting_link: Mapped[str | None] = mapped_column(Text, nullable=True)

    patient: Mapped[Patient] = relationship("Patient", back_populates="appointments")
    provider: Mapped[Provider] = relationship("Provider", back_populates="appointments")
    telehealth_session: Mapped[TelehealthSession | None] = relationship(
        "TelehealthSession",
        back_populates="appointment",
        uselist=False,
        cascade="all, delete-orphan",
    )
    encounter: Mapped[Encounter | None] = relationship(
        "Encounter",
        back_populates="appointment",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Appointment(id={self.id}, status={self.status!r})"
```

---

## 6) `app/db/models/telehealth_session.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.appointment import Appointment


class TelehealthSession(Base, TimestampMixin):
    __tablename__ = "telehealth_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    session_link: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="scheduled", server_default="scheduled")
    patient_joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    provider_joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    session_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    session_ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_reason: Mapped[str | None] = mapped_column(String(120), nullable=True)

    appointment: Mapped[Appointment] = relationship("Appointment", back_populates="telehealth_session")

    def __repr__(self) -> str:
        return f"TelehealthSession(id={self.id}, appointment_id={self.appointment_id})"
```

---

## 7) `app/db/models/intake_submission.py`

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.patient import Patient
    from app.db.models.user import User


class IntakeSubmission(Base, TimestampMixin):
    __tablename__ = "intake_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", server_default="draft")
    service_need: Mapped[str | None] = mapped_column(String(100), nullable=True)
    preferred_contact_method: Mapped[str | None] = mapped_column(String(30), nullable=True)
    screening_ready: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    attachments_json: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    submission_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    patient: Mapped[Patient] = relationship("Patient", back_populates="intake_submissions")
    submitted_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="created_intake_submissions",
        foreign_keys=[submitted_by_user_id],
    )

    def __repr__(self) -> str:
        return f"IntakeSubmission(id={self.id}, status={self.status!r})"
```

---

## 8) `app/db/models/screening.py`

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.encounter import Encounter
    from app.db.models.patient import Patient
    from app.db.models.user import User


class Screening(Base, TimestampMixin):
    __tablename__ = "screenings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    encounter_id: Mapped[int | None] = mapped_column(ForeignKey("encounters.id", ondelete="SET NULL"), nullable=True)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    screening_type: Mapped[str] = mapped_column(String(50), nullable=False, default="EPDS", server_default="EPDS")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed", server_default="completed")
    answers_json: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    severity_band: Mapped[str | None] = mapped_column(String(50), nullable=True)
    interpretation: Mapped[str | None] = mapped_column(Text, nullable=True)
    critical_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    patient: Mapped[Patient] = relationship("Patient", back_populates="screenings")
    encounter: Mapped[Encounter | None] = relationship("Encounter", back_populates="screenings")
    created_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="created_screenings",
        foreign_keys=[created_by_user_id],
    )

    def __repr__(self) -> str:
        return f"Screening(id={self.id}, type={self.screening_type!r}, score={self.score})"
```

---

## 9) `app/db/models/encounter.py`

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.appointment import Appointment
    from app.db.models.patient import Patient
    from app.db.models.provider import Provider
    from app.db.models.referral import Referral
    from app.db.models.screening import Screening
    from app.db.models.user import User


class Encounter(Base, TimestampMixin):
    __tablename__ = "encounters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id", ondelete="RESTRICT"), nullable=False, index=True)
    documented_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", server_default="draft")
    chief_complaint: Mapped[str | None] = mapped_column(Text, nullable=True)
    assessment: Mapped[str | None] = mapped_column(Text, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    care_plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    follow_up_plan: Mapped[str | None] = mapped_column(Text, nullable=True)

    appointment: Mapped[Appointment] = relationship("Appointment", back_populates="encounter")
    patient: Mapped[Patient] = relationship("Patient", back_populates="encounters")
    provider: Mapped[Provider] = relationship("Provider", back_populates="encounters")
    documented_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="documented_encounters",
        foreign_keys=[documented_by_user_id],
    )
    screenings: Mapped[list[Screening]] = relationship("Screening", back_populates="encounter")
    referrals: Mapped[list[Referral]] = relationship("Referral", back_populates="encounter")

    def __repr__(self) -> str:
        return f"Encounter(id={self.id}, appointment_id={self.appointment_id})"
```

---

## 10) `app/db/models/referral.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.encounter import Encounter
    from app.db.models.patient import Patient
    from app.db.models.user import User


class Referral(Base, TimestampMixin):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    encounter_id: Mapped[int | None] = mapped_column(ForeignKey("encounters.id", ondelete="SET NULL"), nullable=True)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    category: Mapped[str] = mapped_column(String(100), nullable=False)
    referral_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    destination_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="created", server_default="created")
    follow_up_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completion_outcome: Mapped[str | None] = mapped_column(Text, nullable=True)

    patient: Mapped[Patient] = relationship("Patient", back_populates="referrals")
    encounter: Mapped[Encounter | None] = relationship("Encounter", back_populates="referrals")
    created_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="created_referrals",
        foreign_keys=[created_by_user_id],
    )

    def __repr__(self) -> str:
        return f"Referral(id={self.id}, category={self.category!r})"
```

---

## 11) `app/db/models/notification.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.user import User


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    channel: Mapped[str] = mapped_column(String(30), nullable=False)
    notification_type: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", server_default="pending")
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        return f"Notification(id={self.id}, channel={self.channel!r}, status={self.status!r})"
```

---

## 12) `app/db/models/audit_log.py`

```python
from __future__ import annotations

from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_name: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="audit_logs")

    def __repr__(self) -> str:
        return f"AuditLog(id={self.id}, action={self.action!r}, entity_name={self.entity_name!r})"
```

---

## 13) `app/db/models/__init__.py`

> This completes the Phase 1 file so the new models are import-stable and discoverable.

```python
from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from app.db.base import Base

MODELS_PACKAGE = __name__
MODELS_PATH = Path(__file__).resolve().parent


EXPLICIT_MODEL_MODULES = [
    "role",
    "user",
    "patient",
    "provider",
    "appointment",
    "telehealth_session",
    "intake_submission",
    "encounter",
    "screening",
    "referral",
    "notification",
    "audit_log",
]


def import_all_models() -> list[str]:
    imported_modules: list[str] = []

    for module_name in EXPLICIT_MODEL_MODULES:
        module_path = f"{MODELS_PACKAGE}.{module_name}"
        importlib.import_module(module_path)
        imported_modules.append(module_name)

    for module_info in pkgutil.iter_modules([str(MODELS_PATH)]):
        if module_info.name.startswith("_"):
            continue
        if module_info.name in imported_modules:
            continue

        module_path = f"{MODELS_PACKAGE}.{module_info.name}"
        importlib.import_module(module_path)
        imported_modules.append(module_info.name)

    return imported_modules


def get_model_class(model_name: str):
    import_all_models()

    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        if model_class.__name__ == model_name:
            return model_class

    return None
```

---

## 14) `app/db/repositories/base.py`

> This is the completed shared repository file for Phase 2. It expands the Phase 1 foundation version so feature repositories can inherit common CRUD behavior.

```python
from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def get_by_id(self, record_id: Any) -> ModelType | None:
        return self.db.get(self.model, record_id)

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        order_by=None,
    ) -> list[ModelType]:
        statement: Select = select(self.model).offset(offset).limit(limit)
        if order_by is not None:
            statement = statement.order_by(order_by)
        return self.db.execute(statement).scalars().all()

    def count(self) -> int:
        statement = select(func.count()).select_from(self.model)
        return int(self.db.execute(statement).scalar_one())

    def update(self, instance: ModelType, **kwargs) -> ModelType:
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def delete(self, instance: ModelType) -> None:
        self.db.delete(instance)
        self.db.flush()
```

---

## 15) `app/db/repositories/user_repository.py`

```python
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.execute(statement).scalars().first()

    def list_active_users(self) -> list[User]:
        statement = select(User).where(User.is_active.is_(True)).order_by(User.created_at.desc())
        return self.db.execute(statement).scalars().all()

    def list_by_role_name(self, role_name: str) -> list[User]:
        statement = (
            select(User)
            .join(User.role)
            .where(User.role.has(name=role_name))
            .order_by(User.created_at.desc())
        )
        return self.db.execute(statement).scalars().all()
```

---

## 16) `app/db/repositories/appointment_repository.py`

```python
from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models.appointment import Appointment
from app.db.repositories.base import BaseRepository


class AppointmentRepository(BaseRepository[Appointment]):
    def __init__(self, db: Session):
        super().__init__(Appointment, db)

    def get_with_related(self, appointment_id: int) -> Appointment | None:
        statement = (
            select(Appointment)
            .options(
                joinedload(Appointment.patient).joinedload("user"),
                joinedload(Appointment.provider).joinedload("user"),
                joinedload(Appointment.telehealth_session),
                joinedload(Appointment.encounter),
            )
            .where(Appointment.id == appointment_id)
        )
        return self.db.execute(statement).scalars().first()

    def list_for_patient(self, patient_id: int) -> list[Appointment]:
        statement = (
            select(Appointment)
            .where(Appointment.patient_id == patient_id)
            .order_by(Appointment.scheduled_start.desc())
        )
        return self.db.execute(statement).scalars().all()

    def list_for_provider(self, provider_id: int) -> list[Appointment]:
        statement = (
            select(Appointment)
            .where(Appointment.provider_id == provider_id)
            .order_by(Appointment.scheduled_start.desc())
        )
        return self.db.execute(statement).scalars().all()

    def list_between(self, starts_at: datetime, ends_at: datetime) -> list[Appointment]:
        statement = (
            select(Appointment)
            .where(Appointment.scheduled_start >= starts_at)
            .where(Appointment.scheduled_start <= ends_at)
            .order_by(Appointment.scheduled_start.asc())
        )
        return self.db.execute(statement).scalars().all()
```

---

## 17) `app/db/repositories/screening_repository.py`

```python
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.screening import Screening
from app.db.repositories.base import BaseRepository


class ScreeningRepository(BaseRepository[Screening]):
    def __init__(self, db: Session):
        super().__init__(Screening, db)

    def list_for_patient(self, patient_id: int) -> list[Screening]:
        statement = (
            select(Screening)
            .where(Screening.patient_id == patient_id)
            .order_by(Screening.created_at.desc())
        )
        return self.db.execute(statement).scalars().all()

    def list_critical(self) -> list[Screening]:
        statement = (
            select(Screening)
            .where(Screening.critical_flag.is_(True))
            .order_by(Screening.created_at.desc())
        )
        return self.db.execute(statement).scalars().all()

    def list_by_type(self, screening_type: str) -> list[Screening]:
        statement = (
            select(Screening)
            .where(Screening.screening_type == screening_type)
            .order_by(Screening.created_at.desc())
        )
        return self.db.execute(statement).scalars().all()
```

---

## 18) `app/db/repositories/encounter_repository.py`

```python
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models.encounter import Encounter
from app.db.repositories.base import BaseRepository


class EncounterRepository(BaseRepository[Encounter]):
    def __init__(self, db: Session):
        super().__init__(Encounter, db)

    def get_by_appointment_id(self, appointment_id: int) -> Encounter | None:
        statement = select(Encounter).where(Encounter.appointment_id == appointment_id)
        return self.db.execute(statement).scalars().first()

    def get_with_related(self, encounter_id: int) -> Encounter | None:
        statement = (
            select(Encounter)
            .options(
                joinedload(Encounter.patient).joinedload("user"),
                joinedload(Encounter.provider).joinedload("user"),
                joinedload(Encounter.screenings),
                joinedload(Encounter.referrals),
            )
            .where(Encounter.id == encounter_id)
        )
        return self.db.execute(statement).scalars().first()

    def list_for_provider(self, provider_id: int) -> list[Encounter]:
        statement = (
            select(Encounter)
            .where(Encounter.provider_id == provider_id)
            .order_by(Encounter.created_at.desc())
        )
        return self.db.execute(statement).scalars().all()
```

---

## 19) `app/db/repositories/referral_repository.py`

```python
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.referral import Referral
from app.db.repositories.base import BaseRepository


class ReferralRepository(BaseRepository[Referral]):
    def __init__(self, db: Session):
        super().__init__(Referral, db)

    def list_for_patient(self, patient_id: int) -> list[Referral]:
        statement = (
            select(Referral)
            .where(Referral.patient_id == patient_id)
            .order_by(Referral.created_at.desc())
        )
        return self.db.execute(statement).scalars().all()

    def list_open(self) -> list[Referral]:
        statement = (
            select(Referral)
            .where(Referral.status.in_(["created", "sent", "acknowledged"]))
            .order_by(Referral.created_at.desc())
        )
        return self.db.execute(statement).scalars().all()

    def list_by_status(self, status: str) -> list[Referral]:
        statement = (
            select(Referral)
            .where(Referral.status == status)
            .order_by(Referral.created_at.desc())
        )
        return self.db.execute(statement).scalars().all()
```

---

## 20) `alembic/env.py`

> Use this if your current Alembic environment is not yet wired to the app metadata and settings.

```python
from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.common.config.settings import get_settings
from app.db.base import Base
from app.db.models import import_all_models

config = context.config
settings = get_settings()

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

import_all_models()
target_metadata = Base.metadata


def get_database_url() -> str:
    return settings.effective_database_url


def run_migrations_offline() -> None:
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()



def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## 21) `alembic/versions/20260421_0001_initial_core_models.py`

```python
"""initial core mvp models

Revision ID: 20260421_0001
Revises: 
Create Date: 2026-04-21 00:00:01
"""

from alembic import op
import sqlalchemy as sa


revision = "20260421_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("name", name="uq_roles_name"),
    )
    op.create_index("ix_roles_name", "roles", ["name"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("must_change_password", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_users_role_id_roles", ondelete="SET NULL"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_index("ix_users_id", "users", ["id"], unique=False)

    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("emergency_contact_name", sa.String(length=150), nullable=True),
        sa.Column("emergency_contact_phone", sa.String(length=30), nullable=True),
        sa.Column("insurance_info", sa.Text(), nullable=True),
        sa.Column("preferred_language", sa.String(length=50), nullable=True),
        sa.Column("consent_status", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_patients_user_id_users", ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", name="uq_patients_user_id"),
    )

    op.create_table(
        "providers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("specialty", sa.String(length=120), nullable=True),
        sa.Column("license_number", sa.String(length=100), nullable=True),
        sa.Column("availability_profile", sa.Text(), nullable=True),
        sa.Column("is_accepting_patients", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_providers_user_id_users", ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", name="uq_providers_user_id"),
    )

    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("provider_id", sa.Integer(), nullable=False),
        sa.Column("appointment_type", sa.String(length=80), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("scheduled_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("scheduled_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("timezone_name", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="booked"),
        sa.Column("meeting_link", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], name="fk_appointments_patient_id_patients", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["provider_id"], ["providers.id"], name="fk_appointments_provider_id_providers", ondelete="RESTRICT"),
    )
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"], unique=False)
    op.create_index("ix_appointments_provider_id", "appointments", ["provider_id"], unique=False)
    op.create_index("ix_appointments_scheduled_start", "appointments", ["scheduled_start"], unique=False)

    op.create_table(
        "telehealth_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("appointment_id", sa.Integer(), nullable=False),
        sa.Column("session_link", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="scheduled"),
        sa.Column("patient_joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("provider_joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("session_started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("session_ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_reason", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["appointment_id"], ["appointments.id"], name="fk_telehealth_sessions_appointment_id_appointments", ondelete="CASCADE"),
        sa.UniqueConstraint("appointment_id", name="uq_telehealth_sessions_appointment_id"),
    )
    op.create_index("ix_telehealth_sessions_appointment_id", "telehealth_sessions", ["appointment_id"], unique=False)

    op.create_table(
        "encounters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("appointment_id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("provider_id", sa.Integer(), nullable=False),
        sa.Column("documented_by_user_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        sa.Column("chief_complaint", sa.Text(), nullable=True),
        sa.Column("assessment", sa.Text(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("care_plan", sa.Text(), nullable=True),
        sa.Column("follow_up_plan", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["appointment_id"], ["appointments.id"], name="fk_encounters_appointment_id_appointments", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], name="fk_encounters_patient_id_patients", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["provider_id"], ["providers.id"], name="fk_encounters_provider_id_providers", ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["documented_by_user_id"], ["users.id"], name="fk_encounters_documented_by_user_id_users", ondelete="SET NULL"),
        sa.UniqueConstraint("appointment_id", name="uq_encounters_appointment_id"),
    )
    op.create_index("ix_encounters_appointment_id", "encounters", ["appointment_id"], unique=False)
    op.create_index("ix_encounters_patient_id", "encounters", ["patient_id"], unique=False)
    op.create_index("ix_encounters_provider_id", "encounters", ["provider_id"], unique=False)

    op.create_table(
        "intake_submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("submitted_by_user_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        sa.Column("service_need", sa.String(length=100), nullable=True),
        sa.Column("preferred_contact_method", sa.String(length=30), nullable=True),
        sa.Column("screening_ready", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("attachments_json", sa.JSON(), nullable=True),
        sa.Column("submission_payload", sa.JSON(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], name="fk_intake_submissions_patient_id_patients", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["submitted_by_user_id"], ["users.id"], name="fk_intake_submissions_submitted_by_user_id_users", ondelete="SET NULL"),
    )
    op.create_index("ix_intake_submissions_patient_id", "intake_submissions", ["patient_id"], unique=False)

    op.create_table(
        "screenings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("encounter_id", sa.Integer(), nullable=True),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("screening_type", sa.String(length=50), nullable=False, server_default="EPDS"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="completed"),
        sa.Column("answers_json", sa.JSON(), nullable=True),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("severity_band", sa.String(length=50), nullable=True),
        sa.Column("interpretation", sa.Text(), nullable=True),
        sa.Column("critical_flag", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("review_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], name="fk_screenings_patient_id_patients", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["encounter_id"], ["encounters.id"], name="fk_screenings_encounter_id_encounters", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], name="fk_screenings_created_by_user_id_users", ondelete="SET NULL"),
    )
    op.create_index("ix_screenings_patient_id", "screenings", ["patient_id"], unique=False)

    op.create_table(
        "referrals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("encounter_id", sa.Integer(), nullable=True),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("referral_type", sa.String(length=100), nullable=True),
        sa.Column("destination_name", sa.String(length=255), nullable=True),
        sa.Column("contact_info", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="created"),
        sa.Column("follow_up_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completion_outcome", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], name="fk_referrals_patient_id_patients", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["encounter_id"], ["encounters.id"], name="fk_referrals_encounter_id_encounters", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], name="fk_referrals_created_by_user_id_users", ondelete="SET NULL"),
    )
    op.create_index("ix_referrals_patient_id", "referrals", ["patient_id"], unique=False)

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("channel", sa.String(length=30), nullable=False),
        sa.Column("notification_type", sa.String(length=100), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_notifications_user_id_users", ondelete="CASCADE"),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity_name", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_audit_logs_user_id_users", ondelete="SET NULL"),
    )
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"], unique=False)

    op.bulk_insert(
        sa.table(
            "roles",
            sa.column("name", sa.String()),
            sa.column("description", sa.Text()),
        ),
        [
            {"name": "patient", "description": "Patient self-service access"},
            {"name": "provider", "description": "Clinical care provider access"},
            {"name": "counselor", "description": "Counseling services access"},
            {"name": "lactation_consultant", "description": "Lactation services access"},
            {"name": "care_coordinator", "description": "Referral and coordination access"},
            {"name": "admin", "description": "Administrative and reporting access"},
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_audit_logs_user_id", table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_table("notifications")

    op.drop_index("ix_referrals_patient_id", table_name="referrals")
    op.drop_table("referrals")

    op.drop_index("ix_screenings_patient_id", table_name="screenings")
    op.drop_table("screenings")

    op.drop_index("ix_intake_submissions_patient_id", table_name="intake_submissions")
    op.drop_table("intake_submissions")

    op.drop_index("ix_encounters_provider_id", table_name="encounters")
    op.drop_index("ix_encounters_patient_id", table_name="encounters")
    op.drop_index("ix_encounters_appointment_id", table_name="encounters")
    op.drop_table("encounters")

    op.drop_index("ix_telehealth_sessions_appointment_id", table_name="telehealth_sessions")
    op.drop_table("telehealth_sessions")

    op.drop_index("ix_appointments_scheduled_start", table_name="appointments")
    op.drop_index("ix_appointments_provider_id", table_name="appointments")
    op.drop_index("ix_appointments_patient_id", table_name="appointments")
    op.drop_table("appointments")

    op.drop_table("providers")
    op.drop_table("patients")

    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_roles_name", table_name="roles")
    op.drop_table("roles")
```

---

## 22) `tests/test_models.py`

```python
from app.db.models import import_all_models, get_model_class
from app.db.session import init_db, db_session_context


def test_models_import_and_registry_resolution():
    imported = import_all_models()
    assert "user" in imported
    assert "appointment" in imported
    assert get_model_class("User") is not None
    assert get_model_class("Referral") is not None


def test_tables_can_be_created():
    init_db()
    with db_session_context() as db:
        assert db is not None
```

---

## 23) `tests/test_relationships.py`

```python
from datetime import datetime, timedelta, timezone

from app.db.models.appointment import Appointment
from app.db.models.encounter import Encounter
from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.referral import Referral
from app.db.models.role import Role
from app.db.models.screening import Screening
from app.db.models.telehealth_session import TelehealthSession
from app.db.models.user import User
from app.db.session import db_session_context, init_db


def test_core_relationship_integrity():
    init_db()

    with db_session_context() as db:
        patient_role = Role(name="patient", description="Patient")
        provider_role = Role(name="provider", description="Provider")
        db.add_all([patient_role, provider_role])
        db.flush()

        patient_user = User(
            role_id=patient_role.id,
            first_name="Sarah",
            last_name="Jones",
            email="sarah@example.com",
            phone="256700000001",
            password_hash="hashed",
        )
        provider_user = User(
            role_id=provider_role.id,
            first_name="Grace",
            last_name="Nankya",
            email="grace@example.com",
            phone="256700000002",
            password_hash="hashed",
        )
        db.add_all([patient_user, provider_user])
        db.flush()

        patient = Patient(user_id=patient_user.id, consent_status=True)
        provider = Provider(user_id=provider_user.id, specialty="Mental Health")
        db.add_all([patient, provider])
        db.flush()

        appointment = Appointment(
            patient_id=patient.id,
            provider_id=provider.id,
            appointment_type="mental_health",
            scheduled_start=datetime.now(timezone.utc),
            scheduled_end=datetime.now(timezone.utc) + timedelta(minutes=45),
            status="booked",
        )
        db.add(appointment)
        db.flush()

        session = TelehealthSession(
            appointment_id=appointment.id,
            session_link="https://example.com/session/1",
            status="scheduled",
        )
        encounter = Encounter(
            appointment_id=appointment.id,
            patient_id=patient.id,
            provider_id=provider.id,
            documented_by_user_id=provider_user.id,
            status="draft",
        )
        db.add_all([session, encounter])
        db.flush()

        screening = Screening(
            patient_id=patient.id,
            encounter_id=encounter.id,
            created_by_user_id=provider_user.id,
            screening_type="EPDS",
            score=14,
            severity_band="moderate",
            critical_flag=False,
        )
        referral = Referral(
            patient_id=patient.id,
            encounter_id=encounter.id,
            created_by_user_id=provider_user.id,
            category="community_support",
            status="created",
        )
        db.add_all([screening, referral])
        db.flush()

        db.refresh(patient)
        db.refresh(provider)
        db.refresh(appointment)
        db.refresh(encounter)

        assert patient.user.email == "sarah@example.com"
        assert provider.user.email == "grace@example.com"
        assert appointment.telehealth_session is not None
        assert appointment.encounter is not None
        assert encounter.screenings[0].screening_type == "EPDS"
        assert encounter.referrals[0].category == "community_support"
```

---

## 24) `tests/test_repositories.py`

```python
from datetime import datetime, timedelta, timezone

from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.role import Role
from app.db.models.screening import Screening
from app.db.models.user import User
from app.db.repositories.appointment_repository import AppointmentRepository
from app.db.repositories.encounter_repository import EncounterRepository
from app.db.repositories.referral_repository import ReferralRepository
from app.db.repositories.screening_repository import ScreeningRepository
from app.db.repositories.user_repository import UserRepository
from app.db.models.appointment import Appointment
from app.db.models.encounter import Encounter
from app.db.models.referral import Referral
from app.db.session import db_session_context, init_db


def test_repository_crud_and_queries():
    init_db()

    with db_session_context() as db:
        patient_role = Role(name="patient", description="Patient")
        provider_role = Role(name="provider", description="Provider")
        db.add_all([patient_role, provider_role])
        db.flush()

        user_repo = UserRepository(db)
        patient_user = user_repo.create(
            role_id=patient_role.id,
            first_name="Amina",
            last_name="Kato",
            email="amina@example.com",
            phone="256700100001",
            password_hash="hashed",
        )
        provider_user = user_repo.create(
            role_id=provider_role.id,
            first_name="Brian",
            last_name="Mugerwa",
            email="brian@example.com",
            phone="256700100002",
            password_hash="hashed",
        )

        patient = Patient(user_id=patient_user.id, consent_status=True)
        provider = Provider(user_id=provider_user.id, specialty="Lactation")
        db.add_all([patient, provider])
        db.flush()

        appointment_repo = AppointmentRepository(db)
        appointment = appointment_repo.create(
            patient_id=patient.id,
            provider_id=provider.id,
            appointment_type="lactation",
            scheduled_start=datetime.now(timezone.utc),
            scheduled_end=datetime.now(timezone.utc) + timedelta(minutes=30),
            status="booked",
        )

        encounter_repo = EncounterRepository(db)
        encounter = encounter_repo.create(
            appointment_id=appointment.id,
            patient_id=patient.id,
            provider_id=provider.id,
            documented_by_user_id=provider_user.id,
            status="draft",
        )

        screening_repo = ScreeningRepository(db)
        screening = screening_repo.create(
            patient_id=patient.id,
            encounter_id=encounter.id,
            created_by_user_id=provider_user.id,
            screening_type="EPDS",
            score=8,
            severity_band="mild",
            critical_flag=False,
        )

        referral_repo = ReferralRepository(db)
        referral = referral_repo.create(
            patient_id=patient.id,
            encounter_id=encounter.id,
            created_by_user_id=provider_user.id,
            category="nutrition_support",
            status="created",
        )

        assert user_repo.get_by_email("amina@example.com") is not None
        assert len(appointment_repo.list_for_patient(patient.id)) == 1
        assert len(encounter_repo.list_for_provider(provider.id)) == 1
        assert len(screening_repo.list_for_patient(patient.id)) == 1
        assert len(referral_repo.list_for_patient(patient.id)) == 1

        screening_repo.update(screening, critical_flag=True, severity_band="high")
        referral_repo.update(referral, status="sent")
        appointment_repo.update(appointment, status="confirmed")

        assert screening_repo.list_critical()[0].id == screening.id
        assert referral_repo.list_by_status("sent")[0].id == referral.id
        assert appointment_repo.get_by_id(appointment.id).status == "confirmed"
```

---

## 25) `tests/test_migrations_smoke.py`

```python
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_alembic_upgrade_and_downgrade_smoke():
    upgrade = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert upgrade.returncode == 0, upgrade.stderr

    downgrade = subprocess.run(
        ["alembic", "downgrade", "base"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert downgrade.returncode == 0, downgrade.stderr

    reupgrade = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert reupgrade.returncode == 0, reupgrade.stderr
```

---

## Minimal role seed note

The migration already seeds the minimum role set:
- patient
- provider
- counselor
- lactation_consultant
- care_coordinator
- admin

That means the system can boot with role records present immediately after:

```bash
alembic upgrade head
```

---

## Commands to run after adding these files

Because this phase introduces and changes model files, run these commands after pasting the code:

```bash
cd /home/trovas/Downloads/projects/byupw/block2_2026/BLISS/bliss-telehealth/pbbf-api

source env/bin/activate  # or your actual venv activation command
pip install -r requirements.txt

alembic upgrade head
pytest tests/test_models.py tests/test_relationships.py tests/test_repositories.py tests/test_migrations_smoke.py -q
```

If you decide to **autogenerate** the migration instead of using the explicit one above, use:

```bash
alembic revision --autogenerate -m "initial core models"
alembic upgrade head
alembic downgrade base
alembic upgrade head
```

---

## Important consistency checks before Phase 3

Before moving on, verify these are all true:
- `import_all_models()` runs without circular import failures.
- `alembic upgrade head` works on a clean database.
- `alembic downgrade base` also works.
- `User`, `Patient`, `Provider`, `Appointment`, `TelehealthSession`, `Encounter`, `Screening`, and `Referral` relationships work both forward and backward.
- repository CRUD methods work without manual session hacks.
- role reference data exists automatically after migration.

---

## Completion checkpoint for this phase

This phase is complete when:
- all core MVP entities exist in the database,
- their relationships are valid,
- migrations apply cleanly on a fresh database,
- downgrade works,
- repository CRUD passes tests,
- the backend is now safe for Phase 3 service-layer and API expansion.
