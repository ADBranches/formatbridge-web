# W05 Conducting a Load Test: Implementation and Submission Timeline

**Student:** Edwin Kambale  
**Course:** CSE 270  
**Activity:** W05 Conducting a Load Test  
**Target:** Full coverage of the 50-point rubric

## Confirmed Local Project Location

The archive has already been extracted successfully. All instructions in this timeline use the confirmed path below and do not use the nonexistent `W05 Activity` directory.

```text
W05 root:
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05

Downloaded archive:
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13.zip

Extracted project root:
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270

Django service directory:
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/directorydata_service

Version 1.3 website directory:
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/teton/1.3
```

## Final Submission Files

A new evidence directory will be created:

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission
```

The final directory must contain exactly these four screenshots:

```text
home-load-test.png
home-stress-test.png
directory-load-test.png
directory-stress-test.png
```

JPG is acceptable if the screenshot utility saves JPG files. Use one format consistently.

Canvas also requires a comment stating the measured average response time and the Pass or Fail result for all four tests.

---

# Phase 1: Verify the Extracted Project

## Objective

Confirm that the extracted version 1.3 project contains the backend service, Home page, Directory page, and configuration file before making changes.

## Directory used

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270
```

## Files inspected

```text
directorydata_service/manage.py
teton/1.3/index.html
teton/1.3/directory.html
teton/1.3/config/config.js
```

## Command

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270" && pwd && ls -l "directorydata_service/manage.py" "teton/1.3/index.html" "teton/1.3/directory.html" "teton/1.3/config/config.js"
```

## Completion criteria

- [ ] `manage.py` exists.
- [ ] `index.html` exists.
- [ ] `directory.html` exists.
- [ ] `config/config.js` exists.

---

# Phase 2: Prepare the Django Virtual Environment

## Objective

Create an isolated Python environment inside the Django project and install the Django version needed to start the local Directory Data Service.

## Directory used

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/directorydata_service
```

## Directory created

```text
.venv/
```

## Files created by the virtual environment

```text
.venv/bin/python
.venv/bin/pip
```

## Step 2.1: Inspect before creating

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/directorydata_service" && pwd && ls -la && find . -maxdepth 2 -type f -path "*/bin/python" -print
```

## Step 2.2: Create `.venv` only if it does not exist

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/directorydata_service" && python3 -m venv .venv
```

## Step 2.3: Install Django

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/directorydata_service" && .venv/bin/python -m pip install --default-timeout 600 --retries 10 "Django==4.2.1"
```

## Step 2.4: Validate the environment

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/directorydata_service" && .venv/bin/python -m django --version && .venv/bin/python manage.py check
```

## Expected result

```text
4.2.1
System check identified no issues
```

## Completion criteria

- [ ] `.venv/bin/python` exists.
- [ ] Django reports version `4.2.1`.
- [ ] `manage.py check` reports no issues.

---

# Phase 3: Inspect and Configure `config.js`

## Objective

Configure version 1.3 to use the local Weather stub and the local Django Directory test endpoint required for this performance activity.

## Directory used

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/teton/1.3
```

## File inspected and edited

```text
config/config.js
```

## Backup file created

```text
config/config.js.backup
```

## Required final values

```javascript
const apiURL = WEATHER_URL_STUB;
const businessDataUrl = DIRECTORY_DATA_URL_TEST;
```

## Step 3.1: Inspect the current file

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/teton/1.3" && sed -n '1,200p' config/config.js
```

Do not edit until the current content has been inspected.

## Step 3.2: Create one backup

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/teton/1.3" && cp config/config.js config/config.js.backup
```

## Step 3.3: Set Weather to the stub

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/teton/1.3" && sed -i 's/const apiURL = WEATHER_URL_PROD;/const apiURL = WEATHER_URL_STUB;/' config/config.js
```

## Step 3.4: Set Directory data to the test service

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/teton/1.3" && sed -i 's/const businessDataUrl = DIRECTORY_DATA_URL_STUB;/const businessDataUrl = DIRECTORY_DATA_URL_TEST;/' config/config.js
```

## Step 3.5: Verify the final values

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/teton/1.3" && grep -nE 'const apiURL|const DIRECTORY_DATA_URL_TEST|const businessDataUrl' config/config.js
```

## Completion criteria

- [ ] `config/config.js.backup` exists.
- [ ] `apiURL` points to `WEATHER_URL_STUB`.
- [ ] `businessDataUrl` points to `DIRECTORY_DATA_URL_TEST`.
- [ ] `DIRECTORY_DATA_URL_TEST` points to `http://127.0.0.1:8000/data/all`.

---

# Phase 4: Create the Submission Evidence Directory

## Objective

Create one clean directory for the four final screenshots so unrelated files are not accidentally uploaded.

## Directory created

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission
```

## Command

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05" && mkdir -p "W05-Load-Test-Submission" && ls -ld "W05-Load-Test-Submission"
```

## Completion criteria

- [ ] `W05-Load-Test-Submission/` exists.
- [ ] The directory is initially empty.

---

# Phase 5: Start and Verify the Local Test Environment

## Objective

