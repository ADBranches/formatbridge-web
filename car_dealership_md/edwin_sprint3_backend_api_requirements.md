# Edwin Sprint 3 Backend API Requirements And Implementation Guideline

> Project: Car Dealership  
> Sprint: Sprint 3  
> Assigned Developer: Edwin  
> Sprint Role: Backend APIs  
> Assigned Sprint 3 Focus: Transaction notifications and defensive backend validation

---

## 1. Edwin's Sprint 3 Assignment

Sprint 3 assigns Edwin to backend API work, specifically around notification dispatch after appointment booking and defensive validation for incoming inventory upload payloads.

### Assigned Task 1 — Transaction Confirmation Notification Dispatcher

**Goal**

Send a confirmation alert when an appointment is booked.

**Requirement**

Integrate a backend Node.js service utility configuration block. The service can use packages such as Nodemailer or SendGrid templates. When a customer schedule log is confirmed, the backend should trigger a clean automated transactional notification dispatch to the customer inbox.

### Assigned Task 2 — Defensive Payload Cleaners

**Goal**

Protect database tables from malicious or badly typed form submissions.

**Requirement**

Create a backend server validation logic layer that intercepts incoming inventory upload request forms. The validation layer should reject invalid submission data explicitly, especially when strings are injected into numeric financial blocks such as price or mileage.

---

## 2. Implementation Principles

Before modifying code in any phase:

1. Confirm the active branch.
2. Pull latest updates from the correct remote branch.
3. Confirm the working tree is clean.
4. Inspect the existing backend file structure.
5. Inspect the current server entrypoint before adding routes or middleware.
6. Avoid creating duplicate backend servers.
7. Avoid changing frontend behavior unless the phase explicitly requires frontend integration.
8. Keep notification logic and validation logic modular.
9. Run targeted checks before global checks whenever possible.
10. Only commit files relevant to the phase being implemented.

Recommended working branch:

```bash
feature/edwin-sprint3-backend-apis
```

If the team wants Sprint 3 work continued on an existing branch, confirm the branch name before implementation.

---

# Phase 0 — Backend Structure Inspection

## Objective

Inspect the existing backend structure before implementing any Sprint 3 backend logic.

## Files/Directories In This Phase

```text
backend/
backend/server.js
backend/package.json
backend/routes/
backend/controllers/
backend/models/
backend/middleware/
backend/utils/
src/backend/
src/tests/
src/docs/
package.json
README.md
```

