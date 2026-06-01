# Phase 4 — API Client, Services and Data Types

**Project:** EB Government Monitoring System  
**Frontend:** React + TypeScript + Vite + Tailwind CSS v4  
**Phase Goal:** Create one clean API communication layer, centralize HTTP requests, token storage, logging, validation helpers, formatting utilities, domain types, and service modules.

---

## Phase 3 Confirmation

Phase 3 is complete.

Your build passed successfully:

```txt
✓ 1815 modules transformed.
✓ built in 1.68s
```

Your screenshot also shows the protected dashboard shell working with:

- Sidebar navigation
- Topbar search area
- Dashboard route at `/dashboard`
- Role-aware route skeleton
- Protected app layout

You can now proceed to Phase 4.

---

# Phase 4 Objectives

This phase implements:

- A standard HTTP client used by all feature modules.
- Centralized token handling and request headers.
- Safe API error formatting.
- Reusable storage and logger utilities.
- TypeScript entity types for all core modules.
- Service files that keep API calls out of React components.
- Utility functions for dates, currency, statuses, and files.

---

# 1. Create Phase 4 Directories

Run this command from the project root:

```bash
mkdir -p src/lib src/services src/types src/utils
```

---

# 2. Create Phase 4 Files

Run this command from the project root:

```bash
touch src/lib/http.ts src/lib/api.ts src/lib/storage.ts src/lib/logger.ts src/lib/validators.ts src/utils/date.ts src/utils/currency.ts src/utils/status.ts src/utils/file.ts src/types/auth.types.ts src/types/user.types.ts src/types/project.types.ts src/types/contractor.types.ts src/types/evidence.types.ts src/types/monitoring.types.ts src/types/approval.types.ts src/types/funds.types.ts src/types/audit.types.ts src/types/report.types.ts src/types/notification.types.ts src/types/common.types.ts src/services/auth.service.ts src/services/projects.service.ts src/services/contractors.service.ts src/services/evidence.service.ts src/services/monitoring.service.ts src/services/approvals.service.ts src/services/funds.service.ts src/services/audits.service.ts src/services/reports.service.ts src/services/notifications.service.ts src/services/users.service.ts src/services/settings.service.ts
```

---

# 3. Populate Core Type Files

---

## `src/types/common.types.ts`

```ts
export type ID = string;

export type ApiStatus = 'idle' | 'loading' | 'success' | 'error';

export type SortDirection = 'asc' | 'desc';

export type ApiResponse<T> = {
  success: boolean;
  message: string;
  data: T;
};

export type ApiErrorResponse = {
  success: false;
  message: string;
  errors?: Record<string, string[]>;
  statusCode?: number;
};

export type PaginatedResponse<T> = {
  items: T[];
  meta: PaginationMeta;
};

export type PaginationMeta = {
  page: number;
  perPage: number;
  totalItems: number;
  totalPages: number;
};

export type PaginationParams = {
  page?: number;
  perPage?: number;
};

export type SearchParams = {
  search?: string;
};

export type DateRangeParams = {
  startDate?: string;
  endDate?: string;
};

export type ListQueryParams = PaginationParams &
  SearchParams &
  DateRangeParams & {
    status?: string;
    district?: string;
    ministry?: string;
    sortBy?: string;
    sortDirection?: SortDirection;
  };

export type SelectOption<TValue extends string = string> = {
  label: string;
  value: TValue;
};

export type AuditMetadata = {
  createdAt: string;
  updatedAt: string;
  createdBy?: ID;
  updatedBy?: ID;
};
```

---

## `src/types/user.types.ts`

```ts
import type { ID, AuditMetadata } from './common.types';
import type { UserRole } from '@/config/permissions';

export type UserStatus = 'ACTIVE' | 'INACTIVE' | 'SUSPENDED' | 'PENDING_SETUP';

export type User = AuditMetadata & {
  id: ID;
  fullName: string;
  email: string;
  phoneNumber?: string;
  role: UserRole;
  title?: string;
  ministryId?: ID;
  districtId?: ID;
  status: UserStatus;
  lastLoginAt?: string;
};

export type CreateUserPayload = {
  fullName: string;
  email: string;
  phoneNumber?: string;
  role: UserRole;
  title?: string;
  ministryId?: ID;
  districtId?: ID;
};

export type UpdateUserPayload = Partial<CreateUserPayload> & {
  status?: UserStatus;
};
```

---

## `src/types/auth.types.ts`

```ts
import type { User } from './user.types';
import type { UserRole } from '@/config/permissions';

export type LoginPayload = {
  email: string;
  password: string;
  role?: UserRole;
};

export type LoginResponse = {
  user: User;
  accessToken: string;
  refreshToken?: string;
  expiresAt?: string;
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
};
```

---

## `src/types/project.types.ts`

