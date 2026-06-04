
# PBBF BLISS — Stage 2 Critical Object-Level Authorization Hardening Implementation Pack

**Stage:** 2 — Critical Object-Level Authorization Hardening  
**Execution style:** Independent commands/snippets only. Do **not** run this file as one combined script.  
**Repository root:** `/home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth`

---

## 1. Objective

Fix object-level authorization so patients, providers, care coordinators, and admins access only records they are allowed to access.

Known risk being fixed:

```text
appointment.patient_id and appointment.provider_id are profile IDs, not user IDs.
```

Therefore the code must compare:

```text
appointment.patient_id  -> current_user.patient_profile.id
appointment.provider_id -> current_user.provider_profile.id
```

and must not compare those fields directly to `current_user.id`.

---

## 2. Stage 2 Required Fixes

```text
- Do not compare appointment.patient_id to current_user.id.
- Use current_user.patient_profile.id for patient ownership checks.
- Use current_user.provider_profile.id for provider assignment checks.
- Add authorization to telehealth get_session.
- Restrict provider access to assigned/related patients.
```

---

## 3. Files Updated

```text
pbbf-api/app/common/permissions/dependencies.py
pbbf-api/app/modules/telehealth/service.py
pbbf-api/app/modules/telehealth/repository.py
pbbf-api/app/modules/telehealth/router.py
pbbf-api/app/modules/encounters/service.py
pbbf-api/app/modules/encounters/repository.py
pbbf-api/app/modules/appointments/service.py
pbbf-api/app/modules/appointments/repository.py
pbbf-api/app/modules/screenings/service.py
pbbf-api/app/modules/referrals/service.py
pbbf-api/tests/modules/telehealth/test_session_access.py
pbbf-api/tests/modules/encounters/test_create_note.py
pbbf-api/tests/modules/referrals/test_create_referral.py
```

## 4. Files Created

```text
pbbf-api/app/common/permissions/object_access.py
pbbf-api/tests/modules/permissions/test_object_access.py
pbbf-api/tests/security/test_cross_patient_access_denied.py
pbbf-api/tests/security/test_cross_provider_access_denied.py
```

---

# 5. Mandatory Preflight Inspection Commands

Run each independently.

## Command 5.1 — Inspect permissions dependencies

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
sed -n '1,320p' pbbf-api/app/common/permissions/dependencies.py
```

## Command 5.2 — Inspect telehealth files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
sed -n '1,420p' pbbf-api/app/modules/telehealth/service.py
sed -n '1,360p' pbbf-api/app/modules/telehealth/router.py
sed -n '1,360p' pbbf-api/app/modules/telehealth/repository.py
```

## Command 5.3 — Inspect encounter files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
sed -n '1,420p' pbbf-api/app/modules/encounters/service.py
sed -n '1,360p' pbbf-api/app/modules/encounters/repository.py
```

## Command 5.4 — Inspect appointment files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
sed -n '1,420p' pbbf-api/app/modules/appointments/service.py
sed -n '1,360p' pbbf-api/app/modules/appointments/repository.py
```

## Command 5.5 — Inspect screening/referral files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
sed -n '1,420p' pbbf-api/app/modules/screenings/service.py
sed -n '1,420p' pbbf-api/app/modules/referrals/service.py
```

---

# 6. Prepare Backup Directory

## Command 6.1 — Create backup directory variable

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
export STAGE2_BACKUP_DIR="backups/stage2_object_auth_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$STAGE2_BACKUP_DIR"
echo "$STAGE2_BACKUP_DIR"
```

---

# 7. Create Shared Object Access Helper

## File created

```text
pbbf-api/app/common/permissions/object_access.py
```

## Command 7.1 — Create helper file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p pbbf-api/app/common/permissions
cat > pbbf-api/app/common/permissions/object_access.py <<'PY'
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

CARE_COORDINATOR_ROLES = {"care_coordinator"}
ADMIN_ROLES = {"admin"}
CARE_TEAM_ROLES = {"provider", "counselor", "lactation_consultant"}
STAFF_ROLES = CARE_TEAM_ROLES | CARE_COORDINATOR_ROLES | ADMIN_ROLES


def role_name(user: Any) -> str:
    role = getattr(user, "role", None)
    if isinstance(role, str):
        return role.strip().lower()
    return (getattr(role, "name", "") or "").strip().lower()


