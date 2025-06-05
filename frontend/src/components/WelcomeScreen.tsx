import React from 'react';
import { cn } from '../lib/utils';

interface WelcomeScreenProps {
  onNext: () => void;
  className?: string;
}

export function WelcomeScreen({ onNext, className }: WelcomeScreenProps) {
  return (
    <div className={cn("flex-1 flex flex-col items-center justify-center p-8", className)}>
      <img 
        src="/onboard.png" 
        alt="Onboarding Welcome" 
        className="max-w-full max-h-[60vh] object-contain mb-8"
      />
      <button 
        onClick={onNext}
        className="px-8 py-3 text-lg font-medium rounded-md transition-colors"
        style={{ 
          backgroundColor: 'rgb(89, 54, 41)', 
          color: 'rgb(235, 225, 204)' 
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = 'rgb(69, 42, 32)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = 'rgb(89, 54, 41)';
        }}
      >
        Next
      </button>
    </div>
  );
}