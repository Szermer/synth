/**
 * Base Page Object
 *
 * Common functionality for all page objects with persona-aware behaviors
 */

import { Page, Locator } from '@playwright/test';

export interface PersonaAttributes {
  tech_comfort: number;
  ai_attitude: string;
  engagement_tier: string;
  capture_behavior: string;
  age: number;
}

export class BasePage {
  readonly page: Page;
  readonly persona: PersonaAttributes;

  constructor(page: Page, persona: PersonaAttributes) {
    this.page = page;
    this.persona = persona;
  }

  /**
   * Navigate with persona-appropriate speed
   * Low tech comfort users take longer
   */
  async navigate(url: string) {
    await this.page.goto(url);
    await this.personaDelay('navigation');
  }

  /**
   * Click with persona-appropriate hesitation
   * Low tech comfort = more hesitation
   * Skeptical AI attitude = extra validation
   */
  async click(locator: Locator, options?: { description?: string }) {
    // Skeptical users read carefully before clicking
    if (this.persona.ai_attitude === 'skeptical' || this.persona.ai_attitude === 'fearful') {
      await this.personaDelay('reading');
    }

    // Low tech comfort users hover before clicking
    if (this.persona.tech_comfort < 0.5) {
      await locator.hover();
      await this.personaDelay('hesitation');
    }

    await locator.click();
    await this.personaDelay('action');
  }

  /**
   * Type with persona-appropriate speed
   * Lower tech comfort = slower typing
   */
  async type(locator: Locator, text: string) {
    const delay = this.getTypingDelay();
    await locator.fill(''); // Clear first
    await locator.type(text, { delay });
  }

  /**
   * Fill form with persona behavior
   */
  async fill(locator: Locator, value: string) {
    // Low tech users validate fields more
    if (this.persona.tech_comfort < 0.5) {
      await locator.fill(value);
      await this.personaDelay('validation');
      // Re-read what they entered
      const currentValue = await locator.inputValue();
      if (currentValue === value) {
        await this.personaDelay('confirmation');
      }
    } else {
      await locator.fill(value);
    }
  }

  /**
   * Upload file with persona-appropriate behavior
   */
  async uploadFile(locator: Locator, filePath: string) {
    // Low tech users may struggle with file selection
    if (this.persona.tech_comfort < 0.4) {
      await this.personaDelay('file_browsing');
    }

    await locator.setInputFiles(filePath);

    // Validate upload started
    await this.personaDelay('validation');
  }

  /**
   * Read content with persona speed
   * Older users and skeptical users read more carefully
   */
  async readContent(locator: Locator): Promise<string> {
    const text = await locator.textContent();

    // Skeptical users read everything
    if (this.persona.ai_attitude === 'skeptical' || this.persona.ai_attitude === 'cautious') {
      await this.personaDelay('careful_reading');
    } else if (this.persona.age > 55) {
      await this.personaDelay('reading');
    } else if (this.persona.tech_comfort > 0.8) {
      await this.personaDelay('scanning');
    } else {
      await this.personaDelay('reading');
    }

    return text || '';
  }

  /**
   * Handle errors with persona behavior
   */
  async handleError(errorMessage: string) {
    // Low tech users panic more
    if (this.persona.tech_comfort < 0.4) {
      await this.personaDelay('panic');
      // May need to re-read error multiple times
      await this.personaDelay('reading');
      await this.personaDelay('reading');
    } else {
      await this.personaDelay('reading');
    }
  }

  /**
   * Persona-appropriate delays
   */
  private async personaDelay(action: string) {
    const delays: Record<string, number> = {
      navigation: 500,
      reading: 2000,
      careful_reading: 5000,
      scanning: 500,
      hesitation: 1000,
      action: 300,
      validation: 800,
      confirmation: 500,
      panic: 2000,
      file_browsing: 3000,
    };

    let baseDelay = delays[action] || 500;

    // Adjust for tech comfort
    const techMultiplier = 2 - this.persona.tech_comfort; // 0.2 comfort = 1.8x slower
    baseDelay *= techMultiplier;

    // Adjust for age
    if (this.persona.age > 60) {
      baseDelay *= 1.3;
    } else if (this.persona.age > 50) {
      baseDelay *= 1.15;
    }

    await this.page.waitForTimeout(baseDelay);
  }

  /**
   * Get typing delay based on tech comfort
   */
  private getTypingDelay(): number {
    if (this.persona.tech_comfort > 0.8) {
      return 30; // Fast typer
    } else if (this.persona.tech_comfort > 0.6) {
      return 50; // Average
    } else if (this.persona.tech_comfort > 0.4) {
      return 80; // Slower
    } else {
      return 120; // Hunt and peck
    }
  }

  /**
   * Wait for element with persona patience
   */
  async waitFor(locator: Locator) {
    const timeout = this.persona.tech_comfort > 0.7 ? 5000 : 10000;
    await locator.waitFor({ timeout });
  }

  /**
   * Check if persona would dropout at this point
   * Used for realistic dropout testing
   */
  shouldDropout(currentStep: number): boolean {
    // Low engagement users more likely to dropout
    if (this.persona.engagement_tier === 'low' && currentStep > 3) {
      return Math.random() < 0.15; // 15% dropout chance
    }

    // Skeptical users dropout if confused
    if (this.persona.ai_attitude === 'skeptical' && currentStep > 2) {
      return Math.random() < 0.08;
    }

    return false;
  }
}
