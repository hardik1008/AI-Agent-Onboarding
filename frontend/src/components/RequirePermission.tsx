"use client";

import { ShieldX } from "lucide-react";
import { useAuth } from "@/lib/auth";
import { Card } from "./ui";

export function AccessDenied() {
  return (
    <Card className="mx-auto max-w-lg p-8 text-center">
      <ShieldX className="mx-auto h-10 w-10 text-red-600" aria-hidden />
      <h1 className="mt-4 text-lg font-semibold text-slate-900">Access denied</h1>
      <p className="mt-2 text-sm text-slate-600">Your role does not include permission to view this page.</p>
    </Card>
  );
}

export function RequirePermission({ permission, children }: { permission: string; children: React.ReactNode }) {
  const { can } = useAuth();
  return can(permission) ? <>{children}</> : <AccessDenied />;
}
