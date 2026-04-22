# PBBF BLISS Frontend — Phase 6 Populated Files
## Telehealth Session Access and Patient Dashboard Completion

## Objective
Finish the patient dashboard around real visit readiness and telehealth access.

Repository root:

`bliss-telehealth/pbbf-telehealth`

This phase completes the patient-facing virtual visit readiness experience so that a signed-in patient can:

- see reminder messaging on the dashboard
- understand whether the next visit is ready to join
- open the session page from the patient shell
- view basic device guidance
- see waiting, ready, in-progress, or ended states clearly
- use a visible join CTA when allowed

---

## Important alignment with your current structure

The structure you shared at the end of Phase 2 is already good:

- `src/main.jsx` is already correctly hydrating auth before render
- `src/app/AppRoutes.jsx` already uses `AppLayout` with `ProtectedRoute`
- `src/app/AppLayout.jsx` already wraps route pages in `AppShell`

That means this phase should **plug into the existing route shell**, not replace it.

### No rewrite needed for these files
You do **not** need to rewrite:
- `src/main.jsx`
- `src/app/AppLayout.jsx`

Your current versions are already appropriate for this phase.

### AppRoutes note
Your current `AppRoutes.jsx` already includes:

- `ROUTES.patient.session`
- `PatientSessionPage`

So this phase does **not** require a route patch unless:
- `ROUTES.patient.session` is missing in `src/shared/constants/routes.js`, or
- the imported page file does not yet exist or is still placeholder-only.

---

## Phase 6 backend assumptions

This frontend phase assumes the backend exposes routes similar to:

- `GET /api/v1/telehealth/sessions/next`
- `POST /api/v1/telehealth/sessions/{session_id}/join`

If your real backend paths differ, update only:

- `src/modules/telehealth/services/telehealthApi.js`

---

## File list for this phase

### Modify these files
- `src/pages/patient/Dashboard.jsx`
- `src/pages/patient/Session.jsx`
- `src/modules/telehealth/pages/*`
- `src/modules/telehealth/components/*`
- `src/modules/telehealth/hooks/*`
- `src/modules/notifications/components/*`

### Create these files if missing
- `src/modules/telehealth/components/JoinSessionCard.jsx`
- `src/modules/telehealth/components/DeviceCheckPanel.jsx`
- `src/modules/telehealth/hooks/useSessionAccess.js`
- `src/modules/telehealth/services/telehealthApi.js`
- `src/modules/notifications/components/ReminderBanner.jsx`
- `src/modules/telehealth/__tests__/JoinSessionCard.test.jsx`
- `src/modules/telehealth/__tests__/SessionPage.test.jsx`

### Recommended support test added for required dashboard reminder coverage
- `src/modules/telehealth/__tests__/DashboardReminder.test.jsx`

---

# 1) `src/modules/telehealth/services/telehealthApi.js`

```jsx
import { api } from "../../../services/api";

export function getNextSessionRequest() {
  return api.get("/telehealth/sessions/next");
}

export function joinSessionRequest(sessionId) {
  return api.post(`/telehealth/sessions/${sessionId}/join`, {});
}
```

---

# 2) `src/modules/telehealth/hooks/useSessionAccess.js`

