import { NextResponse, type NextRequest } from "next/server";

const SESSION_COOKIE = "pn_session";

// UX-only redirect; the backend independently authenticates every API request.
export function middleware(request: NextRequest) {
  if (!request.cookies.get(SESSION_COOKIE)) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    url.search = `?next=${encodeURIComponent(request.nextUrl.pathname + request.nextUrl.search)}`;
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = { matcher: ["/app/:path*"] };
