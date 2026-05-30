# UniRecover — Universal Mobile Device Image Recovery Framework
## Full Development Timeline & Technical Specification v2.0
### Law Enforcement Edition | Government Funding Proposal

---

## Executive Summary

UniRecover is a cross-platform forensic image recovery framework purpose-built for law enforcement agencies and accredited digital forensics laboratories. It recovers deleted photographs and videos from modern iOS and Android smartphones, producing court-admissible evidence with full chain-of-custody integrity.

### Core Architectural Philosophy

The central design principle of UniRecover is **long-term sustainability through modularity**. Existing commercial tools (Cellebrite UFED, Magnet AXIOM, Oxygen Forensic) are brittle because they hardcode specific extraction methods into their core logic. When Apple releases a new Secure Enclave revision or Google ships a new StrongBox TEE implementation, those tools become partially obsolete and require expensive vendor updates.

UniRecover is engineered differently:

> The core parsing, carving, and analysis engine is **completely agnostic of how data was obtained.** It operates on a standard byte stream. The acquisition layer is a set of hot-swappable, independently updatable modules. When a specific extraction method is patched or superseded, only that module is replaced — the entire analysis pipeline, UI, and evidence export system remains untouched.

This is not a tool built around a single exploit. It is a **pipeline framework** that accepts data from any forensically sound source — hardware write-blockers, ADB acquisition, JTAG dumps, physical chip-off images, live memory captures, or vendor engineering mode outputs — and processes it through a unified, court-auditable engine.

**Target users:** Digital forensics units, cybercrime bureaus, national law enforcement agencies  
**Tech stack:** Rust (core engine) · Python (plugin system) · React (web UI)  
**Development cycle:** 16 weeks  
**Deployment:** On-premises (air-gapped), Docker, Kubernetes  

---

## Project Objectives

1. Build a modular ingestion-analysis pipeline that remains functional as mobile OS and hardware security evolves
2. Recover deleted images and videos from iOS (APFS/encrypted) and Android (EXT4/F2FS/FBE) devices
3. Maintain full forensic integrity — AFF4 container storage, dual hash verification, chain-of-custody logging
4. Handle modern device encryption via all available lawful methods: passcode derivation, AFU memory capture, secondary storage vectors, and HITL physical interface testing
5. Provide a plugin SDK for agency-specific device profiles, extraction modules, and database schemas
6. Deliver a court-ready evidence export pipeline (DFXML, AFF4, E01, signed PDF case reports)
7. Support air-gapped, on-premises deployment with zero external dependencies
8. Pass Daubert/Frye admissibility standards — validated against NIST CFTT reference corpora

---

## Repository Structure

```
unirecover/
├── Cargo.toml
├── pyproject.toml
├── docker-compose.yml
├── docker-compose.airgap.yml
├── Makefile
├── README.md
├── CHAIN_OF_CUSTODY.md
├── AUTHORIZED_USE_POLICY.md
├── docs/
│   ├── architecture.md
│   ├── api_reference.md
│   ├── court_admissibility.md
│   ├── validation_report.md
│   ├── hitl_guide.md              # Hardware-in-the-Loop setup guide
│   └── recovery_guides/
│       ├── android_recovery.md
│       ├── ios_recovery.md
│       └── secondary_vectors.md   # SD card, cache, sync service recovery
├── crates/
│   ├── unirecover-core/           # Core engine (source-agnostic)
│   ├── unirecover-cli/
│   ├── unirecover-server/         # REST API
│   ├── unirecover-acquisition/    # Modular acquisition layer
│   ├── unirecover-fs/             # Filesystem parsers
│   ├── unirecover-carving/        # SIMD file carver
│   ├── unirecover-crypto/         # Encryption handling
│   ├── unirecover-audit/          # Audit log & CoC engine
│   ├── unirecover-export/         # DFXML, AFF4, PDF export
│   └── unirecover-ffi/            # Python FFI (PyO3)
├── plugins/
│   ├── base_plugin.py
│   ├── acquisition_providers/     # Hot-swappable extraction modules
│   │   ├── adb_provider.py
│   │   ├── jtag_provider.py
│   │   ├── aff4_provider.py
│   │   └── hitl_provider.py       # Hardware-in-the-Loop provider
│   ├── android_plugins/
│   └── ios_plugins/
├── hitl/                          # Hardware-in-the-Loop firmware & schematics
│   ├── firmware/
│   │   ├── pico_hid_emulator/     # Raspberry Pi Pico HID firmware
│   │   └── fpga_interface/        # FPGA timing control
│   ├── schematics/
│   └── README.md
├── web-ui/
├── tests/
│   ├── test_images/
│   ├── validation/                # NIST CFTT suite
│   └── hitl_simulation/           # Software-simulated HITL tests
└── scripts/
    ├── setup_dev_env.sh
    ├── build_release.sh
    ├── run_validation.sh
    └── airgap_bundle.sh
```

---

## System Architecture — The Three-Layer Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                    LAYER 1: INGESTION                            │
│          Unified Source Interface  (Read + Seek trait)           │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │  ADB /   │ │  AFF4 /  │ │  JTAG /  │ │   HITL   │  ···      │
│  │ Lockdown │ │ DD / E01 │ │  Chip-off│ │ Physical │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│         Each module is independently replaceable                 │
└───────────────────────────────┬──────────────────────────────────┘
                                │  Raw byte stream
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                    LAYER 2: ANALYSIS                             │
│         Source-Agnostic Core Engine  (unirecover-core)           │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │    FS    │ │  SQLite  │ │  Carving │ │  Crypto  │           │
│  │ Parsers  │ │ Recovery │ │  Engine  │ │ Handler  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│         Stable — survives any acquisition layer change           │
└───────────────────────────────┬──────────────────────────────────┘
                                │  Canonical evidence records
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                    LAYER 3: OUTPUT                               │
│         Audit Engine · Evidence Export · Web UI                  │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │  DFXML   │ │   AFF4   │ │   PDF    │ │  React   │           │
│  │  Export  │ │ Container│ │  Report  │ │    UI    │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└──────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Foundation, Core Architecture & Audit Framework (Weeks 1–2)

