pub struct GatekeeperEnrollmentRecord {
    pub user_id: u32,
    pub hashed_password: Vec<u8>,
    pub salt: u64,
}
