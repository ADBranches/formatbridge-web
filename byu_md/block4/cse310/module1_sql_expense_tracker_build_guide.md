# CSE 310 – Module #1 Build Guide
## SQL Relational Databases – Personal Expense Tracker
### Target: 100/100 Submission

---

# Objective

Build a Python and SQLite Personal Expense Tracker that satisfies the complete Module #1 requirements:

- Create a relational database.
- Create at least one table.
- Insert records.
- Retrieve and query records.
- Update records.
- Delete records.
- Execute SQL through Python code.
- Receive and display query results in the application.
- Filter expenses by a date range.
- Use `SUM()` and `AVG()` aggregate functions.
- Write at least 100 lines of original code.
- Add useful function-level comments or docstrings.
- Publish the project in a public GitHub repository.
- Complete the correct SQL Relational Databases `README.md` template.
- Record a 4–5 minute video showing your face, software demonstration, and code walkthrough.
- Post the video link in the correct Microsoft Teams channel.
- Maintain an honest time log totaling at least 20 hours.
- Write a specific learning-strategies reflection.

---

# Confirmed Development Location

Use this CSE 310 course directory on Kali Linux:

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310
```

Create the project inside that directory:

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
```

Every terminal section in this guide starts with the exact directory to enter before running commands.

---

# Planned Final Project Structure

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/
├── module1_time_log.md
└── python-sqlite-expense-tracker/
    ├── .gitignore
    ├── README.md
    ├── database.py
    ├── expense_service.py
    ├── menu.py
    ├── main.py
    ├── sample_data.py
    ├── expenses.db
    ├── tests/
    │   └── test_expense_tracker.py
    └── docs/
        ├── reflection.md
        ├── video_outline.md
        └── screenshots/
```

`expenses.db` is the local SQLite database. Decide later whether to publish a safe sample database or generate it when the program starts. Never publish secrets or private financial information.

---

# Phase 1 – Inspect the Course Directory and Start Time Tracking

## Objective

Confirm the existing CSE 310 directory before changing files, and begin an honest work log.

## Directory

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310
```

## Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310
pwd
find . -maxdepth 2 -type d -print | sort
find . -maxdepth 2 -type f -print | sort
```

Create the time log only after inspecting the current structure:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310
cat > module1_time_log.md <<'EOF'
# Module 1 Time Log

| Date | Work category | Work completed | Start | End | Duration |
|---|---|---|---|---|---|
EOF

date '+%Y-%m-%d %H:%M:%S'
```

Record each genuine work session in:

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/module1_time_log.md
```

## Phase Completion Check

- The course directory is confirmed.
- Existing files were inspected before modifications.
- `module1_time_log.md` exists.
- The first start time is recorded honestly.

---

# Phase 2 – Create and Inspect the Project Directory

## Objective

Create an isolated directory for the SQL Expense Tracker without disturbing existing coursework.

## Parent Directory

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310
```

## Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310
mkdir -p python-sqlite-expense-tracker
```

Inspect the new directory:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
pwd
ls -la
```

Expected project path:

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
```

## Phase Completion Check

- The project has its own dedicated directory.
- The project name is descriptive.
- No generic name such as `Module1` or `CSE310Project` was used.

---

# Phase 3 – Create the Initial File and Directory Structure

## Objective

Create only the files and directories required for implementation, testing, documentation, and submission evidence.

## Project Directory

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
```

## Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
mkdir -p tests docs/screenshots
touch README.md .gitignore database.py expense_service.py menu.py main.py sample_data.py
touch tests/test_expense_tracker.py docs/reflection.md docs/video_outline.md
```

Inspect the structure:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
find . -maxdepth 3 -print | sort
```

## Files Created

```text
.gitignore
README.md
database.py
expense_service.py
menu.py
main.py
sample_data.py
tests/test_expense_tracker.py
docs/reflection.md
docs/video_outline.md
docs/screenshots/
```

## Phase Completion Check

- Every planned source file exists.
- The testing directory exists.
- The documentation directory exists.
- No implementation code has been added before the structure was verified.

---

# Phase 4 – Configure `.gitignore` and Initialize Local Git

## Objective

