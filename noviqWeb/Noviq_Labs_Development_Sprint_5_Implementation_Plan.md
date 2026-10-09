# Noviq Labs Full-Stack Platform

## Development Sprint 5: Products, Portfolio, Insights and Supporting Public Pages

**Sprint position:** Fifth production implementation sprint after the verified Public Website, Corporate and Service Pages  
**Duration:** Two weeks  
**Development environment:** Kali Debian with Zsh  
**Source control:** Git and GitHub  
**Deployment target:** Microsoft Azure development and staging environments  
**Architecture:** Modular monolith with independently deployable web, API and worker workloads  
**Frontend foundation:** Next.js, React, TypeScript, Tailwind CSS and the Noviq design system

## Sprint Objective

Complete the feature scope of the public Noviq Labs website by implementing Products and Platforms, Portfolio, Case Studies, Insights, Careers, Partnerships, Contact, legal and trust pages, public content search and consent foundations. The sprint will present approved products and evidence accurately, protect confidential and unpublished content, complete the public navigation and metadata model, and deploy the verified public website to development and staging without beginning the headless CMS, identity, project-intake, customer-portal or payment capabilities reserved for later sprints.

---

## Phase 1: Sprint Entry and Dependency Verification

### Objectives

- Verify that Development Sprint 4 passed every completion-gate requirement.
- Confirm the verified Sprint 4 Git commit, pushed development branch and approved pull-request state.
- Confirm that the public shell, homepage, corporate pages, service pages and Industries page remain healthy in development and staging.
- Re-run the required responsive, accessibility, performance, security and deployment checks before extending the public website.
- Inspect the current repository and content structures before creating or modifying any file.
- Create the Development Sprint 5 branch only after entry verification passes.
- Stop the sprint if any blocking Sprint 4 regression or unresolved high-risk issue remains.

### Files to create

```text
/docs/evidence/sprint-5-entry-verification.md
/docs/public-site/sprint-5-scope.md
/docs/public-site/sprint-5-route-register.md
/docs/public-site/sprint-5-content-readiness-register.md
/docs/delivery/sprint-5-branch-record.md
```

---

## Phase 2: Route and Feature Organization

### Objectives

- Establish route groups and feature boundaries for Products, Portfolio, Case Studies, Insights, Careers, Partnerships, Contact and supporting legal pages.
- Keep route composition separate from content models, queries and reusable components.
- Use server components by default and client components only for justified interaction.
- Keep CMS, identity, customer accounts, project intake, customer portal and payment features outside this sprint.
- Prevent incomplete routes from appearing in production navigation.
- Maintain stable route names for later CMS integration and search indexing.

### Files to create

```text
/apps/web/src/app/(public)/(products)/products/page.tsx
/apps/web/src/app/(public)/(products)/products/[slug]/page.tsx
/apps/web/src/app/(public)/(work)/portfolio/page.tsx
/apps/web/src/app/(public)/(work)/case-studies/[slug]/page.tsx
/apps/web/src/app/(public)/(insights)/insights/page.tsx
/apps/web/src/app/(public)/(insights)/insights/[slug]/page.tsx
/apps/web/src/app/(public)/(supporting)/careers/page.tsx
/apps/web/src/app/(public)/(supporting)/partnerships/page.tsx
/apps/web/src/app/(public)/(supporting)/contact/page.tsx
/apps/web/src/features/products/index.ts
/apps/web/src/features/portfolio/index.ts
/apps/web/src/features/insights/index.ts
/apps/web/src/features/supporting/index.ts
/docs/public-site/sprint-5-route-ownership.md
```

---

## Phase 3: Typed Content Models and Approval Controls

### Objectives

- Define typed content models for products, projects, case studies, insights, careers, partnerships and contact information.
- Keep the models compatible with later headless CMS integration.
- Represent publication status, approval status, evidence source and revision references explicitly.
- Prevent draft, expired or unapproved entries from rendering publicly.
- Validate slugs, metadata, media references, dates, statuses and relationships at build time.
- Prevent unverified client claims, testimonials, statistics and product availability statements.

### Files to create

```text
/apps/web/src/content/public/sprint-5-content.types.ts
/apps/web/src/content/public/sprint-5-content.schema.ts
/apps/web/src/content/public/sprint-5-content-validation.ts
/apps/web/src/content/public/sprint-5-content-validation.test.ts
/apps/web/src/content/public/publication-status.ts
/apps/web/src/content/public/evidence-reference.ts
/apps/web/src/types/product-content.ts
/apps/web/src/types/portfolio-content.ts
/apps/web/src/types/insight-content.ts
/docs/content/sprint-5-content-model.md
/docs/content/publication-status-policy.md
```

