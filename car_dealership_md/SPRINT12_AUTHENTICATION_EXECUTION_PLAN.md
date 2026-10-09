# Car Dealership Sprint 12 Authentication Execution Plan

## Document Control

- **Assigned developer:** Edwin Kambale
- **Task ID:** TSK-001
- **Sprint:** 12
- **Working title:** Secure Authentication, Account Recovery, Email Verification, and Session Protection
- **Repository:** `/home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership`
- **Starting branch:** `feature/edwin-sprint11-admin-operations`
- **Required Sprint 12 branch:** `feature/edwin-sprint12-secure-authentication`
- **Execution model:** Sequential phase gates
- **Implementation status:** Not started

## Sprint Objective

Improve the dealership application's login and registration experience through stronger validation, secure password handling, safe and useful error feedback, password recovery, email verification, and reliable user-session protection. Preserve the existing canonical authentication context, route guards, role checks, bearer-token API contracts, and previous sprint functionality.

## Inspection Summary

The repository already contains:

- A React and TypeScript frontend built with Vite.
- An Express and PostgreSQL backend.
- Existing login, registration, session verification, bearer-token handling, protected routes, admin routes, password-change functionality, email configuration, and authentication tests.
- Frontend authentication code under `src/features/auth/` and `src/app/context/auth.tsx`.
- Backend authentication code under `backend/controllers/authController.js`, `backend/routes/authRoutes.js`, `backend/middleware/authMiddleware.js`, `backend/models/`, and `backend/utils/jwt.js`.
- Existing manual tests for storage, session restoration, authentication services, protected routes, persistence, password validation, and password changes.

The inspection also exposed risks that Sprint 12 must address:

- Duplicate legacy login and registration pages exist beside the canonical feature-based pages.
- Tokens are stored in browser local storage under a canonical key with legacy-key cleanup support.
- Password reset and email verification flows are not implemented end to end.
- Current login throttling uses an in-memory map and is not suitable as the sole production control.
- Authentication failures previously reached HTTP 500 when the database configuration or `users` relation was unavailable.
- A token-generating utility and a hard-coded token in a backend helper require security review and removal from production-tracked workflows.
- Both `backend/models/User.js` and `backend/models/userModel.js` exist and require reconciliation before schema changes.

## Non-Negotiable Security Rules

1. Do not weaken or remove existing authentication, administrator authorization, protected-route, or role controls.
2. Never log passwords, raw access tokens, reset tokens, verification tokens, authorization headers, or complete authentication payloads.
3. Store reset and verification tokens only as cryptographic hashes in the database.
4. Reset and verification tokens must be single-use and time-limited.
5. Password hashing must remain on the backend. The frontend must never hash passwords as a substitute for transport security.
6. Authentication responses must not reveal whether an email address exists.
7. Validation must run on both frontend and backend, with backend validation authoritative.
8. Any session invalidated by password reset, password change, account disabling, or token-version rotation must lose access to protected routes.
9. No secret values may be committed. Only variable names and safe examples belong in `.env.example` files.
10. No pull request may be created until every required test and build passes without shell errors.

---

# Phase 1: Sprint Baseline, Upstream Review, and Branch Establishment

## Exclusive Objectives

- Preserve the clean Sprint 11 completion point.
- Fetch and inspect current `origin` and `upstream` changes before starting Sprint 12.
- Review upstream authentication-related changes and determine whether integration is required.
- Create the dedicated Sprint 12 development branch from the verified baseline.
- Capture the starting commit, branch, dependency state, and clean working tree.

## Files to Create

- `docs/sprint12/SPRINT12_BASELINE_AND_SCOPE.md`
- `docs/sprint12/UPSTREAM_AUTH_INTEGRATION_REVIEW.md`

## Files to Modify

- None unless upstream integration is proven necessary after review.

## Gate Requirements

- Current Sprint 11 branch is clean and pushed.
- `origin` and `upstream` fetches succeed.
- Incoming upstream authentication scope is documented before any merge or rebase.
- Branch `feature/edwin-sprint12-secure-authentication` exists from the approved baseline.
- Baseline evidence is saved in the project evidence directory.

## Commit Checkpoint

```text
chore: establish Sprint 12 secure authentication baseline
```

---

# Phase 2: Canonical Authentication Contract and Data Model

## Exclusive Objectives

- Define one authoritative authentication contract for login, registration, session verification, logout, email verification, verification resend, forgot-password, and reset-password flows.
- Reconcile the duplicate backend user-model files and select one canonical PostgreSQL-backed user model or repository path.
- Define user verification state, token expiry, session invalidation, and audit-safe response shapes.
- Preserve role information required by existing administrator authorization.