```ts
import type { ID, AuditMetadata } from './common.types';

export type ProjectStatus =
  | 'DRAFT'
  | 'NOT_STARTED'
  | 'IN_PROGRESS'
  | 'UNDER_REVIEW'
  | 'DELAYED'
  | 'COMPLETED'
  | 'SUSPENDED'
  | 'CANCELLED';

export type ProjectCategory =
  | 'ROADS'
  | 'SCHOOLS'
  | 'HEALTH'
  | 'WATER'
  | 'ENERGY'
  | 'AGRICULTURE'
  | 'ICT'
  | 'HOUSING'
  | 'OTHER';

export type ProjectRiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export type ProjectMilestone = AuditMetadata & {
  id: ID;
  projectId: ID;
  title: string;
  description?: string;
  plannedStartDate: string;
  plannedEndDate: string;
  actualCompletionDate?: string;
  budgetAmount: number;
  progressPercentage: number;
  status: ProjectStatus;
};

export type Project = AuditMetadata & {
  id: ID;
  projectCode: string;
  title: string;
  description: string;
  category: ProjectCategory;
  ministryId: ID;
  districtId: ID;
  contractorId?: ID;
  monitoringOfficerId?: ID;
  approvalAuthorityId?: ID;
  auditorId?: ID;
  budgetAmount: number;
  fundsReleased: number;
  fundsUtilized: number;
  startDate: string;
  endDate: string;
  status: ProjectStatus;
  riskLevel: ProjectRiskLevel;
  progressPercentage: number;
  latitude?: number;
  longitude?: number;
  milestones?: ProjectMilestone[];
};

export type CreateProjectPayload = {
  title: string;
  description: string;
  category: ProjectCategory;
  ministryId: ID;
  districtId: ID;
  contractorId?: ID;
  monitoringOfficerId?: ID;
  approvalAuthorityId?: ID;
  auditorId?: ID;
  budgetAmount: number;
  startDate: string;
  endDate: string;
  latitude?: number;
  longitude?: number;
};

export type UpdateProjectPayload = Partial<CreateProjectPayload> & {
  status?: ProjectStatus;
  progressPercentage?: number;
  riskLevel?: ProjectRiskLevel;
};
```

---

## `src/types/contractor.types.ts`

```ts
import type { ID, AuditMetadata } from './common.types';

export type ContractorStatus = 'ACTIVE' | 'SUSPENDED' | 'BLACKLISTED' | 'PENDING_VERIFICATION';

export type Contractor = AuditMetadata & {
  id: ID;
  companyName: string;
  registrationNumber: string;
  taxIdentificationNumber?: string;
  licenseNumber?: string;
  contactPersonName: string;
  contactEmail: string;
  contactPhone: string;
  address?: string;
  status: ContractorStatus;
  complianceScore?: number;
  activeProjectsCount?: number;
  completedProjectsCount?: number;
};

export type CreateContractorPayload = {
  companyName: string;
  registrationNumber: string;
  taxIdentificationNumber?: string;
  licenseNumber?: string;
  contactPersonName: string;
  contactEmail: string;
  contactPhone: string;
  address?: string;
};

export type UpdateContractorPayload = Partial<CreateContractorPayload> & {
  status?: ContractorStatus;
};
```

---

## `src/types/evidence.types.ts`

```ts
import type { ID, AuditMetadata } from './common.types';

export type EvidenceType =
  | 'RECEIPT'
  | 'INVOICE'
  | 'PHOTO'
  | 'VIDEO'
  | 'DELIVERY_NOTE'
  | 'PAYMENT_VOUCHER'
  | 'INSPECTION_REPORT'
  | 'OTHER_DOCUMENT';

export type EvidenceStatus =
  | 'PENDING_REVIEW'
  | 'APPROVED'
  | 'REJECTED'
  | 'NEEDS_CLARIFICATION';

export type Evidence = AuditMetadata & {
  id: ID;
  projectId: ID;
  milestoneId?: ID;
  uploadedBy: ID;
  type: EvidenceType;
  title: string;
  description?: string;
  fileName: string;
  fileUrl: string;
  fileSize: number;
  mimeType: string;
  status: EvidenceStatus;
  reviewedBy?: ID;
  reviewedAt?: string;
  reviewComment?: string;
  gpsLatitude?: number;
  gpsLongitude?: number;
};

export type UploadEvidencePayload = {
  projectId: ID;
  milestoneId?: ID;
  type: EvidenceType;
  title: string;
  description?: string;
  files: File[];
  gpsLatitude?: number;
  gpsLongitude?: number;
};

export type VerifyEvidencePayload = {
  status: Extract<EvidenceStatus, 'APPROVED' | 'REJECTED' | 'NEEDS_CLARIFICATION'>;
  reviewComment?: string;
};
```

---

## `src/types/monitoring.types.ts`

```ts
import type { ID, AuditMetadata } from './common.types';

export type MonitoringReviewStatus = 'PENDING' | 'APPROVED' | 'REJECTED' | 'NEEDS_CLARIFICATION';
export type InspectionStatus = 'SCHEDULED' | 'COMPLETED' | 'CANCELLED';

export type MonitoringReview = AuditMetadata & {
  id: ID;
  projectId: ID;
  milestoneId?: ID;
  evidenceId?: ID;
  officerId: ID;
  status: MonitoringReviewStatus;
  progressVerified: number;
  findings?: string;
  recommendation?: string;
  riskFlag?: boolean;
};

export type FieldInspection = AuditMetadata & {
  id: ID;
  projectId: ID;
  officerId: ID;
  scheduledDate: string;
  completedAt?: string;
  status: InspectionStatus;
  checklistSummary?: string;
  findings?: string;
  gpsLatitude?: number;
  gpsLongitude?: number;
};

export type SubmitMonitoringReviewPayload = {
  projectId: ID;
  milestoneId?: ID;
  evidenceId?: ID;
  status: MonitoringReviewStatus;
  progressVerified: number;
  findings?: string;
  recommendation?: string;
  riskFlag?: boolean;
};

export type CreateFieldInspectionPayload = {
  projectId: ID;
  scheduledDate: string;
  checklistSummary?: string;
  findings?: string;
  gpsLatitude?: number;
  gpsLongitude?: number;
};
```