---

## Phase 4: Product Catalogue

### Objectives

- Implement the Products and Platforms catalogue.
- Present products according to objective readiness states such as concept, research, pilot, available and retired.
- Allow filtering by product status and relevant problem area.
- Prevent concept or research items from appearing commercially available.
- Provide clear actions for learning more, requesting a demonstration or registering interest only where supported.
- Preserve responsive, accessible and low-bandwidth behavior.

### Files to create

```text
/apps/web/src/app/(public)/(products)/products/page.test.tsx
/apps/web/src/features/products/ProductsPage.tsx
/apps/web/src/features/products/ProductsPage.test.tsx
/apps/web/src/features/products/ProductsHero.tsx
/apps/web/src/features/products/ProductGrid.tsx
/apps/web/src/features/products/ProductCard.tsx
/apps/web/src/features/products/ProductStatusBadge.tsx
/apps/web/src/features/products/ProductFilters.tsx
/apps/web/src/features/products/ProductInterestCallToAction.tsx
/apps/web/src/content/public/products.ts
/docs/public-site/products-page-specification.md
```

---

## Phase 5: Product Detail Framework

### Objectives

- Implement a reusable product-detail framework.
- Support problem statement, intended users, capabilities, availability, evidence, documentation and calls to action.
- Display availability and maturity prominently.
- Support limitations and dependencies without hiding material information.
- Generate metadata and structured data only from approved product content.
- Return not found for invalid, unpublished or unapproved product slugs.

### Files to create

```text
/apps/web/src/app/(public)/(products)/products/[slug]/page.test.tsx
/apps/web/src/features/products/ProductDetailPage.tsx
/apps/web/src/features/products/ProductDetailPage.test.tsx
/apps/web/src/features/products/ProductHero.tsx
/apps/web/src/features/products/ProductOverview.tsx
/apps/web/src/features/products/ProductCapabilities.tsx
/apps/web/src/features/products/ProductAvailability.tsx
/apps/web/src/features/products/ProductLimitations.tsx
/apps/web/src/features/products/ProductEvidence.tsx
/apps/web/src/features/products/ProductCallToAction.tsx
/apps/web/src/features/products/product-detail.types.ts
/docs/public-site/product-detail-framework.md
```

---

## Phase 6: Portfolio

### Objectives

- Implement the public portfolio experience.
- Support filtering by service, industry and approved project type.
- Distinguish client work, internal products, research and clearly labeled concept work.
- Respect confidentiality restrictions and suppress unapproved client identities.
- Provide stable links to approved case studies.
- Handle an empty or restricted portfolio state professionally.

### Files to create

```text
/apps/web/src/app/(public)/(work)/portfolio/page.test.tsx
/apps/web/src/features/portfolio/PortfolioPage.tsx
/apps/web/src/features/portfolio/PortfolioPage.test.tsx
/apps/web/src/features/portfolio/PortfolioHero.tsx
/apps/web/src/features/portfolio/PortfolioFilters.tsx
/apps/web/src/features/portfolio/ProjectGrid.tsx
/apps/web/src/features/portfolio/ProjectCard.tsx
/apps/web/src/features/portfolio/ConfidentialWorkNotice.tsx
/apps/web/src/features/portfolio/PortfolioEmptyState.tsx
/apps/web/src/content/public/portfolio.ts
/docs/public-site/portfolio-page-specification.md
```

---

## Phase 7: Case-Study Framework

### Objectives

- Implement evidence-led case-study pages.
- Present context, problem, approach, delivery, architecture, security considerations and measurable results.
- Require evidence references for quantitative claims.
- Support client-approved quotations only when approval records exist.
- Avoid exposing confidential architecture, testing evidence, personal data or client secrets.
- Return not found for unpublished or unauthorized case studies.

### Files to create

```text
/apps/web/src/app/(public)/(work)/case-studies/[slug]/page.test.tsx
/apps/web/src/features/portfolio/CaseStudyPage.tsx
/apps/web/src/features/portfolio/CaseStudyPage.test.tsx
/apps/web/src/features/portfolio/CaseStudyHero.tsx
/apps/web/src/features/portfolio/CaseStudyExecutiveSummary.tsx
/apps/web/src/features/portfolio/CaseStudyContext.tsx
/apps/web/src/features/portfolio/CaseStudyApproach.tsx
/apps/web/src/features/portfolio/CaseStudyArchitecture.tsx
/apps/web/src/features/portfolio/CaseStudySecurity.tsx
/apps/web/src/features/portfolio/CaseStudyResults.tsx
/apps/web/src/features/portfolio/CaseStudyRelatedServices.tsx
/apps/web/src/features/portfolio/case-study.types.ts
/docs/public-site/case-study-framework.md
```

