# Stage 12 — Git and Final Audit Guide

## Objective

Close the enterprise-grade AML SMPC implementation branch and move the project into final audit, pull request review, merge, rehearsal, and defense readiness.

The completed branch should now demonstrate partner-bank onboarding, RBAC permission enforcement, suspicious transaction risk evaluation, SMPC-linked screening evidence, regulator anomaly case workflow, bank anomaly notice response, auditor read-only evidence access, demo seeding, validation scripts, and final documentation.

---

## Step 1 — Confirm Current Branch

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git fetch origin --prune
git status -sb
git branch --show-current
git log --oneline --decorate -8
```

Expected branch:

```text
bank-rbac-suspicion-case-workflow
```

---

## Step 2 — Add Final Stage Files

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git status -sb

git add aml-system/infra/postgres/migrations/008_partner_bank_identity_and_permissions.sql
git add aml-system/infra/postgres/migrations/009_suspicion_rules_and_transaction_risk.sql
git add aml-system/infra/postgres/migrations/010_regulator_anomaly_cases.sql
git add aml-system/services/regulator-api/backend/src
git add aml-system/services/regulator-api/frontend/src
git add aml-system/scripts/dev/seed_bank_rbac_case_demo.py
git add aml-system/scripts/ci/validate-bank-rbac-identity.sh
git add aml-system/scripts/ci/validate-suspicious-transaction-rules.sh
git add aml-system/scripts/ci/validate-regulator-anomaly-case-flow.sh
git add aml-system/scripts/ci/validate-full-enterprise-demo.sh
git add aml-system/docs/demo
git add aml-system/docs/defense
git add aml-system/docs/submission

git status -sb
```

---

## Step 3 — Commit If There Are Staged Changes

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

if git diff --cached --quiet; then
  echo "No staged changes to commit. Continuing to push/check branch."
else
  git commit -m "Add partner bank RBAC suspicion and anomaly case workflow"
fi
```

---

## Step 4 — Push Feature Branch

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git push origin bank-rbac-suspicion-case-workflow

git fetch origin --prune
git status -sb
git rev-list --left-right --count HEAD...origin/bank-rbac-suspicion-case-workflow
```

Expected:

```text
0 0
```

---

## Step 5 — Pull Request Route

Use this because the project is being reviewed through Pull Requests:

```text
GitHub → Pull requests → New pull request
base: main
compare: bank-rbac-suspicion-case-workflow
```

Recommended PR title:

```text
Add partner bank RBAC suspicion and anomaly case workflow
```

Recommended PR description:

```md
## Summary

This PR upgrades the AML SMPC prototype into a stronger enterprise-grade workflow.

## Implemented

- Partner-bank-only onboarding
- Super-admin approval workflow
- Role-based access control with permission attributes
- Bank-side suspicious transaction identification
- AML rules and risk scoring
- SMPC-linked cross-bank evidence
- Proof generation and regulator verification flow
- Regulator anomaly case creation
- Bank-side anomaly notice response
- Auditor read-only evidence access
- Regulator dashboard furnishing
- Partner-bank dashboard furnishing
- Demo seeder
- Enterprise validation scripts
- Final runbooks and defense documentation

## Validation

- Backend build passes.
- Frontend build passes.
- Non-partner registration returns HTTP 400.
- Incompatible bank/regulator role returns HTTP 400.
- Non-super-admin access to `/admin/roles` returns HTTP 403.
- Submitter cannot approve or evaluate risk.
- Reviewer can evaluate risk and approve.
- SMPC screening updates risk score, risk level, suspicion status, and triggered rules.
- Regulator can open anomaly case.
- Bank can view and respond to anomaly notice.
- Auditor can read case but cannot update/close it.
- Raw private bank data is not exposed across banks or to regulator.
```

---

## Step 6 — Merge After PR Review

After the PR is reviewed and approved, merge it on GitHub.

Then sync local main:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git checkout main
git pull origin main

git fetch origin --prune
git rev-list --left-right --count HEAD...origin/main
git status -sb
```

Expected:

```text
0 0
## main...origin/main
```

---

## Step 7 — Final Audit Scripts

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

./aml-system/scripts/ci/final-repository-audit.sh
./aml-system/scripts/demo/final-presentation-rehearsal-check.sh
```

Expected:

```text
FINAL-4 REPOSITORY AUDIT PASSED
FINAL-5 PRESENTATION REHEARSAL CHECK PASSED
```

---

## Step 8 — Enterprise Validation Scripts

Backend services must be running first:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
source env/bin/activate
./scripts/demo/run-frontend-backend.sh
```

In another terminal:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system

./scripts/ci/validate-bank-rbac-identity.sh
./scripts/ci/validate-suspicious-transaction-rules.sh
./scripts/ci/validate-regulator-anomaly-case-flow.sh
./scripts/ci/validate-full-enterprise-demo.sh
```

Expected:

```text
BANK RBAC IDENTITY VALIDATION PASSED
SUSPICIOUS TRANSACTION RULES VALIDATION PASSED
REGULATOR ANOMALY CASE FLOW VALIDATION PASSED
FULL ENTERPRISE DEMO VALIDATION PASSED
```

---

## Final Target State

The application should demonstrate:

1. Partner-bank-only user onboarding.
2. Strong identity binding between user and bank.
3. Explicit RBAC permission attributes.
4. Bank-side suspicious transaction identification.
5. SMPC-supported cross-bank collaboration.
6. Regulator proof and audit verification.
7. Regulator anomaly case creation.
8. Bank-side anomaly notice response.
9. Auditor read-only evidence inspection.
10. No raw private bank data exposed across banks or to the regulator.

---

## Final Rule

Do not add new core implementation after this stage unless final audit or defense rehearsal exposes a real blocker.

The project should now shift to clean repository state, repeatable demo execution, PR review, supervisor review, final defense rehearsal, and submission readiness.
