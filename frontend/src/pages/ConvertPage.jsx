import { useMemo, useState } from "react";
import ConversionSummary from "../components/conversion/ConversionSummary";
import FormatSelector from "../components/conversion/FormatSelector";
import JobStatusCard from "../components/jobs/JobStatusCard";
import UploadDropzone from "../components/upload/UploadDropzone";
import FileCard from "../components/upload/FileCard";
import useJobPolling from "../hooks/useJobPolling";
import { formatFileSize, validateFilesClientSide } from "../utils/fileHelpers";
import { createConversionJob } from "../services/jobService";
import { uploadFiles } from "../services/uploadService";

const MAX_FILES = 10;
const OUTPUT_OPTIONS = ["jpg", "png", "webp", "pdf", "docx"];

export default function ConvertPage() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [clientErrors, setClientErrors] = useState([]);
  const [serverError, setServerError] = useState("");
  const [uploadResult, setUploadResult] = useState(null);
  const [jobCreationError, setJobCreationError] = useState("");
  const [jobId, setJobId] = useState("");
  const [outputFormat, setOutputFormat] = useState("pdf");
  const [isUploading, setIsUploading] = useState(false);
  const [isCreatingJob, setIsCreatingJob] = useState(false);

  const { jobPayload, pollingError, isPolling } = useJobPolling(Boolean(jobId) ? jobId : null);

  const totalSize = useMemo(
    () => selectedFiles.reduce((sum, file) => sum + file.size, 0),
    [selectedFiles]
  );

  const handleFilesAdded = (incomingFiles) => {
    const mergedFiles = [...selectedFiles, ...incomingFiles].slice(0, MAX_FILES);
    const validation = validateFilesClientSide(mergedFiles);

    setSelectedFiles(validation.validFiles);
    setClientErrors(validation.errors);
    setServerError("");
    setUploadResult(null);
    setJobCreationError("");
    setJobId("");
  };

  const handleRemove = (targetIndex) => {
    const nextFiles = selectedFiles.filter((_, index) => index !== targetIndex);
    const validation = validateFilesClientSide(nextFiles);

    setSelectedFiles(validation.validFiles);
    setClientErrors(validation.errors);
  };

  const handleUpload = async () => {
    setServerError("");
    setUploadResult(null);
    setJobCreationError("");
    setJobId("");

    if (!selectedFiles.length) {
      setServerError("Please select at least one file before uploading.");
      return;
    }

    const validation = validateFilesClientSide(selectedFiles);
    if (validation.errors.length) {
      setClientErrors(validation.errors);
      return;
    }

    try {
      setIsUploading(true);
      const response = await uploadFiles(selectedFiles);
      setUploadResult(response);
    } catch (error) {
      setServerError(error.message || "Upload failed.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleCreateJob = async () => {
    setJobCreationError("");
    setJobId("");

    const uploadedFiles = uploadResult?.data?.files || [];
    if (!uploadedFiles.length) {
      setJobCreationError("Upload files first before creating a conversion job.");
      return;
    }

    try {
      setIsCreatingJob(true);
      const response = await createConversionJob(
        uploadedFiles.map((file) => file.public_id),
        outputFormat
      );

      const createdJobId = response?.data?.job?.public_id;
      setJobId(createdJobId || "");
    } catch (error) {
      setJobCreationError(error.message || "Failed to create conversion job.");
    } finally {
      setIsCreatingJob(false);
    }
  };

  const handleClear = () => {
    setSelectedFiles([]);
    setClientErrors([]);
    setServerError("");
    setUploadResult(null);
    setJobCreationError("");
    setJobId("");
  };

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Upload and Convert Files
          </h1>
          <p className="mt-2 text-slate-600">
            Phase 5 adds PDF generation, merged PDF export, and downloadable results.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.95fr]">
          <div className="space-y-6">
            <UploadDropzone
              onFilesAdded={handleFilesAdded}
              maxFiles={MAX_FILES}
              disabled={isUploading || isCreatingJob}
            />

            {clientErrors.length > 0 && (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                <h2 className="text-sm font-semibold text-amber-700">
                  Client-side validation issues
                </h2>
                <ul className="mt-2 ml-5 list-disc space-y-1 text-sm text-amber-700">
                  {clientErrors.map((error, index) => (
                    <li key={`${error}-${index}`}>{error}</li>
                  ))}
                </ul>
              </div>
            )}

            {serverError && (
              <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                {serverError}
              </div>
            )}

            {jobCreationError && (
              <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                {jobCreationError}
              </div>
            )}

            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900">
                    Selected files
                  </h2>
                  <p className="mt-1 text-sm text-slate-500">
                    {selectedFiles.length} file(s) · {formatFileSize(totalSize)}
                  </p>
                </div>

                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={handleClear}
                    disabled={isUploading || isCreatingJob}
                    className="rounded-xl border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    Clear
                  </button>

                  <button
                    type="button"
                    onClick={handleUpload}
                    disabled={isUploading || isCreatingJob || selectedFiles.length === 0}
                    className="rounded-xl bg-brand-600 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {isUploading ? "Uploading..." : "Upload files"}
                  </button>
                </div>
              </div>

              <div className="mt-6 grid gap-4">
                {selectedFiles.length === 0 ? (
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-sm text-slate-500">
                    No files selected yet.
                  </div>
                ) : (
                  selectedFiles.map((file, index) => (
                    <FileCard
                      key={`${file.name}-${index}`}
                      file={file}
                      onRemove={() => handleRemove(index)}
                    />
                  ))
                )}
              </div>
            </div>

            {uploadResult && (
              <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6 shadow-sm">
                <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
                  <div>
                    <h2 className="text-lg font-semibold text-emerald-800">
                      Upload successful
                    </h2>
                    <p className="mt-2 text-sm text-emerald-700">
                      {uploadResult.message}
                    </p>
                  </div>

                  <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
                    <FormatSelector
                      value={outputFormat}
                      onChange={setOutputFormat}
                      options={OUTPUT_OPTIONS}
                      disabled={isCreatingJob}
                    />

                    <button
                      type="button"
                      onClick={handleCreateJob}
                      disabled={isCreatingJob}
                      className="rounded-xl bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      {isCreatingJob ? "Creating job..." : "Create conversion job"}
                    </button>
                  </div>
                </div>

                <div className="mt-4 space-y-3">
                  {uploadResult.data.files.map((file) => (
                    <div
                      key={file.public_id}
                      className="rounded-2xl border border-emerald-200 bg-white p-4 text-sm"
                    >
                      <p className="font-medium text-slate-900">
                        {file.original_filename}
                      </p>
                      <p className="mt-1 text-slate-600">Stored as: {file.stored_filename}</p>
                      <p className="mt-1 text-slate-600">Public ID: {file.public_id}</p>
                      <p className="mt-1 text-slate-600">MIME: {file.mime_type}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <aside className="space-y-6">
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-semibold text-slate-900">
                Phase 5 rules
              </h2>

              <ul className="mt-4 space-y-3 text-sm text-slate-600">
                <li>Single image -> one PDF</li>
                <li>Multiple images -> one merged PDF</li>
                <li>Image order is preserved in the merged PDF</li>
                <li>Worker writes a downloadable PDF result row</li>
              </ul>
            </div>

            
            {jobId && (
              <div className="rounded-3xl border border-brand-200 bg-brand-50 p-4 text-sm text-brand-700">
                <p>
                  Tracking job: <span className="font-semibold break-all">{jobId}</span>
                  {isPolling && <span className="ml-2">• polling...</span>}
                </p>

                <div className="mt-3">
                  <a
                    href={`/results/${jobId}`}
                    className="inline-flex rounded-xl bg-white px-4 py-2 text-sm font-semibold text-slate-900 shadow-sm ring-1 ring-slate-200 transition hover:bg-slate-50"
                  >
                    Open results page
                  </a>
                </div>
              </div>
            )}
            <JobStatusCard
              job={jobPayload?.job}
              results={jobPayload?.results || []}
              pollingError={pollingError}
            />

            <ConversionSummary
              job={jobPayload?.job}
              results={jobPayload?.results || []}
            />
          </aside>
        </div>
      </section>
    </main>
  );
}