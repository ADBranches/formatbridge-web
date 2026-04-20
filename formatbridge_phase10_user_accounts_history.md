# FormatBridge — Phase 10: User Accounts and Conversion History

## Objective
Add account-based history and future monetization readiness.

This phase gives you:

- sign up / login
- token-based auth state on the frontend
- user-linked conversion jobs
- authenticated job history view
- anonymous workflows that can still work when allowed

---

# Important note before you start

Phase 10 **does require database migrations** because you are introducing:

- a new `users` table
- a nullable `user_id` foreign key on `conversion_jobs`

This phase does **not** need:
- a new database name
- a new PostgreSQL user
- new DB grants
- a new Redis service

Keep using the exact identifiers already established in Phase 1–9:

```env
POSTGRES_DB=formatbridge_db
POSTGRES_USER=formatbridge_user
POSTGRES_PASSWORD=formatbridge_pass
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
DATABASE_URL=postgresql://formatbridge_user:formatbridge_pass@127.0.0.1:5433/formatbridge_db

REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

---

# Phase 10 exact additions to `.env`

Add these to your existing `.env` and `.env.example`:

```env
# =========================
# AUTH
# =========================
AUTH_TOKEN_EXPIRY_HOURS=72
ALLOW_ANONYMOUS_CONVERSIONS=true
AUTH_TOKEN_SALT=formatbridge-auth-token
```

## Meaning
- `AUTH_TOKEN_EXPIRY_HOURS=72` -> login tokens remain valid for 72 hours
- `ALLOW_ANONYMOUS_CONVERSIONS=true` -> non-logged-in users can still upload and convert files
- `AUTH_TOKEN_SALT=formatbridge-auth-token` -> signing salt used for auth tokens

---

# Required package additions

No new third-party auth package is strictly required for this MVP.

This phase uses:
- `werkzeug.security` for password hashing
- `itsdangerous` for signed auth tokens

Both are already available through Flask dependencies.

---

# Files to Populate

## 1) `backend/app/models/user.py`

```python
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    conversion_jobs = relationship("ConversionJob", back_populates="user", lazy="selectin")

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"
```

---

## 2) `backend/app/api/v1/auth.py`

```python
from __future__ import annotations

from flask import Blueprint, current_app, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.exceptions import BadRequest, Unauthorized

from app.extensions import db
from app.models.user import User
from app.utils.response import success_response


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def get_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt=current_app.config.get("AUTH_TOKEN_SALT", "formatbridge-auth-token"),
    )


def generate_auth_token(user: User) -> str:
    serializer = get_serializer()
    return serializer.dumps({"user_id": user.id, "email": user.email})


def get_token_max_age_seconds() -> int:
    hours = int(current_app.config.get("AUTH_TOKEN_EXPIRY_HOURS", 72))
    return hours * 3600


def decode_auth_token(token: str) -> dict:
    serializer = get_serializer()

    try:
        return serializer.loads(token, max_age=get_token_max_age_seconds())
    except SignatureExpired as exc:
        raise Unauthorized("Authentication token has expired.") from exc
    except BadSignature as exc:
        raise Unauthorized("Authentication token is invalid.") from exc


def get_bearer_token_from_request() -> str | None:
    auth_header = request.headers.get("Authorization", "").strip()
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header.replace("Bearer ", "", 1).strip()


def get_current_user_from_request(required: bool = True) -> User | None:
    token = get_bearer_token_from_request()

    if not token:
        if required:
            raise Unauthorized("Authentication is required.")
        return None

    payload = decode_auth_token(token)
    user_id = payload.get("user_id")

    if not user_id:
        raise Unauthorized("Authentication token payload is invalid.")

    user = db.session.get(User, user_id)
    if not user or not user.is_active:
        raise Unauthorized("Authenticated user was not found or is inactive.")

    return user


