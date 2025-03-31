'use client';

import React, { useEffect, useState } from 'react';
import { useEngagementPatterns } from '../use_engagement_patterns';
import { useAdaptiveLoading } from '../hooks/use_adaptive_loading';
import { useEnhancedPatterns } from '../hooks/use_enhanced_patterns';
import { usePatternMeasurement } from '../hooks/use_pattern_measurement';
import { useDynamicContentLoading } from '../hooks/use_dynamic_content_loading';
import { useInteractionAdaptation } from '../hooks/use_interaction_adaptation';
import { useProgressPreservation } from '../hooks/use_progress_preservation';
import { User, JourneyStep } from '../types';
import { cn } from '../../lib/utils';

interface JourneyStepProps {
  step: JourneyStep;
  user: User;
  onComplete?: (stepId: string, metrics?: Record<string, unknown>) => void;
}

export function JourneyStepComponent({ step, user, onComplete }: JourneyStepProps) {
  // Initialize measurement framework
  const { 
    startMeasurement, 
    recordInteraction,
    completeMeasurement,
    measurements
  } = usePatternMeasurement(step, user);

  // Using enhanced loading strategy
  const loadingState = useAdaptiveLoading(step);
  
  // Using enhanced pattern application
  const { enhancedStep, patternMetrics } = useEnhancedPatterns(step, user);

  // Dynamic content loading
  const contentState = useDynamicContentLoading(step, user);

  // Interaction-based adaptation
  const adaptedStep = useInteractionAdaptation(measurements, enhancedStep || step);

  // Progress preservation
  const { calculateProgress } = useProgressPreservation(step, user, measurements.interactions);

  // Start measurement when component mounts
  useEffect(() => {
    startMeasurement();
  }, [startMeasurement]);

  // Handle completion with metrics
  const handleComplete = () => {
    // Record completion in measurement framework
    completeMeasurement({ 
      outcome: 'completed',
      metrics: {
        patternMetrics,
        sessionDuration: Date.now() - new Date(measurements.startTime).getTime(),
        progress: calculateProgress()
      }
    });
    
    // Call original handler with metrics
    if (onComplete) {
      onComplete(step.id, {
        patternMetrics,
        sessionDuration: Date.now() - new Date(measurements.startTime).getTime(),
        progress: calculateProgress()
      });
    }
  };

  // Show loading state with progress
  if (loadingState.isLoading || contentState.isLoading) {
    return (
      <div className="space-y-4 p-4 rounded-lg bg-muted">
        <div className="h-2 bg-background rounded-full overflow-hidden">
          <div 
            className="h-full bg-primary transition-all duration-300"
            style={{ width: `${loadingState.progress}%` }}
          />
        </div>
        <div className="text-sm text-muted-foreground">
          {loadingState.loadingPhase === 'initial' && 'Initializing...'}
          {loadingState.loadingPhase === 'critical-content' && 'Loading essential content...'}
          {loadingState.loadingPhase === 'enhanced-context' && 'Adding context...'}
          {loadingState.loadingPhase === 'personalization' && 'Personalizing content...'}
          {loadingState.loadingPhase === 'deep-context' && 'Adding detailed information...'}
          {loadingState.loadingPhase === 'complete' && 'Ready!'}
        </div>
      </div>
    );
  }

  // Show error state if no enhanced step or content loading error
  if (!enhancedStep || contentState.error) {
    return (
      <div className="p-4 rounded-lg bg-destructive/10 text-destructive">
        <p>Error: {contentState.error || 'Unable to load this step. Please try again.'}</p>
      </div>
    );
  }

  // Determine if step should be visible based on progressive disclosure
  if (!adaptedStep.disclosureComponents?.visibilityRules.isVisible) {
    return null;
  }

  // Get the appropriate content based on step type
  const content = step.type === 'comprehensive' && contentState.comprehensive
    ? contentState.comprehensive
    : step.type === 'extended' && contentState.extended
    ? contentState.extended
    : contentState.essential;

  return (
    <div 
      className={cn(
        "space-y-4 p-4 rounded-lg border",
        {
          'bg-white': step.type === 'essential',
          'bg-blue-50': step.type === 'extended',
          'bg-indigo-50': step.type === 'comprehensive'
        }
      )}
      onMouseMove={() => recordInteraction({ 
        type: 'activity', 
        details: { type: 'mouse' } 
      })}
    >
      {/* Step header with tier indicator */}
      <div className="flex items-center justify-between">
        <div className="text-sm font-medium text-muted-foreground">
          {step.type === 'essential' && 'Essential Information'}
          {step.type === 'extended' && 'Extended Learning'}
          {step.type === 'comprehensive' && 'Comprehensive Guide'}
        </div>
      </div>

      {/* Value Preview */}
      {adaptedStep.valueComponents?.preview && (
        <div className="text-sm text-muted-foreground">
          {adaptedStep.valueComponents.preview}
        </div>
      )}

      {/* Main Content */}
      <div className="prose prose-sm">
        {content}
      </div>

      {/* Emotional Support */}
      {adaptedStep.emotionalComponents && (
        <div className={cn(
          "p-3 rounded-md text-sm",
          {
            'bg-blue-50 text-blue-700': adaptedStep.emotionalComponents.type === 'reassurance',
            'bg-green-50 text-green-700': adaptedStep.emotionalComponents.type === 'encouragement',
            'bg-purple-50 text-purple-700': adaptedStep.emotionalComponents.type === 'guidance'
          }
        )}>
          {adaptedStep.emotionalComponents.message}
        </div>
      )}

      {/* Persona Adaptations */}
      {adaptedStep.personaComponents && (
        <div className="space-y-2">
          {adaptedStep.personaComponents.adaptations.map((adaptation, index) => (
            <div key={index} className="text-sm text-muted-foreground">
              {adaptation}
            </div>
          ))}
        </div>
      )}

      {/* Value Confirmation */}
      {adaptedStep.valueComponents?.confirmation && (
        <div className="text-sm font-medium text-primary">
          {adaptedStep.valueComponents.confirmation}
        </div>
      )}

      {/* Contextual Value */}
      {adaptedStep.valueComponents?.contextual && (
        <div className="text-sm text-muted-foreground italic">
          {adaptedStep.valueComponents.contextual}
        </div>
      )}

      {/* Complete Button */}
      <button
        onClick={handleComplete}
        className={cn(
          "w-full px-4 py-2 text-sm font-medium text-white rounded-md transition-all duration-300 focus:outline-none focus:ring-2",
          {
            'bg-primary hover:bg-primary/90 focus:ring-primary/50': step.type === 'essential',
            'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500': step.type === 'extended',
            'bg-indigo-700 hover:bg-indigo-800 focus:ring-indigo-500': step.type === 'comprehensive'
          }
        )}
      >
        {step.type === 'essential' && 'Complete This Step'}
        {step.type === 'extended' && 'Complete & Continue'}
        {step.type === 'comprehensive' && 'Complete & Apply'}
      </button>

      {/* Pattern Visualization (development only) */}
      {process.env.NODE_ENV === 'development' && (
        <div className="mt-4 space-y-4">
          {/* Pattern Metrics */}
          <div className="p-4 bg-muted rounded-lg text-xs">
            <h3 className="font-medium mb-2">Pattern Metrics</h3>
            <div className="space-y-1">
              <div>Value Articulation: {patternMetrics.valueArticulation.toFixed(2)}</div>
              <div>Emotional Scaffolding: {patternMetrics.emotionalScaffolding.toFixed(2)}</div>
              <div>Progressive Disclosure: {patternMetrics.progressiveDisclosure.toFixed(2)}</div>
              <div>Persona Alignment: {patternMetrics.personaAlignment.toFixed(2)}</div>
            </div>
          </div>

          {/* Pattern Visualization */}
          <div className="p-4 bg-muted rounded-lg text-xs">
            <h3 className="font-medium mb-2">Pattern Visualization</h3>
            <div className="space-y-2">
              {Object.entries(adaptedStep).map(([key, value]) => {
                if (key.includes('Components') && value) {
                  return (
                    <div key={key} className="flex items-center space-x-2">
                      <div className="w-2 h-2 rounded-full bg-primary" />
                      <span className="text-muted-foreground">{key}</span>
                    </div>
                  );
                }
                return null;
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 