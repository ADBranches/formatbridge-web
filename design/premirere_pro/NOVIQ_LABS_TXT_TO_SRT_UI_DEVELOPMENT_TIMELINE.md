# Noviq Labs TXT-to-SRT Converter UI Development Timeline

**Organization:** Noviq Labs Ltd  
**Product:** TXT-to-SRT Converter  
**Current stable release:** `v1.0.0`  
**Target UI release:** `v1.1.0`  
**Implementation language:** PHP 8.2+  
**UI approach:** Server-rendered PHP, progressive JavaScript enhancement, responsive CSS  
**Delivery approach:** Fast-track, priority-ordered development  
**Prepared:** 15 September 2026  
**Target duration:** 4 working days

## 1. Project Goal

Add a branded browser interface to the tested TXT-to-SRT conversion engine without duplicating or weakening the existing conversion, validation, repair, security, batch-processing, and overwrite-protection controls.

The interface will allow a user to paste or upload timestamped lyrics, correct problems by source line, preview generated captions, convert the content, and download a Premiere-ready `.srt` file. Version `1.0.0` remains intact while all UI development occurs on the dedicated `development` branch toward version `1.1.0`.

## 2. Priority Order

The UI implementation must follow this dependency order:

1. Protect the existing `v1.0.0` release and inspect the current architecture.
2. Create the HTTP application boundary and secure request handling.
3. Build the core TXT editor and conversion workflow.
4. Add preview, validation feedback, repair controls, and downloads.
5. Apply the official Noviq Labs Ltd visual system and responsive behavior.
6. Add batch upload and advanced usability features.
7. Complete automated accessibility, security, browser, and regression testing.
8. Package, document, tag, and publish version `1.1.0`.

## 3. Official Noviq Labs Ltd UI Colors

All interface colors must be sourced from centralized tokens.

```text
Noviq Navy:  #102337
Noviq Teal:  #45BEA6
Noviq Blue:  #00AEEF
Noviq Mint:  #C4E5DB
Noviq White: #F8FCFE
```

Planned semantic usage:

- **Primary navigation and strong text:** Noviq Navy
- **Primary success actions:** Noviq Teal
- **Links, focus indicators, and information states:** Noviq Blue
- **Supporting surfaces and subtle status backgrounds:** Noviq Mint
- **Main application background:** Noviq White
- **Error colors:** a dedicated accessible error token approved during Phase 1
- **Focus and contrast:** must meet WCAG 2.2 AA requirements

## 4. Proposed UI Architecture

```text
Browser request
    ↓
public/index.php
    ↓
HTTP request validation and CSRF protection
    ↓
UI controller
    ↓
Existing TXT parser, validators, repairer, formatter, and converter
    ↓
Preview or atomic SRT generation
    ↓
Secure browser download
```

The existing domain and application services remain the source of truth. UI controllers must not reproduce timestamp parsing, SRT formatting, overlap detection, repair logic, or output validation.

---

# 5. UI Development Timeline

## Phase 1: UI Requirements, Architecture, and Release Protection

**Duration:** 0.5 working day  
**Target:** Day 1, morning  
**Priority:** Critical foundation

### Objectives

- Verify the `v1.0.0` tag, release commit, clean working tree, and remote alignment.
- Confirm all UI development occurs on `development` or a dedicated UI branch based on `development`.
- Inspect existing conversion services before modification.
- Define the browser user journeys and acceptance criteria.
- Define input size, upload count, filename, MIME, session, and download rules.
- Define the server-rendered PHP architecture and progressive enhancement boundary.
- Define accessible design tokens using the official Noviq Labs Ltd colors.
- Define UI error states, empty states, success states, and loading states.
- Define the route map and UI security controls.
- Preserve CLI behavior and `v1.0.0` compatibility.

### Files to create

