import { apiRequest } from "./apiClient";

export async function uploadFiles(files) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  return apiRequest("/uploads", {
    method: "POST",
    body: formData,
  });
}