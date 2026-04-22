# PBBF BLISS Frontend — Phase 2 Populated Files  
## Authentication UX and Route Protection

## Objective
Build the visible authentication layer and lock private areas behind role-aware guards.

This phase finishes the frontend authentication experience for the React application in:

`bliss-telehealth/pbbf-telehealth`

It keeps the current modular structure, uses one canonical API client strategy, hydrates auth state from persisted storage, and protects private routes by role.

---

## Important Phase 2 decisions

### 1. Canonical API client
Use:

- `src/services/api.js`

as the only canonical API client.

Then let:

- `src/modules/auth/services/authApi.js`

be the auth-specific wrapper around that shared client.

If `src/shared/services/api.js` still exists from earlier work, do **not** keep two different clients with different behavior. Either:
- delete the duplicate later, or
- replace its contents with a re-export of `src/services/api.js`

### 2. Store strategy
This package uses a lightweight auth store built on `useSyncExternalStore`, so it does **not** require Zustand or Redux.

### 3. Route protection strategy
The protection chain is:

- `ProtectedRoute.jsx` → wrapper used in route definitions
- `AuthGuard.jsx` → blocks unauthenticated access
- `RoleGuard.jsx` → blocks wrong-role access

### 4. Backend assumptions
This frontend phase assumes the backend auth layer from your earlier backend phase exposes endpoints similar to:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/forgot-password` (optional — this UI handles missing backend support gracefully)

If your real backend paths differ, only update the endpoint URLs inside `src/modules/auth/services/authApi.js`.

---

## File list for this phase

### Modify these files
- `src/pages/auth/Login.jsx`
- `src/routes/ProtectedRoute.jsx`
- `src/shared/guards/AuthGuard.jsx`
- `src/shared/guards/RoleGuard.jsx`
- `src/store/authStore.js`
- `src/services/auth.service.js`
- `src/services/api.js`

### Create these files if missing
- `src/modules/auth/pages/Register.jsx`
- `src/modules/auth/pages/ForgotPassword.jsx`
- `src/modules/auth/components/LoginForm.jsx`
- `src/modules/auth/components/RegisterForm.jsx`
- `src/modules/auth/hooks/useAuth.js`
- `src/modules/auth/services/authApi.js`
- `src/modules/auth/utils/validators.js`
- `src/modules/auth/__tests__/LoginForm.test.jsx`
- `src/modules/auth/__tests__/RegisterForm.test.jsx`
- `src/modules/auth/__tests__/AuthGuard.test.jsx`

### Recommended support test added for completeness
- `src/modules/auth/__tests__/authStore.test.jsx`

---

# 1) `src/services/api.js`

```jsx
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000/api/v1";

class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

const AUTH_STORAGE_KEY = "pbbf_auth_state";

function readStoredAuth() {
  try {
    const raw = window.localStorage.getItem(AUTH_STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function buildHeaders({ headers = {}, token, isJson = true } = {}) {
  const finalHeaders = new Headers(headers);

  if (isJson && !finalHeaders.has("Content-Type")) {
    finalHeaders.set("Content-Type", "application/json");
  }

  if (token) {
    finalHeaders.set("Authorization", `Bearer ${token}`);
  }

  return finalHeaders;
}

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    return response.json();
  }

  return response.text();
}

export async function apiRequest(path, options = {}) {
  const authState = readStoredAuth();
  const token = options.token || authState?.accessToken || null;

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method || "GET",
    headers: buildHeaders({
      headers: options.headers,
      token,
      isJson: options.isJson !== false,
    }),
    body:
      options.body === undefined
        ? undefined
        : options.isJson === false
        ? options.body
        : JSON.stringify(options.body),
    credentials: options.credentials || "include",
  });

  const data = await parseResponse(response);

  if (!response.ok) {
    const message =
      (typeof data === "object" && data?.message) ||
      (typeof data === "object" && data?.detail) ||
      "Request failed.";
    throw new ApiError(message, response.status, data);
  }

  return data;
}

