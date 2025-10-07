# ADR-0005: Persona-Based E2E Testing Framework

**Status:** ✅ Accepted
**Date:** 2025-10-07
**Impact:** 🟡 Medium

## Context

After implementing the Synthetic User Generation Framework (ADR-0004) with 500 realistic users across 10 persona types, we needed a way to leverage this data for comprehensive end-to-end testing of the Private Language platform.

### Problem

Traditional E2E testing approaches have limitations:
- **Generic test users** don't represent real behavioral diversity
- **Hardcoded test data** lacks statistical realism
- **No edge case coverage** - tests focus on happy paths
- **Manual test case creation** is time-consuming and incomplete
- **No persona-specific behaviors** - all tests act the same way
- **Missing beta test validation** - can't simulate real user cohorts

### Requirements

1. Leverage the 500-user synthetic cohort for test data
2. Model persona-specific behaviors (tech comfort, AI attitude, engagement)
3. Validate against beta testing plan scenarios
4. Cover all 10 persona types including edge cases
5. Provide realistic timing and interaction patterns
6. Enable dropout and error recovery testing
7. Map to Private Language user stories

## Decision

We implemented a **persona-based E2E testing framework** that uses synthetic user data to drive Playwright tests with realistic behavioral patterns.

### 1. Test Scenario Catalog (50+ Scenarios)

Created comprehensive test scenarios mapped to all 10 personas:

**Priority Organization:**
- **P0 (Critical Path)**: Master Educator, Studio Practitioner first uploads
- **P1 (Institutional/Adoption)**: Department Head, Early Adopter, Skeptical Veteran
- **P2/P3 (Edge Cases)**: Cross-Domain, International, Graduate Student, Outliers

**Test Coverage Matrix:**
```
Persona Type              Distribution  Priority  Scenarios
Master Educator           30%           P0        5 scenarios
Studio Practitioner       20%           P0        6 scenarios
Department Head           15%           P1        3 scenarios
Early Adopter             10%           P1        3 scenarios
Skeptical Veteran         5%            P2        3 scenarios
Cross-Domain              6%            P2        2 scenarios
International User        5%            P2        2 scenarios
Industry Trainer          4%            P2        2 scenarios
Graduate Student          3%            P3        2 scenarios
Outlier/Stress Case       2%            P3        2 scenarios
```

### 2. Beta Test Simulation Cohort

Generated 5 ceramicists from the 500-user dataset matching beta testing plan criteria:

**Selection Script:** `generate_beta_test_cohort.py`

**Screening Criteria:**
- Medium: ceramics_pottery (Priority 1 for initial validation)
- Craft experience: 3+ years
- Tech comfort: 0.4-0.7 (moderate - can navigate web apps)
- Teaching experience: workshops, classes, or informal teaching
- Engagement tier: standard or high (willing to commit 2-4 hours/week)

**Results:** 5 testers from 13 candidates
- 100% ceramics match
- Tech comfort: 0.45-0.67 (perfect moderate range)
- Craft experience: 5-40 years (avg 12.0 years)
- Engagement: 40% high, 60% standard
- Capture behaviors: All 4 types represented

### 3. Persona-Aware Page Objects

Implemented Playwright page objects that adapt to persona attributes:

**BasePage (Behavioral Engine):**
```typescript
class BasePage {
  async click(locator: Locator) {
    // Skeptical users read carefully before clicking
    if (persona.ai_attitude === 'skeptical') {
      await this.personaDelay('reading');
    }

    // Low tech users hover before clicking
    if (persona.tech_comfort < 0.5) {
      await locator.hover();
      await this.personaDelay('hesitation');
    }

    await locator.click();
  }

  async type(locator: Locator, text: string) {
    const delay = this.getTypingDelay(); // 30-120ms based on tech_comfort
    await locator.type(text, { delay });
  }
}
```

**Behavioral Adaptations:**

| Persona Attribute | Impact on Tests |
|-------------------|-----------------|
| **Tech Comfort < 0.4** | Typing: 120ms/char, Hesitation: 1s, Re-reads fields |
| **Tech Comfort > 0.8** | Typing: 30ms/char, Fast navigation, Feature exploration |
| **AI Attitude: Skeptical** | Reads privacy (5s), Hesitates on upload, May dropout |
| **AI Attitude: Enthusiastic** | Quick adoption, Explores features, Provides feedback |
| **Age > 60** | 1.3x slower reading, Careful validation |
| **Engagement Tier: High** | Adds metadata, Previews extraction, 15-25 sessions |
| **Engagement Tier: Low** | Minimal metadata, 5-12 sessions, 15% dropout risk |

