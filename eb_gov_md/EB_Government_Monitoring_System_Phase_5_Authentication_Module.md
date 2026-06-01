# Phase 5 — Authentication Module

**Project:** EB Government Monitoring System  
**Frontend:** React + TypeScript + Vite + Tailwind CSS v4  
**Phase Goal:** Replace the temporary Phase 3 authentication placeholders with a real frontend authentication module foundation: login screen, forgot password screen, role-based login handling, persistent auth state, logout flow, safe errors, and future MFA readiness.

---

## Phase 4 Confirmation

Phase 4 is complete.

Your build passed successfully:

```txt
✓ 1815 modules transformed.
✓ built in 2.14s
```

The screenshot also confirms the app shell is still stable after Phase 4:

- `/dashboard` loads successfully.
- Sidebar is visible.
- Topbar is visible.
- Authenticated user display is visible.
- Navigation skeleton still works.

You can proceed to Phase 5.

---

# Phase 5 Objectives

This phase implements:

- Login screen.
- Forgot password screen.
- Role-based login handling.
- Persistent authentication state using Zustand.
- Safe logout behavior.
- Auth redirects after login.
- Safe invalid login handling.
- Preparation for future MFA support.

---

# Important Phase 5 Design Decision

In Phase 3, `useAuth.ts` used temporary local React state. That was enough for route testing, but not good enough for a real authentication module because every hook instance could hold separate state.

In Phase 5, authentication state moves into:

```txt
src/store/auth.store.ts
```

This gives the app one shared auth state across:

- Login form
- ProtectedRoute
- RoleGuard
- Sidebar
- Topbar
- Logout button

---

# 1. Create Phase 5 Directories

Run from the project root:

```bash
mkdir -p src/features/auth/components src/features/auth/pages src/features/auth/hooks src/features/auth/schemas src/store
```

---

# 2. Create Phase 5 Files

Run from the project root:

```bash
touch src/features/auth/pages/LoginPage.tsx src/features/auth/pages/ForgotPasswordPage.tsx src/features/auth/components/LoginForm.tsx src/features/auth/components/ForgotPasswordForm.tsx src/features/auth/components/RoleSelect.tsx src/features/auth/hooks/useLogin.ts src/features/auth/hooks/useLogout.ts src/features/auth/schemas/auth.schema.ts src/store/auth.store.ts
```

The following existing files will also be updated:

```txt
src/hooks/useAuth.ts
src/app/router.tsx
src/services/auth.service.ts
src/types/auth.types.ts
```

---

# 3. Populate Authentication Types

## `src/types/auth.types.ts`

Replace the file content with this:

```ts
import type { UserRole } from '@/config/permissions';
import type { User } from './user.types';

export type LoginPayload = {
  email: string;
  password: string;
  role: UserRole;
};

export type LoginResponse = {
  user: User;
  accessToken: string;
  refreshToken?: string;
  expiresAt?: string;
  mfaRequired?: boolean;
  mfaToken?: string;
};

export type ForgotPasswordPayload = {
  email: string;
};

export type ResetPasswordPayload = {
  token: string;
  password: string;
  confirmPassword: string;
};

export type AuthSession = {
  user: User;
  accessToken: string;
  refreshToken?: string;
  expiresAt?: string;
};

export type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'unauthenticated' | 'error';
```

---

# 4. Populate Auth Schema

## `src/features/auth/schemas/auth.schema.ts`

```ts
import { z } from 'zod';

import { USER_ROLES } from '@/config/permissions';

const roleValues = Object.values(USER_ROLES) as [string, ...string[]];

export const loginSchema = z.object({
  email: z
    .string()
    .trim()
    .min(1, 'Email address is required.')
    .email('Enter a valid email address.'),

  password: z
    .string()
    .min(1, 'Password is required.')
    .min(4, 'Password must be at least 4 characters for this MVP.'),

  role: z.enum(roleValues, {
    message: 'Select a valid role.',
  }),
});

export const forgotPasswordSchema = z.object({
  email: z
    .string()
    .trim()
    .min(1, 'Email address is required.')
    .email('Enter a valid email address.'),
});

export type LoginFormValues = z.infer<typeof loginSchema>;
export type ForgotPasswordFormValues = z.infer<typeof forgotPasswordSchema>;
```

---

# 5. Populate Auth Store

## `src/store/auth.store.ts`

