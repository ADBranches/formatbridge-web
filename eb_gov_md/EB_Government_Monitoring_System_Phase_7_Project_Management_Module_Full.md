# Phase 7 — Project Management Module

**Project:** EB Government Monitoring System  
**Frontend:** React + TypeScript + Vite + Tailwind CSS v4  
**Phase Goal:** Implement a complete MVP-ready Project Management module with project listing, search/filtering, project creation, editing, details, milestones, documents, timeline, and mock/live API readiness.

---

## Phase 6 Confirmation

Phase 6 is complete if your dashboard build passed successfully and the dashboard renders with KPI cards, charts, activities, and risk flags.

Your previous build showed:

```txt
✓ 2545 modules transformed.
✓ built in 3.13s
```

The bundle-size warning is not a blocker for Phase 7. It can be handled later through route-level code splitting.

---

# Phase 7 Objectives

This phase implements:

- Government admin project listing.
- Project search, filtering, and sorting.
- Project creation screen.
- Project editing screen.
- Project details screen.
- Project summary cards.
- Project milestones.
- Project documents.
- Project timeline.
- Status visibility and status badges.
- Mock project data support until the backend API is ready.
- Router integration for `/projects`, `/projects/new`, `/projects/:projectId`, and `/projects/:projectId/edit`.

---

# 1. Create Phase 7 Directories

Run from the project root:

```bash
mkdir -p src/features/projects/components src/features/projects/pages src/features/projects/hooks src/features/projects/schemas src/features/projects/utils
```

---

# 2. Create Phase 7 Files

Run from the project root:

```bash
touch src/features/projects/pages/ProjectsListPage.tsx \
src/features/projects/pages/CreateProjectPage.tsx \
src/features/projects/pages/EditProjectPage.tsx \
src/features/projects/pages/ProjectDetailsPage.tsx \
src/features/projects/components/ProjectForm.tsx \
src/features/projects/components/ProjectFilters.tsx \
src/features/projects/components/ProjectTable.tsx \
src/features/projects/components/ProjectSummaryCards.tsx \
src/features/projects/components/ProjectMilestones.tsx \
src/features/projects/components/ProjectDocuments.tsx \
src/features/projects/components/ProjectTimeline.tsx \
src/features/projects/components/ProjectStatusBadge.tsx \
src/features/projects/hooks/useProjects.ts \
src/features/projects/hooks/useProjectDetails.ts \
src/features/projects/hooks/useCreateProject.ts \
src/features/projects/hooks/useUpdateProject.ts \
src/features/projects/schemas/project.schema.ts \
src/features/projects/utils/projectStatus.ts
```

The following existing files will also be updated:

```txt
src/types/project.types.ts
src/services/projects.service.ts
src/app/router.tsx
```

---

# 3. Update Project Types

## `src/types/project.types.ts`

Replace the file content with this:

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

export type ProjectDocument = AuditMetadata & {
  id: ID;
  projectId: ID;
  title: string;
  type: 'CONTRACT' | 'BOQ' | 'PROCUREMENT' | 'REPORT' | 'CERTIFICATE' | 'OTHER';
  fileName: string;
  fileUrl: string;
  uploadedBy: ID;
};

export type ProjectTimelineItem = {
  id: ID;
  title: string;
  description: string;
  date: string;
  type: 'CREATED' | 'UPDATED' | 'EVIDENCE' | 'REVIEW' | 'APPROVAL' | 'FUNDS' | 'AUDIT';
};

