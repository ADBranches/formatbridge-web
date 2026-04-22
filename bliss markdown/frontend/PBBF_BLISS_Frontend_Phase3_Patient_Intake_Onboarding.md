# PBBF BLISS Frontend — Phase 3 Populated Files  
## Patient Intake and Onboarding Experience

## Objective
Implement the patient onboarding experience for registration completion, consent, and intake capture.

Repository root:

`bliss-telehealth/pbbf-telehealth`

This phase completes the **patient onboarding UI** so that a newly signed-in patient can move through a guided intake flow, save a draft, acknowledge consent, capture emergency-contact details, choose service needs, and submit onboarding data to the backend without manual database intervention.

---

## Phase 3 decisions

### 1. Keep the current modular split
Continue using:

- `src/modules/intake/*` for intake feature logic
- `src/pages/patient/*` for route-level patient-facing page composition

### 2. Guided flow for onboarding
The patient flow in this phase is:

1. Patient signs in
2. Patient lands on dashboard
3. Dashboard detects incomplete onboarding
4. Patient is guided to consent page
5. Patient proceeds to intake form page
6. Patient can save a draft or submit final intake
7. Patient returns to dashboard with onboarding marked complete

### 3. Backend assumptions
This frontend phase assumes your backend Phase 4 intake API exposes endpoints similar to:

- `GET /api/v1/intake/me`
- `POST /api/v1/intake/draft`
- `POST /api/v1/intake/submit`

If your backend uses different route names, only adjust the paths inside:

- `src/modules/intake/services/intakeApi.js`

### 4. Route expectation
This phase needs onboarding routes registered. If your current app route map does not yet include intake routes, I included a small support patch later in this file for:

- `/patient/onboarding/consent`
- `/patient/onboarding/intake`

---

## File list for this phase

### Modify these files
- `src/pages/patient/Dashboard.jsx`
- `src/modules/intake/pages/*`
- `src/modules/intake/components/*`
- `src/modules/intake/hooks/*`
- `src/modules/intake/services/*`

### Create these files if missing
- `src/modules/intake/pages/IntakeFormPage.jsx`
- `src/modules/intake/pages/ConsentPage.jsx`
- `src/modules/intake/components/IntakeForm.jsx`
- `src/modules/intake/components/ConsentCheckboxes.jsx`
- `src/modules/intake/components/EmergencyContactFields.jsx`
- `src/modules/intake/hooks/useIntakeForm.js`
- `src/modules/intake/services/intakeApi.js`
- `src/modules/intake/utils/intakeSchema.js`
- `src/modules/intake/__tests__/IntakeForm.test.jsx`
- `src/modules/intake/__tests__/ConsentPage.test.jsx`

### Recommended support test added for this phase
- `src/modules/intake/__tests__/useIntakeForm.test.jsx`

---

# 1) `src/modules/intake/services/intakeApi.js`

```jsx
import { api } from "../../../services/api";

export function getMyIntakeRequest() {
  return api.get("/intake/me");
}

export function saveIntakeDraftRequest(payload) {
  return api.post("/intake/draft", payload);
}

export function submitIntakeRequest(payload) {
  return api.post("/intake/submit", payload);
}
```

---

# 2) `src/modules/intake/utils/intakeSchema.js`

