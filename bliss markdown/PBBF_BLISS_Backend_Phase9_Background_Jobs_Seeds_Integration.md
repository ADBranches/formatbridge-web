# PBBF BLISS — Backend Phase 9 Population
## Background Jobs, Seed Data, and Integration Test Layer

### Objective
Prepare the backend for realistic QA and deployment by adding asynchronous-job-ready utilities, reliable seed scripts, and broader integration coverage that exercises real multi-step workflows.

### Phase intent
This phase does **not** introduce new domain models. It makes the backend more usable in three practical ways:

1. It adds a clean `app/jobs/` package for reminder and notification job execution.
2. It makes seed scripts idempotent so local bootstrapping and QA can be repeated safely.
3. It adds end-to-end integration tests that simulate patient, provider, and admin journeys instead of testing only isolated units.

### Important implementation note
This phase assumes the earlier backend phases already provide these modules and route families:

- `auth`
- `users`
- `intake`
- `appointments`
- `screenings`
- `telehealth`
- `encounters`
- `referrals`
- `notifications`
- `audit`
- `admin`

It also assumes the database models from Phase 2 already exist and are wired into SQLAlchemy.

### Migration note
No new migration is required for this phase **unless** your actual earlier models still differ from the fields referenced below. This phase mainly adds jobs, scripts, and tests.

---

## File 1 — `app/jobs/__init__.py`

```python
"""Background-job entrypoints for the BLISS backend.

These jobs are intentionally framework-light. They can be triggered:
- directly from scripts
- from FastAPI BackgroundTasks
- from cron / systemd timers
- later from Celery, RQ, Dramatiq, or any real worker system

The goal in Phase 9 is not to introduce infrastructure complexity.
The goal is to make the backend job-ready with clean callable functions.
"""

from app.jobs.notification_jobs import dispatch_pending_notifications, run_notification_dispatch_job
from app.jobs.reminder_jobs import create_due_appointment_reminders, run_reminder_generation_job

__all__ = [
    "create_due_appointment_reminders",
    "run_reminder_generation_job",
    "dispatch_pending_notifications",
    "run_notification_dispatch_job",
]
```

---

## File 2 — `app/jobs/reminder_jobs.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.utils.datetime import utcnow
from app.db.models.appointment import Appointment
from app.db.models.notification import Notification
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ReminderJobResult:
    checked_appointments: int = 0
    created_notifications: int = 0
    skipped_existing: int = 0
    skipped_missing_user: int = 0


REMINDER_ELIGIBLE_STATUSES = {"booked", "confirmed", "rescheduled"}
REMINDER_KIND = "appointment_reminder"


def _window_bounds(now: datetime | None = None, hours_ahead: int = 24) -> tuple[datetime, datetime]:
    current = now or utcnow()
    return current, current + timedelta(hours=hours_ahead)


