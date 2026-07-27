# Edwin Sprint 4 Backend Timeline — Automated Database Image Cleanup Script

> Project: Car Dealership  
> Sprint: Sprint 4  
> Assigned Developer: Edwin  
> Sprint Role: Backend APIs  
> Assigned Task: Automated Database Image Cleanup Script

---

## 1. Sprint 4 Assignment Summary

Edwin’s Sprint 4 backend assignment is to build an automated database image cleanup mechanism.

The task goal is to keep server storage clean by wiping orphan or stale media data.

The backend should provide a scheduled background function, cron job, or utility script that scans the database for car listings marked as `Draft` or `Deleted` for longer than 30 days and strips or removes their associated media links from the storage bucket.

The implementation must be safe, inspect-first, and should avoid deleting active inventory media.

---

## 2. Clear Final Objective

Build a safe backend cleanup system that:

- Finds car listings marked `Draft` or `Deleted` for more than 30 days.
- Identifies media/image links associated with those stale listings.
- Removes or prepares removal of those media links from storage.
- Cleans or updates related database records only when safe.
- Avoids touching active, available, sold, or recently edited listings.
- Runs manually first through dry-run mode before any scheduled deletion is enabled.
- Avoids committing or exposing storage credentials.

---

## 3. Implementation Principles

Before modifying code in any phase:

1. Confirm the active branch.
2. Pull latest changes from the correct remote branch.
3. Confirm the working tree is clean.
4. Inspect the backend structure before adding files.
5. Inspect current database queries before writing cleanup queries.
6. Avoid creating duplicate backend servers.
7. Avoid hardcoding a storage provider.
8. Default cleanup behavior to dry-run mode.
9. Never delete media from active listings.
10. Keep cleanup query logic, storage logic, and scheduling logic modular.
11. Add repeatable manual tests before enabling scheduling.
12. Commit only files relevant to each phase.

Recommended Sprint 4 branch:

```bash
feature/edwin-sprint4-image-cleanup
```

---

# Phase 0 — Backend Storage And Schema Inspection

## Objective

Inspect the current backend structure, car schema, image/media storage approach, and existing route/model logic before implementing cleanup behavior.

## Files/Directories In This Phase

```text
backend/
backend/server.js
backend/package.json
backend/config/db.js
backend/models/carsModel.js
backend/controllers/carsController.js
backend/routes/carsRoutes.js
backend/.env.example
src/tests/
README.md
package.json
```

## Items To Inspect

```text
Active backend entrypoint
Current car model structure
Current image/media table or collection
Existing image URL field names
Existing status values
Existing timestamp fields
Existing storage provider references
Existing cron or job infrastructure
```

## Search Targets

```text
Draft
Deleted
car_images
image_url
images
storage
bucket
cloudinary
s3
firebase
supabase
cron
node-cron
```

## Done Criteria

- Active backend entrypoint is confirmed.
- Current car/image database structure is understood.
- Existing image/media table or field is identified.
- Existing status and timestamp fields are identified.
- Existing storage provider status is known or confirmed as pending.
- No files are modified in this phase.

---

# Phase 1 — Cleanup Contract Definition

## Objective

Define the exact rules for selecting stale listings and media records for cleanup.

## Files/Directories In This Phase

```text
backend/models/carsModel.js
backend/services/
backend/utils/
backend/.env.example
README.md
```

## Cleanup Contract

A car listing is eligible for cleanup only when:

```text
status is Draft or Deleted
AND listing has remained in that state for more than 30 days
AND listing has associated media/image links
```

## Candidate Fields To Confirm

```text
status
created_at
updated_at
deleted_at
drafted_at
car_id
image_url
images
```

## Expected Behavior

- `Draft` listings newer than 30 days must be skipped.
- `Deleted` listings newer than 30 days must be skipped.
- `Available`, `Sold`, active, or published listings must be skipped.
- Listings without media should be handled safely.

## Done Criteria