```ts
import { create } from 'zustand';

import { USER_ROLES } from '@/config/permissions';
import { storage } from '@/lib/storage';
import type { AuthSession, AuthStatus } from '@/types/auth.types';
import type { User } from '@/types/user.types';

const demoAdminUser: User = {
  id: 'user_demo_admin',
  fullName: 'Admin User',
  email: 'admin@eb-gms.local',
  role: USER_ROLES.GOVERNMENT_ADMIN,
  title: 'Government Administrator',
  status: 'ACTIVE',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
};

const demoSession: AuthSession = {
  user: demoAdminUser,
  accessToken: 'demo-access-token',
  refreshToken: 'demo-refresh-token',
};

type AuthStore = {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  status: AuthStatus;
  error: string | null;
  mfaRequired: boolean;
  mfaToken: string | null;

  hydrate: () => void;
  setSession: (session: AuthSession) => void;
  setMfaRequired: (mfaToken: string) => void;
  setLoading: () => void;
  setError: (message: string) => void;
  clearError: () => void;
  logout: () => void;
};

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  status: 'idle',
  error: null,
  mfaRequired: false,
  mfaToken: null,

  hydrate: () => {
    const storedSession = storage.getAuthSession();

    if (storedSession) {
      set({
        user: storedSession.user,
        accessToken: storedSession.accessToken,
        refreshToken: storedSession.refreshToken || null,
        status: 'authenticated',
        error: null,
        mfaRequired: false,
        mfaToken: null,
      });
      return;
    }

    // MVP convenience: keep the app accessible during frontend development.
    // Remove this fallback when the real backend authentication is connected.
    storage.setAuthSession(demoSession);

    set({
      user: demoSession.user,
      accessToken: demoSession.accessToken,
      refreshToken: demoSession.refreshToken || null,
      status: 'authenticated',
      error: null,
      mfaRequired: false,
      mfaToken: null,
    });
  },

  setSession: (session) => {
    storage.setAuthSession(session);

    set({
      user: session.user,
      accessToken: session.accessToken,
      refreshToken: session.refreshToken || null,
      status: 'authenticated',
      error: null,
      mfaRequired: false,
      mfaToken: null,
    });
  },

  setMfaRequired: (mfaToken) => {
    set({
      status: 'unauthenticated',
      error: null,
      mfaRequired: true,
      mfaToken,
    });
  },

  setLoading: () => {
    set({ status: 'loading', error: null });
  },

  setError: (message) => {
    set({ status: 'error', error: message });
  },

  clearError: () => {
    set({ error: null });
  },

  logout: () => {
    storage.clearAuthSession();

    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      status: 'unauthenticated',
      error: null,
      mfaRequired: false,
      mfaToken: null,
    });
  },
}));
```

---

# 6. Update Auth Hook

## `src/hooks/useAuth.ts`

Replace the file content with this:

```ts
import { useMemo } from 'react';

import { useAuthStore } from '@/store/auth.store';

export function useAuth() {
  const user = useAuthStore((state) => state.user);
  const status = useAuthStore((state) => state.status);
  const error = useAuthStore((state) => state.error);
  const mfaRequired = useAuthStore((state) => state.mfaRequired);
  const mfaToken = useAuthStore((state) => state.mfaToken);
  const hydrate = useAuthStore((state) => state.hydrate);
  const logout = useAuthStore((state) => state.logout);
  const clearError = useAuthStore((state) => state.clearError);

  const isAuthenticated = Boolean(user) && status === 'authenticated';

  return useMemo(
    () => ({
      user,
      role: user?.role,
      status,
      error,
      mfaRequired,
      mfaToken,
      isAuthenticated,
      hydrate,
      logout,
      clearError,
    }),
    [
      user,
      status,
      error,
      mfaRequired,
      mfaToken,
      isAuthenticated,
      hydrate,
      logout,
      clearError,
    ]
  );
}
```

---

# 7. Update Auth Service

## `src/services/auth.service.ts`

Replace the file content with this:

