# Noviq Labs Full-Stack Platform

## Development Sprint 4: Public Website, Corporate and Service Pages

**Sprint position:** Fourth production implementation sprint after the verified Design System and Public Application Shell  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure development and staging environments  
**Architecture:** Modular monolith with independently deployable web, API and worker workloads  
**Frontend foundation:** Next.js, React, TypeScript, Tailwind CSS and the Noviq design system

## Sprint Objective

Implement the production public website foundation and the complete corporate and service experience for Noviq Labs. The sprint will build the homepage, About and company pages, the main Services page, four individual service-pillar pages and the Industries experience; integrate responsive media, accessible motion, metadata and calls to action; achieve mobile and low-bandwidth performance targets; and deploy the verified public experience to development and staging without beginning products, portfolio, case studies, insights, CMS, identity or customer-portal features reserved for later sprints.

---

## Phase 1: Sprint Entry and Dependency Verification

### Objectives

- Verify that Development Sprint 3 passed every completion-gate requirement.
- Confirm that the verified Sprint 3 Git commit exists on the approved development branch.
- Confirm that the Noviq design-system package, Storybook and public application shell remain operational.
- Confirm that development and staging deployments remain healthy.
- Verify responsive, accessibility, visual-regression, performance and security baselines before adding public pages.
- Inspect the current frontend structure and design-system exports before creating or modifying files.
- Confirm that the approved Stage 1 product foundation and Stage 2 UX specification remain controlling inputs.
- Create the Development Sprint 4 branch only after entry verification passes.
- Stop the sprint if any Sprint 3 gate is incomplete or any blocking regression remains unresolved.

### Files to create

```text
/docs/evidence/sprint-4-entry-verification.md
/docs/public-site/sprint-4-scope.md
/docs/public-site/content-readiness-register.md
/docs/public-site/stage-2-screen-traceability.md
/docs/delivery/sprint-4-branch-record.md
```

---

## Phase 2: Public Route and Feature Organization

### Objectives

- Establish route groups and feature directories for the approved Sprint 4 pages.
- Separate page composition, reusable sections, content models and server-side data access.
- Preserve server-component rendering by default.
- Use client components only for justified interaction.
- Keep products, portfolio, case studies, insights, CMS, identity and customer features outside this sprint.
- Define stable route names suitable for navigation, metadata and future CMS integration.
- Prevent duplicate content and conflicting page ownership.

### Files to create

```text
/apps/web/src/app/(public)/(corporate)/about/page.tsx
/apps/web/src/app/(public)/(corporate)/company/page.tsx
/apps/web/src/app/(public)/(services)/services/page.tsx
/apps/web/src/app/(public)/(services)/services/software-engineering/page.tsx
/apps/web/src/app/(public)/(services)/services/creative-technology/page.tsx
/apps/web/src/app/(public)/(services)/services/cybersecurity-and-assurance/page.tsx
/apps/web/src/app/(public)/(services)/services/technology-advisory/page.tsx
/apps/web/src/app/(public)/(industries)/industries/page.tsx
/apps/web/src/features/home/index.ts
/apps/web/src/features/corporate/index.ts
/apps/web/src/features/services/index.ts
/apps/web/src/features/industries/index.ts
/apps/web/src/content/public/index.ts
/docs/public-site/route-ownership.md
```

---

## Phase 3: Public Content Models and Validation

### Objectives

- Define typed content models for corporate, service and industry pages.
- Apply schema validation to locally managed Sprint 4 content.
- Keep content structures compatible with later headless CMS integration.
- Distinguish approved facts, claims, calls to action, media and metadata.
- Prevent unverified statistics, client claims and product-readiness claims from being published.
- Support content status, revision reference and approval metadata.
- Fail the build when required page content is missing or malformed.

### Files to create

```text
/apps/web/src/content/public/content.types.ts
/apps/web/src/content/public/content.schema.ts
/apps/web/src/content/public/content-status.ts
/apps/web/src/content/public/content-validation.ts
/apps/web/src/content/public/content-validation.test.ts
/apps/web/src/content/public/approved-claims.ts
/apps/web/src/content/public/approved-claims.test.ts
/apps/web/src/types/public-content.ts
/docs/content/public-content-model.md
/docs/content/claims-and-evidence-policy.md
/docs/content/content-approval-workflow.md
```

---

## Phase 4: Homepage Content and Composition

### Objectives

- Replace the neutral shell placeholder with the production homepage.
- Communicate the Noviq value proposition immediately.
- Present the four service pillars clearly.
- Introduce the services-to-products direction without overstating product maturity.
- Provide selected evidence placeholders only where approved evidence exists.
- Include primary and secondary calls to action.
- Include trust, operating-principle and insight-preview foundations.
- Preserve clear reading order and responsive hierarchy.
- Avoid copying another technology company's visual identity or page sequence.

### Files to create

