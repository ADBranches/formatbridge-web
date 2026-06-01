# Phase 6 — Dashboard Module

**Project:** EB Government Monitoring System  
**Frontend:** React + TypeScript + Vite + Tailwind CSS v4  
**Phase Goal:** Replace the temporary dashboard placeholder with a proper MVP dashboard module that supports role-specific dashboard pages, KPI cards, project status charts, funds utilization, recent activities, and high-risk flags.

---

## Phase 5 Status Check

Your screenshot shows the login page is rendering correctly and safe login error handling is working. The visible error message is expected if the password is intentionally wrong.

Before starting Phase 6, run:

```bash
npm run build
```

If the build succeeds, Phase 5 is complete and Phase 6 can be implemented safely.

---

# Phase 6 Objectives

This phase implements:

- Main government admin dashboard.
- Role-specific dashboard variations.
- KPI cards for total projects, active monitoring, pending reviews, delayed projects, funds, audits, and approvals.
- Funds utilization display.
- Project status donut chart.
- Recent activities list.
- High-risk flag summary.
- Mock dashboard data that can later be replaced by live API data.

---

# 1. Create Phase 6 Directories

Run from the project root:

```bash
mkdir -p src/features/dashboard/components src/features/dashboard/pages src/features/dashboard/hooks src/features/dashboard/widgets
```

---

# 2. Create Phase 6 Files

Run from the project root:

```bash
touch src/features/dashboard/pages/AdminDashboardPage.tsx src/features/dashboard/pages/ContractorDashboardPage.tsx src/features/dashboard/pages/MonitoringDashboardPage.tsx src/features/dashboard/pages/ApprovalDashboardPage.tsx src/features/dashboard/pages/AuditorDashboardPage.tsx src/features/dashboard/components/DashboardKpiGrid.tsx src/features/dashboard/components/RecentActivities.tsx src/features/dashboard/components/RiskFlagSummary.tsx src/features/dashboard/components/FundsUtilizationCard.tsx src/features/dashboard/components/ProjectStatusOverview.tsx src/features/dashboard/widgets/KpiCard.tsx src/features/dashboard/widgets/StatusDonutChart.tsx src/features/dashboard/widgets/FundsProgressChart.tsx src/features/dashboard/hooks/useDashboardStats.ts
```

---

# 3. Populate Dashboard Hook

## `src/features/dashboard/hooks/useDashboardStats.ts`

