# Phase 1 — Product Foundation and Environment Setup

## Objective
Establish the repository, local environments, tooling, and basic frontend/backend scaffolding for **FormatBridge** using:

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** Flask + Celery + Redis
- **Database:** PostgreSQL

## Important note before you paste files
I added **2 supporting files** that are required to make this Phase 1 setup actually boot cleanly with the Tailwind v3-style config you requested:

- `frontend/postcss.config.js`
- `frontend/src/index.css`

That is because the Vite + Tailwind v3 guide uses `tailwind.config.js`, `postcss.config.js`, and a CSS file with Tailwind directives together. citeturn377676search4turn377676search2

---

# Recommended root structure for Phase 1

```text
formatbridge-web/
├── README.md
├── .env.example
├── docker-compose.yml
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       └── routes/
│           └── index.jsx
└── backend/
    ├── requirements.txt
    ├── run.py
    ├── wsgi.py
    ├── celery_worker.py
    └── app/
        ├── __init__.py
        ├── config.py
        ├── extensions.py
        └── database.py
```

---

# 1) `README.md`

```md
# FormatBridge

FormatBridge is a web-based multi-format file conversion platform.

## Phase 1 Stack
- React + Vite + Tailwind CSS
- Flask + Celery + Redis
- PostgreSQL
- Docker Compose for infrastructure services

## Project Structure
- `frontend/` → React client
- `backend/` → Flask API, Celery worker, database integration

## Local Setup

### 1. Clone and enter the repo
```bash
git clone <your-repo-url> formatbridge-web
cd formatbridge-web
```

### 2. Create environment file
```bash
cp .env.example .env
```

### 3. Start PostgreSQL and Redis
```bash
docker compose up -d postgres redis
```

### 4. Start backend
```bash
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python run.py
```

### 5. Start Celery worker
Open a second terminal:

```bash
cd formatbridge-web/backend
source env/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```

### 6. Start frontend
Open a third terminal:

```bash
cd formatbridge-web/frontend
npm install
npm run dev
```

## Health Check
Backend:
- `GET /api/v1/health`

Expected:
```json
{
  "status": "healthy",
  "service": "formatbridge-api",
  "database": "connected",
  "queue": "configured"
}
```

## Flask migration commands
From `backend/`:
```bash
source env/bin/activate
flask --app run.py db init
flask --app run.py db migrate -m "initial setup"
flask --app run.py db upgrade
```

## Phase 1 Done When
- frontend loads in browser
- backend health endpoint returns 200
- Redis is running
- Celery worker starts and connects to Redis
- PostgreSQL is reachable
- Flask-Migrate commands run
```

---

# 2) `.env.example`

```env
# =========================
# APP
# =========================
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=change-me-in-production
API_HOST=0.0.0.0
API_PORT=5000

# =========================
# DATABASE
# =========================
POSTGRES_DB=formatbridge_db
POSTGRES_USER=formatbridge_user
POSTGRES_PASSWORD=formatbridge_pass
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
DATABASE_URL=postgresql://formatbridge_user:formatbridge_pass@127.0.0.1:5433/formatbridge_db

# =========================
# REDIS / CELERY
# =========================
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# =========================
# CORS
# =========================
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

---

# 3) `docker-compose.yml`

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16
    container_name: formatbridge_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: formatbridge_db
      POSTGRES_USER: formatbridge_user
      POSTGRES_PASSWORD: formatbridge_pass
    ports:
      - "5433:5432"
    volumes:
      - formatbridge_postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U formatbridge_user -d formatbridge_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: formatbridge_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - formatbridge_redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  formatbridge_postgres_data:
  formatbridge_redis_data:
```

---

# 4) `frontend/package.json`

React 19.1.1 is the current npm `latest` tag in the npm registry results I checked, Vite is 7.1.4, and `@vitejs/plugin-react` is 5.0.2. citeturn453064search3turn436809search0turn995762search7

```json
{
  "name": "formatbridge-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "react-router-dom": "^6.28.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^5.0.2",
    "autoprefixer": "^10.4.21",
    "postcss": "^8.5.6",
    "tailwindcss": "^3.4.10",
    "vite": "^7.1.4"
  }
}
```

---

# 5) `frontend/vite.config.js`

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
});
```

---

# 6) `frontend/tailwind.config.js`

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eff6ff",
          100: "#dbeafe",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8"
        }
      }
    }
  },
  plugins: []
};
```

---

# 7) `frontend/postcss.config.js`  **(supporting required file)**

```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

---

# 8) `frontend/src/index.css`  **(supporting required file)**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: light;
}

html,
body,
#root {
  min-height: 100%;
}

body {
  @apply bg-slate-50 text-slate-900 antialiased;
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
}
```

---

# 9) `frontend/src/main.jsx`

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

# 10) `frontend/src/App.jsx`

```jsx
import { RouterProvider } from "react-router-dom";
import router from "./routes";

export default function App() {
  return <RouterProvider router={router} />;
}
```

---

# 11) `frontend/src/routes/index.jsx`

