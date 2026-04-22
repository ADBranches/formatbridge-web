# PBBF BLISS Frontend — Phase 7 Populated Files
## Provider Workspace: Dashboard, Notes, and Referrals

## Objective
Build the provider-facing workflow for appointments, chart context, notes, and referrals.

Repository root:

`bliss-telehealth/pbbf-telehealth`

This phase completes the provider-facing clinical workspace so that a signed-in provider can:

- view assigned appointments from a dashboard
- open a notes workspace with patient context
- draft and finalize encounter notes
- create and track referrals
- see screening-alert context while working
- complete the main clinical workflow without falling back to manual tools

---

## Important alignment with your current structure

Your existing app structure already supports this phase well:

- `src/app/AppRoutes.jsx` already contains provider routes
- `src/app/AppLayout.jsx` already wraps protected shell pages
- provider pages already exist:
  - `src/pages/provider/Dashboard.jsx`
  - `src/pages/provider/Notes.jsx`
  - `src/pages/provider/Referrals.jsx`

So this phase should **complete the provider workspace inside the current shell**, not redesign the route structure.

### No route rewrite needed
Based on the `AppRoutes.jsx` you shared, you do **not** need to rewrite the route map for this phase unless one of the provider route constants is missing in:

- `src/shared/constants/routes.js`

---

## Phase 7 backend assumptions

This frontend phase assumes the backend exposes routes similar to:

### Appointments
- `GET /api/v1/appointments`

The current role-authenticated provider should receive provider-relevant appointments from the backend.

### Encounters
- `GET /api/v1/encounters/by-appointment/{appointment_id}`
- `POST /api/v1/encounters`
- `PATCH /api/v1/encounters/{encounter_id}/save`
- `PATCH /api/v1/encounters/{encounter_id}/finalize`

### Referrals
- `GET /api/v1/referrals`
- `POST /api/v1/referrals`
- `PATCH /api/v1/referrals/{referral_id}/status`

If your actual backend paths differ, update only:

- `src/modules/encounters/services/encountersApi.js`
- `src/modules/referrals/services/referralsApi.js`

---

## Practical appointment-hook note

This phase reuses your existing appointments module and assumes:

- `useAppointments()` can already load provider-visible appointments for the authenticated provider

If your current appointments hook still behaves as patient-only, extend the backend response or add a provider-specific request later. The provider pages below are written to work cleanly if the backend already scopes appointments by role.

---

## File list for this phase

### Modify these files
- `src/pages/provider/Dashboard.jsx`
- `src/pages/provider/Notes.jsx`
- `src/pages/provider/Referrals.jsx`
- `src/modules/encounters/pages/*`
- `src/modules/encounters/components/*`
- `src/modules/referrals/pages/*`
- `src/modules/referrals/components/*`

### Create these files if missing
- `src/modules/encounters/components/EncounterEditor.jsx`
- `src/modules/encounters/components/PatientSummaryCard.jsx`
- `src/modules/encounters/hooks/useEncounterEditor.js`
- `src/modules/encounters/services/encountersApi.js`
- `src/modules/referrals/components/ReferralForm.jsx`
- `src/modules/referrals/components/ReferralTimeline.jsx`
- `src/modules/referrals/hooks/useReferrals.js`
- `src/modules/referrals/services/referralsApi.js`
- `src/modules/encounters/__tests__/EncounterEditor.test.jsx`
- `src/modules/referrals/__tests__/ReferralForm.test.jsx`

### Recommended support test for the required dashboard outcome
- `src/pages/provider/__tests__/Dashboard.test.jsx`

---

# 1) `src/modules/encounters/services/encountersApi.js`

```jsx
import { api } from "../../../services/api";

export function getEncounterByAppointmentRequest(appointmentId) {
  return api.get(`/encounters/by-appointment/${appointmentId}`);
}

export function createEncounterRequest(payload) {
  return api.post("/encounters", payload);
}

export function saveEncounterRequest(encounterId, payload) {
  return api.patch(`/encounters/${encounterId}/save`, payload);
}

export function finalizeEncounterRequest(encounterId, payload) {
  return api.patch(`/encounters/${encounterId}/finalize`, payload);
}
```

---

