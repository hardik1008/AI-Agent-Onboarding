import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { LoginForm } from "@/app/(auth)/login/LoginForm";

const replace = vi.fn();
const refresh = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ replace, push: vi.fn() }),
  useSearchParams: () => new URLSearchParams("next=/app/admin/users"),
}));
vi.mock("@/lib/auth", () => ({ useAuth: () => ({ me: null, loading: false, refresh }) }));

describe("LoginForm", () => {
  beforeEach(() => {
    replace.mockReset();
    refresh.mockReset();
  });

  it("shows the server error message on failed sign-in", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ error: { code: "INVALID_CREDENTIALS", message: "Incorrect email or password." } }), { status: 401 }),
    );
    render(<LoginForm />);
    await userEvent.type(screen.getByLabelText("Email"), "a@example.com");
    await userEvent.type(screen.getByLabelText("Password"), "wrong-password1");
    await userEvent.click(screen.getByRole("button", { name: "Sign in" }));
    expect(await screen.findByText("Incorrect email or password.")).toBeInTheDocument();
    expect(replace).not.toHaveBeenCalled();
  });

  it("refreshes the session and redirects to the requested page on success", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ user: {}, permissions: [] }), { status: 200 }));
    render(<LoginForm />);
    await userEvent.type(screen.getByLabelText("Email"), "a@example.com");
    await userEvent.type(screen.getByLabelText("Password"), "Correct-password1");
    await userEvent.click(screen.getByRole("button", { name: "Sign in" }));
    await waitFor(() => expect(replace).toHaveBeenCalledWith("/app/admin/users"));
    expect(refresh).toHaveBeenCalled();
    expect(JSON.parse(fetchMock.mock.calls[0][1]!.body as string)).toEqual({ email: "a@example.com", password: "Correct-password1" });
  });
});
