# CSE 310 Module 2 Data Analysis Execution Roadmap

## Project Identity

- **Module:** Data Analysis
- **Project:** Uganda Food Price Explorer
- **Language:** Python
- **Primary library:** Pandas
- **Visualization:** Matplotlib
- **Project directory:** `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer`
- **Time log:** `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/module2_time_log.md`
- **Proposed repository:** `uganda-food-price-explorer`

## Analysis Questions

1. Which commodities and markets have the highest average reported prices, and how do the results change when the dataset is filtered to a selected date range?
2. Which commodities show the largest price increases over time, and during which months do unusual price spikes appear?

## Rubric Acceptance Criteria

The project is complete only when all of the following are true:

- The software is original and implements every Data Analysis requirement.
- Filtering, sorting, aggregation, and data conversion are demonstrated.
- Both analysis questions are answered with reproducible evidence.
- At least two accurate, readable charts are produced.
- The application contains at least 100 meaningful lines of original code.
- Every function has a useful docstring or function-level comment.
- The correct Data Analysis `README.md` is complete at the repository root.
- The code and README are published in a public GitHub repository.
- A 4–5 minute video includes the presenter’s face, software demonstration, and code walkthrough.
- The video link is posted in the Data Analysis Microsoft Teams channel.
- The Learning Strategies discussion is complete.
- The time log contains at least 20 genuine hours.
- The official Module Submission form is completed and downloaded as a Word document.

## Proposed Final Project Structure

```text
uganda-food-price-explorer/
├── .gitignore
├── README.md
├── analysis.py
├── data_loader.py
├── data_cleaning.py
├── filters.py
├── summaries.py
├── visualizations.py
├── main.py
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── uganda_food_prices_raw.csv
│   └── cleaned/
│       └── uganda_food_prices_cleaned.csv
├── output/
│   ├── raw_data_profile.txt
│   ├── summary_by_commodity.csv
│   ├── summary_by_market.csv
│   ├── price_change_summary.csv
│   ├── price_spikes.csv
│   ├── final_audit.txt
│   └── charts/
│       ├── highest_average_prices.png
│       └── price_trends.png
├── tests/
│   └── test_analysis.py
└── docs/
    ├── requirements_checklist.md
    ├── dataset_source.md
    ├── reflection.md
    └── video_outline.md
```

---

## Phase 1 - Confirm Requirements and Evidence Mapping

**Micro-objective:** Convert the rubric and module plan into a precise checklist before creating project files.

**Files to create:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/docs/requirements_checklist.md`

**Files to edit:**

- None

**Work:**

- Record every common and Data Analysis requirement.
- Map each requirement to a source file, test, output, README section, or video segment.
- Record the two final analysis questions exactly.

**Verification:**

- Every rubric item has a named evidence location.
- Both analysis questions are explicit and measurable.

**Completion gate:**

- The requirements checklist contains no unmapped requirement.

---

## Phase 2 - Create the Workspace and Begin the Time Log

**Micro-objective:** Establish an isolated repository and begin truthful time tracking before implementation.

**Files to create:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/module2_time_log.md`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/.gitignore`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/README.md`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/analysis.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/data_loader.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/data_cleaning.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/filters.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/summaries.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/visualizations.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/main.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/requirements.txt`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/tests/test_analysis.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/docs/reflection.md`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/docs/video_outline.md`

**Files to edit:**

- None

**Work:**

- Create the project, data, output, tests, and docs directories.
- Initialize Git on branch `main`.
- Add the time-log header and the first genuine entry.
- Keep generated caches, temporary files, and private data out of Git.

**Verification:**

- Print the complete initial structure.
- Confirm the Git root and current branch.
- Confirm the time log has date, category, description, start, end, and duration columns.

**Completion gate:**

- The repository is isolated and the time log has a truthful first entry.

---

## Phase 3 - Select and Verify the Dataset

**Micro-objective:** Select a public, documented dataset capable of answering both analysis questions.

**Files to create:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/data/raw/uganda_food_prices_raw.csv`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/docs/dataset_source.md`

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/docs/requirements_checklist.md`

**Work:**

- Record publisher, source link, license or reuse terms, access date, and dataset description.
- Verify that the dataset contains commodity, market, date, price, and unit fields.
- Preserve the raw file unchanged.

**Verification:**

- Print row count, column names, and a small sample.
- Confirm both analysis questions are supported by the available fields.

**Completion gate:**

- The dataset is publicly usable, documented, and analytically suitable.

---

## Phase 4 - Profile the Raw Dataset

**Micro-objective:** Understand schema and quality problems before defining cleaning rules.

**Files to create:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/output/raw_data_profile.txt`

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/data_loader.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/tests/test_analysis.py`

**Work:**

- Implement CSV loading with readable errors.
- Report row count, columns, data types, nulls, duplicates, date range, commodities, markets, and units.
- Identify mixed units and potentially invalid prices.

**Verification:**

- Run the loader against the raw dataset.
- Confirm the profile report describes observed data rather than assumptions.

**Completion gate:**

- Every cleaning rule can be justified by the profile.

---

