use std::io::{Read, Seek, Result as IoResult};
use unirecover_core::source::{AcquisitionSource, SourceDescriptor};
use crate::provider_registry::AcquisitionProvider;
use crate::unified_device_info::UnifiedDeviceInfo;
use unirecover_core::error::Result as CoreResult;

pub struct AdbStreamReader {
    descriptor: SourceDescriptor,
}

impl Read for AdbStreamReader {
    fn read(&mut self, _buf: &mut [u8]) -> IoResult<usize> {
        Ok(0) 
    }
}

impl Seek for AdbStreamReader {
    fn seek(&mut self, _pos: std::io::SeekFrom) -> IoResult<u64> {
        Ok(0)
    }
}

impl AcquisitionSource for AdbStreamReader {
    fn size(&self) -> CoreResult<u64> { Ok(0) }
    fn block_size(&self) -> u64 { 4096 }
    fn sha256(&self) -> CoreResult<[u8; 32]> { Ok([0; 32]) }
    fn md5(&self) -> CoreResult<[u8; 16]> { Ok([0; 16]) }
    fn source_descriptor(&self) -> SourceDescriptor { self.descriptor.clone() }
}

pub struct AdbAcquisitionProvider;

impl AcquisitionProvider for AdbAcquisitionProvider {
    fn name(&self) -> &'static str { "ADB_PROVIDER" }

    fn detect_devices(&self) -> CoreResult<Vec<UnifiedDeviceInfo>> {
        Ok(vec![UnifiedDeviceInfo {
            os_type: "Android".to_string(),
            version: "13.0".to_string(),
            serial_number: "ADB_TEST_SERIAL_01".to_string(),
            model: "Pixel 7 Pro".to_string(),
            encryption_state: "FBE_CE_LOCKED".to_string(),
            extraction_method: "Logical Partition Stream".to_string(),
        }])
    }

    fn execute_acquisition(&self, device_id: &str) -> CoreResult<Box<dyn AcquisitionSource>> {
        let desc = SourceDescriptor {
            source_id: device_id.to_string(),
            acquisition_method: "ADB_STREAM".to_string(),
            timestamp: "2026-05-30T12:00:00Z".to_string(),
        };
        Ok(Box::new(AdbStreamReader { descriptor: desc }))
    }
}
