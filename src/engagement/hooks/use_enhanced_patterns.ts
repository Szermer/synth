import { useState, useEffect } from 'react';
import { useEngagementPatterns } from '../use_engagement_patterns';
import { User, JourneyStep } from '../types';

interface PatternMetrics {
  valueArticulation: number;
  emotionalScaffolding: number;
  progressiveDisclosure: number;
  personaAlignment: number;
}

interface EnhancedStep extends JourneyStep {
  valueComponents?: {
    preview?: string;
    confirmation?: string;
    contextual?: string;
  };
  emotionalComponents?: {
    type: 'reassurance' | 'encouragement' | 'guidance';
    intensity: number;
    message: string;
  };
  disclosureComponents?: {
    visibilityRules: {
      isVisible: boolean;
    };
  };
  personaComponents?: {
    approach: 'direct' | 'indirect' | 'supportive';
    intensity: number;
    adaptations: string[];
  };
}

function createFallbackValueComponents(step: JourneyStep) {
  return {
    preview: `Learn about ${step.content}`,
    confirmation: 'Great job completing this step!',
    contextual: 'This knowledge will help you in your journey.'
  };
}

function createFallbackEmotionalComponents() {
  return {
    type: 'encouragement' as const,
    intensity: 0.5,
    message: "You're doing great! Keep going!"
  };
}

function createFallbackPersonaComponents() {
  return {
    approach: 'supportive' as const,
    intensity: 0.5,
    adaptations: ['Take your time to understand this information.']
  };
}

export function useEnhancedPatterns(step: JourneyStep, user: User) {
  const [enhancedStep, setEnhancedStep] = useState<EnhancedStep | null>(null);
  const [patternMetrics, setPatternMetrics] = useState<PatternMetrics>({
    valueArticulation: 0,
    emotionalScaffolding: 0,
    progressiveDisclosure: 0,
    personaAlignment: 0
  });
  
  const { enhanceJourneyStep } = useEngagementPatterns();
  
  useEffect(() => {
    const applyPatterns = async () => {
      try {
        // Apply all patterns in parallel
        const result = await enhanceJourneyStep(step, user);
        
        // Extract enhanced step components
        const enhancedStepData: EnhancedStep = {
          ...step,
          valueComponents: {
            preview: result.enhancedStep.valuePreview,
            confirmation: result.enhancedStep.valueConfirmation,
            contextual: result.enhancedStep.contextualValue
          },
          emotionalComponents: result.enhancedStep.emotionalSupport,
          disclosureComponents: {
            visibilityRules: {
              isVisible: result.enhancedStep.visibility === 'visible'
            }
          },
          personaComponents: result.enhancedStep.personaAdaptation
        };
        
        // Calculate pattern metrics (simplified for example)
        const metrics: PatternMetrics = {
          valueArticulation: result.enhancedStep.valuePreview ? 0.8 : 0.5,
          emotionalScaffolding: result.enhancedStep.emotionalSupport ? 0.7 : 0.4,
          progressiveDisclosure: result.enhancedStep.visibility === 'visible' ? 0.9 : 0.3,
          personaAlignment: result.enhancedStep.personaAdaptation ? 0.8 : 0.5
        };
        
        setEnhancedStep(enhancedStepData);
        setPatternMetrics(metrics);
      } catch (error) {
        console.error('Error applying patterns:', error);
        // Fall back to original step with basic enhancements
        setEnhancedStep({
          ...step,
          valueComponents: createFallbackValueComponents(step),
          emotionalComponents: createFallbackEmotionalComponents(),
          disclosureComponents: { visibilityRules: { isVisible: true } },
          personaComponents: createFallbackPersonaComponents()
        });
        
        // Set fallback metrics
        setPatternMetrics({
          valueArticulation: 0.5,
          emotionalScaffolding: 0.4,
          progressiveDisclosure: 0.3,
          personaAlignment: 0.5
        });
      }
    };
    
    applyPatterns();
  }, [step, user, enhanceJourneyStep]);
  
  return { enhancedStep, patternMetrics };
} 