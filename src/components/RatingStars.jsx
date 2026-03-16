import { useState } from 'react';

const STAR_COUNT = 5;

export default function RatingStars({ value = 0, onChange, size = 'md', readOnly = false }) {
  const [hover, setHover] = useState(null);
  const displayValue = hover ?? value;

  const sizeClasses = size === 'sm' ? 'w-4 h-4' : size === 'lg' ? 'w-7 h-7' : 'w-5 h-5';

  const handleClick = (index) => {
    if (readOnly || !onChange) return;
    onChange(index);
  };

  return (
    <div className="flex items-center gap-0.5">
      {Array.from({ length: STAR_COUNT }).map((_, i) => {
        const index = i + 1;
        const filled = index <= displayValue;
        return (
          <button
            key={index}
            type="button"
            disabled={readOnly}
            onClick={() => handleClick(index)}
            onMouseEnter={() => !readOnly && setHover(index)}
            onMouseLeave={() => !readOnly && setHover(null)}
            className={`transition ${
              readOnly ? 'cursor-default' : 'cursor-pointer hover:scale-110'
            }`}
          >
            <svg
              className={`${sizeClasses} ${
                filled ? 'text-accent' : 'text-zinc-700'
              } drop-shadow-[0_0_4px_rgba(0,0,0,0.8)]`}
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81H7.03a1 1 0 00.95-.69l1.07-3.292z" />
            </svg>
          </button>
        );
      })}
    </div>
  );
}