# 2) `src/modules/encounters/hooks/useEncounterEditor.js`

```jsx
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  createEncounterRequest,
  finalizeEncounterRequest,
  getEncounterByAppointmentRequest,
  saveEncounterRequest,
} from "../services/encountersApi";

function normalizeEncounter(raw) {
  return {
    id: raw?.id || raw?.encounter_id || null,
    appointmentId: raw?.appointment_id || raw?.appointmentId || null,
    note: raw?.note || raw?.encounter_note || "",
    assessment: raw?.assessment || "",
    followUpPlan: raw?.follow_up_plan || raw?.followUpPlan || "",
    status: raw?.status || "draft",
  };
}

const EMPTY_VALUES = {
  note: "",
  assessment: "",
  followUpPlan: "",
};

function validate(values) {
  const errors = {
    note: "",
    assessment: "",
    followUpPlan: "",
  };

  if (!values.note?.trim()) {
    errors.note = "Encounter note is required.";
  }

  if (!values.assessment?.trim()) {
    errors.assessment = "Assessment is required.";
  }

  if (!values.followUpPlan?.trim()) {
    errors.followUpPlan = "Follow-up plan is required.";
  }

  return errors;
}

function hasErrors(errors) {
  return Object.values(errors).some(Boolean);
}

export function useEncounterEditor(selectedAppointmentId) {
  const [encounterId, setEncounterId] = useState(null);
  const [values, setValues] = useState(EMPTY_VALUES);
  const [errors, setErrors] = useState({
    note: "",
    assessment: "",
    followUpPlan: "",
  });
  const [status, setStatus] = useState("draft");
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [loadError, setLoadError] = useState("");

  const loadEncounter = useCallback(async () => {
    if (!selectedAppointmentId) {
      setEncounterId(null);
      setValues(EMPTY_VALUES);
      setStatus("draft");
      setLoadError("");
      return;
    }

    try {
      setIsLoading(true);
      setLoadError("");
      setMessage("");

      const response = await getEncounterByAppointmentRequest(selectedAppointmentId);
      const payload = response?.data || response;
      const encounter = normalizeEncounter(payload?.encounter || payload || {});

      setEncounterId(encounter.id);
      setValues({
        note: encounter.note,
        assessment: encounter.assessment,
        followUpPlan: encounter.followUpPlan,
      });
      setStatus(encounter.status || "draft");
    } catch (error) {
      setEncounterId(null);
      setValues(EMPTY_VALUES);
      setStatus("draft");
      setLoadError("");
    } finally {
      setIsLoading(false);
    }
  }, [selectedAppointmentId]);

  useEffect(() => {
    loadEncounter();
  }, [loadEncounter]);

  function updateField(field, value) {
    setValues((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: "" }));
    setMessage("");
  }

  async function ensureEncounterExists() {
    if (encounterId) return encounterId;

    const response = await createEncounterRequest({
      appointment_id: selectedAppointmentId,
      note: values.note.trim(),
      assessment: values.assessment.trim(),
      follow_up_plan: values.followUpPlan.trim(),
    });

    const payload = response?.data || response;
    const encounter = normalizeEncounter(payload?.encounter || payload || {});
    setEncounterId(encounter.id);
    return encounter.id;
  }

  async function saveDraft() {
    const nextErrors = validate(values);
    setErrors(nextErrors);

    if (hasErrors(nextErrors) || !selectedAppointmentId) {
      return { success: false };
    }

    try {
      setIsSaving(true);
      setMessage("");

      const nextEncounterId = await ensureEncounterExists();
      const response = await saveEncounterRequest(nextEncounterId, {
        note: values.note.trim(),
        assessment: values.assessment.trim(),
        follow_up_plan: values.followUpPlan.trim(),
      });

      setStatus("draft");
      setMessage(response?.message || "Encounter draft saved successfully.");
      return { success: true, response };
    } catch (error) {
      setMessage(error?.message || "Unable to save encounter draft.");
      return { success: false, error };
    } finally {
      setIsSaving(false);
    }
  }

  async function finalize() {
    const nextErrors = validate(values);
    setErrors(nextErrors);

    if (hasErrors(nextErrors) || !selectedAppointmentId) {
      return { success: false };
    }

    try {
      setIsSaving(true);
      setMessage("");

      const nextEncounterId = await ensureEncounterExists();
      const response = await finalizeEncounterRequest(nextEncounterId, {
        note: values.note.trim(),
        assessment: values.assessment.trim(),
        follow_up_plan: values.followUpPlan.trim(),
      });

      setStatus("finalized");
      setMessage(response?.message || "Encounter finalized successfully.");
      return { success: true, response };
    } catch (error) {
      setMessage(error?.message || "Unable to finalize encounter.");
      return { success: false, error };
    } finally {
      setIsSaving(false);
    }
  }

  const isFinalized = useMemo(() => status === "finalized", [status]);

  return {
    values,
    errors,
    status,
    isFinalized,
    isLoading,
    isSaving,
    message,
    loadError,
    updateField,
    saveDraft,
    finalize,
    reload: loadEncounter,
  };
}
```

