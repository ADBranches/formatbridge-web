function StatusBadge({ status }) {
  const normalized = (status || "").toLowerCase();

  const classes =
    normalized === "success"
      ? "bg-emerald-100 text-emerald-700 border-emerald-200"
      : normalized === "failed"
      ? "bg-red-100 text-red-700 border-red-200"
      : normalized === "processing"
      ? "bg-amber-100 text-amber-700 border-amber-200"
      : "bg-slate-100 text-slate-700 border-slate-200";

  return (
    <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold ${classes}`}>
      {status || "unknown"}
    </span>
  );
}

export default function JobStatusCard({ job, results = [], pollingError = "" }) {
  if (!job) return null;

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Conversion job
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Track asynchronous job state from the worker.
          </p>
        </div>

        <StatusBadge status={job.status} />
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Job ID</p>
          <p className="mt-1 break-all text-sm font-medium text-slate-900">
            {job.public_id}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Target format</p>
          <p className="mt-1 text-sm font-medium text-slate-900">
            {job.requested_output_format?.toUpperCase()}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Source count</p>
          <p className="mt-1 text-sm font-medium text-slate-900">{job.source_count}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Results tracked</p>
          <p className="mt-1 text-sm font-medium text-slate-900">{results.length}</p>
        </div>
      </div>

      {job.error_message && (
        <div className="mt-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {job.error_message}
        </div>
      )}

      {pollingError && (
        <div className="mt-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {pollingError}
        </div>
      )}

      <div className="mt-6 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
        <p><span className="font-medium text-slate-900">Created:</span> {job.created_at}</p>
        <p className="mt-1"><span className="font-medium text-slate-900">Started:</span> {job.started_at || "Not yet started"}</p>
        <p className="mt-1"><span className="font-medium text-slate-900">Completed:</span> {job.completed_at || "Not yet completed"}</p>
      </div>
    </div>
  );
}