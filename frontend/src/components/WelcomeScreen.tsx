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
    
    try {
      // Fetch and play audio
      const response = await fetch('http://localhost:8000/coach');
      if (response.ok) {
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        
        // Play audio and transition immediately when it starts
        audio.play().then(() => {
          // Audio started playing successfully
          onNext();
          
          // Clean up URL when audio finishes
          audio.onended = () => {
            URL.revokeObjectURL(audioUrl);
          };
        }).catch((error) => {
          console.error('Audio playback failed:', error);
          setIsLoading(false);
          onNext();
        });
      } else {
        console.error('Failed to fetch audio');
        onNext();
      }
    } catch (error) {
      console.error('Error fetching audio:', error);
      onNext();
    }
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
        {isLoading ? 'Playing...' : 'Next'}
      </button>
    </div>
  );
}