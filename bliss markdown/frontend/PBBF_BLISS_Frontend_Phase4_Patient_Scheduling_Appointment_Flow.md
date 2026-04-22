# PBBF BLISS Frontend — Phase 4 Populated Files
## Patient Scheduling and Appointment Flow

## Objective
Deliver the patient-facing scheduling experience and appointment lifecycle screens.

Repository root:

`bliss-telehealth/pbbf-telehealth`

This phase completes the patient appointment UX so a signed-in patient can view appointments, book a new appointment, reschedule an existing appointment, cancel an appointment, see status clearly, and see the next upcoming appointment emphasized.

---

## Phase 4 decisions

### 1. Keep the module split
Continue using:
- `src/modules/appointments/*` for appointment feature logic
- `src/pages/patient/*` for patient route-level page composition

### 2. Patient appointment flow
1. Patient opens the appointments page  
2. Existing appointments load from backend  
3. Patient can open booking screen  
4. Patient can submit a booking  
5. Patient can cancel an appointment  
6. Patient can reschedule an appointment  
7. Updated appointment status is reflected in the list  
8. The next appointment is visually emphasized  

### 3. Backend assumptions
This frontend phase assumes the backend exposes routes similar to:
- `GET /api/v1/appointments`
- `POST /api/v1/appointments`
- `PATCH /api/v1/appointments/{appointment_id}/reschedule`
- `PATCH /api/v1/appointments/{appointment_id}/cancel`

If your real backend paths differ, update only:
- `src/modules/appointments/services/appointmentsApi.js`

### 4. Route expectation
This phase needs route registration for:
- `/patient/appointments`
- `/patient/appointments/book`

A support patch for `src/app/AppRoutes.jsx` is included below.

---

## File list for this phase

### Modify these files
- `src/pages/patient/Appointments.jsx`
- `src/modules/appointments/pages/*`
- `src/modules/appointments/components/*`
- `src/modules/appointments/hooks/*`
- `src/modules/appointments/services/*`

### Create these files if missing
- `src/modules/appointments/pages/BookAppointmentPage.jsx`
- `src/modules/appointments/components/AppointmentCard.jsx`
- `src/modules/appointments/components/AppointmentForm.jsx`
- `src/modules/appointments/components/AppointmentStatusBadge.jsx`
- `src/modules/appointments/hooks/useAppointments.js`
- `src/modules/appointments/services/appointmentsApi.js`
- `src/modules/appointments/__tests__/AppointmentForm.test.jsx`
- `src/modules/appointments/__tests__/AppointmentsPage.test.jsx`

### Recommended support patch
- `src/pages/patient/Dashboard.jsx` — to emphasize the next appointment on the patient dashboard

---

# 1) `src/modules/appointments/services/appointmentsApi.js`

```jsx
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
```

---

# 2) `src/modules/appointments/hooks/useAppointments.js`