### Week 1: The Source-Agnostic Core & Audit Engine

#### Day 1–2: Repository, CI/CD & Audit Core

**Files to create:**
```
Cargo.toml
crates/unirecover-core/Cargo.toml
crates/unirecover-core/src/lib.rs
crates/unirecover-core/src/source.rs       # AcquisitionSource trait
crates/unirecover-core/src/error.rs
crates/unirecover-audit/Cargo.toml
crates/unirecover-audit/src/lib.rs
crates/unirecover-audit/src/log.rs         # Append-only HMAC-chained log
crates/unirecover-audit/src/chain.rs       # Chain-of-custody ledger
crates/unirecover-audit/src/operator.rs    # Operator identity & auth
.github/workflows/ci.yml
.github/workflows/release.yml
rust-toolchain.toml
AUTHORIZED_USE_POLICY.md
```

**The critical design decision — `AcquisitionSource` trait:**
```rust
pub trait AcquisitionSource: Read + Seek + Send + Sync {
    fn size(&self) -> Result<u64>;
    fn block_size(&self) -> u64;
    fn sha256(&self) -> Result<[u8; 32]>;
    fn md5(&self) -> Result<[u8; 16]>;
    fn source_descriptor(&self) -> SourceDescriptor;
}
```
Every ingestion module — ADB, AFF4, JTAG image, HITL capture, live memory dump — implements this single trait. The entire analysis engine downstream never sees anything else. This is the architectural guarantee of long-term resilience.

**Audit log objectives:**
- Append-only, HMAC-SHA256-chained entries — every operation produces a tamper-evident log record
- No operation (device read, file export, decryption attempt) executes without a corresponding audit entry
- Case context (case number, operator ID, judicial authorization reference) required before any source can be opened
- Write-blocker enforcement by default: acquisition sources open read-only; any write attempt is denied and logged

#### Day 3–4: AFF4 Container — The Standard Storage Format

**Files to create:**
```
crates/unirecover-acquisition/src/aff4/
├── mod.rs
├── container.rs               # AFF4 container read/write
├── stream.rs                  # Linear stream storage
├── map.rs                     # Sparse map stream (for logical images)
├── metadata.rs                # RDF metadata (device info, hashes, case data)
├── integrity.rs               # SHA-256 chunk verification
└── writer.rs                  # Streaming AFF4 writer during acquisition
```

**Objectives:**
- AFF4 is the primary storage format for all acquired data — physical images, logical images, and file-level extractions all stored in one container
- Built-in SHA-256 integrity hashing at the chunk level
- RDF metadata block: device fingerprint, acquisition timestamp, operator ID, case number, tool version
- AFF4 container written in streaming fashion during acquisition (no full copy to temp storage first)
- Any existing AFF4, E01, or DD image can be opened as an `AcquisitionSource` — the analysis engine sees no difference

#### Day 5–7: Block Device & Memory-Mapped I/O

**Files to create:**
```
crates/unirecover-acquisition/src/sources/
├── mod.rs
├── block_device.rs
├── disk_image.rs              # AFF4 / DD / E01 / raw image reader
├── memory.rs
└── traits.rs
crates/unirecover-acquisition/src/mmap_pool.rs
crates/unirecover-acquisition/src/chunked_reader.rs
crates/unirecover-acquisition/benches/
├── read_benchmark.rs
└── mmap_benchmark.rs
```

**Objectives:**
- `BlockDeviceReader`: O_DIRECT with hardware write-block enforcement
- `DiskImageReader`: memory-mapped access via `memmap2`, supporting AFF4/DD/E01
- `ChunkedReader`: handles images >1TB with per-chunk hash verification
- Software write-blocker: intercept and deny write syscalls to source; log any attempt
- Target: 1 GB/s sequential read; benchmark comparing direct I/O vs mmap vs buffered

---

### Week 2: Modular Acquisition Providers

The acquisition providers are **the only part of the system that needs to change when hardware security evolves.** They are implemented as independently deployable modules, not compiled into the core.

#### Day 1–3: Android Acquisition Provider

**Files to create:**
```
plugins/acquisition_providers/adb_provider/
├── __init__.py
├── provider.py                # ADB acquisition provider
├── adb_protocol.rs            # ADB USB + TCP implementation
├── partition_table.rs         # GPT/MBR parser
└── device_info.rs
crates/unirecover-acquisition/src/android/
├── adb.rs
├── fastboot.rs
├── partition_table.rs
└── device_info.rs
```

**Objectives:**
- ADB provider implements `AcquisitionSource` — outputs a raw byte stream into the AFF4 writer
- Device enumeration: serial, manufacturer, model, Android version, build fingerprint
- Partition table extraction; all partitions listed and logged to case record
- Provider metadata (method used, device root state, acquisition completeness) written into AFF4 RDF block
- If a future Android version breaks ADB-level partition access, only this provider module is updated

#### Day 4–6: iOS Acquisition Provider

**Files to create:**
```
plugins/acquisition_providers/ios_provider/
├── __init__.py
├── provider.py
crates/unirecover-acquisition/src/ios/
├── lockdown.rs
├── afc.rs
├── mobile_device.rs
├── developer_disk.rs
└── jailbreak.rs
crates/unirecover-acquisition/src/ios/ffi/
├── mobile_device_sys.rs
build.rs
```

**Objectives:**
- iOS provider: `MobileDevice.framework` (macOS) and `libimobiledevice` (Linux)
- AFC protocol for file-level access; developer disk mount for filesystem access
- Jailbreak detection (checkra1n, unc0ver, palera1n) — state logged to AFF4 metadata
- Device pairing certificate recorded with case
- Provider outputs raw filesystem stream into AFF4 container

