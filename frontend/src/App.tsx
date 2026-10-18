import { useCallback, useEffect, useState } from "react";

import {
  fetchServiceHealth,
  type ServiceHealth,
} from "./lib/api";

const dependencies = [
  {
    key: "postgresql",
    label: "PostgreSQL",
    description: "Database and vector storage",
  },
  {
    key: "redis",
    label: "Redis",
    description: "Caching and coordination",
  },
  {
    key: "ollama",
    label: "Ollama",
    description: "Local model runtime",
  },
] as const;

function App() {
  const [health, setHealth] = useState<ServiceHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkHealth = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await fetchServiceHealth();

      setHealth(result);
      setLastChecked(new Date());
    } catch {
      setHealth(null);
      setError(
        "Unable to reach the CodeLens API. Check whether the backend is running.",
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void checkHealth();
  }, [checkHealth]);

  const isHealthy = health?.status === "ok";

  return (
    <main className="min-h-screen bg-neutral-950 px-5 text-neutral-100 sm:px-8">
      <div className="mx-auto max-w-5xl">
        <header className="flex items-center justify-between border-b border-neutral-800 py-6">
          <a href="/" className="flex items-center gap-3 no-underline">
            <span className="grid size-10 place-items-center rounded-xl bg-white text-lg font-bold text-neutral-950">
              C
            </span>

            <span className="text-xl font-semibold tracking-tight text-white">
              CodeLens
            </span>
          </a>

          <span className="rounded-full border border-neutral-700 px-3 py-1.5 text-[10px] font-semibold tracking-widest text-neutral-400 sm:text-xs">
            LOCAL DEVELOPMENT
          </span>
        </header>

        <section className="py-14 sm:py-20">
          <p className="mb-4 text-xs font-semibold tracking-[0.2em] text-neutral-500">
            REPOSITORY INTELLIGENCE ENGINE
          </p>

          <h1 className="text-4xl font-semibold tracking-tight sm:text-6xl">
            Welcome to CodeLens.
          </h1>

          <p className="mt-5 max-w-xl text-base leading-7 text-neutral-400 sm:text-lg">
            Understand your codebase, one question at a time.
          </p>
        </section>

        <section
          aria-labelledby="health-heading"
          className="rounded-2xl border border-neutral-800 bg-neutral-900/60 p-5 sm:p-8"
        >
          <div className="flex flex-col justify-between gap-4 border-b border-neutral-800 pb-6 sm:flex-row sm:items-center">
            <div>
              <p className="mb-2 text-[10px] font-semibold tracking-[0.2em] text-neutral-500">
                SYSTEM OVERVIEW
              </p>

              <h2
                id="health-heading"
                className="text-xl font-semibold tracking-tight"
              >
                Service health
              </h2>
            </div>

            <button
              type="button"
              onClick={() => void checkHealth()}
              disabled={loading}
              className="rounded-lg border border-neutral-700 px-4 py-2.5 text-sm font-medium transition hover:bg-neutral-800 disabled:cursor-wait disabled:opacity-50"
            >
              {loading ? "Checking..." : "Refresh status"}
            </button>
          </div>

          {error ? (
            <div
              role="alert"
              className="my-6 flex gap-3 rounded-xl border border-red-900/60 bg-red-950/30 p-5"
            >
              <span className="mt-1.5 size-2 shrink-0 rounded-full bg-red-500" />

              <div>
                <p className="font-medium text-red-300">
                  Backend unavailable
                </p>

                <p className="mt-2 text-sm leading-6 text-neutral-400">
                  {error}
                </p>
              </div>
            </div>
          ) : (
            <>
              <div className="flex items-start gap-3 py-6">
                <span
                  className={`mt-1.5 size-2.5 shrink-0 rounded-full ${
                    loading
                      ? "animate-pulse bg-amber-400"
                      : isHealthy
                        ? "bg-emerald-400"
                        : "bg-red-400"
                  }`}
                />

                <div>
                  <h3 className="font-medium">
                    {loading
                      ? "Checking services..."
                      : isHealthy
                        ? "All systems operational"
                        : "Some services need attention"}
                  </h3>

                  <p className="mt-1.5 text-sm leading-6 text-neutral-400">
                    {loading
                      ? "Contacting the backend and checking dependencies."
                      : "Status reported by the CodeLens backend."}
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                {dependencies.map((dependency) => {
                  const status =
                    health?.dependencies[dependency.key].status;

                  const available = status === "available";

                  return (
                    <article
                      key={dependency.key}
                      className="rounded-xl border border-neutral-800 bg-neutral-950/60 p-5"
                    >
                      <div className="flex items-center gap-2.5">
                        <span
                          className={`size-2 rounded-full ${
                            loading
                              ? "animate-pulse bg-amber-400"
                              : available
                                ? "bg-emerald-400"
                                : status
                                  ? "bg-red-400"
                                  : "bg-neutral-600"
                          }`}
                        />

                        <h3 className="text-sm font-semibold">
                          {dependency.label}
                        </h3>
                      </div>

                      <p className="mt-3 min-h-10 text-xs leading-5 text-neutral-500">
                        {dependency.description}
                      </p>

                      <p
                        className={`mt-4 text-xs font-medium ${
                          loading
                            ? "text-amber-400"
                            : available
                              ? "text-emerald-400"
                              : status
                                ? "text-red-400"
                                : "text-neutral-500"
                        }`}
                      >
                        {loading ? "Checking" : status ?? "Unknown"}
                      </p>
                    </article>
                  );
                })}
              </div>
            </>
          )}

          <footer className="mt-6 flex flex-col gap-2 border-t border-neutral-800 pt-5 text-[11px] text-neutral-500 sm:flex-row sm:items-center sm:justify-between">
            <span>
              {lastChecked
                ? `Last checked: ${lastChecked.toLocaleTimeString()}`
                : "Waiting for health check"}
            </span>

            <span>API · /api/health</span>
          </footer>
        </section>

        <footer className="py-8 text-center text-xs text-neutral-600">
          CodeLens · Built for understanding complex codebases.
        </footer>
      </div>
    </main>
  );
}

export default App;