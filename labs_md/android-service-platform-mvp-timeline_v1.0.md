# Android Service Platform: Focused 10-Hour MVP Delivery Timeline

## 1. Executive Summary

This plan defines a strict **10-hour engineering sprint** for a functional internal demonstration MVP of a lawful Android service platform. The sprint starts from the confirmed parent directory `/home/trovas/labs` on Kali Linux or another Debian-based distribution.

The ten-hour target is realistic only for a deliberately narrow MVP. The deliverable will demonstrate a complete vertical workflow using official ADB and Fastboot tooling, Linux device discovery, read-only diagnostics, firmware package inspection, controlled Fastboot flashing against an explicit test-device allowlist, local workshop job records, authorization gates, audit logs, and a polished Tauri desktop interface.

The ten-hour MVP is **not** a universal Chimera replacement. Native MediaTek BROM, Qualcomm EDL, Samsung Download Mode, UniSoc download protocols, account-protection bypass, carrier-lock bypass, arbitrary bootloader bypass, and device-identity modification are excluded.

### Ten-hour completion target

The sprint is successful when one approved physical test device can complete this workflow:

```text
Create authorized repair job
→ Connect device
→ Detect ADB or Fastboot mode
→ Read and display device information
→ Inspect an approved firmware package
→ Generate a human-readable flash plan
→ Run preflight checks
→ Execute one allowlisted Fastboot write on a dedicated test device
→ Verify the result
→ Record a tamper-evident audit trail
→ Export a signed operation report
```

### Delivery classification

- **Hour 10 output:** Internal demonstration MVP / engineering alpha
- **Not production-ready:** Yes
- **Permitted users:** Named development and QA personnel only
- **Permitted devices:** Dedicated laboratory devices on the approved allowlist only
- **Customer-device use:** Prohibited during the sprint

---

## 2. MVP Scope and Non-Goals

### In scope

- Linux USB hot-plug observation
- ADB device discovery and authorization-state detection
- Fastboot device discovery
- Serial-port discovery for read-only inventory
- VID/PID capture
- Stable target-device selection
- Multiple-device ambiguity protection
- Read-only ADB diagnostics
- Read-only Fastboot diagnostics
- Structured command execution, cancellation, timeout, and bounded retry handling
- ZIP, TAR, and raw image firmware inspection
- SHA-256 checksums
- Basic Android sparse-image identification
- Firmware manifest generation
- Human-readable flash-plan generation
- Explicit device and firmware allowlists
- Controlled Fastboot flashing on dedicated approved test devices
- Battery, connection, model, bootloader, and partition-size preflight checks where data is available
- Post-operation verification
- Local customer, device, technician, authorization, job, and operation records
- Tamper-evident audit chaining
- Ed25519-signed operation reports
- Linux development build

### Explicit non-goals

- Windows production support
- Native MediaTek BROM or Download Agent workflows
- Qualcomm EDL, Sahara, or Firehose workflows
- Samsung proprietary Download Mode implementation
- UniSoc proprietary FDL workflows
- Account-lock or FRP bypass
- Carrier-lock bypass
- Credential extraction
- Unauthorized bootloader operations
- IMEI, MEID, serial, or device-identity modification
- Use of leaked, cracked, or unauthorized loaders
- Proprietary firmware redistribution
- Universal support claims
- Cloud licensing, credits, billing, reseller management, or multi-region deployment
- Production-grade updater
- Customer-device servicing during the sprint

---

## 3. Fixed MVP Technology Stack

### Systems and protocol layer

- **Rust:** Device-process adapters, firmware inspection, workflow enforcement, local audit logic, and report signing
- **Tokio:** Asynchronous process execution, cancellation, timeouts, event streaming, and background tasks
- **Serde:** Internal command, device, firmware, job, and report data structures
- **thiserror:** Typed errors inside reusable Rust crates
- **anyhow:** Contextual error aggregation at application boundaries only
- **tracing and tracing-subscriber:** Structured, sanitized logs
- **SHA-256:** Firmware and artifact checksums
- **Ed25519:** Manifest and operation-report signatures

### Desktop

- **Tauri 2:** Linux desktop shell
- **React:** User interface
- **TypeScript:** Frontend implementation
- **Tailwind CSS:** Interface styling
- **Vite:** Frontend development and bundling
- **npm:** JavaScript package management, unless inspection proves an existing repository already uses another manager

### Device communication

- **udev:** Linux hot-plug events
- **rusb/libusb:** USB enumeration and VID/PID data
- **serialport-rs:** Read-only serial-port discovery
- **Official Android SDK Platform Tools:** ADB and Fastboot
- **Controlled Rust subprocess adapters:** Exact executable and argument allowlists, output parsing, cancellation, and timeouts

### Data and backend boundary

- **SQLite:** Local jobs, devices, authorizations, operations, firmware manifests, and audit staging
- **SQLx:** Rust database access and migrations
- **Axum:** Deferred unless a local API is essential for team integration during the sprint
- **PostgreSQL:** Deferred from the ten-hour critical path
- **Docker Compose:** Deferred unless inspection shows an existing required service

### Quality

- `rustfmt`, Clippy, Rust tests
- ESLint, Prettier, TypeScript compiler, Vitest
- Protocol-output fixtures
- Controlled firmware fixtures
- Physical test devices

---

## 4. Initial Repository Map

The repository must not be created until Phase 0 inspection is reviewed and creation is explicitly authorized.

