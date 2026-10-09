# Noviq Labs Full-Stack Platform

## Development Sprint 3: Design System and Public Application Shell

**Sprint position:** Third production implementation sprint after the verified Engineering Foundation and Azure Platform Foundation  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure development and staging environments  
**Architecture:** Modular monolith with independently deployable web, API and worker workloads  
**Frontend foundation:** Next.js, React, TypeScript, Tailwind CSS and Storybook

## Sprint Objective

Implement the production Noviq design system and the complete responsive public application shell. The sprint will convert the approved Stage 2 brand, UX and interaction specifications into reusable, accessible and tested frontend components; establish mobile, tablet and desktop navigation; implement global layout, metadata, loading, empty and error foundations; and deploy the verified shell to development and staging without beginning the feature-specific public pages reserved for later sprints.

---

## Phase 1: Sprint Entry and Dependency Verification

### Objectives

- Verify that Development Sprint 2 passed every completion-gate requirement.
- Confirm that the verified Sprint 2 Git commit exists on the approved development branch.
- Confirm that development and staging environments remain operational.
- Confirm that Azure Container Registry, Azure Container Apps, PostgreSQL, Redis, Blob Storage, Key Vault and telemetry remain healthy.
- Confirm that the Next.js frontend builds, tests and deploys from the current repository state.
- Inspect the current frontend structure before creating or modifying design-system files.
- Confirm that the approved Stage 2 design package remains the controlling UX specification.
- Create the Development Sprint 3 branch only after entry verification passes.
- Stop the sprint if any Sprint 2 gate is incomplete or any blocking platform regression remains unresolved.

### Files to create

```text
/docs/evidence/sprint-3-entry-verification.md
/docs/design/sprint-3-scope.md
/docs/design/stage-2-specification-traceability.md
/docs/delivery/sprint-3-branch-record.md
```

---

## Phase 2: Design-System Package Foundation

### Objectives

- Create a reusable design-system package within the monorepo.
- Keep shared visual foundations independent from page-specific business features.
- Configure TypeScript, package exports, linting and testing for the design-system package.
- Establish explicit public component exports.
- Prevent private implementation utilities from becoming accidental public APIs.
- Configure package consumption by the Next.js application.
- Preserve compatibility with server and client components.

### Files to create

```text
/packages/design-system/package.json
/packages/design-system/tsconfig.json
/packages/design-system/eslint.config.mjs
/packages/design-system/vitest.config.ts
/packages/design-system/vitest.setup.ts
/packages/design-system/src/index.ts
/packages/design-system/src/components/index.ts
/packages/design-system/src/foundations/index.ts
/packages/design-system/src/hooks/index.ts
/packages/design-system/src/types/index.ts
/packages/design-system/src/utilities/index.ts
/packages/design-system/README.md
```

---

## Phase 3: Brand Asset Foundation

### Objectives

- Organize the supplied Noviq Labs logo resources as controlled production assets.
- Define horizontal, symbol and white-background variants.
- Create reusable brand-mark components with explicit size and contrast rules.
- Prevent image stretching and arbitrary recoloring.
- Add accessible alternative-text behavior.
- Reserve the symbol-only asset for constrained interface contexts.
- Document clear-space, minimum-size and background restrictions.

### Files to create

```text
/packages/design-system/src/components/brand/NoviqLogo.tsx
/packages/design-system/src/components/brand/NoviqLogo.test.tsx
/packages/design-system/src/components/brand/NoviqSymbol.tsx
/packages/design-system/src/components/brand/NoviqSymbol.test.tsx
/packages/design-system/src/components/brand/brand.types.ts
/packages/design-system/src/components/brand/index.ts
/apps/web/public/brand/noviq-labs-horizontal.png
/apps/web/public/brand/noviq-labs-symbol.png
/apps/web/public/brand/noviq-labs-symbol-white-background.png
/docs/design/logo-usage.md
/docs/design/brand-asset-register.md
```

---

## Phase 4: Design Tokens

### Objectives

