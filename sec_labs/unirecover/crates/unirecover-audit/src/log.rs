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
