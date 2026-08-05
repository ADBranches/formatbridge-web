# Uganda Food Price Explorer Web App - Module 3 Execution Roadmap

> **Module:** Web Apps  
> **Framework:** Django with Python  
> **Approach:** Extend the completed Uganda Food Price Explorer analysis into an interactive web application.  
> **Planning method:** Backward design from the rubric and final submission evidence.

## Project Objective

Create a Django web application that allows users to explore Uganda food-price data through dynamically generated pages and user-controlled filters. The web app will reuse verified analysis logic from the completed Data Analysis project while adding web routes, forms, templates, navigation, error handling, and browser-based results.

## Required Web App Evidence

- At least two HTML pages populated dynamically by Django code.
- User input affects application output.
- The application runs locally with the Django development server.
- One additional requirement is completed. This plan uses a third dynamically generated page.
- At least 100 meaningful lines of student-written code.
- Useful documentation for every student-written function.
- The official Web Apps README template is completed at the repository root.
- A public GitHub repository contains the tested project.
- A four-to-five-minute video shows the presenter, running application, and detailed code walkthrough.
- The final video link is posted in the Module-web apps Microsoft Teams channel.
- The official Module Submission document is generated and uploaded to Canvas.

---

# Phase 1 - Complete the Official Module 3 Plan

## Objective

Define the Web Apps project, map every requirement to planned work, schedule at least 20 genuine hours, and identify realistic risks before implementation.

## Files to create

- None.

## Files to edit

- Official course-provided `cse310_module_plan.docx` copy for Module 3.

## Work

- Enter the student name, actual planning date, and Module 3.
- Mark `X` beside Web Apps and leave all other modules unselected.
- Describe the Uganda Food Price Explorer Web App.
- Explain how Django, Python, Pandas, HTML, and CSS will be used.
- Plan three dynamic pages: Home, Explorer, and Results.
- Complete the two-week schedule with at least 10 planned hours per week.
- Include at least two project risks and practical mitigation plans.

## Verification

- Official template remains unchanged in structure.
- Every schedule cell contains a specific task and duration.
- Planned total equals at least 20 hours.
- Web Apps is the only selected module.

## Completion gate

- The completed official Module 3 plan is uploaded to Canvas.

---

# Phase 2 - Inspect and Prepare the Existing Analysis Project

## Objective

Understand the current project structure and identify reusable analysis functions before adding Django.

## Files to create

- None initially.

## Files to inspect

- `analysis.py`
- `data_loader.py`
- `data_cleaning.py`
- `filters.py`
- `summaries.py`
- `visualizations.py`
- `main.py`
- `tests/test_analysis.py`
- `requirements.txt`
- `README.md`

## Work

- Confirm the existing analysis tests pass.
- Identify functions that can be called safely from Django views.
- Confirm the raw and cleaned data paths.
- Identify current chart-generation behavior.
- Decide whether the Web App will extend the existing repository or use a new Web Apps repository.
- Preserve the completed Data Analysis history and deliverables.

## Verification

- All existing tests pass before Django changes begin.
- The raw dataset checksum passes.
- Reusable functions and required web inputs are documented in planning notes.

## Completion gate

- The existing analysis foundation is understood and verified without modification based on assumptions.

---

# Phase 3 - Create the Django Project Foundation

## Objective

Create a minimal Django project that starts successfully and has a dedicated application for the food-price explorer.

## Files to create

- `manage.py`
- `web_project/__init__.py`
- `web_project/settings.py`
- `web_project/urls.py`
- `web_project/asgi.py`
- `web_project/wsgi.py`
- `explorer/__init__.py`
- `explorer/apps.py`
- `explorer/urls.py`
- `explorer/views.py`
- `explorer/tests.py`
- `explorer/templates/explorer/base.html`
- `explorer/static/explorer/css/styles.css`

## Files to edit

- `requirements.txt`
- `.gitignore`

## Work

- Add Django to the declared dependencies.
- Create the Django project and `explorer` application.
- Register the application in Django settings.
- Configure template and static-file handling.
- Add project-level and application-level URL routing.
- Add a simple health-check or home view.
- Keep secrets and machine-specific settings out of version control.

