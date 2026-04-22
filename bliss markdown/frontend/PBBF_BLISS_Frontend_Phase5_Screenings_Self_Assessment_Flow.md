# PBBF BLISS Frontend — Phase 5 Populated Files
## Screenings and Patient Self-Assessment Flow

## Objective
Build the EPDS experience in a patient-safe, readable, form-driven interface.

Repository root:

`bliss-telehealth/pbbf-telehealth`

This phase completes the patient-facing screening experience so that a signed-in patient can:

- open the screening page
- answer a guided EPDS-style questionnaire
- receive a clear completion confirmation
- see a readable score summary after submission
- view prior screenings where allowed by the backend
- avoid broken form state and confusing navigation

---

## Important Phase 5 decisions

### 1. Keep the current split
Continue using:

- `src/modules/screenings/*` for screening feature logic
- `src/pages/patient/*` for patient route-level page composition

### 2. Use the shared API client
Keep:

- `src/services/api.js`

as the single canonical API client.

### 3. Clinical content safety note
This phase intentionally keeps the questionnaire text in a **safe development-ready structure**. For real clinical deployment, the final wording shown to patients should be reviewed and approved by the responsible clinical team and aligned with the exact instrument version the organization intends to use.

That means:
- keep the structure, scoring, and flow here
- replace any placeholder or simplified wording with the approved screening copy before release
- do not let ad hoc UI edits change clinical wording later without review

### 4. Backend assumptions
This frontend phase assumes the backend screening API exposes routes similar to:

- `GET /api/v1/screenings/me`
- `POST /api/v1/screenings/epds`

If your real backend paths differ, update only:

- `src/modules/screenings/services/screeningsApi.js`

### 5. UX flow
The patient-facing screening flow in this phase is:

1. patient opens the screening page  
2. prior screening history loads  
3. current questionnaire renders  
4. patient answers all questions  
5. patient submits  
6. result summary displays  
7. page refresh reflects backend-driven prior screening history  

---

## File list for this phase

### Modify these files
- `src/pages/patient/Screening.jsx`
- `src/modules/screenings/pages/*`
- `src/modules/screenings/components/*`
- `src/modules/screenings/hooks/*`
- `src/modules/screenings/services/*`

### Create these files if missing
- `src/modules/screenings/components/EpdsQuestionnaire.jsx`
- `src/modules/screenings/components/ScoreSummaryCard.jsx`
- `src/modules/screenings/hooks/useEpdsForm.js`
- `src/modules/screenings/services/screeningsApi.js`
- `src/modules/screenings/utils/epdsQuestions.js`
- `src/modules/screenings/__tests__/EpdsQuestionnaire.test.jsx`
- `src/modules/screenings/__tests__/ScreeningPage.test.jsx`

### Recommended support test
- `src/modules/screenings/__tests__/useEpdsForm.test.jsx`

---

# 1) `src/modules/screenings/utils/epdsQuestions.js`

