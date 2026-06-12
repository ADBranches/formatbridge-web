# Phase 2 — Locate Test Drive Integration Points

> Project: Car Dealership Website  
> Owner: Edwin Kambale  
> Active branch: `feature/test-drive-scheduler`  
> Phase status: Ready to execute  
> Approach: Terminal-based inspection only; no feature code changes yet

---

## Objective

Identify exactly where the Test Drive Scheduler should be inserted into the current one-page app flow.

This phase does **not** build the scheduler yet. It only confirms:

- where the vehicle data currently lives,
- where the `BOOK TEST DRIVE` button currently lives,
- where `VIEW DETAILS` actions are located,
- where the scheduler should be mounted inside `src/app/App.tsx`,
- and which existing UI components can support the scheduler in the next phase.

---

## Files/Directories In This Phase

```text
src/app/App.tsx
src/app/components/ui/button.tsx
src/app/components/ui/card.tsx
src/app/components/ui/input.tsx
src/app/components/ui/label.tsx
```

---

## Important Current State

Before starting this phase, confirm:

```text
Phase 1 is already done.
The app runs locally.
The active branch is feature/test-drive-scheduler.
The frontend is served at http://localhost:5173.
```

The current implementation is still a one-page app driven mainly by:

```text
src/main.tsx
src/app/App.tsx
```

So the scheduler should be integrated into the existing page flow rather than introducing React Router or a separate page structure at this point.

---

# Stage 2.1 — Confirm Branch And Working Tree

## Objective

Make sure the work is happening on the correct feature branch and that the current package-lock change is understood before proceeding.

## Terminal Commands

```bash
git branch
```

Expected active branch:

```text
* feature/test-drive-scheduler
  main
```

Then check working tree:

```bash
git status
```

If the only changed file is `package-lock.json` from running `npm i`, inspect it before deciding whether to keep or restore it:

```bash
git diff -- package-lock.json | head -80
```

If the change is not intentional, restore it:

```bash
git restore package-lock.json
```

Then confirm clean state:

```bash
git status
```

## Done Criteria

- Active branch is `feature/test-drive-scheduler`.
- Working tree is clean, or only intentional changes remain.

---

# Stage 2.2 — Locate Vehicle Data And CTA References

## Objective

Find the exact line numbers for vehicle data, `BOOK TEST DRIVE`, `VIEW DETAILS`, and the vehicle card component.

## Terminal Command

```bash
grep -n "BOOK TEST DRIVE\|VIEW DETAILS\|Calendar\|vehicles\|VehicleCard" src/app/App.tsx
```

## Expected Output Pattern

The output should show references similar to:

```text
3: Calendar import from lucide-react
37: const vehicles = [
136: const filteredVehicles = vehicles.filter(...)
143: const VehicleCard = (...)
172: VIEW DETAILS button
192: BOOK TEST DRIVE button
277: filteredVehicles.map(... <VehicleCard />)
```

Line numbers can shift later if the file changes, but the important locations are:

```text
Vehicle data source: const vehicles = [...]
Filtered data source: const filteredVehicles = vehicles.filter(...)
Vehicle card component: const VehicleCard = (...)
Header CTA: BOOK TEST DRIVE
Inventory rendering: filteredVehicles.map(...)
```

## Done Criteria

- `vehicles` array location is known.
- `VehicleCard` location is known.
- `BOOK TEST DRIVE` button location is known.
- `VIEW DETAILS` button location is known.

---

# Stage 2.3 — Inspect The Vehicle Section Context

## Objective

Inspect enough of `src/app/App.tsx` to choose the safest insertion point for the scheduler.

## Terminal Commands

Inspect the vehicle data block:

```bash
sed -n '30,150p' src/app/App.tsx
```

Inspect the vehicle card and action buttons:

```bash
sed -n '140,210p' src/app/App.tsx
```

Inspect the inventory rendering area:

```bash
sed -n '240,305p' src/app/App.tsx
```

Inspect the services/about/contact transition area:

```bash
sed -n '305,370p' src/app/App.tsx
```

## Notes

The scheduler should be mounted after the inventory grid/tabs because the user should first browse vehicles and then book a test drive.

Recommended insertion point:

```text
After the inventory section/tabs and before services/about/contact content.
```

This keeps the flow natural:

```text
Hero -> Search/Inventory -> Test Drive Scheduler -> Services/About/Contact
```

## Done Criteria

- Inventory section ending point is identified.
- Next section after inventory is identified.
- Scheduler insertion point is chosen.

---

# Stage 2.4 — Confirm Existing UI Components For Scheduler

## Objective

Confirm the scheduler can reuse existing UI components instead of introducing new UI libraries.

## Terminal Commands

```bash
ls src/app/components/ui/button.tsx
ls src/app/components/ui/card.tsx
ls src/app/components/ui/input.tsx
ls src/app/components/ui/label.tsx
```

Optional quick inspect:

```bash
sed -n '1,120p' src/app/components/ui/button.tsx
sed -n '1,120p' src/app/components/ui/input.tsx
sed -n '1,120p' src/app/components/ui/label.tsx
sed -n '1,120p' src/app/components/ui/card.tsx
```

