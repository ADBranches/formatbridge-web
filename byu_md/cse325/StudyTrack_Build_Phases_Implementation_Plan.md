# StudyTrack Build Phases and Implementation Plan

**Course:** CSE 325 — .NET Software Development  
**Project:** StudyTrack — Student Assignment and Study Planner  
**Purpose:** Organize the project into clear build phases so the team can implement, test, document, and demonstrate the final application in a way that supports the W07 final-project rubric.  
**Development Environment:** Kali Linux / Debian-based terminal workflow  
**Primary Workflow:** Terminal-first implementation, Git/GitHub version control, Trello project-board tracking, and final demo preparation.

---

## 1. Final Rubric Alignment

The W07 final project is graded across five major rubric areas:

- **Application Function — 30 pts**
- **Application Design / UX — 20 pts**
- **Error Handling — 15 pts**
- **Documentation — 15 pts**
- **Presentation — 20 pts**

To target full credit, each build phase below is designed to support one or more of these grading categories.

---

## 2. Target MVP Scope

StudyTrack should focus first on a stable minimum viable product. The MVP should demonstrate a clear student workflow:

1. User opens the application.
2. User views a dashboard.
3. User manages courses.
4. User manages assignments.
5. User marks assignments complete.
6. User filters or sorts assignments.
7. User receives validation and feedback.
8. Reviewer can read documentation and watch a clear demo.

Optional enhancements should only be added after the MVP is stable.

---

## 3. Recommended Repository Structure

The final project repository should be organized clearly so that reviewers can understand the application quickly.

```text
StudyTrack/
├── README.md
├── .gitignore
├── docs/
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_NOTES.md
│   ├── TESTING_CHECKLIST.md
│   └── VIDEO_DEMO_SCRIPT.md
├── src/
│   └── StudyTrack/
│       ├── StudyTrack.csproj
│       ├── Program.cs
│       ├── appsettings.json
│       ├── appsettings.Development.json
│       ├── Components/
│       │   ├── Layout/
│       │   │   ├── MainLayout.razor
│       │   │   ├── MainLayout.razor.css
│       │   │   └── NavMenu.razor
│       │   ├── Pages/
│       │   │   ├── Dashboard.razor
│       │   │   ├── Courses.razor
│       │   │   ├── CourseDetails.razor
│       │   │   ├── Assignments.razor
│       │   │   ├── AssignmentDetails.razor
│       │   │   ├── StudySessions.razor
│       │   │   └── Error.razor
│       │   └── Shared/
│       │       ├── StatusBadge.razor
│       │       ├── PriorityBadge.razor
│       │       └── ValidationMessagePanel.razor
│       ├── Data/
│       │   ├── StudyTrackDbContext.cs
│       │   └── SeedData.cs
│       ├── Models/
│       │   ├── Course.cs
│       │   ├── AssignmentTask.cs
│       │   ├── StudySession.cs
│       │   ├── AssignmentStatus.cs
│       │   └── AssignmentPriority.cs
│       ├── Services/
│       │   ├── CourseService.cs
│       │   ├── AssignmentService.cs
│       │   ├── DashboardService.cs
│       │   └── StudySessionService.cs
│       └── wwwroot/
│           └── css/
│               └── app.css
└── screenshots/
    ├── dashboard.png
    ├── courses.png
    ├── assignments.png
    └── validation.png
```

If the group uses a simpler MVC or Razor Pages structure, the same feature phases still apply. The key requirement is that the final code is organized, understandable, and demonstrable.

---

# Phase 0 — Project Setup and Repository Hygiene

## Objective

Create a clean repository foundation that works well on Kali Linux / Debian and supports repeatable terminal-based development.

## Rubric Support

- Documentation
- Application Function
- Presentation readiness

## Directories and Files to Create

```text
StudyTrack/
├── README.md
├── .gitignore
├── docs/
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_NOTES.md
│   ├── TESTING_CHECKLIST.md
│   └── VIDEO_DEMO_SCRIPT.md
├── src/
└── screenshots/
```