---

## `src/types/approval.types.ts`

```ts
import type { ID, AuditMetadata } from './common.types';

export type ApprovalStatus = 'PENDING' | 'APPROVED' | 'REJECTED';
export type ApprovalType = 'MILESTONE_APPROVAL' | 'FUND_RELEASE' | 'PROJECT_COMPLETION';

export type ApprovalRequest = AuditMetadata & {
  id: ID;
  projectId: ID;
  milestoneId?: ID;
  type: ApprovalType;
  requestedBy: ID;
  assignedTo: ID;
  status: ApprovalStatus;
  amount?: number;
  reason?: string;
  decisionComment?: string;
  decidedAt?: string;
};

export type SubmitApprovalDecisionPayload = {
  status: Extract<ApprovalStatus, 'APPROVED' | 'REJECTED'>;
  decisionComment?: string;
};
```

---

## `src/types/funds.types.ts`

```ts
import type { ID, AuditMetadata } from './common.types';

export type PaymentStatus = 'PENDING' | 'PROCESSING' | 'RELEASED' | 'FAILED' | 'CANCELLED';

export type FundRelease = AuditMetadata & {
  id: ID;
  projectId: ID;
  milestoneId?: ID;
  approvalId?: ID;
  amount: number;
  status: PaymentStatus;
  releaseDate?: string;
  paymentReference?: string;
  notes?: string;
};

export type FundsSummary = {
  projectId: ID;
  budgetAmount: number;
  allocatedAmount: number;
  releasedAmount: number;
  utilizedAmount: number;
  balanceAmount: number;
  utilizationPercentage: number;
};

export type CreateFundReleasePayload = {
  projectId: ID;
  milestoneId?: ID;
  approvalId?: ID;
  amount: number;
  notes?: string;
};
```

---

## `src/types/audit.types.ts`

```ts
import type { ID, AuditMetadata } from './common.types';

export type AuditStatus = 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
export type FindingSeverity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type ComplianceStatus = 'COMPLIANT' | 'MINOR_ISSUE' | 'MAJOR_ISSUE' | 'NON_COMPLIANT';

export type AuditAssignment = AuditMetadata & {
  id: ID;
  projectId: ID;
  auditorId: ID;
  status: AuditStatus;
  dueDate?: string;
  completedAt?: string;
};

export type AuditFinding = AuditMetadata & {
  id: ID;
  auditAssignmentId: ID;
  projectId: ID;
  severity: FindingSeverity;
  title: string;
  description: string;
  recommendation?: string;
  complianceStatus: ComplianceStatus;
};

export type CreateAuditFindingPayload = {
  auditAssignmentId: ID;
  projectId: ID;
  severity: FindingSeverity;
  title: string;
  description: string;
  recommendation?: string;
  complianceStatus: ComplianceStatus;
};
```

---

## `src/types/report.types.ts`

```ts
import type { DateRangeParams, ID } from './common.types';

export type ReportType =
  | 'PROJECT_STATUS'
  | 'FUNDS_UTILIZATION'
  | 'CONTRACTOR_PERFORMANCE'
  | 'DISTRICT_PERFORMANCE'
  | 'MINISTRY_PERFORMANCE'
  | 'AUDIT_COMPLIANCE'
  | 'DELAYED_PROJECTS';

export type ReportFormat = 'PDF' | 'EXCEL' | 'CSV';

export type ReportFilters = DateRangeParams & {
  districtId?: ID;
  ministryId?: ID;
  contractorId?: ID;
  status?: string;
  type?: ReportType;
};

export type ReportSummary = {
  totalProjects: number;
  activeProjects: number;
  completedProjects: number;
  delayedProjects: number;
  totalBudget: number;
  totalFundsReleased: number;
  totalFundsUtilized: number;
};

export type ExportReportPayload = {
  type: ReportType;
  format: ReportFormat;
  filters?: ReportFilters;
};
```

---

## `src/types/notification.types.ts`

```ts
import type { ID, AuditMetadata } from './common.types';

export type NotificationType =
  | 'PROJECT_CREATED'
  | 'EVIDENCE_SUBMITTED'
  | 'EVIDENCE_REJECTED'
  | 'MILESTONE_APPROVED'
  | 'FUND_RELEASED'
  | 'AUDIT_ASSIGNED'
  | 'RISK_FLAGGED'
  | 'SYSTEM_ALERT';

export type Notification = AuditMetadata & {
  id: ID;
  userId: ID;
  type: NotificationType;
  title: string;
  message: string;
  readAt?: string;
  relatedEntityId?: ID;
  relatedEntityType?: string;
  actionUrl?: string;
};
```

---

# 4. Populate Utility Files

---

## `src/lib/storage.ts`

