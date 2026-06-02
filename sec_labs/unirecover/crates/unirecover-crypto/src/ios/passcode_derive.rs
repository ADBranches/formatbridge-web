use hmac::Hmac;
use sha2::Sha256;

pub struct PasscodeDeriver;

impl PasscodeDeriver {
    pub fn pbkdf2_derive_with_uid(passcode: &str, salt: &[u8]) -> Vec<u8> {
        let mut derived_key = vec![0u8; 32];
        let iterations = 10000;
        pbkdf2::pbkdf2::<Hmac<Sha256>>(passcode.as_bytes(), salt, iterations, &mut derived_key).unwrap_or_default();
        derived_key
    }
}