```text
/home/trovas/labs/android-service-platform/
├── apps/
│   └── desktop/
│       ├── src/
│       ├── src-tauri/
│       └── tests/
├── crates/
│   ├── device-core/
│   ├── usb-transport/
│   ├── adb-adapter/
│   ├── fastboot-adapter/
│   ├── firmware-core/
│   ├── workflow-engine/
│   ├── audit-core/
│   └── job-store/
├── tests/
│   ├── fixtures/
│   ├── integration/
│   └── hardware-in-loop/
├── documentation/
│   ├── architecture/
│   ├── evidence/
│   ├── safety/
│   └── release/
├── scripts/
├── Cargo.toml
├── Cargo.lock
├── package.json
├── package-lock.json
├── .gitignore
└── README.md
```

### Deferred paths

- `apps/admin-portal/`: Not required for the local MVP
- `services/api/`: Not required unless the team proves a hard integration dependency
- `infrastructure/`: No production infrastructure in the ten-hour sprint
- `.github/workflows/`: Useful after the local build is stable, but not on the first critical path

---

## 5. Timeline at a Glance

| Time | Phase | Exit result |
|---|---|---|
| 00:00-00:30 | Phase 0 | Environment, scope, team, devices, and repository state reviewed |
| 00:30-01:20 | Phase 1 | Reproducible repository foundation builds |
| 01:20-02:40 | Phase 2 | USB, ADB, Fastboot, and serial discovery integrated |
| 02:40-04:00 | Phase 3 | Read-only diagnostics and safe command runner work |
| 04:00-05:30 | Phase 4 | Firmware inspection and flash-plan generation work |
| 05:30-07:10 | Phase 5 | Allowlisted Fastboot operation and verification work on test hardware |
| 06:00-07:30 | Phase 6, parallel | Job, authorization, audit, and report workflow integrated |
| 07:30-09:00 | Release candidate | UI integration, negative tests, packaging, and documentation |
| 09:00-10:00 | Internal pilot | Scripted demonstration, evidence review, and acceptance decision |

The critical path is Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → release candidate → pilot. Phase 6 may run partly in parallel but must be integrated before any device-changing demonstration.

---

## 6. Phase 0: Discovery, Boundaries, and Architecture

### Primary Objective

Inspect the actual environment and freeze the ten-hour MVP boundary before creating or modifying the application repository.

### Business Outcome

The team begins from verified facts, named ownership, approved devices, and a fixed demonstration target.

### Technical Outcome

A reviewed inventory of tools, directories, repository conflicts, test devices, firmware fixtures, and required permissions.

### Security and Compliance Objective

Document prohibited operations, proof-of-ownership requirements, authorized test devices, firmware rights, and data-handling restrictions.

### Duration and Dates

- **Duration:** 30 minutes
- **Date:** 15 August 2026
- **Sprint time:** 00:00-00:30

### Dependencies

- Access to `/home/trovas/labs`
- Named technical lead
- Named security/compliance reviewer
- At least two dedicated laboratory Android devices

### Critical Path

Environment inspection, target-device selection, firmware-rights confirmation, and scope freeze.

### Parallel Work

The UI lead may prepare wireframes outside the repository. QA may inventory physical devices and cables.

### In Scope

Read-only inspection, team allocation, device matrix, scope record, architecture decision, and risk register.

### Out of Scope

Repository creation, package installation, dependency updates, source modification, and device writes.

### Exclusive Tools and Technologies

- POSIX shell commands for read-only inspection
- `git`, `rustc`, `cargo`, `node`, `npm`, `adb`, `fastboot`, and package-manager queries for version evidence
- No Tauri, Rust crate, frontend, database, or flashing implementation yet

### Required Team

- Technical lead
- Rust lead
- Frontend lead
- QA/device lead
- Security/compliance reviewer
- Release coordinator

### Required Devices and Laboratory Equipment

- Two dedicated Android test devices
- One unsupported device for rejection testing
- High-quality data cables
- Powered USB hub
- USB power meter
- ESD-safe workspace

### Implementation Sequence

1. Inspect `/home/trovas/labs` and verify whether the planned project root exists.
2. Inspect Git, Rust, Node.js, npm, ADB, Fastboot, libusb, udev, and SQLite availability.
3. Record exact test-device models, variants, Android versions, slot layout, partition type, and connection modes.
4. Record firmware source, rights, hashes, and exact target devices.
5. Freeze the ten-hour feature list and assign component owners.
6. Approve or reject repository creation.

### Repository Impact

#### Inspect First

- `/home/trovas/labs` directory: Parent working area and conflict check
- `/home/trovas/labs/android-service-platform` path: Existence and prior-content check
- Existing Git metadata under the planned root, if present
- Existing package and workspace manifests, if present

#### Create

None before inspection review.

#### Populate

None.

#### Modify

None.

#### Do Not Touch Yet

The entire planned application repository and all device-changing tools.

### Tests and Validation

- Verify commands are read-only
- Confirm each reported executable path and version
- Confirm each physical device is dedicated laboratory hardware
- Confirm firmware packages are authorized for testing

### Deliverables

- Environment inspection output
- Scope record
- Team ownership list
- Device matrix
- Firmware fixture inventory
- Architecture decision record
- Risk register

### Required Evidence

Store later, after repository creation is authorized, under `documentation/evidence/phase-0/`.

### Completion Criteria

- Actual environment inspected
- Repository state known
- Toolchain evidence captured
- Devices and firmware fixtures approved
- MVP scope frozen
- Repository creation explicitly authorized

### Failure Conditions

- Existing repository contents are not understood
- No dedicated test device exists
- Firmware rights are unclear
- Required staff ownership is missing
- The team attempts to include prohibited or proprietary bypass functionality

### Risks and Mitigations

- **Risk:** Inspection consumes too much sprint time. **Mitigation:** Limit inspection to architecture-affecting facts.
- **Risk:** Existing directory conflicts with the planned name. **Mitigation:** Stop and review rather than overwrite.

### Review Checklist

- [ ] Parent directory inspected
- [ ] Planned repository path checked
- [ ] Toolchain versions recorded
- [ ] Test devices approved
- [ ] Firmware rights confirmed
- [ ] Team owners assigned
- [ ] Scope frozen