- `docs/UI_REQUIREMENTS.md`
- `docs/UI_ARCHITECTURE.md`
- `docs/UI_USER_FLOWS.md`
- `docs/UI_SECURITY_RULES.md`
- `docs/UI_ACCESSIBILITY_RULES.md`
- `config/ui.php`
- `config/security.php`
- `resources/css/tokens.css`

### Files to inspect and modify only if required

- `README.md`
- `composer.json`
- `config/brand.php`
- `.gitignore`
- `.gitattributes`

### Completion gate

- Current release and Git state are verified.
- UI routes and user journeys are documented.
- UI security limits and validation boundaries are explicit.
- Brand tokens are centralized and contrast requirements are documented.
- Existing CLI behavior remains unchanged.
- A verified Phase 1 commit is created and pushed.

---

## Phase 2: HTTP Foundation and Secure Application Bootstrap

**Duration:** 0.75 working day  
**Target:** Day 1, afternoon  
**Priority:** Required before visual screens

### Objectives

- Create the public web entry point.
- Add request and response abstractions.
- Add routing for editor, convert, preview, download, and health endpoints.
- Add session initialization and CSRF token protection.
- Add secure HTTP headers.
- Add centralized exception handling with safe user-facing messages.
- Add temporary-file lifecycle controls.
- Prevent direct browser access to source, configuration, tests, and temporary data.
- Add a development server command without changing CLI conversion behavior.

### Files to create

- `public/index.php`
- `public/.htaccess`
- `src/Http/Router.php`
- `src/Http/Request.php`
- `src/Http/Response.php`
- `src/Http/Session.php`
- `src/Http/CsrfTokenManager.php`
- `src/Http/SecurityHeaders.php`
- `src/Http/UploadedFile.php`
- `src/Http/HttpException.php`
- `src/Controller/EditorController.php`
- `src/Controller/HealthController.php`
- `src/Support/TemporaryFileManager.php`
- `bin/serve-ui`

### Files to modify

- `composer.json`
- `.gitignore`
- `README.md`
- `config/security.php`
- `phpstan.neon`
- `phpcs.xml`

### Completion gate

- The PHP development server starts successfully.
- The editor route returns a valid HTML response.
- CSRF tokens are generated and verified.
- Security headers are present.
- Invalid routes return safe `404` responses.
- Temporary files are removed after request completion.
- CLI regression tests remain green.
- A verified Phase 2 commit is created and pushed.

---

## Phase 3: Core Editor, Upload, Convert, and Download Workflow

**Duration:** 1 working day  
**Target:** Day 2, morning through afternoon  
**Priority:** First usable graphical interface

### Objectives

- Build the main browser editor.
- Allow users to paste timestamped TXT content.
- Allow one `.txt` file upload.
- Populate the editor with uploaded UTF-8 content.
- Provide a copy-ready starter template.
- Add repair-mode and overwrite controls.
- Submit content to the existing PHP conversion engine.
- Generate an internally validated SRT file.
- Return the generated SRT as a safe browser download.
- Preserve Unicode text and punctuation.
- Prevent path traversal, unsafe filenames, oversized uploads, and unsupported file types.
- Display truthful success or failure states.

### Files to create

- `src/Controller/ConversionController.php`
- `src/Controller/DownloadController.php`
- `src/Application/ConvertTextContent.php`
- `src/Http/DownloadResponse.php`
- `src/Validation/UploadValidator.php`
- `src/Support/SafeFilename.php`
- `resources/views/layout.php`
- `resources/views/editor.php`
- `resources/views/components/header.php`
- `resources/views/components/editor-form.php`
- `resources/views/components/status-message.php`
- `resources/views/components/footer.php`
- `resources/css/app.css`
- `resources/js/editor.js`

### Files to modify

- `public/index.php`
- `src/Http/Router.php`
- `src/Controller/EditorController.php`
- `config/ui.php`
- `config/security.php`
- `composer.json`
- `README.md`

### Completion gate