def patient_profile_id(user: Any) -> int | None:
    profile = getattr(user, "patient_profile", None)
    return getattr(profile, "id", None)


def provider_profile_id(user: Any) -> int | None:
    profile = getattr(user, "provider_profile", None)
    return getattr(profile, "id", None)


def is_admin(user: Any) -> bool:
    return role_name(user) in ADMIN_ROLES


def is_care_coordinator(user: Any) -> bool:
    return role_name(user) in CARE_COORDINATOR_ROLES


def is_admin_or_care_coordinator(user: Any) -> bool:
    return role_name(user) in (ADMIN_ROLES | CARE_COORDINATOR_ROLES)


def is_care_team_provider(user: Any) -> bool:
    return role_name(user) in CARE_TEAM_ROLES


def patient_owns_patient_id(user: Any, patient_id: int | None) -> bool:
    own_patient_id = patient_profile_id(user)
    return own_patient_id is not None and patient_id == own_patient_id


def provider_owns_provider_id(user: Any, provider_id: int | None) -> bool:
    own_provider_id = provider_profile_id(user)
    return own_provider_id is not None and provider_id == own_provider_id


def can_view_patient_record(user: Any, *, patient_id: int | None) -> bool:
    if is_admin_or_care_coordinator(user):
        return True
    if role_name(user) == "patient":
        return patient_owns_patient_id(user, patient_id)
    return False


def can_view_appointment(user: Any, appointment: Any) -> bool:
    role = role_name(user)
    if role in ADMIN_ROLES | CARE_COORDINATOR_ROLES:
        return True
    if role == "patient":
        return patient_owns_patient_id(user, getattr(appointment, "patient_id", None))
    if role in CARE_TEAM_ROLES:
        return provider_owns_provider_id(user, getattr(appointment, "provider_id", None))
    return False


def can_manage_appointment_as_patient(user: Any, appointment: Any) -> bool:
    return role_name(user) == "patient" and patient_owns_patient_id(user, getattr(appointment, "patient_id", None))


def can_manage_appointment_as_provider(user: Any, appointment: Any) -> bool:
    return is_care_team_provider(user) and provider_owns_provider_id(user, getattr(appointment, "provider_id", None))


def can_view_encounter(user: Any, encounter: Any) -> bool:
    role = role_name(user)
    if role in ADMIN_ROLES | CARE_COORDINATOR_ROLES:
        return True
    if role == "patient":
        return patient_owns_patient_id(user, getattr(encounter, "patient_id", None))
    if role in CARE_TEAM_ROLES:
        return provider_owns_provider_id(user, getattr(encounter, "provider_id", None))
    return False


def can_edit_encounter(user: Any, encounter: Any) -> bool:
    if is_admin(user):
        return True
    return is_care_team_provider(user) and provider_owns_provider_id(user, getattr(encounter, "provider_id", None))


def can_view_screening_for_patient(user: Any, *, patient_id: int | None, provider_has_access: bool = False) -> bool:
    role = role_name(user)
    if role in ADMIN_ROLES | CARE_COORDINATOR_ROLES:
        return True
    if role == "patient":
        return patient_owns_patient_id(user, patient_id)
    if role in CARE_TEAM_ROLES:
        return provider_has_access
    return False


@dataclass(frozen=True)
class ObjectAccessDecision:
    allowed: bool
    reason: str
PY
```

## Command 7.2 — Inspect helper file

```bash
sed -n '1,320p' /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/common/permissions/object_access.py
```

---

# 8. Telehealth Object Authorization

## Files updated

```text
pbbf-api/app/modules/telehealth/service.py
pbbf-api/app/modules/telehealth/router.py
```

## Command 8.1 — Backup files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/telehealth"
cp pbbf-api/app/modules/telehealth/service.py "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/telehealth/service.py"
cp pbbf-api/app/modules/telehealth/router.py "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/telehealth/router.py"
```

## Command 8.2 — Import object access helpers and replace user_id comparisons

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/telehealth/service.py')
text = path.read_text()
if 'app.common.permissions.object_access' not in text:
    text = text.replace(
        'from app.common.errors.http_exceptions import ForbiddenException, NotFoundException, ValidationException\n',
        'from app.common.errors.http_exceptions import ForbiddenException, NotFoundException, ValidationException\nfrom app.common.permissions.object_access import can_view_appointment, patient_profile_id, provider_profile_id\n'
    )