### Phase Gate

**Decision owner:** Technical lead with security/compliance reviewer.

Stop implementation at this phase gate. Do not begin Phase 1 until the inspection evidence has been reviewed, blocking failures have been resolved, and repository creation has been explicitly authorized.

---

## 7. Phase 1: Repository and Development Foundation

### Primary Objective

Create the smallest reproducible Rust/Tauri workspace that all squads can build.

### Business Outcome

All developers work against one stable structure with defined ownership and integration contracts.

### Technical Outcome

A launching Tauri application, Rust workspace, SQLite migration baseline, shared types, linting, and test commands.

### Security and Compliance Objective

Establish secret handling, log sanitization, destructive-operation defaults, and dependency controls before device functionality.

### Duration and Dates

- **Duration:** 50 minutes
- **Date:** 15 August 2026
- **Sprint time:** 00:30-01:20

### Dependencies

Phase 0 go decision.

### Critical Path

Workspace creation, desktop launch, shared contracts, and reproducible build.

### Parallel Work

Frontend shell, Rust crates, local data schema, and test harness may be implemented in parallel after shared contracts are frozen.

### In Scope

Repository skeleton, desktop shell, build scripts, local schema, logs, and quality checks.

### Out of Scope

USB logic, ADB/Fastboot operations, firmware writes, cloud services, and production packaging.

### Exclusive Tools and Technologies

- Rust, Cargo workspace, Tauri 2
- React, TypeScript, Tailwind CSS, Vite, npm
- SQLite and SQLx
- tracing
- No Axum, PostgreSQL, Redis, Docker, or chipset-specific code

### Required Team

- One integration lead
- Two Rust developers
- Two frontend developers
- One local-data developer
- One QA/release engineer

### Required Devices and Laboratory Equipment

No physical device required for this phase.

### Implementation Sequence

1. Create the approved repository structure.
2. Initialize the Cargo workspace and desktop application.
3. Define shared `DeviceSummary`, `OperationRequest`, `OperationEvent`, `FirmwareManifest`, `Job`, and `AuthorizationRecord` contracts.
4. Add SQLite migrations for the minimum local workflow.
5. Add structured sanitized logging.
6. Add formatting, linting, type-checking, and test scripts.
7. Verify a clean build on at least two development machines.

### Repository Impact

#### Inspect First

- Approved Phase 0 evidence
- Any existing repository files discovered during Phase 0

#### Create

- `apps/desktop/`
- `crates/device-core/`
- `crates/workflow-engine/`
- `crates/audit-core/`
- `crates/job-store/`
- `tests/`
- `documentation/`
- Root manifests and ignore rules

#### Populate

- Root `Cargo.toml`
- Root `package.json`
- `README.md`
- Initial SQLx migrations
- Shared data contracts
- Logging initialization

#### Modify

Only files created in this phase or existing files explicitly approved after inspection.

#### Do Not Touch Yet

ADB, Fastboot, USB, firmware, and flashing implementations.

### Tests and Validation

- `cargo fmt --check`
- `cargo clippy --workspace --all-targets`
- `cargo test --workspace`
- `npm run typecheck`
- `npm run lint`
- Tauri development launch

### Deliverables

- Reproducible workspace
- Launching desktop shell
- Shared contracts
- Local schema
- Build instructions

### Required Evidence

- Build outputs
- Tool versions
- Test logs
- Screenshot of the empty shell

### Completion Criteria

Two developers can independently build and launch the same revision.

### Failure Conditions

- Build relies on undocumented local state
- Shared contracts are not frozen
- Secrets appear in source or logs
- Destructive actions are enabled by default

### Risks and Mitigations

- **Risk:** Scaffold conflicts delay integration. **Mitigation:** Integration lead owns root manifests.

### Review Checklist

- [ ] Workspace builds
- [ ] Desktop launches
- [ ] Shared contracts compile
- [ ] SQLite migration applies
- [ ] Logs are sanitized
- [ ] Quality scripts run

### Phase Gate

**Decision owner:** Integration lead.

Stop at this phase gate until build evidence is reviewed and all squads can build the same revision.

---

## 8. Phase 2: Device Discovery and Transport

### Primary Objective

Detect connected devices and maintain stable, unambiguous device sessions.

### Business Outcome

The MVP can reliably show which device is connected and prevent accidental targeting.

### Technical Outcome

udev events, rusb enumeration, serial inventory, VID/PID capture, and mode-transition events.

### Security and Compliance Objective

No device-writing path exists. Ambiguous targets are blocked.

### Duration and Dates

- **Duration:** 80 minutes
- **Date:** 15 August 2026
- **Sprint time:** 01:20-02:40

### Dependencies

Phase 1 shared contracts.

### Critical Path

Hot-plug events, session identity, and target-selection protection.

### Parallel Work

Mock-device fixtures and UI status components.

### In Scope

Read-only enumeration and event tracking.

### Out of Scope

Raw USB protocol implementation and all writes.

### Exclusive Tools and Technologies

- udev
- rusb/libusb
- serialport-rs
- Tokio channels
- No native chipset protocols

### Required Team

Two Rust developers, one frontend developer, and one QA engineer.

### Required Devices and Laboratory Equipment

Two supported test devices, one unsupported device, powered hub, and three known-good cables.

### Implementation Sequence

1. Implement USB enumeration.
2. Implement udev hot-plug observation.
3. Capture VID, PID, bus, port path, and serial where available.
4. Implement serial-port inventory.
5. Create stable session and target-selection logic.
6. Emit connection, disconnection, and mode-change events.
7. Add mock and physical connect/disconnect tests.

### Repository Impact

#### Inspect First

Shared device contracts and desktop event bridge.