```jsx
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  cancelAppointmentRequest,
  createAppointmentRequest,
  listAppointmentsRequest,
  rescheduleAppointmentRequest,
} from "../services/appointmentsApi";

function normalizeAppointment(raw) {
  return {
    id: raw?.id || raw?.appointment_id || "temp-id",
    serviceType: raw?.service_type || raw?.serviceType || "",
    visitReason: raw?.visit_reason || raw?.visitReason || "",
    scheduledAt: raw?.scheduled_at || raw?.scheduledAt || raw?.appointment_time || "",
    timezone: raw?.timezone || "UTC",
    providerName: raw?.provider_name || raw?.providerName || "To be assigned",
    status: raw?.status || "booked",
    locationLabel: raw?.location_label || raw?.locationLabel || "Virtual visit",
  };
}

function sortAppointmentsByDate(items) {
  return [...items].sort((a, b) => new Date(a.scheduledAt) - new Date(b.scheduledAt));
}

function isUpcoming(appointment) {
  const appointmentDate = new Date(appointment.scheduledAt);
  return appointmentDate.getTime() >= Date.now();
}

export function useAppointments() {
  const [appointments, setAppointments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [loadError, setLoadError] = useState("");
  const [flashMessage, setFlashMessage] = useState("");

  const loadAppointments = useCallback(async () => {
    try {
      setIsLoading(true);
      setLoadError("");

      const response = await listAppointmentsRequest();
      const payload = response?.data || response;
      const rows = payload?.appointments || payload || [];
      const normalized = sortAppointmentsByDate(rows.map(normalizeAppointment));

      setAppointments(normalized);
    } catch (error) {
      setLoadError(error?.message || "Unable to load appointments.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAppointments();
  }, [loadAppointments]);

  const upcomingAppointments = useMemo(() => {
    return sortAppointmentsByDate(appointments.filter(isUpcoming));
  }, [appointments]);

  const nextAppointment = useMemo(() => {
    return upcomingAppointments[0] || null;
  }, [upcomingAppointments]);

  async function createAppointment(values) {
    try {
      setIsCreating(true);
      setFlashMessage("");

      const payload = {
        service_type: values.serviceType,
        visit_reason: values.visitReason,
        scheduled_at: values.scheduledAt,
        timezone: values.timezone,
      };

      const response = await createAppointmentRequest(payload);
      await loadAppointments();

      setFlashMessage(response?.message || "Appointment booked successfully.");
      return { success: true, response };
    } catch (error) {
      setFlashMessage(error?.message || "Unable to create appointment.");
      return { success: false, error };
    } finally {
      setIsCreating(false);
    }
  }

  async function rescheduleAppointment(appointmentId, scheduledAt) {
    try {
      setIsUpdating(true);
      setFlashMessage("");

      const response = await rescheduleAppointmentRequest(appointmentId, {
        scheduled_at: scheduledAt,
      });

      await loadAppointments();
      setFlashMessage(response?.message || "Appointment rescheduled successfully.");
      return { success: true, response };
    } catch (error) {
      setFlashMessage(error?.message || "Unable to reschedule appointment.");
      return { success: false, error };
    } finally {
      setIsUpdating(false);
    }
  }

  async function cancelAppointment(appointmentId) {
    try {
      setIsUpdating(true);
      setFlashMessage("");

      const response = await cancelAppointmentRequest(appointmentId, {
        reason: "Cancelled by patient from UI",
      });

      await loadAppointments();
      setFlashMessage(response?.message || "Appointment cancelled successfully.");
      return { success: true, response };
    } catch (error) {
      setFlashMessage(error?.message || "Unable to cancel appointment.");
      return { success: false, error };
    } finally {
      setIsUpdating(false);
    }
  }

  return {
    appointments,
    upcomingAppointments,
    nextAppointment,
    isLoading,
    isCreating,
    isUpdating,
    loadError,
    flashMessage,
    reload: loadAppointments,
    createAppointment,
    rescheduleAppointment,
    cancelAppointment,
  };
}
```

---

# 3) `src/modules/appointments/components/AppointmentStatusBadge.jsx`

```jsx
const badgeStyles = {
  booked: "bg-sky-100 text-sky-800 border-sky-200",
  confirmed: "bg-emerald-100 text-emerald-800 border-emerald-200",
  rescheduled: "bg-amber-100 text-amber-900 border-amber-200",
  cancelled: "bg-rose-100 text-rose-800 border-rose-200",
  completed: "bg-slate-100 text-slate-800 border-slate-200",
  no_show: "bg-orange-100 text-orange-900 border-orange-200",
};

export default function AppointmentStatusBadge({ status = "booked" }) {
  const label = status.replace(/_/g, " ");
  const className = badgeStyles[status] || "bg-slate-100 text-slate-800 border-slate-200";

  return (
    <span
      className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold capitalize ${className}`}
    >
      {label}
    </span>
  );
}
```

---

# 4) `src/modules/appointments/components/AppointmentCard.jsx`

```jsx
import { useState } from "react";
import AppointmentStatusBadge from "./AppointmentStatusBadge";

