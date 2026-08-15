# Enhanced Prompt: MVP Delivery Timeline for the Android Service Platform

## Role

Act as a **principal systems architect, senior Rust engineer, DevOps lead, security engineer, and technical program manager** responsible for planning a lawful, Linux-first Android diagnostics, firmware, recovery, and workshop-management platform.

Use the supplied **Universal Android Service Platform: Delivery Roadmap** as the authoritative baseline. Refine it into a focused, implementation-ready **MVP timeline**. Do not replace the roadmap with an unrelated architecture or expand the plan into post-MVP chipset coverage unless an MVP dependency requires it.

## Project Context

- **Project type:** Lawful Android device diagnostics, firmware analysis, controlled stock-firmware flashing, recovery support, job management, and audit reporting.
- **Primary development environment:** Kali Linux or another Debian-based Linux distribution.
- **Planned project root:** `/home/trovas/labs/android-service-platform`
- **Architecture direction:** Linux-first, with portable core modules and future Windows adapters.
- **Planning baseline:** 15 August 2026.
- **MVP target:** A safe internal workshop release that supports reliable device discovery, ADB and Fastboot diagnostics, firmware inspection, compatibility validation, controlled stock-firmware flashing for an explicitly verified device list, and auditable workshop jobs.
- **Safety boundary:** Authorized servicing only. Do not include credential extraction, account-lock bypassing, carrier-lock bypassing, unauthorized bootloader operations, device-identity alteration, or access to stolen devices.

## Primary Task

Produce a detailed **MVP delivery timeline** that the engineering team can follow from Phase 0 through the internal workshop MVP release.

The plan must be specific enough that, at the start of every phase, the team knows:

1. The phase objective.
2. The exact scope included and excluded.
3. The tools and technologies permitted in that phase.
4. The directories and files that must be inspected, created, populated, or modified.
5. The implementation sequence.
6. The tests and evidence required.
7. The completion criteria.
8. The phase gate that prevents premature progression.

## Mandatory Planning Rules

### 1. Limit the timeline to the focused MVP

Cover only the phases needed to reach the internal workshop MVP. Use the previous roadmap as guidance, particularly:

- Phase 0: Product boundaries and technical research
- Phase 1: Repository and development foundation
- Phase 2: Device discovery and transport layer
- Phase 3: ADB and Fastboot MVP
- Phase 4: Firmware analysis and safe flash planning
- Phase 5: Controlled stock-firmware flashing
- The minimum workshop authorization, job-record, and audit capabilities required for operating the MVP safely

Clearly identify the exact point at which the MVP is considered complete.

Do not include Windows production support, MediaTek BROM operations, Qualcomm EDL operations, Samsung proprietary flashing, UniSoc flashing, reseller management, Kubernetes migration, or global scaling as MVP work. These may appear only in a short **Deferred Until After MVP** section.

### 2. State an explicit objective for every phase

For each phase, provide:

- **Primary objective**
- **Business outcome**
- **Technical outcome**
- **Security and compliance objective**
- **In-scope capabilities**
- **Out-of-scope capabilities**

Objectives must be measurable. Avoid vague statements such as “set up the backend” or “implement device support.”

### 3. Specify the exclusive tools and technologies for every phase

For each phase, list only the tools and technologies that are actually required during that phase. Do not provide several interchangeable alternatives.

Use a single, consistent MVP stack unless the previous roadmap makes a different choice unavoidable. Prefer the following baseline:

- **Systems and protocol implementation:** Rust
- **Async runtime:** Tokio
- **Desktop shell:** Tauri 2
- **Frontend:** React and TypeScript
- **Styling:** Tailwind CSS
- **Package manager:** npm, unless the inspected repository already proves another package manager is in use
- **Local persistence:** SQLite
- **USB:** libusb through `rusb`
- **Linux device discovery:** udev
- **Serial communication:** `serialport-rs`
- **ADB and Fastboot:** Official Android SDK Platform Tools, invoked through controlled Rust adapters
- **Backend API:** Rust with Axum
- **Primary server database:** PostgreSQL
- **Short-lived backend state:** Redis, only where a defined MVP requirement justifies it
- **Development orchestration:** Docker Compose
- **CI:** GitHub Actions
- **Structured logging:** `tracing` and `tracing-subscriber`
- **Serialization and validation:** Serde and explicitly selected validation crates
- **API contracts:** OpenAPI
- **Cryptographic signatures:** Ed25519
- **Checksums:** SHA-256
- **Testing:** Rust built-in tests, integration tests, protocol replay tests, and hardware-in-the-loop tests

