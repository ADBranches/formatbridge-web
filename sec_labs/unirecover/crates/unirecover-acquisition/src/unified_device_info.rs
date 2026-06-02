use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UnifiedDeviceInfo {
    pub os_type: String,         // "Android" or "iOS"
    pub version: String,         // OS Version string
    pub serial_number: String,   // ADB Serial or iOS UDID
    pub model: String,           // Device model designation
    pub encryption_state: String,// "DE", "CE", "Encrypted", "Unlocked"
    pub extraction_method: String,
}
