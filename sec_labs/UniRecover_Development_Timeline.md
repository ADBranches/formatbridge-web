# UniRecover — Universal Mobile Device Image Recovery Framework
## Full Development Timeline & Technical Specification
### Law Enforcement Edition | Government Funding Proposal

---

## Executive Summary

UniRecover is a cross-platform forensic image recovery framework purpose-built for law enforcement agencies and accredited digital forensics laboratories. It recovers deleted photographs and videos from modern iOS and Android smartphones, producing court-admissible evidence with full chain-of-custody integrity.

The tool addresses a critical operational gap: existing commercial forensic tools (Cellebrite UFED, Oxygen Forensic, Magnet AXIOM) are expensive, closed-source, and lag behind OS releases. UniRecover is open-architecture, auditable, and designed to be maintained and extended by government agencies themselves.

**Target users:** Digital forensics units, cybercrime bureaus, national law enforcement agencies  
**Tech stack:** Rust (core engine) · Python (plugin system) · React (web UI)  
**Development cycle:** 16 weeks  
**Deployment:** On-premises (air-gapped support), Docker, Kubernetes  

---

## Project Objectives

1. Recover deleted images and videos from iOS (APFS/encrypted) and Android (EXT4/F2FS/FBE) devices
2. Maintain full forensic integrity — hash verification, write-blocking, chain-of-custody logging
3. Achieve 10+ GB/s file carving throughput via SIMD acceleration
4. Handle modern device encryption (iOS Data Protection classes, Android FBE/FDE)
5. Provide a plugin SDK for agency-specific device profiles and proprietary databases
6. Deliver a court-ready evidence export pipeline (DFXML, E01, case reports)
7. Support air-gapped, on-premises deployment with no external dependencies
8. Pass Daubert/Frye admissibility standards — validated against known test corpora

---

## Repository Structure

```
unirecover/
├── Cargo.toml                         # Rust workspace
├── pyproject.toml                     # Python bindings (maturin)
├── docker-compose.yml                 # Dev environment
├── docker-compose.prod.yml            # Production deployment
├── Makefile
├── README.md
├── CHAIN_OF_CUSTODY.md                # CoC policy documentation
├── LEGAL_NOTICE.md                    # Authorized use policy
├── docs/
│   ├── architecture.md
│   ├── api_reference.md
│   ├── court_admissibility.md
│   ├── validation_report.md
│   └── recovery_guides/
│       ├── android_recovery.md
│       └── ios_recovery.md
├── crates/
│   ├── unirecover-core/               # Core engine
│   ├── unirecover-cli/                # CLI interface
│   ├── unirecover-server/             # REST API server
│   ├── unirecover-acquisition/        # Device acquisition layer
│   ├── unirecover-fs/                 # Filesystem parsers
│   ├── unirecover-carving/            # File carving engine
│   ├── unirecover-crypto/             # Encryption handling
│   ├── unirecover-audit/              # Audit log & CoC engine
│   ├── unirecover-export/             # Evidence export (DFXML, PDF)
│   └── unirecover-ffi/                # Python FFI bindings
├── plugins/
│   ├── base_plugin.py
│   ├── android_plugins/
│   └── ios_plugins/
├── web-ui/                            # React frontend
├── tests/
│   ├── test_images/                   # Reference test corpora
│   ├── validation/                    # NIST/CFTT validation suite
│   └── fixtures/
└── scripts/
    ├── setup_dev_env.sh
    ├── build_release.sh
    ├── run_validation.sh
    └── generate_case_report.sh
```

---

## Phase 1 — Foundation & Infrastructure (Weeks 1–2)

### Week 1: Project Setup, Core Architecture & Audit Framework

#### Day 1–2: Repository, CI/CD & Audit Core

**Files to create:**
```
Cargo.toml
crates/unirecover-core/Cargo.toml
crates/unirecover-core/src/lib.rs
crates/unirecover-core/src/error.rs
crates/unirecover-audit/Cargo.toml
crates/unirecover-audit/src/lib.rs
crates/unirecover-audit/src/log.rs          # Append-only audit log
crates/unirecover-audit/src/chain.rs        # Chain-of-custody ledger
crates/unirecover-audit/src/operator.rs     # Operator identity & auth
.github/workflows/ci.yml
.github/workflows/release.yml
rust-toolchain.toml
LEGAL_NOTICE.md
```

**Objectives:**
- Initialize Rust workspace with all crate stubs
- Set up GitHub Actions with cross-compilation matrix (x86_64, aarch64, musl)
- Implement core error types: `AcquisitionError`, `FSError`, `CarvingError`, `AuditError`
- **CRITICAL — Audit log:** Append-only, HMAC-SHA256-chained log entries. Every operation (device connection, read, export) writes a tamper-evident entry. Log cannot be deleted or modified without breaking the chain.
- Operator authentication: badge/certificate-based login before any device can be accessed
- Case creation: every session is tagged to a case number, investigator ID, and authorizing supervisor
- Set up `tracing` subscriber with structured JSON output piped into the audit log
- Write-blocker enforcement: all acquisition sources default to read-only; write access requires explicit supervisor override with logged justification

#### Day 3–4: Acquisition Layer — Block Device Access

**Files to create:**
```
crates/unirecover-acquisition/Cargo.toml
crates/unirecover-acquisition/src/lib.rs
crates/unirecover-acquisition/src/sources/
├── mod.rs
├── block_device.rs       # Linux block device reader
├── disk_image.rs         # DD/E01/AFF4 image reader
├── memory.rs             # In-memory buffer
└── traits.rs             # AcquisitionSource trait
crates/unirecover-acquisition/src/linux/
├── udev.rs               # Device enumeration via udev
└── sysfs.rs              # Sysfs device info
crates/unirecover-acquisition/src/write_blocker.rs
crates/unirecover-acquisition/src/hasher.rs     # SHA-256/MD5 dual hash
```

