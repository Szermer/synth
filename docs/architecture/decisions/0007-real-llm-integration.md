# ADR-0007: Real LLM Integration for SSR Response Generation

**Status:** ✅ Accepted
**Date:** 2025-10-15
**Impact:** 🟢 High

## Context

After implementing the Semantic Similarity Rating (SSR) methodology (ADR-0006), we identified a limitation: **simulated LLM responses lack the authenticity and nuance of real persona-specific responses**.

### Problem

SSR converts free-text responses to probability distributions, but the quality of the output depends entirely on the quality of the input text. Our simulated responses used templates:

```python
# Simulated template example
if engagement_score > 0.7:
    response = "This is really interesting and relevant to my goals. I'm excited to continue."
```

**Limitations of Simulated Responses:**
1. **Generic and repetitive** - Same templates across all users
2. **Lack context awareness** - Don't reference specific persona attributes
3. **Miss subtle nuances** - Can't capture authentic voice/tone
4. **Limited variation** - Only 3 engagement levels (high/medium/low)
5. **No learning** - Templates don't improve over time

### Requirements

1. Generate authentic, persona-specific free-text responses
2. Maintain backward compatibility with simulated responses
3. Optional feature - users choose real LLM vs simulated
4. Cost-conscious design with clear cost estimation
5. Support multiple LLM providers (start with Anthropic)
6. Graceful fallback if API fails
7. Integration with existing SSR pipeline

## Decision

We integrated **Anthropic Claude Sonnet 4.5** as an optional LLM provider for generating authentic persona responses that feed into the SSR pipeline.

### 1. LLM Response Generator (`core/generators/llm_response_generator.py`)

**Purpose:** Generate persona-appropriate free-text responses using Claude API

**Key Features:**
- Persona context injection (age, tech_comfort, ai_attitude, craft experience)
- Scale-specific prompting (engagement, satisfaction, progress, relevance)
- Emotional state awareness
- Temperature control (0.8 for natural variation)
- 200-token response limit (cost optimization)

**Architecture:**
```python
class LLMResponseGenerator:
    def __init__(self, model="claude-sonnet-4-5-20250929", api_key=None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def generate_response(
        self,
        persona: Dict,
        stimulus: str,
        scale_id: str,
        phase: str,
        emotional_state: str,
        engagement_score: float
    ) -> str:
        """Generate authentic persona response via Claude API"""
        system_prompt = self._build_persona_context(persona, emotional_state, engagement_score)
        user_prompt = f"Stimulus: {stimulus}\nQuestion: {self._get_scale_prompt(scale_id)}"

        message = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            temperature=0.8,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        return message.content[0].text.strip()
```

### 2. Enhanced Journey Generator Integration

**Added Parameters:**
```python
JourneyGenerator(
    journey_type=...,
    phases_config=...,
    emotional_states=...,
    ssr_config_path=...,
    enable_ssr=True,
    use_real_llm=True,  # NEW: Enable real LLM
    llm_model="claude-sonnet-4-5-20250929"  # NEW: Model selection
)
```

**Modified `_generate_ssr_responses()` method:**
```python
def _generate_ssr_responses(self, persona, phase, emotional_state, engagement_score):
    for scale_id in ['engagement', 'satisfaction', 'progress', 'relevance']:
        # Real LLM or simulated fallback
        if self.use_real_llm and self.llm_generator:
            try:
                response_text = self.llm_generator.generate_response(
                    persona=persona.attributes,
                    stimulus=stimulus,
                    scale_id=scale_id,
                    phase=phase.name,
                    emotional_state=emotional_state,
                    engagement_score=engagement_score
                )
            except Exception as e:
                # Fallback to simulated
                response_text = self._simulate_llm_responses(...)[scale_id]
        else:
            response_text = self._simulate_llm_responses(...)[scale_id]

        # Convert to SSR distribution
        ssr_response = self.ssr_generator.generate_persona_response(...)
```

### 3. Environment Configuration

**`.env` file (gitignored):**
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

**`requirements.txt`:**
```python
anthropic>=0.64.0
```

### 4. Cost Estimation Tool

**`estimate_llm_costs.py`:**
- Analyzes journey lengths from existing data
- Calculates token usage per API call
- Estimates costs for different batch sizes
- Provides cost/benefit recommendations

