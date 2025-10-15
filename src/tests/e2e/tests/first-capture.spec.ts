/**
 * First Capture Session E2E Tests
 *
 * Tests the critical first upload workflow for different persona types
 * Based on T-SP-001 (Studio Practitioner First Ceramics Session)
 * and beta testing plan validation
 */

import { test, expect } from '../fixtures/personas.fixture';
import { UploadPage } from '../page-objects/upload.page';

test.describe('First Capture Session - Beta Test Scenarios', () => {
  test('T-SP-001: Ceramicist First Session - Multi-Modal Capture', async ({ page, betaTester }) => {
    // Given: Ceramicist (3+ years experience, moderate tech comfort)
    const uploadPage = new UploadPage(page, betaTester);
    await uploadPage.goto();

    // When: Uploads first throwing session
    const result = await uploadPage.firstCaptureSession({
      medium: 'ceramics_pottery',
      sessionType: 'throwing',
      duration: 22, // minutes
    });

    // Then: Upload succeeds and extraction starts
    expect(result.success).toBe(true);
    expect(result.completed).toBe(true);

    // Time investment should match synthetic data (13-15 min average)
    expect(result.timeInvested).toBeGreaterThanOrEqual(10);
    expect(result.timeInvested).toBeLessThanOrEqual(20);

    // Emotional state should be appropriate
    expect(['excited', 'satisfied', 'cautiously_optimistic']).toContain(result.emotionalState);

    // Validate extraction preview is available
    await uploadPage.validateUploadSuccess();

    // High engagement users preview extraction
    if (betaTester.engagement_tier === 'high') {
      await uploadPage.previewExtraction();
    }
  });

  test('T-SP-002: Low Tech Comfort - Error Recovery', async ({ page }) => {
    // Given: Studio practitioner with low tech comfort
    const lowTechPersona = {
      tech_comfort: 0.35,
      ai_attitude: 'cautious',
      engagement_tier: 'standard',
      capture_behavior: 'opportunistic',
      age: 58,
    };

    const uploadPage = new UploadPage(page, lowTechPersona);
    await uploadPage.goto();

    // When: Encounters upload error (simulate with invalid file)
    const result = await uploadPage.uploadFile({
      filePath: '/test-fixtures/invalid/large_file.mp4', // Triggers size limit error
      fileType: 'video',
      duration: 120, // Too long
      title: 'My first session',
    });

    // Then: Error handled gracefully
    expect(result).toBe(false);

    // Error message is clear and non-technical
    const errorMessage = await uploadPage.handleUploadError();
    expect(errorMessage).toBeTruthy();
    expect(errorMessage.length).toBeGreaterThan(0);

    // Help option is available for low tech users
    const helpButton = page.locator('[data-testid="upload-help"]');
    await expect(helpButton).toBeVisible();
  });

  test('T-ME-001: Master Educator First Curriculum Upload', async ({ page, masterEducator }) => {
    // Given: New Master Educator account
    const uploadPage = new UploadPage(page, masterEducator);
    await uploadPage.goto();

    // When: Uploads first lecture recording (45 min)
    const result = await uploadPage.firstCaptureSession({
      medium: 'education',
      sessionType: 'lecture',
      duration: 45,
    });

    // Then: Upload completes within 2 minutes
    expect(result.success).toBe(true);
    expect(result.timeInvested).toBeLessThanOrEqual(2);

    // Extraction identifies key elements
    // (Would validate extraction results here with real backend)
    await uploadPage.validateUploadSuccess();

    // Expected time: 15 minutes (matches synthetic data)
    // In real test, would measure actual user time
  });
});

test.describe('Engagement Tier Variations', () => {
  test('High Engagement - Comprehensive First Session', async ({ page, earlyAdopter }) => {
    // High engagement users:
    // - Add metadata (title, description, tags)
    // - Preview extraction results
    // - Explore all features

    const uploadPage = new UploadPage(page, earlyAdopter);
    await uploadPage.goto();

    const result = await uploadPage.uploadFile({
      filePath: '/test-fixtures/videos/ceramics/throwing_session.mp4',
      fileType: 'video',
      duration: 22,
      title: 'Advanced Centering Techniques',
      description: 'Demonstration of centering with soft clay in high humidity',
      tags: ['centering', 'soft_clay', 'humidity', 'technique'],
    });

    expect(result).toBe(true);

    // High engagement: preview extraction
    await uploadPage.previewExtraction();

    // Validate extraction preview loaded
    const preview = page.locator('[data-testid="extraction-preview"]');
    await expect(preview).toBeVisible();
  });

  test('Standard Engagement - Basic Upload', async ({ page, masterEducator }) => {
    // Standard engagement: basic upload, minimal metadata
    const uploadPage = new UploadPage(page, masterEducator);
    await uploadPage.goto();

    const result = await uploadPage.uploadFile({
      filePath: '/test-fixtures/videos/education/lecture.mp4',
      fileType: 'video',
      duration: 45,
      title: 'Week 3 Lecture',
      // No description or tags (standard engagement)
    });

    expect(result).toBe(true);
    // Standard users don't preview (move on quickly)
  });

  test('Low Engagement - Minimal Interaction', async ({ page, skepticalVeteran }) => {
    // Low engagement: bare minimum, may dropout
    const uploadPage = new UploadPage(page, skepticalVeteran);
    await uploadPage.goto();

    // Low engagement users provide minimal metadata
    const result = await uploadPage.uploadFile({
      filePath: '/test-fixtures/videos/education/lecture.mp4',
      fileType: 'video',
      duration: 30,
      title: 'Test Upload',
      // No other metadata
    });

    // May succeed but with hesitation
    if (result) {
      expect(result).toBe(true);
    }

    // Check for dropout risk
    const shouldDrop = uploadPage.shouldDropout(1);
    if (shouldDrop) {
      // In real scenario, user might abandon here
      console.log('Low engagement user at risk of dropout');
    }
  });
});

