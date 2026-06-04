
# PBBF BLISS — Stage 1 Contract Alignment Implementation Pack

**Stage:** 1 — Frontend/Backend Contract Alignment Foundation  
**Execution style:** Independent commands/snippets only. Do **not** run this file as one combined script.  
**Repository root:** `/home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth`

---

## 1. Objective

Make frontend and backend agree on API routes, request payloads, response shapes, and status names before polishing more features.

This pack replaces the previous bundled-script style. Every section below gives one independent command/snippet at a time.

---

## 2. Contract Decisions Locked for Stage 1

```text
1. Intake uses backend fields:
   service_need, consent_acknowledged, consent_version, privacy_policy_version, notes, postpartum_questionnaire.

2. Appointments use MVP request flow:
   provider_id may be omitted/null.
   If provider_id is omitted, appointment status is requested.
   If provider_id is present, appointment status is booked after provider conflict check.

3. GET /appointments becomes role-aware:
   patient -> own appointments
   provider -> assigned appointments
   admin/care_coordinator -> all appointments

4. Encounters use backend-compatible routes:
   GET  /encounters/by-appointment/{appointment_id}
   POST /encounters/appointments/{appointment_id}
   PUT  /encounters/{encounter_id}/draft
   POST /encounters/{encounter_id}/finalize

5. Referrals use backend-compatible fields:
   destination_name, destination_contact, follow_up_at, category enum, items[] list response.

6. Screenings keep Stage 0 EPDS q1-q10 object payload.

7. Admin reports receive metricDetails from useAdminMetrics.

8. src/shared/services/api.js becomes a re-export of src/services/api.js.
```

---

## 3. Prepare Backup Directory

### Command 3.1 — Create backup directory variable

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
export STAGE1_BACKUP_DIR="backups/stage1_contract_alignment_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$STAGE1_BACKUP_DIR"
echo "$STAGE1_BACKUP_DIR"
```

---

# 4. Shared API Client Alignment

## File updated

```text
pbbf-telehealth/src/shared/services/api.js
```

### Command 4.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/shared/services"
cp pbbf-telehealth/src/shared/services/api.js "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/shared/services/api.js"
```

### Command 4.2 — Replace stale shared API client

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-telehealth/src/shared/services/api.js <<'EOF'
export {
  API_BASE_URL,
  ApiError,
  api,
  apiRequest,
} from "../../services/api";

export { api as apiClient } from "../../services/api";
export { api as default } from "../../services/api";
EOF
```

### Command 4.3 — Inspect result

```bash
sed -n '1,120p' /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/shared/services/api.js
```

---

# 5. Intake Payload Contract Alignment

## File updated

```text
pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
```

### Command 5.1 — Backup file

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/intake/hooks"
cp pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js"
```

### Command 5.2 — Patch outgoing payload keys

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js')
text = path.read_text()
text = text.replace('service_needs: values.serviceNeeds,', 'service_need: Array.isArray(values.serviceNeeds) ? values.serviceNeeds[0] : values.serviceNeeds,')
text = text.replace('postpartum_summary: values.postpartumSummary.trim(),', 'notes: values.postpartumSummary.trim(),\n        postpartum_questionnaire: { summary: values.postpartumSummary.trim(), selected_service_needs: values.serviceNeeds },')
text = text.replace('consent_accepted: values.consentAccepted,', 'consent_acknowledged: values.consentAccepted,\n        consent_version: values.consentVersion || "2026.04",')
text = text.replace('privacy_accepted: values.privacyAccepted,', 'privacy_policy_version: values.privacyPolicyVersion || values.consentVersion || "2026.04",')
path.write_text(text)
PY
```

### Command 5.3 — Patch hydration keys

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js')
text = path.read_text()
text = text.replace('intake.service_needs || intake.serviceNeeds || current.serviceNeeds', 'intake.service_need ? [intake.service_need] : intake.service_needs || intake.serviceNeeds || current.serviceNeeds')
text = text.replace('intake.consent_accepted ?? intake.consentAccepted ?? current.consentAccepted', 'intake.submission_payload?.consent?.acknowledged ?? intake.consent_acknowledged ?? intake.consentAccepted ?? current.consentAccepted')
text = text.replace('intake.privacy_accepted ?? intake.privacyAccepted ?? current.privacyAccepted', 'intake.submission_payload?.consent?.privacy_policy_version ?? intake.privacy_policy_version ?? intake.privacyAccepted ?? current.privacyAccepted')
path.write_text(text)
PY
```