---

# 3) `src/modules/encounters/components/PatientSummaryCard.jsx`

```jsx
function screeningTone(alertLevel) {
  switch (alertLevel) {
    case "high":
      return "border-rose-200 bg-rose-50 text-rose-800";
    case "moderate":
      return "border-amber-200 bg-amber-50 text-amber-900";
    default:
      return "border-slate-200 bg-slate-50 text-slate-700";
  }
}

export default function PatientSummaryCard({ appointment }) {
  if (!appointment) {
    return (
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Patient summary</h2>
        <p className="mt-2 text-sm text-slate-600">
          Select an appointment to view patient context.
        </p>
      </section>
    );
  }

  const alertLevel = appointment.screeningAlertLevel || "none";
  const alertText =
    appointment.screeningAlertText ||
    (alertLevel === "high"
      ? "High-priority screening follow-up indicator."
      : alertLevel === "moderate"
      ? "Moderate follow-up screening indicator."
      : "No active screening alert shown.");

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">
        Patient context
      </p>
      <h2 className="mt-2 text-xl font-semibold text-slate-900">
        {appointment.patientName || "Unknown patient"}
      </h2>

      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Service type
          </p>
          <p className="mt-2 text-sm font-medium text-slate-900">
            {appointment.serviceType || "Not specified"}
          </p>
        </div>

        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Appointment status
          </p>
          <p className="mt-2 text-sm font-medium text-slate-900">
            {appointment.status || "Unknown"}
          </p>
        </div>

        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Visit reason
          </p>
          <p className="mt-2 text-sm text-slate-700">
            {appointment.visitReason || "No visit reason provided."}
          </p>
        </div>

        <div className={`rounded-2xl border p-4 ${screeningTone(alertLevel)}`}>
          <p className="text-xs font-semibold uppercase tracking-[0.16em]">
            Screening alert
          </p>
          <p className="mt-2 text-sm font-medium">{alertText}</p>
        </div>
      </div>
    </section>
  );
}
```

---

# 4) `src/modules/encounters/components/EncounterEditor.jsx`

```jsx
export default function EncounterEditor({
  values,
  errors = {},
  status = "draft",
  isSaving = false,
  message = "",
  onChange,
  onSaveDraft,
  onFinalize,
}) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">
            Encounter note
          </p>
          <h2 className="mt-2 text-xl font-semibold text-slate-900">
            Draft and finalize documentation
          </h2>
        </div>

        <span className="inline-flex rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold capitalize text-slate-700">
          {status}
        </span>
      </div>

      <form
        className="mt-6 space-y-6"
        onSubmit={(event) => {
          event.preventDefault();
          onSaveDraft();
        }}
        noValidate
      >
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Encounter note
          </label>
          <textarea
            rows={6}
            value={values.note}
            onChange={(event) => onChange("note", event.target.value)}
            className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            placeholder="Document visit details, observations, and clinical context..."
          />
          {errors.note ? <p className="mt-2 text-sm text-rose-600">{errors.note}</p> : null}
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Assessment
          </label>
          <textarea
            rows={4}
            value={values.assessment}
            onChange={(event) => onChange("assessment", event.target.value)}
            className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            placeholder="Summarize assessment findings..."
          />
          {errors.assessment ? (
            <p className="mt-2 text-sm text-rose-600">{errors.assessment}</p>
          ) : null}
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Follow-up plan
          </label>
          <textarea
            rows={4}
            value={values.followUpPlan}
            onChange={(event) => onChange("followUpPlan", event.target.value)}
            className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            placeholder="Describe next steps, scheduling, resources, or care recommendations..."
          />
          {errors.followUpPlan ? (
            <p className="mt-2 text-sm text-rose-600">{errors.followUpPlan}</p>
          ) : null}
        </div>

        {message ? (
          <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
            {message}
          </div>
        ) : null}

        <div className="flex flex-col gap-3 sm:flex-row">
          <button
            type="submit"
            disabled={isSaving}
            className="rounded-xl border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isSaving ? "Saving..." : "Save draft"}
          </button>

          <button
            type="button"
            onClick={onFinalize}
            disabled={isSaving}
            className="rounded-xl bg-sky-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isSaving ? "Working..." : "Finalize note"}
          </button>
        </div>
      </form>
    </section>
  );
}
```

