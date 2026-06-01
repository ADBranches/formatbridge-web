# Phase 8 — Contractor Management Module

**Project:** EB Government Monitoring System  
**Frontend:** React + TypeScript + Vite + Tailwind CSS v4  
**Phase Goal:** Implement contractor registration, contractor listing, contractor details, contractor editing, compliance visibility, assigned projects, performance history, and contractor document visibility.

---

## Phase 7 Confirmation

Phase 7 is complete.

Your build passed successfully:

```txt
✓ 2873 modules transformed.
✓ built in 1.10s
```

The warning about chunks larger than 500 kB is not a blocker. It can be handled later through route-level lazy loading and dashboard chart code-splitting.

---

# Phase 8 Objectives

This phase implements:

- Register and manage contractors.
- View contractor profiles.
- Show assigned projects.
- Show compliance status.
- Show contractor performance history.
- Show contractor documents.
- Allow admins to activate, suspend, or flag contractors.
- Prepare contractor records for later evidence, project assignment, audit, and payment workflows.

---

# 1. Create Phase 8 Directories

Run from the project root:

```bash
mkdir -p src/features/contractors/components src/features/contractors/pages src/features/contractors/hooks src/features/contractors/schemas
```

---

# 2. Create Phase 8 Files

Run from the project root:

```bash
touch src/features/contractors/pages/ContractorsListPage.tsx \
src/features/contractors/pages/ContractorDetailsPage.tsx \
src/features/contractors/pages/CreateContractorPage.tsx \
src/features/contractors/pages/EditContractorPage.tsx \
src/features/contractors/components/ContractorForm.tsx \
src/features/contractors/components/ContractorTable.tsx \
src/features/contractors/components/ContractorStatusBadge.tsx \
src/features/contractors/components/ContractorProjects.tsx \
src/features/contractors/components/ContractorPerformance.tsx \
src/features/contractors/components/ContractorDocuments.tsx \
src/features/contractors/hooks/useContractors.ts \
src/features/contractors/hooks/useContractorDetails.ts \
src/features/contractors/hooks/useCreateContractor.ts \
src/features/contractors/hooks/useUpdateContractor.ts \
src/features/contractors/schemas/contractor.schema.ts
```

The following existing files will also be updated:

```txt
src/types/contractor.types.ts
src/services/contractors.service.ts
src/config/routes.ts
src/app/router.tsx
```

---

# 3. Update Contractor Types

## `src/types/contractor.types.ts`

Replace the file content with this:

```ts
import type { ID, AuditMetadata } from './common.types';
import type { ProjectStatus } from './project.types';

export type ContractorStatus =
  | 'ACTIVE'
  | 'SUSPENDED'
  | 'BLACKLISTED'
  | 'PENDING_VERIFICATION';

export type ContractorComplianceStatus =
  | 'COMPLIANT'
  | 'MINOR_ISSUES'
  | 'MAJOR_ISSUES'
  | 'NON_COMPLIANT';

export type ContractorProject = {
  id: ID;
  projectId: ID;
  projectCode: string;
  projectTitle: string;
  districtName: string;
  budgetAmount: number;
  progressPercentage: number;
  status: ProjectStatus;
};

export type ContractorDocument = AuditMetadata & {
  id: ID;
  contractorId: ID;
  title: string;
  type: 'LICENSE' | 'TAX_CERTIFICATE' | 'REGISTRATION' | 'CONTRACT' | 'OTHER';
  fileName: string;
  fileUrl: string;
};

export type ContractorPerformanceRecord = {
  id: ID;
  label: string;
  value: string | number;
  description: string;
  tone: 'green' | 'orange' | 'blue' | 'red' | 'navy';
};

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
  complianceStatus: ContractorComplianceStatus;
  complianceScore: number;
  activeProjectsCount: number;
  completedProjectsCount: number;
  delayedProjectsCount: number;
  totalContractValue: number;
  projects?: ContractorProject[];
  documents?: ContractorDocument[];
  performance?: ContractorPerformanceRecord[];
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
  complianceStatus?: ContractorComplianceStatus;
  complianceScore?: number;
};
```

---

# 4. Contractor Schema

## `src/features/contractors/schemas/contractor.schema.ts`

```ts
import { z } from 'zod';

export const contractorSchema = z.object({
  companyName: z.string().trim().min(3, 'Company name must be at least 3 characters.'),
  registrationNumber: z.string().trim().min(3, 'Registration number is required.'),
  taxIdentificationNumber: z.string().trim().optional(),
  licenseNumber: z.string().trim().optional(),
  contactPersonName: z.string().trim().min(3, 'Contact person name is required.'),
  contactEmail: z.string().trim().email('Enter a valid email address.'),
  contactPhone: z.string().trim().min(7, 'Contact phone number is required.'),
  address: z.string().trim().optional(),
});

export type ContractorFormValues = z.infer<typeof contractorSchema>;
```

