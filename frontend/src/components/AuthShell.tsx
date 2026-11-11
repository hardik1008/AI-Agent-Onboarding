import Link from "next/link";
import { Logo } from "./Logo";

export function AuthShell({ title, subtitle, children, footer }: { title: string; subtitle?: React.ReactNode; children: React.ReactNode; footer?: React.ReactNode }) {
  return (
    <div className="grid min-h-screen lg:grid-cols-[1fr_minmax(0,36rem)]">
      <aside className="relative hidden overflow-hidden bg-brand-900 p-12 text-brand-50 lg:flex lg:flex-col lg:justify-between">
        <Link href="/" className="relative z-10">
          <Logo inverted />
        </Link>
        <div className="relative z-10 max-w-md space-y-4">
          <p className="text-3xl font-semibold leading-tight text-white">POSP onboarding with verifiable decisions.</p>
          <p className="text-brand-100">
            Every action on PolicyNest is authenticated, permission-checked and written to an append-only audit trail.
          </p>
        </div>
        <p className="relative z-10 text-xs text-brand-200">© {new Date().getFullYear()} PolicyNest Insurance Broking</p>
        <div className="absolute -right-24 -top-24 h-96 w-96 rounded-full bg-brand-700/40 blur-3xl" aria-hidden />
      </aside>
      <main className="flex flex-col justify-center px-6 py-12 sm:px-12">
        <div className="mx-auto w-full max-w-sm">
          <Link href="/" className="mb-8 inline-block lg:hidden">
            <Logo />
          </Link>
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900">{title}</h1>
          {subtitle && <p className="mt-2 text-sm text-slate-600">{subtitle}</p>}
          <div className="mt-8">{children}</div>
          {footer && <div className="mt-8 text-sm text-slate-600">{footer}</div>}
        </div>
      </main>
    </div>
  );
}