---

## Phase 8: Portfolio Media and Evidence Controls

### Objectives

- Implement controlled galleries for approved images, video and project demonstrations.
- Require alternative text, captions and source attribution where applicable.
- Prevent sensitive metadata from being published with media files.
- Display concept work and simulated demonstrations with explicit labels.
- Optimize project media for mobile and constrained networks.
- Validate media ownership, approval and publication status.

### Files to create

```text
/apps/web/src/features/portfolio/ProjectMediaGallery.tsx
/apps/web/src/features/portfolio/ProjectMediaGallery.test.tsx
/apps/web/src/features/portfolio/ProjectMediaItem.tsx
/apps/web/src/features/portfolio/ProjectEvidenceLabel.tsx
/apps/web/src/lib/media/portfolio-media.ts
/apps/web/src/lib/media/portfolio-media.test.ts
/scripts/media/validate-portfolio-media.zsh
/docs/media/portfolio-media-policy.md
/docs/content/evidence-and-attribution.md
```

---

## Phase 9: Insights Hub

### Objectives

- Implement the Insights hub for research, engineering lessons, security updates, product announcements and company updates.
- Support search, topic, content-type and publication-date filters.
- Present featured and latest approved content.
- Preserve author, publication date, revision date and reading-time metadata.
- Provide clear empty and no-results states.
- Keep newsletter subscription as a controlled placeholder until the approved integration exists.

### Files to create

```text
/apps/web/src/app/(public)/(insights)/insights/page.test.tsx
/apps/web/src/features/insights/InsightsPage.tsx
/apps/web/src/features/insights/InsightsPage.test.tsx
/apps/web/src/features/insights/InsightsHero.tsx
/apps/web/src/features/insights/FeaturedInsight.tsx
/apps/web/src/features/insights/InsightFilters.tsx
/apps/web/src/features/insights/InsightSearch.tsx
/apps/web/src/features/insights/InsightGrid.tsx
/apps/web/src/features/insights/InsightCard.tsx
/apps/web/src/features/insights/InsightNoResults.tsx
/apps/web/src/content/public/insights.ts
/docs/public-site/insights-page-specification.md
```

---

## Phase 10: Insight Article Framework

### Objectives

- Implement accessible article pages.
- Support headings, paragraphs, lists, quotations, code, media, tables and callouts through controlled renderers.
- Generate reading time, metadata and related-content links.
- Preserve semantic heading order and accessible code presentation.
- Prevent arbitrary script or unsafe HTML execution.
- Return not found for draft, expired or unknown insight slugs.

### Files to create

```text
/apps/web/src/app/(public)/(insights)/insights/[slug]/page.test.tsx
/apps/web/src/features/insights/InsightArticlePage.tsx
/apps/web/src/features/insights/InsightArticlePage.test.tsx
/apps/web/src/features/insights/ArticleHeader.tsx
/apps/web/src/features/insights/ArticleBody.tsx
/apps/web/src/features/insights/ArticleMetadata.tsx
/apps/web/src/features/insights/ArticleAuthor.tsx
/apps/web/src/features/insights/ArticleRelatedContent.tsx
/apps/web/src/features/insights/ArticleShareLinks.tsx
/apps/web/src/features/insights/article-renderers.tsx
/apps/web/src/features/insights/article.types.ts
/docs/public-site/insight-article-framework.md
```

---

## Phase 11: Public Content Search

### Objectives

- Implement search across approved products, projects, case studies and insights.
- Use a build-time or server-side local index appropriate to the current content volume.
- Support typo-tolerant normalization only where deterministic and safe.
- Prevent draft and restricted content from entering the public index.
- Provide accessible search results and no-results guidance.
- Avoid adopting an external search service before evidence justifies it.

### Files to create

