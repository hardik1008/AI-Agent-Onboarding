"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import { AppShell } from "@/components/AppShell";
import { Alert, Button, Spinner } from "@/components/ui";
import { useAuth } from "@/lib/auth";

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { me, loading, error, refresh } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!loading && !me && !error) router.replace(`/login?next=${encodeURIComponent(pathname)}`);
  }, [loading, me, error, pathname, router]);

  if (error && !me) {
    return (
      <div className="mx-auto max-w-md p-8">
        <Alert tone="error" title="Unable to load your session">
          {error}
        </Alert>
        <Button className="mt-4" variant="secondary" onClick={() => void refresh()}>
          Try again
        </Button>
      </div>
    );
  }
  if (loading || !me) return <Spinner label="Checking your session" />;
  return <AppShell>{children}</AppShell>;
}
