// Sidebar component for conversations

'use client';

import * as React from 'react';
import { Plus, LogOut, Menu } from 'lucide-react';
import Button from '../atoms/Button';
import ConversationItem from '../molecules/ConversationItem';
import { useConversationStore } from '@/store/conversationStore';
import { useChatStore } from '@/store/chatStore';
import { useAuthStore } from '@/store/authStore';
import { conversationsApi } from '@/lib/api';
import { createClient } from '@/lib/supabase';
import { cn } from '@/lib/utils';

const Sidebar: React.FC = () => {
  const { conversations, currentConversation, setCurrentConversation, deleteConversation, addConversation } =
    useConversationStore();
  const { sidebarOpen, setSidebarOpen } = useChatStore();
  const { user } = useAuthStore();
  const supabase = createClient();

  const handleNewChat = async () => {
    try {
      const newConversation = await conversationsApi.create({
        title: 'New Chat',
      });
      addConversation(newConversation);
      setCurrentConversation(newConversation);
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  const handleDeleteConversation = async (
    e: React.MouseEvent,
    conversationId: string
  ) => {
    e.stopPropagation();
    try {
      await conversationsApi.delete(conversationId);
      deleteConversation(conversationId);
    } catch (error) {
      console.error('Failed to delete conversation:', error);
    }
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
  };

  if (!sidebarOpen) {
    return (
      <Button
        variant="ghost"
        size="icon"
        className="fixed top-4 left-4 z-40"
        onClick={() => setSidebarOpen(true)}
      >
        <Menu className="h-5 w-5" />
      </Button>
    );
  }

  return (
    <div className="flex flex-col h-full w-64 border-r bg-background">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <h2 className="font-semibold text-lg">Maya Assistant</h2>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setSidebarOpen(false)}
          className="md:hidden"
        >
          <Menu className="h-5 w-5" />
        </Button>
      </div>

      {/* New Chat Button */}
      <div className="p-3">
        <Button onClick={handleNewChat} className="w-full">
          <Plus className="h-4 w-4 mr-2" />
          New Chat
        </Button>
      </div>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto px-3 space-y-1">
        {conversations.map((conversation) => (
          <ConversationItem
            key={conversation.id}
            conversation={conversation}
            isActive={currentConversation?.id === conversation.id}
            onClick={() => setCurrentConversation(conversation)}
            onDelete={(e) => handleDeleteConversation(e, conversation.id)}
          />
        ))}
      </div>

      {/* User Section */}
      <div className="p-4 border-t">
        <div className="flex items-center justify-between">
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.email}</p>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={handleSignOut}
            title="Sign out"
          >
            <LogOut className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
