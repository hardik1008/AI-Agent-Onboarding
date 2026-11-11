"use client";

import Link from "next/link";
import { useState } from "react";
import { AuthShell } from "@/components/AuthShell";
import { Alert, Button, Field, Input } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import type { Message } from "@/lib/types";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [done, setDone] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const res = await api<Message>("/auth/forgot-password", { method: "POST", body: { email } });
      setDone(res.message);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Request failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthShell
      title="Reset your password"
      subtitle="Enter your account email. If it's registered, we'll send a reset link."
      footer={
        <Link href="/login" className="font-medium text-brand-700 hover:underline">
          Back to sign in
        </Link>
      }
    >
      {done ? (
        <Alert tone="success" title="Check your email">
          {done}
        </Alert>
      ) : (
        <form onSubmit={onSubmit} className="space-y-5" noValidate>
          {error && <Alert tone="error">{error}</Alert>}
          <Field label="Email" htmlFor="email">
            <Input id="email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </Field>
          <Button type="submit" className="w-full" loading={submitting} disabled={!email}>
            Send reset link
          </Button>
        </form>
      )}
    </AuthShell>
  );
}
