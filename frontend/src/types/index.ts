// Type definitions for the application

export interface User {
  id: string;
  email: string;
  name?: string;
  avatar_url?: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  model: string;
  created_at: string;
  updated_at: string;
  message_count?: number;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  content: string;
  model?: string;
  created_at: string;
}

export interface AIModel {
  id: string;
  name: string;
  provider: 'openai' | 'anthropic' | 'google';
  description: string;
}

export interface ConversationCreate {
  title?: string;
  model?: string;
}

export interface ConversationUpdate {
  title?: string;
  model?: string;
}

export interface MessageCreate {
  content: string;
  model?: string;
}

export interface StreamChunk {
  content?: string;
  done?: boolean;
  error?: string;
}