## Files to Create

- `backend/contracts/auth.contract.js`
- `backend/utils/authValidation.js`
- `backend/repositories/authRepository.js`
- `backend/scripts/ensureAuthSecuritySchema.js`
- `docs/sprint12/AUTHENTICATION_CONTRACT.md`

## Files to Modify

- `backend/models/User.js`
- `backend/models/userModel.js`
- `backend/config/db.js`
- `backend/server.js`
- `src/features/auth/types/auth.types.ts`
- `src/features/auth/services/authApi.ts`
- `src/features/auth/services/index.ts`
- `backend/.env.example`
- `.env.example`

## Data Requirements

The canonical user source must support equivalent fields for:

- Email verification status and timestamp.
- Hashed email-verification token and expiry.
- Hashed password-reset token and expiry.
- Session or token version.
- Password-updated timestamp.
- Failed-login counters or a durable rate-limit integration point.
- Optional lockout expiry where implemented.

## Gate Requirements

- Only one canonical user persistence path is used by authentication controllers.
- Database initialization creates or safely migrates required authentication fields.
- Existing users remain compatible.
- No plaintext recovery or verification token is stored.
- API response and error contracts are documented.

## Commit Checkpoint

```text
feat: define secure authentication contracts and persistence
```

---

# Phase 3: Registration Validation and Email Verification

## Exclusive Objectives

- Strengthen registration validation on both frontend and backend.
- Normalize email addresses consistently.
- Enforce a documented password policy.
- Prevent duplicate registration without exposing sensitive account details.
- Generate a cryptographically secure email-verification token.
- Store only the token hash and expiry.
- Send a verification link through the existing email configuration.
- Implement verification and resend flows with generic, enumeration-safe responses.

## Files to Create

- `backend/services/authTokenService.js`
- `backend/services/authEmailService.js`
- `backend/templates/emailVerification.js`
- `src/features/auth/components/EmailVerificationNotice.tsx`
- `src/features/auth/components/VerifyEmailResult.tsx`
- `src/features/auth/components/ResendVerificationForm.tsx`
- `src/pages/VerifyEmail/VerifyEmailPage.tsx`
- `src/features/auth/validation/authValidation.ts`
- `backend/tests/authRegistration.manual.js`
- `backend/tests/authEmailVerification.manual.js`
- `src/tests/authRegistration.manual.ts`
- `src/tests/emailVerification.manual.ts`

## Files to Modify

- `backend/controllers/authController.js`
- `backend/routes/authRoutes.js`
- `backend/config/email.js`
- `backend/models/User.js` or the canonical user-model file selected in Phase 2
- `src/features/auth/components/RegisterForm.tsx`
- `src/features/auth/services/authApi.ts`
- `src/features/auth/services/authService.ts`
- `src/features/auth/types/auth.types.ts`
- `src/app/App.tsx`
- `src/app/routes.tsx`
- `src/pages/Register/RegisterPage.tsx`
- `src/pages/Register.tsx`
- `package.json`
- `backend/package.json`

## Validation Rules

- Trim names and reject empty normalized values.
- Lowercase and normalize email addresses.
- Validate email format and maximum length.
- Enforce password length and strength without silently truncating input.
- Require password confirmation on the frontend.
- Reject known-invalid and oversized payloads.
- Return field-level frontend feedback and safe backend errors.
- Verification links must expire and become unusable after successful verification.

## Gate Requirements

- Registration succeeds only with valid input.
- Duplicate email handling is safe and consistent.
- Verification email dispatch is testable without exposing the raw token in logs.
- Expired, malformed, reused, and valid verification-token paths are covered.
- Existing login behavior is not broken.

## Commit Checkpoint

```text
feat: secure registration and add email verification
```

---

# Phase 4: Login Hardening and Error Feedback

## Exclusive Objectives

- Apply consistent login validation.
- Prevent account enumeration through login responses.
- Improve accessible frontend error feedback.
- Replace or reinforce the process-local login-attempt map with a production-appropriate abstraction or clearly bounded fallback.
- Define the policy for unverified accounts without weakening administrator or user access controls.
- Preserve redirect behavior after successful authentication.

## Files to Create

- `backend/middleware/authRateLimit.js`
- `src/features/auth/components/AuthFieldError.tsx`
- `src/tests/authLoginValidation.manual.ts`
- `backend/tests/authLoginSecurity.manual.js`

## Files to Modify