```ts
import type { AuthSession } from '@/types/auth.types';

const AUTH_SESSION_KEY = 'eb_gms_auth_session';
const ACCESS_TOKEN_KEY = 'eb_gms_access_token';
const REFRESH_TOKEN_KEY = 'eb_gms_refresh_token';

function safeParse<T>(value: string | null): T | null {
  if (!value) return null;

  try {
    return JSON.parse(value) as T;
  } catch {
    return null;
  }
}

export const storage = {
  getAccessToken(): string | null {
    return window.localStorage.getItem(ACCESS_TOKEN_KEY);
  },

  setAccessToken(token: string): void {
    window.localStorage.setItem(ACCESS_TOKEN_KEY, token);
  },

  getRefreshToken(): string | null {
    return window.localStorage.getItem(REFRESH_TOKEN_KEY);
  },

  setRefreshToken(token: string): void {
    window.localStorage.setItem(REFRESH_TOKEN_KEY, token);
  },

  getAuthSession(): AuthSession | null {
    return safeParse<AuthSession>(window.localStorage.getItem(AUTH_SESSION_KEY));
  },

  setAuthSession(session: AuthSession): void {
    window.localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify(session));
    window.localStorage.setItem(ACCESS_TOKEN_KEY, session.accessToken);

    if (session.refreshToken) {
      window.localStorage.setItem(REFRESH_TOKEN_KEY, session.refreshToken);
    }
  },

  clearAuthSession(): void {
    window.localStorage.removeItem(AUTH_SESSION_KEY);
    window.localStorage.removeItem(ACCESS_TOKEN_KEY);
    window.localStorage.removeItem(REFRESH_TOKEN_KEY);
  },
};
```

---

## `src/lib/logger.ts`

```ts
import { env, isDevelopment } from '@/config/env';

type LogMeta = Record<string, unknown>;

function shouldLog(): boolean {
  return isDevelopment || env.enableDebugLogs;
}

export const logger = {
  info(message: string, meta?: LogMeta): void {
    if (!shouldLog()) return;
    console.info(`[INFO] ${message}`, meta ?? '');
  },

  warn(message: string, meta?: LogMeta): void {
    if (!shouldLog()) return;
    console.warn(`[WARN] ${message}`, meta ?? '');
  },

  error(message: string, meta?: LogMeta): void {
    if (!shouldLog()) return;
    console.error(`[ERROR] ${message}`, meta ?? '');
  },
};
```

---

## `src/lib/validators.ts`

```ts
export function isRequired(value: unknown): boolean {
  if (value === null || value === undefined) return false;
  if (typeof value === 'string') return value.trim().length > 0;
  if (Array.isArray(value)) return value.length > 0;
  return true;
}

export function isValidEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export function isValidPhoneNumber(value: string): boolean {
  return /^\+?[0-9\s-]{7,20}$/.test(value);
}

export function isPositiveNumber(value: number): boolean {
  return Number.isFinite(value) && value > 0;
}

export function isPercentage(value: number): boolean {
  return Number.isFinite(value) && value >= 0 && value <= 100;
}

export function isValidDateString(value: string): boolean {
  return !Number.isNaN(Date.parse(value));
}
```

---

## `src/utils/date.ts`

```ts
import { format, formatDistanceToNow, isValid, parseISO } from 'date-fns';

function toDate(value: string | Date): Date | null {
  const date = typeof value === 'string' ? parseISO(value) : value;
  return isValid(date) ? date : null;
}

export function formatDate(value?: string | Date, fallback = 'N/A'): string {
  if (!value) return fallback;
  const date = toDate(value);
  return date ? format(date, 'dd MMM yyyy') : fallback;
}

export function formatDateTime(value?: string | Date, fallback = 'N/A'): string {
  if (!value) return fallback;
  const date = toDate(value);
  return date ? format(date, 'dd MMM yyyy, HH:mm') : fallback;
}

export function formatRelativeTime(value?: string | Date, fallback = 'N/A'): string {
  if (!value) return fallback;
  const date = toDate(value);
  return date ? formatDistanceToNow(date, { addSuffix: true }) : fallback;
}
```

---

## `src/utils/currency.ts`

```ts
import { DEFAULT_CURRENCY } from '@/config/constants';

export function formatCurrency(
  amount?: number,
  currency = DEFAULT_CURRENCY,
  fallback = 'N/A'
): string {
  if (amount === null || amount === undefined || Number.isNaN(amount)) return fallback;

  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatNumber(value?: number, fallback = 'N/A'): string {
  if (value === null || value === undefined || Number.isNaN(value)) return fallback;
  return new Intl.NumberFormat('en-UG').format(value);
}
```

---

## `src/utils/status.ts`

```ts
export function humanizeStatus(status?: string, fallback = 'N/A'): string {
  if (!status) return fallback;

  return status
    .toLowerCase()
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

export function isFinalStatus(status?: string): boolean {
  return ['COMPLETED', 'CANCELLED', 'REJECTED', 'APPROVED'].includes(status || '');
}

export function isRiskStatus(status?: string): boolean {
  return ['DELAYED', 'SUSPENDED', 'NON_COMPLIANT', 'CRITICAL'].includes(status || '');
}
```

---

## `src/utils/file.ts`