---

# 5) `src/modules/referrals/services/referralsApi.js`

```jsx
import { api } from "../../../services/api";

export function listReferralsRequest() {
  return api.get("/referrals");
}

export function createReferralRequest(payload) {
  return api.post("/referrals", payload);
}

export function updateReferralStatusRequest(referralId, payload) {
  return api.patch(`/referrals/${referralId}/status`, payload);
}
```

---

# 6) `src/modules/referrals/hooks/useReferrals.js`

```jsx
import { useCallback, useEffect, useState } from "react";
import {
  createReferralRequest,
  listReferralsRequest,
  updateReferralStatusRequest,
} from "../services/referralsApi";

function normalizeReferral(raw) {
  return {
    id: raw?.id || raw?.referral_id || "temp-referral-id",
    patientName: raw?.patient_name || raw?.patientName || "Unknown patient",
    category: raw?.category || "general",
    destination: raw?.destination || raw?.destination_name || "Not specified",
    status: raw?.status || "created",
    notes: raw?.notes || "",
    followUpDate: raw?.follow_up_date || raw?.followUpDate || "",
    createdAt: raw?.created_at || raw?.createdAt || "",
  };
}

export function useReferrals() {
  const [referrals, setReferrals] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [loadError, setLoadError] = useState("");
  const [message, setMessage] = useState("");

  const loadReferrals = useCallback(async () => {
    try {
      setIsLoading(true);
      setLoadError("");

      const response = await listReferralsRequest();
      const payload = response?.data || response;
      const rows = payload?.referrals || payload || [];

      setReferrals(rows.map(normalizeReferral));
    } catch (error) {
      setLoadError(error?.message || "Unable to load referrals.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadReferrals();
  }, [loadReferrals]);

  async function createReferral(values) {
    try {
      setIsSaving(true);
      setMessage("");

      const response = await createReferralRequest({
        patient_id: values.patientId,
        encounter_id: values.encounterId || null,
        appointment_id: values.appointmentId || null,
        category: values.category,
        destination: values.destination,
        notes: values.notes,
        follow_up_date: values.followUpDate || null,
      });

      await loadReferrals();
      setMessage(response?.message || "Referral created successfully.");
      return { success: true, response };
    } catch (error) {
      setMessage(error?.message || "Unable to create referral.");
      return { success: false, error };
    } finally {
      setIsSaving(false);
    }
  }

  async function updateStatus(referralId, status) {
    try {
      setIsSaving(true);
      setMessage("");

      const response = await updateReferralStatusRequest(referralId, { status });
      await loadReferrals();
      setMessage(response?.message || "Referral status updated.");
      return { success: true, response };
    } catch (error) {
      setMessage(error?.message || "Unable to update referral status.");
      return { success: false, error };
    } finally {
      setIsSaving(false);
    }
  }

  return {
    referrals,
    isLoading,
    isSaving,
    loadError,
    message,
    createReferral,
    updateStatus,
    reload: loadReferrals,
  };
}
```

---

# 7) `src/modules/referrals/components/ReferralForm.jsx`

