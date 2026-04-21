# PBBF Telehealth System — Agile Project Comments and User Stories

## 1. Project Comment Summary

PBBF Telehealth is a strong and meaningful software project because it addresses real maternal and postpartum care coordination needs through a modular digital platform. The breakdown shows clear operational thinking, especially around identity, patient intake, scheduling, virtual visits, screening, referrals, notifications, and governance.

### What Is Strong

- The MVP scope is thoughtfully separated from Phase 2+, which is good agile practice.
- The modules reflect real healthcare workflows instead of generic software features.
- Roles are clearly defined and support role-based access control from the start.
- The system accounts for both clinical workflow and operational oversight.
- Audit and governance are included early, which is very important in a telehealth environment.
- EPDS-first screening gives the MVP a focused clinical value proposition.
- Notification, referral, and documentation modules make the system more complete and usable in practice.

### What Needs Better Definition

- Success criteria for each MVP module should be written more explicitly.
- Acceptance criteria should define what “done” means for each user-facing workflow.
- Data privacy, retention, and access boundaries should be made more explicit.
- External integrations such as calendar sync, SMS, and telehealth session providers should be clearly marked as MVP or deferred.
- The exact patient journey across intake, scheduling, visit, screening, referral, and follow-up should be documented end-to-end.
- Operational reporting formulas such as no-show rate and utilization should be defined early.

### Overall Comment

This is a realistic, socially impactful, and professionally structured digital health project. Its biggest strength is that it already separates core MVP workflows from expansion features, which makes it suitable for agile delivery through epics, backlog prioritization, and phased releases.

---

## 2. Agile Product Framing

## Product Vision
Build a secure telehealth platform that helps patients, providers, counselors, lactation consultants, care coordinators, and administrators manage intake, appointments, virtual visits, screening, referrals, and operational oversight in a structured and auditable way.

## Primary Agile Goal for MVP
Deliver the smallest usable version of the system that allows:

- secure role-based access
- patient onboarding and consent
- appointment booking and visit access
- encounter documentation
- EPDS screening workflow
- basic referral handling
- operational notifications
- auditability of key actions

## Suggested MVP Personas

- **Patient** — registers, submits intake, books appointments, joins visits, receives notifications
- **Provider** — reviews patient information, conducts visits, documents encounters, triggers referrals
- **Counselor** — participates in care delivery and encounter workflows
- **Lactation Consultant** — supports relevant visit and documentation workflows
- **Care Coordinator** — manages referrals and follow-up coordination
- **Admin** — provisions users, monitors operations, reviews metrics and audit records

---

## 3. Agile Epic Structure

## MVP Epics
1. Auth & Identity
2. Patient Intake & Consent
3. Appointment Scheduling
4. Virtual Visit Access
5. Provider Encounter Documentation
6. Screening (EPDS-First)
7. Basic Referral
8. Admin Operations Dashboard
9. Notification
10. Basic Audit & Governance

## Post-MVP Epics
1. Secure Messaging
2. Education Library
3. Community Navigation Directory
4. Multilingual Delivery
5. Mobile App
6. AI-Assisted Triage and Advanced Analytics

---

## 4. MVP User Stories Backlog

The following user stories are written in agile style and grouped by epic.

# Epic 1: Auth & Identity

### US-001
As a patient, I want to self-register for an account so that I can access telehealth services.

**Priority:** Must Have  
**Acceptance Criteria:**
- Patient can create an account with required identity fields.
- New account is stored with the patient role.
- Terms and privacy policy consent are captured during registration.

### US-002
As an admin, I want to provision provider and internal user accounts so that care team members can access the platform with the correct roles.

**Priority:** Must Have  
**Acceptance Criteria:**
- Admin can create internal accounts.
- Internal accounts can be assigned roles such as provider, counselor, lactation_consultant, care_coordinator, and admin.
- Provisioning activity is auditable.