```ts
import { USER_ROLES } from '@/config/permissions';
import { API_ENDPOINTS } from '@/lib/api';
import { apiGet, apiPost } from '@/lib/http';
import { storage } from '@/lib/storage';
import type {
  ForgotPasswordPayload,
  LoginPayload,
  LoginResponse,
  ResetPasswordPayload,
} from '@/types/auth.types';
import type { ApiResponse } from '@/types/common.types';
import type { User } from '@/types/user.types';

function createDemoUser(payload: LoginPayload): User {
  return {
    id: `user_${payload.role.toLowerCase()}`,
    fullName: payload.email.includes('auditor') ? 'Audit User' : 'Admin User',
    email: payload.email,
    role: payload.role,
    title:
      payload.role === USER_ROLES.AUDITOR
        ? 'Government Auditor'
        : payload.role === USER_ROLES.CONTRACTOR
          ? 'Contractor'
          : payload.role === USER_ROLES.ME_OFFICER
            ? 'Monitoring and Evaluation Officer'
            : payload.role === USER_ROLES.APPROVAL_AUTHORITY
              ? 'Approval Authority'
              : 'Government Administrator',
    status: 'ACTIVE',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
}

async function demoLogin(payload: LoginPayload): Promise<LoginResponse> {
  await new Promise((resolve) => window.setTimeout(resolve, 500));

  if (!payload.email || !payload.password) {
    throw new Error('Email and password are required.');
  }

  if (payload.password.toLowerCase() === 'wrong') {
    throw new Error('Invalid login credentials. Please check your details and try again.');
  }

  return {
    user: createDemoUser(payload),
    accessToken: 'demo-access-token',
    refreshToken: 'demo-refresh-token',
    expiresAt: new Date(Date.now() + 1000 * 60 * 60).toISOString(),
    mfaRequired: false,
  };
}

async function demoForgotPassword(payload: ForgotPasswordPayload): Promise<ApiResponse<null>> {
  await new Promise((resolve) => window.setTimeout(resolve, 500));

  if (!payload.email) {
    throw new Error('Email address is required.');
  }

  return {
    success: true,
    message: 'If the email exists, password reset instructions will be sent.',
    data: null,
  };
}

const useMockApi = import.meta.env.VITE_USE_MOCK_API === 'true';

export const authService = {
  async login(payload: LoginPayload): Promise<LoginResponse> {
    if (useMockApi) {
      const response = await demoLogin(payload);

      if (!response.mfaRequired) {
        storage.setAuthSession(response);
      }

      return response;
    }

    const response = await apiPost<ApiResponse<LoginResponse>, LoginPayload>(
      API_ENDPOINTS.auth.login,
      payload
    );

    if (!response.data.mfaRequired) {
      storage.setAuthSession(response.data);
    }

    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiGet<ApiResponse<User>>(API_ENDPOINTS.auth.me);
    return response.data;
  },

  async forgotPassword(payload: ForgotPasswordPayload): Promise<ApiResponse<null>> {
    if (useMockApi) {
      return demoForgotPassword(payload);
    }

    return apiPost<ApiResponse<null>, ForgotPasswordPayload>(
      API_ENDPOINTS.auth.forgotPassword,
      payload
    );
  },

  async resetPassword(payload: ResetPasswordPayload): Promise<ApiResponse<null>> {
    return apiPost<ApiResponse<null>, ResetPasswordPayload>(
      API_ENDPOINTS.auth.resetPassword,
      payload
    );
  },

  async logout(): Promise<void> {
    try {
      if (!useMockApi) {
        await apiPost<ApiResponse<null>>(API_ENDPOINTS.auth.logout);
      }
    } finally {
      storage.clearAuthSession();
    }
  },
};
```

---

# 8. Populate Auth Feature Hooks

## `src/features/auth/hooks/useLogin.ts`

