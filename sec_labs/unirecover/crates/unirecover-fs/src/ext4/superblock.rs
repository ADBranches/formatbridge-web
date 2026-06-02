#[derive(Debug, Clone)]
pub struct Ext4Superblock {
    pub magic: u16,
    pub inodes_count: u32,
    pub blocks_count: u32,
    pub block_size_log2: u32,
}

impl Ext4Superblock {
    pub fn parse(bytes: &[u8]) -> Result<Self, &'static str> {
        if bytes.len() < 1024 { return Err("Buffer too small for EXT4 superblock parsing"); }
        
        let magic = u16::from_le_bytes(bytes[56..58].try_into().unwrap());
        if magic != 0xEF53 { return Err("Invalid EXT4 magic signature"); }

        let inodes_count = u32::from_le_bytes(bytes[0..4].try_into().unwrap());
        let blocks_count = u32::from_le_bytes(bytes[4..8].try_into().unwrap());
        let block_size_log2 = u32::from_le_bytes(bytes[24..28].try_into().unwrap());

        Ok(Self { magic, inodes_count, blocks_count, block_size_log2 })
    }
}