```jsx
import { useState } from "react";

const INITIAL_VALUES = {
  category: "",
  destination: "",
  notes: "",
  followUpDate: "",
};

function validate(values) {
  const errors = {
    category: "",
    destination: "",
    notes: "",
  };

  if (!values.category?.trim()) {
    errors.category = "Referral category is required.";
  }

  if (!values.destination?.trim()) {
    errors.destination = "Referral destination is required.";
  }

  if (!values.notes?.trim()) {
    errors.notes = "Referral notes are required.";
  }

  return errors;
}

function hasErrors(errors) {
  return Object.values(errors).some(Boolean);
}

export default function ReferralForm({
  selectedAppointment,
  onSubmit,
  isSaving = false,
  message = "",
}) {
  const [values, setValues] = useState(INITIAL_VALUES);
  const [errors, setErrors] = useState({
    category: "",
    destination: "",
    notes: "",
  });

  function updateField(field, value) {
    setValues((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: "" }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const nextErrors = validate(values);
    setErrors(nextErrors);

    if (hasErrors(nextErrors) || !selectedAppointment?.patientId) return;

    const result = await onSubmit({
      ...values,
      patientId: selectedAppointment.patientId,
      appointmentId: selectedAppointment.id,
      encounterId: selectedAppointment.encounterId || null,
    });

    if (result?.success) {
      setValues(INITIAL_VALUES);
    }
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">
        Create referral
      </p>
      <h2 className="mt-2 text-xl font-semibold text-slate-900">
        Referral workflow
      </h2>

      {!selectedAppointment ? (
        <p className="mt-4 text-sm text-slate-600">
          Select a patient appointment first to create a referral.
        </p>
      ) : (
        <p className="mt-4 text-sm text-slate-600">
          Creating referral for <span className="font-medium">{selectedAppointment.patientName}</span>.
        </p>
      )}

      <form className="mt-6 space-y-5" onSubmit={handleSubmit} noValidate>
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Referral category
          </label>
          <input
            type="text"
            value={values.category}
            onChange={(event) => updateField("category", event.target.value)}
            className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            placeholder="Example: counseling, clinic, social support"
          />
          {errors.category ? (
            <p className="mt-2 text-sm text-rose-600">{errors.category}</p>
          ) : null}
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Destination
          </label>
          <input
            type="text"
            value={values.destination}
            onChange={(event) => updateField("destination", event.target.value)}
            className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            placeholder="Enter destination organization or service"
          />
          {errors.destination ? (
            <p className="mt-2 text-sm text-rose-600">{errors.destination}</p>
          ) : null}
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Referral notes
          </label>
          <textarea
            rows={4}
            value={values.notes}
            onChange={(event) => updateField("notes", event.target.value)}
            className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            placeholder="Describe why the referral is needed and what follow-up is expected..."
          />
          {errors.notes ? (
            <p className="mt-2 text-sm text-rose-600">{errors.notes}</p>
          ) : null}
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Follow-up date
          </label>
          <input
            type="date"
            value={values.followUpDate}
            onChange={(event) => updateField("followUpDate", event.target.value)}
            className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          />
        </div>

        {message ? (
          <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
            {message}
          </div>
        ) : null}

        <button
          type="submit"
          disabled={isSaving || !selectedAppointment}
          className="rounded-xl bg-sky-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {isSaving ? "Saving..." : "Create referral"}
        </button>
      </form>
    </section>
  );
}
```

---

# 8) `src/modules/referrals/components/ReferralTimeline.jsx`