export const api = {
  get: (path, options = {}) => apiRequest(path, { ...options, method: "GET" }),
  post: (path, body, options = {}) => apiRequest(path, { ...options, method: "POST", body }),
  put: (path, body, options = {}) => apiRequest(path, { ...options, method: "PUT", body }),
  patch: (path, body, options = {}) => apiRequest(path, { ...options, method: "PATCH", body }),
  delete: (path, options = {}) => apiRequest(path, { ...options, method: "DELETE" }),
};

export { API_BASE_URL, ApiError };
```

---

# 2) `src/store/authStore.js`

```jsx
import { useSyncExternalStore } from "react";

const AUTH_STORAGE_KEY = "pbbf_auth_state";

const initialState = {
  isHydrated: false,
  isAuthenticated: false,
  accessToken: null,
  refreshToken: null,
  user: null,
};

let state = { ...initialState };
const listeners = new Set();

function emitChange() {
  listeners.forEach((listener) => listener());
}

function persistAuth(nextState) {
  try {
    const payload = {
      accessToken: nextState.accessToken,
      refreshToken: nextState.refreshToken,
      user: nextState.user,
    };

    if (payload.accessToken || payload.refreshToken || payload.user) {
      window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(payload));
    } else {
      window.localStorage.removeItem(AUTH_STORAGE_KEY);
    }
  } catch {
    // ignore storage failures in the UI layer
  }
}

function setState(partial) {
  state = { ...state, ...partial };
  persistAuth(state);
  emitChange();
}

function clearState() {
  state = {
    ...initialState,
    isHydrated: true,
  };
  persistAuth(state);
  emitChange();
}

function hydrateAuth() {
  try {
    const raw = window.localStorage.getItem(AUTH_STORAGE_KEY);

    if (!raw) {
      state = { ...initialState, isHydrated: true };
      emitChange();
      return state;
    }

    const parsed = JSON.parse(raw);

    state = {
      isHydrated: true,
      isAuthenticated: Boolean(parsed?.accessToken && parsed?.user),
      accessToken: parsed?.accessToken || null,
      refreshToken: parsed?.refreshToken || null,
      user: parsed?.user || null,
    };
    emitChange();
    return state;
  } catch {
    state = { ...initialState, isHydrated: true };
    emitChange();
    return state;
  }
}

function loginSuccess(payload) {
  state = {
    isHydrated: true,
    isAuthenticated: true,
    accessToken: payload?.accessToken || null,
    refreshToken: payload?.refreshToken || null,
    user: payload?.user || null,
  };
  persistAuth(state);
  emitChange();
  return state;
}

function updateUser(user) {
  setState({
    user,
    isAuthenticated: Boolean(state.accessToken && user),
    isHydrated: true,
  });
}

function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function getSnapshot() {
  return state;
}

function getServerSnapshot() {
  return initialState;
}

function getState() {
  return state;
}

function hasRole(allowedRoles = []) {
  if (!allowedRoles.length) return true;
  const role = state.user?.role;
  return allowedRoles.includes(role);
}

export function useAuthStore(selector = (snapshot) => snapshot) {
  const snapshot = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
  return selector(snapshot);
}

export {
  AUTH_STORAGE_KEY,
  initialState,
  subscribe,
  getState,
  hydrateAuth,
  loginSuccess,
  updateUser,
  clearState,
  hasRole,
};
```

---

# 3) `src/services/auth.service.js`

```jsx
import { ApiError } from "./api";
import { clearState, getState, hydrateAuth, loginSuccess, updateUser } from "../store/authStore";
import {
  forgotPasswordRequest,
  getCurrentUserRequest,
  loginRequest,
  logoutRequest,
  registerRequest,
} from "../modules/auth/services/authApi";

function normalizeAuthResponse(response) {
  const data = response?.data || response;

  return {
    accessToken: data?.access_token || data?.accessToken || null,
    refreshToken: data?.refresh_token || data?.refreshToken || null,
    user: data?.user || null,
    message: response?.message || data?.message || "Authentication successful.",
  };
}

