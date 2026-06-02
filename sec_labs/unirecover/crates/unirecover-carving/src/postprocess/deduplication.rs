use std::collections::HashSet;

pub struct ForensicDeduplicator {
    pub processed_hashes: HashSet<[u8; 32]>,
}

impl ForensicDeduplicator {
    pub fn new() -> Self {
        Self { processed_hashes: HashSet::new() }
    }

    pub fn is_exact_duplicate(&mut self, sha256_hash: [u8; 32]) -> bool {
        !self.processed_hashes.insert(sha256_hash)
    }
}