```text
/apps/web/src/app/(public)/page.tsx
/apps/web/src/app/(public)/page.test.tsx
/apps/web/src/features/home/HomePage.tsx
/apps/web/src/features/home/HomePage.test.tsx
/apps/web/src/features/home/sections/HomeHero.tsx
/apps/web/src/features/home/sections/CapabilityPillars.tsx
/apps/web/src/features/home/sections/ProductDirection.tsx
/apps/web/src/features/home/sections/SelectedEvidence.tsx
/apps/web/src/features/home/sections/OperatingPrinciples.tsx
/apps/web/src/features/home/sections/InsightPreview.tsx
/apps/web/src/features/home/sections/HomeCallToAction.tsx
/apps/web/src/content/public/homepage.ts
/docs/public-site/homepage-specification.md
```

---

## Phase 5: Homepage Hero and Media Treatment

### Objectives

- Implement a premium but restrained homepage hero.
- Use approved Noviq brand assets and authentic media only.
- Support responsive image or video art direction.
- Add poster images and non-video fallback behavior.
- Prevent autoplay media from blocking content or consuming excessive mobile data.
- Respect reduced-motion and low-bandwidth preferences.
- Maintain strong text contrast in every supported media state.
- Keep the primary call to action visible without forcing unnecessary scrolling.

### Files to create

```text
/apps/web/src/features/home/components/HomeHeroMedia.tsx
/apps/web/src/features/home/components/HomeHeroMedia.test.tsx
/apps/web/src/features/home/components/ResponsiveHeroImage.tsx
/apps/web/src/features/home/components/ResponsiveHeroVideo.tsx
/apps/web/src/features/home/components/HeroMediaFallback.tsx
/apps/web/src/lib/media/media-preferences.ts
/apps/web/src/lib/media/media-preferences.test.ts
/apps/web/src/lib/media/responsive-sources.ts
/apps/web/public/media/home/hero-poster.webp
/apps/web/public/media/home/hero-mobile.webp
/apps/web/public/media/home/hero-tablet.webp
/apps/web/public/media/home/hero-desktop.webp
/docs/public-site/homepage-media.md
```

---

## Phase 6: About Page

### Objectives

- Implement the approved About experience.
- Present the Noviq purpose, mission, vision and institutional direction.
- Explain the services-to-products operating model.
- Present trust, evidence, security and responsible-growth principles.
- Provide leadership and governance foundations without publishing unsupported profiles.
- Connect the About experience to services, partnerships, careers and contact actions.
- Maintain a professional and restrained corporate tone.

### Files to create

```text
/apps/web/src/app/(public)/(corporate)/about/page.test.tsx
/apps/web/src/features/corporate/AboutPage.tsx
/apps/web/src/features/corporate/AboutPage.test.tsx
/apps/web/src/features/corporate/sections/AboutHero.tsx
/apps/web/src/features/corporate/sections/PurposeMissionVision.tsx
/apps/web/src/features/corporate/sections/ServicesToProductsModel.tsx
/apps/web/src/features/corporate/sections/OperatingModel.tsx
/apps/web/src/features/corporate/sections/TrustPrinciples.tsx
/apps/web/src/features/corporate/sections/LeadershipFoundation.tsx
/apps/web/src/features/corporate/sections/AboutCallToAction.tsx
/apps/web/src/content/public/about.ts
/docs/public-site/about-page-specification.md
```

---

## Phase 7: Company Page

### Objectives

- Implement the company-information page for institutional and procurement review.
- Present verified company information and operating scope.
- Present service coverage and delivery standards.
- Present governance, privacy, security and responsible-technology commitments.
- Provide pathways for partnerships, careers and formal enquiries.
- Avoid publishing sensitive registration, ownership or contact information beyond approved disclosure.
- Keep legal entity claims consistent across the platform.

### Files to create

```text
/apps/web/src/app/(public)/(corporate)/company/page.test.tsx
/apps/web/src/features/corporate/CompanyPage.tsx
/apps/web/src/features/corporate/CompanyPage.test.tsx
/apps/web/src/features/corporate/sections/CompanyOverview.tsx
/apps/web/src/features/corporate/sections/CompanyCapabilities.tsx
/apps/web/src/features/corporate/sections/DeliveryStandards.tsx
/apps/web/src/features/corporate/sections/GovernanceCommitments.tsx
/apps/web/src/features/corporate/sections/CompanyEnquiries.tsx
/apps/web/src/content/public/company.ts
/docs/public-site/company-page-specification.md
```

---

## Phase 8: Main Services Page

### Objectives

- Implement the main service-discovery experience.
- Organize services around business outcomes rather than a generic technology list.
- Present the four service pillars with clear distinctions.
- Explain the integrated Discover, Design, Build, Secure, Launch and Improve lifecycle.
- Guide users toward the relevant individual service page.
- Provide consultation and project-start actions.
- Add appropriate cross-links to industries and later case-study routes without broken destinations.
- Preserve accessible card and navigation behavior.

### Files to create

```text
/apps/web/src/app/(public)/(services)/services/page.test.tsx
/apps/web/src/features/services/ServicesPage.tsx
/apps/web/src/features/services/ServicesPage.test.tsx
/apps/web/src/features/services/sections/ServicesHero.tsx
/apps/web/src/features/services/sections/ServicePillarGrid.tsx
/apps/web/src/features/services/sections/IntegratedDeliveryLifecycle.tsx
/apps/web/src/features/services/sections/EngagementApproach.tsx
/apps/web/src/features/services/sections/ServiceSelectionGuidance.tsx
/apps/web/src/features/services/sections/ServicesCallToAction.tsx
/apps/web/src/content/public/services.ts
/docs/public-site/services-page-specification.md
```