**Objectives:**
- `AcquisitionSource` trait: `read()`, `size()`, `block_size()`, `hash()`, `verify()`
- `BlockDeviceReader`: Direct I/O with `O_DIRECT` and hardware write-block enforcement
- `DiskImageReader`: Memory-mapped file access via `memmap2` for DD/E01/AFF4 images
- **Forensic hash:** Dual SHA-256 + MD5 computed during acquisition (matches legacy tool expectations); hash logged to audit chain before any processing begins
- Software write-blocker: intercept and deny any write syscall to acquisition source; log attempt if write is tried
- Benchmark: >500 MB/s sequential read on NVMe
- Unit tests with mock block device (`/dev/loop0`)

#### Day 5–7: Memory-Mapped I/O, Async Layer & Evidence Integrity

**Files to create:**
```
crates/unirecover-acquisition/src/async_io.rs
crates/unirecover-acquisition/src/chunked_reader.rs
crates/unirecover-acquisition/src/mmap_pool.rs
crates/unirecover-acquisition/src/integrity.rs    # Sector-level hash verification
crates/unirecover-acquisition/benches/
├── read_benchmark.rs
└── mmap_benchmark.rs
```

**Objectives:**
- `ChunkedReader` for large images (>1TB) with per-chunk hash verification
- `MmapPool` for memory-mapped region management
- Async I/O using `tokio::fs` with io_uring (Linux 5.1+)
- Sector-level integrity verification: flag bad sectors, log them, continue acquisition
- Acquisition report: auto-generated after every image acquisition (device info, hash values, sector errors, operator ID, timestamp)
- Target: 1 GB/s sequential read on modern NVMe

---

### Week 2: Platform Detection & Device Communication

#### Day 1–3: Android Device Interface

**Files to create:**
```
crates/unirecover-acquisition/src/android/
├── mod.rs
├── adb.rs                    # ADB protocol (USB + TCP)
├── fastboot.rs               # Fastboot mode support
├── partition_table.rs        # GPT/MBR parser
├── device_info.rs            # Device fingerprinting
└── root_check.rs             # Root/su access detection
crates/unirecover-acquisition/tests/
├── mock_adb_device.rs
└── test_adb_protocol.rs
```

**Objectives:**
- ADB protocol over USB and TCP/IP transport
- Device enumeration: serial number, manufacturer, model, Android version, build fingerprint
- Root detection via `su -c id`; log root status to audit chain
- Partition table extraction via `adb shell gdisk -l`; log all detected partitions
- All ADB commands logged to audit chain with timestamps
- Test against Android emulator images

#### Day 4–6: iOS Device Interface

**Files to create:**
```
crates/unirecover-acquisition/src/ios/
├── mod.rs
├── lockdown.rs               # Lockdown protocol (usbmuxd)
├── afc.rs                    # Apple File Conduit
├── mobile_device.rs          # MobileDevice framework bindings
├── developer_disk.rs         # Developer disk image mount
└── jailbreak.rs              # Jailbreak detection & SSH
crates/unirecover-acquisition/src/ios/ffi/
├── mod.rs
└── mobile_device_sys.rs      # Raw FFI bindings
build.rs                      # Link MobileDevice.framework / libimobiledevice
```

**Objectives:**
- FFI bindings to `MobileDevice.framework` (macOS host)
- Linux: Link `libimobiledevice` via `pkg-config`
- AFC protocol for file-level access
- Developer disk image mount for filesystem access
- Jailbreak detection (checkra1n, unc0ver, palera1n); log status to audit chain
- Device trust pairing certificate logged with case record

#### Day 7: Cross-Platform Abstraction & Device Registry

**Files to create:**
```
crates/unirecover-acquisition/src/platform.rs
crates/unirecover-acquisition/src/device_enum.rs
crates/unirecover-acquisition/src/device_registry.rs   # Centralized device DB
```

**Objectives:**
- Unified `DeviceInfo` struct (platform, OS version, IMEI/serial, storage size, encryption state)
- USB vendor ID database for automatic device identification
- Device registry: log every connected device to the case record
- Platform detection via compile-time feature flags
- Mock device for CI testing

---

## Phase 2 — Filesystem Parsing Engine (Weeks 3–5)

### Week 3: APFS Parser (iOS)

#### Day 1–3: APFS Container Superblock

**Files to create:**
```
crates/unirecover-fs/Cargo.toml
crates/unirecover-fs/src/lib.rs
crates/unirecover-fs/src/apfs/
├── mod.rs
├── container.rs              # Container superblock
├── nx_superblock.rs          # NXSB structure
├── checkpoint.rs             # Checkpoint descriptor area
├── object_map.rs             # Object map B-tree
├── spaceman.rs               # Space manager
└── constants.rs              # Magic numbers, flags
crates/unirecover-fs/tests/
├── apfs_test_images/
│   └── create_test_apfs.sh
└── test_apfs_container.rs
```

**Objectives:**
- Parse NXSB at offset 32: block size, total blocks, features, incompatible flags
- Read checkpoint descriptor area; find latest valid checkpoint
- Validate against real APFS images (macOS disk utility output)
- Log parsed container metadata to audit chain
- Fuzz testing: verify parser does not panic on malformed input

#### Day 4–5: APFS B-Tree Implementation

**Files to create:**
```
crates/unirecover-fs/src/apfs/btree/
├── mod.rs
├── node.rs                   # B-tree node structures
├── fixed_size_keys.rs
├── variable_size_keys.rs
├── traversal.rs
└── iterator.rs
```

**Objectives:**
- Generic B-tree node parsing (fixed and variable-size keys)
- Tree traversal for object map lookups
- Copy-on-Write node versioning — older nodes may contain deleted file references
- Fuzz testing with arbitrary bit flips to validate robustness

