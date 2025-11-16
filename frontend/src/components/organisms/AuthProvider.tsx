// Authentication provider component

'use client';

import * as React from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase';
import { setAuthToken } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import type { User } from '@/types';

interface AuthProviderProps {
  children: React.ReactNode;
}

const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const { setUser, setIsLoading } = useAuthStore();
  const router = useRouter();
  const supabase = createClient();

  React.useEffect(() => {
    const initAuth = async () => {
      try {
        // Get initial session
        const {
          data: { session },
        } = await supabase.auth.getSession();

        if (session) {
          const user: User = {
            id: session.user.id,
            email: session.user.email || '',
            name: session.user.user_metadata?.name,
            avatar_url: session.user.user_metadata?.avatar_url,
          };
          setUser(user);
          setAuthToken(session.access_token);
        } else {
          setUser(null);
          setAuthToken(null);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        setUser(null);
        setAuthToken(null);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(async (event, session) => {
      if (session) {
        const user: User = {
          id: session.user.id,
          email: session.user.email || '',
          name: session.user.user_metadata?.name,
          avatar_url: session.user.user_metadata?.avatar_url,
        };
        setUser(user);
        setAuthToken(session.access_token);

        if (event === 'SIGNED_IN') {
          router.push('/chat');
        }
      } else {
        setUser(null);
        setAuthToken(null);
        router.push('/login');
      }
    });

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  return <>{children}</>;
};

export default AuthProvider;
