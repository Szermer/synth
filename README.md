# Synth - Multi-Domain Synthetic User Data Generator

**Generate realistic synthetic user data across different domains using persona archetypes and journey phase modeling.**

Synth is a flexible framework for creating synthetic user datasets based on configurable personas and user journeys. Originally built for healthcare applications, it now supports any domain through YAML-based project configurations.

## ✨ Features

- **Multi-Domain Support** - Configure different projects with domain-specific personas and journeys
- **Statistical Realism** - Correlation matrices model realistic attribute relationships (age ↔ tech comfort, etc.)
- **Engagement Stratification** - Within-persona variation (20% high, 60% standard, 20% low engagement)
- **Knowledge Capture Behaviors** - Realistic patterns (systematic, opportunistic, crisis-driven, experimental)
- **Persona-Driven Generation** - Create users based on 10 behavioral archetypes with precise distributions
- **Journey Phase Modeling** - Simulate user progression through discovery, onboarding, active use, and maturity
- **Emotional State Tracking** - Model emotional progression throughout user journeys
- **Narrative Generation** - Create realistic conversational responses based on persona characteristics
- **Flexible Journey Types** - Support for time-based, session-based, or milestone-based journeys
- **Semantic Similarity Rating (SSR)** - Research-validated methodology for generating realistic Likert-scale response distributions (optional)
- **Real LLM Integration** - Generate authentic persona-specific responses using Claude Sonnet 4.5 (optional)
- **YAML Configuration** - Human-readable, version-controllable project definitions
- **Validated Framework** - 500-user cohorts with perfect distribution accuracy

## 🏗️ Architecture

```
synth/
├── core/                       # Domain-agnostic engine
│   ├── models/                # Data models (Persona, Journey, UserProfile)
│   ├── generators/            # Generation engines
│   ├── validation/            # Validation framework
│   └── utils/                 # Config loaders and utilities
│
├── projects/                   # Project-specific configurations
│   └── private_language/      # Example: Knowledge sovereignty platform
│       ├── config.yaml        # Project metadata
│       ├── personas.yaml      # Persona definitions
│       ├── journey_phases.yaml # Journey structure
│       ├── emotional_states.yaml # Emotional progressions
│       ├── data_schema.yaml   # Data fields
│       └── narrative_patterns.yaml # Response styles
│
├── cli.py                     # Command-line interface
└── output/                    # Generated datasets
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Szermer/synth.git
cd synth

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install SSR dependencies for semantic similarity rating
# Note: Adds ~500MB embedding model on first run
pip install polars sentence-transformers
pip install git+https://github.com/pymc-labs/semantic-similarity-rating.git
```

### Generate Synthetic Users

```bash
# List available projects
python cli.py list-projects

# Generate 1000 users for Private Language
python cli.py generate private_language --count 1000

# Validate project configuration
python cli.py validate private_language
```

### Output

Generated data is saved to `output/<project_name>_synthetic_users.json`:

```json
{
  "id": "uuid",
  "persona_type": "studio_practitioner",
  "name": "Sarah Martinez",
  "age": 42,
  "gender": "female",
  "education": "bachelors",
  "attributes": {
    "expertise_domain": "ceramics",
    "years_in_craft": 15,
    "tech_comfort": 0.65
  },
  "journey": {
    "journey_type": "session_based",
    "phases": [...],
    "steps": [...],
    "overall_completion": 0.73
  }
}
```

## 🎯 Semantic Similarity Rating (SSR)

Synth optionally integrates the **Semantic Similarity Rating (SSR)** methodology for generating realistic Likert-scale response distributions. Unlike direct numerical elicitation (which produces unrealistic narrow peaks), SSR converts free-text LLM responses to probability distributions using semantic similarity.

### Why SSR?

Based on research from "LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings" (Maier et al., 2025):

- ✅ **90% test-retest reliability** (vs human data)
- ✅ **KS similarity > 0.85** with real human response distributions
- ✅ **Full scale utilization** - uses entire 1-5 range naturally
- ✅ **Rich qualitative feedback** - provides free-text explanations

### Quick Start

```python
from core.generators.ssr_response_generator import SSRResponseGenerator

# Initialize with reference scales
generator = SSRResponseGenerator(
    reference_config_path="projects/private_language/response_scales.yaml"
)

# Generate response PMF from text
persona = {"age": 25, "level": "beginner", "goal": "travel"}
response = generator.generate_persona_response(
    persona_config=persona,
    stimulus="Complete this 15-minute lesson",
    scale_id="engagement",
    llm_response="This looks interesting! I want to try it."
)

print(f"Expected engagement: {response['expected_value']:.2f}/5")
print(f"PMF: {response['pmf']}")  # Probability distribution [0.05, 0.10, 0.20, 0.35, 0.30]
```

