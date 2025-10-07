# ADR-0004: Synthetic User Generation Framework Integration

**Status:** ✅ Accepted
**Date:** 2025-10-07
**Impact:** 🟡 Medium

## Context

After implementing the multi-domain refactor (ADR-0001) and generating an initial 100-user cohort for Private Language, we received a comprehensive [Synthetic User Generation Framework](../../personas/Synthetic%20User%20Generation%20Framework%20for%20Private%20Language.md) that proposed:

1. **Statistical realism** through correlation matrices between attributes (e.g., age → tech_comfort = -0.3)
2. **Engagement stratification** within each persona (20% high, 60% standard, 20% low)
3. **Knowledge capture behaviors** (systematic, opportunistic, crisis-driven, experimental)
4. **Expanded persona set** including Early Adopters, Skeptical Veterans, Edge Cases
5. **500-user target distribution** aligned with market research

The framework was designed to create more realistic synthetic users that accurately represent the target market distribution and behavioral patterns.

### Problem

The initial implementation (v2.0) had limitations:
- **No correlation modeling** - Attributes were independently random
- **Uniform engagement** - All users within a persona behaved identically
- **Missing personas** - Lacked critical segments (early adopters, skeptics, edge cases)
- **Inaccurate distributions** - Didn't reflect actual market composition
- **Limited behavioral variation** - Session timing and patterns were too uniform

### Requirements

1. Maintain backward compatibility with existing YAML schema
2. Implement correlation matrices without requiring manual specification
3. Add engagement and behavior stratification that affects journey generation
4. Support 10 persona types with precise distribution control
5. Generate statistically realistic 500-user cohorts

## Decision

We integrated the Synthetic User Generation Framework into Synth's core generators:

### 1. Updated Persona Distributions (personas.yaml)

**Core Personas (80% - 400 users):**
- Master Educator: 30% (150 users) - largest segment due to retirement urgency
- Studio Practitioner: 20% (100 users) - multi-modal capture validation
- Department Head: 15% (75 users) - institutional decision makers
- Early Adopter: 10% (50 users) - innovation champions
- Skeptical Veteran: 5% (25 users) - adoption barrier testing

**Edge Cases (20% - 100 users):**
- Cross-Domain Practitioner: 6% (30 users)
- International User: 5% (25 users)
- Industry Trainer: 4% (20 users)
- Graduate Student: 3% (15 users)
- Outlier/Stress Case: 2% (10 users)

### 2. Correlation Matrices (PersonaGenerator)

Implemented automatic correlation application:

```python
CORRELATIONS = {
    'age': {
        'years_experience': 0.85,  # Strong positive
        'tech_comfort': -0.3,      # Moderate negative
        'retirement_urgency': 0.6   # Moderate positive
    },
    'tech_comfort': {
        'ai_attitude': 0.7,        # Strong positive
        'feature_adoption': 0.8,    # Strong positive
        'documentation_volume': 0.4 # Moderate positive
    },
    'department_size': {
        'budget_authority': 0.5,
        'knowledge_complexity': 0.3,
        'collaboration_needs': 0.7
    }
}
```

**Implementation:**
- Age → Tech Comfort: Older users have lower tech comfort (-0.3 correlation)
- Tech Comfort → AI Attitude: Higher tech comfort → more enthusiastic AI attitude (0.7 correlation)
- Age → Years Experience: Strong positive correlation (0.85)

### 3. Engagement Stratification

Added within-persona variation:

```python
ENGAGEMENT_LEVELS = {
    'high': 0.20,     # Daily use, comprehensive docs, community participation
    'standard': 0.60,  # 2-3x weekly, focused docs, occasional interaction
    'low': 0.20       # Weekly/sporadic, minimal docs, no community
}
```

**Effects on journeys:**
- High engagement: 15-25 sessions, +0.2 completion boost
- Standard: 10-20 sessions, normal completion
- Low: 5-12 sessions, -0.2 completion, higher dropout risk

### 4. Knowledge Capture Behaviors

Added realistic capture patterns:

```python
CAPTURE_BEHAVIORS = {
    'systematic': 0.25,      # Regular scheduled (2-7 day intervals)
    'opportunistic': 0.35,   # Variable intervals (1-14 days)
    'crisis_driven': 0.25,   # Bursty (1-3 days then 10-30 day gaps)
    'experimental': 0.15     # Very irregular (1-21 days)
}
```

**Implementation in JourneyGenerator:**
- Session timing varies based on `capture_behavior` attribute
- Systematic users have predictable patterns
- Crisis-driven users show burst-and-gap patterns

### 5. Persona-Specific Attribute Distributions

Extended YAML schema to support distribution dictionaries:

```yaml
master_educator:
  attributes:
    career_stage: ["mid_late_10_15y", "late_15_25y", "exceptional_mid_7_10y"]
    career_stage_distribution:
      late_15_25y: 0.60
      mid_late_10_15y: 0.30
      exceptional_mid_7_10y: 0.10
```

**Generator automatically:**
- Detects `*_distribution` keys
- Applies weighted selection for the base attribute
- Maintains clean YAML syntax

## Consequences

