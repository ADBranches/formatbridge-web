use crate::apfs::constants::*;

#[derive(Debug, Clone)]
pub struct NxSuperblock {
    pub magic: [u8; 4],
    pub block_size: u32,
    pub block_count: u64,
    pub features: u64,
    pub omap_oid: u64,
    pub xp_desc_blocks: u32,
    pub xp_desc_base: u64,
}

impl NxSuperblock {
    pub fn parse(bytes: &[u8]) -> Result<Self, &'static str> {
        if bytes.len() < 128 {
            return Err("Buffer too small for NXSB parsing");
        }
        
        let mut magic = [0u8; 4];
        magic.copy_from_slice(&bytes[0..4]);
        
        if &magic != APFS_NX_SIGNATURE {
            return Err("Invalid NXSB block magic signature");
        }

        let block_size = u32::from_le_bytes(bytes[32..36].try_into().unwrap());
        let block_count = u64::from_le_bytes(bytes[40..48].try_into().unwrap());
        let features = u64::from_le_bytes(bytes[48..56].try_into().unwrap());
        let omap_oid = u64::from_le_bytes(bytes[64..72].try_into().unwrap());
        let xp_desc_blocks = u32::from_le_bytes(bytes[80..84].try_into().unwrap());
        let xp_desc_base = u64::from_le_bytes(bytes[88..96].try_into().unwrap());

        Ok(NxSuperblock {
            magic,
            block_size,
            block_count,
            features,
            omap_oid,
            xp_desc_blocks,
            xp_desc_base,
        })
    }
}
