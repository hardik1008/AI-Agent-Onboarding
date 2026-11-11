"use client";

import clsx from "clsx";
import { AlertCircle, CheckCircle2, Info, Loader2, TriangleAlert, X } from "lucide-react";
import { forwardRef, useEffect, useId, useRef } from "react";

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";

export const Button = forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: ButtonVariant; loading?: boolean; size?: "sm" | "md" }
>(function Button({ variant = "primary", loading, size = "md", className, children, disabled, ...props }, ref) {
  return (
    <button
      ref={ref}
      disabled={disabled || loading}
      className={clsx(
        "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600 disabled:cursor-not-allowed disabled:opacity-60",
        size === "sm" ? "h-8 px-3 text-sm" : "h-10 px-4 text-sm",
        {
          "bg-brand-700 text-white hover:bg-brand-800": variant === "primary",
          "border border-slate-300 bg-white text-slate-800 hover:bg-slate-50": variant === "secondary",
          "text-slate-700 hover:bg-slate-100": variant === "ghost",
          "bg-red-600 text-white hover:bg-red-700": variant === "danger",
        },
        className,
      )}
      {...props}
    >
      {loading && <Loader2 className="h-4 w-4 animate-spin" aria-hidden />}
      {children}
    </button>
  );
});

export function Field({
  label,
  error,
  hint,
  children,
  htmlFor,
}: {
  label: string;
  error?: string;
  hint?: React.ReactNode;
  children: React.ReactNode;
  htmlFor: string;
}) {
  return (
    <div className="space-y-1.5">
      <label htmlFor={htmlFor} className="block text-sm font-medium text-slate-800">
        {label}
      </label>
      {children}
      {error ? (
        <p id={`${htmlFor}-error`} className="text-sm text-red-700" role="alert">
          {error}
        </p>
      ) : hint ? (
        <p className="text-xs text-slate-500">{hint}</p>
      ) : null}
    </div>
  );
}

const controlClass =
  "block w-full rounded-lg border bg-white px-3 py-2 text-sm text-slate-900 shadow-sm placeholder:text-slate-400 focus:border-brand-600 focus:outline-none focus:ring-2 focus:ring-brand-600/20 disabled:bg-slate-50";

export const Input = forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement> & { invalid?: boolean }>(
  function Input({ invalid, className, id, ...props }, ref) {
    return (
      <input
        ref={ref}
        id={id}
        aria-invalid={invalid || undefined}
        aria-describedby={invalid && id ? `${id}-error` : undefined}
        className={clsx(controlClass, invalid ? "border-red-500" : "border-slate-300", "h-10", className)}
        {...props}
      />
    );
  },
);

export const Select = forwardRef<HTMLSelectElement, React.SelectHTMLAttributes<HTMLSelectElement>>(function Select(
  { className, ...props },
  ref,
) {
  return <select ref={ref} className={clsx(controlClass, "h-10 border-slate-300", className)} {...props} />;
});

export function Card({ className, children }: { className?: string; children: React.ReactNode }) {
  return <div className={clsx("rounded-xl border border-slate-200 bg-white shadow-sm", className)}>{children}</div>;
}

export function CardHeader({ title, description, action }: { title: string; description?: string; action?: React.ReactNode }) {
  return (
    <div className="flex flex-wrap items-start justify-between gap-3 border-b border-slate-100 px-5 py-4">
      <div>
        <h2 className="text-base font-semibold text-slate-900">{title}</h2>
        {description && <p className="mt-0.5 text-sm text-slate-500">{description}</p>}
      </div>
      {action}
    </div>
  );
}

type Tone = "info" | "success" | "warning" | "error";
const toneIcon = { info: Info, success: CheckCircle2, warning: TriangleAlert, error: AlertCircle };

