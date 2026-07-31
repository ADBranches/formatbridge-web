# Edwin Sprint 5 Development Timeline

## Frontend Dev #2: State Cleanup and Deployment Build

**Project:** Car Dealership Website  
**Sprint:** Sprint 5  
**Owner:** Edwin  
**Primary focus:** Authentication state persistence, production build optimization, environment compilation, launch validation, and pull request readiness.

---

## 1. Sprint Objectives

### Objective A: Global Authentication State Persistence Router

Keep authenticated users signed in across page refreshes and browser restarts by restoring a valid stored session during application startup.

The implementation must:

- inspect browser storage for an existing JWT;
- verify the token through the backend API owned by Devine;
- restore the authenticated user's global state when verification succeeds;
- prevent protected-route redirects while session restoration is still running;
- clear expired, malformed, or rejected sessions safely;
- route unauthenticated users to the login experience;
- preserve the intended protected destination where practical.

### Objective B: Production Build Optimization and Environment Compilation

Produce a minimized, deployable frontend bundle that uses the hosted production API instead of local testing endpoints.

The implementation must:

- audit dependencies and remove unused packages safely;
- remove unused imports and unreachable frontend code;
- centralize API base URL handling;
- replace hardcoded local endpoints with Vite environment variables;
- confirm production minification and bundle behavior;
- validate the final build against the secured backend API;
- ensure no credentials or private tokens are bundled into client assets.

### Cross-Functional Objective: Launch Drill

Edwin must generate and validate the final frontend bundle while:

- Devine runs the secured production-ready API;
- Ronald and Max prepare representative database data;
- Edward verifies compressed images and URL-synchronized inventory filters;
- the team confirms the production frontend runs without browser-console errors.

---

## 2. Delivery Strategy

This timeline prioritizes implementation speed while preserving safety:

1. Inspect before editing.
2. Implement authentication restoration before broader build cleanup.
3. Use targeted tests before the full production build.
4. Keep environment configuration centralized.
5. Validate the launch flow before writing final PR documentation.
6. Commit each meaningful phase separately for easier review and rollback.

### Phase Gate Rule

At the end of each phase:

- run the targeted checks;
- confirm the working tree changes match that phase only;
- commit the phase;
- pause for instructions before beginning the next phase.

---

# Phase 0: Sprint 5 Baseline Inspection

## Objective

Understand the current frontend authentication, routing, API-client, storage, environment, dependency, and build structure before changing files.

## Files and Directories to Inspect

```text
package.json
package-lock.json
vite.config.js
vite.config.ts
src/
src/main.*
src/App.*
src/context/
src/contexts/
src/store/
src/routes/
src/router/
src/components/
src/pages/
src/services/
src/api/
src/utils/
src/hooks/
src/tests/
.env.example
.gitignore
README.md
```

Only paths that actually exist should be used. Do not create replacement architecture until the current structure has been inspected.

## Development Tasks

- Confirm the active frontend entrypoint.
- Identify the router implementation and protected-route logic.
- Identify the login and logout flows.
- Locate JWT read, write, and clear behavior.
- Identify the current global authentication state mechanism.
- Locate all API clients and hardcoded backend URLs.
- Identify current Vite environment variables.
- Inspect build scripts and Vite configuration.
- Inspect frontend tests and test tooling.
- Record the active feature branch and baseline build result.

## Validation

- Current branch is correct.
- Working tree is clean.
- Existing frontend build result is recorded.
- Existing targeted authentication tests are identified.
- No files are modified in this phase.

## Done Criteria

- Authentication architecture is mapped.
- Routing architecture is mapped.
- Token storage location is confirmed.
- API base URL usage is mapped.
- Build tooling is confirmed.
- Exact Phase 1 files are known.

---

# Phase 1: Authentication Persistence Contract

## Objective

Define the session-restoration rules and frontend authentication state contract before implementation.

## Files and Directories to Update or Create

```text
src/types/auth.*
src/utils/authStorage.*
src/services/authService.*
src/api/auth.*
README.md
```

Use existing equivalent files if the project already has them. Avoid duplicate authentication utilities.

## Contract to Define

The frontend authentication state should clearly represent:

```text
user
accessToken or session reference
isAuthenticated
isRestoringSession
isAuthReady
error
```

The startup flow should be:

1. Application starts.
2. Authentication state enters restoration mode.
3. Stored token is read.
4. Missing token ends restoration as unauthenticated.
5. Existing token is sent to the backend verification endpoint.
6. Valid response restores the authenticated user.
7. Invalid or expired response clears stored session data.
8. Authentication state becomes ready.
9. Router renders the correct public or protected destination.