- `backend/controllers/authController.js`
- `backend/middleware/authMiddleware.js`
- `backend/routes/authRoutes.js`
- `src/features/auth/components/LoginForm.tsx`
- `src/features/auth/services/authApi.ts`
- `src/features/auth/services/authService.ts`
- `src/features/auth/validation/authValidation.ts`
- `src/pages/Login/LoginPage.tsx`
- `src/pages/Login.tsx`
- `src/app/components/auth/PublicOnlyRoute.tsx`
- `package.json`
- `backend/package.json`

## Gate Requirements

- Invalid credentials return one generic public response.
- Rate-limited requests return a stable status and safe retry guidance.
- Form errors are associated with fields and announced accessibly.
- Submission is disabled while a request is active.
- No password or token appears in logs, errors, or test output.
- Valid redirect parameters are preserved safely and open redirects are rejected.

## Commit Checkpoint

```text
feat: harden login validation and error handling
```

---

# Phase 5: Password Reset and Account Recovery

## Exclusive Objectives

- Add a complete forgot-password and reset-password workflow.
- Return the same public result whether an account exists or not.
- Generate secure, single-use, expiring reset tokens.
- Store only token hashes.
- Revoke existing sessions after a successful password reset.
- Reuse the canonical password policy and avoid duplicating validation logic.

## Files to Create

- `backend/templates/passwordReset.js`
- `src/features/auth/components/ForgotPasswordForm.tsx`
- `src/features/auth/components/ResetPasswordForm.tsx`
- `src/pages/ForgotPassword/ForgotPasswordPage.tsx`
- `src/pages/ResetPassword/ResetPasswordPage.tsx`
- `backend/tests/passwordReset.manual.js`
- `src/tests/passwordReset.manual.ts`

## Files to Modify

- `backend/controllers/authController.js`
- `backend/routes/authRoutes.js`
- `backend/services/authTokenService.js`
- `backend/services/authEmailService.js`
- `backend/repositories/authRepository.js`
- `backend/models/User.js` or the canonical model selected in Phase 2
- `src/features/auth/components/LoginForm.tsx`
- `src/features/auth/services/authApi.ts`
- `src/features/auth/services/authService.ts`
- `src/features/auth/services/index.ts`
- `src/features/auth/types/auth.types.ts`
- `src/features/auth/validation/authValidation.ts`
- `src/app/App.tsx`
- `src/app/routes.tsx`
- `src/features/profile/utils/passwordValidation.ts`
- `package.json`
- `backend/package.json`

## Gate Requirements

- Forgot-password responses are enumeration-safe.
- Reset tokens expire, are single-use, and are stored only as hashes.
- New passwords satisfy the canonical policy.
- Successful reset invalidates prior sessions.
- Invalid, expired, reused, and valid reset-token paths are tested.
- Reset links do not expose tokens through application logs.

## Commit Checkpoint

```text
feat: implement secure password recovery flow
```

---

# Phase 6: Session Protection and Token Lifecycle

## Exclusive Objectives

- Strengthen session verification without bypassing the existing canonical auth context.
- Make password reset, password change, and account-state changes invalidate previous tokens.
- Centralize unauthorized-session cleanup.
- Preserve administrator role enforcement.
- Remove reliance on legacy direct local-storage checks from active application paths where the canonical context is available.
- Review token storage risk and document the approved migration path if HttpOnly cookies are outside current team scope.

## Files to Create

- `backend/services/sessionService.js`
- `src/features/auth/services/sessionGuard.ts`
- `src/tests/sessionProtection.manual.ts`
- `backend/tests/sessionProtection.manual.js`
- `docs/sprint12/SESSION_SECURITY_DECISION.md`

## Files to Modify

- `backend/utils/jwt.js`
- `backend/middleware/authMiddleware.js`
- `backend/controllers/authController.js`
- `backend/routes/authRoutes.js`
- `backend/repositories/authRepository.js`
- `src/app/context/auth.tsx`
- `src/app/components/auth/ProtectedRoute.tsx`
- `src/app/components/auth/AdminRoute.tsx`
- `src/app/components/auth/PublicOnlyRoute.tsx`
- `src/app/components/auth/routeAccess.ts`
- `src/features/auth/services/authStorage.ts`
- `src/features/auth/services/authService.ts`
- `src/features/auth/services/authApi.ts`
- `src/api/client.ts`
- `src/app/lib/auth.ts`
- `src/utils/routeGuards.js`
- `src/app/components/test-drive/TestDriveScheduler.tsx`
- `src/features/profile/services/passwordApi.ts`
- `src/features/profile/hooks/usePasswordChange.ts`
- `src/tests/authBootstrap.manual.ts`
- `src/tests/authPersistence.manual.ts`
- `src/tests/authService.manual.ts`
- `src/tests/authStorage.manual.ts`
- `src/tests/protectedRoute.manual.ts`
- `package.json`
- `backend/package.json`

