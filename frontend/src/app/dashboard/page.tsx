"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { AppHeader } from "@/lib/components/AppHeader";
import { AuthGuard } from "@/components/AuthGuard";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { apiFetch, RunListResponse } from "@/lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [runs, setRuns] = useState<RunListResponse | null>(null);

  useEffect(() => {
    apiFetch<RunListResponse>("/runs", { auth: true })
      .then(setRuns)
      .catch(() => setRuns({ items: [] }));
  }, []);

  return (
    <AuthGuard>
      <AppHeader />

      <main className="min-h-screen bg-muted px-6 py-10">
        <div className="mx-auto max-w-5xl space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Dashboard</CardTitle>
            </CardHeader>

            <CardContent className="flex items-center justify-between gap-4">
              <p className="text-muted-foreground">
                Run early egress and stairs checks for residential projects.
              </p>

              <Button onClick={() => router.push("/runs/new")}>
                New Check
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recent Runs</CardTitle>
            </CardHeader>

            <CardContent>
              {!runs ? (
                <p className="text-sm text-muted-foreground">Loading...</p>
              ) : runs.items.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No runs yet. Create your first check.
                </p>
              ) : (
                <div className="space-y-3">
                  {runs.items.map((run) => (
                    <button
                      key={run.id}
                      onClick={() => router.push(`/runs/${run.id}`)}
                      className="flex w-full items-center justify-between rounded-lg border bg-background p-4 text-left hover:bg-muted"
                    >
                      <div>
                        <p className="font-medium">Run #{run.id}</p>
                        <p className="text-sm text-muted-foreground">
                          {run.project_type}
                        </p>
                      </div>

                      <span className="text-sm font-medium">{run.status}</span>
                    </button>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </AuthGuard>
  );
}