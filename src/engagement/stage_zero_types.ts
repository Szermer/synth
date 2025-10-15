import { z } from 'zod';

// Updated schemas for Stage Zero Health narrative approach
export const StageZeroUserSchema = z.object({
  id: z.string(),
  persona: z.enum([
    'healthcare_professional_consumer_bridge',
    'structured_system_seeker', 
    'health_aware_avoider',
    'balanced_life_integrator',
    'overlooked_risk_group'
  ]),
  email: z.string().email(),
  currentWeek: z.number().min(1).max(10),
  conversationProgress: z.object({
    completedWeeks: z.array(z.number()),
    trustLevel: z.number().min(0).max(1),
    engagementScore: z.number().min(0).max(1),
    narrativeRichness: z.number().min(0).max(1)
  }),
  clinicalData: z.object({
    riskFactors: z.array(z.string()),
    familyHistory: z.record(z.any()).optional(),
    personalHealth: z.record(z.any()).optional(),
    lifestyleFactors: z.record(z.any()).optional()
  }),
  createdAt: z.string(),
  updatedAt: z.string()
});

export const WeeklyConversationSchema = z.object({
  week: z.number().min(1).max(10),
  theme: z.string(),
  clinicalObjectives: z.array(z.string()),
  emotionalObjectives: z.array(z.string()),
  conversationElements: z.array(z.object({
    id: z.string(),
    type: z.enum(['narrative_question', 'clinical_capture', 'emotional_support', 'progress_reflection']),
    content: z.string(),
    responsePattern: z.object({
      expected_length: z.enum(['brief', 'moderate', 'detailed']),
      emotional_tone: z.string(),
      clinical_relevance: z.number().min(0).max(1)
    }),
    personaAdaptation: z.object({
      approach: z.enum(['direct', 'gradual', 'supportive', 'analytical', 'reflective']),
      languageStyle: z.enum(['clinical', 'conversational', 'empathetic', 'educational']),
      supportLevel: z.enum(['minimal', 'moderate', 'high'])
    })
  })),
  completionCriteria: z.object({
    narrativeDepth: z.number().min(0).max(1),
    clinicalCompleteness: z.number().min(0).max(1),
    emotionalReadiness: z.number().min(0).max(1),
    trustIndicators: z.array(z.string())
  })
});

export const NarrativeResponseSchema = z.object({
  elementId: z.string(),
  userResponse: z.string(),
  extractedData: z.object({
    clinicalFactors: z.record(z.any()),
    emotionalIndicators: z.array(z.string()),
    narrativeThemes: z.array(z.string()),
    trustSignals: z.array(z.string())
  }),
  responseMetrics: z.object({
    length: z.number(),
    emotionalDepth: z.number().min(0).max(1),
    clinicalRelevance: z.number().min(0).max(1),
    confidenceLevel: z.number().min(0).max(1)
  }),
  followUpNeeded: z.boolean(),
  adaptationTriggers: z.array(z.string())
});

export const JourneyProgressSchema = z.object({
  currentWeek: z.number().min(1).max(10),
  completionStatus: z.object({
    weeklyCompletion: z.record(z.boolean()),
    overallProgress: z.number().min(0).max(1),
    clinicalDataCompleteness: z.number().min(0).max(1),
    narrativeRichness: z.number().min(0).max(1)
  }),
  trustEvolution: z.object({
    currentLevel: z.number().min(0).max(1),
    weeklyProgression: z.array(z.number()),
    trustMilestones: z.array(z.string())
  }),
  engagementPatterns: z.object({
    sessionDuration: z.array(z.number()),
    responseDepth: z.array(z.number()),
    emotionalEngagement: z.array(z.number()),
    questionPatterns: z.array(z.string())
  }),
  riskProfile: z.object({
    traditionalModels: z.object({
      gail: z.number().optional(),
      tyrerCuzick: z.number().optional(),
      boadicea: z.number().optional()
    }),
    narrativeContext: z.object({
      familyStory: z.string(),
      personalJourney: z.string(),
      lifeContext: z.string(),
      values: z.array(z.string())
    }),
    integratedAssessment: z.object({
      riskLevel: z.enum(['low', 'moderate', 'elevated', 'high']),
      confidence: z.number().min(0).max(1),
      keyFactors: z.array(z.string()),
      narrativeInfluence: z.string()
    })
  })
});