```ts
import { useMutation } from '@tanstack/react-query';
import { useNavigate, useLocation } from 'react-router-dom';

import { PRIVATE_ROUTES } from '@/config/routes';
import { authService } from '@/services/auth.service';
import { useAuthStore } from '@/store/auth.store';
import type { LoginPayload } from '@/types/auth.types';

type LocationState = {
  from?: string;
};

function getSafeRedirectPath(path?: string): string {
  if (!path) return PRIVATE_ROUTES.DASHBOARD;
  if (!path.startsWith('/')) return PRIVATE_ROUTES.DASHBOARD;
  if (path === '/login' || path === '/forgot-password') return PRIVATE_ROUTES.DASHBOARD;
  return path;
}

export function useLogin() {
  const navigate = useNavigate();
  const location = useLocation();
  const setSession = useAuthStore((state) => state.setSession);
  const setMfaRequired = useAuthStore((state) => state.setMfaRequired);
  const setLoading = useAuthStore((state) => state.setLoading);
  const setError = useAuthStore((state) => state.setError);
  const clearError = useAuthStore((state) => state.clearError);

  const state = location.state as LocationState | null;

  return useMutation({
    mutationFn: async (payload: LoginPayload) => {
      setLoading();
      clearError();
      return authService.login(payload);
    },
    onSuccess: (response) => {
      if (response.mfaRequired && response.mfaToken) {
        setMfaRequired(response.mfaToken);
        return;
      }

      setSession(response);
      navigate(getSafeRedirectPath(state?.from), { replace: true });
    },
    onError: (error) => {
      const message =
        error instanceof Error
          ? error.message
          : 'Login failed. Please check your credentials and try again.';

      setError(message);
    },
  });
}
```

---

## `src/features/auth/hooks/useLogout.ts`

```ts
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

import { PUBLIC_ROUTES } from '@/config/routes';
import { authService } from '@/services/auth.service';
import { useAuthStore } from '@/store/auth.store';

export function useLogout() {
  const navigate = useNavigate();
  const logoutStore = useAuthStore((state) => state.logout);

  return useMutation({
    mutationFn: authService.logout,
    onSettled: () => {
      logoutStore();
      navigate(PUBLIC_ROUTES.LOGIN, { replace: true });
    },
  });
}
```

---

# 9. Populate Auth Components

## `src/features/auth/components/RoleSelect.tsx`

```tsx
import { Select } from '@/components/ui/Select';
import { USER_ROLES, type UserRole } from '@/config/permissions';

const roleOptions: { label: string; value: UserRole }[] = [
  { label: 'Government Admin', value: USER_ROLES.GOVERNMENT_ADMIN },
  { label: 'Contractor', value: USER_ROLES.CONTRACTOR },
  { label: 'M&E Officer', value: USER_ROLES.ME_OFFICER },
  { label: 'Approval Authority', value: USER_ROLES.APPROVAL_AUTHORITY },
  { label: 'Auditor', value: USER_ROLES.AUDITOR },
  { label: 'District Officer', value: USER_ROLES.DISTRICT_OFFICER },
  { label: 'Ministry Officer', value: USER_ROLES.MINISTRY_OFFICER },
  { label: 'Super Admin', value: USER_ROLES.SUPER_ADMIN },
];

type RoleSelectProps = {
  value: UserRole;
  onChange: (value: UserRole) => void;
  hasError?: boolean;
};

export function RoleSelect({ value, onChange, hasError }: RoleSelectProps) {
  return (
    <Select
      value={value}
      hasError={hasError}
      onChange={(event) => onChange(event.target.value as UserRole)}
    >
      {roleOptions.map((role) => (
        <option key={role.value} value={role.value}>
          {role.label}
        </option>
      ))}
    </Select>
  );
}
```

---

## `src/features/auth/components/LoginForm.tsx`