## Safety Rules

- Do not decode a JWT and treat the decoded payload as proof of validity.
- Backend verification remains authoritative.
- Never log JWT values.
- Never place private backend secrets in frontend environment files.
- Clear malformed or rejected tokens safely.
- Avoid redirecting the user before restoration completes.

## Team Dependency

Confirm with Devine:

```text
verification endpoint
HTTP method
Authorization header format
success response shape
invalid-token status code
expired-token status code
restored user object shape
refresh-token behavior, if any
```

## Done Criteria

- Session restoration states are defined.
- Token storage behavior is defined.
- Backend verification contract is documented.
- Invalid-session behavior is defined.
- No routing race condition is permitted by the contract.

---

# Phase 2: Authentication Storage and Verification Service

## Objective

Implement a single safe path for reading, verifying, persisting, and clearing frontend authentication sessions.

## Files and Directories to Update or Create

```text
src/utils/authStorage.*
src/services/authService.*
src/api/client.*
src/api/auth.*
src/types/auth.*
src/tests/authStorage.*
src/tests/authService.*
```

## Development Tasks

- Add typed token/session storage helpers.
- Centralize storage key names.
- Add token read, write, and clear functions.
- Add backend session verification call.
- Normalize successful verification responses.
- Normalize unauthorized and expired-session responses.
- Ensure verification failures do not expose raw tokens.
- Ensure API requests consistently attach the authorization header.
- Keep network and storage concerns separate from UI components.

## Expected Functions

Names should follow the existing project conventions. Likely responsibilities include:

```text
getStoredSession()
saveSession(session)
clearStoredSession()
verifySession(token)
getAuthenticatedUser()
```

## Targeted Tests

- Missing token returns no session.
- Valid stored session can be read.
- Session save writes the expected storage record.
- Session clear removes the expected storage record.
- Verification sends the expected authorization header.
- Unauthorized verification clears the session.
- Network failure does not falsely authenticate the user.
- No token appears in logs or user-facing errors.

## Done Criteria

- Authentication storage helper exists.
- Verification service exists.
- Invalid sessions are safely cleared.
- Token handling is centralized.
- Targeted storage and service tests pass.

---

# Phase 3: Global Authentication Bootstrap State

## Objective

Restore valid sessions automatically when the application starts and expose a stable global authentication state to the router and UI.

## Files and Directories to Update or Create

```text
src/context/AuthContext.*
src/contexts/AuthContext.*
src/store/authStore.*
src/providers/AuthProvider.*
src/hooks/useAuth.*
src/main.*
src/App.*
```

Update the existing global-state solution rather than creating a competing provider or store.

## Development Tasks

- Add the session-restoration lifecycle.
- Start with `isAuthReady` false or equivalent.
- Read the stored token once during application bootstrap.
- Verify the token through the authentication service.
- Restore the user on successful verification.
- Clear the session on invalid or expired verification.
- End restoration in a `finally` path.
- Expose login, logout, restore, and authentication readiness actions.
- Prevent duplicate verification calls caused by development rendering behavior.

## Expected Behavior

- A valid session is restored without manual login.
- A missing session reaches the public application quickly.
- An invalid session is removed and does not create a redirect loop.
- A temporary verification failure does not fabricate an authenticated session.
- The application shows a controlled bootstrap state while verification runs.

## Targeted Tests

- Valid stored token restores the user.
- Missing token completes as unauthenticated.
- Expired token clears storage.
- Invalid token clears storage.
- Restoration always exits the loading state.
- Verification is not called repeatedly without reason.
- Logout clears global state and browser storage.

## Done Criteria

- Global authentication restoration exists.
- Authentication readiness is exposed.
- Login and logout remain functional.
- Restoration errors are handled safely.
- Targeted global-state tests pass.

---

# Phase 4: Persistence-Aware Protected Routing

## Objective

Prevent protected routes from redirecting valid users while session restoration is still in progress.

## Files and Directories to Update or Create

```text
src/routes/
src/router/
src/components/ProtectedRoute.*
src/components/AuthGuard.*
src/App.*
src/pages/Login/
src/pages/Dashboard/
src/tests/protectedRoute.*
```

## Development Tasks

- Update the protected-route guard to recognize restoration state.
- Render a stable loading or bootstrap screen while authentication is unresolved.
- Redirect only after authentication state is ready.
- Preserve the requested destination for post-login navigation where supported.
- Prevent authenticated users from being unnecessarily returned to login.
- Prevent invalid sessions from reaching protected content.
- Confirm logout returns the user to an appropriate public route.

