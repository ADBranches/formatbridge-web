import { useEffect, useState } from "react";
import { apiRequest } from "../services/apiClient";
import authStore from "../store/authStore";

export default function HistoryPage() {
  const [jobs, setJobs] = useState([]);
  const [historyError, setHistoryError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const token = authStore.getToken();
  const currentUser = authStore.getUser();

  useEffect(() => {
    const loadHistory = async () => {
      try {
        setIsLoading(true);
        setHistoryError("");

        const response = await apiRequest("/jobs/history", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setJobs(response?.data?.jobs || []);
      } catch (error) {
        setHistoryError(error.message || "Failed to load conversion history.");
      } finally {
        setIsLoading(false);
      }
    };

    loadHistory();
  }, [token]);

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Conversion History
          </h1>
          <p className="mt-2 text-slate-600">
            Signed-in users can review past conversion jobs linked to their account.
          </p>
          {currentUser && (
            <p className="mt-2 text-sm text-slate-500">
              Signed in as <span className="font-medium text-slate-800">{currentUser.email}</span>
            </p>
          )}
        </div>

        {isLoading && (
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm text-sm text-slate-600">
            Loading history...
          </div>
        )}

        {historyError && (
          <div className="rounded-3xl border border-red-200 bg-red-50 p-6 shadow-sm text-sm text-red-700">
            {historyError}
          </div>
        )}

        {!isLoading && !historyError && (
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            {jobs.length === 0 ? (
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
                No conversion history found yet.
              </div>
            ) : (
              <div className="space-y-4">
                {jobs.map((job) => (
                  <div
                    key={job.public_id}
                    className="rounded-2xl border border-slate-200 p-4"
                  >
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div>
                        <p className="text-sm font-semibold text-slate-900">
                          Job ID: {job.public_id}
                        </p>
                        <p className="mt-1 text-xs text-slate-600">
                          Output: {job.requested_output_format?.toUpperCase()} · Status: {job.status}
                        </p>
                      </div>

                      <a
                        href={`/results/${job.public_id}`}
                        className="inline-flex rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"
                      >
                        Open results
                      </a>
                    </div>

                    <div className="mt-3 grid gap-3 md:grid-cols-3 text-sm text-slate-600">
                      <p>Sources: {job.source_count}</p>
                      <p>OCR: {job.ocr_enabled ? "Enabled" : "Disabled"}</p>
                      <p>Created: {job.created_at}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}