Prevent generated files and local data from entering version control, then create the repository locally before connecting it to GitHub.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/.gitignore
```

## Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
cat > .gitignore <<'EOF'
__pycache__/
*.py[cod]
.pytest_cache/
.venv/
venv/
*.db-journal
*.sqlite-journal
.env
EOF
```

Inspect the file:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
cat .gitignore
```

Initialize Git locally:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
git init
git branch -M main
git status --short
```

## Phase Completion Check

- `.gitignore` is correct.
- Git was initialized inside the project directory, not the parent course directory.
- The current branch is `main`.

---

# Phase 5 – Design the Database Schema

## Objective

Define a simple relational schema that supports CRUD operations, date filtering, and numerical summaries.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/database.py
```

## Required Database

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/expenses.db
```

## Required Table

```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    expense_date TEXT NOT NULL
);
```

Store dates using ISO format:

```text
YYYY-MM-DD
```

## Required Functions in `database.py`

```python
get_connection()
create_tables()
```

Every function must include a useful docstring that explains its purpose.

## Targeted Verification

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 database.py
ls -la expenses.db
```

If the SQLite CLI is installed, inspect the schema:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
sqlite3 expenses.db '.schema expenses'
```

## Phase Completion Check

- `expenses.db` is created by the program.
- The `expenses` table exists.
- The table includes ID, description, category, amount, and date fields.
- Database functions have docstrings.

---

# Phase 6 – Implement Expense Insertion

## Objective

Allow the Python application to insert validated expense records using parameterized SQL.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/expense_service.py
```

## Required Function

```python
add_expense(description, category, amount, expense_date)
```

## Required SQL Behavior

```sql
INSERT INTO expenses (description, category, amount, expense_date)
VALUES (?, ?, ?, ?);
```

Use placeholders rather than building SQL with string concatenation.

## Validation Requirements

- Description cannot be empty.
- Category cannot be empty.
- Amount must be numeric and greater than zero.
- Date must follow `YYYY-MM-DD`.

## Targeted Test

Insert one known sample expense, then inspect it:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -c "from database import create_tables; from expense_service import add_expense; create_tables(); print(add_expense('Internet', 'Utilities', 120.0, '2026-07-12'))"
```

Inspect records:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
sqlite3 -header -column expenses.db 'SELECT * FROM expenses;'
```

## Phase Completion Check

- A valid expense can be inserted.
- Invalid values are rejected safely.
- SQL uses parameters.
- The function has a useful docstring.

---

# Phase 7 – Implement Retrieval and Category Search

## Objective

Retrieve stored data and display query results through the Python application.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/expense_service.py
```

## Required Functions

```python
get_all_expenses()
search_expenses_by_category(category)
```

## Expected Result Format

```text
ID | Description | Category | Amount | Date
1  | Internet    | Utilities| 120.00 | 2026-07-12
```

## Targeted Tests

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -c "from expense_service import get_all_expenses; print(get_all_expenses())"
```

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -c "from expense_service import search_expenses_by_category; print(search_expenses_by_category('Utilities'))"
```

## Phase Completion Check

- All expenses can be retrieved.
- Category searches work.
- Empty query results are handled clearly.
- Query results are returned to and used by Python.

---

# Phase 8 – Implement Expense Updates

## Objective

Modify an existing database record through the software.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/expense_service.py
```

## Required Function

```python
update_expense(expense_id, description, category, amount, expense_date)
```

## Required SQL Behavior

```sql
UPDATE expenses
SET description = ?, category = ?, amount = ?, expense_date = ?
WHERE id = ?;
```

## Targeted Verification

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -c "from expense_service import update_expense; print(update_expense(1, 'Home Internet', 'Utilities', 125.0, '2026-07-12'))"
```

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
sqlite3 -header -column expenses.db 'SELECT * FROM expenses WHERE id = 1;'
```

## Phase Completion Check

- Existing records can be updated.
- A nonexistent ID is handled clearly.
- Updated values persist in SQLite.
- The function has a useful docstring.

---

# Phase 9 – Implement Expense Deletion

## Objective

Delete selected records safely while confirming whether a record existed.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/expense_service.py
```

## Required Function

```python
delete_expense(expense_id)
```

## Required SQL Behavior

