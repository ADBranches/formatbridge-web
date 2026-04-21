import { formatFileSize, getFileExtension } from "../utils/fileHelpers";

export default function FileCard({ file, onRemove }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="truncate text-sm font-semibold text-slate-900">
            {file.name}
          </h3>
          <p className="mt-1 text-xs text-slate-500">
            Extension: {getFileExtension(file.name).toUpperCase() || "Unknown"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Type: {file.type || "Unknown"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Size: {formatFileSize(file.size)}
          </p>
        </div>

        <button
          type="button"
          onClick={onRemove}
          className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:bg-slate-50"
        >
          Remove
        </button>
      </div>
    </div>
  );
}