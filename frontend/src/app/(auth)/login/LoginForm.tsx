"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AuthShell } from "@/components/AuthShell";
import { PasswordField } from "@/components/PasswordField";
import { Alert, Button, Field, Input } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { safeNext } from "@/lib/format";

export function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const { me, loading, refresh } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const next = safeNext(params.get("next"));

  useEffect(() => {
    if (!loading && me) router.replace(next);
  }, [loading, me, next, router]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await api("/auth/login", { method: "POST", body: { email, password } });
      await refresh();
      router.replace(next);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Sign-in failed. Please try again.");
      setSubmitting(false);
    }
  }

  return (
    <AuthShell
      title="Sign in"
      subtitle="Applicants and PolicyNest staff use the same sign-in."
      footer={
        <>
          New to PolicyNest?{" "}
          <Link href="/register" className="font-medium text-brand-700 hover:underline">
            Create an applicant account
          </Link>
        </>
      }
    >
      <form onSubmit={onSubmit} className="space-y-5" noValidate>
        {params.get("reset") === "1" && <Alert tone="success">Password updated. Sign in with your new password.</Alert>}
        {params.get("expired") === "1" && <Alert tone="warning">Your session ended. Sign in again to continue.</Alert>}
        {error && <Alert tone="error">{error}</Alert>}
        <Field label="Email" htmlFor="email">
          <Input id="email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </Field>
        <PasswordField id="password" label="Password" value={password} onChange={setPassword} autoComplete="current-password" />
        <div className="flex justify-end">
          <Link href="/forgot-password" className="text-sm font-medium text-brand-700 hover:underline">
            Forgot password?
          </Link>
        </div>
        <Button type="submit" className="w-full" loading={submitting} disabled={!email || !password}>
          Sign in
        </Button>
      </form>
    </AuthShell>
  );
}
