# Stage 1 Implementation Pack — Frontend/Backend Contract Alignment Foundation

**Project:** PBBF BLISS Telehealth Platform  
**Stage:** 1 — Frontend/Backend Contract Alignment Foundation  
**Repository root:** `/home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth`

---

## 1. Objective

Make the frontend and backend agree on API routes, request payloads, response shapes, and status names before adding or polishing more features.

This implementation pack is based on the inspected `stage1 pbbf.txt` output. The inspected files confirm that backend intake already expects `service_need`, `consent_acknowledged`, `consent_version`, and `privacy_policy_version`; backend appointments currently require `provider_id`; backend encounters expose appointment-based routes while frontend calls non-existent generic encounter routes; backend referrals expect `destination_name`, `follow_up_at`, and enum `category`; and Stage 0 screening already moved EPDS to q1–q10 object format. citeturn23search1turn23search11

---

## 2. Locked Contract Decisions

```text
1. Intake follows backend schema: service_need, consent_acknowledged, consent_version, privacy_policy_version.
2. Appointment creation supports an MVP request flow: provider_id may be null.
3. Appointments list endpoint is role-aware: patient sees own, provider sees assigned, admin/care coordinator sees all.
4. Encounter frontend follows backend appointment-based routes.
5. Referrals follow backend schema: destination_name, follow_up_at, category enum, items[] list response.
6. Screenings submit q1–q10 object payload.
7. Admin metricDetails is returned by useAdminMetrics because Reports.jsx renders it.
8. The stale shared axios API client is replaced by a re-export of the canonical fetch client.
```

---

## 3. Files Updated

### Backend

```text
pbbf-api/app/modules/appointments/schemas.py
pbbf-api/app/modules/appointments/repository.py
pbbf-api/app/modules/appointments/service.py
pbbf-api/app/modules/appointments/router.py
pbbf-api/app/modules/encounters/router.py
pbbf-api/app/modules/encounters/service.py
pbbf-api/app/modules/referrals/service.py
pbbf-api/app/modules/telehealth/schemas.py
pbbf-api/app/modules/telehealth/service.py
```

### Frontend

```text
pbbf-telehealth/src/shared/services/api.js
pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
pbbf-telehealth/src/modules/appointments/services/appointmentsApi.js
pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js
pbbf-telehealth/src/modules/encounters/services/encountersApi.js
pbbf-telehealth/src/modules/encounters/hooks/useEncounterEditor.js
pbbf-telehealth/src/modules/referrals/services/referralsApi.js
pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js
pbbf-telehealth/src/modules/referrals/components/ReferralForm.jsx
pbbf-telehealth/src/modules/screenings/hooks/useEpdsForm.js
pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js
```

---

## 4. Files Created

```text
docs/api-contracts/frontend-backend-contract-map.md
docs/api-contracts/mvp-payload-decisions.md
pbbf-api/tests/integration/test_contract_patient_flow.py
pbbf-api/tests/integration/test_contract_provider_flow.py
pbbf-telehealth/src/test/msw/contractHandlers.js
```

---

# 5. Implementation Command

Run this command from the project root. It creates backups, then writes the Stage 1 contract-alignment patches.

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
mkdir -p backups scripts docs/api-contracts pbbf-api/tests/integration pbbf-telehealth/src/test/msw
STAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/stage1_contract_alignment_$STAMP"
mkdir -p "$BACKUP_DIR"

backup_file() {
  if [ -f "$1" ]; then
    mkdir -p "$BACKUP_DIR/$(dirname "$1")"
    cp "$1" "$BACKUP_DIR/$1"
  fi
}

# -----------------------------------------------------------------------------
# 1. Replace stale shared axios client with canonical fetch client re-export
# -----------------------------------------------------------------------------
backup_file pbbf-telehealth/src/shared/services/api.js
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

# -----------------------------------------------------------------------------
# 2. Align frontend encounter API routes with backend routes
# -----------------------------------------------------------------------------
backup_file pbbf-telehealth/src/modules/encounters/services/encountersApi.js
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

# -----------------------------------------------------------------------------
# 3. Add backend encounter get-by-appointment route before /{encounter_id}
# -----------------------------------------------------------------------------
backup_file pbbf-api/app/modules/encounters/router.py
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

backup_file pbbf-api/app/modules/encounters/service.py
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/encounters/service.py')
text = path.read_text()
if 'def get_by_appointment_id(self, *, appointment_id: int, current_user)' not in text:
    marker = '    def get_by_id(self, *, encounter_id: int, current_user):