## Key Objectives

- Create the base project folder.
- Initialize Git.
- Add `.gitignore` to exclude build artifacts.
- Create documentation folders early.
- Confirm the app builds successfully before feature work begins.
- Confirm all team members can clone, pull, branch, commit, and push.

## Terminal-First Notes

When implementation begins, all setup should be done from the terminal. Avoid editing generated files blindly. Always inspect files before changing them.

Recommended inspection commands later:

```bash
pwd
ls -la
find . -maxdepth 4 -type f | sort
git status
dotnet --version
dotnet build
```

## Completion Criteria

- Repository exists and is pushed.
- `.gitignore` exists.
- `README.md` exists.
- Documentation folder exists.
- Project builds with zero errors.

---

# Phase 1 — Project Skeleton and Navigation

## Objective

Create the basic application shell with consistent navigation, layout, branding, and placeholder pages.

## Rubric Support

- Application Design / UX
- Application Function
- Documentation

## Directories and Files to Create

```text
src/StudyTrack/
├── Program.cs
├── StudyTrack.csproj
├── Components/
│   ├── Layout/
│   │   ├── MainLayout.razor
│   │   ├── MainLayout.razor.css
│   │   └── NavMenu.razor
│   └── Pages/
│       ├── Dashboard.razor
│       ├── Courses.razor
│       ├── Assignments.razor
│       ├── StudySessions.razor
│       └── Error.razor
└── wwwroot/
    └── css/
        └── app.css
```

## Key Objectives

- Create layout and navigation.
- Add app name: `StudyTrack`.
- Add navigation links:
  - Dashboard
  - Courses
  - Assignments
  - Study Sessions
  - Documentation or Help, if implemented
- Ensure every page has a clear heading.
- Ensure navigation is consistent across the app.
- Add early responsive styling.

## User Actions Supported

- Users can open the application.
- Users can navigate between major pages.
- Users can identify the app purpose from the layout.

## Completion Criteria

- App opens without errors.
- Navigation links work.
- Pages render with headings.
- Layout is consistent.

---

# Phase 2 — Data Models and Database Layer

## Objective

Define the core entities needed for StudyTrack and create the database/data-access foundation.

## Rubric Support

- Application Function
- Error Handling
- Documentation

## Directories and Files to Create

```text
src/StudyTrack/
├── Data/
│   ├── StudyTrackDbContext.cs
│   └── SeedData.cs
├── Models/
│   ├── Course.cs
│   ├── AssignmentTask.cs
│   ├── StudySession.cs
│   ├── AssignmentStatus.cs
│   └── AssignmentPriority.cs
└── appsettings.json
```

## Key Objectives

- Define `Course` model.
- Define `AssignmentTask` model.
- Define `StudySession` model.
- Define assignment status values:
  - Pending
  - In Progress
  - Completed
  - Overdue
- Define assignment priority values:
  - Low
  - Medium
  - High
- Configure database context.
- Add seed data for demo/testing.

## Recommended Model Fields

### Course

```text
Id
Name
Code
Description
CreatedAt
UpdatedAt
```

### AssignmentTask

```text
Id
CourseId
Title
Description
DueDate
Priority
Status
CreatedAt
UpdatedAt
CompletedAt
```

### StudySession

```text
Id
AssignmentTaskId
PlannedDate
DurationMinutes
Notes
IsCompleted
CreatedAt
```

## User Actions Supported

- Users can store courses.
- Users can store assignments.
- Users can link assignments to courses.
- Users can store planned study sessions.

## Completion Criteria

- Models compile.
- Database context compiles.
- Seed data can be loaded.
- Database migration or in-memory data strategy is documented.

---

# Phase 3 — Course Management CRUD

## Objective

Implement create, read, update, and delete workflows for courses.

## Rubric Support

- Application Function
- Design / UX
- Error Handling
- Presentation

## Directories and Files to Create or Update

```text
src/StudyTrack/
├── Components/Pages/
│   ├── Courses.razor
│   └── CourseDetails.razor
├── Services/
│   └── CourseService.cs
├── Models/
│   └── Course.cs
└── docs/
    └── TESTING_CHECKLIST.md
```