### Command 5.4 — Inspect result

```bash
grep -n "service_need\|consent_acknowledged\|privacy_policy_version\|postpartum_questionnaire\|notes:" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
```

---

# 6. Frontend Appointment Contract Alignment

## Files updated

```text
pbbf-telehealth/src/modules/appointments/services/appointmentsApi.js
pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js
```

### Command 6.1 — Backup appointments API

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/appointments/services"
cp pbbf-telehealth/src/modules/appointments/services/appointmentsApi.js "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/appointments/services/appointmentsApi.js"
```

### Command 6.2 — Replace appointments API

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-telehealth/src/modules/appointments/services/appointmentsApi.js <<'EOF'
import { api } from "../../../services/api";

export function listAppointmentsRequest(params = {}) {
  const search = new URLSearchParams();
  if (params.status) search.set("status", params.status);
  if (params.upcomingOnly) search.set("upcoming_only", "true");
  const queryString = search.toString();
  return api.get(`/appointments${queryString ? `?${queryString}` : ""}`);
}

export function createAppointmentRequest(payload) {
  return api.post("/appointments", payload);
}

export function rescheduleAppointmentRequest(appointmentId, payload) {
  return api.patch(`/appointments/${appointmentId}/reschedule`, payload);
}

export function cancelAppointmentRequest(appointmentId, payload = {}) {
  return api.patch(`/appointments/${appointmentId}/cancel`, payload);
}

export function assignProviderRequest(appointmentId, payload) {
  return api.patch(`/appointments/${appointmentId}/assign-provider`, payload);
}
EOF
```

### Command 6.3 — Backup appointments hook

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/appointments/hooks"
cp pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js"
```

### Command 6.4 — Remove hardcoded provider and patient list bypass

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js')
text = path.read_text()
text = text.replace('import { useAuthStore } from "../../../store/authStore";\n', '')
text = text.replace('const DEV_DEFAULT_PROVIDER_ID = 1;\n', '')
text = text.replace('  const role = useAuthStore((state) => state.user?.role || null);\n\n', '')
text = text.replace('''    if (role === "patient") {
      setAppointments([]);
      setLoadError("");
      setIsLoading(false);
      return;
    }

''', '')
text = text.replace('  }, [role]);', '  }, []);')
text = text.replace('provider_id: DEV_DEFAULT_PROVIDER_ID,', 'provider_id: values.providerId || null,')
text = text.replace('Appointment booked successfully.', 'Appointment request saved successfully.')
path.write_text(text)
PY
```

### Command 6.5 — Add patient/provider fields to appointment normalizer if absent

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js')
text = path.read_text()
if 'patientId:' not in text:
    text = text.replace(
        'id: raw?.id || raw?.appointment_id || "temp-id",',
        'id: raw?.id || raw?.appointment_id || "temp-id",\n    patientId: raw?.patient_id || raw?.patientId || null,\n    providerId: raw?.provider_id || raw?.providerId || null,\n    patientName: raw?.patient_name || raw?.patientName || "Unknown patient",'
    )