```text
/apps/web/src/app/(public)/search/page.tsx
/apps/web/src/app/(public)/search/page.test.tsx
/apps/web/src/features/search/SearchPage.tsx
/apps/web/src/features/search/SearchForm.tsx
/apps/web/src/features/search/SearchResults.tsx
/apps/web/src/features/search/SearchResultItem.tsx
/apps/web/src/features/search/SearchNoResults.tsx
/apps/web/src/lib/search/build-index.ts
/apps/web/src/lib/search/query-index.ts
/apps/web/src/lib/search/search.types.ts
/apps/web/src/lib/search/search.test.ts
/scripts/content/build-public-search-index.zsh
/docs/public-site/public-search.md
```

---

## Phase 12: Careers Page

### Objectives

- Implement the Careers page and culture narrative.
- Present approved employment, internship and talent-community information.
- Support job-listing placeholders from approved local content only.
- Avoid collecting applications until the approved application workflow exists.
- Provide accessible contact or interest actions without misrepresenting vacancies.
- Include candidate privacy guidance.

### Files to create

```text
/apps/web/src/app/(public)/(supporting)/careers/page.test.tsx
/apps/web/src/features/supporting/CareersPage.tsx
/apps/web/src/features/supporting/CareersPage.test.tsx
/apps/web/src/features/supporting/careers/CareersHero.tsx
/apps/web/src/features/supporting/careers/CultureAndValues.tsx
/apps/web/src/features/supporting/careers/OpportunityList.tsx
/apps/web/src/features/supporting/careers/TalentCommunityNotice.tsx
/apps/web/src/features/supporting/careers/CandidatePrivacyNotice.tsx
/apps/web/src/content/public/careers.ts
/docs/public-site/careers-page-specification.md
```

---

## Phase 13: Partnerships Page

### Objectives

- Implement the Partnerships page.
- Explain technology, research, delivery, education and ecosystem partnership categories.
- Set clear partnership expectations and evaluation criteria.
- Provide a controlled contact action until the structured partnership workflow exists.
- Avoid implying active partnerships without approved evidence.
- Preserve professional procurement and institutional language.

### Files to create

```text
/apps/web/src/app/(public)/(supporting)/partnerships/page.test.tsx
/apps/web/src/features/supporting/PartnershipsPage.tsx
/apps/web/src/features/supporting/PartnershipsPage.test.tsx
/apps/web/src/features/supporting/partnerships/PartnershipsHero.tsx
/apps/web/src/features/supporting/partnerships/PartnershipTypes.tsx
/apps/web/src/features/supporting/partnerships/PartnershipPrinciples.tsx
/apps/web/src/features/supporting/partnerships/PartnershipCriteria.tsx
/apps/web/src/features/supporting/partnerships/PartnershipCallToAction.tsx
/apps/web/src/content/public/partnerships.ts
/docs/public-site/partnerships-page-specification.md
```

---

## Phase 14: Contact Page

### Objectives

- Implement the public Contact page.
- Provide approved contact channels and expected response guidance.
- Route service, partnership, careers, media and security enquiries clearly.
- Avoid collecting sensitive project or security information through an unprotected generic form.
- Provide an urgent-security or responsible-disclosure route where approved.
- Keep consultation booking and structured project intake deferred to the approved sprint.

### Files to create

```text
/apps/web/src/app/(public)/(supporting)/contact/page.test.tsx
/apps/web/src/features/supporting/ContactPage.tsx
/apps/web/src/features/supporting/ContactPage.test.tsx
/apps/web/src/features/supporting/contact/ContactHero.tsx
/apps/web/src/features/supporting/contact/ContactChannels.tsx
/apps/web/src/features/supporting/contact/EnquiryRouting.tsx
/apps/web/src/features/supporting/contact/ResponseExpectations.tsx
/apps/web/src/features/supporting/contact/SecurityDisclosureRoute.tsx
/apps/web/src/content/public/contact.ts
/docs/public-site/contact-page-specification.md
```

---

## Phase 15: Legal, Privacy and Trust Pages

### Objectives

- Implement public legal and trust pages required before wider release.
- Publish approved privacy, terms, cookie, accessibility and responsible-disclosure content.
- Present effective dates and revision dates.
- Keep legal wording controlled and reviewable.
- Avoid generating jurisdiction-specific commitments without approval.
- Make trust pages reachable from the global footer.

### Files to create

