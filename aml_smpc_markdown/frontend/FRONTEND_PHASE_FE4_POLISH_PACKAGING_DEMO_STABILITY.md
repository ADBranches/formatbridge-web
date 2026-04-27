# Frontend Phase FE4 — Polish, Packaging, and Demo Stability

## Objective

Make the frontend polished, stable, and ready for defense or investor-style presentation.

## Target Directory

```text
aml-system/services/regulator-api/frontend/
```

## Files and Directories

```text
src/components/ui/Button.tsx
src/components/ui/Card.tsx
src/components/ui/Input.tsx
src/components/ui/JsonViewer.tsx
src/components/ui/CopyButton.tsx
src/components/evidence/ExportEvidenceButton.tsx
src/components/errors/ErrorBoundary.tsx
src/hooks/useAsync.ts
src/hooks/useToast.ts
src/utils/formatDate.ts
src/utils/formatStatus.ts
scripts/demo/run-frontend-demo.sh
scripts/demo/build-frontend.sh
```

## Step 1 — Create Supporting Directories

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system/services/regulator-api/frontend

mkdir -p src/components/errors src/hooks src/utils
```

## Step 2 — Create UI Polish Components

Create:

```text
src/components/ui/Button.tsx
src/components/ui/Card.tsx
src/components/ui/Input.tsx
src/components/ui/JsonViewer.tsx
src/components/ui/CopyButton.tsx
```

Purpose:

```text
Button.tsx      -> consistent button styling
Card.tsx        -> consistent card layout
Input.tsx       -> consistent input styling
JsonViewer.tsx  -> safe JSON display
CopyButton.tsx  -> copy proof ID or tx_id
```

## Step 3 — Create Error Boundary

```bash
cat > src/components/errors/ErrorBoundary.tsx <<'EOF'
import { Component, ReactNode } from "react";

type ErrorBoundaryProps = {
  children: ReactNode;
};

type ErrorBoundaryState = {
  error: Error | null;
};

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error) {
    return { error };
  }

  render() {
    if (this.state.error) {
      return (
        <div className="m-6 rounded-2xl border border-red-300 bg-red-50 p-6 text-red-700">
          <h1 className="text-xl font-bold">Something went wrong</h1>
          <p className="mt-2 text-sm">{this.state.error.message}</p>
        </div>
      );
    }

    return this.props.children;
  }
}
EOF
```

## Step 4 — Utility Helpers

```bash
cat > src/utils/formatDate.ts <<'EOF'
export function formatDate(value?: string) {
  if (!value) return "N/A";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString();
}
EOF

cat > src/utils/formatStatus.ts <<'EOF'
export function formatStatus(value?: string) {
  if (!value) return "UNKNOWN";
  return value.replaceAll("_", " ").toUpperCase();
}
EOF
```

## Step 5 — Demo Scripts

Return to project root:

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC/aml-system
```

Create frontend runner:

```bash
cat > scripts/demo/run-frontend-demo.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/services/regulator-api/frontend"

cd "$FRONTEND_DIR"

if [ ! -d node_modules ]; then
  npm install
fi

echo "Starting AML SMPC frontend demo..."
echo "Open: http://127.0.0.1:5173"

npm run dev -- --host 127.0.0.1 --port 5173
EOF

chmod +x scripts/demo/run-frontend-demo.sh
```

Create frontend builder:

```bash
cat > scripts/demo/build-frontend.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/services/regulator-api/frontend"

cd "$FRONTEND_DIR"

if [ ! -d node_modules ]; then
  npm install
fi

npm run build

echo "Frontend build complete:"
echo "$FRONTEND_DIR/dist"
EOF

chmod +x scripts/demo/build-frontend.sh
```

## Step 6 — Verify

```bash
bash -n scripts/demo/run-frontend-demo.sh
bash -n scripts/demo/build-frontend.sh

./scripts/demo/build-frontend.sh
```

## Acceptance Criteria

```text
npm run build passes.
run-frontend-demo.sh starts the browser UI.
Error boundary exists.
Reusable UI components exist.
Frontend can be packaged for demo.
```

## Git Commands

```bash
cd /home/trovas/Downloads/sem32/a_final_year_project/AML_SMPC

git add aml-system/services/regulator-api/frontend/src
git add aml-system/scripts/demo/run-frontend-demo.sh
git add aml-system/scripts/demo/build-frontend.sh

git commit -m "Polish frontend UI and add demo packaging scripts"

git push origin main
```