#### Day 7: Provider Registry & Platform Abstraction

**Files to create:**
```
crates/unirecover-acquisition/src/provider_registry.rs
crates/unirecover-acquisition/src/device_enum.rs
crates/unirecover-acquisition/src/unified_device_info.rs
```

**Objectives:**
- Provider registry: discovers and loads acquisition provider modules at runtime
- `UnifiedDeviceInfo` struct: platform-agnostic device record (OS, version, IMEI/serial, storage, encryption state, acquisition method used)
- New providers can be added by dropping a module into `plugins/acquisition_providers/` — no core recompilation needed
- Mock provider for CI testing

---

## Phase 2 — Filesystem Parsing Engine (Weeks 3–5)

### Week 3: APFS Parser (iOS)

#### Day 1–3: APFS Container & Checkpoint

**Files to create:**
```
crates/unirecover-fs/Cargo.toml
crates/unirecover-fs/src/apfs/
├── mod.rs
├── container.rs
├── nx_superblock.rs
├── checkpoint.rs
├── object_map.rs
├── spaceman.rs
└── constants.rs
crates/unirecover-fs/tests/
├── apfs_test_images/
└── test_apfs_container.rs
```

**Objectives:**
- Receives `AcquisitionSource` byte stream — no knowledge of how data was obtained
- Parse NXSB at offset 32: block size, total blocks, features
- Checkpoint descriptor area: find latest valid checkpoint
- All parsed metadata written to canonical schema (see Phase 2 Day 7)
- Fuzz testing: parser must not panic on malformed input

#### Day 4–5: APFS B-Tree

**Files to create:**
```
crates/unirecover-fs/src/apfs/btree/
├── mod.rs
├── node.rs
├── fixed_size_keys.rs
├── variable_size_keys.rs
├── traversal.rs
└── iterator.rs
```

**Objectives:**
- Generic B-tree node parsing (fixed and variable-size keys)
- Copy-on-Write node versioning: older nodes may reference deleted file metadata
- Tree traversal for object map lookups
- Fuzz testing with arbitrary bit-flip corruption

#### Day 6–7: APFS Volume & Deleted File Recovery

**Files to create:**
```
crates/unirecover-fs/src/apfs/
├── volume.rs
├── inode.rs
├── extent.rs
├── recovery.rs
└── encryption.rs
```

**Objectives:**
- APFS volume superblock (APSB) parsing
- Inode parsing: name, size, timestamps, extended attributes, Data Protection class
- Extent tree traversal for block locations
- Deleted inode recovery from orphaned CoW B-tree nodes
- Encryption state extraction: per-file wrapped key and protection class recorded for crypto layer

---

### Week 4: EXT4 & F2FS Parsers (Android)

#### Day 1–3: EXT4

**Files to create:**
```
crates/unirecover-fs/src/ext4/
├── mod.rs
├── superblock.rs
├── group_descriptor.rs
├── inode.rs
├── extent_tree.rs
├── directory.rs
├── journal.rs
└── recovery.rs
```

**Objectives:**
- Superblock (magic 0xEF53), block group descriptors, extent tree traversal (5 levels)
- JBD2 journal replay: recover recently committed writes before deletion
- Orphan list: inodes unlinked but not yet zeroed
- Test against Android `userdata` partition dumps from reference image corpus

#### Day 4–6: F2FS

**Files to create:**
```
crates/unirecover-fs/src/f2fs/
├── mod.rs
├── superblock.rs
├── checkpoint.rs
├── nat.rs
├── sit.rs
├── segment.rs
├── node.rs
└── recovery.rs
```

**Objectives:**
- F2FS superblock (magic 0xF2F52010), NAT and SIT traversal
- GC victim segment recovery: garbage collection victim segments retain old data until overwritten — scan for recoverable content
- F2FS inline compression (LZO/LZ4/ZSTD)
- Recovered candidates logged with offset, size, confidence

#### Day 7: Filesystem Abstraction & Canonical Schema

**Files to create:**
```
crates/unirecover-fs/src/traits.rs
crates/unirecover-fs/src/fs_detect.rs
crates/unirecover-fs/src/block_iter.rs
crates/unirecover-fs/src/canonical_schema.rs    # THE key to cross-platform consistency
```

**The canonical schema — why this matters:**

Every filesystem parser (APFS, EXT4, F2FS, future additions) outputs to a single unified record format:

```rust
pub struct CanonicalFileRecord {
    pub case_id: String,
    pub source_hash: [u8; 32],        // Links back to AFF4 acquisition
    pub original_path: Option<String>,
    pub filename: Option<String>,
    pub size: Option<u64>,
    pub created: Option<DateTime<Utc>>,
    pub modified: Option<DateTime<Utc>>,
    pub deleted: Option<DateTime<Utc>>,
    pub file_type: FileType,
    pub recovery_method: RecoveryMethod,
    pub block_offsets: Vec<(u64, u64)>,
    pub encryption_state: EncryptionState,
    pub confidence: f32,
    pub gps: Option<GpsCoordinate>,
    pub exif: Option<ExifRecord>,
    pub audit_ref: String,
}
```

The React UI, Python plugins, and evidence export layer only ever work with `CanonicalFileRecord`. When a new vendor database schema or filesystem variant is added, only a new parser is written — the entire downstream pipeline remains unchanged.

---

### Week 5: SQLite Recovery, Thumbnail Caches & Secondary Vectors

#### Day 1–3: SQLite Database Recovery

**Files to create:**
```
crates/unirecover-fs/src/sqlite/
├── mod.rs
├── wal_recovery.rs
├── freelist_carving.rs
├── cell_parser.rs
├── mediastore_parser.rs       # Android MediaStore → CanonicalFileRecord
└── photos_sqlite_parser.rs    # iOS Photos.sqlite → CanonicalFileRecord
```