## Key Objectives

- Show all courses.
- Add a course.
- Edit course details.
- Delete a course.
- View assignments connected to a course.
- Validate course name.
- Display user feedback after save/delete.

## User Actions Supported

- Users can create a course.
- Users can view a list of courses.
- Users can edit a course.
- Users can delete a course.
- Users can view course-related assignments.

## User Stories Covered

- US-05: Create Course
- US-06: View Courses
- US-07: Edit Course
- US-08: Delete Course

## Completion Criteria

- Course list displays correctly.
- Create form validates required fields.
- Edit saves updates.
- Delete requires confirmation or clear intent.
- UI feedback appears after actions.

---

# Phase 4 — Assignment Management CRUD

## Objective

Build the core StudyTrack feature: assignment management.

## Rubric Support

- Application Function
- Error Handling
- Design / UX
- Presentation

## Directories and Files to Create or Update

```text
src/StudyTrack/
├── Components/Pages/
│   ├── Assignments.razor
│   └── AssignmentDetails.razor
├── Components/Shared/
│   ├── StatusBadge.razor
│   └── PriorityBadge.razor
├── Services/
│   └── AssignmentService.cs
├── Models/
│   ├── AssignmentTask.cs
│   ├── AssignmentStatus.cs
│   └── AssignmentPriority.cs
└── docs/
    └── TESTING_CHECKLIST.md
```

## Key Objectives

- Create assignments.
- View assignments.
- Edit assignments.
- Delete assignments.
- Mark assignments complete.
- Reopen assignments if needed.
- Connect assignments to courses.
- Show priority and status clearly.

## User Actions Supported

- Users can create assignments.
- Users can view assignments.
- Users can edit assignments.
- Users can delete assignments.
- Users can mark assignments completed.
- Users can see assignment priority and status.

## User Stories Covered

- US-09: Create Assignment
- US-10: View Assignment List
- US-11: View Assignment Details
- US-12: Edit Assignment
- US-13: Delete Assignment
- US-14: Complete Assignment
- US-15: Reopen Assignment

## Completion Criteria

- Assignment CRUD works end-to-end.
- Assignments connect to courses.
- Required fields validate properly.
- Completion status updates correctly.
- Dashboard can consume assignment data.

---

# Phase 5 — Dashboard and Summary Views

## Objective

Create a dashboard that helps students quickly understand what needs attention.

## Rubric Support

- Application Function
- Design / UX
- Presentation

## Directories and Files to Create or Update

```text
src/StudyTrack/
├── Components/Pages/
│   └── Dashboard.razor
├── Components/Shared/
│   ├── StatusBadge.razor
│   └── PriorityBadge.razor
├── Services/
│   └── DashboardService.cs
└── wwwroot/css/
    └── app.css
```

## Key Objectives

- Show upcoming assignments.
- Show overdue assignments.
- Show completed assignment count.
- Show high-priority tasks.
- Provide quick links to assignment details.
- Visually separate urgent items.

## User Actions Supported

- Users can view upcoming work.
- Users can identify overdue assignments.
- Users can see completed progress.
- Users can open assignment details from dashboard.

## User Stories Covered

- US-04: Dashboard Summary
- US-14: Complete Assignment
- US-19: Filter by Due Date

## Completion Criteria

- Dashboard data is accurate.
- Overdue items are clearly shown.
- Completed and pending counts update.
- Dashboard is visually clean and demo-ready.

---

# Phase 6 — Filtering, Sorting, and Search

## Objective

Allow users to focus on the most relevant assignments.

## Rubric Support

- Application Function
- Design / UX
- Presentation

## Directories and Files to Create or Update

```text
src/StudyTrack/
├── Components/Pages/
│   └── Assignments.razor
├── Services/
│   └── AssignmentService.cs
└── docs/
    └── TESTING_CHECKLIST.md
```

## Key Objectives

