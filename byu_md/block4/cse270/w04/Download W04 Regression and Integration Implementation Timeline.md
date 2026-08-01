# W04 Regression and Integration Testing Implementation Timeline

**Student:** Edwin Kambale  
**Course:** CSE 270  
**Activity:** W04 Regression and Integration Tests  
**Target:** Complete evidence for all **110 rubric points**

---

## Rubric Breakdown

- Common regression: **13 points**
- Home regression: **13 points**
- Join regression: **13 points**
- Directory regression: **13 points**
- Weather API integration: **13 points**
- Directory Data integration: **13 points**
- Correct six-test Integration and Regression plan: **22 points**
- Test-case list included: **10 points**
- **Total: 110 points**

---

## Implementation Timeline

1. Correct and capture both integration screenshots.
2. Create the `Integration Tests` folder in Squash.
3. Create the `Weather API` test case.
4. Create the `Directory Data` test case.
5. Create the six-test campaign.
6. Create the `Kambale-W4R` iteration.
7. Execute the Weather API integration test.
8. Execute the Directory Data integration test.
9. Execute the four selected regression tests.
10. Update the defect tracker.
11. Generate the two Squash execution PDFs.
12. Audit and submit the five required files.

---

# Phase 1: Finalize the Integration Screenshots

## Phase 1A: Weather API Screenshot

### Confirm the Postman request

Use:

```text
Method: GET
Endpoint: https://api.openweathermap.org/data/2.5/weather
lat: 43.8866
lon: -111.6777
appid: stored securely as {{appid}}
units: imperial
```

### Capture complete evidence

1. Send the request in Postman.
2. Confirm the response status is `200 OK`.
3. Open the lower response panel.
4. Select `Body`.
5. Select `Pretty`.
6. Select `JSON` if prompted.
7. Expand the response panel until the JSON is readable.
8. Confirm the response visibly includes:

```text
weather
main.temp
wind.speed
```

9. Keep `200 OK` visible.
10. Keep the real API key concealed.
11. Save the screenshot as:

```text
Kambale-weather-integration.png
```

### Weather screenshot checklist

- [ ] GET method is visible.
- [ ] OpenWeather endpoint is visible.
- [ ] Latitude is visible.
- [ ] Longitude is visible.
- [ ] `units=imperial` is visible.
- [ ] API key is concealed.
- [ ] `200 OK` is visible.
- [ ] JSON response body is visible.
- [ ] Weather description is visible.
- [ ] `main.temp` is visible.
- [ ] `wind.speed` is visible.

## Phase 1B: Directory Data Screenshot

### Keep both local servers running

#### Terminal 1: Django Directory Data Service

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w04/W04 Activity/cse270-v12/cse270/directorydata_service"
.venv/bin/python manage.py runserver
```

Expected service endpoint:

```text
http://127.0.0.1:8000/data/all
```

#### Terminal 2: Local version 1.2 website

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w04/W04 Activity/cse270-v12/cse270/teton/1.2"
python3 -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500/directory.html
```

### Capture complete Directory evidence

1. Open Chrome Developer Tools with `Ctrl + Shift + I`.
2. Select `Network`.
3. Remove any existing filter such as `submit`.
4. Enter this filter:

```text
all
```

5. Confirm Network recording is enabled.
6. Reload the page with `Ctrl + R`.
7. Select the request named `all`.
8. Open `Headers` and verify:

```text
Request URL: http://127.0.0.1:8000/data/all
Request Method: GET
Status Code: 200 OK
```

9. Open `Response`.
10. Confirm the JSON contains a `businesses` collection.
11. Confirm business fields such as:

```text
name
streetAddress
cityStateZip
websiteURL
imageURL
membershipLevel
adcopy
```

12. Resize Developer Tools so that the Directory page and API response are both visible.
13. Save the screenshot as:

```text
Kambale-directory-integration.png
```

### Directory screenshot checklist

- [ ] Local Directory page is visible.
- [ ] Network tab is selected.
- [ ] Filter says `all`.
- [ ] Request named `all` is selected.
- [ ] Request URL points to `127.0.0.1:8000/data/all`.
- [ ] `200 OK` is visible.
- [ ] Response tab is selected.
- [ ] JSON business records are visible.

---

# Phase 2: Create the Integration Tests Folder

1. Open Squash.
2. Click `Test cases`.
3. Select the project root:

```text
Teton CoC
```

4. Click `+`.
5. Select `Add a folder`.
6. Enter:

```text
Name:
Integration Tests
```

7. Enter this description:

```text
Contains manual integration tests for the OpenWeather API and Directory Data Service used by the local version 1.2 Teton Chamber of Commerce website.
```

8. Click `Add`.

Expected tree:

```text
Teton CoC
├── Common
├── Directory
├── Home
├── Integration Tests
└── Join
```

---

# Phase 3: Create the Weather API Test Case

Select `Integration Tests`, then choose:

```text
+ → Add a test case
```

## Test-case fields

```text
Format:
Classic
```

```text
Name:
Weather API
```

```text
Reference:
Leave blank
```