```jsx
import { useCallback, useEffect, useMemo, useState } from "react";
import { getNextSessionRequest, joinSessionRequest } from "../services/telehealthApi";

function normalizeSession(raw) {
  if (!raw) return null;

  return {
    id: raw?.id || raw?.session_id || null,
    appointmentId: raw?.appointment_id || raw?.appointmentId || null,
    appointmentTime:
      raw?.appointment_time || raw?.scheduled_at || raw?.appointmentTime || "",
    sessionStatus: raw?.session_status || raw?.status || "scheduled",
    joinUrl: raw?.join_url || raw?.joinUrl || "",
    providerName: raw?.provider_name || raw?.providerName || "Care team",
    serviceType: raw?.service_type || raw?.serviceType || "Telehealth visit",
    reminderMessage:
      raw?.reminder_message ||
      raw?.reminderMessage ||
      "Your next visit is coming up. Please review your device readiness before joining.",
  };
}

function minutesUntil(dateValue) {
  if (!dateValue) return null;
  const target = new Date(dateValue);
  if (Number.isNaN(target.getTime())) return null;
  return Math.round((target.getTime() - Date.now()) / 60000);
}

export function useSessionAccess() {
  const [session, setSession] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isJoining, setIsJoining] = useState(false);
  const [loadError, setLoadError] = useState("");
  const [joinError, setJoinError] = useState("");
  const [joinMessage, setJoinMessage] = useState("");

  const loadSession = useCallback(async () => {
    try {
      setIsLoading(true);
      setLoadError("");

      const response = await getNextSessionRequest();
      const payload = response?.data || response;
      const nextSession = normalizeSession(payload?.session || payload || null);

      setSession(nextSession);
    } catch (error) {
      setLoadError(error?.message || "Unable to load session readiness.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSession();
  }, [loadSession]);

  const minutesToSession = useMemo(() => {
    return minutesUntil(session?.appointmentTime);
  }, [session]);

  const readiness = useMemo(() => {
    if (!session) {
      return {
        canJoin: false,
        state: "no_session",
        message: "You do not have a telehealth session ready to join right now.",
      };
    }

    if (session.sessionStatus === "ended") {
      return {
        canJoin: false,
        state: "ended",
        message: "This visit has already ended.",
      };
    }

    if (session.sessionStatus === "in_progress") {
      return {
        canJoin: true,
        state: "in_progress",
        message: "Your session is in progress and ready to join.",
      };
    }

    if (typeof minutesToSession === "number" && minutesToSession > 15) {
      return {
        canJoin: false,
        state: "too_early",
        message: "Your session is scheduled later. Please come back closer to the appointment time.",
      };
    }

    if (typeof minutesToSession === "number" && minutesToSession >= -60) {
      return {
        canJoin: true,
        state: "ready",
        message: "Your session is available to join.",
      };
    }

    return {
      canJoin: false,
      state: "scheduled",
      message: "Your session is scheduled but not yet ready for entry.",
    };
  }, [session, minutesToSession]);

  async function joinSession() {
    if (!session?.id || !readiness.canJoin) {
      return { success: false };
    }

    try {
      setIsJoining(true);
      setJoinError("");
      setJoinMessage("");

      const response = await joinSessionRequest(session.id);
      const payload = response?.data || response;
      const nextSession = normalizeSession(payload?.session || session);

      if (payload?.join_url || nextSession?.joinUrl) {
        window.open(payload?.join_url || nextSession.joinUrl, "_blank", "noopener,noreferrer");
      }

      setSession(nextSession);
      setJoinMessage(response?.message || "Joining session...");
      return { success: true, response };
    } catch (error) {
      setJoinError(error?.message || "Unable to join session.");
      return { success: false, error };
    } finally {
      setIsJoining(false);
    }
  }

  return {
    session,
    readiness,
    minutesToSession,
    isLoading,
    isJoining,
    loadError,
    joinError,
    joinMessage,
    joinSession,
    reload: loadSession,
  };
}
```

---

# 3) `src/modules/notifications/components/ReminderBanner.jsx`

```jsx
import { Link } from "react-router-dom";
import { ROUTES } from "../../../shared/constants/routes";

function formatDateTime(value) {
  if (!value) return "Not scheduled";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export default function ReminderBanner({ session }) {
  if (!session) return null;

  return (
    <section className="rounded-3xl border border-sky-200 bg-sky-50 p-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.18em] text-sky-700">
            Upcoming visit
          </p>
          <h2 className="mt-2 text-xl font-semibold text-sky-950">
            {session.serviceType}
          </h2>
          <p className="mt-2 text-sm text-sky-900">
            {formatDateTime(session.appointmentTime)} with {session.providerName}
          </p>
          <p className="mt-2 text-sm leading-6 text-sky-800">
            {session.reminderMessage}
          </p>
        </div>

        <Link
          to={ROUTES.patient.session}
          className="inline-flex rounded-xl bg-sky-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-800"
        >
          View session access
        </Link>
      </div>
    </section>
  );
}
```

---

# 4) `src/modules/telehealth/components/DeviceCheckPanel.jsx`

