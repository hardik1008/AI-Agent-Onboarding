"use client";

import { Eye, EyeOff } from "lucide-react";
import { useState } from "react";
import { Field, Input } from "./ui";

export function passwordChecks(password: string, minLength: number) {
  return [
    { label: `At least ${minLength} characters`, ok: password.length >= minLength },
    { label: "Contains a letter and a number", ok: /[A-Za-z]/.test(password) && /\d/.test(password) },
  ];
}

export function PasswordField({
  id,
  label,
  value,
  onChange,
  error,
  autoComplete,
  showChecks,
  minLength = 12,
}: {
  id: string;
  label: string;
  value: string;
  onChange: (v: string) => void;
  error?: string;
  autoComplete: "current-password" | "new-password";
  showChecks?: boolean;
  minLength?: number;
}) {
  const [visible, setVisible] = useState(false);
  const checks = passwordChecks(value, minLength);
  return (
    <Field
      label={label}
      htmlFor={id}
      error={error}
      hint={
        showChecks ? (
          <span className="flex flex-wrap gap-x-4 gap-y-1">
            {checks.map((c) => (
              <span key={c.label} className={c.ok ? "text-emerald-700" : "text-slate-500"}>
                {c.ok ? "✓" : "•"} {c.label}
              </span>
            ))}
          </span>
        ) : undefined
      }
    >
      <div className="relative">
        <Input
          id={id}
          type={visible ? "text" : "password"}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          autoComplete={autoComplete}
          invalid={!!error}
          required
          className="pr-10"
        />
        <button
          type="button"
          onClick={() => setVisible((v) => !v)}
          className="absolute inset-y-0 right-0 flex w-10 items-center justify-center text-slate-500 hover:text-slate-800"
          aria-label={visible ? "Hide password" : "Show password"}
        >
          {visible ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
        </button>
      </div>
    </Field>
  );
}