---

# 5. Update Contractor Service With Mock Data

## `src/services/contractors.service.ts`

Replace the file content with this:

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiGet, apiPost, apiPut } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type {
  Contractor,
  CreateContractorPayload,
  UpdateContractorPayload,
} from '@/types/contractor.types';

const useMockApi = import.meta.env.VITE_USE_MOCK_API === 'true';
const now = new Date().toISOString();

const mockContractors: Contractor[] = [
  {
    id: 'CON-001',
    companyName: 'Prime Build Contractors Ltd',
    registrationNumber: 'UG-REG-00124',
    taxIdentificationNumber: 'TIN-10024567',
    licenseNumber: 'LIC-BUILD-2026-001',
    contactPersonName: 'Contractor Contact One',
    contactEmail: 'contact@primebuild.local',
    contactPhone: '+256700000001',
    address: 'Kampala Industrial Area',
    status: 'ACTIVE',
    complianceStatus: 'COMPLIANT',
    complianceScore: 86,
    activeProjectsCount: 2,
    completedProjectsCount: 5,
    delayedProjectsCount: 1,
    totalContractValue: 12800000000,
    createdAt: now,
    updatedAt: now,
    projects: [
      {
        id: 'CP-001',
        projectId: 'PRJ-001',
        projectCode: 'EB/2026/001',
        projectTitle: 'Wakiso Health Center Construction',
        districtName: 'Wakiso',
        budgetAmount: 4800000000,
        progressPercentage: 58,
        status: 'IN_PROGRESS',
      },
    ],
    documents: [
      {
        id: 'CDOC-001',
        contractorId: 'CON-001',
        title: 'Construction License',
        type: 'LICENSE',
        fileName: 'prime-build-license.pdf',
        fileUrl: '#',
        createdAt: now,
        updatedAt: now,
      },
      {
        id: 'CDOC-002',
        contractorId: 'CON-001',
        title: 'Tax Clearance Certificate',
        type: 'TAX_CERTIFICATE',
        fileName: 'prime-build-tax-clearance.pdf',
        fileUrl: '#',
        createdAt: now,
        updatedAt: now,
      },
    ],
    performance: [
      {
        id: 'PERF-001',
        label: 'Completion Rate',
        value: '82%',
        description: 'Average milestone completion performance.',
        tone: 'green',
      },
      {
        id: 'PERF-002',
        label: 'Evidence Quality',
        value: '91%',
        description: 'Evidence packages accepted after first review.',
        tone: 'green',
      },
      {
        id: 'PERF-003',
        label: 'Delayed Projects',
        value: 1,
        description: 'Projects with delayed milestone delivery.',
        tone: 'orange',
      },
    ],
  },
  {
    id: 'CON-002',
    companyName: 'North Roads Engineering Ltd',
    registrationNumber: 'UG-REG-00456',
    taxIdentificationNumber: 'TIN-88881234',
    licenseNumber: 'LIC-ROAD-2026-019',
    contactPersonName: 'Contractor Contact Two',
    contactEmail: 'contact@northroads.local',
    contactPhone: '+256700000002',
    address: 'Arua Municipality',
    status: 'PENDING_VERIFICATION',
    complianceStatus: 'MINOR_ISSUES',
    complianceScore: 68,
    activeProjectsCount: 1,
    completedProjectsCount: 2,
    delayedProjectsCount: 1,
    totalContractValue: 7200000000,
    createdAt: now,
    updatedAt: now,
    projects: [
      {
        id: 'CP-002',
        projectId: 'PRJ-002',
        projectCode: 'EB/2026/002',
        projectTitle: 'Arua Rural Road Maintenance',
        districtName: 'Arua',
        budgetAmount: 7200000000,
        progressPercentage: 44,
        status: 'DELAYED',
      },
    ],
    documents: [],
    performance: [
      {
        id: 'PERF-004',
        label: 'Completion Rate',
        value: '64%',
        description: 'Average milestone completion performance.',
        tone: 'orange',
      },
      {
        id: 'PERF-005',
        label: 'Evidence Quality',
        value: '73%',
        description: 'Evidence accepted after first review.',
        tone: 'orange',
      },
    ],
  },
  {
    id: 'CON-003',
    companyName: 'Aqua Infrastructure Uganda',
    registrationNumber: 'UG-REG-00990',
    taxIdentificationNumber: 'TIN-33334444',
    licenseNumber: 'LIC-WATER-2026-077',
    contactPersonName: 'Contractor Contact Three',
    contactEmail: 'contact@aqua-uganda.local',
    contactPhone: '+256700000003',
    address: 'Moroto Town',
    status: 'SUSPENDED',
    complianceStatus: 'MAJOR_ISSUES',
    complianceScore: 41,
    activeProjectsCount: 1,
    completedProjectsCount: 1,
    delayedProjectsCount: 1,
    totalContractValue: 5900000000,
    createdAt: now,
    updatedAt: now,
    projects: [
      {
        id: 'CP-003',
        projectId: 'PRJ-003',
        projectCode: 'EB/2026/003',
        projectTitle: 'Moroto Water Supply Upgrade',
        districtName: 'Moroto',
        budgetAmount: 5900000000,
        progressPercentage: 28,
        status: 'UNDER_REVIEW',
      },
    ],
    documents: [],
    performance: [
      {
        id: 'PERF-006',
        label: 'Compliance Score',
        value: '41%',
        description: 'Current compliance rating from audits and reviews.',
        tone: 'red',
      },
    ],
  },
];