## Verification

- `python manage.py check` passes.
- `python manage.py runserver` starts successfully.
- The browser loads the local home route without an error.

## Completion gate

- A clean Django foundation runs locally and is committed.

---

# Phase 4 - Build the Shared Layout and Navigation

## Objective

Create a consistent visual structure that connects all required pages.

## Files to create

- `explorer/templates/explorer/base.html`
- `explorer/templates/explorer/home.html`
- `explorer/static/explorer/css/styles.css`

## Files to edit

- `explorer/views.py`
- `explorer/urls.py`

## Work

- Build a shared base template.
- Add navigation links for Home, Explorer, and Results.
- Add a page title, main content region, and footer.
- Use semantic HTML and readable responsive styling.
- Ensure every page extends the shared template.

## Verification

- Navigation links resolve correctly.
- Templates render without duplicate HTML structure.
- Layout remains readable on narrow and wide browser windows.

## Completion gate

- The shared layout supports all three planned dynamic pages.

---

# Phase 5 - Implement the Dynamic Home Page

## Objective

Show a dynamically generated project and dataset overview on the first page.

## Files to create

- `explorer/templates/explorer/home.html`

## Files to edit

- `explorer/views.py`
- `explorer/urls.py`

## Work

- Load verified dataset summary information through Python code.
- Display counts for records, commodities, markets, units, and date range.
- Explain the application purpose.
- Add a clear link to the Explorer page.
- Handle missing or unreadable data with a user-friendly message.

## Verification

- The home route returns HTTP 200.
- Dataset values are supplied by the view rather than hard-coded into the template.
- Missing-data behavior is tested.

## Completion gate

- Page 1 is dynamically populated and supports navigation.

---

# Phase 6 - Build the Explorer Form Page

## Objective

Allow users to select filters that control the analysis results.

## Files to create

- `explorer/forms.py`
- `explorer/templates/explorer/explorer.html`

## Files to edit

- `explorer/views.py`
- `explorer/urls.py`

## Work

- Create form fields for commodity, market, unit, start date, end date, and spike threshold.
- Populate choices from verified dataset values where appropriate.
- Validate date ranges and numeric thresholds.
- Preserve user selections after submission.
- Submit the form to the Results route.
- Add accessible labels and readable validation messages.

## Verification

- Explorer route returns HTTP 200.
- Valid form input is accepted.
- Reversed dates and invalid thresholds are rejected clearly.
- Form choices come from actual data where required.

## Completion gate

- Page 2 accepts meaningful user input and forwards validated values.

---

# Phase 7 - Implement the Dynamic Results Page

## Objective

Use validated user input to run the analysis and display dynamically generated results.

## Files to create

- `explorer/templates/explorer/results.html`

## Files to edit

- `explorer/views.py`
- `explorer/urls.py`
- Existing analysis modules only if a verified integration issue requires a focused correction.

## Work

- Pass validated filters into the existing analysis functions.
- Display active filters and matching-record count.
- Display mean, minimum, maximum, and record count.
- Display sorted commodity or market summaries.
- Display monthly changes and detected spikes.
- Show a clear empty-results state.
- Prevent large unbounded tables from overwhelming the page.

## Verification

- Results route returns HTTP 200 for valid submissions.
- Different inputs produce different results.
- Empty results display a readable explanation.
- Measurement units remain separated.
- Numerical claims match the underlying analysis outputs.

## Completion gate

- Page 3 is dynamically generated from user input and analysis code.

---

# Phase 8 - Integrate Charts into the Web Experience

## Objective

Present analysis results visually without mixing incompatible measurement units.

## Files to create

- `explorer/static/explorer/generated/` only if file-based charts are used.

## Files to edit

- `explorer/views.py`
- `explorer/templates/explorer/results.html`
- `visualizations.py` only if web-safe chart generation requires a verified change.
- `.gitignore` if generated web charts should remain untracked.

## Work

- Generate or select charts based on active filters.
- Ensure each chart uses one measurement unit.
- Add titles, labels, legends, and sample-size context.
- Prevent filename collisions between requests.
- Decide whether charts are generated per request or served from verified outputs.

