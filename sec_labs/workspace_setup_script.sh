#!/bin/bash

echo "[*] Initializing UniRecover Workspace..."
mkdir -p unirecover
cd unirecover

echo "[*] Creating directory structure..."
mkdir -p crates/unirecover-core/src
mkdir -p crates/unirecover-audit/src
mkdir -p crates/unirecover-acquisition/src/{aff4,sources}
mkdir -p crates/unirecover-acquisition/benches
mkdir -p .github/workflows

# ==========================================
# 1. ROOT WORKSPACE & METADATA
# ==========================================
echo "[*] Populating Root Files..."

cat << 'EOF' > Cargo.toml
[workspace]
members = [
    "crates/unirecover-core",
    "crates/unirecover-audit",
    "crates/unirecover-acquisition"
]
resolver = "2"

[profile.release]
opt-level = 3
lto = "fat"
codegen-units = 1
panic = "abort"
EOF

cat << 'EOF' > rust-toolchain.toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
EOF

cat << 'EOF' > AUTHORIZED_USE_POLICY.md
# Authorized Use Policy

**WARNING:** UniRecover is a restricted-use framework designed exclusively for authorized digital forensics, incident response, and law enforcement operations. 
By compiling or executing this software, you attest that you have explicit, documented legal authorization (e.g., a warrant, court order, or signed consent) to process the target data. Unauthorized access to computer systems or mobile devices is a criminal offense under applicable cybercrime legislation.
EOF

cat << 'EOF' > .github/workflows/ci.yml
name: UniRecover CI
on: [push, pull_request]
jobs:
  build_and_test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: cargo clippy --workspace -- -D warnings
      - run: cargo test --workspace
EOF

# ==========================================
# 2. CORE CRATE (unirecover-core)
# ==========================================
echo "[*] Populating unirecover-core..."

cat << 'EOF' > crates/unirecover-core/Cargo.toml
[package]
name = "unirecover-core"
version = "0.1.0"
edition = "2021"

[dependencies]
thiserror = "1.0"
EOF

cat << 'EOF' > crates/unirecover-core/src/lib.rs
pub mod error;
pub mod source;
EOF

cat << 'EOF' > crates/unirecover-core/src/error.rs
use thiserror::Error;

#[derive(Error, Debug)]
pub enum CoreError {
    #[error("I/O Error: {0}")]
    Io(#[from] std::io::Error),
    #[error("Invalid source descriptor")]
    InvalidDescriptor,
    #[error("Write blocked by hardware/software policy")]
    WriteBlocked,
    #[error("Audit validation failed: {0}")]
    AuditFailure(String),
}

pub type Result<T> = std::result::Result<T, CoreError>;
EOF

cat << 'EOF' > crates/unirecover-core/src/source.rs
use std::io::{Read, Seek};
use crate::error::Result;

#[derive(Debug, Clone)]
pub struct SourceDescriptor {
    pub source_id: String,
    pub acquisition_method: String,
    pub timestamp: String,
}

/// The critical trait guaranteeing cross-layer resilience.
/// Any parsed block device, AFF4 container, or decrypted stream implements this.
pub trait AcquisitionSource: Read + Seek + Send + Sync {
    fn size(&self) -> Result<u64>;
    fn block_size(&self) -> u64;
    fn sha256(&self) -> Result<[u8; 32]>;
    fn md5(&self) -> Result<[u8; 16]>;
    fn source_descriptor(&self) -> SourceDescriptor;
}

/// Allows live streaming data (AFU memory, ADB streams) to be ingested 
/// and written sequentially into an AFF4 container before being exposed 
/// as an AcquisitionSource for Layer 2 analysis.
pub trait StreamingSource: Read + Send + Sync {
    fn stream_descriptor(&self) -> SourceDescriptor;
}
EOF

# ==========================================
# 3. AUDIT CRATE (unirecover-audit)
# ==========================================
echo "[*] Populating unirecover-audit..."

cat << 'EOF' > crates/unirecover-audit/Cargo.toml
[package]
name = "unirecover-audit"
version = "0.1.0"
edition = "2021"

[dependencies]
unirecover-core = { path = "../unirecover-core" }
hmac = "0.12"
sha2 = "0.10"
chrono = "0.4"
EOF

cat << 'EOF' > crates/unirecover-audit/src/lib.rs
pub mod chain;
pub mod log;
pub mod operator;
EOF

cat << 'EOF' > crates/unirecover-audit/src/log.rs
use hmac::{Hmac, Mac};
use sha2::Sha256;
use std::fs::{File, OpenOptions};
use std::io::Write;
use chrono::Utc;

type HmacSha256 = Hmac<Sha256>;

pub struct AuditLedger {
    file: File,
    last_hash: [u8; 32],
    secret_key: Vec<u8>,
}

impl AuditLedger {
    pub fn new(path: &str, case_id: &str, secret_key: &[u8]) -> std::io::Result<Self> {
        let file = OpenOptions::new().create(true).append(true).open(path)?;
        let mut ledger = Self {
            file,
            last_hash: [0; 32], // Origin hash
            secret_key: secret_key.to_vec(),
        };
        ledger.append("SYSTEM", case_id, "Ledger Initialized")?;
        Ok(ledger)
    }

