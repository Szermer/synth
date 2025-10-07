/**
 * Upload/Capture Page Object
 *
 * Handles file upload workflows with persona-specific behaviors
 */

import { Page, Locator, expect } from '@playwright/test';
import { BasePage, PersonaAttributes } from './base.page';

export interface UploadOptions {
  filePath: string;
  fileType: 'video' | 'audio' | 'document';
  duration?: number; // minutes
  title?: string;
  description?: string;
  tags?: string[];
}

export class UploadPage extends BasePage {
  // Locators
  readonly uploadButton: Locator;
  readonly fileInput: Locator;
  readonly titleInput: Locator;
  readonly descriptionInput: Locator;
  readonly tagsInput: Locator;
  readonly uploadProgress: Locator;
  readonly uploadSuccess: Locator;
  readonly uploadError: Locator;
  readonly previewButton: Locator;
  readonly submitButton: Locator;

  constructor(page: Page, persona: PersonaAttributes) {
    super(page, persona);

    // Initialize locators
    this.uploadButton = page.locator('[data-testid="upload-button"]');
    this.fileInput = page.locator('input[type="file"]');
    this.titleInput = page.locator('[data-testid="upload-title"]');
    this.descriptionInput = page.locator('[data-testid="upload-description"]');
    this.tagsInput = page.locator('[data-testid="upload-tags"]');
    this.uploadProgress = page.locator('[data-testid="upload-progress"]');
    this.uploadSuccess = page.locator('[data-testid="upload-success"]');
    this.uploadError = page.locator('[data-testid="upload-error"]');
    this.previewButton = page.locator('[data-testid="preview-extraction"]');
    this.submitButton = page.locator('[data-testid="submit-upload"]');
  }

  /**
   * Navigate to upload page
   */
  async goto() {
    await this.navigate('/capture/upload');
  }

  /**
   * Complete upload flow with persona behavior
   */
  async uploadFile(options: UploadOptions): Promise<boolean> {
    // Click upload button
    await this.click(this.uploadButton, { description: 'Start upload' });

    // Low tech users may struggle here
    if (this.persona.tech_comfort < 0.4) {
      await this.personaDelay('file_browsing');
    }

    // Upload file
    await this.uploadFile(this.fileInput, options.filePath);

    // Wait for upload progress
    await this.waitFor(this.uploadProgress);

    // Fill metadata
    if (options.title) {
      await this.type(this.titleInput, options.title);
    }

    if (options.description) {
      await this.type(this.descriptionInput, options.description);
    }

    if (options.tags && options.tags.length > 0) {
      // High engagement users add tags
      if (this.persona.engagement_tier === 'high') {
        await this.type(this.tagsInput, options.tags.join(', '));
      }
    }

    // Submit upload
    await this.click(this.submitButton);

    // Wait for success or error
    try {
      await this.uploadSuccess.waitFor({ timeout: 120000 }); // 2 min for large files
      return true;
    } catch (error) {
      // Handle error
      const errorMessage = await this.uploadError.textContent();
      await this.handleError(errorMessage || 'Upload failed');
      return false;
    }
  }

  /**
   * Check extraction preview (high engagement users do this)
   */
  async previewExtraction(): Promise<void> {
    if (this.persona.engagement_tier !== 'high') {
      return; // Only high engagement users preview
    }

    await this.click(this.previewButton);
    await this.personaDelay('reading');

    // Read extraction results
    const preview = this.page.locator('[data-testid="extraction-preview"]');
    await this.readContent(preview);
  }

  /**
   * Validate upload success
   */
  async validateUploadSuccess(): Promise<boolean> {
    const success = await this.uploadSuccess.isVisible();
    if (success) {
      await this.readContent(this.uploadSuccess);
    }
    return success;
  }

  /**
   * Handle upload error scenario
   */
  async handleUploadError(): Promise<string> {
    const errorText = await this.uploadError.textContent();

    // Low tech users need clear guidance
    if (this.persona.tech_comfort < 0.4) {
      const helpButton = this.page.locator('[data-testid="upload-help"]');
      if (await helpButton.isVisible()) {
        await this.click(helpButton);
      }
    }

    return errorText || '';
  }

  /**
   * Simulate first capture session for beta testers
   * Based on Private Language beta testing plan
   */
  async firstCaptureSession(options: {
    medium: string;
    sessionType: string;
    duration: number;
  }): Promise<{
    success: boolean;
    timeInvested: number;
    completed: boolean;
    emotionalState: string;
  }> {
    const startTime = Date.now();

    // Generate realistic file based on medium
    const filePath = this.generateMockFilePath(options.medium, options.sessionType);

    // Upload file
    const uploadSuccess = await this.uploadFile({
      filePath,
      fileType: 'video',
      duration: options.duration,
      title: `First ${options.sessionType} session`,
      description: `Captured ${options.medium} ${options.sessionType}`,
    });

    // Preview extraction if high engagement
    if (this.persona.engagement_tier === 'high') {
      await this.previewExtraction();
    }

    const timeInvested = Math.round((Date.now() - startTime) / 1000 / 60); // minutes

    // Determine emotional state based on experience
    let emotionalState = 'neutral';
    if (uploadSuccess) {
      if (this.persona.ai_attitude === 'enthusiastic') {
        emotionalState = 'excited';
      } else if (this.persona.tech_comfort > 0.6) {
        emotionalState = 'satisfied';
      } else {
        emotionalState = 'cautiously_optimistic';
      }
    } else {
      if (this.persona.tech_comfort < 0.4) {
        emotionalState = 'frustrated';
      } else {
        emotionalState = 'uncertain';
      }
    }

    return {
      success: uploadSuccess,
      timeInvested,
      completed: uploadSuccess,
      emotionalState,
    };
  }

  /**
   * Generate mock file path for testing
   */
  private generateMockFilePath(medium: string, sessionType: string): string {
    return `/test-fixtures/videos/${medium}/${sessionType}_session.mp4`;
  }
}