```jsx
export const SERVICE_NEED_OPTIONS = [
  { value: "mental_health", label: "Mental health support" },
  { value: "lactation", label: "Lactation consultation" },
  { value: "wellness_follow_up", label: "Maternal wellness follow-up" },
  { value: "community_support", label: "Community / social support" },
];

export const PREFERRED_CONTACT_OPTIONS = [
  { value: "email", label: "Email" },
  { value: "sms", label: "SMS" },
  { value: "phone", label: "Phone call" },
];

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
};

export function validatePhone(value) {
  if (!value?.trim()) return "Phone number is required.";
  const compact = value.replace(/\s+/g, "");
  if (compact.length < 7) return "Enter a valid phone number.";
  return "";
}

export function validateDate(value) {
  if (!value) return "Date of birth is required.";
  return "";
}

export function validateEmergencyContact(values) {
  const errors = {
    emergencyContactName: "",
    emergencyContactRelationship: "",
    emergencyContactPhone: "",
  };

  if (!values.emergencyContactName?.trim()) {
    errors.emergencyContactName = "Emergency contact name is required.";
  }

  if (!values.emergencyContactRelationship?.trim()) {
    errors.emergencyContactRelationship = "Emergency contact relationship is required.";
  }

  errors.emergencyContactPhone = validatePhone(values.emergencyContactPhone);

  return errors;
}

export function validateConsent(values) {
  return {
    consentAccepted: values.consentAccepted ? "" : "You must accept care consent.",
    privacyAccepted: values.privacyAccepted ? "" : "You must accept the privacy acknowledgement.",
  };
}

export function validateIntake(values, { requireConsent = true } = {}) {
  const errors = {
    fullName: "",
    dateOfBirth: "",
    phoneNumber: "",
    preferredContactMethod: "",
    serviceNeeds: "",
    postpartumSummary: "",
    emergencyContactName: "",
    emergencyContactRelationship: "",
    emergencyContactPhone: "",
    consentAccepted: "",
    privacyAccepted: "",
  };

  if (!values.fullName?.trim()) {
    errors.fullName = "Full name is required.";
  }

  errors.dateOfBirth = validateDate(values.dateOfBirth);
  errors.phoneNumber = validatePhone(values.phoneNumber);

  if (!values.preferredContactMethod) {
    errors.preferredContactMethod = "Preferred contact method is required.";
  }

  if (!Array.isArray(values.serviceNeeds) || values.serviceNeeds.length === 0) {
    errors.serviceNeeds = "Select at least one service need.";
  }

  if (!values.postpartumSummary?.trim()) {
    errors.postpartumSummary = "Please provide a short onboarding summary.";
  }

  Object.assign(errors, validateEmergencyContact(values));

  if (requireConsent) {
    Object.assign(errors, validateConsent(values));
  }

  return errors;
}

export function hasIntakeErrors(errors) {
  return Object.values(errors).some(Boolean);
}
```

---

# 3) `src/modules/intake/hooks/useIntakeForm.js`