## Route Decision Contract

```text
Auth unresolved -> render bootstrap/loading state
Auth ready and valid -> render protected route
Auth ready and invalid -> redirect to login
Authenticated user on login route -> redirect to dashboard or intended route
```

## Targeted Tests

- Protected route waits during restoration.
- Valid restored session renders protected content.
- Missing session redirects after restoration.
- Invalid session redirects after cleanup.
- Authenticated user does not remain on login page.
- Redirect state does not cause a navigation loop.

## Done Criteria

- Protected routing is restoration-aware.
- Refreshing a protected page does not force a valid user to log in again.
- Invalid sessions cannot access protected views.
- Router tests pass.

---

# Phase 5: End-to-End Session Persistence Validation

## Objective

Validate the complete authentication restoration experience against Devine's verification API before beginning production build cleanup.

## Files and Directories to Update or Create

```text
src/tests/authPersistence.*
src/tests/protectedRoute.*
src/tests/setup.*
README.md
```

## Validation Scenarios

- Login stores the expected session.
- Refresh restores the authenticated user.
- Closing and reopening the browser restores a still-valid session.
- Expired token is rejected and cleared.
- Malformed token is rejected and cleared.
- Backend unauthorized response returns the user to login.
- Verification network failure produces a safe state.
- Logout clears storage and protected access.
- Direct navigation to a protected URL works after successful restoration.
- No token or private data appears in console output.

## Team Dependency

Devine's verification endpoint must be available or represented by an agreed mock contract.

## Done Criteria

- Authentication persistence works through the full frontend flow.
- Protected-route refresh behavior is verified.
- Invalid-session cleanup is verified.
- No severe console errors remain.
- Authentication work is committed before build-optimization changes begin.

---

# Phase 6: Production API Environment Compilation

## Objective

Remove hardcoded local API endpoints and compile the frontend against explicit environment-based API configuration.

## Files and Directories to Update or Create

```text
.env.example
.env.development
.env.production
.gitignore
src/config/env.*
src/api/client.*
src/services/
vite.config.*
README.md
```

Private environment files must remain ignored. Only safe placeholders belong in tracked example files.

## Development Tasks

- Search for hardcoded `localhost`, loopback, and testing API URLs.
- Introduce or confirm `VITE_API_BASE_URL`.
- Centralize environment access in one configuration module where practical.
- Validate that the API base URL exists in production mode.
- Normalize trailing slashes to prevent malformed routes.
- Update authentication, inventory, booking, upload, and admin services to use the shared API client.
- Ensure only `VITE_` public values are exposed to the frontend.
- Confirm no JWT secret, database URL, Cloudinary secret, or backend credential enters the frontend bundle.

## Suggested Environment Contract

```text
VITE_API_BASE_URL=https://approved-production-api.example.com
```

The actual hosted API URL must be supplied by the deployment owner.

## Targeted Checks

- No hardcoded local API URL remains in production source paths.
- Development can still use an approved local environment value.
- Production build fails clearly or reports configuration problems when the required public API URL is absent.
- Frontend client does not expose backend secrets.

## Done Criteria

- API URL is environment-driven.
- Environment example is documented.
- Private environment files are ignored.
- All frontend API calls use the centralized configuration.
- Hardcoded test endpoints are removed.

---

# Phase 7: Dependency and Source Cleanup

## Objective

Reduce frontend bundle size and maintenance overhead by removing unused dependencies, imports, and dead code without disrupting working features.

## Files and Directories to Update

```text
package.json
package-lock.json
src/
```

## Development Tasks

- Identify unused runtime and development dependencies.
- Confirm each removal against actual imports and build tooling.
- Remove unused imports reported by TypeScript, ESLint, or the bundler.
- Remove unreachable or duplicate frontend helpers only after confirming no references.
- Consolidate duplicate API-client code where safe.
- Avoid large architectural refactors unrelated to Sprint 5.
- Reinstall dependencies only when package metadata changes.

## Fast-Moving Scope Rule

Prioritize:

```text
unused package removal
unused import removal
obvious duplicate API base configuration
large accidental imports
production warnings
```

Defer unrelated UI refactors unless they block the build.

## Validation

- Authentication persistence tests pass.
- Existing frontend tests pass.
- Development server starts.
- Production build passes.
- No required Vite plugin or test tool was removed.
- Package lock remains synchronized.

## Done Criteria