```ts
import { useMemo } from 'react';

import { USER_ROLES, type UserRole } from '@/config/permissions';

export type DashboardKpi = {
  label: string;
  value: string | number;
  description: string;
  trend?: string;
  tone?: 'green' | 'orange' | 'blue' | 'red' | 'navy';
};

export type ProjectStatusDatum = {
  name: string;
  value: number;
  color: string;
};

export type FundsUtilizationDatum = {
  label: string;
  amount: number;
  percentage: number;
  color: 'green' | 'orange' | 'blue' | 'red';
};

export type RecentActivity = {
  id: string;
  title: string;
  description: string;
  time: string;
  type: 'project' | 'evidence' | 'approval' | 'audit' | 'funds';
};

export type RiskFlag = {
  id: string;
  title: string;
  project: string;
  district: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
};

export type DashboardStats = {
  kpis: DashboardKpi[];
  projectStatuses: ProjectStatusDatum[];
  fundsUtilization: FundsUtilizationDatum[];
  recentActivities: RecentActivity[];
  riskFlags: RiskFlag[];
};

const adminStats: DashboardStats = {
  kpis: [
    {
      label: 'Total Projects',
      value: 256,
      description: 'All monitored government projects',
      trend: '+12 this month',
      tone: 'navy',
    },
    {
      label: 'Active Monitoring',
      value: 158,
      description: 'Projects currently under monitoring',
      trend: '62% active',
      tone: 'green',
    },
    {
      label: 'Pending Reviews',
      value: 42,
      description: 'Submissions waiting for M&E action',
      trend: 'Needs attention',
      tone: 'orange',
    },
    {
      label: 'Delayed Projects',
      value: 18,
      description: 'Projects past planned milestone dates',
      trend: 'High priority',
      tone: 'red',
    },
  ],
  projectStatuses: [
    { name: 'Completed', value: 84, color: '#009659' },
    { name: 'In Progress', value: 112, color: '#2A78DC' },
    { name: 'Pending Review', value: 42, color: '#F58420' },
    { name: 'Delayed', value: 18, color: '#DC4343' },
  ],
  fundsUtilization: [
    { label: 'Released Funds', amount: 18400000000, percentage: 72, color: 'green' },
    { label: 'Utilized Funds', amount: 13900000000, percentage: 54, color: 'blue' },
    { label: 'Pending Release', amount: 4600000000, percentage: 18, color: 'orange' },
    { label: 'Flagged Variance', amount: 920000000, percentage: 4, color: 'red' },
  ],
  recentActivities: [
    {
      id: 'ACT-001',
      title: 'Evidence submitted',
      description: 'Contractor uploaded receipts for Wakiso Health Center milestone 2.',
      time: '10 minutes ago',
      type: 'evidence',
    },
    {
      id: 'ACT-002',
      title: 'Approval completed',
      description: 'Road works milestone approval was completed by approval authority.',
      time: '38 minutes ago',
      type: 'approval',
    },
    {
      id: 'ACT-003',
      title: 'Risk flag raised',
      description: 'Low progress versus high funds utilized detected on water project.',
      time: '1 hour ago',
      type: 'audit',
    },
    {
      id: 'ACT-004',
      title: 'Project created',
      description: 'New ICT infrastructure project added for monitoring.',
      time: '3 hours ago',
      type: 'project',
    },
  ],
  riskFlags: [
    {
      id: 'RISK-001',
      title: 'Low progress with high utilization',
      project: 'District Water Supply Upgrade',
      district: 'Moroto',
      severity: 'CRITICAL',
      description: 'Project reports 28% progress but 76% funds utilization.',
    },
    {
      id: 'RISK-002',
      title: 'Delayed milestone',
      project: 'Community Health Center Construction',
      district: 'Wakiso',
      severity: 'HIGH',
      description: 'Milestone 3 is 21 days behind schedule.',
    },
    {
      id: 'RISK-003',
      title: 'Missing supporting evidence',
      project: 'Rural Road Maintenance Package',
      district: 'Arua',
      severity: 'MEDIUM',
      description: 'Receipt package submitted without delivery notes.',
    },
  ],
};

function statsForRole(role?: UserRole): DashboardStats {
  switch (role) {
    case USER_ROLES.CONTRACTOR:
      return {
        ...adminStats,
        kpis: [
          {
            label: 'Assigned Projects',
            value: 8,
            description: 'Projects assigned to your company',
            trend: '3 active milestones',
            tone: 'navy',
          },
          {
            label: 'Pending Evidence',
            value: 5,
            description: 'Evidence packages required',
            trend: 'Action needed',
            tone: 'orange',
          },
          {
            label: 'Approved Milestones',
            value: 12,
            description: 'Milestones approved after review',
            trend: '+2 this month',
            tone: 'green',
          },
          {
            label: 'Payment Requests',
            value: 3,
            description: 'Awaiting fund release processing',
            trend: 'Pending approval',
            tone: 'blue',
          },
        ],
      };

    case USER_ROLES.ME_OFFICER:
      return {
        ...adminStats,
        kpis: [
          {
            label: 'Assigned Reviews',
            value: 31,
            description: 'Reviews assigned to you',
            trend: '9 due today',
            tone: 'orange',
          },
          {
            label: 'Field Inspections',
            value: 14,
            description: 'Scheduled field inspections',
            trend: '4 this week',
            tone: 'blue',
          },
          {
            label: 'Verified Evidence',
            value: 76,
            description: 'Evidence packages verified',
            trend: '+11 this week',
            tone: 'green',
          },
          {
            label: 'Risk Flags',
            value: 9,
            description: 'Projects requiring escalation',
            trend: 'Needs action',
            tone: 'red',
          },
        ],
      };

    case USER_ROLES.APPROVAL_AUTHORITY:
      return {
        ...adminStats,
        kpis: [
          {
            label: 'Pending Approvals',
            value: 24,
            description: 'Requests awaiting your decision',
            trend: '8 urgent',
            tone: 'orange',
          },
          {
            label: 'Approved Requests',
            value: 91,
            description: 'Requests approved this period',
            trend: '+17 this month',
            tone: 'green',
          },
          {
            label: 'Fund Requests',
            value: 12,
            description: 'Milestone-based fund requests',
            trend: 'UGX queue active',
            tone: 'blue',
          },
          {
            label: 'Rejected Requests',
            value: 6,
            description: 'Rejected due to incomplete evidence',
            trend: 'Requires corrections',
            tone: 'red',
          },
        ],
      };

    case USER_ROLES.AUDITOR:
      return {
        ...adminStats,
        kpis: [
          {
            label: 'Audit Assignments',
            value: 19,
            description: 'Projects assigned for audit',
            trend: '5 high priority',
            tone: 'navy',
          },
          {
            label: 'Open Findings',
            value: 27,
            description: 'Findings awaiting resolution',
            trend: '11 major issues',
            tone: 'orange',
          },
          {
            label: 'Compliant Projects',
            value: 64,
            description: 'Projects passing compliance checks',
            trend: '71% compliance',
            tone: 'green',
          },
          {
            label: 'Critical Flags',
            value: 4,
            description: 'Critical risk findings',
            trend: 'Escalate now',
            tone: 'red',
          },
        ],
      };

    default:
      return adminStats;
  }
}

export function useDashboardStats(role?: UserRole) {
  return useMemo(() => statsForRole(role), [role]);
}
```