```jsx
export const EPDS_OPTIONS = [
  { label: "Not at all / none", value: 0 },
  { label: "Sometimes / a little", value: 1 },
  { label: "Often / moderate", value: 2 },
  { label: "Most of the time / strong", value: 3 },
];

export const EPDS_QUESTIONS = [
  {
    id: "q1",
    title: "Question 1",
    prompt: "Over the past week, how often have you been able to feel positive enjoyment in daily life?",
  },
  {
    id: "q2",
    title: "Question 2",
    prompt: "Over the past week, how often have you felt hopeful or looked forward to things?",
  },
  {
    id: "q3",
    title: "Question 3",
    prompt: "Over the past week, how often have you blamed yourself unfairly when things felt difficult?",
  },
  {
    id: "q4",
    title: "Question 4",
    prompt: "Over the past week, how often have you felt worried or tense without feeling settled?",
  },
  {
    id: "q5",
    title: "Question 5",
    prompt: "Over the past week, how often have you felt overwhelmed or unsettled in a way that was hard to manage?",
  },
  {
    id: "q6",
    title: "Question 6",
    prompt: "Over the past week, how often have you found coping with daily responsibilities difficult?",
  },
  {
    id: "q7",
    title: "Question 7",
    prompt: "Over the past week, how often have you had trouble resting or sleeping because of emotional distress?",
  },
  {
    id: "q8",
    title: "Question 8",
    prompt: "Over the past week, how often have you felt sad or emotionally low?",
  },
  {
    id: "q9",
    title: "Question 9",
    prompt: "Over the past week, how often have you felt tearful or close to crying?",
  },
  {
    id: "q10",
    title: "Question 10",
    prompt: "Over the past week, have you experienced a serious emotional safety concern that should be followed up promptly by the care team?",
    helperText:
      "This final item is safety-sensitive. The care team should review it carefully when selected above the lowest option.",
    isSafetySensitive: true,
  },
];

export function getInitialAnswers() {
  return EPDS_QUESTIONS.reduce((accumulator, question) => {
    accumulator[question.id] = null;
    return accumulator;
  }, {});
}

export function areAllQuestionsAnswered(answers) {
  return EPDS_QUESTIONS.every((question) => answers[question.id] !== null);
}

export function calculateEpdsScore(answers) {
  return EPDS_QUESTIONS.reduce((total, question) => {
    const value = Number(answers[question.id] ?? 0);
    return total + value;
  }, 0);
}

export function classifyEpdsBand(score) {
  if (score <= 9) return "lower concern range";
  if (score <= 12) return "moderate follow-up range";
  return "higher follow-up range";
}

export function hasSafetyFlag(answers) {
  return Number(answers.q10 ?? 0) > 0;
}
```

---

# 2) `src/modules/screenings/services/screeningsApi.js`

```jsx
import { api } from "../../../services/api";

export function listMyScreeningsRequest() {
  return api.get("/screenings/me");
}

export function submitEpdsRequest(payload) {
  return api.post("/screenings/epds", payload);
}
```

---

# 3) `src/modules/screenings/hooks/useEpdsForm.js`

```jsx
import { useCallback, useEffect, useMemo, useState } from "react";
import { listMyScreeningsRequest, submitEpdsRequest } from "../services/screeningsApi";
import {
  areAllQuestionsAnswered,
  calculateEpdsScore,
  classifyEpdsBand,
  getInitialAnswers,
  hasSafetyFlag,
} from "../utils/epdsQuestions";

function normalizeScreening(raw) {
  return {
    id: raw?.id || raw?.screening_id || "temp-screening-id",
    submittedAt: raw?.submitted_at || raw?.submittedAt || raw?.created_at || "",
    score: raw?.score ?? 0,
    band: raw?.band || raw?.severity_band || "lower concern range",
    status: raw?.status || "completed",
    safetyFlag: Boolean(raw?.safety_flag ?? raw?.critical_flag ?? false),
  };
}

export function useEpdsForm() {
  const [answers, setAnswers] = useState(getInitialAnswers());
  const [priorScreenings, setPriorScreenings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loadError, setLoadError] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [completionMessage, setCompletionMessage] = useState("");
  const [submittedSummary, setSubmittedSummary] = useState(null);

  const localScore = useMemo(() => calculateEpdsScore(answers), [answers]);
  const localBand = useMemo(() => classifyEpdsBand(localScore), [localScore]);
  const localSafetyFlag = useMemo(() => hasSafetyFlag(answers), [answers]);

  const loadHistory = useCallback(async () => {
    try {
      setIsLoading(true);
      setLoadError("");

      const response = await listMyScreeningsRequest();
      const payload = response?.data || response;
      const rows = payload?.screenings || payload || [];

      setPriorScreenings(rows.map(normalizeScreening));
    } catch (error) {
      setLoadError(error?.message || "Unable to load screening history.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  function setAnswer(questionId, value) {
    setAnswers((current) => ({
      ...current,
      [questionId]: Number(value),
    }));
    setSubmitError("");
    setCompletionMessage("");
  }

  function resetForm() {
    setAnswers(getInitialAnswers());
    setSubmitError("");
    setCompletionMessage("");
    setSubmittedSummary(null);
  }

  async function submit() {
    if (!areAllQuestionsAnswered(answers)) {
      setSubmitError("Please answer all questions before submitting the screening.");
      return { success: false };
    }

    try {
      setIsSubmitting(true);
      setSubmitError("");

      const payload = {
        answers: Object.entries(answers).map(([question_id, score]) => ({
          question_id,
          score,
        })),
      };

      const response = await submitEpdsRequest(payload);
      const data = response?.data || response;

      const summary = {
        score: data?.score ?? localScore,
        band: data?.band || localBand,
        safetyFlag: Boolean(data?.safety_flag ?? localSafetyFlag),
      };

      setSubmittedSummary(summary);
      setCompletionMessage(
        response?.message || "Your screening has been submitted successfully."
      );

      await loadHistory();

      return { success: true, response, summary };
    } catch (error) {
      setSubmitError(error?.message || "Unable to submit screening.");
      return { success: false, error };
    } finally {
      setIsSubmitting(false);
    }
  }

  return {
    answers,
    priorScreenings,
    isLoading,
    isSubmitting,
    loadError,
    submitError,
    completionMessage,
    submittedSummary,
    localScore,
    localBand,
    localSafetyFlag,
    setAnswer,
    submit,
    resetForm,
    reload: loadHistory,
  };
}
```