```sql
DELETE FROM expenses WHERE id = ?;
```

## Targeted Verification

Add a temporary record, note its ID, delete it, then confirm it is absent:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
sqlite3 -header -column expenses.db 'SELECT * FROM expenses;'
```

## Phase Completion Check

- Existing records can be deleted.
- A nonexistent ID does not crash the program.
- Deletion is confirmed using the affected-row count.
- The function has a useful docstring.

---

# Phase 10 – Implement Date-Range Filtering

## Objective

Satisfy the date/time additional SQL requirement by querying expenses between two dates.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/expense_service.py
```

## Required Function

```python
get_expenses_by_date_range(start_date, end_date)
```

## Required SQL Behavior

```sql
SELECT id, description, category, amount, expense_date
FROM expenses
WHERE expense_date BETWEEN ? AND ?
ORDER BY expense_date, id;
```

## Targeted Test

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -c "from expense_service import get_expenses_by_date_range; print(get_expenses_by_date_range('2026-07-01', '2026-07-31'))"
```

## Phase Completion Check

- Start and end dates are validated.
- The query uses `BETWEEN` or equivalent range conditions.
- Matching records are displayed in chronological order.
- Empty date ranges are handled clearly.

---

# Phase 11 – Implement `SUM()` and `AVG()` Summaries

## Objective

Demonstrate at least two SQL aggregate functions and display the results in the program.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/expense_service.py
```

## Required Function

```python
get_spending_summary()
```

## Required SQL Behavior

```sql
SELECT
    COUNT(*) AS expense_count,
    COALESCE(SUM(amount), 0) AS total_spending,
    COALESCE(AVG(amount), 0) AS average_expense
FROM expenses;
```

## Expected Output

```text
Expense count: 5
Total spending: 450.00
Average expense: 90.00
```

## Targeted Test

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -c "from expense_service import get_spending_summary; print(get_spending_summary())"
```

## Phase Completion Check

- `SUM()` is used in SQL.
- `AVG()` is used in SQL.
- Empty-database summaries return safe numerical values.
- Python receives and displays the aggregate results.

---

# Phase 12 – Build the Console Menu

## Objective

Create a clear, repeatable user interface for every required feature.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/menu.py
```

## Required Menu

```text
1. Add expense
2. View all expenses
3. Search by category
4. Update expense
5. Delete expense
6. Filter by date range
7. View spending summary
8. Exit
```

## Required Functions

```python
display_menu()
read_menu_choice()
read_positive_amount()
read_iso_date()
format_expenses()
```

Each function must have a useful docstring.

## Targeted Test

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -m py_compile menu.py
```

## Phase Completion Check

- Every required feature has a menu option.
- Invalid menu choices are rejected without crashing.
- Empty lists and success/error messages are readable.
- Every menu function has a docstring.

---

# Phase 13 – Create the Application Entry Point

## Objective

Connect database initialization, menu handling, CRUD operations, filtering, and summaries into one working program.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/main.py
```

## Required Behavior

- Call `create_tables()` when the program starts.
- Display the menu repeatedly.
- Dispatch each menu selection to the appropriate function.
- Continue until the user selects Exit.
- Catch expected input and database errors.
- Avoid broad exception handling that hides programming errors.

## Run the Program

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 main.py
```

## Manual Acceptance Test

Complete this sequence:

1. Add at least three expenses.
2. View all expenses.
3. Search by category.
4. Update one expense.
5. Delete one expense.
6. Filter expenses by date range.
7. Display the total and average.
8. Exit normally.

## Phase Completion Check

- The full application runs from `main.py`.
- Every menu option works.
- The application exits cleanly.
- The database persists after restarting the program.

---

# Phase 14 – Add Reproducible Sample Data

## Objective

Create safe demonstration data without exposing actual personal financial records.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/sample_data.py
```

## Sample Records

Use fictional data such as:

```text
Internet | Utilities | 120.00 | 2026-07-02
Groceries | Food | 85.50 | 2026-07-05
Transport | Travel | 40.00 | 2026-07-08
Software subscription | Technology | 25.00 | 2026-07-11
Office supplies | Work | 32.75 | 2026-07-15
```

The script should avoid creating duplicate samples when run repeatedly.

