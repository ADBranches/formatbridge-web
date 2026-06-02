pub struct ExtentHeader {
    pub entries_count: u16,
    pub max_entries_count: u16,
    pub depth: u16,
}

pub struct ExtentLeafNode {
    pub block_index: u32,
    pub block_length: u16,
    pub start_physical_block: u64,
}