## Phase 5 - Implement Reproducible Data Cleaning

**Micro-objective:** Create a valid analysis layer without altering the original dataset.

**Files to create:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/data/cleaned/uganda_food_prices_cleaned.csv`

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/data_cleaning.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/tests/test_analysis.py`

**Work:**

- Convert dates to datetime values.
- Convert prices to finite numeric values.
- Trim whitespace and normalize commodity, market, and unit labels.
- Remove exact duplicates.
- Remove or report rows that cannot support analysis.
- Preserve the raw source file.

**Verification:**

- Test date conversion, numeric conversion, duplicates, and invalid-row handling.
- Confirm the cleaned output contains valid dates and positive finite prices.

**Completion gate:**

- Cleaning is deterministic, documented, and covered by targeted tests.

---

## Phase 6 - Add Reusable Filters

**Micro-objective:** Allow analysis of selected dates, commodities, and markets without changing the source DataFrame.

**Files to create:**

- None

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/filters.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/tests/test_analysis.py`

**Work:**

- Implement inclusive date-range filtering.
- Implement case-insensitive commodity and market filtering.
- Reject reversed date ranges.
- Return a documented empty result when nothing matches.

**Verification:**

- Test each filter independently and in combination.
- Confirm filtering does not modify the input DataFrame.

**Completion gate:**

- All filters are reusable, parameterized, and tested.

---

## Phase 7 - Answer Question 1: Highest Average Prices

**Micro-objective:** Produce transparent grouped statistics that answer the first question.

**Files to create:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/output/summary_by_commodity.csv`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/output/summary_by_market.csv`

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/summaries.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/analysis.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/tests/test_analysis.py`

**Work:**

- Group by commodity, market, and unit where required.
- Calculate count, mean, minimum, and maximum price.
- Sort by mean price descending.
- Prevent comparisons across incompatible units.

**Verification:**

- Validate calculations and sort order with a small known DataFrame.

**Completion gate:**

- Exported tables directly answer Question 1 and retain sample-size context.

---

## Phase 8 - Answer Question 2: Price Change and Spikes

**Micro-objective:** Calculate monthly trends and identify unusual changes with an explicit rule.

**Files to create:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/output/price_change_summary.csv`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/output/price_spikes.csv`

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/summaries.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/analysis.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/tests/test_analysis.py`

**Work:**

- Convert dates to monthly periods.
- Group by commodity, market, unit, and month.
- Calculate monthly averages, absolute change, and percentage change.
- Define and document a reproducible spike rule.

**Verification:**

- Test monthly averages, percentage change, and spike boundaries using known inputs.

**Completion gate:**

- Outputs directly answer Question 2 and the spike rule is explicit.

---

## Phase 9 - Create the Charts

**Micro-objective:** Convert the statistical findings into readable and non-misleading visual evidence.

**Files to create:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/output/charts/highest_average_prices.png`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/output/charts/price_trends.png`

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/visualizations.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/analysis.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/tests/test_analysis.py`

**Work:**

- Create a sorted bar chart for highest average prices.
- Create a time-series chart for selected commodity trends.
- Include clear titles, axes, units, legends, and filter context.

**Verification:**

- Confirm both PNGs exist and are non-empty.
- Open both charts and inspect readability and accuracy.

**Completion gate:**

- Each chart answers a stated question without mixing units or hiding small samples.

---

## Phase 10 - Build the Reproducible Entry Point

**Micro-objective:** Run the complete analysis from one command in a deterministic order.

**Files to create:**

- None

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/main.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/analysis.py`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/requirements.txt`

**Work:**

- Run loading, cleaning, filtering, summaries, exports, and charts.
- Print source, row counts, active filters, findings, and output paths.
- Return nonzero status for invalid configuration or input.

**Verification:**

- Run `python3 main.py`.
- Confirm all expected outputs are regenerated.

**Completion gate:**

- A new developer can repeat the complete analysis using the README instructions.

---

## Phase 11 - Complete the Automated Test Suite

**Micro-objective:** Protect every unique Data Analysis behavior with fast, deterministic tests.

**Files to create:**

- None

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/tests/test_analysis.py`

**Work:**

- Test loading, cleaning, conversion, filters, grouping, sorting, price changes, spikes, empty results, and invalid configuration.
- Use in-memory DataFrames or temporary files.
- Avoid depending on the entire production dataset for most unit tests.

**Verification:**

- Run the targeted test file with verbose output.
- Confirm failures do not modify production data.

**Completion gate:**

- All tests pass and each unique requirement has test evidence.

---

## Phase 12 - Run the Technical and Data-Quality Audits

**Micro-objective:** Confirm that the project is correct, documented, sufficiently large, and analytically honest.

**Files to create:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/output/final_audit.txt`

**Files to edit:**

