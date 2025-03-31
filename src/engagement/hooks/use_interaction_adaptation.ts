import { useState, useEffect } from 'react';
import { EnhancedStep } from '../types';

interface InteractionPattern {
  scanningBehavior: boolean;
  deepEngagement: boolean;
  hesitation: boolean;
}

interface Measurements {
  interactions: Array<{
    type: string;
    timestamp: string;
    details: Record<string, unknown>;
  }>;
}

function analyzeInteractionPatterns(interactions: Measurements['interactions']): InteractionPattern {
  const recentInteractions = interactions.slice(-10); // Look at last 10 interactions
  
  // Calculate time between interactions
  const timeBetweenInteractions = recentInteractions.slice(1).map((interaction, index) => {
    const prevTime = new Date(recentInteractions[index].timestamp).getTime();
    const currentTime = new Date(interaction.timestamp).getTime();
    return currentTime - prevTime;
  });

  // Analyze patterns
  const scanningBehavior = timeBetweenInteractions.some(time => time < 1000); // Less than 1 second between interactions
  const deepEngagement = timeBetweenInteractions.every(time => time > 5000); // More than 5 seconds between interactions
  const hesitation = timeBetweenInteractions.some(time => time > 10000); // More than 10 seconds between interactions

  return {
    scanningBehavior,
    deepEngagement,
    hesitation
  };
}

function simplifyContent(step: EnhancedStep): EnhancedStep {
  return {
    ...step,
    content: step.content.split('\n').slice(0, 3).join('\n'), // Keep only first 3 lines
    valueComponents: step.valueComponents ? {
      ...step.valueComponents,
      preview: step.valueComponents.preview?.split('.')[0] + '.',
      contextual: undefined
    } : undefined
  };
}

function enhanceContent(step: EnhancedStep): EnhancedStep {
  return {
    ...step,
    content: `${step.content}\n\nAdditional insights and detailed information...`,
    valueComponents: step.valueComponents ? {
      ...step.valueComponents,
      contextual: 'Here are some additional insights to deepen your understanding...'
    } : undefined
  };
}

function addGuidance(step: EnhancedStep): EnhancedStep {
  return {
    ...step,
    emotionalComponents: {
      type: 'guidance',
      intensity: 0.8,
      message: 'Take your time to understand this information. We\'re here to help guide you through it.'
    }
  };
}

export function useInteractionAdaptation(measurements: Measurements, enhancedStep: EnhancedStep) {
  const [adaptedStep, setAdaptedStep] = useState(enhancedStep);

  useEffect(() => {
    const patterns = analyzeInteractionPatterns(measurements.interactions);
    
    if (patterns.scanningBehavior) {
      setAdaptedStep(simplifyContent(enhancedStep));
    } else if (patterns.deepEngagement) {
      setAdaptedStep(enhanceContent(enhancedStep));
    } else if (patterns.hesitation) {
      setAdaptedStep(addGuidance(enhancedStep));
    }
  }, [measurements.interactions, enhancedStep]);

  return adaptedStep;
} 