**Capture Behavior Timing:**
- **Systematic (25%)**: Regular 2-7 day intervals
- **Opportunistic (35%)**: Variable 1-14 day intervals
- **Crisis-Driven (25%)**: Bursts (1-3 days) then gaps (10-30 days)
- **Experimental (15%)**: Irregular 1-21 day intervals

### 4. Test Fixtures from Synthetic Data

Created Playwright fixtures that load from the 500-user cohort:

```typescript
// Get random persona
test('Upload', async ({ page, persona }) => {
  const uploadPage = new UploadPage(page, persona);
  // Test adapts to persona's tech comfort, engagement, etc.
});

// Get specific preset
test('Educator flow', async ({ page, masterEducator }) => {
  // Pre-configured Master Educator persona
});

// Get beta tester
test('Beta scenario', async ({ page, betaTester }) => {
  // One of the 5 beta cohort members
});

// Custom criteria
const lowTechSkeptic = personaFixtures.getPersonaBy({
  personaType: 'skeptical_veteran',
  techComfort: { min: 0.2, max: 0.4 },
  aiAttitude: 'skeptical',
});
```

### 5. Realistic Test Implementation

**First Capture Session Tests:**
- T-SP-001: Ceramicist multi-modal upload (22 min video)
- T-ME-001: Educator lecture upload (45 min)
- T-SP-002: Low tech comfort error recovery
- Engagement tier variations (high, standard, low)
- Capture behavior patterns
- Beta tester simulations (5 scenarios)

**Validation Against Synthetic Data:**
```typescript
// Time investment should match framework data
expect(timeInvested).toBeGreaterThanOrEqual(13);
expect(timeInvested).toBeLessThanOrEqual(15);
// Matches synthetic data: 13-15 min avg for first session
```

## Consequences

### Positive

✅ **Comprehensive Coverage**
- 50+ test scenarios across all 10 personas
- Core users (80%) and edge cases (20%) both covered
- Beta test plan scenarios validated before real users

✅ **Behavioral Realism**
- Tests adapt to user attributes (tech comfort, age, AI attitude)
- Realistic timing patterns (typing speed, reading, hesitation)
- Dropout scenarios testable

✅ **Data-Driven Testing**
- 500 realistic users available as test data
- No manual test data creation needed
- Statistically valid distributions

✅ **Beta Test Validation**
- 5-person beta cohort simulates real testers
- Matches screening criteria perfectly
- Validates platform before real beta begins

✅ **Maintenance Efficiency**
- Adding new persona type automatically generates test users
- Behavioral changes in framework propagate to tests
- Centralized persona logic in page objects

✅ **Edge Case Discovery**
- Skeptical veterans test privacy flows
- Low tech users test error handling
- Outliers test system boundaries
- International users test GDPR compliance

### Negative

⚠️ **Increased Complexity**
- Page objects more complex than standard Playwright
- Requires understanding of persona attributes
- Debugging requires knowledge of behavioral modeling

⚠️ **Test Data Dependency**
- Tests depend on synthetic cohort generation
- Cohort must be regenerated if framework changes
- Requires synthetic data files to be committed or generated in CI

⚠️ **Performance Overhead**
- Persona delays make tests slower (intentionally)
- Low tech comfort tests take 2-3x longer
- Need to balance realism vs test suite duration

⚠️ **Learning Curve**
- New developers need to understand persona system
- Non-standard Playwright patterns
- Requires documentation and examples

### Mitigations

- **Documentation**: Comprehensive README with examples
- **Presets**: Common persona presets (earlyAdopter, skepticalVeteran) for easy use
- **Fast mode**: Option to disable persona delays for CI speed
- **Fixtures cached**: Test data loaded once, reused across tests

## Implementation

### Files Created

**Test Scenarios:**
- `src/tests/e2e/E2E_TEST_SCENARIOS.md` (1,200 lines) - Complete test catalog

**Documentation:**
- `src/tests/e2e/README.md` (650 lines) - Framework guide