@auth_bp.post("/signup")
def signup():
    payload = request.get_json(silent=True) or {}

    full_name = (payload.get("full_name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not full_name:
        raise BadRequest("full_name is required.")
    if not email:
        raise BadRequest("email is required.")
    if "@" not in email:
        raise BadRequest("email must be valid.")
    if len(password) < 8:
        raise BadRequest("password must be at least 8 characters long.")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise BadRequest("An account with that email already exists.")

    user = User(full_name=full_name, email=email, is_active=True)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    token = generate_auth_token(user)

    return success_response(
        "Account created successfully.",
        data={
            "user": user.to_dict(),
            "token": token,
        },
        status_code=201,
    )


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email:
        raise BadRequest("email is required.")
    if not password:
        raise BadRequest("password is required.")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        raise Unauthorized("Invalid email or password.")

    if not user.is_active:
        raise Unauthorized("This account is inactive.")

    token = generate_auth_token(user)

    return success_response(
        "Login successful.",
        data={
            "user": user.to_dict(),
            "token": token,
        },
        status_code=200,
    )


@auth_bp.get("/me")
def me():
    user = get_current_user_from_request(required=True)

    return success_response(
        "Authenticated user fetched successfully.",
        data={"user": user.to_dict()},
        status_code=200,
    )
```

---

## 3) `frontend/src/pages/HistoryPage.jsx`

```jsx
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
```

---

## 4) `frontend/src/store/authStore.js`

```javascript
const TOKEN_KEY = "formatbridge_auth_token";
const USER_KEY = "formatbridge_auth_user";

function readJson(key) {
  const rawValue = window.localStorage.getItem(key);
  if (!rawValue) return null;

  try {
    return JSON.parse(rawValue);
  } catch {
    return null;
  }
}

const authStore = {
  getToken() {
    return window.localStorage.getItem(TOKEN_KEY) || "";
  },

  getUser() {
    return readJson(USER_KEY);
  },

  isAuthenticated() {
    return Boolean(this.getToken());
  },

  setSession({ token, user }) {
    window.localStorage.setItem(TOKEN_KEY, token);
    window.localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  clearSession() {
    window.localStorage.removeItem(TOKEN_KEY);
    window.localStorage.removeItem(USER_KEY);
  },
};

export default authStore;
```

---

## 5) `frontend/src/components/common/ProtectedRoute.jsx`

```jsx
import { Navigate } from "react-router-dom";
import authStore from "../../store/authStore";

export default function ProtectedRoute({ children }) {
  if (!authStore.isAuthenticated()) {
    return <Navigate to="/convert" replace />;
  }

  return children;
}
```

---

# Required supporting edits

These files were not in your Phase 10 list, but they are required for the phase to actually run cleanly.

---

## A) Update `backend/app/models/conversion_job.py`

Replace your current file with this version so jobs can belong to users:

```python
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ConversionJob(Base):
    __tablename__ = "conversion_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    public_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    requested_output_format: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    source_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_public_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)

    ocr_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="queued", index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user = relationship("User", back_populates="conversion_jobs")
    results = relationship(
        "ConversionResult",
        back_populates="job",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<ConversionJob id={self.id} public_id={self.public_id!r} "
            f"user_id={self.user_id} status={self.status!r} "
            f"output={self.requested_output_format!r} ocr_enabled={self.ocr_enabled}>"
        )
```

### Exact migration commands after editing this model

From `backend/`:

```bash
source env/bin/activate
flask --app run.py db migrate -m "add users and link conversion_jobs to users"
flask --app run.py db upgrade
```

---

## B) Update `backend/app/models/__init__.py`

Replace with:

```python
from .file_asset import FileAsset
from .conversion_job import ConversionJob
from .conversion_result import ConversionResult
from .user import User

__all__ = ["FileAsset", "ConversionJob", "ConversionResult", "User"]
```

---

## C) Update `backend/app/api/v1/__init__.py`

Replace your current file with this version:

```python
from flask import Blueprint

from app.api.v1.auth import auth_bp
from app.api.v1.conversions import conversions_bp
from app.api.v1.downloads import downloads_bp
from app.api.v1.jobs import jobs_bp
from app.api.v1.uploads import uploads_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/v1")
api_v1_bp.register_blueprint(uploads_bp)
api_v1_bp.register_blueprint(conversions_bp)
api_v1_bp.register_blueprint(jobs_bp)
api_v1_bp.register_blueprint(downloads_bp)
api_v1_bp.register_blueprint(auth_bp)
```

---

## D) Update `backend/app/api/v1/jobs.py`

Replace your current file with this version so users can fetch their own history:

```python
from flask import Blueprint

from app.api.v1.auth import get_current_user_from_request
from app.models.conversion_job import ConversionJob
from app.schemas.result_schema import serialize_job_status_response
from app.utils.response import success_response
from werkzeug.exceptions import NotFound

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs_bp.get("/<string:job_public_id>")
def get_job_status(job_public_id: str):
    job = ConversionJob.query.filter_by(public_id=job_public_id).first()

    if not job:
        raise NotFound("Conversion job was not found.")

    payload = serialize_job_status_response(
        message="Job status fetched successfully.",
        job=job,
    )
    return success_response(
        message=payload["message"],
        data=payload["data"],
        status_code=200,
    )


@jobs_bp.get("/history")
def get_job_history():
    current_user = get_current_user_from_request(required=True)

    jobs = (
        ConversionJob.query.filter_by(user_id=current_user.id)
        .order_by(ConversionJob.created_at.desc())
        .all()
    )

    serialized_jobs = [
        {
            "public_id": job.public_id,
            "requested_output_format": job.requested_output_format,
            "source_count": job.source_count,
            "ocr_enabled": job.ocr_enabled,
            "status": job.status,
            "created_at": job.created_at.isoformat(),
        }
        for job in jobs
    ]

    return success_response(
        "Conversion history fetched successfully.",
        data={"jobs": serialized_jobs},
        status_code=200,
    )
```

---

## E) Update `backend/app/api/v1/conversions.py`

Replace your current file with this version so conversion jobs can optionally be linked to the authenticated user while still allowing anonymous use when configured:

```python
import os
import uuid

from flask import Blueprint, request
from werkzeug.exceptions import NotFound, Unauthorized

from app.api.v1.auth import get_current_user_from_request
from app.extensions import db
from app.models.conversion_job import ConversionJob
from app.models.file_asset import FileAsset
from app.schemas.conversion_schema import (
    serialize_conversion_job_created,
    validate_conversion_request,
)
from app.tasks.conversion_tasks import process_conversion_job_task
from app.utils.response import success_response

conversions_bp = Blueprint("conversions", __name__, url_prefix="/conversions")


@conversions_bp.post("")
def create_conversion_job():
    payload = request.get_json(silent=True) or {}
    data = validate_conversion_request(payload)

    source_public_ids = data["file_public_ids"]
    requested_output_format = data["output_format"]
    ocr_enabled = data["ocr_enabled"]

    allow_anonymous = os.getenv("ALLOW_ANONYMOUS_CONVERSIONS", "true").lower() == "true"
    current_user = get_current_user_from_request(required=False)

    if not current_user and not allow_anonymous:
        raise Unauthorized("Authentication is required to create conversion jobs.")

    files = (
        FileAsset.query.filter(FileAsset.public_id.in_(source_public_ids))
        .order_by(FileAsset.id.asc())
        .all()
    )

    if len(files) != len(source_public_ids):
        found_ids = {file.public_id for file in files}
        missing_ids = [public_id for public_id in source_public_ids if public_id not in found_ids]
        raise NotFound(f"Some uploaded files were not found: {', '.join(missing_ids)}")

    job = ConversionJob(
        public_id=uuid.uuid4().hex,
        user_id=current_user.id if current_user else None,
        requested_output_format=requested_output_format,
        source_count=len(source_public_ids),
        source_public_ids=source_public_ids,
        ocr_enabled=ocr_enabled,
        status="queued",
    )

    db.session.add(job)
    db.session.commit()

    process_conversion_job_task.delay(job.public_id)

    payload = serialize_conversion_job_created(
        message="Conversion job created successfully.",
        job=job,
    )

    return success_response(
        message=payload["message"],
        data=payload["data"],
        status_code=202,
    )
```

---

## F) Update `backend/app/config.py`

Add these lines into `BaseConfig`:

```python
AUTH_TOKEN_EXPIRY_HOURS = int(os.getenv("AUTH_TOKEN_EXPIRY_HOURS", "72"))
ALLOW_ANONYMOUS_CONVERSIONS = os.getenv("ALLOW_ANONYMOUS_CONVERSIONS", "true").lower() == "true"
AUTH_TOKEN_SALT = os.getenv("AUTH_TOKEN_SALT", "formatbridge-auth-token")
```

Full `BaseConfig` should include them alongside your existing settings.

---

## G) Update `frontend/src/routes/index.jsx`

Replace your current file with this Phase 10 version so history is protected and routed:

```jsx
import { createBrowserRouter, Link } from "react-router-dom";
import ProtectedRoute from "../components/common/ProtectedRoute";
import ConvertPage from "../pages/ConvertPage";
import HistoryPage from "../pages/HistoryPage";
import ResultsPage from "../pages/ResultsPage";

function HomePage() {
  return (
    <main className="min-h-screen">
      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <span className="inline-flex rounded-full bg-brand-50 px-3 py-1 text-sm font-medium text-brand-700">
            Phase 10 accounts and history
          </span>

          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900">
            FormatBridge
          </h1>

          <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-600">
            User accounts, authenticated history, and future monetization readiness.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/convert"
              className="inline-flex rounded-xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
            >
              Open convert page
            </Link>

            <Link
              to="/history"
              className="inline-flex rounded-xl border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            >
              View history
            </Link>
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
    path: "/convert",
    element: <ConvertPage />,
  },
  {
    path: "/results/:jobId",
    element: <ResultsPage />,
  },
  {
    path: "/history",
    element: (
      <ProtectedRoute>
        <HistoryPage />
      </ProtectedRoute>
    ),
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);

export default router;
```

---

## H) Frontend auth UI note

The file list for Phase 10 does not include dedicated `LoginPage.jsx` or `SignupPage.jsx`.

So for this phase, keep auth minimal and API-ready:
- `authStore.js` manages session persistence
- `/api/v1/auth/signup`
- `/api/v1/auth/login`
- `/api/v1/auth/me`

You can test auth immediately with Postman / curl, or add full auth pages as a follow-up polish step.

---

# Exact migration commands

Because `user.py` and `conversion_job.py` are changed in this phase, run these exact commands:

```bash
cd backend
source env/bin/activate
flask --app run.py db migrate -m "add users and link conversion_jobs to users"
flask --app run.py db upgrade
```

---

# Exact startup order after Phase 10 files are in place

## 1. Start infrastructure
From repo root:

```bash
cp .env.example .env
docker compose up -d postgres redis
```

## 2. Start backend
From `backend/`:

```bash
source env/bin/activate
pip install -r requirements.txt
python run.py
```

## 3. Start Celery worker
From `backend/` in a second terminal:

```bash
source env/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```

## 4. Start frontend
From `frontend/`:

```bash
npm install
npm run dev
```

---

# Optional direct API flow test

## A) Sign up

```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Edwin Bwambale",
    "email": "edwin@example.com",
    "password": "Password123"
  }'
```

Copy the returned `token`.

## B) Login

```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "edwin@example.com",
    "password": "Password123"
  }'
```

Copy the returned `token`.

## C) Create a conversion job as an authenticated user

```bash
curl -X POST http://127.0.0.1:5000/api/v1/conversions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer PUT_REAL_TOKEN_HERE" \
  -d '{
    "file_public_ids": ["PUT_REAL_FILE_ID_HERE"],
    "output_format": "pdf",
    "ocr_enabled": false
  }'
```

Expected:
- the new job is created
- `conversion_jobs.user_id` is populated

## D) Fetch account history

```bash
curl http://127.0.0.1:5000/api/v1/jobs/history \
  -H "Authorization: Bearer PUT_REAL_TOKEN_HERE"
```

Expected:
- only that user’s jobs are returned

---

# Exact SQL checks

Check the users table:

```bash
docker exec -it formatbridge_postgres psql -U formatbridge_user -d formatbridge_db -c "SELECT id, full_name, email, is_active, created_at FROM users ORDER BY id DESC;"
```

Check linked jobs:

```bash
docker exec -it formatbridge_postgres psql -U formatbridge_user -d formatbridge_db -c "SELECT id, public_id, user_id, requested_output_format, status, created_at FROM conversion_jobs ORDER BY id DESC;"
```

Expected:
- signed-in jobs have `user_id`
- anonymous jobs may still have `user_id = NULL` when anonymous use is allowed

---

# Completion Check

## Check 1 — authenticated users see their past jobs

Expected:
- signed-in user can call `/api/v1/jobs/history`
- only their jobs are listed
- frontend `/history` route loads when authenticated

---

## Check 2 — anonymous workflows still work if allowed

With:

```env
ALLOW_ANONYMOUS_CONVERSIONS=true
```

Expected:
- non-logged-in users can still upload and create jobs
- those jobs will have `user_id = NULL`
- authenticated users still get history for their own linked jobs

---

# What Phase 10 completes

Once this works, your project will have:

- user accounts
- signed token auth
- authenticated history view
- user-linked conversion jobs
- anonymous workflows still supported if enabled
- a foundation for future paid plans, quotas, and ownership rules

That is a proper Phase 10 foundation.

---

# Best next step after Phase 10

The next clean move is MVP polish and release readiness:
- add dedicated signup / login UI pages
- add logout button and account menu
- add per-user quotas / plan limits
- add ownership checks for future stricter result access