```jsx
function formatDate(value) {
  if (!value) return "Not available";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
  }).format(date);
}

export default function ReferralTimeline({ referrals = [], onUpdateStatus, isSaving = false }) {
  if (!referrals.length) {
    return (
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Referral timeline</h2>
        <p className="mt-2 text-sm text-slate-600">
          No referrals are visible yet.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-900">Referral timeline</h2>

      <div className="mt-6 grid gap-4">
        {referrals.map((referral) => (
          <div
            key={referral.id}
            className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
          >
            <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
              <div>
                <p className="text-sm font-semibold text-slate-900">
                  {referral.patientName}
                </p>
                <p className="mt-1 text-sm text-slate-600">
                  {referral.category} → {referral.destination}
                </p>
                <p className="mt-1 text-sm text-slate-600">
                  Status: <span className="font-medium capitalize">{referral.status}</span>
                </p>
                <p className="mt-1 text-sm text-slate-600">
                  Follow-up date: {formatDate(referral.followUpDate)}
                </p>
              </div>

              <div className="flex flex-col gap-2 sm:flex-row">
                <button
                  type="button"
                  onClick={() => onUpdateStatus(referral.id, "acknowledged")}
                  disabled={isSaving}
                  className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-70"
                >
                  Acknowledge
                </button>

                <button
                  type="button"
                  onClick={() => onUpdateStatus(referral.id, "completed")}
                  disabled={isSaving}
                  className="rounded-xl bg-sky-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
                >
                  Mark completed
                </button>
              </div>
            </div>

            {referral.notes ? (
              <p className="mt-4 text-sm leading-6 text-slate-700">{referral.notes}</p>
            ) : null}
          </div>
        ))}
      </div>
    </section>
  );
}
```

---

# 9) `src/pages/provider/Dashboard.jsx`

```jsx
import { Link } from "react-router-dom";
import { ROUTES } from "../../shared/constants/routes";
import { useAppointments } from "../../modules/appointments/hooks/useAppointments";
import Loader from "../../shared/components/Loader";
import EmptyState from "../../shared/components/EmptyState";
import ErrorState from "../../shared/components/ErrorState";

function normalizeProviderAppointment(raw) {
  return {
    id: raw?.id || raw?.appointment_id || "temp-appointment-id",
    patientId: raw?.patient_id || raw?.patientId || null,
    patientName: raw?.patient_name || raw?.patientName || "Unknown patient",
    serviceType: raw?.service_type || raw?.serviceType || "Visit",
    visitReason: raw?.visit_reason || raw?.visitReason || "",
    status: raw?.status || "booked",
    scheduledAt: raw?.scheduled_at || raw?.scheduledAt || "",
    screeningAlertLevel:
      raw?.screening_alert_level || raw?.screeningAlertLevel || "none",
    screeningAlertText:
      raw?.screening_alert_text || raw?.screeningAlertText || "",
  };
}

function formatDateTime(value) {
  if (!value) return "Not scheduled";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export default function ProviderDashboard() {
  const { appointments, isLoading, loadError } = useAppointments();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading provider dashboard..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load provider dashboard" message={loadError} />;
  }

  const normalized = appointments.map(normalizeProviderAppointment);
  const upcoming = normalized.filter(
    (item) => item.status !== "cancelled" && item.status !== "completed"
  );

  const highAlerts = normalized.filter((item) => item.screeningAlertLevel === "high");

  return (
    <div className="space-y-8">
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Provider workspace</p>
        <h1 className="mt-2 text-3xl font-semibold">Clinical dashboard</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Review assigned visits, identify screening alerts, document notes, and manage referrals.
        </p>
      </section>

      <section className="grid gap-5 md:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Assigned appointments</h2>
          <p className="mt-3 text-3xl font-semibold text-slate-900">{normalized.length}</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Open workflow</h2>
          <p className="mt-3 text-3xl font-semibold text-slate-900">{upcoming.length}</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Screening alerts</h2>
          <p className="mt-3 text-3xl font-semibold text-slate-900">{highAlerts.length}</p>
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[1.3fr_0.7fr]">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-slate-900">Upcoming appointments</h2>
            <Link
              to={ROUTES.provider.notes}
              className="text-sm font-semibold text-sky-700 hover:text-sky-800"
            >
              Open notes workspace
            </Link>
          </div>

          {!upcoming.length ? (
            <div className="mt-6">
              <EmptyState
                title="No upcoming appointments"
                message="No provider appointments are visible right now."
              />
            </div>
          ) : (
            <div className="mt-6 grid gap-4">
              {upcoming.slice(0, 6).map((appointment) => (
                <div
                  key={appointment.id}
                  className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
                >
                  <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                    <div>
                      <p className="text-sm font-semibold text-slate-900">
                        {appointment.patientName}
                      </p>
                      <p className="mt-1 text-sm text-slate-600">
                        {appointment.serviceType}
                      </p>
                      <p className="mt-1 text-sm text-slate-600">
                        {formatDateTime(appointment.scheduledAt)}
                      </p>
                    </div>

                    <span className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-semibold capitalize text-slate-700">
                      {appointment.status}
                    </span>
                  </div>

                  {appointment.screeningAlertLevel !== "none" ? (
                    <div className="mt-3 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900">
                      Screening alert:{" "}
                      {appointment.screeningAlertText || appointment.screeningAlertLevel}
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">Workspace shortcuts</h2>

          <div className="mt-6 grid gap-4">
            <Link
              to={ROUTES.provider.notes}
              className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm font-semibold text-slate-900 transition hover:border-slate-300"
            >
              Encounter notes
            </Link>

            <Link
              to={ROUTES.provider.referrals}
              className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm font-semibold text-slate-900 transition hover:border-slate-300"
            >
              Referrals
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
```