```jsx
export default function DeviceCheckPanel() {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">
        Device readiness
      </p>
      <h2 className="mt-2 text-xl font-semibold text-slate-900">
        Basic checks before joining
      </h2>

      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl bg-slate-50 p-4">
          <h3 className="text-sm font-semibold text-slate-900">Internet</h3>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Use the most stable connection available before starting your visit.
          </p>
        </div>

        <div className="rounded-2xl bg-slate-50 p-4">
          <h3 className="text-sm font-semibold text-slate-900">Audio</h3>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Confirm your microphone and speaker work properly.
          </p>
        </div>

        <div className="rounded-2xl bg-slate-50 p-4">
          <h3 className="text-sm font-semibold text-slate-900">Camera</h3>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Allow camera access if your visit requires video.
          </p>
        </div>

        <div className="rounded-2xl bg-slate-50 p-4">
          <h3 className="text-sm font-semibold text-slate-900">Quiet space</h3>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Join from a calm and private place where you can focus on the visit.
          </p>
        </div>
      </div>
    </section>
  );
}
```

---

# 5) `src/modules/telehealth/components/JoinSessionCard.jsx`

```jsx
function formatDateTime(value) {
  if (!value) return "Not scheduled";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

const stateStyles = {
  no_session: "border-slate-200 bg-slate-50 text-slate-700",
  too_early: "border-amber-200 bg-amber-50 text-amber-900",
  ready: "border-emerald-200 bg-emerald-50 text-emerald-900",
  in_progress: "border-emerald-200 bg-emerald-50 text-emerald-900",
  ended: "border-slate-200 bg-slate-50 text-slate-700",
  scheduled: "border-slate-200 bg-slate-50 text-slate-700",
};

export default function JoinSessionCard({
  session,
  readiness,
  isJoining = false,
  joinError = "",
  joinMessage = "",
  onJoin,
}) {
  const styleClass = stateStyles[readiness?.state] || stateStyles.scheduled;

  return (
    <section className={`rounded-3xl border p-6 shadow-sm ${styleClass}`}>
      <p className="text-sm font-medium uppercase tracking-[0.18em]">
        Session access
      </p>

      <h2 className="mt-2 text-2xl font-semibold">
        {session ? session.serviceType : "No current session"}
      </h2>

      <p className="mt-3 text-sm leading-6">
        {readiness?.message}
      </p>

      {session ? (
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.16em]">
              Scheduled time
            </p>
            <p className="mt-2 text-sm font-medium">
              {formatDateTime(session.appointmentTime)}
            </p>
          </div>

          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.16em]">
              Care team
            </p>
            <p className="mt-2 text-sm font-medium">{session.providerName}</p>
          </div>
        </div>
      ) : null}

      {joinMessage ? (
        <div className="mt-5 rounded-2xl border border-emerald-200 bg-white/70 px-4 py-3 text-sm">
          {joinMessage}
        </div>
      ) : null}

      {joinError ? (
        <div className="mt-5 rounded-2xl border border-rose-200 bg-white/70 px-4 py-3 text-sm text-rose-700">
          {joinError}
        </div>
      ) : null}

      <div className="mt-6">
        <button
          type="button"
          onClick={onJoin}
          disabled={!readiness?.canJoin || isJoining}
          className="rounded-xl bg-sky-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {isJoining ? "Joining..." : "Join session"}
        </button>
      </div>
    </section>
  );
}
```

---

# 6) `src/pages/patient/Session.jsx`

```jsx
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";
import DeviceCheckPanel from "../../modules/telehealth/components/DeviceCheckPanel";
import JoinSessionCard from "../../modules/telehealth/components/JoinSessionCard";
import { useSessionAccess } from "../../modules/telehealth/hooks/useSessionAccess";

export default function PatientSessionPage() {
  const {
    session,
    readiness,
    isLoading,
    isJoining,
    loadError,
    joinError,
    joinMessage,
    joinSession,
  } = useSessionAccess();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading session access..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load session access" message={loadError} />;
  }

  return (
    <div className="space-y-8">
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Telehealth session</p>
        <h1 className="mt-2 text-3xl font-semibold">Join your visit</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
          Review your visit status, confirm basic device readiness, and join when your session is available.
        </p>
      </section>

      <JoinSessionCard
        session={session}
        readiness={readiness}
        isJoining={isJoining}
        joinError={joinError}
        joinMessage={joinMessage}
        onJoin={joinSession}
      />

      <DeviceCheckPanel />
    </div>
  );
}
```

---

# 7) `src/pages/patient/Dashboard.jsx`

Use this version only if your current patient dashboard still needs the telehealth reminder and readiness block merged in.