```ts
export const FILE_SIZE_MB = 1024 * 1024;

export function bytesToMb(bytes: number): number {
  return Number((bytes / FILE_SIZE_MB).toFixed(2));
}

export function isAllowedFileType(file: File, allowedTypes: string[]): boolean {
  return allowedTypes.includes(file.type);
}

export function isWithinFileSize(file: File, maxMb: number): boolean {
  return bytesToMb(file.size) <= maxMb;
}

export function getFileExtension(fileName: string): string {
  return fileName.split('.').pop()?.toLowerCase() || '';
}

export function buildFileAcceptString(types: string[]): string {
  return types.join(',');
}
```

---

# 5. Populate API Client Files

---

## `src/lib/http.ts`

```ts
import axios, { AxiosError, type AxiosInstance, type AxiosRequestConfig } from 'axios';

import { env } from '@/config/env';
import { storage } from './storage';
import { logger } from './logger';
import type { ApiErrorResponse } from '@/types/common.types';

export type HttpError = {
  message: string;
  statusCode?: number;
  errors?: Record<string, string[]>;
};

function createHttpClient(): AxiosInstance {
  const instance = axios.create({
    baseURL: env.apiBaseUrl,
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
  });

  instance.interceptors.request.use((config) => {
    const token = storage.getAccessToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  });

  instance.interceptors.response.use(
    (response) => response,
    (error: AxiosError<ApiErrorResponse>) => {
      const statusCode = error.response?.status;
      const message =
        error.response?.data?.message ||
        error.message ||
        'Something went wrong while communicating with the server.';

      if (statusCode === 401) {
        storage.clearAuthSession();
      }

      logger.error('HTTP request failed', {
        url: error.config?.url,
        method: error.config?.method,
        statusCode,
        message,
      });

      return Promise.reject({
        message,
        statusCode,
        errors: error.response?.data?.errors,
      } satisfies HttpError);
    }
  );

  return instance;
}

export const http = createHttpClient();

export async function apiGet<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const response = await http.get<T>(url, config);
  return response.data;
}

export async function apiPost<T, TPayload = unknown>(
  url: string,
  payload?: TPayload,
  config?: AxiosRequestConfig
): Promise<T> {
  const response = await http.post<T>(url, payload, config);
  return response.data;
}

export async function apiPut<T, TPayload = unknown>(
  url: string,
  payload?: TPayload,
  config?: AxiosRequestConfig
): Promise<T> {
  const response = await http.put<T>(url, payload, config);
  return response.data;
}

export async function apiPatch<T, TPayload = unknown>(
  url: string,
  payload?: TPayload,
  config?: AxiosRequestConfig
): Promise<T> {
  const response = await http.patch<T>(url, payload, config);
  return response.data;
}

export async function apiDelete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const response = await http.delete<T>(url, config);
  return response.data;
}
```

---

## `src/lib/api.ts`

```ts
export const API_ENDPOINTS = {
  auth: {
    login: '/auth/login',
    logout: '/auth/logout',
    me: '/auth/me',
    forgotPassword: '/auth/forgot-password',
    resetPassword: '/auth/reset-password',
  },

  users: '/users',
  projects: '/projects',
  contractors: '/contractors',
  evidence: '/evidence',
  monitoring: '/monitoring',
  approvals: '/approvals',
  funds: '/funds',
  audits: '/audits',
  reports: '/reports',
  notifications: '/notifications',
  settings: '/settings',
} as const;

export function withId(baseEndpoint: string, id: string): string {
  return `${baseEndpoint}/${id}`;
}

export function buildQueryString(params: Record<string, unknown> = {}): string {
  const query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return;
    query.set(key, String(value));
  });

  const queryString = query.toString();
  return queryString ? `?${queryString}` : '';
}
```

---

# 6. Populate Service Files

---

## `src/services/auth.service.ts`

```ts
import { API_ENDPOINTS } from '@/lib/api';
import { apiGet, apiPost } from '@/lib/http';
import { storage } from '@/lib/storage';
import type {
  ForgotPasswordPayload,
  LoginPayload,
  LoginResponse,
  ResetPasswordPayload,
} from '@/types/auth.types';
import type { User } from '@/types/user.types';
import type { ApiResponse } from '@/types/common.types';

export const authService = {
  async login(payload: LoginPayload): Promise<LoginResponse> {
    const response = await apiPost<ApiResponse<LoginResponse>, LoginPayload>(
      API_ENDPOINTS.auth.login,
      payload
    );

    storage.setAuthSession(response.data);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiGet<ApiResponse<User>>(API_ENDPOINTS.auth.me);
    return response.data;
  },

  async forgotPassword(payload: ForgotPasswordPayload): Promise<ApiResponse<null>> {
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
      await apiPost<ApiResponse<null>>(API_ENDPOINTS.auth.logout);
    } finally {
      storage.clearAuthSession();
    }
  },
};
```

---

## `src/services/projects.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiDelete, apiGet, apiPost, apiPut } from '@/lib/http';
import type { ApiResponse, ListQueryParams, PaginatedResponse, ID } from '@/types/common.types';
import type { CreateProjectPayload, Project, UpdateProjectPayload } from '@/types/project.types';

