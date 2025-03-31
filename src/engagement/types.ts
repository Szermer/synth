export type User = {
  id: string;
  persona: string;
  email: string;
  created_at: string;
  updated_at: string;
};

export type JourneyStep = {
  id: string;
  type: 'essential' | 'extended' | 'comprehensive';
  content: string;
  visibility: 'visible' | 'hidden';
  emotionalSupport?: {
    type: 'reassurance' | 'encouragement' | 'guidance';
    intensity: number;
    message: string;
  };
  valuePreview?: string;
  valueConfirmation?: string;
  contextualValue?: string;
  personaAdaptation?: {
    approach: 'direct' | 'indirect' | 'supportive';
    intensity: number;
    adaptations: string[];
  };
  created_at: string;
  updated_at: string;
}; 