- Convert the approved visual foundations into versioned design tokens.
- Define neutral surfaces and controlled Noviq brand accents.
- Define semantic colors separately from brand colors.
- Define typography, spacing, sizing, border, elevation, layer and motion tokens.
- Support light interface foundations without creating an unapproved dark theme.
- Expose tokens to Tailwind CSS and component styles.
- Prevent arbitrary hard-coded values in reusable components.
- Preserve accessible contrast requirements.

### Files to create

```text
/packages/design-system/src/foundations/tokens/colors.ts
/packages/design-system/src/foundations/tokens/typography.ts
/packages/design-system/src/foundations/tokens/spacing.ts
/packages/design-system/src/foundations/tokens/sizing.ts
/packages/design-system/src/foundations/tokens/borders.ts
/packages/design-system/src/foundations/tokens/shadows.ts
/packages/design-system/src/foundations/tokens/layers.ts
/packages/design-system/src/foundations/tokens/motion.ts
/packages/design-system/src/foundations/tokens/breakpoints.ts
/packages/design-system/src/foundations/tokens/index.ts
/packages/design-system/src/foundations/css/tokens.css
/packages/design-system/src/foundations/css/reset.css
/packages/design-system/src/foundations/css/base.css
/apps/web/src/styles/design-tokens.css
/docs/design/design-tokens.md
```

---

## Phase 5: Tailwind CSS and Global Styling Integration

### Objectives

- Integrate the Noviq design tokens with Tailwind CSS.
- Establish mobile-first responsive utility behavior.
- Configure content sources across the web application and design-system package.
- Define global typography, focus, selection and reduced-motion behavior.
- Establish controlled container widths and responsive page gutters.
- Prevent utility usage from bypassing semantic component APIs where a reusable component exists.
- Verify production CSS generation and unused-style removal.

### Files to create

```text
/apps/web/tailwind.config.ts
/apps/web/src/app/globals.css
/apps/web/src/styles/accessibility.css
/apps/web/src/styles/typography.css
/apps/web/src/styles/layout.css
/apps/web/src/styles/motion.css
/apps/web/src/styles/utilities.css
/packages/design-system/src/foundations/tailwind/preset.ts
/packages/design-system/src/foundations/tailwind/plugin.ts
/packages/design-system/src/foundations/tailwind/index.ts
/docs/design/tailwind-usage.md
/docs/design/responsive-style-rules.md
```

---

## Phase 6: Typography System

### Objectives

- Implement display, page-title, section-title, subsection, lead, body, label, caption and metadata styles.
- Support fluid typography within approved minimum and maximum sizes.
- Maintain readable line length and line height.
- Configure local or approved web-font loading only after licensing and performance checks pass.
- Provide a reliable system-font fallback stack.
- Prevent visual heading styles from replacing semantic heading order.
- Verify typography at mobile, tablet, desktop and 200 percent zoom.

### Files to create

```text
/packages/design-system/src/components/typography/Heading.tsx
/packages/design-system/src/components/typography/Heading.test.tsx
/packages/design-system/src/components/typography/Text.tsx
/packages/design-system/src/components/typography/Text.test.tsx
/packages/design-system/src/components/typography/Label.tsx
/packages/design-system/src/components/typography/Caption.tsx
/packages/design-system/src/components/typography/typography.types.ts
/packages/design-system/src/components/typography/index.ts
/apps/web/src/app/fonts.ts
/docs/design/typography-system.md
```

---

## Phase 7: Layout Primitives

### Objectives

- Implement reusable page, section, container, stack, cluster, grid and divider primitives.
- Support mobile-first one-column layouts and adaptive tablet and desktop compositions.
- Bound content width on large and ultrawide displays.
- Preserve semantic HTML and avoid layout-only markup where possible.
- Support responsive gaps through approved spacing tokens.
- Prevent ordinary content from causing horizontal scrolling.
- Verify portrait and landscape behavior.

### Files to create

