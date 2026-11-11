import { describe, expect, it, vi } from "vitest";
import { api, ApiError, buildUrl } from "@/lib/api";

function mockFetch(status: number, body: unknown) {
  return vi.spyOn(globalThis, "fetch").mockImplementation(async () => new Response(JSON.stringify(body), { status }));
}

describe("api client", () => {
  it("sends the CSRF cookie as a header on unsafe methods only", async () => {
    document.cookie = "pn_csrf=abc123; path=/";
    const fetchMock = mockFetch(200, { ok: true });
    await api("/auth/logout", { method: "POST" });
    await api("/auth/me");
    const [, postInit] = fetchMock.mock.calls[0];
    const [, getInit] = fetchMock.mock.calls[1];
    expect((postInit!.headers as Record<string, string>)["X-CSRF-Token"]).toBe("abc123");
    expect((getInit!.headers as Record<string, string>)["X-CSRF-Token"]).toBeUndefined();
    expect(postInit!.credentials).toBe("same-origin");
    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/auth/logout");
  });

  it("raises structured ApiError with field errors", async () => {
    mockFetch(422, {
      error: { code: "VALIDATION_ERROR", message: "Some fields are invalid.", details: [{ field: "email", message: "Bad email" }] },
    });
    const err = await api("/auth/register", { method: "POST", body: {} }).catch((e: ApiError) => e) as ApiError;
    expect(err).toBeInstanceOf(ApiError);
    expect(err.status).toBe(422);
    expect(err.code).toBe("VALIDATION_ERROR");
    expect(err.fieldErrors).toEqual({ email: "Bad email" });
  });

  it("maps network failures to NETWORK_ERROR", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new TypeError("Failed to fetch"));
    const err = await api("/auth/me").catch((e: ApiError) => e) as ApiError;
    expect(err.code).toBe("NETWORK_ERROR");
  });

  it("builds query strings and drops empty values", () => {
    expect(buildUrl("/x", { a: "1", b: "", c: undefined, d: 2 })).toBe("/x?a=1&d=2");
    expect(buildUrl("/x")).toBe("/x");
  });
});