**Objectives:**
- SQLite WAL recovery: recently deleted records persist in the write-ahead log
- Freelist page carving: deleted records remain in freelist pages until overwritten
- Android `external.db`: extract filename, path, date, GPS, dimensions → canonical schema
- iOS `Photos.sqlite`: deleted photo records, album membership, edit history → canonical schema
- Both parsers output `CanonicalFileRecord` — UI sees no difference between Android and iOS sources

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
- Android: parse `DCIM/.thumbnails/` and `.thumbdata3` binary stores
- iOS: parse `PhotoData/Thumbnails/` from Camera Roll structures
- Match thumbnails to deleted originals via embedded metadata
- Thumbnails exported as standalone evidence items with provenance

#### Day 6–7: Secondary Storage & Sync Service Vectors

**Files to create:**
```
crates/unirecover-fs/src/secondary/
├── mod.rs
├── sd_card.rs                 # External SD card (FAT32/exFAT/F2FS)
├── app_cache.rs               # App-level unencrypted caches
└── cloud_sync_artifacts.rs    # Local sync metadata (not cloud access)
plugins/ios_plugins/photos_sqlite_plugin.py
plugins/android_plugins/sd_card_plugin.py
docs/recovery_guides/secondary_vectors.md
```

**Secondary vectors rationale:**

When primary partition encryption is not bypassable on a given device, the framework pivots to secondary data locations where the OS architecture naturally duplicates or mirrors content:

- **External SD cards:** Android apps frequently mirror DCIM media to removable storage configured as portable storage. SD cards use FAT32/exFAT (no FBE), making them directly parseable
- **App-level caches:** Gallery and social media apps generate unencrypted thumbnail and preview caches in world-readable app directories on rooted devices
- **Local sync metadata:** Cloud sync services (Google Photos, iCloud) write local SQLite databases recording synced file paths and hashes — recoverable even if the original file is gone, and useful for correlating with cloud warrant returns
- **These are not workarounds — they are primary investigation vectors** for devices where hardware-backed encryption is intact

---

## Phase 3 — File Carving Engine (Weeks 6–7)

### Week 6: SIMD-Accelerated Signature Scanning

#### Day 1–3: SIMD Core

**Files to create:**
```
crates/unirecover-carving/Cargo.toml
crates/unirecover-carving/src/simd/
├── mod.rs
├── avx2_engine.rs
├── avx512_engine.rs
├── neon_engine.rs
├── wasm_engine.rs
└── runtime_detect.rs
crates/unirecover-carving/benches/
├── simd_benchmark.rs
└── comparison_scalar.rs
```

