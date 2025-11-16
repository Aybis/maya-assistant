// Message bubble component with enhanced markdown styling

'use client';

import * as React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check } from 'lucide-react';
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
    <div className={cn('flex gap-4 py-6', isUser && 'flex-row-reverse')}>
      <Avatar
        fallback={isUser ? 'U' : 'AI'}
        className={cn(
          'h-8 w-8 flex-shrink-0',
          isUser ? 'bg-blue-600 text-white' : 'bg-gradient-to-br from-purple-500 to-pink-500 text-white'
        )}
      />

      <div
        className={cn(
          'flex-1 max-w-3xl rounded-2xl px-5 py-4 shadow-sm',
          isUser
            ? 'bg-blue-600 text-white ml-12'
            : 'bg-card text-card-foreground border border-border mr-12'
        )}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap break-words leading-relaxed">{message.content}</p>
        ) : (
          <div className="markdown-body">
            <ReactMarkdown
              components={{
                // Code blocks with copy button
                code(props) {
                  const { node, className, children, ...rest } = props;
                  const match = /language-(\w+)/.exec(className || '');
                  const inline = !match;
                  const codeString = String(children).replace(/\n$/, '');

                  return !inline && match ? (
                    <CodeBlock code={codeString} language={match[1]} />
                  ) : (
                    <code className="px-1.5 py-0.5 rounded bg-muted text-sm font-mono border border-border" {...rest}>
                      {children}
                    </code>
                  );
                },
                // Headings
                h1: ({children}) => <h1 className="text-2xl font-bold mt-6 mb-4 text-foreground border-b pb-2">{children}</h1>,
                h2: ({children}) => <h2 className="text-xl font-bold mt-5 mb-3 text-foreground">{children}</h2>,
                h3: ({children}) => <h3 className="text-lg font-semibold mt-4 mb-2 text-foreground">{children}</h3>,
                h4: ({children}) => <h4 className="text-base font-semibold mt-3 mb-2 text-foreground">{children}</h4>,
                // Paragraphs
                p: ({children}) => <p className="mb-4 leading-7 text-foreground/90">{children}</p>,
                // Lists
                ul: ({children}) => <ul className="mb-4 ml-6 list-disc space-y-2 text-foreground/90">{children}</ul>,
                ol: ({children}) => <ol className="mb-4 ml-6 list-decimal space-y-2 text-foreground/90">{children}</ol>,
                li: ({children}) => <li className="leading-relaxed">{children}</li>,
                // Blockquotes
                blockquote: ({children}) => (
                  <blockquote className="border-l-4 border-primary pl-4 py-2 my-4 bg-muted/50 rounded-r italic">
                    {children}
                  </blockquote>
                ),
                // Tables
                table: ({children}) => (
                  <div className="overflow-x-auto my-4">
                    <table className="min-w-full divide-y divide-border border border-border rounded-lg">
                      {children}
                    </table>
                  </div>
                ),
                thead: ({children}) => <thead className="bg-muted">{children}</thead>,
                th: ({children}) => <th className="px-4 py-2 text-left text-sm font-semibold">{children}</th>,
                td: ({children}) => <td className="px-4 py-2 text-sm border-t border-border">{children}</td>,
                // Links
                a: ({href, children}) => (
                  <a href={href} className="text-primary hover:underline font-medium" target="_blank" rel="noopener noreferrer">
                    {children}
                  </a>
                ),
                // Horizontal rule
                hr: () => <hr className="my-6 border-border" />,
                // Strong/Bold
                strong: ({children}) => <strong className="font-bold text-foreground">{children}</strong>,
                // Emphasis/Italic
                em: ({children}) => <em className="italic">{children}</em>,
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
        {isStreaming && (
          <span className="inline-block w-1 h-4 ml-1 bg-current animate-pulse rounded" />
        )}
      </div>
    </div>
  );
};

// Code block component with copy functionality
const CodeBlock: React.FC<{ code: string; language: string }> = ({ code, language }) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group my-4">
      <div className="flex items-center justify-between bg-zinc-800 px-4 py-2 rounded-t-lg border border-zinc-700">
        <span className="text-xs text-zinc-400 font-mono uppercase">{language}</span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-2 py-1 text-xs rounded bg-zinc-700 hover:bg-zinc-600 text-zinc-200 transition-colors"
        >
          {copied ? (
            <>
              <Check className="w-3 h-3" />
              Copied!
            </>
          ) : (
            <>
              <Copy className="w-3 h-3" />
              Copy
            </>
          )}
        </button>
      </div>
      <SyntaxHighlighter
        style={oneDark}
        language={language}
        PreTag="div"
        className="!mt-0 !rounded-t-none !rounded-b-lg border border-t-0 border-zinc-700"
        customStyle={{
          margin: 0,
          borderTopLeftRadius: 0,
          borderTopRightRadius: 0,
        }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
};

export default MessageBubble;