export type Project = AuditMetadata & {
  id: ID;
  projectCode: string;
  title: string;
  description: string;
  category: ProjectCategory;
  ministryId: ID;
  ministryName?: string;
  districtId: ID;
  districtName?: string;
  contractorId?: ID;
  contractorName?: string;
  monitoringOfficerId?: ID;
  monitoringOfficerName?: string;
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
  documents?: ProjectDocument[];
  timeline?: ProjectTimelineItem[];
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

# 4. Project Status Utility

## `src/features/projects/utils/projectStatus.ts`

```ts
import type { ProjectRiskLevel, ProjectStatus } from '@/types/project.types';

export function getProjectStatusLabel(status: ProjectStatus): string {
  const labels: Record<ProjectStatus, string> = {
    DRAFT: 'Draft',
    NOT_STARTED: 'Not Started',
    IN_PROGRESS: 'In Progress',
    UNDER_REVIEW: 'Under Review',
    DELAYED: 'Delayed',
    COMPLETED: 'Completed',
    SUSPENDED: 'Suspended',
    CANCELLED: 'Cancelled',
  };

  return labels[status];
}

export function getProjectStatusVariant(status: ProjectStatus) {
  if (status === 'COMPLETED') return 'success';
  if (status === 'DELAYED' || status === 'SUSPENDED' || status === 'CANCELLED') return 'danger';
  if (status === 'UNDER_REVIEW') return 'warning';
  if (status === 'IN_PROGRESS') return 'info';
  return 'default';
}

export function getRiskVariant(riskLevel: ProjectRiskLevel) {
  if (riskLevel === 'CRITICAL' || riskLevel === 'HIGH') return 'danger';
  if (riskLevel === 'MEDIUM') return 'warning';
  return 'success';
}
```

---

# 5. Project Schema

## `src/features/projects/schemas/project.schema.ts`

```ts
import { z } from 'zod';

const projectCategories = [
  'ROADS',
  'SCHOOLS',
  'HEALTH',
  'WATER',
  'ENERGY',
  'AGRICULTURE',
  'ICT',
  'HOUSING',
  'OTHER',
] as const;

export const projectSchema = z.object({
  title: z.string().trim().min(3, 'Project title must be at least 3 characters.'),
  description: z.string().trim().min(10, 'Project description must be at least 10 characters.'),
  category: z.enum(projectCategories, { message: 'Select a valid project category.' }),
  ministryId: z.string().trim().min(1, 'Ministry is required.'),
  districtId: z.string().trim().min(1, 'District is required.'),
  contractorId: z.string().optional(),
  monitoringOfficerId: z.string().optional(),
  budgetAmount: z.coerce.number().positive('Budget amount must be greater than zero.'),
  startDate: z.string().trim().min(1, 'Start date is required.'),
  endDate: z.string().trim().min(1, 'End date is required.'),
});

export type ProjectFormValues = z.infer<typeof projectSchema>;
```

---

# 6. Update Projects Service With Mock Data

## `src/services/projects.service.ts`

Replace the file content with this:

```ts
import { API_ENDPOINTS, buildQueryString, withId } from '@/lib/api';
import { apiDelete, apiGet, apiPost, apiPut } from '@/lib/http';
import type { ApiResponse, ID, ListQueryParams, PaginatedResponse } from '@/types/common.types';
import type { CreateProjectPayload, Project, UpdateProjectPayload } from '@/types/project.types';

const useMockApi = import.meta.env.VITE_USE_MOCK_API === 'true';

const now = new Date().toISOString();

const mockProjects: Project[] = [
  {
    id: 'PRJ-001',
    projectCode: 'EB/2026/001',
    title: 'Wakiso Health Center Construction',
    description: 'Construction of a community health center with maternity wing and outpatient department.',
    category: 'HEALTH',
    ministryId: 'MIN-HEALTH',
    ministryName: 'Ministry of Health',
    districtId: 'DIST-WAKISO',
    districtName: 'Wakiso',
    contractorId: 'CON-001',
    contractorName: 'Prime Build Contractors Ltd',
    monitoringOfficerId: 'USR-ME-001',
    monitoringOfficerName: 'M&E Officer Demo',
    budgetAmount: 4800000000,
    fundsReleased: 2600000000,
    fundsUtilized: 2100000000,
    startDate: '2026-01-15',
    endDate: '2026-12-15',
    status: 'IN_PROGRESS',
    riskLevel: 'MEDIUM',
    progressPercentage: 58,
    createdAt: now,
    updatedAt: now,
    milestones: [
      {
        id: 'MIL-001',
        projectId: 'PRJ-001',
        title: 'Foundation and substructure',
        description: 'Foundation excavation, concrete works, and substructure completion.',
        plannedStartDate: '2026-01-15',
        plannedEndDate: '2026-03-30',
        actualCompletionDate: '2026-04-05',
        budgetAmount: 900000000,
        progressPercentage: 100,
        status: 'COMPLETED',
        createdAt: now,
        updatedAt: now,
      },
      {
        id: 'MIL-002',
        projectId: 'PRJ-001',
        title: 'Walling and roofing',
        description: 'Superstructure walling, roofing frame, and roof covering.',
        plannedStartDate: '2026-04-01',
        plannedEndDate: '2026-07-30',
        budgetAmount: 1600000000,
        progressPercentage: 62,
        status: 'IN_PROGRESS',
        createdAt: now,
        updatedAt: now,
      },
    ],
    documents: [
      {
        id: 'DOC-001',
        projectId: 'PRJ-001',
        title: 'Signed Contract Agreement',
        type: 'CONTRACT',
        fileName: 'wakiso-health-center-contract.pdf',
        fileUrl: '#',
        uploadedBy: 'USR-ADMIN-001',
        createdAt: now,
        updatedAt: now,
      },
    ],
    timeline: [
      {
        id: 'TML-001',
        title: 'Project created',
        description: 'Project was created and assigned to contractor.',
        date: '2026-01-10',
        type: 'CREATED',
      },
      {
        id: 'TML-002',
        title: 'Evidence submitted',
        description: 'Contractor submitted foundation completion evidence.',
        date: '2026-04-06',
        type: 'EVIDENCE',
      },
    ],
  },
  {
    id: 'PRJ-002',
    projectCode: 'EB/2026/002',
    title: 'Arua Rural Road Maintenance',
    description: 'Maintenance and grading of rural road network connecting farming communities.',
    category: 'ROADS',
    ministryId: 'MIN-WORKS',
    ministryName: 'Ministry of Works and Transport',
    districtId: 'DIST-ARUA',
    districtName: 'Arua',
    contractorId: 'CON-002',
    contractorName: 'North Roads Engineering Ltd',
    monitoringOfficerId: 'USR-ME-002',
    monitoringOfficerName: 'Roads M&E Officer',
    budgetAmount: 7200000000,
    fundsReleased: 5200000000,
    fundsUtilized: 5000000000,
    startDate: '2026-02-01',
    endDate: '2026-11-30',
    status: 'DELAYED',
    riskLevel: 'HIGH',
    progressPercentage: 44,
    createdAt: now,
    updatedAt: now,
    milestones: [],
    documents: [],
    timeline: [],
  },
  {
    id: 'PRJ-003',
    projectCode: 'EB/2026/003',
    title: 'Moroto Water Supply Upgrade',
    description: 'Upgrade of water supply infrastructure and borehole distribution network.',
    category: 'WATER',
    ministryId: 'MIN-WATER',
    ministryName: 'Ministry of Water and Environment',
    districtId: 'DIST-MOROTO',
    districtName: 'Moroto',
    contractorId: 'CON-003',
    contractorName: 'Aqua Infrastructure Uganda',
    budgetAmount: 5900000000,
    fundsReleased: 4500000000,
    fundsUtilized: 4300000000,
    startDate: '2026-03-01',
    endDate: '2026-10-20',
    status: 'UNDER_REVIEW',
    riskLevel: 'CRITICAL',
    progressPercentage: 28,
    createdAt: now,
    updatedAt: now,
    milestones: [],
    documents: [],
    timeline: [],
  },
];

function filterProjects(params?: ListQueryParams): Project[] {
  let result = [...mockProjects];

  if (params?.search) {
    const search = params.search.toLowerCase();
    result = result.filter((project) =>
      [project.title, project.projectCode, project.districtName, project.contractorName]
        .filter(Boolean)
        .some((value) => String(value).toLowerCase().includes(search))
    );
  }

  if (params?.status) {
    result = result.filter((project) => project.status === params.status);
  }

  if (params?.district) {
    result = result.filter((project) => project.districtName === params.district);
  }

  if (params?.ministry) {
    result = result.filter((project) => project.ministryName === params.ministry);
  }

  return result;
}

function paginateProjects(projects: Project[], params?: ListQueryParams): PaginatedResponse<Project> {
  const page = params?.page || 1;
  const perPage = params?.perPage || 10;
  const start = (page - 1) * perPage;
  const items = projects.slice(start, start + perPage);

  return {
    items,
    meta: {
      page,
      perPage,
      totalItems: projects.length,
      totalPages: Math.max(1, Math.ceil(projects.length / perPage)),
    },
  };
}

export const projectsService = {
  async list(params?: ListQueryParams): Promise<PaginatedResponse<Project>> {
    if (useMockApi) {
      return paginateProjects(filterProjects(params), params);
    }

    const response = await apiGet<ApiResponse<PaginatedResponse<Project>>>(
      `${API_ENDPOINTS.projects}${buildQueryString(params)}`
    );
    return response.data;
  },

  async getById(projectId: ID): Promise<Project> {
    if (useMockApi) {
      const project = mockProjects.find((item) => item.id === projectId);
      if (!project) throw new Error('Project not found.');
      return project;
    }

    const response = await apiGet<ApiResponse<Project>>(withId(API_ENDPOINTS.projects, projectId));
    return response.data;
  },

  async create(payload: CreateProjectPayload): Promise<Project> {
    if (useMockApi) {
      return {
        id: `PRJ-${Date.now()}`,
        projectCode: `EB/2026/${mockProjects.length + 1}`,
        title: payload.title,
        description: payload.description,
        category: payload.category,
        ministryId: payload.ministryId,
        districtId: payload.districtId,
        contractorId: payload.contractorId,
        monitoringOfficerId: payload.monitoringOfficerId,
        approvalAuthorityId: payload.approvalAuthorityId,
        auditorId: payload.auditorId,
        budgetAmount: payload.budgetAmount,
        fundsReleased: 0,
        fundsUtilized: 0,
        startDate: payload.startDate,
        endDate: payload.endDate,
        status: 'DRAFT',
        riskLevel: 'LOW',
        progressPercentage: 0,
        latitude: payload.latitude,
        longitude: payload.longitude,
        milestones: [],
        documents: [],
        timeline: [],
        createdAt: now,
        updatedAt: now,
      };
    }

    const response = await apiPost<ApiResponse<Project>, CreateProjectPayload>(
      API_ENDPOINTS.projects,
      payload
    );
    return response.data;
  },

  async update(projectId: ID, payload: UpdateProjectPayload): Promise<Project> {
    if (useMockApi) {
      const project = mockProjects.find((item) => item.id === projectId);
      if (!project) throw new Error('Project not found.');
      return { ...project, ...payload, updatedAt: new Date().toISOString() };
    }

    const response = await apiPut<ApiResponse<Project>, UpdateProjectPayload>(
      withId(API_ENDPOINTS.projects, projectId),
      payload
    );
    return response.data;
  },

  async remove(projectId: ID): Promise<ApiResponse<null>> {
    if (useMockApi) {
      return { success: true, message: `Project ${projectId} archived.`, data: null };
    }

    return apiDelete<ApiResponse<null>>(withId(API_ENDPOINTS.projects, projectId));
  },
};
```

---

# 7. Project Hooks

## `src/features/projects/hooks/useProjects.ts`

```ts
import { useQuery } from '@tanstack/react-query';

import { projectsService } from '@/services/projects.service';
import type { ListQueryParams } from '@/types/common.types';

export function useProjects(params?: ListQueryParams) {
  return useQuery({
    queryKey: ['projects', params],
    queryFn: () => projectsService.list(params),
  });
}
```

---

## `src/features/projects/hooks/useProjectDetails.ts`

```ts
import { useQuery } from '@tanstack/react-query';

import { projectsService } from '@/services/projects.service';

export function useProjectDetails(projectId?: string) {
  return useQuery({
    queryKey: ['project', projectId],
    queryFn: () => projectsService.getById(projectId as string),
    enabled: Boolean(projectId),
  });
}
```

---

## `src/features/projects/hooks/useCreateProject.ts`

```ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

import { projectsService } from '@/services/projects.service';
import type { CreateProjectPayload } from '@/types/project.types';

export function useCreateProject() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateProjectPayload) => projectsService.create(payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['projects'] });
      navigate('/projects');
    },
  });
}
```

---

## `src/features/projects/hooks/useUpdateProject.ts`

```ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

import { projectsService } from '@/services/projects.service';
import type { UpdateProjectPayload } from '@/types/project.types';

export function useUpdateProject(projectId: string) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UpdateProjectPayload) => projectsService.update(projectId, payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['projects'] });
      await queryClient.invalidateQueries({ queryKey: ['project', projectId] });
      navigate(`/projects/${projectId}`);
    },
  });
}
```

---

# 8. Project Components

## `src/features/projects/components/ProjectStatusBadge.tsx`

```tsx
import { Badge } from '@/components/ui/Badge';
import type { ProjectStatus } from '@/types/project.types';

import { getProjectStatusLabel, getProjectStatusVariant } from '../utils/projectStatus';

type ProjectStatusBadgeProps = {
  status: ProjectStatus;
};

export function ProjectStatusBadge({ status }: ProjectStatusBadgeProps) {
  return <Badge variant={getProjectStatusVariant(status)}>{getProjectStatusLabel(status)}</Badge>;
}
```

---

## `src/features/projects/components/ProjectFilters.tsx`

```tsx
import { SearchInput } from '@/components/forms/SearchInput';
import { Select } from '@/components/ui/Select';
import type { ProjectStatus } from '@/types/project.types';

export type ProjectFilterState = {
  search: string;
  status: string;
  district: string;
  ministry: string;
};

type ProjectFiltersProps = {
  filters: ProjectFilterState;
  onChange: (filters: ProjectFilterState) => void;
};

export function ProjectFilters({ filters, onChange }: ProjectFiltersProps) {
  function updateFilter(key: keyof ProjectFilterState, value: string) {
    onChange({ ...filters, [key]: value });
  }

  return (
    <div className="mb-5 grid gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-2 xl:grid-cols-4">
      <SearchInput
        placeholder="Search project, code, district..."
        value={filters.search}
        onChange={(event) => updateFilter('search', event.target.value)}
      />

      <Select value={filters.status} onChange={(event) => updateFilter('status', event.target.value as ProjectStatus)}>
        <option value="">All statuses</option>
        <option value="DRAFT">Draft</option>
        <option value="NOT_STARTED">Not Started</option>
        <option value="IN_PROGRESS">In Progress</option>
        <option value="UNDER_REVIEW">Under Review</option>
        <option value="DELAYED">Delayed</option>
        <option value="COMPLETED">Completed</option>
        <option value="SUSPENDED">Suspended</option>
        <option value="CANCELLED">Cancelled</option>
      </Select>

      <Select value={filters.district} onChange={(event) => updateFilter('district', event.target.value)}>
        <option value="">All districts</option>
        <option value="Wakiso">Wakiso</option>
        <option value="Arua">Arua</option>
        <option value="Moroto">Moroto</option>
      </Select>

      <Select value={filters.ministry} onChange={(event) => updateFilter('ministry', event.target.value)}>
        <option value="">All ministries</option>
        <option value="Ministry of Health">Ministry of Health</option>
        <option value="Ministry of Works and Transport">Ministry of Works and Transport</option>
        <option value="Ministry of Water and Environment">Ministry of Water and Environment</option>
      </Select>
    </div>
  );
}
```

---

## `src/features/projects/components/ProjectTable.tsx`

```tsx
import { Link } from 'react-router-dom';
import { Eye, Pencil } from 'lucide-react';

import { Button } from '@/components/ui/Button';
import { EmptyState } from '@/components/ui/EmptyState';
import { ProgressBar } from '@/components/ui/ProgressBar';
import type { Project } from '@/types/project.types';
import { formatCurrency } from '@/utils/currency';
import { formatDate } from '@/utils/date';

import { ProjectStatusBadge } from './ProjectStatusBadge';

type ProjectTableProps = {
  projects: Project[];
};

export function ProjectTable({ projects }: ProjectTableProps) {
  if (projects.length === 0) {
    return (
      <EmptyState
        title="No projects found"
        description="Try changing your search or filter criteria."
      />
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Project</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">District</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Budget</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Progress</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">Status</th>
              <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-500">End Date</th>
              <th className="px-4 py-3 text-right text-xs font-bold uppercase tracking-wide text-slate-500">Actions</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100 bg-white">
            {projects.map((project) => (
              <tr key={project.id} className="hover:bg-slate-50">
                <td className="px-4 py-4">
                  <div>
                    <p className="font-bold text-slate-950">{project.title}</p>
                    <p className="text-xs text-slate-500">{project.projectCode}</p>
                  </div>
                </td>
                <td className="px-4 py-4 text-sm text-slate-600">{project.districtName || project.districtId}</td>
                <td className="px-4 py-4 text-sm font-semibold text-slate-700">{formatCurrency(project.budgetAmount)}</td>
                <td className="px-4 py-4 min-w-44">
                  <ProgressBar value={project.progressPercentage} showValue />
                </td>
                <td className="px-4 py-4"><ProjectStatusBadge status={project.status} /></td>
                <td className="px-4 py-4 text-sm text-slate-600">{formatDate(project.endDate)}</td>
                <td className="px-4 py-4">
                  <div className="flex justify-end gap-2">
                    <Link to={`/projects/${project.id}`}>
                      <Button variant="ghost" size="sm"><Eye className="h-4 w-4" /></Button>
                    </Link>
                    <Link to={`/projects/${project.id}/edit`}>
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

## `src/features/projects/components/ProjectSummaryCards.tsx`

```tsx
import { AlertTriangle, CheckCircle2, Clock, FolderKanban } from 'lucide-react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import type { Project } from '@/types/project.types';
import { formatCurrency } from '@/utils/currency';

export function ProjectSummaryCards({ projects }: { projects: Project[] }) {
  const totalBudget = projects.reduce((sum, project) => sum + project.budgetAmount, 0);
  const activeProjects = projects.filter((project) => project.status === 'IN_PROGRESS').length;
  const completedProjects = projects.filter((project) => project.status === 'COMPLETED').length;
  const delayedProjects = projects.filter((project) => project.status === 'DELAYED').length;

  const cards = [
    { label: 'Total Projects', value: projects.length, description: 'Projects in current list', icon: FolderKanban },
    { label: 'Active Projects', value: activeProjects, description: 'Currently in progress', icon: Clock },
    { label: 'Completed', value: completedProjects, description: 'Completed projects', icon: CheckCircle2 },
    { label: 'Delayed', value: delayedProjects, description: `Budget: ${formatCurrency(totalBudget)}`, icon: AlertTriangle },
  ];

  return (
    <div className="mb-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <Card key={card.label}>
            <CardHeader>
              <div className="flex items-center justify-between gap-3">
                <div>
                  <CardDescription>{card.label}</CardDescription>
                  <CardTitle className="mt-2 text-3xl font-black">{card.value}</CardTitle>
                </div>
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#051931]/10 text-[#051931]">
                  <Icon className="h-5 w-5" />
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-slate-500">{card.description}</p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
```

---

## `src/features/projects/components/ProjectMilestones.tsx`

```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { EmptyState } from '@/components/ui/EmptyState';
import { ProgressBar } from '@/components/ui/ProgressBar';
import type { ProjectMilestone } from '@/types/project.types';
import { formatCurrency } from '@/utils/currency';
import { formatDate } from '@/utils/date';

import { ProjectStatusBadge } from './ProjectStatusBadge';

export function ProjectMilestones({ milestones = [] }: { milestones?: ProjectMilestone[] }) {
  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle>Milestones</CardTitle>
          <CardDescription>Planned phases, budgets, deadlines, and progress.</CardDescription>
        </div>
      </CardHeader>
      <CardContent>
        {milestones.length === 0 ? (
          <EmptyState title="No milestones recorded" description="Milestones will appear here once added." />
        ) : (
          <div className="space-y-4">
            {milestones.map((milestone) => (
              <article key={milestone.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <div className="flex flex-col justify-between gap-3 md:flex-row md:items-start">
                  <div>
                    <h3 className="font-bold text-slate-950">{milestone.title}</h3>
                    <p className="mt-1 text-sm text-slate-600">{milestone.description}</p>
                    <p className="mt-2 text-xs text-slate-500">
                      {formatDate(milestone.plannedStartDate)} — {formatDate(milestone.plannedEndDate)}
                    </p>
                  </div>
                  <ProjectStatusBadge status={milestone.status} />
                </div>

                <div className="mt-4 grid gap-4 md:grid-cols-[1fr_12rem] md:items-center">
                  <ProgressBar value={milestone.progressPercentage} label="Progress" />
                  <p className="text-sm font-bold text-slate-700">{formatCurrency(milestone.budgetAmount)}</p>
                </div>
              </article>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

---

## `src/features/projects/components/ProjectDocuments.tsx`

```tsx
import { FileText } from 'lucide-react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { EmptyState } from '@/components/ui/EmptyState';
import type { ProjectDocument } from '@/types/project.types';
import { formatDate } from '@/utils/date';

export function ProjectDocuments({ documents = [] }: { documents?: ProjectDocument[] }) {
  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle>Project Documents</CardTitle>
          <CardDescription>Contracts, BOQs, reports, and certificates.</CardDescription>
        </div>
      </CardHeader>
      <CardContent>
        {documents.length === 0 ? (
          <EmptyState title="No documents uploaded" description="Project documents will appear here." />
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

## `src/features/projects/components/ProjectTimeline.tsx`

```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { EmptyState } from '@/components/ui/EmptyState';
import type { ProjectTimelineItem } from '@/types/project.types';
import { formatDate } from '@/utils/date';

export function ProjectTimeline({ timeline = [] }: { timeline?: ProjectTimelineItem[] }) {
  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle>Project Timeline</CardTitle>
          <CardDescription>Important project events and workflow actions.</CardDescription>
        </div>
      </CardHeader>
      <CardContent>
        {timeline.length === 0 ? (
          <EmptyState title="No timeline events" description="Workflow events will appear here." />
        ) : (
          <div className="space-y-4">
            {timeline.map((item) => (
              <div key={item.id} className="relative border-l-2 border-slate-200 pl-5">
                <span className="absolute -left-[7px] top-1 h-3 w-3 rounded-full bg-[#009659]" />
                <p className="text-sm font-bold text-slate-950">{item.title}</p>
                <p className="mt-1 text-sm text-slate-600">{item.description}</p>
                <p className="mt-1 text-xs font-semibold text-slate-400">{formatDate(item.date)}</p>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

---

## `src/features/projects/components/ProjectForm.tsx`

```tsx
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

import { FormField } from '@/components/forms/FormField';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Textarea } from '@/components/ui/Textarea';
import type { CreateProjectPayload, Project } from '@/types/project.types';

import { projectSchema, type ProjectFormValues } from '../schemas/project.schema';

type ProjectFormProps = {
  defaultValues?: Project;
  isSubmitting?: boolean;
  onSubmit: (payload: CreateProjectPayload) => void;
};

export function ProjectForm({ defaultValues, isSubmitting, onSubmit }: ProjectFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProjectFormValues>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      title: defaultValues?.title || '',
      description: defaultValues?.description || '',
      category: defaultValues?.category || 'HEALTH',
      ministryId: defaultValues?.ministryId || 'MIN-HEALTH',
      districtId: defaultValues?.districtId || 'DIST-WAKISO',
      contractorId: defaultValues?.contractorId || '',
      monitoringOfficerId: defaultValues?.monitoringOfficerId || '',
      budgetAmount: defaultValues?.budgetAmount || 0,
      startDate: defaultValues?.startDate || '',
      endDate: defaultValues?.endDate || '',
    },
  });

  function submit(values: ProjectFormValues) {
    onSubmit(values);
  }

  return (
    <form onSubmit={handleSubmit(submit)} className="space-y-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="grid gap-5 md:grid-cols-2">
        <FormField label="Project Title" error={errors.title?.message} required>
          <Input hasError={Boolean(errors.title)} {...register('title')} />
        </FormField>

        <FormField label="Category" error={errors.category?.message} required>
          <Select hasError={Boolean(errors.category)} {...register('category')}>
            <option value="HEALTH">Health</option>
            <option value="ROADS">Roads</option>
            <option value="SCHOOLS">Schools</option>
            <option value="WATER">Water</option>
            <option value="ENERGY">Energy</option>
            <option value="AGRICULTURE">Agriculture</option>
            <option value="ICT">ICT</option>
            <option value="HOUSING">Housing</option>
            <option value="OTHER">Other</option>
          </Select>
        </FormField>
      </div>

      <FormField label="Description" error={errors.description?.message} required>
        <Textarea hasError={Boolean(errors.description)} {...register('description')} />
      </FormField>

      <div className="grid gap-5 md:grid-cols-2">
        <FormField label="Ministry" error={errors.ministryId?.message} required>
          <Select hasError={Boolean(errors.ministryId)} {...register('ministryId')}>
            <option value="MIN-HEALTH">Ministry of Health</option>
            <option value="MIN-WORKS">Ministry of Works and Transport</option>
            <option value="MIN-WATER">Ministry of Water and Environment</option>
          </Select>
        </FormField>

        <FormField label="District" error={errors.districtId?.message} required>
          <Select hasError={Boolean(errors.districtId)} {...register('districtId')}>
            <option value="DIST-WAKISO">Wakiso</option>
            <option value="DIST-ARUA">Arua</option>
            <option value="DIST-MOROTO">Moroto</option>
          </Select>
        </FormField>
      </div>

      <div className="grid gap-5 md:grid-cols-2">
        <FormField label="Contractor ID">
          <Input placeholder="CON-001" {...register('contractorId')} />
        </FormField>

        <FormField label="Monitoring Officer ID">
          <Input placeholder="USR-ME-001" {...register('monitoringOfficerId')} />
        </FormField>
      </div>

      <div className="grid gap-5 md:grid-cols-3">
        <FormField label="Budget Amount" error={errors.budgetAmount?.message} required>
          <Input type="number" hasError={Boolean(errors.budgetAmount)} {...register('budgetAmount')} />
        </FormField>

        <FormField label="Start Date" error={errors.startDate?.message} required>
          <Input type="date" hasError={Boolean(errors.startDate)} {...register('startDate')} />
        </FormField>

        <FormField label="End Date" error={errors.endDate?.message} required>
          <Input type="date" hasError={Boolean(errors.endDate)} {...register('endDate')} />
        </FormField>
      </div>

      <div className="flex justify-end gap-3">
        <Button type="submit" isLoading={isSubmitting}>
          Save Project
        </Button>
      </div>
    </form>
  );
}
```

---

# 9. Project Pages

## `src/features/projects/pages/ProjectsListPage.tsx`

```tsx
import { useState } from 'react';
import { Link } from 'react-router-dom';

import { Button } from '@/components/ui/Button';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';

import { ProjectFilters, type ProjectFilterState } from '../components/ProjectFilters';
import { ProjectSummaryCards } from '../components/ProjectSummaryCards';
import { ProjectTable } from '../components/ProjectTable';
import { useProjects } from '../hooks/useProjects';

export function ProjectsListPage() {
  const [filters, setFilters] = useState<ProjectFilterState>({
    search: '',
    status: '',
    district: '',
    ministry: '',
  });

  const { data, isLoading, error } = useProjects({
    search: filters.search,
    status: filters.status,
    district: filters.district,
    ministry: filters.ministry,
    page: 1,
    perPage: 10,
  });

  const projects = data?.items || [];

  return (
    <PageContainer>
      <PageHeader
        title="Projects"
        description="Create, monitor, filter, and manage government projects."
        actions={
          <Link to="/projects/new">
            <Button>New Project</Button>
          </Link>
        }
      />

      <ProjectSummaryCards projects={projects} />
      <ProjectFilters filters={filters} onChange={setFilters} />

      {isLoading && <LoadingSpinner label="Loading projects..." />}
      {error && <p className="text-sm font-semibold text-red-600">Unable to load projects.</p>}
      {!isLoading && !error && <ProjectTable projects={projects} />}
    </PageContainer>
  );
}
```

---

## `src/features/projects/pages/CreateProjectPage.tsx`

```tsx
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';

import { ProjectForm } from '../components/ProjectForm';
import { useCreateProject } from '../hooks/useCreateProject';

export function CreateProjectPage() {
  const createProject = useCreateProject();

  return (
    <PageContainer>
      <PageHeader
        title="Create Project"
        description="Register a new government project for monitoring and accountability."
      />

      <ProjectForm
        isSubmitting={createProject.isPending}
        onSubmit={(payload) => createProject.mutate(payload)}
      />
    </PageContainer>
  );
}
```

---

## `src/features/projects/pages/EditProjectPage.tsx`

```tsx
import { useParams } from 'react-router-dom';

import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';

import { ProjectForm } from '../components/ProjectForm';
import { useProjectDetails } from '../hooks/useProjectDetails';
import { useUpdateProject } from '../hooks/useUpdateProject';

export function EditProjectPage() {
  const { projectId } = useParams();
  const { data: project, isLoading } = useProjectDetails(projectId);
  const updateProject = useUpdateProject(projectId as string);

  return (
    <PageContainer>
      <PageHeader
        title="Edit Project"
        description="Update project details, assignments, and key monitoring data."
      />

      {isLoading && <LoadingSpinner label="Loading project..." />}

      {project && (
        <ProjectForm
          defaultValues={project}
          isSubmitting={updateProject.isPending}
          onSubmit={(payload) => updateProject.mutate(payload)}
        />
      )}
    </PageContainer>
  );
}
```

---

## `src/features/projects/pages/ProjectDetailsPage.tsx`

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
import { formatDate } from '@/utils/date';

import { ProjectDocuments } from '../components/ProjectDocuments';
import { ProjectMilestones } from '../components/ProjectMilestones';
import { ProjectStatusBadge } from '../components/ProjectStatusBadge';
import { ProjectTimeline } from '../components/ProjectTimeline';
import { useProjectDetails } from '../hooks/useProjectDetails';
import { getRiskVariant } from '../utils/projectStatus';

export function ProjectDetailsPage() {
  const { projectId } = useParams();
  const { data: project, isLoading, error } = useProjectDetails(projectId);

  if (isLoading) {
    return (
      <PageContainer>
        <LoadingSpinner label="Loading project details..." />
      </PageContainer>
    );
  }

  if (error || !project) {
    return (
      <PageContainer>
        <p className="text-sm font-semibold text-red-600">Project could not be loaded.</p>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <PageHeader
        title={project.title}
        description={`${project.projectCode} • ${project.districtName || project.districtId}`}
        actions={
          <Link to={`/projects/${project.id}/edit`}>
            <Button>Edit Project</Button>
          </Link>
        }
      />

      <div className="mb-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <CardHeader>
            <div>
              <CardTitle>Project Overview</CardTitle>
              <CardDescription>{project.description}</CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">Status</p>
                <div className="mt-2"><ProjectStatusBadge status={project.status} /></div>
              </div>
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">Risk Level</p>
                <div className="mt-2"><Badge variant={getRiskVariant(project.riskLevel)}>{project.riskLevel}</Badge></div>
              </div>
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">Budget</p>
                <p className="mt-2 font-bold text-slate-950">{formatCurrency(project.budgetAmount)}</p>
              </div>
              <div>
                <p className="text-xs font-bold uppercase text-slate-400">Timeline</p>
                <p className="mt-2 font-bold text-slate-950">{formatDate(project.startDate)} — {formatDate(project.endDate)}</p>
              </div>
            </div>

            <div className="mt-6">
              <ProgressBar value={project.progressPercentage} label="Overall Progress" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Assignments</CardTitle>
            <CardDescription>Responsible parties and monitoring ownership.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 text-sm">
              <div>
                <p className="font-bold text-slate-500">Contractor</p>
                <p className="text-slate-950">{project.contractorName || 'Not assigned'}</p>
              </div>
              <div>
                <p className="font-bold text-slate-500">Monitoring Officer</p>
                <p className="text-slate-950">{project.monitoringOfficerName || 'Not assigned'}</p>
              </div>
              <div>
                <p className="font-bold text-slate-500">Ministry</p>
                <p className="text-slate-950">{project.ministryName || project.ministryId}</p>
              </div>
              <div>
                <p className="font-bold text-slate-500">District</p>
                <p className="text-slate-950">{project.districtName || project.districtId}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <ProjectMilestones milestones={project.milestones} />
        <ProjectDocuments documents={project.documents} />
      </div>

      <div className="mt-6">
        <ProjectTimeline timeline={project.timeline} />
      </div>
    </PageContainer>
  );
}
```

---

# 10. Update Router to Use Project Pages

## `src/app/router.tsx`

Add these imports near the top:

```tsx
import { CreateProjectPage } from '@/features/projects/pages/CreateProjectPage';
import { EditProjectPage } from '@/features/projects/pages/EditProjectPage';
import { ProjectDetailsPage } from '@/features/projects/pages/ProjectDetailsPage';
import { ProjectsListPage } from '@/features/projects/pages/ProjectsListPage';
```

Then replace the existing placeholder project routes with these route elements:

```tsx
{
  path: PRIVATE_ROUTES.PROJECTS,
  element: (
    <RoleGuard permission={PERMISSIONS.VIEW_PROJECTS}>
      <ProjectsListPage />
    </RoleGuard>
  ),
},
{
  path: PRIVATE_ROUTES.PROJECT_NEW,
  element: (
    <RoleGuard permission={PERMISSIONS.CREATE_PROJECT}>
      <CreateProjectPage />
    </RoleGuard>
  ),
},
{
  path: PRIVATE_ROUTES.PROJECT_DETAILS,
  element: (
    <RoleGuard permission={PERMISSIONS.VIEW_PROJECT_DETAILS}>
      <ProjectDetailsPage />
    </RoleGuard>
  ),
},
{
  path: PRIVATE_ROUTES.PROJECT_EDIT,
  element: (
    <RoleGuard permission={PERMISSIONS.EDIT_PROJECT}>
      <EditProjectPage />
    </RoleGuard>
  ),
},
```

Keep the rest of your router unchanged.

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
/projects
/projects/new
/projects/PRJ-001
/projects/PRJ-001/edit
```

Expected behavior:

- `/projects` shows project summary cards, filters, and project table.
- Search filters projects by title, project code, district, or contractor.
- Status filter works.
- District filter works.
- Ministry filter works.
- View button opens project details.
- Edit button opens edit form.
- Create project form submits and returns to `/projects`.
- Project details shows overview, assignments, milestones, documents, and timeline.

---

# 13. Phase 7 Completion Checklist

Phase 7 is complete when:

- `ProjectsListPage.tsx` renders project list.
- `CreateProjectPage.tsx` renders project form.
- `EditProjectPage.tsx` loads project and renders form.
- `ProjectDetailsPage.tsx` renders project overview and workflow sections.
- `ProjectFilters.tsx` filters project list.
- `ProjectTable.tsx` opens details and edit pages.
- `ProjectMilestones.tsx` displays milestone records.
- `ProjectDocuments.tsx` displays project documents.
- `ProjectTimeline.tsx` displays workflow events.
- `projects.service.ts` supports mock data and live API readiness.
- Router uses real project pages instead of placeholders.
- `npm run build` passes.

---

# Phase 7 Expected Output

After this phase:

- Projects can be listed.
- Projects can be searched and filtered.
- Projects can be opened.
- Projects can be created.
- Projects can be edited.
- Project details are structured for later evidence, approvals, funds, and audit workflows.

---

# Next Phase

After Phase 7 passes build and browser testing, proceed to:

```txt
Phase 8: Contractor Management Module
```
