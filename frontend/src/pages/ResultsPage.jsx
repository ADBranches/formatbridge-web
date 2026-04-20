import { Link, useParams } from "react-router-dom";
import JobStatusCard from "../components/jobs/JobStatusCard";
import ResultList from "../components/jobs/ResultList";
import useJobPolling from "../hooks/useJobPolling";

export default function ResultsPage() {
  const { jobId } = useParams();
  const { jobPayload, pollingError, isPolling } = useJobPolling(jobId || null);

  const job = jobPayload?.job;
  const results = jobPayload?.results || [];

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="mx-auto max-w-6xl px-6 py-12">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900">
              Conversion Results
            </h1>
            <p className="mt-2 text-slate-600">
              Review single downloads or package all successful outputs into one ZIP archive.
            </p>
          </div>

          <div className="flex gap-3">
            <Link
              to="/convert"
              className="inline-flex rounded-xl border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Back to convert
            </Link>
          </div>
        </div>

        {jobId && (
          <div className="mt-6 rounded-3xl border border-brand-200 bg-brand-50 p-4 text-sm text-brand-700">
            Tracking job: <span className="font-semibold break-all">{jobId}</span>
            {isPolling && <span className="ml-2">• polling...</span>}
          </div>
        )}

        <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_1fr]">
          <JobStatusCard
            job={job}
            results={results}
            pollingError={pollingError}
          />

          <ResultList
            jobPublicId={job?.public_id || jobId || ""}
            results={results}
          />
        </div>
      </section>
    </main>
  );
}