---

## Phase 9: Shared Service-Page Framework

### Objectives

- Create a reusable service-detail framework for the four service pillars.
- Support service-specific problems, outcomes, capabilities, delivery approaches and calls to action.
- Support approved related-industry and evidence references.
- Support security and authorization notices where required.
- Prevent all service pages from becoming identical content templates.
- Preserve semantic heading order and responsive section composition.
- Keep the framework compatible with future CMS-managed service content.

### Files to create

```text
/apps/web/src/features/services/components/ServicePageLayout.tsx
/apps/web/src/features/services/components/ServicePageLayout.test.tsx
/apps/web/src/features/services/components/ServiceHero.tsx
/apps/web/src/features/services/components/ServiceProblems.tsx
/apps/web/src/features/services/components/ServiceOutcomes.tsx
/apps/web/src/features/services/components/ServiceCapabilities.tsx
/apps/web/src/features/services/components/ServiceDeliveryProcess.tsx
/apps/web/src/features/services/components/ServicePrinciples.tsx
/apps/web/src/features/services/components/ServiceEngagementOptions.tsx
/apps/web/src/features/services/components/RelatedIndustries.tsx
/apps/web/src/features/services/components/ServiceCallToAction.tsx
/apps/web/src/features/services/service-page.types.ts
/docs/public-site/service-page-framework.md
```

---

## Phase 10: Software Engineering Service Page

### Objectives

- Implement the Software Engineering service page.
- Present custom web, mobile, enterprise, integration, automation and SaaS capabilities.
- Explain product discovery, architecture, development, security, deployment and improvement.
- Emphasize maintainability, reliability, scalability and measurable outcomes.
- Add approved engagement options.
- Add project-start and technical-consultation actions.
- Avoid guaranteeing unsupported delivery times, scale or outcomes.

### Files to create

```text
/apps/web/src/app/(public)/(services)/services/software-engineering/page.test.tsx
/apps/web/src/features/services/software-engineering/SoftwareEngineeringPage.tsx
/apps/web/src/features/services/software-engineering/SoftwareEngineeringPage.test.tsx
/apps/web/src/features/services/software-engineering/EngineeringCapabilities.tsx
/apps/web/src/features/services/software-engineering/EngineeringLifecycle.tsx
/apps/web/src/features/services/software-engineering/ArchitectureAndSecurity.tsx
/apps/web/src/features/services/software-engineering/EngineeringEngagements.tsx
/apps/web/src/features/services/software-engineering/index.ts
/apps/web/src/content/public/services/software-engineering.ts
/docs/public-site/software-engineering-page-specification.md
```

---

## Phase 11: Creative Technology Service Page

### Objectives

- Implement the Creative Technology service page.
- Present brand identity, graphic design, UI/UX, animation, motion graphics, visual effects and product visualization.
- Explain how creative technology improves clarity, recognition, adoption and trust.
- Support approved visual portfolio placeholders without publishing unfinished work as client evidence.
- Explain the concept-to-production process.
- Add creative-brief and consultation actions.
- Preserve media performance and accessibility.

### Files to create

```text
/apps/web/src/app/(public)/(services)/services/creative-technology/page.test.tsx
/apps/web/src/features/services/creative-technology/CreativeTechnologyPage.tsx
/apps/web/src/features/services/creative-technology/CreativeTechnologyPage.test.tsx
/apps/web/src/features/services/creative-technology/CreativeCapabilities.tsx
/apps/web/src/features/services/creative-technology/CreativeProcess.tsx
/apps/web/src/features/services/creative-technology/MediaShowcaseFoundation.tsx
/apps/web/src/features/services/creative-technology/CreativeEngagements.tsx
/apps/web/src/features/services/creative-technology/index.ts
/apps/web/src/content/public/services/creative-technology.ts
/docs/public-site/creative-technology-page-specification.md
```

---

## Phase 12: Cybersecurity and Assurance Service Page

### Objectives

- Implement the Cybersecurity and Assurance service page.
- Present web, mobile, API, network, infrastructure and cloud assessment capabilities.
- Distinguish authorized penetration testing from vulnerability assessment.
- Explain rules of engagement, written authorization and evidence handling.
- Explain reporting, remediation guidance and verification.
- Add confidential consultation pathways.
- Avoid operational details that could expose testing methods, client targets or sensitive evidence.
- Present clear legal and authorization boundaries.

### Files to create

```text
/apps/web/src/app/(public)/(services)/services/cybersecurity-and-assurance/page.test.tsx
/apps/web/src/features/services/cybersecurity/CybersecurityPage.tsx
/apps/web/src/features/services/cybersecurity/CybersecurityPage.test.tsx
/apps/web/src/features/services/cybersecurity/SecurityCapabilities.tsx
/apps/web/src/features/services/cybersecurity/AuthorizationRequirements.tsx
/apps/web/src/features/services/cybersecurity/AssessmentLifecycle.tsx
/apps/web/src/features/services/cybersecurity/ReportingAndRemediation.tsx
/apps/web/src/features/services/cybersecurity/ConfidentialConsultation.tsx
/apps/web/src/features/services/cybersecurity/index.ts
/apps/web/src/content/public/services/cybersecurity-and-assurance.ts
/docs/public-site/cybersecurity-page-specification.md
```