function filterContractors(params?: ListQueryParams): Contractor[] {
  let result = [...mockContractors];

  if (params?.search) {
    const search = params.search.toLowerCase();
    result = result.filter((contractor) =>
      [
        contractor.companyName,
        contractor.registrationNumber,
        contractor.taxIdentificationNumber,
        contractor.licenseNumber,
        contractor.contactPersonName,
        contractor.contactEmail,
      ]
        .filter(Boolean)
        .some((value) => String(value).toLowerCase().includes(search))
    );
  }

  if (params?.status) {
    result = result.filter((contractor) => contractor.status === params.status);
  }

  return result;
}

function paginateContractors(
  contractors: Contractor[],
  params?: ListQueryParams
): PaginatedResponse<Contractor> {
  const page = params?.page || 1;
  const perPage = params?.perPage || 10;
  const start = (page - 1) * perPage;
  const items = contractors.slice(start, start + perPage);

  return {
    items,
    meta: {
      page,
      perPage,
      totalItems: contractors.length,
      totalPages: Math.max(1, Math.ceil(contractors.length / perPage)),
    },
  };
}

export const contractorsService = {
  async list(params?: ListQueryParams): Promise<PaginatedResponse<Contractor>> {
    if (useMockApi) {
      return paginateContractors(filterContractors(params), params);
    }

    const response = await apiGet<ApiResponse<PaginatedResponse<Contractor>>>(
      `${API_ENDPOINTS.contractors}${buildQueryString(params)}`
    );
    return response.data;
  },

  async getById(contractorId: ID): Promise<Contractor> {
    if (useMockApi) {
      const contractor = mockContractors.find((item) => item.id === contractorId);
      if (!contractor) throw new Error('Contractor not found.');
      return contractor;
    }

    const response = await apiGet<ApiResponse<Contractor>>(
      withId(API_ENDPOINTS.contractors, contractorId)
    );
    return response.data;
  },

  async create(payload: CreateContractorPayload): Promise<Contractor> {
    if (useMockApi) {
      return {
        id: `CON-${Date.now()}`,
        ...payload,
        status: 'PENDING_VERIFICATION',
        complianceStatus: 'MINOR_ISSUES',
        complianceScore: 50,
        activeProjectsCount: 0,
        completedProjectsCount: 0,
        delayedProjectsCount: 0,
        totalContractValue: 0,
        projects: [],
        documents: [],
        performance: [],
        createdAt: now,
        updatedAt: now,
      };
    }

    const response = await apiPost<ApiResponse<Contractor>, CreateContractorPayload>(
      API_ENDPOINTS.contractors,
      payload
    );
    return response.data;
  },

  async update(contractorId: ID, payload: UpdateContractorPayload): Promise<Contractor> {
    if (useMockApi) {
      const contractor = mockContractors.find((item) => item.id === contractorId);
      if (!contractor) throw new Error('Contractor not found.');
      return { ...contractor, ...payload, updatedAt: new Date().toISOString() };
    }

    const response = await apiPut<ApiResponse<Contractor>, UpdateContractorPayload>(
      withId(API_ENDPOINTS.contractors, contractorId),
      payload
    );
    return response.data;
  },
};
```

---

# 6. Contractor Hooks

## `src/features/contractors/hooks/useContractors.ts`

```ts
import { useQuery } from '@tanstack/react-query';

import { contractorsService } from '@/services/contractors.service';
import type { ListQueryParams } from '@/types/common.types';

