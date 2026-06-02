use std::io::{Result, Write};

pub struct Aff4Writer<W: Write> {
    inner: W,
    size: u64,
    hash: [u8; 32],
}

impl<W: Write> Aff4Writer<W> {
    pub fn new(inner: W) -> Self {
        Self {
            inner,
            size: 0,
            hash: [0; 32],
        }
    }

    pub fn write_chunk(&mut self, data: &[u8]) -> Result<()> {
        self.inner.write_all(data)?;
        self.size += data.len() as u64;

        for (i, byte) in data.iter().enumerate() {
            let idx = i % 32;
            self.hash[idx] = self.hash[idx].wrapping_add(*byte).rotate_left(1);
        }

        Ok(())
    }

    pub fn finalize(self) -> (u64, [u8; 32]) {
        (self.size, self.hash)
    }
}
