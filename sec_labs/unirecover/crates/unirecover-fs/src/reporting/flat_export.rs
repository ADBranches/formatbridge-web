use serde_json::json;

pub struct FlatExportEngine;

impl FlatExportEngine {
    pub fn format_as_json_string(hash: &str, path: &str, size: u64, audit_ref: &str) -> String {
        json!({
            "file_hash": hash,
            "extracted_path": path,
            "byte_size": size,
            "audit_reference": audit_ref,
            "export_status": "VERIFIED"
        }).to_string()
    }

    pub fn format_as_csv_line(hash: &str, path: &str, size: u64, confidence: f32) -> String {
        format!("{},{},{},{}\n", hash, path, size, confidence)
    }
}