---

# 4. Populate Dashboard Widgets

## `src/features/dashboard/widgets/KpiCard.tsx`

```tsx
import type { ReactNode } from 'react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { cn } from '@/utils/cn';

type KpiCardProps = {
  label: string;
  value: string | number;
  description: string;
  trend?: string;
  tone?: 'green' | 'orange' | 'blue' | 'red' | 'navy';
  icon?: ReactNode;
};

const toneClasses = {
  green: 'bg-emerald-50 text-emerald-700',
  orange: 'bg-orange-50 text-orange-700',
  blue: 'bg-blue-50 text-blue-700',
  red: 'bg-red-50 text-red-700',
  navy: 'bg-[#051931]/10 text-[#051931]',
};

export function KpiCard({
  label,
  value,
  description,
  trend,
  tone = 'navy',
  icon,
}: KpiCardProps) {
  return (
    <Card className="min-h-36 transition hover:-translate-y-0.5 hover:shadow-md">
      <CardHeader className="mb-3">
        <div>
          <CardDescription>{label}</CardDescription>
          <CardTitle className="mt-4 text-4xl font-black">{value}</CardTitle>
        </div>

        {icon && (
          <div className={cn('flex h-11 w-11 items-center justify-center rounded-xl', toneClasses[tone])}>
            {icon}
          </div>
        )}
      </CardHeader>

      <CardContent>
        <p className="text-sm text-slate-500">{description}</p>
        {trend && (
          <p className={cn('mt-3 inline-flex rounded-full px-2.5 py-1 text-xs font-bold', toneClasses[tone])}>
            {trend}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
```

---

## `src/features/dashboard/widgets/StatusDonutChart.tsx`

```tsx
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';

import type { ProjectStatusDatum } from '../hooks/useDashboardStats';

type StatusDonutChartProps = {
  data: ProjectStatusDatum[];
};

export function StatusDonutChart({ data }: StatusDonutChartProps) {
  const total = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="grid gap-6 md:grid-cols-[220px_1fr] md:items-center">
      <div className="relative h-56">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={64}
              outerRadius={92}
              paddingAngle={3}
            >
              {data.map((entry) => (
                <Cell key={entry.name} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>

        <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-black text-slate-950">{total}</span>
          <span className="text-xs font-semibold text-slate-500">Projects</span>
        </div>
      </div>

      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.name} className="flex items-center justify-between gap-3 rounded-xl bg-slate-50 px-3 py-2">
            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-full" style={{ backgroundColor: item.color }} />
              <span className="text-sm font-semibold text-slate-700">{item.name}</span>
            </div>
            <span className="text-sm font-black text-slate-950">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## `src/features/dashboard/widgets/FundsProgressChart.tsx`

```tsx
import { ProgressBar } from '@/components/ui/ProgressBar';
import { formatCurrency } from '@/utils/currency';