## Expected Result

These files should exist:

```text
src/app/components/ui/button.tsx
src/app/components/ui/card.tsx
src/app/components/ui/input.tsx
src/app/components/ui/label.tsx
```

## Done Criteria

- Existing button component is available.
- Existing card component is available.
- Existing input component is available.
- Existing label component is available.
- No new UI library is needed for Phase 3.

---

# Stage 2.5 — Confirm No Router/Login Page Exists Yet

## Objective

Avoid introducing React Router prematurely unless the app already has real routes or login pages.

## Terminal Commands

Search for router usage:

```bash
grep -R "BrowserRouter\|Routes\|Route\|createBrowserRouter\|react-router" -n src/app src/main.tsx
```

Search for login page/component references:

```bash
grep -R "Login\|login\|SignIn\|signin\|auth" -n src/app src/main.tsx
```

## Expected Result

If no router or login page exists, do not add React Router in this phase.

Use a lightweight redirect placeholder in Phase 3/5 only:

```text
/login?redirect=/test-drive
```

## Done Criteria

- Router usage is confirmed or ruled out.
- Login page existence is confirmed or ruled out.
- Decision is made not to introduce routing yet if no route structure exists.

---

# Stage 2.6 — Create A Phase 2 Notes File In The Repo

## Objective

Create a repo-local Markdown note documenting the findings from Phase 2.

## File To Create

```text
guidelines/phase-2-test-drive-integration-points.md
```

## Terminal Commands

Create the guidelines directory if it already does not exist:

```bash
mkdir -p guidelines
```

Create the Phase 2 note file:

```bash
cat > guidelines/phase-2-test-drive-integration-points.md <<'EOF'
# Phase 2 — Test Drive Integration Points

## Objective

Identify where the Test Drive Scheduler should be inserted into the current one-page app flow.

## Files Reviewed

```text
src/app/App.tsx
src/app/components/ui/button.tsx
src/app/components/ui/card.tsx
src/app/components/ui/input.tsx
src/app/components/ui/label.tsx
```

## Key Findings

### Vehicle Data Source

The current vehicle data is defined inside:

```text
src/app/App.tsx
```

Search command:

```bash
grep -n "vehicles" src/app/App.tsx
```

Main location:

```text
const vehicles = [...]
```

### Vehicle Filtering

The filtered vehicle list is created in:

```text
const filteredVehicles = vehicles.filter(...)
```

This filtered list is used to render inventory cards.

### Vehicle Card

The existing vehicle card renderer is:

```text
const VehicleCard = ({ vehicle }) => (...)
```

The `VIEW DETAILS` button currently lives inside this card.

### Header Test Drive CTA

The existing header button is labelled:

```text
BOOK TEST DRIVE
```

This button should become the scroll trigger to the scheduler section.

### Recommended Scheduler Insertion Point

Mount the scheduler after the inventory section/tabs and before the next major content section.

Recommended flow:

```text
Hero -> Search/Inventory -> Test Drive Scheduler -> Services/About/Contact
```

### Scheduler Section ID

The scheduler section should use:

```text
id="test-drive"
```

### Header Button Behavior

The header `BOOK TEST DRIVE` button should scroll to:

```text
#test-drive
```

Expected handler:

```tsx
onClick={() =>
  document.getElementById("test-drive")?.scrollIntoView({ behavior: "smooth" })
}
```

## Decision

Do not introduce React Router yet because the current app is operating as a one-page layout. The scheduler should be integrated into `src/app/App.tsx` and should reuse existing UI components.

## Done Criteria

- Vehicle data source identified.
- Header CTA identified.
- Vehicle card action identified.
- Scheduler insertion point selected.
- Existing UI components confirmed.
EOF
```

Confirm file was created:

```bash
cat guidelines/phase-2-test-drive-integration-points.md
```

## Done Criteria

- `guidelines/phase-2-test-drive-integration-points.md` exists.
- File documents vehicle source, CTA source, insertion point, and routing decision.

---

# Stage 2.7 — Git Status Check

## Objective

Confirm that Phase 2 only adds the documentation note and does not accidentally modify app code.

## Terminal Command

```bash
git status
```

## Expected Changed File

```text
guidelines/phase-2-test-drive-integration-points.md
```

If `package-lock.json` appears and was not intentional, restore it:

```bash
git restore package-lock.json
```

Then check again:

```bash
git status
```

## Done Criteria

- Only the Phase 2 Markdown note is changed/added.
- No app code has been modified in Phase 2.

---

# Final Phase 2 Decision

The Test Drive Scheduler should be inserted inside:

```text
src/app/App.tsx
```

Recommended mount location:

```text
After the inventory tabs/grid section and before the next major section such as services/about/contact.
```

The existing `BOOK TEST DRIVE` button should scroll to:

```text
#test-drive
```

The scheduler should receive initial vehicle data from:

```text
const vehicles = [...]
```

Phase 3 can now proceed with creating:

```text
src/app/components/test-drive/TestDriveScheduler.tsx
```

and integrating it into:

```text
src/app/App.tsx
```