```jsx
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  getMyIntakeRequest,
  saveIntakeDraftRequest,
  submitIntakeRequest,
} from "../services/intakeApi";
import {
  hasIntakeErrors,
  initialIntakeValues,
  validateConsent,
  validateIntake,
} from "../utils/intakeSchema";

export function useIntakeForm() {
  const [values, setValues] = useState(initialIntakeValues);
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [isSavingDraft, setIsSavingDraft] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState("");
  const [draftMessage, setDraftMessage] = useState("");
  const [loadError, setLoadError] = useState("");

  const onboardingComplete = useMemo(() => {
    return Boolean(values?.intakeStatus === "submitted");
  }, [values]);

  const loadInitialData = useCallback(async () => {
    try {
      setIsLoading(true);
      setLoadError("");

      const response = await getMyIntakeRequest();
      const payload = response?.data || response;

      if (payload?.intake) {
        const intake = payload.intake;

        setValues((current) => ({
          ...current,
          fullName: intake.full_name || intake.fullName || current.fullName,
          dateOfBirth: intake.date_of_birth || intake.dateOfBirth || current.dateOfBirth,
          phoneNumber: intake.phone_number || intake.phoneNumber || current.phoneNumber,
          preferredContactMethod:
            intake.preferred_contact_method ||
            intake.preferredContactMethod ||
            current.preferredContactMethod,
          serviceNeeds: intake.service_needs || intake.serviceNeeds || current.serviceNeeds,
          postpartumSummary:
            intake.postpartum_summary || intake.postpartumSummary || current.postpartumSummary,
          emergencyContactName:
            intake.emergency_contact_name ||
            intake.emergencyContactName ||
            current.emergencyContactName,
          emergencyContactRelationship:
            intake.emergency_contact_relationship ||
            intake.emergencyContactRelationship ||
            current.emergencyContactRelationship,
          emergencyContactPhone:
            intake.emergency_contact_phone ||
            intake.emergencyContactPhone ||
            current.emergencyContactPhone,
          consentAccepted: Boolean(
            intake.consent_accepted ?? intake.consentAccepted ?? current.consentAccepted
          ),
          privacyAccepted: Boolean(
            intake.privacy_accepted ?? intake.privacyAccepted ?? current.privacyAccepted
          ),
          intakeStatus: intake.status || intake.intakeStatus || current.intakeStatus,
        }));
      }
    } catch (error) {
      setLoadError(error?.message || "Unable to load intake data.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadInitialData();
  }, [loadInitialData]);

  function updateField(field, value) {
    setValues((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: "" }));
    setSubmitMessage("");
    setDraftMessage("");
  }

  function toggleServiceNeed(value) {
    setValues((current) => {
      const existing = current.serviceNeeds || [];
      const next = existing.includes(value)
        ? existing.filter((item) => item !== value)
        : [...existing, value];

      return { ...current, serviceNeeds: next };
    });

    setErrors((current) => ({ ...current, serviceNeeds: "" }));
  }

  function validateConsentStep() {
    const nextErrors = validateConsent(values);
    setErrors((current) => ({ ...current, ...nextErrors }));
    return !Object.values(nextErrors).some(Boolean);
  }

  async function saveDraft() {
    const nextErrors = validateIntake(values, { requireConsent: false });
    setErrors(nextErrors);

    if (hasIntakeErrors({ ...nextErrors, consentAccepted: "", privacyAccepted: "" })) {
      return { success: false };
    }

    try {
      setIsSavingDraft(true);
      setDraftMessage("");

      const payload = {
        full_name: values.fullName.trim(),
        date_of_birth: values.dateOfBirth,
        phone_number: values.phoneNumber.trim(),
        preferred_contact_method: values.preferredContactMethod,
        service_needs: values.serviceNeeds,
        postpartum_summary: values.postpartumSummary.trim(),
        emergency_contact_name: values.emergencyContactName.trim(),
        emergency_contact_relationship: values.emergencyContactRelationship.trim(),
        emergency_contact_phone: values.emergencyContactPhone.trim(),
        consent_accepted: values.consentAccepted,
        privacy_accepted: values.privacyAccepted,
      };

      const response = await saveIntakeDraftRequest(payload);
      setDraftMessage(response?.message || "Draft saved successfully.");
      return { success: true, response };
    } catch (error) {
      setDraftMessage(error?.message || "Unable to save draft.");
      return { success: false, error };
    } finally {
      setIsSavingDraft(false);
    }
  }

  async function submitIntake() {
    const nextErrors = validateIntake(values, { requireConsent: true });
    setErrors(nextErrors);

    if (hasIntakeErrors(nextErrors)) {
      return { success: false };
    }

    try {
      setIsSubmitting(true);
      setSubmitMessage("");

      const payload = {
        full_name: values.fullName.trim(),
        date_of_birth: values.dateOfBirth,
        phone_number: values.phoneNumber.trim(),
        preferred_contact_method: values.preferredContactMethod,
        service_needs: values.serviceNeeds,
        postpartum_summary: values.postpartumSummary.trim(),
        emergency_contact_name: values.emergencyContactName.trim(),
        emergency_contact_relationship: values.emergencyContactRelationship.trim(),
        emergency_contact_phone: values.emergencyContactPhone.trim(),
        consent_accepted: values.consentAccepted,
        privacy_accepted: values.privacyAccepted,
      };

      const response = await submitIntakeRequest(payload);
      setValues((current) => ({ ...current, intakeStatus: "submitted" }));
      setSubmitMessage(response?.message || "Intake submitted successfully.");
      return { success: true, response };
    } catch (error) {
      setSubmitMessage(error?.message || "Unable to submit intake.");
      return { success: false, error };
    } finally {
      setIsSubmitting(false);
    }
  }

  return {
    values,
    errors,
    isLoading,
    isSavingDraft,
    isSubmitting,
    submitMessage,
    draftMessage,
    loadError,
    onboardingComplete,
    updateField,
    toggleServiceNeed,
    validateConsentStep,
    saveDraft,
    submitIntake,
    reload: loadInitialData,
  };
}
```

