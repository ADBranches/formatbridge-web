# Edwin's Frontend Delivery Timeline — Car Dealership Project

> Owner: Edwin Kambale  
> Assigned area: Frontend Dev #2 — Admin Panels & Interaction Forms  
> Start date: Fri, 12 Jun 2026  
> Working style: fork-based collaboration, feature branches, pull requests to upstream project

---

## Important Note About The Stack

The project `.docx` does **not** exclusively define the technical stack. It describes project roles, backend/frontend user stories, API expectations, and acceptance criteria, but it does not lock the team into one frontend framework, styling library, database, ORM, or package manager.

So before coding deeply, confirm the actual stack from the repository files, especially:

- `package.json`
- `vite.config.ts`
- `pnpm-workspace.yaml`
- `src/`
- `backend/`
- existing component structure
- existing auth/state management pattern
- existing routing setup

Based on the current repository shape, follow the repo’s existing stack instead of introducing unnecessary new libraries.

---

## Your Assigned User Stories

### User Story 1: Interactive Test Drive Scheduler

As a serious car buyer, the user should be able to pick an open calendar date and time on the Car Details page so that the user can reserve a real-world test drive slot.

Acceptance checklist:

- [ ] Date picker blocks historical dates.
- [ ] Form blocks invalid times.
- [ ] Unauthenticated users cannot submit.
- [ ] Unauthenticated users are redirected politely to login.
- [ ] Successful submission shows a clear visual confirmation.

### User Story 2: Admin Dashboard & Operations Control Panel

As a dealership manager, the user should see a private dashboard table with current listings and Edit/Delete controls so that pricing can be updated or sold cars can be removed.

Acceptance checklist:

- [ ] Admin dashboard route is protected.
- [ ] Route guard checks admin permissions.
- [ ] Current listings are shown in a table.
- [ ] Each listing has Edit and Delete actions.
- [ ] Delete opens a confirmation modal before deletion.

---

## Git Collaboration Rules

### Remotes

Your fork should be `origin`:

```bash
origin    https://github.com/ADBranches/cardealership.git
```

The original project should be `upstream`:

```bash
upstream  https://github.com/stevenssebuma/cardealership.git
```

### Daily Sync Before Work

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### Branch Naming

Use focused branches:

```bash
feature/test-drive-scheduler
feature/admin-dashboard
fix/test-drive-auth-redirect
fix/admin-delete-confirmation-modal
```

### Push Feature Branch

```bash
git push -u origin feature/test-drive-scheduler
```

### Pull Request Target

When opening a PR:

```text
base repository: stevenssebuma/cardealership
base branch: main
head repository: ADBranches/cardealership
compare branch: feature/your-branch-name
```

---

# Timeline

## Phase 0 — Setup Verification

**Date:** Fri, 12 Jun 2026  
**Goal:** Confirm your local setup is clean and ready.

Tasks:

- [ ] Confirm `origin` points to your fork.
- [ ] Confirm `upstream` points to the original repo.
- [ ] Run project install command based on the repo package manager.
- [ ] Start frontend locally.
- [ ] Identify current routing setup.
- [ ] Identify auth storage pattern: token, user object, role/admin flag.
- [ ] Identify existing car details page.
- [ ] Identify existing admin/dashboard structure if present.

Suggested commands:

```bash
git remote -v
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

Deliverable:

- [ ] Local app running.
- [ ] Notes on where routes, components, auth, and API helpers are located.

---

## Phase 1 — Test Drive Scheduler Planning

**Date:** Sat, 13 Jun 2026  
**Branch:** `feature/test-drive-scheduler`

Tasks:

- [ ] Create feature branch from updated `main`.
- [ ] Inspect Car Details page.
- [ ] Decide scheduler component location.
- [ ] Define form fields:
  - [ ] Full name if needed.
  - [ ] Contact if needed.
  - [ ] Date.
  - [ ] Time.
  - [ ] Optional note/message.
  - [ ] Car ID from route params.
- [ ] Confirm how authentication is checked.
- [ ] Confirm login route path.
- [ ] Decide fallback behavior if backend booking endpoint is not ready.

Suggested commands:

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
git checkout -b feature/test-drive-scheduler
```

