import { useEffect } from 'react';
import { JourneyStep, User } from '../types';

interface Progress {
  userId: string;
  stepId: string;
  progress: number;
  lastInteraction: string;
  interactions: Array<{
    type: string;
    timestamp: string;
    details: Record<string, unknown>;
  }>;
}

// Simulated storage - replace with actual storage implementation
const storage = {
  save: (key: string, value: unknown) => {
    localStorage.setItem(key, JSON.stringify(value));
  },
  load: (key: string) => {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : null;
  }
};

function calculateProgress(interactions: Progress['interactions']): number {
  // Simple progress calculation based on interaction count
  // Replace with more sophisticated calculation
  return Math.min(interactions.length / 10, 1);
}

export function useProgressPreservation(step: JourneyStep, user: User, interactions: Progress['interactions']) {
  // Save progress when component unmounts
  useEffect(() => {
    return () => {
      const progress: Progress = {
        userId: user.id,
        stepId: step.id,
        progress: calculateProgress(interactions),
        lastInteraction: new Date().toISOString(),
        interactions
      };

      const key = `progress_${user.id}_${step.id}`;
      storage.save(key, progress);
    };
  }, [step.id, user.id, interactions]);

  // Load progress when component mounts
  useEffect(() => {
    const key = `progress_${user.id}_${step.id}`;
    const savedProgress = storage.load(key) as Progress | null;

    if (savedProgress) {
      // Restore progress - implement restoration logic
      console.log('Restoring progress:', savedProgress);
    }
  }, [step.id, user.id]);

  return {
    calculateProgress: () => calculateProgress(interactions)
  };
} 