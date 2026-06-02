pub struct SensitiveKeyBuffer {
    pub raw_key: Vec<u8>,
}

impl Drop for SensitiveKeyBuffer {
    fn drop(&mut self) {
        for byte in self.raw_key.iter_mut() {
            *byte = 0;
        }
    }
}
