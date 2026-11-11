"use client";

import { Check, Minus } from "lucide-react";
import { useEffect, useState } from "react";
import { RequirePermission } from "@/components/RequirePermission";
import { Alert, Badge, Card, CardHeader, PageHeader, Spinner } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import type { RolesMatrix } from "@/lib/types";

export default function RolesPage() {
  return (
    <RequirePermission permission="roles:read">
      <RolesView />
    </RequirePermission>
  );
}

function RolesView() {
  const [data, setData] = useState<RolesMatrix | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    api<RolesMatrix>("/admin/roles").then(setData, (e) => setError(e instanceof ApiError ? e.message : "Failed to load roles."));
  }, []);
  if (error) return <Alert tone="error">{error}</Alert>;
  if (!data) return <Spinner />;
  const categories = [...new Set(data.permissions.map((p) => p.category))];
  return (
    <>
      <PageHeader
        title="Roles & permissions"
        description="Roles grant permissions (RBAC). The server additionally applies attribute rules (ABAC): applicants only see their own records, reviewers are limited to their region and clearance level, and administrators cannot change their own role or status."
      />
      <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {data.roles.map((r) => (
          <Card key={r.code} className="p-5">
            <div className="flex items-center justify-between">
              <p className="font-semibold text-slate-900">{r.name}</p>
              <Badge tone={r.is_staff ? "brand" : "neutral"}>{r.is_staff ? "Staff" : "External"}</Badge>
            </div>
            <p className="mt-2 text-sm text-slate-600">{r.description}</p>
            <p className="mt-3 text-xs text-slate-500">
              {r.user_count} user{r.user_count === 1 ? "" : "s"} · {r.permissions.length} permissions
            </p>
          </Card>
        ))}
      </div>
      <Card>
        <CardHeader title="Permission matrix" description="Administrators manage the platform but cannot decide applications (separation of duties)." />
        <div className="relative overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-slate-100 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-5 py-3 text-left font-medium">Permission</th>
                {data.roles.map((r) => (
                  <th key={r.code} className="px-3 py-3 text-center font-medium">
                    {r.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {categories.map((cat) => (
                <CategoryRows key={cat} category={cat} data={data} />
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </>
  );
}

function CategoryRows({ category, data }: { category: string; data: RolesMatrix }) {
  return (
    <>
      <tr className="bg-slate-50/60">
        <td colSpan={data.roles.length + 1} className="px-5 py-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
          {category}
        </td>
      </tr>
      {data.permissions
        .filter((p) => p.category === category)
        .map((p) => (
          <tr key={p.code} className="border-t border-slate-100">
            <td className="px-5 py-3">
              <p className="font-mono text-xs text-slate-900">{p.code}</p>
              <p className="text-xs text-slate-500">{p.description}</p>
            </td>
            {data.roles.map((r) => (
              <td key={r.code} className="px-3 py-3 text-center">
                {r.permissions.includes(p.code) ? (
                  <Check className="mx-auto h-4 w-4 text-emerald-600" aria-label="Granted" />
                ) : (
                  <Minus className="mx-auto h-4 w-4 text-slate-300" aria-label="Not granted" />
                )}
              </td>
            ))}
          </tr>
        ))}
    </>
  );
}