async function login(credentials) {
  const response = await loginRequest(credentials);
  const normalized = normalizeAuthResponse(response);

  if (!normalized.accessToken || !normalized.user) {
    throw new ApiError("Login response is missing token or user data.", 500, response);
  }

  loginSuccess(normalized);
  return normalized;
}

async function register(payload) {
  const response = await registerRequest(payload);
  const normalized = normalizeAuthResponse(response);

  if (normalized.accessToken && normalized.user) {
    loginSuccess(normalized);
  }

  return normalized;
}

async function hydrate() {
  const hydrated = hydrateAuth();

  if (!hydrated.isAuthenticated || !hydrated.accessToken) {
    return hydrated;
  }

  try {
    const response = await getCurrentUserRequest();
    const data = response?.data || response;
    const user = data?.user || data;
    updateUser(user);
    return getState();
  } catch {
    clearState();
    return getState();
  }
}

async function logout() {
  try {
    await logoutRequest();
  } catch {
    // best-effort logout
  } finally {
    clearState();
  }
}

async function requestPasswordReset(email) {
  return forgotPasswordRequest({ email });
}

function getCurrentUser() {
  return getState().user;
}

function isAuthenticated() {
  return getState().isAuthenticated;
}

export const authService = {
  login,
  register,
  hydrate,
  logout,
  getCurrentUser,
  isAuthenticated,
  requestPasswordReset,
};
```

---

# 4) `src/modules/auth/services/authApi.js`

```jsx
import { api } from "../../../services/api";

export function loginRequest(payload) {
  return api.post("/auth/login", payload);
}

export function registerRequest(payload) {
  return api.post("/auth/register", payload);
}

export function logoutRequest() {
  return api.post("/auth/logout", {});
}

export function getCurrentUserRequest() {
  return api.get("/auth/me");
}

export function forgotPasswordRequest(payload) {
  return api.post("/auth/forgot-password", payload);
}
```

---

# 5) `src/modules/auth/utils/validators.js`

```jsx
export function validateEmail(value) {
  if (!value?.trim()) return "Email is required.";
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(value.trim())) return "Enter a valid email address.";
  return "";
}

export function validatePassword(value) {
  if (!value) return "Password is required.";
  if (value.length < 8) return "Password must be at least 8 characters.";
  return "";
}

export function validateLoginForm(values) {
  return {
    email: validateEmail(values.email),
    password: validatePassword(values.password),
  };
}

export function validateRegisterForm(values) {
  const errors = {
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  };

  if (!values.fullName?.trim()) {
    errors.fullName = "Full name is required.";
  }

  errors.email = validateEmail(values.email);
  errors.password = validatePassword(values.password);

  if (!values.confirmPassword) {
    errors.confirmPassword = "Please confirm your password.";
  } else if (values.confirmPassword !== values.password) {
    errors.confirmPassword = "Passwords do not match.";
  }

  return errors;
}

export function hasFormErrors(errors) {
  return Object.values(errors).some(Boolean);
}
```

---

# 6) `src/modules/auth/hooks/useAuth.js`

```jsx
import { useMemo } from "react";
import { authService } from "../../../services/auth.service";
import { useAuthStore } from "../../../store/authStore";

export function useAuth() {
  const authState = useAuthStore();

  return useMemo(
    () => ({
      ...authState,
      login: authService.login,
      register: authService.register,
      hydrate: authService.hydrate,
      logout: authService.logout,
      requestPasswordReset: authService.requestPasswordReset,
    }),
    [authState]
  );
}
```

---

# 7) `src/shared/guards/AuthGuard.jsx`

```jsx
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import Loader from "../components/Loader";