---

## Phase 13: Technology Advisory Service Page

### Objectives

- Implement the Technology Advisory service page.
- Present strategy, architecture, transformation, assessment, cloud planning and delivery assurance capabilities.
- Explain common advisory scenarios and expected decision outputs.
- Present assessment, roadmap and governance methods.
- Add executive-consultation actions.
- Avoid presenting advisory recommendations as guaranteed outcomes.
- Keep language understandable to both executive and technical audiences.

### Files to create

```text
/apps/web/src/app/(public)/(services)/services/technology-advisory/page.test.tsx
/apps/web/src/features/services/technology-advisory/TechnologyAdvisoryPage.tsx
/apps/web/src/features/services/technology-advisory/TechnologyAdvisoryPage.test.tsx
/apps/web/src/features/services/technology-advisory/AdvisoryCapabilities.tsx
/apps/web/src/features/services/technology-advisory/AdvisoryScenarios.tsx
/apps/web/src/features/services/technology-advisory/AssessmentAndRoadmap.tsx
/apps/web/src/features/services/technology-advisory/GovernanceAndAssurance.tsx
/apps/web/src/features/services/technology-advisory/ExecutiveConsultation.tsx
/apps/web/src/features/services/technology-advisory/index.ts
/apps/web/src/content/public/services/technology-advisory.ts
/docs/public-site/technology-advisory-page-specification.md
```

---

## Phase 14: Industries Page

### Objectives

- Implement the Industries experience without claiming unverified specialization.
- Present evidence-led focus areas such as financial technology, education technology, media and digital communication, business automation, secure digital infrastructure and public-interest technology.
- Explain common sector problems and relevant Noviq capabilities.
- Distinguish validated experience from strategic direction.
- Provide pathways to relevant services and project-start actions.
- Prepare the page for future sector-specific case studies.

### Files to create

```text
/apps/web/src/app/(public)/(industries)/industries/page.test.tsx
/apps/web/src/features/industries/IndustriesPage.tsx
/apps/web/src/features/industries/IndustriesPage.test.tsx
/apps/web/src/features/industries/IndustriesHero.tsx
/apps/web/src/features/industries/IndustryFocusGrid.tsx
/apps/web/src/features/industries/IndustryProblemPatterns.tsx
/apps/web/src/features/industries/IndustryCapabilityMapping.tsx
/apps/web/src/features/industries/IndustriesCallToAction.tsx
/apps/web/src/content/public/industries.ts
/docs/public-site/industries-page-specification.md
```

---

## Phase 15: Calls to Action and Route-Safe Destinations

### Objectives

- Implement consistent project-start, consultation, contact and service-discovery calls to action.
- Prevent calls to action from linking to incomplete routes.
- Use approved temporary destinations where later workflows are not yet implemented.
- Preserve campaign-source and referring-page context for future lead intake.
- Maintain accessible action labels and clear user expectations.
- Prevent deceptive or ambiguous disabled actions.

### Files to create

```text
/apps/web/src/components/actions/StartProjectLink.tsx
/apps/web/src/components/actions/ConsultationLink.tsx
/apps/web/src/components/actions/ContactLink.tsx
/apps/web/src/components/actions/ServiceDiscoveryLink.tsx
/apps/web/src/lib/navigation/public-routes.ts
/apps/web/src/lib/navigation/route-availability.ts
/apps/web/src/lib/navigation/route-availability.test.ts
/apps/web/src/lib/navigation/referral-context.ts
/docs/public-site/call-to-action-standard.md
```

---

## Phase 16: Responsive Image Delivery

### Objectives

- Implement responsive image components for public page media.
- Generate mobile, tablet and desktop source variants.
- Use modern formats where supported.
- Define image dimensions and aspect ratios to prevent layout shift.
- Add meaningful alternative text or intentionally empty alternatives for decorative media.
- Add lazy loading for non-critical media.
- Keep above-the-fold media prioritized deliberately.
- Validate asset size against performance budgets.

### Files to create

```text
/apps/web/src/components/media/ResponsiveImage.tsx
/apps/web/src/components/media/ResponsiveImage.test.tsx
/apps/web/src/components/media/DecorativeImage.tsx
/apps/web/src/components/media/ContentImage.tsx
/apps/web/src/components/media/media.types.ts
/apps/web/src/components/media/index.ts
/apps/web/src/lib/media/image-config.ts
/apps/web/src/lib/media/image-validation.ts
/apps/web/src/lib/media/image-validation.test.ts
/scripts/media/validate-image-assets.zsh
/docs/media/responsive-images.md
```

---

## Phase 17: Responsive Video Delivery

### Objectives