- Pasted TXT content converts and downloads as a valid `.srt` file.
- Uploaded TXT content loads into the editor and converts successfully.
- Invalid uploads fail safely with no output file.
- Unicode lyrics remain intact.
- Overwrite remains disabled unless explicitly selected.
- Existing parser, repair, formatter, and SRT validator are reused.
- The CLI test suite remains green.
- A verified Phase 3 commit is created and pushed.

---

## Phase 4: Live Validation, Caption Preview, and Repair Experience

**Duration:** 0.75 working day  
**Target:** Day 3, morning  
**Priority:** High usability

### Objectives

- Add line numbers to the editor.
- Add browser-side syntax feedback for immediate guidance.
- Keep server-side PHP validation authoritative.
- Highlight malformed rows by source line.
- Display reversed timestamp, overlap, empty lyric, and invalid-range errors clearly.
- Add a structured caption preview showing index, start, end, duration, and text.
- Add repair-mode explanation before conversion.
- Show exactly which safe normalizations are supported.
- Add copy-to-clipboard and clear-editor actions.
- Add character and caption counts.
- Add keyboard-accessible status announcements.
- Prevent the preview from being mistaken for a successful final conversion.

### Files to create

- `src/Controller/PreviewController.php`
- `src/Application/PreviewConversion.php`
- `src/Support/PreviewResult.php`
- `resources/views/components/caption-preview.php`
- `resources/views/components/validation-summary.php`
- `resources/views/components/repair-options.php`
- `resources/js/line-numbers.js`
- `resources/js/live-validation.js`
- `resources/js/preview.js`
- `resources/css/editor.css`
- `resources/css/preview.css`

### Files to modify

- `public/index.php`
- `src/Http/Router.php`
- `resources/views/editor.php`
- `resources/views/components/editor-form.php`
- `resources/css/app.css`
- `resources/js/editor.js`
- `docs/ERROR_REFERENCE.md`
- `README.md`

### Completion gate

- Source-line validation errors are displayed accurately.
- Preview numbering and timestamps match final SRT output.
- Repair mode changes only documented minor formatting issues.
- Preview failure never appears as conversion success.
- Keyboard users can reach and operate every editor action.
- Screen readers receive status updates.
- A verified Phase 4 commit is created and pushed.

---

## Phase 5: Noviq Labs Visual System and Responsive Interface

**Duration:** 0.75 working day  
**Target:** Day 3, afternoon  
**Priority:** Brand and production usability

### Objectives

- Apply the official Noviq Labs Ltd colors through CSS variables.
- Build a clean light-dominant interface.
- Apply Navy to primary text and navigation.
- Apply Teal to primary success actions.
- Apply Blue to focus, links, and information states.
- Apply Mint to supporting surfaces.
- Add reusable buttons, fields, cards, badges, alerts, and loading states.
- Ensure mobile, tablet, laptop, and wide-screen responsiveness.
- Ensure sufficient color contrast and visible keyboard focus.
- Respect reduced-motion preferences.
- Prevent color from being the only status indicator.
- Add a concise project journey and version indicator.

### Files to create

- `resources/css/base.css`
- `resources/css/components.css`
- `resources/css/responsive.css`
- `resources/css/accessibility.css`
- `resources/views/components/navigation.php`
- `resources/views/components/action-bar.php`
- `resources/views/components/version-badge.php`
- `resources/views/components/journey-summary.php`
- `docs/UI_STYLE_GUIDE.md`

### Files to modify

- `resources/css/tokens.css`
- `resources/css/app.css`
- `resources/css/editor.css`
- `resources/css/preview.css`
- `resources/views/layout.php`
- `resources/views/editor.php`
- `resources/views/components/header.php`
- `resources/views/components/footer.php`
- `config/brand.php`
- `config/ui.php`
- `README.md`

### Completion gate

- Official brand colors come from centralized tokens.
- The interface is usable at mobile, tablet, and desktop widths.
- Keyboard focus is always visible.
- Text and controls meet WCAG 2.2 AA contrast targets.
- Reduced-motion behavior is supported.
- Status meaning is communicated with text and structure, not color alone.
- A verified Phase 5 commit is created and pushed.

