pub struct PinKeyspaceIterator {
    current: u32,
    max: u32,
}

impl PinKeyspaceIterator {
    pub fn new(digits: u32) -> Self {
        let max = if digits == 6 { 1_000_000 } else { 10_000 };
        Self { current: 0, max }
    }
}

impl Iterator for PinKeyspaceIterator {
    type Item = String;
    fn next(&mut self) -> Option<Self::Item> {
        if self.current >= self.max { return None; }
        let val = format!("{:04}", self.current);
        self.current += 1;
        Some(val)
    }
}
