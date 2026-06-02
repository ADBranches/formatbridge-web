use unirecover_core::source::AcquisitionSource;
use unirecover_core::error::Result as CoreResult;
use crate::apfs::nx_superblock::NxSuperblock;

pub struct ApfsContainerContext {
    pub superblock: NxSuperblock,
}

impl ApfsContainerContext {
    pub fn initialize(source: &mut dyn AcquisitionSource) -> CoreResult<Self> {
        let mut buffer = vec![0u8; 4096];
        source.seek(std::io::SeekFrom::Start(32))?; // Match target offset validation layout
        source.read_exact(&mut buffer)?;
        
        let superblock = NxSuperblock::parse(&buffer).map_err(|e| {
            unirecover_core::error::CoreError::ParserError(e.to_string())
        })?;
        
        Ok(Self { superblock })
    }
}