#### Day 6–7: APFS Volume & Deleted File Recovery

**Files to create:**
```
crates/unirecover-fs/src/apfs/volume.rs
crates/unirecover-fs/src/apfs/inode.rs
crates/unirecover-fs/src/apfs/extent.rs
crates/unirecover-fs/src/apfs/recovery.rs
crates/unirecover-fs/src/apfs/encryption.rs
crates/unirecover-fs/tests/test_apfs_recovery.rs
```

**Objectives:**
- Parse APFS volume superblock (APSB)
- Inode structure parsing (`j_inode_val_t`): name, size, timestamps, extended attributes
- Extent tree traversal for file block locations
- **Deleted file recovery:** Scan orphaned B-tree nodes from CoW snapshots for unlinked inodes
- Recover deleted inodes with original filenames, timestamps, and partial metadata where available
- Log every recovered file candidate to the results database with confidence score

---

### Week 4: EXT4 & F2FS Parsers (Android)

#### Day 1–3: EXT4 Implementation

**Files to create:**
```
crates/unirecover-fs/src/ext4/
├── mod.rs
├── superblock.rs
├── group_descriptor.rs
├── inode.rs
├── extent_tree.rs
├── directory.rs
├── journal.rs               # JBD2 journal recovery
└── recovery.rs
crates/unirecover-fs/tests/
├── ext4_test_images/
└── test_ext4.rs
```

**Objectives:**
- Parse superblock (magic 0xEF53, offset 1024)
- Block group descriptor table traversal
- Extent tree traversal (up to 5 levels)
- Journal (JBD2) replay for recently committed writes — recovers files deleted after last commit
- Orphan list recovery: inodes unlinked but not yet zeroed
- Test against Android `userdata` partition dumps from known-good reference images

#### Day 4–6: F2FS Implementation

**Files to create:**
```
crates/unirecover-fs/src/f2fs/
├── mod.rs
├── superblock.rs
├── checkpoint.rs
├── nat.rs                   # Node Address Table
├── sit.rs                   # Segment Information Table
├── segment.rs
├── node.rs
└── recovery.rs
crates/unirecover-fs/tests/test_f2fs.rs
```

**Objectives:**
- Parse F2FS superblock (magic 0xF2F52010); two copies for redundancy
- NAT traversal, SIT for locating invalid/stale segments
- **Key technique:** Garbage collection victim segments retain old data until overwritten — scan these for recoverable file content
- Handle F2FS inline compression (LZO/LZ4/ZSTD)
- Log recovered segment candidates with offset, size, and confidence

#### Day 7: Filesystem Abstraction Layer

**Files to create:**
```
crates/unirecover-fs/src/traits.rs
crates/unirecover-fs/src/fs_detect.rs
crates/unirecover-fs/src/block_iter.rs
```

**Objectives:**
- `FSParser` trait: `parse()`, `list_files()`, `get_deleted()`, `get_unallocated()`
- Filesystem auto-detection via magic bytes
- Unified `BlockIterator` for all FS types, feeding into the carving pipeline
- Plugin registration for custom filesystem parsers

---

### Week 5: Advanced Recovery — Databases, Thumbnails & Memory

#### Day 1–3: SQLite Database Recovery (MediaStore & Photos.sqlite)

**Files to create:**
```
crates/unirecover-fs/src/sqlite/
├── mod.rs
├── wal_recovery.rs
├── freelist_carving.rs
├── cell_parser.rs
└── mediastore_parser.rs
crates/unirecover-fs/tests/test_sqlite_recovery.rs
```

**Objectives:**
- Parse SQLite WAL (Write-Ahead Log) for recently deleted records
- Freelist page carving: deleted records persist in freelist pages until overwritten
- Extract image metadata from Android `external.db` (MediaStore): original filename, path, date added, GPS coordinates, dimensions
- iOS: Parse `Photos.sqlite` for deleted photo records including album membership and edit history
- Reconstruct file paths for deleted images to correlate with carving results

#### Day 4–5: Thumbnail Cache Recovery

**Files to create:**
```
crates/unirecover-fs/src/thumbnail/
├── mod.rs
├── android_thumbnails.rs
├── ios_thumbnails.rs
└── cache_parser.rs
```

**Objectives:**
- Android: Parse `DCIM/.thumbnails/` and `.thumbdata3` binary files (JPEG thumbnail store)
- iOS: Parse `PhotoData/Thumbnails/` from Camera Roll backup structures
- Match recovered thumbnails to deleted originals via embedded metadata (file ID, original path)
- Export thumbnails as standalone evidence items with provenance metadata

#### Day 6–7: Live Memory Analysis (Authorized Root Access)

**Files to create:**
```
crates/unirecover-acquisition/src/memory/
├── mod.rs
├── memdump.rs
├── process_scanner.rs
└── key_extraction.rs
crates/unirecover-crypto/src/memory_scanner.rs
```

**Objectives:**
- Access `/proc/<pid>/mem` on rooted Android devices (requires explicit case authorization)
- Scan for AES key schedules and encryption key material in running Gallery/Photos app process memory
- Authorization gate: memory analysis requires supervisor-level case authorization; logged to audit chain
- Volatility-compatible signatures for key material identification
- Extracted key material stored encrypted, access-controlled, and logged

---

## Phase 3 — File Carving Engine (Weeks 6–7)

### Week 6: SIMD-Accelerated Signature Scanning

#### Day 1–3: SIMD Core Implementation

