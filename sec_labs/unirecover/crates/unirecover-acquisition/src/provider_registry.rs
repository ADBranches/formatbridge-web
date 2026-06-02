use std::collections::HashMap;
use unirecover_core::source::AcquisitionSource;
use crate::unified_device_info::UnifiedDeviceInfo;
use unirecover_core::error::Result;

pub trait AcquisitionProvider: Send + Sync {
    fn name(&self) -> &'static str;
    fn detect_devices(&self) -> Result<Vec<UnifiedDeviceInfo>>;
    fn execute_acquisition(&self, device_id: &str) -> Result<Box<dyn AcquisitionSource>>;
}

pub struct ProviderRegistry {
    providers: HashMap<String, Box<dyn AcquisitionProvider>>,
}

impl ProviderRegistry {
    pub fn new() -> Self {
        Self { providers: HashMap::new() }
    }

    pub fn register(&mut self, provider: Box<dyn AcquisitionProvider>) {
        self.providers.insert(provider.name().to_string(), provider);
    }

    pub fn get_provider(&self, name: &str) -> Option<&Box<dyn AcquisitionProvider>> {
        self.providers.get(name)
    }
    
    pub fn list_available_providers(&self) -> Vec<String> {
        self.providers.keys().cloned().collect()
    }
}