- Implement a controlled video component for approved public media.
- Require poster images, captions or transcripts where necessary.
- Prevent uncontrolled autoplay with audio.
- Support reduced-motion and low-bandwidth alternatives.
- Defer loading until video is likely to be viewed.
- Provide user controls for playback.
- Validate video dimensions and fallback behavior.
- Avoid introducing video where a still image communicates the same information effectively.

### Files to create

```text
/apps/web/src/components/media/ResponsiveVideo.tsx
/apps/web/src/components/media/ResponsiveVideo.test.tsx
/apps/web/src/components/media/VideoPoster.tsx
/apps/web/src/components/media/VideoTranscriptLink.tsx
/apps/web/src/lib/media/video-config.ts
/apps/web/src/lib/media/video-preferences.ts
/apps/web/src/lib/media/video-preferences.test.ts
/scripts/media/validate-video-assets.zsh
/docs/media/responsive-video.md
```

---

## Phase 18: Accessible Page Motion

### Objectives

- Apply restrained entrance and state-transition motion to approved public sections.
- Use motion to clarify hierarchy and continuity.
- Avoid scroll hijacking and content blocking.
- Disable non-essential motion for reduced-motion users.
- Ensure content remains available when JavaScript or animation fails.
- Verify that animation does not cause layout instability.
- Keep animation performance within approved budgets.

### Files to create

```text
/apps/web/src/components/motion/Reveal.tsx
/apps/web/src/components/motion/Reveal.test.tsx
/apps/web/src/components/motion/Stagger.tsx
/apps/web/src/components/motion/PageTransition.tsx
/apps/web/src/components/motion/motion.types.ts
/apps/web/src/components/motion/index.ts
/apps/web/src/lib/motion/public-motion.ts
/apps/web/tests/accessibility/reduced-motion.spec.ts
/docs/design/public-page-motion.md
```

---

## Phase 19: Page Metadata and Structured Data

### Objectives

- Add unique titles, descriptions and canonical URLs for all Sprint 4 pages.
- Add Open Graph and social-card metadata using approved content.
- Add organization, service and breadcrumb structured data where appropriate.
- Avoid unsupported ratings, reviews, claims or product availability metadata.
- Keep staging environments non-indexable.
- Validate metadata completeness and structured-data syntax.
- Update sitemap coverage for completed routes only.

### Files to create

```text
/apps/web/src/lib/seo/page-metadata.ts
/apps/web/src/lib/seo/structured-data.ts
/apps/web/src/lib/seo/structured-data.types.ts
/apps/web/src/lib/seo/structured-data.test.ts
/apps/web/src/components/seo/StructuredData.tsx
/apps/web/src/components/seo/PageMetadataAudit.tsx
/apps/web/src/content/public/metadata.ts
/apps/web/tests/seo/metadata.spec.ts
/apps/web/tests/seo/structured-data.spec.ts
/scripts/quality/validate-public-metadata.zsh
/docs/seo/public-page-metadata.md
```

---

## Phase 20: Breadcrumbs and Internal Linking

### Objectives

- Implement breadcrumbs on service and other deep public routes.
- Add intentional internal links between corporate, service and industry pages.
- Prevent circular or low-value link patterns.
- Ensure every link has descriptive accessible text.
- Prevent broken links to deferred features.
- Preserve future CMS and localization compatibility.
- Add automated internal-link validation.

### Files to create

```text
/apps/web/src/components/navigation/PublicBreadcrumbs.tsx
/apps/web/src/components/navigation/PublicBreadcrumbs.test.tsx
/apps/web/src/lib/navigation/breadcrumbs.ts
/apps/web/src/lib/navigation/breadcrumbs.test.ts
/apps/web/src/lib/navigation/internal-links.ts
/apps/web/src/lib/navigation/internal-links.test.ts
/apps/web/tests/navigation/internal-links.spec.ts
/scripts/quality/check-public-links.zsh
/docs/public-site/internal-linking.md
```

---

## Phase 21: Public Loading, Empty and Error States

### Objectives

- Implement route-level loading states for Sprint 4 pages.
- Implement safe page-level failure and recovery behavior.
- Configure the global not-found experience.
- Provide empty content behavior where optional evidence or media is unavailable.
- Avoid exposing stack traces, internal identifiers or sensitive configuration.
- Preserve navigation and recovery actions during failures.
- Verify behavior with JavaScript disabled where practical.

### Files to create

```text
/apps/web/src/app/(public)/(corporate)/loading.tsx
/apps/web/src/app/(public)/(corporate)/error.tsx
/apps/web/src/app/(public)/(services)/loading.tsx
/apps/web/src/app/(public)/(services)/error.tsx
/apps/web/src/app/(public)/(industries)/loading.tsx
/apps/web/src/app/(public)/(industries)/error.tsx
/apps/web/src/components/states/PublicPageSkeleton.tsx
/apps/web/src/components/states/PublicPageError.tsx
/apps/web/src/components/states/OptionalContentEmptyState.tsx
/apps/web/src/components/states/index.ts
/apps/web/tests/resilience/public-page-errors.spec.ts
/docs/public-site/loading-empty-error-states.md
```

---

## Phase 22: Mobile and Low-Bandwidth Optimization

