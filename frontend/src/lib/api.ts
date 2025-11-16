// API client for backend communication

import axios from 'axios';
import type {
  Conversation,
  ConversationCreate,
  ConversationUpdate,
  Message,
  MessageCreate,
  AIModel,
  GroupedModels
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
export const setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// Conversations API
export const conversationsApi = {
  getAll: async (): Promise<Conversation[]> => {
    const { data } = await api.get('/api/conversations');
    return data;
  },

  create: async (conversation: ConversationCreate): Promise<Conversation> => {
    const { data } = await api.post('/api/conversations', conversation);
    return data;
  },

  getById: async (id: string): Promise<Conversation> => {
    const { data } = await api.get(`/api/conversations/${id}`);
    return data;
  },

  update: async (id: string, update: ConversationUpdate): Promise<Conversation> => {
    const { data } = await api.put(`/api/conversations/${id}`, update);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/conversations/${id}`);
  },
};

// Messages API
export const messagesApi = {
  getAll: async (conversationId: string): Promise<Message[]> => {
    const { data } = await api.get(`/api/conversations/${conversationId}/messages`);
    return data;
  },

  send: async (
    conversationId: string,
    message: MessageCreate,
    onChunk: (chunk: string) => void,
    onDone: () => void,
    onError: (error: string) => void
  ): Promise<void> => {
    const token = api.defaults.headers.common['Authorization']?.toString().replace('Bearer ', '');

    const response = await fetch(
      `${API_URL}/api/conversations/${conversationId}/messages`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(message),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('No response body');
    }

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));

            if (data.error) {
              onError(data.error);
            } else if (data.done) {
              onDone();
            } else if (data.content) {
              onChunk(data.content);
            }
          }
        }
      }
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Unknown error');
    }
  },
};

// Models API
export const modelsApi = {
  getAll: async (): Promise<GroupedModels> => {
    const { data } = await api.get('/api/models');
    return data;
  },
};

// Memory API
export const memoryApi = {
  getStats: async (): Promise<{
    memories: {
      total: number;
      by_type: {
        preference: number;
        fact: number;
        goal: number;
        context: number;
        interest: number;
      };
    };
    summaries: { total: number };
    conversations: { total: number };
  }> => {
    const { data } = await api.get('/api/memory-utils/stats');
    return data;
  },

  processAllConversations: async (limit: number = 20): Promise<{
    conversations: number;
    memories_extracted: number;
    summaries_created: number;
    errors: any[];
  }> => {
    const { data } = await api.post(`/api/memory-utils/process-all-conversations?limit=${limit}`);
    return data;
  },

  getAllMemories: async (): Promise<any[]> => {
    const { data } = await api.get('/api/memory');
    return data;
  },

  getRecentSummaries: async (limit: number = 10): Promise<any[]> => {
    const { data } = await api.get(`/api/summaries/recent?limit=${limit}`);
    return data;
  },
};

// Health check
export const healthCheck = async (): Promise<{ status: string }> => {
  const { data } = await api.get('/api/health');
  return data;
};

export default api;