Run the local Django Directory service and the version 1.3 static website at the same time, then confirm all test endpoints return HTTP 200.

## Terminal 1: Start Django

### Directory used

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/directorydata_service
```

### Command

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/directorydata_service" && .venv/bin/python manage.py runserver
```

Leave Terminal 1 open.

Expected endpoint:

```text
http://127.0.0.1:8000/data/all
```

## Terminal 2: Start the website

### Directory used

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/teton/1.3
```

### Command

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270/teton/1.3" && python3 -m http.server 5500
```

Leave Terminal 2 open.

Expected pages:

```text
http://127.0.0.1:5500/index.html
http://127.0.0.1:5500/directory.html
```

## Terminal 3: Verify listeners

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270" && ss -ltnp | grep -E ':8000|:5500'
```

## Verify each endpoint

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/cse270-v13/cse270" && curl -s -o /dev/null -w "Directory API: %{http_code}\n" "http://127.0.0.1:8000/data/all" && curl -s -o /dev/null -w "Home page: %{http_code}\n" "http://127.0.0.1:5500/index.html" && curl -s -o /dev/null -w "Directory page: %{http_code}\n" "http://127.0.0.1:5500/directory.html"
```

## Expected result

```text
Directory API: 200
Home page: 200
Directory page: 200
```

## Completion criteria

- [ ] Port `8000` is listening.
- [ ] Port `5500` is listening.
- [ ] Directory API returns `200`.
- [ ] Home page returns `200`.
- [ ] Directory page returns `200`.
- [ ] Home and Directory pages render correctly in Chrome.

---

# Phase 6: Create the Postman Collection and Requests

## Objective

Create and save the two GET requests that Postman Performance Runner will use for all four tests.

## Postman objects created

```text
Collection: Web Site Test
Request: Home Page Request
Request: Directory Page Request
```

## Home request

```text
Name: Home Page Request
Method: GET
URL: http://127.0.0.1:5500/index.html
```

## Directory request

```text
Name: Directory Page Request
Method: GET
URL: http://127.0.0.1:5500/directory.html
```

## Procedure

1. Open Postman.
2. Open `Collections`.
3. Create a collection named `Web Site Test`.
4. Add `Home Page Request` using the Home URL.
5. Save the request.
6. Send the request once and confirm `200 OK`.
7. Add `Directory Page Request` using the Directory URL.
8. Save the request.
9. Send the request once and confirm `200 OK`.

## Completion criteria

- [ ] `Web Site Test` exists.
- [ ] `Home Page Request` exists and is saved.
- [ ] `Directory Page Request` exists and is saved.
- [ ] Both manual requests return `200 OK`.

---

# Phase 7: Run the Home Page Load Test

## Objective

Measure Home-page response time under average load and determine whether the average is below 50 ms.

## Postman request used

```text
Home Page Request
```

## Test configuration

```text
Virtual Users: 5
Duration: 1 minute
Load Profile: Fixed
Pass threshold: Average response time < 50 ms
```

## Output file created

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission/home-load-test.png
```

## Procedure

1. Select `Web Site Test` in Postman.
2. Click `Run`.
3. Select `Performance`.
4. Enable only `Home Page Request`.
5. Set 5 virtual users.
6. Set 1 minute.
7. Select Fixed profile.
8. Run the test.
9. Record the average response time, throughput, and error count.
10. Capture a screenshot showing the settings, graph, statistics, date, and time.
11. Save it as `home-load-test.png` in the submission directory.

## Outcome rule

```text
Average < 50 ms: PASS
Average >= 50 ms: FAIL
```

---

# Phase 8: Run the Home Page Stress Test

## Objective

Measure Home-page response time under peak load and determine whether the average is below 100 ms.

## Postman request used

```text
Home Page Request
```

## Test configuration

```text
Virtual Users: 100
Duration: 2 minutes
Load Profile: Ramp up
Pass threshold: Average response time < 100 ms
```

## Output file created

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission/home-stress-test.png
```

## Procedure

1. Start a new Performance Runner execution.
2. Enable only `Home Page Request`.
3. Set 100 virtual users.
4. Set 2 minutes.
5. Select Ramp up.
6. Run the test.
7. Record the average response time, throughput, and error count.
8. Capture the full result with date and time.
9. Save it as `home-stress-test.png`.

## Outcome rule

```text
Average < 100 ms: PASS
Average >= 100 ms: FAIL
```

---

# Phase 9: Run the Directory Page Load Test

## Objective

Measure Directory-page response time under average load while the local Django service is running.

## Postman request used

```text
Directory Page Request
```

## Test configuration

```text
Virtual Users: 5
Duration: 1 minute
Load Profile: Fixed
Pass threshold: Average response time < 50 ms
```

