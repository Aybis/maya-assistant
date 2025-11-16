// Chat UI store using Zustand

import { create } from 'zustand';

interface ChatState {
  isStreaming: boolean;
  streamingContent: string;
  inputValue: string;
  selectedModel: string;
  sidebarOpen: boolean;

  // Actions
  setIsStreaming: (isStreaming: boolean) => void;
  setStreamingContent: (content: string) => void;
  appendStreamingContent: (chunk: string) => void;
  setInputValue: (value: string) => void;
  setSelectedModel: (model: string) => void;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  reset: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  isStreaming: false,
  streamingContent: '',
  inputValue: '',
  selectedModel: 'gpt-3.5-turbo',
  sidebarOpen: true,

  setIsStreaming: (isStreaming) => set({ isStreaming }),

  setStreamingContent: (content) => set({ streamingContent: content }),

  appendStreamingContent: (chunk) =>
    set((state) => ({ streamingContent: state.streamingContent + chunk })),

  setInputValue: (value) => set({ inputValue: value }),

  setSelectedModel: (model) => set({ selectedModel: model }),

  setSidebarOpen: (open) => set({ sidebarOpen: open }),

  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),

  reset: () =>
    set({
      isStreaming: false,
      streamingContent: '',
      inputValue: '',
    }),
}));