## Verification

- Chart images are non-empty and load in the browser.
- Chart labels match the submitted filters.
- Invalid filters do not create misleading charts.
- Temporary chart files do not pollute the repository.

## Completion gate

- The Results page presents readable visual evidence tied to user input.

---

# Phase 9 - Add Web Application Tests

## Objective

Prove that routes, forms, templates, and analysis integration behave correctly.

## Files to create

- `explorer/tests/test_views.py`
- `explorer/tests/test_forms.py`
- `explorer/tests/test_integration.py`
- `explorer/tests/__init__.py`

## Files to edit

- Existing tests only when verified shared behavior requires adjustment.

## Work

- Test the Home, Explorer, and Results routes.
- Test navigation links.
- Test valid and invalid form submissions.
- Test reversed date ranges.
- Test empty results.
- Test that filters reach the analysis layer.
- Test dynamic context values.
- Retain and rerun the original 36 analysis tests.

## Verification

- All Django tests pass.
- All original analysis tests pass.
- Tests use temporary outputs and do not modify production data.

## Completion gate

- Both the analysis layer and web layer have deterministic passing tests.

---

# Phase 10 - Improve Accessibility, Validation, and Error Handling

## Objective

Make the web application usable, readable, and resilient during demonstration and grading.

## Files to edit

- `explorer/forms.py`
- `explorer/views.py`
- `explorer/templates/explorer/base.html`
- `explorer/templates/explorer/home.html`
- `explorer/templates/explorer/explorer.html`
- `explorer/templates/explorer/results.html`
- `explorer/static/explorer/css/styles.css`

## Work

- Add visible form labels and validation summaries.
- Use semantic headings and landmarks.
- Add meaningful alternative text for charts.
- Ensure keyboard-accessible navigation.
- Display readable messages for missing files, invalid data, and empty filters.
- Avoid exposing stack traces or private system paths.

## Verification

- Pages remain usable with keyboard navigation.
- Errors are readable and do not expose private details.
- Heading order and form labels are consistent.

## Completion gate

- The application handles expected user and data errors professionally.

---

# Phase 11 - Complete the Official Web Apps README

## Objective

Document the finished web application using the exact course-provided Web Apps template.

## Files to edit

- `README.md`

## Required top-level headings

```markdown
# Overview
# Web Pages
# Development Environment
# Useful Websites
# Future Work
```

## Work

- Explain the web application and learning purpose.
- Explain how to create the environment and install dependencies.
- Explain how to run the Django test server.
- State the exact local URL for the first page.
- Describe each page, route, navigation path, user input, and dynamic content.
- Add the final four-to-five-minute video link.
- List only resources genuinely used.
- Include at least three specific future improvements.
- Remove every template placeholder.

## Verification

- Exact official headings are present.
- README is at the repository root.
- Commands work in a clean environment.
- No assignment-focused language appears in the Overview.
- No placeholders remain.

## Completion gate

- README is complete, accurate, professional, and source-faithful.

---

# Phase 12 - Perform Full Reproducibility Verification

## Objective

Prove that a clean clone can install, test, and run the web application without manual source corrections.

## Files to edit

- Any file that fails the reproducibility check.

## Work

- Clone the public repository into a temporary directory.
- Create an isolated virtual environment.
- Install only declared dependencies.
- Run Django checks and migrations if required.
- Run all web and analysis tests.
- Start the development server.
- Verify all three pages in a browser.
- Submit at least one filter and confirm dynamic results.

## Verification

- Clean installation succeeds.
- All tests pass.
- Server starts without manual fixes.
- Home, Explorer, and Results pages work.
- Temporary clone is removed after verification.

## Completion gate

- Fresh-clone reproducibility passes.

---

# Phase 13 - Audit and Publish the Stable Repository

## Objective

Publish only intended, tested files without credentials, caches, private data, or internal planning artifacts.

## Files to edit

- `.gitignore`
- Any file corrected during the final review.

## Work

- Inspect complete tracked-file list.
- Remove caches, local environments, generated temporary charts, and editor files.
- Scan for secrets and machine-specific paths.
- Check tracked file sizes.
- Confirm README and source code are at the expected locations.
- Commit the tested snapshot.
- Push `main` to the public GitHub repository.

