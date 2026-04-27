# Document Alterations Checklist (Professional Alignment)

> **Purpose:** Ensure your written work matches **correct standards** and the implemented system.

## A) FATF terminology fixes (must-do)
Replace any wording like:
- “FATF Rule 11” → **FATF Recommendation 11 (R.11) — Record Keeping**
- “FATF Rule 16” → **FATF Recommendation 16 (R.16) — Payment Transparency / Travel Rule**
- “FATF Rule 10” → **FATF Recommendation 10 (R.10) — Customer Due Diligence**

## B) Performance KPI wording (must-do)
In your report, write performance results as two lines:
1. **Capacity / throughput**: “X requests/sec sustained under load; 0% error rate.”
2. **Batch test**: “1000 transactions completed in Y seconds.”

> This prevents confusion when a Locust run lasts longer than 5 seconds but proves throughput.

## C) GDPR retention statement (confirm)
If you claim “automated 30-day erasure”:
- explicitly show the purge mechanism (cron/job/db scheduled procedure)
- document it in `docs/compliance/gdpr-controls.md` and link to code/script.

If purge is not implemented, write:
- “Retention policies configured; purge disabled by default in MVP.”

## D) Evidence packaging statement (must-do)
Include references to:
- `tests/evidence/phase7_1/`
- `tests/evidence/phase7_2/`
- `tests/evidence/phase7_3/`

and describe how the evidence was produced (scripts).

## E) Final consistency checklist
- Report chapters match implemented services
- Diagrams match endpoints
- Terminology matches FATF official naming
- Benchmarks match KPI definitions