### Available Scales

Synth includes 8 pre-defined scales for learning domains:
- `engagement` - Content engagement levels
- `satisfaction` - Experience satisfaction
- `difficulty` - Perceived difficulty
- `progress` - Learning progress perception
- `relevance` - Goal relevance
- `completion` - Completion likelihood
- `confidence` - Application confidence
- `interest` - Continuation interest

### Journey Integration

Enable SSR in journey generation:

```python
from core.generators.journey_generator import JourneyGenerator

generator = JourneyGenerator(
    journey_type=JourneyType.SESSION_BASED,
    phases_config=phases,
    emotional_states=emotions,
    ssr_config_path="projects/private_language/response_scales.yaml",
    enable_ssr=True  # Enable SSR responses
)

journey = generator.generate(persona, user_id)

# Access SSR responses in journey steps
for step in journey.steps:
    if hasattr(step, 'ssr_responses'):
        engagement = step.ssr_responses['engagement']
        print(f"Text: {engagement['text_response']}")
        print(f"PMF: {engagement['pmf']}")
        print(f"Expected: {engagement['expected_value']:.2f}/5")
```

### Example Script

Run the comprehensive example to see SSR in action:

```bash
PYTHONPATH=. python example_ssr_generation.py
```

This demonstrates:
- Single persona responses
- Different personas producing different distributions
- Journey progression across multiple touchpoints
- Survey aggregation statistics
- Multiple scale usage
- Temperature effects on distribution sharpness

### Documentation

- [ADR-0006: SSR Integration](docs/architecture/decisions/0006-semantic-similarity-rating-integration.md) - Complete design rationale
- [example_ssr_generation.py](example_ssr_generation.py) - 6 comprehensive usage examples
- [Research Paper](docs/2510.08338v2.pdf) - Original SSR methodology paper

## 🤖 Real LLM Integration

Synth optionally integrates **Anthropic Claude Sonnet 4.5** for generating authentic, persona-specific responses. Unlike simulated template responses, real LLM responses reference specific persona attributes, use natural language variation, and capture nuanced contextual awareness.

### Why Real LLM?

