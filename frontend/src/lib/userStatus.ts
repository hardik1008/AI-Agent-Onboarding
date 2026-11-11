import { isLocked } from "./format";
import type { AdminUser } from "./types";

export function userStatus(u: AdminUser): { label: string; tone: "success" | "warning" | "danger" | "neutral" } {
  if (!u.is_active) return { label: "Deactivated", tone: "danger" };
  if (isLocked(u.locked_until)) return { label: "Locked", tone: "danger" };
  if (u.invitation_pending) return { label: "Invited", tone: "neutral" };
  if (!u.email_verified) return { label: "Unverified", tone: "warning" };
  return { label: "Active", tone: "success" };
}
