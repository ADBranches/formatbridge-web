# PBBF BLISS Frontend — Phase 9 Populated Files
## Shared UX Hardening, Error States, and Accessibility Pass

## Objective
Refine the product so it feels dependable, understandable, and consistent across roles.

Repository root:

`bliss-telehealth/pbbf-telehealth`

This phase hardens the shared UI layer so patient, provider, and admin experiences feel like one product instead of separate screens built at different times.

It introduces:
- standardized page structure primitives
- stronger form feedback
- reusable input controls
- reusable modal/table/tabs primitives
- accessibility helpers
- shared toast behavior
- component smoke tests
- a clear rule to **centralize payload mapping logic instead of scattering it across pages**

---

## Critical architectural rule for this phase

## Do **not** scatter mapping logic across pages

You called this out correctly, and I agree.

### Recommended rule
Use this structure:

- **API services** only make requests
- **feature hooks** normalize and prepare backend data for UI use
- **pages** compose sections and pass props
- **shared UI components** stay presentational

### Best pattern for this project
Since you are using a feature/module structure, the cleanest rule is:

- put backend-to-frontend normalization inside the relevant **module hook**
- when the same mapping is reused across multiple pages in the same module, move it into:
  - `src/modules/<feature>/utils/mappers.js`
- when the same mapper is truly cross-cutting, move it into:
  - `src/shared/utils/mappers.js`

### Example
Good:
- `src/modules/appointments/hooks/useAppointments.js`
- `src/modules/admin/hooks/useAdminMetrics.js`

Better when reuse grows:
- `src/modules/appointments/utils/mappers.js`
- `src/modules/admin/utils/mappers.js`

Avoid:
- normalizing backend payloads directly inside:
  - `src/pages/patient/Appointments.jsx`
  - `src/pages/provider/Dashboard.jsx`
  - `src/pages/admin/Users.jsx`

### Recommended standard
For this project, use this simple rule going forward:

> **All backend response mapping should happen in feature hooks or feature utils, never directly inside page components.**

That keeps the page layer clean and makes your sfile methodology easier to maintain.

---

## Directories to modify
- `src/shared/components`
- `src/components/ui`
- `src/modules/*`
- `src/pages/*`

## Create or complete these files
- `src/shared/components/FormErrorSummary.jsx`
- `src/shared/components/PageHeader.jsx`
- `src/shared/components/SectionCard.jsx`
- `src/shared/hooks/useToast.js`
- `src/shared/utils/a11y.js`
- `src/components/ui/Input.jsx`
- `src/components/ui/Select.jsx`
- `src/components/ui/Modal.jsx`
- `src/components/ui/Table.jsx`
- `src/components/ui/Textarea.jsx`
- `src/components/ui/Tabs.jsx`
- `src/components/ui/__tests__/Button.test.jsx`
- `src/components/ui/__tests__/Card.test.jsx`

### Recommended support files for this phase
These are not mandatory from your prompt, but they are the cleanest support files for the hardening objective:
- `src/components/ui/__tests__/Input.test.jsx`
- `src/components/ui/__tests__/Modal.test.jsx`
- `src/shared/components/__tests__/PageHeader.test.jsx`

---

# 1) Shared implementation strategy for this phase

## What this phase should change across the product

### Patient, provider, and admin pages should all move toward:
- one loading pattern
- one empty state pattern
- one error pattern
- one page-header pattern
- one section-card pattern
- one form-control pattern
- one form-error-summary pattern

### This means pages should gradually use:
- `PageHeader`
- `SectionCard`
- `FormErrorSummary`
- `Input`
- `Select`
- `Textarea`
- `Modal`
- `Table`
- `Tabs`

Do **not** rewrite every page immediately. Instead:
- add these primitives now
- begin using them in new work
- refactor earlier pages incrementally as you touch them

That fits your current phase-by-phase sfile workflow much better than a risky big-bang rewrite.

---

# 2) `src/shared/utils/a11y.js`