// Type exports
export type StageZeroUser = z.infer<typeof StageZeroUserSchema>;
export type WeeklyConversation = z.infer<typeof WeeklyConversationSchema>;
export type NarrativeResponse = z.infer<typeof NarrativeResponseSchema>;
export type JourneyProgress = z.infer<typeof JourneyProgressSchema>;

// Enhanced conversation element types
export interface ConversationElement {
  id: string;
  week: number;
  type: 'narrative_question' | 'clinical_capture' | 'emotional_support' | 'progress_reflection';
  content: string;
  personaAdaptations: {
    [key: string]: {
      approach: string;
      content: string;
      supportLevel: string;
    };
  };
  expectedResponse: {
    clinicalData: string[];
    narrativeElements: string[];
    emotionalIndicators: string[];
  };
  followUpLogic: {
    triggers: string[];
    adaptations: string[];
  };
}

// Weekly theme definitions
export interface WeeklyTheme {
  week: number;
  title: string;
  description: string;
  clinicalObjectives: string[];
  emotionalObjectives: string[];
  narrativeGoals: string[];
  riskModelInputs: string[];
  trustBuildingElements: string[];
  personaAdaptations: {
    [persona: string]: {
      approach: string;
      emphasisAreas: string[];
      supportNeeds: string[];
    };
  };
}

// Trust building indicators
export interface TrustIndicators {
  currentLevel: number;
  indicators: {
    vulnerability_sharing: number;
    question_asking: number;
    detail_providing: number;
    emotional_openness: number;
    future_planning: number;
  };
  milestones: {
    week: number;
    achievement: string;
    significance: string;
  }[];
  progression: number[];
}

// Clinical data integration
export interface ClinicalDataIntegration {
  traditionalModels: {
    gail: {
      inputs: Record<string, any>;
      score: number;
      interpretation: string;
    };
    tyrerCuzick: {
      inputs: Record<string, any>;
      score: number;
      interpretation: string;
    };
    boadicea: {
      inputs: Record<string, any>;
      score: number;
      interpretation: string;
    };
  };
  narrativeEnhancement: {
    contextualFactors: string[];
    lifeCircumstances: string[];
    values: string[];
    preferences: string[];
  };
  integratedAssessment: {
    finalRisk: string;
    confidence: number;
    personalizedFactors: string[];
    detectionPlan: {
      timeline: string;
      approaches: string[];
      support: string[];
    };
  };
}

// Persona-specific patterns
export const PersonaPatterns = {
  healthcare_professional_consumer_bridge: {
    responseStyle: 'analytical_personal',
    engagementLevel: 'high',
    trustBuildingSpeed: 'moderate',
    clinicalDetail: 'comprehensive',
    narrativeSharing: 'structured',
    questionPattern: 'evidence_seeking'
  },
  structured_system_seeker: {
    responseStyle: 'organized_systematic',
    engagementLevel: 'high',
    trustBuildingSpeed: 'steady',
    clinicalDetail: 'thorough',
    narrativeSharing: 'timeline_focused',
    questionPattern: 'planning_oriented'
  },
  health_aware_avoider: {
    responseStyle: 'cautious_gradual',
    engagementLevel: 'variable',
    trustBuildingSpeed: 'slow',
    clinicalDetail: 'selective',
    narrativeSharing: 'hesitant_growing',
    questionPattern: 'support_seeking'
  },
  balanced_life_integrator: {
    responseStyle: 'reflective_holistic',
    engagementLevel: 'steady',
    trustBuildingSpeed: 'moderate',
    clinicalDetail: 'contextual',
    narrativeSharing: 'wisdom_focused',
    questionPattern: 'value_alignment'
  },
  overlooked_risk_group: {
    responseStyle: 'learning_engaged',
    engagementLevel: 'growing',
    trustBuildingSpeed: 'accelerating',
    clinicalDetail: 'educational',
    narrativeSharing: 'discovery_focused',
    questionPattern: 'validation_seeking'
  }
} as const;

export type PersonaType = keyof typeof PersonaPatterns;
