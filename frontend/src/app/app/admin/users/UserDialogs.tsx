"use client";

import { useEffect, useState } from "react";
import { Alert, Button, Dialog, Field, Input, Select } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import type { AdminUser, RoleCode } from "@/lib/types";

const STAFF_ROLES: { code: RoleCode; name: string }[] = [
  { code: "REVIEWER", name: "Reviewer" },
  { code: "SENIOR_REVIEWER", name: "Senior Reviewer" },
  { code: "ADMIN", name: "Administrator" },
];
const ALL_ROLES: { code: RoleCode; name: string }[] = [{ code: "APPLICANT", name: "Applicant" }, ...STAFF_ROLES];
const REGIONS = ["NORTH", "SOUTH", "EAST", "WEST", "ALL"];

export function InviteUserDialog({
  open,
  onClose,
  onDone,
}: {
  open: boolean;
  onClose: () => void;
  onDone: (message: string, tone: "success" | "warning") => void;
}) {
  const empty = { email: "", full_name: "", role: "REVIEWER" as RoleCode, region: "", clearance_level: 1 };
  const [form, setForm] = useState(empty);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (open) {
      setForm(empty);
      setErrors({});
      setError(null);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setErrors({});
    setError(null);
    try {
      const user = await api<AdminUser & { email_delivery?: string }>("/admin/users", {
        method: "POST",
        body: { ...form, region: form.region || null },
      });
      onDone(
        `Invitation created for ${user.email}. They activate the account by setting a password from the emailed link.`,
        "success",
      );
    } catch (err) {
      if (err instanceof ApiError) {
        setErrors(err.fieldErrors);
        setError(err.message);
      }
    } finally {
      setSaving(false);
    }
  }

  return (
    <Dialog open={open} onClose={onClose} title="Invite staff user" description="The invitee receives a single-use link to set their password.">
      <form onSubmit={submit} className="space-y-4" noValidate>
        {error && <Alert tone="error">{error}</Alert>}
        <Field label="Full name" htmlFor="inv-name" error={errors.full_name}>
          <Input id="inv-name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} invalid={!!errors.full_name} />
        </Field>
        <Field label="Work email" htmlFor="inv-email" error={errors.email}>
          <Input id="inv-email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} invalid={!!errors.email} />
        </Field>
        <Field label="Role" htmlFor="inv-role">
          <Select id="inv-role" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value as RoleCode })}>
            {STAFF_ROLES.map((r) => (
              <option key={r.code} value={r.code}>{r.name}</option>
            ))}
          </Select>
        </Field>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Region scope" htmlFor="inv-region" error={errors.region}>
            <Select id="inv-region" value={form.region} onChange={(e) => setForm({ ...form, region: e.target.value })}>
              <option value="">None</option>
              {REGIONS.map((r) => <option key={r} value={r}>{r}</option>)}
            </Select>
          </Field>
          <Field label="Clearance level" htmlFor="inv-clearance">
            <Select id="inv-clearance" value={form.clearance_level} onChange={(e) => setForm({ ...form, clearance_level: Number(e.target.value) })}>
              <option value={1}>1 — Standard</option>
              <option value={2}>2 — Elevated</option>
              <option value={3}>3 — Restricted</option>
            </Select>
          </Field>
        </div>
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" loading={saving}>Send invitation</Button>
        </div>
      </form>
    </Dialog>
  );
}

export function EditUserDialog({ user, onClose, onDone }: { user: AdminUser | null; onClose: () => void; onDone: (message: string) => void }) {
  const [form, setForm] = useState({ role: "APPLICANT" as RoleCode, region: "", clearance_level: 1, is_active: true });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (user) {
      setForm({ role: user.role.code, region: user.region ?? "", clearance_level: user.clearance_level, is_active: user.is_active });
      setError(null);
    }
  }, [user]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!user) return;
    setSaving(true);
    setError(null);
    const body: Record<string, unknown> = {};
    if (form.role !== user.role.code) body.role = form.role;
    if (form.is_active !== user.is_active) body.is_active = form.is_active;
    if (form.clearance_level !== user.clearance_level) body.clearance_level = form.clearance_level;
    if ((form.region || null) !== user.region) {
      if (form.region) body.region = form.region;
      else body.clear_region = true;
    }
    if (Object.keys(body).length === 0) {
      onClose();
      setSaving(false);
      return;
    }
    try {
      await api(`/admin/users/${user.id}`, { method: "PATCH", body });
      onDone(`${user.full_name} updated. Their active sessions were signed out where access changed.`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Update failed.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Dialog open={!!user} onClose={onClose} title={user ? `Edit ${user.full_name}` : "Edit user"} description={user?.email}>
      <form onSubmit={submit} className="space-y-4" noValidate>
        {error && <Alert tone="error">{error}</Alert>}
        <Field label="Role" htmlFor="edit-role">
          <Select id="edit-role" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value as RoleCode })}>
            {ALL_ROLES.map((r) => <option key={r.code} value={r.code}>{r.name}</option>)}
          </Select>
        </Field>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Region scope" htmlFor="edit-region">
            <Select id="edit-region" value={form.region} onChange={(e) => setForm({ ...form, region: e.target.value })}>
              <option value="">None</option>
              {REGIONS.map((r) => <option key={r} value={r}>{r}</option>)}
            </Select>
          </Field>
          <Field label="Clearance level" htmlFor="edit-clearance">
            <Select id="edit-clearance" value={form.clearance_level} onChange={(e) => setForm({ ...form, clearance_level: Number(e.target.value) })}>
              <option value={1}>1 — Standard</option>
              <option value={2}>2 — Elevated</option>
              <option value={3}>3 — Restricted</option>
            </Select>
          </Field>
        </div>
        <label className="flex items-center gap-3 text-sm text-slate-700">
          <input type="checkbox" checked={form.is_active} onChange={(e) => setForm({ ...form, is_active: e.target.checked })} className="h-4 w-4 rounded border-slate-300" />
          Account active (unchecking signs the user out and blocks sign-in)
        </label>
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" loading={saving}>Save changes</Button>
        </div>
      </form>
    </Dialog>
  );
}
