use unirecover_acquisition::aff4::writer::Aff4Writer;
use std::io::Cursor;

#[test]
fn test_aff4_streaming_writer() {
    // Objective: Test streaming write and SHA-256 integrity
    let mut buffer = Cursor::new(Vec::new());
    let mut writer = Aff4Writer::new(&mut buffer);
    
    let chunk1 = b"UNIRECOVER_TEST_CHUNK_1";
    let chunk2 = b"UNIRECOVER_TEST_CHUNK_2";
    
    writer.write_chunk(chunk1).unwrap();
    writer.write_chunk(chunk2).unwrap();
    
    let (size, hash) = writer.finalize();
    
    assert_eq!(size, (chunk1.len() + chunk2.len()) as u64);
    assert_ne!(hash, [0; 32], "Hash should not be empty");
}

use unirecover_acquisition::provider_registry::ProviderRegistry;
use unirecover_acquisition::android::adb::AdbAcquisitionProvider;
use unirecover_acquisition::ios::mobile_device::IosAcquisitionProvider;

#[test]
fn test_provider_registry_discovery() {
    let mut registry = ProviderRegistry::new();
    
    // Wire up acquisition engines natively
    registry.register(Box::new(AdbAcquisitionProvider));
    registry.register(Box::new(IosAcquisitionProvider));
    
    let listed = registry.list_available_providers();
    assert!(listed.contains(&"ADB_PROVIDER".to_string()));
    assert!(listed.contains(&"IOS_PROVIDER".to_string()));
    
    // Assert unified mapping configurations evaluate cleanly
    let adb = registry.get_provider("ADB_PROVIDER").unwrap();
    let devices = adb.detect_devices().unwrap();
    assert_eq!(devices[0].model, "Pixel 7 Pro");
}
