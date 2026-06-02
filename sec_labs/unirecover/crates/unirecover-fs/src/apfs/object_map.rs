pub struct ObjectMapTable {
    pub omap_id: u64,
}

impl ObjectMapTable {
    pub fn resolve_physical_block(&self, _virtual_oid: u64, _transaction_id: u64) -> Option<u64> {
        Some(0)
    }
}