**Objectives:**
- Runtime CPU feature detection via `cpuid`
- AVX2: 32-byte parallel header/footer scanning
- AVX-512: 64-byte operations for server workstations
- ARM NEON: native mobile forensic hardware
- WASM SIMD: browser-side preview carving in the web UI
- Target: 10 GB/s on modern server CPU

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
└── signatures.yaml
```

**Objectives:**
- 50+ image and video format signatures
- JPEG: SOI (FFD8) to EOI (FFD9), entropy-validated
- HEIC: `ftyp` box validation, `mdat` extraction
- PNG: IHDR/IDAT/IEND chunk CRC validation
- Camera RAW: CR2, NEF, ARW, DNG, ORF, RW2
- Entropy filtering: high-entropy regions flagged as potentially encrypted (logged, not discarded — useful for decryption targeting)
- Confidence scoring: 0.0–1.0 per candidate

#### Day 6–7: Fragmented File Reconstruction

**Files to create:**
```
crates/unirecover-carving/src/reassembly/
├── mod.rs
├── bifragment_gap_carving.rs
├── smart_reassembly.rs
├── pixel_continuity.rs
└── ml_reassembly.rs
```

**Objectives:**
- Bifragment gap carving: validate JPEG restart markers across fragment boundaries
- Smart reassembly: use filesystem metadata hints from the FS parsing layer to guide ordering
- Pixel continuity analysis at proposed fragment joins
- Parallel matching with Rayon
- Partial recovery: export incomplete fragments flagged as partial with confidence score

---

### Week 7: Parallel Pipeline & Evidence Database

#### Day 1–3: Parallel Carver

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
- 64 MB work chunks with 64 KB boundary overlap
- Dynamic work stealing via Rayon
- Lock-free result collection
- Real-time progress: throughput, files found, confidence distribution
- Graceful cancellation with partial result preservation and full audit entry

#### Day 4–5: Deduplication & Validation

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
- SHA-256 exact deduplication; pHash near-duplicate detection
- JPEG structural validation
- Thumbnail generation for UI preview
- Final scoring: structural validity + metadata consistency + fragment completeness
- All results output as `CanonicalFileRecord`

#### Day 6–7: Evidence Results Database

**Files to create:**
```
crates/unirecover-carving/src/storage/
├── schema.rs
├── writer.rs
├── queries.rs
└── migration.rs
migrations/
├── 001_initial_schema.sql
└── 002_add_thumbnails.sql
```

**Schema:** `file_hash`, `case_id`, `operator_id`, `source_aff4_ref`, `offset`, `size`, `type`, `confidence`, `recovery_method`, `thumbnail`, `exif_json`, `gps_json`, `recovered_at`, `audit_ref`

**Objectives:**
- SQLite per-case evidence database
- Every record linked to AFF4 source container and audit log entry
- Batch inserts: 1,000+/sec
- Full-text search on EXIF data
- Export to DFXML, CSV, JSON

---

## Phase 4 — Encryption Handling (Weeks 8–9)

> **Sustainable encryption strategy:** UniRecover does not attempt to build a universal cryptographic bypass. Modern hardware security (Apple A12+ Secure Enclave, Android StrongBox on Tensor/Snapdragon 8 Gen) makes software-only key extraction infeasible. The framework instead implements a **tiered approach**: passcode derivation where lawfully obtained, AFU memory capture on live devices, HITL physical interface for hardware-enforced PIN spaces, and secondary vector pivoting when primary extraction is unavailable. Every tier is a separately loadable module.

### Week 8: iOS Encryption

#### Day 1–3: Apple Keybag & Data Protection

**Files to create:**
```
crates/unirecover-crypto/Cargo.toml
crates/unirecover-crypto/src/ios/
├── mod.rs
├── keybag.rs
├── class_keys.rs
├── key_wrapping.rs
└── passcode_derive.rs
```

**Objectives:**
- Parse `/var/keybags/systembag.kb` from acquired AFF4 image
- Extract wrapped class keys for all NSProtection classes
- AES key unwrapping per RFC 3394
- Passcode derivation: PBKDF2 with device-specific UID-derived salt
- 4-digit PIN (10,000): seconds; 6-digit (1,000,000): minutes
- All operations require case authorization token; logged to audit chain

#### Day 4–5: APFS Per-File Decryption

**Files to create:**
```
crates/unirecover-crypto/src/ios/
├── apfs_crypto.rs
├── perfile_keys.rs
└── crypto_state.rs
```

**Objectives:**
- Parse `cp_state_t` from APFS inode: protection class, per-file wrapped key
- Decrypt extents with AES-XTS using unwrapped class key + per-file key
- Handle multiple protection classes across different files
- Verify decrypted output via format signature before recording as recovered
- Decrypted data fed back into the analysis pipeline as a new `AcquisitionSource` — the carving engine sees decrypted bytes, not ciphertext

#### Day 6–7: AFU Live Memory Capture Provider

**Files to create:**
```
plugins/acquisition_providers/afu_memory_provider/
├── __init__.py
├── provider.py                # AFU memory capture acquisition provider
crates/unirecover-acquisition/src/memory/
├── mod.rs
├── memdump.rs
├── process_scanner.rs
└── key_extraction.rs
```

**AFU (After First Unlock) rationale:**

When a device is seized in a powered-on, unlocked state (AFU), the iOS Data Protection class keys and Android FBE credential-encrypted keys reside in volatile RAM. This is a well-established, lawfully used forensic technique. The window exists between first unlock and device power-down:

- **iOS AFU:** Class keys are loaded into kernel memory; memory imaging via jailbreak-enabled diagnostic channel or checkm8 (pre-A12) captures them before power-down
- **Android AFU:** FBE CE key held in kernel keyring; accessible via root + `/proc/<pid>/mem` scan of `vold` process

**Objectives:**
- AFU provider implements `AcquisitionSource` — outputs a memory image into AFF4 container
- Key material scanner: identify AES key schedules in process memory using Volatility-compatible signatures
- Extracted keys handed to the crypto layer for filesystem decryption
- **Operational note:** AFU capture requires device to be seized powered-on. Evidence handling SOP documented in `docs/recovery_guides/afu_handling.md`
- All memory access operations require supervisor-level case authorization; logged

---

### Week 9: Android Encryption & HITL Physical Interface

#### Day 1–3: Android FBE Key Derivation

**Files to create:**
```
crates/unirecover-crypto/src/android/
├── mod.rs
├── fbe.rs
├── keymaster.rs
├── gatekeeper.rs
├── keystore.rs
├── vold.rs
└── metadata_encryption.rs
```

**Objectives:**
- Parse `/data/misc/vold/user_keys/` from AFF4 image
- Extract wrapped CE (Credential Encrypted) and DE (Device Encrypted) keys
- Derive credential key from PIN/password via scrypt with device-stored N/r/p parameters
- Decrypt CE keyring to expose user data partition
- All derivation operations require case authorization; logged

#### Day 4–5: GPU-Accelerated Passcode Engine

**Files to create:**
```
crates/unirecover-crypto/src/bruteforce/
├── mod.rs
├── pin_generator.rs
├── pattern_generator.rs
├── dictionary.rs
├── gpu_accel.rs               # CUDA/OpenCL scrypt acceleration
└── distributed.rs
```

**Objectives:**
- 4-digit PIN: 10,000 combinations
- 6-digit PIN: 1,000,000 combinations
- Android pattern: 389,112 valid patterns (minimum 4-node)
- GPU-accelerated scrypt: 100,000+ derivations/sec on RTX-class hardware
- Distributed keyspace splitting via gRPC across multiple machines
- Every job requires case authorization; start, progress, and completion logged

#### Day 6–7: Hardware-in-the-Loop (HITL) Physical Interface Provider

**Files to create:**
```
hitl/
├── firmware/
│   ├── pico_hid_emulator/
│   │   ├── main.c             # Raspberry Pi Pico USB HID firmware
│   │   ├── timing.c           # Hardware-enforced delay management
│   │   └── CMakeLists.txt
│   └── fpga_interface/
│       └── timing_controller.v  # FPGA-based precise timing
├── schematics/
│   ├── pico_connection_diagram.pdf
│   └── usb_passthrough_board.pdf
├── README.md
└── calibration/
    └── delay_calibration.py   # Calibrate timing for specific device models
plugins/acquisition_providers/hitl_provider/
├── __init__.py
├── provider.py
└── device_profiles/
    ├── pixel_7.json
    ├── iphone_12.json
    └── samsung_s23.json