### US-003
As a user, I want to sign in and sign out securely so that I can access the platform safely.

**Priority:** Must Have

### US-004
As an internal user, I want MFA during sign-in so that privileged access is better protected.

**Priority:** Must Have

### US-005
As an admin, I want to activate, deactivate, and change user roles so that access remains controlled over time.

**Priority:** Must Have

### US-006
As a user, I want password reset and account recovery so that I can regain access when locked out.

**Priority:** Should Have

### US-007
As the system, I want authentication and role events audited so that security-sensitive actions are traceable.

**Priority:** Must Have

---

# Epic 2: Patient Intake & Consent

### US-008
As a patient, I want to complete my profile basics so that the care team has my essential identity and contact information.

**Priority:** Must Have

### US-009
As a patient, I want to acknowledge consent and privacy terms so that my intake is compliant with program requirements.

**Priority:** Must Have

### US-010
As a patient, I want the system to store the consent version I accepted so that consent records are traceable.

**Priority:** Must Have

### US-011
As a patient, I want to save my intake form as a draft so that I can complete it later.

**Priority:** Should Have

### US-012
As a patient, I want to submit my intake form when complete so that I can move forward to care review and scheduling.

**Priority:** Must Have

### US-013
As a patient, I want to select my service need so that my care request is routed appropriately.

**Priority:** Must Have

### US-014
As a patient, I want to add an emergency contact so that the care team has critical support information when needed.

**Priority:** Must Have

### US-015
As a care team member, I want to see intake status values such as draft, submitted, under_review, and ready_to_schedule so that I can manage workflow progression.

**Priority:** Must Have

### US-016
As a patient, I want to upload intake-related attachments so that supporting documents can be reviewed with my submission.

**Priority:** Should Have

### US-017
As the system, I want timestamped intake submission history so that changes and submissions are traceable.

**Priority:** Must Have

---

# Epic 3: Appointment Scheduling

### US-018
As a patient, I want to see bookable service types so that I can choose the correct type of visit.

**Priority:** Must Have

### US-019
As a patient, I want to view available appointment slots so that I can choose a suitable time.

**Priority:** Must Have

### US-020
As a patient, I want to book an appointment so that I can secure a telehealth visit.

**Priority:** Must Have

### US-021
As a patient, I want to reschedule or cancel an appointment so that I can manage changes in availability.

**Priority:** Must Have

### US-022
As a scheduler or care team member, I want appointments to include reason and visit type so that visit preparation is clearer.

**Priority:** Should Have

### US-023
As a provider, I want appointments to be assigned to a specific provider so that responsibility is clear.

**Priority:** Must Have

### US-024
As a user, I want appointment times displayed in the correct timezone so that I do not miss visits due to time confusion.

**Priority:** Must Have

### US-025
As the system, I want appointment statuses such as booked, confirmed, rescheduled, cancelled, completed, and no_show so that scheduling workflow is trackable.

**Priority:** Must Have

---

# Epic 4: Virtual Visit Access

### US-026
As a patient, I want access to my telehealth session link so that I can join my scheduled visit.

**Priority:** Must Have

### US-027
As a provider, I want a provider join page or launch action so that I can start the visit from within the platform.

**Priority:** Must Have

### US-028
As the system, I want to capture patient and provider join timestamps so that participation can be tracked.

**Priority:** Must Have

### US-029
As a patient, I want a waiting room or lobby state so that I know I am in the correct place before the session begins.

**Priority:** Must Have

### US-030
As the system, I want session states such as scheduled, waiting, in_progress, ended, and no_show so that visit lifecycle is visible.

**Priority:** Must Have

### US-031
As a patient, I want a post-visit next-steps page so that I know what happens after the session ends.

**Priority:** Should Have

### US-032
As a user, I want basic device and browser guidance before joining so that I can reduce technical issues during my visit.

**Priority:** Should Have

### US-033
As the system, I want visit access controlled by appointment and role so that only authorized participants can join.