#### Create

- `crates/usb-transport/`
- Transport fixtures under `tests/fixtures/usb/`

#### Populate

USB watcher, serial inventory, session tracker, and event models.

#### Modify

Desktop device-status store and Tauri commands.

#### Do Not Touch Yet

Firmware and flashing crates.

### Tests and Validation

- One-device detection
- Multiple-device detection
- Unsupported-device classification
- Ten rapid connect/disconnect cycles per device
- Cable replacement and hub-port movement

### Deliverables

Live device panel and transport event log.

### Required Evidence

Sanitized event logs, device matrix, and test results.

### Completion Criteria

No command-capable target is selected automatically when more than one device is present.

### Failure Conditions

Crashes, stale sessions, ambiguous selection, or lost disconnection events.

### Risks and Mitigations

- **Risk:** udev permissions. **Mitigation:** Diagnose and document; do not silently run the entire app as root.

### Review Checklist

- [ ] Hot-plug works
- [ ] Disconnect works
- [ ] Multiple devices are blocked
- [ ] Unsupported device is labeled
- [ ] Serial inventory is read-only

### Phase Gate

**Decision owner:** Device-engine lead.

Stop at this phase gate until physical event logs and ambiguity-rejection evidence are reviewed.

---

## 9. Phase 3: ADB and Fastboot Diagnostics

### Primary Objective

Provide controlled read-only diagnostics through official ADB and Fastboot executables.

### Business Outcome

Technicians can identify a device and connection state without using a terminal.

### Technical Outcome

Structured process adapters with exact command allowlists, timeouts, cancellation, output parsing, and serial targeting.

### Security and Compliance Objective

Unrestricted shell input is prohibited. Every command identifies one exact device.

### Duration and Dates

- **Duration:** 80 minutes
- **Date:** 15 August 2026
- **Sprint time:** 02:40-04:00

### Dependencies

Stable device selection from Phase 2.

### Critical Path

Safe runner, ADB parser, Fastboot parser, and UI integration.

### Parallel Work

Fixture capture and diagnostic-report presentation.

### In Scope

Read-only properties, state, Fastboot variables, slot information, and supported reboot operations.

### Out of Scope

Arbitrary shell, APK installation, factory reset, unlock, erase, and flash.

### Exclusive Tools and Technologies

- Official `adb` and `fastboot`
- Tokio process control
- Serde structured results
- tracing sanitized logs
- No native ADB/Fastboot replacement

### Required Team

Two Rust developers, one Android systems developer, one frontend developer, and one QA engineer.

### Required Devices and Laboratory Equipment

Authorized ADB device, unauthorized ADB state, Fastboot-capable device, and multiple-device setup.

### Implementation Sequence

1. Implement executable discovery and version checks.
2. Implement serial-bound ADB requests.
3. Parse ADB state and approved properties.
4. Implement serial-bound Fastboot queries.
5. Parse slots, product, bootloader state where reported, and partition variables.
6. Add cancellation, timeout, and one bounded retry for read-only transient failures.
7. Render a diagnostic report.

### Repository Impact

#### Inspect First

Device session API and target-selection behavior.

#### Create

- `crates/adb-adapter/`
- `crates/fastboot-adapter/`
- Protocol fixtures under `tests/fixtures/adb/` and `tests/fixtures/fastboot/`

#### Populate

Command allowlists, parsers, error types, and fixture tests.

#### Modify

Desktop diagnostic panel and operation event stream.

#### Do Not Touch Yet

Write, erase, unlock, and factory-reset commands.

### Tests and Validation

- Authorized, unauthorized, offline, missing executable, timeout, and multiple-device cases
- Fastboot variable parsing with output variations
- Cancellation and process cleanup
- Sensitive-output redaction

### Deliverables

Read-only ADB/Fastboot diagnostics and diagnostic report.

### Required Evidence

Fixture inventory, physical-device screenshots, sanitized logs, and test output.

### Completion Criteria

The UI identifies the approved test devices in ADB and Fastboot without manual terminal commands.

### Failure Conditions

Wrong-device targeting, unrestricted arguments, leaked secrets, or hung processes.

### Risks and Mitigations

- **Risk:** Vendor output differences. **Mitigation:** Preserve raw sanitized output alongside parsed fields and fail closed on ambiguity.

### Review Checklist

- [ ] Exact device serial required
- [ ] Unauthorized ADB handled
- [ ] Fastboot data parsed
- [ ] Cancellation works
- [ ] Timeout works
- [ ] Logs sanitized

### Phase Gate

**Decision owner:** Android systems lead.

Stop at this phase gate until diagnostic evidence is reviewed and all destructive commands remain inaccessible.

---

## 10. Phase 4: Firmware Inspection and Flash Planning

### Primary Objective

Inspect approved firmware and produce a safe, human-readable plan without writing to a device.

### Business Outcome

The technician sees package identity, hashes, images, sizes, targets, and risks before any write is considered.

### Technical Outcome

Sandboxed archive inspection, SHA-256 checksums, image classification, sparse-image detection, manifest generation, and compatibility rules for the tiny approved matrix.

### Security and Compliance Objective

Reject path traversal, malformed archives, checksum mismatches, cross-model packages, and unknown compatibility.

### Duration and Dates

- **Duration:** 90 minutes
- **Date:** 15 August 2026
- **Sprint time:** 04:00-05:30

### Dependencies

Device identity from Phase 3 and approved firmware fixtures from Phase 0.

### Critical Path

Safe extraction, hashing, manifest, compatibility decision, and plan display.

### Parallel Work

Negative fixture creation and UI visualization.

### In Scope

ZIP, TAR, raw IMG, hashes, basic sparse recognition, image-to-partition mapping for approved fixtures, and model/build rules.

### Out of Scope

