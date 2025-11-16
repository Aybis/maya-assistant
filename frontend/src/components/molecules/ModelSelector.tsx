// Model selector dropdown component with grouped display

'use client';

import * as React from 'react';
import { Check, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { AIModel, GroupedModels } from '@/types';

interface ModelSelectorProps {
  groupedModels: GroupedModels | null;
  selectedModel: string;
  onSelectModel: (modelId: string) => void;
  disabled?: boolean;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({
  groupedModels,
  selectedModel,
  onSelectModel,
  disabled = false,
}) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const ref = React.useRef<HTMLDivElement>(null);

  // Find selected model from flat list
  const selected = groupedModels?.flat.find((m) => m.id === selectedModel);

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (!groupedModels) {
    return (
      <div className="flex items-center justify-between gap-2 rounded-md border border-input bg-background px-3 py-2 text-sm w-full min-w-[200px]">
        <span className="text-muted-foreground">Loading models...</span>
      </div>
    );
  }

  // Define brand order
  const brandOrder = ['GPT', 'Claude', 'Gemini'];
  const sortedBrands = Object.keys(groupedModels.grouped).sort((a, b) => {
    const indexA = brandOrder.indexOf(a);
    const indexB = brandOrder.indexOf(b);
    if (indexA === -1 && indexB === -1) return a.localeCompare(b);
    if (indexA === -1) return 1;
    if (indexB === -1) return -1;
    return indexA - indexB;
  });

  return (
    <div className="relative" ref={ref}>
      <button
        className={cn(
          'flex items-center justify-between gap-2 rounded-md border border-input bg-background px-3 py-2 text-sm w-full min-w-[250px]',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
      >
        <div className="flex items-center gap-2 truncate">
          {selected ? (
            <>
              <span className="font-semibold text-xs px-2 py-0.5 rounded bg-primary/10 text-primary">
                {selected.brand}
              </span>
              <span className="truncate">{selected.name}</span>
            </>
          ) : (
            <span>Select model</span>
          )}
        </div>
        <ChevronDown className="h-4 w-4 shrink-0" />
      </button>

      {isOpen && (
        <div className="absolute z-50 mt-2 w-full min-w-[350px] max-h-[500px] overflow-y-auto rounded-md border bg-popover shadow-lg">
          {sortedBrands.map((brand) => (
            <div key={brand} className="py-2">
              {/* Brand Header */}
              <div className="px-3 py-1.5 bg-muted/50">
                <h3 className="font-bold text-sm text-primary">{brand}</h3>
              </div>

              {/* Categories */}
              {Object.entries(groupedModels.grouped[brand]).map(([category, models]) => (
                <div key={category} className="px-2 py-1">
                  {/* Category Header */}
                  <div className="px-2 py-1">
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                      {category}
                    </p>
                  </div>

                  {/* Models */}
                  {(models as AIModel[]).map((model) => (
                    <button
                      key={model.id}
                      className="flex w-full items-center gap-2 rounded-sm px-3 py-2 text-sm hover:bg-accent transition-colors"
                      onClick={() => {
                        onSelectModel(model.id);
                        setIsOpen(false);
                      }}
                    >
                      <Check
                        className={cn(
                          'h-4 w-4 shrink-0',
                          selectedModel === model.id ? 'opacity-100 text-primary' : 'opacity-0'
                        )}
                      />
                      <div className="flex-1 text-left min-w-0">
                        <p className="font-medium truncate">{model.name}</p>
                        <p className="text-xs text-muted-foreground truncate">
                          {model.description}
                        </p>
                      </div>
                    </button>
                  ))}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ModelSelector;