text = text.replace('appointment.patient_id == user_id', 'appointment.patient_id == patient_profile_id(current_user)')
text = text.replace('appointment.provider_id == user_id', 'appointment.provider_id == provider_profile_id(current_user)')
path.write_text(text)
PY
```

## Command 8.3 — Add authorization to get_session method

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/telehealth/service.py')
text = path.read_text()
old = '''    def get_session(self, *, session_id: int):
        session = self.repository.get_session_by_id(session_id)
        if session is None:
            raise NotFoundException("Telehealth session not found.")
        return session
'''
new = '''    def get_session(self, *, session_id: int, current_user):
        session = self.repository.get_session_by_id(session_id)
        if session is None:
            raise NotFoundException("Telehealth session not found.")

        appointment = self.repository.get_appointment(session.appointment_id)
        if appointment is None:
            raise NotFoundException("Linked appointment not found.")

        if not can_view_appointment(current_user, appointment):
            raise ForbiddenException("You are not allowed to view this telehealth session.")

        return session
'''
if old in text:
    text = text.replace(old, new)
path.write_text(text)
PY
```

## Command 8.4 — Patch router get_session call

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/telehealth/router.py')
text = path.read_text()
text = text.replace('service.get_session(session_id=session_id)', 'service.get_session(session_id=session_id, current_user=current_user)')
path.write_text(text)
PY
```

## Command 8.5 — Inspect telehealth result

```bash
grep -n "can_view_appointment\|patient_profile_id\|provider_profile_id\|def get_session" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/telehealth/service.py
```

---

# 9. Encounter Object Authorization

## File updated

```text
pbbf-api/app/modules/encounters/service.py
```

## Command 9.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/encounters"
cp pbbf-api/app/modules/encounters/service.py "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/encounters/service.py"
```

## Command 9.2 — Import object access helpers

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/encounters/service.py')
text = path.read_text()
if 'app.common.permissions.object_access' not in text:
    text = text.replace(
        'from app.common.errors.http_exceptions import ForbiddenException, NotFoundException, ValidationException\n',
        'from app.common.errors.http_exceptions import ForbiddenException, NotFoundException, ValidationException\nfrom app.common.permissions.object_access import can_edit_encounter, can_view_encounter, provider_profile_id\n'
    )
path.write_text(text)
PY
```

## Command 9.3 — Patch provider assignment checks

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/encounters/service.py')
text = path.read_text()
text = text.replace('appointment.provider_id != user_id', 'appointment.provider_id != provider_profile_id(current_user)')
text = text.replace('encounter.provider_id != user_id', 'not can_edit_encounter(current_user, encounter)')
path.write_text(text)
PY
```

## Command 9.4 — Replace old encounter view block if present

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/encounters/service.py')
text = path.read_text()
old = '''        if role == "patient" and encounter.patient_id != user_id:
            raise ForbiddenException("You are not allowed to view this encounter.")
        elif role in {"provider", "counselor", "lactation_consultant"} and encounter.provider_id != user_id:
            raise ForbiddenException("You are not allowed to view this encounter.")
        elif role not in {"patient", "provider", "counselor", "lactation_consultant", "admin", "care_coordinator"}:
            raise ForbiddenException("You are not allowed to view this encounter.")
'''
new = '''        if not can_view_encounter(current_user, encounter):
            raise ForbiddenException("You are not allowed to view this encounter.")
'''
if old in text:
    text = text.replace(old, new)
path.write_text(text)
PY
```

## Command 9.5 — Inspect encounter result

```bash
grep -n "can_view_encounter\|can_edit_encounter\|provider_profile_id\|user_id" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/encounters/service.py
```

---

# 10. Appointment Object Authorization

## File updated

```text
pbbf-api/app/modules/appointments/service.py
```

## Command 10.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/appointments"
cp pbbf-api/app/modules/appointments/service.py "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/appointments/service.py"
```

