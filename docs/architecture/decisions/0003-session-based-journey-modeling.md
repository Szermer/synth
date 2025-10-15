# ADR-0003: Session-Based Journey Modeling

## Status
Accepted

## Context
The original Stage Zero implementation used **time-based journeys** (10 weekly sessions with fixed timing). Private Language, our first new domain, requires **session-based journeys** where:
- Users capture knowledge at irregular intervals (not weekly)
- Session count varies by user (some record daily, others monthly)
- Journey progression depends on behavior, not calendar
- Emotional states evolve per-session, not per-week

We needed a journey model flexible enough to support both patterns and future variations.

## Decision
Implement **three journey types** with a unified model:

### 1. Journey Types
```python
class JourneyType(Enum):
    TIME_BASED = "time_based"        # Fixed intervals (e.g., weekly)
    SESSION_BASED = "session_based"  # Variable capture sessions
    MILESTONE_BASED = "milestone_based"  # Achievement-triggered
```

### 2. Journey Architecture
```python
@dataclass
class Journey:
    id: str
    user_id: str
    persona_type: str
    journey_type: JourneyType
    phases: List[JourneyPhase]
    steps: List[JourneyStep]
    overall_completion: float
```

**Key Design Choices:**
- Journey contains multiple `phases` (discovery, onboarding, etc.)
- Each phase contains multiple `steps` (individual sessions/weeks)
- Steps track completion status, emotional state, data collected
- Overall completion calculated from completed steps

### 3. Journey Generation Strategies

#### Time-Based (Stage Zero Pattern)
```python
def _generate_time_based_steps(persona, journey):
    current_time = journey.started_at
    for phase in journey.phases:
        for week in range(num_weeks_in_phase):
            step = create_step(phase, current_time, persona)
            steps.append(step)
            current_time += timedelta(days=7)  # Fixed 7-day interval
```

**Characteristics:**
- ✅ Predictable timing (weekly, daily, etc.)
- ✅ Easy to model churn (missed weeks)
- ✅ Good for structured programs

#### Session-Based (Private Language Pattern)
```python
def _generate_session_based_steps(persona, journey):
    current_time = journey.started_at
    total_sessions = random.randint(5, 20)  # Variable count

    for session_num in range(total_sessions):
        step = create_step(phase, current_time, persona)
        steps.append(step)
        # Variable intervals: 1-14 days
        current_time += timedelta(days=random.randint(1, 14))
```

**Characteristics:**
- ✅ Realistic usage patterns (irregular activity)
- ✅ Models natural engagement variance
- ✅ Good for self-paced products

#### Milestone-Based (Future Pattern)
```python
def _generate_milestone_based_steps(persona, journey):
    for phase in journey.phases:
        milestone_reached = False
        while not milestone_reached:
            step = create_step(phase, current_time, persona)
            steps.append(step)
            # Progress to next phase when milestone met
            milestone_reached = check_milestone(step, phase)
```

**Characteristics:**
- ✅ Achievement-driven progression
- ✅ Natural for gamified products
- ✅ Good for skill-based journeys

### 4. Emotional State Modeling

**Per-Phase Emotions:**
```yaml
# emotional_states.yaml
emotional_progressions:
  studio_practitioner:
    discovery:
      - "skeptical"
      - "curious"
    onboarding:
      - "uncertain"
      - "confident"
    active_use:
      - "engaged"
      - "productive"
```

**Step-Level Assignment:**
```python
def _create_step(phase, persona):
    # Get emotions for this persona + phase combination
    persona_emotions = emotional_states.get(persona.persona_type, {})
    phase_emotions = persona_emotions.get(phase.name, ["neutral"])

    # Pick random emotion from phase-appropriate list
    emotional_state = random.choice(phase_emotions)
```

## Consequences

### Positive ✅
- **Flexible**: Supports diverse product patterns
- **Realistic**: Models real user behavior accurately
- **Extensible**: Easy to add new journey types
- **Persona-Aware**: Emotional states match persona + phase
- **Testable**: Can validate journey progression logic

### Negative ⚠️
- **Complexity**: Three generation strategies to maintain
- **Configuration**: More YAML to define per project
- **Validation**: Harder to validate irregular patterns

### Private Language Impact

**Before (Time-Based Only):**
- ❌ Couldn't model variable capture frequency
- ❌ Weekly intervals too rigid
- ❌ Missed realistic engagement patterns

**After (Session-Based):**
- ✅ Users capture 5-20 sessions over variable timeframes
- ✅ Session intervals: 1-14 days (realistic)
- ✅ Completion tied to behavior, not calendar
- ✅ Emotional progression per session

## Implementation Details

### Journey Phase Configuration
```yaml
# projects/private_language/journey_phases.yaml
phases:
  - name: "discovery"
    order: 0
    duration_estimate: "1-3 sessions"  # Not time-based!
    objectives:
      - "understand_value_proposition"
      - "first_capture_attempt"
```

### Session Generation
```python
# For Private Language: 5-20 sessions total
total_sessions = random.randint(5, 20)

# Distribute across phases (3-10 per phase)
for session_num in range(total_sessions):
    phase_idx = min(session_num // 3, len(phases) - 1)
    phase = phases[phase_idx]

    # Create session with realistic timing
    interval_days = random.randint(1, 14)
    current_time += timedelta(days=interval_days)
```

### Completion Tracking
```python
def _update_completion(self):
    if not self.steps:
        self.overall_completion = 0.0
        return

    completed_steps = sum(
        1 for step in self.steps
        if step.completion_status == CompletionStatus.COMPLETED
    )

    # Completion = completed / expected steps
    total_possible = len(self.phases) * 10  # ~10 steps per phase
    self.overall_completion = min(completed_steps / total_possible, 1.0)
```

## Testing Strategy

### Scenario Tests
```python
def test_session_based_journey():
    """Test session-based journey generation"""
    generator = JourneyGenerator(
        journey_type=JourneyType.SESSION_BASED,
        phases=phases,
        emotional_states=emotions
    )

    journey = generator.generate(persona, user_id)

    # Sessions should be irregular
    assert 5 <= len(journey.steps) <= 20

    # Intervals should vary
    intervals = calculate_intervals(journey.steps)
    assert min(intervals) >= 1
    assert max(intervals) <= 14
```

### Validation
```bash
# Generate and inspect
python cli.py generate private_language --count 10

# Analyze session patterns
python analyze_scenarios.py
```

## Real-World Example

**Sarah (Studio Practitioner) Journey:**
```
Day 1:  Discovery - First capture (skeptical → curious)
Day 3:  Discovery - Second session (intrigued)
Day 10: Onboarding - Knowledge atoms generated (surprised)
Day 12: Onboarding - Gap detection review (confident)
Day 25: Active Use - Weekly capture habit forming (engaged)
Day 28: Active Use - Teaching materials export (productive)
...
```

**Notice:**
- Variable intervals (2 days, 7 days, 15 days, 3 days)
- Not tied to calendar weeks
- Progression based on behavior
- Emotional evolution through phases

## Related Documents
- [ADR-0001: Multi-Domain Architecture Refactor](0001-multi-domain-architecture-refactor.md)
- [ADR-0002: YAML Configuration Schema](0002-yaml-configuration-schema.md)
- [Private Language Journey Config](../../../projects/private_language/journey_phases.yaml)

## Future Enhancements
- [ ] Hybrid journey types (time + milestone)
- [ ] Configurable interval distributions
- [ ] A/B testing different journey patterns
- [ ] Journey visualization tools

## Date
2025-10-07

## Authors
- Stephen Szermer (with Claude Code assistance)
