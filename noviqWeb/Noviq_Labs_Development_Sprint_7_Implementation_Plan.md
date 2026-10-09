# Noviq Labs Full-Stack Platform

## Development Sprint 7: Identity, Customer Accounts and Organizations

**Sprint position:** Seventh production implementation sprint after the verified Content Management and Editorial Administration sprint  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Identity platform:** Microsoft Entra External ID  
**Deployment target:** Microsoft Azure development and staging environments  
**Architecture:** Modular monolith with external authentication and application-controlled authorization

## Sprint Objective

Implement secure customer identity, account lifecycle, customer organizations, team invitations, role-based and policy-based authorization, secure sessions, profile settings, administrative account controls and identity audit logging. Authentication will be delegated to Microsoft Entra External ID, while Noviq Labs will retain authoritative control over application profiles, organization membership and business authorization. Customer project, lead-intake, billing and payment functionality remain outside this sprint.

---

## Phase 1: Entry verification

### Objectives

- Verify Sprint 6 completion evidence and Git state.
- Confirm Entra External ID tenant, licensing, domains and administrators.
- Inspect the repository before changes.
- Create the Sprint 7 branch only after all entry checks pass.

### Files to create

```text
/docs/evidence/sprint-7-entry-verification.md
/docs/identity/entra-external-id-readiness.md
/docs/identity/sprint-7-scope.md
/docs/delivery/sprint-7-branch-record.md
```

---

## Phase 2: Identity architecture

### Objectives

- Define Entra External ID as the authentication authority.
- Keep application authorization and organization membership in Noviq.
- Document browser, web, API, identity-provider and database trust boundaries.
- Use OpenID Connect and OAuth 2.0.

### Files to create

```text
/docs/architecture/identity-context.md
/docs/architecture/identity-trust-boundaries.md
/docs/architecture/identity-sequence-flows.md
/docs/architecture/adr/0026-use-microsoft-entra-external-id.md
/docs/architecture/adr/0027-separate-authentication-and-authorization.md
```

---

## Phase 3: Entra applications and policies

### Objectives

- Create isolated development, staging and production applications.
- Configure redirect URIs, logout URIs, scopes and API audiences.
- Disable insecure and unsupported grant types.
- Keep production registration inactive until approved.

### Files to create

```text
/infrastructure/identity/entra-applications.json
/infrastructure/identity/entra-development.json
/infrastructure/identity/entra-staging.json
/infrastructure/identity/entra-production.json
/scripts/identity/configure-entra-applications.zsh
/scripts/identity/verify-entra-applications.zsh
/docs/identity/entra-application-registration.md
```

---

## Phase 4: Identity configuration and secrets

### Objectives

- Store confidential identity configuration in Azure Key Vault.
- Prevent credentials from entering source control, browser bundles and logs.
- Validate required identity configuration at startup.
- Define credential rotation and emergency revocation.

### Files to create

```text
/infrastructure/azure/config/identity-secret-names.json
/infrastructure/azure/modules/identity-key-vault-secrets.bicep
/apps/web/src/lib/auth/auth-env.ts
/apps/web/src/lib/auth/auth-env.test.ts
/apps/api/NoviqLabs.Infrastructure/Identity/EntraExternalIdOptions.cs
/apps/api/NoviqLabs.Infrastructure/Identity/EntraExternalIdOptionsValidator.cs
/docs/security/identity-secret-management.md
```

---

## Phase 5: Identity and organization domain model

### Objectives