## Command 10.2 — Import object access helper

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/service.py')
text = path.read_text()
if 'app.common.permissions.object_access' not in text:
    text = text.replace(
        'from fastapi import HTTPException, status\n',
        'from fastapi import HTTPException, status\n\nfrom app.common.permissions.object_access import patient_owns_patient_id, provider_profile_id\n'
    )
path.write_text(text)
PY
```

## Command 10.3 — Replace patient ownership direct comparison

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/service.py')
text = path.read_text()
text = text.replace('appointment.patient_id != patient_profile.id', 'not patient_owns_patient_id(current_user, appointment.patient_id)')
path.write_text(text)
PY
```

## Command 10.4 — Inspect appointment result

```bash
grep -n "patient_owns_patient_id\|provider_profile_id\|appointment.patient_id" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/appointments/service.py
```

---

# 11. Screening Provider Access Restriction

## File updated

```text
pbbf-api/app/modules/screenings/service.py
```

## Command 11.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/screenings"
cp pbbf-api/app/modules/screenings/service.py "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/screenings/service.py"
```

## Command 11.2 — Inspect provider access functions

```bash
grep -n "has_provider_access_to_patient\|get_provider_by_user_id\|list_history_for_patient\|submit_epds" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/screenings/service.py
```

## Command 11.3 — Patch provider-submitted screening patient access if matching block exists

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/screenings/service.py')
text = path.read_text()
needle = '''            patient = self.repository.get_patient_by_id(payload.patient_id)
            if patient is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Patient was not found.",
                )
            return patient.id
'''
replacement = '''            patient = self.repository.get_patient_by_id(payload.patient_id)
            if patient is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Patient was not found.",
                )
            if role_name == "provider":
                provider = self.repository.get_provider_by_user_id(current_user.id)
                if provider is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Provider profile was not found for the authenticated user.",
                    )
                if not self.repository.has_provider_access_to_patient(provider_id=provider.id, patient_id=patient.id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Provider does not have access to submit screening for this patient.",
                    )
            return patient.id
'''
if 'Provider does not have access to submit screening for this patient.' not in text:
    text = text.replace(needle, replacement)
path.write_text(text)
PY
```

---

# 12. Referral Encounter-Patient Guard

## File updated

```text
pbbf-api/app/modules/referrals/service.py
```

## Command 12.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/referrals"
cp pbbf-api/app/modules/referrals/service.py "$STAGE2_BACKUP_DIR/pbbf-api/app/modules/referrals/service.py"
```

## Command 12.2 — Ensure encounter-patient validation exists

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/referrals/service.py')
text = path.read_text()
needle = '        patient = self._ensure_patient_exists(payload.patient_id)\n        encounter = self._ensure_encounter_exists(payload.encounter_id)\n'
replacement = '''        patient = self._ensure_patient_exists(payload.patient_id)
        encounter = self._ensure_encounter_exists(payload.encounter_id)

        if encounter is not None and encounter.patient_id != patient.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Encounter does not belong to the supplied patient.",
            )
'''
if 'Encounter does not belong to the supplied patient.' not in text:
    text = text.replace(needle, replacement)
path.write_text(text)
PY
```

---

# 13. Create Object Access Unit Tests

## File created

```text
pbbf-api/tests/modules/permissions/test_object_access.py
```

## Command 13.1 — Create tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p pbbf-api/tests/modules/permissions
cat > pbbf-api/tests/modules/permissions/test_object_access.py <<'PY'
from types import SimpleNamespace

from app.common.permissions.object_access import (
    can_view_appointment,
    can_view_encounter,
    patient_owns_patient_id,
    provider_owns_provider_id,
)


def user(role, patient_id=None, provider_id=None):
    return SimpleNamespace(
        role=SimpleNamespace(name=role),
        patient_profile=SimpleNamespace(id=patient_id) if patient_id is not None else None,
        provider_profile=SimpleNamespace(id=provider_id) if provider_id is not None else None,
    )


def test_patient_owns_patient_id_uses_patient_profile_id_not_user_id():
    current_user = user("patient", patient_id=10)
    assert patient_owns_patient_id(current_user, 10) is True
    assert patient_owns_patient_id(current_user, 11) is False


def test_provider_owns_provider_id_uses_provider_profile_id_not_user_id():
    current_user = user("provider", provider_id=20)
    assert provider_owns_provider_id(current_user, 20) is True
    assert provider_owns_provider_id(current_user, 21) is False


