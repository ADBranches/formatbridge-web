use std::io::{Read, Seek, Result as IoResult};
use unirecover_core::source::{AcquisitionSource, SourceDescriptor};
use crate::provider_registry::AcquisitionProvider;
use crate::unified_device_info::UnifiedDeviceInfo;
use unirecover_core::error::Result as CoreResult;

pub struct IosNativeReader {
    descriptor: SourceDescriptor,
}

impl Read for IosNativeReader {
    fn read(&mut self, _buf: &mut [u8]) -> IoResult<usize> { Ok(0) }
}
impl Seek for IosNativeReader {
    fn seek(&mut self, _pos: std::io::SeekFrom) -> IoResult<u64> { Ok(0) }
}
impl AcquisitionSource for IosNativeReader {
    fn size(&self) -> CoreResult<u64> { Ok(0) }
    fn block_size(&self) -> u64 { 4096 }
    fn sha256(&self) -> CoreResult<[u8; 32]> { Ok([0; 32]) }
    fn md5(&self) -> CoreResult<[u8; 16]> { Ok([0; 16]) }
    fn source_descriptor(&self) -> SourceDescriptor { self.descriptor.clone() }
}

pub struct IosAcquisitionProvider;

impl AcquisitionProvider for IosAcquisitionProvider {
    fn name(&self) -> &'static str { "IOS_PROVIDER" }

    fn detect_devices(&self) -> CoreResult<Vec<UnifiedDeviceInfo>> {
        Ok(vec![UnifiedDeviceInfo {
            os_type: "iOS".to_string(),
            version: "16.4".to_string(),
            serial_number: "IOS_UDID_TEST_99X".to_string(),
            model: "iPhone 14 Pro Max".to_string(),
            encryption_state: "DataProtection_ClassKey_Loaded".to_string(),
            extraction_method: "AFC File Connection".to_string(),
        }])
    }

    fn execute_acquisition(&self, device_id: &str) -> CoreResult<Box<dyn AcquisitionSource>> {
        let desc = SourceDescriptor {
            source_id: device_id.to_string(),
            acquisition_method: "LIBIMOBILEDEVICE_AFC".to_string(),
            timestamp: "2026-05-30T12:05:00Z".to_string(),
        };
        Ok(Box::new(IosNativeReader { descriptor: desc }))
    }
}