export default function AuthGuard({ children }) {
  const location = useLocation();
  const { isHydrated, isAuthenticated } = useAuthStore((state) => ({
    isHydrated: state.isHydrated,
    isAuthenticated: state.isAuthenticated,
  }));

  if (!isHydrated) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Loader label="Checking your session..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return children || <Outlet />;
}
```

---

# 8) `src/shared/guards/RoleGuard.jsx`

```jsx
import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";

function getHomePathForRole(role) {
  switch (role) {
    case "admin":
      return "/admin";
    case "provider":
    case "counselor":
    case "care_coordinator":
      return "/provider";
    case "patient":
    default:
      return "/patient";
  }
}

export default function RoleGuard({ allowedRoles = [], children }) {
  const user = useAuthStore((state) => state.user);

  if (!allowedRoles.length) {
    return children || <Outlet />;
  }

  if (!user?.role || !allowedRoles.includes(user.role)) {
    return <Navigate to={getHomePathForRole(user?.role)} replace />;
  }

  return children || <Outlet />;
}
```

---

# 9) `src/routes/ProtectedRoute.jsx`

```jsx
import AuthGuard from "../shared/guards/AuthGuard";
import RoleGuard from "../shared/guards/RoleGuard";

export default function ProtectedRoute({ children, allowedRoles = [] }) {
  return (
    <AuthGuard>
      <RoleGuard allowedRoles={allowedRoles}>{children}</RoleGuard>
    </AuthGuard>
  );
}
```

---

# 10) `src/pages/auth/Login.jsx`

```jsx
import { Link } from "react-router-dom";
import LoginForm from "../../modules/auth/components/LoginForm";

