"use client";

import { Fragment, useState } from "react";
import { Badge, EmptyState } from "@/components/ui";
import { formatDateTime } from "@/lib/format";
import type { AuditLog } from "@/lib/types";

const outcomeTone = { SUCCESS: "success", FAILURE: "warning", DENIED: "danger" } as const;

export function AuditTable({ items, compact }: { items: AuditLog[]; compact?: boolean }) {
  const [open, setOpen] = useState<number | null>(null);
  if (items.length === 0) return <EmptyState title="No audit events match" />;
  return (
    <div className="relative overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-slate-100 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
          <tr>
            <th className="px-5 py-3 font-medium">Time</th>
            <th className="px-5 py-3 font-medium">Action</th>
            <th className="px-5 py-3 font-medium">Actor</th>
            <th className="px-5 py-3 font-medium">Outcome</th>
            {!compact && <th className="px-5 py-3 font-medium">Resource</th>}
            {!compact && <th className="px-5 py-3 font-medium">IP</th>}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {items.map((a) => (
            <Fragment key={a.id}>
              <tr className={compact ? "" : "cursor-pointer hover:bg-slate-50"} onClick={compact ? undefined : () => setOpen(open === a.id ? null : a.id)}>
                <td className="whitespace-nowrap px-5 py-3 text-slate-600">{formatDateTime(a.occurred_at)}</td>
                <td className="px-5 py-3 font-mono text-xs text-slate-900">{a.action}</td>
                <td className="px-5 py-3 text-slate-700">
                  {a.actor_email ?? <span className="text-slate-400">anonymous</span>}
                  {a.actor_role && <span className="ml-1 text-xs text-slate-400">({a.actor_role})</span>}
                </td>
                <td className="px-5 py-3">
                  <Badge tone={outcomeTone[a.outcome]}>{a.outcome}</Badge>
                </td>
                {!compact && (
                  <td className="px-5 py-3 text-xs text-slate-600">
                    {a.resource_type ? `${a.resource_type}:${a.resource_id?.slice(0, 8) ?? ""}` : "—"}
                  </td>
                )}
                {!compact && <td className="px-5 py-3 text-xs text-slate-600">{a.ip_address ?? "—"}</td>}
              </tr>
              {open === a.id && (
                <tr className="bg-slate-50">
                  <td colSpan={6} className="px-5 py-3">
                    <pre className="overflow-x-auto whitespace-pre-wrap text-xs text-slate-700">
                      {JSON.stringify({ request_id: a.request_id, resource_id: a.resource_id, details: a.details }, null, 2)}
                    </pre>
                  </td>
                </tr>
              )}
            </Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
}