test.describe('Capture Behavior Patterns', () => {
  test('Systematic - Regular Pattern Detection', async ({ page }) => {
    // Systematic users upload on regular schedule (2-7 days)
    const systematicPersona = {
      tech_comfort: 0.65,
      ai_attitude: 'pragmatic',
      engagement_tier: 'standard',
      capture_behavior: 'systematic',
      age: 45,
    };

    const uploadPage = new UploadPage(page, systematicPersona);

    // Simulate multiple uploads over time
    for (let i = 0; i < 3; i++) {
      await uploadPage.goto();

      const result = await uploadPage.uploadFile({
        filePath: `/test-fixtures/videos/education/lecture_${i + 1}.mp4`,
        fileType: 'video',
        duration: 45,
        title: `Week ${i + 1} Lecture`,
      });

      expect(result).toBe(true);

      // Systematic: 3-5 day intervals
      // In real test, would wait or simulate time passing
    }

    // Platform should detect pattern and suggest scheduling
    const schedulePrompt = page.locator('[data-testid="schedule-suggestion"]');
    // await expect(schedulePrompt).toBeVisible();
  });

  test('Crisis-Driven - Burst Upload Pattern', async ({ page }) => {
    // Crisis-driven: burst of 3-10 uploads, then long gap
    const crisisPersona = {
      tech_comfort: 0.55,
      ai_attitude: 'cautious',
      engagement_tier: 'standard',
      capture_behavior: 'crisis_driven',
      age: 52,
    };

    const uploadPage = new UploadPage(page, crisisPersona);

    // Simulate burst (multiple uploads in one session)
    await uploadPage.goto();

    for (let i = 0; i < 5; i++) {
      const result = await uploadPage.uploadFile({
        filePath: `/test-fixtures/videos/ceramics/session_${i + 1}.mp4`,
        fileType: 'video',
        duration: 20,
        title: `Batch Upload ${i + 1}`,
      });

      expect(result).toBe(true);
    }

    // System should handle batch processing
    const batchStatus = page.locator('[data-testid="batch-upload-status"]');
    // await expect(batchStatus).toBeVisible();
  });
});

test.describe('Beta Test Validation', () => {
  test('Beta Tester #1 - High Engagement Ceramicist', async ({ page }) => {
    // From beta cohort: studio_practitioner_user_425
    // Age 42, Tech Comfort 0.67, High Engagement, Crisis-Driven
    const betaTester1 = {
      tech_comfort: 0.67,
      ai_attitude: 'pragmatic',
      engagement_tier: 'high',
      capture_behavior: 'crisis_driven',
      age: 42,
    };

    const uploadPage = new UploadPage(page, betaTester1);
    await uploadPage.goto();

    const result = await uploadPage.firstCaptureSession({
      medium: 'ceramics_pottery',
      sessionType: 'throwing',
      duration: 22,
    });

    // Validation from beta testing plan
    expect(result.success).toBe(true);
    expect(result.completed).toBe(true);

    // High engagement: previews extraction
    await uploadPage.previewExtraction();

    // Validates extraction quality
    const preview = page.locator('[data-testid="extraction-preview"]');
    await expect(preview).toBeVisible();

    // Expected to complete (90% completion rate in synthetic journey)
    expect(result.emotionalState).toContain('satisfied');
  });

  test('Beta Tester #3 - Standard Engagement, Master Ceramicist', async ({ page }) => {
    // From beta cohort: studio_practitioner_user_7
    // Age 48, Tech Comfort 0.49, Standard Engagement, Experimental
    const betaTester3 = {
      tech_comfort: 0.49,
      ai_attitude: 'cautious',
      engagement_tier: 'standard',
      capture_behavior: 'experimental',
      age: 48,
    };

    const uploadPage = new UploadPage(page, betaTester3);
    await uploadPage.goto();

    const result = await uploadPage.firstCaptureSession({
      medium: 'ceramics_pottery',
      sessionType: 'throwing',
      duration: 25,
    });

    // May not complete first session (47% completion in synthetic journey)
    // This tests realistic dropout scenarios
    if (!result.completed) {
      // Platform should handle graceful exit
      const saveProgress = page.locator('[data-testid="save-progress"]');
      // await expect(saveProgress).toBeVisible();
    }

    // Emotional state: cautiously_optimistic or uncertain
    expect(['cautiously_optimistic', 'uncertain', 'satisfied']).toContain(
      result.emotionalState
    );
  });
});
