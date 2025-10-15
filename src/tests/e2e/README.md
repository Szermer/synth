# E2E Testing Framework for Private Language

**Persona-Based End-to-End Testing Using Synthetic User Data**

This framework uses the 500-user synthetic cohort to drive realistic E2E tests for the Private Language platform, ensuring the product works for all user segments including edge cases.

## Overview

- **500 synthetic users** with validated behavioral patterns
- **10 persona types** covering 80% core users + 20% edge cases
- **Persona-aware page objects** that mimic real user behavior
- **Beta test simulation** with 5 ceramicists matching screening criteria
- **Realistic timing and interaction patterns** based on user attributes

## Quick Start

### Installation

```bash
# Install dependencies
npm install

# Install Playwright browsers
npx playwright install

# Run tests
npm run test:e2e
```

### Run Specific Test Suites

```bash
# First capture session tests (critical path)
npx playwright test first-capture.spec.ts

# Beta tester simulation
npx playwright test first-capture.spec.ts --grep "Beta Test"

# Engagement tier variations
npx playwright test first-capture.spec.ts --grep "Engagement Tier"

# Specific persona
npx playwright test --grep "Master Educator"
```

## Architecture

```
src/tests/e2e/
├── README.md                          # This file
├── E2E_TEST_SCENARIOS.md              # Comprehensive test scenarios
├── playwright.config.ts               # Playwright configuration
├── page-objects/                      # Persona-aware page objects
│   ├── base.page.ts                   # Base with persona behaviors
│   ├── upload.page.ts                 # Upload/capture workflows
│   ├── query.page.ts                  # Query and search
│   └── review.page.ts                 # Extraction review
├── fixtures/                          # Test data from synthetic cohort
│   ├── personas.fixture.ts            # Persona fixtures
│   └── journeys.fixture.ts            # Journey data
├── tests/                             # Actual test specs
│   ├── first-capture.spec.ts          # First session tests
│   ├── query-workflow.spec.ts         # Query tests
│   ├── engagement-patterns.spec.ts    # Engagement tier tests
│   └── beta-simulation.spec.ts        # Beta test scenarios
└── scenarios/                         # Test scenario definitions
    └── beta-testers/                  # Beta test cohort scenarios
```

## Test Data Sources

### 500-User Cohort (`output/private_language_synthetic_users.json`)

**Distribution:**
- Master Educator: 150 users (30%)
- Studio Practitioner: 100 users (20%)
- Department Head: 75 users (15%)
- Early Adopter: 50 users (10%)
- Skeptical Veteran: 25 users (5%)
- Cross-Domain Practitioner: 30 users (6%)
- International User: 25 users (5%)
- Industry Trainer: 20 users (4%)
- Graduate Student: 15 users (3%)
- Outlier/Stress Case: 10 users (2%)

**Each user includes:**
- Demographics (age, gender, education)
- Tech comfort level (0.0-1.0)
- AI attitude (enthusiastic, pragmatic, cautious, skeptical, fearful)
- Engagement tier (high 20%, standard 60%, low 20%)
- Capture behavior (systematic, opportunistic, crisis-driven, experimental)
- Complete journey with 5-25 sessions
- Realistic timestamps and completion patterns

### Beta Test Cohort (`output/beta_test_cohort.json`)

**5 ceramicists matching beta screening criteria:**
1. High engagement, crisis-driven (Tech: 0.67, Age: 42)
2. High engagement, experimental (Tech: 0.45, Age: 53)
3. Standard engagement, experimental (Tech: 0.49, Age: 48)
4. Standard engagement, opportunistic (Tech: 0.62, Age: 43)
5. Standard engagement, systematic (Tech: 0.58, Age: 53)

**All meet criteria:**
- ✅ Medium: ceramics_pottery
- ✅ Craft experience: 3+ years (avg 12 years)
- ✅ Tech comfort: 0.4-0.7 (moderate)
- ✅ Teaching experience: workshops/classes
- ✅ Engagement: standard or high

## Persona-Aware Testing

### How It Works

Tests use `PersonaAttributes` to drive realistic user behavior:

```typescript
interface PersonaAttributes {
  tech_comfort: number;        // 0.0-1.0 (low to high)
  ai_attitude: string;          // enthusiastic, pragmatic, cautious, skeptical, fearful
  engagement_tier: string;      // high, standard, low
  capture_behavior: string;     // systematic, opportunistic, crisis_driven, experimental
  age: number;                  // Affects reading speed, typing speed
}
```

### Behavioral Adaptations

**Low Tech Comfort (< 0.4):**
- Slower typing (120ms/char vs 30ms)
- More hesitation before clicks
- Re-reads form fields for validation
- Needs clear error messages
- May panic on errors