- Any application `.py` file containing a verified defect.
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/tests/test_analysis.py` if a test gap is discovered.

**Work:**

- Compile all Python files.
- Count meaningful application lines.
- Audit every function for a useful docstring.
- Check tables for nulls, mixed units, duplicates, non-finite values, and misleading sample sizes.
- Check charts for readable labels, units, and filter context.

**Verification:**

- Save all audit results in `output/final_audit.txt`.

**Completion gate:**

- Code exceeds 100 meaningful lines, all functions are documented, and no unresolved audit issue remains.

---

## Phase 13 - Complete the Data Analysis README

**Micro-objective:** Document the finished project accurately using the correct module template.

**Files to create:**

- None

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/README.md`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/docs/dataset_source.md`
- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/docs/reflection.md`

**Work:**

- Document purpose, questions, dataset, cleaning, filters, aggregation, sorting, conversion, findings, charts, limitations, environment, commands, tests, and resources.
- Include a final video-link section.
- Remove all placeholders and unfinished instructions.

**Verification:**

- Audit for placeholders.
- Compare README claims against actual source and outputs.

**Completion gate:**

- The README is complete, professional, accurate, and located at the repository root.

---

## Phase 14 - Verify Full Reproducibility

**Micro-objective:** Prove that a clean environment can regenerate the results without manual corrections.

**Files to create:**

- None

**Files to edit:**

- Any file that fails the reproducibility check.

**Work:**

- Use a clean test copy or temporary workspace.
- Install declared dependencies.
- Remove generated cleaned data, tables, and charts from the test copy.
- Run the application from the raw data.
- Compare regenerated schemas, row counts, files, and non-empty charts.

**Verification:**

- Confirm all expected outputs are regenerated successfully.

**Completion gate:**

- Reproducibility passes without manual fixes.

---

## Phase 15 - Commit and Publish the Stable Project

**Micro-objective:** Preserve and publish the tested snapshot without private or unintended files.

**Files to create:**

- None

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/.gitignore`
- Any file corrected during final review.

**Work:**

- Inspect Git status and the complete file list.
- Audit for secrets, private data, generated caches, and unintended large files.
- Commit the stable project.
- Create the empty public GitHub repository `uganda-food-price-explorer`.
- Add `origin` and push `main`.

**Verification:**

- Confirm `main` tracks `origin/main`.
- Confirm the public repository opens in an incognito browser.

**Completion gate:**

- Repository is public, synchronized, and the working tree is clean.

---

## Phase 16 - Prepare the Demonstration Video

**Micro-objective:** Create a focused 4–5 minute training-video plan covering all assessed evidence.

**Files to create:**

- None

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/docs/video_outline.md`

**Work:**

- Plan the introduction, application run, both questions, both charts, code walkthrough, README, tests, and GitHub conclusion.
- Include filtering, sorting, aggregation, conversion, findings, and limitations.
- Keep the presenter’s face visible.

**Verification:**

- Complete a timed rehearsal.
- Confirm the outline fits 4–5 minutes.

**Completion gate:**

- Every rubric item has a specific video segment.

---

## Phase 17 - Record, Publish, and Test the Video

**Micro-objective:** Publish an instructor-accessible demonstration with complete technical evidence.

**Files to create:**

- None

**Files to edit:**

- `/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/uganda-food-price-explorer/README.md`

**Work:**

- Record with webcam and clear microphone audio.
- Show the running analysis, outputs, charts, tests, and code.
- Upload as Public or Unlisted.
- Test the link in an incognito browser.
- Post the link in the Data Analysis Microsoft Teams channel.
- Add the final video link to the README.

**Verification:**

- Confirm the video opens without account-specific permission.
- Confirm face, software demo, and detailed code walkthrough are present.

**Completion gate:**

- Video is accessible, posted in Teams, and documented in the README.

---

## Phase 18 - Complete the Official Module Submission

**Micro-objective:** Produce the final Word document required for Canvas.

**Files to create:**

- None locally until the official form generates the final document.

**Files to edit:**

- The Word document downloaded from the official Module Submission form, only if a verified correction is required.

**Work:**

- Select Data Analysis and Module 2.
- Enter the student name, public GitHub link, and final video link.
- Answer all module-specific and general checklist items truthfully.
- Provide the verified total hours and complete daily time log.
- Write the Learning Strategies reflection.
- Download the generated Word document.

**Verification:**

- Audit the document for placeholders, broken links, missing rows, and unsupported claims.

**Completion gate:**

- The final DOCX or PDF contains GitHub, video, time log, reflection, and completed checklists and is ready for Canvas.

---

## Final Pre-Submission Gate

The project is ready for Canvas only when every item below is true:

- [ ] Project is original and reproducible.
- [ ] Both analysis questions are answered.
- [ ] Filtering, sorting, aggregation, and data conversion are demonstrated.
- [ ] At least two accurate charts are present.
- [ ] All tests pass.
- [ ] Code exceeds 100 meaningful lines.
- [ ] Every function has a useful docstring.
- [ ] README uses the correct template and contains no placeholders.
- [ ] GitHub repository is public and synchronized.
- [ ] Video is 4–5 minutes with face, demo, and code walkthrough.
- [ ] Video link is posted in the Data Analysis Teams channel.
- [ ] Learning Strategies discussion is complete.
- [ ] Time log contains at least 20 genuine hours.
- [ ] Official Module Submission Word document is complete.