```jsx
import { Link } from "react-router-dom";
import { ROUTES } from "../../shared/constants/routes";
import { useAuthStore } from "../../store/authStore";
import { useIntakeForm } from "../../modules/intake/hooks/useIntakeForm";
import { useAppointments } from "../../modules/appointments/hooks/useAppointments";
import { useSessionAccess } from "../../modules/telehealth/hooks/useSessionAccess";
import ReminderBanner from "../../modules/notifications/components/ReminderBanner";
import Loader from "../../shared/components/Loader";
import ErrorState from "../../shared/components/ErrorState";

export default function PatientDashboard() {
  const user = useAuthStore((state) => state.user);
  const {
    values,
    isLoading: intakeLoading,
    loadError: intakeError,
    onboardingComplete,
  } = useIntakeForm();
  const { nextAppointment } = useAppointments();
  const { session, readiness } = useSessionAccess();

  if (intakeLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading patient dashboard..." />
      </div>
    );
  }

  if (intakeError) {
    return <ErrorState title="Unable to load patient dashboard" message={intakeError} />;
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

      <ReminderBanner session={session} />

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

            <Link
              to={ROUTES.patient.dashboard}
              className="rounded-xl bg-amber-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-amber-700"
            >
              Continue onboarding
            </Link>
          </div>
        </section>
      ) : null}

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
          <h3 className="text-lg font-semibold text-slate-900">Next appointment</h3>
          {nextAppointment ? (
            <>
              <p className="mt-2 text-sm font-medium text-slate-900">
                {nextAppointment.serviceType}
              </p>
              <p className="mt-1 text-sm text-slate-600">{nextAppointment.status}</p>
              <Link
                to={ROUTES.patient.appointments}
                className="mt-4 inline-flex text-sm font-semibold text-sky-700 hover:text-sky-800"
              >
                Manage appointments
              </Link>
            </>
          ) : (
            <p className="mt-2 text-sm text-slate-600">
              You do not have an upcoming appointment yet.
            </p>
          )}
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Visit readiness</h3>
          <p className="mt-2 text-sm text-slate-600">
            {readiness?.message || "No telehealth session state available yet."}
          </p>
          <Link
            to={ROUTES.patient.session}
            className="mt-4 inline-flex text-sm font-semibold text-sky-700 hover:text-sky-800"
          >
            Open session access
          </Link>
        </div>
      </section>
    </div>
  );
}
```

### Important correction inside the onboarding CTA
If you already have onboarding routes from earlier phases, do **not** point that button to `ROUTES.patient.dashboard`. Point it to your real onboarding route, for example:

```jsx
to="/patient/onboarding/consent"
```

If your `ROUTES` constant already contains onboarding paths, use those instead.

---

# 8) `src/modules/telehealth/__tests__/JoinSessionCard.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import JoinSessionCard from "../components/JoinSessionCard";

describe("JoinSessionCard", () => {
  it("disables join button when session is not ready", () => {
    render(
      <JoinSessionCard
        session={{
          id: "session-1",
          appointmentTime: "2026-05-02T10:00:00Z",
          providerName: "Provider",
          serviceType: "Telehealth visit",
        }}
        readiness={{
          canJoin: false,
          state: "too_early",
          message: "Your session is scheduled later.",
        }}
        onJoin={vi.fn()}
      />
    );

    expect(screen.getByRole("button", { name: /join session/i })).toBeDisabled();
  });

  it("calls join handler when session is ready", () => {
    const onJoin = vi.fn();

    render(
      <JoinSessionCard
        session={{
          id: "session-1",
          appointmentTime: "2026-05-02T10:00:00Z",
          providerName: "Provider",
          serviceType: "Telehealth visit",
        }}
        readiness={{
          canJoin: true,
          state: "ready",
          message: "Your session is available to join.",
        }}
        onJoin={onJoin}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /join session/i }));
    expect(onJoin).toHaveBeenCalledTimes(1);
  });
});
```

---

# 9) `src/modules/telehealth/__tests__/SessionPage.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import PatientSessionPage from "../../../pages/patient/Session";

vi.mock("../hooks/useSessionAccess", () => ({
  useSessionAccess: () => ({
    session: null,
    readiness: {
      canJoin: false,
      state: "no_session",
      message: "You do not have a telehealth session ready to join right now.",
    },
    isLoading: false,
    isJoining: false,
    loadError: "",
    joinError: "",
    joinMessage: "",
    joinSession: vi.fn(),
  }),
}));