export const projectsService = {
  async list(params?: ListQueryParams): Promise<PaginatedResponse<Project>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<Project>>>(
      `${API_ENDPOINTS.projects}${buildQueryString(params)}`
    );
    return response.data;
  },

  async getById(projectId: ID): Promise<Project> {
    const response = await apiGet<ApiResponse<Project>>(withId(API_ENDPOINTS.projects, projectId));
    return response.data;
  },

  async create(payload: CreateProjectPayload): Promise<Project> {
    const response = await apiPost<ApiResponse<Project>, CreateProjectPayload>(
      API_ENDPOINTS.projects,
      payload
    );
    return response.data;
  },

  async update(projectId: ID, payload: UpdateProjectPayload): Promise<Project> {
    const response = await apiPut<ApiResponse<Project>, UpdateProjectPayload>(
      withId(API_ENDPOINTS.projects, projectId),
      payload
    );
    return response.data;
  },

  async remove(projectId: ID): Promise<ApiResponse<null>> {
    return apiDelete<ApiResponse<null>>(withId(API_ENDPOINTS.projects, projectId));
  },
};
```

---

## `src/services/contractors.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiGet, apiPost, apiPut } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type {
  Contractor,
  CreateContractorPayload,
  UpdateContractorPayload,
} from '@/types/contractor.types';

export const contractorsService = {
  async list(params?: ListQueryParams): Promise<PaginatedResponse<Contractor>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<Contractor>>>(
      `${API_ENDPOINTS.contractors}${buildQueryString(params)}`
    );
    return response.data;
  },

  async getById(contractorId: ID): Promise<Contractor> {
    const response = await apiGet<ApiResponse<Contractor>>(
      withId(API_ENDPOINTS.contractors, contractorId)
    );
    return response.data;
  },

  async create(payload: CreateContractorPayload): Promise<Contractor> {
    const response = await apiPost<ApiResponse<Contractor>, CreateContractorPayload>(
      API_ENDPOINTS.contractors,
      payload
    );
    return response.data;
  },

  async update(contractorId: ID, payload: UpdateContractorPayload): Promise<Contractor> {
    const response = await apiPut<ApiResponse<Contractor>, UpdateContractorPayload>(
      withId(API_ENDPOINTS.contractors, contractorId),
      payload
    );
    return response.data;
  },
};
```

---

## `src/services/evidence.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiGet, apiPatch, apiPost } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type { Evidence, UploadEvidencePayload, VerifyEvidencePayload } from '@/types/evidence.types';

export const evidenceService = {
  async list(params?: ListQueryParams): Promise<PaginatedResponse<Evidence>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<Evidence>>>(
      `${API_ENDPOINTS.evidence}${buildQueryString(params)}`
    );
    return response.data;
  },

  async getById(evidenceId: ID): Promise<Evidence> {
    const response = await apiGet<ApiResponse<Evidence>>(withId(API_ENDPOINTS.evidence, evidenceId));
    return response.data;
  },

  async upload(payload: UploadEvidencePayload): Promise<Evidence[]> {
    const formData = new FormData();
    formData.append('projectId', payload.projectId);
    if (payload.milestoneId) formData.append('milestoneId', payload.milestoneId);
    formData.append('type', payload.type);
    formData.append('title', payload.title);
    if (payload.description) formData.append('description', payload.description);
    if (payload.gpsLatitude !== undefined) formData.append('gpsLatitude', String(payload.gpsLatitude));
    if (payload.gpsLongitude !== undefined) formData.append('gpsLongitude', String(payload.gpsLongitude));

    payload.files.forEach((file) => formData.append('files', file));

    const response = await apiPost<ApiResponse<Evidence[]>, FormData>(
      `${API_ENDPOINTS.evidence}/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  async verify(evidenceId: ID, payload: VerifyEvidencePayload): Promise<Evidence> {
    const response = await apiPatch<ApiResponse<Evidence>, VerifyEvidencePayload>(
      `${withId(API_ENDPOINTS.evidence, evidenceId)}/verify`,
      payload
    );
    return response.data;
  },
};
```

---

## `src/services/monitoring.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiGet, apiPost } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type {
  CreateFieldInspectionPayload,
  FieldInspection,
  MonitoringReview,
  SubmitMonitoringReviewPayload,
} from '@/types/monitoring.types';

export const monitoringService = {
  async getReviewQueue(params?: ListQueryParams): Promise<PaginatedResponse<MonitoringReview>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<MonitoringReview>>>(
      `${API_ENDPOINTS.monitoring}/review-queue${buildQueryString(params)}`
    );
    return response.data;
  },

  async submitReview(payload: SubmitMonitoringReviewPayload): Promise<MonitoringReview> {
    const response = await apiPost<ApiResponse<MonitoringReview>, SubmitMonitoringReviewPayload>(
      `${API_ENDPOINTS.monitoring}/reviews`,
      payload
    );
    return response.data;
  },

  async listFieldInspections(params?: ListQueryParams): Promise<PaginatedResponse<FieldInspection>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<FieldInspection>>>(
      `${API_ENDPOINTS.monitoring}/field-inspections${buildQueryString(params)}`
    );
    return response.data;
  },

  async getFieldInspectionById(inspectionId: ID): Promise<FieldInspection> {
    const response = await apiGet<ApiResponse<FieldInspection>>(
      withId(`${API_ENDPOINTS.monitoring}/field-inspections`, inspectionId)
    );
    return response.data;
  },

  async createFieldInspection(payload: CreateFieldInspectionPayload): Promise<FieldInspection> {
    const response = await apiPost<ApiResponse<FieldInspection>, CreateFieldInspectionPayload>(
      `${API_ENDPOINTS.monitoring}/field-inspections`,
      payload
    );
    return response.data;
  },
};
```

---

## `src/services/approvals.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiGet, apiPatch } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type { ApprovalRequest, SubmitApprovalDecisionPayload } from '@/types/approval.types';