docs/hitl_guide.md
```

**HITL rationale and design:**

Hardware-enforced rate-limiting (iOS: 10 attempts then lockout/wipe; Android: exponential delays) cannot be defeated in software because the OS detects rapid automated attempts. The HITL approach sidesteps this entirely by operating at the **physical input layer** — the OS cannot distinguish a human typing from a precisely timed hardware emulator:

- A **Raspberry Pi Pico** (or custom FPGA board) is programmed to enumerate as a USB HID keyboard/touchscreen
- The device receives timed input signals exactly matching the hardware's expected human interaction latency window
- Hardware-enforced lockout delays (30 seconds, 1 minute, 5 minutes) are managed by the microcontroller's timing loop — it simply waits the enforced period and resumes
- The HITL provider connects to the orchestration server via USB serial; the passcode engine sends candidates; the microcontroller submits them to the device; the result (success/fail/lockout) is read back via screen state detection or ADB status

**Device profile system:** Each supported device model has a JSON profile specifying the lockout schedule, input timing parameters, screen state detection method, and wipe threshold. New device profiles are added without firmware changes.

**Objectives:**
- Pico firmware: USB HID enumeration, timing loop management, lockout delay handling
- FPGA variant: sub-millisecond precision for devices with strict timing requirements
- Orchestration server: receives PIN candidates from bruteforce engine, dispatches to HITL hardware, collects results
- Device profiles for common law enforcement targets (Pixel, iPhone, Samsung flagship)
- Calibration tool: `delay_calibration.py` measures device-specific input acceptance window
- Full audit logging: every attempt, result, and lockout event recorded
- **Scope note:** HITL operates on the device's own passcode verification — it does not extract keys directly. On success, the passcode is handed to the cryptographic derivation layer (Week 9, Day 1–3) which derives the actual encryption key

---

## Phase 5 — Plugin System & REST API (Weeks 10–11)

### Week 10: PyO3 Python Bindings & Plugin SDK

#### Day 1–3: Python Bindings

**Files to create:**
```
crates/unirecover-ffi/Cargo.toml
crates/unirecover-ffi/src/python/
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
- Build with `maturin` — `pip install unirecover`
- `RecoveryEngine` Python class: full pipeline access
- GIL release during long Rust operations
- Type stubs for IDE autocomplete
- Typed Python exceptions from Rust errors

#### Day 4–5: Vendor Plugin System

**Files to create:**
```
plugins/
├── base_plugin.py
├── plugin_manager.py
├── android_plugins/
│   ├── samsung_plugin.py          # Galaxy MediaStore + Secure Folder DB
│   ├── pixel_plugin.py            # Pixel-specific recovery paths
│   └── xiaomi_plugin.py           # MIUI gallery database
└── ios_plugins/
    └── photos_sqlite_plugin.py
```

**Objectives:**
- Plugin base class: `process(source: AcquisitionSource, case: CaseContext) -> List[CanonicalFileRecord]`
- All plugin output is `CanonicalFileRecord` — feeds into the unified evidence database
- Hot-reload for development; versioned loading for production
- Samsung: Galaxy MediaStore schema variants, Secure Folder database structure
- iOS: Photos.sqlite deleted records, face recognition tables, edit history

#### Day 6–7: Plugin SDK & Custom Parser Guide

**Files to create:**
```
plugins/sdk/
├── fs_parser_sdk.py
├── signature_sdk.py
├── acquisition_provider_sdk.py    # For writing new acquisition providers
└── examples/
    ├── custom_acquisition_provider.py
    ├── custom_fs_parser.py
    └── new_image_format.py
docs/plugin_development.md
```

**Objectives:**
- SDK for agency-developed plugins across all three layer types (ingestion, analysis, output)
- Example: write a new acquisition provider for a proprietary forensic hardware interface
- Example: Xiaomi EROFS partition parser
- Example: custom RAW format for agency-specific camera hardware
- Full API documentation with runnable examples

---

### Week 11: REST API Server & Deployment

#### Day 1–3: Actix-Web API Server

**Files to create:**
```
crates/unirecover-server/src/
├── main.rs
├── routes/
│   ├── acquisition.rs
│   ├── carving.rs
│   ├── results.rs
│   ├── export.rs
│   ├── plugins.rs
│   └── websocket.rs
├── auth.rs                    # mTLS + API key
└── middleware/
    ├── audit_middleware.rs    # Every API call → audit chain
    ├── logging.rs
    └── cors.rs
```

**Objectives:**
- RESTful API, JSON responses, OpenAPI/Swagger docs
- WebSocket for real-time job progress
- mTLS authentication for agency deployments
- Every API call logged: endpoint, operator, case ID, timestamp, result
- Rate limiting on passcode derivation endpoints

#### Day 4–5: Job Queue

**Files to create:**
```
crates/unirecover-server/src/queue/
├── redis_backend.rs
├── local_backend.rs
├── worker.rs
└── scheduler.rs
```

**Objectives:**
- Redis-backed job queue for multi-operator labs
- Job types: Acquire, Parse, Carve, Decrypt, HITL, Export
- Priority queue for active investigations
- Job persistence across restarts; partial result preservation on cancellation

#### Day 6–7: Docker & Air-Gap Deployment

**Files to create:**
```
Dockerfile
docker-compose.yml
docker-compose.airgap.yml
kubernetes/
├── deployment.yaml
├── service.yaml
└── network-policy.yaml       # Egress restriction for air-gapped ops
scripts/airgap_bundle.sh
```

**Objectives:**
- Multi-stage Docker build: musl static linking, minimal attack surface
- Air-gap bundle: packages all container images and dependencies for offline install
- Kubernetes network egress policies: no outbound connections in sensitive deployments
- Persistent volumes for case data and audit logs
- Resource limits preventing carving from starving audit log writes

---

## Phase 6 — Web UI (Weeks 12–13)

### Week 12: React Frontend

#### Day 1–3: Foundation & Case Management

**Files to create:**
```
web-ui/src/
├── main.tsx
├── App.tsx
├── api/
│   ├── client.ts
│   ├── websocket.ts
│   └── types.ts              # Types derived from CanonicalFileRecord
├── components/
│   ├── CaseManager.tsx
│   ├── OperatorAuth.tsx
│   └── AuditPanel.tsx
```

**Objectives:**
- Operator login before any case data is accessible
- Case creation: case number, investigator, authorizing supervisor, judicial reference
- Case dashboard: active cases, status, evidence item count
- Audit log panel: live-streaming append-only view
- Dark theme for forensic workstation environments

#### Day 4–5: Acquisition Interface

