import { z } from 'zod';
import { ValueArticulationSystem } from './pattern_system';
import { User, JourneyStep } from './types';

// Value articulation schemas
const PersonalizedValueSchema = z.object({
  healthInsights: z.array(z.string()),
  actionableSteps: z.array(z.string()),
  valuePreview: z.string(),
  valueConfirmation: z.string(),
  contextualValue: z.string()
});

// Value articulation implementation
export class ValueArticulationImpl extends ValueArticulationSystem {
  protected async identifyPersonalizedValue(user: User): Promise<{
    healthInsights: string[];
    actionableSteps: string[];
  }> {
    const value = PersonalizedValueSchema.parse({
      healthInsights: this.getHealthInsights(user.persona),
      actionableSteps: this.getActionableSteps(user.persona),
      valuePreview: "",
      valueConfirmation: "",
      contextualValue: ""
    });

    return {
      healthInsights: value.healthInsights,
      actionableSteps: value.actionableSteps
    };
  }

  protected async generateValuePreview(personalizedValue: { healthInsights: string[]; actionableSteps: string[] }): Promise<string> {
    return `Here's what you'll learn: ${personalizedValue.healthInsights.join(", ")}`;
  }

  protected async generateValueConfirmation(personalizedValue: { healthInsights: string[]; actionableSteps: string[] }): Promise<string> {
    return `Great job! You've learned: ${personalizedValue.healthInsights.join(", ")}`;
  }

  protected async generateContextualValue(
    personalizedValue: { healthInsights: string[]; actionableSteps: string[] },
    user: User
  ): Promise<string> {
    return `This knowledge will help you: ${personalizedValue.actionableSteps.join(", ")}`;
  }

  private getHealthInsights(persona: string): string[] {
    const insights = {
      health_aware_avoider: [
        "Understanding your health status",
        "Identifying manageable steps",
        "Building confidence in your health journey"
      ],
      structured_system_seeker: [
        "Systematic health assessment",
        "Clear health metrics",
        "Structured improvement plans"
      ],
      balanced_life_integrator: [
        "Holistic health understanding",
        "Life-integrated wellness",
        "Sustainable health practices"
      ],
      healthcare_professional: [
        "Clinical health insights",
        "Evidence-based approaches",
        "Professional health standards"
      ],
      overlooked_risk_group: [
        "Accessible health information",
        "Clear health guidance",
        "Supportive health practices"
      ]
    };

    return insights[persona] || [];
  }

  private getActionableSteps(persona: string): string[] {
    const steps = {
      health_aware_avoider: [
        "Take small, manageable steps",
        "Track your progress",
        "Celebrate your achievements"
      ],
      structured_system_seeker: [
        "Follow systematic approaches",
        "Use clear frameworks",
        "Implement structured plans"
      ],
      balanced_life_integrator: [
        "Integrate health into daily life",
        "Balance different life aspects",
        "Maintain sustainable practices"
      ],
      healthcare_professional: [
        "Apply clinical knowledge",
        "Follow evidence-based practices",
        "Maintain professional standards"
      ],
      overlooked_risk_group: [
        "Access clear guidance",
        "Follow supportive practices",
        "Build health confidence"
      ]
    };

    return steps[persona] || [];
  }
}

// Value articulation hooks
export function useValueArticulation() {
  const valueArticulationImpl = ValueArticulationImpl.getInstance();

  const enhanceStepValue = async (step: JourneyStep, user: User) => {
    const valueArticulation = await valueArticulationImpl.enhanceValueArticulation(step, user);
    
    return {
      preview: valueArticulation.preview,
      confirmation: valueArticulation.confirmation,
      context: valueArticulation.context
    };
  };

  return {
    enhanceStepValue
  };
} 