function formatDateTime(value) {
  if (!value) return "Not scheduled";
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export default function AppointmentCard({
  appointment,
  onCancel,
  onReschedule,
  showNextLabel = false,
  isBusy = false,
}) {
  const [editing, setEditing] = useState(false);
  const [rescheduleValue, setRescheduleValue] = useState("");

  const canManage =
    appointment.status !== "cancelled" && appointment.status !== "completed";

  async function handleRescheduleSubmit(event) {
    event.preventDefault();
    if (!rescheduleValue) return;
    await onReschedule(appointment.id, rescheduleValue);
    setEditing(false);
    setRescheduleValue("");
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          {showNextLabel ? (
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.18em] text-sky-700">
              Next appointment
            </p>
          ) : null}

          <h3 className="text-xl font-semibold text-slate-900">
            {appointment.serviceType || "Appointment"}
          </h3>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            {appointment.visitReason || "No visit reason added yet."}
          </p>
        </div>

        <AppointmentStatusBadge status={appointment.status} />
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Scheduled time
          </p>
          <p className="mt-2 text-sm font-medium text-slate-900">
            {formatDateTime(appointment.scheduledAt)}
          </p>
          <p className="mt-1 text-sm text-slate-600">{appointment.timezone}</p>
        </div>

        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Provider / location
          </p>
          <p className="mt-2 text-sm font-medium text-slate-900">{appointment.providerName}</p>
          <p className="mt-1 text-sm text-slate-600">{appointment.locationLabel}</p>
        </div>
      </div>

      {canManage ? (
        <div className="mt-6 space-y-4">
          <div className="flex flex-col gap-3 sm:flex-row">
            <button
              type="button"
              onClick={() => setEditing((current) => !current)}
              disabled={isBusy}
              className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {editing ? "Close reschedule" : "Reschedule"}
            </button>

            <button
              type="button"
              onClick={() => onCancel(appointment.id)}
              disabled={isBusy}
              className="rounded-xl border border-rose-300 bg-white px-4 py-3 text-sm font-semibold text-rose-700 transition hover:bg-rose-50 disabled:cursor-not-allowed disabled:opacity-70"
            >
              Cancel appointment
            </button>
          </div>

          {editing ? (
            <form className="space-y-3 rounded-2xl border border-slate-200 p-4" onSubmit={handleRescheduleSubmit}>
              <label className="block text-sm font-medium text-slate-700">
                New appointment date and time
              </label>
              <input
                type="datetime-local"
                value={rescheduleValue}
                onChange={(event) => setRescheduleValue(event.target.value)}
                className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
              />
              <button
                type="submit"
                disabled={!rescheduleValue || isBusy}
                className="rounded-xl bg-sky-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
              >
                Confirm reschedule
              </button>
            </form>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
```

---

# 5) `src/modules/appointments/components/AppointmentForm.jsx`

```jsx
import { useState } from "react";

const SERVICE_TYPES = [
  { value: "mental_health", label: "Mental health consultation" },
  { value: "lactation", label: "Lactation consultation" },
  { value: "wellness_follow_up", label: "Maternal wellness follow-up" },
  { value: "community_support", label: "Community support review" },
];

const DEFAULT_VALUES = {
  serviceType: "",
  visitReason: "",
  scheduledAt: "",
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC",
};

function validate(values) {
  const errors = {
    serviceType: "",
    visitReason: "",
    scheduledAt: "",
  };

  if (!values.serviceType) {
    errors.serviceType = "Please select a service type.";
  }

  if (!values.visitReason?.trim()) {
    errors.visitReason = "Please provide a visit reason.";
  }

  if (!values.scheduledAt) {
    errors.scheduledAt = "Please select a date and time.";
  }

  return errors;
}

function hasErrors(errors) {
  return Object.values(errors).some(Boolean);
}

export default function AppointmentForm({
  onSubmit,
  isSubmitting = false,
  serverMessage = "",
}) {
  const [values, setValues] = useState(DEFAULT_VALUES);
  const [errors, setErrors] = useState({
    serviceType: "",
    visitReason: "",
    scheduledAt: "",
  });

  function updateField(field, value) {
    setValues((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: "" }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const nextErrors = validate(values);
    setErrors(nextErrors);

    if (hasErrors(nextErrors)) return;

    const result = await onSubmit(values);

    if (result?.success) {
      setValues(DEFAULT_VALUES);
    }
  }

  return (
    <form className="space-y-6" onSubmit={handleSubmit} noValidate>
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">
          Service type
        </label>
        <select
          value={values.serviceType}
          onChange={(event) => updateField("serviceType", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
        >
          <option value="">Select appointment type</option>
          {SERVICE_TYPES.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        {errors.serviceType ? (
          <p className="mt-2 text-sm text-rose-600">{errors.serviceType}</p>
        ) : null}
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">
          Visit reason
        </label>
        <textarea
          rows={4}
          value={values.visitReason}
          onChange={(event) => updateField("visitReason", event.target.value)}
          className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="Describe what you would like help with during this appointment."
        />
        {errors.visitReason ? (
          <p className="mt-2 text-sm text-rose-600">{errors.visitReason}</p>
        ) : null}
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">
          Preferred date and time
        </label>
        <input
          type="datetime-local"
          value={values.scheduledAt}
          onChange={(event) => updateField("scheduledAt", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
        />
        {errors.scheduledAt ? (
          <p className="mt-2 text-sm text-rose-600">{errors.scheduledAt}</p>
        ) : null}
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium text-slate-700">
          Timezone
        </label>
        <input
          type="text"
          value={values.timezone}
          readOnly
          className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-600"
        />
      </div>

      {serverMessage ? (
        <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
          {serverMessage}
        </div>
      ) : null}

      <button
        type="submit"
        disabled={isSubmitting}
        className="rounded-xl bg-sky-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isSubmitting ? "Booking..." : "Book appointment"}
      </button>
    </form>
  );
}
```

---

# 6) `src/modules/appointments/pages/BookAppointmentPage.jsx`

```jsx
import { useNavigate } from "react-router-dom";
import AppointmentForm from "../components/AppointmentForm";
import { useAppointments } from "../hooks/useAppointments";
import Loader from "../../../shared/components/Loader";
import ErrorState from "../../../shared/components/ErrorState";

export default function BookAppointmentPage() {
  const navigate = useNavigate();
  const {
    isLoading,
    isCreating,
    loadError,
    flashMessage,
    createAppointment,
  } = useAppointments();

  async function handleCreate(values) {
    const result = await createAppointment(values);

    if (result?.success) {
      navigate("/patient/appointments", { replace: true });
    }

    return result;
  }

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading scheduling..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load appointment booking" message={loadError} />;
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-sky-700">
          Patient scheduling
        </p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Book an appointment</h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          Choose the service you need, provide your visit reason, and request an appointment time.
        </p>

        <div className="mt-8">
          <AppointmentForm
            onSubmit={handleCreate}
            isSubmitting={isCreating}
            serverMessage={flashMessage}
          />
        </div>
      </div>
    </div>
  );
}
```

---

# 7) `src/pages/patient/Appointments.jsx`

```jsx
import { Link } from "react-router-dom";
import AppointmentCard from "../../modules/appointments/components/AppointmentCard";
import { useAppointments } from "../../modules/appointments/hooks/useAppointments";
import Loader from "../../shared/components/Loader";
import EmptyState from "../../shared/components/EmptyState";
import ErrorState from "../../shared/components/ErrorState";

export default function PatientAppointmentsPage() {
  const {
    appointments,
    nextAppointment,
    isLoading,
    isUpdating,
    loadError,
    flashMessage,
    cancelAppointment,
    rescheduleAppointment,
  } = useAppointments();

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Loading appointments..." />
      </div>
    );
  }

  if (loadError) {
    return <ErrorState title="Unable to load appointments" message={loadError} />;
  }

  return (
    <div className="space-y-8">
      <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Patient scheduling</p>
            <h1 className="mt-2 text-3xl font-semibold">Appointments</h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">
              Manage booking, rescheduling, cancellation, and status updates for your care visits.
            </p>
          </div>

          <Link
            to="/patient/appointments/book"
            className="inline-flex rounded-xl bg-white px-5 py-3 text-sm font-semibold text-sky-900 transition hover:bg-sky-50"
          >
            Book appointment
          </Link>
        </div>
      </section>

      {flashMessage ? (
        <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
          {flashMessage}
        </div>
      ) : null}

      {nextAppointment ? (
        <section className="space-y-4">
          <div>
            <h2 className="text-2xl font-semibold text-slate-900">Next upcoming visit</h2>
            <p className="mt-1 text-sm text-slate-600">
              Your nearest scheduled appointment is highlighted here.
            </p>
          </div>

          <AppointmentCard
            appointment={nextAppointment}
            onCancel={cancelAppointment}
            onReschedule={rescheduleAppointment}
            isBusy={isUpdating}
            showNextLabel
          />
        </section>
      ) : null}

      <section className="space-y-4">
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">All appointments</h2>
          <p className="mt-1 text-sm text-slate-600">
            View appointment history and current scheduling state.
          </p>
        </div>

        {!appointments.length ? (
          <EmptyState
            title="No appointments yet"
            message="You have not booked any appointments yet. Start by creating your first appointment request."
            actionLabel="Book appointment"
            actionTo="/patient/appointments/book"
          />
        ) : (
          <div className="grid gap-5">
            {appointments.map((appointment) => (
              <AppointmentCard
                key={appointment.id}
                appointment={appointment}
                onCancel={cancelAppointment}
                onReschedule={rescheduleAppointment}
                isBusy={isUpdating}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
```

---

# 8) `src/modules/appointments/__tests__/AppointmentForm.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import AppointmentForm from "../components/AppointmentForm";

describe("AppointmentForm", () => {
  it("shows validation errors for empty required fields", async () => {
    render(<AppointmentForm onSubmit={vi.fn()} />);

    fireEvent.click(screen.getByRole("button", { name: /book appointment/i }));

    expect(await screen.findByText("Please select a service type.")).toBeInTheDocument();
    expect(await screen.findByText("Please provide a visit reason.")).toBeInTheDocument();
    expect(await screen.findByText("Please select a date and time.")).toBeInTheDocument();
  });

  it("submits valid form data", async () => {
    const onSubmit = vi.fn().mockResolvedValue({ success: true });

    render(<AppointmentForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByLabelText(/service type/i), {
      target: { value: "mental_health" },
    });

    fireEvent.change(screen.getByLabelText(/visit reason/i), {
      target: { value: "I need postpartum counseling support." },
    });

    fireEvent.change(screen.getByLabelText(/preferred date and time/i), {
      target: { value: "2026-05-01T10:30" },
    });

    fireEvent.click(screen.getByRole("button", { name: /book appointment/i }));

    expect(onSubmit).toHaveBeenCalledTimes(1);
    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        serviceType: "mental_health",
        visitReason: "I need postpartum counseling support.",
        scheduledAt: "2026-05-01T10:30",
      })
    );
  });
});
```

---

# 9) `src/modules/appointments/__tests__/AppointmentsPage.test.jsx`

```jsx
import { MemoryRouter } from "react-router-dom";
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import PatientAppointmentsPage from "../../../pages/patient/Appointments";

const cancelAppointmentMock = vi.fn();
const rescheduleAppointmentMock = vi.fn();

vi.mock("../hooks/useAppointments", () => ({
  useAppointments: () => ({
    appointments: [
      {
        id: "appt-1",
        serviceType: "mental_health",
        visitReason: "First visit",
        scheduledAt: "2026-05-01T10:30:00Z",
        timezone: "Africa/Kampala",
        providerName: "Assigned later",
        status: "booked",
        locationLabel: "Virtual visit",
      },
    ],
    nextAppointment: {
      id: "appt-1",
      serviceType: "mental_health",
      visitReason: "First visit",
      scheduledAt: "2026-05-01T10:30:00Z",
      timezone: "Africa/Kampala",
      providerName: "Assigned later",
      status: "booked",
      locationLabel: "Virtual visit",
    },
    isLoading: false,
    isUpdating: false,
    loadError: "",
    flashMessage: "",
    cancelAppointment: cancelAppointmentMock,
    rescheduleAppointment: rescheduleAppointmentMock,
  }),
}));

describe("PatientAppointmentsPage", () => {
  beforeEach(() => {
    cancelAppointmentMock.mockReset();
    rescheduleAppointmentMock.mockReset();
  });

  it("renders appointment list and next appointment emphasis", () => {
    render(
      <MemoryRouter>
        <PatientAppointmentsPage />
      </MemoryRouter>
    );

    expect(screen.getByText("Next upcoming visit")).toBeInTheDocument();
    expect(screen.getAllByText("mental_health").length).toBeGreaterThan(0);
  });

  it("triggers cancel action", () => {
    render(
      <MemoryRouter>
        <PatientAppointmentsPage />
      </MemoryRouter>
    );

    fireEvent.click(screen.getAllByRole("button", { name: /cancel appointment/i })[0]);

    expect(cancelAppointmentMock).toHaveBeenCalledTimes(1);
    expect(cancelAppointmentMock).toHaveBeenCalledWith("appt-1");
  });
});
```

---

# 10) Required support patch for route registration: `src/app/AppRoutes.jsx`

Merge these patient appointment routes into your existing route map:

```jsx
import { Navigate, Route, Routes } from "react-router-dom";
import ProtectedRoute from "../routes/ProtectedRoute";

import Login from "../pages/auth/Login";
import Register from "../modules/auth/pages/Register";
import ForgotPassword from "../modules/auth/pages/ForgotPassword";

import PatientDashboard from "../pages/patient/Dashboard";
import PatientAppointmentsPage from "../pages/patient/Appointments";
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

# 11) Recommended support patch for `src/pages/patient/Dashboard.jsx`

This is the cleanest way to satisfy the UX requirement:

> next appointment emphasis on dashboard

Merge this appointment summary block into the patient dashboard:

```jsx
import { Link } from "react-router-dom";
import { useAppointments } from "../../modules/appointments/hooks/useAppointments";

function formatDateTime(value) {
  if (!value) return "Not scheduled";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export default function PatientDashboard() {
  const { nextAppointment } = useAppointments();

  return (
    <div className="space-y-8">
      {/* existing dashboard sections stay here */}

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-slate-900">Next appointment</h2>
            {nextAppointment ? (
              <>
                <p className="mt-2 text-sm font-medium text-slate-900">
                  {nextAppointment.serviceType}
                </p>
                <p className="mt-1 text-sm text-slate-600">
                  {formatDateTime(nextAppointment.scheduledAt)}
                </p>
                <p className="mt-1 text-sm text-slate-600">{nextAppointment.status}</p>
              </>
            ) : (
              <p className="mt-2 text-sm text-slate-600">
                You do not have an upcoming appointment yet.
              </p>
            )}
          </div>

          <Link
            to="/patient/appointments"
            className="rounded-xl bg-sky-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-800"
          >
            Manage appointments
          </Link>
        </div>
      </section>
    </div>
  );
}
```

---

# Exact commands to run after pasting these files

## 1. Run the appointment-focused tests
```bash
npx vitest run src/modules/appointments/__tests__/AppointmentForm.test.jsx src/modules/appointments/__tests__/AppointmentsPage.test.jsx
```

## 2. Start the frontend
```bash
npm run dev
```

## 3. Manual validation flow
After the frontend boots, validate this path:

1. Sign in as a patient  
2. Open `/patient/appointments`  
3. Confirm appointment list loads  
4. Click **Book appointment**  
5. Submit invalid form and confirm validation feedback appears  
6. Submit valid form and confirm redirect back to appointment list  
7. Use **Reschedule** on an existing appointment  
8. Use **Cancel appointment** on an existing appointment  
9. Confirm the next appointment block reflects backend updates  
10. Confirm the dashboard can show the next appointment summary  

---

# Completion checklist

This phase is complete when all of the following are true:

- patient appointments page renders correctly
- patient can open the book appointment page
- booking form validation works
- booking submission works
- appointment list renders backend data
- appointment status badge is visible
- reschedule UI works
- cancel UI works
- next appointment is clearly emphasized
- appointment tests pass cleanly
- patient sees backend-driven appointment updates reflected in the UI

---

# Practical note before Phase 5
Before moving on, verify that the backend appointment response returns consistent date-time fields and status values. If the API mixes formats, normalize them now in the hook layer so the rest of the appointment UX stays stable.