```text
/packages/design-system/src/components/layout/Page.tsx
/packages/design-system/src/components/layout/Section.tsx
/packages/design-system/src/components/layout/Container.tsx
/packages/design-system/src/components/layout/Stack.tsx
/packages/design-system/src/components/layout/Cluster.tsx
/packages/design-system/src/components/layout/Grid.tsx
/packages/design-system/src/components/layout/Divider.tsx
/packages/design-system/src/components/layout/layout.types.ts
/packages/design-system/src/components/layout/index.ts
/packages/design-system/src/components/layout/layout.test.tsx
/docs/design/layout-primitives.md
```

---

## Phase 8: Button and Link Components

### Objectives

- Implement primary, secondary, text, icon and destructive button variants.
- Implement internal, external and download link patterns.
- Define default, hover, focus-visible, active, disabled and loading states.
- Prevent duplicate actions while an operation is pending.
- Require accessible names for icon-only controls.
- Maintain minimum touch-target dimensions.
- Distinguish navigation links from action buttons semantically.
- Verify keyboard, pointer and screen-reader behavior.

### Files to create

```text
/packages/design-system/src/components/actions/Button.tsx
/packages/design-system/src/components/actions/Button.test.tsx
/packages/design-system/src/components/actions/Button.stories.tsx
/packages/design-system/src/components/actions/IconButton.tsx
/packages/design-system/src/components/actions/IconButton.test.tsx
/packages/design-system/src/components/actions/Link.tsx
/packages/design-system/src/components/actions/Link.test.tsx
/packages/design-system/src/components/actions/ActionGroup.tsx
/packages/design-system/src/components/actions/action.types.ts
/packages/design-system/src/components/actions/index.ts
/docs/design/buttons-and-links.md
```

---

## Phase 9: Form Foundation Components

### Objectives

- Implement accessible field, label, description and error-message primitives.
- Implement text, email, telephone, URL, textarea, select, checkbox, radio and switch controls.
- Define required, optional, disabled, read-only, valid, invalid and loading states.
- Preserve persistent labels rather than placeholder-only identification.
- Associate help and error text programmatically.
- Support keyboard and screen-reader interaction.
- Prepare integration with React Hook Form and schema validation without implementing feature-specific forms.
- Establish accessible error-summary behavior for future multi-step workflows.

### Files to create

```text
/packages/design-system/src/components/forms/Field.tsx
/packages/design-system/src/components/forms/FieldLabel.tsx
/packages/design-system/src/components/forms/FieldDescription.tsx
/packages/design-system/src/components/forms/FieldError.tsx
/packages/design-system/src/components/forms/ErrorSummary.tsx
/packages/design-system/src/components/forms/TextInput.tsx
/packages/design-system/src/components/forms/TextArea.tsx
/packages/design-system/src/components/forms/Select.tsx
/packages/design-system/src/components/forms/Checkbox.tsx
/packages/design-system/src/components/forms/RadioGroup.tsx
/packages/design-system/src/components/forms/Switch.tsx
/packages/design-system/src/components/forms/form.types.ts
/packages/design-system/src/components/forms/index.ts
/packages/design-system/src/components/forms/forms.test.tsx
/docs/design/form-components.md
/docs/design/form-error-language.md
```

---

## Phase 10: Content Components

### Objectives

- Implement reusable hero, section-header, card, statistic, media and call-to-action components.
- Keep content components flexible enough for future public pages without embedding page-specific copy.
- Support responsive image and video placeholders.
- Preserve heading hierarchy and accessible landmark usage.
- Define card-link behavior without ambiguous nested interactions.
- Support loading and empty content states.
- Verify long titles, long body copy and missing optional media.

### Files to create

```text
/packages/design-system/src/components/content/Hero.tsx
/packages/design-system/src/components/content/SectionHeader.tsx
/packages/design-system/src/components/content/Card.tsx
/packages/design-system/src/components/content/CardGrid.tsx
/packages/design-system/src/components/content/Statistic.tsx
/packages/design-system/src/components/content/MediaFrame.tsx
/packages/design-system/src/components/content/CallToAction.tsx
/packages/design-system/src/components/content/content.types.ts
/packages/design-system/src/components/content/index.ts
/packages/design-system/src/components/content/content.test.tsx
/docs/design/content-components.md
```