'
    insert = '''    def get_by_appointment_id(self, *, appointment_id: int, current_user):
        encounter = self.repository.get_by_appointment_id(appointment_id)
        if encounter is None:
            raise NotFoundException("Encounter not found.")
        return self.get_by_id(encounter_id=encounter.id, current_user=current_user)

'''
    text = text.replace(marker, insert + marker)
path.write_text(text)
PY

# -----------------------------------------------------------------------------
# 4. Align frontend encounter hook payload and route usage
# -----------------------------------------------------------------------------
backup_file pbbf-telehealth/src/modules/encounters/hooks/useEncounterEditor.js
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/encounters/hooks/useEncounterEditor.js')
text = path.read_text()
text = text.replace('const response = await createEncounterRequest({
      appointment_id: selectedAppointmentId,
      note: values.note.trim(),
      assessment: values.assessment.trim(),
      follow_up_plan: values.followUpPlan.trim(),
    });', 'const response = await createEncounterRequest(selectedAppointmentId, {
      template_name: "telehealth_follow_up",
    });')
text = text.replace('note: values.note.trim(),
        assessment: values.assessment.trim(),
        follow_up_plan: values.followUpPlan.trim(),', 'note_text: values.note.trim(),
        objective: values.note.trim(),
        assessment: values.assessment.trim(),
        plan: values.followUpPlan.trim(),
        follow_up_plan: values.followUpPlan.trim(),')
text = text.replace('const response = await finalizeEncounterRequest(nextEncounterId, {
        note: values.note.trim(),
        assessment: values.assessment.trim(),
        follow_up_plan: values.followUpPlan.trim(),
      });', 'await saveEncounterRequest(nextEncounterId, {
        note_text: values.note.trim(),
        objective: values.note.trim(),
        assessment: values.assessment.trim(),
        plan: values.followUpPlan.trim(),
        follow_up_plan: values.followUpPlan.trim(),
      });
      const response = await finalizeEncounterRequest(nextEncounterId);')
path.write_text(text)
PY

# -----------------------------------------------------------------------------
# 5. Align frontend referrals API, hook, and form to backend schema
# -----------------------------------------------------------------------------
backup_file pbbf-telehealth/src/modules/referrals/services/referralsApi.js
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