Universal `payload.bin`, GPT mutation, arbitrary vendor formats, and firmware downloads.

### Exclusive Tools and Technologies

- Rust archive libraries
- SHA-256
- Sandboxed temporary directory
- Serde manifests
- No external firmware repository

### Required Team

Two Rust developers, one firmware specialist, one frontend developer, and one security tester.

### Required Devices and Laboratory Equipment

Physical device metadata from approved devices; no device write required.

### Implementation Sequence

1. Implement size-limited archive listing.
2. Block absolute paths, `..` traversal, symlinks, and expansion limits.
3. Hash package and contained images.
4. Identify raw and sparse Android images.
5. Generate a versioned firmware manifest.
6. Match firmware against the approved device profile.
7. Produce a proposed partition plan and risk report.
8. Reject unknown, mismatched, malformed, and modified packages.

### Repository Impact

#### Inspect First

Approved fixtures, device-profile contracts, and temporary-storage behavior.

#### Create

- `crates/firmware-core/`
- `tests/fixtures/firmware/`

#### Populate

Archive inspector, manifests, hashes, classifiers, compatibility checks, and negative fixtures.

#### Modify

Desktop firmware and flash-plan views.

#### Do Not Touch Yet

Fastboot write adapter and customer-device packages.

### Tests and Validation

- Valid package
- Corrupted ZIP/TAR
- Path traversal
- Oversized expansion
- Truncated image
- Invalid sparse header
- Wrong model
- Checksum mismatch
- Unsupported partition

### Deliverables

Firmware inspector, manifest, risk report, and flash plan.

### Required Evidence

Fixture inventory, manifest samples, rejection test results, and UI screenshots.

### Completion Criteria

No firmware package can reach the write workflow without a valid manifest and exact allowlist match.

### Failure Conditions

Unsafe extraction, unknown package accepted, wrong model accepted, or unchecked image size.

### Risks and Mitigations

- **Risk:** Ninety minutes is insufficient for broad format support. **Mitigation:** Limit support to fixtures for one or two approved devices.

### Review Checklist

- [ ] Hash generated
- [ ] Manifest generated
- [ ] Traversal blocked
- [ ] Wrong model blocked
- [ ] Unknown format blocked
- [ ] Flash plan displayed

### Phase Gate

**Decision owner:** Firmware-engine lead with security reviewer.

Stop at this phase gate. Do not enable a write path until compatibility and hostile-fixture evidence has been reviewed.

---

## 11. Phase 5: Controlled Flashing and Recovery Validation

### Primary Objective

Execute one narrowly allowlisted Fastboot write on dedicated laboratory hardware and verify the result.

### Business Outcome

The team demonstrates the platform's core service workflow without claiming universal support.

### Technical Outcome

Preflight, explicit authorization, exact target binding, write execution, progress events, verification, and recovery documentation.

### Security and Compliance Objective

Only approved laboratory devices, approved firmware hashes, approved partitions, and approved technicians can trigger a write.

### Duration and Dates

- **Duration:** 100 minutes
- **Date:** 15 August 2026
- **Sprint time:** 05:30-07:10

### Dependencies

Phase 4 manifest and compatibility gate. Phase 6 authorization API must be integrated before the physical write demonstration.

### Critical Path

Allowlist enforcement, preflight, write adapter, verification, and recovery test.

### Parallel Work

Report signing, UI progress, and recovery documentation.

### In Scope

One approved Fastboot partition operation, such as a dedicated non-customer test partition or an approved stock image on a recovery-capable lab device.

### Out of Scope

Bootloader bypass, unsupported unlock, account bypass, erase-all, arbitrary partition selection, or customer devices.

### Exclusive Tools and Technologies

- Official Fastboot executable
- Rust allowlisted process adapter
- Workflow engine
- SHA-256 manifest verification
- Ed25519 report signing
- No native chipset protocols

### Required Team

Android systems lead, Rust protocol developer, QA/device technician, security reviewer, and release recorder.

### Required Devices and Laboratory Equipment

At least two dedicated devices of the same supported revision if possible, known-good firmware, powered hub, USB power meter, bench power supply, and recovery instructions.

### Implementation Sequence

1. Bind operation to exact job, technician, device serial, firmware hash, and partition.
2. Run battery, cable, mode, model, bootloader, partition-size, and firmware preflight checks where exposed.
3. Require explicit destructive-operation approval.
4. Execute only the predetermined Fastboot command template.
5. Stream progress and capture sanitized output.
6. Verify post-write state.
7. Generate signed operation report.
8. Run one controlled cable-loss test only on recovery-capable lab hardware.
9. Document recovery outcome.

### Repository Impact

#### Inspect First

Fastboot adapter, firmware manifest, workflow contracts, authorization record, and approved matrix.

#### Create

- Hardware test records under `tests/hardware-in-loop/`
- Recovery evidence under `documentation/evidence/phase-5/`

#### Populate

Allowlist, preflight policy, write workflow, verification routine, and recovery record.

#### Modify

Fastboot adapter, workflow engine, desktop operation panel, audit core, and report generator.

#### Do Not Touch Yet

MTK, Qualcomm, Samsung, UniSoc, account-lock, carrier-lock, and identity functions.

### Tests and Validation

- Missing job rejected
- Missing authorization rejected
- Wrong technician rejected
- Wrong device rejected
- Wrong firmware hash rejected
- Wrong partition rejected
- Multiple-device ambiguity rejected
- Cable interruption recovery documented
- Successful post-write verification

### Deliverables

Controlled operation, signed report, test record, and recovery procedure.

### Required Evidence

Video or screenshots, timestamps, hashes, sanitized logs, signed report, and physical-device disposition.

### Completion Criteria

One allowlisted operation succeeds and all negative authorization/compatibility tests fail closed.

### Failure Conditions