---

## Phase 11: Feedback and Status Components

### Objectives

- Implement alert, notice, status badge, loading indicator, skeleton, empty state and offline state components.
- Define informational, success, warning and error semantics.
- Ensure status is not communicated by color alone.
- Support polite and assertive live-region behavior where appropriate.
- Prevent excessive or disruptive announcements.
- Implement retry and recovery action slots.
- Provide safe generic system-failure messages without exposing internal details.

### Files to create

```text
/packages/design-system/src/components/feedback/Alert.tsx
/packages/design-system/src/components/feedback/Notice.tsx
/packages/design-system/src/components/feedback/StatusBadge.tsx
/packages/design-system/src/components/feedback/LoadingIndicator.tsx
/packages/design-system/src/components/feedback/Skeleton.tsx
/packages/design-system/src/components/feedback/EmptyState.tsx
/packages/design-system/src/components/feedback/OfflineState.tsx
/packages/design-system/src/components/feedback/feedback.types.ts
/packages/design-system/src/components/feedback/index.ts
/packages/design-system/src/components/feedback/feedback.test.tsx
/docs/design/feedback-and-status.md
```

---

## Phase 12: Overlay and Disclosure Components

### Objectives

- Implement accessible dialog, drawer, popover, accordion and disclosure components.
- Manage focus entry, focus containment and focus restoration.
- Support Escape dismissal where dismissal is safe.
- Prevent background interaction while modal dialogs are active.
- Provide mobile navigation drawer behavior without duplicating page content.
- Respect reduced-motion preferences.
- Verify keyboard and screen-reader behavior.

### Files to create

```text
/packages/design-system/src/components/overlays/Dialog.tsx
/packages/design-system/src/components/overlays/Drawer.tsx
/packages/design-system/src/components/overlays/Popover.tsx
/packages/design-system/src/components/overlays/Accordion.tsx
/packages/design-system/src/components/overlays/Disclosure.tsx
/packages/design-system/src/components/overlays/overlay.types.ts
/packages/design-system/src/components/overlays/index.ts
/packages/design-system/src/components/overlays/overlays.test.tsx
/docs/design/overlays-and-disclosure.md
```

---

## Phase 13: Public Navigation Components

### Objectives

- Implement the approved primary navigation structure.
- Implement desktop, tablet and mobile navigation behavior.
- Implement a visible Start a Project action.
- Implement active-location behavior.
- Add skip navigation and accessible menu controls.
- Preserve keyboard order and focus handling.
- Prevent background scrolling while the mobile menu is open.
- Prepare supporting navigation for Contact, Careers, Partnerships, Sign In and legal pages.
- Keep authenticated application navigation separate from the public navigation.

### Files to create

```text
/packages/design-system/src/components/navigation/SkipLink.tsx
/packages/design-system/src/components/navigation/SiteHeader.tsx
/packages/design-system/src/components/navigation/DesktopNavigation.tsx
/packages/design-system/src/components/navigation/MobileNavigation.tsx
/packages/design-system/src/components/navigation/NavigationLink.tsx
/packages/design-system/src/components/navigation/Breadcrumbs.tsx
/packages/design-system/src/components/navigation/SiteFooter.tsx
/packages/design-system/src/components/navigation/navigation.config.ts
/packages/design-system/src/components/navigation/navigation.types.ts
/packages/design-system/src/components/navigation/index.ts
/packages/design-system/src/components/navigation/navigation.test.tsx
/docs/design/public-navigation.md
```

---

## Phase 14: Public Application Shell

### Objectives

- Implement the shared public layout using the approved design-system components.
- Integrate the global header, main region and footer.
- Configure responsive page gutters and maximum widths.
- Add accessible skip navigation.
- Add a neutral placeholder homepage for shell verification only.
- Preserve future page-level metadata and content slots.
- Keep public shell concerns separate from authenticated customer and administration shells.
- Verify server rendering and hydration behavior.

