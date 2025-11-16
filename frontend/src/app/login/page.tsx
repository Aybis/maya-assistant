// Login page

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase';
import { useAuthStore } from '@/store/authStore';
import Button from '@/components/atoms/Button';
import Input from '@/components/atoms/Input';
import Spinner from '@/components/atoms/Spinner';

export default function LoginPage() {
  const router = useRouter();
  const { user, isLoading } = useAuthStore();
  const supabase = createClient();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (!isLoading && user) {
      router.push('/chat');
    }
  }, [user, isLoading, router]);

  const handleGoogleSignIn = async () => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      });

      if (error) {
        console.error('Sign in error:', error);
      }
    } catch (error) {
      console.error('Sign in error:', error);
    }
  };

  const handleEmailSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) {
        console.error('Sign in error:', error);
        alert('Invalid email or password');
      }
    } catch (error) {
      console.error('Sign in error:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#F9F5EC]">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F9F5EC]">
      {/* Header Navigation */}
      <header className="flex items-center justify-between px-8 py-4">
        <div className="text-2xl font-bold text-black">Maya Assistant</div>
        <div className="flex items-center gap-6">
          <a
            href="mailto:contact@maya-assistant.com"
            className="text-sm text-black hover:opacity-70 transition-opacity"
          >
            contact@maya-assistant.com
          </a>
          <a
            href="#"
            className="text-sm text-black hover:opacity-70 transition-opacity"
          >
            Sign Up
          </a>
          <Button
            className="bg-[#F7C796] text-black hover:bg-[#f5b978] rounded-lg px-6"
            variant="default"
          >
            Request Demo
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">
          {/* Login Card */}
          <div className="bg-white rounded-2xl shadow-lg p-8 space-y-6">
            <div>
              <h1 className="text-3xl font-bold text-black mb-2">
                Agent Login
              </h1>
            </div>

            {/* Email/Password Form */}
            <form onSubmit={handleEmailSignIn} className="space-y-4">
              <div>
                <Input
                  type="email"
                  placeholder="Enter Email / Phone No"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full h-12 rounded-xl border-gray-300 focus:border-[#F7C796] focus:ring-[#F7C796]"
                  required
                />
              </div>

              <div className="relative">
                <Input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Passcode"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full h-12 rounded-xl border-gray-300 focus:border-[#F7C796] focus:ring-[#F7C796] pr-16"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500 hover:text-black"
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>

              <Button
                type="submit"
                className="w-full h-12 bg-[#F7C796] text-black hover:bg-[#f5b978] rounded-xl text-base font-semibold"
              >
                Sign In
              </Button>
            </form>

            <div className="text-center">
              <a
                href="#"
                className="text-sm text-black hover:opacity-70 transition-opacity"
              >
                Having trouble in sign in?
              </a>
            </div>

            {/* Divider */}
            <div className="flex items-center gap-3">
              <div className="flex-1 h-px bg-gray-300"></div>
              <span className="text-sm text-gray-500">Or Sign in with</span>
              <div className="flex-1 h-px bg-gray-300"></div>
            </div>

            {/* Social Sign-In Buttons */}
            <div className="grid grid-cols-3 gap-3">
              <button
                onClick={handleGoogleSignIn}
                className="h-12 flex items-center justify-center rounded-xl border-2 border-gray-200 hover:border-gray-300 hover:bg-gray-50 transition-all"
              >
                <svg className="w-6 h-6" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  />
                </svg>
              </button>

              <button className="h-12 flex items-center justify-center rounded-xl border-2 border-gray-200 hover:border-gray-300 hover:bg-gray-50 transition-all">
                <svg className="w-6 h-6" viewBox="0 0 24 24" fill="black">
                  <path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z" />
                </svg>
              </button>

              <button className="h-12 flex items-center justify-center rounded-xl border-2 border-gray-200 hover:border-gray-300 hover:bg-gray-50 transition-all">
                <svg className="w-6 h-6" viewBox="0 0 24 24" fill="#1877F2">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                </svg>
              </button>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-6 text-center space-y-2">
            <p className="text-sm text-black">
              Don't have an account?{' '}
              <a href="#" className="font-semibold hover:opacity-70">
                Request Now
              </a>
            </p>
            <p className="text-xs text-gray-600">
              Copyright @Maya Assistant 2024 |{' '}
              <a href="#" className="hover:opacity-70">
                Privacy Policy
              </a>
            </p>
          </div>
        </div>

        {/* Decorative Illustration */}
        <div className="hidden lg:block ml-16">
          <svg
            width="300"
            height="300"
            viewBox="0 0 300 300"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Simple line-art illustration of a person with laptop */}
            <circle cx="150" cy="80" r="30" stroke="black" strokeWidth="2" />
            <path
              d="M150 110 L150 180 M150 140 L120 160 M150 140 L180 160 M150 180 L120 220 M150 180 L180 220"
              stroke="black"
              strokeWidth="2"
              strokeLinecap="round"
            />
            <rect
              x="100"
              y="150"
              width="100"
              height="60"
              rx="4"
              stroke="black"
              strokeWidth="2"
              fill="none"
            />
            <line
              x1="110"
              y1="160"
              x2="190"
              y2="160"
              stroke="black"
              strokeWidth="1"
            />
            <line
              x1="110"
              y1="170"
              x2="170"
              y2="170"
              stroke="black"
              strokeWidth="1"
            />
          </svg>
        </div>
      </div>
    </div>
  );
}
