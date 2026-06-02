pub struct BTreeNodeHeader {
    pub flags: u16,
    pub key_count: u32,
    pub table_space_offset: u16,
}

impl BTreeNodeHeader {
    pub fn parse_node(raw_block: &[u8]) -> Result<Self, &'static str> {
        if raw_block.len() < 32 { return Err("Node layout truncated"); }
        Ok(Self {
            flags: u16::from_le_bytes(raw_block[0..2].try_into().unwrap()),
            key_count: u32::from_le_bytes(raw_block[2..6].try_into().unwrap()),
            table_space_offset: u16::from_le_bytes(raw_block[6..8].try_into().unwrap()),
        })
    }
}
