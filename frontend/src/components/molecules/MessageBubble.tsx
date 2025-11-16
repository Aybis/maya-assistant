// Message bubble component

'use client';

import * as React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { cn } from '@/lib/utils';
import Avatar from '../atoms/Avatar';
import type { Message } from '@/types';

interface MessageBubbleProps {
  message: Message;
  isStreaming?: boolean;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isStreaming }) => {
  const isUser = message.role === 'user';

  return (
    <div className={cn('flex gap-3 py-4', isUser && 'flex-row-reverse')}>
      <Avatar
        fallback={isUser ? 'U' : 'AI'}
        className={cn(
          'h-8 w-8',
          isUser ? 'bg-blue-500 text-white' : 'bg-purple-500 text-white'
        )}
      />

      <div
        className={cn(
          'flex-1 max-w-3xl rounded-lg px-4 py-3',
          isUser
            ? 'bg-blue-500 text-white ml-12'
            : 'bg-muted text-foreground mr-12'
        )}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap break-words">{message.content}</p>
        ) : (
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <ReactMarkdown
              components={{
                code(props) {
                  const { node, className, children, ...rest } = props;
                  const match = /language-(\w+)/.exec(className || '');
                  const inline = !match;
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={vscDarkPlus}
                      language={match[1]}
                      PreTag="div"
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...rest}>
                      {children}
                    </code>
                  );
                },
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
        {isStreaming && <span className="inline-block w-2 h-4 ml-1 bg-current animate-pulse" />}
      </div>
    </div>
  );
};

export default MessageBubble;