**Files to create:**
```
web-ui/src/pages/
├── Acquisition.tsx
├── components/
│   ├── ProviderSelector.tsx       # Shows available acquisition providers
│   ├── DeviceCard.tsx
│   ├── AFF4Progress.tsx           # AFF4 write progress + running hash
│   └── AcquisitionReport.tsx
```

**Objectives:**
- Provider selector: lists available acquisition modules (ADB, iOS, AFF4 import, HITL)
- AFF4 container write progress with running SHA-256 display
- Write-blocker status indicator
- Auto-generate acquisition report on completion: device info, dual hash, operator, timestamp

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
- Multi-select format targets
- Real-time per-format statistics
- Thumbnail gallery; EXIF panel on click
- Confidence filter slider
- Bulk export

---

### Week 13: Forensic Viewers & Evidence Export

#### Day 1–3: Analysis Viewers

**Files to create:**
```
web-ui/src/components/viewers/
├── HexViewer.tsx
├── DiskMap.tsx
├── FileSystemTree.tsx
├── TimelineView.tsx
├── MapView.tsx                    # GPS map, offline tile support
└── ComparisonView.tsx
```

**Objectives:**
- Hex viewer with header/footer highlights and carving match offsets
- Block allocation heatmap: allocated / unallocated / recovered / high-entropy (encrypted)
- Filesystem tree with deleted files flagged
- EXIF timeline and GPS map with offline tile support (no external network in air-gap)
- Side-by-side comparison: thumbnail vs recovered fragment

#### Day 4–5: Evidence Export

**Files to create:**
```
crates/unirecover-export/src/
├── dfxml.rs
├── aff4_export.rs             # Package results back into AFF4
├── pdf_report.rs
├── csv_export.rs
└── zip_export.rs
web-ui/src/pages/Export.tsx
```

**Objectives:**
- DFXML: standard interoperable forensic XML (compatible with Autopsy, AXIOM, UFED)
- AFF4 evidence package: recovered files + metadata + source container reference + audit log
- Case report PDF: cover page, evidence table, per-file metadata, chain-of-custody, hash table
- All exports signed with operator certificate, logged to audit chain
- Export access restricted to authorized case members

#### Day 6–7: Chain-of-Custody Dashboard

**Files to create:**
```
web-ui/src/pages/
├── AuditDashboard.tsx
├── ChainOfCustody.tsx
├── components/
│   ├── AuditTimeline.tsx
│   ├── OperatorActivity.tsx
│   └── IntegrityVerifier.tsx  # Re-verify AFF4 hash on demand
```

**Objectives:**
- Full audit timeline per case
- Operator activity report
- Chain-of-custody ledger: intake → acquisition → analysis → export, with digital signatures
- On-demand AFF4 hash re-verification: recompute and compare to logged value at any time
- Export signed CoC document as PDF for court submission

---

## Phase 7 — Validation, Security Hardening & Documentation (Week 14)

### Week 14

#### Day 1–3: NIST/CFTT Validation Suite

**Files to create:**
```
tests/validation/
├── nist_cftt_suite.rs
├── known_image_tests.rs
├── hash_verification_tests.rs
├── write_blocker_tests.rs
├── recovery_accuracy_tests.rs
└── aff4_integrity_tests.rs
scripts/run_validation.sh
docs/validation_report.md
```

**Objectives:**
- NIST CFTT reference images: verify recovery accuracy against known-content corpus
- Write-blocker validation: zero writes to any acquisition source across all test cases
- Hash consistency: AFF4 container hash must match re-computation 100%
- Recovery accuracy metrics: true positive rate, false positive rate, partial recovery rate
- Document all results in `validation_report.md` for funding body submission

#### Day 4–5: Security Hardening

**Files to create:**
```
crates/unirecover-core/src/security/
├── memory_protection.rs       # Zeroize key material after use
├── privilege_drop.rs
└── sandboxing.rs              # Seccomp for worker processes
```

**Objectives:**
- Zeroize all key material immediately after use (`zeroize` crate)
- Privilege separation: acquisition (root/admin) in isolated process; analysis unprivileged
- Seccomp filter for carving workers: read + compute syscalls only
- TLS 1.3 enforced for all API communication
- `cargo audit` in CI on every commit; vendored deps for air-gap builds

#### Day 6–7: Performance Benchmarks

**Files to create:**
```
benches/
├── full_pipeline_benchmark.rs
├── filesystem_benchmark.rs
└── carving_benchmark.rs
docs/performance_report.md
docs/operator_manual.md
docs/deployment_guide.md
```

**Objectives:**
- Full pipeline benchmark on 64 GB reference image: acquisition → carving → export
- Document throughput, memory usage, CPU utilization for funding proposal
- Operator manual: step-by-step from case creation to court report
- Deployment guide: Ubuntu 22.04/24.04, Windows WSL2, air-gapped environments

---

## Phase 8 — Integration, Release & Funding Package (Weeks 15–16)

### Week 15: Integration Testing & CI Pipeline

#### Day 1–3: End-to-End Tests

**Files to create:**
```
tests/integration/
├── android_e2e_test.rs
├── ios_e2e_test.rs
├── encrypted_device_test.rs
├── aff4_roundtrip_test.rs     # Acquire → AFF4 → re-open → analyze → export
├── air_gap_test.sh
└── court_report_test.rs
```

**Objectives:**
- End-to-end tests on reference device images
- AFF4 round-trip: acquire into AFF4, close, re-open as source, full analysis, export — verify hash integrity throughout
- Audit chain integrity across full case lifecycle
- Air-gap: confirm zero external network calls in airgap deployment
- Court report: validate PDF structure and required field presence

#### Day 4–7: Release Pipeline

**Files to create:**
```
.github/workflows/release.yml
.github/workflows/validation.yml
scripts/build_release.sh
scripts/sign_release.sh
CHANGELOG.md
```

