"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AuthShell } from "@/components/AuthShell";
import { PasswordField } from "@/components/PasswordField";
import { Alert, Button, Spinner } from "@/components/ui";
import { api, ApiError } from "@/lib/api";

type TokenInfo = { purpose: "PASSWORD_RESET" | "INVITE"; email: string; full_name?: string };

export function ResetPasswordForm() {
  const router = useRouter();
  const token = useSearchParams().get("token") ?? "";
  const [info, setInfo] = useState<TokenInfo | null>(null);
  const [tokenError, setTokenError] = useState<string | null>(null);
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [fieldError, setFieldError] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!token) {
      setTokenError("This link is incomplete. Request a new one.");
      return;
    }
    api<TokenInfo>("/auth/check-token", { method: "POST", body: { token } }).then(setInfo, (err) =>
      setTokenError(err instanceof ApiError ? err.message : "This link could not be checked."),
    );
  }, [token]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setFieldError(undefined);
    if (password !== confirm) {
      setFieldError("Passwords do not match.");
      return;
    }
    setSubmitting(true);
    try {
      await api("/auth/reset-password", { method: "POST", body: { token, password } });
      router.replace("/login?reset=1");
    } catch (err) {
      if (err instanceof ApiError) {
        setFieldError(err.fieldErrors.password);
        setError(err.message);
      } else setError("Could not update the password.");
      setSubmitting(false);
    }
  }

  const invite = info?.purpose === "INVITE";
  return (
    <AuthShell
      title={invite ? "Set up your staff account" : "Choose a new password"}
      subtitle={info ? `For ${info.email}` : undefined}
      footer={
        <Link href="/login" className="font-medium text-brand-700 hover:underline">
          Back to sign in
        </Link>
      }
    >
      {tokenError ? (
        <div className="space-y-4">
          <Alert tone="error">{tokenError}</Alert>
          <Link href="/forgot-password" className="text-sm font-medium text-brand-700 hover:underline">
            Request a new reset link
          </Link>
        </div>
      ) : !info ? (
        <Spinner label="Checking link" />
      ) : (
        <form onSubmit={onSubmit} className="space-y-5" noValidate>
          {error && <Alert tone="error">{error}</Alert>}
          <PasswordField id="password" label="New password" value={password} onChange={setPassword} autoComplete="new-password" showChecks error={fieldError} />
          <PasswordField id="confirm" label="Confirm password" value={confirm} onChange={setConfirm} autoComplete="new-password" />
          <Button type="submit" className="w-full" loading={submitting} disabled={!password || !confirm}>
            {invite ? "Activate account" : "Update password"}
          </Button>
        </form>
      )}
    </AuthShell>
  );
}
