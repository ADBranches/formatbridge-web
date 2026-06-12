# PBBF BLISS — Stage 4 Intake and Consent Governance Guide

**Stage:** 4 — Intake and Consent Governance  
**Version:** Stage 4.a — Inspection-First Governance Pack  
**Repository root:** `/home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth`  
**Backend:** `pbbf-api/`  
**Frontend:** `pbbf-telehealth/`  
**Development OS:** Debian/Linux  
**Execution style:** Independent commands/snippets only. Run one command at a time.

---

## Objective

Make intake and consent reliable, auditable, and aligned between frontend and backend.

The completion goal is that consent is no longer only a transient checkbox in the UI. Consent must be persisted as a durable backend event with version metadata, timestamps, actor/user context, and policy/version details that can be reviewed later.

---

## Stage 4 Scope

### Files to update

```text
pbbf-api/app/modules/intake/router.py
pbbf-api/app/modules/intake/schemas.py
pbbf-api/app/modules/intake/service.py
pbbf-api/app/modules/intake/repository.py
pbbf-api/app/modules/intake/validators.py
pbbf-telehealth/src/modules/intake/hooks/useIntakeForm.js
pbbf-telehealth/src/modules/intake/utils/intakeSchema.js
pbbf-telehealth/src/modules/intake/pages/ConsentPage.jsx
pbbf-telehealth/src/modules/intake/pages/IntakeFormPage.jsx
pbbf-telehealth/src/modules/intake/components/IntakeForm.jsx
```

### Files to create

```text
pbbf-api/app/db/models/consent_event.py
pbbf-api/alembic/versions/<new>_add_consent_events.py
pbbf-api/tests/modules/intake/test_consent_versioning.py
pbbf-api/tests/modules/intake/test_consent_event_history.py
pbbf-telehealth/src/modules/intake/__tests__/ConsentPersistence.test.jsx
```

---

## Required Decisions for Stage 4

Before modifying files, lock these decisions:

```text
1. Consent event storage is backend-authoritative.
2. Consent events are append-only audit records.
3. Intake submission references the active consent versions used during submission.
4. Frontend may preserve consent state between pages, but backend persistence is required.
5. Use service_needs as the canonical field unless current backend schemas prove a different field is already canonical.
6. Map postpartum summary to backend notes or questionnaire data, not to an undefined field.
7. Persist consent_policy_version and privacy_policy_version.
8. Include terms_policy_version if the current UI/contract already references terms.
9. The platform must support consent event history retrieval for care team/admin review or tests.
```

---

## Improved Stage 4 Requirements

The original Stage 4 instruction is strong, but this guide adds the following hardening improvements:

```text
- Add inspection before patching because current intake schemas/services must be confirmed.
- Make consent_event append-only instead of overwriting consent state.
- Store consent source metadata where available: request_id, IP-derived metadata if already supported, user agent if available through request context.
- Add explicit consent_event_type values, for example intake_consent_accepted and privacy_policy_acknowledged.
- Add tests that prove consent survives navigation between ConsentPage and IntakeFormPage.
- Add tests that prove old consent events remain available after new versions are accepted.
- Prevent frontend-only consent from being treated as final persistence.
- Keep backend as source of truth for consent version accepted during intake submission.
```

---

# 0. Preflight Positioning

Run from repository root:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
pwd
ls
```

Expected root entries:

```text
pbbf-api
pbbf-telehealth
docs
infra
scripts
```

---

# 1. Stage 4 Inspection Pack

Do not patch Stage 4 until the current file structures below are captured.

## Command 1.1 — Backend intake files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api

printf '\n=== INTAKE ROUTER ===\n'
sed -n '1,320p' app/modules/intake/router.py

printf '\n=== INTAKE SCHEMAS ===\n'
sed -n '1,420p' app/modules/intake/schemas.py

printf '\n=== INTAKE SERVICE ===\n'
sed -n '1,520p' app/modules/intake/service.py

printf '\n=== INTAKE REPOSITORY ===\n'
sed -n '1,420p' app/modules/intake/repository.py

printf '\n=== INTAKE VALIDATORS ===\n'
sed -n '1,320p' app/modules/intake/validators.py

printf '\n=== INTAKE CONSTANTS ===\n'
sed -n '1,320p' app/modules/intake/constants.py

printf '\n=== INTAKE SUBMISSION MODEL ===\n'
sed -n '1,360p' app/db/models/intake_submission.py
```

