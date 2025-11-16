// Main chat layout template

'use client';

import * as React from 'react';
import Sidebar from '../organisms/Sidebar';
import ChatArea from '../organisms/ChatArea';
import Spinner from '../atoms/Spinner';
import { useConversationStore } from '@/store/conversationStore';
import { conversationsApi, modelsApi } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';

const ChatLayout: React.FC = () => {
  const { isLoading } = useAuthStore();
  const { setConversations, setModels, setCurrentConversation } = useConversationStore();
  const [isInitializing, setIsInitializing] = React.useState(true);

  React.useEffect(() => {
    const initialize = async () => {
      try {
        // Load conversations and models in parallel
        const [conversations, models] = await Promise.all([
          conversationsApi.getAll(),
          modelsApi.getAll(),
        ]);

        setConversations(conversations);
        setModels(models);

        // Set the first conversation as current if exists
        if (conversations.length > 0) {
          setCurrentConversation(conversations[0]);
        }
      } catch (error) {
        console.error('Failed to initialize:', error);
      } finally {
        setIsInitializing(false);
      }
    };

    if (!isLoading) {
      initialize();
    }
  }, [isLoading]);

  if (isLoading || isInitializing) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-hidden">
        <ChatArea />
      </main>
    </div>
  );
};

export default ChatLayout;
