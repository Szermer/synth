import { useState, useEffect } from 'react';
import { JourneyStep, User } from '../types';

interface ContentState {
  essential: string;
  extended: string | null;
  comprehensive: string | null;
  isLoading: boolean;
  error: string | null;
}

export function useDynamicContentLoading(step: JourneyStep, user: User) {
  const [contentState, setContentState] = useState<ContentState>({
    essential: step.content,
    extended: null,
    comprehensive: null,
    isLoading: false,
    error: null
  });

  // Load extended content when needed
  useEffect(() => {
    const loadExtendedContent = async () => {
      if (step.type === 'extended' || step.type === 'comprehensive') {
        try {
          setContentState(prev => ({ ...prev, isLoading: true, error: null }));
          
          // Simulate API call - replace with actual API call
          const response = await new Promise<{ content: string }>((resolve) => {
            setTimeout(() => {
              resolve({
                content: `${step.content}\n\nExtended content for ${step.type}...`
              });
            }, 500);
          });

          setContentState(prev => ({
            ...prev,
            extended: response.content,
            isLoading: false
          }));
        } catch (error) {
          setContentState(prev => ({
            ...prev,
            error: 'Failed to load extended content',
            isLoading: false
          }));
        }
      }
    };

    loadExtendedContent();
  }, [step.type, step.id]);

  // Load comprehensive content when needed
  useEffect(() => {
    const loadComprehensiveContent = async () => {
      if (step.type === 'comprehensive') {
        try {
          setContentState(prev => ({ ...prev, isLoading: true, error: null }));
          
          // Simulate API call - replace with actual API call
          const response = await new Promise<{ content: string }>((resolve) => {
            setTimeout(() => {
              resolve({
                content: `${step.content}\n\nComprehensive content with detailed information...`
              });
            }, 800);
          });

          setContentState(prev => ({
            ...prev,
            comprehensive: response.content,
            isLoading: false
          }));
        } catch (error) {
          setContentState(prev => ({
            ...prev,
            error: 'Failed to load comprehensive content',
            isLoading: false
          }));
        }
      }
    };

    loadComprehensiveContent();
  }, [step.type, step.id]);

  return contentState;
} 