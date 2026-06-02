pub struct WorkChunk {
    pub chunk_id: u64,
    pub absolute_offset: u64,
    pub data: Vec<u8>,
}

pub struct StreamChunker {
    pub chunk_size: usize,
    pub overlap_size: usize,
}

impl StreamChunker {
    pub fn new() -> Self {
        Self {
            chunk_size: 64 * 1024 * 1024,   // 64 MB Default Allocation
            overlap_size: 64 * 1024,        // 64 KB Boundary Slip Guard
        }
    }
}
