"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useCallback, useEffect, useState } from "react";
import { RequirePermission } from "@/components/RequirePermission";
import { Alert, Badge, Button, Card, Input, PageHeader, Pagination, Select, Spinner, EmptyState } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { formatDate, formatDateTime, isLocked } from "@/lib/format";
import { userStatus } from "@/lib/userStatus";
import type { AdminUser, EmailDispatchResult, Page } from "@/lib/types";
import { EditUserDialog, InviteUserDialog } from "./UserDialogs";

export default function UsersPage() {
  return (
    <RequirePermission permission="users:read">
      <Suspense>
        <UsersView />
      </Suspense>
    </RequirePermission>
  );
}

function UsersView() {
  const { can, me } = useAuth();
  const params = useSearchParams();
  const router = useRouter();
  const filters = { q: params.get("q") ?? "", role: params.get("role") ?? "", status: params.get("status") ?? "", page: Number(params.get("page") ?? 1) };
  const [q, setQ] = useState(filters.q);
  const [data, setData] = useState<Page<AdminUser> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<{ tone: "success" | "warning" | "error"; text: string } | null>(null);
  const [inviteOpen, setInviteOpen] = useState(false);
  const [editing, setEditing] = useState<AdminUser | null>(null);
  const key = params.toString();
  const canManage = can("users:manage");

  const load = useCallback(() => {
    api<Page<AdminUser>>("/admin/users", { query: filters }).then(
      (d) => {
        setData(d);
        setError(null);
      },
      (e) => setError(e instanceof ApiError ? e.message : "Failed to load users."),
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);
  useEffect(load, [load]);

  function apply(next: Partial<typeof filters>) {
    const merged = { ...filters, ...next };
    const qs = new URLSearchParams();
    Object.entries(merged).forEach(([k, v]) => {
      if (v && !(k === "page" && v === 1)) qs.set(k, String(v));
    });
    router.push(`/app/admin/users${qs.toString() ? `?${qs}` : ""}`);
  }

  async function action(u: AdminUser, kind: "unlock" | "resend-invite") {
    setNotice(null);
    try {
      if (kind === "unlock") {
        await api(`/admin/users/${u.id}/unlock`, { method: "POST" });
        setNotice({ tone: "success", text: `${u.full_name} unlocked.` });
      } else {
        const res = await api<EmailDispatchResult>(`/admin/users/${u.id}/resend-invite`, { method: "POST" });
        setNotice({ tone: res.email_delivery === "NOT_CONFIGURED" ? "warning" : "success", text: res.message });
      }
      load();
    } catch (e) {
      setNotice({ tone: "error", text: e instanceof ApiError ? e.message : "Action failed." });
    }
  }

  return (
    <>
      <PageHeader
        title="Users"
        description="Applicants self-register. Staff accounts are created by invitation and activated when the invitee sets a password."
        action={canManage && <Button onClick={() => setInviteOpen(true)}>Invite staff user</Button>}
      />
      {notice && <Alert tone={notice.tone} className="mb-4">{notice.text}</Alert>}
      <Card>
        <form
          className="flex flex-wrap items-end gap-3 border-b border-slate-100 px-5 py-4"
          onSubmit={(e) => {
            e.preventDefault();
            apply({ q, page: 1 });
          }}
        >
          <div className="w-64">
            <label htmlFor="u-q" className="mb-1 block text-xs font-medium text-slate-600">Search name or email</label>
            <Input id="u-q" value={q} onChange={(e) => setQ(e.target.value)} />
          </div>
          <div className="w-44">
            <label htmlFor="u-role" className="mb-1 block text-xs font-medium text-slate-600">Role</label>
            <Select id="u-role" value={filters.role} onChange={(e) => apply({ role: e.target.value, page: 1 })}>
              <option value="">All roles</option>
              <option value="APPLICANT">Applicant</option>
              <option value="REVIEWER">Reviewer</option>
              <option value="SENIOR_REVIEWER">Senior Reviewer</option>
              <option value="ADMIN">Administrator</option>
            </Select>
          </div>
          <div className="w-40">
            <label htmlFor="u-status" className="mb-1 block text-xs font-medium text-slate-600">Status</label>
            <Select id="u-status" value={filters.status} onChange={(e) => apply({ status: e.target.value, page: 1 })}>
              <option value="">Any status</option>
              <option value="active">Active</option>
              <option value="unverified">Unverified</option>
              <option value="invited">Invited</option>
              <option value="locked">Locked</option>
              <option value="inactive">Deactivated</option>
            </Select>
          </div>
          <Button type="submit" variant="secondary">Search</Button>
        </form>
        {error && <Alert tone="error" className="m-5">{error}</Alert>}
        {!data ? (
          <Spinner />
        ) : data.items.length === 0 ? (
          <EmptyState title="No users match these filters" />
        ) : (
          <div className="relative overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-slate-100 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="px-5 py-3 font-medium">User</th>
                  <th className="px-5 py-3 font-medium">Role</th>
                  <th className="px-5 py-3 font-medium">Scope</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium">Last sign-in</th>
                  <th className="px-5 py-3 font-medium">Joined</th>
                  {canManage && <th className="px-5 py-3 font-medium"><span className="sr-only">Actions</span></th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {data.items.map((u) => {
                  const st = userStatus(u);
                  return (
                    <tr key={u.id}>
                      <td className="px-5 py-3">
                        <p className="font-medium text-slate-900">{u.full_name}</p>
                        <p className="text-slate-500">{u.email}</p>
                      </td>
                      <td className="px-5 py-3 text-slate-700">{u.role.name}</td>
                      <td className="px-5 py-3 text-xs text-slate-600">
                        {u.role.code === "APPLICANT" ? "Own records" : `${u.region ?? "No region"} · L${u.clearance_level}`}
                      </td>
                      <td className="px-5 py-3"><Badge tone={st.tone}>{st.label}</Badge></td>
                      <td className="whitespace-nowrap px-5 py-3 text-slate-600">{formatDateTime(u.last_login_at)}</td>
                      <td className="whitespace-nowrap px-5 py-3 text-slate-600">{formatDate(u.created_at)}</td>
                      {canManage && (
                        <td className="whitespace-nowrap px-5 py-3 text-right">
                          <div className="flex justify-end gap-2">
                            {isLocked(u.locked_until) && <Button size="sm" variant="secondary" onClick={() => action(u, "unlock")}>Unlock</Button>}
                            {u.invitation_pending && u.is_active && <Button size="sm" variant="secondary" onClick={() => action(u, "resend-invite")}>Resend invite</Button>}
                            {u.id !== me?.user.id && <Button size="sm" variant="ghost" onClick={() => setEditing(u)}>Edit</Button>}
                          </div>
                        </td>
                      )}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
        {data && <Pagination page={data.page} pageSize={data.page_size} total={data.total} onPage={(p) => apply({ page: p })} />}
      </Card>
      <InviteUserDialog
        open={inviteOpen}
        onClose={() => setInviteOpen(false)}
        onDone={(text, tone) => {
          setInviteOpen(false);
          setNotice({ text, tone });
          load();
        }}
      />
      <EditUserDialog
        user={editing}
        onClose={() => setEditing(null)}
        onDone={(text) => {
          setEditing(null);
          setNotice({ tone: "success", text });
          load();
        }}
      />
    </>
  );
}