**Priority:** Must Have

---

# Epic 5: Provider Encounter Documentation

### US-034
As a provider, I want to see a patient chart summary during a visit so that I have the context I need for care delivery.

**Priority:** Must Have

### US-035
As a provider, I want to create an encounter record tied to an appointment so that clinical documentation matches the visit.

**Priority:** Must Have

### US-036
As a provider, I want to draft, save, update, and finalize encounter notes so that documentation can be completed accurately.

**Priority:** Must Have

### US-037
As a provider, I want documentation templates so that note-taking is faster and more consistent.

**Priority:** Should Have

### US-038
As a provider, I want to review screening results inside the encounter so that my documentation reflects patient risk and status.

**Priority:** Must Have

### US-039
As a provider, I want to capture assessment and follow-up plans so that the care record includes next actions.

**Priority:** Must Have

### US-040
As a provider, I want to trigger a referral from the encounter workflow so that follow-on care can be initiated directly from documentation.

**Priority:** Must Have

### US-041
As the system, I want note changes audited so that documentation updates are traceable.

**Priority:** Must Have

---

# Epic 6: Screening (EPDS-First)

### US-042
As a patient, I want to complete the EPDS questionnaire digitally so that screening can happen efficiently.

**Priority:** Must Have

### US-043
As the system, I want EPDS answers captured and scored automatically so that screening results are immediate and consistent.

**Priority:** Must Have

### US-044
As the system, I want EPDS score banding and severity categories so that providers can interpret results more quickly.

**Priority:** Must Have

### US-045
As the system, I want critical responses flagged so that urgent concerns can be escalated appropriately.

**Priority:** Must Have

### US-046
As a provider, I want to review EPDS results and history by patient so that I can understand current and past screening outcomes.

**Priority:** Must Have

### US-047
As the system, I want the EPDS result linked to the encounter and a rescreen due date stored so that follow-up care remains organized.

**Priority:** Must Have

### US-048
As the system, I want EPDS completion status tracked so that incomplete and completed screenings can be distinguished.

**Priority:** Must Have

---

# Epic 7: Basic Referral

### US-049
As a provider or care coordinator, I want to create a referral for a patient so that additional support or services can be initiated.

**Priority:** Must Have

### US-050
As a provider or care coordinator, I want to specify referral category, destination, notes, and follow-up date so that the referral is actionable.

**Priority:** Must Have

### US-051
As a care team member, I want referral statuses such as created, sent, acknowledged, completed, and closed so that referral progress can be monitored.

**Priority:** Must Have

### US-052
As a care team member, I want referrals linked to both patient and encounter so that clinical context is preserved.

**Priority:** Must Have

### US-053
As a care team member, I want a basic referral status timeline so that I can see how the referral progressed over time.

**Priority:** Should Have

---

# Epic 8: Admin Operations Dashboard

### US-054
As an admin, I want role-based user counts so that I can monitor staffing and enrollment levels.

**Priority:** Must Have

### US-055
As an admin, I want appointment volume, completed telehealth visits, and no-show rate so that I can monitor service delivery.

**Priority:** Must Have

### US-056
As an admin, I want EPDS completion and referral completion metrics so that I can measure workflow adoption and outcomes.

**Priority:** Must Have

### US-057
As an admin, I want provider utilization and scheduling oversight views so that I can manage operational balance.

**Priority:** Should Have

### US-058
As an admin, I want basic export functionality for operational and grant reporting so that I can share program evidence externally.

**Priority:** Should Have

---

# Epic 9: Notification

### US-059
As a patient, I want appointment confirmation notifications so that I know my booking succeeded.

**Priority:** Must Have

### US-060
As a patient, I want appointment reminder notifications so that I remember upcoming visits.

**Priority:** Must Have

### US-061
As a patient, I want reschedule, cancellation, and missed-visit follow-up notifications so that I stay informed when visit status changes.