### Files to create

```text
/apps/web/src/app/(public)/layout.tsx
/apps/web/src/app/(public)/page.tsx
/apps/web/src/app/(public)/loading.tsx
/apps/web/src/app/(public)/error.tsx
/apps/web/src/app/(public)/not-found.tsx
/apps/web/src/components/shell/PublicShell.tsx
/apps/web/src/components/shell/PublicHeader.tsx
/apps/web/src/components/shell/PublicFooter.tsx
/apps/web/src/components/shell/PublicMain.tsx
/apps/web/src/components/shell/index.ts
/apps/web/src/components/shell/PublicShell.test.tsx
/docs/design/public-application-shell.md
```

---

## Phase 15: Authenticated Shell Foundations

### Objectives

- Create non-functional structural foundations for the future customer and administration applications.
- Keep authenticated shells inaccessible from public production navigation until identity implementation is approved.
- Define responsive side navigation, top navigation, content area and status region patterns.
- Support mobile and tablet adaptation.
- Avoid implementing customer or administrator business features prematurely.
- Preserve future role-aware navigation integration points.

### Files to create

```text
/apps/web/src/components/shell/AuthenticatedShell.tsx
/apps/web/src/components/shell/ApplicationHeader.tsx
/apps/web/src/components/shell/ApplicationSidebar.tsx
/apps/web/src/components/shell/ApplicationMobileNavigation.tsx
/apps/web/src/components/shell/ApplicationMain.tsx
/apps/web/src/components/shell/ApplicationStatusRegion.tsx
/apps/web/src/components/shell/authenticated-shell.types.ts
/apps/web/src/components/shell/AuthenticatedShell.test.tsx
/docs/design/authenticated-application-shell.md
```

---

## Phase 16: Metadata, Icons and Document Foundation

### Objectives

- Configure global title templates and default metadata.
- Add favicon and application-icon foundations from approved Noviq assets.
- Configure viewport, color-scheme and theme-color behavior.
- Establish canonical URL and social-card placeholders without publishing unapproved claims.
- Add robots and sitemap foundations for later public-page implementation.
- Define page-level metadata requirements.
- Prevent staging environments from being indexed.

### Files to create

```text
/apps/web/src/app/metadata.ts
/apps/web/src/app/manifest.ts
/apps/web/src/app/robots.ts
/apps/web/src/app/sitemap.ts
/apps/web/src/app/icon.png
/apps/web/src/app/apple-icon.png
/apps/web/src/lib/seo/metadata.ts
/apps/web/src/lib/seo/robots.ts
/apps/web/src/lib/seo/sitemap.ts
/apps/web/src/lib/seo/urls.ts
/apps/web/src/lib/seo/index.ts
/docs/design/metadata-and-icons.md
/docs/delivery/search-indexing-controls.md
```

---

## Phase 17: Motion and Reduced-Motion Foundation

### Objectives

- Implement approved motion-duration and easing tokens.
- Provide reusable transition helpers.
- Apply motion only where it communicates state or continuity.
- Disable non-essential motion when reduced motion is requested.
- Prevent scroll hijacking and blocking animations.
- Verify that all interaction remains understandable without animation.
- Avoid production-heavy three-dimensional effects in this sprint.

### Files to create

```text
/packages/design-system/src/foundations/motion/transitions.ts
/packages/design-system/src/foundations/motion/easings.ts
/packages/design-system/src/foundations/motion/index.ts
/packages/design-system/src/hooks/useReducedMotion.ts
/packages/design-system/src/hooks/useReducedMotion.test.ts
/packages/design-system/src/utilities/motion.ts
/docs/design/motion-principles.md
/docs/design/reduced-motion.md
```

---

## Phase 18: Storybook Foundation

### Objectives

- Configure Storybook for the design-system package.
- Document component purpose, variants, states and accessibility expectations.
- Add stories for foundations and reusable components.
- Configure viewport presets for mobile, tablet and desktop review.
- Configure accessibility checks.
- Configure reduced-motion and theme backgrounds.
- Keep stories deterministic for visual regression testing.
- Publish Storybook only to an approved internal or staging location.