- Filter assignments by course.
- Filter assignments by status.
- Filter assignments by priority.
- Sort assignments by due date.
- Sort assignments by priority.
- Clear filters.

## User Actions Supported

- Users can filter by course.
- Users can filter by status.
- Users can filter by priority.
- Users can sort by due date.
- Users can reset filters.

## User Stories Covered

- US-16: Filter by Course
- US-17: Filter by Status
- US-18: Filter by Priority
- US-19: Filter by Due Date

## Completion Criteria

- Filters return expected results.
- Filters can be combined if implemented.
- Filter UI is clear.
- Filtering behavior is included in testing checklist.

---

# Phase 7 — Study Session Planning

## Objective

Add planning support so users can schedule focused study time for assignments.

## Rubric Support

- Application Function
- Design / UX
- Presentation

## Directories and Files to Create or Update

```text
src/StudyTrack/
├── Components/Pages/
│   └── StudySessions.razor
├── Services/
│   └── StudySessionService.cs
├── Models/
│   └── StudySession.cs
└── docs/
    └── USER_GUIDE.md
```

## Key Objectives

- Create a study session.
- Link study session to assignment.
- Add planned date.
- Add duration.
- Add notes.
- Mark study session complete.

## User Actions Supported

- Users can create study sessions.
- Users can link sessions to assignments.
- Users can add notes.
- Users can mark sessions complete.

## User Stories Covered

- US-20: Create Study Session
- US-21: Complete Study Session

## Completion Criteria

- Study sessions save correctly.
- Sessions link to assignments.
- Sessions display in a useful list.
- Feature is documented as completed or partially completed.

---

# Phase 8 — Validation, Error Handling, and User Feedback

## Objective

Improve reliability and user confidence with clear validation and friendly feedback.

## Rubric Support

- Error Handling — directly supports 15 pts
- Design / UX
- Application Function

## Directories and Files to Create or Update

```text
src/StudyTrack/
├── Components/Shared/
│   └── ValidationMessagePanel.razor
├── Components/Pages/
│   ├── Courses.razor
│   ├── Assignments.razor
│   ├── AssignmentDetails.razor
│   └── Error.razor
├── Services/
│   ├── CourseService.cs
│   └── AssignmentService.cs
└── docs/
    └── TESTING_CHECKLIST.md
```

## Key Objectives

- Validate required fields.
- Show friendly validation messages.
- Handle missing records safely.
- Show success messages after create/edit/delete.
- Avoid raw crash pages during normal user workflows.
- Add defensive checks in services.

## User Actions Supported

- Users receive clear validation feedback.
- Users receive success feedback.
- Users see friendly errors for missing or invalid records.
- Users can recover from mistakes.

## User Stories Covered

- US-22: Validation Feedback
- US-23: Success Feedback
- US-24: Friendly Error Page

## Completion Criteria

- Required field validation works.
- Invalid routes or missing IDs do not crash the app.
- User feedback appears after important actions.
- Testing checklist includes error-handling scenarios.

---

# Phase 9 — Design, UX, Accessibility, and Responsiveness

## Objective

Polish the interface so the final app is pleasant, consistent, and usable.

## Rubric Support

- Application Design / UX — directly supports 20 pts
- Presentation
- Documentation

## Directories and Files to Create or Update

```text
src/StudyTrack/
├── Components/Layout/
│   ├── MainLayout.razor
│   ├── MainLayout.razor.css
│   └── NavMenu.razor
├── Components/Pages/
│   ├── Dashboard.razor
│   ├── Courses.razor
│   └── Assignments.razor
└── wwwroot/css/
    └── app.css
```

## Key Objectives

- Ensure consistent page headings.
- Ensure buttons are clear and consistently styled.
- Ensure form labels are visible and meaningful.
- Ensure color contrast is readable.
- Ensure keyboard-friendly navigation where practical.
- Improve table/card layout for smaller screens.
- Add empty-state messages.

## User Actions Supported

- Users can navigate easily.
- Users can understand each form.
- Users can use the app on different screen sizes.
- Users receive clear visual cues.