```text
Description:
Verify that the local Teton Chamber of Commerce version 1.2 website correctly retrieves and displays current weather data from the OpenWeather API.
```

Click `Add`.

## Prerequisite

Open `Prerequisites and test steps`. Expand the `PREREQUISITES` section above the Action and Expected Result columns.

Enter:

```text
The local version 1.2 website is running, the OpenWeather API key is active, the website is configured to use WEATHER_URL_PROD, and Postman is available.
```

## Test steps

### Step 1

**Action**

```text
Send a GET request in Postman to the OpenWeather current-weather endpoint using the configured latitude, longitude, API key, and units=imperial.
```

**Expected Result**

```text
OpenWeather returns HTTP 200 OK and a valid JSON weather response.
```

### Step 2

**Action**

```text
Inspect the OpenWeather JSON response in Postman.
```

**Expected Result**

```text
The response contains a weather description, temperature in main.temp, and wind speed in wind.speed.
```

### Step 3

**Action**

```text
Open the local version 1.2 Home page and inspect the Weather section.
```

**Expected Result**

```text
The Weather section displays a weather icon, description, Fahrenheit temperature, and wind speed in MPH.
```

### Step 4

**Action**

```text
Compare the weather description, rounded temperature, and rounded wind speed returned by OpenWeather with the values displayed on the Home page.
```

**Expected Result**

```text
The weather description, rounded Fahrenheit temperature, and rounded MPH wind speed displayed on the Home page match the OpenWeather response.
```

Do not link this integration test to a requirement.

---

# Phase 4: Create the Directory Data Test Case

Select `Integration Tests`, then choose:

```text
+ → Add a test case
```

## Test-case fields

```text
Format:
Classic
```

```text
Name:
Directory Data
```

```text
Reference:
Leave blank
```

```text
Description:
Verify that the local Teton Chamber of Commerce version 1.2 Directory page correctly retrieves and displays member data from the Django Directory Data Service.
```

Click `Add`.

## Prerequisite

```text
The local version 1.2 website and Django Directory Data Service are running, the website is configured to use DIRECTORY_DATA_URL_TEST, and Chrome Developer Tools is available.
```

## Test steps

### Step 1

**Action**

```text
Open the local Directory page, open Chrome Developer Tools, select Network, and reload the page.
```

**Expected Result**

```text
A GET request named all is sent to http://127.0.0.1:8000/data/all.
```

### Step 2

**Action**

```text
Select the all request and inspect its Headers.
```

**Expected Result**

```text
The Directory Data Service returns HTTP 200 OK.
```

### Step 3

**Action**

```text
Open the Response tab for the all request.
```

**Expected Result**

```text
The response contains a valid JSON businesses collection.
```

### Step 4

**Action**

```text
Compare the number of businesses returned by the service with the number displayed on the Directory page.
```

**Expected Result**

```text
The API response and Directory page display the same number of businesses.
```

### Step 5

**Action**

```text
Compare the business names, addresses, website URLs, images, and descriptions returned by the service with the Directory page.
```

**Expected Result**

```text
The content displayed on the Directory page matches the business data returned by the Directory Data Service.
```

Do not link this integration test to a requirement.

---

# Phase 5: Create the Six-Test Campaign

1. Click `Executions`.
2. Select:

```text
Teton CoC
```

3. Click:

```text
+ → Add a campaign
```

## Campaign fields

```text
Name:
Integration and Regression Test Plan
```

```text
Reference:
Leave blank
```

```text
Description:
Limited regression and integration test plan for local version 1.2 of the Teton Chamber of Commerce website.
```

4. Click `Add`.
5. Open the campaign's `Execution plan`.
6. Add exactly these six test cases:

```text
Weather API
Directory Data
1.2.1 Navigation Links Visible (Desktop)
2.6.1 Current Weather Visible
3.2.1 First Name Required
4.1.2 Business List Website Opens
```

7. Confirm the final count is:

```text
6 test cases
```

Do not add any other test cases.

---

# Phase 6: Create the Iteration

1. Select:

```text
Integration and Regression Test Plan
```

2. Click:

```text
+ → Add an iteration
```

3. Enter:

```text
Name:
Kambale-W4R
```

```text
Reference:
Leave blank
```

```text
Description:
Execution of the Integration and Regression Test Plan against the local version 1.2 Teton Chamber of Commerce environment.
```

4. Keep checked:

```text
Copy the campaign execution plan
```

5. Click `Add`.
6. Open the new iteration's `Execution plan`.
7. Confirm it contains exactly six tests.

---

# Phases 7-9: Execute All Six Tests

Execute against the local environment:

```text
http://127.0.0.1:5500/
```

Run in this order:

```text
1. Weather API
2. Directory Data
3. 1.2.1 Navigation Links Visible (Desktop)
4. 2.6.1 Current Weather Visible
5. 3.2.1 First Name Required
6. 4.1.2 Business List Website Opens
```

## Execution rhythm

For every Squash step:

1. Read the Action.
2. Read the Expected Result.
3. Switch to Postman, Chrome Developer Tools, or the local website.
4. Perform the Action exactly.
5. Observe the actual result.
6. Return to Squash.
7. Record Passed, Failed, or Blocked.
8. Add a failure comment when applicable.
9. Update the defect tracker when applicable.

