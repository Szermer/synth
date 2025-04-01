import React, { useState } from 'react';
import { JourneyStepComponent } from './src/engagement/components/journey_step';
import { User, JourneyStep } from './src/engagement/types';

// Define persona types for the dropdown
const personaTypes = [
  'health_aware_avoider',
  'structured_system_seeker',
  'balanced_life_integrator',
  'healthcare_professional',
  'overlooked_risk_group'
];

// Define step types for the dropdown
const stepTypes = [
  'essential',
  'extended',
  'comprehensive'
];

export default function EngagementPatternExample() {
  // User state with default values
  const [user, setUser] = useState<User>({
    id: "user123",
    persona: "health_aware_avoider",
    email: "user@example.com",
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  });

  // Step state with default values
  const [step, setStep] = useState<JourneyStep>({
    id: "risk-assessment-intro",
    type: "essential",
    content: "Understanding your health risks is an important first step toward prevention. This assessment will help identify potential areas of concern based on your age, family history, and lifestyle.",
    visibility: "visible"
  });

  // Completion state
  const [completionData, setCompletionData] = useState<any>(null);

  // Handle persona change
  const handlePersonaChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setUser({
      ...user,
      persona: e.target.value
    });
  };

  // Handle step type change
  const handleStepTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setStep({
      ...step,
      type: e.target.value as "essential" | "extended" | "comprehensive"
    });
  };

  // Handle step content change
  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setStep({
      ...step,
      content: e.target.value
    });
  };

  // Handle step completion
  const handleStepComplete = (stepId: string, metrics?: Record<string, unknown>) => {
    setCompletionData({
      stepId,
      completedAt: new Date().toISOString(),
      metrics
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold">Engagement Pattern Demo</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-6">
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Configuration</h2>
            
            <div>
              <label className="block text-sm font-medium mb-1">User Persona</label>
              <select 
                value={user.persona}
                onChange={handlePersonaChange}
                className="w-full p-2 border rounded"
              >
                {personaTypes.map(persona => (
                  <option key={persona} value={persona}>
                    {persona.replace(/_/g, ' ')}
                  </option>
                ))}
              </select>
              <p className="mt-1 text-sm text-gray-500">
                Changes how content is adapted for the user
              </p>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-1">Step Type</label>
              <select 
                value={step.type}
                onChange={handleStepTypeChange}
                className="w-full p-2 border rounded"
              >
                {stepTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
              <p className="mt-1 text-sm text-gray-500">
                Controls content depth and presentation style
              </p>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-1">Step Content</label>
              <textarea 
                value={step.content}
                onChange={handleContentChange}
                rows={4}
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
          
          {completionData && (
            <div className="p-4 bg-green-50 border border-green-200 rounded">
              <h3 className="font-medium text-green-800 mb-2">Step Completed!</h3>
              <pre className="text-xs overflow-auto p-2 bg-white rounded">
                {JSON.stringify(completionData, null, 2)}
              </pre>
            </div>
          )}
        </div>
        
        <div className="border rounded p-4 bg-gray-50">
          <h2 className="text-xl font-semibold mb-4">Rendered Journey Step</h2>
          <JourneyStepComponent 
            step={step}
            user={user}
            onComplete={handleStepComplete}
          />
        </div>
      </div>
    </div>
  );
}