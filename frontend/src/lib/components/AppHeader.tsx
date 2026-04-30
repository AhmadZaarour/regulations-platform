"use client";

import Link from "next/link";

import { logout } from "@/lib/auth";
import { Button } from "@/components/ui/button";

export function AppHeader() {
  return (
    <header className="border-b bg-background">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link href="/dashboard" className="font-semibold">
          Regulations Platform
        </Link>

        <nav className="flex items-center gap-3">
          <Link href="/dashboard" className="text-sm text-muted-foreground">
            Dashboard
          </Link>
          <Link href="/runs/new" className="text-sm text-muted-foreground">
            New Run
          </Link>
          <Button variant="outline" size="sm" onClick={logout}>
            Logout
          </Button>
        </nav>
      </div>
    </header>
  );
}