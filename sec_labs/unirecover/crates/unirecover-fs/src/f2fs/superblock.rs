#[derive(Debug, Clone)]
pub struct F2fsSuperblock {
    pub magic: u32,
    pub log_sectors_per_block: u32,
    pub log_blocks_per_segment: u32,
}

impl F2fsSuperblock {
    pub fn parse(bytes: &[u8]) -> Result<Self, &'static str> {
        if bytes.len() < 100 { return Err("F2FS structure tracking space too small"); }
        
        let magic = u32::from_le_bytes(bytes[0..4].try_into().unwrap());
        if magic != 0xF2F52010 { return Err("Invalid F2FS magic identifier signature"); }

        Ok(Self {
            magic,
            log_sectors_per_block: u32::from_le_bytes(bytes[4..8].try_into().unwrap()),
            log_blocks_per_segment: u32::from_le_bytes(bytes[8..12].try_into().unwrap()),
        })
    }
}
