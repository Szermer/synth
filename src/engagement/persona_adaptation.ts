import { z } from 'zod';
import { PersonaAdaptationSystem } from './pattern_system';
import { User, JourneyStep } from './types';

// Persona adaptation schemas
const PersonaProfileSchema = z.object({
  traits: z.array(z.string()),
  preferences: z.array(z.string()),
  needs: z.array(z.string()),
  goals: z.array(z.string())
});

const AdaptationStrategySchema = z.object({
  approach: z.enum(['direct', 'indirect', 'supportive']),
  intensity: z.number(),
  focus: z.array(z.string())
});

// Persona adaptation implementation
export class PersonaAdaptationImpl extends PersonaAdaptationSystem {
  protected async analyzePersonaProfile(user: User): Promise<{
    traits: string[];
    preferences: string[];
    needs: string[];
    goals: string[];
  }> {
    const profile = PersonaProfileSchema.parse({
      traits: this.getPersonaTraits(user.persona),
      preferences: this.getPersonaPreferences(user.persona),
      needs: this.getPersonaNeeds(user.persona),
      goals: this.getPersonaGoals(user.persona)
    });

    return {
      traits: profile.traits,
      preferences: profile.preferences,
      needs: profile.needs,
      goals: profile.goals
    };
  }

  protected async generateAdaptationStrategy(
    profile: { traits: string[]; preferences: string[]; needs: string[]; goals: string[] },
    persona: string
  ): Promise<{
    approach: 'direct' | 'indirect' | 'supportive';
    intensity: number;
  }> {
    const strategy = AdaptationStrategySchema.parse({
      approach: this.determineAdaptationApproach(profile, persona),
      intensity: this.calculateAdaptationIntensity(profile),
      focus: this.getAdaptationFocus(persona)
    });

    return {
      approach: strategy.approach,
      intensity: strategy.intensity
    };
  }

  protected async applyPersonaAdaptation(
    content: JourneyStep[],
    strategy: { approach: 'direct' | 'indirect' | 'supportive'; intensity: number }
  ): Promise<JourneyStep[]> {
    return content.map(step => ({
      ...step,
      personaAdaptation: {
        approach: strategy.approach,
        intensity: strategy.intensity,
        adaptations: this.generateAdaptations(strategy, step)
      }
    }));
  }

  protected async generatePersonaInsights(
    profile: { traits: string[]; preferences: string[]; needs: string[]; goals: string[] },
    persona: string
  ): Promise<string[]> {
    const insights: string[] = [];

    if (profile.needs.includes('guidance')) {
      insights.push("Let's break this down into manageable steps");
    }

    if (profile.preferences.includes('visual')) {
      insights.push("Here's a visual representation to help you understand");
    }

    if (profile.goals.includes('efficiency')) {
      insights.push("Here's a streamlined approach to achieve your goals");
    }

    return insights;
  }

  private determineAdaptationApproach(
    profile: { traits: string[]; preferences: string[]; needs: string[]; goals: string[] },
    persona: string
  ): 'direct' | 'indirect' | 'supportive' {
    if (profile.traits.includes('analytical')) {
      return 'direct';
    } else if (profile.needs.includes('support')) {
      return 'supportive';
    } else {
      return 'indirect';
    }
  }

  private calculateAdaptationIntensity(profile: { traits: string[]; preferences: string[]; needs: string[]; goals: string[] }): number {
    const needsCount = profile.needs.length;
    const preferencesCount = profile.preferences.length;
    return Math.min(1, (needsCount + preferencesCount) / 6);
  }

  private generateAdaptations(
    strategy: { approach: 'direct' | 'indirect' | 'supportive'; intensity: number },
    step: JourneyStep
  ): string[] {
    const adaptations: string[] = [];

    if (strategy.approach === 'direct') {
      adaptations.push("Here's the key information you need");
      adaptations.push("Let's focus on the essential points");
    } else if (strategy.approach === 'supportive') {
      adaptations.push("We'll work through this together");
      adaptations.push("Take your time to process this information");
    } else {
      adaptations.push("Consider this perspective");
      adaptations.push("Here's something to think about");
    }

    return adaptations;
  }

  private getPersonaTraits(persona: string): string[] {
    const personaTraits = {
      health_aware_avoider: ['cautious', 'detail-oriented', 'methodical'],
      structured_system_seeker: ['analytical', 'organized', 'systematic'],
      balanced_life_integrator: ['practical', 'holistic', 'balanced'],
      healthcare_professional: ['professional', 'knowledgeable', 'efficient'],
      overlooked_risk_group: ['pragmatic', 'resourceful', 'adaptive']
    };

    return personaTraits[persona] || [];
  }

  private getPersonaPreferences(persona: string): string[] {
    const personaPreferences = {
      health_aware_avoider: ['visual', 'structured', 'detailed'],
      structured_system_seeker: ['systematic', 'organized', 'comprehensive'],
      balanced_life_integrator: ['practical', 'integrated', 'contextual'],
      healthcare_professional: ['efficient', 'evidence-based', 'practical'],
      overlooked_risk_group: ['accessible', 'practical', 'supportive']
    };

    return personaPreferences[persona] || [];
  }

  private getPersonaNeeds(persona: string): string[] {
    const personaNeeds = {
      health_aware_avoider: ['guidance', 'reassurance', 'structure'],
      structured_system_seeker: ['organization', 'clarity', 'comprehensiveness'],
      balanced_life_integrator: ['integration', 'practicality', 'context'],
      healthcare_professional: ['efficiency', 'evidence', 'practicality'],
      overlooked_risk_group: ['accessibility', 'support', 'guidance']
    };

    return personaNeeds[persona] || [];
  }

  private getPersonaGoals(persona: string): string[] {
    const personaGoals = {
      health_aware_avoider: ['safety', 'understanding', 'control'],
      structured_system_seeker: ['comprehension', 'organization', 'efficiency'],
      balanced_life_integrator: ['integration', 'balance', 'practicality'],
      healthcare_professional: ['efficiency', 'effectiveness', 'impact'],
      overlooked_risk_group: ['accessibility', 'understanding', 'support']
    };

    return personaGoals[persona] || [];
  }

  private getAdaptationFocus(persona: string): string[] {
    const personaFocus = {
      health_aware_avoider: ['safety', 'guidance', 'structure'],
      structured_system_seeker: ['organization', 'clarity', 'comprehensiveness'],
      balanced_life_integrator: ['integration', 'practicality', 'context'],
      healthcare_professional: ['efficiency', 'evidence', 'practicality'],
      overlooked_risk_group: ['accessibility', 'support', 'guidance']
    };

    return personaFocus[persona] || [];
  }
}

// Persona adaptation hooks
export function usePersonaAdaptation() {
  const personaAdaptationImpl = PersonaAdaptationImpl.getInstance();

  const enhancePersonaAdaptation = async (content: JourneyStep[], user: User) => {
    const personaAdaptation = await personaAdaptationImpl.enhancePersonaAdaptation(user, content);
    
    return {
      adaptedContent: personaAdaptation.adaptedContent,
      personaInsights: personaAdaptation.personaInsights
    };
  };

  return {
    enhancePersonaAdaptation
  };
} 