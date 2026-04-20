import { useEffect, useState } from "react";
import { fetchJobStatus } from "../services/jobService";

const TERMINAL_STATUSES = new Set(["success", "failed"]);
const DEFAULT_INTERVAL_MS = 2000;

export default function useJobPolling(jobId, enabled = true, intervalMs = DEFAULT_INTERVAL_MS) {
  const [jobPayload, setJobPayload] = useState(null);
  const [pollingError, setPollingError] = useState("");
  const [isPolling, setIsPolling] = useState(false);

  useEffect(() => {
    if (!jobId || !enabled) return;

    let intervalId;
    let cancelled = false;

    const poll = async () => {
      try {
        setIsPolling(true);
        const payload = await fetchJobStatus(jobId);

        if (cancelled) return;

        setJobPayload(payload.data);
        setPollingError("");

        const status = payload?.data?.job?.status;
        if (TERMINAL_STATUSES.has(status)) {
          clearInterval(intervalId);
          setIsPolling(false);
        }
      } catch (error) {
        if (cancelled) return;
        setPollingError(error.message || "Failed to fetch job status.");
        clearInterval(intervalId);
        setIsPolling(false);
      }
    };

    poll();
    intervalId = window.setInterval(poll, intervalMs);

    return () => {
      cancelled = true;
      clearInterval(intervalId);
    };
  }, [jobId, enabled, intervalMs]);

  return {
    jobPayload,
    pollingError,
    isPolling,
  };
}