Any cross-device targeting, uncontrolled argument, unverified package, missing authorization, unrecoverable test device, or false success status.

### Risks and Mitigations

- **Risk:** Physical failure consumes the sprint. **Mitigation:** Use a known recovery-capable device and keep a second matching unit.
- **Risk:** Cable-loss test is unsafe under the schedule. **Mitigation:** Perform only if recovery preparation and a safe interruption point are approved; otherwise mark the MVP write feature incomplete.

### Review Checklist

- [ ] Exact allowlist enforced
- [ ] Job and authorization required
- [ ] Firmware hash verified
- [ ] Partition size checked
- [ ] Progress captured
- [ ] Result verified
- [ ] Signed report generated
- [ ] Recovery documented

### Phase Gate

**Decision owner:** Technical lead and QA/device lead jointly.

Stop at this phase gate if any physical or authorization test fails. Do not proceed to the internal pilot with a device-changing demonstration until recovery and verification evidence is accepted.

---

## 12. Phase 6: Minimum Workshop Authorization and Audit Layer

### Primary Objective

Require customer authorization, proof of ownership, technician identity, and job linkage for device-changing operations.

### Business Outcome

The platform demonstrates a responsible workshop workflow rather than an unrestricted device tool.

### Technical Outcome

SQLite-backed customers, devices, jobs, authorizations, operations, chained audit records, and signed reports.

### Security and Compliance Objective

Sensitive operations fail closed when authorization data is absent or invalid.

### Duration and Dates

- **Duration:** 90 minutes, partially parallel
- **Date:** 15 August 2026
- **Sprint time:** 06:00-07:30

### Dependencies

Phase 1 schema and Phase 5 operation contract.

### Critical Path

Authorization gate and operation-to-job linkage.

### Parallel Work

UI forms, database implementation, and signature logic.

### In Scope

Minimum local records and report export.

### Out of Scope

Billing, subscriptions, cloud identity, reseller management, and customer credential storage.

### Exclusive Tools and Technologies

- SQLite
- SQLx
- Ed25519
- SHA-256 hash chaining
- No PostgreSQL or cloud identity

### Required Team

One Rust/data developer, one frontend developer, one security reviewer, and one QA engineer.

### Required Devices and Laboratory Equipment

None beyond the test devices used in Phase 5.

### Implementation Sequence

1. Add customer, device, technician, job, authorization, operation, and audit tables.
2. Create minimal intake and authorization forms.
3. Link every operation request to one job and technician.
4. Block writes when authorization fields are missing.
5. Chain audit records using previous-record hashes.
6. Sign the final operation report.
7. Test tampering and missing-record cases.

### Repository Impact

#### Inspect First

Phase 1 migrations, workflow contracts, and Phase 5 operation request.

#### Create

Additional SQLx migrations and report templates.

#### Populate

Job store, authorization gate, audit chain, and report signer.

#### Modify

Desktop job view, workflow engine, audit core, and operation controls.

#### Do Not Touch Yet

Cloud accounts, billing, and customer credentials.

### Tests and Validation

- Missing job
- Missing proof of ownership
- Missing repair authorization
- Missing technician
- Audit-record modification
- Invalid report signature
- Log redaction

### Deliverables

Local workshop workflow and signed report.

### Required Evidence

Database migration output, negative tests, sample authorized job, and signed report verification.

### Completion Criteria

A device write cannot be requested without a complete authorized job.

### Failure Conditions

Bypassable authorization, mutable audit history without detection, signing-key leakage, or customer secrets in logs.

### Risks and Mitigations

- **Risk:** Intake UI consumes integration time. **Mitigation:** Use a minimal form with enforceable required fields.

### Review Checklist

- [ ] Job required
- [ ] Proof of ownership required
- [ ] Authorization required
- [ ] Technician required
- [ ] Audit chain verified
- [ ] Report signature verified

### Phase Gate

**Decision owner:** Security/compliance reviewer.

Stop at this phase gate until every missing-authorization test is proven to fail closed.

---

## 13. MVP Release Candidate and Internal Workshop Pilot

### Primary Objective

Integrate the vertical workflow, run the scripted demonstration, document limitations, and make an explicit acceptance decision.

### Business Outcome

Stakeholders receive a verifiable engineering alpha instead of unsupported universal claims.

### Technical Outcome

One tagged Linux build, reproducible instructions, demonstration script, test report, and known-limitations document.

### Security and Compliance Objective

Confirm no prohibited function, unrestricted terminal, hidden write path, customer secret, or unsupported support claim exists.

### Duration and Dates

- **Duration:** 150 minutes
- **Date:** 15 August 2026
- **Sprint time:** 07:30-10:00

### Dependencies

All prior phase gates passed.

### Critical Path

Integration, negative tests, physical demonstration, report verification, and acceptance review.

### Parallel Work

Release documentation, screenshots, test execution, and packaging.

### In Scope

Internal installation, demonstration, known limitations, supported matrix, and go/no-go decision.

### Out of Scope

Public release and customer-device use.

### Exclusive Tools and Technologies

- Existing fixed MVP stack only
- Local build and release tools
- No new framework or protocol introduced during stabilization

### Required Team

All component leads, QA, security reviewer, release coordinator, and one technician acting as the pilot user.

### Required Devices and Laboratory Equipment

Approved device set, unsupported rejection device, known-good cables, powered hub, power meter, recovery equipment, and external evidence storage.

### Implementation Sequence

1. Merge only phase-gated revisions.
2. Run complete automated test suite.
3. Run negative security and firmware tests.
4. Build the Linux release candidate.
5. Execute the scripted end-to-end workflow.
6. Verify signed report and audit chain.
7. Test unsupported-device rejection.
8. Record known limitations and failures.
9. Make a documented accept, conditionally accept, or reject decision.