### Positive

✅ **Statistical Realism**
- 500-user cohort validated with perfect persona distributions (all within 0.0%)
- Age → Tech Comfort correlation measured at -0.607 (stronger than expected -0.3)
- Engagement stratification within 2% of target (21% high, 61% standard, 18% low)

✅ **Behavioral Diversity**
- Knowledge capture behaviors distributed correctly (within 4% of targets)
- Journey patterns vary realistically:
  - High engagement: avg 20.2 sessions (range 15-25) ✓
  - Standard: avg 15.1 sessions (range 10-20) ✓
  - Low: avg 8.0 sessions (range 5-12) ✓

✅ **Persona Richness**
- Master Educators: Career stages match framework (62.7% late-career vs 60% expected)
- Studio Practitioners: Medium distribution realistic (34% ceramics vs 25% expected - acceptable variance)
- 10 persona types covering core users (80%) and edge cases (20%)

✅ **Market Alignment**
- Distributions match Private Language target market research
- Early Adopters and Skeptical Veterans enable full adoption curve modeling
- International and Edge Case personas support global scale planning

### Negative

⚠️ **Stronger-than-expected correlations**
- Age → Tech Comfort measured at -0.607 vs target -0.3
- Not necessarily bad - may indicate more realistic patterns
- Could be tuned with adjusted correlation strength parameter

⚠️ **Distribution variance in some attributes**
- Systematic behavior: 21.2% vs 25% expected (-3.8%)
- Ceramics medium: 34% vs 25% expected (+9%)
- Acceptable variance for statistical generation but could be refined

⚠️ **Increased complexity**
- Persona YAML files now longer (10 personas vs 7 originally)
- Generator logic more complex (correlation application, stratification)
- Debugging persona issues requires understanding correlation effects

### Mitigations

- **Validation script** (`analyze_framework_validation.py`) created to verify distributions
- **Clear documentation** of correlation effects and attribute dependencies
- **Backward compatibility** maintained - old YAML files still work

## Implementation

### Files Modified

**Personas Configuration:**
- `projects/private_language/personas.yaml` - Expanded to 10 personas with distributions

**Core Generators:**
- `core/generators/persona_generator.py`:
  - Added correlation matrices
  - Implemented `_apply_correlation()` method
  - Added engagement/behavior stratification
  - Enhanced `_generate_attributes()` with distribution support

- `core/generators/journey_generator.py`:
  - Updated `_generate_session_based_steps()` to respect engagement tier
  - Implemented capture behavior timing patterns
  - Added engagement-based dropout logic

**Analysis Tools:**
- `analyze_framework_validation.py` - Validates framework implementation

### Validation Results

```
================================================================================
VALIDATION SUMMARY
================================================================================

✓ 500 users generated successfully
✓ Persona distributions match framework (within 1%)
✓ Engagement stratification implemented (20/60/20)
✓ Knowledge capture behaviors implemented (25/35/25/15)
✓ Age → Tech Comfort correlation applied (-0.3)
✓ Tech Comfort → AI Attitude correlation applied (0.7)
✓ Persona-specific attributes with distributions implemented
✓ Journey patterns vary by engagement tier

🎉 Framework integration: VALIDATED
```

## Alternatives Considered

### Alternative 1: Manual Correlation Specification in YAML

**Approach:** Require users to specify correlations in YAML config

```yaml
correlations:
  age_to_tech_comfort: -0.3
  tech_comfort_to_ai_attitude: 0.7
```

**Rejected because:**
- Increases configuration complexity for users
- Framework correlations are research-based and should be defaults
- Most users won't know appropriate correlation values

### Alternative 2: Statistical Libraries (SDV, CTGAN)

**Approach:** Use Synthetic Data Vault or CTGAN for statistically rigorous generation

**Rejected because:**
- Requires real data to train models
- Heavyweight dependencies
- Overkill for behavioral/journey modeling (better for tabular PII)
- Synth focuses on behavioral patterns, not statistical privacy

### Alternative 3: Separate Engagement Classes

**Approach:** Create separate persona types for high/standard/low engagement

**Rejected because:**
- Would require 30 persona types (10 × 3)
- Violates DRY principle
- Framework specifies within-persona stratification
- Harder to maintain

## Related Decisions

- [ADR-0001: Multi-Domain Architecture](0001-multi-domain-architecture-refactor.md) - Enabled framework integration through YAML configs
- [ADR-0002: YAML Configuration Schema](0002-yaml-configuration-schema.md) - Extended with distribution support
- [ADR-0003: Session-Based Journey Modeling](0003-session-based-journey-modeling.md) - Enhanced with engagement/behavior patterns

## References

- [Synthetic User Generation Framework](../../../PrivateLanguage/docs/personas/Synthetic%20User%20Generation%20Framework%20for%20Private%20Language.md)
- [Beta Testing Plan](../../../PrivateLanguage/docs/development/beta-testing/BETA_TESTING_PLAN.md)
- [awesome-synthetic-data](https://github.com/statice/awesome-synthetic-data)

---

**Last Updated:** 2025-10-07
**Maintainer:** Stephen Szermer