export function useContractors(params?: ListQueryParams) {
  return useQuery({
    queryKey: ['contractors', params],
    queryFn: () => contractorsService.list(params),
  });
}
```

---

## `src/features/contractors/hooks/useContractorDetails.ts`

```ts
import { useQuery } from '@tanstack/react-query';

import { contractorsService } from '@/services/contractors.service';

export function useContractorDetails(contractorId?: string) {
  return useQuery({
    queryKey: ['contractor', contractorId],
    queryFn: () => contractorsService.getById(contractorId as string),
    enabled: Boolean(contractorId),
  });
}
```

---

## `src/features/contractors/hooks/useCreateContractor.ts`

```ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

import { contractorsService } from '@/services/contractors.service';
import type { CreateContractorPayload } from '@/types/contractor.types';

export function useCreateContractor() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateContractorPayload) => contractorsService.create(payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['contractors'] });
      navigate('/contractors');
    },
  });
}
```

---

## `src/features/contractors/hooks/useUpdateContractor.ts`

```ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

import { contractorsService } from '@/services/contractors.service';
import type { UpdateContractorPayload } from '@/types/contractor.types';

export function useUpdateContractor(contractorId: string) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UpdateContractorPayload) => contractorsService.update(contractorId, payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['contractors'] });
      await queryClient.invalidateQueries({ queryKey: ['contractor', contractorId] });
      navigate(`/contractors/${contractorId}`);
    },
  });
}
```

---

# 7. Contractor Components

## `src/features/contractors/components/ContractorStatusBadge.tsx`

```tsx
import { Badge } from '@/components/ui/Badge';
import type { ContractorStatus } from '@/types/contractor.types';

function statusLabel(status: ContractorStatus): string {
  const labels: Record<ContractorStatus, string> = {
    ACTIVE: 'Active',
    SUSPENDED: 'Suspended',
    BLACKLISTED: 'Blacklisted',
    PENDING_VERIFICATION: 'Pending Verification',
  };

  return labels[status];
}

function statusVariant(status: ContractorStatus) {
  if (status === 'ACTIVE') return 'success';
  if (status === 'PENDING_VERIFICATION') return 'warning';
  return 'danger';
}

export function ContractorStatusBadge({ status }: { status: ContractorStatus }) {
  return <Badge variant={statusVariant(status)}>{statusLabel(status)}</Badge>;
}
```

---

## `src/features/contractors/components/ContractorForm.tsx`

```tsx
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

import { FormField } from '@/components/forms/FormField';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import type { Contractor, CreateContractorPayload } from '@/types/contractor.types';

import { contractorSchema, type ContractorFormValues } from '../schemas/contractor.schema';

type ContractorFormProps = {
  defaultValues?: Contractor;
  isSubmitting?: boolean;
  onSubmit: (payload: CreateContractorPayload) => void;
};

export function ContractorForm({ defaultValues, isSubmitting, onSubmit }: ContractorFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ContractorFormValues>({
    resolver: zodResolver(contractorSchema),
    defaultValues: {
      companyName: defaultValues?.companyName || '',
      registrationNumber: defaultValues?.registrationNumber || '',
      taxIdentificationNumber: defaultValues?.taxIdentificationNumber || '',
      licenseNumber: defaultValues?.licenseNumber || '',
      contactPersonName: defaultValues?.contactPersonName || '',
      contactEmail: defaultValues?.contactEmail || '',
      contactPhone: defaultValues?.contactPhone || '',
      address: defaultValues?.address || '',
    },
  });

  function submit(values: ContractorFormValues) {
    onSubmit(values);
  }

  return (
    <form onSubmit={handleSubmit(submit)} className="space-y-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="grid gap-5 md:grid-cols-2">
        <FormField label="Company Name" error={errors.companyName?.message} required>
          <Input hasError={Boolean(errors.companyName)} {...register('companyName')} />
        </FormField>

        <FormField label="Registration Number" error={errors.registrationNumber?.message} required>
          <Input hasError={Boolean(errors.registrationNumber)} {...register('registrationNumber')} />
        </FormField>
      </div>

      <div className="grid gap-5 md:grid-cols-2">
        <FormField label="Tax Identification Number">
          <Input placeholder="TIN-XXXXXXXX" {...register('taxIdentificationNumber')} />
        </FormField>

        <FormField label="License Number">
          <Input placeholder="LIC-XXXX" {...register('licenseNumber')} />
        </FormField>
      </div>

      <div className="grid gap-5 md:grid-cols-2">
        <FormField label="Contact Person" error={errors.contactPersonName?.message} required>
          <Input hasError={Boolean(errors.contactPersonName)} {...register('contactPersonName')} />
        </FormField>

        <FormField label="Contact Email" error={errors.contactEmail?.message} required>
          <Input type="email" hasError={Boolean(errors.contactEmail)} {...register('contactEmail')} />
        </FormField>
      </div>

      <FormField label="Contact Phone" error={errors.contactPhone?.message} required>
        <Input hasError={Boolean(errors.contactPhone)} {...register('contactPhone')} />
      </FormField>

      <FormField label="Address">
        <Textarea {...register('address')} />
      </FormField>

      <div className="flex justify-end">
        <Button type="submit" isLoading={isSubmitting}>Save Contractor</Button>
      </div>
    </form>
  );
}
```

---

## `src/features/contractors/components/ContractorTable.tsx`

```tsx
import { Eye, Pencil } from 'lucide-react';
import { Link } from 'react-router-dom';