- Unused dependencies are removed safely.
- Unused imports are cleaned.
- Package metadata is valid.
- No regression is introduced.

---

# Phase 8: Vite Production Build Optimization

## Objective

Produce a minimized, deployable frontend bundle and document its output characteristics.

## Files and Directories to Update or Create

```text
vite.config.js
vite.config.ts
package.json
src/
README.md
```

## Development Tasks

- Confirm production minification is enabled.
- Confirm source maps follow the team's production policy.
- Review output chunk sizes and build warnings.
- Add safe manual chunking only if a clearly oversized dependency justifies it.
- Ensure dynamic imports or lazy loading do not break routes.
- Confirm environment variables are compiled correctly.
- Confirm no development-only tooling enters the production bundle.
- Record build duration and output sizes.

## Optimization Priorities

1. Remove unused code and dependencies.
2. Preserve Vite tree-shaking.
3. Avoid importing entire libraries for one helper.
4. Lazy-load large route modules only where it provides clear value.
5. Avoid premature manual chunk complexity.

## Validation

- `npm run build` passes.
- Build output is minimized.
- No local API endpoint appears in compiled assets.
- No secret-like value appears in compiled assets.
- Main routes load from a local production preview.
- Authentication restoration still works in the production build.

## Done Criteria

- Production bundle is generated successfully.
- Bundle warnings are reviewed.
- API environment compilation is verified.
- No frontend secret exposure is detected.
- Build metrics are recorded for the PR.

---

# Phase 9: Production Preview and Regression Validation

## Objective

Validate the actual production bundle rather than relying only on development-server behavior.

## Files and Directories to Update or Create

```text
src/tests/
README.md
package.json
```

## Development Tasks

- Run the production build.
- Start the Vite production preview.
- Validate public routes.
- Validate login and logout.
- Validate session restoration after refresh.
- Validate direct navigation to protected pages.
- Validate invalid-token cleanup.
- Validate production API requests.
- Validate inventory images and URL-synchronized search routes.
- Inspect browser console and network failures.

## Regression Checklist

```text
Login works
Logout works
Valid session restores
Invalid session clears
Protected routes wait for auth readiness
Direct protected URL works after verification
Production API base URL is correct
Inventory loads
Images load
Search deep links load
No severe console errors
No mixed-content errors
No local endpoint calls
```

## Done Criteria

- Production preview behaves correctly.
- Authentication persistence survives production compilation.
- No critical frontend regression remains.
- No hardcoded local endpoint is used.

---

# Phase 10: Cross-Functional Launch Drill

## Objective

Validate Edwin's final bundle with the secured API, seeded database, compressed images, and deep-linked inventory routes.

## Participants and Responsibilities

### Edwin

- Build the final frontend bundle.
- Supply the approved production API environment value.
- Run the production preview or deployment candidate.
- Verify authentication restoration.
- Monitor frontend console and network requests.

### Devine

- Run the secured API.
- Confirm CORS permits the approved frontend origin.
- Confirm the token verification endpoint works.
- Confirm security headers do not block valid frontend behavior.

### Ronald and Max

- Prepare representative database data.
- Ensure inventory and booking records support launch testing.
- Confirm indexed search and API performance remain acceptable.

### Edward

- Verify optimized images load correctly.
- Verify fixed image layouts remain stable.
- Verify inventory query URLs restore filters.
- Confirm shared deep links work with the production frontend.

## Launch Scenarios

- Fresh unauthenticated visit.
- Successful login.
- Refresh on protected page.
- Browser reopen with valid session.
- Expired-session handling.
- Logout and protected-route rejection.
- Inventory list loading.
- Compressed image loading.
- Deep-linked inventory search.
- Secure API CORS response.
- Mobile-sized viewport smoke test.
- Browser console and network inspection.

## Evidence to Record

```text
build result
bundle output sizes
frontend origin
API origin
verification endpoint result
session restoration result
protected-route result
image-loading result
deep-link result
console error summary
known limitations
```

## Done Criteria

- Final bundle works against the secured API.
- Authentication restoration works in the launch environment.
- CORS permits only the approved frontend origin.
- Images and deep links work.
- No release-blocking console error remains.
- Team dependencies are recorded.

---

# Phase 11: Documentation and Deployment Handoff

## Objective

Document production configuration, operational expectations, and unresolved dependencies before preparing the pull request.

## Files and Directories to Update

```text
README.md
.env.example
package.json
vite.config.*
```

## Documentation Scope