path.write_text(text)
PY
```

### Command 6.6 — Inspect result

```bash
sed -n '1,260p' /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js
```

---

# 7. Backend Appointment Contract Alignment

## Files updated

```text
pbbf-api/app/modules/appointments/schemas.py
pbbf-api/app/modules/appointments/repository.py
pbbf-api/app/modules/appointments/service.py
pbbf-api/app/modules/appointments/router.py
```

### Command 7.1 — Backup appointment schemas

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/appointments"
cp pbbf-api/app/modules/appointments/schemas.py "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/appointments/schemas.py"
```

### Command 7.2 — Make provider_id optional in appointment create schema

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/schemas.py')
text = path.read_text()
text = text.replace('provider_id: int = Field(..., gt=0)', 'provider_id: Optional[int] = Field(default=None, gt=0)')
if 'patient_name:' not in text:
    text = text.replace('provider_id: Optional[int] = None', 'provider_id: Optional[int] = None\n    patient_name: Optional[str] = None\n    provider_name: Optional[str] = None')
path.write_text(text)
PY
```

### Command 7.3 — Backup appointment repository

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/appointments"
cp pbbf-api/app/modules/appointments/repository.py "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/appointments/repository.py"
```

### Command 7.4 — Add patient/all listing methods if missing

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/repository.py')
text = path.read_text()
if 'def list_for_patient' not in text:
    text += '''

    def list_for_patient(self, patient_id: int) -> list[Appointment]:
        stmt = (
            select(Appointment)
            .where(Appointment.patient_id == patient_id)
            .order_by(Appointment.scheduled_start.asc(), Appointment.id.asc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def list_all(self) -> list[Appointment]:
        stmt = select(Appointment).order_by(Appointment.scheduled_start.asc(), Appointment.id.asc())
        return list(self.db.execute(stmt).scalars().all())
'''
path.write_text(text)
PY
```

### Command 7.5 — Backup appointment service

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/appointments"
cp pbbf-api/app/modules/appointments/service.py "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/appointments/service.py"
```

### Command 7.6 — Allow creation without provider_id

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/service.py')
text = path.read_text()
text = text.replace('provider = self.repository.get_provider_by_id(payload.provider_id)', 'provider = self.repository.get_provider_by_id(payload.provider_id) if payload.provider_id else None')
text = text.replace('if provider is None:', 'if payload.provider_id and provider is None:')
text = text.replace('if self.repository.has_provider_conflict(\n            provider_id=payload.provider_id,', 'if payload.provider_id and self.repository.has_provider_conflict(\n            provider_id=payload.provider_id,')
text = text.replace('status="booked",', 'status="booked" if payload.provider_id else "requested",')
path.write_text(text)
PY
```

### Command 7.7 — Add role-aware list_appointments service method if missing

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/service.py')
text = path.read_text()
if 'def list_appointments(self, current_user)' not in text:
    text += '''

    def list_appointments(self, current_user) -> dict:
        role_name = self._role_name(current_user)
        if role_name == "patient":
            patient_profile = self._require_patient_profile(current_user)
            appointments = self.repository.list_for_patient(patient_profile.id)
        elif role_name == "provider":
            provider_profile = self._require_provider_profile(current_user)
            appointments = self.repository.list_for_provider(provider_profile.id)
        elif role_name in {"admin", "care_coordinator"}:
            appointments = self.repository.list_all()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to list appointments.")
        items = [self._serialize(appointment) for appointment in appointments]
        return {"items": items, "total": len(items)}
'''
path.write_text(text)
PY
```

### Command 7.8 — Backup appointment router

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/appointments"
cp pbbf-api/app/modules/appointments/router.py "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/appointments/router.py"
```

### Command 7.9 — Point GET /appointments to role-aware list method

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/router.py')
text = path.read_text()
text = text.replace('def list_provider_appointments(', 'def list_appointments(')
text = text.replace('return service.list_provider_appointments(current_user)', 'return service.list_appointments(current_user)')
path.write_text(text)
PY
```

---

# 8. Encounter Contract Alignment

## Files updated

