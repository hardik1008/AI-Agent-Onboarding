"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import { AuthShell } from "@/components/AuthShell";
import { Alert, Button } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export function VerifyEmail() {
  const token = useSearchParams().get("token") ?? "";
  const { me, refresh } = useAuth();
  const [state, setState] = useState<"idle" | "working" | "done">("idle");
  const [error, setError] = useState<string | null>(null);

  async function confirm() {
    setState("working");
    setError(null);
    try {
      await api("/auth/verify-email", { method: "POST", body: { token } });
      setState("done");
      void refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Verification failed.");
      setState("idle");
    }
  }

  return (
    <AuthShell title="Verify your email" subtitle="Confirm that this email address belongs to you.">
      <div className="space-y-5">
        {!token && <Alert tone="error">This verification link is incomplete. Request a new one from your dashboard.</Alert>}
        {error && <Alert tone="error">{error}</Alert>}
        {state === "done" ? (
          <>
            <Alert tone="success" title="Email verified">
              Your email address is confirmed.
            </Alert>
            <Link href={me ? "/app" : "/login"} className="inline-flex h-10 items-center rounded-lg bg-brand-700 px-4 text-sm font-medium text-white hover:bg-brand-800">
              {me ? "Go to dashboard" : "Sign in"}
            </Link>
          </>
        ) : (
          token && (
            <Button className="w-full" onClick={confirm} loading={state === "working"}>
              Confirm email address
            </Button>
          )
        )}
      </div>
    </AuthShell>
  );
}
