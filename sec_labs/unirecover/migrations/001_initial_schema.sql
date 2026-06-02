CREATE TABLE IF NOT EXISTS evidence_records (
    file_hash TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    operator_id TEXT NOT NULL,
    source_aff4_ref TEXT NOT NULL,
    block_offset INTEGER NOT NULL,
    byte_size INTEGER NOT NULL,
    confidence REAL NOT NULL,
    audit_ref TEXT NOT NULL,
    recovered_at TEXT NOT NULL
);