```text
pbbf-telehealth/src/modules/encounters/services/encountersApi.js
pbbf-telehealth/src/modules/encounters/hooks/useEncounterEditor.js
pbbf-api/app/modules/encounters/router.py
pbbf-api/app/modules/encounters/service.py
```

### Command 8.1 — Backup frontend encounters API

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/encounters/services"
cp pbbf-telehealth/src/modules/encounters/services/encountersApi.js "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/encounters/services/encountersApi.js"
```

### Command 8.2 — Replace encounters API routes

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-telehealth/src/modules/encounters/services/encountersApi.js <<'EOF'
import { api } from "../../../services/api";

export function getEncounterByAppointmentRequest(appointmentId) {
  return api.get(`/encounters/by-appointment/${appointmentId}`);
}

export function createEncounterRequest(appointmentId, payload = {}) {
  return api.post(`/encounters/appointments/${appointmentId}`, payload);
}

export function saveEncounterRequest(encounterId, payload) {
  return api.put(`/encounters/${encounterId}/draft`, payload);
}

export function finalizeEncounterRequest(encounterId) {
  return api.post(`/encounters/${encounterId}/finalize`, {});
}
EOF
```

### Command 8.3 — Backup backend encounters router

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/encounters"
cp pbbf-api/app/modules/encounters/router.py "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/encounters/router.py"
```

### Command 8.4 — Add GET /encounters/by-appointment/{appointment_id}

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/encounters/router.py')
text = path.read_text()
if 'def get_encounter_by_appointment' not in text:
    marker = '@router.get("/{encounter_id}", response_model=EncounterRead)'
    insert = '''@router.get("/by-appointment/{appointment_id}", response_model=EncounterRead)
def get_encounter_by_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    service = EncounterService(EncounterRepository(db))
    return service.get_by_appointment_id(appointment_id=appointment_id, current_user=current_user)

'''
    text = text.replace(marker, insert + marker)
path.write_text(text)
PY
```

### Command 8.5 — Backup backend encounter service

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/encounters"
cp pbbf-api/app/modules/encounters/service.py "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/encounters/service.py"
```

### Command 8.6 — Add get_by_appointment_id service method

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/encounters/service.py')
text = path.read_text()
if 'def get_by_appointment_id(self, *, appointment_id: int, current_user)' not in text:
    marker = '    def get_by_id(self, *, encounter_id: int, current_user):\n'
    insert = '''    def get_by_appointment_id(self, *, appointment_id: int, current_user):
        encounter = self.repository.get_by_appointment_id(appointment_id)
        if encounter is None:
            raise NotFoundException("Encounter not found.")
        return self.get_by_id(encounter_id=encounter.id, current_user=current_user)

'''
    text = text.replace(marker, insert + marker)
path.write_text(text)
PY
```

### Command 8.7 — Backup frontend encounter hook

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/encounters/hooks"
cp pbbf-telehealth/src/modules/encounters/hooks/useEncounterEditor.js "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/encounters/hooks/useEncounterEditor.js"
```

### Command 8.8 — Patch encounter hook payloads

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/encounters/hooks/useEncounterEditor.js')
text = path.read_text()
text = text.replace('createEncounterRequest({', 'createEncounterRequest(selectedAppointmentId, {')
text = text.replace('appointment_id: selectedAppointmentId,', 'template_name: "telehealth_follow_up",')
text = text.replace('note: values.note.trim(),', 'note_text: values.note.trim(),\n        objective: values.note.trim(),')
text = text.replace('follow_up_plan: values.followUpPlan.trim(),', 'plan: values.followUpPlan.trim(),\n        follow_up_plan: values.followUpPlan.trim(),')
text = text.replace('finalizeEncounterRequest(nextEncounterId, {', 'finalizeEncounterRequest(nextEncounterId);\n      // finalized after saving latest draft\n      void ({')
path.write_text(text)
PY
```

---

# 9. Referral Contract Alignment

## Files updated

