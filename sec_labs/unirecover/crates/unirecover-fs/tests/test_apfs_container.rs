use unirecover_core::source::{AcquisitionSource, SourceDescriptor};
use unirecover_core::error::Result as CoreResult;
use unirecover_fs::apfs::container::ApfsContainerContext;
use std::io::{Read, Seek, Cursor};

pub struct MockAcquisitionStream {
    pub memory_backing: Cursor<Vec<u8>>,
}

impl Read for MockAcquisitionStream {
    fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
        self.memory_backing.read(buf)
    }
}

impl Seek for MockAcquisitionStream {
    fn seek(&mut self, pos: std::io::SeekFrom) -> std::io::Result<u64> {
        self.memory_backing.seek(pos)
    }
}

impl AcquisitionSource for MockAcquisitionStream {
    fn size(&self) -> CoreResult<u64> { Ok(8192) }
    fn block_size(&self) -> u64 { 4096 }
    fn sha256(&self) -> CoreResult<[u8; 32]> { Ok([0; 32]) }
    fn md5(&self) -> CoreResult<[u8; 16]> { Ok([0; 16]) }
    fn source_descriptor(&self) -> SourceDescriptor {
        SourceDescriptor {
            source_id: "MOCK_STREAM".to_string(),
            acquisition_method: "VIRTUAL_IMAGE".to_string(),
            timestamp: "2026-05-30T17:00:00Z".to_string(),
        }
    }
}

#[test]
fn test_apfs_container_validation_flow() {
    // Create an 8KB image stream to account for offset reads comfortably
    let mut blank_raw_block = vec![0u8; 8192];
    
    // ApfsContainerContext seeks to 32 and reads 4096 bytes.
    // The NxSuperblock::parse functions reads from the start of that read buffer.
    // Therefore, NXSB needs to be at absolute index 32 within the stream.
    blank_raw_block[32..36].copy_from_slice(b"NXSB");
    
    // Inject mock Block Size configuration at block offset 32 (absolute byte 64)
    blank_raw_block[64..68].copy_from_slice(&4096u32.to_le_bytes()); 

    let mut mock_source = MockAcquisitionStream {
        memory_backing: Cursor::new(blank_raw_block),
    };
    
    let container = ApfsContainerContext::initialize(&mut mock_source);
    assert!(container.is_ok(), "Container initialization failed parsing block layout");
    assert_eq!(&container.unwrap().superblock.magic, b"NXSB");
}