**Limitations of Simulated Responses:**
- Generic and repetitive (same templates across all users)
- Lack context awareness (don't reference persona attributes)
- Limited variation (only 3 engagement levels: high/medium/low)
- Miss subtle nuances in voice and tone

**Real LLM Benefits:**
- ✅ **Authentic persona voices** - References craft medium, experience level, tech comfort
- ✅ **Natural language variation** - No two responses identical
- ✅ **Contextual awareness** - Adapts to journey phase and emotional state
- ✅ **Research-grade quality** - Suitable for validation studies and beta test simulation

**Example Comparison:**

*Simulated:*
> "This seems useful. I'll keep going for now."

*Real LLM (Claude Sonnet 4.5):*
> "I'm intrigued by the knowledge sovereignty angle—I've definitely felt like my creative process gets lost in platforms that don't really *get* performance work. But I need to understand better how this actually helps me document and develop my pieces in a way that's more useful than what I'm already cobbling together with video files and scattered notes."

### Installation

```bash
# Install Anthropic SDK
pip install anthropic>=0.64.0

# Set up API key (create .env file)
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

**Get API Key:** Sign up at [console.anthropic.com](https://console.anthropic.com/)

### Quick Start

```python
from core.generators.llm_response_generator import LLMResponseGenerator

# Initialize generator
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

print(response)
# Output: "I'm curious about this, though I have to admit I'm a bit hesitant
# about AI being involved in documenting my ceramic work..."
```

### Journey Integration

Enable real LLM in journey generation (works seamlessly with SSR):

```python
from core.generators.journey_generator import JourneyGenerator

generator = JourneyGenerator(
    journey_type=JourneyType.SESSION_BASED,
    phases_config=phases,
    emotional_states=emotions,
    ssr_config_path="projects/private_language/response_scales.yaml",
    enable_ssr=True,
    use_real_llm=True,  # Enable real LLM responses
    llm_model="claude-sonnet-4-5-20250929"
)

journey = generator.generate(persona, user_id)

# Each step includes authentic LLM responses converted to SSR distributions
for step in journey.steps:
    if hasattr(step, 'ssr_responses'):
        engagement = step.ssr_responses['engagement']
        print(f"Response: {engagement['text_response']}")
        print(f"Expected Value: {engagement['expected_value']:.2f}/5")
        print(f"PMF: {engagement['pmf']}")
```

**Graceful Fallback:** If API fails, automatically falls back to simulated responses (no data loss).

### Cost Information

**Pricing (Claude Sonnet 4.5):**
- Single API call: ~$0.002 (~0.2¢)
- Single journey (14 steps × 4 scales): ~$0.12 (12¢)
- 10-user cohort: ~$1.20
- 100-user cohort: ~$12
- 500-user cohort: ~$60

**Cost Estimation Tool:**
```bash
PYTHONPATH=. python estimate_llm_costs.py

# Output shows estimated costs for different batch sizes
```

**Recommended Hybrid Approach:**
Generate 5-10 critical personas with real LLM, use simulated for the rest:
```
5 real LLM users: $0.60
495 simulated users: $0.00
Total for 500-user cohort: $0.60
```

### Example Scripts

**Quick Validation (2 API calls, ~10 seconds):**
```bash
PYTHONPATH=. python quick_llm_test.py
```

**Focused Test (2 journey steps, ~30 seconds):**
```bash
PYTHONPATH=. python test_focused_llm.py
```

**Full Journey (56 API calls, ~2 minutes):**
```bash
PYTHONPATH=. python test_one_journey.py
```

**Batch Generation (full cohort):**
```bash
PYTHONPATH=. python generate_llm_cohort.py
```

### Documentation

- [ADR-0007: Real LLM Integration](docs/architecture/decisions/0007-real-llm-integration.md) - Complete design rationale and implementation details
- [LLMResponseGenerator](core/generators/llm_response_generator.py) - Core implementation
- [Cost Estimation](estimate_llm_costs.py) - Cost calculator tool

## 📋 Creating a New Project

### 1. Create Project Directory

```bash
mkdir -p projects/your_project
```

### 2. Define Configuration Files

#### `config.yaml` - Project Metadata

```yaml
name: "Your Project"
description: "Description of your domain"
version: "1.0"
domain: "your_domain"

default_count: 1000
journey_type: "session_based"  # or "time_based" or "milestone_based"

journey:
  type: "session_based"
  phases:
    - discovery
    - onboarding
    - active_use
```

#### `personas.yaml` - Define Your Personas

```yaml
personas:
  persona_type_1:
    name: "Persona Name"
    description: "Who they are"
    distribution: 0.30  # 30% of users

    demographics:
      age_range: [25, 55]
      gender_distribution:
        female: 0.50
        male: 0.50
      education_distribution:
        bachelors: 0.60
        masters: 0.40

    behavioral:
      engagement_pattern: "cautious_gradual"
      action_tendency: [0.5, 0.7]
      anxiety_level: [0.3, 0.6]

    completion_thresholds:
      discovery: [0.6, 0.8]
      onboarding: [0.5, 0.7]
```

#### `journey_phases.yaml` - Define User Journey

```yaml
phases:
  - name: "discovery"
    order: 0
    description: "User discovers your product"
    objectives:
      - "understand_value_proposition"
      - "evaluate_fit"
    emotional_objectives:
      - "reduce_skepticism"
      - "build_curiosity"
    data_to_collect:
      - "discovery_source"
      - "primary_pain_point"
```

#### `emotional_states.yaml` - Define Emotional Progression

```yaml
emotional_progressions:
  persona_type_1:
    discovery:
      - "skeptical"
      - "curious"
    onboarding:
      - "learning"
      - "confident"
```

#### `narrative_patterns.yaml` - Define Response Styles

```yaml
patterns:
  persona_type_1:
    response_style: "cautious_practical"
    detail_level: "moderate"
    linguistic_markers:
      - "I think"
      - "maybe"
```

### 3. Generate Data

```bash
python cli.py validate your_project
python cli.py generate your_project --count 500
```

## 💡 Example Projects

### Private Language
A knowledge sovereignty platform for craft expertise preservation. Demonstrates:
- 10 distinct personas (Master Educator, Studio Practitioner, Department Head, Early Adopter, etc.)
- Session-based journey progression with engagement stratification
- Tacit knowledge capture and documentation patterns
- Legacy preservation motivations
- Comprehensive E2E testing framework with persona-based behaviors

## 🧪 E2E Testing Framework

Synth includes a persona-based E2E testing framework that uses the synthetic user data to drive realistic Playwright tests:

### Features
- **Persona-Aware Behaviors** - Tests adapt to user attributes (tech comfort, AI attitude, engagement tier)
- **50+ Test Scenarios** - Coverage across all 10 persona types including edge cases
- **Beta Test Simulation** - 5-person cohort matching real beta screening criteria
- **Realistic Timing** - Typing speed, hesitation, reading time based on persona
- **Dropout Testing** - Simulate realistic user dropout scenarios

### Quick Start

```bash
# Install Playwright
npm install -D @playwright/test

# Run E2E tests
npx playwright test

# Run beta test simulation
npx playwright test --grep "Beta Test"

# Run specific persona tests
npx playwright test --grep "Master Educator"
```

### Example Test

```typescript
import { test, expect } from './fixtures/personas.fixture';
import { UploadPage } from './page-objects/upload.page';

test('First capture session', async ({ page, betaTester }) => {
  // betaTester has realistic attributes: tech_comfort, engagement_tier, etc.
  const uploadPage = new UploadPage(page, betaTester);

  const result = await uploadPage.firstCaptureSession({
    medium: 'ceramics_pottery',
    sessionType: 'throwing',
    duration: 22
  });

  expect(result.success).toBe(true);
  expect(result.timeInvested).toBeGreaterThanOrEqual(13); // Matches synthetic data
});
```

### Documentation
- [E2E Test Scenarios](src/tests/e2e/E2E_TEST_SCENARIOS.md) - 50+ test scenarios
- [E2E Framework README](src/tests/e2e/README.md) - Complete guide
- [ADR-0005: E2E Testing Framework](docs/architecture/decisions/0005-e2e-testing-framework-persona-based.md)

## 🛠️ Development

### Project Structure

- **Core Engine** (`core/`) - Domain-agnostic generation logic
- **Models** (`core/models/`) - Data structures for personas, journeys, users
- **Generators** (`core/generators/`) - Persona, journey, and narrative generation
- **Utils** (`core/utils/`) - Configuration loading and helpers
- **Projects** (`projects/`) - Domain-specific configurations

### Architecture

- [C4 Architecture Diagram](docs/architecture/C4_ARCHITECTURE.md) - System architecture overview
- [Decision Registry](docs/architecture/DECISION_REGISTRY.md) - All architectural decisions
- [Architecture Decision Records](docs/architecture/decisions/) - Detailed ADRs
  - [ADR-0001: Multi-Domain Architecture Refactor](docs/architecture/decisions/0001-multi-domain-architecture-refactor.md)
  - [ADR-0002: YAML Configuration Schema](docs/architecture/decisions/0002-yaml-configuration-schema.md)
  - [ADR-0003: Session-Based Journey Modeling](docs/architecture/decisions/0003-session-based-journey-modeling.md)
  - [ADR-0004: Synthetic User Framework Integration](docs/architecture/decisions/0004-synthetic-user-framework-integration.md)
  - [ADR-0005: Persona-Based E2E Testing Framework](docs/architecture/decisions/0005-e2e-testing-framework-persona-based.md)
  - [ADR-0006: Semantic Similarity Rating Integration](docs/architecture/decisions/0006-semantic-similarity-rating-integration.md)
  - [ADR-0007: Real LLM Integration](docs/architecture/decisions/0007-real-llm-integration.md)

### Adding Features

The core engine is designed to be extended without modification. Add new capabilities by:
1. Extending YAML schemas in project configs
2. Adding custom attributes to persona configs
3. Defining new journey phases
4. Creating domain-specific narrative patterns

### Testing

**Unit Tests:**
```bash
# Run Python unit tests
PYTHONPATH=. pytest

# Run specific test
PYTHONPATH=. pytest src/tests/test_file.py::test_name
```

**E2E Tests:**
```bash
# Run Playwright E2E tests
npx playwright test

# Run beta test simulation
npx playwright test --grep "Beta Test"

# Debug mode
npx playwright test --debug
```

See [E2E Testing Framework](#-e2e-testing-framework) for details.

## 📚 Documentation

### Concepts
- **Personas** - Behavioral archetypes with demographic and psychological traits
- **Journey Phases** - Stages users progress through (discovery → mature use)
- **Journey Types**:
  - **Time-Based**: Weekly/daily progression (e.g., 10-week program)
  - **Session-Based**: Variable capture sessions (e.g., knowledge logging)
  - **Milestone-Based**: Achievement-triggered progression
- **Emotional States** - How user emotions evolve through journey
- **Narrative Patterns** - How personas communicate and respond

### Documentation
- [Recent Changes](docs/RECENT_CHANGES.md) - Version 2.0 migration guide
- [TODO](TODO.md) - Roadmap and planned features
- [Architecture](docs/architecture/) - System design and ADRs
- [Decision Registry](docs/architecture/DECISION_REGISTRY.md) - All architectural decisions

## 🗃️ Archive

Previous domain-specific implementations are archived in `archive/`:
- `stage_zero/` - Healthcare risk assessment synthetic users (10-week conversation flows)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Related Projects

- **Private Language** - Knowledge sovereignty platform ([/Szermer/PrivateLanguage](https://github.com/Szermer/PrivateLanguage))

---

**Version 2.0** - Multi-domain refactor | Originally built for Stage Zero Health