- Cleanup eligibility rules are defined.
- Status filters are confirmed as `Draft` and `Deleted`.
- Age threshold is confirmed as 30 days.
- Candidate timestamp field is selected.
- Cleanup behavior is documented before destructive logic is written.

---

# Phase 2 — Stale Car Media Query Service

## Objective

Create a read-only backend service that identifies stale Draft/Deleted cars and their associated media records.

## Files/Directories In This Phase

```text
backend/services/
backend/services/staleCarMediaService.js
backend/models/carsModel.js
backend/config/db.js
```

## Planned Functions

```text
findStaleCarMediaCandidates(options)
getStaleCarMediaSummary(options)
```

## Suggested Options

```js
{
  olderThanDays: 30,
  statuses: ["Draft", "Deleted"],
  limit: 100
}
```

## Expected Behavior

The service should query for:

- Draft cars older than 30 days.
- Deleted cars older than 30 days.
- Associated media/image links.
- Candidate records only, without deleting anything.

## Done Criteria

- Read-only service exists.
- Service can identify stale cleanup candidates.
- Service returns structured candidate data.
- No storage deletion occurs.
- No database deletion occurs.

---

# Phase 3 — Storage Cleanup Adapter

## Objective

Create a provider-safe storage cleanup adapter without hardcoding Cloudinary, S3, Firebase, Supabase, or another storage provider.

## Files/Directories In This Phase

```text
backend/services/
backend/services/storageCleanupService.js
backend/config/
backend/.env.example
```

## Provider Possibilities

```text
pending
cloudinary
s3
firebase
supabase
local
other team-approved provider
```

## Planned Functions

```text
getStorageProvider()
deleteMediaObject(mediaUrl, options)
deleteMediaBatch(mediaItems, options)
```

## Safety Rule

If the provider is not confirmed, the adapter must not delete anything.

It should return a safe skipped response, such as:

```js
{
  deleted: false,
  skipped: true,
  reason: "Storage provider is not configured."
}
```

## Done Criteria

- Storage cleanup adapter exists.
- Provider is read from environment variables.
- No credentials are hardcoded.
- Unknown provider defaults to safe skip behavior.
- No real storage deletion happens until provider is confirmed.

---

# Phase 4 — Main Car Image Cleanup Service

## Objective

Create the main orchestration service that combines stale listing discovery with storage cleanup and database media-link cleanup.

## Files/Directories In This Phase

```text
backend/services/
backend/services/carImageCleanupService.js
backend/services/staleCarMediaService.js
backend/services/storageCleanupService.js
backend/models/carsModel.js
backend/config/db.js
```

## Planned Main Function

```text
cleanupStaleCarImages(options)
```

## Suggested Options

```js
{
  dryRun: true,
  olderThanDays: 30,
  statuses: ["Draft", "Deleted"],
  limit: 100
}
```

## Expected Behavior

The cleanup service should:

- Find stale Draft/Deleted listings.
- Find associated media/image records.
- Skip active listings.
- Support dry-run mode.
- Call storage cleanup adapter only when safe.
- Clean database links only when deletion succeeds or where team-approved.
- Return a structured cleanup summary.

## Done Criteria

- Main cleanup service exists.
- Dry-run mode is supported.
- Cleanup summary is returned.
- Active listings are skipped.
- No irreversible deletion occurs by default.

---

# Phase 5 — Database Media Link Removal Logic

## Objective

Add model-level functions to remove, mark, or detach image/media links after safe cleanup.

## Files/Directories In This Phase

```text
backend/models/carsModel.js
backend/models/
backend/services/carImageCleanupService.js
backend/config/db.js
```

## Possible Model Functions

```text
removeCarImageLinks(carId)
markCarImagesCleaned(carId)
deleteCarImageRecords(carId)
deleteCarImageRecordById(imageId)
```

## Safety Requirements

Database image cleanup should only happen when:

- `dryRun` is false.
- The listing is eligible.
- The media item belongs to a Draft or Deleted listing older than 30 days.
- Storage cleanup is skipped safely or completed successfully according to agreed policy.

