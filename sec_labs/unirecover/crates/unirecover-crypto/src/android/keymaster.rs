#[derive(Debug, Clone)]
pub struct KeymasterBlob {
    pub version: u32,
    pub encrypted_key: Vec<u8>,
}

pub struct KeymasterParser;

impl KeymasterParser {
    pub fn parse_blob(data: &[u8]) -> Option<KeymasterBlob> {
        if data.is_empty() {
            return None;
        }

        Some(KeymasterBlob {
            version: 1,
            encrypted_key: data.to_vec(),
        })
    }
}