### Repository Impact

#### Inspect First

All merged revisions, manifests, migrations, fixtures, and evidence.

#### Create

- `documentation/release/mvp-supported-matrix.md`
- `documentation/release/mvp-known-limitations.md`
- `documentation/release/mvp-demo-script.md`
- `documentation/release/mvp-test-report.md`
- `documentation/release/mvp-acceptance-decision.md`

#### Populate

Release and evidence documents with actual verified results only.

#### Modify

README build and run instructions, version metadata, and defects found during integration.

#### Do Not Touch Yet

All deferred chipset and cloud modules.

### Tests and Validation

- Full unit and integration suite
- Protocol replay
- Firmware negative fixtures
- Device connect/disconnect
- Multiple-device rejection
- Unauthorized operation rejection
- Approved controlled operation
- Signed report verification
- Audit-tampering detection
- Unsupported-device rejection

### Deliverables

- Linux engineering-alpha build
- Demo script
- Supported and unsupported matrix
- Test report
- Known limitations
- Acceptance decision

### Required Evidence

Build logs, test logs, screenshots, physical test record, signed report, and decision record.

### Completion Criteria

The MVP is complete only when the end-to-end workflow succeeds on the approved matrix, negative controls fail closed, and the acceptance decision is documented.

### Failure Conditions

Crash, wrong-device targeting, authorization bypass, unsupported firmware acceptance, false completion, missing evidence, or unrecoverable device failure.

### Risks and Mitigations

- **Risk:** Late integration failure. **Mitigation:** Freeze features at Hour 7:30 and fix only blockers.
- **Risk:** Demo succeeds once but is not repeatable. **Mitigation:** Require two consecutive full demonstrations.

### Review Checklist

- [ ] Build reproduced
- [ ] Automated tests pass
- [ ] Negative tests pass
- [ ] Two end-to-end demonstrations pass
- [ ] Signed report verifies
- [ ] Audit chain verifies
- [ ] Known limitations recorded
- [ ] Acceptance decision signed

### Phase Gate

**Decision owner:** Technical lead, QA lead, and security/compliance reviewer jointly.

Stop after the MVP acceptance decision. Do not begin post-MVP expansion until the evidence is reviewed and a separate next-phase plan is explicitly authorized.

---

## 14. Cross-Phase File and Directory Change Index

| Path | Type | Responsibility | First phase | Later use |
|---|---|---|---|---|
| `/home/trovas/labs/android-service-platform` | Directory | Project root | Phase 1 | All phases |
| `Cargo.toml` | File | Rust workspace | Phase 1 | Updated as approved crates enter |
| `package.json` | File | Frontend scripts and dependencies | Phase 1 | UI integration |
| `README.md` | File | Build, run, safety, limitations | Phase 1 | Finalized in release candidate |
| `apps/desktop` | Directory | Tauri and React application | Phase 1 | All UI phases |
| `crates/device-core` | Directory | Shared device/session contracts | Phase 1 | Phases 2-5 |
| `crates/usb-transport` | Directory | USB and hot-plug discovery | Phase 2 | Release testing |
| `crates/adb-adapter` | Directory | Controlled ADB diagnostics | Phase 3 | Release testing |
| `crates/fastboot-adapter` | Directory | Fastboot diagnostics and one allowlisted operation | Phase 3 | Phase 5 |
| `crates/firmware-core` | Directory | Firmware inspection and plans | Phase 4 | Phase 5 |
| `crates/workflow-engine` | Directory | Phase-gated operation enforcement | Phase 1 | Phases 3-6 |
| `crates/audit-core` | Directory | Audit chain and report signing | Phase 1 | Phases 5-6 |
| `crates/job-store` | Directory | SQLite job and authorization records | Phase 1 | Phase 6 |
| `tests/fixtures` | Directory | Sanitized protocol and firmware fixtures | Phase 2 | All test phases |
| `tests/integration` | Directory | Cross-component tests | Phase 1 | Release candidate |
| `tests/hardware-in-loop` | Directory | Physical test records and harness | Phase 5 | Release candidate |
| `documentation/evidence` | Directory | Phase evidence without customer secrets | Phase 1 | All gates |
| `documentation/release` | Directory | MVP release documents | Release candidate | Acceptance |

---

## 15. Cross-Phase Test Matrix

### Unit tests

- Command argument construction
- Output parsers
- Device-session transitions
- Firmware hashing
- Archive path validation
- Manifest generation
- Compatibility decisions
- Authorization rules
- Audit chaining
- Signature verification

### Integration tests

- Desktop-to-Tauri event flow
- Tauri-to-Rust command flow
- Device session to ADB/Fastboot adapter
- Firmware manifest to flash-plan workflow
- Job authorization to operation gate
- Operation result to audit and report

### Protocol replay tests

- Authorized ADB
- Unauthorized ADB
- ADB offline
- Fastboot variable variants
- Missing tools
- Timeouts
- Malformed output

### Firmware fixture tests

- Valid approved package
- Corrupt archive
- Path traversal
- Expansion limit
- Truncated image
- Invalid sparse image
- Wrong model
- Wrong hash
- Unsupported partition

### Hardware-in-the-loop tests

- Connect and disconnect
- Reconnect
- ADB-to-Fastboot transition
- Multiple-device protection
- Unsupported-device rejection
- One allowlisted controlled write
- Post-write verification
- Controlled cable interruption only with approved recovery preparation

### Security tests

- Missing job rejected
- Missing owner authorization rejected
- Missing technician rejected
- Wrong device rejected
- Wrong firmware rejected
- Audit tampering detected
- Report modification detected
- Secrets absent from logs

---

## 16. Security, Legal, and Data-Handling Controls