## Done Criteria

- Model-level cleanup functions exist.
- Cleanup functions are limited to eligible stale listings.
- Active listing media cannot be removed by these functions.
- Dry-run mode does not mutate the database.

---

# Phase 6 — Manual Cleanup Script

## Objective

Create a repeatable script that teammates can run manually before enabling any cron job or scheduler.

## Files/Directories In This Phase

```text
backend/scripts/
backend/scripts/cleanupStaleCarImages.js
backend/services/carImageCleanupService.js
backend/package.json
```

## Suggested Commands

```bash
node backend/scripts/cleanupStaleCarImages.js --dry-run
node backend/scripts/cleanupStaleCarImages.js --execute
```

## Expected Output

```text
cleanup mode
olderThanDays value
statuses scanned
stale listings found
media links found
media links skipped
media links cleaned
errors encountered
startedAt
finishedAt
```

## Safety Requirements

- Dry-run should be the default.
- Execute mode should require an explicit flag.
- Script should print clear results.
- Script should not expose credentials.

## Done Criteria

- Manual cleanup script exists.
- Dry-run command works.
- Execute command requires explicit flag.
- Script output is structured and understandable.
- Teammates can repeat the cleanup check safely.

---

# Phase 7 — Scheduled Cleanup Job

## Objective

Add a scheduler-ready cleanup job or cron wrapper for automated background cleanup.

## Files/Directories In This Phase

```text
backend/jobs/
backend/jobs/cleanupStaleCarImagesJob.js
backend/services/carImageCleanupService.js
backend/server.js
backend/package.json
backend/.env.example
```

## Scheduling Options

Option A:

```text
Use node-cron inside backend process.
```

Option B:

```text
Use scheduler-ready script and let the deployment platform run it.
```

## Recommended Professional Approach

Start with scheduler-ready script support first.

Enable automatic cron only after the deployment owner confirms:

- Hosting platform
- Scheduler responsibility
- Runtime safety
- Production storage provider
- Secrets management

## Suggested Defaults

```text
CLEANUP_CRON_ENABLED=false
CLEANUP_CRON_SCHEDULE=0 2 * * *
CLEANUP_DRY_RUN=true
```

## Done Criteria

- Cleanup job file exists.
- Job uses the main cleanup service.
- Scheduling is disabled by default.
- Cron behavior is environment-driven.
- No cleanup runs automatically without explicit approval.

---

# Phase 8 — Cleanup Logging And Reporting

## Objective

Add structured cleanup reporting that helps reviewers understand what happened without exposing secrets.

## Files/Directories In This Phase

```text
backend/services/carImageCleanupService.js
backend/scripts/cleanupStaleCarImages.js
backend/jobs/cleanupStaleCarImagesJob.js
backend/logs/ optional only if team uses log files
```

## Report Should Include

```text
runId
startedAt
finishedAt
dryRun
olderThanDays
statusesScanned
candidateCount
mediaCount
deletedCount
skippedCount
failureCount
errors
```

## Report Should Avoid

```text
storage credentials
raw bucket secrets
JWT values
private access tokens
provider stack traces in API responses
```

## Done Criteria

- Cleanup summary is structured.
- Logs are clear and safe.
- No secrets are logged.
- Errors are useful but not overly sensitive.

---

# Phase 9 — Cleanup Tests And Dry-Run Validation

## Objective

Add repeatable checks proving the cleanup targets only stale Draft/Deleted listings and does not mutate data in dry-run mode.

## Files/Directories In This Phase

```text
backend/tests/
backend/tests/carImageCleanup.manual.js
src/tests/
src/tests/cleanup.http optional if route exists later
```

## Test Cases

```text
Draft older than 30 days is selected
Deleted older than 30 days is selected
Draft newer than 30 days is skipped
Deleted newer than 30 days is skipped
Available listing is skipped
Sold listing is skipped
Listing with no images is handled safely
Malformed media link is skipped safely
Dry-run does not delete anything
Execute mode requires explicit flag
```

