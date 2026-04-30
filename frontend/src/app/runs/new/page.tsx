"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { apiFetch, RunCreateResponse } from "@/lib/api";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AuthGuard } from "@/components/AuthGuard";
import { AppHeader } from "@/lib/components/AppHeader";

export default function NewRunPage() {
  const router = useRouter();

  const [floorsAboveGrade, setFloorsAboveGrade] = useState(6);
  const [totalUnits, setTotalUnits] = useState(24);
  const [sprinklered, setSprinklered] = useState(true);
  const [stairCountProposed, setStairCountProposed] = useState(1);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await apiFetch<RunCreateResponse>("/runs", {
        method: "POST",
        auth: true,
        body: {
          building_use: "residential",
          floors_above_grade: floorsAboveGrade,
          total_units: totalUnits,
          sprinklered,
          stair_count_proposed: stairCountProposed,
        },
      });

      router.push(`/runs/${result.run_id}`);
    } catch {
      setError("Failed to create run.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthGuard>
    <AppHeader></AppHeader>
    <main className="min-h-screen bg-muted px-6 py-10">
      <div className="mx-auto max-w-xl">
        <Card>
          <CardHeader>
            <CardTitle>New Egress + Stairs Check</CardTitle>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">

              <div className="space-y-2">
                <Label>Floors Above Grade</Label>
                <Input
                  type="number"
                  value={floorsAboveGrade}
                  onChange={(e) => setFloorsAboveGrade(Number(e.target.value))}
                />
              </div>

              <div className="space-y-2">
                <Label>Total Units</Label>
                <Input
                  type="number"
                  value={totalUnits}
                  onChange={(e) => setTotalUnits(Number(e.target.value))}
                />
              </div>

              <div className="space-y-2">
                <Label>Proposed Stair Count</Label>
                <Input
                  type="number"
                  value={stairCountProposed}
                  onChange={(e) =>
                    setStairCountProposed(Number(e.target.value))
                  }
                />
              </div>

              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={sprinklered}
                  onChange={(e) => setSprinklered(e.target.checked)}
                />
                Sprinklered Building
              </label>

              {error ? (
                <p className="text-sm text-red-600">{error}</p>
              ) : null}

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? "Submitting..." : "Run Check"}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </main>
    </AuthGuard>
  );
}