---

# 4) `src/modules/intake/components/ConsentCheckboxes.jsx`

```jsx
export default function ConsentCheckboxes({
  consentAccepted,
  privacyAccepted,
  errors = {},
  onChange,
}) {
  return (
    <div className="space-y-5">
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
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
            I acknowledge the privacy notice and understand that my information will be used to
            support care coordination, screening, scheduling, and follow-up.
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

# 5) `src/modules/intake/components/EmergencyContactFields.jsx`

```jsx
export default function EmergencyContactFields({ values, errors = {}, onChange }) {
  return (
    <div className="space-y-5 rounded-2xl border border-slate-200 bg-white p-5">
      <div>
        <h3 className="text-lg font-semibold text-slate-900">Emergency contact</h3>
        <p className="mt-1 text-sm text-slate-600">
          This helps the care team support safer follow-up when needed.
        </p>
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">
          Emergency contact name
        </label>
        <input
          type="text"
          value={values.emergencyContactName}
          onChange={(event) => onChange("emergencyContactName", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="Enter emergency contact name"
        />
        {errors.emergencyContactName ? (
          <p className="mt-2 text-sm text-rose-600">{errors.emergencyContactName}</p>
        ) : null}
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">
          Relationship
        </label>
        <input
          type="text"
          value={values.emergencyContactRelationship}
          onChange={(event) => onChange("emergencyContactRelationship", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="Example: Sister, spouse, parent"
        />
        {errors.emergencyContactRelationship ? (
          <p className="mt-2 text-sm text-rose-600">{errors.emergencyContactRelationship}</p>
        ) : null}
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">
          Emergency contact phone
        </label>
        <input
          type="tel"
          value={values.emergencyContactPhone}
          onChange={(event) => onChange("emergencyContactPhone", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="Enter emergency contact phone"
        />
        {errors.emergencyContactPhone ? (
          <p className="mt-2 text-sm text-rose-600">{errors.emergencyContactPhone}</p>
        ) : null}
      </div>
    </div>
  );
}
```

---

# 6) `src/modules/intake/components/IntakeForm.jsx`

```jsx
import EmergencyContactFields from "./EmergencyContactFields";
import { PREFERRED_CONTACT_OPTIONS, SERVICE_NEED_OPTIONS } from "../utils/intakeSchema";

export default function IntakeForm({
  values,
  errors = {},
  onChange,
  onToggleServiceNeed,
  onSaveDraft,
  onSubmit,
  isSavingDraft = false,
  isSubmitting = false,
  draftMessage = "",
  submitMessage = "",
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
      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-xl font-semibold text-slate-900">Basic profile</h2>
        <p className="mt-1 text-sm text-slate-600">
          Complete your profile so the care team can prepare the right support path.
        </p>

        <div className="mt-6 grid gap-5 md:grid-cols-2">
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Full name</label>
            <input
              type="text"
              value={values.fullName}
              onChange={(event) => onChange("fullName", event.target.value)}
              className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
              placeholder="Enter your full name"
            />
            {errors.fullName ? (
              <p className="mt-2 text-sm text-rose-600">{errors.fullName}</p>
            ) : null}
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Date of birth</label>
            <input
              type="date"
              value={values.dateOfBirth}
              onChange={(event) => onChange("dateOfBirth", event.target.value)}
              className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            />
            {errors.dateOfBirth ? (
              <p className="mt-2 text-sm text-rose-600">{errors.dateOfBirth}</p>
            ) : null}
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Phone number</label>
            <input
              type="tel"
              value={values.phoneNumber}
              onChange={(event) => onChange("phoneNumber", event.target.value)}
              className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
              placeholder="Enter your phone number"
            />
            {errors.phoneNumber ? (
              <p className="mt-2 text-sm text-rose-600">{errors.phoneNumber}</p>
            ) : null}
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Preferred contact method
            </label>
            <select
              value={values.preferredContactMethod}
              onChange={(event) => onChange("preferredContactMethod", event.target.value)}
              className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            >
              {PREFERRED_CONTACT_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            {errors.preferredContactMethod ? (
              <p className="mt-2 text-sm text-rose-600">{errors.preferredContactMethod}</p>
            ) : null}
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-xl font-semibold text-slate-900">Service needs</h2>
        <p className="mt-1 text-sm text-slate-600">
          Select the support areas that best describe what you need right now.
        </p>

        <div className="mt-6 grid gap-3 md:grid-cols-2">
          {SERVICE_NEED_OPTIONS.map((option) => {
            const selected = values.serviceNeeds.includes(option.value);

            return (
              <button
                key={option.value}
                type="button"
                onClick={() => onToggleServiceNeed(option.value)}
                className={`rounded-2xl border px-4 py-4 text-left transition ${
                  selected
                    ? "border-sky-700 bg-sky-50 text-sky-900"
                    : "border-slate-200 bg-white text-slate-700 hover:border-slate-300"
                }`}
              >
                <span className="block text-sm font-medium">{option.label}</span>
              </button>
            );
          })}
        </div>

        {errors.serviceNeeds ? (
          <p className="mt-3 text-sm text-rose-600">{errors.serviceNeeds}</p>
        ) : null}
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-xl font-semibold text-slate-900">Short postpartum summary</h2>
        <p className="mt-1 text-sm text-slate-600">
          Give a short description of your current needs, concerns, or follow-up goals.
        </p>

        <div className="mt-6">
          <textarea
            rows={5}
            value={values.postpartumSummary}
            onChange={(event) => onChange("postpartumSummary", event.target.value)}
            className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            placeholder="Describe what kind of support you are looking for..."
          />
          {errors.postpartumSummary ? (
            <p className="mt-2 text-sm text-rose-600">{errors.postpartumSummary}</p>
          ) : null}
        </div>
      </div>

      <EmergencyContactFields values={values} errors={errors} onChange={onChange} />

      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div className="text-sm text-slate-600">
            Save a draft if you want to continue later, or submit when your onboarding is complete.
          </div>

          <div className="flex flex-col gap-3 sm:flex-row">
            <button
              type="button"
              onClick={onSaveDraft}
              disabled={isSavingDraft}
              className="rounded-xl border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isSavingDraft ? "Saving draft..." : "Save draft"}
            </button>

            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-xl bg-sky-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isSubmitting ? "Submitting..." : "Submit onboarding"}
            </button>
          </div>
        </div>

        {draftMessage ? (
          <p className="mt-4 text-sm text-slate-700">{draftMessage}</p>
        ) : null}

        {submitMessage ? (
          <p className="mt-2 text-sm text-slate-700">{submitMessage}</p>
        ) : null}
      </div>
    </form>
  );
}
```

---

# 7) `src/modules/intake/pages/ConsentPage.jsx`

```jsx
import { useNavigate } from "react-router-dom";
import ConsentCheckboxes from "../components/ConsentCheckboxes";
import { useIntakeForm } from "../hooks/useIntakeForm";
import Loader from "../../../shared/components/Loader";
import ErrorState from "../../../shared/components/ErrorState";

export default function ConsentPage() {
  const navigate = useNavigate();
  const {
    values,
    errors,
    isLoading,
    loadError,
    updateField,
    validateConsentStep,
  } = useIntakeForm();

  function handleContinue() {
    const valid = validateConsentStep();
    if (!valid) return;
    navigate("/patient/onboarding/intake");
  }

  if (isLoading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <Loader label="Loading onboarding..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load consent step" message={loadError} />;
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-sky-700">
          Patient onboarding
        </p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Consent and privacy</h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          Before continuing with intake, please acknowledge the care consent and privacy notice.
        </p>

        <div className="mt-8">
          <ConsentCheckboxes
            consentAccepted={values.consentAccepted}
            privacyAccepted={values.privacyAccepted}
            errors={errors}
            onChange={updateField}
          />
        </div>

        <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-end">
          <button
            type="button"
            onClick={handleContinue}
            className="rounded-xl bg-sky-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-800"
          >
            Continue to intake
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

# 8) `src/modules/intake/pages/IntakeFormPage.jsx`

```jsx
import { useNavigate } from "react-router-dom";
import Loader from "../../../shared/components/Loader";
import ErrorState from "../../../shared/components/ErrorState";
import IntakeForm from "../components/IntakeForm";
import { useIntakeForm } from "../hooks/useIntakeForm";

export default function IntakeFormPage() {
  const navigate = useNavigate();
  const {
    values,
    errors,
    isLoading,
    isSavingDraft,
    isSubmitting,
    draftMessage,
    submitMessage,
    loadError,
    updateField,
    toggleServiceNeed,
    saveDraft,
    submitIntake,
  } = useIntakeForm();

  async function handleSubmit() {
    const result = await submitIntake();
    if (result?.success) {
      navigate("/patient", { replace: true });
    }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <Loader label="Loading intake form..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load intake form" message={loadError} />;
  }

  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <div className="mb-8">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-sky-700">
          Patient onboarding
        </p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">
          Complete your intake form
        </h1>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
          Finish your onboarding details so the care team can prepare the right care pathway,
          scheduling support, and follow-up plan.
        </p>
      </div>

      <IntakeForm
        values={values}
        errors={errors}
        onChange={updateField}
        onToggleServiceNeed={toggleServiceNeed}
        onSaveDraft={saveDraft}
        onSubmit={handleSubmit}
        isSavingDraft={isSavingDraft}
        isSubmitting={isSubmitting}
        draftMessage={draftMessage}
        submitMessage={submitMessage}
      />
    </div>
  );
}
```

---

# 9) `src/pages/patient/Dashboard.jsx`

```jsx
import { Link } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import { useIntakeForm } from "../../modules/intake/hooks/useIntakeForm";
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";

export default function PatientDashboard() {
  const user = useAuthStore((state) => state.user);
  const { values, isLoading, loadError, onboardingComplete } = useIntakeForm();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading patient dashboard..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load patient dashboard" message={loadError} />;
  }

  const firstName =
    user?.full_name?.split(" ")[0] ||
    user?.fullName?.split(" ")[0] ||
    "Patient";

  return (
    <div className="space-y-8">
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Patient dashboard</p>
        <h1 className="mt-2 text-3xl font-semibold">Welcome back, {firstName}.</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Use this dashboard to complete onboarding, manage appointments, access telehealth,
          review care plans, and follow up with the Post Baby Bliss Foundation care team.
        </p>
      </section>

      {!onboardingComplete ? (
        <section className="rounded-3xl border border-amber-200 bg-amber-50 p-6">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-amber-900">Complete your onboarding</h2>
              <p className="mt-2 text-sm leading-6 text-amber-800">
                Your intake is not submitted yet. Finish consent and onboarding so scheduling and
                care routing can continue without staff-side manual work.
              </p>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row">
              <Link
                to="/patient/onboarding/consent"
                className="rounded-xl bg-amber-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-amber-700"
              >
                Continue onboarding
              </Link>
            </div>
          </div>
        </section>
      ) : (
        <section className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6">
          <h2 className="text-xl font-semibold text-emerald-900">Onboarding complete</h2>
          <p className="mt-2 text-sm leading-6 text-emerald-800">
            Your onboarding has been submitted successfully. The care team can now use your intake
            details for triage, scheduling, and follow-up.
          </p>
        </section>
      )}

      <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Current intake status</h3>
          <p className="mt-2 text-sm text-slate-600">
            Status: <span className="font-medium capitalize">{values.intakeStatus || "not started"}</span>
          </p>
          <p className="mt-2 text-sm text-slate-600">
            Service needs selected:{" "}
            <span className="font-medium">
              {values.serviceNeeds?.length ? values.serviceNeeds.join(", ") : "None yet"}
            </span>
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Next step</h3>
          <p className="mt-2 text-sm text-slate-600">
            {onboardingComplete
              ? "Watch for scheduling and follow-up updates from the care team."
              : "Finish your consent and intake flow to unlock the rest of the patient journey."}
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Preferred contact</h3>
          <p className="mt-2 text-sm text-slate-600">
            {values.preferredContactMethod
              ? values.preferredContactMethod
              : "Not selected yet"}
          </p>
        </div>
      </section>
    </div>
  );
}
```

---

# 10) `src/modules/intake/__tests__/IntakeForm.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import IntakeForm from "../components/IntakeForm";

describe("IntakeForm", () => {
  const baseProps = {
    values: {
      fullName: "",
      dateOfBirth: "",
      phoneNumber: "",
      preferredContactMethod: "email",
      serviceNeeds: [],
      postpartumSummary: "",
      emergencyContactName: "",
      emergencyContactRelationship: "",
      emergencyContactPhone: "",
    },
    errors: {},
    onChange: vi.fn(),
    onToggleServiceNeed: vi.fn(),
    onSaveDraft: vi.fn(),
    onSubmit: vi.fn(),
    isSavingDraft: false,
    isSubmitting: false,
    draftMessage: "",
    submitMessage: "",
  };

  it("renders intake form sections", () => {
    render(<IntakeForm {...baseProps} />);

    expect(screen.getByText("Basic profile")).toBeInTheDocument();
    expect(screen.getByText("Service needs")).toBeInTheDocument();
    expect(screen.getByText("Emergency contact")).toBeInTheDocument();
  });

  it("calls save draft callback", () => {
    const onSaveDraft = vi.fn();
    render(<IntakeForm {...baseProps} onSaveDraft={onSaveDraft} />);

    fireEvent.click(screen.getByRole("button", { name: /save draft/i }));
    expect(onSaveDraft).toHaveBeenCalledTimes(1);
  });

  it("calls submit callback", () => {
    const onSubmit = vi.fn();
    render(<IntakeForm {...baseProps} onSubmit={onSubmit} />);

    fireEvent.click(screen.getByRole("button", { name: /submit onboarding/i }));
    expect(onSubmit).toHaveBeenCalledTimes(1);
  });
});
```

---

# 11) `src/modules/intake/__tests__/ConsentPage.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";
import ConsentPage from "../pages/ConsentPage";

const navigateMock = vi.fn();
const validateConsentStepMock = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => navigateMock,
  };
});

vi.mock("../hooks/useIntakeForm", () => ({
  useIntakeForm: () => ({
    values: {
      consentAccepted: false,
      privacyAccepted: false,
    },
    errors: {},
    isLoading: false,
    loadError: "",
    updateField: vi.fn(),
    validateConsentStep: validateConsentStepMock,
  }),
}));

describe("ConsentPage", () => {
  beforeEach(() => {
    navigateMock.mockReset();
    validateConsentStepMock.mockReset();
  });

  it("renders consent page text", () => {
    render(
      <MemoryRouter>
        <ConsentPage />
      </MemoryRouter>
    );

    expect(screen.getByText("Consent and privacy")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /continue to intake/i })).toBeInTheDocument();
  });

  it("does not navigate when consent validation fails", () => {
    validateConsentStepMock.mockReturnValue(false);

    render(
      <MemoryRouter>
        <ConsentPage />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /continue to intake/i }));

    expect(validateConsentStepMock).toHaveBeenCalledTimes(1);
    expect(navigateMock).not.toHaveBeenCalled();
  });

  it("navigates to intake page when consent validation succeeds", () => {
    validateConsentStepMock.mockReturnValue(true);

    render(
      <MemoryRouter>
        <ConsentPage />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /continue to intake/i }));

    expect(navigateMock).toHaveBeenCalledWith("/patient/onboarding/intake");
  });
});
```

---

# 12) Recommended support test: `src/modules/intake/__tests__/useIntakeForm.test.jsx`

```jsx
import { renderHook } from "@testing-library/react";
import { vi } from "vitest";
import { useIntakeForm } from "../hooks/useIntakeForm";

