const API_BASE_URL = "http://127.0.0.1:5000/api/v1";

function buildSingleDownloadUrl(resultId) {
  return `${API_BASE_URL}/downloads/results/${resultId}`;
}

function buildZipDownloadUrl(jobPublicId) {
  return `${API_BASE_URL}/downloads/jobs/${jobPublicId}/zip`;
}

export default function ResultList({ jobPublicId, results = [] }) {
  const successfulResults = results.filter((result) => result.status === "success");
  const failedResults = results.filter((result) => result.status === "failed");

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Downloadable outputs
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Download single results or bundle all successful outputs into one ZIP file.
          </p>
        </div>

        {jobPublicId && successfulResults.length > 0 && (
          <a
            href={buildZipDownloadUrl(jobPublicId)}
            className="inline-flex rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"
          >
            Download ZIP
          </a>
        )}
      </div>

      <div className="mt-6 space-y-4">
        {successfulResults.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
            No successful results available yet.
          </div>
        ) : (
          successfulResults.map((result) => (
            <div
              key={result.id}
              className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4"
            >
              <p className="text-sm font-semibold text-slate-900">
                {result.output_filename || `Result ${result.id}`}
              </p>
              <p className="mt-1 text-xs text-slate-600">
                Format: {result.output_format?.toUpperCase()}
              </p>

              <div className="mt-4">
                <a
                  href={buildSingleDownloadUrl(result.id)}
                  className="inline-flex rounded-xl bg-white px-4 py-2 text-sm font-semibold text-slate-900 shadow-sm ring-1 ring-slate-200 transition hover:bg-slate-50"
                >
                  Download result
                </a>
              </div>
            </div>
          ))
        )}

        {failedResults.length > 0 && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-4">
            <h3 className="text-sm font-semibold text-red-700">
              Failed outputs
            </h3>
            <ul className="mt-2 space-y-2 text-sm text-red-700">
              {failedResults.map((result) => (
                <li key={result.id}>
                  {result.output_filename || `Result ${result.id}`} — {result.status}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}