use std::fs::{File, OpenOptions};
use std::io::{self, Read, Seek, SeekFrom};
#[cfg(target_os = "linux")]
use std::os::unix::fs::OpenOptionsExt;
use unirecover_core::error::{CoreError, Result};
use unirecover_core::source::{AcquisitionSource, SourceDescriptor};

pub struct BlockDeviceReader {
    file: File,
    descriptor: SourceDescriptor,
    size: u64,
}

impl BlockDeviceReader {
    /// Opens a block device (e.g., /dev/loop0) strictly read-only.
    /// In Linux, applies O_DIRECT to bypass page cache and prevent host RAM poisoning.
    pub fn open(path: &str, descriptor: SourceDescriptor) -> Result<Self> {
        let mut options = OpenOptions::new();
        options.read(true);
        options.write(false); // Explicit Software Write-Blocker

        #[cfg(target_os = "linux")]
        options.custom_flags(libc::O_DIRECT);

        let file = options.open(path).map_err(CoreError::Io)?;
        let size = file.metadata().map_err(CoreError::Io)?.len();

        Ok(Self { file, descriptor, size })
    }
}

impl Read for BlockDeviceReader {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        self.file.read(buf)
    }
}

impl Seek for BlockDeviceReader {
    fn seek(&mut self, pos: SeekFrom) -> io::Result<u64> {
        self.file.seek(pos)
    }
}

impl AcquisitionSource for BlockDeviceReader {
    fn size(&self) -> Result<u64> { Ok(self.size) }
    fn block_size(&self) -> u64 { 4096 }
    fn sha256(&self) -> Result<[u8; 32]> { Ok([0; 32]) } // Stubbed for full disk hash
    fn md5(&self) -> Result<[u8; 16]> { Ok([0; 16]) }
    fn source_descriptor(&self) -> SourceDescriptor { self.descriptor.clone() }
}