## Done Criteria

- Manual cleanup test exists.
- Dry-run test exists.
- Eligible stale listings are selected.
- Non-eligible listings are skipped.
- Active listings are never selected.
- Teammates can repeat the tests safely.

---

# Phase 10 — Environment And Security Review

## Objective

Confirm cleanup-related environment variables, credentials, and provider configuration are documented and protected safely.

## Files/Directories In This Phase

```text
backend/.env.example
backend/.gitignore
backend/config/
backend/services/storageCleanupService.js
backend/services/carImageCleanupService.js
```

## Environment Variables To Prepare

General cleanup variables:

```text
STORAGE_PROVIDER=pending
CLEANUP_DRY_RUN=true
CLEANUP_OLDER_THAN_DAYS=30
CLEANUP_CRON_ENABLED=false
CLEANUP_CRON_SCHEDULE=0 2 * * *
```

If Cloudinary is selected:

```text
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

If S3 is selected:

```text
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_BUCKET_NAME=
```

## Security Review Items

- Real credentials are not committed.
- `.env` remains ignored.
- `.env.example` contains placeholders only.
- Dry-run mode is default.
- Real deletion requires explicit execution or config.
- Logs do not expose secrets.

## Done Criteria

- Environment variables are documented.
- No provider secrets are committed.
- Cleanup cannot run destructively by default.
- Provider config remains safe for review.

---

# Phase 11 — Final Sprint 4 PR Readiness

## Objective

Confirm Edwin’s Sprint 4 cleanup task is complete, safe, tested, documented, and ready for review.

## Files/Directories In This Phase

```text
backend/server.js
backend/package.json
backend/config/
backend/models/
backend/services/
backend/scripts/
backend/jobs/
backend/tests/
backend/.env.example
README.md
src/tests/
```

## Final Checklist

- Active branch is correct.
- Latest origin/upstream changes were pulled.
- Backend cleanup candidates are clearly defined.
- Draft listings older than 30 days are targeted.
- Deleted listings older than 30 days are targeted.
- Active listings are skipped.
- Dry-run mode exists.
- Manual cleanup script exists.
- Scheduler-ready job exists.
- Storage provider is abstracted.
- No real credentials are committed.
- Manual validation exists.
- Build passes.
- Branch is clean.
- PR explains implemented scope and provider-dependent work.

## Final Commands

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CAR_DEALERSHIP/cardealership
git status
git pull --ff-only origin feature/edwin-sprint4-image-cleanup
npm run build
git restore dist
git status
git log --oneline -8
```

## Done Criteria

- Cleanup script/job is implemented or safely scaffolded.
- Stale Draft/Deleted listings older than 30 days are handled.
- Media link cleanup is provider-safe.
- Dry-run validation exists.
- Scheduler behavior is documented and safe.
- PR is ready for review.

---

# Implementation Dependencies To Confirm With Team

Before enabling final destructive cleanup behavior, confirm:

- Active backend entrypoint.
- Exact car listing status field.
- Exact timestamp field for the 30-day age check.
- Exact image/media table or collection.
- Whether media links should be deleted from DB or marked cleaned.
- Storage provider.
- Storage bucket naming rules.
- Whether deletion should remove files from storage, DB records, or both.
- Whether cleanup should run inside backend server or deployment scheduler.
- Cron schedule.
- Production dry-run policy.
- Who owns approval for destructive cleanup.

---

# Sprint 4 Completion Summary Template

Use this summary once implementation is complete:

```text
Implemented Edwin’s Sprint 4 backend cleanup requirement.

The cleanup system identifies car listings marked Draft or Deleted for more than 30 days, finds associated media records, supports safe dry-run execution, prepares storage cleanup through a provider-safe adapter, and includes scheduler-ready cleanup behavior. The implementation avoids touching active listings, keeps credentials out of source control, and provides repeatable manual validation for teammates.
```