**Typical Costs (Claude Sonnet 4.5):**
- Single API call: ~$0.0021 (~0.2¢)
- Journey (14 steps × 4 scales): ~$0.12 (12¢)
- 10-user cohort: ~$1.20
- 100-user cohort: ~$12
- 500-user cohort: ~$60

### 5. Test Scripts

**Created comprehensive test suite:**
- `test_single_llm_call.py` - Single API call test ($0.004)
- `test_focused_llm.py` - 2 journey steps test ($0.02)
- `test_one_journey.py` - Full journey test ($0.12)
- `generate_llm_cohort.py` - Batch generation
- `estimate_llm_costs.py` - Cost calculator
- `quick_llm_test.py` - Rapid validation

## Consequences

### Positive

✅ **Dramatic Quality Improvement**
- Authentic, persona-specific responses
- References specific attributes (craft medium, experience level)
- Natural language variation
- Contextual and nuanced

Example comparison:

**Simulated:**
> "This seems useful. I'll keep going for now."

**Real LLM (Claude Sonnet 4.5):**
> "I'm intrigued by the knowledge sovereignty angle—I've definitely felt like my creative process gets lost in platforms that don't really *get* performance work. But I need to understand better how this actually helps me document and develop my pieces in a way that's more useful than what I'm already cobbling together with video files and scattered notes."

✅ **Research-Grade Data Quality**
- Suitable for validation studies
- E2E testing with realistic user behavior
- Beta test simulation with authentic feedback
- User research with genuine persona voices

✅ **Flexible Architecture**
- Optional feature (backward compatible)
- Easy to toggle on/off per generation
- Graceful fallback to simulated
- Cost-transparent design

✅ **Production-Ready**
- Error handling and fallbacks
- API key security (environment variables)
- Clear cost estimation
- Comprehensive test coverage

✅ **Model Flexibility**
- Default: Claude Sonnet 4.5 (latest, most capable)
- Easy to swap models
- Can add other providers (OpenAI, etc.)

### Negative

⚠️ **API Costs**
- $0.12 per journey (~14 steps)
- $1.20 per 10 users
- $60 for 500-user cohort
- Mitigation: Clear cost estimation, optional feature, hybrid approach

⚠️ **Generation Speed**
- ~1-2 minutes per journey (vs instant simulated)
- Sequential API calls (could parallelize)
- Mitigation: Background generation, batch processing

⚠️ **External Dependency**
- Requires Anthropic API access
- Network connectivity needed
- API rate limits may apply
- Mitigation: Graceful fallback, retry logic, simulated as backup

⚠️ **API Key Management**
- Requires secure key storage
- Environment variable setup
- Cost monitoring needed
- Mitigation: `.env` gitignored, clear documentation

### Mitigations

**Hybrid Approach (Recommended):**
```
5 critical personas with real LLM: $0.60
495 simulated responses: $0.00
Total: $0.60 for 500-user cohort
```

**Cost Controls:**
- Cost estimation tool before generation
- Max tokens limit (200 per response)
- Optional per-user enablement
- Batch size recommendations

**Reliability:**
- Automatic fallback to simulated on API error
- Retry logic for transient failures
- Clear error messages
- No data loss if API unavailable

## Implementation

### Files Created

**Core Generator:**
- `core/generators/llm_response_generator.py` (180 lines)
  - `LLMResponseGenerator` class
  - Anthropic Claude API integration
  - Persona context building
  - Scale-specific prompting

**Test Scripts:**
- `test_single_llm_call.py` - Basic validation
- `test_focused_llm.py` - Multi-step test
- `test_one_journey.py` - Full journey test
- `generate_llm_cohort.py` - Batch generation
- `estimate_llm_costs.py` - Cost calculator
- `quick_llm_test.py` - Rapid validation

**Configuration:**
- `.env` - API key storage (gitignored)
- Updated `.gitignore` - Protects `.env`

### Files Modified

**Journey Generator:**
- `core/generators/journey_generator.py`
  - Added `use_real_llm` parameter
  - Added `llm_model` parameter
  - Added `llm_generator` initialization
  - Modified `_generate_ssr_responses()` with LLM integration
  - Fallback logic for API errors

