const API_BASE_URL = "http://127.0.0.1:5000/api/v1";

function buildDownloadUrl(resultId) {
  return `${API_BASE_URL}/downloads/results/${resultId}`;
}

export default function ConversionSummary({ job, results = [] }) {
  if (!job) return null;

  const successfulResults = results.filter((result) => result.status === "success");
  const failedResults = results.filter((result) => result.status === "failed");

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Conversion summary
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Review generated outputs and download completed results.
          </p>
        </div>

        <span className="inline-flex rounded-full border border-slate-200 bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
          {job.requested_output_format?.toUpperCase()}
        </span>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Job status</p>
          <p className="mt-1 text-sm font-medium text-slate-900">{job.status}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Successful outputs</p>
          <p className="mt-1 text-sm font-medium text-slate-900">
            {successfulResults.length}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 p-4">
          <p className="text-xs uppercase tracking-wide text-slate-500">Failed outputs</p>
          <p className="mt-1 text-sm font-medium text-slate-900">
            {failedResults.length}
          </p>
        </div>
      </div>

      <div className="mt-6 space-y-4">
        {successfulResults.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
            No downloadable outputs yet.
          </div>
        ) : (
          successfulResults.map((result) => (
            <div
              key={result.id}
              className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4"
            >
              <p className="text-sm font-semibold text-slate-900">
                {result.output_filename || "Generated output"}
              </p>
              <p className="mt-1 text-xs text-slate-600">
                Format: {result.output_format?.toUpperCase()}
              </p>

              <div className="mt-4">
                <a
                  href={buildDownloadUrl(result.id)}
                  className="inline-flex rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"
                >
                  Download result
                </a>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}