## Gate Requirements

- Expired, malformed, revoked, and version-mismatched tokens are rejected.
- Password reset and password change invalidate prior sessions.
- Unauthorized API responses clear the canonical local session safely.
- Protected and administrator routes remain inaccessible without valid authorization.
- Tokens are never returned in error objects or logs.
- Legacy auth keys are removed during logout and invalid-session cleanup.

## Commit Checkpoint

```text
feat: enforce session revocation and protected access
```

---

# Phase 7: Security Cleanup and Duplicate-Flow Reconciliation

## Exclusive Objectives

- Ensure only the canonical login and registration pages are routed.
- Remove or isolate obsolete authentication implementations without deleting required compatibility code prematurely.
- Remove tracked hard-coded token usage and prevent accidental credential leakage.
- Review generated token utilities and restrict them to safe local development use or remove them.
- Confirm environment and ignore rules protect secrets, logs, and local artifacts.

## Files to Create

- `docs/sprint12/AUTH_SECURITY_REVIEW.md`
- `docs/sprint12/AUTH_ROLLBACK_PLAN.md`

## Files to Modify

- `src/pages/Login.tsx`
- `src/pages/Register.tsx`
- `src/pages/Login/LoginPage.tsx`
- `src/pages/Register/RegisterPage.tsx`
- `src/app/App.tsx`
- `src/app/routes.tsx`
- `backend/download-pdf.js`
- `backend/generate-token.js`
- `.gitignore`
- `backend/.gitignore`
- `README.md`

## Gate Requirements

- A single routed login flow and a single routed registration flow remain.
- No hard-coded bearer token remains in tracked production code.
- Local `.env` files, runtime logs, and generated reports are not newly committed.
- No existing protected route or admin role check is removed.
- Rollback instructions identify the last known-good commit and schema rollback considerations.

## Commit Checkpoint

```text
security: remove legacy auth risks and reconcile flows
```

---

# Phase 8: End-to-End Authentication Validation

## Exclusive Objectives

- Validate all Sprint 12 authentication paths and previous-sprint regressions.
- Test database-backed registration, login, email verification, recovery, reset, session restoration, invalidation, and protected-route behavior.
- Verify accessible form behavior and user feedback.
- Confirm the production build succeeds.
- Record every command and complete output in evidence files.

## Files to Create

- `src/tests/authValidation.manual.ts`
- `src/tests/authRecovery.manual.ts`
- `src/tests/authAccessibility.manual.ts`
- `backend/tests/authEndpoints.manual.js`
- `src/tests/sprint12-auth.http`
- `docs/sprint12/SPRINT12_VALIDATION_REPORT.md`
- `docs/sprint12/SPRINT12_SECURITY_CHECKLIST.md`

## Files to Modify

- `package.json`
- `backend/package.json`
- `src/tests/sprint10-required-endpoints.http`
- `src/requests.http`
- `README.md`

## Required Validation Groups

### Frontend targeted validation

- Registration validation.
- Login validation and generic error handling.
- Verification status and resend behavior.
- Forgot-password and reset-password handling.
- Session restoration and invalid-session cleanup.
- Protected-route and administrator-route enforcement.
- Accessibility announcements, labels, focus behavior, and disabled submission states.

### Backend targeted validation

- Registration and duplicate-account handling.
- Password hashing and comparison.
- Verification-token issue, expiry, one-time use, and resend.
- Password-reset token issue, expiry, one-time use, and session revocation.
- Login throttling behavior.
- Session endpoint and token-version enforcement.
- Database-unavailable and missing-schema error normalization.

### Regression validation

Run all existing authentication, protected-route, persistence, profile, password, booking, API configuration, administrator operations, and build checks that are relevant to the changed surface.

## Gate Requirements

- Every required test command exits successfully.
- No shell errors occur.
- No secret or token appears in evidence output.
- Frontend and backend builds/startup checks succeed as applicable.
- Database-backed API tests produce expected status codes.
- A clean `git status` is obtained after the validation commit.

## Commit Checkpoint

```text
test: validate Sprint 12 authentication security
```

---

# Phase 9: Upstream Reinspection, Final Documentation, and Handoff

## Exclusive Objectives

