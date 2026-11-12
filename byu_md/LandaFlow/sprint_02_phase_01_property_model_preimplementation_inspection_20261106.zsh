#!/usr/bin/env zsh
setopt PIPE_FAIL

project_dir="/home/trovas/Downloads/projects/byupw/NOVIQ/tenant management system/Land-Flow"
results_dir="/home/trovas/Downloads/projects/byupw/NOVIQ/tenant management system"
evidence_file="$results_dir/sprint_02_phase_01_property_model_preimplementation_inspection_20261106.txt"
cd "$project_dir" || return 1

{
  printf '%s\n' "=== SPRINT 02 PROPERTY MODEL PREIMPLEMENTATION INSPECTION ==="
  printf 'Timestamp: '
  date --iso-8601=seconds

  printf '\n=== Repository safety and collaborator state ===\n'
  git status --short --branch
  git fetch --all --prune
  fetch_status=$?
  printf 'FETCH_EXIT_CODE=%s\n' "$fetch_status"
  git remote -v
  git branch -vv
  git log -5 --oneline --decorate

  printf '\n=== Remote branch inventory ===\n'
  git for-each-ref --sort=-committerdate \
    --format='%(refname:short) | %(objectname:short) | %(committerdate:iso8601) | %(subject)' \
    refs/remotes/origin

  printf '\n=== Main divergence and incoming commits ===\n'
  git log --oneline --decorate HEAD..origin/main
  printf '\n=== Current commits not in main ===\n'
  git log --oneline --decorate origin/main..HEAD
  printf '\n=== Divergence counts ===\n'
  git rev-list --left-right --count HEAD...origin/main

  printf '\n=== Pull-request state ===\n'
  gh pr list --state open \
    --json number,title,headRefName,baseRefName,url,statusCheckRollup \
    || true
  gh pr list --state merged --limit 10 \
    --json number,title,headRefName,baseRefName,mergedAt,url \
    || true

  printf '\n=== Existing database schema and migrations ===\n'
  sed -n '1,760p' packages/database/prisma/schema.prisma
  find packages/database/prisma/migrations -maxdepth 2 -type f \
    -name migration.sql -print | sort

  printf '\n=== Existing database package and scoped repositories ===\n'
  for inspected_file in \
    packages/database/package.json \
    packages/database/tsconfig.json \
    packages/database/src/index.ts \
    packages/database/src/tenant-scope.ts \
    packages/database/src/tenant-scope.spec.ts \
    packages/database/prisma/seed.ts; do
    printf '\n--- %s ---\n' "$inspected_file"
    if [[ -f "$inspected_file" ]]; then
      sed -n '1,760p' "$inspected_file"
    else
      printf 'MISSING\n'
    fi
  done

  printf '\n=== Existing shared type contracts ===\n'
  for inspected_file in \
    packages/types/package.json \
    packages/types/tsconfig.json \
    packages/types/src/index.ts \
    packages/types/src/authorisation.ts; do
    printf '\n--- %s ---\n' "$inspected_file"
    if [[ -f "$inspected_file" ]]; then
      sed -n '1,520p' "$inspected_file"
    else
      printf 'MISSING\n'
    fi
  done

  printf '\n=== Existing property-like assets and references ===\n'
  find apps packages docs tests -maxdepth 8 -type f \
    \( -iname '*property*' -o -iname '*unit*' -o -iname '*address*' \) \
    -not -path '*/node_modules/*' \
    -not -path '*/dist/*' \
    -not -path '*/.next/*' \
    -print | sort
  git grep -nEI 'Property|PropertyAddress|UnitStatus|UnitState|propertyId|unitId' \
    -- ':!pnpm-lock.yaml' ':!*.md' || true

  printf '\n=== Database and migration documentation ===\n'
  for inspected_file in \
    docs/architecture/database-model.md \
    docs/development/database-migrations.md; do
    printf '\n--- %s ---\n' "$inspected_file"
    if [[ -f "$inspected_file" ]]; then
      sed -n '1,620p' "$inspected_file"
    else
      printf 'MISSING\n'
    fi
  done

  printf '\n=== Runtime database readiness and existing relations ===\n'
  docker compose ps
  compose_status=$?
  printf 'COMPOSE_PS_EXIT_CODE=%s\n' "$compose_status"
  docker compose exec -T postgres pg_isready -U landaflow -d landaflow
  postgres_status=$?
  printf 'POSTGRES_READY_EXIT_CODE=%s\n' "$postgres_status"
  docker compose exec -T postgres psql -U landaflow -d landaflow \
    -c '\dt'
  relations_status=$?
  printf 'RELATIONS_QUERY_EXIT_CODE=%s\n' "$relations_status"
  docker compose exec -T postgres psql -U landaflow -d landaflow \
    -c 'SELECT migration_name, finished_at IS NOT NULL AS applied FROM "_prisma_migrations" ORDER BY started_at;'
  migration_query_status=$?
  printf 'MIGRATION_QUERY_EXIT_CODE=%s\n' "$migration_query_status"

  printf '\n=== Current database validation baseline ===\n'
  export DATABASE_URL="postgresql://landaflow:landaflow_local_only@localhost:55432/landaflow"
  pnpm --filter @landaflow/database prisma validate
  prisma_status=$?
  printf 'PRISMA_VALIDATE_EXIT_CODE=%s\n' "$prisma_status"
  pnpm --filter @landaflow/database test
  database_test_status=$?
  printf 'DATABASE_TEST_EXIT_CODE=%s\n' "$database_test_status"

  printf '\n=== Tracked environment and secret safety ===\n'
  git ls-files | grep -E '(^|/)\.env($|\.)' | grep -vE '\.env\.(example|mock\.example)$' || true
  git diff --check
  diff_status=$?
  printf 'GIT_DIFF_CHECK_EXIT_CODE=%s\n' "$diff_status"

  printf '\n=== Final repository state ===\n'
  git status --short --branch

  if (( fetch_status == 0 && compose_status == 0 && postgres_status == 0 && relations_status == 0 && migration_query_status == 0 && prisma_status == 0 && database_test_status == 0 && diff_status == 0 )); then
    printf '\nSPRINT_02_PHASE_01_PROPERTY_MODEL_PREIMPLEMENTATION_INSPECTION_COMPLETE\n'
  else
    printf '\nSPRINT_02_PHASE_01_PROPERTY_MODEL_PREIMPLEMENTATION_INSPECTION_FAILED\n'
  fi
} 2>&1 | tee "$evidence_file"
