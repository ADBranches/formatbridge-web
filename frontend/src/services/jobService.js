import { apiRequest } from "./apiClient";

export async function createConversionJob(filePublicIds, outputFormat, ocrEnabled = false) {
  return apiRequest("/conversions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      file_public_ids: filePublicIds,
      output_format: outputFormat,
      ocr_enabled: ocrEnabled,
    }),
  });
}

export async function fetchJobStatus(jobPublicId) {
  return apiRequest(`/jobs/${jobPublicId}`, {
    method: "GET",
  });
}