- Create user profiles linked to immutable external subjects.
- Create organizations, memberships, roles and invitations.
- Separate authentication identity from business profiles.
- Support auditable lifecycle states.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Identity/UserProfile.cs
/apps/api/NoviqLabs.Domain/Identity/UserStatus.cs
/apps/api/NoviqLabs.Domain/Identity/ExternalIdentityReference.cs
/apps/api/NoviqLabs.Domain/Organizations/Organization.cs
/apps/api/NoviqLabs.Domain/Organizations/OrganizationMembership.cs
/apps/api/NoviqLabs.Domain/Organizations/OrganizationRole.cs
/apps/api/NoviqLabs.Domain/Organizations/Invitation.cs
/apps/api/NoviqLabs.Domain/Organizations/InvitationStatus.cs
```

---

## Phase 6: Persistence and migration

### Objectives

- Map identity and organization entities to PostgreSQL.
- Add unique constraints, concurrency controls and authorization indexes.
- Do not store access, ID or refresh tokens in business tables.
- Validate migration upgrade and rollback boundaries.

### Files to create

```text
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/UserProfileConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/OrganizationConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/OrganizationMembershipConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Configurations/InvitationConfiguration.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddIdentityAndOrganizations.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Migrations/AddIdentityAndOrganizations.Designer.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Persistence/IdentityMigrationTests.cs
/docs/database/identity-and-organization-schema.md
```

---

## Phase 7: ASP.NET Core authentication

### Objectives

- Validate token issuer, audience, signature, lifetime and algorithms.
- Normalize external claims into the current-user abstraction.
- Reject tokens from unapproved applications and policies.
- Emit safe unauthorized responses and telemetry.

### Files to create

```text
/apps/api/NoviqLabs.Api/Security/AuthenticationConfiguration.cs
/apps/api/NoviqLabs.Api/Security/EntraTokenValidation.cs
/apps/api/NoviqLabs.Api/Security/ClaimsTransformation.cs
/apps/api/NoviqLabs.Application/Identity/ICurrentUser.cs
/apps/api/NoviqLabs.Infrastructure/Identity/CurrentUser.cs
/apps/api/NoviqLabs.Api/Errors/AuthenticationProblemDetails.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Identity/AuthenticationTests.cs
```

---

## Phase 8: Next.js authentication

### Objectives

- Implement sign-in, callback and sign-out.
- Use secure server-managed browser sessions.
- Keep tokens inaccessible to browser JavaScript.
- Validate return destinations and callback state.

### Files to create

```text
/apps/web/src/app/(auth)/sign-in/page.tsx
/apps/web/src/app/(auth)/sign-out/page.tsx
/apps/web/src/app/(auth)/auth/error/page.tsx
/apps/web/src/app/api/auth/sign-in/route.ts
/apps/web/src/app/api/auth/callback/route.ts
/apps/web/src/app/api/auth/sign-out/route.ts
/apps/web/src/lib/auth/auth-server.ts
/apps/web/src/lib/auth/session.ts
/apps/web/src/lib/auth/return-url.ts
/apps/web/src/lib/auth/return-url.test.ts
```

---

## Phase 9: Registration and first sign-in

### Objectives

- Support approved registration through Entra External ID.
- Create one application profile on verified first sign-in.
- Require current terms and privacy acceptance where applicable.
- Handle retries idempotently.

### Files to create

```text
/apps/api/NoviqLabs.Application/Identity/RegisterExternalUserCommand.cs
/apps/api/NoviqLabs.Application/Identity/RegisterExternalUserHandler.cs
/apps/api/NoviqLabs.Api/Endpoints/Identity/RegisterExternalUserEndpoint.cs
/apps/api/NoviqLabs.Contracts/Identity/RegisterExternalUserRequest.cs
/apps/web/src/features/auth/FirstSignInPage.tsx
/apps/web/src/features/auth/TermsAcceptance.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Identity/FirstSignInTests.cs
```

---

## Phase 10: Multi-factor authentication

### Objectives

- Enable approved MFA policies.
- Require stronger authentication for privileged operations.
- Do not store MFA secrets in Noviq.
- Test required, failed, cancelled and unavailable challenges.

### Files to create

```text
/infrastructure/identity/authentication-strengths.json
/infrastructure/identity/mfa-policies.json
/scripts/identity/configure-mfa-policies.zsh
/apps/api/NoviqLabs.Api/Security/AuthenticationStrengthRequirement.cs
/apps/api/NoviqLabs.Api/Security/AuthenticationStrengthHandler.cs
/apps/web/src/features/auth/MfaRequiredPage.tsx
/apps/web/tests/e2e/mfa-flow.spec.ts
/docs/identity/multi-factor-authentication.md
```

---

## Phase 11: Account recovery

### Objectives

- Integrate Entra recovery without revealing account existence.
- Provide consistent recovery and support guidance.
- Revoke affected sessions when required.
- Prevent human support from bypassing verification.

### Files to create

```text
/apps/web/src/app/(auth)/recover-account/page.tsx
/apps/web/src/features/auth/AccountRecoveryPage.tsx
/apps/web/src/features/auth/RecoveryHelp.tsx
/apps/web/src/lib/auth/recovery.ts
/apps/web/tests/e2e/account-recovery.spec.ts
/docs/identity/account-recovery.md
/docs/operations/identity-recovery-support.md
```

---

## Phase 12: Session management and revocation

### Objectives

- Implement secure creation, renewal, inactivity timeout and absolute lifetime.
- Rotate identifiers after authentication and privilege changes.
- Support local and provider sign-out plus revocation.
- Prevent revoked sessions from regaining authorization through stale caches.

### Files to create

```text
/apps/web/src/lib/auth/session-store.ts
/apps/web/src/lib/auth/session-cookie.ts
/apps/web/src/lib/auth/session-lifecycle.ts
/apps/web/src/middleware/auth-session.ts
/apps/api/NoviqLabs.Application/Identity/RevokeSessionsCommand.cs
/apps/api/NoviqLabs.Infrastructure/Identity/SessionRevocationStore.cs
/apps/web/tests/security/session-fixation.spec.ts
/apps/web/tests/e2e/session-revocation.spec.ts
/docs/identity/session-management.md
```

---

## Phase 13: Policy-based authorization

### Objectives

- Define authenticated, organization-member, organization-administrator and platform-administrator policies.
- Enforce authorization in the API regardless of frontend visibility.
- Use deny-by-default behavior.
- Separate platform and organization-scoped roles.

### Files to create

```text
/apps/api/NoviqLabs.Api/Security/AuthorizationPolicies.cs
/apps/api/NoviqLabs.Api/Security/AuthorizationConfiguration.cs
/apps/api/NoviqLabs.Application/Authorization/OrganizationMemberRequirement.cs
/apps/api/NoviqLabs.Application/Authorization/OrganizationAdministratorRequirement.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/OrganizationMemberHandler.cs
/apps/api/NoviqLabs.Infrastructure/Authorization/OrganizationAdministratorHandler.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Authorization/PolicyAuthorizationTests.cs
```

---

## Phase 14: Organization creation

### Objectives

- Implement controlled organization creation.
- Assign one verified initial organization administrator.
- Prevent unlimited abusive creation.
- Record ownership, status and audit events.

### Files to create

```text
/apps/api/NoviqLabs.Application/Organizations/CreateOrganizationCommand.cs
/apps/api/NoviqLabs.Application/Organizations/CreateOrganizationHandler.cs
/apps/api/NoviqLabs.Api/Endpoints/Organizations/CreateOrganizationEndpoint.cs
/apps/api/NoviqLabs.Contracts/Organizations/CreateOrganizationRequest.cs
/apps/web/src/features/organizations/CreateOrganizationPage.tsx
/apps/web/src/features/organizations/CreateOrganizationForm.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Organizations/CreateOrganizationTests.cs
```

---

## Phase 15: Tenant isolation and organization context

### Objectives

- Scope every organization request through verified membership.
- Block cross-organization object references.
- Apply organization boundaries in queries and commands.
- Prove isolation with negative tests.

### Files to create

```text
/apps/api/NoviqLabs.Application/Organizations/IOrganizationContext.cs
/apps/api/NoviqLabs.Infrastructure/Organizations/OrganizationContext.cs
/apps/api/NoviqLabs.Infrastructure/Persistence/Interceptors/OrganizationScopeInterceptor.cs
/apps/api/NoviqLabs.Api/Middleware/OrganizationContextMiddleware.cs
/apps/web/src/lib/organizations/organization-context.ts
/apps/web/src/components/organizations/OrganizationSwitcher.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Organizations/TenantIsolationTests.cs
/docs/security/organization-isolation.md
```

---

## Phase 16: Team invitations

### Objectives

- Implement creation, resend, cancellation, expiry and acceptance.
- Use strong single-use invitation secrets.
- Prevent unintended identities and role manipulation from accepting invitations.
- Audit the full invitation lifecycle.

### Files to create

```text
/apps/api/NoviqLabs.Application/Organizations/Invitations/CreateInvitationCommand.cs
/apps/api/NoviqLabs.Application/Organizations/Invitations/AcceptInvitationCommand.cs
/apps/api/NoviqLabs.Application/Organizations/Invitations/CancelInvitationCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Organizations/CreateInvitationEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Organizations/AcceptInvitationEndpoint.cs
/apps/web/src/app/(auth)/invitations/[token]/page.tsx
/apps/web/src/features/organizations/InvitationAcceptancePage.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Organizations/InvitationTests.cs
```

---

## Phase 17: Organization role management

### Objectives

- Implement controlled role assignment and removal.
- Prevent removal of the final organization administrator.
- Require stronger authorization for administrative role changes.
- Audit before and after role state.

### Files to create

```text
/apps/api/NoviqLabs.Application/Organizations/Roles/AssignOrganizationRoleCommand.cs
/apps/api/NoviqLabs.Application/Organizations/Roles/RemoveOrganizationRoleCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Organizations/AssignOrganizationRoleEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Organizations/RemoveOrganizationRoleEndpoint.cs
/apps/web/src/features/organizations/MemberRoleEditor.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Organizations/OrganizationRoleTests.cs
/docs/organizations/role-management.md
```

---

## Phase 18: Profile and notification preferences

### Objectives

- Implement profile viewing and approved updates.
- Separate provider-owned and application-owned attributes.
- Implement operational and optional notification preferences.
- Prevent disabling legally required notices.

### Files to create

```text
/apps/api/NoviqLabs.Application/Identity/GetProfileQuery.cs
/apps/api/NoviqLabs.Application/Identity/UpdateProfileCommand.cs
/apps/api/NoviqLabs.Application/Identity/UpdateNotificationPreferencesCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Identity/GetProfileEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Identity/UpdateProfileEndpoint.cs
/apps/web/src/app/(account)/account/profile/page.tsx
/apps/web/src/app/(account)/account/notifications/page.tsx
/apps/web/src/features/account/ProfileForm.tsx
/apps/web/src/features/account/NotificationPreferencesForm.tsx
```

---

## Phase 19: Account and organization administration

### Objectives

- Implement privileged account suspension, reactivation and organization-status management.
- Keep platform administration separate from the CMS.
- Require MFA and reasons for privileged actions.
- Do not introduce impersonation.

### Files to create

```text
/apps/api/NoviqLabs.Application/Administration/SuspendUserCommand.cs
/apps/api/NoviqLabs.Application/Administration/ReactivateUserCommand.cs
/apps/api/NoviqLabs.Application/Administration/UpdateOrganizationStatusCommand.cs
/apps/api/NoviqLabs.Api/Endpoints/Administration/SuspendUserEndpoint.cs
/apps/api/NoviqLabs.Api/Endpoints/Administration/ReactivateUserEndpoint.cs
/apps/web/src/app/(admin)/admin/accounts/page.tsx
/apps/web/src/app/(admin)/admin/organizations/page.tsx
/apps/web/src/features/admin/AccountAdministrationPage.tsx
/tests/api/NoviqLabs.Api.IntegrationTests/Administration/AccountAdministrationTests.cs
```

---

## Phase 20: Identity audit logging

### Objectives

- Audit authentication, recovery, revocation, organization, invitation, role and administrative events.
- Record actor, target, organization, result, timestamp and correlation identifier.
- Exclude tokens, invitation secrets and unnecessary personal data.
- Restrict security-event access.

### Files to create

```text
/apps/api/NoviqLabs.Domain/Audit/IdentityAuditEvent.cs
/apps/api/NoviqLabs.Domain/Audit/IdentityAuditAction.cs
/apps/api/NoviqLabs.Application/Audit/IIdentityAuditWriter.cs
/apps/api/NoviqLabs.Infrastructure/Audit/IdentityAuditWriter.cs
/apps/api/NoviqLabs.Api/Endpoints/Administration/GetIdentityAuditEventsEndpoint.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Audit/IdentityAuditTests.cs
/docs/security/identity-audit-logging.md
```

---

## Phase 21: Protected routes and authenticated shell

### Objectives

- Protect account, organization and administration routes.
- Render safe unauthenticated and forbidden states.
- Populate the authenticated shell with profile and organization context.
- Keep project, billing and later modules inaccessible.

### Files to create

```text
/apps/web/src/app/(account)/layout.tsx
/apps/web/src/app/(admin)/layout.tsx
/apps/web/src/middleware/authorization.ts
/apps/web/src/components/auth/ProtectedRoute.tsx
/apps/web/src/components/auth/ForbiddenState.tsx
/apps/web/src/components/auth/AuthenticationRequiredState.tsx
/apps/web/src/components/shell/AuthenticatedProfileMenu.tsx
/apps/web/src/components/shell/AuthenticatedOrganizationContext.tsx
/apps/web/tests/security/protected-routes.spec.ts
```

---

## Phase 22: API contracts and OpenAPI

### Objectives

- Define versioned profile, organization, membership and invitation contracts.
- Use standards-based problem details.
- Apply validation and request-size limits.
- Verify OpenAPI compatibility.

### Files to create

```text
/apps/api/NoviqLabs.Contracts/Identity/IdentityContracts.cs
/apps/api/NoviqLabs.Contracts/Organizations/OrganizationContracts.cs
/apps/api/NoviqLabs.Contracts/Organizations/MembershipResponse.cs
/apps/api/NoviqLabs.Contracts/Organizations/InvitationResponse.cs
/apps/api/NoviqLabs.Api/OpenApi/IdentityOpenApiExamples.cs
/apps/api/NoviqLabs.Api/OpenApi/OrganizationOpenApiExamples.cs
/tests/api/NoviqLabs.Api.IntegrationTests/OpenApi/IdentityContractTests.cs
/docs/api/identity-and-organization-api.md
```

---

## Phase 23: Security and privacy validation

### Objectives

- Test token validation, policy bypass, tenant isolation, open redirects, CSRF, session fixation and invitation replay.
- Verify personal-data minimization and retention rules.
- Verify no identity credentials or tokens leak into logs or client bundles.
- Resolve all critical and high-risk findings.

### Files to create

```text
/apps/web/tests/security/auth-open-redirects.spec.ts
/apps/web/tests/security/auth-csrf.spec.ts
/apps/web/tests/security/auth-cookie-protection.spec.ts
/apps/web/tests/security/invitation-replay.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Security/TokenValidationTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/AuthorizationBypassTests.cs
/tests/api/NoviqLabs.Api.IntegrationTests/Security/CrossOrganizationAccessTests.cs
/scripts/security/scan-sprint-7-identity.zsh
/docs/privacy/identity-data-inventory.md
/docs/evidence/sprint-7-security-and-privacy.md
```

---

## Phase 24: Accessibility and usability validation

### Objectives

- Test all identity and organization workflows with keyboard navigation.
- Verify labels, errors, focus, status messages and 200 percent zoom.
- Verify errors do not reveal account existence.
- Conduct representative customer and administrator tasks.

### Files to create

```text
/apps/web/tests/accessibility/sign-in.spec.ts
/apps/web/tests/accessibility/account-recovery.spec.ts
/apps/web/tests/accessibility/mfa.spec.ts
/apps/web/tests/accessibility/profile-settings.spec.ts
/apps/web/tests/accessibility/organization-management.spec.ts
/apps/web/tests/accessibility/account-administration.spec.ts
/apps/web/tests/usability/sprint-7-customer-tasks.spec.ts
/apps/web/tests/usability/sprint-7-administrator-tasks.spec.ts
/docs/evidence/sprint-7-accessibility-and-usability.md
```

---

## Phase 25: End-to-end and resilience testing

### Objectives

- Test registration, sign-in, MFA, recovery, sign-out and revocation.
- Test organization creation, invitation acceptance, role changes and organization switching.
- Test suspension, audit completeness and provider outages.
- Measure authentication and authorization latency.

### Files to create

```text
/apps/web/tests/e2e/registration-and-first-sign-in.spec.ts
/apps/web/tests/e2e/sign-in-sign-out.spec.ts
/apps/web/tests/e2e/organization-creation.spec.ts
/apps/web/tests/e2e/organization-invitations.spec.ts
/apps/web/tests/e2e/organization-role-management.spec.ts
/apps/web/tests/e2e/account-suspension.spec.ts
/apps/web/tests/e2e/identity-provider-failure.spec.ts
/apps/web/tests/performance/authentication-performance.spec.ts
/tests/api/NoviqLabs.Api.IntegrationTests/Identity/IdentityLifecycleTests.cs
/docs/evidence/sprint-7-end-to-end-and-resilience.md
```

---

## Phase 26: CI/CD quality gates

### Objectives

- Add identity configuration, migration, authentication, authorization, isolation, accessibility and security checks.
- Validate Entra configuration without exposing secrets.
- Preserve evidence as workflow artifacts.
- Fail deployment when any required validation fails.

### Files to create

```text
/.github/workflows/ci-identity.yml
/.github/workflows/test-authentication.yml
/.github/workflows/test-authorization.yml
/.github/workflows/test-tenant-isolation.yml
/.github/workflows/test-identity-accessibility.yml
/.github/workflows/test-identity-security.yml
/.github/workflows/validate-identity-migration.yml
/scripts/ci/verify-sprint-7-identity.zsh
/scripts/ci/verify-sprint-7-quality-gates.zsh
/docs/delivery/sprint-7-quality-gates.md
```

---

## Phase 27: Azure deployment and monitoring

### Objectives

- Configure identity integrations for development and staging.
- Apply migrations through the controlled migration job.
- Deploy verified web and API images.
- Verify redirect URIs, cookies, telemetry and alerts.
- Keep production registration disabled.

### Files to create

```text
/infrastructure/azure/modules/identity-application-configuration.bicep
/infrastructure/azure/modules/identity-alerts.bicep
/infrastructure/azure/config/identity-alert-thresholds.json
/.github/workflows/deploy-identity-development.yml
/.github/workflows/deploy-identity-staging.yml
/scripts/cloud/deploy-sprint-7-development.zsh
/scripts/cloud/deploy-sprint-7-staging.zsh
/scripts/cloud/smoke-test-identity.zsh
/docs/evidence/sprint-7-development-deployment.md
/docs/evidence/sprint-7-staging-deployment.md
```

---

## Phase 28: Rollback, incident response and documentation

### Objectives

- Verify rollback does not weaken authorization or restore revoked sessions.
- Document credential exposure, suspicious sign-in and tenant-isolation incident response.
- Document customer and administrator procedures.
- Keep all runbooks Zsh-compatible for Kali Debian.

### Files to create

```text
/.github/workflows/rollback-identity-release.yml
/scripts/cloud/rollback-sprint-7-identity.zsh
/scripts/identity/revoke-compromised-credential.zsh
/docs/operations/identity-rollback-runbook.md
/docs/operations/identity-incident-response.md
/docs/operations/tenant-isolation-incident-response.md
/docs/identity/customer-account-handbook.md
/docs/identity/organization-administrator-handbook.md
/docs/development/sprint-7-kali-debian-zsh.md
/docs/evidence/sprint-7-rollback-verification.md
```

---

## Phase 29: Integrated validation and sprint closure

### Objectives

- Validate the complete identity and organization implementation from a clean checkout.
- Execute all build, migration, authentication, authorization, isolation, accessibility, usability, resilience and security tests.
- Verify development and staging deployments, monitoring and rollback.
- Create and push the verified Sprint 7 Git commit.
- Create a pull request only after every gate passes.
- Stop before Sprint 8.

### Files to create

```text
/scripts/release/sprint-7-final-validation.zsh
/docs/evidence/sprint-7-identity-configuration-summary.md
/docs/evidence/sprint-7-migration-summary.md
/docs/evidence/sprint-7-authentication-summary.md
/docs/evidence/sprint-7-authorization-summary.md
/docs/evidence/sprint-7-tenant-isolation-summary.md
/docs/evidence/sprint-7-accessibility-summary.md
/docs/evidence/sprint-7-security-summary.md
/docs/evidence/sprint-7-deployment-summary.md
/docs/evidence/sprint-7-completion-record.md
/docs/delivery/sprint-7-pull-request.md
```

---

## Development Sprint 7 Completion Gate

Development Sprint 7 is complete only when every condition below passes:

- Microsoft Entra External ID development and staging integrations are operational.
- Application registrations, redirect URIs, scopes and audiences are correct.
- Identity credentials remain in Azure Key Vault and server-side boundaries.
- Registration, first sign-in, sign-in, sign-out, MFA and account recovery work.
- Secure browser-session creation, renewal, timeout and revocation work.
- Tokens are not exposed to browser JavaScript, source control or logs.
- ASP.NET Core token validation passes issuer, audience, signature, lifetime and algorithm checks.
- Application profiles are linked to immutable external identity subjects.
- Customer organizations can be created through the authorized workflow.
- Organization memberships, invitations and roles work correctly.
- Cross-organization access is blocked and proven by negative tests.
- Policy-based backend authorization is authoritative and deny-by-default.
- Privileged operations require appropriate roles and strong authentication.
- Profile and notification settings work correctly.
- Administrative suspension, reactivation and organization-status controls work.
- Identity and access audit events are complete and protected.
- Protected routes cannot be accessed through client-side bypass.
- Authentication and authorization API contracts pass.
- Accessibility and usability checks pass.
- Security and privacy checks pass with no unresolved critical or high-risk findings.
- Identity-provider failure and degraded-mode behavior are verified.
- Identity and organization migrations pass in development and staging.
- Development and staging deployment smoke tests pass.
- Identity telemetry and alerts reach Azure monitoring.
- Identity rollback is verified without restoring revoked access.
- Documentation matches the verified implementation.
- A verified Development Sprint 7 Git commit exists.
- The Development Sprint 7 branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- No unresolved blocking defect remains.
- The next sprint has not started.

## Development Sprint 7 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_7_COMPLETE
```