## Command 1.2 — Frontend intake files

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth

printf '\n=== USE INTAKE FORM HOOK ===\n'
sed -n '1,420p' src/modules/intake/hooks/useIntakeForm.js

printf '\n=== INTAKE SCHEMA JS ===\n'
sed -n '1,420p' src/modules/intake/utils/intakeSchema.js

printf '\n=== CONSENT PAGE ===\n'
sed -n '1,420p' src/modules/intake/pages/ConsentPage.jsx

printf '\n=== INTAKE FORM PAGE ===\n'
sed -n '1,420p' src/modules/intake/pages/IntakeFormPage.jsx

printf '\n=== INTAKE FORM COMPONENT ===\n'
sed -n '1,520p' src/modules/intake/components/IntakeForm.jsx

printf '\n=== INTAKE API ===\n'
sed -n '1,260p' src/modules/intake/services/intakeApi.js
```

## Command 1.3 — Current intake tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

printf '\n=== BACKEND INTAKE TESTS ===\n'
find pbbf-api/tests/modules/intake -type f -name '*.py' -print -maxdepth 1 | sort

for f in pbbf-api/tests/modules/intake/*.py; do
  printf '\n=== %s ===\n' "$f"
  sed -n '1,320p' "$f"
done

printf '\n=== FRONTEND INTAKE TESTS ===\n'
find pbbf-telehealth/src/modules/intake/__tests__ -type f -maxdepth 1 | sort

for f in pbbf-telehealth/src/modules/intake/__tests__/*; do
  printf '\n=== %s ===\n' "$f"
  sed -n '1,320p' "$f"
done
```

## Command 1.4 — Alembic head and model registry

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api

printf '\n=== ALEMBIC HEADS ===\n'
alembic heads