export function Alert({ tone = "info", title, children, className }: { tone?: Tone; title?: string; children?: React.ReactNode; className?: string }) {
  const Icon = toneIcon[tone];
  return (
    <div
      role={tone === "error" ? "alert" : "status"}
      className={clsx(
        "flex gap-3 rounded-lg border px-4 py-3 text-sm",
        {
          "border-sky-200 bg-sky-50 text-sky-900": tone === "info",
          "border-emerald-200 bg-emerald-50 text-emerald-900": tone === "success",
          "border-amber-200 bg-amber-50 text-amber-900": tone === "warning",
          "border-red-200 bg-red-50 text-red-900": tone === "error",
        },
        className,
      )}
    >
      <Icon className="mt-0.5 h-4 w-4 shrink-0" aria-hidden />
      <div className="space-y-1">
        {title && <p className="font-semibold">{title}</p>}
        {children && <div>{children}</div>}
      </div>
    </div>
  );
}

type BadgeTone = "neutral" | "brand" | "success" | "warning" | "danger";
export function Badge({ tone = "neutral", children }: { tone?: BadgeTone; children: React.ReactNode }) {
  return (
    <span
      className={clsx("inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset", {
        "bg-slate-50 text-slate-700 ring-slate-200": tone === "neutral",
        "bg-brand-50 text-brand-800 ring-brand-200": tone === "brand",
        "bg-emerald-50 text-emerald-800 ring-emerald-200": tone === "success",
        "bg-amber-50 text-amber-800 ring-amber-200": tone === "warning",
        "bg-red-50 text-red-800 ring-red-200": tone === "danger",
      })}
    >
      {children}
    </span>
  );
}

export function Spinner({ label = "Loading" }: { label?: string }) {
  return (
    <div className="flex items-center justify-center gap-2 py-10 text-sm text-slate-500" role="status">
      <Loader2 className="h-5 w-5 animate-spin" aria-hidden />
      {label}
    </div>
  );
}

export function PageHeader({ title, description, action }: { title: string; description?: string; action?: React.ReactNode }) {
  return (
    <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-slate-900">{title}</h1>
        {description && <p className="mt-1 max-w-2xl text-sm text-slate-600">{description}</p>}
      </div>
      {action}
    </div>
  );
}

export function EmptyState({ title, children }: { title: string; children?: React.ReactNode }) {
  return (
    <div className="px-6 py-12 text-center">
      <p className="text-sm font-medium text-slate-900">{title}</p>
      {children && <div className="mt-1 text-sm text-slate-500">{children}</div>}
    </div>
  );
}

export function Dialog({
  open,
  onClose,
  title,
  description,
  children,
}: {
  open: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: React.ReactNode;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const titleId = useId();
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (open && !el.open) el.showModal?.();
    if (!open && el.open) el.close?.();
  }, [open]);
  return (
    <dialog
      ref={ref}
      aria-labelledby={titleId}
      onClose={onClose}
      onCancel={onClose}
      className="m-auto w-[min(32rem,calc(100vw-2rem))] rounded-xl border border-slate-200 p-0 shadow-xl backdrop:bg-slate-900/40"
    >
      {open && (
        <div className="p-6">
          <div className="mb-4 flex items-start justify-between gap-4">
            <div>
              <h2 id={titleId} className="text-lg font-semibold text-slate-900">
                {title}
              </h2>
              {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}
            </div>
            <button type="button" onClick={onClose} className="rounded p-1 text-slate-500 hover:bg-slate-100" aria-label="Close">
              <X className="h-4 w-4" />
            </button>
          </div>
          {children}
        </div>
      )}
    </dialog>
  );
}

export function Pagination({ page, pageSize, total, onPage }: { page: number; pageSize: number; total: number; onPage: (p: number) => void }) {
  const pages = Math.max(1, Math.ceil(total / pageSize));
  const from = total === 0 ? 0 : (page - 1) * pageSize + 1;
  const to = Math.min(total, page * pageSize);
  return (
    <div className="flex items-center justify-between border-t border-slate-100 px-5 py-3 text-sm text-slate-600">
      <span>
        {from}–{to} of {total}
      </span>
      <div className="flex gap-2">
        <Button variant="secondary" size="sm" disabled={page <= 1} onClick={() => onPage(page - 1)}>
          Previous
        </Button>
        <Button variant="secondary" size="sm" disabled={page >= pages} onClick={() => onPage(page + 1)}>
          Next
        </Button>
      </div>
    </div>
  );
}
