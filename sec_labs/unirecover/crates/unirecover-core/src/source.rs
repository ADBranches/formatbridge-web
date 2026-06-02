use std::io::{Read, Seek};
use crate::error::Result;

#[derive(Debug, Clone)]
pub struct SourceDescriptor {
    pub source_id: String,
    pub acquisition_method: String,
    pub timestamp: String,
}

/// The critical trait guaranteeing cross-layer resilience.
/// Any parsed block device, AFF4 container, or decrypted stream implements this.
pub trait AcquisitionSource: Read + Seek + Send + Sync {
    fn size(&self) -> Result<u64>;
    fn block_size(&self) -> u64;
    fn sha256(&self) -> Result<[u8; 32]>;
    fn md5(&self) -> Result<[u8; 16]>;
    fn source_descriptor(&self) -> SourceDescriptor;
}

/// Allows live streaming data (AFU memory, ADB streams) to be ingested 
/// and written sequentially into an AFF4 container before being exposed 
/// as an AcquisitionSource for Layer 2 analysis.
pub trait StreamingSource: Read + Send + Sync {
    fn stream_descriptor(&self) -> SourceDescriptor;
}
