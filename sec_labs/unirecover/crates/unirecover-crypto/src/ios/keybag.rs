#[derive(Debug, Clone)]
pub struct AppleSystemKeybag {
    pub version: u32,
    pub keybag_type: u32,
    pub uuid: [u8; 16],
}

impl AppleSystemKeybag {
    pub fn parse_binary_blob(raw_bytes: &[u8]) -> Result<Self, &'static str> {
        if raw_bytes.len() < 40 { return Err("Keybag binary stream truncated"); }
        
        let version = u32::from_le_bytes(raw_bytes[0..4].try_into().unwrap());
        let keybag_type = u32::from_le_bytes(raw_bytes[4..8].try_into().unwrap());
        let mut uuid = [0u8; 16];
        uuid.copy_from_slice(&raw_bytes[8..24]);

        Ok(Self { version, keybag_type, uuid })
    }
}
