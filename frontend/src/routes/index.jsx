import { createBrowserRouter, Link } from "react-router-dom";
import ConvertPage from "../pages/ConvertPage";

function HomePage() {
  return (
    <main className="min-h-screen">
      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <span className="inline-flex rounded-full bg-brand-50 px-3 py-1 text-sm font-medium text-brand-700">
            Phase 2 upload flow
          </span>

          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900">
            FormatBridge
          </h1>

          <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-600">
            Secure upload, validation, and temporary persistence for supported image formats.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/convert"
              className="inline-flex rounded-xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
            >
              Open upload page
            </Link>

            <a
              href="http://127.0.0.1:5000/api/v1/health"
              target="_blank"
              rel="noreferrer"
              className="inline-flex rounded-xl border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
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
    path: "/convert",
    element: <ConvertPage />,
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);

export default router;