- Only owned or explicitly authorized laboratory devices may be used.
- Device-changing operations require an authorized local job.
- The application must not store customer account credentials.
- Logs must redact tokens, credentials, and prohibited device data.
- The MVP must not change IMEI, MEID, serial numbers, or equivalent identifiers.
- The MVP must not bypass account protection or carrier controls.
- Only official ADB and Fastboot binaries may be used.
- Firmware must have a documented lawful source and exact hash.
- Signing keys must be generated outside source control and stored with restrictive permissions.
- The application must fail closed when compatibility or authorization is unknown.
- Support claims must name the exact tested model, revision, Android build, and operation.

---

## 17. Risks, Dependencies, and Contingencies

### Critical risks

1. **Toolchain missing:** The ten-hour clock should not be spent on major workstation repair. Use a prepared development machine or adjust the acceptance target.
2. **Tauri dependency failure:** Keep the Rust engine independently testable; use a minimal UI rather than changing frameworks mid-sprint.
3. **Device permission problems:** Diagnose udev rules explicitly. Do not run the entire desktop application as root.
4. **Firmware complexity:** Support only preapproved fixtures for one or two devices.
5. **Physical flashing failure:** Use dedicated recovery-capable devices and maintain a known recovery path.
6. **Late feature requests:** Freeze scope after Phase 0.
7. **Integration conflicts:** One integration lead owns root manifests and release branches.
8. **False universality:** Label the result an engineering alpha with an exact support matrix.

### Schedule contingency

If Phase 5 cannot be validated safely, ship the Hour 10 build as a **read-only diagnostics and firmware-planning MVP**. Do not fake flashing support or bypass the phase gate.

---

## 18. MVP Definition of Done

The ten-hour MVP is complete only when all applicable items below are verified:

- [ ] Repository was created only after read-only inspection approval
- [ ] Linux build is reproducible
- [ ] Device discovery handles connect, disconnect, and reconnect
- [ ] Multiple connected devices cannot cause ambiguous targeting
- [ ] ADB authorization states are shown correctly
- [ ] Read-only ADB diagnostics work without manual terminal intervention
- [ ] Read-only Fastboot diagnostics work without manual terminal intervention
- [ ] Firmware inspection does not write to a device
- [ ] Firmware SHA-256 is recorded
- [ ] Hostile archive fixtures are rejected
- [ ] Wrong-model and wrong-hash firmware are rejected
- [ ] Every proposed write is displayed before execution
- [ ] Controlled flashing is restricted to the approved matrix
- [ ] Preflight runs before the write
- [ ] Post-write verification runs after the write
- [ ] Recovery evidence exists for the tested failure condition
- [ ] Device-changing operation requires job, technician, ownership, and authorization records
- [ ] Operation report is signed
- [ ] Audit tampering is detectable
- [ ] Logs contain no customer credentials
- [ ] Supported and unsupported lists are documented
- [ ] Known limitations are documented
- [ ] Two consecutive demonstration runs succeed
- [ ] Acceptance decision is documented

---

## 19. Deferred Until After MVP

### First stabilization sprint: next 3 to 7 days

- Expand automated tests
- Improve USB mode correlation
- Harden firmware parser
- Add CI
- Improve packaging
- Expand exact Fastboot support matrix
- Conduct longer interruption and recovery tests

### Workshop beta: next 2 to 4 weeks

- More physical devices and firmware revisions
- Improved customer and technician workflow
- Better report export
- Local role-based permissions
- Signed plugin foundation
- Controlled internal workshop pilot

### Native chipset research: months, not hours

- Authorized MediaTek support
- Authorized Qualcomm support
- Samsung stock-flashing interoperability
- UniSoc support
- Windows production adapters
- Vendor partnerships and lawful loader access

---

## 20. Immediate Next Action

The immediate action is **Phase 0 inspection only**. Do not create the repository, initialize Git, install dependencies, or modify files until the output is reviewed.

Run this read-only inspection from the exact parent directory:

```bash
cd /home/trovas/labs
printf '%s
' '--- CURRENT DIRECTORY ---'
pwd
printf '%s
' '--- FIRST AND SECOND LEVEL CONTENTS ---'
find /home/trovas/labs -mindepth 1 -maxdepth 2 -printf '%y %p
' | sort
printf '%s
' '--- PLANNED PROJECT ROOT ---'
if [ -e /home/trovas/labs/android-service-platform ]; then
  printf '%s
' 'EXISTS'
  find /home/trovas/labs/android-service-platform -mindepth 1 -maxdepth 2 -printf '%y %p
' | sort
else
  printf '%s
' 'MISSING'
fi
printf '%s
' '--- GIT ---'
command -v git
git --version
printf '%s
' '--- RUST ---'
command -v rustc
rustc --version
command -v cargo
cargo --version
printf '%s
' '--- NODE AND NPM ---'
command -v node
node --version
command -v npm
npm --version
printf '%s
' '--- ANDROID PLATFORM TOOLS ---'
command -v adb
adb version
command -v fastboot
fastboot --version
printf '%s
' '--- LIBUSB, UDEV, SQLITE, AND TAURI-RELATED PACKAGES ---'
dpkg-query -W -f='${binary:Package}	${Version}
' libusb-1.0-0-dev libudev-dev libsqlite3-dev pkg-config build-essential curl wget file libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev 2>/dev/null
printf '%s
' '--- DOCKER ---'
command -v docker
docker --version
docker compose version
```

Collect the output and review:

1. Existing directory conflicts
2. Existing repository state
3. Missing toolchain components
4. Installed package versions
5. The exact physical test-device matrix
6. Approved firmware fixtures
7. Team ownership
8. The go/no-go decision for repository creation

**Stop implementation at the Phase 0 gate. Do not create or modify `/home/trovas/labs/android-service-platform` until the inspection output has been reviewed and repository creation has been explicitly authorized.**