- Authentication restoration lifecycle.
- Token storage policy.
- Token verification endpoint dependency.
- Public frontend environment variables.
- Development and production commands.
- Production build command.
- Production preview command.
- Build output summary.
- Launch drill result.
- Known limitations.
- Security note that frontend variables are public.
- Rollback guidance for authentication restoration changes.

## Done Criteria

- Environment requirements are documented.
- Build and preview commands are documented.
- Authentication persistence behavior is documented.
- Team-owned dependencies are clearly listed.
- No private value appears in documentation.

---

# Phase 12: Final Sprint 5 PR Readiness

## Objective

Confirm Edwin's Sprint 5 work is complete, tested, documented, synchronized, and ready for review.

## Files and Directories to Review

```text
package.json
package-lock.json
vite.config.*
.env.example
.gitignore
README.md
src/main.*
src/App.*
src/context/
src/contexts/
src/store/
src/routes/
src/router/
src/components/
src/pages/
src/services/
src/api/
src/utils/
src/hooks/
src/tests/
```

## Final Checklist

- Correct Sprint 5 branch is active.
- Latest origin and upstream state has been fetched.
- Authentication storage is centralized.
- Session verification uses Devine's API.
- Valid session restoration works.
- Invalid and expired sessions are cleared.
- Protected routes wait for authentication readiness.
- Login and logout work.
- API URL is environment-driven.
- No hardcoded local production endpoint remains.
- No frontend secret is committed or bundled.
- Unused dependencies and imports are cleaned safely.
- Vite production minification is confirmed.
- Targeted authentication tests pass.
- Existing frontend tests pass.
- Production build passes.
- Production preview passes.
- Launch drill passes.
- Documentation is complete.
- Branch is clean and pushed.
- PR describes implemented scope and cross-team dependencies.

## Final Validation Commands

Use the project's actual test scripts confirmed during Phase 0. The final sequence should include:

```text
git status
git fetch origin
git fetch upstream
git pull --ff-only origin <active-sprint-5-branch>
npm run test
npm run build
git restore dist
git status
git log --oneline -10
```

Do not substitute `<active-sprint-5-branch>` until the actual Sprint 5 branch name has been confirmed.

## Done Criteria

- Authentication persistence is implemented.
- Production build optimization is complete.
- Environment compilation is correct.
- Launch drill evidence is recorded.
- Tests and build pass.
- Branch is clean and current.
- PR is ready for review.

---

# Pull Request Preparation

## Suggested PR Title

```text
Add persistent authentication and optimize the production frontend build
```

## PR Description Sections

The final PR should include:

```text
Summary
Problem addressed
Authentication persistence implementation
Protected routing behavior
Production environment compilation
Dependency and bundle optimization
Security considerations
Testing completed
Build metrics
Launch drill results
Files added and updated
Cross-functional dependencies
Known limitations
Reviewer guidance
Final readiness checklist
```

## PR Evidence to Include

- Authentication persistence test summary.
- Existing frontend test summary.
- Production build output.
- Bundle sizes before and after optimization, when available.
- Production preview result.
- Launch drill result.
- Confirmation that no local API endpoint remains in production assets.
- Confirmation that no private credential was bundled.

---

# Team Dependencies to Confirm Early

## From Devine

- Token verification endpoint.
- Authorization-header format.
- Valid-session response shape.
- Invalid and expired token behavior.
- Production API URL.
- Approved frontend origin for CORS.

## From Ronald and Max

- Seeded users and representative inventory data.
- Stable API data required for launch validation.
- Availability of indexed inventory search behavior.

## From Edward

- Final image-loading behavior.
- Inventory deep-link URL format.
- Expected route and filter restoration behavior.

## From Deployment Owner

- Hosted frontend domain.
- Hosted API domain.
- Production environment-variable mechanism.
- Source-map policy.
- Deployment command.
- Preview or staging environment.
- Final release approval owner.

---

# Execution Summary

The fastest safe path is:

```text
Phase 0: Inspect architecture
Phase 1: Define auth contract
Phase 2: Build storage and verification service
Phase 3: Add global bootstrap restoration
Phase 4: Fix protected routing
Phase 5: Validate auth persistence end-to-end
Phase 6: Move API URLs to environment config
Phase 7: Remove unused dependencies and imports
Phase 8: Optimize production build
Phase 9: Validate production preview
Phase 10: Run launch drill
Phase 11: Document handoff
Phase 12: Final PR readiness
```

Authentication persistence is the critical path. Production optimization should begin after the session restoration flow and protected routing are stable. This sequencing minimizes rework while keeping development speed high.