**Files to create:**
```
crates/unirecover-carving/Cargo.toml
crates/unirecover-carving/src/lib.rs
crates/unirecover-carving/src/simd/
├── mod.rs
├── avx2_engine.rs            # AVX2 256-bit pattern matching
├── avx512_engine.rs          # AVX-512 (server workstations)
├── neon_engine.rs            # ARM NEON (mobile-native recovery)
├── wasm_engine.rs            # WASM SIMD (browser preview)
└── runtime_detect.rs         # CPU feature detection at runtime
crates/unirecover-carving/benches/
├── simd_benchmark.rs
└── comparison_scalar.rs
```

**Objectives:**
- Runtime CPU feature detection via `cpuid`
- AVX2: 32-byte parallel header/footer pattern matching
- AVX-512: 64-byte operations for server-grade workstations
- ARM NEON: Native recovery on ARM forensic hardware
- WASM SIMD: Browser-side preview carving in the web UI
- Target throughput: 10 GB/s on modern server CPU

#### Day 4–5: Image Format Signature Database

**Files to create:**
```
crates/unirecover-carving/src/signatures/
├── mod.rs
├── database.rs
├── jpeg.rs
├── heif.rs
├── png.rs
├── gif.rs
├── webp.rs
├── mp4.rs
├── raw.rs
└── signatures.yaml           # Extensible signature definitions
```

**Objectives:**
- 50+ image and video format signatures
- JPEG: SOI (FFD8) to EOI (FFD9); entropy-validated between markers
- HEIC/HEIF: `ftyp` box validation, `mdat` extraction
- PNG: IHDR/IDAT/IEND chunk CRC validation
- Camera RAW: CR2, NEF, ARW, DNG, ORF, RW2
- MP4/MOV: Atom tree walking, `moov`/`mdat` extraction
- Entropy filtering: high-entropy blocks flagged as potentially encrypted (logged, not discarded)
- Confidence scoring: 0.0–1.0 per recovered candidate based on structural validity

#### Day 6–7: Fragmented File Reconstruction

**Files to create:**
```
crates/unirecover-carving/src/reassembly/
├── mod.rs
├── bifragment_gap_carving.rs
├── smart_reassembly.rs
├── pixel_continuity.rs
└── ml_reassembly.rs          # Optional ML-assisted reassembly
crates/unirecover-carving/tests/
├── test_fragmented_jpeg.rs
└── fragmented_test_images/
```

**Objectives:**
- Bifragment gap carving: validate JPEG restart markers across fragment boundaries
- Smart reassembly: use filesystem metadata hints (block allocation maps) to guide fragment ordering
- Pixel continuity analysis: validate image row continuity at proposed fragment joins
- Parallel fragment matching with Rayon across 10,000+ fragment scenarios
- Partial recovery: export incomplete fragments with metadata flagging them as partial

---

### Week 7: Parallel Processing Pipeline & Results Database

#### Day 1–3: Rayon-Based Parallel Carver

**Files to create:**
```
crates/unirecover-carving/src/pipeline/
├── mod.rs
├── chunker.rs
├── worker_pool.rs
├── collector.rs
├── progress.rs
└── cancellation.rs
```

**Objectives:**
- Divide acquisition image into 64 MB work chunks with 64 KB overlap at boundaries
- Dynamic work stealing via Rayon thread pool
- Lock-free result collection
- Real-time progress reporting: chunks completed, files found, current throughput
- Graceful cancellation: save partial results with full audit log entry on abort

#### Day 4–5: Deduplication, Validation & Confidence Scoring

**Files to create:**
```
crates/unirecover-carving/src/postprocess/
├── mod.rs
├── deduplication.rs
├── validation.rs
├── thumbnail_gen.rs
└── scoring.rs
```

**Objectives:**
- SHA-256 exact deduplication
- Perceptual hash (pHash) for near-duplicate detection
- JPEG structural validation: parse all markers, flag malformed files
- Thumbnail generation for UI preview
- Final scoring: structural validity + metadata consistency + fragment completeness

#### Day 6–7: Evidence Results Database

**Files to create:**
```
crates/unirecover-carving/src/storage/
├── mod.rs
├── schema.rs
├── writer.rs
├── queries.rs
└── migration.rs
migrations/
├── 001_initial_schema.sql
└── 002_add_thumbnails.sql
```

**Schema:** `file_hash`, `case_id`, `operator_id`, `offset`, `size`, `type`, `confidence`, `recovery_method`, `thumbnail`, `exif_json`, `recovered_at`, `audit_ref`

**Objectives:**
- SQLite results database per case
- Batch inserts: 1,000+ records/sec
- Full-text search on EXIF data
- Every result linked to an audit log entry
- Export to DFXML, CSV, JSON

---

## Phase 4 — Encryption Handling (Weeks 8–9)

> **Authorization requirement:** All decryption operations require a valid case number, judicial authorization reference, and supervisor approval logged to the audit chain before any key material is accessed or used.

### Week 8: iOS Encryption

#### Day 1–3: Apple Keybag Parser

**Files to create:**
```
crates/unirecover-crypto/Cargo.toml
crates/unirecover-crypto/src/lib.rs
crates/unirecover-crypto/src/ios/
├── mod.rs
├── keybag.rs                 # Keybag plist parser
├── class_keys.rs             # Data Protection class key hierarchy
├── key_wrapping.rs           # AES key unwrapping (RFC 3394)
└── passcode_derive.rs        # PBKDF2/scrypt passcode derivation
crates/unirecover-crypto/tests/
├── test_keybag.rs
└── test_vectors/
```

**Objectives:**
- Parse `/var/keybags/systembag.kb` plist (obtained from acquired image)
- Extract wrapped class keys for all NSProtection classes (NSFileProtectionComplete, etc.)
- AES key unwrapping per RFC 3394
- Passcode-based key derivation: PBKDF2 with device-specific UID salt
- 4-digit PIN space (10,000): seconds on modern hardware
- 6-digit PIN space (1,000,000): minutes
- Alphanumeric passcode: dictionary + rule-based attack
- All decryption attempts and outcomes logged to audit chain with timestamps