## User Stories Covered

- US-25: Responsive UI

## Completion Criteria

- App is visually consistent.
- Forms are readable and usable.
- Navigation is clear.
- Empty pages show helpful messages.
- Layout is acceptable on desktop and narrow screens.

---

# Phase 10 — Documentation Package

## Objective

Create complete documentation for reviewers, users, and developers.

## Rubric Support

- Documentation — directly supports 15 pts
- Presentation
- Application Function

## Directories and Files to Create or Update

```text
StudyTrack/
├── README.md
├── docs/
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_NOTES.md
│   ├── TESTING_CHECKLIST.md
│   └── VIDEO_DEMO_SCRIPT.md
└── screenshots/
    ├── dashboard.png
    ├── courses.png
    ├── assignments.png
    └── validation.png
```

## Key Objectives

- Write setup instructions.
- Write run instructions.
- List implemented features.
- List known limitations.
- Document user workflows.
- Document testing steps.
- Include project-board URL.
- Include team member contributions.

## Recommended README Sections

```text
Project Title
Project Overview
Team Members
Features Implemented
Technology Stack
How to Run
How to Test
Project Board Link
Demo Video Link
Known Limitations
Future Improvements
```

## Completion Criteria

- README is complete.
- User guide is clear.
- Testing checklist is complete.
- Video demo script exists.
- Project board is linked.

---

# Phase 11 — Testing and Final QA

## Objective

Verify that the application works correctly before final submission.

## Rubric Support

- Application Function
- Error Handling
- Presentation
- Documentation

## Directories and Files to Create or Update

```text
StudyTrack/
├── docs/
│   └── TESTING_CHECKLIST.md
└── screenshots/
    ├── dashboard.png
    ├── courses.png
    ├── assignments.png
    └── validation.png
```

## Key Objectives

- Build project successfully.
- Run app locally.
- Test course CRUD.
- Test assignment CRUD.
- Test completion status.
- Test filters.
- Test validation.
- Test missing record handling.
- Capture screenshots.

## Terminal Verification Commands for Later

```bash
pwd
ls -la
find . -maxdepth 4 -type f | sort
dotnet --version
dotnet build
dotnet run
git status
```

## Completion Criteria

- `dotnet build` succeeds.
- No obvious runtime errors.
- Core workflows pass manual testing.
- Screenshots are captured.
- Testing checklist is updated.

---

# Phase 12 — Final Video Demonstration

## Objective

Create a clear, organized presentation video that demonstrates the completed application and supports the presentation rubric.

## Rubric Support

- Presentation — directly supports 20 pts
- Application Function
- Design / UX
- Error Handling
- Documentation

## Directories and Files to Create or Update

```text
StudyTrack/
├── docs/
│   └── VIDEO_DEMO_SCRIPT.md
└── screenshots/
    ├── dashboard.png
    ├── courses.png
    ├── assignments.png
    └── validation.png
```

## Suggested Video Flow

```text
1. Introduce StudyTrack and the problem it solves.
2. Show project board and documentation briefly.
3. Open the app and explain navigation.
4. Demonstrate dashboard.
5. Demonstrate course management.
6. Demonstrate assignment creation.
7. Demonstrate assignment edit/delete/complete workflow.
8. Demonstrate filtering and sorting.
9. Demonstrate validation/error handling.
10. Summarize team contributions and final status.
```

## Completion Criteria

- Video is organized.
- Video shows working functionality.
- Video includes all major features.
- Video mentions documentation and project board.
- Video link is ready for Canvas text entry.

---

# Phase 13 — Final Submission Assembly

## Objective

Prepare the final Canvas text entry and confirm every required link and artifact is ready.

## Rubric Support

- All rubric areas

## Files / Links Needed

```text
GitHub Repository URL
Trello Project Board URL
Demo Video URL
README.md
USER_GUIDE.md
DEVELOPER_NOTES.md
TESTING_CHECKLIST.md
VIDEO_DEMO_SCRIPT.md
Peer Review Form, if required separately
```