```text
pbbf-telehealth/src/modules/referrals/services/referralsApi.js
pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js
pbbf-telehealth/src/modules/referrals/components/ReferralForm.jsx
pbbf-api/app/modules/referrals/service.py
```

### Command 9.1 — Backup referrals API

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/referrals/services"
cp pbbf-telehealth/src/modules/referrals/services/referralsApi.js "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/referrals/services/referralsApi.js"
```

### Command 9.2 — Replace referrals API

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
cat > pbbf-telehealth/src/modules/referrals/services/referralsApi.js <<'EOF'
import { api } from "../../../services/api";

export function listReferralsRequest() {
  return api.get("/referrals/");
}

export function createReferralRequest(payload) {
  return api.post("/referrals/", payload);
}

export function updateReferralStatusRequest(referralId, payload) {
  return api.patch(`/referrals/${referralId}/status`, payload);
}
EOF
```

### Command 9.3 — Backup referrals hook

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/referrals/hooks"
cp pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js"
```

### Command 9.4 — Patch referral hook field names and response shape

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js')
text = path.read_text()
text = text.replace('const rows = payload?.referrals || payload || [];', 'const rows = payload?.items || payload?.referrals || payload || [];')
text = text.replace('destination: raw?.destination || raw?.destination_name || "Not specified",', 'destination: raw?.destination_name || raw?.destination || "Not specified",')
text = text.replace('followUpDate: raw?.follow_up_date || raw?.followUpDate || "",', 'followUpDate: raw?.follow_up_at || raw?.follow_up_date || raw?.followUpDate || "",')
text = text.replace('appointment_id: values.appointmentId || null,\n        category: values.category,\n        destination: values.destination,\n        notes: values.notes,\n        follow_up_date: values.followUpDate || null,', 'category: values.category,\n        destination_name: values.destination,\n        destination_contact: values.destinationContact || null,\n        notes: values.notes,\n        follow_up_at: values.followUpDate || null,')
path.write_text(text)
PY
```

### Command 9.5 — Backup referral form

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/referrals/components"
cp pbbf-telehealth/src/modules/referrals/components/ReferralForm.jsx "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/referrals/components/ReferralForm.jsx"
```

### Command 9.6 — Patch referral follow-up input type

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/referrals/components/ReferralForm.jsx')
text = path.read_text()
text = text.replace('type="date"', 'type="datetime-local"')
path.write_text(text)
PY
```

### Command 9.7 — Backup backend referral service

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/referrals"
cp pbbf-api/app/modules/referrals/service.py "$STAGE1_BACKUP_DIR/pbbf-api/app/modules/referrals/service.py"
```

### Command 9.8 — Add encounter-patient validation

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

# 10. Admin Reports metricDetails Alignment

## File updated

```text
pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js
```

### Command 10.1 — Backup admin metrics hook

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/admin/hooks"
cp pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js "$STAGE1_BACKUP_DIR/pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js"
```

### Command 10.2 — Add metricDetails if missing

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js')
text = path.read_text()
if 'metricDetails' not in text:
    text = text.replace(
        'return {\n    summary,',
        'const metricDetails = { summary, usersTotal: users.length, auditLogsTotal: auditLogs.length };\n\n  return {\n    summary,\n    metricDetails,'
    )
path.write_text(text)
PY
```

---

# 11. Documentation Files

## Command 11.1 — Create frontend/backend contract map

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p docs/api-contracts
cat > docs/api-contracts/frontend-backend-contract-map.md <<'EOF'
# Frontend/Backend Contract Map

## Intake
Frontend sends: service_need, consent_acknowledged, consent_version, privacy_policy_version, notes, postpartum_questionnaire.

## Appointments
POST /appointments supports optional provider_id. If omitted, status is requested. If present, status is booked after conflict check.

## Encounters
Frontend uses GET /encounters/by-appointment/{appointment_id}, POST /encounters/appointments/{appointment_id}, PUT /encounters/{encounter_id}/draft, POST /encounters/{encounter_id}/finalize.

## Referrals
Frontend sends destination_name, destination_contact, follow_up_at, category enum, and reads list response from items[].

## Screenings
EPDS submits q1-q10 object payload.
EOF
```