**Priority:** Must Have

### US-062
As a care team member, I want referral follow-up reminders so that pending referrals are not overlooked.

**Priority:** Should Have

### US-063
As the system, I want notification templates with patient/provider names, date, time, and service type so that messages are useful and consistent.

**Priority:** Must Have

### US-064
As a patient, I want my contact preference and notification channel stored so that communication reaches me appropriately.

**Priority:** Must Have

### US-065
As the system, I want delivery status logs for notifications so that communication attempts can be verified.

**Priority:** Must Have

---

# Epic 10: Basic Audit & Governance

### US-066
As an admin, I want authentication, consent, intake, appointment, encounter, referral, and admin actions logged so that the platform remains accountable.

**Priority:** Must Have

### US-067
As an admin, I want to filter audit events by user, action, and date so that investigations and reviews are manageable.

**Priority:** Must Have

### US-068
As an admin, I want a basic incident tracking record so that governance issues can be documented.

**Priority:** Should Have

### US-069
As an admin, I want the audit trail exportable so that compliance and reporting activities are supported.

**Priority:** Should Have

---

## 5. Post-MVP Backlog User Stories

# Epic 11: Secure Messaging

### US-070
As a patient, I want secure one-to-one messaging with my care team so that I can communicate between visits.

### US-071
As a care team member, I want thread access controlled by role so that messages remain private and relevant.

### US-072
As a user, I want unread status, attachments, and search in messages so that conversations are manageable.

---

# Epic 12: Education Library

### US-073
As a patient, I want a searchable education resource library so that I can access relevant support materials.

### US-074
As a provider, I want to assign curated resources to patients so that education can be personalized.

---

# Epic 13: Community Navigation Directory

### US-075
As a care coordinator, I want a filterable resource directory so that I can route patients to community support services.

### US-076
As a care team member, I want closed-loop referral tracking into community resources so that outcomes are easier to monitor.

---

# Epic 14: Multilingual Delivery

### US-077
As a patient, I want to receive content in my preferred language so that I can understand care information clearly.

### US-078
As the system, I want language fallback logic so that untranslated content still remains usable.

---

# Epic 15: Mobile App

### US-079
As a patient, I want a mobile dashboard and telehealth join flow so that I can use the system conveniently on my phone.

### US-080
As a patient, I want push notifications on mobile so that I do not miss important updates.

---

# Epic 16: AI-Assisted Triage and Advanced Analytics

### US-081
As a care team member, I want triage suggestions based on intake and screening data so that risk routing can be supported.

### US-082
As an admin, I want advanced trend and cohort analytics so that operational and grant reporting become more insightful.

### US-083
As the system, I want all AI-generated recommendations to require human review before acceptance so that care decisions remain supervised.

---

## 6. Suggested Backlog Prioritization for First Release

## Release 1 — Core Usable MVP
Focus first on:

- US-001 to US-005
- US-008 to US-015
- US-018 to US-025
- US-026 to US-030
- US-034 to US-041
- US-042 to US-048
- US-049 to US-052
- US-054 to US-056
- US-059 to US-065
- US-066 to US-067

## Release 2 — MVP Hardening
Add next:

- US-006
- US-016 to US-017
- US-031 to US-033
- US-053
- US-057 to US-058
- US-068 to US-069

## Release 3 — Phase 2 Expansion
Add:

- US-070 to US-083

---

## 7. Definition of Done for Agile Delivery

A user story should be considered done only when:

- development is complete
- role permissions work correctly
- validation rules are enforced
- audit logging works where required
- success and failure states are handled
- the workflow is testable end-to-end
- acceptance criteria are met
- documentation is updated

---

## 8. Closing Note

This backlog is structured to match agile planning practice: vision, personas, epics, MVP scope, prioritized user stories, and phased delivery. It can be used directly for backlog grooming, sprint planning, Jira/Trello setup, and software requirements documentation for the PBBF Telehealth System.