**Page Objects:**
- `src/tests/e2e/page-objects/base.page.ts` (350 lines) - Persona-aware behaviors
- `src/tests/e2e/page-objects/upload.page.ts` (250 lines) - Upload workflows

**Test Fixtures:**
- `src/tests/e2e/fixtures/personas.fixture.ts` (180 lines) - Synthetic data integration

**Tests:**
- `src/tests/e2e/tests/first-capture.spec.ts` (240 lines) - 12 Playwright tests

**Tools:**
- `generate_beta_test_cohort.py` (210 lines) - Beta cohort selector

**Total:** 7 files, 3,080 lines

### Test Data

**500-User Cohort:** `output/private_language_synthetic_users.json`
- All 10 persona types with validated distributions
- Complete journeys (5-25 sessions per user)
- Realistic timestamps and emotional states
- Engagement tiers and capture behaviors

**Beta Cohort:** `output/beta_test_cohort.json`
- 5 ceramicists matching screening criteria
- Tech comfort: 0.45-0.67
- Engagement: 40% high, 60% standard
- All capture behaviors represented

### Performance Baselines

From synthetic user framework:
- **Upload time**: <2 min for 45-min video
- **Query response**: <10s for complex queries
- **First session time**: 13-15 min average
- **Extraction accuracy**: >85% (user approval rate)

### Success Criteria

From beta testing plan:
- ✅ Extraction accuracy >85%
- ✅ Query satisfaction >85% "helpful"
- ✅ Review efficiency: >60% of flagged items reviewed
- ✅ Retention: >75% complete all 6 weeks
- ✅ NPS >0 (more promoters than detractors)

## Alternatives Considered

### Alternative 1: Generic Playwright Tests

**Approach:** Standard Playwright tests without persona modeling

**Rejected because:**
- Doesn't test behavioral diversity
- Misses edge cases (low tech comfort, skeptical users)
- No validation against real user patterns
- Can't simulate beta test cohort
- All tests act the same way (unrealistic)

### Alternative 2: Manual Test Case Creation

**Approach:** Manually write test scenarios for each persona

**Rejected because:**
- Time-consuming (months of work)
- Incomplete coverage (easy to miss edge cases)
- No statistical validation
- Hard to maintain as personas evolve
- Doesn't leverage synthetic data investment

### Alternative 3: Record-and-Replay Tools

**Approach:** Use tools like Selenium IDE to record user sessions

**Rejected because:**
- Requires real users (chicken-and-egg problem for new features)
- No persona diversity in recordings
- Brittle tests that break with UI changes
- Can't model behavioral patterns
- No edge case coverage

### Alternative 4: Property-Based Testing

**Approach:** Generate random test inputs with QuickCheck-style tools

**Rejected because:**
- Random inputs don't represent real user distributions
- No behavioral modeling
- Hard to validate against expected patterns
- Doesn't align with persona-driven product development

## Related Decisions

- [ADR-0001: Multi-Domain Architecture](0001-multi-domain-architecture-refactor.md) - Enabled domain-agnostic testing
- [ADR-0004: Synthetic User Framework](0004-synthetic-user-framework-integration.md) - Provided test data and personas
- Future: ADR on load testing using persona distributions

## References

- [E2E Test Scenarios](../../src/tests/e2e/E2E_TEST_SCENARIOS.md)
- [E2E Framework README](../../src/tests/e2e/README.md)
- [Synthetic User Framework](0004-synthetic-user-framework-integration.md)
- [Beta Testing Plan](/Users/stephenszermer/Dev/PrivateLanguage/docs/development/beta-testing/BETA_TESTING_PLAN.md)
- [Playwright Documentation](https://playwright.dev/)

## Future Enhancements

### Short-term
- Implement QueryPage and ReviewPage objects
- Add multi-session journey tests
- Create mock upload files (videos, documents)
- CI/CD integration

### Medium-term
- Load testing with realistic persona distributions
- Performance benchmarking against baselines
- Coverage reporting by persona type
- Visual regression testing

### Long-term
- AI-powered test generation from user stories
- Automatic test maintenance as personas evolve
- Cross-platform testing (mobile, tablet)
- Accessibility testing for all personas

---

**Last Updated:** 2025-10-07
**Maintainer:** Stephen Szermer