```jsx
let idCounter = 0;

export function createFieldIds(name = "field") {
  idCounter += 1;
  const base = `${name}-${idCounter}`;
  return {
    inputId: `${base}-input`,
    hintId: `${base}-hint`,
    errorId: `${base}-error`,
  };
}

export function getAriaDescribedBy({ hint, error, hintId, errorId }) {
  return [hint ? hintId : null, error ? errorId : null].filter(Boolean).join(" ") || undefined;
}

export function getFieldA11yProps({ hint, error, hintId, errorId }) {
  return {
    "aria-invalid": Boolean(error) || undefined,
    "aria-describedby": getAriaDescribedBy({ hint, error, hintId, errorId }),
  };
}

export function onEnterOrSpace(handler) {
  return function handleKeyDown(event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handler?.(event);
    }
  };
}
```

---

# 3) `src/shared/hooks/useToast.js`

```jsx
import { useCallback, useEffect, useState } from "react";

let listeners = new Set();
let toastQueue = [];

function emit() {
  listeners.forEach((listener) => listener([...toastQueue]));
}

export function pushToast(toast) {
  const entry = {
    id: toast?.id || `toast-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
    type: toast?.type || "info",
    title: toast?.title || "",
    message: toast?.message || "",
    duration: toast?.duration ?? 3000,
  };

  toastQueue = [...toastQueue, entry];
  emit();

  if (entry.duration > 0) {
    window.setTimeout(() => {
      dismissToast(entry.id);
    }, entry.duration);
  }

  return entry.id;
}

export function dismissToast(id) {
  toastQueue = toastQueue.filter((toast) => toast.id !== id);
  emit();
}