## Inspection Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
git status
git branch
git pull --ff-only origin <current-branch>
find backend -maxdepth 4 -type f | sort
find src/backend -maxdepth 4 -type f | sort
find backend/routes backend/controllers backend/models backend/middleware backend/utils -maxdepth 3 -type f | sort
cat backend/package.json
cat package.json
sed -n '1,260p' backend/server.js
```

## Done Criteria

- Active branch is confirmed.
- Working tree is clean.
- Active backend folder is known.
- Existing routes, controllers, models, middleware, and utils are known.
- No files have been modified.

---

# Phase 1 — Notification Service Contract Planning

## Objective

Define the backend notification service contract before choosing Nodemailer, SendGrid, or another provider.

## Files/Directories In This Phase

```text
backend/utils/
backend/services/
backend/config/
backend/.env
backend/package.json
```

## Planned Files

```text
backend/services/notificationService.js
backend/config/email.js
```

## Requirements

The notification service should support sending customer-facing transactional messages after schedule confirmation.

The service contract should prepare for:

- Recipient name
- Recipient email
- Vehicle name or vehicle ID
- Appointment date
- Appointment time
- Confirmation reference if available
- Dealership contact details if available

## Suggested Notification Payload Shape

```js
const notificationPayload = {
  to: "customer@example.com",
  customerName: "Customer Name",
  vehicleName: "Toyota Land Cruiser",
  appointmentDate: "2026-07-15",
  appointmentTime: "10:00",
  reference: "TD-12345",
};
```

## Done Criteria

- Notification payload shape is defined.
- Required environment variables are identified.
- Notification provider decision is documented or deferred.
- No outbound email is sent yet unless provider configuration is confirmed.

---

# Phase 2 — Notification Provider Configuration

## Objective

Add a backend utility configuration block for transactional email sending.

## Files/Directories In This Phase

```text
backend/config/email.js
backend/services/notificationService.js
backend/.env
backend/package.json
```

## Possible Provider Options

```text
Nodemailer
SendGrid
Other team-approved transactional email provider
```

## Expected Environment Variables

For Nodemailer-style setup:

```text
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_FROM=
```

For SendGrid-style setup:

```text
SENDGRID_API_KEY=
EMAIL_FROM=
```

## Implementation Notes

The provider should be wrapped behind a service function so future provider changes do not affect route/controller logic.

Suggested service function:

```js
sendAppointmentConfirmationEmail(payload)
```

## Done Criteria

- Email provider configuration file exists.
- Notification service file exists.
- Secrets are read from environment variables.
- No hardcoded credentials are committed.
- Service can be called from booking/schedule confirmation logic.

---

# Phase 3 — Appointment Confirmation Notification Trigger

## Objective

Trigger the notification dispatcher when a booking or schedule log is confirmed.

## Files/Directories In This Phase

```text
backend/routes/
backend/controllers/
backend/services/notificationService.js
backend/models/
backend/server.js
```

## Backend Route To Inspect Or Coordinate

```text
POST /api/test-drives
```

or the team-confirmed appointment booking route.

## Expected Behavior

When an appointment booking is confirmed:

1. Backend validates the appointment payload.
2. Backend saves or confirms the schedule log.
3. Backend calls the notification service.
4. Customer receives a confirmation email.
5. API response remains clean and does not expose provider internals.

## Failure Behavior

If notification dispatch fails after the booking is confirmed, the backend should not corrupt or undo the successful booking automatically unless the team explicitly requires transactional rollback.

Recommended response strategy:

- Booking success remains successful.
- Notification failure is logged server-side.
- Response can include a safe warning if needed.

## Done Criteria

- Notification service is called only after booking confirmation.
- Missing recipient email is handled safely.
- Provider errors are caught and logged.
- API response does not leak sensitive provider details.
- No duplicate booking route is added if another teammate owns it.

---

# Phase 4 — Notification Message Template

## Objective

Create a clean transactional email template for appointment confirmation.

## Files/Directories In This Phase

```text
backend/services/notificationService.js
backend/templates/
backend/templates/appointmentConfirmation.js
```

## Template Content Should Include

- Customer greeting
- Confirmation that appointment was booked
- Vehicle name or vehicle identifier
- Appointment date
- Appointment time
- Dealership contact details if available
- Friendly message that the dealership team will follow up if needed

## Template Should Avoid

- Exposing database IDs unnecessarily
- Exposing JWT or session data
- Overly technical backend/internal language
- Hardcoded customer information

## Done Criteria

- Appointment confirmation template exists.
- Template accepts dynamic payload values.
- Template is reusable by the notification service.
- Template does not expose sensitive internal fields.

---

# Phase 5 — Defensive Payload Cleaner Contract Planning

## Objective

Define the validation layer contract for incoming inventory upload and car creation payloads.

## Files/Directories In This Phase

```text
backend/middleware/
backend/utils/
backend/routes/carsRoutes.js
backend/controllers/carsController.js
backend/models/carsModel.js
```

## Planned Files

```text
backend/middleware/validateCarPayload.js
backend/utils/cleanPayload.js
```

## Fields To Validate

Inventory forms may include:

- Make
- Model
- Name
- Brand
- Type
- Category
- Year
- Price
- Mileage
- Power
- Engine
- Drive
- Images
- Status

## Numeric Fields Requiring Strict Validation

```text
price
mileage
year
```

## Done Criteria

- Validation target route is identified.
- Required fields are confirmed.
- Numeric fields are identified.
- Middleware placement is planned.
- No database write logic is modified yet.

---

# Phase 6 — Defensive Payload Cleaner Middleware

## Objective

Create middleware that rejects malicious or badly typed inventory submissions before controller/model logic runs.

## Files/Directories In This Phase

```text
backend/middleware/validateCarPayload.js
backend/routes/carsRoutes.js
```

## Validation Rules

The middleware should reject:

- Missing required text fields.
- Empty strings for required fields.
- String injection into numeric fields.
- Non-numeric price.
- Price less than or equal to zero.
- Non-numeric mileage.
- Mileage less than zero.
- Invalid year.
- Malformed image payload if images are included.

## Required Error Style

Errors should be explicit and safe.

Example messages:

```text
Price must be a valid positive number.
Mileage must be a valid non-negative number.
Year must be valid.
Make is required.
Model is required.
```

## Done Criteria

- Middleware file exists.
- Numeric validation is strict.
- Invalid payloads return 400 responses.
- Controller does not run for invalid payloads.
- Middleware is reusable and isolated.

---

# Phase 7 — Attach Payload Cleaner To Inventory Routes

## Objective

Connect the validation middleware to the inventory creation or upload route without altering unrelated backend routes.

## Files/Directories In This Phase

```text
backend/routes/carsRoutes.js
backend/middleware/validateCarPayload.js
backend/controllers/carsController.js
```

## Target Routes

```text
POST /api/cars
POST /api/cars/upload
```

The upload endpoint should only be connected if it already exists or if the team has approved adding it.

## Expected Route Pattern

```js
router.post("/", requireAuth, requireAdmin, validateCarPayload, addCar);
```

If `requireAuth` and `requireAdmin` are not finalized, add TODOs and avoid inventing conflicting middleware names.

## Done Criteria

- Validation middleware is attached to the correct inventory route.
- Invalid numeric payloads are rejected before database operations.
- No unrelated routes are modified.
- Admin auth middleware integration is coordinated with the backend owner.

---

# Phase 8 — Payload Cleaner Tests And HTTP Samples

## Objective

Create manual or automated checks for valid and invalid inventory payloads.

## Files/Directories In This Phase

```text
src/tests/cars.http
backend/tests/
backend/routes/carsRoutes.js
```

## Test Cases

Valid payload:

- Numeric price
- Numeric mileage
- Valid year
- Required strings present

Invalid payloads:

- Price as text
- Price as empty string
- Price less than or equal to zero
- Mileage as text
- Mileage below zero
- Year as text
- Missing make/model/name fields
- Malicious script string in numeric field

## Example Invalid Payload

```json
{
  "make": "Toyota",
  "model": "Harrier",
  "year": 2024,
  "price": "abc<script>",
  "mileage": "50000"
}
```

Expected response:

```text
400 Bad Request
Price must be a valid positive number.
```

## Done Criteria

- Valid payload test exists.
- Invalid numeric tests exist.
- Expected 400 responses are documented.
- Manual testing can be repeated by teammates.

---

# Phase 9 — Notification Tests And Failure Handling

## Objective

Verify notification dispatch behavior and failure handling.

## Files/Directories In This Phase

```text
backend/services/notificationService.js
backend/templates/appointmentConfirmation.js
backend/controllers/
backend/routes/
src/tests/
```

## Test Scenarios

- Booking confirmation with valid email triggers notification.
- Booking confirmation with missing email is handled safely.
- Email provider failure is caught and logged.
- API does not expose provider secrets.
- Notification service can be disabled or mocked in development if needed.

## Done Criteria

- Notification success path is testable.
- Notification failure path is safe.
- No credentials are exposed.
- API response remains stable.

---

# Phase 10 — Environment And Security Review

## Objective

Confirm secrets, tokens, and provider keys are handled safely.

## Files/Directories In This Phase

```text
backend/.env
backend/.gitignore
backend/config/email.js
backend/services/notificationService.js
backend/middleware/validateCarPayload.js
```

## Review Items

- Email credentials are not committed.
- `.env` is ignored by git.
- Error messages do not leak secrets.
- Validation does not mutate trusted data unexpectedly.
- Notification logs avoid sensitive data.
- Backend routes do not expose internals.

## Done Criteria

- No secrets are committed.
- Environment variables are documented.
- Sensitive provider errors are not returned to users.
- Validation and notification utilities are safe for review.

---

# Phase 11 — Final Sprint 3 Backend PR Readiness

## Objective

Confirm Edwin’s Sprint 3 backend API work is ready for review.

## Files/Directories In This Phase

```text
backend/server.js
backend/routes/
backend/controllers/
backend/models/
backend/middleware/
backend/services/
backend/config/
backend/utils/
src/tests/
README.md
```

## Checklist

- [ ] Active branch is correct.
- [ ] Latest origin branch was pulled with `--ff-only`.
- [ ] Notification service is isolated.
- [ ] Notification template is reusable.
- [ ] Booking confirmation trigger is coordinated with booking route owner.
- [ ] Payload cleaner middleware is isolated.
- [ ] Numeric price validation blocks strings.
- [ ] Numeric mileage validation blocks strings.
- [ ] Invalid payload responses are explicit and safe.
- [ ] No duplicate backend server was added.
- [ ] No credentials were committed.
- [ ] Manual HTTP tests exist or are documented.
- [ ] Branch is clean.

## Final Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
git status
git pull --ff-only origin <current-branch>
npm run build
git status
git log --oneline -8
```

## Done Criteria

- Backend notification requirement is implemented or safely scaffolded.
- Defensive payload validation requirement is implemented.
- Required tests or HTTP examples exist.
- Backend ownership conflicts are avoided.
- PR description clearly explains what was completed and what remains dependent on team endpoints.

---

# Implementation Dependencies To Confirm With Team

Before connecting final backend behavior, confirm:

- The active backend entrypoint.
- The confirmed booking route for appointment/test-drive confirmation.
- Whether Nodemailer or SendGrid should be used.
- Required production email sender.
- Final inventory creation route request body.
- Final upload endpoint ownership.
- Final admin JWT middleware name.
- Final user role field in JWT payload.
- Whether backend tests should be added under `backend/tests/` or manual `.http` files.

---

# Sprint 3 Completion Summary Template

Use this summary once implementation is complete:

```text
Implemented Edwin’s Sprint 3 backend API requirements.

The notification dispatcher prepares and sends appointment confirmation messages after schedule confirmation. The defensive payload cleaner validates incoming car inventory payloads before database writes and rejects invalid numeric fields such as price and mileage. Backend integration was kept modular, with provider configuration and validation rules isolated for maintainability.
```
