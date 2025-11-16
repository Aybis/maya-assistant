// Model selector dropdown component

'use client';

import * as React from 'react';
import { Check, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { AIModel } from '@/types';

interface ModelSelectorProps {
  models: AIModel[];
  selectedModel: string;
  onSelectModel: (modelId: string) => void;
  disabled?: boolean;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({
  models,
  selectedModel,
  onSelectModel,
  disabled = false,
}) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const ref = React.useRef<HTMLDivElement>(null);

  const selected = models.find((m) => m.id === selectedModel);

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={ref}>
      <button
        className={cn(
          'flex items-center justify-between gap-2 rounded-md border border-input bg-background px-3 py-2 text-sm w-full min-w-[200px]',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
      >
        <span className="truncate">{selected?.name || 'Select model'}</span>
        <ChevronDown className="h-4 w-4 shrink-0" />
      </button>

      {isOpen && (
        <div className="absolute z-50 mt-2 w-full rounded-md border bg-popover p-1 shadow-md">
          {models.map((model) => (
            <button
              key={model.id}
              className="flex w-full items-center gap-2 rounded-sm px-2 py-1.5 text-sm hover:bg-accent"
              onClick={() => {
                onSelectModel(model.id);
                setIsOpen(false);
              }}
            >
              <Check
                className={cn(
                  'h-4 w-4',
                  selectedModel === model.id ? 'opacity-100' : 'opacity-0'
                )}
              />
              <div className="flex-1 text-left">
                <p className="font-medium">{model.name}</p>
                <p className="text-xs text-muted-foreground">
                  {model.description}
                </p>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default ModelSelector;