```tsx
import { zodResolver } from '@hookform/resolvers/zod';
import { Eye, EyeOff, Lock, Mail } from 'lucide-react';
import { useState } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';

import { AlertBox } from '@/components/feedback/AlertBox';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { PUBLIC_ROUTES } from '@/config/routes';
import { USER_ROLES } from '@/config/permissions';
import { FormField } from '@/components/forms/FormField';
import { useAuth } from '@/hooks/useAuth';
import { loginSchema, type LoginFormValues } from '../schemas/auth.schema';
import { useLogin } from '../hooks/useLogin';
import { RoleSelect } from './RoleSelect';

export function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);
  const { error, mfaRequired } = useAuth();
  const loginMutation = useLogin();

  const {
    control,
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: 'admin@eb-gms.local',
      password: 'demo',
      role: USER_ROLES.GOVERNMENT_ADMIN,
    },
  });

  function onSubmit(values: LoginFormValues) {
    loginMutation.mutate(values);
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      {error && <AlertBox type="error" title="Login failed">{error}</AlertBox>}

      {mfaRequired && (
        <AlertBox type="info" title="MFA Required">
          Multi-factor authentication is prepared for a future implementation.
        </AlertBox>
      )}

      <FormField label="Email Address" htmlFor="email" error={errors.email?.message} required>
        <div className="relative">
          <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <Input
            id="email"
            type="email"
            placeholder="admin@eb-gms.local"
            className="pl-10"
            hasError={Boolean(errors.email)}
            {...register('email')}
          />
        </div>
      </FormField>

      <FormField label="Password" htmlFor="password" error={errors.password?.message} required>
        <div className="relative">
          <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <Input
            id="password"
            type={showPassword ? 'text' : 'password'}
            placeholder="Enter password"
            className="pl-10 pr-10"
            hasError={Boolean(errors.password)}
            {...register('password')}
          />
          <button
            type="button"
            onClick={() => setShowPassword((current) => !current)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
      </FormField>

      <FormField label="Login Role" error={errors.role?.message} required>
        <Controller
          control={control}
          name="role"
          render={({ field }) => (
            <RoleSelect
              value={field.value}
              onChange={field.onChange}
              hasError={Boolean(errors.role)}
            />
          )}
        />
      </FormField>

      <Button type="submit" size="lg" className="w-full" isLoading={loginMutation.isPending}>
        Secure Login
      </Button>

      <div className="flex items-center justify-between text-sm">
        <span className="text-slate-300">Authorized users only</span>
        <Link to={PUBLIC_ROUTES.FORGOT_PASSWORD} className="font-semibold text-[#F58420] hover:underline">
          Forgot password?
        </Link>
      </div>

      <div className="rounded-xl border border-white/10 bg-white/5 p-3 text-xs leading-5 text-slate-300">
        MVP demo tip: use any valid email and password <strong>demo</strong>. Use password{' '}
        <strong>wrong</strong> to test safe error handling.
      </div>
    </form>
  );
}
```

---

## `src/features/auth/components/ForgotPasswordForm.tsx`

```tsx
import { zodResolver } from '@hookform/resolvers/zod';
import { Mail } from 'lucide-react';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';

import { AlertBox } from '@/components/feedback/AlertBox';
import { FormField } from '@/components/forms/FormField';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { PUBLIC_ROUTES } from '@/config/routes';
import { authService } from '@/services/auth.service';
import { forgotPasswordSchema, type ForgotPasswordFormValues } from '../schemas/auth.schema';

export function ForgotPasswordForm() {
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordFormValues>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: {
      email: '',
    },
  });

  async function onSubmit(values: ForgotPasswordFormValues) {
    setIsSubmitting(true);
    setSuccessMessage(null);
    setErrorMessage(null);

    try {
      const response = await authService.forgotPassword(values);
      setSuccessMessage(response.message);
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : 'Unable to process password reset request. Please try again.';
      setErrorMessage(message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      {successMessage && <AlertBox type="success" title="Request received">{successMessage}</AlertBox>}
      {errorMessage && <AlertBox type="error" title="Request failed">{errorMessage}</AlertBox>}

      <FormField label="Email Address" htmlFor="email" error={errors.email?.message} required>
        <div className="relative">
          <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <Input
            id="email"
            type="email"
            placeholder="your.email@gov.example"
            className="pl-10"
            hasError={Boolean(errors.email)}
            {...register('email')}
          />
        </div>
      </FormField>

      <Button type="submit" size="lg" className="w-full" isLoading={isSubmitting}>
        Send Reset Instructions
      </Button>

      <div className="text-center text-sm">
        <Link to={PUBLIC_ROUTES.LOGIN} className="font-semibold text-[#F58420] hover:underline">
          Back to login
        </Link>
      </div>
    </form>
  );
}
```

---

# 10. Populate Auth Pages

## `src/features/auth/pages/LoginPage.tsx`

```tsx
import { LoginForm } from '../components/LoginForm';

export function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#051931] px-6 py-10">
      <section className="w-full max-w-md rounded-3xl border border-white/10 bg-white/10 p-8 shadow-2xl backdrop-blur">
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-[#F58420] text-xl font-black text-white">
          EB
        </div>

        <div className="mb-8 text-center">
          <p className="text-xs font-bold uppercase tracking-[0.25em] text-[#009659]">
            Secure Access
          </p>
          <h1 className="mt-3 text-2xl font-bold text-white">
            EB Government Monitoring System
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            Sign in to monitor projects, evidence, approvals, funds, audits, and reports.
          </p>
        </div>

        <LoginForm />
      </section>
    </main>
  );
}
```

---