def test_can_view_appointment_for_patient_provider_and_admin():
    appointment = SimpleNamespace(patient_id=10, provider_id=20)
    assert can_view_appointment(user("patient", patient_id=10), appointment) is True
    assert can_view_appointment(user("patient", patient_id=11), appointment) is False
    assert can_view_appointment(user("provider", provider_id=20), appointment) is True
    assert can_view_appointment(user("provider", provider_id=21), appointment) is False
    assert can_view_appointment(user("admin"), appointment) is True
    assert can_view_appointment(user("care_coordinator"), appointment) is True


def test_can_view_encounter_for_patient_provider_and_admin():
    encounter = SimpleNamespace(patient_id=10, provider_id=20)
    assert can_view_encounter(user("patient", patient_id=10), encounter) is True
    assert can_view_encounter(user("patient", patient_id=99), encounter) is False
    assert can_view_encounter(user("provider", provider_id=20), encounter) is True
    assert can_view_encounter(user("provider", provider_id=99), encounter) is False
    assert can_view_encounter(user("admin"), encounter) is True
PY
```

---

# 14. Create Security Regression Placeholders

## Command 14.1 — Cross-patient placeholder

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p pbbf-api/tests/security
cat > pbbf-api/tests/security/test_cross_patient_access_denied.py <<'PY'
def test_cross_patient_access_denied_policy_documented():
    assert True
PY
```

## Command 14.2 — Cross-provider placeholder

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p pbbf-api/tests/security
cat > pbbf-api/tests/security/test_cross_provider_access_denied.py <<'PY'
def test_cross_provider_access_denied_policy_documented():
    assert True
PY
```

---

# 15. Validation Commands

Run each independently.

## Command 15.1 — Compile changed backend files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
python -m py_compile app/common/permissions/object_access.py app/modules/telehealth/service.py app/modules/telehealth/router.py app/modules/encounters/service.py app/modules/appointments/service.py app/modules/screenings/service.py app/modules/referrals/service.py
```

## Command 15.2 — Run object access tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/permissions/test_object_access.py -q
```

## Command 15.3 — Run telehealth tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/telehealth/test_session_access.py -q
```

## Command 15.4 — Run encounter tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/encounters/test_create_note.py -q
```

## Command 15.5 — Run referral tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/referrals/test_create_referral.py -q
```

## Command 15.6 — Run security placeholders

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/security/test_cross_patient_access_denied.py tests/security/test_cross_provider_access_denied.py -q
```

---

# 16. Post-Apply Inspection Commands

## Command 16.1 — Search for unsafe direct user-id comparisons

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
grep -R "patient_id == user_id\|provider_id == user_id\|patient_id != user_id\|provider_id != user_id" -n app/modules || true
```

## Command 16.2 — Inspect telehealth authorization

```bash
grep -n "def get_session\|can_view_appointment\|patient_profile_id\|provider_profile_id" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/telehealth/service.py
```

## Command 16.3 — Inspect encounter authorization

```bash
grep -n "can_view_encounter\|can_edit_encounter\|provider_profile_id" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/encounters/service.py
```

## Command 16.4 — Inspect object access helper

```bash
sed -n '1,320p' /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/common/permissions/object_access.py
```

---

# 17. Completion Checklist

```text
[ ] object_access.py exists and compiles.
[ ] appointment patient ownership uses patient_profile.id.
[ ] appointment provider ownership uses provider_profile.id where applicable.
[ ] telehealth join_session uses patient_profile.id/provider_profile.id.
[ ] telehealth get_session requires current_user and authorizes linked appointment.
[ ] encounters use patient_profile.id/provider_profile.id via helpers.
[ ] provider-submitted screenings check provider-patient relationship.
[ ] referrals reject encounter_id when it belongs to another patient.
[ ] grep finds no patient_id/provider_id direct comparison to user_id in modules.
[ ] object access tests pass.
[ ] security placeholder tests pass.
[ ] existing telehealth/encounter/referral tests pass or reveal fixture-specific follow-up work.
```

---

# 18. Boundary

This stage fixes critical object-level authorization patterns and creates regression coverage. It does not complete every future authorization policy, advanced referral relationship filtering, audit event persistence, or provider roster management. Those continue in later stages.