import type { FundsUtilizationDatum } from '../hooks/useDashboardStats';

type FundsProgressChartProps = {
  data: FundsUtilizationDatum[];
};

export function FundsProgressChart({ data }: FundsProgressChartProps) {
  return (
    <div className="space-y-5">
      {data.map((item) => (
        <div key={item.label}>
          <div className="mb-2 flex items-center justify-between gap-4">
            <div>
              <p className="text-sm font-bold text-slate-800">{item.label}</p>
              <p className="text-xs text-slate-500">{formatCurrency(item.amount)}</p>
            </div>
            <span className="text-sm font-black text-slate-950">{item.percentage}%</span>
          </div>

          <ProgressBar value={item.percentage} showValue={false} color={item.color} />
        </div>
      ))}
    </div>
  );
}
```

---

# 5. Populate Dashboard Components

## `src/features/dashboard/components/DashboardKpiGrid.tsx`

```tsx
import {
  AlertTriangle,
  ClipboardCheck,
  FolderKanban,
  ShieldCheck,
} from 'lucide-react';

import type { DashboardKpi } from '../hooks/useDashboardStats';
import { KpiCard } from '../widgets/KpiCard';

type DashboardKpiGridProps = {
  kpis: DashboardKpi[];
};

const icons = [FolderKanban, ClipboardCheck, ShieldCheck, AlertTriangle];

export function DashboardKpiGrid({ kpis }: DashboardKpiGridProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      {kpis.map((kpi, index) => {
        const Icon = icons[index % icons.length];

        return (
          <KpiCard
            key={kpi.label}
            label={kpi.label}
            value={kpi.value}
            description={kpi.description}
            trend={kpi.trend}
            tone={kpi.tone}
            icon={<Icon className="h-5 w-5" />}
          />
        );
      })}
    </div>
  );
}
```

---

## `src/features/dashboard/components/ProjectStatusOverview.tsx`

```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

import type { ProjectStatusDatum } from '../hooks/useDashboardStats';
import { StatusDonutChart } from '../widgets/StatusDonutChart';

type ProjectStatusOverviewProps = {
  data: ProjectStatusDatum[];
};

export function ProjectStatusOverview({ data }: ProjectStatusOverviewProps) {
  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle>Project Status Overview</CardTitle>
          <CardDescription>Distribution of monitored projects by current status.</CardDescription>
        </div>
      </CardHeader>

      <CardContent>
        <StatusDonutChart data={data} />
      </CardContent>
    </Card>
  );
}
```

---

## `src/features/dashboard/components/FundsUtilizationCard.tsx`

```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

import type { FundsUtilizationDatum } from '../hooks/useDashboardStats';
import { FundsProgressChart } from '../widgets/FundsProgressChart';

type FundsUtilizationCardProps = {
  data: FundsUtilizationDatum[];
};

export function FundsUtilizationCard({ data }: FundsUtilizationCardProps) {
  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle>Funds Utilization</CardTitle>
          <CardDescription>Released, utilized, pending, and flagged funds.</CardDescription>
        </div>
      </CardHeader>

      <CardContent>
        <FundsProgressChart data={data} />
      </CardContent>
    </Card>
  );
}
```

---

## `src/features/dashboard/components/RecentActivities.tsx`

```tsx
import {
  ClipboardCheck,
  FileText,
  FolderKanban,
  Landmark,
  WalletCards,
} from 'lucide-react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { cn } from '@/utils/cn';

import type { RecentActivity } from '../hooks/useDashboardStats';

type RecentActivitiesProps = {
  activities: RecentActivity[];
};

const activityIcons = {
  project: FolderKanban,
  evidence: FileText,
  approval: ClipboardCheck,
  audit: Landmark,
  funds: WalletCards,
};

const activityTones = {
  project: 'bg-blue-50 text-blue-700',
  evidence: 'bg-orange-50 text-orange-700',
  approval: 'bg-emerald-50 text-emerald-700',
  audit: 'bg-red-50 text-red-700',
  funds: 'bg-purple-50 text-purple-700',
};