## Final Canvas Text Entry Template

```text
Project Title:
StudyTrack — Student Assignment and Study Planner

GitHub Repository URL:
https://github.com/ADBranches/StudyTrack.git

Project Board URL:
https://trello.com/b/kXoxNah7

Demo Video URL:
[Paste video link here]

Documentation:
The repository includes README.md, user documentation, developer notes, testing checklist, and project-board references.

Azure DevOps Note:
Azure DevOps organization creation was attempted with the BYU-Pathway Microsoft account, but the account required an Azure subscription that was not available. The Trello board is the working project board used by the group.

Completed Features:
- [List final implemented features]

Known Limitations:
- [List honest limitations]
```

## Completion Criteria

- Repository link works.
- Project board link works.
- Video link works.
- README is visible in repository.
- Documentation files are visible in repository.
- Final app build succeeds.
- Peer review is completed if required.

---

# Phase 14 — Peer Review Preparation

## Objective

Prepare accurate peer review information if Canvas requires the peer review document.

## Files to Prepare

```text
CSE325GroupProjectPeerReview.docx
```

## Information Needed

```text
Project Name/Title: StudyTrack
Group Members:
- Edwin Kambale
- Cesar Lizandro Vivanco
- Arthur Weale
- Pastor Zimondi

Performance Categories:
- Project Management
- Communication
- Collaboration
- Contribution
- Professionalism
```

## Rating Scale

```text
3 = Exceeded expectations or did most work in the area
2 = Average / about the same as others
1 = Least contribution or weak performance
0 = Did nothing or no opportunity to rate
```

## Completion Criteria

- Peer review form is complete.
- Ratings are fair and professional.
- Optional notes are respectful and specific.

---

# Final Build-Phase Checklist

Use this checklist to confirm the project is ready for W07 final submission.

```text
[ ] Repository structure is clean.
[ ] App builds with zero errors.
[ ] Dashboard works.
[ ] Course CRUD works.
[ ] Assignment CRUD works.
[ ] Assignment completion works.
[ ] Filtering/sorting works.
[ ] Validation messages work.
[ ] Friendly error handling exists.
[ ] UI is consistent and readable.
[ ] README.md is complete.
[ ] User guide exists.
[ ] Developer notes exist.
[ ] Testing checklist exists.
[ ] Project board is organized.
[ ] Demo video is recorded and linked.
[ ] Peer review is completed if required.
[ ] Canvas final text entry includes all links.
```

---

# Notes for Kali Linux / Debian Terminal Workflow

When implementation begins, use terminal-first habits:

```bash
pwd
ls -la
git status
find . -maxdepth 4 -type f | sort
dotnet --version
dotnet build
```

Before editing files:

```bash
sed -n '1,220p' path/to/file
```

After editing files:

```bash
dotnet build
git diff -- path/to/file
git status
```

Before committing:

```bash
git add .
git status
git commit -m "meaningful commit message"
git push origin main
```

Avoid committing build artifacts:

```text
bin/
obj/
.vs/
*.user
*.suo
```

---

# Recommended Commit Sequence

```text
Phase 0 commit: Initialize project structure and documentation
Phase 1 commit: Add layout and navigation shell
Phase 2 commit: Add data models and database context
Phase 3 commit: Implement course management
Phase 4 commit: Implement assignment management
Phase 5 commit: Add dashboard summaries
Phase 6 commit: Add filtering and sorting
Phase 7 commit: Add study session planning
Phase 8 commit: Add validation and error handling
Phase 9 commit: Polish UI and responsive design
Phase 10 commit: Complete documentation package
Phase 11 commit: Final QA and demo preparation
```

---

# Final Recommendation

Build the project in this order:

```text
1. Repository and docs
2. Layout/navigation
3. Models/database
4. Course CRUD
5. Assignment CRUD
6. Dashboard
7. Filtering
8. Error handling
9. UI polish
10. Documentation
11. Video demo
12. Final submission
```

This order gives the team the highest chance of completing a stable, demonstrable application that aligns with the final W07 rubric.
