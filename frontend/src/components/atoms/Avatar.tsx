// Avatar component

import * as React from 'react';
import { cn } from '@/lib/utils';

interface AvatarProps {
  src?: string;
  alt?: string;
  fallback: string;
  className?: string;
}

const Avatar: React.FC<AvatarProps> = ({ src, alt, fallback, className }) => {
  const [imgError, setImgError] = React.useState(false);

  return (
    <div
      className={cn(
        'relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full bg-muted',
        className
      )}
    >
      {src && !imgError ? (
        <img
          src={src}
          alt={alt || fallback}
          className="aspect-square h-full w-full"
          onError={() => setImgError(true)}
        />
      ) : (
        <div className="flex h-full w-full items-center justify-center bg-muted text-sm font-medium">
          {fallback}
        </div>
      )}
    </div>
  );
};

export default Avatar;