#### Day 4–5: APFS Per-File Encryption

**Files to create:**
```
crates/unirecover-crypto/src/ios/apfs_crypto.rs
crates/unirecover-crypto/src/ios/perfile_keys.rs
crates/unirecover-crypto/src/ios/crypto_state.rs
```

**Objectives:**
- Parse `cp_state_t` from APFS inode extended attributes
- Extract per-file wrapped key from inode
- Decrypt file extents using unwrapped class key + per-file key (AES-XTS)
- Handle multiple keys per file (different extents with different protection classes)
- Verify decrypted data via file format signature before logging as recovered

#### Day 6–7: Secure Enclave — Documented Research & JTAG Methods

**Files to create:**
```
crates/unirecover-crypto/src/ios/sep_research/
├── mod.rs
├── checkm8.rs                # Checkm8-based pre-A12 key extraction
└── jtag.rs                   # JTAG/SWD debug interface methods
docs/recovery_guides/ios_sep_methods.md
```

**Objectives:**
- Document checkm8 exploit chain for pre-A12 devices (iPhone X and earlier): boot ROM vulnerability allowing RAM dump and key material extraction before Secure Enclave locks
- JTAG/SWD pinouts for iPhone 6–X logic board test pads (well-documented in public forensic literature)
- Ephemeral key capture from SEP shared memory region on vulnerable devices
- A12+ devices: document current limitations; these require physical chip-off or remain inaccessible pending future research
- All methods documented with device compatibility matrix and legal prerequisite checklist

---

### Week 9: Android Encryption

#### Day 1–3: File-Based Encryption (FBE)

**Files to create:**
```
crates/unirecover-crypto/src/android/
├── mod.rs
├── fbe.rs                    # FBE key hierarchy
├── keymaster.rs              # Keymaster HAL metadata parser
├── gatekeeper.rs             # PIN/pattern/password derivation
├── keystore.rs               # /data/misc/keystore parsing
├── vold.rs                   # Volume daemon key metadata
└── metadata_encryption.rs    # DM-default-key (metadata partition)
```

**Objectives:**
- Parse `/data/misc/vold/user_keys/` structure
- Extract wrapped per-user FBE keys (CE = Credential Encrypted, DE = Device Encrypted)
- Derive credential key from PIN/password using scrypt with device-stored parameters
- Extract scrypt N/r/p parameters from vold metadata
- Decrypt CE keyring to access user data partition
- All key derivation operations logged with case authorization reference

#### Day 4–5: Hardware-Backed Keystore Research

**Files to create:**
```
crates/unirecover-crypto/src/android/tee/
├── mod.rs
├── trusty.rs                 # Google Trusty TEE interface
├── qualcomm.rs               # Qualcomm QSEE research
└── trustzone.rs              # ARM TrustZone architecture notes
docs/recovery_guides/android_tee_methods.md
```

**Objectives:**
- Document Trusty TEE key storage architecture: how hardware-backed keys are wrapped and stored
- Qualcomm QSEE: document known research paths for extracting TEE-protected keys on older Snapdragon SoCs
- TEE memory extraction via `/dev/tee0` on rooted devices (requires root + case authorization)
- Samsung Knox: document Keymaster TA interface and known academic research on Knox key extraction
- Compatibility matrix: which methods apply to which device/OS combinations

#### Day 6–7: PIN & Pattern Bruteforce Engine

**Files to create:**
```
crates/unirecover-crypto/src/bruteforce/
├── mod.rs
├── pin_generator.rs
├── pattern_generator.rs
├── dictionary.rs
├── gpu_accel.rs              # CUDA/OpenCL scrypt acceleration
└── distributed.rs            # Multi-node workload distribution
```

**Objectives:**
- 4-digit PIN: 10,000 combinations
- 6-digit PIN: 1,000,000 combinations
- Android pattern unlock: 389,112 valid patterns (minimum 4-node, full graph)
- GPU-accelerated scrypt via CUDA/OpenCL: 100,000+ derivations/sec on RTX-class GPU
- Distributed bruteforce: split keyspace across multiple machines via gRPC workload queue
- All bruteforce jobs require case authorization; job start, progress, and completion logged

---

## Phase 5 — Plugin System & REST API (Weeks 10–11)

### Week 10: PyO3 Python Bindings & Plugin SDK

#### Day 1–3: Python Bindings

**Files to create:**
```
crates/unirecover-ffi/Cargo.toml
crates/unirecover-ffi/src/lib.rs
crates/unirecover-ffi/src/python/
├── mod.rs
├── engine.rs
├── acquisition.rs
├── carving.rs
├── results.rs
└── errors.rs
pyproject.toml
python/unirecover/
├── __init__.py
├── engine.py
├── types.py
└── py.typed
```

**Objectives:**
- Build with `maturin` for wheel distribution
- `RecoveryEngine` Python class: full access to acquisition, parsing, carving, and export pipeline
- GIL release during long-running Rust operations
- Type stubs for IDE autocomplete
- Auto-convert Rust errors to typed Python exceptions
- Installable via `pip install unirecover`

#### Day 4–5: Vendor Plugin System

**Files to create:**
```
plugins/
├── base_plugin.py
├── plugin_manager.py
├── android_plugins/
│   ├── samsung_plugin.py        # Samsung Galaxy MediaStore + Secure Folder
│   ├── pixel_plugin.py          # Google Pixel Titan M notes
│   └── xiaomi_plugin.py         # Xiaomi MIUI gallery database
└── ios_plugins/
    └── photos_sqlite_plugin.py  # Photos.sqlite relational recovery
```