Deliverable:

- [ ] Scheduler implementation plan written in code comments or issue notes.

---

## Phase 2 — Build Test Drive Scheduler UI

**Date:** Sun, 14 Jun 2026  
**Branch:** `feature/test-drive-scheduler`

Tasks:

- [ ] Create reusable scheduler form component.
- [ ] Add date input/date picker.
- [ ] Block past dates using today’s date as the minimum date.
- [ ] Add time selection.
- [ ] Block invalid time slots.
- [ ] Add form validation messages.
- [ ] Add loading/submitting state.
- [ ] Add success confirmation UI.
- [ ] Place component on Car Details page.
- [ ] Ensure responsive layout.

Deliverable:

- [ ] User can see and interact with the scheduler on the Car Details page.

---

## Phase 3 — Add Auth Redirect For Scheduler

**Date:** Mon, 15 Jun 2026  
**Branch:** `feature/test-drive-scheduler`

Tasks:

- [ ] Check if user is authenticated before submission.
- [ ] If unauthenticated, redirect to login.
- [ ] Preserve return path if routing setup supports it.
- [ ] Show polite message before redirect or on login page.
- [ ] Prevent API call if user is unauthenticated.
- [ ] Test with logged-out state.
- [ ] Test with logged-in state.

Deliverable:

- [ ] Scheduler respects authentication requirement.

---

## Phase 4 — Connect Scheduler To API Or Temporary Mock

**Date:** Tue, 16 Jun 2026  
**Branch:** `feature/test-drive-scheduler`

Tasks:

- [ ] Check whether backend booking/test-drive endpoint exists.
- [ ] If endpoint exists, connect form submission.
- [ ] If endpoint does not exist, create a clean temporary mock function or TODO block.
- [ ] Handle success response.
- [ ] Handle validation errors.
- [ ] Handle network/server errors.
- [ ] Avoid hardcoded fake success if backend is expected soon.

Deliverable:

- [ ] Scheduler has complete submit flow with success/error states.

---

## Phase 5 — Test, Commit, Push, And PR For Scheduler

**Date:** Wed, 17 Jun 2026  
**Branch:** `feature/test-drive-scheduler`

Tasks:

- [ ] Test mobile, tablet, and desktop layout.
- [ ] Test past dates are blocked.
- [ ] Test invalid times are blocked.
- [ ] Test unauthenticated redirect.
- [ ] Test success confirmation.
- [ ] Run lint/build if available.
- [ ] Commit changes.
- [ ] Push branch to your fork.
- [ ] Open PR into original project repo.

Suggested commands:

```bash
git status
git add .
git commit -m "Build test drive scheduler form"
git push -u origin feature/test-drive-scheduler
```

PR title:

```text
Build Test Drive Scheduler Form
```

PR description:

```markdown
## What this PR does
- Adds test drive scheduler form on car details page
- Blocks past dates and invalid time selections
- Redirects unauthenticated users to login before booking
- Shows success confirmation after submission

## Assigned section
Edwin - Frontend Dev #2: Admin Panels & Interaction Forms

## User story
Interactive Test Drive Scheduler
```

Deliverable:

- [ ] PR opened and ready for review.

---

## Phase 6 — Admin Dashboard Planning

**Date:** Thu, 18 Jun 2026  
**Branch:** `feature/admin-dashboard`

Tasks:

- [ ] Sync `main` again before starting.
- [ ] Create `feature/admin-dashboard` branch.
- [ ] Identify admin route path.
- [ ] Identify auth role/admin permission format.
- [ ] Identify cars API endpoint for listing current inventory.
- [ ] Identify edit/update endpoint if available.
- [ ] Identify delete endpoint if available.
- [ ] Plan table columns:
  - [ ] Image/thumbnail.
  - [ ] Make.
  - [ ] Model.
  - [ ] Year.
  - [ ] Price.
  - [ ] Mileage.
  - [ ] Status if available.
  - [ ] Actions.