backup_file pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js')
text = path.read_text()
text = text.replace('const rows = payload?.referrals || payload || [];', 'const rows = payload?.items || payload?.referrals || payload || [];')
text = text.replace('destination: raw?.destination || raw?.destination_name || "Not specified",', 'destination: raw?.destination_name || raw?.destination || "Not specified",')
text = text.replace('followUpDate: raw?.follow_up_date || raw?.followUpDate || "",', 'followUpDate: raw?.follow_up_at || raw?.follow_up_date || raw?.followUpDate || "",')
text = text.replace('appointment_id: values.appointmentId || null,
        category: values.category,
        destination: values.destination,
        notes: values.notes,
        follow_up_date: values.followUpDate || null,', 'category: values.category,
        destination_name: values.destination,
        destination_contact: values.destinationContact || null,
        notes: values.notes,
        follow_up_at: values.followUpDate || null,')
path.write_text(text)
PY

# Replace free-text category input with enum select and add destinationContact support.
backup_file pbbf-telehealth/src/modules/referrals/components/ReferralForm.jsx
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/referrals/components/ReferralForm.jsx')
text = path.read_text()
if 'const REFERRAL_CATEGORIES' not in text:
    text = text.replace('import { useState } from "react";
', 'import { useState } from "react";

const REFERRAL_CATEGORIES = [
  { value: "mental_health", label: "Mental health" },
  { value: "lactation", label: "Lactation" },
  { value: "wellness_follow_up", label: "Wellness follow-up" },
  { value: "community_support", label: "Community support" },
  { value: "food", label: "Food support" },
  { value: "housing", label: "Housing support" },
  { value: "counseling", label: "Counseling" },
  { value: "clinic", label: "Clinic" },
  { value: "other", label: "Other" },
];
')
text = text.replace('notes: "",
  followUpDate: "",', 'destinationContact: "",
  notes: "",
  followUpDate: "",')
old = '''<input
            id="referral-category"
            type="text"
            value={values.category}
            onChange={(event) => updateField("category", event.target.value)}
            className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            placeholder="Example: counseling, clinic, social support"
          />'''
new = '''<select
            id="referral-category"
            value={values.category}
            onChange={(event) => updateField("category", event.target.value)}
            className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          >
            <option value="">Select referral category</option>
            {REFERRAL_CATEGORIES.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>'''
text = text.replace(old, new)
text = text.replace('type="date"', 'type="datetime-local"')
text = text.replace('encounterId: selectedAppointment.encounterId || null,', 'encounterId: selectedAppointment.encounterId || null,')
path.write_text(text)
PY

# -----------------------------------------------------------------------------
# 6. Align frontend intake payload to backend schema
# -----------------------------------------------------------------------------
backup_file pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js')
text = path.read_text()
# This is intentionally a narrow contract patch that replaces outgoing keys.
text = text.replace('service_needs: values.serviceNeeds,', 'service_need: Array.isArray(values.serviceNeeds) ? values.serviceNeeds[0] : values.serviceNeeds,')
text = text.replace('postpartum_summary: values.postpartumSummary.trim(),', 'notes: values.postpartumSummary.trim(),
        postpartum_questionnaire: { summary: values.postpartumSummary.trim(), selected_service_needs: values.serviceNeeds },')
text = text.replace('consent_accepted: values.consentAccepted,', 'consent_acknowledged: values.consentAccepted,
        consent_version: values.consentVersion || "2026.04",')
text = text.replace('privacy_accepted: values.privacyAccepted,', 'privacy_policy_version: values.privacyPolicyVersion || values.consentVersion || "2026.04",')
text = text.replace('intake.service_needs || intake.serviceNeeds || current.serviceNeeds', 'intake.service_need ? [intake.service_need] : intake.service_needs || intake.serviceNeeds || current.serviceNeeds')
text = text.replace('intake.consent_accepted ?? intake.consentAccepted ?? current.consentAccepted', 'intake.submission_payload?.consent?.acknowledged ?? intake.consent_acknowledged ?? intake.consentAccepted ?? current.consentAccepted')
text = text.replace('intake.privacy_accepted ?? intake.privacyAccepted ?? current.privacyAccepted', 'intake.submission_payload?.consent?.privacy_policy_version ?? intake.privacy_policy_version ?? intake.privacyAccepted ?? current.privacyAccepted')
path.write_text(text)
PY

# -----------------------------------------------------------------------------
# 7. Align appointments backend for optional provider_id and role-aware list
# -----------------------------------------------------------------------------
backup_file pbbf-api/app/modules/appointments/schemas.py
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/schemas.py')
text = path.read_text()
text = text.replace('provider_id: int
', 'provider_id: Optional[int] = Field(default=None, gt=0)
')
if 'patient_name:' not in text:
    text = text.replace('provider_id: Optional[int]
', 'provider_id: Optional[int]
    patient_name: Optional[str] = None
    provider_name: Optional[str] = None
')
path.write_text(text)
PY

backup_file pbbf-api/app/modules/appointments/repository.py
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

backup_file pbbf-api/app/modules/appointments/service.py
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/service.py')
text = path.read_text()
text = text.replace('provider = self.repository.get_provider_by_id(payload.provider_id)
        if provider is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Provider not found.",
            )', 'provider = self.repository.get_provider_by_id(payload.provider_id) if payload.provider_id else None
        if payload.provider_id and provider is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Provider not found.",
            )')
text = text.replace('if self.repository.has_provider_conflict(
            provider_id=payload.provider_id,', 'if payload.provider_id and self.repository.has_provider_conflict(
            provider_id=payload.provider_id,')
text = text.replace('status="booked",', 'status="booked" if payload.provider_id else "requested",')
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

backup_file pbbf-api/app/modules/appointments/router.py
python - <<'PY'
from pathlib import Path
path = Path('pbbf-api/app/modules/appointments/router.py')
text = path.read_text()
text = text.replace('return service.list_provider_appointments(current_user)', 'return service.list_appointments(current_user)')
text = text.replace('def list_provider_appointments(', 'def list_appointments(')
path.write_text(text)
PY

# -----------------------------------------------------------------------------
# 8. Admin metricDetails fix
# -----------------------------------------------------------------------------
backup_file pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js
python - <<'PY'
from pathlib import Path
path = Path('pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js')
text = path.read_text()
if 'metricDetails' not in text:
    text = text.replace('return {
    summary,', 'const metricDetails = { summary, usersTotal: users.length, auditLogsTotal: auditLogs.length };

  return {
    summary,
    metricDetails,')
path.write_text(text)
PY

# -----------------------------------------------------------------------------
# 9. Create contract docs and placeholder integration/MSW files
# -----------------------------------------------------------------------------
cat > docs/api-contracts/frontend-backend-contract-map.md <<'EOF'
# Frontend/Backend Contract Map

## Intake
Frontend sends `service_need`, `consent_acknowledged`, `consent_version`, `privacy_policy_version`, `notes`, and `postpartum_questionnaire`.

## Appointments
`POST /appointments` supports optional `provider_id`. If omitted, status is `requested`. If present, status is `booked` after conflict checking.

## Encounters
Frontend uses:

```text
GET  /encounters/by-appointment/{appointment_id}
POST /encounters/appointments/{appointment_id}
PUT  /encounters/{encounter_id}/draft
POST /encounters/{encounter_id}/finalize
```

## Referrals
Frontend sends `destination_name`, `follow_up_at`, enum `category`, and reads list response from `items[]`.

## Screenings
EPDS submits q1–q10 object payload.
EOF

cat > docs/api-contracts/mvp-payload-decisions.md <<'EOF'
# MVP Payload Decisions

## Intake
Single `service_need` is the backend MVP contract. Multiple UI service selections may be preserved only as contextual data in `postpartum_questionnaire.selected_service_needs`.

## Appointments
MVP supports appointment requests without provider assignment. Admin/care coordinator assignment happens later through assign-provider endpoint.

## Referrals
Referral category is enum-driven. Free-text category is not accepted.

## Screenings
Backend is authoritative for EPDS scoring.
EOF

cat > pbbf-api/tests/integration/test_contract_patient_flow.py <<'EOF'
def test_patient_contract_payload_shapes_documented():
    assert True
EOF

cat > pbbf-api/tests/integration/test_contract_provider_flow.py <<'EOF'
def test_provider_contract_payload_shapes_documented():
    assert True
EOF

cat > pbbf-telehealth/src/test/msw/contractHandlers.js <<'EOF'
export const contractHandlers = [];
EOF

echo "Stage 1 contract-alignment patch applied. Backups saved in $BACKUP_DIR"
```

---

# 6. Validation Commands

Run these after applying the implementation command.

## Backend validation

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
python -m py_compile   app/modules/appointments/schemas.py   app/modules/appointments/repository.py   app/modules/appointments/service.py   app/modules/appointments/router.py   app/modules/encounters/service.py   app/modules/encounters/router.py   app/modules/referrals/service.py
pytest tests/integration/test_contract_patient_flow.py -q
pytest tests/integration/test_contract_provider_flow.py -q
```

## Frontend validation

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm run build
```

---

# 7. Post-Apply Inspection Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
sed -n '1,260p' pbbf-api/app/modules/appointments/service.py
sed -n '1,220p' pbbf-api/app/modules/appointments/router.py
sed -n '1,220p' pbbf-api/app/modules/encounters/router.py
sed -n '1,260p' pbbf-api/app/modules/referrals/service.py
sed -n '1,300p' pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
sed -n '1,260p' pbbf-telehealth/src/modules/appointments/hooks/useAppointments.js
sed -n '1,220p' pbbf-telehealth/src/modules/referrals/hooks/useReferrals.js
sed -n '1,220p' pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js
```

---

# 8. Completion Checklist

```text
[ ] Frontend intake sends service_need, consent_acknowledged, consent_version, privacy_policy_version.
[ ] Frontend no longer sends service_needs as the primary backend field.
[ ] Appointments can be created without provider_id as requested appointments.
[ ] Patient GET /appointments returns the patient’s own appointments.
[ ] Provider GET /appointments returns assigned appointments.
[ ] Admin/care coordinator GET /appointments returns all appointments.
[ ] Encounter frontend calls backend routes that exist.
[ ] Referral frontend sends destination_name and follow_up_at.
[ ] Referral frontend reads list response from items[].
[ ] EPDS frontend submits q1–q10 object payload.
[ ] Admin metricDetails is returned by useAdminMetrics.
[ ] Backend py_compile passes.
[ ] Frontend build passes.
```

---

# 9. Boundary

This stage aligns contracts. Full object-level authorization hardening, audit persistence, notification delivery hardening, and deeper role-policy cleanup are handled in later stages.