## Targeted Test

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 sample_data.py
sqlite3 -header -column expenses.db 'SELECT * FROM expenses ORDER BY expense_date;'
```

## Phase Completion Check

- Sample data is fictional.
- Sample data covers multiple categories and dates.
- The script is repeatable and does not create uncontrolled duplicates.

---

# Phase 15 – Add Automated Targeted Tests

## Objective

Verify database behavior before relying on a full manual test.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/tests/test_expense_tracker.py
```

## Required Test Areas

- Table creation.
- Valid insertion.
- Invalid amount rejection.
- Retrieval.
- Update.
- Delete.
- Date-range filtering.
- `SUM()` and `AVG()` results.
- Empty-database behavior.

Use a temporary test database rather than modifying the demonstration database.

## Run Targeted Tests

If using `unittest`:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -m unittest tests/test_expense_tracker.py -v
```

## Phase Completion Check

- All targeted tests pass.
- Tests do not alter the demonstration database.
- Failing tests are fixed before continuing.

---

# Phase 16 – Run Syntax, Code-Size, and Docstring Audits

## Objective

Confirm that the source code is syntactically valid, exceeds 100 lines, and documents every function.

## Project Directory

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
```

## Syntax Test

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -m py_compile database.py expense_service.py menu.py main.py sample_data.py
```

No output means the syntax test passed.

## Code-Size Check

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
wc -l database.py expense_service.py menu.py main.py sample_data.py
```

The total must be at least 100 lines of meaningful original code. Do not pad the project with blank lines or irrelevant code.

## Function Audit

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
grep -Rni '^def ' --include='*.py' .
```

Inspect each function and confirm that a useful docstring appears immediately inside it.

## Cleanup

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
rm -rf __pycache__ tests/__pycache__
```

## Phase Completion Check

- All Python files compile.
- Meaningful code exceeds 100 lines.
- Every function has a useful docstring or function-level comment.
- Generated cache files are removed and ignored.

---

# Phase 17 – Complete the Correct SQL README

## Objective

Document the finished software using the SQL Relational Databases README template at the repository root.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/README.md
```

## Required Content

Include the exact headings required by the official SQL module template. At minimum, fully explain:

- Software overview.
- Purpose for writing the software.
- Database structure.
- Relational database and SQL features demonstrated.
- CRUD operations.
- Date-range query.
- `SUM()` and `AVG()` aggregate queries.
- Development environment.
- Python and SQLite versions.
- Instructions for running the program.
- Useful learning resources.
- Final demonstration-video link.

Do not leave placeholder instructions, braces, or unfinished text.

## Placeholder Audit

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
grep -nE '\{|\}|TODO|TBD|YOUR_|VIDEO_LINK_TO_BE_ADDED|url\.link\.goes\.here|youtube\.link\.goes\.here' README.md \
  && echo 'FAIL: README contains unfinished content.' \
  || echo 'PASS: README contains no known placeholders.'
```

## Phase Completion Check

- `README.md` is at the repository root.
- The correct SQL module template was used.
- Every section is fully populated.
- Grammar and spelling are professional.
- The video link will be added after upload.

---

# Phase 18 – Review the Time Log

## Objective

Maintain complete, truthful evidence of planning, research, implementation, troubleshooting, documentation, video production, and publishing.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/module1_time_log.md
```

## Required Entry Format

```markdown
| 2026-07-12 | Planning | Reviewed SQL requirements and defined acceptance criteria | 09:00 | 10:30 | 1.5 hours |
```

## Required Work Categories

- Planning
- Research
- Setup
- Database design
- Implementation
- Testing
- Troubleshooting
- Documentation
- Video production
- Publishing

## Review Command

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310
cat module1_time_log.md
```

## Phase Completion Check

- Every session has a date, category, description, and duration.
- The total reflects real work only.
- The final total is at least 20 genuine hours for full rubric credit.

---

# Phase 19 – Commit the Stable Local Project

## Objective

Preserve a tested project snapshot before creating the public remote repository.

## Project Directory

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
```

## Inspect Before Committing

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
git status --short
find . -maxdepth 3 -type f -print | sort
```

