const dateTime = new Intl.DateTimeFormat("en-IN", { dateStyle: "medium", timeStyle: "short" });
const dateOnly = new Intl.DateTimeFormat("en-IN", { dateStyle: "medium" });

export function formatDateTime(value: string | null | undefined): string {
  return value ? dateTime.format(new Date(value)) : "—";
}

export function formatDate(value: string | null | undefined): string {
  return value ? dateOnly.format(new Date(value)) : "—";
}

export function describeUserAgent(ua: string | null): string {
  if (!ua) return "Unknown device";
  const browser = /Edg\//.test(ua)
    ? "Edge"
    : /Chrome\//.test(ua)
      ? "Chrome"
      : /Firefox\//.test(ua)
        ? "Firefox"
        : /Safari\//.test(ua)
          ? "Safari"
          : "Browser";
  const os = /Windows/.test(ua)
    ? "Windows"
    : /Android/.test(ua)
      ? "Android"
      : /iPhone|iPad/.test(ua)
        ? "iOS"
        : /Mac OS X/.test(ua)
          ? "macOS"
          : /Linux/.test(ua)
            ? "Linux"
            : "";
  return os ? `${browser} on ${os}` : browser;
}

export function isLocked(lockedUntil: string | null): boolean {
  return !!lockedUntil && new Date(lockedUntil).getTime() > Date.now();
}

export function safeNext(next: string | null | undefined): string {
  return next && next.startsWith("/app") && !next.startsWith("//") ? next : "/app";
}
