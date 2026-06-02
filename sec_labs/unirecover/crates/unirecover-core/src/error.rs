use thiserror::Error;

#[derive(Error, Debug)]
pub enum CoreError {
    #[error("I/O Error: {0}")]
    Io(#[from] std::io::Error),
    #[error("Invalid source descriptor")]
    InvalidDescriptor,
    #[error("Write blocked by hardware/software policy")]
    WriteBlocked,
    #[error("Audit validation failed: {0}")]
    AuditFailure(String),
    #[error("Parser Engine Failure: {0}")]
    ParserError(String),
}

pub type Result<T> = std::result::Result<T, CoreError>;
