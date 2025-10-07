/**
 * Persona Test Fixtures
 *
 * Loads synthetic users from the 500-user cohort and provides
 * them as test fixtures for Playwright tests
 */

import { test as base } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import { PersonaAttributes } from '../page-objects/base.page';

// Load synthetic user cohorts
const COHORT_PATH = path.join(__dirname, '../../../output/private_language_synthetic_users.json');
const BETA_COHORT_PATH = path.join(__dirname, '../../../output/beta_test_cohort.json');

let fullCohort: any[] = [];
let betaCohort: any[] = [];

try {
  fullCohort = JSON.parse(fs.readFileSync(COHORT_PATH, 'utf-8'));
  betaCohort = JSON.parse(fs.readFileSync(BETA_COHORT_PATH, 'utf-8'));
} catch (error) {
  console.warn('Failed to load cohort data:', error);
}

/**
 * Convert synthetic user to PersonaAttributes
 */
function toPersonaAttributes(user: any): PersonaAttributes {
  return {
    tech_comfort: user.attributes?.tech_comfort || 0.5,
    ai_attitude: user.attributes?.ai_attitude || 'pragmatic',
    engagement_tier: user.attributes?.engagement_tier || 'standard',
    capture_behavior: user.attributes?.capture_behavior || 'opportunistic',
    age: user.age || 40,
  };
}

/**
 * Persona fixture selectors
 */
export const personaFixtures = {
  /**
   * Get a random user from a specific persona type
   */
  getPersona(personaType: string): PersonaAttributes {
    const users = fullCohort.filter(u => u.persona_type === personaType);
    if (users.length === 0) {
      throw new Error(`No users found for persona type: ${personaType}`);
    }
    const user = users[Math.floor(Math.random() * users.length)];
    return toPersonaAttributes(user);
  },

  /**
   * Get a user with specific characteristics
   */
  getPersonaBy(criteria: {
    personaType?: string;
    engagementTier?: string;
    techComfort?: { min: number; max: number };
    aiAttitude?: string;
  }): PersonaAttributes {
    let filtered = fullCohort;

    if (criteria.personaType) {
      filtered = filtered.filter(u => u.persona_type === criteria.personaType);
    }

    if (criteria.engagementTier) {
      filtered = filtered.filter(u =>
        u.attributes?.engagement_tier === criteria.engagementTier
      );
    }

    if (criteria.techComfort) {
      filtered = filtered.filter(u => {
        const tc = u.attributes?.tech_comfort || 0.5;
        return tc >= criteria.techComfort!.min && tc <= criteria.techComfort!.max;
      });
    }

    if (criteria.aiAttitude) {
      filtered = filtered.filter(u =>
        u.attributes?.ai_attitude === criteria.aiAttitude
      );
    }

    if (filtered.length === 0) {
      throw new Error(`No users found matching criteria: ${JSON.stringify(criteria)}`);
    }

    const user = filtered[Math.floor(Math.random() * filtered.length)];
    return toPersonaAttributes(user);
  },

  /**
   * Get beta test cohort member
   */
  getBetaTester(index?: number): PersonaAttributes {
    if (betaCohort.length === 0) {
      throw new Error('Beta cohort not loaded');
    }

    const idx = index !== undefined ? index : Math.floor(Math.random() * betaCohort.length);
    if (idx >= betaCohort.length) {
      throw new Error(`Beta tester index ${idx} out of range (0-${betaCohort.length - 1})`);
    }

    return toPersonaAttributes(betaCohort[idx]);
  },

  /**
   * Get all users of a persona type
   */
  getAllPersonas(personaType: string): PersonaAttributes[] {
    return fullCohort
      .filter(u => u.persona_type === personaType)
      .map(toPersonaAttributes);
  },

  /**
   * Get complete user data (for journey tests)
   */
  getUserWithJourney(personaType: string): any {
    const users = fullCohort.filter(u =>
      u.persona_type === personaType &&
      u.journey &&
      u.journey.steps &&
      u.journey.steps.length > 0
    );

    if (users.length === 0) {
      throw new Error(`No users with journeys found for: ${personaType}`);
    }

    return users[Math.floor(Math.random() * users.length)];
  },
};

/**
 * Preset personas for common test scenarios
 */
export const presetPersonas = {
  // High tech comfort, enthusiastic
  earlyAdopter: () => personaFixtures.getPersonaBy({
    personaType: 'early_adopter',
    engagementTier: 'high',
    techComfort: { min: 0.8, max: 1.0 },
    aiAttitude: 'enthusiastic',
  }),

  // Low tech comfort, skeptical
  skepticalVeteran: () => personaFixtures.getPersonaBy({
    personaType: 'skeptical_veteran',
    engagementTier: 'low',
    techComfort: { min: 0.2, max: 0.4 },
    aiAttitude: 'skeptical',
  }),

  // Moderate tech, teaching focused
  masterEducator: () => personaFixtures.getPersonaBy({
    personaType: 'master_educator',
    engagementTier: 'standard',
    techComfort: { min: 0.5, max: 0.7 },
  }),

  // Beta tester profile
  betaTester: () => personaFixtures.getBetaTester(),

  // Studio practitioner - any
  studioPractitioner: () => personaFixtures.getPersona('studio_practitioner'),
};

/**
 * Extend Playwright test with persona fixtures
 */
export const test = base.extend<{
  persona: PersonaAttributes;
  earlyAdopter: PersonaAttributes;
  skepticalVeteran: PersonaAttributes;
  masterEducator: PersonaAttributes;
  betaTester: PersonaAttributes;
}>({
  persona: async ({}, use) => {
    // Default: random from any persona
    const personaTypes = [
      'master_educator',
      'studio_practitioner',
      'department_head',
      'early_adopter',
      'skeptical_veteran',
    ];
    const type = personaTypes[Math.floor(Math.random() * personaTypes.length)];
    await use(personaFixtures.getPersona(type));
  },

  earlyAdopter: async ({}, use) => {
    await use(presetPersonas.earlyAdopter());
  },

  skepticalVeteran: async ({}, use) => {
    await use(presetPersonas.skepticalVeteran());
  },

  masterEducator: async ({}, use) => {
    await use(presetPersonas.masterEducator());
  },

  betaTester: async ({}, use) => {
    await use(presetPersonas.betaTester());
  },
});

export { expect } from '@playwright/test';