## Status rules

```text
Passed:
Every step can be performed and every expected result occurs.
```

```text
Failed:
The validation point is reached, but at least one expected result differs.
```

```text
Blocked:
A missing dependency or unrelated error prevents the validation point from being reached.
```

One failed step makes the complete test case fail.

## Failure comment template

```text
Expected:
[Expected result]

Actual:
[Observed result]

Reproduction:
[Exact actions performed]

Environment:
Local version 1.2, Google Chrome/Postman, Django service on 127.0.0.1:8000, website on 127.0.0.1:5500.
```

---

# Phase 10: Update the Defect Tracker

Use the defect-tracking workbook from the previous W04 activity.

## If the defect is new

Use the next available Defect ID and complete:

```text
Detected Date
Status: 1-New
User Impact
Business Impact
Subject
Reported By: Edwin Kambale
Defect / Issue Description
Environment
```

## If the same defect already exists

Do not create an unnecessary duplicate. Update the existing defect's detected date to the current regression-test date when required.

## Preserve

- Workbook structure
- Formulas
- Dropdowns
- Formatting
- Existing defects

Save the updated workbook as:

```text
Kambale-cs270-defect-tracker-regression.xlsx
```

---

# Phase 11: Generate the Two Squash Reports

1. Open `Reporting` in Squash.
2. Select `Teton CoC`.
3. Click:

```text
+ → Add a report
```

4. Choose:

```text
Execution Progress Report
```

5. Enter:

```text
Name:
Integration and Regression
```

6. Set:

```text
Report perimeter:
Select campaigns
```

7. Select only:

```text
Integration and Regression Test Plan
```

8. Confirm the selection.
9. Save the report.
10. Run the report.

## Download report 1

```text
Campaign monitoring dashboard
```

Save as:

```text
Kambale-integration-regression-dashboard.pdf
```

## Download report 2

```text
Test case list by campaign
```

Save as:

```text
Kambale-integration-regression-tests.pdf
```

Both reports must show only the six-test campaign and 100% execution progress.

---

# Phase 12: Final Submission Package

Submit exactly these five artifacts:

```text
1. Kambale-cs270-defect-tracker-regression.xlsx
2. Kambale-integration-regression-dashboard.pdf
3. Kambale-integration-regression-tests.pdf
4. Kambale-weather-integration.png
5. Kambale-directory-integration.png
```

---

# Final 110-Point Rubric Audit

## Regression execution

- [ ] Common regression test was executed.
- [ ] Home regression test was executed.
- [ ] Join regression test was executed.
- [ ] Directory regression test was executed.
- [ ] Any failed regression tests have complete defect records.

## Integration execution

- [ ] Weather API integration test was executed.
- [ ] Weather screenshot shows request URL and response body.
- [ ] Weather screenshot shows `200 OK`.
- [ ] Weather screenshot conceals the API key.
- [ ] Directory Data integration test was executed.
- [ ] Directory screenshot shows the `all` request.
- [ ] Directory screenshot shows the API response.
- [ ] Directory screenshot shows enough page context to prove comparison.
- [ ] Any failed integration tests have complete defect records.

## Test plan

- [ ] `Integration Tests` folder exists.
- [ ] `Weather API` test case exists.
- [ ] `Directory Data` test case exists.
- [ ] `Integration and Regression Test Plan` campaign exists.
- [ ] Campaign contains exactly six test cases.
- [ ] Campaign includes Weather API.
- [ ] Campaign includes Directory Data.
- [ ] Campaign includes Common `1.2.1`.
- [ ] Campaign includes Home `2.6.1`.
- [ ] Campaign includes Join `3.2.1`.
- [ ] Campaign includes Directory `4.1.2`.
- [ ] `Kambale-W4R` iteration exists.
- [ ] Iteration contains exactly six tests.
- [ ] All six tests have final statuses.

## Reports and submission

- [ ] Execution Progress report selects only the new campaign.
- [ ] Dashboard PDF shows the selected campaign.
- [ ] Dashboard shows 100% execution.
- [ ] Test-case-list PDF contains all six tests.
- [ ] Updated defect tracker is saved as XLSX.
- [ ] Exactly five required artifacts are attached in Canvas.

---

# Current Readiness Snapshot

```text
Local environment: COMPLETE
Weather connection: WORKING
Directory page: WORKING
Weather screenshot: RESPONSE BODY MUST BE VISIBLE
Directory screenshot: ALL REQUEST AND RESPONSE MUST BE VISIBLE
Squash integration tests: NEXT
Six-test campaign: PENDING
Kambale-W4R iteration: PENDING
Final reports: PENDING
Final submission: PENDING
```

---

# Immediate Next Action

1. Correct the Weather screenshot so the JSON response body is visible.
2. Correct the Directory screenshot so the selected `all` request and response are visible.
3. Create the `Integration Tests` folder in Squash.
4. Create the `Weather API` and `Directory Data` test cases.
5. Stop for verification before creating the campaign.