vi.mock("../services/intakeApi", () => ({
  getMyIntakeRequest: vi.fn().mockResolvedValue({ data: {} }),
  saveIntakeDraftRequest: vi.fn().mockResolvedValue({ message: "Draft saved successfully." }),
  submitIntakeRequest: vi.fn().mockResolvedValue({ message: "Intake submitted successfully." }),
}));

describe("useIntakeForm", () => {
  it("loads with default state", async () => {
    const { result } = renderHook(() => useIntakeForm());
    expect(result.current.values.fullName).toBe("");
  });
});
```

---

# 13) Required support patch for route registration: `src/app/AppRoutes.jsx`

This intake phase needs route registration or the new pages cannot be accessed from the UI.

Merge these routes into your existing `src/app/AppRoutes.jsx`:

```jsx
import { Navigate, Route, Routes } from "react-router-dom";
import ProtectedRoute from "../routes/ProtectedRoute";

import Login from "../pages/auth/Login";
import Register from "../modules/auth/pages/Register";
import ForgotPassword from "../modules/auth/pages/ForgotPassword";

import PatientDashboard from "../pages/patient/Dashboard";
import ProviderDashboard from "../pages/provider/Dashboard";
import AdminDashboard from "../pages/admin/Dashboard";

import ConsentPage from "../modules/intake/pages/ConsentPage";
import IntakeFormPage from "../modules/intake/pages/IntakeFormPage";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />

      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      <Route
        path="/patient"
        element={
          <ProtectedRoute allowedRoles={["patient"]}>
            <PatientDashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/patient/onboarding/consent"
        element={
          <ProtectedRoute allowedRoles={["patient"]}>
            <ConsentPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/patient/onboarding/intake"
        element={
          <ProtectedRoute allowedRoles={["patient"]}>
            <IntakeFormPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/provider"
        element={
          <ProtectedRoute allowedRoles={["provider", "counselor", "care_coordinator"]}>
            <ProviderDashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin"
        element={
          <ProtectedRoute allowedRoles={["admin"]}>
            <AdminDashboard />
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
```

---

# 14) Optional support patch for patient navigation: `src/shared/constants/navigation.js`

If your sidebar uses a central navigation map, add patient onboarding visibility here:

```jsx
export const navigationByRole = {
  patient: [
    { label: "Dashboard", to: "/patient" },
    { label: "Onboarding", to: "/patient/onboarding/consent" },
    { label: "Appointments", to: "/patient/appointments" },
    { label: "Screening", to: "/patient/screening" },
    { label: "Session", to: "/patient/session" },
    { label: "Care Plan", to: "/patient/care-plan" },
  ],
  provider: [
    { label: "Dashboard", to: "/provider" },
  ],
  admin: [
    { label: "Dashboard", to: "/admin" },
  ],
};
```

---

# Exact commands to run after pasting these files

## 1. Run the intake-focused tests
```bash
npx vitest run src/modules/intake/__tests__/IntakeForm.test.jsx src/modules/intake/__tests__/ConsentPage.test.jsx src/modules/intake/__tests__/useIntakeForm.test.jsx
```

## 2. Start the frontend
```bash
npm run dev
```

## 3. Manual validation flow
After the frontend boots, validate this path:

1. Sign in as a patient  
2. Open `/patient`  
3. Click **Continue onboarding**  
4. Try continuing without consent — it should block progress  
5. Accept consent and privacy  
6. Continue to intake form  
7. Fill the fields  
8. Save a draft  
9. Submit the onboarding  
10. Confirm redirect back to `/patient`

---

# Completion checklist

This phase is complete when all of the following are true:

- patient dashboard shows onboarding status clearly
- consent page is accessible only to patient role
- intake form is accessible only after sign-in
- required field validation is visible in the UI
- service need selection works
- emergency contact details are captured
- draft save works from the UI
- final submit works from the UI
- consent acknowledgement is required for final submission
- patient can complete onboarding without manual database editing
- intake tests pass cleanly

---

# Practical note before Phase 4
Before moving on, verify that the backend intake response fields match what this frontend expects. If your API uses only snake_case or only camelCase, standardize now to avoid repeated adapter logic in later modules.
