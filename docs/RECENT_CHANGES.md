# Recent Changes

## Version 2.4.0 - Real LLM Integration (2025-10-15)

### 🤖 Authentic Persona-Specific Response Generation

**Real LLM Integration** ([ADR-0007](architecture/decisions/0007-real-llm-integration.md))
- Integrated Anthropic Claude Sonnet 4.5 for generating authentic persona-specific responses
- Replaces simulated template responses with natural language generation
- References specific persona attributes (craft medium, experience level, tech comfort, AI attitude)
- Contextual awareness of journey phase and emotional state
- Research-grade quality suitable for validation studies and beta test simulation

### 🎯 Problem Solved

**Limitations of Simulated Responses:**
- Generic and repetitive (same templates across all users)
- Lack context awareness (don't reference specific persona attributes)
- Limited variation (only 3 engagement levels: high/medium/low)
- Miss subtle nuances in voice and tone
- No learning or improvement over time

**Real LLM Solution:**
- Authentic persona voices with natural language variation
- Contextual awareness of user attributes, journey phase, emotional state
- Full 1-5 scale utilization in responses
- Nuanced communication patterns matching persona characteristics
- Production-quality responses suitable for research validation

### 📊 Core Features

**LLMResponseGenerator** (`core/generators/llm_response_generator.py`, 180 lines)
- Anthropic Claude Sonnet 4.5 API integration (model: `claude-sonnet-4-5-20250929`)
- Persona context injection (age, tech_comfort, ai_attitude, craft medium, years_in_craft)
- Scale-specific prompting (engagement, satisfaction, progress, relevance)
- Emotional state awareness in prompt engineering
- Temperature control (0.8) for natural variation
- 200-token response limit for cost optimization
- Graceful error handling with automatic fallback to simulated responses

**Journey Generator Integration**
- Added `use_real_llm` and `llm_model` parameters to `JourneyGenerator`
- Optional feature - defaults to simulated responses (backward compatible)
- Seamless integration with SSR pipeline
- Real LLM responses automatically converted to probability distributions
- Fallback to simulated on API error (no data loss)

**Cost Management**
- Cost estimation tool (`estimate_llm_costs.py`)
- Clear per-call pricing (~$0.002 per API call, ~$0.12 per journey)
- Batch size recommendations with cost breakdowns
- Hybrid approach support (mix real LLM + simulated)
- Environment variable security (.env for API keys)

### 🎨 Example Comparison

**Simulated Response:**
> "This seems useful. I'll keep going for now."

**Real LLM (Claude Sonnet 4.5):**
> "I'm intrigued by the knowledge sovereignty angle—I've definitely felt like my creative process gets lost in platforms that don't really *get* performance work. But I need to understand better how this actually helps me document and develop my pieces in a way that's more useful than what I'm already cobbling together with video files and scattered notes."

### 💰 Cost Information

**Pricing (Claude Sonnet 4.5):**
- Single API call: ~$0.002 (~0.2¢)
- Single journey (14 steps × 4 scales): ~$0.12 (12¢)
- 10-user cohort: ~$1.20
- 100-user cohort: ~$12
- 500-user cohort: ~$60

**Recommended Hybrid Approach:**
```
5 real LLM users: $0.60
495 simulated users: $0.00
Total for 500-user cohort: $0.60
```

### 🔧 Technical Implementation

**Files Created**
- `core/generators/llm_response_generator.py` (180 lines)
- `test_single_llm_call.py` - Single API call validation
- `test_focused_llm.py` - 2 journey steps test (~$0.02)
- `test_one_journey.py` - Full journey test (~$0.12)
- `generate_llm_cohort.py` - Batch generation script
- `generate_two_users_llm.py` - 2-user test script
- `quick_llm_test.py` - Rapid validation (2 API calls, ~10 seconds)
- `estimate_llm_costs.py` - Cost calculator tool
- `.env` - API key storage (gitignored)

**Files Modified**
- `core/generators/journey_generator.py` - Added LLM integration with fallback
- `requirements.txt` - Added `anthropic>=0.64.0`
- `.gitignore` - Confirmed .env protection

### 🎓 Usage Examples

**Basic Usage:**
```python
from core.generators.llm_response_generator import LLMResponseGenerator

# Initialize with Claude Sonnet 4.5
llm_gen = LLMResponseGenerator(model="claude-sonnet-4-5-20250929")

# Generate persona-specific response
response = llm_gen.generate_response(
    persona={
        "age": 46,
        "tech_comfort": 0.49,
        "medium": "ceramics",
        "years_in_craft": 15,
        "ai_attitude": "cautious"
    },
    stimulus="Starting your knowledge capture session",
    scale_id="engagement",
    phase="discovery",
    emotional_state="curious_cautious",
    engagement_score=0.65
)
```

**Journey Integration:**
```python
from core.generators.journey_generator import JourneyGenerator

generator = JourneyGenerator(
    journey_type=JourneyType.SESSION_BASED,
    phases_config=phases,
    emotional_states=emotions,
    ssr_config_path="projects/private_language/response_scales.yaml",
    enable_ssr=True,
    use_real_llm=True,  # Enable real LLM
    llm_model="claude-sonnet-4-5-20250929"
)

journey = generator.generate(persona, user_id)

# Each step includes authentic LLM responses + SSR distributions
for step in journey.steps:
    if hasattr(step, 'ssr_responses'):
        print(step.ssr_responses['engagement']['text_response'])
        print(step.ssr_responses['engagement']['expected_value'])
```

**Cost Estimation:**
```bash
PYTHONPATH=. python estimate_llm_costs.py

# Output shows costs for different batch sizes
# Single journey: $0.12
# 10 journeys: $1.20
# 100 journeys: $12.00
```

### ✨ Key Advantages

- ✅ **Authentic Persona Voices** - References specific attributes (craft medium, experience)
- ✅ **Natural Language Variation** - No two responses identical
- ✅ **Contextual Awareness** - Adapts to journey phase and emotional state
- ✅ **Research-Grade Quality** - Suitable for validation studies
- ✅ **Seamless SSR Integration** - Works perfectly with probability distributions
- ✅ **Backward Compatible** - Optional feature, existing code unchanged
- ✅ **Cost Transparent** - Clear estimation before generation
- ✅ **Graceful Fallback** - Automatic simulated responses on API error
- ✅ **Production Ready** - Error handling, security, comprehensive testing

### 🧪 Test Scripts

**Quick Validation (2 API calls, ~10 seconds, $0.004):**
```bash
PYTHONPATH=. python quick_llm_test.py
```

**Focused Test (2 journey steps, 8 API calls, ~30 seconds, $0.02):**
```bash
PYTHONPATH=. python test_focused_llm.py
```

**Full Journey (56 API calls, ~2 minutes, $0.12):**
```bash
PYTHONPATH=. python test_one_journey.py
```

**Batch Generation (full cohort):**
```bash
PYTHONPATH=. python generate_llm_cohort.py
```

### 🚀 Future Enhancements (Phase 2)

Documented in ADR-0007:
- [ ] Prompt caching (90% cost reduction for repeated system prompts)
- [ ] Parallel API calls (4x faster generation)
- [ ] Multi-provider support (OpenAI GPT-4, local LLM)
- [ ] Response caching for common persona/stimulus combinations
- [ ] Streaming responses for better UX
- [ ] Budget controls and limits

### 📚 Documentation

**New ADR**
- ADR-0007: Real LLM Integration
- Complete design rationale with 400+ lines
- Implementation details and code examples
- Alternatives considered (OpenAI, local LLM, fine-tuning)
- Cost analysis and optimization strategies
- Future enhancements roadmap
- Cross-references to ADRs 0004-0006

**Updated Files**
- README.md with Real LLM Integration section
- TODO.md with v2.4 completed items and future enhancements
- DECISION_REGISTRY.md with ADR-0007
- C4_ARCHITECTURE.md with LLM integration layer
- This file (RECENT_CHANGES.md)

### 🔗 References

- ADR: [ADR-0007](architecture/decisions/0007-real-llm-integration.md)
- Implementation: `core/generators/llm_response_generator.py`
- Cost Tool: `estimate_llm_costs.py`
- Test Scripts: `quick_llm_test.py`, `test_focused_llm.py`, `test_one_journey.py`
- Anthropic API: https://docs.anthropic.com/
- Claude Sonnet 4.5: Model ID `claude-sonnet-4-5-20250929`

---

## Version 2.3.0 - Semantic Similarity Rating (SSR) Integration (2025-10-15)

### 🎯 Research-Validated Response Generation

**Semantic Similarity Rating (SSR)** ([ADR-0006](architecture/decisions/0006-semantic-similarity-rating-integration.md))
- Integrated PyMC Labs SSR methodology for realistic Likert-scale response distributions
- Converts free-text LLM responses to probability distributions using semantic similarity
- 90% test-retest reliability vs human data (research-validated)
- KS similarity > 0.85 with real human response distributions
- Solves narrow-distribution problem of direct numerical elicitation

### 📊 Core Features

**SSRResponseGenerator** (`core/generators/ssr_response_generator.py`, 393 lines)
- YAML-driven reference scale loading
- Text-to-PMF conversion using sentence-transformers embeddings
- Journey response generation across multiple touchpoints
- Survey aggregation for cohort-level statistics
- Temperature control for distribution sharpness (0.5-2.0)
- Expected value, most likely rating, and full PMF output

**8 Pre-Defined Reference Scales** (`projects/private_language/response_scales.yaml`, 147 lines)
- `engagement` - Content engagement levels
- `satisfaction` - Experience satisfaction
- `difficulty` - Perceived difficulty
- `progress` - Learning progress perception
- `relevance` - Goal relevance
- `completion` - Completion likelihood
- `confidence` - Application confidence
- `interest` - Continuation interest

**Optional Journey Integration**
- Added `ssr_config_path` and `enable_ssr` parameters to `JourneyGenerator`
- Each journey step can include SSR responses across multiple scales
- Simulated LLM response templates based on engagement level
- Ready integration point for real LLM API calls (OpenAI/Anthropic)

### 🔧 Technical Implementation

**Files Created**
- `core/generators/ssr_response_generator.py` (393 lines)
- `projects/private_language/response_scales.yaml` (147 lines)
- `example_ssr_generation.py` (320 lines)

**Files Modified**
- `core/generators/journey_generator.py` - Optional SSR support
- `requirements.txt` - Added SSR dependencies

**Dependencies Added**
```
polars>=0.20.0
sentence-transformers>=2.2.0
semantic-similarity-rating @ git+https://github.com/pymc-labs/semantic-similarity-rating.git
```

### 📚 Comprehensive Example Script

**`example_ssr_generation.py` - 6 Usage Examples**
1. Single persona response generation
2. Different personas producing different distributions
3. Learning journey with multiple touchpoints
4. Survey aggregation statistics
5. Multiple scale usage (engagement, satisfaction, relevance)
6. Temperature effects on distribution sharpness

Run with:
```bash
PYTHONPATH=. python example_ssr_generation.py
```

### 🎨 Usage Example

```python
from core.generators.ssr_response_generator import SSRResponseGenerator

# Initialize with reference scales
generator = SSRResponseGenerator(
    reference_config_path="projects/private_language/response_scales.yaml"
)

# Generate response PMF from text
persona = {"age": 25, "level": "beginner"}
response = generator.generate_persona_response(
    persona_config=persona,
    stimulus="Complete this 15-minute lesson",
    scale_id="engagement",
    llm_response="This looks interesting! I want to try it."
)

# Output: Expected: 4.2/5, PMF: [0.05, 0.10, 0.20, 0.35, 0.30]
```

### 🔬 Research Foundation

Based on "LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings" (Maier et al., 2025, arXiv:2510.08338v2):

- **Problem**: Direct numerical elicitation produces unrealistic narrow distributions (KS ~0.26-0.39)
- **Solution**: SSR method achieves KS > 0.85 with full scale utilization
- **Validation**: Tested on 57 surveys with 9,300 human responses
- **Reliability**: 90% of human test-retest reliability

### ✨ Key Advantages

- ✅ **Realistic Distributions** - No more unrealistic peaks at rating 3
- ✅ **Full Scale Utilization** - Uses entire 1-5 range naturally
- ✅ **Rich Qualitative Data** - Free-text explanations for every rating
- ✅ **Backward Compatible** - Entirely optional feature
- ✅ **Domain Agnostic** - Works with any project via YAML scales
- ✅ **Production Ready** - Clear integration point for real LLM calls

### 📈 Response Characteristics

**Without SSR** (Direct Elicitation):
- Narrow distributions centered at 3
- Rarely uses 1 or 5
- KS similarity: 0.26-0.39

**With SSR**:
- Full scale utilization (1-5)
- Realistic distribution spreads
- KS similarity: > 0.85
- Probability distributions instead of point estimates

### 🚀 Future Enhancements (Phase 2)

- [ ] Real LLM integration (replace simulated responses with API calls)
- [ ] Dynamic scale generation from descriptions
- [ ] Batch embedding computation for performance
- [ ] Distribution comparison visualizations
- [ ] Cohort segmentation by response patterns
- [ ] Cost tracking and optimization for LLM calls
- [ ] Caching for repeated stimuli

### 📚 Documentation

**New ADR**
- ADR-0006: Semantic Similarity Rating Integration
- Complete design rationale and alternatives considered
- Implementation details and usage examples
- Cross-references to ADRs 0001-0005

**Updated Files**
- README.md with SSR section and usage examples
- TODO.md with v2.3 completed items
- DECISION_REGISTRY.md with ADR-0006
- This file (RECENT_CHANGES.md)

### 🔗 References

- Research Paper: `docs/2510.08338v2.pdf`
- PyMC Labs Implementation: https://github.com/pymc-labs/semantic-similarity-rating
- Example Script: `example_ssr_generation.py`
- ADR: [ADR-0006](architecture/decisions/0006-semantic-similarity-rating-integration.md)

---

## Version 2.2.0 - Persona-Based E2E Testing Framework (2025-10-07)

### 🧪 E2E Testing Integration

**Framework Overview** ([ADR-0005](architecture/decisions/0005-e2e-testing-framework-persona-based.md))
- Persona-based E2E testing using 500-user synthetic cohort
- Playwright tests that adapt to user attributes (tech comfort, AI attitude, engagement tier)
- 50+ test scenarios across all 10 persona types
- Beta test simulation with 5 ceramicists matching screening criteria

**Test Scenario Catalog**
- Created `E2E_TEST_SCENARIOS.md` with comprehensive test catalog (1,200 lines)
- Priority organization (P0: Critical path, P1: Institutional/adoption, P2/P3: Edge cases)
- Mapped to Private Language user stories (US001-US025)
- Coverage matrix:
  - Master Educator (30%): 5 scenarios
  - Studio Practitioner (20%): 6 scenarios
  - Department Head (15%): 3 scenarios
  - Early Adopter (10%): 3 scenarios
  - Skeptical Veteran + Edge Cases (25%): 15+ scenarios

**Beta Test Simulation**
- Generated beta cohort: 5 ceramicists from 500-user dataset
- Screening criteria applied:
  - Medium: ceramics_pottery ✓
  - Tech comfort: 0.4-0.7 (moderate) ✓
  - Craft experience: 3+ years (avg 12.0 years) ✓
  - Teaching experience: workshops/classes ✓
  - Engagement: standard or high ✓
- `generate_beta_test_cohort.py` - Automated cohort selector (210 lines)
- `output/beta_test_cohort.json` - 5 realistic beta testers

**Persona-Aware Page Objects**
- `BasePage` (350 lines): Behavioral adaptation engine
  - Typing speed: 30-120ms/char based on tech_comfort
  - Reading delays: 2-5s based on age and AI attitude
  - Hesitation patterns: Low tech users hover before clicking
  - Dropout simulation: 15% risk for low engagement users
- `UploadPage` (250 lines): Upload/capture workflows
  - `firstCaptureSession()` - Beta test scenario
  - `previewExtraction()` - High engagement users only
  - `handleUploadError()` - Error recovery flows
- Behavioral adaptations by persona:
  - Low tech comfort (< 0.4): 120ms/char typing, 1s hesitation, re-reads fields
  - High tech comfort (> 0.8): 30ms/char typing, fast navigation
  - Skeptical AI attitude: 5s reading privacy, hesitation before upload
  - Age > 60: 1.3x slower reading

**Test Fixtures**
- `personas.fixture.ts` (180 lines): Loads from synthetic cohort
- Preset personas: earlyAdopter, skepticalVeteran, masterEducator, betaTester
- Custom criteria filtering: `getPersonaBy({ techComfort, aiAttitude, engagementTier })`
- Extends Playwright test with persona fixtures

**Playwright Tests**
- `first-capture.spec.ts` (240 lines): 12 test scenarios
  - T-SP-001: Ceramicist first session (multi-modal capture)
  - T-SP-002: Low tech comfort error recovery
  - T-ME-001: Master educator curriculum upload
  - Engagement tier variations (high, standard, low)
  - Capture behavior patterns (systematic, crisis-driven)
  - Beta tester simulations (5 scenarios)

**Performance Baselines**
From synthetic user data:
- Upload time: <2 min for 45-min video
- Query response: <10s for complex queries
- First session time: 13-15 min average
- Extraction accuracy: >85% (measured by approval rate)

**Success Criteria** (From Beta Testing Plan)
- ✅ Extraction accuracy >85%
- ✅ Query satisfaction >85% "helpful"
- ✅ Review efficiency: >60% of flagged items reviewed
- ✅ Retention: >75% complete all 6 weeks
- ✅ NPS >0 (more promoters than detractors)

### 📚 Documentation

**E2E Framework Documentation**
- `src/tests/e2e/README.md` (650 lines): Comprehensive framework guide
  - Architecture overview
  - Test data sources (500-user cohort, beta cohort)
  - Persona-aware testing details
  - Fixtures usage examples
  - Page object patterns
  - Running tests guide
  - Metrics & validation
  - User story mapping
  - Best practices
  - Troubleshooting

**New ADR**
- ADR-0005: Persona-Based E2E Testing Framework
- Documents test scenario catalog, beta simulation, persona-aware behaviors
- Implementation details (7 files, 3,080 lines)
- Consequences: Comprehensive coverage vs increased complexity
- Alternatives considered: Generic tests, manual test cases, record-and-replay

**Updated Files**
- Decision Registry with ADR-0005
- README with E2E Testing Framework section
- TODO.md with completed E2E items

### 🔧 Technical Changes

**Files Created**
- `src/tests/e2e/E2E_TEST_SCENARIOS.md` (1,200 lines)
- `src/tests/e2e/README.md` (650 lines)
- `src/tests/e2e/page-objects/base.page.ts` (350 lines)
- `src/tests/e2e/page-objects/upload.page.ts` (250 lines)
- `src/tests/e2e/fixtures/personas.fixture.ts` (180 lines)
- `src/tests/e2e/tests/first-capture.spec.ts` (240 lines)
- `generate_beta_test_cohort.py` (210 lines)

**Total:** 7 files, 3,080 lines

### 📊 Results

- **Coverage**: 50+ test scenarios across all 10 persona types
- **Beta Cohort**: 5 ceramicists with perfect criteria match
- **Realism**: Tests adapt to tech comfort, AI attitude, engagement tier
- **Validation**: Beta test plan scenarios validated before real users
- **Integration**: Seamless use of 500-user synthetic cohort for test data

---

## Version 2.1.0 - Synthetic User Framework Integration (2025-10-07)

### 🎯 Framework Enhancements

**Aligned with Synthetic User Generation Framework**
- Integrated comprehensive framework from Private Language research
- 500-user target distribution validated with perfect accuracy
- Statistical realism through correlation matrices and behavioral modeling

**Expanded Persona Set** ([ADR-0004](architecture/decisions/0004-synthetic-user-framework-integration.md))
- Added 3 new core personas:
  - Early Adopter (10%) - Innovation champions driving word-of-mouth
  - Skeptical Veteran (5%) - AI resistance and adoption barriers
  - Department Head expanded to 15% (was 3%) - Key decision makers
- Added 5 edge case personas (20% total):
  - Cross-Domain Practitioner (6%)
  - International User (5%)
  - Industry Trainer (4%)
  - Graduate Student (3%)
  - Outlier/Stress Case (2%)

**Correlation Matrices**
- Age → Tech Comfort (-0.3 correlation): Older users less comfortable with tech
- Tech Comfort → AI Attitude (0.7 correlation): Higher comfort = more positive attitude
- Age → Years Experience (0.85 correlation): Strong positive relationship
- Automatic correlation application in persona generation

**Engagement Stratification**
- Within-persona variation: 20% high, 60% standard, 20% low
- Affects journey generation:
  - High: 15-25 sessions, +20% completion boost
  - Standard: 10-20 sessions, normal patterns
  - Low: 5-12 sessions, -20% completion, higher dropout

**Knowledge Capture Behaviors**
- Systematic (25%): Regular 2-7 day intervals
- Opportunistic (35%): Variable 1-14 day intervals
- Crisis-Driven (25%): Burst patterns (1-3 days then 10-30 day gaps)
- Experimental (15%): Very irregular 1-21 day intervals
- Affects session timing in journey generation

**Persona-Specific Distributions**
- Extended YAML schema with `*_distribution` pattern
- Master Educators: Career stage distributions (60% late-career, 30% mid-late, 10% exceptional)
- Studio Practitioners: Medium distributions (ceramics, visual arts, textile, woodworking, etc.)
- Department Heads: Sector and concern distributions

### 🧪 Validation

**Generated and Validated 500-User Cohort**
- Perfect persona distribution accuracy (all within 0.0%)
- Engagement stratification within 2% of targets
- Capture behaviors within 4% of targets
- Journey patterns validated:
  - High engagement: avg 20.2 sessions (15-25 range) ✓
  - Standard: avg 15.1 sessions (10-20 range) ✓
  - Low: avg 8.0 sessions (5-12 range) ✓

**New Analysis Tool**
- `analyze_framework_validation.py` - Comprehensive validation of distributions and correlations
- Validates personas, engagement, behaviors, correlations, and journey patterns
- 8-section validation report with statistical analysis

### 📚 Documentation

**New ADR**
- ADR-0004: Synthetic User Generation Framework Integration
- Documents correlation matrices, engagement stratification, capture behaviors
- Validation results and alternatives considered

**Updated Files**
- Decision Registry with ADR-0004
- personas.yaml expanded to 10 personas with detailed distributions
- PersonaGenerator and JourneyGenerator enhanced

### 🔧 Technical Changes

**Core Generators Enhanced**
- `PersonaGenerator`:
  - Correlation matrices with `_apply_correlation()` method
  - Engagement tier assignment
  - Knowledge capture behavior assignment
  - Weighted distribution support for persona attributes
  - Tech Comfort → AI Attitude bias logic

- `JourneyGenerator`:
  - Engagement-tier-aware session generation
  - Capture-behavior-based timing patterns
  - Dropout logic based on engagement tier
  - Systematic, opportunistic, crisis-driven, experimental patterns

### 📊 Results

- **Realism**: Age-tech comfort correlation measured at -0.607 (stronger than -0.3 target)
- **Accuracy**: Master Educator career stages 62.7% late-career (vs 60% target)
- **Diversity**: 10 persona types covering full adoption curve and edge cases
- **Scale**: Successfully generated and validated 500-user cohort

---

## Version 2.0.0 - Multi-Domain Refactor (2025-10-07)

### 🔴 Breaking Changes

**Architecture Overhaul**
- Refactored from single-purpose (Stage Zero Health) to multi-domain framework
- Moved domain logic from code to YAML configuration files
- Stage Zero code archived to `archive/stage_zero/`
- New project structure: `projects/{project_name}/`

**Migration Required**
- Existing Stage Zero users need to create new project configs
- Original functionality preserved in archive
- Follow migration guide in ADR-0001

### ✨ New Features

**Multi-Domain Support** ([ADR-0001](architecture/decisions/0001-multi-domain-architecture-refactor.md))
- Domain-agnostic core engine
- YAML-based project configuration system
- Support for unlimited domains via config files
- First new project: Private Language (knowledge sovereignty platform)

**Journey Type Flexibility** ([ADR-0003](architecture/decisions/0003-session-based-journey-modeling.md))
- Time-Based: Fixed intervals (e.g., weekly check-ins)
- Session-Based: Variable capture sessions (e.g., knowledge logging)
- Milestone-Based: Achievement-triggered progression

**CLI Interface**
```bash
python cli.py generate <project> --count N
python cli.py validate <project>
python cli.py list-projects
```

**Project Templates**
- Complete Private Language project config
- 7 detailed personas with distributions
- 4-phase session-based journey
- Emotional state progressions
- Narrative response patterns

**Analysis Tools**
- `analyze_scenarios.py` - Analyze user cohorts
- `generate_persona_scenarios.py` - Create user stories
- `example_generate.py` - Programmatic usage reference

### 🏗️ Architecture Changes

**New Structure**
```
synth/
├── core/                    # Domain-agnostic engine
│   ├── models/             # Persona, Journey, UserProfile
│   ├── generators/         # Core generation logic
│   └── utils/              # ConfigLoader, helpers
├── projects/               # Project configurations
│   └── private_language/  # Example project
├── archive/stage_zero/    # Original implementation
└── docs/                  # Documentation & ADRs
```

**Core Components**
- `PersonaGenerator`: Generate persona instances from configs
- `JourneyGenerator`: Create user journeys with phases/steps
- `NarrativeGenerator`: Generate persona-specific responses
- `ConfigLoader`: YAML configuration parser

**Data Models**
- `Persona`: User archetype with behavioral traits
- `Journey`: User progression through phases
- `JourneyStep`: Individual session/week in journey
- `UserProfile`: Complete user with persona + journey

### 📚 Documentation

**New ADRs**
- ADR-0001: Multi-Domain Architecture Refactor
- ADR-0002: YAML Configuration Schema
- ADR-0003: Session-Based Journey Modeling

**Updated Docs**
- Complete README rewrite
- Architecture decision registry
- Project creation guide
- Configuration schema reference

### 🧪 Testing

**Private Language Validation**
- Generated 100-user test cohort
- Validated persona distributions (perfect match)
- Tested session-based journey generation
- Analyzed first capture session patterns
- Created realistic user scenarios

**Test Results**
- ✅ Persona distribution: Exact match to configuration
- ✅ Journey generation: 5-20 sessions with variable intervals
- ✅ Emotional progression: Phase-appropriate states
- ✅ Time investment: 13-15 min average (realistic)

### 🛠️ Technical Details

**Dependencies**
- Added: `pyyaml>=6.0.0` for configuration parsing
- Retained: `faker`, `pandas`, `numpy` for data generation
- Dev: `pytest`, `black`, `isort`, `mypy`

**Removed**
- Stage Zero-specific generators (10 files)
- Hardcoded persona configurations
- Healthcare domain models
- Time-based-only journey logic

**File Changes**
```
73 files changed
4,119 insertions(+)
84,166 deletions(-)
```

### 🔗 Related Projects

**Private Language Integration**
- First multi-domain project using Synth
- Knowledge sovereignty platform for craft expertise
- 7 personas mapped from user research
- Session-based knowledge capture journeys
- Realistic first-session scenarios generated

## Migration Guide

### From v1.x (Stage Zero) to v2.0

**Option 1: Use Archived Code**
Original Stage Zero code preserved in `archive/stage_zero/`
```bash
python archive/stage_zero/stage_zero_generator.py
```

**Option 2: Create New Config**
1. Create `projects/stage_zero/` directory
2. Copy YAML templates from `projects/private_language/`
3. Adapt personas to healthcare domain
4. Use time-based journey type
5. Run `python cli.py generate stage_zero --count 500`

**Option 3: Continue with Archive**
No migration needed - archived version still functional

### Breaking Changes Checklist

- [ ] Review ADR-0001 for architecture changes
- [ ] Decide: Archive or migrate?
- [ ] If migrating: Create project configs
- [ ] Update any automation scripts to use new CLI
- [ ] Test generation with new system

## Previous Versions

### Version 1.x - Stage Zero Health (2025-03 to 2025-06)

**Features**
- Healthcare-focused synthetic user generation
- 10-week conversation flow modeling
- 5 health awareness personas
- Journey phase validation framework
- Test execution framework

**Archived:** All v1.x code preserved in `archive/stage_zero/`

---

**For detailed architectural decisions, see:**
- [ADR-0001: Multi-Domain Architecture](architecture/decisions/0001-multi-domain-architecture-refactor.md)
- [Decision Registry](architecture/DECISION_REGISTRY.md)
- [C4 Architecture](architecture/C4_ARCHITECTURE.md)