**High Tech Comfort (> 0.8):**
- Fast typing (30ms/char)
- Quick navigation
- Scans content vs reads carefully
- Explores features proactively

**Skeptical/Fearful AI Attitude:**
- Reads privacy policies carefully
- Hesitates before data upload
- Needs transparency about AI usage
- May dropout if trust not established

**Engagement Tiers:**
- **High (20%)**: 15-25 sessions, adds metadata, previews extraction, explores features
- **Standard (60%)**: 10-20 sessions, basic workflows, occasional queries
- **Low (20%)**: 5-12 sessions, minimal interaction, high dropout risk

**Capture Behaviors:**
- **Systematic (25%)**: Regular 2-7 day intervals, scheduling suggestions
- **Opportunistic (35%)**: Variable 1-14 days, mobile-friendly
- **Crisis-Driven (25%)**: Bursts (3-10 uploads), batch processing
- **Experimental (15%)**: Irregular patterns, feature exploration

## Test Scenarios

### Priority 0 (Critical Path)

**T-SP-001: Studio Practitioner First Capture**
- Beta test validation scenario
- Multi-modal upload (video, audio commentary)
- Extraction across 6 dimensions
- Time: 13-15 minutes (matches synthetic data)

**T-ME-001: Master Educator First Upload**
- 45-min lecture recording
- Upload completes <2 minutes
- Extraction preview shown
- Expected time: 15 minutes

**T-SP-002: Low Tech Comfort Error Recovery**
- Simulates upload error (file size, format)
- Tests error handling for tech_comfort < 0.4
- Validates help/support availability

### Priority 1 (Institutional/Adoption)

**T-DH-001: Department Head Institution Setup**
- Multi-faculty onboarding
- Permission controls
- Budget tracking
- ROI dashboard

**T-EA-001: Early Adopter Feature Exploration**
- Explores all features in first week
- API integration
- Community features
- Feature requests

**T-SV-001: Skeptical Veteran Privacy Flow**
- Privacy-first onboarding
- Data sovereignty transparency
- "How AI is used" explanation
- Granular sharing controls

### Priority 2/3 (Edge Cases)

- Cross-domain workflows
- GDPR compliance (International)
- Compliance audit trails (Industry Trainer)
- Budget-constrained users (Graduate Student)
- System boundaries (Outlier/Stress Case)

## Fixtures Usage

### Get a Random Persona

```typescript
import { test, expect } from '../fixtures/personas.fixture';

test('Upload workflow', async ({ page, persona }) => {
  // persona is randomly selected from any type
  const uploadPage = new UploadPage(page, persona);
  await uploadPage.goto();
  // ... test continues
});
```

### Get Specific Persona Type

```typescript
test('Educator workflow', async ({ page, masterEducator }) => {
  // masterEducator fixture from preset personas
  const uploadPage = new UploadPage(page, masterEducator);
  await uploadPage.goto();
});
```

### Get Beta Tester

```typescript
test('Beta test scenario', async ({ page, betaTester }) => {
  // betaTester from the 5-person beta cohort
  const uploadPage = new UploadPage(page, betaTester);
  await uploadPage.goto();
});
```

### Custom Criteria

```typescript
import { personaFixtures } from '../fixtures/personas.fixture';

const lowTechSkeptic = personaFixtures.getPersonaBy({
  personaType: 'skeptical_veteran',
  techComfort: { min: 0.2, max: 0.4 },
  aiAttitude: 'skeptical',
  engagementTier: 'low',
});
```

## Page Objects

### BasePage

Provides persona-aware behaviors:
- `click()` - Hesitation for low tech comfort
- `type()` - Variable typing speed
- `readContent()` - Reading time based on age/attitude
- `handleError()` - Panic response for low tech
- `shouldDropout()` - Realistic dropout simulation

### UploadPage

Upload/capture workflows:
- `uploadFile()` - Complete upload with metadata
- `previewExtraction()` - High engagement users only
- `firstCaptureSession()` - Beta test scenario
- `handleUploadError()` - Error recovery flows

### QueryPage

Query and search:
- `submitQuery()` - Natural language queries
- `validateResults()` - Result quality checks
- `refineQuery()` - Iterative refinement
- `rateAnswer()` - Satisfaction tracking

### ReviewPage

Extraction review:
- `reviewInsights()` - Approve/reject extractions
- `bulkActions()` - Batch review
- `addContext()` - Refine low-confidence items
- `trackTime()` - Time investment measurement

## Running Tests

### Development

```bash
# Run with UI (headed mode)
npx playwright test --headed

# Debug specific test
npx playwright test --debug first-capture.spec.ts

# Run with specific persona
npx playwright test --grep "Early Adopter"
```

### CI/CD