## `src/features/auth/pages/ForgotPasswordPage.tsx`

```tsx
import { ForgotPasswordForm } from '../components/ForgotPasswordForm';

export function ForgotPasswordPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#051931] px-6 py-10">
      <section className="w-full max-w-md rounded-3xl border border-white/10 bg-white/10 p-8 shadow-2xl backdrop-blur">
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-[#F58420] text-xl font-black text-white">
          EB
        </div>

        <div className="mb-8 text-center">
          <p className="text-xs font-bold uppercase tracking-[0.25em] text-[#009659]">
            Account Recovery
          </p>
          <h1 className="mt-3 text-2xl font-bold text-white">Forgot Password</h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            Enter your email address to receive password reset instructions.
          </p>
        </div>

        <ForgotPasswordForm />
      </section>
    </main>
  );
}
```

---

# 11. Update App Providers

## `src/app/providers.tsx`

Replace the file content with this:

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useEffect, type ReactNode } from 'react';

import { useAuthStore } from '@/store/auth.store';

type AppProvidersProps = {
  children: ReactNode;
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 1000 * 60,
    },
    mutations: {
      retry: 0,
    },
  },
});

function AuthBootstrapper({ children }: AppProvidersProps) {
  const hydrate = useAuthStore((state) => state.hydrate);

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return children;
}

export function AppProviders({ children }: AppProvidersProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthBootstrapper>{children}</AuthBootstrapper>
    </QueryClientProvider>
  );
}
```

---

# 12. Update Topbar Logout

## `src/components/layout/Topbar.tsx`

Replace the file content with this:

```tsx
import { Bell, LogOut, Menu, Search } from 'lucide-react';
import { useLocation } from 'react-router-dom';

import { Avatar } from '@/components/ui/Avatar';
import { Button } from '@/components/ui/Button';
import { getRouteLabel } from '@/config/routes';
import { useAuth } from '@/hooks/useAuth';
import { useLogout } from '@/features/auth/hooks/useLogout';

export function Topbar() {
  const location = useLocation();
  const { user } = useAuth();
  const logoutMutation = useLogout();
  const title = getRouteLabel(location.pathname);

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6 lg:ml-[17rem]">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="sm" className="lg:hidden">
          <Menu className="h-5 w-5" />
        </Button>

        <div>
          <h1 className="text-base font-bold text-slate-950">{title}</h1>
          <p className="text-xs text-slate-500">
            Government Project Accountability Platform
          </p>
        </div>
      </div>

      <div className="hidden w-full max-w-md items-center rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 md:flex">
        <Search className="mr-2 h-4 w-4 text-slate-400" />
        <input
          type="search"
          placeholder="Search projects, contractors, reports..."
          className="w-full bg-transparent text-sm outline-none placeholder:text-slate-400"
        />
      </div>

      <div className="flex items-center gap-3">
        <button
          type="button"
          className="relative rounded-full p-2 text-slate-600 hover:bg-slate-100"
          aria-label="Notifications"
        >
          <Bell className="h-5 w-5" />
          <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-500" />
        </button>

        <div className="hidden text-right md:block">
          <p className="text-sm font-bold text-slate-900">{user?.fullName}</p>
          <p className="text-xs text-slate-500">{user?.title}</p>
        </div>

        <Avatar name={user?.fullName || 'User'} />

        <Button
          variant="ghost"
          size="sm"
          onClick={() => logoutMutation.mutate()}
          isLoading={logoutMutation.isPending}
          aria-label="Logout"
        >
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
}
```

---

# 13. Update Sidebar Width if Needed

## `src/components/layout/Sidebar.tsx`

In your existing sidebar file, replace:

```txt
w-68
```

With:

```txt
w-[17rem]
```

So the opening `<aside>` should look like:

```tsx
<aside className="fixed inset-y-0 left-0 hidden w-[17rem] flex-col bg-[#051931] text-white lg:flex">
```

---

# 14. Update App Layout Width if Needed

## `src/components/layout/AppLayout.tsx`

Replace:

```txt
lg:ml-68
```

With:

```txt
lg:ml-[17rem]
```

Final file:

```tsx
import { Outlet } from 'react-router-dom';

import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';

