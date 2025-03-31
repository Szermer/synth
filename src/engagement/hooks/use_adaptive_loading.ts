import { useState, useEffect } from 'react';
import { JourneyStep } from '../types';

interface LoadingState {
  isLoading: boolean;
  loadingPhase: 'initial' | 'critical-content' | 'enhanced-context' | 'personalization' | 'deep-context' | 'complete';
  progress: number;
}

interface LoadingPhase {
  phase: LoadingState['loadingPhase'];
  progress: number;
  time: number;
}

function executeLoadingSequence(phases: LoadingPhase[], setLoadingState: (state: LoadingState) => void) {
  phases.forEach((phase, index) => {
    setTimeout(() => {
      setLoadingState({
        isLoading: index < phases.length - 1,
        loadingPhase: phase.phase,
        progress: phase.progress
      });
    }, phase.time);
  });
}

export function useAdaptiveLoading(step: JourneyStep) {
  const [loadingState, setLoadingState] = useState<LoadingState>({
    isLoading: true,
    loadingPhase: 'initial',
    progress: 0
  });
  
  useEffect(() => {
    // Essential content loads immediately
    if (step.type === 'essential') {
      setLoadingState({
        isLoading: true,
        loadingPhase: 'critical-content',
        progress: 30
      });
      
      // Simulate essential content loading quickly
      setTimeout(() => {
        setLoadingState({
          isLoading: false,
          loadingPhase: 'complete',
          progress: 100
        });
      }, 300);
    } 
    // Extended content gets progressive loading
    else if (step.type === 'extended') {
      // Load sequence for extended content
      const loadSequence: LoadingPhase[] = [
        { phase: 'critical-content' as const, progress: 30, time: 300 },
        { phase: 'enhanced-context' as const, progress: 60, time: 600 },
        { phase: 'complete' as const, progress: 100, time: 900 }
      ];
      
      // Execute the loading sequence
      executeLoadingSequence(loadSequence, setLoadingState);
    }
    // Comprehensive content gets the most detailed loading
    else if (step.type === 'comprehensive') {
      // Load sequence for comprehensive content
      const loadSequence: LoadingPhase[] = [
        { phase: 'critical-content' as const, progress: 20, time: 300 },
        { phase: 'enhanced-context' as const, progress: 40, time: 600 },
        { phase: 'personalization' as const, progress: 60, time: 900 },
        { phase: 'deep-context' as const, progress: 80, time: 1200 },
        { phase: 'complete' as const, progress: 100, time: 1500 }
      ];
      
      // Execute the loading sequence
      executeLoadingSequence(loadSequence, setLoadingState);
    }
  }, [step.type]);
  
  return loadingState;
} 