    pub fn append(&mut self, operator_id: &str, case_id: &str, action: &str) -> std::io::Result<()> {
        let timestamp = Utc::now().to_rfc3339();
        let payload = format!("{}|{}|{}|{}|{:?}", timestamp, operator_id, case_id, action, self.last_hash);
        
        let mut mac = HmacSha256::new_from_slice(&self.secret_key).expect("HMAC can take key of any size");
        mac.update(payload.as_bytes());
        let result = mac.finalize();
        let current_hash: [u8; 32] = result.into_bytes().into();
        
        let log_entry = format!("{}|HASH:{:?}\n", payload, current_hash);
        self.file.write_all(log_entry.as_bytes())?;
        self.last_hash = current_hash;
        
        Ok(())
    }
}
EOF

cat << 'EOF' > crates/unirecover-audit/src/operator.rs
#[derive(Debug, Clone)]
pub struct OperatorContext {
    pub operator_id: String,
    pub case_id: String,
    pub judicial_authorization: String,
}
EOF

cat << 'EOF' > crates/unirecover-audit/src/chain.rs
// Stub for the Chain of Custody logic
pub struct ChainOfCustodyRecord {
    pub item_id: String,
    pub current_custodian: String,
    pub transfer_history: Vec<String>,
}
EOF

# ==========================================
# 4. ACQUISITION CRATE (unirecover-acquisition)
# ==========================================
echo "[*] Populating unirecover-acquisition..."

cat << 'EOF' > crates/unirecover-acquisition/Cargo.toml
[package]
name = "unirecover-acquisition"
version = "0.1.0"
edition = "2021"

[dependencies]
unirecover-core = { path = "../unirecover-core" }
unirecover-audit = { path = "../unirecover-audit" }
memmap2 = "0.7"
EOF

cat << 'EOF' > crates/unirecover-acquisition/src/lib.rs
pub mod aff4;
pub mod sources;
pub mod mmap_pool;
pub mod chunked_reader;
EOF

cat << 'EOF' > crates/unirecover-acquisition/src/aff4/mod.rs
pub mod container;
pub mod integrity;
pub mod map;
pub mod metadata;
pub mod stream;
pub mod writer;
EOF

cat << 'EOF' > crates/unirecover-acquisition/src/sources/mod.rs
pub mod block_device;
pub mod disk_image;
pub mod memory;
pub mod traits;
EOF

cat << 'EOF' > crates/unirecover-acquisition/src/mmap_pool.rs
// Stub for Memory-Mapped pool optimized for multi-threading
EOF

cat << 'EOF' > crates/unirecover-acquisition/src/chunked_reader.rs
// Stub for Large >1TB Chunked Hashing Engine
EOF

# Create stub benchmark files
echo "// Benchmarks will go here" > crates/unirecover-acquisition/benches/read_benchmark.rs
echo "// MMAP benchmarks will go here" > crates/unirecover-acquisition/benches/mmap_benchmark.rs

# Stub AFF4 internals so the crate compiles
for f in container integrity map metadata stream writer; do
    echo "// AFF4 $f implementation" > crates/unirecover-acquisition/src/aff4/$f.rs
done

# Stub source internals
for f in block_device disk_image memory traits; do
    echo "// Source $f implementation" > crates/unirecover-acquisition/src/sources/$f.rs
done

echo "[*] Verifying workspace compiles..."
cargo check --workspace

echo "[*] Phase 1 Environment successfully built."