---

## Phase 6: Batch Upload and Advanced Usability

**Duration:** 0.75 working day  
**Target:** Day 4, morning  
**Priority:** Productivity enhancement

### Objectives

- Add multiple TXT file selection.
- Add drag-and-drop input with an accessible file-picker fallback.
- Reuse existing batch conversion behavior.
- Show a per-file processing list.
- Report passed, skipped, and failed counts truthfully.
- Allow downloading individual SRT files.
- Add a ZIP download for multiple successful conversions.
- Protect existing generated names from collisions.
- Preserve relative naming without accepting user-controlled paths.
- Enforce upload count and total-size limits.
- Ensure one failed file does not falsely mark the entire batch successful.
- Add progress behavior without requiring a JavaScript framework.

### Files to create

- `src/Controller/BatchConversionController.php`
- `src/Controller/ArchiveDownloadController.php`
- `src/Application/ConvertUploadedBatch.php`
- `src/Support/BatchConversionResult.php`
- `src/Support/ZipArchiveBuilder.php`
- `resources/views/batch.php`
- `resources/views/components/drop-zone.php`
- `resources/views/components/file-list.php`
- `resources/views/components/batch-summary.php`
- `resources/js/batch-upload.js`
- `resources/css/batch.css`

### Files to modify

- `public/index.php`
- `src/Http/Router.php`
- `src/Validation/UploadValidator.php`
- `src/Support/SafeFilename.php`
- `config/security.php`
- `config/ui.php`
- `resources/views/layout.php`
- `resources/views/components/navigation.php`
- `resources/css/app.css`
- `README.md`

### Completion gate

- Single and multiple TXT uploads both work.
- Batch conversion summaries are accurate.
- Failed files are isolated and reported clearly.
- ZIP output contains only successful, internally validated SRT files.
- Upload size and count limits are enforced.
- Drag-and-drop has a keyboard-accessible alternative.
- Temporary uploads and generated archives are removed safely.
- A verified Phase 6 commit is created and pushed.

---

## Phase 7: Automated UI, Security, Accessibility, and Regression Tests

**Duration:** 1 working day  
**Target:** Day 4 afternoon through Day 5 morning  
**Priority:** Release gate

### Objectives

- Test editor page rendering.
- Test paste, upload, preview, conversion, and download workflows.
- Test Unicode lyrics and punctuation.
- Test malformed separators, invalid timestamps, overlaps, empty lyrics, and invalid UTF-8.
- Test CSRF rejection.
- Test upload extension, MIME, size, count, and filename controls.
- Test path traversal resistance.
- Test truthful batch summaries and HTTP status codes.
- Test secure response headers.
- Test output headers and filenames.
- Test no-JavaScript conversion fallback.
- Test keyboard operation and accessibility landmarks.
- Run static analysis, coding style, PHPUnit, dependency audit, and regression tests.
- Perform manual browser testing at mobile and desktop widths.
- Reconfirm the downloaded SRT imports into Adobe Premiere Pro.

### Files to create

- `tests/Unit/SafeFilenameTest.php`
- `tests/Unit/UploadValidatorTest.php`
- `tests/Unit/CsrfTokenManagerTest.php`
- `tests/Unit/TemporaryFileManagerTest.php`
- `tests/Feature/EditorPageTest.php`
- `tests/Feature/PreviewEndpointTest.php`
- `tests/Feature/WebConversionTest.php`
- `tests/Feature/WebBatchConversionTest.php`
- `tests/Feature/DownloadResponseTest.php`
- `tests/Feature/SecurityHeadersTest.php`
- `tests/Feature/CsrfProtectionTest.php`
- `tests/Fixtures/uploads/valid-ui-lyrics.txt`
- `tests/Fixtures/uploads/invalid-ui-lyrics.txt`
- `tests/Fixtures/uploads/unicode-ui-lyrics.txt`
- `docs/UI_BROWSER_TEST.md`
- `docs/UI_ACCESSIBILITY_TEST.md`
- `docs/UI_SECURITY_TEST.md`
- `docs/UI_PREMIERE_IMPORT_TEST.md`