```text
/apps/web/src/app/(public)/(legal)/privacy/page.tsx
/apps/web/src/app/(public)/(legal)/terms/page.tsx
/apps/web/src/app/(public)/(legal)/cookies/page.tsx
/apps/web/src/app/(public)/(legal)/accessibility/page.tsx
/apps/web/src/app/(public)/(legal)/responsible-disclosure/page.tsx
/apps/web/src/features/legal/LegalPageLayout.tsx
/apps/web/src/features/legal/LegalDocumentMetadata.tsx
/apps/web/src/features/legal/index.ts
/apps/web/src/content/public/legal/privacy.ts
/apps/web/src/content/public/legal/terms.ts
/apps/web/src/content/public/legal/cookies.ts
/apps/web/src/content/public/legal/accessibility.ts
/apps/web/src/content/public/legal/responsible-disclosure.ts
/docs/legal/public-legal-content-control.md
```

---

## Phase 16: Cookie and Consent Interface Foundation

### Objectives

- Implement a consent interface for essential and optional categories.
- Keep essential storage separate from analytics and marketing consent.
- Allow users to revisit and change preferences.
- Prevent optional analytics from loading before valid consent.
- Store only the consent state required for the defined purpose.
- Preserve accessibility and keyboard operability.

### Files to create

```text
/apps/web/src/components/consent/ConsentBanner.tsx
/apps/web/src/components/consent/ConsentBanner.test.tsx
/apps/web/src/components/consent/ConsentPreferences.tsx
/apps/web/src/components/consent/ConsentCategory.tsx
/apps/web/src/components/consent/ConsentSettingsLink.tsx
/apps/web/src/lib/consent/consent.types.ts
/apps/web/src/lib/consent/consent-storage.ts
/apps/web/src/lib/consent/consent-storage.test.ts
/apps/web/src/lib/consent/consent-policy.ts
/docs/privacy/consent-interface.md
```

---

## Phase 17: Navigation and Footer Completion

### Objectives

- Add Products, Work, Insights, Careers, Partnerships, Contact and trust pages to the approved navigation model.
- Keep the primary navigation concise.
- Place supporting and legal destinations in the footer or appropriate secondary navigation.
- Preserve mobile focus management and active-location behavior.
- Prevent incomplete later-sprint destinations from appearing.
- Verify every destination and label.

### Files to create

```text
/apps/web/src/components/navigation/sprint-5-navigation.config.ts
/apps/web/src/components/navigation/sprint-5-navigation.test.ts
/apps/web/src/components/navigation/FooterNavigation.tsx
/apps/web/src/components/navigation/FooterNavigation.test.tsx
/apps/web/src/components/navigation/TrustNavigation.tsx
/apps/web/src/components/navigation/ContentSearchLink.tsx
/docs/public-site/sprint-5-navigation.md
```

---

## Phase 18: Metadata, Structured Data and Sitemap Expansion

### Objectives

- Add unique metadata for every Sprint 5 route.
- Add appropriate product, article, breadcrumb and organization structured data.
- Exclude draft and restricted content from metadata and sitemap output.
- Include only completed and approved routes in the sitemap.
- Preserve staging no-index behavior.
- Validate canonical URLs and content dates.

### Files to create

```text
/apps/web/src/content/public/sprint-5-metadata.ts
/apps/web/src/lib/seo/product-structured-data.ts
/apps/web/src/lib/seo/article-structured-data.ts
/apps/web/src/lib/seo/case-study-structured-data.ts
/apps/web/src/lib/seo/sprint-5-sitemap.ts
/apps/web/src/lib/seo/sprint-5-seo.test.ts
/apps/web/tests/seo/sprint-5-metadata.spec.ts
/apps/web/tests/seo/sprint-5-structured-data.spec.ts
/scripts/quality/validate-sprint-5-seo.zsh
/docs/seo/sprint-5-seo.md
```

---

## Phase 19: Loading, Empty, No-Results and Error States

### Objectives

- Implement route-level loading and error boundaries for Sprint 5 route groups.
- Provide empty states for unavailable products, portfolio entries, careers and related content.
- Provide no-results states for filters and search.
- Preserve user-entered query and filter context where safe.
- Avoid sensitive error disclosure.
- Provide clear recovery actions.

### Files to create

```text
/apps/web/src/app/(public)/(products)/loading.tsx
/apps/web/src/app/(public)/(products)/error.tsx
/apps/web/src/app/(public)/(work)/loading.tsx
/apps/web/src/app/(public)/(work)/error.tsx
/apps/web/src/app/(public)/(insights)/loading.tsx
/apps/web/src/app/(public)/(insights)/error.tsx
/apps/web/src/app/(public)/(supporting)/loading.tsx
/apps/web/src/app/(public)/(supporting)/error.tsx
/apps/web/src/components/states/SearchNoResults.tsx
/apps/web/src/components/states/RestrictedContentState.tsx
/apps/web/tests/resilience/sprint-5-errors.spec.ts
/docs/public-site/sprint-5-states.md
```

