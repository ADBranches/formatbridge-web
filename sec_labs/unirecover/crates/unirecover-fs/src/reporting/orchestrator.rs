use crate::reporting::dfxml::DfxmlReportGenerator;
use std::io::Write;

pub struct ReportingOrchestrator {
    pub active_case_id: String,
}

impl ReportingOrchestrator {
    pub fn new(case_id: &str) -> Self {
        Self { active_case_id: case_id.to_string() }
    }

    pub fn stream_report_to_writer<W: Write>(&self, writer: &mut W) -> std::io::Result<()> {
        let header = DfxmlReportGenerator::generate_xml_header(&self.active_case_id, "FORENSIC_OFFICER");
        writer.write_all(header.as_bytes())?;
        
        // Emulate streaming records directly out of the processing pool
        let mock_node = DfxmlReportGenerator::append_file_node(
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "DCIM/Camera/IMG_0001.JPG",
            204857,
            0.95
        );
        writer.write_all(mock_node.as_bytes())?;

        let footer = DfxmlReportGenerator::generate_xml_footer();
        writer.write_all(footer.as_bytes())?;
        Ok(())
    }
}