### Objectives

- Measure page weight and request count for Sprint 4 pages.
- Keep essential content usable on constrained networks.
- Reduce non-critical client-side JavaScript.
- Defer non-essential media and third-party code.
- Preserve functional navigation and calls to action when media is unavailable.
- Apply responsive image and video policies.
- Define low-bandwidth media alternatives.
- Verify slow-network loading and recovery behavior.

### Files to create

```text
/apps/web/src/lib/performance/network-profile.ts
/apps/web/src/lib/performance/low-bandwidth.ts
/apps/web/src/lib/performance/low-bandwidth.test.ts
/apps/web/tests/performance/slow-network.spec.ts
/apps/web/tests/performance/page-weight.spec.ts
/apps/web/tests/performance/media-loading.spec.ts
/scripts/quality/report-public-page-weight.zsh
/scripts/quality/validate-low-bandwidth.zsh
/docs/quality/low-bandwidth-standard.md
/docs/evidence/sprint-4-low-bandwidth-results.md
```

---

## Phase 23: Analytics Event Foundation

### Objectives

- Define privacy-conscious page and call-to-action events for Sprint 4.
- Avoid invasive tracking and unnecessary personal data.
- Require consent before activating non-essential analytics.
- Preserve source-page and service-interest context for future lead workflows.
- Keep analytics failures from blocking page operation.
- Document event names and allowed properties.
- Add tests preventing sensitive content from entering analytics payloads.

### Files to create

```text
/apps/web/src/lib/analytics/public-events.ts
/apps/web/src/lib/analytics/public-event.types.ts
/apps/web/src/lib/analytics/consent.ts
/apps/web/src/lib/analytics/consent.test.ts
/apps/web/src/lib/analytics/sanitize.ts
/apps/web/src/lib/analytics/sanitize.test.ts
/apps/web/src/components/analytics/PublicPageAnalytics.tsx
/apps/web/tests/analytics/public-events.spec.ts
/docs/analytics/public-site-event-catalogue.md
/docs/privacy/public-analytics-boundary.md
```

---

## Phase 24: Unit and Integration Testing

### Objectives

- Add unit tests for every new Sprint 4 component with meaningful behavior.
- Add page-composition tests for all completed routes.
- Verify content validation and approved-claim enforcement.
- Verify page metadata and internal links.
- Verify responsive media fallback behavior.
- Verify loading, empty and error states.
- Keep tests deterministic and independent of unapproved external services.
- Prevent test failures from being hidden by fallback output.

### Files to create

```text
/apps/web/src/features/home/HomePage.integration.test.tsx
/apps/web/src/features/corporate/AboutPage.integration.test.tsx
/apps/web/src/features/corporate/CompanyPage.integration.test.tsx
/apps/web/src/features/services/ServicesPage.integration.test.tsx
/apps/web/src/features/services/software-engineering/SoftwareEngineeringPage.integration.test.tsx
/apps/web/src/features/services/creative-technology/CreativeTechnologyPage.integration.test.tsx
/apps/web/src/features/services/cybersecurity/CybersecurityPage.integration.test.tsx
/apps/web/src/features/services/technology-advisory/TechnologyAdvisoryPage.integration.test.tsx
/apps/web/src/features/industries/IndustriesPage.integration.test.tsx
/apps/web/src/testing/public-page-fixtures.ts
/apps/web/src/testing/public-content-builders.ts
/docs/quality/sprint-4-testing.md
```

---

## Phase 25: End-to-End Public Journey Testing

### Objectives

- Verify navigation from the homepage to each service pillar.
- Verify service discovery from the Services page.
- Verify navigation from industry focus areas to relevant services.
- Verify calls to action route only to available destinations.
- Verify breadcrumbs and back navigation.
- Verify error recovery and not-found behavior.
- Verify mobile navigation across completed routes.
- Verify keyboard-only completion of core public journeys.

### Files to create

```text
/apps/web/tests/e2e/home-to-service.spec.ts
/apps/web/tests/e2e/service-discovery.spec.ts
/apps/web/tests/e2e/industry-to-service.spec.ts
/apps/web/tests/e2e/public-calls-to-action.spec.ts
/apps/web/tests/e2e/public-breadcrumbs.spec.ts
/apps/web/tests/e2e/public-error-recovery.spec.ts
/apps/web/tests/e2e/mobile-public-navigation.spec.ts
/apps/web/tests/e2e/keyboard-public-journeys.spec.ts
/docs/evidence/sprint-4-public-journey-results.md
```

---

## Phase 26: Accessibility Validation

### Objectives

- Run automated accessibility tests across every Sprint 4 route.
- Verify landmarks, heading order, links, buttons, images and motion.
- Verify mobile-menu and breadcrumb accessibility.
- Verify meaningful alternative text and decorative-image handling.
- Verify keyboard operation and visible focus.
- Verify 200 percent zoom and responsive reflow.
- Record manual accessibility review outcomes.
- Resolve every critical and serious accessibility defect before sprint closure.

### Files to create