For every selected technology, include:

- Its exact purpose in that phase.
- The component that uses it.
- Why it is required at that point.
- What must not yet be introduced.

Do not use phrases such as “Go or Rust,” “GitHub Actions or Azure DevOps,” or “gRPC or local sockets.” Select one technology when a choice is necessary and explain the choice briefly.

### 4. Provide exact file and directory impact for every phase

For each phase, include a **Repository Impact** subsection divided into:

- **Inspect first**
- **Create**
- **Populate**
- **Modify**
- **Do not touch yet**

Use exact paths relative to:

```text
/home/trovas/labs/android-service-platform
```

Every listed path must include:

- Whether it is a file or directory.
- Its responsibility.
- The phase in which it first appears.
- The specific content or configuration added in that phase.
- Whether later phases are expected to modify it.

Do not invent files merely to make the structure look comprehensive. Every path must support a named objective, deliverable, test, or operational requirement.

Start from this candidate structure, but refine it when necessary:

```text
android-service-platform/
├── apps/
│   ├── desktop/
│   └── admin-portal/
├── crates/
│   ├── device-core/
│   ├── usb-transport/
│   ├── serial-transport/
│   ├── adb-adapter/
│   ├── fastboot-adapter/
│   ├── firmware-core/
│   ├── workflow-engine/
│   └── audit-core/
├── services/
│   └── api/
├── schemas/
├── tests/
│   ├── fixtures/
│   ├── protocol-replay/
│   ├── integration/
│   └── hardware-in-loop/
├── infrastructure/
├── documentation/
├── scripts/
├── .github/
├── Cargo.toml
├── package.json
├── docker-compose.yml
└── README.md
```

If a proposed path is unnecessary for the MVP, explicitly remove or defer it instead of retaining it automatically.

### 5. Respect inspection-first implementation

Do not assume the current state of `/home/trovas/labs` or the project repository.

Phase 0 must begin with a read-only inspection of:

- The exact working directory.
- Existing project directories and files.
- Git state, if a repository already exists.
- Installed Rust, Node.js, npm, Docker, ADB, and Fastboot versions.
- Existing configuration that may affect architecture or setup.

File creation or modification must not be proposed as already completed before inspection results are reviewed.

When displaying terminal commands:

- Begin every command block with the exact directory to enter.
- Use `/home/trovas/labs` before the repository exists.
- Use `/home/trovas/labs/android-service-platform` only after repository creation is approved by the applicable phase gate.
- Avoid wildcarded project paths.
- Do not use `|| exit 1`.
- Avoid heredocs.
- Use directly executable, syntax-checked shell commands.
- Keep inspection commands read-only until the plan explicitly reaches an approved creation step.

### 6. Enforce strict phase gates

At the end of every phase, provide:

- **Required evidence**
- **Pass criteria**
- **Failure conditions**
- **Review checklist**
- **Go/no-go decision owner**
- **Artifacts to archive**
- **Rollback or remediation action if the gate fails**

Do not continue automatically to the next phase. End each phase with an explicit instruction stating that implementation must stop until the phase evidence has been reviewed and the next phase has been authorized.

### 7. Include realistic scheduling and dependencies

For every phase, state:

- Duration in weeks.
- Planned start and end dates.
- Dependencies from earlier phases.
- Work that can run in parallel.
- Critical-path tasks.
- Required engineering roles.
- Required physical devices, cables, hubs, or laboratory equipment.
- Main risks and mitigations.

Base the dates on a planning start of **17 August 2026**. If the focused MVP can realistically be delivered earlier than the previous internal flashing target, explain which scope reductions make that possible. Do not compress hardware testing into unrealistic timeframes.

### 8. Define measurable MVP success criteria

The final MVP definition must include, at minimum:

- Reliable discovery and tracking of the approved physical-device test matrix.
- Safe handling of device connection, disconnection, and mode transitions.
- ADB and Fastboot read-only diagnostics without manual terminal intervention.
- Unambiguous targeting when multiple devices are connected.
- Firmware archive inspection without writing to a device.
- Package checksum and manifest verification.
- Model, region, bootloader, slot, partition, and downgrade-risk checks where applicable.
- Human-readable flash plans before execution.
- Controlled stock-firmware flashing for an explicitly approved device list.
- Preflight and post-write verification.
- Tested cable-loss and power-loss recovery procedures.
- Proof-of-ownership and repair authorization records.
- Technician identity and job linkage for every destructive action.
- Signed operation reports and tamper-evident audit records.
- A documented physical-device pass rate and a list of unsupported devices.
- Installation, rollback, backup, recovery, and support documentation.

## Required Output Structure

Return the answer as a single, polished Markdown document using this exact high-level structure:

```markdown
# Android Service Platform: Focused MVP Delivery Timeline

## 1. Executive Summary
## 2. MVP Scope and Non-Goals
## 3. Fixed MVP Technology Stack
## 4. Initial Repository Map
## 5. Timeline at a Glance
## 6. Phase 0: Discovery, Boundaries, and Architecture
## 7. Phase 1: Repository and Development Foundation
## 8. Phase 2: Device Discovery and Transport
## 9. Phase 3: ADB and Fastboot Diagnostics
## 10. Phase 4: Firmware Inspection and Flash Planning
## 11. Phase 5: Controlled Flashing and Recovery Validation
## 12. Phase 6: Minimum Workshop Authorization and Audit Layer
## 13. MVP Release Candidate and Internal Workshop Pilot
## 14. Cross-Phase File and Directory Change Index
## 15. Cross-Phase Test Matrix
## 16. Security, Legal, and Data-Handling Controls
## 17. Risks, Dependencies, and Contingencies
## 18. MVP Definition of Done
## 19. Deferred Until After MVP
## 20. Immediate Next Action
```

## Required Phase Template

Use the following subsection order for every phase:

```markdown
### Objective
### Business Outcome
### Technical Outcome
### Security and Compliance Objective
### Duration and Dates
### Dependencies
### In Scope
### Out of Scope
### Exclusive Tools and Technologies
### Required Team and Hardware
### Implementation Sequence
### Repository Impact
#### Inspect First
#### Create
#### Populate
#### Modify
#### Do Not Touch Yet
### Tests and Validation
### Deliverables
### Required Evidence
### Completion Criteria
### Failure Conditions
### Risks and Mitigations
### Phase Gate
```

## Formatting Requirements

- Produce valid GitHub-flavored Markdown.
- Use tables only for concise summaries such as dates, ownership, milestones, or traceability.
- Do not place source code or terminal commands inside tables.
- Place directory trees and terminal commands in fenced code blocks.
- Use checklists for phase gates and definitions of done.
- Use exact dates rather than only “Week 1” or “Month 2.”
- Keep technology names and file paths consistent across all phases.
- Distinguish clearly between files that are created, populated, and later modified.
- Do not claim that commands have been executed, files have been created, or tests have passed.
- Do not provide exploit procedures or unauthorized device-access techniques.
- Do not include placeholder phrases such as “and so on,” “etc.,” or “as needed” where an exact requirement can be stated.

## Final Quality Check

Before returning the document, verify that:

- Every phase has a specific and measurable objective.
- Every phase names an exclusive, non-ambiguous technology set.
- Every phase lists exact repository paths and the required action for each path.
- Every file or directory supports a stated deliverable or test.
- Dates and dependencies are internally consistent.
- No destructive operation appears before firmware compatibility validation and authorization controls.
- No phase begins before its previous gate is passed.
- The MVP endpoint is explicit and testable.
- Post-MVP work is clearly separated from MVP commitments.
- The immediate next action is Phase 0 inspection only.

## Source Material

Use the supplied **Universal Android Service Platform: Delivery Roadmap** as the baseline for scope, dates, architecture, safety boundaries, repository planning, completion criteria, and phase gates. Where this enhanced prompt is stricter or more specific, follow this prompt while preserving the original roadmap’s lawful-service restrictions.
