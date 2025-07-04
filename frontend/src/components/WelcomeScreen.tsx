import React, { useState } from 'react';
import { cn } from '../lib/utils';

interface WelcomeScreenProps {
  onNext: () => void;
  className?: string;
}

export function WelcomeScreen({ onNext, className }: WelcomeScreenProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleNext = async () => {
    setIsLoading(true);
    
    // No audio here - just transition to the game
    onNext();
  };

  return (
    <div className={cn("flex-1 flex flex-col items-center justify-center p-8", className)}>
      <img 
        src="/onboard.png" 
        alt="Onboarding Welcome" 
        className="max-w-full max-h-[60vh] object-contain mb-8"
      />
      <button 
        onClick={handleNext}
        disabled={isLoading}
        className="px-8 py-3 text-lg font-medium rounded-md transition-colors disabled:opacity-50"
        style={{ 
          backgroundColor: isLoading ? 'rgb(69, 42, 32)' : 'rgb(89, 54, 41)', 
          color: 'rgb(235, 225, 204)' 
        }}
        onMouseEnter={(e) => {
          if (!isLoading) {
            e.currentTarget.style.backgroundColor = 'rgb(69, 42, 32)';
          }
        }}
        onMouseLeave={(e) => {
          if (!isLoading) {
            e.currentTarget.style.backgroundColor = 'rgb(89, 54, 41)';
          }
        }}
      >
        {isLoading ? 'Loading...' : 'Next'}
      </button>
    </div>
  );
}