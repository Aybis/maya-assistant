'use client';

import * as React from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, User, Mail, Calendar, Brain, Sparkles, RefreshCw, CheckCircle, XCircle } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import Button from '@/components/atoms/Button';
import { memoryApi } from '@/lib/api';

export default function ProfilePage() {
  const router = useRouter();
  const { user } = useAuthStore();

  // Memory state
  const [memoryStats, setMemoryStats] = React.useState<any>(null);
  const [isProcessing, setIsProcessing] = React.useState(false);
  const [processResult, setProcessResult] = React.useState<any>(null);
  const [isLoadingStats, setIsLoadingStats] = React.useState(false);

  // Load memory stats on mount
  React.useEffect(() => {
    if (user) {
      loadMemoryStats();
    }
  }, [user]);

  const loadMemoryStats = async () => {
    setIsLoadingStats(true);
    try {
      const stats = await memoryApi.getStats();
      setMemoryStats(stats);
      setProcessResult(null); // Clear any previous errors
    } catch (error: any) {
      console.error('Failed to load memory stats:', error);
      // Show migration needed error
      if (error.response?.status === 400 || error.response?.data?.detail?.includes('migration')) {
        setProcessResult({
          error: 'Database migration required. Please run the migration SQL in Supabase first.',
          migrationNeeded: true
        });
      } else if (error.response?.status === 500) {
        setProcessResult({
          error: 'Database tables not found. Please run the migration SQL in Supabase.',
          migrationNeeded: true
        });
      }
      // Set empty stats as fallback
      setMemoryStats({
        memories: { total: 0, by_type: { preference: 0, fact: 0, goal: 0, context: 0, interest: 0 } },
        summaries: { total: 0 },
        conversations: { total: 0 }
      });
    } finally {
      setIsLoadingStats(false);
    }
  };

  const handleProcessConversations = async () => {
    setIsProcessing(true);
    setProcessResult(null);
    try {
      const result = await memoryApi.processAllConversations(20);
      setProcessResult(result);
      // Reload stats after processing
      await loadMemoryStats();
    } catch (error) {
      console.error('Failed to process conversations:', error);
      setProcessResult({ error: 'Failed to process conversations' });
    } finally {
      setIsProcessing(false);
    }
  };

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

            {/* Usage Stats */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Usage Statistics</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-lg bg-muted/50 text-center">
                  <p className="text-3xl font-bold text-primary">
                    {isLoadingStats ? '...' : memoryStats?.conversations?.total || 0}
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">Total Conversations</p>
                </div>
                <div className="p-4 rounded-lg bg-muted/50 text-center">
                  <p className="text-3xl font-bold text-primary">
                    {isLoadingStats ? '...' : memoryStats?.memories?.total || 0}
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">Stored Memories</p>
                </div>
                <div className="p-4 rounded-lg bg-muted/50 text-center">
                  <p className="text-3xl font-bold text-primary">
                    {isLoadingStats ? '...' : memoryStats?.summaries?.total || 0}
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">Conversation Summaries</p>
                </div>
              </div>
            </div>

            {/* Memory Management */}
            <div className="border-t pt-6">
              <div className="flex items-center gap-2 mb-4">
                <Brain className="h-5 w-5 text-primary" />
                <h3 className="text-lg font-semibold">AI Memory System</h3>
              </div>

              <div className="space-y-4">
                <div className="p-4 rounded-lg bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/20">
                  <div className="flex items-start gap-3">
                    <Sparkles className="h-5 w-5 text-purple-500 mt-0.5" />
                    <div className="flex-1">
                      <h4 className="font-semibold mb-1">Cross-Chat Memory</h4>
                      <p className="text-sm text-muted-foreground mb-3">
                        Enable the AI to remember your preferences, facts, and past conversations across different chats.
                        {memoryStats?.memories?.total === 0 && ' Click below to extract memories from your existing conversations.'}
                      </p>

                      {/* Process Button */}
                      <div className="flex items-center gap-3">
                        <Button
                          onClick={handleProcessConversations}
                          disabled={isProcessing}
                          className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                        >
                          {isProcessing ? (
                            <>
                              <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                              Processing...
                            </>
                          ) : (
                            <>
                              <Brain className="h-4 w-4 mr-2" />
                              {memoryStats?.memories?.total === 0 ? 'Initialize Memory System' : 'Refresh Memories'}
                            </>
                          )}
                        </Button>

                        <Button
                          variant="outline"
                          onClick={loadMemoryStats}
                          disabled={isLoadingStats}
                          size="icon"
                        >
                          <RefreshCw className={`h-4 w-4 ${isLoadingStats ? 'animate-spin' : ''}`} />
                        </Button>
                      </div>

                      {/* Process Result */}
                      {processResult && (
                        <div className={`mt-3 p-3 rounded-lg ${
                          processResult.error
                            ? 'bg-red-500/10 border border-red-500/20'
                            : 'bg-green-500/10 border border-green-500/20'
                        }`}>
                          <div className="flex items-start gap-2">
                            {processResult.error ? (
                              <XCircle className="h-4 w-4 text-red-500 mt-0.5" />
                            ) : (
                              <CheckCircle className="h-4 w-4 text-green-500 mt-0.5" />
                            )}
                            <div className="flex-1">
                              {processResult.error ? (
                                <>
                                  <p className="text-sm font-medium text-red-600 dark:text-red-400 mb-1">
                                    {processResult.error}
                                  </p>
                                  {processResult.migrationNeeded && (
                                    <div className="text-xs text-muted-foreground mt-2 space-y-1">
                                      <p className="font-medium">To fix this:</p>
                                      <ol className="list-decimal ml-4 space-y-0.5">
                                        <li>Open Supabase Dashboard → SQL Editor</li>
                                        <li>Run the migration from: <code className="bg-muted px-1 py-0.5 rounded">/database/migration_add_memory.sql</code></li>
                                        <li>Refresh this page</li>
                                      </ol>
                                    </div>
                                  )}
                                </>
                              ) : (
                                <>
                                  <p className="text-sm font-medium text-green-600 dark:text-green-400 mb-1">
                                    Successfully processed {processResult.conversations} conversations!
                                  </p>
                                  <div className="text-xs text-muted-foreground space-y-0.5">
                                    <p>• Extracted {processResult.memories_extracted} memories</p>
                                    <p>• Created {processResult.summaries_created} summaries</p>
                                    {processResult.errors?.length > 0 && (
                                      <p className="text-yellow-600">• {processResult.errors.length} errors occurred</p>
                                    )}
                                  </div>
                                </>
                              )}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Memory Breakdown */}
                {memoryStats && memoryStats.memories.total > 0 && (
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    <div className="p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 text-center">
                      <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                        {memoryStats.memories.by_type.preference}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">Preferences</p>
                    </div>
                    <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-center">
                      <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                        {memoryStats.memories.by_type.fact}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">Facts</p>
                    </div>
                    <div className="p-3 rounded-lg bg-purple-500/10 border border-purple-500/20 text-center">
                      <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                        {memoryStats.memories.by_type.goal}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">Goals</p>
                    </div>
                    <div className="p-3 rounded-lg bg-orange-500/10 border border-orange-500/20 text-center">
                      <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                        {memoryStats.memories.by_type.interest}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">Interests</p>
                    </div>
                    <div className="p-3 rounded-lg bg-gray-500/10 border border-gray-500/20 text-center">
                      <p className="text-2xl font-bold text-gray-600 dark:text-gray-400">
                        {memoryStats.memories.by_type.context}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">Context</p>
                    </div>
                  </div>
                )}

                {/* Info */}
                <div className="text-xs text-muted-foreground bg-muted/30 p-3 rounded-lg">
                  <p className="font-medium mb-1">How it works:</p>
                  <ul className="space-y-1 ml-4">
                    <li>• Memories are automatically extracted from your conversations</li>
                    <li>• AI uses this context in future chats to provide personalized responses</li>
                    <li>• New memories are created every 5 messages automatically</li>
                    <li>• Summaries help AI understand your conversation history</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