def _notification_exists(
    db: Session,
    *,
    appointment_id: int | str,
    user_id: int | str,
    scheduled_for: datetime,
) -> bool:
    stmt = (
        select(Notification.id)
        .where(Notification.appointment_id == appointment_id)
        .where(Notification.user_id == user_id)
        .where(Notification.kind == REMINDER_KIND)
        .where(Notification.scheduled_for == scheduled_for)
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none() is not None


def _build_message(appointment: Appointment) -> str:
    start = appointment.scheduled_start.isoformat()
    service = getattr(appointment, "service_type", "appointment")
    return f"Reminder: your {service} is scheduled for {start}."


def _infer_recipient_user_id(appointment: Appointment) -> int | str | None:
    patient = getattr(appointment, "patient", None)
    if patient is not None and getattr(patient, "user_id", None) is not None:
        return patient.user_id

    if getattr(appointment, "patient_user_id", None) is not None:
        return appointment.patient_user_id

    return None


def create_due_appointment_reminders(
    db: Session,
    *,
    now: datetime | None = None,
    hours_ahead: int = 24,
) -> ReminderJobResult:
    """Create queued notification rows for appointments approaching soon.

    This function only creates reminder records. It does not send them.
    Sending is handled by `notification_jobs.py`.
    """

    window_start, window_end = _window_bounds(now=now, hours_ahead=hours_ahead)
    result = ReminderJobResult()

    stmt = (
        select(Appointment)
        .where(Appointment.scheduled_start >= window_start)
        .where(Appointment.scheduled_start <= window_end)
        .where(Appointment.status.in_(REMINDER_ELIGIBLE_STATUSES))
        .order_by(Appointment.scheduled_start.asc())
    )
    appointments = list(db.execute(stmt).scalars().all())
    result.checked_appointments = len(appointments)

    for appointment in appointments:
        recipient_user_id = _infer_recipient_user_id(appointment)
        if recipient_user_id is None:
            result.skipped_missing_user += 1
            logger.warning(
                "Skipping reminder creation because appointment %s has no recipient user.",
                appointment.id,
            )
            continue

        if _notification_exists(
            db,
            appointment_id=appointment.id,
            user_id=recipient_user_id,
            scheduled_for=appointment.scheduled_start,
        ):
            result.skipped_existing += 1
            continue

        notification = Notification(
            user_id=recipient_user_id,
            appointment_id=appointment.id,
            channel="email",
            kind=REMINDER_KIND,
            message=_build_message(appointment),
            status="queued",
            scheduled_for=appointment.scheduled_start,
        )
        db.add(notification)
        result.created_notifications += 1

    db.commit()
    return result


def run_reminder_generation_job(*, hours_ahead: int = 24) -> ReminderJobResult:
    """Open a session and generate due reminder records."""

    db = SessionLocal()
    try:
        result = create_due_appointment_reminders(db, hours_ahead=hours_ahead)
        logger.info(
            "Reminder job complete: checked=%s created=%s skipped_existing=%s skipped_missing_user=%s",
            result.checked_appointments,
            result.created_notifications,
            result.skipped_existing,
            result.skipped_missing_user,
        )
        return result
    finally:
        db.close()
```

---

## File 3 — `app/jobs/notification_jobs.py`

```python
from __future__ import annotations

from dataclasses import dataclass
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.utils.datetime import utcnow
from app.db.models.notification import Notification
from app.db.session import SessionLocal
from app.modules.notifications.channels import send_email_notification, send_sms_notification

logger = logging.getLogger(__name__)

SUPPORTED_CHANNELS = {"email", "sms"}


@dataclass(slots=True)
class NotificationDispatchResult:
    attempted: int = 0
    sent: int = 0
    failed: int = 0
    skipped: int = 0


def _dispatch_single(notification: Notification) -> None:
    if notification.channel == "email":
        send_email_notification(notification)
        return

    if notification.channel == "sms":
        send_sms_notification(notification)
        return

    raise ValueError(f"Unsupported notification channel: {notification.channel}")


def dispatch_pending_notifications(
    db: Session,
    *,
    limit: int = 50,
) -> NotificationDispatchResult:
    """Dispatch queued notifications and update delivery status."""

    result = NotificationDispatchResult()

    stmt = (
        select(Notification)
        .where(Notification.status.in_(["queued", "pending"]))
        .order_by(Notification.created_at.asc())
        .limit(limit)
    )
    notifications = list(db.execute(stmt).scalars().all())

    for notification in notifications:
        result.attempted += 1

        if notification.channel not in SUPPORTED_CHANNELS:
            notification.status = "failed"
            notification.error_message = f"Unsupported channel: {notification.channel}"
            result.failed += 1
            continue

        try:
            _dispatch_single(notification)
            notification.status = "sent"
            notification.sent_at = utcnow()
            notification.error_message = None
            result.sent += 1
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Notification dispatch failed for notification=%s", notification.id)
            notification.status = "failed"
            notification.error_message = str(exc)
            result.failed += 1

    db.commit()
    return result


def run_notification_dispatch_job(*, limit: int = 50) -> NotificationDispatchResult:
    db = SessionLocal()
    try:
        result = dispatch_pending_notifications(db, limit=limit)
        logger.info(
            "Notification dispatch complete: attempted=%s sent=%s failed=%s skipped=%s",
            result.attempted,
            result.sent,
            result.failed,
            result.skipped,
        )
        return result
    finally:
        db.close()
```

---

## File 4 — `scripts/seed_roles.py`

```python
from __future__ import annotations

"""Seed system roles.

Usage:
    python -m scripts.seed_roles
"""

from sqlalchemy import select

from app.db.models.role import Role
from app.db.session import SessionLocal

DEFAULT_ROLES: tuple[dict[str, str], ...] = (
    {"name": "admin", "description": "System administrator"},
    {"name": "patient", "description": "External patient user"},
    {"name": "provider", "description": "Clinical provider"},
    {"name": "care_coordinator", "description": "Care coordination user"},
)


def seed_roles(db, *, commit: bool = True) -> list[Role]:
    seeded: list[Role] = []

    for payload in DEFAULT_ROLES:
        stmt = select(Role).where(Role.name == payload["name"])
        role = db.execute(stmt).scalar_one_or_none()

        if role is None:
            role = Role(
                name=payload["name"],
                description=payload["description"],
            )
            db.add(role)
            seeded.append(role)

    if commit:
        db.commit()

    return seeded


def main() -> None:
    db = SessionLocal()
    try:
        created = seed_roles(db)
        print(f"Role seeding complete. Newly created roles: {len(created)}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
```

---

## File 5 — `scripts/seed_users.py` (modify)

```python
from __future__ import annotations

"""Seed baseline demo users for development and QA.

Usage:
    python -m scripts.seed_users
"""

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.utils.security import hash_password
from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.role import Role
from app.db.models.user import User
from app.db.session import SessionLocal
from scripts.seed_roles import seed_roles


@dataclass(frozen=True, slots=True)
class DemoCredential:
    role: str
    email: str
    full_name: str
    password: str


DEFAULT_PASSWORD = "ChangeMe123!"

DEMO_USERS: tuple[DemoCredential, ...] = (
    DemoCredential(
        role="admin",
        email="admin@pbbf.local",
        full_name="PBBF Admin",
        password=DEFAULT_PASSWORD,
    ),
    DemoCredential(
        role="provider",
        email="provider@pbbf.local",
        full_name="PBBF Provider",
        password=DEFAULT_PASSWORD,
    ),
    DemoCredential(
        role="patient",
        email="patient@pbbf.local",
        full_name="PBBF Patient",
        password=DEFAULT_PASSWORD,
    ),
    DemoCredential(
        role="care_coordinator",
        email="care.coordinator@pbbf.local",
        full_name="PBBF Care Coordinator",
        password=DEFAULT_PASSWORD,
    ),
)


def _get_role_map(db: Session) -> dict[str, Role]:
    roles = db.execute(select(Role)).scalars().all()
    return {role.name: role for role in roles}


def _ensure_patient_profile(db: Session, user: User) -> None:
    existing = db.execute(select(Patient).where(Patient.user_id == user.id)).scalar_one_or_none()
    if existing is None:
        db.add(
            Patient(
                user_id=user.id,
                preferred_contact_method="email",
                intake_status="not_started",
            )
        )


def _ensure_provider_profile(db: Session, user: User) -> None:
    existing = db.execute(select(Provider).where(Provider.user_id == user.id)).scalar_one_or_none()
    if existing is None:
        db.add(
            Provider(
                user_id=user.id,
                specialty="Maternal Wellness",
                is_accepting_patients=True,
            )
        )


def seed_demo_users(db: Session, *, commit: bool = True) -> list[User]:
    seed_roles(db, commit=True)
    role_map = _get_role_map(db)

    created: list[User] = []

    for entry in DEMO_USERS:
        existing = db.execute(select(User).where(User.email == entry.email)).scalar_one_or_none()
        if existing is not None:
            continue

        user = User(
            email=entry.email,
            full_name=entry.full_name,
            password_hash=hash_password(entry.password),
            role_id=role_map[entry.role].id,
            is_active=True,
        )
        db.add(user)
        db.flush()

        if entry.role == "patient":
            _ensure_patient_profile(db, user)
        elif entry.role == "provider":
            _ensure_provider_profile(db, user)

        created.append(user)

    if commit:
        db.commit()

    return created


def main() -> None:
    db = SessionLocal()
    try:
        created = seed_demo_users(db)
        print(f"User seeding complete. Newly created users: {len(created)}")
        print("Default password for demo accounts: ChangeMe123!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
```

---

## File 6 — `scripts/seed_reference_data.py`

```python
from __future__ import annotations

"""Seed a realistic QA baseline dataset.

This script assumes roles and demo users exist or can be created.
It then creates:
- patient/provider profiles if missing
- a submitted intake
- a confirmed appointment
- a telehealth session
- an EPDS screening
- a draft encounter
- an open referral
- a queued notification
- a baseline audit record

Usage:
    python -m scripts.seed_reference_data
"""

from datetime import timedelta
from sqlalchemy import select

from app.common.utils.datetime import utcnow
from app.db.models.appointment import Appointment
from app.db.models.audit_log import AuditLog
from app.db.models.encounter import Encounter
from app.db.models.intake_submission import IntakeSubmission
from app.db.models.notification import Notification
from app.db.models.patient import Patient
from app.db.models.provider import Provider
from app.db.models.referral import Referral
from app.db.models.screening import Screening
from app.db.models.telehealth_session import TelehealthSession
from app.db.models.user import User
from app.db.session import SessionLocal
from scripts.seed_roles import seed_roles
from scripts.seed_users import seed_demo_users


def _get_user_by_email(db, email: str) -> User:
    user = db.execute(select(User).where(User.email == email)).scalar_one()
    return user


def seed_reference_data(db, *, commit: bool = True) -> None:
    seed_roles(db, commit=True)
    seed_demo_users(db, commit=True)

    admin = _get_user_by_email(db, "admin@pbbf.local")
    provider_user = _get_user_by_email(db, "provider@pbbf.local")
    patient_user = _get_user_by_email(db, "patient@pbbf.local")

    patient = db.execute(select(Patient).where(Patient.user_id == patient_user.id)).scalar_one()
    provider = db.execute(select(Provider).where(Provider.user_id == provider_user.id)).scalar_one()

    intake = db.execute(
        select(IntakeSubmission).where(IntakeSubmission.patient_id == patient.id)
    ).scalar_one_or_none()
    if intake is None:
        intake = IntakeSubmission(
            patient_id=patient.id,
            status="submitted",
            consent_accepted=True,
            service_need_category="mental_health",
            emergency_contact_name="Demo Emergency Contact",
            emergency_contact_phone="+256700000001",
            triage_ready=True,
        )
        db.add(intake)
        db.flush()

    appointment = db.execute(
        select(Appointment).where(Appointment.patient_id == patient.id)
    ).scalar_one_or_none()
    if appointment is None:
        appointment = Appointment(
            patient_id=patient.id,
            provider_id=provider.id,
            service_type="mental_health",
            scheduled_start=utcnow() + timedelta(hours=8),
            scheduled_end=utcnow() + timedelta(hours=9),
            timezone="Africa/Kampala",
            status="confirmed",
            reason="Initial postpartum wellness follow-up",
        )
        db.add(appointment)
        db.flush()

    session = db.execute(
        select(TelehealthSession).where(TelehealthSession.appointment_id == appointment.id)
    ).scalar_one_or_none()
    if session is None:
        db.add(
            TelehealthSession(
                appointment_id=appointment.id,
                session_key=f"session-{appointment.id}",
                join_url=f"https://telehealth.local/session/{appointment.id}",
                status="scheduled",
            )
        )

    screening = db.execute(
        select(Screening)
        .where(Screening.patient_id == patient.id)
        .where(Screening.screening_type == "epds")
    ).scalar_one_or_none()
    if screening is None:
        db.add(
            Screening(
                patient_id=patient.id,
                appointment_id=appointment.id,
                screening_type="epds",
                status="submitted",
                score=7,
                severity_band="low",
                critical_flag=False,
                answers_json={
                    "q1": 1, "q2": 1, "q3": 1, "q4": 0, "q5": 0,
                    "q6": 1, "q7": 1, "q8": 1, "q9": 1, "q10": 0,
                },
            )
        )

    encounter = db.execute(
        select(Encounter).where(Encounter.appointment_id == appointment.id)
    ).scalar_one_or_none()
    if encounter is None:
        encounter = Encounter(
            appointment_id=appointment.id,
            patient_id=patient.id,
            provider_id=provider.id,
            status="draft",
            note_text="Seeded draft encounter note.",
            follow_up_plan="Follow up in one week.",
        )
        db.add(encounter)
        db.flush()

    referral = db.execute(
        select(Referral).where(Referral.patient_id == patient.id)
    ).scalar_one_or_none()
    if referral is None:
        db.add(
            Referral(
                patient_id=patient.id,
                encounter_id=encounter.id,
                category="community_support",
                destination_name="Community Wellness Partner",
                status="created",
                notes="Seeded referral for QA.",
            )
        )

    existing_notification = db.execute(
        select(Notification)
        .where(Notification.user_id == patient_user.id)
        .where(Notification.kind == "appointment_reminder")
        .where(Notification.appointment_id == appointment.id)
    ).scalar_one_or_none()
    if existing_notification is None:
        db.add(
            Notification(
                user_id=patient_user.id,
                appointment_id=appointment.id,
                channel="email",
                kind="appointment_reminder",
                message="Seeded reminder notification.",
                status="queued",
                scheduled_for=appointment.scheduled_start,
            )
        )

    db.add(
        AuditLog(
            actor_user_id=admin.id,
            action="seed.reference_data",
            entity_type="system",
            entity_id="bootstrap",
            metadata_json={"source": "scripts.seed_reference_data"},
        )
    )

    if commit:
        db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        seed_reference_data(db)
        print("Reference data seeding complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
```

---

## File 7 — `tests/integration/test_patient_journey.py`

```python
from __future__ import annotations

"""Integration tests for a realistic patient workflow.

Assumes the Phase 1-8 routes exist and the global `client` fixture from tests/conftest.py
returns a FastAPI TestClient with a test database override.
"""

from app.jobs.notification_jobs import dispatch_pending_notifications
from app.jobs.reminder_jobs import create_due_appointment_reminders


def _register_patient(client, email: str, password: str = "PatientPass123!"):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Journey Patient",
            "role": "patient",
        },
    )


def _login(client, email: str, password: str):
    return client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )


def _token_from_response(response) -> str:
    payload = response.json()
    data = payload.get("data", payload)
    return data["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_patient_journey_end_to_end(client, db_session):
    email = "integration.patient@example.com"
    password = "PatientPass123!"

    register_response = _register_patient(client, email=email, password=password)
    assert register_response.status_code in (200, 201), register_response.text

    login_response = _login(client, email=email, password=password)
    assert login_response.status_code == 200, login_response.text
    token = _token_from_response(login_response)
    headers = _auth_headers(token)

    me_response = client.get("/api/v1/users/me", headers=headers)
    assert me_response.status_code == 200, me_response.text

    draft_response = client.post(
        "/api/v1/intake/drafts",
        json={
            "preferred_contact_method": "email",
            "service_need_category": "mental_health",
            "emergency_contact_name": "Emergency Person",
            "emergency_contact_phone": "+256700111111",
            "consent_accepted": True,
        },
        headers=headers,
    )
    assert draft_response.status_code in (200, 201), draft_response.text
    draft_payload = draft_response.json()
    draft_data = draft_payload.get("data", draft_payload)
    intake_id = draft_data["id"]

    submit_response = client.post(f"/api/v1/intake/{intake_id}/submit", headers=headers)
    assert submit_response.status_code == 200, submit_response.text

    appointment_response = client.post(
        "/api/v1/appointments",
        json={
            "provider_id": 1,
            "service_type": "mental_health",
            "scheduled_start": "2026-05-01T10:00:00Z",
            "scheduled_end": "2026-05-01T11:00:00Z",
            "timezone": "Africa/Kampala",
            "reason": "Postpartum mental health support",
        },
        headers=headers,
    )
    assert appointment_response.status_code in (200, 201), appointment_response.text
    appointment_payload = appointment_response.json()
    appointment_data = appointment_payload.get("data", appointment_payload)
    appointment_id = appointment_data["id"]

    screening_response = client.post(
        "/api/v1/screenings/epds",
        json={
            "appointment_id": appointment_id,
            "answers": {
                "q1": 1, "q2": 1, "q3": 2, "q4": 1, "q5": 1,
                "q6": 1, "q7": 1, "q8": 1, "q9": 1, "q10": 0,
            },
        },
        headers=headers,
    )
    assert screening_response.status_code in (200, 201), screening_response.text

    list_response = client.get("/api/v1/appointments/me", headers=headers)
    assert list_response.status_code == 200, list_response.text
    payload = list_response.json()
    items = payload.get("data", payload)
    assert len(items) >= 1

    reminder_result = create_due_appointment_reminders(db_session, hours_ahead=24 * 365)
    assert reminder_result.created_notifications >= 1

    dispatch_result = dispatch_pending_notifications(db_session, limit=20)
    assert dispatch_result.attempted >= 1
```

---

## File 8 — `tests/integration/test_provider_journey.py`

```python
from __future__ import annotations

from scripts.seed_reference_data import seed_reference_data


def _login(client, email: str, password: str):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )


def _token_from_response(response) -> str:
    payload = response.json()
    data = payload.get("data", payload)
    return data["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_provider_journey_end_to_end(client, db_session):
    seed_reference_data(db_session, commit=True)

    login_response = _login(client, "provider@pbbf.local", "ChangeMe123!")
    assert login_response.status_code == 200, login_response.text
    token = _token_from_response(login_response)
    headers = _auth_headers(token)

    appointments_response = client.get("/api/v1/appointments/me", headers=headers)
    assert appointments_response.status_code == 200, appointments_response.text
    appointments_payload = appointments_response.json()
    appointments = appointments_payload.get("data", appointments_payload)
    assert len(appointments) >= 1
    appointment_id = appointments[0]["id"]

    session_response = client.post(
        f"/api/v1/telehealth/sessions/{appointment_id}/join",
        headers=headers,
    )
    assert session_response.status_code == 200, session_response.text

    encounter_create = client.post(
        "/api/v1/encounters",
        json={
            "appointment_id": appointment_id,
            "note_text": "Patient attended session. Initial assessment completed.",
            "follow_up_plan": "Follow up in 7 days.",
        },
        headers=headers,
    )
    assert encounter_create.status_code in (200, 201), encounter_create.text
    encounter_payload = encounter_create.json()
    encounter_data = encounter_payload.get("data", encounter_payload)
    encounter_id = encounter_data["id"]

    finalize_response = client.patch(
        f"/api/v1/encounters/{encounter_id}/finalize",
        json={"final_note_text": "Finalized postpartum consult note."},
        headers=headers,
    )
    assert finalize_response.status_code == 200, finalize_response.text

    referral_response = client.post(
        "/api/v1/referrals",
        json={
            "appointment_id": appointment_id,
            "encounter_id": encounter_id,
            "category": "community_support",
            "destination_name": "Community Wellness Partner",
            "notes": "Follow-up social support referral.",
        },
        headers=headers,
    )
    assert referral_response.status_code in (200, 201), referral_response.text

    screenings_response = client.get(
        "/api/v1/screenings/patient-history",
        params={"appointment_id": appointment_id},
        headers=headers,
    )
    assert screenings_response.status_code in (200, 201), screenings_response.text
```

---

## File 9 — `tests/integration/test_admin_journey.py`

```python
from __future__ import annotations

from scripts.seed_reference_data import seed_reference_data


def _login(client, email: str, password: str):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )


def _token_from_response(response) -> str:
    payload = response.json()
    data = payload.get("data", payload)
    return data["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_admin_journey_end_to_end(client, db_session):
    seed_reference_data(db_session, commit=True)

    login_response = _login(client, "admin@pbbf.local", "ChangeMe123!")
    assert login_response.status_code == 200, login_response.text
    token = _token_from_response(login_response)
    headers = _auth_headers(token)

    dashboard_response = client.get("/api/v1/admin/dashboard/summary", headers=headers)
    assert dashboard_response.status_code == 200, dashboard_response.text
    dashboard_payload = dashboard_response.json()
    dashboard_data = dashboard_payload.get("data", dashboard_payload)

    assert "users" in dashboard_data
    assert "appointments" in dashboard_data
    assert "referrals" in dashboard_data

    audit_response = client.get("/api/v1/audit/logs", headers=headers)
    assert audit_response.status_code == 200, audit_response.text

    notifications_response = client.get("/api/v1/notifications", headers=headers)
    assert notifications_response.status_code == 200, notifications_response.text

    referrals_response = client.get("/api/v1/referrals", headers=headers)
    assert referrals_response.status_code == 200, referrals_response.text


def test_seeded_data_boot_smoke(client, db_session):
    seed_reference_data(db_session, commit=True)

    login_response = _login(client, "admin@pbbf.local", "ChangeMe123!")
    assert login_response.status_code == 200, login_response.text

    provider_login = _login(client, "provider@pbbf.local", "ChangeMe123!")
    assert provider_login.status_code == 200, provider_login.text

    patient_login = _login(client, "patient@pbbf.local", "ChangeMe123!")
    assert patient_login.status_code == 200, patient_login.text
```

---

# Recommended supporting adjustments

These are not additional required files for this phase, but they help this phase run cleanly.

## 1. Ensure `app/jobs/` is a real package
Earlier you noted the odd path `app/jobs/{__init__.py}`. Make sure the filesystem is corrected to this:

```bash
mkdir -p app/jobs
touch app/jobs/__init__.py
```

If a file literally exists with braces in its path, fix it:

```bash
rm -f 'app/jobs/{__init__.py}'
touch app/jobs/__init__.py
```

## 2. Ensure your notification channel functions exist
The job code above expects these functions from Phase 8:

- `send_email_notification(notification)`
- `send_sms_notification(notification)`

If your existing `app/modules/notifications/channels.py` currently uses different function names, rename the imports in `app/jobs/notification_jobs.py` accordingly.

## 3. Make your test database predictable
Your existing `tests/conftest.py` should already expose at least:

- `client`
- `db_session`

If not, add those before running the integration suite.

---

# Commands to run for this phase

## 1. Seed baseline data

```bash
python -m scripts.seed_roles
python -m scripts.seed_users
python -m scripts.seed_reference_data
```

## 2. Run integration tests

```bash
pytest tests/integration/test_patient_journey.py -q
pytest tests/integration/test_provider_journey.py -q
pytest tests/integration/test_admin_journey.py -q
```

## 3. Run the full integration layer

```bash
pytest tests/integration -q
```

## 4. Optional direct smoke checks for jobs

```bash
python - <<'PY'
from app.jobs.reminder_jobs import run_reminder_generation_job
from app.jobs.notification_jobs import run_notification_dispatch_job

print(run_reminder_generation_job(hours_ahead=24))
print(run_notification_dispatch_job(limit=20))
PY
```

---

# Completion checklist for Phase 9

The phase is complete when all of the following are true:

- background-job package exists and imports cleanly
- demo roles and users seed idempotently
- reference data seeds without duplicate explosions
- patient integration journey passes
- provider integration journey passes
- admin integration journey passes
- reminder creation job produces queued notifications
- notification dispatch job updates queued notifications to sent or failed deterministically

---

# Final practical note

This phase is intentionally written to be **worker-ready but not worker-dependent**.  
That is the right level for now.

You do **not** need Celery, Redis queues, or deployment-time scheduler complexity yet just to prove:
- reminders can be generated
- notifications can be dispatched
- demo environments can be seeded
- multi-step workflows actually work end to end

Once this is stable, you can move to the next backend phase or start tightening frontend integration against these flows.