export function useToast() {
  const [toasts, setToasts] = useState(toastQueue);

  useEffect(() => {
    const listener = (nextToasts) => setToasts(nextToasts);
    listeners.add(listener);

    return () => {
      listeners.delete(listener);
    };
  }, []);

  const success = useCallback((message, title = "Success") => {
    return pushToast({ type: "success", title, message });
  }, []);

  const error = useCallback((message, title = "Error") => {
    return pushToast({ type: "error", title, message, duration: 5000 });
  }, []);

  const info = useCallback((message, title = "Info") => {
    return pushToast({ type: "info", title, message });
  }, []);

  return {
    toasts,
    success,
    error,
    info,
    dismiss: dismissToast,
  };
}
```

---

# 4) `src/shared/components/PageHeader.jsx`

```jsx
export default function PageHeader({
  eyebrow = "",
  title,
  description = "",
  actions = null,
}) {
  return (
    <section className="rounded-3xl bg-sky-900 px-8 py-8 text-white">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          {eyebrow ? (
            <p className="text-sm uppercase tracking-[0.2em] text-sky-200">{eyebrow}</p>
          ) : null}
          <h1 className="mt-2 text-3xl font-semibold">{title}</h1>
          {description ? (
            <p className="mt-3 max-w-2xl text-sm leading-6 text-sky-100">{description}</p>
          ) : null}
        </div>

        {actions ? <div className="flex flex-wrap gap-3">{actions}</div> : null}
      </div>
    </section>
  );
}
```

---

# 5) `src/shared/components/SectionCard.jsx`

```jsx
export default function SectionCard({
  title,
  description = "",
  actions = null,
  children,
  className = "",
}) {
  return (
    <section className={`rounded-3xl border border-slate-200 bg-white p-6 shadow-sm ${className}`}>
      {(title || description || actions) ? (
        <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div>
            {title ? <h2 className="text-xl font-semibold text-slate-900">{title}</h2> : null}
            {description ? (
              <p className="mt-2 text-sm leading-6 text-slate-600">{description}</p>
            ) : null}
          </div>

          {actions ? <div className="flex flex-wrap gap-3">{actions}</div> : null}
        </div>
      ) : null}

      {children}
    </section>
  );
}
```

---

# 6) `src/shared/components/FormErrorSummary.jsx`

```jsx
export default function FormErrorSummary({
  errors = {},
  title = "Please correct the following issues before continuing.",
}) {
  const items = Object.values(errors).filter(Boolean);

  if (!items.length) return null;

  return (
    <div
      role="alert"
      className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-4"
    >
      <h3 className="text-sm font-semibold text-rose-800">{title}</h3>
      <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-rose-700">
        {items.map((item, index) => (
          <li key={`${item}-${index}`}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

# 7) `src/components/ui/Input.jsx`

```jsx
import { useMemo } from "react";
import { createFieldIds, getFieldA11yProps } from "../../shared/utils/a11y";

export default function Input({
  label,
  hint = "",
  error = "",
  className = "",
  containerClassName = "",
  ...props
}) {
  const ids = useMemo(() => createFieldIds(props.name || "input"), [props.name]);

  return (
    <div className={containerClassName}>
      {label ? (
        <label htmlFor={ids.inputId} className="mb-2 block text-sm font-medium text-slate-700">
          {label}
        </label>
      ) : null}

      <input
        id={ids.inputId}
        {...props}
        {...getFieldA11yProps({
          hint,
          error,
          hintId: ids.hintId,
          errorId: ids.errorId,
        })}
        className={`w-full rounded-xl border px-4 py-3 outline-none transition ${
          error
            ? "border-rose-400 focus:border-rose-500 focus:ring-2 focus:ring-rose-100"
            : "border-slate-300 focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
        } ${className}`}
      />

      {hint ? (
        <p id={ids.hintId} className="mt-2 text-sm text-slate-500">
          {hint}
        </p>
      ) : null}

      {error ? (
        <p id={ids.errorId} className="mt-2 text-sm text-rose-600">
          {error}
        </p>
      ) : null}
    </div>
  );
}
```

---

# 8) `src/components/ui/Select.jsx`

```jsx
import { useMemo } from "react";
import { createFieldIds, getFieldA11yProps } from "../../shared/utils/a11y";

export default function Select({
  label,
  hint = "",
  error = "",
  options = [],
  placeholder = "Select an option",
  className = "",
  containerClassName = "",
  ...props
}) {
  const ids = useMemo(() => createFieldIds(props.name || "select"), [props.name]);

  return (
    <div className={containerClassName}>
      {label ? (
        <label htmlFor={ids.inputId} className="mb-2 block text-sm font-medium text-slate-700">
          {label}
        </label>
      ) : null}

      <select
        id={ids.inputId}
        {...props}
        {...getFieldA11yProps({
          hint,
          error,
          hintId: ids.hintId,
          errorId: ids.errorId,
        })}
        className={`w-full rounded-xl border px-4 py-3 outline-none transition ${
          error
            ? "border-rose-400 focus:border-rose-500 focus:ring-2 focus:ring-rose-100"
            : "border-slate-300 focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
        } ${className}`}
      >
        <option value="">{placeholder}</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      {hint ? (
        <p id={ids.hintId} className="mt-2 text-sm text-slate-500">
          {hint}
        </p>
      ) : null}

      {error ? (
        <p id={ids.errorId} className="mt-2 text-sm text-rose-600">
          {error}
        </p>
      ) : null}
    </div>
  );
}
```

---

# 9) `src/components/ui/Textarea.jsx`

```jsx
import { useMemo } from "react";
import { createFieldIds, getFieldA11yProps } from "../../shared/utils/a11y";

export default function Textarea({
  label,
  hint = "",
  error = "",
  className = "",
  containerClassName = "",
  rows = 4,
  ...props
}) {
  const ids = useMemo(() => createFieldIds(props.name || "textarea"), [props.name]);

  return (
    <div className={containerClassName}>
      {label ? (
        <label htmlFor={ids.inputId} className="mb-2 block text-sm font-medium text-slate-700">
          {label}
        </label>
      ) : null}

      <textarea
        id={ids.inputId}
        rows={rows}
        {...props}
        {...getFieldA11yProps({
          hint,
          error,
          hintId: ids.hintId,
          errorId: ids.errorId,
        })}
        className={`w-full rounded-2xl border px-4 py-3 outline-none transition ${
          error
            ? "border-rose-400 focus:border-rose-500 focus:ring-2 focus:ring-rose-100"
            : "border-slate-300 focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
        } ${className}`}
      />

      {hint ? (
        <p id={ids.hintId} className="mt-2 text-sm text-slate-500">
          {hint}
        </p>
      ) : null}

      {error ? (
        <p id={ids.errorId} className="mt-2 text-sm text-rose-600">
          {error}
        </p>
      ) : null}
    </div>
  );
}
```

---

# 10) `src/components/ui/Modal.jsx`

```jsx
import { useEffect } from "react";

export default function Modal({
  open,
  title,
  description = "",
  onClose,
  children,
  footer = null,
}) {
  useEffect(() => {
    if (!open) return;

    function handleEscape(event) {
      if (event.key === "Escape") {
        onClose?.();
      }
    }

    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={title}
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 px-4"
    >
      <div className="w-full max-w-2xl rounded-3xl bg-white p-6 shadow-2xl">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-semibold text-slate-900">{title}</h2>
            {description ? (
              <p className="mt-2 text-sm leading-6 text-slate-600">{description}</p>
            ) : null}
          </div>

          <button
            type="button"
            onClick={onClose}
            className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
          >
            Close
          </button>
        </div>

        <div className="mt-6">{children}</div>

        {footer ? <div className="mt-6">{footer}</div> : null}
      </div>
    </div>
  );
}
```

---

# 11) `src/components/ui/Table.jsx`

```jsx
export default function Table({
  columns = [],
  rows = [],
  emptyMessage = "No records available.",
}) {
  if (!rows.length) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-600">
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-2xl border border-slate-200">
      <table className="min-w-full border-collapse text-left text-sm">
        <thead className="bg-slate-50">
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                className="border-b border-slate-200 px-4 py-3 font-semibold text-slate-600"
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={row.id || rowIndex} className="border-b border-slate-100">
              {columns.map((column) => (
                <td key={column.key} className="px-4 py-3 text-slate-700">
                  {column.render ? column.render(row) : row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

# 12) `src/components/ui/Tabs.jsx`

```jsx
import { useState } from "react";

export default function Tabs({ tabs = [], initialTab = "" }) {
  const fallback = tabs[0]?.id || "";
  const [activeTab, setActiveTab] = useState(initialTab || fallback);

  const currentTab = tabs.find((tab) => tab.id === activeTab) || tabs[0];

  if (!tabs.length) return null;

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap gap-2">
        {tabs.map((tab) => {
          const active = tab.id === currentTab?.id;

          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id)}
              className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
                active
                  ? "bg-sky-700 text-white"
                  : "border border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
              }`}
            >
              {tab.label}
            </button>
          );
        })}
      </div>

      <div>{currentTab?.content}</div>
    </div>
  );
}
```

---

# 13) `src/components/ui/__tests__/Button.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import Button from "../Button";

describe("Button", () => {
  it("renders button text", () => {
    render(<Button>Continue</Button>);
    expect(screen.getByRole("button", { name: /continue/i })).toBeInTheDocument();
  });

  it("fires click handler", () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Continue</Button>);

    fireEvent.click(screen.getByRole("button", { name: /continue/i }));
    expect(onClick).toHaveBeenCalledTimes(1);
  });
});
```

---

# 14) `src/components/ui/__tests__/Card.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import Card from "../Card";

describe("Card", () => {
  it("renders card children", () => {
    render(<Card>Card Content</Card>);
    expect(screen.getByText("Card Content")).toBeInTheDocument();
  });
});
```

---

# 15) Recommended support test: `src/components/ui/__tests__/Input.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import Input from "../Input";

describe("Input", () => {
  it("renders label and error state", () => {
    render(
      <Input
        name="email"
        label="Email address"
        error="Email is required."
      />
    );

    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByText("Email is required.")).toBeInTheDocument();
  });
});
```

---

# 16) Recommended support test: `src/components/ui/__tests__/Modal.test.jsx`

```jsx
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import Modal from "../Modal";

describe("Modal", () => {
  it("renders modal content when open", () => {
    render(
      <Modal open title="Example modal" onClose={vi.fn()}>
        Modal body
      </Modal>
    );

    expect(screen.getByRole("dialog", { name: /example modal/i })).toBeInTheDocument();
    expect(screen.getByText("Modal body")).toBeInTheDocument();
  });

  it("calls onClose when close button is clicked", () => {
    const onClose = vi.fn();

    render(
      <Modal open title="Example modal" onClose={onClose}>
        Modal body
      </Modal>
    );

    fireEvent.click(screen.getByRole("button", { name: /close/i }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
```

---

# 17) Recommended support test: `src/shared/components/__tests__/PageHeader.test.jsx`

```jsx
import { render, screen } from "@testing-library/react";
import PageHeader from "../PageHeader";

describe("PageHeader", () => {
  it("renders title and description", () => {
    render(
      <PageHeader
        eyebrow="Patient workspace"
        title="Appointments"
        description="Manage upcoming care visits."
      />
    );

    expect(screen.getByText("Appointments")).toBeInTheDocument();
    expect(screen.getByText("Manage upcoming care visits.")).toBeInTheDocument();
  });
});
```

---

# 18) Recommended usage guidance for pages and modules

## Use this hardening pattern going forward

### Pages
Pages should mostly do:
- hook calls
- layout composition
- section ordering
- route-aware actions

### Hooks
Hooks should do:
- API calls through services
- backend payload normalization
- derived UI state
- submission and loading logic

### UI components
UI components should do:
- rendering
- accessibility props
- visual state
- small interaction behavior

### Shared components
Shared components should do:
- repeatable layout patterns
- repeatable error summary patterns
- repeatable feedback primitives

---

# 19) Example refactor recommendation for earlier phases

You asked not to scatter mapping logic across pages. Here is exactly how I recommend you handle cleanup as you continue:

## Appointments
Move any repeated appointment normalization into:

- `src/modules/appointments/utils/mappers.js`

Example exported functions:
- `normalizeAppointment`
- `normalizeProviderAppointment`

## Telehealth
Move telehealth session normalization into:

- `src/modules/telehealth/utils/mappers.js`

Example exported functions:
- `normalizeSession`
- `deriveSessionReadiness`

## Admin
Move admin payload mapping into:

- `src/modules/admin/utils/mappers.js`

Example exported functions:
- `normalizeMetricCard`
- `normalizeUsers`
- `normalizeAuditLogs`
- `normalizeUtilizationRows`

## Encounters / Referrals
Do the same when more reuse appears:
- `src/modules/encounters/utils/mappers.js`
- `src/modules/referrals/utils/mappers.js`

### Strong recommendation
Do **not** rush to move every mapper today if it will slow this phase down.  
But from this phase onward, every new mapper should be placed in:
- the module hook, if used once
- the module utils file, if reused

That is the best balance of cleanliness and delivery speed for your current development method.

---

# 20) Exact commands to run after pasting these files

## 1. Run the shared UI tests
```bash
npx vitest run src/components/ui/__tests__/Button.test.jsx src/components/ui/__tests__/Card.test.jsx src/components/ui/__tests__/Input.test.jsx src/components/ui/__tests__/Modal.test.jsx src/shared/components/__tests__/PageHeader.test.jsx
```

## 2. Start the frontend
```bash
npm run dev
```

## 3. Manual hardening checklist
As you move through the app manually, verify:
1. tab navigation works on major forms
2. focused inputs are clearly visible
3. error text is visible and near the right field
4. major forms can display top-level error summaries
5. shared headers look consistent across patient, provider, and admin pages
6. shared cards feel visually consistent
7. modals can be closed by button and Escape key
8. empty and error states remain understandable

---

# Completion checklist

This phase is complete when all of the following are true:

- shared page header and section card patterns exist
- form error summary exists
- reusable input, select, textarea, modal, table, and tabs primitives exist
- button and card tests pass
- additional shared UI smoke tests pass
- keyboard navigation is improved
- form feedback is clearer
- the product feels more consistent across patient, provider, and admin areas
- backend mapping logic is no longer being newly introduced inside page components

---

# Practical note before Phase 10
Do not try to fully redesign every earlier page during this hardening phase. Add the shared primitives now, then refactor touched pages gradually. That keeps progress stable and avoids unnecessary regressions while still moving the codebase toward a cleaner architecture.