## Commit

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
git add .gitignore README.md database.py expense_service.py menu.py main.py sample_data.py tests docs
git status
git commit -m "Build Python SQLite expense tracker"
```

## Verify

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
git log --oneline --decorate -1
git status
```

## Phase Completion Check

- Only intended files were committed.
- The working tree is clean.
- No credentials or private data were committed.

---

# Phase 20 – Create and Connect the Public GitHub Repository

## Objective

Create an empty public GitHub destination and push the existing local repository without cloning or duplicating the project.

## Remote Repository Name

```text
python-sqlite-expense-tracker
```

On GitHub, create a new public repository with that exact name. Do not initialize the remote with a README, `.gitignore`, or license because those files already exist locally.

## Project Directory

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
```

## Connect the Remote

Replace `YOUR_USERNAME` with the actual GitHub account name:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
git remote add origin https://github.com/YOUR_USERNAME/python-sqlite-expense-tracker.git
git remote -v
```

## Push

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
git push -u origin main
```

## Verify Synchronization

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
git branch -vv
git status
git log --oneline --decorate -1
```

## Phase Completion Check

- The GitHub repository is public.
- `main` tracks `origin/main`.
- The repository contains the source code and root `README.md`.
- The public URL opens in an incognito browser.

---

# Phase 21 – Prepare the Demonstration Video

## Objective

Plan a focused 4–5 minute video that demonstrates every important requirement and explains the code clearly.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/docs/video_outline.md
```

## Required Video Outline

```text
0:00–0:30 — Introduction and purpose; face visible
0:30–2:15 — Run the program and demonstrate CRUD operations
2:15–2:50 — Demonstrate date-range filtering, SUM(), and AVG()
2:50–4:30 — Walk through database.py, expense_service.py, menu.py, and main.py
4:30–5:00 — Show README and public GitHub repository; conclude
```

## Required Demonstration Sequence

Run:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 main.py
```

Show:

1. Add an expense.
2. View expenses.
3. Update an expense.
4. Delete an expense.
5. Filter by date range.
6. Show total spending.
7. Show average spending.
8. Explain the source code and SQL statements.

## Phase Completion Check

- The recording plan fits 4–5 minutes.
- Your face will remain visible.
- Every unique SQL requirement will be demonstrated.
- A detailed code walkthrough is included.

---

# Phase 22 – Record, Publish, and Test the Video

## Objective

Publish an instructor-accessible video containing your face, a complete software demonstration, and a detailed code walkthrough.

## Project Directory Used During Recording

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
```

## Recording Checklist

- Webcam image visible.
- Microphone clear and not clipping.
- Terminal and code text readable.
- No passwords, tokens, email inboxes, or private data visible.
- Program demonstration included.
- Code walkthrough included.
- Video is 4–5 minutes.

Upload the video as Public or Unlisted, not Private.

Test the final link in an incognito browser.

## Phase Completion Check

- The video opens without account-specific permission.
- Your face is visible.
- The running program is demonstrated.
- The code is explained.
- The final URL is copied safely.

---

# Phase 23 – Add the Video Link and Push the Final README

## Objective

Complete the README with the actual published video URL and synchronize the final documentation with GitHub.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/README.md
```

Replace the temporary video line with the real URL.

## Verify the Link

Replace `VIDEO_ID` with the real identifier:

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
grep -n 'https://youtu.be/VIDEO_ID' README.md
```

## Commit and Push

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
git add README.md
git commit -m "Add SQL module demonstration video"
git push origin main
git status
```

## Phase Completion Check

- The placeholder is removed.
- The published video link is in `README.md`.
- The final README is visible on GitHub.
- The local and remote branches are synchronized.

---

# Phase 24 – Post in Microsoft Teams

## Objective

Earn the Teams-post rubric points by sharing the final video link in the correct CSE 310 channel.

## Post Content

```text
SQL Relational Databases – Personal Expense Tracker

Video:
https://youtu.be/YOUR_VIDEO_ID

Public GitHub Repository:
https://github.com/YOUR_USERNAME/python-sqlite-expense-tracker
```

Use the channel specifically associated with SQL Relational Databases or Module #1, according to the course Team menu.

## Evidence Directory

