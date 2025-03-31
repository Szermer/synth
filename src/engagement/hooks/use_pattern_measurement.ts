import { useState, useEffect } from 'react';
import { JourneyStep, User } from '../types';

interface Measurement {
  startTime: string;
  interactions: Interaction[];
  completed: boolean;
  outcome?: 'completed' | 'abandoned';
  metrics?: Record<string, number>;
}

interface Interaction {
  type: string;
  timestamp: string;
  details: Record<string, unknown>;
}

export function usePatternMeasurement(step: JourneyStep, user: User) {
  const [measurements, setMeasurements] = useState<Measurement>({
    startTime: new Date().toISOString(),
    interactions: [],
    completed: false
  });

  const startMeasurement = () => {
    setMeasurements(prev => ({
      ...prev,
      startTime: new Date().toISOString()
    }));
  };

  const recordInteraction = (interaction: Omit<Interaction, 'timestamp'>) => {
    setMeasurements(prev => ({
      ...prev,
      interactions: [
        ...prev.interactions,
        {
          ...interaction,
          timestamp: new Date().toISOString()
        }
      ]
    }));
  };

  const completeMeasurement = (data: { outcome: 'completed' | 'abandoned'; metrics?: Record<string, number> }) => {
    setMeasurements(prev => ({
      ...prev,
      completed: true,
      outcome: data.outcome,
      metrics: data.metrics
    }));
  };

  // Cleanup on unmount if not completed
  useEffect(() => {
    return () => {
      if (!measurements.completed) {
        completeMeasurement({ outcome: 'abandoned' });
      }
    };
  }, []);

  return {
    startMeasurement,
    recordInteraction,
    completeMeasurement,
    measurements
  };
} 