### Files to create

```text
/packages/design-system/.storybook/main.ts
/packages/design-system/.storybook/preview.tsx
/packages/design-system/.storybook/manager.ts
/packages/design-system/.storybook/preview-head.html
/packages/design-system/.storybook/viewports.ts
/packages/design-system/src/stories/Foundations.stories.tsx
/packages/design-system/src/stories/Typography.stories.tsx
/packages/design-system/src/stories/Layout.stories.tsx
/packages/design-system/src/stories/Actions.stories.tsx
/packages/design-system/src/stories/Forms.stories.tsx
/packages/design-system/src/stories/Content.stories.tsx
/packages/design-system/src/stories/Feedback.stories.tsx
/packages/design-system/src/stories/Navigation.stories.tsx
/docs/design/storybook-governance.md
```

---

## Phase 19: Accessibility Automation

### Objectives

- Add automated accessibility testing for components and the public shell.
- Test landmark structure, heading order, labels, focus, contrast-dependent states and accessible names.
- Add keyboard interaction tests for menus, dialogs and form controls.
- Verify 200 percent zoom behavior.
- Verify mobile touch-target requirements.
- Treat automated accessibility tests as required but not sufficient for final approval.
- Preserve manual review requirements.

### Files to create

```text
/packages/design-system/src/testing/accessibility.ts
/packages/design-system/src/testing/keyboard.ts
/packages/design-system/src/testing/render.tsx
/packages/design-system/src/testing/index.ts
/apps/web/tests/accessibility/public-shell.spec.ts
/apps/web/tests/accessibility/navigation.spec.ts
/apps/web/tests/accessibility/forms.spec.ts
/apps/web/tests/accessibility/zoom.spec.ts
/apps/web/playwright.config.ts
/docs/quality/accessibility-testing.md
/docs/evidence/sprint-3-accessibility-results.md
```

---

## Phase 20: Responsive and Visual Regression Testing

### Objectives

- Configure browser-based responsive testing.
- Create mobile, tablet and desktop viewport profiles.
- Capture deterministic component and shell snapshots.
- Detect layout overflow, clipping, unexpected wrapping and spacing drift.
- Verify portrait and landscape behavior where applicable.
- Verify that public navigation changes correctly across breakpoints.
- Keep visual differences reviewable and approved through pull requests.

### Files to create

```text
/apps/web/tests/visual/public-shell.visual.spec.ts
/apps/web/tests/visual/navigation.visual.spec.ts
/apps/web/tests/visual/components.visual.spec.ts
/apps/web/tests/responsive/mobile.spec.ts
/apps/web/tests/responsive/tablet.spec.ts
/apps/web/tests/responsive/desktop.spec.ts
/apps/web/tests/responsive/landscape.spec.ts
/apps/web/tests/fixtures/viewports.ts
/apps/web/tests/fixtures/test-pages.ts
/docs/quality/visual-regression-testing.md
/docs/evidence/sprint-3-responsive-results.md
```

---

## Phase 21: Unit and Integration Test Coverage

### Objectives

- Add unit tests for all design-system components introduced in the sprint.
- Add integration tests for the public application shell.
- Verify component variants and invalid prop combinations.
- Verify loading, disabled, empty and error states.
- Verify server and client component boundaries.
- Verify that design-system exports remain stable.
- Ensure test failures are not hidden by fallback commands.

### Files to create

```text
/packages/design-system/src/testing/component-contracts.test.ts
/packages/design-system/src/testing/public-exports.test.ts
/apps/web/src/components/shell/PublicShell.integration.test.tsx
/apps/web/src/components/shell/AuthenticatedShell.integration.test.tsx
/apps/web/src/app/(public)/page.test.tsx
/apps/web/src/app/(public)/error.test.tsx
/apps/web/src/app/(public)/not-found.test.tsx
/docs/quality/design-system-testing.md
```

---