export const approvalsService = {
  async list(params?: ListQueryParams): Promise<PaginatedResponse<ApprovalRequest>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<ApprovalRequest>>>(
      `${API_ENDPOINTS.approvals}${buildQueryString(params)}`
    );
    return response.data;
  },

  async getById(approvalId: ID): Promise<ApprovalRequest> {
    const response = await apiGet<ApiResponse<ApprovalRequest>>(
      withId(API_ENDPOINTS.approvals, approvalId)
    );
    return response.data;
  },

  async submitDecision(
    approvalId: ID,
    payload: SubmitApprovalDecisionPayload
  ): Promise<ApprovalRequest> {
    const response = await apiPatch<ApiResponse<ApprovalRequest>, SubmitApprovalDecisionPayload>(
      `${withId(API_ENDPOINTS.approvals, approvalId)}/decision`,
      payload
    );
    return response.data;
  },
};
```

---

## `src/services/funds.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiGet, apiPost } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type { CreateFundReleasePayload, FundRelease, FundsSummary } from '@/types/funds.types';

export const fundsService = {
  async listReleases(params?: ListQueryParams): Promise<PaginatedResponse<FundRelease>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<FundRelease>>>(
      `${API_ENDPOINTS.funds}/releases${buildQueryString(params)}`
    );
    return response.data;
  },

  async getReleaseById(releaseId: ID): Promise<FundRelease> {
    const response = await apiGet<ApiResponse<FundRelease>>(
      withId(`${API_ENDPOINTS.funds}/releases`, releaseId)
    );
    return response.data;
  },

  async createRelease(payload: CreateFundReleasePayload): Promise<FundRelease> {
    const response = await apiPost<ApiResponse<FundRelease>, CreateFundReleasePayload>(
      `${API_ENDPOINTS.funds}/releases`,
      payload
    );
    return response.data;
  },

  async getProjectSummary(projectId: ID): Promise<FundsSummary> {
    const response = await apiGet<ApiResponse<FundsSummary>>(
      `${API_ENDPOINTS.funds}/projects/${projectId}/summary`
    );
    return response.data;
  },
};
```

---

## `src/services/audits.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiGet, apiPost } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type { AuditAssignment, AuditFinding, CreateAuditFindingPayload } from '@/types/audit.types';

export const auditsService = {
  async listAssignments(params?: ListQueryParams): Promise<PaginatedResponse<AuditAssignment>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<AuditAssignment>>>(
      `${API_ENDPOINTS.audits}/assignments${buildQueryString(params)}`
    );
    return response.data;
  },

  async getAssignmentById(assignmentId: ID): Promise<AuditAssignment> {
    const response = await apiGet<ApiResponse<AuditAssignment>>(
      withId(`${API_ENDPOINTS.audits}/assignments`, assignmentId)
    );
    return response.data;
  },

  async createFinding(payload: CreateAuditFindingPayload): Promise<AuditFinding> {
    const response = await apiPost<ApiResponse<AuditFinding>, CreateAuditFindingPayload>(
      `${API_ENDPOINTS.audits}/findings`,
      payload
    );
    return response.data;
  },
};
```

---

## `src/services/reports.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString } from '@/lib/api';
import { apiGet, apiPost } from '@/lib/http';
import type { ApiResponse } from '@/types/common.types';
import type { ExportReportPayload, ReportFilters, ReportSummary } from '@/types/report.types';

export const reportsService = {
  async getSummary(filters?: ReportFilters): Promise<ReportSummary> {
    const response = await apiGet<ApiResponse<ReportSummary>>(
      `${API_ENDPOINTS.reports}/summary${buildQueryString(filters)}`
    );
    return response.data;
  },

  async exportReport(payload: ExportReportPayload): Promise<Blob> {
    return apiPost<Blob, ExportReportPayload>(`${API_ENDPOINTS.reports}/export`, payload, {
      responseType: 'blob',
    });
  },
};
```

---

## `src/services/notifications.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiGet, apiPatch } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type { Notification } from '@/types/notification.types';

export const notificationsService = {
  async list(params?: ListQueryParams): Promise<PaginatedResponse<Notification>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<Notification>>>(
      `${API_ENDPOINTS.notifications}${buildQueryString(params)}`
    );
    return response.data;
  },

  async markAsRead(notificationId: ID): Promise<Notification> {
    const response = await apiPatch<ApiResponse<Notification>>(
      `${withId(API_ENDPOINTS.notifications, notificationId)}/read`
    );
    return response.data;
  },

  async markAllAsRead(): Promise<ApiResponse<null>> {
    return apiPatch<ApiResponse<null>>(`${API_ENDPOINTS.notifications}/read-all`);
  },
};
```

---

## `src/services/users.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiGet, apiPost, apiPut } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type { CreateUserPayload, UpdateUserPayload, User } from '@/types/user.types';