Save a screenshot, if needed, in:

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/docs/screenshots/
```

Do not commit screenshots containing private class information unless appropriate.

## Phase Completion Check

- The post is a new channel post, not an unrelated reply.
- Both links are correct.
- The post is visible in the proper channel.

---

# Phase 25 – Write the Learning-Strategies Reflection

## Objective

Prepare concrete evidence for the reflection section of the final Module Submission document.

## File

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker/docs/reflection.md
```

## Reflection Prompts

Answer in one or two substantial paragraphs:

1. Which learning strategies worked well?
2. Which strategies or lack of strategy did not work well?
3. What evidence supports your assessment?
4. What will you change in the next module?

## Strong Topics to Address

- Official documentation.
- Breaking implementation into CRUD increments.
- Targeted tests before complete application tests.
- Parameterized-query practice.
- Git commits after stable features.
- Task-estimation accuracy.
- Troubleshooting or recording delays.
- Improvements for the next sprint.

## Phase Completion Check

- The reflection is specific to this project.
- It includes both successes and weaknesses.
- It states a measurable improvement for the next module.

---

# Phase 26 – Perform Final Rubric Verification

## Objective

Verify every graded requirement before preparing the Canvas submission document.

## Project Directory

```text
/home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
```

## Final Technical Checks

```bash
cd /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/python-sqlite-expense-tracker
python3 -m unittest tests/test_expense_tracker.py -v
python3 -m py_compile database.py expense_service.py menu.py main.py sample_data.py
wc -l database.py expense_service.py menu.py main.py sample_data.py
grep -Rni '^def ' --include='*.py' .
git status
git branch -vv
git log --oneline --decorate -3
```

## Final Repository Checks

Confirm on GitHub:

- Repository visibility is Public.
- Source code is present.
- Root `README.md` is present and complete.
- Video link opens.
- Latest commit is visible.

## Final Submission Evidence Required

Prepare these facts for the Word submission document:

```text
Student name: Edwin Kambale
Module number: 1
Selected module: SQL Relational Databases
GitHub repository URL: ______________________________
YouTube video URL: _________________________________
Code is at least 100 lines: Yes
Every function has useful comments/docstrings: Yes
Correct SQL README template used: Yes
README completely populated: Yes
Video includes face, demo, and code walkthrough: Yes
Video posted in the correct Teams channel: Yes
Repository is public: Yes
Total genuine hours: ________________________________
Daily time log: Complete
Learning-strategies reflection: Complete
```

## Phase Completion Check

- Every answer above is supported by evidence.
- No unfinished requirement is marked Yes.
- The time total is truthful and matches the daily log.
- The project is ready for the Module Submission Word document.

---

# Final 100/100 Readiness Checklist

- [ ] Personal Expense Tracker runs from `main.py`.
- [ ] Database is created through Python.
- [ ] At least one SQLite table is created.
- [ ] Insert works.
- [ ] Retrieve/query works.
- [ ] Update works.
- [ ] Delete works.
- [ ] Date-range filtering works.
- [ ] `SUM()` works.
- [ ] `AVG()` works.
- [ ] Query results are used and displayed by Python.
- [ ] Input validation works.
- [ ] Expected errors are handled clearly.
- [ ] Meaningful original code totals at least 100 lines.
- [ ] Every function has a useful docstring or function-level comment.
- [ ] Targeted automated tests pass.
- [ ] Full manual acceptance test passes.
- [ ] Correct SQL Relational Databases README template is used.
- [ ] The README is fully populated at the repository root.
- [ ] The public GitHub repository contains the final project.
- [ ] Local `main` tracks `origin/main`.
- [ ] The 4–5 minute video is published.
- [ ] Your face is visible in the video.
- [ ] The running software is demonstrated.
- [ ] The code is explained in detail.
- [ ] The video works in an incognito browser.
- [ ] The final video link is included in `README.md`.
- [ ] The video link is posted in the correct Microsoft Teams channel.
- [ ] The truthful time log totals at least 20 hours.
- [ ] The learning-strategies reflection is complete.
- [ ] GitHub URL, video URL, time log, and reflection are ready for the submission document.

---

# Stop Point

Do not generate the final Canvas submission document until every checklist item is complete and supported by actual evidence.