```text
/apps/web/tests/accessibility/homepage.spec.ts
/apps/web/tests/accessibility/corporate-pages.spec.ts
/apps/web/tests/accessibility/services-pages.spec.ts
/apps/web/tests/accessibility/industries-page.spec.ts
/apps/web/tests/accessibility/public-media.spec.ts
/apps/web/tests/accessibility/public-motion.spec.ts
/apps/web/tests/accessibility/public-reflow.spec.ts
/docs/evidence/sprint-4-accessibility-automated.md
/docs/evidence/sprint-4-accessibility-manual.md
```

---

## Phase 27: Responsive and Cross-Browser Validation

### Objectives

- Test every Sprint 4 page at approved mobile, tablet, desktop and ultrawide widths.
- Verify portrait and landscape layouts.
- Verify no ordinary content causes horizontal scrolling.
- Verify current mainstream browser behavior.
- Verify navigation, media, typography and motion consistency.
- Capture approved visual baselines.
- Resolve clipping, overlap, wrapping and spacing defects.

### Files to create

```text
/apps/web/tests/responsive/sprint-4-mobile.spec.ts
/apps/web/tests/responsive/sprint-4-tablet.spec.ts
/apps/web/tests/responsive/sprint-4-desktop.spec.ts
/apps/web/tests/responsive/sprint-4-ultrawide.spec.ts
/apps/web/tests/responsive/sprint-4-landscape.spec.ts
/apps/web/tests/cross-browser/sprint-4-public-pages.spec.ts
/apps/web/tests/visual/sprint-4-public-pages.visual.spec.ts
/docs/evidence/sprint-4-responsive-results.md
/docs/evidence/sprint-4-cross-browser-results.md
/docs/evidence/sprint-4-visual-baselines.md
```

---

## Phase 28: Performance Validation

### Objectives

- Measure Core Web Vitals for all Sprint 4 pages in staging.
- Verify page weight, image size, client JavaScript and request count against approved budgets.
- Verify homepage media does not degrade mobile performance unacceptably.
- Verify caching and static-generation behavior.
- Verify no major layout shift occurs during font or media loading.
- Record performance regressions and resolve all budget violations.
- Preserve evidence for the sprint completion gate.

### Files to create

```text
/apps/web/tests/performance/homepage-performance.spec.ts
/apps/web/tests/performance/corporate-performance.spec.ts
/apps/web/tests/performance/services-performance.spec.ts
/apps/web/tests/performance/industries-performance.spec.ts
/apps/web/lighthouse.sprint-4.config.cjs
/scripts/quality/validate-sprint-4-performance.zsh
/docs/evidence/sprint-4-core-web-vitals.md
/docs/evidence/sprint-4-page-weight-report.md
/docs/evidence/sprint-4-performance-summary.md
```

---

## Phase 29: Public-Site Security Validation

### Objectives

- Verify security headers and content security policy across Sprint 4 pages.
- Verify no secret or server-only configuration appears in client bundles.
- Verify external links use safe behavior.
- Verify media sources comply with the approved content security policy.
- Verify calls to action cannot be manipulated into unsafe redirects.
- Verify error responses do not disclose implementation details.
- Run dependency and frontend security scans.
- Resolve all critical and high-risk findings before deployment approval.

### Files to create

```text
/apps/web/tests/security/sprint-4-security-headers.spec.ts
/apps/web/tests/security/sprint-4-content-security-policy.spec.ts
/apps/web/tests/security/sprint-4-open-redirects.spec.ts
/apps/web/tests/security/sprint-4-client-bundle.spec.ts
/apps/web/tests/security/sprint-4-error-disclosure.spec.ts
/scripts/security/scan-sprint-4-frontend.zsh
/docs/evidence/sprint-4-security-scan.md
/docs/evidence/sprint-4-client-exposure-review.md
```

---

## Phase 30: CI/CD Quality-Gate Expansion

### Objectives

- Add Sprint 4 routes to pull-request quality checks.
- Run content validation, metadata validation and internal-link checks.
- Run end-to-end, accessibility, responsive, visual, performance and security tests.
- Preserve evidence as workflow artifacts.
- Build and publish the web image only after all required checks pass.
- Prevent unapproved routes or draft content from reaching staging.
- Fail the pipeline when any required underlying command fails.

### Files to create

```text
/.github/workflows/ci-public-pages.yml
/.github/workflows/test-public-journeys.yml
/.github/workflows/test-public-accessibility.yml
/.github/workflows/test-public-links-and-metadata.yml
/.github/workflows/test-public-performance.yml
/.github/workflows/test-public-security.yml
/scripts/ci/verify-sprint-4-content.zsh
/scripts/ci/verify-sprint-4-routes.zsh
/scripts/ci/verify-sprint-4-quality-gates.zsh
/docs/delivery/sprint-4-quality-gates.md
```

---

## Phase 31: Development and Staging Deployment

### Objectives

- Build a verified commit-tagged web image containing the Sprint 4 pages.
- Deploy the image to the Azure development environment.
- Execute deployment smoke, journey, accessibility and performance checks.
- Promote the exact verified image to staging.
- Verify page availability, metadata, media and telemetry in staging.
- Verify staging remains non-indexable.
- Verify rollback to the previous web revision.
- Keep Sprint 5 and later routes unavailable.

