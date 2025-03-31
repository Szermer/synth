import { useValueArticulation } from './value_articulation';
import { useProgressiveDisclosure } from './progressive_disclosure';
import { useEmotionalScaffolding } from './emotional_scaffolding';
import { usePersonaAdaptation } from './persona_adaptation';
import { User, JourneyStep } from './types';

export function useEngagementPatterns() {
  const { enhanceStepValue } = useValueArticulation();
  const { enhanceContentVisibility } = useProgressiveDisclosure();
  const { enhanceEmotionalSupport } = useEmotionalScaffolding();
  const { enhancePersonaAdaptation } = usePersonaAdaptation();

  const enhanceJourneyStep = async (step: JourneyStep, user: User) => {
    const [
      valueArticulation,
      progressiveDisclosure,
      emotionalScaffolding,
      personaAdaptation
    ] = await Promise.all([
      enhanceStepValue(step, user),
      enhanceContentVisibility([step], user),
      enhanceEmotionalSupport([step], user),
      enhancePersonaAdaptation([step], user)
    ]);

    return {
      valueArticulation,
      progressiveDisclosure,
      emotionalScaffolding,
      personaAdaptation,
      enhancedStep: {
        ...step,
        valuePreview: valueArticulation.preview,
        valueConfirmation: valueArticulation.confirmation,
        contextualValue: valueArticulation.context,
        emotionalSupport: emotionalScaffolding.supportedContent[0]?.emotionalSupport,
        personaAdaptation: personaAdaptation.adaptedContent[0]?.personaAdaptation
      }
    };
  };

  return {
    enhanceJourneyStep
  };
} 