describe("PatientSessionPage", () => {
  it("renders no-session state correctly", () => {
    render(<PatientSessionPage />);

    expect(screen.getByText("Join your visit")).toBeInTheDocument();
    expect(
      screen.getByText("You do not have a telehealth session ready to join right now.")
    ).toBeInTheDocument();
  });
});
```

---

# 10) Recommended support test for the required dashboard reminder outcome  
## `src/modules/telehealth/__tests__/DashboardReminder.test.jsx`

```jsx
import { MemoryRouter } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import PatientDashboard from "../../../pages/patient/Dashboard";

vi.mock("../../../store/authStore", () => ({
  useAuthStore: (selector) =>
    selector({
      user: { full_name: "Jane Patient", role: "patient" },
    }),
}));

vi.mock("../../../modules/intake/hooks/useIntakeForm", () => ({
  useIntakeForm: () => ({
    values: { intakeStatus: "submitted", serviceNeeds: ["mental_health"] },
    isLoading: false,
    loadError: "",
    onboardingComplete: true,
  }),
}));

vi.mock("../../../modules/appointments/hooks/useAppointments", () => ({
  useAppointments: () => ({
    nextAppointment: {
      id: "appt-1",
      serviceType: "mental_health",
      status: "booked",
    },
  }),
}));

vi.mock("../../../modules/telehealth/hooks/useSessionAccess", () => ({
  useSessionAccess: () => ({
    session: {
      id: "session-1",
      appointmentTime: "2026-05-02T10:00:00Z",
      providerName: "Provider",
      serviceType: "Telehealth visit",
      reminderMessage:
        "Your next visit is coming up. Please review your device readiness before joining.",
    },
    readiness: {
      canJoin: true,
      state: "ready",
      message: "Your session is available to join.",
    },
  }),
}));

describe("PatientDashboard telehealth reminder", () => {
  it("renders reminder messaging on the dashboard", () => {
    render(
      <MemoryRouter>
        <PatientDashboard />
      </MemoryRouter>
    );

    expect(screen.getByText("Upcoming visit")).toBeInTheDocument();
    expect(screen.getByText("View session access")).toBeInTheDocument();
  });
});
```

---

# 11) Optional note for `src/shared/constants/routes.js`

Your `AppRoutes.jsx` already uses `ROUTES.patient.session`, so confirm that the constant exists in `src/shared/constants/routes.js`.

A safe shape looks like this:

```jsx
export const ROUTES = {
  root: "/",
  login: "/login",
  register: "/register",
  forgotPassword: "/forgot-password",
  patient: {
    dashboard: "/patient",
    appointments: "/patient/appointments",
    messages: "/patient/messages",
    resources: "/patient/resources",
    screening: "/patient/screening",
    session: "/patient/session",
    carePlan: "/patient/care-plan",
  },
  provider: {
    dashboard: "/provider",
    notes: "/provider/notes",
    referrals: "/provider/referrals",
  },
  admin: {
    dashboard: "/admin",
    users: "/admin/users",
    reports: "/admin/reports",
    auditLogs: "/admin/audit-logs",
    settings: "/admin/settings",
  },
};
```

---

# Exact commands to run after pasting these files

## 1. Run the telehealth-focused tests
```bash
npx vitest run src/modules/telehealth/__tests__/JoinSessionCard.test.jsx src/modules/telehealth/__tests__/SessionPage.test.jsx src/modules/telehealth/__tests__/DashboardReminder.test.jsx
```

## 2. Start the frontend
```bash
npm run dev
```

## 3. Manual validation flow
After the frontend boots, validate this path:

1. Sign in as a patient  
2. Open the patient dashboard  
3. Confirm reminder information appears when a next session exists  
4. Click **View session access**  
5. Confirm the session page loads  
6. Confirm the join CTA is disabled when the session is too early  
7. Confirm device guidance is visible  
8. Confirm the join CTA becomes active when the backend says the visit is ready  
9. Confirm no-session messaging is readable when no upcoming session exists  

---

# Completion checklist

This phase is complete when all of the following are true:

- dashboard surfaces reminder information for the next visit
- patient can open the session page from the main shell
- session join CTA is visible
- join button state changes correctly based on readiness
- no-session state is readable
- device guidance is visible
- waiting / ready / in-progress / ended state messaging is understandable
- telehealth tests pass cleanly
- a patient can enter the portal and clearly understand how to join the next visit

---

# Practical note before Phase 7
Before moving on, make sure the backend is the source of truth for actual session availability and join authorization. The frontend should explain readiness clearly, but it should never become the final authority for whether a session may be joined.