- Fetch and inspect collaborator changes received during Sprint 12.
- Review incoming scope before integrating anything.
- Integrate only compatible changes and rerun affected validations afterward.
- Finalize the Sprint 12 implementation report and pull-request checklist.
- Push the completed branch to Edwin's fork.
- Create a pull request only when all required checks pass and no unresolved errors remain.

## Files to Create

- `docs/sprint12/FINAL_SPRINT12_REPORT.md`
- `docs/sprint12/SPRINT12_PULL_REQUEST_CHECKLIST.md`
- `docs/sprint12/FINAL_UPSTREAM_INTEGRATION_REVIEW.md`

## Files to Modify

- `README.md`
- Any Sprint 12 source or test files affected by a reviewed and approved upstream integration.

## Final Gate Requirements

- All Sprint 12 objectives are implemented.
- All required validation groups pass.
- Upstream changes have been fetched and reviewed.
- Any integration is documented and validated afterward.
- The final branch is clean and pushed to `origin`.
- The final commit is verified on the remote branch.
- The pull request targets the parent integration repository branch selected by the integration lead.
- No direct merge to `main` is performed by Edwin.

## Final Commit Checkpoint

```text
docs: finalize Sprint 12 secure authentication handoff
```

---

# Planned Authentication Endpoints

The final route names must follow the approved contract from Phase 2. The expected endpoint set is:

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/session
POST /api/auth/logout
GET  /api/auth/verify-email
POST /api/auth/resend-verification
POST /api/auth/forgot-password
POST /api/auth/reset-password
```

If logout remains stateless, the endpoint must still provide a clear client contract or be omitted explicitly in the Phase 2 decision record. Session invalidation must still occur after password reset and password change through token versioning or an equivalent server-side control.

# Expected Environment Variables

Add only variables required by the approved implementation. Likely additions include:

```text
AUTH_VERIFICATION_TOKEN_TTL_MINUTES
AUTH_RESET_TOKEN_TTL_MINUTES
AUTH_LOGIN_WINDOW_MS
AUTH_LOGIN_MAX_ATTEMPTS
AUTH_LOCKOUT_MINUTES
AUTH_JWT_EXPIRES_IN
AUTH_PASSWORD_MIN_LENGTH
```

Actual values must be configured locally or through deployment secrets. No real secret may be written into tracked example files.

# Evidence and Output Rules

Every terminal command batch and its complete output must be saved directly in:

```text
/home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/
```

Use descriptive filenames such as:

```text
sprint12_phase1_baseline_and_branch.txt
sprint12_phase2_auth_contract_validation.txt
sprint12_phase3_registration_verification_tests.txt
sprint12_phase4_login_hardening_tests.txt
sprint12_phase5_password_reset_tests.txt
sprint12_phase6_session_protection_tests.txt
sprint12_phase7_security_cleanup_review.txt
sprint12_phase8_full_validation.txt
sprint12_phase9_final_upstream_review.txt
sprint12_final_push_and_remote_verification.txt
```

Do not report a phase as passed when an underlying command failed. Targeted checks and overall validation status must remain clearly separated.

# Git Execution Policy

1. Work only on `feature/edwin-sprint12-secure-authentication`.
2. Inspect the current file before modifying it.
3. Make minimal, reversible changes.
4. Validate each phase before committing.
5. Push every completed phase commit to Edwin's fork.
6. Periodically fetch and inspect the parent integration repository.
7. Review incoming scope before integrating changes.
8. Rerun affected tests after integration.
9. Do not create a pull request while any required validation fails.
10. Do not merge directly to `main`.

# Definition of Done

Sprint 12 is complete only when:

- Login and registration validation is consistent and accessible.
- Passwords are validated and hashed securely on the backend.
- Authentication errors are useful without exposing account existence or secrets.
- Email verification works end to end.
- Password recovery and reset work end to end.
- Recovery and verification tokens are hashed, expiring, and single-use.
- Successful password reset and password change invalidate prior sessions.
- Protected and administrator routes reject invalid sessions.
- Duplicate and obsolete auth flows are reconciled safely.
- Hard-coded tracked bearer tokens are removed.
- Targeted tests, regression tests, backend checks, and production build all pass.
- Upstream changes are reviewed and any integration is validated.
- Documentation, evidence, commits, remote push, and pull-request checklist are complete.

# Immediate Next Action

Begin with **Phase 1 only**. Establish and verify the Sprint 12 branch, capture the baseline, inspect current upstream authentication changes, and stop at the Phase 1 gate before modifying authentication source code.