export const usersService = {
  async list(params?: ListQueryParams): Promise<PaginatedResponse<User>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<User>>>(
      `${API_ENDPOINTS.users}${buildQueryString(params)}`
    );
    return response.data;
  },

  async getById(userId: ID): Promise<User> {
    const response = await apiGet<ApiResponse<User>>(withId(API_ENDPOINTS.users, userId));
    return response.data;
  },

  async create(payload: CreateUserPayload): Promise<User> {
    const response = await apiPost<ApiResponse<User>, CreateUserPayload>(
      API_ENDPOINTS.users,
      payload
    );
    return response.data;
  },

  async update(userId: ID, payload: UpdateUserPayload): Promise<User> {
    const response = await apiPut<ApiResponse<User>, UpdateUserPayload>(
      withId(API_ENDPOINTS.users, userId),
      payload
    );
    return response.data;
  },
};
```

---

## `src/services/settings.service.ts`

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiDelete, apiGet, apiPost, apiPut } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';

type ReferenceDataType = 'ministries' | 'districts' | 'project-categories' | 'approval-levels' | 'risk-rules';

export type ReferenceDataItem = {
  id: ID;
  name: string;
  code?: string;
  description?: string;
  isActive: boolean;
};

export type CreateReferenceDataPayload = {
  name: string;
  code?: string;
  description?: string;
  isActive?: boolean;
};

export const settingsService = {
  async listReferenceData(
    type: ReferenceDataType,
    params?: ListQueryParams
  ): Promise<PaginatedResponse<ReferenceDataItem>> {
    const response = await apiGet<ApiResponse<PaginatedResponse<ReferenceDataItem>>>(
      `${API_ENDPOINTS.settings}/${type}${buildQueryString(params)}`
    );
    return response.data;
  },

  async createReferenceData(
    type: ReferenceDataType,
    payload: CreateReferenceDataPayload
  ): Promise<ReferenceDataItem> {
    const response = await apiPost<ApiResponse<ReferenceDataItem>, CreateReferenceDataPayload>(
      `${API_ENDPOINTS.settings}/${type}`,
      payload
    );
    return response.data;
  },

  async updateReferenceData(
    type: ReferenceDataType,
    itemId: ID,
    payload: Partial<CreateReferenceDataPayload>
  ): Promise<ReferenceDataItem> {
    const response = await apiPut<ApiResponse<ReferenceDataItem>, Partial<CreateReferenceDataPayload>>(
      withId(`${API_ENDPOINTS.settings}/${type}`, itemId),
      payload
    );
    return response.data;
  },

  async removeReferenceData(type: ReferenceDataType, itemId: ID): Promise<ApiResponse<null>> {
    return apiDelete<ApiResponse<null>>(withId(`${API_ENDPOINTS.settings}/${type}`, itemId));
  },
};
```

---

# 7. Optional Barrel Files

These are optional but useful for cleaner imports.

Run:

```bash
touch src/services/index.ts src/types/index.ts
```

---

## `src/services/index.ts`

```ts
export * from './auth.service';
export * from './projects.service';
export * from './contractors.service';
export * from './evidence.service';
export * from './monitoring.service';
export * from './approvals.service';
export * from './funds.service';
export * from './audits.service';
export * from './reports.service';
export * from './notifications.service';
export * from './users.service';
export * from './settings.service';
```

---

## `src/types/index.ts`

```ts
export * from './common.types';
export * from './auth.types';
export * from './user.types';
export * from './project.types';
export * from './contractor.types';
export * from './evidence.types';
export * from './monitoring.types';
export * from './approval.types';
export * from './funds.types';
export * from './audit.types';
export * from './report.types';
export * from './notification.types';
```

---

# 8. Build Test

Run:

```bash
npm run build
```

Expected result:

```txt
✓ built
```

---

# 9. Important Integration Note

At this stage, the frontend API layer is ready, but most service calls will only work once backend endpoints exist.

For now, Phase 4 is successful if:

- TypeScript compiles.
- `npm run build` passes.
- No service files are imported into UI components randomly.
- API logic is centralized inside `src/services/` and `src/lib/http.ts`.

---

# 10. Phase 4 Completion Checklist

Phase 4 is complete when:

- `src/lib/http.ts` centralizes all HTTP requests.
- `src/lib/api.ts` centralizes API endpoint paths.
- `src/lib/storage.ts` centralizes token/session storage.
- `src/lib/logger.ts` centralizes logging.
- `src/lib/validators.ts` provides basic validation helpers.
- `src/types/` contains core domain types.
- `src/services/` contains API modules for every major feature.
- Utility files for date, currency, status, and files exist.
- `npm run build` passes.

---

# Phase 4 Expected Output

After completing this phase:

- The frontend has one standard way of calling backend APIs.
- UI components remain clean and focused on presentation.
- TypeScript types are ready for safer module development.
- Future feature phases can import services instead of writing HTTP logic inside pages.

---

# Next Phase

After Phase 4 passes build and review, proceed to:

```txt
Phase 5: Authentication Module
```