## Verification

- Public repository opens anonymously.
- Local `main` matches `origin/main`.
- Working tree is clean.
- No private credentials are tracked.

## Completion gate

- Repository is public, synchronized, tested, and clean.

---

# Phase 14 - Prepare, Record, and Publish the Demonstration Video

## Objective

Produce a focused four-to-five-minute training video covering all assessed Web Apps evidence.

## Files to edit

- `README.md` to add the final video URL.

## Required video segments

- Introduction and software purpose.
- Start the Django development server.
- Open and navigate all dynamic pages.
- Submit user input and show changed results.
- Show chart output and error handling.
- Walk through URLs, views, forms, templates, static files, and analysis integration.
- Show automated tests.
- Show the public GitHub repository and official README.

## Verification

- Duration is between 4:00 and 5:00.
- Presenter is visible.
- Audio is clear.
- Software demonstration and detailed code walkthrough are present.
- Video opens in an incognito browser.

## Completion gate

- Video is public or unlisted, accessible, and documented in the README.

---

# Phase 15 - Post the Video in Microsoft Teams

## Objective

Provide the required peer-accessible video link in the correct module channel.

## Files to create or edit

- None.

## Work

- Post in the `Module-web apps` Microsoft Teams channel.
- Include the project name, short purpose, video URL, and public repository URL.
- Refresh the channel and open the posted link.
- Retain a screenshot as private evidence.

## Verification

- Post appears in the correct channel.
- Final video link opens successfully.
- Repository link opens successfully.

## Completion gate

- The final video is posted in the correct Web Apps channel.

---

# Phase 16 - Generate and Audit the Official Submission Document

## Objective

Create the official Word document required for Canvas and verify every claim.

## Files to create

- Official Word document generated by the Module Submission form.

## Work

- Select Web Apps and Module 3.
- Enter the student name, public GitHub link, and final video link.
- Answer all module-specific and general checklist items truthfully.
- Enter the verified total hours and complete daily time log.
- Write the Learning Strategies reflection in the student own words.
- Download the generated Word document.

## Verification

- Web Apps requirements table is present.
- GitHub and video links are correct.
- General checklist is complete.
- Time total matches the daily log.
- Reflection answers what worked, what failed, and how the next module will improve.
- No placeholders, broken links, missing rows, or unsupported claims remain.

## Completion gate

- The final DOCX is complete and ready for Canvas.

---

# Phase 17 - Submit to Canvas and Preserve Evidence

## Objective

Complete the official Module 3 submission and retain proof of successful delivery.

## Files to submit

- The Word document generated by the official Module Submission form.

## Work

- Open the Module 3 submission assignment in Canvas.
- Upload the generated Word document.
- Submit the assignment.
- Confirm the uploaded filename and timestamp.
- Retain the Canvas confirmation screenshot.

## Verification

- Canvas shows a successful submission.
- The submitted file opens correctly.

## Completion gate

- Module 3 Web Apps submission is complete.

---

# Final Rubric Gate

```text
[ ] Official Module 3 plan submitted
[ ] At least 20 genuine hours recorded
[ ] Django development server runs
[ ] At least three dynamic pages implemented
[ ] User input changes application output
[ ] More than 100 meaningful lines of code
[ ] Every student-written function documented
[ ] Original analysis tests still pass
[ ] Web application tests pass
[ ] Official Web Apps README completed
[ ] Public GitHub repository verified
[ ] Four-to-five-minute presenter video published
[ ] Video posted in Module-web apps
[ ] Official submission DOCX generated and audited
[ ] Canvas submission confirmed
```

# Planned Page Map

```text
/           Home page with dynamic dataset overview
/explorer/  Filter form populated from dataset values
/results/   Dynamic summaries, changes, spikes, and charts
```

# Planned Technology Stack

```text
Python
Django
Pandas
Matplotlib
HTML
CSS
Django test client
unittest
Git and GitHub
```

# Implementation Principle

> Inspect the current project before every modification. Make only evidence-based changes, test the smallest affected area first, and move to the next phase only after the current completion gate passes.