---

## Phase 20: Unit and Integration Testing

### Objectives

- Add unit tests for components with meaningful behavior.
- Add page-composition tests for all Sprint 5 route types.
- Verify publication-status, evidence, confidentiality and product-readiness controls.
- Verify filters, search, consent and navigation.
- Verify metadata and structured-data generation.
- Keep tests deterministic and independent of unapproved external services.

### Files to create

```text
/apps/web/src/features/products/ProductsPage.integration.test.tsx
/apps/web/src/features/products/ProductDetailPage.integration.test.tsx
/apps/web/src/features/portfolio/PortfolioPage.integration.test.tsx
/apps/web/src/features/portfolio/CaseStudyPage.integration.test.tsx
/apps/web/src/features/insights/InsightsPage.integration.test.tsx
/apps/web/src/features/insights/InsightArticlePage.integration.test.tsx
/apps/web/src/features/supporting/CareersPage.integration.test.tsx
/apps/web/src/features/supporting/PartnershipsPage.integration.test.tsx
/apps/web/src/features/supporting/ContactPage.integration.test.tsx
/apps/web/src/testing/sprint-5-content-builders.ts
/docs/quality/sprint-5-testing.md
```

---

## Phase 21: End-to-End Public Journey Testing

### Objectives

- Verify product discovery and maturity-state comprehension.
- Verify portfolio filtering and case-study navigation.
- Verify insight search, filtering and article navigation.
- Verify Careers, Partnerships and Contact journeys.
- Verify legal, privacy, consent and responsible-disclosure access.
- Verify keyboard-only and mobile completion of all priority journeys.

### Files to create

```text
/apps/web/tests/e2e/product-discovery.spec.ts
/apps/web/tests/e2e/product-status.spec.ts
/apps/web/tests/e2e/portfolio-and-case-study.spec.ts
/apps/web/tests/e2e/insight-search-and-article.spec.ts
/apps/web/tests/e2e/careers-partnerships-contact.spec.ts
/apps/web/tests/e2e/legal-privacy-consent.spec.ts
/apps/web/tests/e2e/sprint-5-mobile-navigation.spec.ts
/apps/web/tests/e2e/sprint-5-keyboard-journeys.spec.ts
/docs/evidence/sprint-5-public-journey-results.md
```

---

## Phase 22: Accessibility Validation

### Objectives

- Run automated accessibility tests across every Sprint 5 route.
- Verify filters, search, article content, galleries, consent controls and status labels.
- Verify headings, landmarks, alternative text and link purpose.
- Verify keyboard operation, visible focus and focus restoration.
- Verify 200 percent zoom and responsive reflow.
- Record manual testing and resolve critical or serious defects.

### Files to create

```text
/apps/web/tests/accessibility/products.spec.ts
/apps/web/tests/accessibility/portfolio-case-studies.spec.ts
/apps/web/tests/accessibility/insights.spec.ts
/apps/web/tests/accessibility/supporting-pages.spec.ts
/apps/web/tests/accessibility/legal-and-consent.spec.ts
/apps/web/tests/accessibility/sprint-5-reflow.spec.ts
/docs/evidence/sprint-5-accessibility-automated.md
/docs/evidence/sprint-5-accessibility-manual.md
```

---

## Phase 23: Responsive, Cross-Browser and Visual Validation

### Objectives

- Test every Sprint 5 route at approved mobile, tablet, desktop, landscape and ultrawide widths.
- Verify filters, grids, articles, legal content, media galleries and consent interfaces.
- Verify mainstream browser behavior.
- Capture approved visual baselines.
- Resolve overflow, clipping, wrapping and spacing defects.
- Verify constrained-network media behavior.

### Files to create

```text
/apps/web/tests/responsive/sprint-5-mobile.spec.ts
/apps/web/tests/responsive/sprint-5-tablet.spec.ts
/apps/web/tests/responsive/sprint-5-desktop.spec.ts
/apps/web/tests/responsive/sprint-5-ultrawide.spec.ts
/apps/web/tests/responsive/sprint-5-landscape.spec.ts
/apps/web/tests/cross-browser/sprint-5-public-pages.spec.ts
/apps/web/tests/visual/sprint-5-public-pages.visual.spec.ts
/docs/evidence/sprint-5-responsive-results.md
/docs/evidence/sprint-5-cross-browser-results.md
/docs/evidence/sprint-5-visual-baselines.md
```