**Dependencies:**
- `requirements.txt`
  - Added `anthropic>=0.64.0`

### Usage Examples

**Basic Usage:**
```python
from core.generators.llm_response_generator import LLMResponseGenerator

generator = LLMResponseGenerator()

response = generator.generate_response(
    persona={"age": 46, "tech_comfort": 0.49, "medium": "ceramics"},
    stimulus="Starting knowledge capture session",
    scale_id="engagement",
    phase="discovery",
    emotional_state="curious_cautious",
    engagement_score=0.65
)

# Output: "I'm intrigued by the knowledge sovereignty angle..."
```

**With Journey Generator:**
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

# Each step includes authentic LLM responses converted to SSR distributions
for step in journey.steps:
    if hasattr(step, 'ssr_responses'):
        print(step.ssr_responses['engagement']['text_response'])
        print(step.ssr_responses['engagement']['pmf'])
```

**Cost Estimation:**
```bash
PYTHONPATH=. python estimate_llm_costs.py

# Output:
# Single journey: $0.12
# 10 journeys: $1.20
# 500 journeys: $60.00
```

## Alternatives Considered

### Alternative 1: OpenAI GPT-4

**Approach:** Use OpenAI instead of Anthropic

**Rejected because:**
- Claude Sonnet 4.5 is latest/most capable model
- Anthropic's extended context window better for personas
- Similar pricing but Claude excels at following persona instructions
- Anthropic API simpler for our use case
- Can add OpenAI as alternative provider later

### Alternative 2: Local LLM (Llama, Mistral)

**Approach:** Run open-source LLM locally

**Rejected because:**
- Quality significantly lower for persona roleplay
- Requires GPU infrastructure
- Slower generation (no API parallelization)
- Maintenance burden
- Cost savings minimal for typical usage
- Better as future optimization, not initial implementation

### Alternative 3: Fine-tuned Model

**Approach:** Fine-tune model on persona response examples

**Rejected because:**
- Requires large training dataset (don't have yet)
- Expensive to train and maintain
- Off-the-shelf Claude Sonnet 4.5 already excellent
- Premature optimization
- Can consider after validating approach

### Alternative 4: Prompt Caching

**Approach:** Cache system prompts to reduce costs

**Considered for future:**
- Anthropic supports prompt caching
- Could reduce costs by 90% for repeated system prompts
- Good optimization for batch generation
- Implement in Phase 2

## Related Decisions

- [ADR-0006: SSR Integration](0006-semantic-similarity-rating-integration.md) - Real LLM fulfills "Future Enhancements: Real LLM Integration"
- [ADR-0004: Synthetic User Framework](0004-synthetic-user-framework-integration.md) - Enhanced with authentic persona voices
- [ADR-0005: E2E Testing Framework](0005-e2e-testing-framework-persona-based.md) - Can use real LLM for test data validation

## References

- **Claude Sonnet 4.5**: Latest Anthropic model (claude-sonnet-4-5-20250929)
- **Anthropic API**: https://docs.anthropic.com/
- **Pricing**: $3/MTok input, $15/MTok output (as of 2025-01)
- **Documentation**: `core/generators/llm_response_generator.py`
- **Example Scripts**: `test_single_llm_call.py`, `estimate_llm_costs.py`

## Future Enhancements

### Phase 2 (Optional)

1. **Prompt Caching**
   - Cache system prompts (persona context)
   - Reduce costs by 90%
   - Good for batch generation

2. **Parallel API Calls**
   - Generate multiple scales simultaneously
   - 4x faster generation
   - Requires careful rate limit handling

3. **Multi-Provider Support**
   - Add OpenAI GPT-4 as alternative
   - Add local LLM option
   - Provider selection per use case

4. **Response Caching**
   - Cache common persona/stimulus combinations
   - Avoid duplicate API calls
   - Significant cost savings for repeated generation

5. **Streaming Responses**
   - Stream LLM output for faster perceived performance
   - Progress indicators for batch generation
   - Better UX for interactive use

6. **Cost Optimization**
   - Hybrid: Real LLM for 10%, simulated for 90%
   - Selective generation by persona importance
   - Budget controls and limits

---

**Last Updated:** 2025-10-15
**Maintainer:** Stephen Szermer
