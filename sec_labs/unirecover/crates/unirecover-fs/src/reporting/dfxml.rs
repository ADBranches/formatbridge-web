pub struct DfxmlReportGenerator;

impl DfxmlReportGenerator {
    pub fn generate_xml_header(case_id: &str, operator_id: &str) -> String {
        format!(
            r#"<?xml version="1.0" encoding="UTF-8"?>
<dfxml xmloutputversion="1.0">
  <creator>
    <program>UniRecover</program>
    <version>0.1.0</version>
  </creator>
  <configuration>
    <case_id>{}</case_id>
    <operator_id>{}</operator_id>
  </configuration>
  <source>"#,
            case_id, operator_id
        )
    }

    pub fn append_file_node(hash: &str, path: &str, size: u64, confidence: f32) -> String {
        format!(
            r#"
    <fileobject>
      <filename>{}</filename>
      <filesize>{}</filesize>
      <hashdigest type="sha256">{}</hashdigest>
      <confidence>{}</confidence>
    </fileobject>"#,
            path, size, hash, confidence
        )
    }

    pub fn generate_xml_footer() -> String {
        "\n  </source>\n</dfxml>".to_string()
    }
}