---

# 10) `src/pages/provider/Notes.jsx`

```jsx
import { useMemo, useState } from "react";
import { useAppointments } from "../../modules/appointments/hooks/useAppointments";
import PatientSummaryCard from "../../modules/encounters/components/PatientSummaryCard";
import EncounterEditor from "../../modules/encounters/components/EncounterEditor";
import { useEncounterEditor } from "../../modules/encounters/hooks/useEncounterEditor";
import Loader from "../../shared/components/Loader";
import EmptyState from "../../shared/components/EmptyState";
import ErrorState from "../../shared/components/ErrorState";

function normalizeProviderAppointment(raw) {
  return {
    id: raw?.id || raw?.appointment_id || "temp-appointment-id",
    patientId: raw?.patient_id || raw?.patientId || null,
    patientName: raw?.patient_name || raw?.patientName || "Unknown patient",
    serviceType: raw?.service_type || raw?.serviceType || "Visit",
    visitReason: raw?.visit_reason || raw?.visitReason || "",
    status: raw?.status || "booked",
    screeningAlertLevel:
      raw?.screening_alert_level || raw?.screeningAlertLevel || "none",
    screeningAlertText:
      raw?.screening_alert_text || raw?.screeningAlertText || "",
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
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Provider notes</p>
        <h1 className="mt-2 text-3xl font-semibold">Encounter workspace</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Select an appointment, review patient context, and complete structured documentation.
        </p>
      </section>

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

# 11) `src/pages/provider/Referrals.jsx`

```jsx
import { useMemo, useState } from "react";
import { useAppointments } from "../../modules/appointments/hooks/useAppointments";
import ReferralForm from "../../modules/referrals/components/ReferralForm";
import ReferralTimeline from "../../modules/referrals/components/ReferralTimeline";
import { useReferrals } from "../../modules/referrals/hooks/useReferrals";
import Loader from "../../shared/components/Loader";
import EmptyState from "../../shared/components/EmptyState";
import ErrorState from "../../shared/components/ErrorState";

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
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Provider referrals</p>
        <h1 className="mt-2 text-3xl font-semibold">Referral management</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Create referrals for follow-up support and track referral progress over time.
        </p>
      </section>

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

# 12) `src/modules/encounters/__tests__/EncounterEditor.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import EncounterEditor from "../components/EncounterEditor";

describe("EncounterEditor", () => {
  it("calls save draft action", () => {
    const onSaveDraft = vi.fn();

    render(
      <EncounterEditor
        values={{
          note: "Visit note",
          assessment: "Assessment content",
          followUpPlan: "Follow-up plan",
        }}
        errors={{}}
        onChange={vi.fn()}
        onSaveDraft={onSaveDraft}
        onFinalize={vi.fn()}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /save draft/i }));
    expect(onSaveDraft).toHaveBeenCalledTimes(1);
  });

  it("calls finalize action", () => {
    const onFinalize = vi.fn();

    render(
      <EncounterEditor
        values={{
          note: "Visit note",
          assessment: "Assessment content",
          followUpPlan: "Follow-up plan",
        }}
        errors={{}}
        onChange={vi.fn()}
        onSaveDraft={vi.fn()}
        onFinalize={onFinalize}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /finalize note/i }));
    expect(onFinalize).toHaveBeenCalledTimes(1);
  });
});
```

---

# 13) `src/modules/referrals/__tests__/ReferralForm.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import ReferralForm from "../components/ReferralForm";