---

## Phase 24: Performance and Search-Index Validation

### Objectives

- Measure Core Web Vitals, page weight, request count and client JavaScript for Sprint 5 pages.
- Verify image and article-media optimization.
- Verify search-index generation excludes draft and restricted content.
- Verify static-generation and caching behavior.
- Resolve all approved performance-budget violations.
- Record staging measurements as completion evidence.

### Files to create

```text
/apps/web/tests/performance/sprint-5-products.spec.ts
/apps/web/tests/performance/sprint-5-portfolio.spec.ts
/apps/web/tests/performance/sprint-5-insights.spec.ts
/apps/web/tests/performance/sprint-5-supporting-pages.spec.ts
/apps/web/tests/search/public-index-exclusions.spec.ts
/apps/web/lighthouse.sprint-5.config.cjs
/scripts/quality/validate-sprint-5-performance.zsh
/scripts/quality/validate-public-search-index.zsh
/docs/evidence/sprint-5-performance-summary.md
/docs/evidence/sprint-5-search-index-verification.md
```

---

## Phase 25: Security and Privacy Validation

### Objectives

- Verify article rendering cannot execute unsafe HTML or scripts.
- Verify unpublished and restricted content cannot be enumerated publicly.
- Verify product and case-study slugs resist traversal and unsafe redirects.
- Verify consent controls block optional analytics until consent.
- Verify client bundles expose no secret or restricted content.
- Run dependency and frontend security scans and resolve critical or high-risk findings.

### Files to create

```text
/apps/web/tests/security/article-sanitization.spec.ts
/apps/web/tests/security/content-enumeration.spec.ts
/apps/web/tests/security/sprint-5-route-inputs.spec.ts
/apps/web/tests/security/consent-enforcement.spec.ts
/apps/web/tests/security/sprint-5-client-bundle.spec.ts
/scripts/security/scan-sprint-5-frontend.zsh
/docs/evidence/sprint-5-security-scan.md
/docs/evidence/sprint-5-privacy-review.md
```

---

## Phase 26: CI/CD Quality-Gate Expansion

### Objectives

- Add Sprint 5 content, route, search, consent, accessibility, performance and security checks to pull-request validation.
- Preserve complete evidence as workflow artifacts.
- Prevent draft or restricted content from reaching staging.
- Build and publish the web image only after all required validation passes.
- Fail the pipeline when any required underlying command fails.
- Keep later-sprint features excluded.

### Files to create

```text
/.github/workflows/ci-sprint-5-public-content.yml
/.github/workflows/test-products-portfolio-insights.yml
/.github/workflows/test-sprint-5-accessibility.yml
/.github/workflows/test-sprint-5-search-and-seo.yml
/.github/workflows/test-sprint-5-performance.yml
/.github/workflows/test-sprint-5-security.yml
/scripts/ci/verify-sprint-5-content.zsh
/scripts/ci/verify-sprint-5-routes.zsh
/scripts/ci/verify-sprint-5-quality-gates.zsh
/docs/delivery/sprint-5-quality-gates.md
```

---

## Phase 27: Development and Staging Deployment

### Objectives

- Build a verified commit-tagged web image containing Sprint 5 features.
- Deploy to the Azure development environment and execute smoke, journey, accessibility, search, performance and security checks.
- Promote the exact verified image to staging.
- Verify metadata, sitemap, search index, consent controls and telemetry in staging.
- Verify staging remains non-indexable.
- Verify rollback to the previous healthy web revision.
- Keep CMS, identity, project intake, customer portal and payment routes unavailable.

### Files to create

```text
/scripts/cloud/deploy-sprint-5-development.zsh
/scripts/cloud/deploy-sprint-5-staging.zsh
/scripts/cloud/smoke-test-sprint-5-public-pages.zsh
/scripts/cloud/verify-sprint-5-staging.zsh
/tests/deployment/sprint-5-development-smoke-tests.json
/tests/deployment/sprint-5-staging-smoke-tests.json
/docs/evidence/sprint-5-development-deployment.md
/docs/evidence/sprint-5-staging-deployment.md
/docs/evidence/sprint-5-web-rollback-verification.md
```

---

## Phase 28: Documentation and Governance

### Objectives

- Document ownership and maintenance rules for Sprint 5 pages and content.
- Document product-status, evidence, confidentiality, publication and article-rendering rules.
- Document search-index maintenance and consent behavior.
- Record architecture decisions made during implementation.
- Keep documentation aligned with source code and tests.
- Document Kali Debian and Zsh validation procedures.