Suggested commands:

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
git checkout -b feature/admin-dashboard
```

Deliverable:

- [ ] Dashboard page/component plan ready.

---

## Phase 7 — Build Admin Route Guard

**Date:** Fri, 19 Jun 2026  
**Branch:** `feature/admin-dashboard`

Tasks:

- [ ] Create or reuse protected route component.
- [ ] Check authentication.
- [ ] Check admin permission/role.
- [ ] Redirect unauthenticated users to login.
- [ ] Redirect non-admin users to unauthorized/home page.
- [ ] Add loading state while checking auth.
- [ ] Protect admin dashboard route.

Deliverable:

- [ ] Admin dashboard is hidden from non-admin users.

---

## Phase 8 — Build Admin Listings Table

**Date:** Sat, 20 Jun 2026  
**Branch:** `feature/admin-dashboard`

Tasks:

- [ ] Fetch current car listings.
- [ ] Show loading state.
- [ ] Show empty state if no cars exist.
- [ ] Show error state if fetch fails.
- [ ] Render responsive table.
- [ ] Add Edit button.
- [ ] Add Delete button.
- [ ] Keep UI consistent with existing design.

Deliverable:

- [ ] Admin can view inventory in a private dashboard table.

---

## Phase 9 — Add Delete Confirmation Modal

**Date:** Sun, 21 Jun 2026  
**Branch:** `feature/admin-dashboard`

Tasks:

- [ ] Create confirmation modal.
- [ ] Show selected car name/details in modal.
- [ ] Add Cancel button.
- [ ] Add Confirm Delete button.
- [ ] Prevent accidental deletion.
- [ ] Call delete API if available.
- [ ] Remove deleted car from UI after success.
- [ ] Show error message if delete fails.

Deliverable:

- [ ] Delete flow is safe and user-friendly.

---

## Phase 10 — Admin Edit Flow And Final PR

**Date:** Mon, 22 Jun 2026  
**Branch:** `feature/admin-dashboard`

Tasks:

- [ ] Decide whether Edit opens a page, modal, or existing form.
- [ ] Wire Edit button to selected approach.
- [ ] Add basic price/update flow if backend supports it.
- [ ] Test admin route guard.
- [ ] Test table loading/empty/error states.
- [ ] Test delete modal.
- [ ] Test mobile/tablet/desktop layout.
- [ ] Run lint/build if available.
- [ ] Commit, push, and open PR.

Suggested commands:

```bash
git status
git add .
git commit -m "Build admin dashboard inventory controls"
git push -u origin feature/admin-dashboard
```

PR title:

```text
Build Admin Dashboard Inventory Control Panel
```

PR description:

```markdown
## What this PR does
- Adds protected admin dashboard view
- Displays current vehicle listings in a table
- Adds Edit and Delete actions
- Adds confirmation modal before deletion

## Assigned section
Edwin - Frontend Dev #2: Admin Panels & Interaction Forms

## User story
Admin Dashboard & Operations Control Panel
```

Deliverable:

- [ ] PR opened and ready for admin review.

---

# Definition Of Done

Your assigned section is complete when:

- [ ] Test drive scheduler exists on the Car Details page.
- [ ] Past dates and invalid times are blocked.
- [ ] Unauthenticated users cannot submit scheduler form.
- [ ] Scheduler success confirmation is clear.
- [ ] Admin dashboard is protected by admin route guard.
- [ ] Admin dashboard lists current vehicles.
- [ ] Edit/Delete buttons are visible for listings.
- [ ] Delete requires confirmation modal.
- [ ] Code is pushed to your fork on feature branches.
- [ ] Pull requests are opened against `stevenssebuma/cardealership:main`.
- [ ] PR descriptions clearly mention Edwin’s assigned user stories.

---

# Quick Recovery Commands

## If You Forgot To Set Upstream On First Push

```bash
git push -u origin feature/branch-name
```

## If Your Branch Falls Behind Main

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
git checkout feature/branch-name
git merge main
```

## If You Need To See Current Branch

```bash
git branch
```

## If You Need To See Changed Files

```bash
git status
```

---

# Daily Standup Template

```markdown
## Yesterday
- Completed:

## Today
- Working on:

## Blockers
- Need from backend:
- Need from design/frontend team:

## PR/Branch
- Branch:
- PR link:
```