**Objectives:**
- Plugin base class: `process(acquisition, case_context) -> List[RecoveredFile]`
- Auto-discovery and hot-reload from `plugins/` directory
- Samsung: Parse Galaxy-specific MediaStore schema and Secure Folder database structure
- Pixel: Document Titan M interaction; note current limitations for hardware-backed keys
- iOS: Recover deleted photo records from `Photos.sqlite` including face recognition data, album history, and edit records
- All plugin operations run under case context and logged

#### Day 6–7: Custom Parser SDK & Documentation

**Files to create:**
```
plugins/sdk/
├── fs_parser_sdk.py
├── signature_sdk.py
└── examples/
    ├── custom_fs_parser.py
    └── new_image_format.py
docs/plugin_development.md
```

**Objectives:**
- SDK for agency-developed plugins: register custom FS parsers and image signatures
- Example: Xiaomi EROFS partition parser
- Example: Oppo ColorOS gallery database
- Example: Custom RAW format (agency-specific camera hardware)
- Full API reference with runnable examples

---

### Week 11: REST API Server & Docker Deployment

#### Day 1–3: Actix-Web API Server

**Files to create:**
```
crates/unirecover-server/src/
├── main.rs
├── routes/
│   ├── acquisition.rs        # POST /api/v1/acquire
│   ├── carving.rs            # POST /api/v1/carve
│   ├── results.rs            # GET /api/v1/results/:case_id
│   ├── export.rs             # POST /api/v1/export
│   ├── plugins.rs            # GET/POST /api/v1/plugins
│   └── websocket.rs          # WS /ws/progress/:job_id
├── state.rs
├── auth.rs                   # mTLS + API key authentication
└── middleware/
    ├── audit_middleware.rs   # Log every API call to audit chain
    ├── logging.rs
    └── cors.rs
```

**Objectives:**
- RESTful API with JSON responses; OpenAPI/Swagger documentation
- WebSocket for real-time job progress
- mTLS authentication for agency deployments (client certificates)
- API key authentication for workstation clients
- Every API call logged to audit chain: endpoint, operator, case ID, timestamp, result
- Rate limiting on bruteforce endpoints

#### Day 4–5: Job Queue & Processing

**Files to create:**
```
crates/unirecover-server/src/queue/
├── mod.rs
├── redis_backend.rs
├── local_backend.rs
├── worker.rs
└── scheduler.rs
```

**Objectives:**
- Redis-backed job queue for multi-operator deployments
- Job types: Acquire, Parse, Carve, Decrypt, Export
- Priority queue: urgent/active investigations elevated
- Worker pool with configurable concurrency limits
- Job persistence across server restarts
- Job cancellation with partial result preservation

#### Day 6–7: Docker & Air-Gap Deployment

**Files to create:**
```
Dockerfile
docker-compose.yml
docker-compose.prod.yml
docker-compose.airgap.yml     # No external network dependencies
.dockerignore
kubernetes/
├── deployment.yaml
├── service.yaml
├── ingress.yaml
└── network-policy.yaml       # Restrict egress for air-gapped ops
scripts/docker_entrypoint.sh
scripts/airgap_bundle.sh      # Package all dependencies for offline install
```

**Objectives:**
- Multi-stage Docker build (musl for static linking, minimal attack surface)
- Air-gap bundle: script to package all container images and dependencies for offline installation
- Kubernetes manifests with network egress policies (prevent data exfiltration)
- Persistent volumes for case data and audit logs
- Health check endpoints
- Resource limits: memory and CPU caps to prevent carving jobs from starving audit log writes

---

## Phase 6 — Web UI (Weeks 12–13)

### Week 12: React Frontend

#### Day 1–3: Foundation & Case Management Interface

**Files to create:**
```
web-ui/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── api/
│   │   ├── client.ts
│   │   ├── websocket.ts
│   │   └── types.ts
│   ├── components/
│   │   ├── Layout.tsx
│   │   ├── Sidebar.tsx
│   │   ├── CaseManager.tsx       # Case creation + authorization
│   │   ├── OperatorAuth.tsx      # Login + badge authentication
│   │   └── AuditPanel.tsx        # Live audit log viewer
│   ├── hooks/
│   │   ├── useWebSocket.ts
│   │   └── useApi.ts
│   └── styles/globals.css
```

**Objectives:**
- Operator login: certificate or credential-based authentication before any case data is accessible
- Case creation form: case number, investigator name, authorizing supervisor, judicial reference
- Case dashboard: active cases, status, assigned operators, evidence item count
- Audit log panel: live-streaming append-only log view for active session
- Dark theme optimized for forensic workstation environments

#### Day 4–5: Acquisition Interface

**Files to create:**
```
web-ui/src/pages/
├── Acquisition.tsx
├── components/
│   ├── DeviceSelector.tsx
│   ├── DeviceCard.tsx
│   ├── AcquisitionOptions.tsx    # Partition selection + hash algorithm
│   ├── ProgressMonitor.tsx       # Speed, ETA, sectors read, hash running
│   └── AcquisitionReport.tsx     # Auto-generated post-acquisition report
```

**Objectives:**
- USB device detection and listing with device fingerprint display
- Partition selection with size and filesystem type shown
- Dual hash (SHA-256 + MD5) displayed in real-time during acquisition
- Write-blocker status indicator (hardware or software)
- Auto-generate acquisition report on completion: PDF with device info, hashes, operator, timestamp
- Pause/Resume/Cancel with partial state preserved

#### Day 6–7: Carving & Recovery Interface

**Files to create:**
```
web-ui/src/pages/
├── Carving.tsx
├── components/
│   ├── SignatureSelector.tsx
│   ├── CarvingProgress.tsx
│   ├── FilePreview.tsx
│   └── ThumbnailGrid.tsx
```

**Objectives:**
- Multi-select file format targets
- Real-time per-format statistics: found count, data volume, confidence distribution
- Thumbnail gallery with Masonry layout; click to open full preview + EXIF panel
- Confidence filter slider: hide low-confidence candidates
- Bulk selection and export