export function RecentActivities({ activities }: RecentActivitiesProps) {
  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle>Recent Activities</CardTitle>
          <CardDescription>Latest project, evidence, approval, and audit events.</CardDescription>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-4">
          {activities.map((activity) => {
            const Icon = activityIcons[activity.type];

            return (
              <article key={activity.id} className="flex gap-3 rounded-2xl border border-slate-100 bg-slate-50 p-3">
                <div className={cn('flex h-10 w-10 shrink-0 items-center justify-center rounded-xl', activityTones[activity.type])}>
                  <Icon className="h-5 w-5" />
                </div>

                <div className="min-w-0 flex-1">
                  <div className="flex flex-col justify-between gap-1 sm:flex-row sm:items-start">
                    <h3 className="font-bold text-slate-900">{activity.title}</h3>
                    <span className="text-xs font-semibold text-slate-400">{activity.time}</span>
                  </div>
                  <p className="mt-1 text-sm leading-6 text-slate-600">{activity.description}</p>
                </div>
              </article>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
```

---

## `src/features/dashboard/components/RiskFlagSummary.tsx`

```tsx
import { AlertTriangle } from 'lucide-react';

import { Badge } from '@/components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

import type { RiskFlag } from '../hooks/useDashboardStats';

type RiskFlagSummaryProps = {
  risks: RiskFlag[];
};

function severityVariant(severity: RiskFlag['severity']) {
  if (severity === 'CRITICAL' || severity === 'HIGH') return 'danger';
  if (severity === 'MEDIUM') return 'warning';
  return 'info';
}

export function RiskFlagSummary({ risks }: RiskFlagSummaryProps) {
  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle>High-Risk Flags</CardTitle>
          <CardDescription>Projects requiring urgent monitoring or audit attention.</CardDescription>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-4">
          {risks.map((risk) => (
            <article key={risk.id} className="rounded-2xl border border-slate-100 bg-white p-4 shadow-sm">
              <div className="flex items-start justify-between gap-3">
                <div className="flex gap-3">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-50 text-red-600">
                    <AlertTriangle className="h-5 w-5" />
                  </div>

                  <div>
                    <h3 className="font-bold text-slate-950">{risk.title}</h3>
                    <p className="mt-1 text-sm text-slate-500">
                      {risk.project} — {risk.district}
                    </p>
                  </div>
                </div>

                <Badge variant={severityVariant(risk.severity)}>{risk.severity}</Badge>
              </div>

              <p className="mt-3 text-sm leading-6 text-slate-600">{risk.description}</p>
            </article>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
```

---

# 6. Populate Dashboard Pages

## `src/features/dashboard/pages/AdminDashboardPage.tsx`

```tsx
import { Button } from '@/components/ui/Button';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { useAuth } from '@/hooks/useAuth';

import { DashboardKpiGrid } from '../components/DashboardKpiGrid';
import { FundsUtilizationCard } from '../components/FundsUtilizationCard';
import { ProjectStatusOverview } from '../components/ProjectStatusOverview';
import { RecentActivities } from '../components/RecentActivities';
import { RiskFlagSummary } from '../components/RiskFlagSummary';
import { useDashboardStats } from '../hooks/useDashboardStats';

export function AdminDashboardPage() {
  const { role } = useAuth();
  const stats = useDashboardStats(role);

  return (
    <PageContainer>
      <PageHeader
        title="Government Admin Dashboard"
        description="Overview of government projects, funds, monitoring activity, approvals, and risk flags."
        actions={
          <>
            <Button variant="outline">Export Summary</Button>
            <Button>New Project</Button>
          </>
        }
      />

      <DashboardKpiGrid kpis={stats.kpis} />

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <ProjectStatusOverview data={stats.projectStatuses} />
        <FundsUtilizationCard data={stats.fundsUtilization} />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <RecentActivities activities={stats.recentActivities} />
        <RiskFlagSummary risks={stats.riskFlags} />
      </div>
    </PageContainer>
  );
}
```

---

## `src/features/dashboard/pages/ContractorDashboardPage.tsx`

```tsx
import { Button } from '@/components/ui/Button';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { useAuth } from '@/hooks/useAuth';

import { DashboardKpiGrid } from '../components/DashboardKpiGrid';
import { FundsUtilizationCard } from '../components/FundsUtilizationCard';
import { RecentActivities } from '../components/RecentActivities';
import { useDashboardStats } from '../hooks/useDashboardStats';

export function ContractorDashboardPage() {
  const { role } = useAuth();
  const stats = useDashboardStats(role);

  return (
    <PageContainer>
      <PageHeader
        title="Contractor Dashboard"
        description="Track assigned projects, evidence submissions, milestone approvals, and payment progress."
        actions={<Button>Upload Evidence</Button>}
      />

      <DashboardKpiGrid kpis={stats.kpis} />

      <div className="mt-6 grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <FundsUtilizationCard data={stats.fundsUtilization} />
        <RecentActivities activities={stats.recentActivities} />
      </div>
    </PageContainer>
  );
}
```

---

## `src/features/dashboard/pages/MonitoringDashboardPage.tsx`

```tsx
import { Button } from '@/components/ui/Button';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { useAuth } from '@/hooks/useAuth';

import { DashboardKpiGrid } from '../components/DashboardKpiGrid';
import { ProjectStatusOverview } from '../components/ProjectStatusOverview';
import { RecentActivities } from '../components/RecentActivities';
import { RiskFlagSummary } from '../components/RiskFlagSummary';
import { useDashboardStats } from '../hooks/useDashboardStats';

export function MonitoringDashboardPage() {
  const { role } = useAuth();
  const stats = useDashboardStats(role);

  return (
    <PageContainer>
      <PageHeader
        title="M&E Officer Dashboard"
        description="Review evidence, field inspections, monitoring recommendations, and project risk flags."
        actions={<Button>Open Review Queue</Button>}
      />

      <DashboardKpiGrid kpis={stats.kpis} />

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <ProjectStatusOverview data={stats.projectStatuses} />
        <RiskFlagSummary risks={stats.riskFlags} />
      </div>

      <div className="mt-6">
        <RecentActivities activities={stats.recentActivities} />
      </div>
    </PageContainer>
  );
}
```

---

## `src/features/dashboard/pages/ApprovalDashboardPage.tsx`

```tsx
import { Button } from '@/components/ui/Button';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { useAuth } from '@/hooks/useAuth';

import { DashboardKpiGrid } from '../components/DashboardKpiGrid';
import { FundsUtilizationCard } from '../components/FundsUtilizationCard';
import { RecentActivities } from '../components/RecentActivities';
import { useDashboardStats } from '../hooks/useDashboardStats';

export function ApprovalDashboardPage() {
  const { role } = useAuth();
  const stats = useDashboardStats(role);

  return (
    <PageContainer>
      <PageHeader
        title="Approval Authority Dashboard"
        description="Review pending approvals, milestone decisions, and fund release requests."
        actions={<Button>View Pending Approvals</Button>}
      />

      <DashboardKpiGrid kpis={stats.kpis} />

      <div className="mt-6 grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <FundsUtilizationCard data={stats.fundsUtilization} />
        <RecentActivities activities={stats.recentActivities} />
      </div>
    </PageContainer>
  );
}
```

---

## `src/features/dashboard/pages/AuditorDashboardPage.tsx`

```tsx
import { Button } from '@/components/ui/Button';
import { PageContainer } from '@/components/layout/PageContainer';
import { PageHeader } from '@/components/layout/PageHeader';
import { useAuth } from '@/hooks/useAuth';

import { DashboardKpiGrid } from '../components/DashboardKpiGrid';
import { ProjectStatusOverview } from '../components/ProjectStatusOverview';
import { RecentActivities } from '../components/RecentActivities';
import { RiskFlagSummary } from '../components/RiskFlagSummary';
import { useDashboardStats } from '../hooks/useDashboardStats';

export function AuditorDashboardPage() {
  const { role } = useAuth();
  const stats = useDashboardStats(role);

  return (
    <PageContainer>
      <PageHeader
        title="Auditor Dashboard"
        description="Audit assignments, compliance status, risk findings, and suspicious project activity."
        actions={<Button>Open Audit Assignments</Button>}
      />

      <DashboardKpiGrid kpis={stats.kpis} />

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <ProjectStatusOverview data={stats.projectStatuses} />
        <RiskFlagSummary risks={stats.riskFlags} />
      </div>

      <div className="mt-6">
        <RecentActivities activities={stats.recentActivities} />
      </div>
    </PageContainer>
  );
}
```

---

# 7. Update Router to Use Role-Specific Dashboard Pages

## `src/app/router.tsx`

You do **not** need to rewrite the whole router file. Only update the dashboard page logic.

First, add these imports near the top of `src/app/router.tsx`:

```tsx
import { AdminDashboardPage } from '@/features/dashboard/pages/AdminDashboardPage';
import { ApprovalDashboardPage } from '@/features/dashboard/pages/ApprovalDashboardPage';
import { AuditorDashboardPage } from '@/features/dashboard/pages/AuditorDashboardPage';
import { ContractorDashboardPage } from '@/features/dashboard/pages/ContractorDashboardPage';
import { MonitoringDashboardPage } from '@/features/dashboard/pages/MonitoringDashboardPage';
import { useAuth } from '@/hooks/useAuth';
```

Then delete the old local `DashboardPage` function from `src/app/router.tsx`.

Replace the old `DashboardPage` function with this function:

```tsx
function DashboardPage() {
  const { role } = useAuth();

  if (role === USER_ROLES.CONTRACTOR) {
    return <ContractorDashboardPage />;
  }

  if (role === USER_ROLES.ME_OFFICER) {
    return <MonitoringDashboardPage />;
  }

  if (role === USER_ROLES.APPROVAL_AUTHORITY) {
    return <ApprovalDashboardPage />;
  }

  if (role === USER_ROLES.AUDITOR) {
    return <AuditorDashboardPage />;
  }

  return <AdminDashboardPage />;
}
```

Keep the dashboard route as it already is:

```tsx
{
  path: PRIVATE_ROUTES.DASHBOARD,
  element: (
    <RoleGuard permission={PERMISSIONS.VIEW_DASHBOARD}>
      <DashboardPage />
    </RoleGuard>
  ),
},
```

---

# 8. Optional: Remove Unused Imports from Router

After deleting the old local dashboard, your router may no longer need these imports:

```tsx
import { Button } from '@/components/ui/Button';
```

Only remove imports if TypeScript reports them as unused.

---

# 9. Build Test

Run:

```bash
npm run build
```

Expected result:

```txt
✓ built
```

---

# 10. Browser Test

Run:

```bash
npm run dev
```

Open:

```txt
http://localhost:5173/dashboard
```

Test role-based dashboard variations:

1. Go to `/login`.
2. Select **Government Admin** and log in.
3. Confirm dashboard title is **Government Admin Dashboard**.
4. Logout.
5. Select **Contractor** and log in.
6. Confirm dashboard title is **Contractor Dashboard**.
7. Logout.
8. Select **M&E Officer** and log in.
9. Confirm dashboard title is **M&E Officer Dashboard**.
10. Logout.
11. Select **Approval Authority** and log in.
12. Confirm dashboard title is **Approval Authority Dashboard**.
13. Logout.
14. Select **Auditor** and log in.
15. Confirm dashboard title is **Auditor Dashboard**.

---

# 11. Phase 6 Completion Checklist

Phase 6 is complete when:

- `src/features/dashboard/pages/AdminDashboardPage.tsx` exists.
- `src/features/dashboard/pages/ContractorDashboardPage.tsx` exists.
- `src/features/dashboard/pages/MonitoringDashboardPage.tsx` exists.
- `src/features/dashboard/pages/ApprovalDashboardPage.tsx` exists.
- `src/features/dashboard/pages/AuditorDashboardPage.tsx` exists.
- KPI cards render correctly.
- Project status donut chart renders correctly.
- Funds utilization progress chart renders correctly.
- Recent activities render correctly.
- Risk flags render correctly.
- Dashboard changes based on login role.
- `npm run build` passes.

---

# Phase 6 Expected Output

After completing this phase:

- Admin dashboard matches the MVP design direction.
- Different roles have different dashboard cards and page titles.
- Dashboard uses mock data from a dedicated hook.
- Dashboard is ready to connect to a live backend API later.
- UI components remain reusable and clean.

---

# Next Phase

After Phase 6 passes build and browser testing, proceed to:

```txt
Phase 7: Project Management Module
```