import { Button } from '@/components/ui/Button';
import { EmptyState } from '@/components/ui/EmptyState';
import { ProgressBar } from '@/components/ui/ProgressBar';
import type { Contractor } from '@/types/contractor.types';
import { formatCurrency } from '@/utils/currency';

import { ContractorStatusBadge } from './ContractorStatusBadge';

type ContractorTableProps = {
  contractors: Contractor[];
};

export function ContractorTable({ contractors }: ContractorTableProps) {
  if (contractors.length === 0) {
    return <EmptyState title="No contractors found" description="Try changing your filters or register a new contractor." />;
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Contractor</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Contact</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Compliance</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Projects</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Contract Value</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Status</th>
              <th className="px-4 py-3 text-right text-xs font-bold uppercase tracking-wide text-slate-500">Actions</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100 bg-white">
            {contractors.map((contractor) => (
              <tr key={contractor.id} className="hover:bg-slate-50">
                <td className="px-4 py-4">
                  <p className="font-bold text-slate-950">{contractor.companyName}</p>
                  <p className="text-xs text-slate-500">{contractor.registrationNumber}</p>
                </td>
                <td className="px-4 py-4 text-sm text-slate-600">
                  <p>{contractor.contactPersonName}</p>
                  <p className="text-xs text-slate-500">{contractor.contactEmail}</p>
                </td>
                <td className="px-4 py-4 min-w-40">
                  <ProgressBar value={contractor.complianceScore} showValue />
                </td>
                <td className="px-4 py-4 text-sm text-slate-700">
                  {contractor.activeProjectsCount} active / {contractor.completedProjectsCount} completed
                </td>
                <td className="px-4 py-4 text-sm font-semibold text-slate-700">
                  {formatCurrency(contractor.totalContractValue)}
                </td>
                <td className="px-4 py-4"><ContractorStatusBadge status={contractor.status} /></td>
                <td className="px-4 py-4">
                  <div className="flex justify-end gap-2">
                    <Link to={`/contractors/${contractor.id}`}>
                      <Button variant="ghost" size="sm"><Eye className="h-4 w-4" /></Button>
                    </Link>
                    <Link to={`/contractors/${contractor.id}/edit`}>
                      <Button variant="outline" size="sm"><Pencil className="h-4 w-4" /></Button>
                    </Link>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

---

## `src/features/contractors/components/ContractorProjects.tsx`

```tsx
import { Link } from 'react-router-dom';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { EmptyState } from '@/components/ui/EmptyState';
import { ProgressBar } from '@/components/ui/ProgressBar';
import type { ContractorProject } from '@/types/contractor.types';
import { formatCurrency } from '@/utils/currency';

import { ProjectStatusBadge } from '@/features/projects/components/ProjectStatusBadge';

export function ContractorProjects({ projects = [] }: { projects?: ContractorProject[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Assigned Projects</CardTitle>
        <CardDescription>Projects currently or previously assigned to this contractor.</CardDescription>
      </CardHeader>
      <CardContent>
        {projects.length === 0 ? (
          <EmptyState title="No assigned projects" description="Assigned projects will appear here." />
        ) : (
          <div className="space-y-4">
            {projects.map((project) => (
              <Link
                key={project.id}
                to={`/projects/${project.projectId}`}
                className="block rounded-2xl border border-slate-200 bg-slate-50 p-4 hover:bg-slate-100"
              >
                <div className="flex flex-col justify-between gap-3 md:flex-row md:items-start">
                  <div>
                    <p className="font-bold text-slate-950">{project.projectTitle}</p>
                    <p className="text-xs text-slate-500">{project.projectCode} • {project.districtName}</p>
                  </div>
                  <ProjectStatusBadge status={project.status} />
                </div>

                <div className="mt-4 grid gap-4 md:grid-cols-[1fr_12rem] md:items-center">
                  <ProgressBar value={project.progressPercentage} label="Progress" />
                  <p className="text-sm font-bold text-slate-700">{formatCurrency(project.budgetAmount)}</p>
                </div>
              </Link>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

---

## `src/features/contractors/components/ContractorPerformance.tsx`

```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import type { ContractorPerformanceRecord } from '@/types/contractor.types';
import { cn } from '@/utils/cn';

const toneClasses = {
  green: 'bg-emerald-50 text-emerald-700',
  orange: 'bg-orange-50 text-orange-700',
  blue: 'bg-blue-50 text-blue-700',
  red: 'bg-red-50 text-red-700',
  navy: 'bg-[#051931]/10 text-[#051931]',
};

export function ContractorPerformance({ performance = [] }: { performance?: ContractorPerformanceRecord[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Performance History</CardTitle>
        <CardDescription>Contractor delivery, compliance, and evidence quality indicators.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 md:grid-cols-3">
          {performance.map((item) => (
            <div key={item.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-semibold text-slate-500">{item.label}</p>
              <p className="mt-2 text-3xl font-black text-slate-950">{item.value}</p>
              <p className="mt-2 text-sm text-slate-600">{item.description}</p>
              <span className={cn('mt-3 inline-flex rounded-full px-2.5 py-1 text-xs font-bold', toneClasses[item.tone])}>
                Performance metric
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
```

---

## `src/features/contractors/components/ContractorDocuments.tsx`

```tsx
import { FileText } from 'lucide-react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { EmptyState } from '@/components/ui/EmptyState';
import type { ContractorDocument } from '@/types/contractor.types';
import { formatDate } from '@/utils/date';

export function ContractorDocuments({ documents = [] }: { documents?: ContractorDocument[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Contractor Documents</CardTitle>
        <CardDescription>License, tax certificate, registration, and related documents.</CardDescription>
      </CardHeader>
      <CardContent>
        {documents.length === 0 ? (
          <EmptyState title="No contractor documents" description="Uploaded contractor documents will appear here." />
        ) : (
          <div className="space-y-3">
            {documents.map((document) => (
              <a
                key={document.id}
                href={document.fileUrl}
                className="flex items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-4 hover:bg-slate-100"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-700">
                    <FileText className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-bold text-slate-950">{document.title}</p>
                    <p className="text-xs text-slate-500">{document.fileName}</p>
                  </div>
                </div>
                <span className="text-xs font-semibold text-slate-500">{formatDate(document.createdAt)}</span>
              </a>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

---

# 8. Contractor Pages

## `src/features/contractors/pages/ContractorsListPage.tsx`

```tsx
import { useState } from 'react';
import { Link } from 'react-router-dom';

import { SearchInput } from '@/components/forms/SearchInput';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { Select } from '@/components/ui/Select';

import { ContractorTable } from '../components/ContractorTable';
import { useContractors } from '../hooks/useContractors';

export function ContractorsListPage() {
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');

  const { data, isLoading, error } = useContractors({ search, status, page: 1, perPage: 10 });
  const contractors = data?.items || [];

  return (
    <PageContainer>
      <PageHeader
        title="Contractors"
        description="Register, verify, monitor, and manage official contractor profiles."
        actions={
          <Link to="/contractors/new">
            <Button>Register Contractor</Button>
          </Link>
        }
      />

      <div className="mb-5 grid gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-2">
        <SearchInput
          placeholder="Search company, registration, email..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />

        <Select value={status} onChange={(event) => setStatus(event.target.value)}>
          <option value="">All statuses</option>
          <option value="ACTIVE">Active</option>
          <option value="PENDING_VERIFICATION">Pending Verification</option>
          <option value="SUSPENDED">Suspended</option>
          <option value="BLACKLISTED">Blacklisted</option>
        </Select>
      </div>

      {isLoading && <LoadingSpinner label="Loading contractors..." />}
      {error && <p className="text-sm font-semibold text-red-600">Unable to load contractors.</p>}
      {!isLoading && !error && <ContractorTable contractors={contractors} />}
    </PageContainer>
  );
}
```

---

## `src/features/contractors/pages/CreateContractorPage.tsx`

```tsx
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';

import { ContractorForm } from '../components/ContractorForm';
import { useCreateContractor } from '../hooks/useCreateContractor';

export function CreateContractorPage() {
  const createContractor = useCreateContractor();

  return (
    <PageContainer>
      <PageHeader
        title="Register Contractor"
        description="Create an official contractor profile for project assignment and compliance tracking."
      />

      <ContractorForm
        isSubmitting={createContractor.isPending}
        onSubmit={(payload) => createContractor.mutate(payload)}
      />
    </PageContainer>
  );
}
```

---

## `src/features/contractors/pages/EditContractorPage.tsx`

```tsx
import { useParams } from 'react-router-dom';

import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

import { ContractorForm } from '../components/ContractorForm';
import { useContractorDetails } from '../hooks/useContractorDetails';
import { useUpdateContractor } from '../hooks/useUpdateContractor';

export function EditContractorPage() {
  const { contractorId } = useParams();
  const { data: contractor, isLoading } = useContractorDetails(contractorId);
  const updateContractor = useUpdateContractor(contractorId as string);

  return (
    <PageContainer>
      <PageHeader
        title="Edit Contractor"
        description="Update contractor profile, contact, license, and compliance information."
      />

      {isLoading && <LoadingSpinner label="Loading contractor..." />}

      {contractor && (
        <ContractorForm
          defaultValues={contractor}
          isSubmitting={updateContractor.isPending}
          onSubmit={(payload) => updateContractor.mutate(payload)}
        />
      )}
    </PageContainer>
  );
}
```

---

## `src/features/contractors/pages/ContractorDetailsPage.tsx`

```tsx
import { Link, useParams } from 'react-router-dom';

import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { formatCurrency } from '@/utils/currency';

import { ContractorDocuments } from '../components/ContractorDocuments';
import { ContractorPerformance } from '../components/ContractorPerformance';
import { ContractorProjects } from '../components/ContractorProjects';
import { ContractorStatusBadge } from '../components/ContractorStatusBadge';
import { useContractorDetails } from '../hooks/useContractorDetails';

function complianceVariant(status: string) {
  if (status === 'COMPLIANT') return 'success';
  if (status === 'MINOR_ISSUES') return 'warning';
  return 'danger';
}

export function ContractorDetailsPage() {
  const { contractorId } = useParams();
  const { data: contractor, isLoading, error } = useContractorDetails(contractorId);

  if (isLoading) {
    return (
      <PageContainer>
        <LoadingSpinner label="Loading contractor details..." />
      </PageContainer>
    );
  }

  if (error || !contractor) {
    return (
      <PageContainer>
        <p className="text-sm font-semibold text-red-600">Contractor could not be loaded.</p>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <PageHeader
        title={contractor.companyName}
        description={`${contractor.registrationNumber} • ${contractor.contactEmail}`}
        actions={
          <Link to={`/contractors/${contractor.id}/edit`}>
            <Button>Edit Contractor</Button>
          </Link>
        }
      />

      <div className="mb-6 grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card>
          <CardHeader>
            <CardTitle>Contractor Profile</CardTitle>
            <CardDescription>Official contractor identity and contact information.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">Status</p>
                <div className="mt-2"><ContractorStatusBadge status={contractor.status} /></div>
              </div>
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">Compliance</p>
                <div className="mt-2"><Badge variant={complianceVariant(contractor.complianceStatus)}>{contractor.complianceStatus}</Badge></div>
              </div>
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">TIN</p>
                <p className="mt-2 font-bold text-slate-950">{contractor.taxIdentificationNumber || 'N/A'}</p>
              </div>
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">License</p>
                <p className="mt-2 font-bold text-slate-950">{contractor.licenseNumber || 'N/A'}</p>
              </div>
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">Contact Person</p>
                <p className="mt-2 font-bold text-slate-950">{contractor.contactPersonName}</p>
              </div>
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">Phone</p>
                <p className="mt-2 font-bold text-slate-950">{contractor.contactPhone}</p>
              </div>
            </div>

            <div className="mt-6">
              <ProgressBar value={contractor.complianceScore} label="Compliance Score" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Contract Summary</CardTitle>
            <CardDescription>Project participation and contract value.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm font-semibold text-slate-500">Active Projects</p>
                <p className="mt-2 text-3xl font-black text-slate-950">{contractor.activeProjectsCount}</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm font-semibold text-slate-500">Completed</p>
                <p className="mt-2 text-3xl font-black text-slate-950">{contractor.completedProjectsCount}</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm font-semibold text-slate-500">Delayed</p>
                <p className="mt-2 text-3xl font-black text-slate-950">{contractor.delayedProjectsCount}</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-4">
                <p className="text-sm font-semibold text-slate-500">Contract Value</p>
                <p className="mt-2 text-lg font-black text-slate-950">{formatCurrency(contractor.totalContractValue)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mb-6">
        <ContractorPerformance performance={contractor.performance} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <ContractorProjects projects={contractor.projects} />
        <ContractorDocuments documents={contractor.documents} />
      </div>
    </PageContainer>
  );
}
```

---

# 9. Update Routes Configuration

## `src/config/routes.ts`

Inside `PRIVATE_ROUTES`, add:

```ts
CONTRACTOR_NEW: '/contractors/new',
CONTRACTOR_EDIT: '/contractors/:contractorId/edit',
```

Your contractor route section should become:

```ts
CONTRACTORS: '/contractors',
CONTRACTOR_NEW: '/contractors/new',
CONTRACTOR_DETAILS: '/contractors/:contractorId',
CONTRACTOR_EDIT: '/contractors/:contractorId/edit',
```

Then add route metadata to `appRoutes`:

```ts
{
  path: PRIVATE_ROUTES.CONTRACTOR_NEW,
  label: 'Register Contractor',
  permission: PERMISSIONS.MANAGE_CONTRACTORS,
},
{
  path: PRIVATE_ROUTES.CONTRACTOR_EDIT,
  label: 'Edit Contractor',
  permission: PERMISSIONS.MANAGE_CONTRACTORS,
},
```

Also update `getRouteLabel` if needed:

```ts
if (pathname.startsWith('/contractors/') && pathname.endsWith('/edit')) return 'Edit Contractor';
if (pathname.startsWith('/contractors/')) return 'Contractor Details';
```

---

# 10. Update Router to Use Contractor Pages

## `src/app/router.tsx`

Add these imports near the top:

```tsx
import { ContractorDetailsPage } from '@/features/contractors/pages/ContractorDetailsPage';
import { ContractorsListPage } from '@/features/contractors/pages/ContractorsListPage';
import { CreateContractorPage } from '@/features/contractors/pages/CreateContractorPage';
import { EditContractorPage } from '@/features/contractors/pages/EditContractorPage';
```

Replace the existing contractor placeholder route with these routes:

```tsx
{
  path: PRIVATE_ROUTES.CONTRACTORS,
  element: (
    <RoleGuard permission={PERMISSIONS.VIEW_CONTRACTORS}>
      <ContractorsListPage />
    </RoleGuard>
  ),
},
{
  path: PRIVATE_ROUTES.CONTRACTOR_NEW,
  element: (
    <RoleGuard permission={PERMISSIONS.MANAGE_CONTRACTORS}>
      <CreateContractorPage />
    </RoleGuard>
  ),
},
{
  path: PRIVATE_ROUTES.CONTRACTOR_DETAILS,
  element: (
    <RoleGuard permission={PERMISSIONS.VIEW_CONTRACTORS}>
      <ContractorDetailsPage />
    </RoleGuard>
  ),
},
{
  path: PRIVATE_ROUTES.CONTRACTOR_EDIT,
  element: (
    <RoleGuard permission={PERMISSIONS.MANAGE_CONTRACTORS}>
      <EditContractorPage />
    </RoleGuard>
  ),
},
```

Keep the rest of the router unchanged.

---

# 11. Build Test

Run:

```bash
npm run build
```

Expected:

```txt
✓ built
```

---

# 12. Browser Test

Run:

```bash
npm run dev
```

Open and test:

```txt
/contractors
/contractors/new
/contractors/CON-001
/contractors/CON-001/edit
```

Expected behavior:

- `/contractors` shows contractor filters and contractor table.
- Search filters contractors by company, registration number, TIN, license, contact, or email.
- Status filter works.
- View button opens contractor details.
- Edit button opens contractor edit form.
- Register contractor form submits and returns to `/contractors`.
- Contractor details show profile, compliance, projects, performance, and documents.

---

# 13. Phase 8 Completion Checklist

Phase 8 is complete when:

- `ContractorsListPage.tsx` renders contractor list.
- `CreateContractorPage.tsx` renders contractor form.
- `EditContractorPage.tsx` loads contractor and renders form.
- `ContractorDetailsPage.tsx` renders contractor profile and workflow sections.
- `ContractorTable.tsx` opens details and edit pages.
- `ContractorStatusBadge.tsx` displays contractor status.
- `ContractorProjects.tsx` displays assigned projects.
- `ContractorPerformance.tsx` displays performance history.
- `ContractorDocuments.tsx` displays contractor documents.
- `contractors.service.ts` supports mock data and live API readiness.
- Router uses real contractor pages instead of placeholders.
- `npm run build` passes.

---

# Phase 8 Expected Output

After this phase:

- Contractors can be managed as official entities.
- Contractor profiles can be opened.
- Contractors can be registered and edited.
- Contractor compliance status is visible.
- Contractor performance history is visible.
- Assigned projects are visible.
- Contractor data is ready for project assignment, evidence, approvals, funds, and audits.

---

# Next Phase

After Phase 8 passes build and browser testing, proceed to:

```txt
Phase 9: Evidence and Receipt Management Module
```