## Output file created

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission/directory-load-test.png
```

## Procedure

1. Confirm Django is still running on port 8000.
2. Start a new Postman Performance run.
3. Enable only `Directory Page Request`.
4. Set 5 virtual users.
5. Set 1 minute.
6. Select Fixed profile.
7. Run the test.
8. Record average response time, throughput, and errors.
9. Capture the complete result.
10. Save it as `directory-load-test.png`.

## Outcome rule

```text
Average < 50 ms: PASS
Average >= 50 ms: FAIL
```

---

# Phase 10: Run the Directory Page Stress Test

## Objective

Measure Directory-page response time under peak load and determine whether the average remains below 100 ms.

## Postman request used

```text
Directory Page Request
```

## Test configuration

```text
Virtual Users: 100
Duration: 2 minutes
Load Profile: Ramp up
Pass threshold: Average response time < 100 ms
```

## Output file created

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission/directory-stress-test.png
```

## Procedure

1. Confirm both local servers remain running.
2. Start a new Postman Performance run.
3. Enable only `Directory Page Request`.
4. Set 100 virtual users.
5. Set 2 minutes.
6. Select Ramp up.
7. Run the test.
8. Record average response time, throughput, and errors.
9. Capture the complete result.
10. Save it as `directory-stress-test.png`.

## Outcome rule

```text
Average < 100 ms: PASS
Average >= 100 ms: FAIL
```

---

# Phase 11: Audit the Four Screenshot Files

## Objective

Ensure every screenshot is readable, unique, correctly named, and contains enough evidence for full rubric credit.

## Directory inspected

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission
```

## Command

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission" && ls -lh
```

## Required files

```text
home-load-test.png
home-stress-test.png
directory-load-test.png
directory-stress-test.png
```

## Screenshot content checklist

Each screenshot must show:

- [ ] Correct request name.
- [ ] Virtual-user count.
- [ ] Test duration.
- [ ] Load profile.
- [ ] Performance graph.
- [ ] Average response time.
- [ ] Throughput or request rate.
- [ ] Error count.
- [ ] Date and time.
- [ ] Readable text.

## Optional file-type verification

```bash
cd "/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission" && file home-load-test.png home-stress-test.png directory-load-test.png directory-stress-test.png
```

---

# Phase 12: Prepare the Canvas Outcome Comment

## Objective

Report all four measured averages, thresholds, and Pass or Fail conclusions to satisfy the 10-point Outcome criterion.

## File optionally created for local reference

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE270/w05/W05-Load-Test-Submission/canvas-comment.txt
```

The comment is pasted into Canvas but is not uploaded as a fifth assignment file.

## Comment template

```text
W05 Conducting a Load Test Outcomes

Home Page Load Test
Average response time: [VALUE] ms
Requirement: Less than 50 ms under 5 simultaneous users
Outcome: PASS or FAIL

Home Page Stress Test
Average response time: [VALUE] ms
Requirement: Less than 100 ms under 100 simultaneous users
Outcome: PASS or FAIL

Directory Page Load Test
Average response time: [VALUE] ms
Requirement: Less than 50 ms under 5 simultaneous users
Outcome: PASS or FAIL

Directory Page Stress Test
Average response time: [VALUE] ms
Requirement: Less than 100 ms under 100 simultaneous users
Outcome: PASS or FAIL
```

Do not estimate values. Copy each average directly from the matching screenshot.

---

# Phase 13: Submit in Canvas

## Objective

Upload exactly the four required screenshots, paste the complete outcome comment, and confirm Canvas records the submission.

## Files uploaded

```text
home-load-test.png
home-stress-test.png
directory-load-test.png
directory-stress-test.png
```

## File not uploaded

```text
canvas-comment.txt
```

The content of `canvas-comment.txt` is pasted into the Canvas comments field.

## Procedure

1. Open `W05 Activity: Conducting a Load Test` in Canvas.
2. Click `Start Assignment` or `Submit Assignment`.
3. Upload all four screenshots.
4. Confirm all four filenames are visible.
5. Paste the completed outcome comment.
6. Recheck all measured averages and outcomes.
7. Click `Submit Assignment`.
8. Wait for confirmation.
9. Verify all four attachments are listed in the submitted attempt.

---

# Final 50-Point Rubric Audit

```text
Home Page Load Test:       10 points
Home Page Stress Test:     10 points
Directory Page Load Test:  10 points
Directory Page Stress Test:10 points
All four outcomes stated:  10 points
Total:                     50 points
```

## Final checklist

- [ ] Version 1.3 project is used.
- [ ] `apiURL` uses `WEATHER_URL_STUB`.
- [ ] `businessDataUrl` uses `DIRECTORY_DATA_URL_TEST`.
- [ ] Django service runs on port 8000.
- [ ] Website runs on port 5500.
- [ ] Home request returns 200.
- [ ] Directory request returns 200.
- [ ] Home load test used 5 users, 1 minute, Fixed.
- [ ] Home stress test used 100 users, 2 minutes, Ramp up.
- [ ] Directory load test used 5 users, 1 minute, Fixed.
- [ ] Directory stress test used 100 users, 2 minutes, Ramp up.
- [ ] All four screenshots contain complete performance evidence.
- [ ] Canvas comment gives all four averages.
- [ ] Canvas comment gives all four Pass or Fail outcomes.
- [ ] Exactly four screenshots are attached.
- [ ] Canvas shows submission confirmation.

## Working-directory rule

Every terminal command in this timeline starts with the exact directory required for that command. Do not add the nonexistent `W05 Activity` directory to any path.
