#!/bin/bash
set -e
echo "Executing NIST CFTT Forensic Validation Suite..."
cargo test --workspace --release