### Files to create

```text
/scripts/cloud/deploy-sprint-4-development.zsh
/scripts/cloud/deploy-sprint-4-staging.zsh
/scripts/cloud/smoke-test-sprint-4-public-pages.zsh
/scripts/cloud/verify-sprint-4-staging.zsh
/tests/deployment/sprint-4-development-smoke-tests.json
/tests/deployment/sprint-4-staging-smoke-tests.json
/docs/evidence/sprint-4-development-deployment.md
/docs/evidence/sprint-4-staging-deployment.md
/docs/evidence/sprint-4-web-rollback-verification.md
```

---

## Phase 32: Documentation and Content Governance

### Objectives

- Document ownership and maintenance rules for Sprint 4 pages.
- Document approved content sources and claim-review requirements.
- Document media preparation and optimization procedures.
- Document metadata and internal-link maintenance.
- Record architectural decisions made during public-page implementation.
- Keep documentation aligned with the implemented routes and tests.
- Document Kali Debian and Zsh validation procedures.

### Files to create

```text
/docs/public-site/page-ownership.md
/docs/public-site/page-maintenance.md
/docs/content/public-content-governance.md
/docs/media/public-media-preparation.md
/docs/seo/public-seo-governance.md
/docs/architecture/adr/0017-use-typed-local-content-before-cms.md
/docs/architecture/adr/0018-use-server-components-by-default.md
/docs/architecture/adr/0019-use-responsive-media-art-direction.md
/docs/development/sprint-4-kali-debian-zsh.md
/docs/development/public-site-troubleshooting.md
```

---

## Phase 33: Integrated Validation and Sprint Closure

### Objectives

- Validate every Sprint 4 route from a clean checkout.
- Verify formatting, linting, strict TypeScript and content schemas.
- Execute all unit, integration, end-to-end, accessibility, responsive, cross-browser, visual, performance and security tests.
- Validate metadata, structured data and internal links.
- Build the production Next.js application.
- Build and publish the verified web container image.
- Verify development and staging deployments.
- Verify staging indexing controls and frontend telemetry.
- Verify web-revision rollback.
- Confirm that products, portfolio, case studies, insights, CMS, identity and customer features have not been started outside approved scope.
- Update documentation to match the verified implementation.
- Create the verified Development Sprint 4 Git commit.
- Push the development branch to GitHub.
- Create a pull request only after every required validation passes.
- Stop at the Development Sprint 4 completion gate before beginning the next sprint.

### Files to create

```text
/scripts/release/sprint-4-final-validation.zsh
/docs/evidence/sprint-4-content-validation.md
/docs/evidence/sprint-4-route-validation.md
/docs/evidence/sprint-4-journey-summary.md
/docs/evidence/sprint-4-accessibility-summary.md
/docs/evidence/sprint-4-responsive-summary.md
/docs/evidence/sprint-4-performance-summary.md
/docs/evidence/sprint-4-security-summary.md
/docs/evidence/sprint-4-deployment-summary.md
/docs/evidence/sprint-4-completion-record.md
/docs/delivery/sprint-4-pull-request.md
```

---

## Development Sprint 4 Completion Gate

Development Sprint 4 is complete only when every condition below passes:

- The production homepage is complete and renders successfully.
- The About page is complete and renders successfully.
- The company page is complete and renders successfully.
- The main Services page is complete and renders successfully.
- The Software Engineering page is complete and renders successfully.
- The Creative Technology page is complete and renders successfully.
- The Cybersecurity and Assurance page is complete and renders successfully.
- The Technology Advisory page is complete and renders successfully.
- The Industries page is complete and renders successfully.
- Approved content models and validation pass.
- No unsupported claim, statistic, client reference or product-readiness statement is published.
- All Sprint 4 pages use the approved Noviq design system.
- Mobile, tablet, desktop, landscape and ultrawide layouts pass.
- No ordinary content produces horizontal scrolling at supported widths.
- Keyboard navigation and visible focus pass.
- Automated and required manual accessibility checks pass.
- Responsive image delivery works.
- Responsive video delivery and fallback behavior work where video is used.
- Reduced-motion and low-bandwidth behavior work.
- Page metadata, canonical URLs and structured data pass validation.
- Staging remains non-indexable.
- Internal links and breadcrumbs pass validation.
- Calls to action do not link to incomplete or unsafe destinations.
- Loading, empty, not-found and error states work without sensitive disclosure.
- Core public journeys pass end-to-end testing.
- Frontend performance budgets and Core Web Vitals targets pass.
- Security headers and content security policy checks pass.
- No secret or server-only configuration is exposed to the browser.
- The production Next.js application builds successfully.
- The verified web image is deployed to development and staging.
- Development and staging smoke tests pass.
- Frontend telemetry reaches the approved Azure monitoring resources.
- Web-revision rollback is verified.
- Documentation matches the verified implementation.
- A verified Development Sprint 4 Git commit exists.
- The Development Sprint 4 development branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- No unresolved critical, high-risk or blocking defect remains.
- The next sprint has not started.

## Development Sprint 4 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_4_COMPLETE
```