### Files to modify

- `phpunit.xml`
- `phpstan.neon`
- `phpcs.xml`
- `composer.json`
- `.gitignore`
- `README.md`

### Completion gate

- All unit, feature, regression, and HTTP tests pass.
- PHPStan reports no errors.
- PSR-12 checks pass.
- Composer validation and security audit pass.
- Failed web conversions are never reported as successful.
- CSRF, upload, path, filename, size, and temporary-file controls pass.
- Keyboard and responsive browser checks pass.
- Downloaded SRT output matches a fixed fixture.
- The UI-generated SRT imports into Premiere Pro and creates a usable caption track.
- A verified Phase 7 commit is created and pushed.

---

## Phase 8: Documentation, Packaging, and Version 1.1.0 Release

**Duration:** 0.5 working day  
**Target:** Day 5, afternoon  
**Priority:** Final release

### Objectives

- Finalize web-interface installation and server requirements.
- Document local development and production deployment.
- Document Apache and PHP development-server startup.
- Document security-sensitive configuration.
- Add UI usage screenshots after final visual verification.
- Update the changelog and version marker.
- Build a clean release archive.
- Verify the package contains no uploads, generated SRT files, sessions, caches, logs, or other temporary files.
- Smoke-test the packaged UI and CLI.
- Create the release commit.
- Tag `v1.1.0` only after every required check passes.
- Push the release commit and annotated tag.

### Files to create

- `docs/UI_QUICK_START.md`
- `docs/UI_DEPLOYMENT_GUIDE.md`
- `docs/UI_USER_GUIDE.md`
- `docs/UI_TROUBLESHOOTING.md`
- `docs/UI_RELEASE_CHECKLIST.md`
- `docs/images/ui-editor.png`
- `docs/images/ui-validation.png`
- `docs/images/ui-preview.png`
- `docs/images/ui-batch.png`

### Files to modify

- `CHANGELOG.md`
- `VERSION`
- `README.md`
- `composer.json`
- `.gitignore`
- `.gitattributes`
- `docs/QUICK_START.md`
- `docs/PREMIERE_IMPORT_GUIDE.md`

### Completion gate

- A new user can install and open the UI from the documentation.
- Paste, upload, preview, convert, batch, and download workflows operate in the packaged release.
- CLI and web UI regression tests pass.
- The release archive contains no runtime or temporary user data.
- The packaged UI passes a clean-environment smoke test.
- Local and remote `development` commits match.
- Annotated tag `v1.1.0` points to the verified release commit.
- Version `1.1.0` is pushed only after every gate passes.

---

# 6. Proposed Version 1.1.0 File Structure

```text
txt-to-srt-converter/
├── bin/
│   ├── serve-ui
│   └── txt-to-srt
├── config/
│   ├── brand.php
│   ├── security.php
│   └── ui.php
├── docs/
│   ├── images/
│   ├── BRAND_TOKENS.md
│   ├── CLI_REFERENCE.md
│   ├── ERROR_REFERENCE.md
│   ├── INPUT_FORMAT.md
│   ├── PREMIERE_IMPORT_GUIDE.md
│   ├── PREMIERE_IMPORT_TEST.md
│   ├── QUICK_START.md
│   ├── TROUBLESHOOTING.md
│   ├── UI_ACCESSIBILITY_RULES.md
│   ├── UI_ACCESSIBILITY_TEST.md
│   ├── UI_ARCHITECTURE.md
│   ├── UI_BROWSER_TEST.md
│   ├── UI_DEPLOYMENT_GUIDE.md
│   ├── UI_PREMIERE_IMPORT_TEST.md
│   ├── UI_QUICK_START.md
│   ├── UI_RELEASE_CHECKLIST.md
│   ├── UI_REQUIREMENTS.md
│   ├── UI_SECURITY_RULES.md
│   ├── UI_SECURITY_TEST.md
│   ├── UI_STYLE_GUIDE.md
│   ├── UI_TROUBLESHOOTING.md
│   ├── UI_USER_FLOWS.md
│   └── UI_USER_GUIDE.md
├── public/
│   ├── .htaccess
│   └── index.php
├── resources/
│   ├── css/
│   ├── js/
│   └── views/
├── samples/
├── src/
│   ├── Application/
│   ├── Console/
│   ├── Controller/
│   ├── Domain/
│   ├── Exception/
│   ├── Formatter/
│   ├── Http/
│   ├── Parser/
│   ├── Repair/
│   ├── Support/
│   └── Validation/
├── templates/
├── tests/
│   ├── Feature/
│   ├── Fixtures/
│   └── Unit/
├── .editorconfig
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── composer.json
├── composer.lock
├── phpcs.xml
├── phpstan.neon
├── phpunit.xml
├── README.md
└── VERSION
```

