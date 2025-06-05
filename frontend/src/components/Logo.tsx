import React from 'react';
import { cn } from '../lib/utils';

interface LogoProps {
  className?: string;
}

export function Logo({ className }: LogoProps) {
  return (
    <div className={cn("flex items-center gap-4 py-4", className)}>
      <img 
        src="/logo.png" 
        alt="Logo" 
        className="w-12 h-12 object-contain"
      />
      <h1 className="font-medium text-xl tracking-wider uppercase" style={{ color: 'rgb(89, 54, 41)' }}>
        acme onboarding
      </h1>
    </div>
  );
}