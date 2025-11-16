// Main chat area component

'use client';

import * as React from 'react';
import MessageBubble from '../molecules/MessageBubble';
import ChatInput from '../molecules/ChatInput';
import ModelSelector from '../molecules/ModelSelector';
import Spinner from '../atoms/Spinner';
import { useConversationStore } from '@/store/conversationStore';
import { useChatStore } from '@/store/chatStore';
import { messagesApi, conversationsApi } from '@/lib/api';
import type { Message } from '@/types';

const ChatArea: React.FC = () => {
  const {
    currentConversation,
    messages,
    groupedModels,
    setMessages,
    addMessage,
    updateConversation,
  } = useConversationStore();

  const {
    isStreaming,
    streamingContent,
    inputValue,
    selectedModel,
    setIsStreaming,
    setStreamingContent,
    appendStreamingContent,
    setInputValue,
    setSelectedModel,
    reset: resetChat,
  } = useChatStore();

  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const [isLoadingMessages, setIsLoadingMessages] = React.useState(false);

  // Load messages when conversation changes
  React.useEffect(() => {
    const loadMessages = async () => {
      if (!currentConversation) {
        setMessages([]);
        return;
      }

      setIsLoadingMessages(true);
      try {
        const conversationMessages = await messagesApi.getAll(
          currentConversation.id
        );
        setMessages(conversationMessages);
        setSelectedModel(currentConversation.model);
      } catch (error) {
        console.error('Failed to load messages:', error);
      } finally {
        setIsLoadingMessages(false);
      }
    };

    loadMessages();
  }, [currentConversation?.id]);

  // Auto-scroll to bottom
  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingContent]);

  const handleSendMessage = async () => {
    if (!currentConversation || !inputValue.trim() || isStreaming) return;

    const userMessage = inputValue;
    setInputValue('');
    setIsStreaming(true);
    setStreamingContent('');

    // Create temporary user message
    const tempUserMessage: Message = {
      id: `temp-${Date.now()}`,
      conversation_id: currentConversation.id,
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString(),
    };

    addMessage(tempUserMessage);

    try {
      // Send message and stream response
      await messagesApi.send(
        currentConversation.id,
        { content: userMessage, model: selectedModel },
        (chunk) => {
          appendStreamingContent(chunk);
        },
        () => {
          // On done, reload messages from server
          messagesApi.getAll(currentConversation.id).then((msgs) => {
            setMessages(msgs);
            setIsStreaming(false);
            resetChat();

            // Update conversation title if it's the first message
            if (msgs.length === 2) {
              const title = userMessage.slice(0, 50);
              conversationsApi
                .update(currentConversation.id, { title })
                .then((updated) => {
                  updateConversation(currentConversation.id, updated);
                });
            }
          });
        },
        (error) => {
          console.error('Streaming error:', error);
          setIsStreaming(false);
          resetChat();
        }
      );
    } catch (error) {
      console.error('Failed to send message:', error);
      setIsStreaming(false);
      resetChat();
    }
  };

  if (!currentConversation) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to Maya Assistant</h1>
        <p className="text-lg text-muted-foreground mb-8">
          Chat with multiple AI models in one place
        </p>
        <p className="text-sm text-muted-foreground">
          Select a conversation or create a new one to get started
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header with model selector */}
      <div className="border-b p-4">
        <ModelSelector
          groupedModels={groupedModels}
          selectedModel={selectedModel}
          onSelectModel={setSelectedModel}
          disabled={isStreaming}
        />
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4">
        {isLoadingMessages ? (
          <div className="flex items-center justify-center h-full">
            <Spinner size="lg" />
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}

            {/* Streaming message */}
            {isStreaming && streamingContent && (
              <MessageBubble
                message={{
                  id: 'streaming',
                  conversation_id: currentConversation.id,
                  role: 'assistant',
                  content: streamingContent,
                  created_at: new Date().toISOString(),
                }}
                isStreaming={true}
              />
            )}

            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t p-4">
        <ChatInput
          value={inputValue}
          onChange={setInputValue}
          onSubmit={handleSendMessage}
          disabled={isStreaming}
          placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
        />
      </div>
    </div>
  );
};

export default ChatArea;
