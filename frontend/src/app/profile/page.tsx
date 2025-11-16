'use client';

import * as React from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, User, Mail, Calendar } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import Button from '@/components/atoms/Button';

export default function ProfilePage() {
  const router = useRouter();
  const { user } = useAuthStore();

  if (!user) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-muted-foreground mb-4">Please sign in to view your profile</p>
          <Button onClick={() => router.push('/login')}>Sign In</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-card">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => router.push('/chat')}
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <h1 className="text-2xl font-bold">Profile</h1>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="bg-card border rounded-lg shadow-sm">
          {/* Profile Header */}
          <div className="p-6 border-b">
            <div className="flex items-center gap-4">
              <div className="h-20 w-20 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                <User className="h-10 w-10 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-xl font-semibold">{user.email?.split('@')[0]}</h2>
                <p className="text-sm text-muted-foreground">Maya Assistant User</p>
              </div>
            </div>
          </div>

          {/* Profile Details */}
          <div className="p-6 space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Account Information</h3>

              <div className="space-y-4">
                {/* Email */}
                <div className="flex items-start gap-3 p-4 rounded-lg bg-muted/50">
                  <Mail className="h-5 w-5 text-muted-foreground mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-muted-foreground">Email</p>
                    <p className="text-base">{user.email}</p>
                  </div>
                </div>

                {/* User ID */}
                <div className="flex items-start gap-3 p-4 rounded-lg bg-muted/50">
                  <User className="h-5 w-5 text-muted-foreground mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-muted-foreground">User ID</p>
                    <p className="text-base font-mono text-sm">{user.id}</p>
                  </div>
                </div>

                {/* Account Type */}
                <div className="flex items-start gap-3 p-4 rounded-lg bg-muted/50">
                  <Calendar className="h-5 w-5 text-muted-foreground mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-muted-foreground">Account Type</p>
                    <p className="text-base">Free Tier</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Usage Stats (Placeholder) */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Usage Statistics</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-lg bg-muted/50 text-center">
                  <p className="text-3xl font-bold text-primary">-</p>
                  <p className="text-sm text-muted-foreground mt-1">Total Conversations</p>
                </div>
                <div className="p-4 rounded-lg bg-muted/50 text-center">
                  <p className="text-3xl font-bold text-primary">-</p>
                  <p className="text-sm text-muted-foreground mt-1">Messages Sent</p>
                </div>
                <div className="p-4 rounded-lg bg-muted/50 text-center">
                  <p className="text-3xl font-bold text-primary">-</p>
                  <p className="text-sm text-muted-foreground mt-1">AI Models Used</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