---

# 4) `src/modules/screenings/components/EpdsQuestionnaire.jsx`

```jsx
import { EPDS_OPTIONS, EPDS_QUESTIONS } from "../utils/epdsQuestions";

export default function EpdsQuestionnaire({
  answers,
  onAnswer,
  onSubmit,
  isSubmitting = false,
  submitError = "",
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
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-sky-700">
          Patient screening
        </p>
        <h2 className="mt-2 text-2xl font-semibold text-slate-900">
          Complete the self-assessment
        </h2>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          Answer each item based on the last week. Choose the option that feels closest to your experience.
        </p>
      </div>

      {EPDS_QUESTIONS.map((question, index) => (
        <section
          key={question.id}
          className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <div className="mb-5">
            <p className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
              {question.title} of {EPDS_QUESTIONS.length}
            </p>
            <h3 className="mt-2 text-lg font-semibold text-slate-900">
              {question.prompt}
            </h3>
            {question.helperText ? (
              <p className="mt-2 text-sm leading-6 text-slate-600">{question.helperText}</p>
            ) : null}
          </div>

          <div className="grid gap-3">
            {EPDS_OPTIONS.map((option) => {
              const checked = answers[question.id] === option.value;

              return (
                <label
                  key={`${question.id}-${option.value}`}
                  className={`flex cursor-pointer items-start gap-3 rounded-2xl border px-4 py-4 transition ${
                    checked
                      ? "border-sky-700 bg-sky-50"
                      : "border-slate-200 bg-white hover:border-slate-300"
                  }`}
                >
                  <input
                    type="radio"
                    name={question.id}
                    checked={checked}
                    onChange={() => onAnswer(question.id, option.value)}
                    className="mt-1 h-4 w-4 border-slate-300 text-sky-700 focus:ring-sky-500"
                  />
                  <span className="text-sm leading-6 text-slate-700">{option.label}</span>
                </label>
              );
            })}
          </div>
        </section>
      ))}

      {submitError ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {submitError}
        </div>
      ) : null}

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded-xl bg-sky-700 px-6 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isSubmitting ? "Submitting..." : "Submit screening"}
        </button>
      </div>
    </form>
  );
}
```

---

# 5) `src/modules/screenings/components/ScoreSummaryCard.jsx`

