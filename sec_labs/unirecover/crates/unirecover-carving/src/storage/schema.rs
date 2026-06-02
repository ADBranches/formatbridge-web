pub struct EvidenceRecordDescriptor {
    pub file_hash: String,
    pub case_id: String,
    pub source_aff4_ref: String,
    pub block_offset: u64,
    pub byte_size: u64,
    pub extraction_confidence: f32,
    pub audit_ref: String,
}