# 7. Version 1.1.0 Definition of Done

Version `1.1.0` is complete only when:

- The existing CLI remains operational and backward compatible.
- Users can paste or upload timestamped TXT lyrics.
- Users can preview captions before conversion.
- Exact source-line errors are visible and understandable.
- Safe repair mode remains explicit and limited.
- Generated output passes the internal SRT validator.
- Users can download a Premiere-ready SRT file.
- Multiple TXT files can be converted with truthful results.
- Batch ZIP downloads contain only successful SRT outputs.
- CSRF, upload validation, path traversal prevention, safe filenames, and temporary-file cleanup are verified.
- The UI remains usable without JavaScript for the core conversion flow.
- The UI is responsive and keyboard accessible.
- Official Noviq Labs Ltd colors come from centralized configuration and CSS tokens.
- PHPUnit, PHPStan, PSR-12, Composer validation, and security audit pass.
- A UI-generated SRT imports successfully into Adobe Premiere Pro.
- Documentation covers installation, operation, deployment, troubleshooting, and security.
- The clean release package passes CLI and UI smoke tests.
- A verified release commit is pushed to `origin/development`.
- Annotated tag `v1.1.0` is created and pushed only after all checks pass.

# 8. Recommended Execution Rules

- Inspect every existing target file before modification.
- Use the existing PHP services rather than duplicating conversion logic.
- Create a verified Git commit at the end of every completed UI phase.
- Push every completed phase to `origin/development`.
- Do not develop or merge directly on `main`.
- Stop when a validation gate fails and correct the verified root cause.
- Never report fallback output as PASS after an underlying failure.
- Save every terminal command batch and complete output directly in:

```text
/home/trovas/Downloads/projects/byupw/design
```

- Use descriptive trace filenames, for example:

```text
txt-to-srt-ui-phase-1-requirements-inspection.txt
txt-to-srt-ui-phase-2-http-foundation.txt
txt-to-srt-ui-phase-3-editor-conversion.txt
txt-to-srt-ui-phase-4-preview-validation.txt
txt-to-srt-ui-phase-5-brand-responsive-ui.txt
txt-to-srt-ui-phase-6-batch-upload.txt
txt-to-srt-ui-phase-7-quality-verification.txt
txt-to-srt-ui-phase-8-release-v1.1.0.txt
```

# 9. Critical Path for Fast Delivery

To move quickly, implementation should remain focused on this order:

1. Secure PHP HTTP bootstrap.
2. Paste and single-file upload workflow.
3. Conversion and SRT download.
4. Validation errors and preview.
5. Noviq-branded responsive design.
6. Batch upload and ZIP download.
7. Automated security, accessibility, and regression gates.
8. Documentation, packaging, smoke testing, and `v1.1.0` release.

Nonessential features such as accounts, cloud storage, collaboration, automatic transcription, translations, waveform synchronization, analytics, and remote uploads should remain outside version `1.1.0` unless separately approved after the core UI release.