export default function Login() {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto grid min-h-screen max-w-6xl lg:grid-cols-2">
        <div className="hidden flex-col justify-center bg-sky-900 px-10 py-16 text-white lg:flex">
          <p className="mb-3 text-sm uppercase tracking-[0.22em] text-sky-200">
            Post Baby Bliss Foundation
          </p>
          <h1 className="max-w-md text-4xl font-bold leading-tight">
            Secure telehealth care for postpartum support, screening, and follow-up.
          </h1>
          <p className="mt-5 max-w-lg text-base leading-7 text-sky-100">
            Sign in to access appointments, intake forms, screenings, telehealth visits,
            provider documentation, referrals, and operational reporting.
          </p>
        </div>

        <div className="flex items-center justify-center px-6 py-12">
          <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
            <div className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900">Welcome back</h2>
              <p className="mt-2 text-sm text-slate-600">
                Sign in to continue to the PBBF telehealth platform.
              </p>
            </div>

            <LoginForm />

            <div className="mt-6 space-y-2 text-sm text-slate-600">
              <p>
                Need an account?{" "}
                <Link to="/register" className="font-medium text-sky-700 hover:text-sky-800">
                  Create one here
                </Link>
              </p>
              <p>
                Forgot your password?{" "}
                <Link to="/forgot-password" className="font-medium text-sky-700 hover:text-sky-800">
                  Reset access
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

# 11) `src/modules/auth/pages/Register.jsx`

```jsx
import { Link } from "react-router-dom";
import RegisterForm from "../components/RegisterForm";

export default function Register() {
  return (
    <div className="min-h-screen bg-slate-50 px-6 py-12">
      <div className="mx-auto max-w-lg rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
        <div className="mb-8">
          <p className="text-sm font-medium uppercase tracking-[0.18em] text-sky-700">
            New patient onboarding
          </p>
          <h1 className="mt-2 text-3xl font-semibold text-slate-900">Create your account</h1>
          <p className="mt-3 text-sm leading-6 text-slate-600">
            Start by creating your secure account. You will complete intake, consent,
            appointment booking, and telehealth access after sign-up.
          </p>
        </div>

        <RegisterForm />

        <p className="mt-6 text-sm text-slate-600">
          Already have an account?{" "}
          <Link to="/login" className="font-medium text-sky-700 hover:text-sky-800">
            Sign in here
          </Link>
        </p>
      </div>
    </div>
  );
}
```

---

# 12) `src/modules/auth/pages/ForgotPassword.jsx`

```jsx
import { useState } from "react";
import { Link } from "react-router-dom";
import { validateEmail } from "../utils/validators";
import { useAuth } from "../hooks/useAuth";

export default function ForgotPassword() {
  const { requestPasswordReset } = useAuth();
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [serverMessage, setServerMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setServerMessage("");

    const emailError = validateEmail(email);
    setError(emailError);

    if (emailError) return;

    try {
      setIsSubmitting(true);
      const response = await requestPasswordReset(email.trim());
      setServerMessage(
        response?.message ||
          "If this email exists in the system, recovery instructions will be sent."
      );
    } catch (requestError) {
      setServerMessage(
        requestError?.message ||
          "Password recovery is not available yet. Please contact support."
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 px-6 py-12">
      <div className="mx-auto max-w-lg rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
        <h1 className="text-3xl font-semibold text-slate-900">Reset your password</h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          Enter your email address and we will attempt to start the account recovery flow.
        </p>

        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="forgot-email" className="mb-2 block text-sm font-medium text-slate-700">
              Email address
            </label>
            <input
              id="forgot-email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
              placeholder="you@example.com"
            />
            {error ? <p className="mt-2 text-sm text-rose-600">{error}</p> : null}
          </div>

          {serverMessage ? (
            <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
              {serverMessage}
            </div>
          ) : null}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-xl bg-sky-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isSubmitting ? "Submitting..." : "Send recovery request"}
          </button>
        </form>

        <p className="mt-6 text-sm text-slate-600">
          Back to{" "}
          <Link to="/login" className="font-medium text-sky-700 hover:text-sky-800">
            sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
```

---

# 13) `src/modules/auth/components/LoginForm.jsx`

```jsx
import { useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { hasFormErrors, validateLoginForm } from "../utils/validators";

function getHomePathForRole(role) {
  switch (role) {
    case "admin":
      return "/admin";
    case "provider":
    case "counselor":
    case "care_coordinator":
      return "/provider";
    case "patient":
    default:
      return "/patient";
  }
}

export default function LoginForm() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [values, setValues] = useState({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({
    email: "",
    password: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [serverError, setServerError] = useState("");

  const redirectTarget = useMemo(
    () => location.state?.from || null,
    [location.state]
  );

  function updateField(field, value) {
    setValues((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: "" }));
    setServerError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const nextErrors = validateLoginForm(values);
    setErrors(nextErrors);

    if (hasFormErrors(nextErrors)) return;

    try {
      setIsSubmitting(true);
      const result = await login({
        email: values.email.trim(),
        password: values.password,
      });

      const role = result?.user?.role;
      navigate(redirectTarget || getHomePathForRole(role), { replace: true });
    } catch (error) {
      setServerError(error?.message || "Unable to sign in.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form className="space-y-5" onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="login-email" className="mb-2 block text-sm font-medium text-slate-700">
          Email address
        </label>
        <input
          id="login-email"
          name="email"
          type="email"
          autoComplete="email"
          value={values.email}
          onChange={(event) => updateField("email", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="you@example.com"
        />
        {errors.email ? <p className="mt-2 text-sm text-rose-600">{errors.email}</p> : null}
      </div>

      <div>
        <label htmlFor="login-password" className="mb-2 block text-sm font-medium text-slate-700">
          Password
        </label>
        <input
          id="login-password"
          name="password"
          type="password"
          autoComplete="current-password"
          value={values.password}
          onChange={(event) => updateField("password", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="Enter your password"
        />
        {errors.password ? <p className="mt-2 text-sm text-rose-600">{errors.password}</p> : null}
      </div>

      {serverError ? (
        <div className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {serverError}
        </div>
      ) : null}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-xl bg-sky-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isSubmitting ? "Signing in..." : "Sign in"}
      </button>
    </form>
  );
}
```

---

# 14) `src/modules/auth/components/RegisterForm.jsx`

```jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { hasFormErrors, validateRegisterForm } from "../utils/validators";

function getHomePathForRole(role) {
  switch (role) {
    case "admin":
      return "/admin";
    case "provider":
    case "counselor":
    case "care_coordinator":
      return "/provider";
    case "patient":
    default:
      return "/patient";
  }
}

export default function RegisterForm() {
  const navigate = useNavigate();
  const { register } = useAuth();

  const [values, setValues] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "patient",
  });
  const [errors, setErrors] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [serverError, setServerError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function updateField(field, value) {
    setValues((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: "" }));
    setServerError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const nextErrors = validateRegisterForm(values);
    setErrors(nextErrors);

    if (hasFormErrors(nextErrors)) return;

    try {
      setIsSubmitting(true);
      const result = await register({
        full_name: values.fullName.trim(),
        email: values.email.trim(),
        password: values.password,
        role: values.role,
      });

      if (result?.user?.role && result?.accessToken) {
        navigate(getHomePathForRole(result.user.role), { replace: true });
      } else {
        navigate("/login", { replace: true });
      }
    } catch (error) {
      setServerError(error?.message || "Unable to create account.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form className="space-y-5" onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="register-full-name" className="mb-2 block text-sm font-medium text-slate-700">
          Full name
        </label>
        <input
          id="register-full-name"
          type="text"
          value={values.fullName}
          onChange={(event) => updateField("fullName", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="Enter your full name"
        />
        {errors.fullName ? (
          <p className="mt-2 text-sm text-rose-600">{errors.fullName}</p>
        ) : null}
      </div>

      <div>
        <label htmlFor="register-email" className="mb-2 block text-sm font-medium text-slate-700">
          Email address
        </label>
        <input
          id="register-email"
          type="email"
          value={values.email}
          onChange={(event) => updateField("email", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="you@example.com"
        />
        {errors.email ? <p className="mt-2 text-sm text-rose-600">{errors.email}</p> : null}
      </div>

      <div>
        <label htmlFor="register-password" className="mb-2 block text-sm font-medium text-slate-700">
          Password
        </label>
        <input
          id="register-password"
          type="password"
          value={values.password}
          onChange={(event) => updateField("password", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="Create a strong password"
        />
        {errors.password ? <p className="mt-2 text-sm text-rose-600">{errors.password}</p> : null}
      </div>

      <div>
        <label
          htmlFor="register-confirm-password"
          className="mb-2 block text-sm font-medium text-slate-700"
        >
          Confirm password
        </label>
        <input
          id="register-confirm-password"
          type="password"
          value={values.confirmPassword}
          onChange={(event) => updateField("confirmPassword", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
          placeholder="Re-enter your password"
        />
        {errors.confirmPassword ? (
          <p className="mt-2 text-sm text-rose-600">{errors.confirmPassword}</p>
        ) : null}
      </div>

      <div>
        <label htmlFor="register-role" className="mb-2 block text-sm font-medium text-slate-700">
          Role
        </label>
        <select
          id="register-role"
          value={values.role}
          onChange={(event) => updateField("role", event.target.value)}
          className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
        >
          <option value="patient">Patient</option>
          <option value="provider">Provider</option>
          <option value="care_coordinator">Care Coordinator</option>
          <option value="admin">Admin</option>
        </select>
      </div>

      {serverError ? (
        <div className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {serverError}
        </div>
      ) : null}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-xl bg-sky-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-sky-800 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isSubmitting ? "Creating account..." : "Create account"}
      </button>
    </form>
  );
}
```

---

# 15) `src/modules/auth/__tests__/LoginForm.test.jsx`

```jsx
import { MemoryRouter } from "react-router-dom";
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";

import LoginForm from "../components/LoginForm";

const loginMock = vi.fn();

vi.mock("../hooks/useAuth", () => ({
  useAuth: () => ({
    login: loginMock,
  }),
}));

describe("LoginForm", () => {
  beforeEach(() => {
    loginMock.mockReset();
  });

  it("shows validation errors for empty inputs", async () => {
    render(
      <MemoryRouter>
        <LoginForm />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    expect(await screen.findByText("Email is required.")).toBeInTheDocument();
    expect(await screen.findByText("Password is required.")).toBeInTheDocument();
  });

  it("shows validation error for invalid email", async () => {
    render(
      <MemoryRouter>
        <LoginForm />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "invalid-email" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    expect(await screen.findByText("Enter a valid email address.")).toBeInTheDocument();
  });
});
```

---

# 16) `src/modules/auth/__tests__/RegisterForm.test.jsx`

```jsx
import { MemoryRouter } from "react-router-dom";
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";

import RegisterForm from "../components/RegisterForm";

const registerMock = vi.fn();

vi.mock("../hooks/useAuth", () => ({
  useAuth: () => ({
    register: registerMock,
  }),
}));

describe("RegisterForm", () => {
  beforeEach(() => {
    registerMock.mockReset();
  });

  it("shows validation errors for missing required fields", async () => {
    render(
      <MemoryRouter>
        <RegisterForm />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /create account/i }));

    expect(await screen.findByText("Full name is required.")).toBeInTheDocument();
    expect(await screen.findByText("Email is required.")).toBeInTheDocument();
    expect(await screen.findByText("Password is required.")).toBeInTheDocument();
    expect(await screen.findByText("Please confirm your password.")).toBeInTheDocument();
  });

  it("shows password mismatch validation error", async () => {
    render(
      <MemoryRouter>
        <RegisterForm />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/full name/i), {
      target: { value: "Test User" },
    });
    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "user@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/^password$/i), {
      target: { value: "password123" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "different123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /create account/i }));

    expect(await screen.findByText("Passwords do not match.")).toBeInTheDocument();
  });
});
```

---

# 17) `src/modules/auth/__tests__/AuthGuard.test.jsx`

```jsx
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

import AuthGuard from "../../../shared/guards/AuthGuard";
import RoleGuard from "../../../shared/guards/RoleGuard";

const useAuthStoreMock = vi.fn();

vi.mock("../../../store/authStore", () => ({
  useAuthStore: (selector) =>
    selector(
      useAuthStoreMock() || {
        isHydrated: true,
        isAuthenticated: false,
        user: null,
      }
    ),
}));

describe("AuthGuard and RoleGuard", () => {
  it("redirects to login when user is unauthenticated", () => {
    useAuthStoreMock.mockReturnValue({
      isHydrated: true,
      isAuthenticated: false,
      user: null,
    });

    render(
      <MemoryRouter initialEntries={["/patient"]}>
        <Routes>
          <Route path="/login" element={<div>Login Screen</div>} />
          <Route
            path="/patient"
            element={
              <AuthGuard>
                <div>Patient Dashboard</div>
              </AuthGuard>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Login Screen")).toBeInTheDocument();
  });

  it("renders protected content when user is authenticated", () => {
    useAuthStoreMock.mockReturnValue({
      isHydrated: true,
      isAuthenticated: true,
      user: { role: "patient" },
    });

    render(
      <MemoryRouter initialEntries={["/patient"]}>
        <Routes>
          <Route
            path="/patient"
            element={
              <AuthGuard>
                <div>Patient Dashboard</div>
              </AuthGuard>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Patient Dashboard")).toBeInTheDocument();
  });

  it("redirects wrong role to role home path", () => {
    useAuthStoreMock.mockReturnValue({
      isHydrated: true,
      isAuthenticated: true,
      user: { role: "patient" },
    });

    render(
      <MemoryRouter initialEntries={["/admin"]}>
        <Routes>
          <Route path="/patient" element={<div>Patient Home</div>} />
          <Route
            path="/admin"
            element={
              <RoleGuard allowedRoles={["admin"]}>
                <div>Admin Area</div>
              </RoleGuard>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Patient Home")).toBeInTheDocument();
  });
});
```

---

# 18) Recommended support test: `src/modules/auth/__tests__/authStore.test.jsx`

```jsx
import { afterEach, describe, expect, it } from "vitest";
import {
  AUTH_STORAGE_KEY,
  clearState,
  getState,
  hydrateAuth,
  loginSuccess,
  updateUser,
} from "../../../store/authStore";

describe("authStore", () => {
  afterEach(() => {
    window.localStorage.removeItem(AUTH_STORAGE_KEY);
    clearState();
  });

  it("hydrates empty state when storage is empty", () => {
    const state = hydrateAuth();
    expect(state.isHydrated).toBe(true);
    expect(state.isAuthenticated).toBe(false);
    expect(state.user).toBeNull();
  });

  it("transitions to authenticated state on loginSuccess", () => {
    loginSuccess({
      accessToken: "access-token",
      refreshToken: "refresh-token",
      user: { id: "user-1", role: "patient", full_name: "Test User" },
    });

    const state = getState();
    expect(state.isAuthenticated).toBe(true);
    expect(state.accessToken).toBe("access-token");
    expect(state.user.role).toBe("patient");
  });

  it("updates only the user payload when updateUser is called", () => {
    loginSuccess({
      accessToken: "access-token",
      refreshToken: "refresh-token",
      user: { id: "user-1", role: "patient", full_name: "Old Name" },
    });

    updateUser({ id: "user-1", role: "patient", full_name: "New Name" });

    const state = getState();
    expect(state.user.full_name).toBe("New Name");
    expect(state.isAuthenticated).toBe(true);
  });
});
```

---

# 19) Required support patch for route wiring: `src/app/AppRoutes.jsx`

This phase cannot be considered complete unless the auth pages and protected route wrapper are actually registered in the route map.

If your current `src/app/AppRoutes.jsx` is still incomplete, use this version or merge the same routing pattern into it.

```jsx
import { Navigate, Route, Routes } from "react-router-dom";
import ProtectedRoute from "../routes/ProtectedRoute";

import Login from "../pages/auth/Login";
import Register from "../modules/auth/pages/Register";
import ForgotPassword from "../modules/auth/pages/ForgotPassword";

import PatientDashboard from "../pages/patient/Dashboard";
import ProviderDashboard from "../pages/provider/Dashboard";
import AdminDashboard from "../pages/admin/Dashboard";

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

# 20) Recommended support patch for hydration boot: `src/main.jsx`

To make token persistence actually work after refresh, make sure auth hydration runs once before the main app becomes interactive.

If your `src/main.jsx` does not already do this, merge this patch:

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";
import { authService } from "./services/auth.service";

authService.hydrate();

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

---

# Exact commands to run after pasting these files

## 1. Install required test packages if they are not already installed
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

## 2. Ensure React Router is installed
```bash
npm install react-router-dom
```

## 3. Run the auth-focused frontend tests
```bash
npx vitest run src/modules/auth/__tests__/LoginForm.test.jsx src/modules/auth/__tests__/RegisterForm.test.jsx src/modules/auth/__tests__/AuthGuard.test.jsx src/modules/auth/__tests__/authStore.test.jsx
```

## 4. Start the frontend locally
```bash
npm run dev
```

---

# Completion checklist

This phase is complete when all of the following are true:

- login screen renders correctly
- registration screen renders correctly
- forgot-password screen renders without breaking the route tree
- auth store hydrates from persisted browser storage
- access token and user data persist across page refresh
- logout clears persisted auth state
- private routes redirect unauthenticated users to `/login`
- wrong-role users are blocked from protected areas
- only one API client strategy is being used
- auth tests pass cleanly

---

# Practical note before Phase 3
This phase will only work smoothly if your role strings match exactly between frontend and backend.

Verify that the backend is returning role values consistently, especially for:
- `patient`
- `provider`
- `care_coordinator`
- `counselor`
- `admin`

If your backend uses different role names, align them now before building patient onboarding and dashboard features.
