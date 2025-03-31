'use client';

import React, { useEffect, useState } from 'react';
import { useEngagementPatterns } from '../use_engagement_patterns';
import { User, JourneyStep } from '../types';
import { cn } from '../../lib/utils';

interface JourneyStepProps {
  step: JourneyStep;
  user: User;
  onComplete?: (stepId: string) => void;
}

export function JourneyStepComponent({ step, user, onComplete }: JourneyStepProps) {
  const { enhanceJourneyStep } = useEngagementPatterns();
  const [enhancedStep, setEnhancedStep] = useState<JourneyStep | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const enhanceStep = async () => {
      try {
        setIsLoading(true);
        const result = await enhanceJourneyStep(step, user);
        setEnhancedStep(result.enhancedStep);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to enhance step');
      } finally {
        setIsLoading(false);
      }
    };

    enhanceStep();
  }, [step, user, enhanceJourneyStep]);

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-4 p-4 rounded-lg bg-muted">
        <div className="h-4 bg-background rounded w-3/4" />
        <div className="h-4 bg-background rounded w-1/2" />
        <div className="h-4 bg-background rounded w-2/3" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-destructive/10 text-destructive">
        <p>Error: {error}</p>
      </div>
    );
  }

  if (!enhancedStep) {
    return null;
  }

  return (
    <div className="space-y-4 p-4 rounded-lg border">
      {/* Value Preview */}
      {enhancedStep.valuePreview && (
        <div className="text-sm text-muted-foreground">
          {enhancedStep.valuePreview}
        </div>
      )}

      {/* Main Content */}
      <div className="prose prose-sm">
        {enhancedStep.content}
      </div>

      {/* Emotional Support */}
      {enhancedStep.emotionalSupport && (
        <div className={cn(
          "p-3 rounded-md text-sm",
          {
            'bg-blue-50 text-blue-700': enhancedStep.emotionalSupport.type === 'reassurance',
            'bg-green-50 text-green-700': enhancedStep.emotionalSupport.type === 'encouragement',
            'bg-purple-50 text-purple-700': enhancedStep.emotionalSupport.type === 'guidance'
          }
        )}>
          {enhancedStep.emotionalSupport.message}
        </div>
      )}

      {/* Persona Adaptations */}
      {enhancedStep.personaAdaptation && (
        <div className="space-y-2">
          {enhancedStep.personaAdaptation.adaptations.map((adaptation, index) => (
            <div key={index} className="text-sm text-muted-foreground">
              {adaptation}
            </div>
          ))}
        </div>
      )}

      {/* Value Confirmation */}
      {enhancedStep.valueConfirmation && (
        <div className="text-sm font-medium text-primary">
          {enhancedStep.valueConfirmation}
        </div>
      )}

      {/* Contextual Value */}
      {enhancedStep.contextualValue && (
        <div className="text-sm text-muted-foreground italic">
          {enhancedStep.contextualValue}
        </div>
      )}

      {/* Complete Button */}
      <button
        onClick={() => onComplete?.(enhancedStep.id)}
        className="w-full px-4 py-2 text-sm font-medium text-white bg-primary rounded-md hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary/50"
      >
        Complete Step
      </button>
    </div>
  );
} 