## Phase 22: Performance Foundation

### Objectives

- Establish initial frontend performance budgets.
- Verify server rendering and minimize unnecessary client-side JavaScript.
- Ensure brand images have explicit dimensions and optimized delivery.
- Verify font loading does not cause avoidable layout shift.
- Add bundle-size reporting.
- Add Lighthouse-based staging checks.
- Prevent heavy animation or media libraries from entering the foundational shell without approval.
- Record baseline Core Web Vitals measurements for the shell.

### Files to create

```text
/apps/web/performance-budget.json
/apps/web/lighthouse.config.cjs
/apps/web/src/lib/performance/web-vitals.ts
/apps/web/src/lib/performance/reporting.ts
/apps/web/src/lib/performance/index.ts
/scripts/quality/validate-web-performance.zsh
/scripts/quality/report-web-bundle.zsh
/docs/quality/frontend-performance-budget.md
/docs/evidence/sprint-3-performance-baseline.md
```

---

## Phase 23: Frontend Security Foundation

### Objectives

- Verify baseline security headers for the public shell.
- Establish a deliberate content security policy foundation.
- Prevent unapproved inline script and style behavior.
- Verify that no server-only configuration is exposed to the browser.
- Configure safe external-link behavior.
- Verify dependency and supply-chain scans for the design-system additions.
- Add security regression tests for headers and public configuration.

### Files to create

```text
/apps/web/src/security/content-security-policy.ts
/apps/web/src/security/security-headers.ts
/apps/web/src/security/external-links.ts
/apps/web/src/security/public-environment.ts
/apps/web/tests/security/headers.spec.ts
/apps/web/tests/security/content-security-policy.spec.ts
/apps/web/tests/security/public-environment.spec.ts
/docs/security/frontend-security-baseline.md
/docs/evidence/sprint-3-frontend-security-results.md
```

---

## Phase 24: CI/CD Integration for the Design System

### Objectives

- Add design-system linting, type checking and testing to pull-request validation.
- Build Storybook in continuous integration.
- Run accessibility, responsive and visual regression checks.
- Run frontend performance checks against the approved thresholds.
- Publish verified web images only after the expanded quality gates pass.
- Deploy the public shell to development and staging.
- Preserve test and visual evidence as workflow artifacts.
- Prevent failed quality checks from being reported as passing.

### Files to create

```text
/.github/workflows/ci-design-system.yml
/.github/workflows/build-storybook.yml
/.github/workflows/test-accessibility.yml
/.github/workflows/test-responsive-layouts.yml
/.github/workflows/test-visual-regression.yml
/.github/workflows/test-web-performance.yml
/.github/workflows/deploy-storybook-staging.yml
/scripts/ci/verify-design-system.zsh
/scripts/ci/verify-storybook.zsh
/scripts/ci/verify-public-shell.zsh
/docs/delivery/design-system-quality-gates.md
```

---

## Phase 25: Development and Staging Deployment

### Objectives

- Build a verified commit-tagged web image containing the design system and public shell.
- Deploy the image to the Azure development environment.
- Execute smoke, accessibility and responsive checks against development.
- Promote the verified image to staging.
- Verify header, navigation, footer, metadata, error and loading behavior in staging.
- Verify centralized telemetry and frontend error reporting.
- Verify rollback to the previous web revision.
- Keep unfinished page-specific features inaccessible.

### Files to create

```text
/scripts/cloud/deploy-sprint-3-development.zsh
/scripts/cloud/deploy-sprint-3-staging.zsh
/scripts/cloud/smoke-test-public-shell.zsh
/scripts/cloud/verify-storybook-staging.zsh
/tests/deployment/sprint-3-development-smoke-tests.json
/tests/deployment/sprint-3-staging-smoke-tests.json
/docs/evidence/sprint-3-development-deployment.md
/docs/evidence/sprint-3-staging-deployment.md
/docs/evidence/sprint-3-web-rollback-verification.md
```

---

## Phase 26: Documentation and Design-System Governance

### Objectives