export function AppLayout() {
  return (
    <div className="min-h-screen bg-[#F4F7FB]">
      <Sidebar />
      <Topbar />

      <div className="lg:ml-[17rem]">
        <Outlet />
      </div>
    </div>
  );
}
```

---

# 15. Update Router to Use Real Auth Pages

## `src/app/router.tsx`

Replace the file content with this:

```tsx
import { createBrowserRouter, Navigate } from 'react-router-dom';

import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { AppLayout } from '@/components/layout/AppLayout';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { ProtectedRoute } from '@/components/layout/ProtectedRoute';
import { RoleGuard } from '@/components/layout/RoleGuard';
import { PRIVATE_ROUTES, PUBLIC_ROUTES } from '@/config/routes';
import { PERMISSIONS, USER_ROLES } from '@/config/permissions';
import { ForgotPasswordPage } from '@/features/auth/pages/ForgotPasswordPage';
import { LoginPage } from '@/features/auth/pages/LoginPage';

function PlaceholderPage({
  title,
  description,
  badge = 'MVP Route',
}: {
  title: string;
  description: string;
  badge?: string;
}) {
  return (
    <PageContainer>
      <PageHeader
        title={title}
        description={description}
        actions={<Badge variant="success">{badge}</Badge>}
      />

      <Card>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>
            This screen is connected to the routing skeleton.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center">
            <p className="text-sm font-semibold text-slate-700">
              Full business UI for this module will be implemented in its dedicated feature phase.
            </p>
          </div>
        </CardContent>
      </Card>
    </PageContainer>
  );
}

function DashboardPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Dashboard"
        description="Role-aware overview for government project monitoring."
        actions={
          <>
            <Button variant="outline">Export Summary</Button>
            <Button>New Project</Button>
          </>
        }
      />

      <div className="grid gap-6 lg:grid-cols-4">
        {[
          ['Total Projects', '256'],
          ['Active Monitoring', '158'],
          ['Pending Reviews', '42'],
          ['Delayed Projects', '18'],
        ].map(([label, value]) => (
          <Card key={label}>
            <CardHeader>
              <CardDescription>{label}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-4xl font-black text-slate-950">{value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Authentication Module Ready</CardTitle>
          <CardDescription>
            Login, forgot password, auth store, protected routes, and logout flow are active.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p>
            Use the logout button in the topbar to test authentication redirects.
          </p>
        </CardContent>
      </Card>
    </PageContainer>
  );
}

function NotFoundPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#F4F7FB] px-6">
      <Card className="max-w-lg text-center">
        <CardHeader>
          <CardTitle>Page Not Found</CardTitle>
          <CardDescription>The requested route does not exist.</CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={() => window.location.assign(PRIVATE_ROUTES.DASHBOARD)}>
            Go to Dashboard
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to={PRIVATE_ROUTES.DASHBOARD} replace />,
  },
  {
    path: PUBLIC_ROUTES.LOGIN,
    element: <LoginPage />,
  },
  {
    path: PUBLIC_ROUTES.FORGOT_PASSWORD,
    element: <ForgotPasswordPage />,
  },
  {
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: PRIVATE_ROUTES.DASHBOARD,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_DASHBOARD}>
            <DashboardPage />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROJECTS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_PROJECTS}>
            <PlaceholderPage title="Projects" description="View and manage government projects." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROJECT_NEW,
        element: (
          <RoleGuard permission={PERMISSIONS.CREATE_PROJECT}>
            <PlaceholderPage title="Create Project" description="Create a new government monitoring project." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROJECT_DETAILS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_PROJECT_DETAILS}>
            <PlaceholderPage title="Project Details" description="View project milestones, funds, evidence, and audit status." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROJECT_EDIT,
        element: (
          <RoleGuard permission={PERMISSIONS.EDIT_PROJECT}>
            <PlaceholderPage title="Edit Project" description="Update government project details." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.CONTRACTORS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_CONTRACTORS}>
            <PlaceholderPage title="Contractors" description="Manage contractors and compliance profiles." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.CONTRACTOR_DETAILS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_CONTRACTORS}>
            <PlaceholderPage title="Contractor Details" description="View contractor profile, projects, and performance history." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.EVIDENCE,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_EVIDENCE}>
            <PlaceholderPage title="Evidence & Receipts" description="Track submitted receipts, invoices, and evidence." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.EVIDENCE_DETAILS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_EVIDENCE}>
            <PlaceholderPage title="Evidence Details" description="Review evidence package and verification history." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.MONITORING_REVIEW_QUEUE,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_MONITORING}>
            <PlaceholderPage title="M&E Review Queue" description="Review contractor submissions and monitoring tasks." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.MONITORING_FIELD_INSPECTIONS,
        element: (
          <RoleGuard permission={PERMISSIONS.CREATE_FIELD_INSPECTION}>
            <PlaceholderPage title="Field Inspections" description="Capture and review field inspection reports." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.APPROVALS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_APPROVALS}>
            <PlaceholderPage title="Approvals" description="Review pending milestone and fund release approvals." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.APPROVAL_DETAILS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_APPROVALS}>
            <PlaceholderPage title="Approval Details" description="Review approval request details and supporting evidence." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.FUNDS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_FUNDS}>
            <PlaceholderPage title="Funds" description="Track budget allocation, release, utilization, and balances." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.AUDITS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_AUDITS}>
            <PlaceholderPage title="Audits" description="Audit projects, evidence, payments, and compliance status." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.REPORTS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_REPORTS}>
            <PlaceholderPage title="Reports" description="Generate project, funds, audit, district, and ministry reports." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.NOTIFICATIONS,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_NOTIFICATIONS}>
            <PlaceholderPage title="Notifications" description="View alerts, reminders, review tasks, and approval updates." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.USERS,
        element: (
          <RoleGuard
            permission={PERMISSIONS.VIEW_USERS}
            allowedRoles={[USER_ROLES.SUPER_ADMIN, USER_ROLES.GOVERNMENT_ADMIN]}
          >
            <PlaceholderPage title="User Management" description="Manage users, roles, and access permissions." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.SETTINGS,
        element: (
          <RoleGuard
            permission={PERMISSIONS.VIEW_SETTINGS}
            allowedRoles={[USER_ROLES.SUPER_ADMIN, USER_ROLES.GOVERNMENT_ADMIN]}
          >
            <PlaceholderPage title="Settings" description="Configure ministries, districts, categories, and workflow rules." />
          </RoleGuard>
        ),
      },
      {
        path: PRIVATE_ROUTES.PROFILE,
        element: (
          <RoleGuard permission={PERMISSIONS.VIEW_PROFILE}>
            <PlaceholderPage title="Profile" description="View and update current user profile." />
          </RoleGuard>
        ),
      },
    ],
  },
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);
```

---

# 16. Required Package Check

Phase 5 uses:

```txt
@hookform/resolvers
```

If it is not installed, run:

```bash
npm install @hookform/resolvers
```

You already installed these earlier, but if any are missing, install them:

```bash
npm install react-hook-form zod zustand @tanstack/react-query
```

---

# 17. Build Test

Run:

```bash
npm run build
```

Expected result:

```txt
✓ built
```

---

# 18. Browser Test

Run:

```bash
npm run dev
```

Open:

```txt
http://localhost:5173/login
```

Test these actions:

1. Login with default values.
2. Confirm redirect to `/dashboard`.
3. Click logout button in topbar.
4. Confirm redirect to `/login`.
5. Try password `wrong`.
6. Confirm safe error message appears.
7. Open `/forgot-password`.
8. Submit a valid email.
9. Confirm success message appears.

---

# 19. Phase 5 Completion Checklist

Phase 5 is complete when:

- `src/features/auth/pages/LoginPage.tsx` exists.
- `src/features/auth/pages/ForgotPasswordPage.tsx` exists.
- `LoginForm` validates email, password, and role.
- `ForgotPasswordForm` validates email.
- `RoleSelect` supports MVP roles.
- `useLogin` redirects authenticated users to dashboard or intended route.
- `useLogout` clears auth state and redirects to login.
- `auth.store.ts` stores shared authentication state.
- `ProtectedRoute` still works.
- Topbar logout works.
- Invalid login attempts show safe errors.
- `npm run build` passes.

---

# Phase 5 Expected Output

After completing this phase:

- Users can log in.
- Authenticated users are redirected to the dashboard.
- Invalid login attempts are handled with safe messages.
- Logout works correctly.
- Forgot password screen is available.
- Authentication state is centralized and ready for real backend integration.
- MFA support is prepared through `mfaRequired` and `mfaToken` fields.

---

# Next Phase

After Phase 5 passes build and browser testing, proceed to:

```txt
Phase 6: Dashboard Module
```
