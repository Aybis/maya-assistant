// Conversation store using Zustand

import { create } from 'zustand';
import type { Conversation, Message, AIModel } from '@/types';

interface ConversationState {
  conversations: Conversation[];
  currentConversation: Conversation | null;
  messages: Message[];
  models: AIModel[];
  isLoading: boolean;
  error: string | null;

  // Actions
  setConversations: (conversations: Conversation[]) => void;
  setCurrentConversation: (conversation: Conversation | null) => void;
  setMessages: (messages: Message[]) => void;
  setModels: (models: AIModel[]) => void;
  setIsLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  addMessage: (message: Message) => void;
  updateMessage: (messageId: string, content: string) => void;
  addConversation: (conversation: Conversation) => void;
  updateConversation: (conversationId: string, update: Partial<Conversation>) => void;
  deleteConversation: (conversationId: string) => void;
  reset: () => void;
}

export const useConversationStore = create<ConversationState>((set) => ({
  conversations: [],
  currentConversation: null,
  messages: [],
  models: [],
  isLoading: false,
  error: null,

  setConversations: (conversations) => set({ conversations }),

  setCurrentConversation: (conversation) => set({ currentConversation: conversation }),

  setMessages: (messages) => set({ messages }),

  setModels: (models) => set({ models }),

  setIsLoading: (isLoading) => set({ isLoading }),

  setError: (error) => set({ error }),

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  updateMessage: (messageId, content) =>
    set((state) => ({
      messages: state.messages.map((msg) =>
        msg.id === messageId ? { ...msg, content } : msg
      ),
    })),

  addConversation: (conversation) =>
    set((state) => ({
      conversations: [conversation, ...state.conversations],
    })),

  updateConversation: (conversationId, update) =>
    set((state) => ({
      conversations: state.conversations.map((conv) =>
        conv.id === conversationId ? { ...conv, ...update } : conv
      ),
      currentConversation:
        state.currentConversation?.id === conversationId
          ? { ...state.currentConversation, ...update }
          : state.currentConversation,
    })),

  deleteConversation: (conversationId) =>
    set((state) => ({
      conversations: state.conversations.filter((conv) => conv.id !== conversationId),
      currentConversation:
        state.currentConversation?.id === conversationId
          ? null
          : state.currentConversation,
    })),

  reset: () =>
    set({
      conversations: [],
      currentConversation: null,
      messages: [],
      models: [],
      isLoading: false,
      error: null,
    }),
}));
