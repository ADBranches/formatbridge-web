pub enum HardwareVectorTarget {
    Avx512,
    Avx2,
    Neon,
    ScalarFallback,
}

pub fn detect_supported_architecture() -> HardwareVectorTarget {
    if is_x86_feature_detected!("avx512f") {
        HardwareVectorTarget::Avx512
    } else if is_x86_feature_detected!("avx2") {
        HardwareVectorTarget::Avx2
    } else {
        // Fallback for non-x86 or ARM target compilation layouts
        HardwareVectorTarget::ScalarFallback
    }
}