- Document component ownership and contribution rules.
- Document when to create a new component and when to extend an existing component.
- Define component deprecation and versioning expectations.
- Document responsive, accessibility, motion and content requirements.
- Record architecture decisions made during implementation.
- Keep documentation aligned with Storybook and the source code.
- Document Kali Debian and Zsh commands required to validate the frontend locally.

### Files to create

```text
/docs/design/component-contribution.md
/docs/design/component-ownership.md
/docs/design/component-versioning.md
/docs/design/component-deprecation.md
/docs/design/content-and-label-guidelines.md
/docs/architecture/adr/0013-use-shared-design-system-package.md
/docs/architecture/adr/0014-use-storybook.md
/docs/architecture/adr/0015-use-tailwind-design-token-preset.md
/docs/architecture/adr/0016-separate-public-and-authenticated-shells.md
/docs/development/design-system-kali-debian-zsh.md
/docs/development/frontend-troubleshooting.md
```

---

## Phase 27: Integrated Validation and Sprint Closure

### Objectives

- Validate the design-system package from a clean checkout.
- Verify formatting, linting, strict TypeScript and public exports.
- Execute all unit, integration, accessibility, responsive and visual tests.
- Build the Next.js production application.
- Build Storybook.
- Verify performance budgets.
- Verify security headers and public environment boundaries.
- Build and publish the verified web container image.
- Verify development and staging deployments.
- Verify web-revision rollback.
- Confirm that no feature-specific public page has been started outside the approved sprint scope.
- Update documentation to match the verified implementation.
- Create the verified Development Sprint 3 Git commit.
- Push the development branch to GitHub.
- Create a pull request only after every required validation passes.
- Stop at the Development Sprint 3 completion gate before beginning the next sprint.

### Files to create

```text
/scripts/release/sprint-3-final-validation.zsh
/docs/evidence/sprint-3-design-system-validation.md
/docs/evidence/sprint-3-storybook-validation.md
/docs/evidence/sprint-3-accessibility-summary.md
/docs/evidence/sprint-3-responsive-summary.md
/docs/evidence/sprint-3-visual-regression-summary.md
/docs/evidence/sprint-3-performance-summary.md
/docs/evidence/sprint-3-security-summary.md
/docs/evidence/sprint-3-deployment-summary.md
/docs/evidence/sprint-3-completion-record.md
/docs/delivery/sprint-3-pull-request.md
```

---

## Development Sprint 3 Completion Gate

Development Sprint 3 is complete only when every condition below passes:

- The reusable Noviq design-system package builds successfully.
- Design tokens are implemented and consumed by Tailwind CSS and reusable components.
- Approved horizontal and symbol logo variants render without distortion.
- Typography and layout primitives operate across mobile, tablet and desktop widths.
- Buttons, links, forms, content, feedback, overlay and navigation components pass required tests.
- Storybook builds successfully and documents approved component variants and states.
- The responsive public application shell renders successfully.
- The authenticated shell foundations remain non-functional and inaccessible from public production navigation.
- Desktop, tablet and mobile navigation work correctly.
- Keyboard navigation and focus management pass.
- Automated accessibility tests pass.
- Required manual accessibility checks are recorded.
- Responsive and visual regression tests pass.
- No ordinary content produces horizontal scrolling at supported widths.
- The interface remains usable at 200 percent zoom.
- Reduced-motion behavior works.
- Frontend performance budgets pass.
- Required security headers and content-security-policy checks pass.
- No server-only configuration or secret is exposed to the browser.
- The production Next.js application builds successfully.
- The Storybook static build succeeds.
- The verified web image is deployed to development and staging.
- Development and staging smoke tests pass.
- Frontend telemetry reaches the approved Azure monitoring resources.
- Web-revision rollback is verified.
- Documentation matches the verified implementation.
- A verified Development Sprint 3 Git commit exists.
- The Development Sprint 3 development branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- No unresolved critical, high-risk or blocking defect remains.
- The next sprint has not started.

## Development Sprint 3 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_3_COMPLETE
```