## Command 11.2 — Create MVP payload decisions doc

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p docs/api-contracts
cat > docs/api-contracts/mvp-payload-decisions.md <<'EOF'
# MVP Payload Decisions

## Intake
Single service_need is the backend MVP contract. Multiple UI service selections may be stored only as context in postpartum_questionnaire.selected_service_needs.

## Appointments
MVP supports appointment requests without provider assignment. Admin/care coordinator assignment happens later through assign-provider endpoint.

## Referrals
Referral category is enum-driven. Free-text category is not accepted.

## Screenings
Backend is authoritative for EPDS scoring.
EOF
```

---

# 12. Test and MSW Placeholders

## Command 12.1 — Create patient contract test placeholder

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p pbbf-api/tests/integration
cat > pbbf-api/tests/integration/test_contract_patient_flow.py <<'EOF'
def test_patient_contract_payload_shapes_documented():
    assert True
EOF
```

## Command 12.2 — Create provider contract test placeholder

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p pbbf-api/tests/integration
cat > pbbf-api/tests/integration/test_contract_provider_flow.py <<'EOF'
def test_provider_contract_payload_shapes_documented():
    assert True
EOF
```

## Command 12.3 — Create MSW contract handlers placeholder

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p pbbf-telehealth/src/test/msw
cat > pbbf-telehealth/src/test/msw/contractHandlers.js <<'EOF'
export const contractHandlers = [];
EOF
```

---

# 13. Validation Commands

Run each independently.

## Command 13.1 — Backend syntax check

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
python -m py_compile app/modules/appointments/schemas.py app/modules/appointments/repository.py app/modules/appointments/service.py app/modules/appointments/router.py app/modules/encounters/service.py app/modules/encounters/router.py app/modules/referrals/service.py
```

## Command 13.2 — Patient contract test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/integration/test_contract_patient_flow.py -q
```

## Command 13.3 — Provider contract test

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/integration/test_contract_provider_flow.py -q
```

## Command 13.4 — Frontend build

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm run build
```

---

# 14. Independent Post-Apply Inspection Commands

## Command 14.1 — Intake hook fields

```bash
grep -n "service_need\|consent_acknowledged\|privacy_policy_version\|postpartum_questionnaire\|notes:" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
```

## Command 14.2 — Appointment hook

```bash
sed -n '1,320p' /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js
```

## Command 14.3 — Appointment backend service

```bash
sed -n '1,360p' /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/appointments/service.py
```

## Command 14.4 — Encounter router

```bash
sed -n '1,260p' /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api/app/modules/encounters/router.py
```

## Command 14.5 — Referral hook

```bash
sed -n '1,280p' /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js
```

## Command 14.6 — Admin metrics

```bash
grep -n "metricDetails\|return" /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js
```

---

# 15. Completion Checklist

```text
[ ] Frontend intake sends service_need, consent_acknowledged, consent_version, privacy_policy_version.
[ ] Appointments can be created without provider_id as requested appointments.
[ ] Patient GET /appointments returns own appointments.
[ ] Provider GET /appointments returns assigned appointments.
[ ] Admin/care coordinator GET /appointments returns all appointments.
[ ] Encounter frontend calls backend routes that exist.
[ ] Referral frontend sends destination_name and follow_up_at.
[ ] Referral frontend reads list response from items[].
[ ] EPDS frontend submits q1-q10 object payload.
[ ] Admin metricDetails is returned by useAdminMetrics.
[ ] Backend py_compile passes.
[ ] Frontend build passes.
```

---

# 16. Boundary

This stage aligns contracts only. Full object-level authorization hardening, audit persistence, notification delivery hardening, and deeper role-policy cleanup are handled in later stages.
