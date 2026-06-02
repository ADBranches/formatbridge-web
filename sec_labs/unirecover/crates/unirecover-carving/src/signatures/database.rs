use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct FileSignature {
    pub name: String,
    pub extension: String,
    pub header: Vec<u8>,
    pub footer: Option<Vec<u8>>,
}
