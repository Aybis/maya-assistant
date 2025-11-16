// Middleware for authentication

import { createServerClient } from '@supabase/ssr';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(req: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request: req,
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return req.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) => req.cookies.set(name, value));
          supabaseResponse = NextResponse.next({
            request: req,
          });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  const {
    data: { session },
  } = await supabase.auth.getSession();

  // Protect /chat routes
  if (req.nextUrl.pathname.startsWith('/chat') && !session) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  // Redirect to chat if already logged in
  if (req.nextUrl.pathname === '/login' && session) {
    return NextResponse.redirect(new URL('/chat', req.url));
  }

  return supabaseResponse;
}

export const config = {
  matcher: ['/', '/chat/:path*', '/login'],
};
