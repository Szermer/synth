import { z } from 'zod';
import { EmotionalScaffoldingSystem } from './pattern_system';
import { User, JourneyStep } from './types';

// Emotional scaffolding schemas
const EmotionalStateSchema = z.object({
  anxiety: z.number(),
  curiosity: z.number(),
  motivation: z.number(),
  confidence: z.number()
});

const SupportiveContextSchema = z.object({
  type: z.enum(['reassurance', 'encouragement', 'guidance']),
  intensity: z.number(),
  triggers: z.array(z.string())
});

// Emotional scaffolding implementation
export class EmotionalScaffoldingImpl extends EmotionalScaffoldingSystem {
  protected async assessEmotionalState(user: User): Promise<{
    anxiety: number;
    curiosity: number;
    motivation: number;
  }> {
    const state = EmotionalStateSchema.parse({
      anxiety: 0.5, // Default value, should be calculated from user data
      curiosity: 0.7, // Default value, should be calculated from user data
      motivation: 0.6, // Default value, should be calculated from user data
      confidence: 0.5 // Default value, should be calculated from user data
    });

    return {
      anxiety: state.anxiety,
      curiosity: state.curiosity,
      motivation: state.motivation
    };
  }

  protected async generateSupportiveContext(
    emotionalState: { anxiety: number; curiosity: number; motivation: number },
    persona: string
  ): Promise<{
    type: 'reassurance' | 'encouragement' | 'guidance';
    intensity: number;
  }> {
    const context = SupportiveContextSchema.parse({
      type: this.determineSupportType(emotionalState),
      intensity: this.calculateSupportIntensity(emotionalState),
      triggers: this.getSupportTriggers(persona)
    });

    return {
      type: context.type,
      intensity: context.intensity
    };
  }

  protected async applyEmotionalScaffolding(
    content: JourneyStep[],
    context: { type: 'reassurance' | 'encouragement' | 'guidance'; intensity: number }
  ): Promise<JourneyStep[]> {
    return content.map(step => ({
      ...step,
      emotionalSupport: {
        type: context.type,
        intensity: context.intensity,
        message: this.generateSupportMessage(context, step)
      }
    }));
  }

  protected async generateMotivationTriggers(
    emotionalState: { anxiety: number; curiosity: number; motivation: number },
    persona: string
  ): Promise<string[]> {
    const triggers: string[] = [];

    if (emotionalState.motivation < 0.6) {
      triggers.push("You're making great progress!");
      triggers.push("Let's build on what you've learned!");
    }

    if (emotionalState.curiosity > 0.8) {
      triggers.push("Want to explore this further?");
      triggers.push("Here's something interesting to consider...");
    }

    return triggers;
  }

  private determineSupportType(emotionalState: { anxiety: number; curiosity: number; motivation: number }): 'reassurance' | 'encouragement' | 'guidance' {
    if (emotionalState.anxiety > 0.7) {
      return 'reassurance';
    } else if (emotionalState.motivation < 0.5) {
      return 'encouragement';
    } else {
      return 'guidance';
    }
  }

  private calculateSupportIntensity(emotionalState: { anxiety: number; curiosity: number; motivation: number }): number {
    return Math.max(
      emotionalState.anxiety * 0.4,
      (1 - emotionalState.motivation) * 0.3,
      emotionalState.curiosity * 0.3
    );
  }

  private generateSupportMessage(
    context: { type: 'reassurance' | 'encouragement' | 'guidance'; intensity: number },
    step: JourneyStep
  ): string {
    const messages = {
      reassurance: [
        "You're doing great! Take it one step at a time.",
        "Remember, progress is progress, no matter how small.",
        "You have what it takes to succeed."
      ],
      encouragement: [
        "Let's build on your strengths!",
        "You're making meaningful progress.",
        "Keep going - you're on the right track!"
      ],
      guidance: [
        "Here's a helpful tip to consider...",
        "Let's explore this together.",
        "Think about it this way..."
      ]
    };

    const typeMessages = messages[context.type];
    return typeMessages[Math.floor(Math.random() * typeMessages.length)];
  }

  private getSupportTriggers(persona: string): string[] {
    const personaTriggers = {
      health_aware_avoider: [
        "Focus on small, manageable steps",
        "Emphasize progress over perfection",
        "Highlight positive outcomes"
      ],
      structured_system_seeker: [
        "Provide clear frameworks",
        "Show systematic approaches",
        "Demonstrate logical progression"
      ],
      balanced_life_integrator: [
        "Connect to life context",
        "Show practical applications",
        "Emphasize holistic benefits"
      ],
      healthcare_professional: [
        "Reference clinical evidence",
        "Focus on professional impact",
        "Highlight practical applications"
      ],
      overlooked_risk_group: [
        "Use accessible language",
        "Provide clear guidance",
        "Offer supportive context"
      ]
    };

    return personaTriggers[persona] || [];
  }
}

// Emotional scaffolding hooks
export function useEmotionalScaffolding() {
  const emotionalScaffoldingImpl = EmotionalScaffoldingImpl.getInstance();

  const enhanceEmotionalSupport = async (content: JourneyStep[], user: User) => {
    const emotionalScaffolding = await emotionalScaffoldingImpl.enhanceEmotionalScaffolding(user, content);
    
    return {
      supportedContent: emotionalScaffolding.supportedContent,
      motivationTriggers: emotionalScaffolding.motivationTriggers
    };
  };

  return {
    enhanceEmotionalSupport
  };
} 