```jsx
function formatSubmittedAt(value) {
  if (!value) return "Not available";
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function ScreeningHistoryList({ screenings = [] }) {
  if (!screenings.length) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm">
        No prior screenings are visible yet.
      </div>
    );
  }

  return (
    <div className="grid gap-4">
      {screenings.map((screening) => (
        <div
          key={screening.id}
          className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
        >
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-sm font-semibold text-slate-900">
                Screening submitted {formatSubmittedAt(screening.submittedAt)}
              </p>
              <p className="mt-1 text-sm text-slate-600">
                Score: <span className="font-medium">{screening.score}</span>
              </p>
              <p className="mt-1 text-sm text-slate-600">
                Band: <span className="font-medium capitalize">{screening.band}</span>
              </p>
            </div>

            <div className="text-sm text-slate-600">
              {screening.safetyFlag ? "Marked for provider follow-up." : "No urgent flag shown."}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

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

      {completionMessage ? (
        <p className="mt-3 text-sm leading-6 text-emerald-800">{completionMessage}</p>
      ) : null}

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
            Care team note
          </p>
          <p className="mt-2 text-sm font-medium text-slate-900">
            {safetyFlag
              ? "A provider follow-up review may be needed."
              : "Your result has been recorded for normal care review."}
          </p>
        </div>
      </div>
    </div>
  );
}
```

---

# 6) `src/pages/patient/Screening.jsx`

```jsx
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";
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
    return <ErrorState title="Unable to load screening" message={loadError} />;
  }

  return (
    <div className="space-y-8">
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Patient screening</p>
        <h1 className="mt-2 text-3xl font-semibold">Self-assessment</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Complete your screening in one guided flow. Your responses are submitted to the care team
          so they can review follow-up needs and continue support planning.
        </p>
      </section>

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

      <section className="space-y-4">
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">Prior screenings</h2>
          <p className="mt-1 text-sm text-slate-600">
            Previous submissions are shown here when available from the backend.
          </p>
        </div>

        <ScreeningHistoryList screenings={priorScreenings} />
      </section>
    </div>
  );
}
```

---

# 7) `src/modules/screenings/__tests__/EpdsQuestionnaire.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import EpdsQuestionnaire from "../components/EpdsQuestionnaire";
import { getInitialAnswers } from "../utils/epdsQuestions";

describe("EpdsQuestionnaire", () => {
  it("renders questionnaire and submit button", () => {
    render(
      <EpdsQuestionnaire
        answers={getInitialAnswers()}
        onAnswer={vi.fn()}
        onSubmit={vi.fn()}
      />
    );

    expect(screen.getByText("Complete the self-assessment")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /submit screening/i })).toBeInTheDocument();
  });

  it("calls submit handler when submit button is clicked", () => {
    const onSubmit = vi.fn();

    render(
      <EpdsQuestionnaire
        answers={getInitialAnswers()}
        onAnswer={vi.fn()}
        onSubmit={onSubmit}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /submit screening/i }));
    expect(onSubmit).toHaveBeenCalledTimes(1);
  });

  it("shows submit error message when provided", () => {
    render(
      <EpdsQuestionnaire
        answers={getInitialAnswers()}
        onAnswer={vi.fn()}
        onSubmit={vi.fn()}
        submitError="Please answer all questions before submitting the screening."
      />
    );

    expect(
      screen.getByText("Please answer all questions before submitting the screening.")
    ).toBeInTheDocument();
  });
});
```

---

# 8) `src/modules/screenings/__tests__/ScreeningPage.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import PatientScreeningPage from "../../../pages/patient/Screening";

vi.mock("../hooks/useEpdsForm", () => ({
  useEpdsForm: () => ({
    answers: {
      q1: null,
      q2: null,
      q3: null,
      q4: null,
      q5: null,
      q6: null,
      q7: null,
      q8: null,
      q9: null,
      q10: null,
    },
    priorScreenings: [
      {
        id: "screen-1",
        submittedAt: "2026-05-03T09:00:00Z",
        score: 8,
        band: "lower concern range",
        status: "completed",
        safetyFlag: false,
      },
    ],
    isLoading: false,
    isSubmitting: false,
    loadError: "",
    submitError: "",
    completionMessage: "Your screening has been submitted successfully.",
    submittedSummary: {
      score: 8,
      band: "lower concern range",
      safetyFlag: false,
    },
    setAnswer: vi.fn(),
    submit: vi.fn(),
  }),
}));

