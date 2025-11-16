// Conversation list item component

'use client';

import * as React from 'react';
import { MessageSquare, Trash2 } from 'lucide-react';
import { cn, formatDate, truncate } from '@/lib/utils';
import type { Conversation } from '@/types';
import Button from '../atoms/Button';

interface ConversationItemProps {
  conversation: Conversation;
  isActive: boolean;
  onClick: () => void;
  onDelete: (e: React.MouseEvent) => void;
}

const ConversationItem: React.FC<ConversationItemProps> = ({
  conversation,
  isActive,
  onClick,
  onDelete,
}) => {
  return (
    <div
      className={cn(
        'group flex items-center gap-3 rounded-lg px-3 py-2 cursor-pointer transition-colors',
        isActive
          ? 'bg-accent text-accent-foreground'
          : 'hover:bg-accent/50'
      )}
      onClick={onClick}
    >
      <MessageSquare className="h-4 w-4 shrink-0 text-muted-foreground" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">{truncate(conversation.title, 30)}</p>
        <p className="text-xs text-muted-foreground">
          {formatDate(conversation.updated_at)}
        </p>
      </div>
      <Button
        variant="ghost"
        size="icon"
        className="opacity-0 group-hover:opacity-100 h-8 w-8 shrink-0"
        onClick={onDelete}
      >
        <Trash2 className="h-4 w-4" />
      </Button>
    </div>
  );
};

export default ConversationItem;
