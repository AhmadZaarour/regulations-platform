"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { apiFetch, RunResultResponse } from "@/lib/api";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AuthGuard } from "@/components/AuthGuard";
import { AppHeader } from "@/lib/components/AppHeader";
import { Button } from "@/components/ui/button";

type RequirementItem = {
  code: string;
  title: string;
  status: string;
  why: string[];
  missing_inputs: string[];
  checklist: string[];
};

type EngineResult = {
  applies: RequirementItem[];
  maybe: RequirementItem[];
  not_applicable: RequirementItem[];
};

function StatusBadge({ status }: { status: string }) {
  return <AuthGuard><Badge variant="outline">{status}</Badge></AuthGuard>;
}

function RequirementCard({ item }: { item: RequirementItem }) {
  return (
    <AuthGuard>
    <Card>
      <CardHeader>
        <CardTitle className="text-base">
          {item.code} — {item.title}
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-3 text-sm">
        {item.why.length > 0 ? (
          <div>
            <p className="font-medium">Why</p>
            <ul className="list-disc pl-5">
              {item.why.map((reason) => (
                <li key={reason}>{reason}</li>
              ))}
            </ul>
          </div>
        ) : null}

        {item.missing_inputs.length > 0 ? (
          <div>
            <p className="font-medium">Missing inputs</p>
            <ul className="list-disc pl-5">
              {item.missing_inputs.map((input) => (
                <li key={input}>{input}</li>
              ))}
            </ul>
          </div>
        ) : null}

        {item.checklist.length > 0 ? (
          <div>
            <p className="font-medium">Checklist</p>
            <ul className="list-disc pl-5">
              {item.checklist.map((check) => (
                <li key={check}>{check}</li>
              ))}
            </ul>
          </div>
        ) : null}
      </CardContent>
    </Card>
    </AuthGuard>
  );
}

export default function RunResultPage() {
  const params = useParams<{ id: string }>();
  const runId = params.id;

  const [run, setRun] = useState<RunResultResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    async function fetchRun() {
      try {
        const data = await apiFetch<RunResultResponse>(`/runs/${runId}`, {
          auth: true,
        });

        if (!active) return;
        setRun(data);

        if (data.status === "succeeded" || data.status === "failed") {
          return;
        }
      } catch {
        if (active) setError("Failed to load run.");
      }
    }

    fetchRun();
    const interval = setInterval(fetchRun, 2000);

    return () => {
      active = false;
      clearInterval(interval);
    };
  }, [runId]);

  const result = run?.result as EngineResult | null;

  return (
    <AuthGuard>
    <AppHeader></AppHeader>
    <main className="min-h-screen bg-muted px-6 py-10">
      <div className="mx-auto max-w-4xl space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Run #{runId}</span>
              {run ? <StatusBadge status={run.status} /> : null}
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-2 text-sm">
            {error ? <p className="text-red-600">{error}</p> : null}
            {!run ? <p>Loading...</p> : null}
            {run?.status === "queued" || run?.status === "running" ? (
              <p className="text-muted-foreground">
                Processing regulation check...
              </p>
            ) : null}
            {run?.status === "failed" ? (
                <div className="space-y-3">
                    <p className="text-red-600">{run.error_message}</p>

                    <Button
                    onClick={async () => {
                        await apiFetch(`/runs/${runId}/retry`, {
                        method: "POST",
                        auth: true,
                        });

                        window.location.reload();
                    }}
                    >
                    Retry Run
                    </Button>
                </div>
                ) : null}
          </CardContent>
        </Card>

        {result ? (
          <div className="space-y-6">
            <section className="space-y-3">
              <h2 className="text-xl font-semibold">Applies</h2>
              {result.applies.length > 0 ? (
                result.applies.map((item) => (
                  <RequirementCard key={item.code} item={item} />
                ))
              ) : (
                <p className="text-sm text-muted-foreground">No applies items.</p>
              )}
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold">Maybe</h2>
              {result.maybe.length > 0 ? (
                result.maybe.map((item) => (
                  <RequirementCard key={item.code} item={item} />
                ))
              ) : (
                <p className="text-sm text-muted-foreground">No maybe items.</p>
              )}
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold">Not Applicable</h2>
              {result.not_applicable.length > 0 ? (
                result.not_applicable.map((item) => (
                  <RequirementCard key={item.code} item={item} />
                ))
              ) : (
                <p className="text-sm text-muted-foreground">
                  No not-applicable items.
                </p>
              )}
            </section>
          </div>
        ) : null}
      </div>
    </main>
    </AuthGuard>
  );
}