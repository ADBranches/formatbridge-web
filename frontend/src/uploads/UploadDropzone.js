import { useCallback } from "react";
import { useDropzone } from "react-dropzone";

const ACCEPTED_TYPES = {
  "image/heic": [".heic"],
  "image/heif": [".heif"],
  "image/jpeg": [".jpg", ".jpeg"],
  "image/png": [".png"],
  "image/webp": [".webp"],
  "image/gif": [".gif"],
};

export default function UploadDropzone({
  onFilesAdded,
  maxFiles = 10,
  disabled = false,
}) {
  const handleDrop = useCallback(
    (acceptedFiles) => {
      if (!acceptedFiles.length) return;
      onFilesAdded(acceptedFiles);
    },
    [onFilesAdded]
  );

  const { getRootProps, getInputProps, isDragActive, fileRejections } =
    useDropzone({
      onDrop: handleDrop,
      accept: ACCEPTED_TYPES,
      multiple: true,
      maxFiles,
      disabled,
    });

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`rounded-3xl border-2 border-dashed p-8 text-center transition ${
          isDragActive
            ? "border-brand-600 bg-brand-50"
            : "border-slate-300 bg-white hover:border-brand-500"
        } ${disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer"}`}
      >
        <input {...getInputProps()} />

        <div className="mx-auto max-w-2xl">
          <h2 className="text-xl font-semibold text-slate-900">
            Drag and drop files here
          </h2>

          <p className="mt-2 text-sm text-slate-600">
            Supported formats: HEIC, HEIF, JPG, JPEG, PNG, WEBP, GIF
          </p>

          <p className="mt-1 text-sm text-slate-500">
            You can upload up to {maxFiles} files at once.
          </p>

          <div className="mt-6">
            <span className="inline-flex rounded-xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-sm">
              Choose files
            </span>
          </div>
        </div>
      </div>

      {fileRejections.length > 0 && (
        <div className="rounded-2xl border border-red-200 bg-red-50 p-4">
          <h3 className="text-sm font-semibold text-red-700">
            Some files were rejected by the browser picker
          </h3>

          <ul className="mt-2 space-y-2 text-sm text-red-600">
            {fileRejections.map((entry, index) => (
              <li key={`${entry.file.name}-${index}`}>
                <span className="font-medium">{entry.file.name}</span>
                <ul className="ml-5 mt-1 list-disc">
                  {entry.errors.map((error) => (
                    <li key={error.code}>{error.message}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}