---

### Week 13: Forensic Viewers & Evidence Export

#### Day 1–3: Forensic Analysis Viewers

**Files to create:**
```
web-ui/src/components/viewers/
├── HexViewer.tsx              # Hex dump with pattern highlighting
├── DiskMap.tsx                # Visual block allocation heatmap
├── FileSystemTree.tsx         # Interactive FS tree
├── TimelineView.tsx           # File timeline from EXIF dates
├── MapView.tsx                # GPS coordinate map (Leaflet, offline tiles)
└── ComparisonView.tsx         # Side-by-side file comparison
```

**Objectives:**
- Hex viewer with highlighted header/footer markers and pattern match offsets
- Block allocation heatmap: color-coded by allocated/unallocated/recovered/encrypted
- Interactive filesystem tree with deleted files flagged in red
- EXIF-based timeline: recovered photos plotted chronologically
- GPS map with offline tile support (no external network required in air-gapped deployments)
- Side-by-side comparison: original thumbnail vs recovered fragment

#### Day 4–5: Evidence Export & Case Report Generator

**Files to create:**
```
crates/unirecover-export/Cargo.toml
crates/unirecover-export/src/
├── mod.rs
├── dfxml.rs                   # Digital Forensics XML (DFXML)
├── e01.rs                     # Expert Witness Format export
├── pdf_report.rs              # Case report PDF
├── csv_export.rs
└── zip_export.rs              # Evidence package (files + metadata)
web-ui/src/pages/Export.tsx
```

**Objectives:**
- DFXML export: standard interoperable forensic XML format (compatible with Autopsy, AXIOM)
- Case report PDF: cover page (case number, operator, device info, authorization ref), evidence summary table, per-file metadata, audit log excerpt, hash verification table
- ZIP evidence package: recovered files + sidecar JSON metadata + hash manifest
- All exports signed with operator certificate and logged to audit chain
- Export access control: only authorized case members can export

#### Day 6–7: Audit & Chain-of-Custody Dashboard

**Files to create:**
```
web-ui/src/pages/
├── AuditDashboard.tsx
├── ChainOfCustody.tsx
├── components/
│   ├── AuditTimeline.tsx
│   ├── OperatorActivity.tsx
│   └── IntegrityVerifier.tsx   # Re-verify acquisition hash on demand
```

**Objectives:**
- Full audit timeline: every action in the case displayed chronologically
- Operator activity report: what each investigator accessed and when
- Chain-of-custody ledger: device intake → acquisition → analysis → export, with signatures
- Hash integrity re-verification: re-compute acquisition image hash at any time and compare to logged value
- Export chain-of-custody document as signed PDF for court submission

---

## Phase 7 — Validation, Testing & Hardening (Week 14)

### Week 14: NIST/CFTT Validation & Security Hardening

#### Day 1–3: Forensic Validation Suite

**Files to create:**
```
tests/validation/
├── nist_cftt_suite.rs         # NIST Computer Forensics Tool Testing
├── known_image_tests.rs       # Tests against reference images with known contents
├── hash_verification_tests.rs
├── write_blocker_tests.rs
└── recovery_accuracy_tests.rs
scripts/run_validation.sh
docs/validation_report.md
```

**Objectives:**
- Run against NIST CFTT reference disk images (publicly available test corpus)
- Validate write-blocker: confirm zero writes to acquisition source during all operations
- Hash consistency: acquisition hash must match re-computation 100% of the time
- Recovery accuracy: measure true positive rate against reference images with known deleted files
- Document all test results in `validation_report.md` for submission to funding body

#### Day 4–5: Security Hardening

**Files to create:**
```
crates/unirecover-core/src/security/
├── memory_protection.rs       # Zeroize key material after use
├── privilege_drop.rs          # Drop privileges after device access
└── sandboxing.rs              # Seccomp filter for worker processes
```

**Objectives:**
- Zeroize all key material from memory immediately after use (`zeroize` crate)
- Privilege separation: acquisition (requires root/admin) runs in isolated process; analysis runs unprivileged
- Seccomp filter for carving workers: restrict to read + compute syscalls only
- TLS 1.3 enforced for all API communication
- Dependency audit: `cargo audit` run in CI on every commit

#### Day 6–7: Performance Benchmarks & Documentation

**Files to create:**
```
benches/
├── full_pipeline_benchmark.rs
├── filesystem_benchmark.rs
└── carving_benchmark.rs
docs/performance_report.md
docs/deployment_guide.md
docs/operator_manual.md
```

**Objectives:**
- Full pipeline benchmark: acquisition → carving → export on 64 GB reference image
- Document throughput, memory usage, and CPU utilization for inclusion in funding proposal
- Operator manual: step-by-step guide for investigators with no forensics software background
- Deployment guide: installation on Ubuntu 22.04/24.04 LTS, Windows (WSL2), and air-gapped environments

---

## Phase 8 — Integration, Hardening & Release (Weeks 15–16)

### Week 15: Integration Testing & CI Pipeline

#### Day 1–3: End-to-End Integration Tests

**Files to create:**
```
tests/integration/
├── android_e2e_test.rs        # Full Android acquisition → recovery → export
├── ios_e2e_test.rs            # Full iOS acquisition → recovery → export
├── encrypted_device_test.rs   # Decryption → recovery pipeline
├── air_gap_test.sh            # Verify no external network calls
└── court_report_test.rs       # Validate PDF report structure
```

**Objectives:**
- End-to-end tests using reference device images (not live devices)
- Verify chain-of-custody ledger integrity across a full case lifecycle
- Confirm air-gap deployment makes zero external network calls
- Validate court report PDF contains all required fields and passes structure checks
- Regression test suite covering all supported device profiles