printf '\n=== MODEL REGISTRY ===\n'
sed -n '1,280p' app/db/models/__init__.py
```

---

# 2. Stage 4 Implementation Design

The exact patch pack should be generated after Command 1 outputs are reviewed. The target design should be:

## Backend durable consent event model

Create:

```text
pbbf-api/app/db/models/consent_event.py
```

Recommended model fields:

```text
id
patient_id
user_id
intake_submission_id nullable
event_type
consent_policy_version
privacy_policy_version
terms_policy_version nullable
accepted
accepted_at
source
request_id nullable
metadata_json nullable
created_at
updated_at
```

Recommended event types:

```text
intake_consent_accepted
privacy_policy_acknowledged
terms_acknowledged
consent_reconfirmed
```

## Backend repository responsibilities

`pbbf-api/app/modules/intake/repository.py` should support:

```text
create_consent_event(...)
list_consent_events_for_patient(patient_id)
get_latest_consent_event_for_patient(patient_id)
```

## Backend service responsibilities

`pbbf-api/app/modules/intake/service.py` should:

```text
- Validate consent fields during submit.
- Persist consent event when consent is captured or submitted.
- Store consent_policy_version and privacy_policy_version.
- Attach intake_submission_id when the consent is tied to an intake submission.
- Avoid silently accepting missing consent version fields.
- Return latest consent metadata in /intake/me/latest if useful for frontend state restoration.
```

## Backend router responsibilities

`pbbf-api/app/modules/intake/router.py` should expose only routes that match the existing route style. Possible routes after inspection:

```text
POST /intake/{intake_id}/submit
GET /intake/me/latest
GET /intake/me/consent-events
```

Do not add routes before confirming current router structure.

## Frontend persistence responsibilities

Frontend should:

```text
- Persist consent state between ConsentPage and IntakeFormPage.
- Submit consent_policy_version and privacy_policy_version to backend.
- Use the backend response as final consent persistence confirmation.
- Not treat localStorage/sessionStorage alone as final consent capture.
```

Recommended frontend storage strategy for this stage:

```text
- Use sessionStorage for in-progress onboarding consent handoff.
- Clear the temporary consent handoff after successful backend submission.
- Rehydrate consent state when navigating from consent to intake page.
```

---

# 3. Stage 4 Test Requirements

## Backend tests to create

```text
pbbf-api/tests/modules/intake/test_consent_versioning.py
pbbf-api/tests/modules/intake/test_consent_event_history.py
```

### Required backend test cases

```text
1. Consent submission persists consent_policy_version.
2. Consent submission persists privacy_policy_version.
3. Consent event is linked to patient profile.
4. Consent event is linked to intake submission when submitted with intake.
5. Multiple consent events are preserved as history.
6. Latest consent event can be resolved for a patient.
7. Missing required consent version fails validation.
```

## Frontend test to create

```text
pbbf-telehealth/src/modules/intake/__tests__/ConsentPersistence.test.jsx
```

### Required frontend test cases

```text
1. Consent selections survive navigation from ConsentPage to IntakeFormPage.
2. Intake submission includes consent_policy_version.
3. Intake submission includes privacy_policy_version.
4. Temporary consent state is cleared after successful submit.
5. UI prevents continuing without required consent acknowledgements.
```

---

# 4. Stage 4 Backup Plan

Only run after inspection confirms Stage 4 patch direction.

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

# 5. Validation Commands for Stage 4

Run after the Stage 4 implementation patch is produced and applied.

## Backend compile

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

## Alembic smoke

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
alembic heads
alembic history | tail -20
```

## Backend intake tests

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
pytest tests/modules/intake/test_create_draft.py \
       tests/modules/intake/test_submit_intake.py \
       tests/modules/intake/test_consent_capture.py \
       tests/modules/intake/test_consent_versioning.py \
       tests/modules/intake/test_consent_event_history.py -q
```

## Frontend intake tests and build

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm test -- --run src/modules/intake/__tests__/ConsentPersistence.test.jsx
npm run build
```

---

# 6. Completion Checklist

```text
[ ] Current backend intake structure inspected before patching.
[ ] Current frontend intake structure inspected before patching.
[ ] consent_events model exists.
[ ] consent_events migration uses current Alembic head.
[ ] consent_events model is registered in app/db/models/__init__.py.
[ ] Consent event persists patient_id.
[ ] Consent event persists user_id.
[ ] Consent event persists consent_policy_version.
[ ] Consent event persists privacy_policy_version.
[ ] Consent event persists accepted_at.
[ ] Consent event history is append-only.
[ ] Intake submit creates/links durable consent event.
[ ] Frontend consent survives ConsentPage -> IntakeFormPage navigation.
[ ] Frontend sends consent versions to backend.
[ ] service_needs vs service_need decision is locked and reflected in schemas/UI.
[ ] Postpartum summary maps to a backend-supported field.
[ ] Backend intake tests pass.
[ ] Frontend consent persistence test passes.
[ ] Frontend build passes.
```

---

# 7. Boundary

```text
Stage 4 does not add clinical scoring or EPDS behavior.
Stage 4 does not redesign the whole intake questionnaire.
Stage 4 does not replace Stage 1 contract alignment; it only fixes intake/consent governance.
Stage 4 does not rely on frontend storage as the final consent record.
Backend durable consent event is the source of truth.
```

---

# 8. Next Step After This Guide

Run the inspection commands in Section 1 and paste the outputs.

After the exact file structures are confirmed, produce the Stage 4.b implementation pack with safe commands for:

```text
- consent_event model creation
- model registry update
- Alembic migration using actual current head
- intake schema updates
- intake repository/service/router updates
- frontend consent handoff persistence
- backend and frontend tests
```