describe("PatientScreeningPage", () => {
  it("renders screening page sections", () => {
    render(<PatientScreeningPage />);

    expect(screen.getByText("Self-assessment")).toBeInTheDocument();
    expect(screen.getByText("Prior screenings")).toBeInTheDocument();
    expect(screen.getByText("Submission received")).toBeInTheDocument();
  });
});
```

---

# 9) Recommended support test: `src/modules/screenings/__tests__/useEpdsForm.test.jsx`

```jsx
import { renderHook, act } from "@testing-library/react";
import { vi } from "vitest";
import { useEpdsForm } from "../hooks/useEpdsForm";

vi.mock("../services/screeningsApi", () => ({
  listMyScreeningsRequest: vi.fn().mockResolvedValue({ data: { screenings: [] } }),
  submitEpdsRequest: vi.fn().mockResolvedValue({
    data: { score: 8, band: "lower concern range", safety_flag: false },
    message: "Your screening has been submitted successfully.",
  }),
}));

describe("useEpdsForm", () => {
  it("blocks submit when required answers are missing", async () => {
    const { result } = renderHook(() => useEpdsForm());

    await act(async () => {
      await result.current.submit();
    });

    expect(result.current.submitError).toBe(
      "Please answer all questions before submitting the screening."
    );
  });
});
```

---

# 10) Required support patch for route registration: `src/app/AppRoutes.jsx`

Merge the screening route into your existing route map:

```jsx
import { Navigate, Route, Routes } from "react-router-dom";
import ProtectedRoute from "../routes/ProtectedRoute";

import Login from "../pages/auth/Login";
import Register from "../modules/auth/pages/Register";
import ForgotPassword from "../modules/auth/pages/ForgotPassword";

import PatientDashboard from "../pages/patient/Dashboard";
import PatientAppointmentsPage from "../pages/patient/Appointments";
import PatientScreeningPage from "../pages/patient/Screening";
import ProviderDashboard from "../pages/provider/Dashboard";
import AdminDashboard from "../pages/admin/Dashboard";

import ConsentPage from "../modules/intake/pages/ConsentPage";
import IntakeFormPage from "../modules/intake/pages/IntakeFormPage";
import BookAppointmentPage from "../modules/appointments/pages/BookAppointmentPage";

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
        path="/patient/appointments"
        element={
          <ProtectedRoute allowedRoles={["patient"]}>
            <PatientAppointmentsPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/patient/appointments/book"
        element={
          <ProtectedRoute allowedRoles={["patient"]}>
            <BookAppointmentPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/patient/screening"
        element={
          <ProtectedRoute allowedRoles={["patient"]}>
            <PatientScreeningPage />
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

# Exact commands to run after pasting these files

## 1. Run the screening-focused tests
```bash
npx vitest run src/modules/screenings/__tests__/EpdsQuestionnaire.test.jsx src/modules/screenings/__tests__/ScreeningPage.test.jsx src/modules/screenings/__tests__/useEpdsForm.test.jsx
```

## 2. Start the frontend
```bash
npm run dev
```

## 3. Manual validation flow
After the frontend boots, validate this path:

1. Sign in as a patient  
2. Open `/patient/screening`  
3. Confirm the questionnaire renders clearly  
4. Try submitting with unanswered items and confirm the required-answer message appears  
5. Answer all items  
6. Submit the screening  
7. Confirm the completion summary appears  
8. Confirm prior screenings render when returned by the backend  

---

# Completion checklist

This phase is complete when all of the following are true:

- screening page renders correctly
- questionnaire displays all items
- unanswered submission is blocked
- form state remains stable while answering
- submission succeeds when all answers are provided
- completion summary displays after submit
- prior screenings are visible when returned by the backend
- patient flow stays readable and not confusing
- screening tests pass cleanly

---

# Practical note before Phase 6
Before moving on, verify that the backend remains the source of truth for final score persistence and follow-up classification. The frontend may preview or display the result, but the stored clinical record should come from the backend response.