**Objectives:**
- Cross-compile: Linux (x86_64, aarch64), macOS (arm64), Windows (x86_64)
- GPG-signed release artifacts
- Automated NIST CFTT validation on every release candidate
- Release notes with device compatibility matrix and known limitations per platform

---

### Week 16: Documentation, Legal Framework & Funding Package

#### Day 1–3: Documentation

**Files to create:**
```
docs/
├── operator_manual.md
├── deployment_guide.md
├── api_reference.md
├── plugin_development.md
├── court_admissibility.md
├── hitl_guide.md
├── validation_report.md
├── afu_handling.md            # Evidence handling SOP for AFU seizures
├── architecture.md
└── funding_proposal/
    ├── executive_summary.md
    ├── technical_specification.md
    ├── competitive_analysis.md
    ├── budget_breakdown.md
    └── roadmap_post_v1.md
```

**Objectives:**
- Operator manual: full step-by-step guide written for investigators without forensic software background
- HITL guide: hardware setup, device profile configuration, calibration procedure
- AFU handling SOP: evidence seizure procedures for live device scenarios
- Court admissibility guide: how UniRecover satisfies Daubert/Frye (reproducibility, audit trail, known error rate, validated against NIST corpus)
- Competitive analysis: Cellebrite UFED ($15k–$30k/unit), Magnet AXIOM ($5k–$15k/yr), Oxygen Forensic ($3k–$8k/yr) vs UniRecover (government license, auditable, extensible)

#### Day 4–5: Legal & Policy Framework

**Files to create:**
```
AUTHORIZED_USE_POLICY.md
CHAIN_OF_CUSTODY.md
docs/data_retention_policy.md
docs/export_control_notice.md
docs/privacy_impact_assessment_template.md
```

**Objectives:**
- Authorized use policy: tool requires lawful authority (warrant, court order, or equivalent) — unauthorized use is a criminal offence under applicable statutes
- Data retention: recovered evidence stored only for case duration; destruction procedure documented
- Export control notice: encryption components may be subject to export regulations
- Privacy impact assessment template for agency procurement process

#### Day 6–7: Final Release & Funding Submission

**Objectives:**
- Tag v1.0.0; publish signed binaries
- Assemble government funding proposal: executive summary, full technical spec, validation report, competitive analysis, budget, team CVs
- Demo environment: pre-loaded with synthetic reference case for funding body presentation
- Submit to applicable funding bodies: national law enforcement technology programs, justice department research grants, EU law enforcement innovation funds

---

## Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Core engine | Rust | Memory safety, zero-cost abstractions, fearless concurrency |
| SIMD acceleration | AVX2 / AVX-512 / NEON | 10 GB/s carving throughput |
| Async runtime | Tokio + io_uring | Non-blocking I/O for large images |
| Evidence format | AFF4 | Industry standard; integrity-hashed; logical+physical in one container |
| Python bindings | PyO3 + Maturin | Plugin SDK without sacrificing core performance |
| REST API | Actix-Web | Production-grade Rust web framework |
| Job queue | Redis | Persistent, multi-operator |
| Web UI | React + TypeScript + Vite | Modern, maintainable |
| Database | SQLite (per-case) | Portable, no server dependency, forensically auditable |
| Containerization | Docker + Kubernetes | Reproducible deployment; air-gap support |
| HITL hardware | Raspberry Pi Pico / FPGA | Physical input emulation for hardware rate-limit navigation |
| Audit log | HMAC-SHA256 chain | Tamper-evident; court-admissible |

---

## Encryption Tier Matrix

| Scenario | Method | Applies To | Notes |
|---|---|---|---|
| Known passcode | Direct key derivation | All devices | Fastest path |
| Short numeric PIN | Passcode engine (GPU) | All devices | 4-digit: seconds; 6-digit: minutes |
| Hardware rate-limited PIN | HITL physical interface | All devices | Navigates lockout delays via HID emulation |
| Device seized AFU (unlocked, powered on) | Memory capture | iOS + Android | Keys in RAM; requires immediate seizure action |
| Pre-A12 iPhone (checkm8 vulnerable) | Boot ROM exploit + memory | iPhone 5s–X | Established law enforcement technique |
| A12+ iPhone (Secure Enclave intact) | Secondary vectors + cloud warrant | iPhone XS+ | Hardware extraction not currently feasible |
| Android (rooted or engineering mode) | Direct FBE key extraction | Android | Root required |
| Android (no root, TEE intact) | HITL + scrypt derivation | Android | PIN space determines feasibility |
| Any device | Secondary storage, caches, sync artifacts | All devices | Always-available fallback |

---

## Compliance & Standards

- **NIST SP 800-101 Rev 1** — Guidelines on Mobile Device Forensics
- **ACPO Good Practice Guide** — Digital Evidence (UK)
- **ISO/IEC 27037** — Identification, collection, and preservation of digital evidence
- **SWGDE Best Practices** — Mobile Device Evidence
- **AFF4 Specification** — Advanced Forensic Format 4 (open standard)
- **RFC 3394** — AES Key Wrap Algorithm
- **DFXML** — Digital Forensics XML (MITRE)

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| iOS Secure Enclave revision (A12+) breaks crypto | Already present | High | Acknowledged in tier matrix; secondary vectors + HITL remain functional |
| Android StrongBox update restricts TEE access | Medium | Medium | HITL layer operates below OS; plugin update for new extraction paths |
| New device model requires HITL profile | High (routine) | Low | JSON device profile system; new profiles in days, no firmware change |
| Legal challenge to evidence admissibility | Low | High | NIST validation, AFF4 integrity, full audit chain, write-blocker compliance |
| AFF4 write performance bottleneck on slow media | Low | Medium | Chunked streaming writer; benchmarks in CI |
| HITL hardware unavailable in field | Medium | Medium | Software passcode engine as fallback; secondary vectors always available |

---

*UniRecover — Modular by design. Resilient by architecture. Validated for court.*
