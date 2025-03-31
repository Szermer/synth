import { z } from 'zod';

export const UserSchema = z.object({
  id: z.string(),
  persona: z.string(),
  email: z.string().email(),
  createdAt: z.string(),
  updatedAt: z.string()
});

export const JourneyStepSchema = z.object({
  id: z.string(),
  type: z.enum(['essential', 'extended', 'comprehensive']),
  content: z.string(),
  visibility: z.enum(['visible', 'hidden']),
  emotionalSupport: z.object({
    type: z.enum(['reassurance', 'encouragement', 'guidance']),
    intensity: z.number().min(0).max(1),
    message: z.string()
  }).optional(),
  personaAdaptation: z.object({
    approach: z.enum(['direct', 'indirect', 'supportive']),
    intensity: z.number().min(0).max(1),
    adaptations: z.array(z.string())
  }).optional()
});

export type User = z.infer<typeof UserSchema>;
export type JourneyStep = z.infer<typeof JourneyStepSchema>;

export interface EnhancedStep extends JourneyStep {
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