### Files to create

```text
/docs/public-site/sprint-5-page-ownership.md
/docs/content/product-status-governance.md
/docs/content/case-study-evidence-governance.md
/docs/content/insight-publication-governance.md
/docs/search/public-search-governance.md
/docs/privacy/consent-governance.md
/docs/architecture/adr/0020-use-local-public-search-index.md
/docs/architecture/adr/0021-enforce-publication-status-at-build-and-runtime.md
/docs/architecture/adr/0022-use-controlled-article-renderers.md
/docs/development/sprint-5-kali-debian-zsh.md
/docs/development/sprint-5-troubleshooting.md
```

---

## Phase 29: Integrated Validation and Sprint Closure

### Objectives

- Validate every Sprint 5 route from a clean checkout.
- Verify formatting, linting, strict TypeScript, content schemas and publication controls.
- Execute all unit, integration, end-to-end, accessibility, responsive, cross-browser, visual, performance, search, SEO, privacy and security tests.
- Build the production Next.js application and public search index.
- Build and publish the verified web container image.
- Verify development and staging deployments, telemetry and rollback.
- Confirm CMS, identity, project intake, customer portal and payment features have not been started outside approved scope.
- Update documentation to match the verified implementation.
- Create the verified Development Sprint 5 Git commit and push the development branch.
- Create a pull request only after every required validation passes.
- Stop at the Development Sprint 5 completion gate before beginning the next sprint.

### Files to create

```text
/scripts/release/sprint-5-final-validation.zsh
/docs/evidence/sprint-5-content-validation.md
/docs/evidence/sprint-5-route-validation.md
/docs/evidence/sprint-5-journey-summary.md
/docs/evidence/sprint-5-accessibility-summary.md
/docs/evidence/sprint-5-responsive-summary.md
/docs/evidence/sprint-5-performance-summary.md
/docs/evidence/sprint-5-search-and-seo-summary.md
/docs/evidence/sprint-5-security-and-privacy-summary.md
/docs/evidence/sprint-5-deployment-summary.md
/docs/evidence/sprint-5-completion-record.md
/docs/delivery/sprint-5-pull-request.md
```

---


## Development Sprint 5 Completion Gate

Development Sprint 5 is complete only when every condition below passes:

- The Products and Platforms catalogue is complete and renders successfully.
- Product-detail pages enforce approved publication and maturity states.
- Concept, research, pilot, available and retired statuses are communicated accurately.
- The Portfolio page is complete and renders successfully.
- Case-study pages are complete and enforce evidence and confidentiality controls.
- Unapproved client identities, claims, testimonials and project details are not published.
- The Insights hub and article pages are complete and render safely.
- Public search excludes draft, restricted and unpublished content.
- Careers, Partnerships and Contact pages are complete.
- Privacy, Terms, Cookies, Accessibility and Responsible Disclosure pages are reachable and approved.
- Consent controls prevent optional analytics from loading before consent.
- Global navigation and footer include only complete and approved destinations.
- Loading, empty, no-results, restricted, not-found and error states work safely.
- Metadata, canonical URLs, structured data and sitemap entries pass validation.
- Staging remains non-indexable.
- All Sprint 5 pages use the approved Noviq design system.
- Mobile, tablet, desktop, landscape and ultrawide layouts pass.
- Keyboard navigation, visible focus and screen-reader semantics pass.
- Automated and required manual accessibility checks pass.
- Responsive media and constrained-network behavior meet the approved standard.
- Core public journeys pass end-to-end testing.
- Frontend performance budgets and Core Web Vitals targets pass.
- Article-rendering and content-enumeration security checks pass.
- No secret, restricted content or server-only configuration is exposed to the browser.
- The production Next.js application and public search index build successfully.
- The verified web image is deployed to development and staging.
- Development and staging smoke tests pass.
- Frontend telemetry reaches the approved Azure monitoring resources.
- Web-revision rollback is verified.
- Documentation matches the verified implementation.
- A verified Development Sprint 5 Git commit exists.
- The Development Sprint 5 development branch is pushed to GitHub.
- The pull request is created only after all required validations pass.
- No unresolved critical, high-risk or blocking defect remains.
- The next sprint has not started.

## Development Sprint 5 Final Completion Marker

```text
NOVIQ_LABS_DEVELOPMENT_SPRINT_5_COMPLETE
```