```bash
# Run all E2E tests
npm run test:e2e:ci

# Generate HTML report
npx playwright show-report
```

### Beta Test Simulation

```bash
# Run all beta test scenarios
npx playwright test --grep "Beta Test"

# Specific beta tester
npx playwright test --grep "Beta Tester #1"

# Generate beta test report
npm run test:beta-report
```

## Metrics & Validation

### Performance Baselines

From synthetic user data:
- **Upload time**: <2 min for 45-min video
- **Query response**: <10s for complex queries
- **Time investment**: 13-15 min avg for first session
- **Extraction accuracy**: >85% (measured by approval rate)

### Success Criteria

**From Beta Testing Plan:**
- ✅ Extraction accuracy >85%
- ✅ Query satisfaction >85% "helpful"
- ✅ Review efficiency: >60% of flagged items reviewed within 1 week
- ✅ Artist engagement: >75% complete all 6 weeks
- ✅ NPS >0 (more promoters than detractors)

### Conversion Thresholds

Per persona (from synthetic data):
- **Discovery completion**: 40%-95% depending on persona
- **Onboarding completion**: 30%-95%
- **Active use engagement**: 20%-95%
- **Low engagement dropout**: <15% unplanned

## User Story Mapping

See `E2E_TEST_SCENARIOS.md` for complete mapping to Private Language user stories (US001-US025).

**Example Mapping:**

| Test ID | User Story | Persona | Priority |
|---------|------------|---------|----------|
| T-SP-001 | US007: Multi-modal Capture | Studio Practitioner | P0 |
| T-ME-001 | US002: Lecture Upload | Master Educator | P0 |
| T-SV-001 | US015: Privacy Controls | Skeptical Veteran | P1 |
| T-DH-001 | US020: Institution Setup | Department Head | P1 |
| T-EA-001 | US023: API Integration | Early Adopter | P2 |

## Best Practices

### 1. Use Realistic Personas

```typescript
// ✅ Good: Use fixture for realistic behavior
test('Upload test', async ({ page, betaTester }) => {
  const uploadPage = new UploadPage(page, betaTester);
  // Test will adapt to beta tester's tech comfort, engagement tier
});

// ❌ Bad: Hardcoded persona
const fakePerson = { tech_comfort: 0.5, ... };
```

### 2. Respect Persona Behaviors

```typescript
// ✅ Good: Let page object handle timing
await uploadPage.click(button);

// ❌ Bad: Fixed waits ignore persona
await button.click();
await page.waitForTimeout(1000); // Same for all users
```

### 3. Test Dropout Scenarios

```typescript
// ✅ Good: Test realistic dropout
if (uploadPage.shouldDropout(stepNumber)) {
  // Validate graceful exit flow
  await expect(saveProgressButton).toBeVisible();
}
```

### 4. Validate Against Synthetic Data

```typescript
// ✅ Good: Compare to framework expectations
expect(timeInvested).toBeGreaterThanOrEqual(13);
expect(timeInvested).toBeLessThanOrEqual(15);

// From synthetic data: avg 13-15 min for first session
```

## Troubleshooting

**Tests failing with timeout?**
- Check if persona has low tech comfort (needs longer timeouts)
- Verify persona fixtures loading correctly
- Check if test expectations match persona behavior

**Unrealistic test behavior?**
- Review PersonaAttributes being passed to page objects
- Ensure page object methods use `personaDelay()` not fixed waits
- Validate persona selection criteria in fixtures

**Beta test scenarios not matching plan?**
- Verify beta cohort loaded from `output/beta_test_cohort.json`
- Check screening criteria in `generate_beta_test_cohort.py`
- Ensure beta testers meet all criteria (ceramics, 3+ years, moderate tech)

## Next Steps

1. **Implement remaining page objects**: QueryPage, ReviewPage, DashboardPage
2. **Add journey-based tests**: Multi-session workflows from synthetic journeys
3. **Performance testing**: Load test with engagement tier distributions
4. **CI/CD integration**: Automate test runs on PR
5. **Test data generation**: Generate mock files (videos, documents) for upload tests

## References

- [E2E Test Scenarios](./E2E_TEST_SCENARIOS.md) - Complete test scenario catalog
- [Synthetic User Framework](../../docs/architecture/decisions/0004-synthetic-user-framework-integration.md)
- [Beta Testing Plan](/Users/stephenszermer/Dev/PrivateLanguage/docs/development/beta-testing/BETA_TESTING_PLAN.md)
- [Private Language User Personas](/Users/stephenszermer/Dev/PrivateLanguage/docs/personas/USER_PERSONAS.md)

---

**Maintained by:** QA & Product Teams
**Last Updated:** 2025-10-07
**Framework Version:** 2.1