describe("ReferralForm", () => {
  it("shows validation errors when required fields are missing", async () => {
    render(
      <ReferralForm
        selectedAppointment={{ id: "appt-1", patientId: "patient-1", patientName: "Jane Patient" }}
        onSubmit={vi.fn()}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /create referral/i }));

    expect(await screen.findByText("Referral category is required.")).toBeInTheDocument();
    expect(await screen.findByText("Referral destination is required.")).toBeInTheDocument();
    expect(await screen.findByText("Referral notes are required.")).toBeInTheDocument();
  });

  it("submits referral when fields are valid", async () => {
    const onSubmit = vi.fn().mockResolvedValue({ success: true });

    render(
      <ReferralForm
        selectedAppointment={{ id: "appt-1", patientId: "patient-1", patientName: "Jane Patient" }}
        onSubmit={onSubmit}
      />
    );

    fireEvent.change(screen.getByLabelText(/referral category/i), {
      target: { value: "counseling" },
    });

    fireEvent.change(screen.getByLabelText(/destination/i), {
      target: { value: "Community Counseling Center" },
    });

    fireEvent.change(screen.getByLabelText(/referral notes/i), {
      target: { value: "Patient requires structured follow-up support." },
    });

    fireEvent.click(screen.getByRole("button", { name: /create referral/i }));

    expect(onSubmit).toHaveBeenCalledTimes(1);
    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        patientId: "patient-1",
        appointmentId: "appt-1",
        category: "counseling",
        destination: "Community Counseling Center",
      })
    );
  });
});
```

---

# 14) Recommended support test for required provider dashboard render outcome  
## `src/pages/provider/__tests__/Dashboard.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";
import ProviderDashboard from "../Dashboard";

vi.mock("../../../modules/appointments/hooks/useAppointments", () => ({
  useAppointments: () => ({
    appointments: [
      {
        id: "appt-1",
        patient_id: "patient-1",
        patient_name: "Jane Patient",
        service_type: "mental_health",
        status: "booked",
        scheduled_at: "2026-05-02T10:00:00Z",
        screening_alert_level: "high",
        screening_alert_text: "High-priority EPDS follow-up flag.",
      },
    ],
    isLoading: false,
    loadError: "",
  }),
}));

describe("ProviderDashboard", () => {
  it("renders provider dashboard appointment context", () => {
    render(
      <MemoryRouter>
        <ProviderDashboard />
      </MemoryRouter>
    );

    expect(screen.getByText("Clinical dashboard")).toBeInTheDocument();
    expect(screen.getByText("Jane Patient")).toBeInTheDocument();
    expect(screen.getByText("High-priority EPDS follow-up flag.")).toBeInTheDocument();
  });
});
```

---

# Exact commands to run after pasting these files

## 1. Run the provider-focused tests
```bash
npx vitest run src/modules/encounters/__tests__/EncounterEditor.test.jsx src/modules/referrals/__tests__/ReferralForm.test.jsx src/pages/provider/__tests__/Dashboard.test.jsx
```

## 2. Start the frontend
```bash
npm run dev
```

## 3. Manual validation flow
After the frontend boots, validate this path:

1. Sign in as a provider  
2. Open the provider dashboard  
3. Confirm provider appointments render  
4. Confirm screening alert visibility is obvious  
5. Open the notes page  
6. Select an appointment  
7. Draft and save an encounter note  
8. Finalize the encounter note  
9. Open the referrals page  
10. Select a patient appointment context  
11. Create a referral  
12. Update referral status from the timeline  

---

# Completion checklist

This phase is complete when all of the following are true:

- provider dashboard renders assigned appointments
- screening alerts are visible from provider-facing pages
- provider notes page shows patient summary context
- encounter note drafting works
- encounter finalization works
- referral creation works
- referral timeline and status updates work
- provider dashboard render test passes
- encounter editor save test passes
- referral submission test passes
- providers can complete their main clinical workflow from the frontend without fallback manual tools

---

# Practical note before Phase 8
Before moving on, verify that the backend remains the source of truth for encounter finalization state and referral lifecycle state. The frontend should make the workflow easy, but final audit-sensitive status should still be enforced by backend rules.
