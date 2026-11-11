"use client";

import { useState } from "react";
import { api, ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import type { EmailDispatchResult } from "@/lib/types";
import { Alert, Button } from "./ui";

export function VerificationBanner() {
  const { me } = useAuth();
  const [sending, setSending] = useState(false);
  const [result, setResult] = useState<{ tone: "success" | "error" | "warning"; text: string } | null>(null);
  if (!me) return null;

  async function resend() {
    setSending(true);
    setResult(null);
    try {
      const res = await api<EmailDispatchResult>("/auth/resend-verification", { method: "POST" });
      setResult({ tone: res.email_delivery === "NOT_CONFIGURED" ? "warning" : "success", text: res.message });
    } catch (err) {
      setResult({ tone: "error", text: err instanceof ApiError ? err.message : "Could not send the email." });
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="mb-6 space-y-3">
      <Alert tone="warning" title="Verify your email address">
        <p>
          We sent a verification link to <strong>{me.user.email}</strong>. Most features stay locked until you confirm it.
        </p>
        {!me.email_delivery_configured && (
          <p className="mt-1">Email delivery is not configured on this server, so the link cannot be delivered yet.</p>
        )}
        <Button variant="secondary" size="sm" className="mt-3" onClick={resend} loading={sending}>
          Resend verification email
        </Button>
      </Alert>
      {result && <Alert tone={result.tone}>{result.text}</Alert>}
    </div>
  );
}