#### Day 4–7: CI/CD Release Pipeline

**Files to create:**
```
.github/workflows/release.yml
.github/workflows/validation.yml
scripts/build_release.sh
scripts/sign_release.sh        # GPG-sign release artifacts
CHANGELOG.md
```

**Objectives:**
- Cross-compile release binaries: Linux (x86_64, aarch64), macOS (arm64), Windows (x86_64)
- GPG-signed release artifacts: investigators can verify binary integrity before deployment
- Automated NIST CFTT validation run on every release candidate
- Release notes with device compatibility matrix and known limitations

---

### Week 16: Documentation, Legal Review & Funding Package

#### Day 1–3: Complete Documentation

**Files to create:**
```
docs/
├── operator_manual.md               # Step-by-step investigator guide
├── deployment_guide.md              # Installation and configuration
├── api_reference.md                 # Full REST API reference
├── plugin_development.md            # Third-party plugin guide
├── court_admissibility.md           # Legal admissibility guidance
├── validation_report.md             # NIST/CFTT test results
├── architecture.md                  # Full system architecture
└── funding_proposal/
    ├── executive_summary.md
    ├── technical_specification.md
    ├── competitive_analysis.md       # vs Cellebrite, AXIOM, Oxygen
    ├── budget_breakdown.md
    └── roadmap_post_v1.md
```

**Objectives:**
- Operator manual: full step-by-step guide from case creation to court report, written for investigators without forensics software expertise
- Court admissibility guide: how UniRecover satisfies Daubert/Frye standards (reproducibility, peer review, known error rate, general acceptance)
- Competitive analysis: feature and price comparison against Cellebrite UFED ($15k–$30k/unit), Magnet AXIOM ($5k–$15k/year), and Oxygen Forensic ($3k–$8k/year)
- Budget breakdown: development costs, infrastructure, training, ongoing maintenance

#### Day 4–5: Legal & Policy Framework

**Files to create:**
```
LEGAL_NOTICE.md
CHAIN_OF_CUSTODY.md
docs/authorized_use_policy.md
docs/data_retention_policy.md
```

**Objectives:**
- Authorized use policy: tool may only be operated under lawful authority (search warrant, court order, or equivalent); unauthorized use constitutes a criminal offence under applicable computer crime statutes
- Data retention policy: recovered evidence stored only for duration of case; destruction procedure documented
- Export control notice: encryption-handling components may be subject to export controls; document applicable jurisdictions
- Privacy impact assessment template for agency procurement

#### Day 6–7: Final Release & Funding Package Assembly

**Objectives:**
- Tag v1.0.0 release; publish signed binaries
- Assemble government funding proposal package: executive summary, full technical specification, validation report, competitive analysis, budget, and team CVs
- Prepare demonstration environment: pre-loaded with anonymized reference case (synthetic data) for funding body presentation
- Submit to relevant funding bodies: national law enforcement technology programs, justice department research grants, EU law enforcement innovation funds

---

## Technology Stack Summary

| Layer | Technology | Rationale |
|---|---|---|
| Core engine | Rust | Memory safety, zero-cost abstractions, fearless concurrency |
| SIMD acceleration | AVX2/AVX-512/NEON | 10 GB/s carving throughput |
| Async runtime | Tokio + io_uring | Non-blocking I/O for large image handling |
| Python bindings | PyO3 + Maturin | Plugin SDK without sacrificing core performance |
| REST API | Actix-Web | High-performance, production-grade Rust web framework |
| Job queue | Redis | Persistent, multi-operator job management |
| Web UI | React + TypeScript + Vite | Modern, maintainable, responsive |
| Database | SQLite (per-case) | Portable, no server dependency, forensically auditable |
| Containerization | Docker + Kubernetes | Reproducible deployment; air-gap support |
| Evidence format | DFXML + E01 + PDF | Interoperable with existing forensic toolchain |
| Audit log | HMAC-SHA256 chain | Tamper-evident; court-admissible |

---

## Competitive Landscape

| Tool | Price | Source | iOS Encrypted | Android FBE | Extensible | Air-gap |
|---|---|---|---|---|---|---|
| Cellebrite UFED | $15k–$30k/unit | Closed | Yes (limited) | Yes (limited) | No | Yes |
| Magnet AXIOM | $5k–$15k/yr | Closed | Partial | Partial | Plugin SDK | Partial |
| Oxygen Forensic | $3k–$8k/yr | Closed | Partial | Partial | Limited | No |
| **UniRecover** | **Open / Gov license** | **Open** | **Yes** | **Yes** | **Full SDK** | **Yes** |

---

## Compliance & Standards

- **NIST SP 800-101 Rev 1** — Guidelines on Mobile Device Forensics
- **ACPO Good Practice Guide** — Digital Evidence (UK)
- **ISO/IEC 27037** — Guidelines for identification, collection, and preservation of digital evidence
- **SWGDE Best Practices** — Mobile Device Evidence
- **RFC 3394** — AES Key Wrap Algorithm
- **DFXML** — Digital Forensics XML schema (MITRE)

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| iOS encryption changes (new OS) | High | High | Modular crypto layer; plugin updates within 30 days of OS release |
| Android vendor fragmentation | High | Medium | Plugin SDK allows agency-specific additions |
| Hardware security chip (A16+, Titan M2) | Medium | High | Document limitations; focus on pre-chip devices; track research |
| Legal challenge to evidence admissibility | Low | High | NIST validation, audit chain, write-blocker compliance |
| Performance regression | Low | Medium | Benchmarks in CI; performance gates on release |
| Supply chain / dependency vulnerability | Medium | Medium | `cargo audit` in CI; vendored dependencies for air-gap builds |

---

*UniRecover — Built for investigators. Validated for court. Open for inspection.*