```jsx
import { createBrowserRouter, Link } from "react-router-dom";

function HomePage() {
  return (
    <main className="min-h-screen">
      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <span className="inline-flex rounded-full bg-brand-50 px-3 py-1 text-sm font-medium text-brand-700">
            Phase 1 foundation
          </span>

          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900">
            FormatBridge
          </h1>

          <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-600">
            A web-based file conversion platform for HEIC, JPG, JPEG, PNG, WEBP,
            GIF, PDF, and DOCX workflows.
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-200 p-5">
              <h2 className="text-lg font-semibold text-slate-900">Frontend</h2>
              <p className="mt-2 text-sm text-slate-600">
                React + Vite + Tailwind CSS with route scaffolding ready.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 p-5">
              <h2 className="text-lg font-semibold text-slate-900">Backend</h2>
              <p className="mt-2 text-sm text-slate-600">
                Flask app factory, PostgreSQL connection, health endpoint,
                Celery and Redis configuration.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 p-5">
              <h2 className="text-lg font-semibold text-slate-900">Next Step</h2>
              <p className="mt-2 text-sm text-slate-600">
                Build file upload, validation, and conversion job creation in
                Phase 2.
              </p>
            </div>
          </div>

          <div className="mt-8">
            <a
              href="http://127.0.0.1:5000/api/v1/health"
              target="_blank"
              rel="noreferrer"
              className="inline-flex rounded-xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
            >
              Check backend health
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}

function NotFoundPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">404</h1>
        <p className="mt-2 text-slate-600">Page not found.</p>
        <Link
          to="/"
          className="mt-4 inline-flex rounded-lg bg-slate-900 px-4 py-2 text-white"
        >
          Go home
        </Link>
      </div>
    </main>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);

export default router;
```

---

# 12) `backend/requirements.txt`

```txt
Flask
Flask-Cors
Flask-SQLAlchemy
Flask-Migrate
SQLAlchemy
psycopg2-binary
python-dotenv
celery
redis
gunicorn
```

---

# 13) `backend/run.py`

```python
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "5000")),
        debug=os.getenv("FLASK_ENV", "development") == "development",
    )
```

---

# 14) `backend/wsgi.py`

```python
from app import create_app

app = create_app()
```

---

# 15) `backend/app/config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://formatbridge_user:formatbridge_pass@127.0.0.1:5433/formatbridge_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ]


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config(config_name: str | None = None):
    name = (config_name or os.getenv("FLASK_ENV", "development")).lower()

    mapping = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    return mapping.get(name, DevelopmentConfig)
```

---

# 16) `backend/app/extensions.py`

```python
from celery import Celery, Task
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
celery_app = Celery(__name__)


def init_celery(app):
    celery_app.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        task_ignore_result=False,
        broker_connection_retry_on_startup=True,
        timezone="UTC",
    )

    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = FlaskTask
    app.extensions["celery"] = celery_app
    return celery_app
```

---

# 17) `backend/app/database.py`

```python
from sqlalchemy import text

from app.extensions import db

Base = db.Model


def ping_database():
    with db.engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True
```

---

# 18) `backend/app/__init__.py`

```python
from flask import Flask, jsonify

from app.config import get_config
from app.database import ping_database
from app.extensions import cors, db, init_celery, migrate


def create_app(config_name: str | None = None):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )
    init_celery(app)

    @app.get("/api/v1/health")
    def health_check():
        database_status = "connected"
        status = "healthy"
        error_message = None

        try:
            ping_database()
        except Exception as exc:
            database_status = "disconnected"
            status = "degraded"
            error_message = str(exc)

        payload = {
            "status": status,
            "service": "formatbridge-api",
            "database": database_status,
            "queue": "configured",
            "error": error_message,
        }

        return jsonify(payload), 200 if database_status == "connected" else 503

    return app
```

---

# 19) `backend/celery_worker.py`

```python
from app import create_app

flask_app = create_app()
celery = flask_app.extensions["celery"]


@celery.task(name="tasks.ping")
def ping():
    return {"message": "pong"}
```

---

# 20) Commands to create the folders quickly

```bash
mkdir -p formatbridge-web/frontend/src/routes
mkdir -p formatbridge-web/backend/app
cd formatbridge-web
```

---

# 21) Exact setup commands to run after pasting the files

## A. Start infrastructure
```bash
cp .env.example .env
docker compose up -d postgres redis
```

## B. Start backend
```bash
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python run.py
```

## C. In a second terminal, start Celery
```bash
cd formatbridge-web/backend
source env/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```

## D. In a third terminal, start frontend
```bash
cd formatbridge-web/frontend
npm install
npm run dev
```

---

# 22) Exact completion checks for Phase 1

## Check 1 — frontend boots
Open:
```text
http://127.0.0.1:5173
```

You should see the **FormatBridge** landing page.

## Check 2 — backend health returns 200
```bash
curl http://127.0.0.1:5000/api/v1/health
```

Expected:
```json
{
  "database": "connected",
  "error": null,
  "queue": "configured",
  "service": "formatbridge-api",
  "status": "healthy"
}
```

## Check 3 — Celery worker starts
Look for worker startup logs similar to:
```text
Connected to redis://127.0.0.1:6379/0
```

## Check 4 — PostgreSQL is reachable
```bash
docker ps
```

You should see both:
- `formatbridge_postgres`
- `formatbridge_redis`

## Check 5 — Flask migrations can run
From `backend/`:
```bash
source env/bin/activate
flask --app run.py db init
flask --app run.py db migrate -m "initial setup"
flask --app run.py db upgrade
```

Even before you add models, the migration tooling should initialize correctly.

---

# 23) Immediate next files after Phase 1
Once this phase works, the next clean move is **Phase 2**:
- upload pipeline
- file validation
- file storage metadata
- upload endpoint
- React upload UI

---

# 24) Notes on the chosen frontend toolchain
React’s official docs currently document React 19.2, the npm `latest` tag for `react` and `react-dom` is 19.1.1 in the package registry results I checked, Vite is 7.1.4, and the official Vite React plugin is `@vitejs/plugin-react` 5.0.2. Tailwind’s current main line is v4, but because you explicitly wanted `tailwind.config.js`, I used the Tailwind v3 Vite setup pattern, which still uses `tailwind.config.js` plus `postcss.config.js`. citeturn965149search3turn453064search3turn965149search0turn436809search0turn995762search7turn377676search4turn377676search2
