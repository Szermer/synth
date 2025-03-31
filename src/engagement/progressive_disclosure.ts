import { z } from 'zod';
import { Database } from '@kit/supabase/database';
import { ProgressiveDisclosureSystem } from './pattern_system';

type User = Database['public']['Tables']['users']['Row'];
type JourneyStep = Database['public']['Tables']['journey_steps']['Row'];

// Progressive disclosure schemas
const EngagementDepthSchema = z.object({
  essentialCompletion: z.number(),
  extendedCompletion: z.number(),
  comprehensiveCompletion: z.number(),
  emotionalState: z.string(),
  timeSpent: z.number()
});

const TransitionSignalsSchema = z.object({
  toExtended: z.boolean(),
  toComprehensive: z.boolean(),
  confidence: z.number(),
  triggers: z.array(z.string())
});

// Progressive disclosure implementation
export class ProgressiveDisclosureImpl extends ProgressiveDisclosureSystem {
  protected async calculateEngagementDepth(user: User): Promise<number> {
    // Calculate engagement depth based on completion rates and emotional state
    const depth = EngagementDepthSchema.parse({
      essentialCompletion: 0.8, // Default value, should be calculated from user data
      extendedCompletion: 0.6, // Default value, should be calculated from user data
      comprehensiveCompletion: 0.4, // Default value, should be calculated from user data
      emotionalState: "engaged", // Default value, should be calculated from user data
      timeSpent: 0 // Default value, should be calculated from user data
    });

    // Weighted calculation of engagement depth
    return (
      depth.essentialCompletion * 0.4 +
      depth.extendedCompletion * 0.3 +
      depth.comprehensiveCompletion * 0.3
    );
  }

  protected async generateTransitionSignals(depth: number, persona: string): Promise<{
    toExtended: boolean;
    toComprehensive: boolean;
  }> {
    const signals = TransitionSignalsSchema.parse({
      toExtended: depth >= 0.6,
      toComprehensive: depth >= 0.8,
      confidence: depth,
      triggers: this.getTransitionTriggers(persona)
    });

    return {
      toExtended: signals.toExtended,
      toComprehensive: signals.toComprehensive
    };
  }

  protected async applyVisibilityRules(content: JourneyStep[], shouldShow: boolean): Promise<JourneyStep[]> {
    if (!shouldShow) {
      return [];
    }

    return content.map(step => ({
      ...step,
      visibility: shouldShow ? "visible" : "hidden"
    }));
  }

  protected async generateTransitionCues(signals: { toExtended: boolean; toComprehensive: boolean }): Promise<string[]> {
    const cues: string[] = [];

    if (signals.toExtended) {
      cues.push("Ready for more detailed information?");
      cues.push("Want to explore this topic further?");
    }

    if (signals.toComprehensive) {
      cues.push("Ready for a deep dive into this topic?");
      cues.push("Want to understand this in detail?");
    }

    return cues;
  }

  private getTransitionTriggers(persona: string): string[] {
    const personaTriggers = {
      health_aware_avoider: [
        "Low anxiety threshold",
        "Clear value proposition",
        "Gradual progression"
      ],
      structured_system_seeker: [
        "Systematic approach",
        "Clear methodology",
        "Comprehensive framework"
      ],
      balanced_life_integrator: [
        "Life context",
        "Practical application",
        "Holistic view"
      ],
      healthcare_professional: [
        "Clinical relevance",
        "Evidence-based approach",
        "Professional context"
      ],
      overlooked_risk_group: [
        "Accessible format",
        "Supportive context",
        "Clear guidance"
      ]
    };

    return personaTriggers[persona] || [];
  }
}

// Progressive disclosure hooks
export function useProgressiveDisclosure() {
  const progressiveDisclosureImpl = ProgressiveDisclosureImpl.getInstance();

  const enhanceContentVisibility = async (content: JourneyStep[], user: User) => {
    const progressiveDisclosure = await progressiveDisclosureImpl.refineProgressiveDisclosure(user, content);
    
    return {
      essentialContent: progressiveDisclosure.essentialContent,
      extendedContent: progressiveDisclosure.extendedContent,
      comprehensiveContent: progressiveDisclosure.comprehensiveContent,
      transitionCues: progressiveDisclosure.transitionCues
    };
  };

  return {
    enhanceContentVisibility
  };
} 